# coralReef — Iteration 46: Structural Refactor + Coverage Expansion

**Date**: March 15, 2026
**Primal**: coralReef
**Phase**: 10 — Iteration 46
**Builds on**: CORALREEF_PHASE10_ITERATION45_DEEP_AUDIT_REFACTOR_HANDOFF_MAR14_2026

---

## Summary

Structural decomposition of the largest remaining file (`diagnostic/runner.rs`,
2485 lines) into an `experiments/` submodule with 8 handler files and a shared
context struct. All clippy warnings resolved workspace-wide. 53+ new tests
covering AMD ISA generated tables, Unix JSON-RPC paths, and SM70 encoder/latency
logic. Zero files over 1000 lines. Zero clippy warnings. 1804 tests passing.

## Changes

### diagnostic/runner.rs Refactored (2485 → 769 lines)

The monolithic `diagnostic_matrix` function's 25-arm experiment match was
extracted into `diagnostic/experiments/`:

| File | Lines | Content |
|------|-------|---------|
| `runner.rs` | 769 | Init, setup, teardown, result capture |
| `experiments/mod.rs` | 67 | Dispatch match → handlers |
| `experiments/context.rs` | 54 | `ExperimentContext` struct + helpers |
| `experiments/scheduler.rs` | 70 | Orderings A–D |
| `experiments/direct_pbdma.rs` | 141 | Orderings E–I, T |
| `experiments/vram.rs` | 551 | Orderings J, K, L, Q |
| `experiments/dispatch.rs` | 302 | Orderings N, O, P |
| `experiments/sched_doorbell.rs` | 318 | Orderings R, S, U, U2, V |
| `experiments/runlist_ack.rs` | 236 | Orderings W, X, Y |
| `experiments/reinit.rs` | 294 | Orderings M, Z, Z2, Z3 |

Public API unchanged: `diagnostic::diagnostic_matrix` works identically.

### Clippy Warnings Resolved

- 7 identity ops (`| 0`) removed in runner.rs
- `too_many_arguments` resolved via `ExperimentContext` struct
- `for_loop_over_single_element` → direct assignment
- Benchmark semicolons, redundant closures, `assert_eq!(x, false)` → `assert!(!x)`
- `RangeInclusive::contains` in latency tests
- `# Errors` doc section added to `assign_regs`
- Zero warnings across entire workspace

### Test Coverage Expanded (53+ new tests)

- **25 AMD ISA lookup table tests** — exercises all 20+ generated table files
- **8 Unix JSON-RPC tests** — concurrent connections, client disconnect, server shutdown
- **10 SM70 latency tests** — RAW/WAR/WAW hazard latency validation
- **9 integer ALU encoder tests** — LOP immediate folding
- **1 SM70 encoder integration test** — Bra+Exit control flow

### Metrics

| Metric | Before (Iter 45) | After (Iter 46) |
|--------|-------------------|------------------|
| Tests passing | 1751 | 1804 |
| Tests ignored | 61 | 61 |
| Line coverage | 65.90% | 66.43% |
| Function coverage | 73.75% | 75.15% |
| Clippy warnings | 19 | 0 |
| Files >1000 lines | 1 (runner.rs) | 0 |

## For toadStool

No action required. Public API unchanged.

## For hotSpring

The `diagnostic_matrix` function works identically. The `ExperimentContext`
struct is `pub(in crate::vfio::channel::diagnostic)` — internal only.

## For barraCuda

No action required. Compiler and IPC interfaces unchanged.

---

*coralReef Iteration 46 — Zero files over 1000 lines. Zero clippy warnings.
1804 tests. Structural refactoring completes the file size compliance.*
