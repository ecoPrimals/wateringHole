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

### 4. Cipher Selection Logic (with minimum enforcement)

```
if !has_session_key → CipherSuite::Null (no key material = can't encrypt)
if has_session_key  → max(client's preferred_cipher, bond_type minimum)
```

Bond-type minimum enforcement:
- `Covalent` → any cipher (including Null)
- `Metallic` → minimum HMAC-SHA256
- `Ionic` → minimum ChaCha20-Poly1305

Currently: session keys are never stored (BearDog's `btsp.session.verify` response
doesn't propagate them through our handshake pipeline yet). So all negotiations
return `"null"` — which is the correct, spec-compliant fallback.

### 5. Full Crypto Pipeline (`negotiate.rs`)

- `derive_session_keys`: HKDF-SHA256 key derivation (handshake_key + nonces → 64B split)
- `encrypt_frame`: ChaCha20-Poly1305 AEAD with frame counter nonce
- `decrypt_frame`: ChaCha20-Poly1305 decryption with authentication
- `cipher_strength`: Ordinal comparison for minimum enforcement

All exercised in tests — ready to activate on key propagation.

### 6. Tests (48 new since last handoff, 287 total)

Crypto pipeline: `derive_session_keys_deterministic`, `derive_session_keys_different_nonces`,
`encrypt_decrypt_roundtrip`, `decrypt_wrong_counter_fails`, `decrypt_wrong_key_fails`,
`decrypt_tampered_ciphertext_fails`, `select_cipher_enforces_minimum`, `cipher_strength_ordering`

Coverage expansion: `StatisticalProfiler` (rolling window, anomaly detection, thresholds),
`LayerTopologyValidator` (bypass detection, empty paths), `LocalLineageVerifier` (conservative deny),
`ThreatType/Severity` (serde roundtrip, ordering), JSON-RPC types (request/response/notification)

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo clippy --workspace --all-targets -- -D warnings` | CLEAN |
| `cargo fmt --all -- --check` | CLEAN |
| `cargo doc --workspace --no-deps -D warnings` | CLEAN |
| `cargo deny check` | CLEAN |
| `cargo test --workspace --lib --bins` | 287 pass |

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

- **39** source files, **9,540** total lines, max **672** lines/file
- **287** tests, 0 failures
- Pure Rust, `forbid(unsafe_code)`, Edition 2024
- `Cargo.lock` committed (reproducible builds)
- Crypto pipeline fully tested (key derivation + AEAD roundtrip)
- Bond-type minimum cipher enforcement operational
- Idiomatic: `.to_owned()` over `.to_string()`, `.into_owned()`, `mul_add`
