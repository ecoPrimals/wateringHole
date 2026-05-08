<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 94: JH-1 Primal-Native Identity and Ionic Token Infrastructure

**Date**: May 8, 2026
**Primal**: BearDog (crypto/security)
**Wave**: 94
**Scope**: JH-1 — `identity.create`, `auth.issue_ionic`, `auth.verify_ionic`, bearer extraction, real cryptographic verification in MethodGate

---

## Summary

JH-1 delivers primal-native identity and Ed25519-signed ionic capability tokens, replacing the JH-0 presence-only `bearer_token.is_some()` check with full cryptographic verification. This is the single biggest blocker for Step 2b (BTSP auth inside the tunnel).

## New Files

### `crates/beardog-tunnel/src/ionic_token.rs` (~250 LOC + tests)

Token core:

- `IonicTokenHeader` / `IonicTokenPayload` structs (serde-serializable)
- `issue_ionic_token(signing_key, issuer_did, subject, scopes, ttl)` — creates and signs a compact token
- `verify_ionic_token(token_str, verifying_key)` — decode, verify Ed25519 sig, check expiry
- `scope_covers_method(scopes, method)` — glob matching (`*`, `prefix.*`, exact)
- `TokenError` enum: `Malformed`, `InvalidSignature`, `Expired`, `UnsupportedFormat`

Wire format: `base64(header).base64(payload).base64(signature)` — three dot-separated standard-base64 segments. Signature over `base64(header).base64(payload)` ASCII bytes using Ed25519.

### `crates/beardog-tunnel/src/ionic_token_handlers.rs` (~200 LOC + tests)

Gate-dispatched JSON-RPC handlers:

- `handle_identity_create()` — ephemeral Ed25519 keypair + `did:key:z6Mk...` DID
- `handle_auth_issue_ionic(primal_name, node_id, params)` — issue signed token
- `handle_auth_verify_ionic(verifying_key, params)` — verify token, return claims

## Modified Files

### `crates/beardog-tunnel/src/method_gate.rs`

- `MethodGate` now stores `verifying_key: VerifyingKey`, `primal_name`, `node_id`
- `MethodGate::new()` / `from_env()` take `primal_name` and `node_id` params
- `check()` performs full verification pipeline: decode → Ed25519 sig → expiry → scope → populate `CallerContext.validated_claims`
- `CallerContext.validated_claims: Option<IonicTokenPayload>` added
- `handle_auth_check` includes `claims` field when validated
- `dispatch_auth_method` takes `params` arg, routes `identity.create`, `auth.issue_ionic`, `auth.verify_ionic`
- `PUBLIC_METHODS` includes `identity.create`, `auth.issue_ionic`, `auth.verify_ionic`

### `crates/beardog-tunnel/src/unix_socket_ipc/server.rs`

- `route_jsonrpc` extracts `_bearer_token` from `request.params` before gate check
- `CallerContext` passed as `&mut` through dispatch chain

### `crates/beardog-tunnel/src/unix_socket_ipc/connection_handlers.rs`

- All 4 handler functions use `mut caller` to support validated_claims population

### `crates/beardog-tunnel/src/tcp_ipc/server.rs`

- Bearer extraction in NDJSON and BTSP TCP paths
- `CallerContext` passed as `&mut`
- `MethodGate` initialized with primal identity

### `crates/beardog-tunnel/src/unix_socket_ipc/handlers/capabilities.rs`

- Auth capability v2.0: `["check", "mode", "peer_info", "issue_ionic", "verify_ionic"]`
- New identity capability v1.0: `["get", "create"]`
- Cost estimates, cleartext methods, discover_capabilities all updated

## Token Design Decisions

- **Asymmetric (Ed25519)** — not HMAC — so any primal can verify without shared secrets
- **Issuer key** — same `primal_signing::derive_primal_signing_key(name, node_id)` used for announcements/bonds/contracts
- **Issuer DID** — `did:key:z6Mk...` multicodec Ed25519 + base58btc
- **Scope model** — glob patterns: `*` (all), `crypto.*` (namespace), exact match. Empty scope = no access.
- **Default TTL** — 3600s, configurable per issuance
- **`jti`** — 16-byte random hex for future revocation (JH-3)
- **Bearer extraction** — `_bearer_token` field in JSON-RPC `params` object (biomeOS convention)

## Method Count

114 → 117 (+3: `identity.create`, `auth.issue_ionic`, `auth.verify_ionic`)

## Test Coverage

- 21 tests in `ionic_token` (roundtrip, sig, expiry, scope, malformed)
- 10 tests in `ionic_token_handlers` (identity create, issue/verify roundtrip, scope check, defaults)
- 34 tests in `method_gate` (real token verification, expired/insufficient scope, permissive vs enforced)
- 2192 total `beardog-tunnel` lib tests pass

## Deferred to Future Waves

- **JH-2**: Resource envelope fields (mem, cpu, method allowlist) in tokens — biomeOS/ToadStool
- **JH-3**: Token revocation list (the `jti` field is included for forward compatibility)
- **JH-4**: Token UX for non-CLI researchers (browser-based token request flow)
- **SO_PEERCRED extraction**: Blocked on Rust API stabilization
- **Permissive mode scope enforcement**: Scope mismatches logged but allowed (same pattern as JH-0)

## primalSpring Action Items

- Update `METHOD_GATE_STANDARD.md` with JH-1 token wire format spec
- Update `PRIMAL_GAPS.md` to mark BearDog JH-1 as RESOLVED
- Propagate ionic token design to other primals (JH-1 is now 1/13 across ecosystem)
