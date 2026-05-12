# loamSpine v0.9.16 — BTSP Phase 3 FULL: ChaCha20-Poly1305 AEAD

**Date**: May 2, 2026
**From**: loamSpine v0.9.16
**Responding to**: primalSpring `CRYPTO_CONSUMPTION_HIERARCHY.md` — loamSpine reclassified from "null-by-design" to "ionic-bond-blocking"

---

## Summary

loamSpine is now the **10th of 13 NUCLEUS primals** with FULL BTSP Phase 3
implementation. The `btsp.negotiate` handler has been evolved from null
cipher to ChaCha20-Poly1305 AEAD, resolving the ionic-bond-blocking
classification. loamSpine can now participate in ionic and weak bond
compositions (healthSpring dual-tower enclave, cross-family data
federation, anchoring pipeline transport integrity).

## What Changed

### Key Acquisition — Pattern B (Tower-Provided)

loamSpine receives the handshake key from `BearDog`'s `btsp.session.verify`
response (`session_key` field, base64, 32 bytes). Previously this field was
discarded. Ed25519 delegation stays with BearDog — only symmetric transport
crypto (HKDF expansion + ChaCha20-Poly1305 AEAD) runs locally.

### `btsp/phase3.rs` — New Module

- `SessionKeys::derive()` — HKDF-SHA256 expansion from handshake key + nonces
- Mirrored client/server keys (client encrypt = server decrypt)
- `encrypt()` / `decrypt()` — ChaCha20-Poly1305 AEAD, 12-byte random nonce
- `generate_nonce()` — 32-byte cryptographic random for negotiate exchange
- `read_encrypted_frame()` / `write_encrypted_frame()` — async I/O
- Keys zeroed on drop via `zeroize`

### Wire Format

```
Client → Server: btsp.negotiate { session_id, preferred_cipher, client_nonce }
Server → Client: { cipher: "chacha20-poly1305", server_nonce: "<base64 32B>" }
Both derive: HKDF-SHA256(handshake_key, client_nonce || server_nonce)
Post-negotiate: [4B len BE u32][12B nonce][ciphertext + 16B Poly1305 tag]
```

### Graceful Degradation

When no handshake key is available (unauthenticated covalent same-family
bonds), `btsp.negotiate` returns `cipher: "null"` — no breakage for
existing compositions. `BtspEnforcer` `min_cipher_for_bond` is satisfied:

| Bond Type | Min Cipher | loamSpine |
|-----------|-----------|-----------|
| Covalent | Null | **PASS** (null fallback) |
| Metallic | HmacPlain | **PASS** (via Tower) |
| Ionic | ChaCha20Poly1305 | **PASS** (Phase 3 FULL) |
| Weak | ChaCha20Poly1305 | **PASS** (Phase 3 FULL) |

### Dependencies Added

All RustCrypto pure Rust, pass `cargo deny check`, match primalSpring versions:

| Crate | Version | Purpose |
|-------|---------|---------|
| `chacha20poly1305` | 0.10 | AEAD encrypt/decrypt |
| `hkdf` | 0.13.0 | Session key derivation |
| `sha2` | 0.11.0 | HKDF hash function |
| `zeroize` | 1.8.2 | Key material zeroing |
| `getrandom` | 0.4.2 | Nonce generation |

### Architectural Boundary (Preserved)

| Crypto Layer | Where | |
|---|---|---|
| Asymmetric (Ed25519) | BearDog (Tower) | Unchanged |
| Symmetric transport (HKDF + ChaCha20) | Local (in-process) | **NEW** |
| Integrity (Blake3) | Local (in-process) | Unchanged |

---

## What This Unblocks

- **healthSpring dual-tower ionic-fenced enclave**: loamSpine in Nest
  atomic can sustain encrypted transport behind the ionic fence
- **Cross-family data federation**: All Nest primals now handle AEAD
- **Anchoring pipeline**: Signed Merkle root → encrypted loamSpine
  certificate → sweetGrass attribution — no plaintext gap
- **`BtspEnforcer`**: `min_cipher_for_bond(BondType::Ionic)` — loamSpine
  qualifies

## Deep Debt Audit (CLEAN)

10-dimension audit performed same session — zero findings:

| Dimension | Status |
|---|---|
| TODO/FIXME/HACK | Zero |
| Mocks in production | Zero (all cfg-gated) |
| Hardcoded primal names | Zero in production |
| Large files (>800L prod) | Zero (max 605L) |
| Unsafe code | Forbidden |
| `Result<_, String>` | Zero in production |
| `#[allow]` audit | 2 justified (feature-conditional) |
| Dead code | 2 justified |
| Dependencies | All RustCrypto pure Rust, deny clean |
| Security advisories | Zero |

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,486 (all concurrent, zero flaky) |
| JSON-RPC methods | 38 |
| Source files | 180+ `.rs` |
| Max .rs file | 807L (test), 605L (production) |
| Clippy | Clean (pedantic + nursery) |
| cargo deny | Clean (0 advisories) |
| Unsafe | Forbidden |
| New deps | 5 (all RustCrypto pure Rust) |

---

*Ref: `LOAMSPINE_V0916_BTSP_PHASE3_HANDOFF_MAY02_2026.md` for prior null-cipher handoff*
*Ref: `wateringHole/CRYPTO_CONSUMPTION_HIERARCHY.md` for the ecosystem standard*
