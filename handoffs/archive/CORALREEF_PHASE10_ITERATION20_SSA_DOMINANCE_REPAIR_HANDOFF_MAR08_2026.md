# coralReef — Phase 10 Iteration 20 Handoff (SSA Dominance Repair)

**Date**: March 8, 2026
**From**: coralReef
**To**: All springs (hotSpring, groundSpring, neuralSpring, wetSpring, airSpring)

---

## Summary

Iteration 20 fixes an SSA dominance violation in the compiler IR that was
the root cause of the sigmoid_f64 failure. Values defined inside one branch
arm but used on both paths to a merge block created a live-in to the entry
block — a pathological state. New `fix_entry_live_in()` pass inserts OpUndef
at entry and calls `repair_ssa()` to generate correct phi nodes. SM75
gpr_tests.rs extracted to keep gpr.rs under 1000 lines.

## Fixes

| Fix | Impact |
|-----|--------|
| SSA dominance repair (`fix_entry_live_in`) | sigmoid_f64 unblocked |
| Scheduler `debug_assert_eq!` re-promoted | Stronger invariant checking |
| SM75 gpr_tests.rs extraction | gpr.rs 1013 → 813 LOC |

## Test Status

- **1142 passing**, 25 ignored (was 1141/26)
- **63% line coverage**
- Zero clippy warnings, zero fmt issues, zero production `unwrap()`/`todo!()`

## Cross-Spring Shaders

- **47 cross-spring WGSL shaders** total
- **40 compiling SM70** (was 39/47)
- **WGSL corpus**: 47/49 passing, 2 ignored

## Remaining Blockers

| Blocker | Shaders | Notes |
|---------|---------|-------|
| Math function (Acos) | local_elementwise | Polynomial approximation needed |
| Complex64 preamble | dielectric_mermin | Complex arithmetic type needed |

## Pipeline Change

`fix_entry_live_in()` runs early in `pipeline.rs`, before the scheduler and
register allocator. All subsequent passes now operate on valid SSA form.

## Pin Version

All springs should update their coralReef pin to **Phase 10 Iteration 20**.

---

*AGPL-3.0-only*
