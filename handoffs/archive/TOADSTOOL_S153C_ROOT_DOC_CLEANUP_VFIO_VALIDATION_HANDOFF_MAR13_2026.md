# toadStool S153c — Root Doc Cleanup + VFIO Validation Absorption

**Date**: March 13, 2026
**From**: toadStool (S153c)
**To**: All primals (barraCuda, coralReef, hotSpring)

---

## Summary

Root documentation cleanup and final VFIO validation absorption from hotSpring.
All stale date stamps, metrics, and gap statuses updated across 7 root documents.
Zero production code changes — documentation-only session.

## Documentation Updates

| Document | Change |
|----------|--------|
| `DEBT.md` | S150 → S153. D-COV: 121K → ~150K lines, 19,567 → 20,262 tests. D-KEYRING marked RESOLVED S152 (OS keyring implemented). |
| `EVOLUTION_TRACKER.md` | S150 → S153. Quality gates: 20,015 → 20,262 tests. Coverage: 121K → ~150K lines. Added S151/S152/S153 session entries. |
| `STATUS.md` | S152 → S153. Added S153 session entry with IPC-first reconciliation, `compute.hardware.vfio_devices`, `ecoprimals-mode` CLI, hotSpring VFIO absorption. |
| `NEXT_STEPS.md` | S152 → S153. Updated banner with IPC-first pipeline and VFIO 6/7 validation status. |
| `specs/README.md` | S150 → S153. Test count: 19,567 → 20,262. JSON-RPC: 95+ → 96+. |
| `SPRING_ABSORPTION_TRACKER.md` | S152 → S153. Added S153 absorption note with hotSpring VFIO validation, coralReef USERD_TARGET status, spring pins. |

## Debris Audit Results

**Rust codebase**: Zero TODO/FIXME/HACK markers in production code. All dated comments are legitimate evolution history (not stale debt).

**Root directory**: Clean — only markdown, Cargo, and dotfiles. No stray scripts or loose files.

**ecoPrimals root**: Clean — no loose files. `fossil/` directory already contains archived toadStool material.

**wateringHole handoffs**: 17 active toadStool handoffs (S137–S153b), 24 archived. No false positives identified.

## Cross-Primal Status

| Primal | Status |
|--------|--------|
| **toadStool** | S153 — All 12 toadStool-owned sovereign compute gaps resolved. Infrastructure ready. 96+ JSON-RPC methods. 20,262 tests. |
| **coralReef** | Iteration 43 — PFIFO channel init. 6/7 VFIO tests pass on Titan V. Blocked on USERD_TARGET encoding fix (DW0 bits [3:2]). |
| **barraCuda** | v0.35 IPC-first — Zero compile-time primal deps. Depends on toadStool `compute.hardware.vfio_devices` for VFIO detection. |
| **hotSpring** | v0.6.31 — 848 tests. Titan V VFIO validation complete. CUDA-as-oracle debugging strategy active. |

## Remaining Cross-Primal Gap

The sole blocker for end-to-end sovereign GPU dispatch:

**coralReef USERD_TARGET encoding** — Runlist entry DW0 bits [3:2] currently set to 0 (VRAM) but must be 2 (SYS_MEM_COHERENT) for system memory USERD. One-register fix in `coralReef/crates/coral-driver/src/vfio/channel.rs`. Once fixed, dispatch completes and the entire sovereign pipeline is functional.

---

*toadStool S153c — documentation complete, infrastructure ready, awaiting coralReef one-register fix*
