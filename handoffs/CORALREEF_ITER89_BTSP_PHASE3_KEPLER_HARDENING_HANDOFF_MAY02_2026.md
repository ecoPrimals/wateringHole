<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Iteration 89: BTSP Phase 3, Kepler Hardening, Deep Audit

**Date**: May 2, 2026
**From**: coralReef team
**To**: primalSpring, hotSpring, all downstream springs

---

## Summary

BTSP Phase 3 convergence (9th of 13 primals), Kepler SCHED_ERROR resolution from hotSpring downstream, and comprehensive deep audit confirmation.

## BTSP Phase 3 — `btsp.negotiate` Server Handler

coralReef now implements `btsp.negotiate` per the Phase 3 spec:

- **Session registry**: Tracks `session_id`s from Phase 2 BTSP authentications
- **Validation**: Rejects empty session_id, validates against live sessions, rejects empty client_nonce
- **Nonce generation**: 24-byte random server nonce (base64-encoded)
- **Cipher**: Returns `"null"` — real ChaCha20-Poly1305 requires BearDog `btsp.session.key_export`
- **Capability**: `btsp.negotiate` advertised in `capability.list`

primalSpring detects the upgrade automatically. NULL cipher fallback means no behavioral change for existing compositions.

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

- 4645+ passing, 0 failures, ~177 ignored (hardware-gated)
- Zero clippy warnings (pedantic + nursery)

## Downstream Impact

- **primalSpring**: Auto-detects `btsp.negotiate` in capability.list
- **hotSpring**: Kepler PFIFO pipeline now functional (SCHED_ERROR resolved)
- **compositions**: No behavioral change (NULL cipher = same as before)

## Dependencies Added

- `rand` 0.9 (nonce generation)
- `base64` 0.22 (nonce encoding)

Both pure Rust, no transitive C.
