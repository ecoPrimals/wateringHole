<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Iteration 89: BTSP Phase 3, Kepler Hardening, Deep Audit

**Date**: May 2, 2026
**From**: coralReef team
**To**: primalSpring, hotSpring, all downstream springs

---

## Summary

BTSP Phase 3 convergence (9th of 13 primals), Kepler SCHED_ERROR resolution from hotSpring downstream, and comprehensive deep audit confirmation.

## BTSP Phase 3 — Full AEAD Upgrade

coralReef now implements `btsp.negotiate` with **real ChaCha20-Poly1305 AEAD**:

- **Key extraction**: `create_btsp_session` extracts `handshake_key` from BearDog's `btsp.session.create` response (per BTSP_PROTOCOL_STANDARD v1.0)
- **HKDF derivation**: `SessionKeys::derive(handshake_key, client_nonce || server_nonce)` with info strings `btsp-session-v1-c2s`/`btsp-session-v1-s2c`
- **Cipher response**: Returns `"chacha20-poly1305"` when handshake key available; graceful `"null"` fallback when absent
- **SessionKeys**: `Zeroize + ZeroizeOnDrop`, ChaCha20-Poly1305 encrypt/decrypt with random 12-byte nonces
- **Transport API**: `take_negotiated_keys(session_id)` for the encrypted frame loop
- **Session registry**: `HashMap<String, SessionEntry>` with per-session handshake key
- **Validation**: base64-decoded client_nonce (>= 12 bytes), session_id against registry
- **Capability**: `btsp.negotiate` advertised in `capability.list`
- **Module split**: `btsp.rs` (Phase 2 guard, 461L) + `btsp_negotiate.rs` (Phase 3, 619L)

primalSpring detects the cipher upgrade automatically. Null cipher fallback means no breakage for compositions where BearDog hasn't exposed key material yet.

## Kepler SCHED_ERROR Resolution (hotSpring downstream)

Two commits from hotSpring resolved the Kepler CONTEXT_RELOAD_TIMEOUT:

1. **RAMFC missing fields**: Added DW 0x3C (`DMA_LIMIT_REF`) and 0x44 (`PB_DMA_SUBROUTINE`) — without these, PBDMA rejects context during reload
2. **Runlist polling fix**: Replaced GV100-only `RUNLIST_PENDING` (0x2284) with Kepler-correct PFIFO_INTR bit 30 interrupt-based completion
3. **Panic elimination**: `expect()` → `Result` propagation for Kepler guard invariant

## Deep Audit Confirmation

| Dimension | Status |
|---|---|
| `Result<_, String>` | Zero in production |
| `TODO/FIXME/HACK` | Zero in .rs code |
| Bare `#[allow]` without reason | Zero (7 fixed this iteration) |
| Files >1000L | Zero |
| `.unwrap()` in production | Zero |
| `anyhow` | Not used |
| C dependencies | Zero in default builds |
| Unsafe code | Confined to `coral-driver` kernel boundary, all `// SAFETY:` documented |
| Mocks in production | Zero (all test-isolated) |
| Hardcoded paths | All env-var-backed with sane defaults |

## Test Results

- 4632 passing, 0 failures, 160 ignored (hardware-gated)
- 21 BTSP Phase 3 crypto tests (negotiate, HKDF, encrypt/decrypt, tamper, wrong-key)
- Zero clippy warnings (pedantic + nursery)

## Downstream Impact

- **primalSpring**: Auto-detects `btsp.negotiate` in capability.list
- **hotSpring**: Kepler PFIFO pipeline now functional (SCHED_ERROR resolved)
- **compositions**: No behavioral change (NULL cipher = same as before)

## Dependencies Added

- `hkdf` 0.12 (HKDF-SHA256 key derivation)
- `sha2` 0.10 (SHA-256 for HKDF)
- `chacha20poly1305` 0.10 (AEAD encrypt/decrypt)
- `getrandom` 0.3 (cryptographic random nonces)
- `zeroize` 1 (secure key erasure)
- `rand` 0.9 (server nonce generation)
- `base64` 0.22 (nonce encoding/decoding)

All pure Rust (RustCrypto ecosystem), no transitive C.
