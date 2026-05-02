# skunkBat v0.2.0-dev — BTSP Phase 3 `btsp.negotiate` Server Handler

**Date**: May 2, 2026
**From**: skunkBat team
**To**: primalSpring, BearDog, ecosystem
**Triggered by**: primalSpring Phase 3 downstream audit

---

## Summary

Implemented `btsp.negotiate` JSON-RPC server handler per BTSP Protocol Standard.
primalSpring can now detect Phase 3 capability when connecting to skunkBat.
Currently returns `{"cipher":"null"}` (graceful fallback) — full ChaCha20-Poly1305
encrypted framing will activate once BearDog propagates session key material.

---

## What Was Implemented

### 1. Session Registry (`negotiate.rs`)

- `SessionRegistry`: concurrent `Arc<RwLock<HashMap>>` storing session state
- Sessions inserted after successful Phase 2 handshake
- Tracks: `created_at`, `cipher`, `session_key`, `server_nonce`
- `CipherSuite` enum: `Null`, `HmacPlain`, `ChaCha20Poly1305`
- `BondType` enum with minimum cipher enforcement rules

### 2. `btsp.negotiate` Method Handler

- Added to dispatch METHODS list (capabilities.list includes it)
- Routed in `server.rs` before general dispatch (intercepts at connection level)
- Validates `session_id` against registry
- Generates 12-byte random `server_nonce` (hex-encoded in response)
- Selects cipher based on: request + bond_type minimum + key availability
- Returns `{"cipher": "<selected>", "server_nonce": "<hex>"}`

### 3. Crypto Dependencies (Pure Rust)

Added to workspace (all RustCrypto / pure Rust, pass `cargo deny`):
- `chacha20poly1305` 0.10
- `hkdf` 0.12
- `sha2` 0.10
- `rand` 0.8
- `hex` 0.4

### 4. Cipher Selection Logic

```
if !has_session_key → CipherSuite::Null (no key material = can't encrypt)
if has_session_key  → honor client's preferred_cipher
```

Currently: session keys are never stored (BearDog's `btsp.session.verify` response
doesn't propagate them through our handshake pipeline yet). So all negotiations
return `"null"` — which is the correct, spec-compliant fallback.

### 5. Tests (14 new, 239 total)

- `cipher_suite_roundtrip`, `bond_type_minimum_cipher`, `bond_type_parsing`
- `session_registry_lifecycle`, `session_registry_with_key`
- `negotiate_missing_params`, `negotiate_empty_session_id`, `negotiate_unknown_session`
- `negotiate_null_fallback_no_key`, `negotiate_chacha_with_key`
- `select_cipher_no_key_always_null`, `select_cipher_with_key_honors_request`
- `test_btsp_negotiate_no_session`, `test_btsp_negotiate_with_session`

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo clippy --workspace --all-targets -- -D warnings` | CLEAN |
| `cargo fmt --all -- --check` | CLEAN |
| `cargo doc --workspace --no-deps` | CLEAN |
| `cargo deny check` | CLEAN |
| `cargo test --workspace --lib --bins` | 239 pass |

---

## What Remains for Full Phase 3

1. **Session key propagation**: When `btsp.server.verify` returns `session_key`,
   store it in the registry. The `select_cipher` logic will then automatically
   return `chacha20-poly1305` instead of `null`.

2. **Encrypted framing switch**: After negotiate response is sent, subsequent
   frames should use `[4B len][12B nonce][ciphertext + tag]` format. Requires
   refactoring `handle_connection` to support frame-mode I/O post-negotiate.

3. **primalSpring validation**: Once key propagation is in place, the
   `phase3_transport_full_roundtrip` integration test should pass automatically
   on next plasmidBin fetch.

---

## Metrics

- **39** source files, **8,852** total lines, max **672** lines/file
- **239** tests, 0 failures
- Pure Rust, `forbid(unsafe_code)`, Edition 2024
- `Cargo.lock` committed (reproducible builds)
