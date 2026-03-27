# barraCuda v0.3.4 — Deep Cleanup Sprint 4 Handoff

**Date**: March 9, 2026
**Source**: barraCuda internal audit
**Scope**: Debris removal, orphaned code cleanup, doc accuracy

---

## What Changed

### Orphaned Test Directories Removed (~4,000 lines)

Four test subdirectories under `crates/barracuda/tests/` were never compiled
because no root test file imported them via `mod`. They drifted from the API
and accumulated 84–125 compilation errors each:

| Directory | Lines | Errors | Superseded By |
|-----------|-------|--------|---------------|
| `tests/chaos/` | ~1,400 | 84 | `scientific_chaos_tests.rs`, `fhe_chaos_tests.rs` |
| `tests/fault/` | ~1,300 | 125 | `scientific_fault_injection_tests.rs`, `fhe_fault_tests.rs` |
| `tests/e2e/` | ~500 | 88 | `scientific_e2e_tests.rs` |
| `tests/precision/` | ~400 | 37 | `cross_hardware_parity.rs`, in-module precision tests |

### three_springs Test Suite Wired In

`tests/three_springs/` (4 submodules: basic_tests, e2e_tests, edge_case_tests,
precision_tests) was compiling but never linked. Created `three_springs_tests.rs`
root harness. Compiles clean.

### Stale Comments Cleaned

Removed informal TODO comments from `ops/mod.rs` lines 426–427 about
`logsumexp` vs `logsumexp_wgsl` — both modules are actively used by different
consumers (`LogSumExp` for HMM/batch ops, `LogsumexpWgsl` for Felsenstein).

### Doc Count Accuracy

All documentation updated to match actual verified counts:

| Metric | Was (inflated) | Now (verified) |
|--------|---------------|----------------|
| Lib tests | 3,450+ | 3,262 |
| Integration suites | 31 | 28 |
| Rust source files | 1,062 | 1,044 |
| Showcase demos | 10 | 9 |

---

## Files Changed

| File | Change |
|------|--------|
| `README.md` | Test/file/suite counts corrected |
| `STATUS.md` | Grade notes: demo count, test count, orphan cleanup noted |
| `CHANGELOG.md` | Sprint 4 section added |
| `WHATS_NEXT.md` | Cleanup added to recently completed, showcase count corrected |
| `specs/REMAINING_WORK.md` | Sprint 4 achieved section, test/suite counts corrected |
| `crates/barracuda/src/ops/mod.rs` | Stale comments removed |
| `crates/barracuda/tests/three_springs_tests.rs` | New root harness |
| `crates/barracuda/tests/chaos/` | Removed (orphaned, drifted) |
| `crates/barracuda/tests/fault/` | Removed (orphaned, drifted) |
| `crates/barracuda/tests/e2e/` | Removed (orphaned, drifted) |
| `crates/barracuda/tests/precision/` | Removed (orphaned, drifted) |

---

## Impact on Springs

None — the removed code was never compiled and had no consumers. The
`three_springs/` wiring adds test coverage for primitives used by wetSpring,
airSpring, and hotSpring.

## Quality Gates

All green: `cargo check`, `cargo clippy`, `cargo fmt --check`, `cargo test
-p barracuda --test three_springs_tests --no-run`.
