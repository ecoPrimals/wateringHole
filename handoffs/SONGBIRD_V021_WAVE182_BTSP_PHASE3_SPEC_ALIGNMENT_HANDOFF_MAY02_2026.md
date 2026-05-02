# Songbird v0.2.1 — Wave 182: BTSP Phase 3 Spec Alignment (primalSpring Audit)

**Date**: May 2, 2026  
**Primal**: Songbird  
**Wave**: 182  
**Trigger**: primalSpring downstream audit — BTSP Phase 3 spec gaps

---

## Summary

Aligned Songbird's BTSP Phase 3 `btsp.negotiate` server-side handler with the
`BTSP_PROTOCOL_STANDARD.md` and the primalSpring audit blurb. Wave 180 implemented
the core negotiate + encrypted framing; Wave 182 closes the spec gaps identified
by the audit.

## Changes

### `NegotiateParams` — dual-format acceptance

`btsp_phase3.rs` now accepts both wire formats:

- **primalSpring Phase 3**: `{ session_id, ciphers: [...], client_nonce }`
- **BTSP Protocol Standard**: `{ session_id, preferred_cipher, bond_type }`

When `ciphers` is empty/absent but `preferred_cipher` is present, it's promoted
into a single-element cipher list via `effective_ciphers()`.

### `bond_type` + BondingPolicy cipher floor enforcement

New `select_cipher()` function applies `BTSP_PROTOCOL_STANDARD.md` cipher floor
rules:

| Bond Type | Minimum Cipher | Behavior |
|-----------|---------------|----------|
| Covalent | `BTSP_NULL` | All ciphers allowed |
| Metallic | `BTSP_HMAC_PLAIN` | ChaCha20-Poly1305 preferred |
| Ionic / Weak / ZeroTrust | `BTSP_CHACHA20_POLY1305` | Encrypted only — null rejected |

### Server nonce alignment

Server nonce reduced from 32 bytes to 12 bytes, aligning with the primalSpring
audit spec and ecosystem convention. HKDF-SHA256 derivation remains correct at
any salt length.

### Underscore normalization

Both `chacha20-poly1305` (hyphen) and `chacha20_poly1305` (underscore) are
accepted as valid cipher identifiers.

## Files Modified

| File | Change |
|------|--------|
| `crates/songbird-orchestrator/src/ipc/btsp_phase3.rs` | `NegotiateParams` expanded, `select_cipher()` added, nonce size aligned, module doc updated |
| `REMAINING_WORK.md` | Wave 182 status |
| `CHANGELOG.md` | Wave 182 entry |
| `PRIMAL_REGISTRY.md` (wateringHole) | Songbird: Phase 2 → Phase 3, test count updated |

## Test Results

- 28 btsp_phase3 unit tests (10 new) — all pass
- 0 clippy warnings (`-D warnings`)
- Full workspace lib: 4740 passed, 1 pre-existing flaky failure, 20 ignored

## Ecosystem Impact

Songbird now accepts `btsp.negotiate` requests from any primal using either the
primalSpring Phase 3 format or the BTSP Protocol Standard format. The `bond_type`
field is used for cipher floor enforcement. No breaking changes.
