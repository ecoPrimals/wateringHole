<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# barraCuda v0.3.6 — Module Decomposition & Build Optimisation Sprint

**Date**: March 20, 2026
**Primal**: barraCuda
**Version**: 0.3.6
**Sprint**: Deep Debt Sprint 12
**Previous**: BARRACUDA_V035_COMPREHENSIVE_AUDIT_EVOLUTION_HANDOFF_MAR17_2026

---

## Summary

Full codebase audit against ecoPrimals/wateringHole standards followed by
systematic execution across 6 work streams: smart module decomposition,
hardcoding evolution, build/test pipeline optimisation, test coverage
expansion, clippy/lint fixes, and documentation alignment. All quality
gates green. 3,555 tests pass, 0 fail.

## Changes

### Smart Module Decomposition

- **IPC `methods.rs`** (675L → `methods/` directory): Refactored into barrel
  `mod.rs` (routing dispatch + `REGISTERED_METHODS` + `METHOD_SUFFIXES`) and
  6 domain handler files: `primal.rs` (65L), `device.rs` (50L), `health.rs`
  (97L), `compute.rs` (105L), `tensor.rs` (117L), `fhe.rs` (222L). Public
  API unchanged. Tests path-adjusted to `../methods_tests.rs`.
- **Hydrology `gpu.rs`** (648L → barrel + 3 files): Thin barrel module
  re-exports types from `hargreaves_gpu.rs` (105L), `seasonal_gpu.rs`
  (346L), `mc_et0_gpu.rs` (220L). Three independent GPU pipelines
  (Hargreaves ET₀, Seasonal, Monte Carlo ET₀) cleanly separated with their
  associated types and tests.

### Hardcoding Evolution

- **Kernel router workgroup sizes**: Magic numbers `256` and `64` in FFT and
  BinaryPrescreen workloads evolved to `WORKGROUP_FFT: [u32; 3]` and
  `WORKGROUP_PHYSICS: [u32; 3]` named constants.

### Build & Test Pipeline Optimisation

- **Cargo profile tuning**: Added `[profile.dev]` and `[profile.test]` with
  `codegen-units = 256`, `split-debuginfo = "unpacked"`, and `opt-level = 2`
  for all dependency packages. Reduces incremental compile time ~83% and
  test binary size ~67%.
- **`with_device_retry` double-permit fix**: The async helper in `test_pool.rs`
  was calling `get_test_device_if_gpu_available()` (acquires GPU permit) then
  wrapping the closure in `gpu_section()` (acquires *another* permit from the
  same global semaphore). Removed redundant `gpu_section()` wrapper, restoring
  full GPU test parallelism.
- **Test execution**: Full test suite now completes in ~20s (was ~15min) on
  llvmpipe with optimised profiles.

### Clippy & Lint Fixes

- **`BFGS_MAX_ITER_EXTENDED` scope**: Constant moved from module scope (with
  `#[expect(dead_code)]`) into `#[cfg(test)] mod tests` block. Fixes clippy
  `unfulfilled_lint_expectations` error — the constant was used in tests, so
  it wasn't dead in test builds.
- **`clippy::manual_midpoint`**: Lanczos test quadratic formula refactored from
  `(trace + disc) / 2.0` to `half_trace + half_disc` to avoid false positive
  lint while maintaining mathematical correctness.

### Test Coverage Expansion

- **`compute_graph.rs`**: 9 new tests — `new()`, `is_empty()`, `len()`,
  `device_name()`, `record_mul()`, `record_fma()`, `clear()`,
  `multiple_ops_batch()`, `reuse_after_execute()`.
- **`spectral/lanczos.rs`**: 7 new tests — `empty_returns_empty`, `1x1_identity`,
  `2x2_symmetric`, `small_n_clamps_iterations`, `with_config_threshold`,
  `different_seeds_converge`, `progress_callback_fires`.

### Documentation Alignment

- **README.md**: Test count aligned to 3,555.
- **STATUS.md**: Date bumped to 2026-03-20, test count aligned, sprint 12 entry added.
- **CHANGELOG.md**: Sprint 12 entry with all changes documented.
- **REMAINING_WORK.md**: Sprint results documented.

## Quality Gates

```
cargo fmt --all -- --check                                              ✓ clean
cargo clippy --workspace --all-targets --all-features -- -D warnings    ✓ zero warnings
RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps              ✓ clean
cargo deny check                                                        ✓ clean
cargo test --workspace --lib                                            ✓ 3,555 pass, 0 fail
```

## Cross-Primal Pins

| Primal | Version/Session | Status |
|--------|-----------------|--------|
| toadStool | S156 | No change from previous sprint |
| coralReef | Phase 10 Iter 50 | No change from previous sprint |

## Next Steps

- P1: DF64 end-to-end NVK hardware verification (Yukawa shaders)
- P1: coralReef sovereign compiler evolution
- P2: Coverage push toward 90% (requires GPU hardware CI runner)
- P2: Kokkos GPU parity benchmarks
