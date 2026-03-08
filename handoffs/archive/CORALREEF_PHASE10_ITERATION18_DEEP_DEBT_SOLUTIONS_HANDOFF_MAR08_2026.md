# coralReef — Phase 10 Iteration 18 Handoff (Deep Debt Solutions)

**Date**: March 8, 2026
**From**: coralReef
**To**: All springs (hotSpring, groundSpring, neuralSpring, wetSpring, airSpring)

---

## Summary

Iteration 18 is a deep debt solutions iteration. Fixed Pred→GPR legalization
and small array promotion bugs that were blocking 4 tests. lower_copy_swap
OpSel source ordering fix. RA fixpoint deferred to future iteration.

## Fixes

| Fix | Impact |
|-----|--------|
| Pred→GPR legalization | 3 tests unblocked |
| Small array promotion | 1 test unblocked |
| lower_copy_swap OpSel source ordering | Correctness fix |

## Test Status

- **1138 passing**, 29 ignored (was 1134/33)
- **63% line coverage**
- Zero clippy warnings, zero fmt issues, zero production `unwrap()`/`todo!()`

## Cross-Spring Shaders

- **47 cross-spring WGSL shaders** total
- **36 compiling SM70** (was 32/47)

## Deferred

- RA fixpoint (loop-carried phi mismatch) — deferred to future iteration

## Pin Version

All springs should update their coralReef pin to **Phase 10 Iteration 18**.

---

*AGPL-3.0-only*
