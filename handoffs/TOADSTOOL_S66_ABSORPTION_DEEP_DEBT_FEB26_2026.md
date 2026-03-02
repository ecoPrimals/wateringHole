# ToadStool/BarraCuda Session 66 — Absorption + Deep Debt

**Date**: February 26, 2026
**Session**: 66
**Status**: All quality gates green | 2,526 barracuda tests | 0 clippy | 0 fmt diffs

---

## Cross-Spring Absorption

### airSpring V009 (metalForge)
- **`stats::regression`**: `fit_linear`, `fit_quadratic`, `fit_exponential`, `fit_logarithmic`, `fit_all()`, `FitResult::predict_one()`/`predict()` — 12 tests
- **`stats::hydrology`**: `hargreaves_et0`, `hargreaves_et0_batch`, `crop_coefficient`, `soil_water_balance` — 13 tests, FAO-56 validated
- **`stats::moving_window_f64`**: CPU f64 sliding window (mean/variance/min/max) complementing GPU f32 `ops::moving_window_stats` — 7 tests

### groundSpring V7
- **`stats::bootstrap::rawr_mean`**: RAWR Dirichlet-weighted resampling (Wang et al. 2021) — 4 tests
- **`mc_et0_propagate.wgsl`**: Already absorbed (verified at `shaders/bio/mc_et0_propagate_f64.wgsl`)
- **`batched_multinomial.wgsl`**: Already absorbed

### P0 Fixes
- **`spearman_correlation`** re-exported from `stats/mod.rs` (was private)
- **`softmax_dim(axis)`**: Already exists in `ops::tensor_axis_ops.rs` (neuralSpring stale request)
- **`WGSL_MEAN_REDUCE`**: Already `pub const` in `ops::mean.rs`

---

## Richards PDE Evolution

- 8 named `SoilParams` constants (Carsel & Parrish 1988): `SANDY_LOAM`, `SILT_LOAM`, `CLAY_LOAM`, `SAND`, `CLAY`, `LOAM`, `SILTY_CLAY_LOAM`, `LOAMY_SAND`
- Picard iteration: 9 buffer vectors preallocated outside loop (was per-iteration allocation)
- Magic numbers → named: `HARMONIC_MEAN_GUARD` (1e-30), `MIN_CAPACITY` (1e-10)

---

## Smart Refactoring

| File | Before | After | Reduction |
|------|--------|-------|-----------|
| `morse_f64.rs` | 804 | 556 | 31% |
| `resource_quota.rs` | 795 | 547 | 31% |

Tests extracted to `*_tests.rs` files. `morse_f64` additionally factored shared `bond_geometry()` and `test_bond()` factory.

---

## Dead Code Evolution (13 → 10)

- `griffin_lim.rs`: `n_fft`/`hop_length` now used for STFT dimension validation + `expected_signal_length()` accessor
- `fhe_key_switch.rs`: `pipeline_accumulate` wired into 2-pass execute (decompose + accumulate)
- `nn/mod.rs`: blanket `#![allow(dead_code)]` removed — zero warnings surfaced

---

## Deep Debt Audit Results

| Category | Count | Status |
|----------|-------|--------|
| Large files (600+) | 21 | Top 2 refactored below threshold |
| `unsafe` blocks | 2 | SPIR-V passthrough + pipeline cache (documented) |
| `#[allow(dead_code)]` | 10 | All Phase 5+ reserved |
| `todo!()`/`unimplemented!()` | 0 | Clean |
| Production mocks | 0 | Mock TPU feature-gated |
| `unwrap()` in production | 0 | Test-only |
| `expect()` in production | ~100 | All lock-poisoning (correct) or test-only |

---

## Remaining Items for Future Sessions

### Large File Candidates (19 remaining >600 lines)
- `gpu_hmc_trajectory.rs` (785): Production logic, needs structural refactoring
- `pppm_gpu/mod.rs` (736): PPPM electrostatics, complex but coherent
- `shaders/precision/mod.rs` (733): Shader registry
- `ops/nonzero/compute.rs` (689): GPU nonzero op

### Spring Feedback
- airSpring: Total WGSL count discrepancy (758 vs 694) needs reconciliation
- hotSpring: `prng_pcg_f64.wgsl`, `su3_math_f64.wgsl`, `polyakov_loop_f64.wgsl` absorption confirmed
- neuralSpring: `tolerance_registry!` macro pattern recommended for cross-spring tolerance management
