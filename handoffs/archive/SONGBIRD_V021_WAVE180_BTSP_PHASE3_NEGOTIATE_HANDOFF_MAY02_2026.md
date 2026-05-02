# Songbird v0.2.1 — Wave 180: BTSP Phase 3 `btsp.negotiate` Server-Side

**Date**: May 2, 2026
**Primal**: Songbird (network orchestration)
**Source**: primalSpring Phase 56 audit — BTSP Phase 3 evolution target

## Summary

Implemented the server-side `btsp.negotiate` JSON-RPC handler to support BTSP Phase 3 encrypted framing (ChaCha20-Poly1305). After a successful Phase 1 handshake, primalSpring sends `btsp.negotiate` as the first method call. Songbird now handles this, derives session keys, and switches to encrypted framing for all subsequent traffic.

## What Was Implemented

### New Module: `songbird-orchestrator/src/ipc/btsp_phase3.rs`

- **`SessionKeys`** struct with directional encryption (server encrypts with s2c, decrypts with c2s)
  - `derive(handshake_key, client_nonce, server_nonce, is_client)` — HKDF-SHA256 with `btsp-session-v1-c2s`/`btsp-session-v1-s2c` info strings
  - `encrypt(plaintext)` — returns `[12B random nonce][ciphertext + Poly1305 tag]`
  - `decrypt(frame)` — verifies and decrypts
- **`NegotiateParams`** / **`NegotiateResult`** wire types
- **`handle_negotiate()`** — parses request, validates cipher support, exports handshake key from BearDog via `btsp.server.export_keys`, generates server nonce, derives keys, returns result + keys. Graceful NULL fallback on any failure.
- **`read_encrypted_frame()`** / **`write_encrypted_frame()`** — length-prefixed frame I/O (16 MiB max)

### SecurityRpcClient Extension: `btsp_export_keys()`

New method on `SecurityRpcClient` calling `btsp.server.export_keys` with `session_id`, returning the base64-decoded 32-byte handshake key.

### Connection Wiring

Both IPC paths evolved to handle Phase 3:

1. **Pure Rust UDS server** (`connection.rs`): `handle_ndjson_session` intercepts `btsp.negotiate` inline, processes negotiation, sends NDJSON response, then transitions to `handle_encrypted_session` (encrypted frame loop).
2. **bin_interface server** (`server.rs`): `handle_json_rpc_lines` intercepts `btsp.negotiate`, transitions to `handle_encrypted_json_rpc`.

### Protocol Flow (Server Perspective)

```
1. Client sends NDJSON: {"method":"btsp.negotiate","params":{"session_id":"...","ciphers":["chacha20-poly1305"],"client_nonce":"<base64>"}}
2. Server calls BearDog: btsp.server.export_keys → handshake_key
3. Server generates 32-byte server_nonce
4. Server derives SessionKeys via HKDF-SHA256
5. Server responds NDJSON: {"result":{"cipher":"chacha20-poly1305","server_nonce":"<base64>"}}
6. All subsequent frames: [4B len BE u32][12B nonce][ciphertext + Poly1305 tag]
```

## Dependencies Added

- `chacha20poly1305 = "0.10"` (RustCrypto AEAD)
- `hkdf = "0.12"` (HKDF key derivation)

Already present: `sha2 = "0.10"`, `getrandom`, `base64`

## Tests (19 new)

- SessionKeys: directional key derivation, deterministic, different nonces produce different keys
- Encrypt/decrypt: bidirectional round-trip, empty plaintext, tamper rejection, cross-key rejection, unique nonces per encryption
- Wire types: NegotiateParams/NegotiateResult serde
- Frame I/O: write/read round-trip, oversized frame rejection
- Full session: multi-message encrypted round-trip

## Quality Gates

- `cargo fmt`: PASS
- `cargo clippy -D warnings`: PASS (0 warnings)
- `cargo test --lib`: **7,803 passing** / 0 failures
- `forbid(unsafe_code)`: maintained

## Upstream Context

This resolves the "BTSP Phase 3" item from the primalSpring Phase 56 audit for Songbird. The implementation aligns with primalSpring's client-side (`ecoPrimal/src/ipc/btsp_handshake.rs` `negotiate_phase3()`) and petalTongue's reference server (`crates/petal-tongue-ipc/src/btsp/json_line.rs`).

GAP-06 (Squirrel `discovery.register` naming) was already resolved by Squirrel in their Apr 29 session — no Songbird action needed.
