# BearDog v0.9.0 — Wave 37: primalSpring Audit Resolution — Contract Signing, BTSP Relay Path, Encoding Docs

| Field | Value |
|-------|-------|
| Date | 2026-04-12 |
| From | BearDog v0.9.0 (primalSpring audit resolution session) |
| To | primalSpring, barraCuda, all downstream primals |
| License | AGPL-3.0-or-later |
| Supersedes | BEARDOG_V090_WAVE36_COMPOSITION_ELEVATION_HANDOFF_APR12_2026 |

---

## 1. What Happened

Resolved three gaps identified in the primalSpring downstream audit:
1. **IONIC-RUNTIME**: `crypto.sign_contract` + `crypto.verify_contract` implemented
2. **BTSP-BARRACUDA-WIRE**: `btsp.server.export_keys` completes the relay path
3. **LD-01**: `crypto.hash` base64 encoding requirement documented in wire contract

**All five quality gates pass clean.** 14,774+ tests, 0 failures.

---

## 2. `crypto.sign_contract` (IONIC-RUNTIME — RESOLVED)

New JSON-RPC method for programmatic cross-family trust establishment.

**Wire contract:**

```json
{
  "method": "crypto.sign_contract",
  "params": {
    "signer": "hotSpring",
    "terms": { "type": "gpu_lease", "provider": "family_a", "consumer": "family_b" },
    "context": "gpu_lease"
  }
}
→ {
  "terms_hash": "<SHA-256 hex of canonical JSON>",
  "signature": "<Ed25519 hex, 128 chars>",
  "public_key": "<Ed25519 hex, 64 chars>",
  "signed_at": "2026-04-12T..."
}
```

**Key properties:**
- Terms are serialized with **sorted keys** (canonical JSON) before hashing, so field order in the caller's payload does not affect the terms hash
- Signing key is derived deterministically from BearDog's runtime identity (`PRIMAL_NAME` + `NODE_ID`)
- Context label is optional metadata (not included in the hash)

**For other primals:** Call `crypto.sign_contract` to get your contract signed, then pass the `terms_hash`, `signature`, and `public_key` to the counterparty. They call `crypto.verify_contract` to confirm the signature is valid.

---

## 3. `crypto.verify_contract` (IONIC-RUNTIME — RESOLVED)

Companion verification endpoint:

```json
{
  "method": "crypto.verify_contract",
  "params": {
    "terms_hash": "<SHA-256 hex>",
    "signature": "<Ed25519 hex>",
    "public_key": "<Ed25519 hex>"
  }
}
→ { "valid": true } | { "valid": false, "error": "..." }
```

**Stateless:** Does not require the contract to be stored in BearDog — any party with the hash, signature, and public key can verify independently.

---

## 4. `btsp.server.export_keys` (BTSP-BARRACUDA-WIRE — RESOLVED)

Completes the BTSP relay path. After barraCuda calls `btsp.server.create_session` + `btsp.server.verify`, it calls `export_keys` to retrieve the session keys needed for post-handshake stream encryption.

**Wire contract:**

```json
{
  "method": "btsp.server.export_keys",
  "params": {
    "session_id": "<hex session ID from btsp.server.verify>",
    "caller_ephemeral_pub": "<base64 X25519 public key>"
  }
}
→ {
  "wrapped_keys": "<base64: nonce(12) || ChaCha20-Poly1305(encrypt_key || decrypt_key)>",
  "wrapper_ephemeral_pub": "<base64 X25519 public key>",
  "cipher": "chacha20_poly1305"
}
```

**Key wrapping scheme:**
1. BearDog generates a fresh X25519 ephemeral keypair
2. DH with caller's ephemeral pub → shared secret
3. HKDF(shared, salt="btsp-key-export-v1", info="wrap") → wrapping key
4. ChaCha20-Poly1305 encrypts `server_to_client_key(32) || client_to_server_key(32)`
5. Response = `nonce(12) || ciphertext(80)` as base64

**Session keys never appear as plaintext in JSON-RPC responses.**

**For barraCuda:** After receiving `wrapped_keys`, perform the reverse DH with your ephemeral secret + `wrapper_ephemeral_pub`, derive the wrapping key via the same HKDF, then decrypt to recover the two 32-byte session keys.

---

## 5. LD-01 Encoding Documentation (RESOLVED)

`crypto.hash` expects the `data` parameter as **standard Base64** (RFC 4648 §4). This is now documented in:

1. **Handler doc comments** — `handle_blake3_hash` in `crypto/hash.rs`
2. **Module-level docs** — `hash.rs` module header §Encoding Contract
3. **wateringHole `CAPABILITY_WIRE_STANDARD.md`** — New §Parameter Encoding (LD-01) table covering all BearDog crypto methods, their input/output encoding, and the BD-01 per-field encoding hints

**For primalSpring:** When calling `crypto.hash`, encode your raw bytes as Base64 first. If you pass raw UTF-8, the hash will be over the Base64 string bytes, not the original data.

---

## 6. Capability Surface Changes

| Capability | Version | Methods |
|------------|---------|---------|
| `ionic_bond` | **1.1** (was 1.0) | propose, accept, verify, revoke, list |
| `contract_signing` | **1.0** (NEW) | sign_contract, verify_contract |
| BTSP server | +1 method | create_session, verify, **export_keys**, negotiate, status |

New cost_estimates entries:
- `crypto.sign_contract`: cpu=low, latency_ms=1
- `crypto.verify_contract`: cpu=low, latency_ms=1

---

## 7. Quality Gate Results

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace --all-features -- -D warnings` | 0 warnings |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | 0 warnings |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| `cargo test --workspace` | 14,774+ passed, 0 failed |

---

## 8. primalSpring Audit Items — Resolution Status

| Audit Item | Status | Resolution |
|------------|--------|------------|
| IONIC-RUNTIME: `crypto.sign_contract` | **RESOLVED** | Full sign + verify + canonical JSON + 5 tests |
| BTSP-BARRACUDA-WIRE: relay path completion | **RESOLVED** | `btsp.server.export_keys` with wrapped key export |
| LD-01: `crypto.hash` encoding docs | **RESOLVED** | Wire contract docs in handler, module, and wateringHole |
| btsp.negotiate metadata inconsistency | **RESOLVED** (Wave 36) | Docs aligned to `btsp.server.*` |
| Ionic bond e2e lifecycle | **RESOLVED** (Wave 36) | Ed25519 re-verification + 4 lifecycle tests |
