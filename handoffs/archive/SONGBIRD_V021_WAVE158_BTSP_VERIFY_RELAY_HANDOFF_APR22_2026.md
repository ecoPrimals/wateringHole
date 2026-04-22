# Songbird v0.2.1 Wave 158 — BTSP Step 3→4 Verification Relay

**Date**: April 22, 2026
**Primal**: Songbird v0.2.1
**Wave**: 158
**Trigger**: primalSpring Phase 45 audit — BTSP handshake fails at step 4

## Problem

primalSpring's guidestone completes BTSP steps 1-2 (ClientHello → ServerHello) with
Songbird after Wave 153/156 fixes. The handshake fails at step 4 — no
`HandshakeComplete` after `ChallengeResponse`. Root cause: **6 wire-protocol
mismatches** between Songbird's BTSP relay and BearDog's `btsp.server.*` methods.

## Root Causes Identified

### 1. `btsp_session_create` wrong params
- **Was**: `{ "family_seed_ref": "env:FAMILY_SEED", "client_ephemeral_pub": ..., "challenge": ... }`
- **BearDog expects**: `{ "family_seed": "<base64>" }` (`SessionCreateParams`)
- **Impact**: BearDog rejects with "missing field family_seed"

### 2. `btsp_session_create` wrong response parsing
- **Was**: parsed `session_id` + `handshake_key`
- **BearDog returns**: `session_token` + `server_ephemeral_pub` + `challenge` (`SessionCreateResponse`)
- **Impact**: "Missing session_id" error after create call

### 3. Songbird generated its own challenge
- Both handshake paths generated 32 random challenge bytes locally
- BearDog generates and stores its own challenge during `create_session`
- HMAC verification always fails because client computes HMAC over BearDog's
  challenge (from ServerHello) but BearDog verifies against its stored challenge

### 4. ServerHello missing `session_id`
- primalSpring's `ServerHello` struct requires `session_id: String` (non-optional)
- Songbird's `ServerHello` only had `version`, `server_ephemeral_pub`, `challenge`

### 5. `btsp_session_verify` wrong params
- **Was**: `{ "session_id": ..., "client_response": ..., "client_ephemeral_pub": ..., "server_ephemeral_pub": ..., "challenge": ... }`
- **BearDog expects**: `{ "session_token": ..., "client_ephemeral_pub": ..., "response": ..., "preferred_cipher": ... }` (`SessionVerifyParams`)
- **Impact**: BearDog rejects with "Invalid server.verify params"

### 6. `btsp_session_verify` wrong response parsing + missing `session_key`
- **Was**: expected `session_key: Option<Vec<u8>>`
- **BearDog returns**: `{ verified, session_id, cipher, error }` (`SessionVerifyResponse`)
- Session keys are separate via `btsp.server.export_keys`

## Fixes Applied

### `songbird-http-client/security_rpc_client/btsp.rs`
- `BtspSessionCreated`: `session_id` → `session_token`, `handshake_key` → `challenge`
- `BtspSessionVerified`: `session_key` → `session_id` + `cipher`
- `BtspNegotiation`: `allowed` → `accepted`
- `btsp_session_create`: sends `{ "family_seed": ... }`, parses `session_token` + `challenge`
- `btsp_session_verify`: sends `session_token`, `response`, `preferred_cipher`; parses `session_id` + `cipher`
- `btsp_negotiate`: calls `btsp.session.negotiate` (was `btsp.negotiate`), sends `session_token` + `cipher`

### `songbird-orchestrator/ipc/btsp.rs`
- `ServerHello`: added `session_id: String` field
- `BtspSession`: removed `session_key` (unused; keys via `export_keys`)
- `resolve_family_seed_b64()`: reads `FAMILY_SEED` from env, base64-encodes if needed
- Both `perform_server_handshake` and `perform_server_handshake_ndjson`:
  - Use BearDog's challenge (from create response) instead of local random
  - Include `session_id` in `ServerHello`
  - Pass correct verify params (`session_token`, `response`, `preferred_cipher`)
  - Use `session_id` + `cipher` from verify response
  - Removed separate `btsp_negotiate` call (verify includes cipher negotiation)
- `parse_cipher`: moved to `#[cfg(test)]` (no longer called in production)

## Verification

- `cargo check`: 0 errors, 0 warnings
- `cargo clippy --workspace --all-targets`: 0 warnings
- `cargo fmt --all --check`: clean
- `cargo test --workspace --lib`: 7,387 passed, 0 failed

## What Remains (BTSP Phase 3)

1. **E2E integration test**: Run Songbird + BearDog + primalSpring guidestone to
   confirm the 4-step NDJSON handshake completes end-to-end
2. **`btsp.server.export_keys`**: Implement call for ciphers that require stream
   encryption (ChaCha20-Poly1305)
3. **Encrypted framing**: Post-handshake stream encryption using exported session keys
4. **BTSP client path**: `btsp_client.rs` still uses `family_seed_ref` — needs same fix
