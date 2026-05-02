# skunkBat v0.2.0-dev — BTSP Phase 3 Fully Wired (Encrypted Framing)

**Date**: May 2, 2026 (updated)
**From**: skunkBat team
**To**: primalSpring, BearDog, ecosystem
**Triggered by**: primalSpring Phase 56c + May 2 evolution audit

---

## Summary

BTSP Phase 3 is now fully wired end-to-end. The handshake key from Phase 2 is plumbed
into the `SessionRegistry`, `btsp.negotiate` derives directional session keys via
HKDF-SHA256, and the connection loop auto-upgrades from NDJSON to encrypted
`ChaCha20-Poly1305` framing (`[4B len][12B nonce][ct+tag]`). Full end-to-end test
exercises the complete NDJSON→negotiate→encrypted-frame-loop path.

When `FAMILY_SEED` is set, connections that complete BTSP handshake + negotiate will
encrypt all subsequent traffic. Falls back to authenticated NULL cipher when no seed.

---

## What Was Implemented

### 1. Session Registry (`negotiate.rs`)

- `SessionRegistry`: concurrent `Arc<RwLock<HashMap>>` storing session state
- Sessions inserted after successful Phase 2 handshake
- Tracks: `created_at`, `cipher`, `session_key`, `server_nonce`
- `CipherSuite` enum: `Null`, `HmacPlain`, `ChaCha20Poly1305`
- `BondType` enum with minimum cipher enforcement rules

### 2. Handshake Key Plumbing (`btsp.rs` → `mod.rs`)

- `perform_server_handshake` now returns `HandshakeResult { session_id, handshake_key }`
- `derive_handshake_key_from_env()`: `HKDF-SHA256(ikm=FAMILY_SEED, salt="btsp-v1", info="handshake")` → 32 bytes
- Key stored in `SessionRegistry` alongside session_id at Phase 2 completion
- Both TCP and UDS paths updated to pass handshake key

### 3. `btsp.negotiate` Method Handler

- Added to dispatch METHODS list (capabilities.list includes it)
- Routed in `server.rs` before general dispatch (intercepts at connection level)
- Validates `session_id` against registry, decodes `client_nonce` (base64)
- Generates 32-byte random `server_nonce` (base64-encoded in response)
- Selects cipher via `select_best_cipher` (ecosystem preference order)
- Returns `NegotiateOutcome` with both JSON response and derived `SessionKeys`

### 4. Encrypted Frame Loop (`server.rs`)

- `try_negotiate_upgrade` intercepts `btsp.negotiate` in NDJSON mode
- Sends negotiate response via NDJSON, then switches to frame mode
- `run_encrypted_frame_loop`: reads `[4B len][12B nonce][ct+tag]`, decrypts,
  dispatches JSON-RPC, encrypts response, writes encrypted frame
- Key directionality: server encrypts with s2c key, decrypts with c2s key

### 3. Crypto Dependencies (Pure Rust)

Added to workspace (all RustCrypto / pure Rust, pass `cargo deny`):
- `chacha20poly1305` 0.10
- `hkdf` 0.12
- `sha2` 0.10
- `rand` 0.8
- `hex` 0.4

### 5. Crypto Pipeline (`negotiate.rs`)

- `derive_session_keys`: HKDF-SHA256 with salt=`client_nonce||server_nonce`, directional info strings
- `encrypt_frame`: `ChaCha20-Poly1305` AEAD with random per-frame nonce → `nonce(12)||ct||tag(16)`
- `decrypt_frame`: Extracts nonce from first 12 bytes, authenticates + decrypts
- `select_best_cipher`: Ecosystem preference order (chacha20-poly1305 > hmac-plain > null)

### 6. Tests (303 total)

End-to-end: `test_btsp_negotiate_upgrade_to_encrypted` — exercises full NDJSON negotiate →
encrypted frame → dispatch → encrypted response → decrypt path.

Crypto pipeline: `derive_session_keys_deterministic`, `encrypt_decrypt_roundtrip`,
`decrypt_wrong_key_fails`, `decrypt_tampered_ciphertext_fails`, `directional_keys_encrypt_decrypt`

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo clippy --workspace --all-targets -- -D warnings` | CLEAN |
| `cargo fmt --all -- --check` | CLEAN |
| `cargo doc --workspace --no-deps -D warnings` | CLEAN |
| `cargo deny check` | CLEAN |
| `cargo test --workspace --lib --bins` | 303 pass |

---

## What Remains

1. **primalSpring validation**: `phase3_transport_full_roundtrip` integration test
   should pass automatically on next plasmidBin fetch.

2. **HSM integration path**: Currently key is derived from `FAMILY_SEED` env var.
   Future evolution: HSM-backed key derivation.

3. **Session TTL and cleanup**: `created_at` field exists but no periodic
   expiry task yet.

---

## Metrics

- **39** source files, **10,026** total lines, max **780** lines/file
- **303** tests, 0 failures
- Pure Rust, `forbid(unsafe_code)`, Edition 2024
- `Cargo.lock` committed (reproducible builds)
- Full end-to-end encrypted frame loop tested
- Aligned with BearDog reference: base64 nonces, `ciphers` array, directional keys
- Handshake key plumbed from Phase 2 into registry
- Connection auto-upgrades from NDJSON to encrypted framing post-negotiate
