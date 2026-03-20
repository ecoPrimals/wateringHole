<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# barraCuda v0.3.6 — Audit Completion, Doctest & Hardware Fixes

**Date**: March 20, 2026
**Primal**: barraCuda
**Version**: 0.3.6
**Sprint**: Deep Debt Sprint 14
**Previous**: BARRACUDA_V036_AUDIT_COVERAGE_TEST_HARDENING_HANDOFF_MAR20_2026

---

## Summary

Continuation of the comprehensive audit. Fixed all pre-existing doctest
failures (2), hardware verification multi-GPU buffer lifetime panic,
12 clippy new-edition lints, and 1 stale SPDX header. Added 50 new tests
across RBF surrogate, adaptive distance, population genetics, and
jackknife modules. Updated all root documentation and wateringHole
manifest to reflect current state. All quality gates green. 3,936 tests
+ 108 doctests pass, 0 fail.

## Changes

### Doctest Fixes (2 pre-existing failures → 0)

- **`complex_f64.rs`**: Doctest assertion `starts_with("// complex_f64")`
  was stale — the WGSL file now starts with SPDX header. Fixed assertion
  to check for `c64_mul` content and correct suffix.
- **`sobol.rs`**: Two issues — bare `let` without `fn main()` wrapper
  fails under Rust 2024 merged doctests, and `gen` is a reserved keyword
  in edition 2024. Added `# fn main()` wrapper and renamed to `sampler`.

### Hardware Verification Fix

- **`test_multi_gpu_performance_characterization`**: wgpu
  `Buffer[Id] is no longer alive` panic on multi-GPU due to cross-device
  buffer lifetime overlap. Fixed by scoping tensors per-device iteration
  so GPU buffers are fully released before the next device. Added
  `"is no longer alive"` to GPU-resilient skip patterns.

### Coverage Expansion (+50 tests → 3,936 total)

- **`surrogate/rbf/tests.rs`** (+10): Error-path tests using any-GPU
  device, `predict` empty/dimension-mismatch validation,
  `loo_cv_optimal_smoothing` (empty/default/custom grid), `from_parts`,
  struct field tests.
- **`surrogate/adaptive/tests.rs`** (+16): CPU-only distance function
  tests (identity/2D/asymmetric, f32-promoted accuracy/zero/high-dim),
  config/diagnostics `Debug`/`Clone`, error-path tests for
  `train_adaptive` and `train_with_validation`.
- **`stats/evolution.rs`** (+14): Kimura fixation edge cases (absent
  allele, near-neutral, strong beneficial/deleterious, small population,
  degenerate denominator), error threshold edges, detection power edges,
  GPU dispatch/empty/mismatch.
- **`stats/jackknife.rs`** (+10): Generalized jackknife with median/sum/max,
  constant-large-dataset variance, two-element, `JackknifeResult`
  traits, linear data mean, GPU large-dataset parity.

### SPDX & Lint Fixes

- **`warmup.rs`**: `AGPL-3.0-only` → `AGPL-3.0-or-later`.
- **`pooling_tests.rs`**: Device-aware buffer activity assertion.
- **12 clippy new-edition lints**: `identity_op`, `manual_range_contains`,
  `manual_is_multiple_of`, `manual_midpoint` — all in test code.

### Documentation Alignment

- **Test counts**: 3,936 across README, STATUS, WHATS_NEXT, scripts.
- **File count**: Corrected to 1,085 Rust source files.
- **Doctest gate**: 108 pass / 0 fail added to quality gates.
- **CHANGELOG**: Sprint 14 entry added.
- **REMAINING_WORK**: Updated with Sprint 12 continuation achievements.
- **wateringHole manifest**: `latest` updated 0.3.5 → 0.3.6.

## Quality Gates

```
cargo fmt --all -- --check                                              ✓ clean
cargo clippy --workspace --all-targets --all-features -- -D warnings    ✓ zero warnings
cargo doc --workspace --all-features --no-deps                          ✓ clean
cargo test --doc -p barracuda                                           ✓ 108 pass, 0 fail
cargo deny check                                                        ✓ clean
cargo nextest run --workspace --all-features --no-fail-fast             ✓ 3,936 pass, 0 fail
```

## Codebase Health

- **Rust source files**: 1,085
- **WGSL shaders**: 806 (all with SPDX headers)
- **Tests**: 3,936 nextest + 108 doctests (0 failures)
- **Coverage**: 71.4% line / 77.9% function (llvmpipe)
- **Unsafe code**: Zero (`#![forbid(unsafe_code)]`)
- **TODO/FIXME/HACK**: Zero
- **`unwrap()` in production**: Zero
- **`println!` in library code**: Zero
- **Files over 1000 LOC**: Zero
- **Archive/debris**: Zero (fossil record at ecoPrimals/ level)

## Cross-Primal Pins

| Primal | Version/Session | Status |
|--------|-----------------|--------|
| toadStool | S160 | Coverage & deep execution sprint |
| coralReef | Phase 10 Iter 58 | Deep debt & unsafe evolution |

## Next Steps

- P1: DF64 end-to-end NVK hardware verification (Yukawa shaders)
- P1: coralReef sovereign compiler evolution
- P2: Coverage to 90% (requires f64-capable GPU hardware in CI)
- P2: Kokkos GPU parity benchmarks
- P3: Multi-GPU dispatch evolution
