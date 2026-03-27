# groundSpring V90 — Deep Debt Execution + Ecosystem Rewire

**Date**: March 7, 2026
**From**: groundSpring V90
**To**: barraCuda, toadStool, coralReef
**Pins**: barraCuda v0.3.3 (local path), toadStool S128, coralReef Phase 9

## Executive Summary

groundSpring V90 is a deep-debt execution session that also rewires to catch up with
significant barraCuda, toadStool, and coralReef evolution since V89. Key outcomes:

1. **Unsafe code eliminated** — `temp-env` RAII replaces all `std::env::set_var` unsafe blocks
2. **11 validation binaries** migrated from inline math to `barracuda::stats` delegation
3. **18 new tests** added — pipeline coverage 0→99.6%, bootstrap +8%, regression +12%
4. **6 bare tolerances** documented with mathematical justifications
5. **CovarianceF64 GPU op** wired (direct dispatch, no longer derived from CorrelationF64)
6. **Marchenko-Pastur bounds** wired via `barracuda::stats::spectral_density`
7. **FFT gap closed** — barraCuda now has `ops::fft::{Fft1D, Fft1DF64, Fft2D, Fft3D, Rfft}`
8. **Specs updated** — PAPER_REVIEW_QUEUE, BARRACUDA_REQUIREMENTS, BARRACUDA_EVOLUTION
9. **798 tests passing**, 91.55%+ line coverage, zero clippy warnings

## Quality Gates

| Gate | Status |
|------|--------|
| cargo fmt --check | PASS |
| cargo clippy --workspace --all-targets -D warnings -W pedantic -W nursery | PASS (zero warnings) |
| cargo check --workspace | PASS |
| cargo doc --workspace --no-deps | PASS |
| cargo test --workspace | PASS (798 tests, 0 failures) |
| Python provenance (test_baseline_integrity.py) | PASS (261/261, unchanged) |
| GPU tests (--all-features) | BLOCKED (barraCuda Fp64Strategy regression, unchanged from V89) |

## Deep Debt Execution Summary

### Unsafe Code Elimination (V90)

| File | Before | After |
|------|--------|-------|
| `tests/biomeos_integration.rs` | `unsafe { std::env::set_var(...) }` | `temp_env::with_var()` / `temp_env::with_vars()` |

Added `temp-env` as dev dependency. All `#[allow(unsafe_code)]` attributes removed.
Workspace-wide `#![forbid(unsafe_code)]` now fully honoured.

### Validation Binary Migration (V90)

11 binaries migrated from inline mean/variance/mbe/rmse to `groundspring::stats::*`
(which delegates to `barracuda::stats`):

| Binary | Inline Math Replaced |
|--------|---------------------|
| validate_real_ghcnd_et0 | mean (2×) |
| validate_uncertainty_bridge | mean, std_dev |
| validate_fao56 | mean, std_dev, variance, percentile |
| validate_et0_anderson | mean, std_dev |
| validate_aggregate_stability | mean, std_dev |
| validate_signal_specificity | mean (3×), variance |
| validate_vendor_parity | mbe, rmse |
| validate_precision_drift | mean (4×), variance, rmse |
| validate_quasispecies | mean |

### Tolerance Documentation (V90)

6 bare numeric tolerances documented with mathematical justifications:

| File | Tolerance | Justification |
|------|-----------|---------------|
| validate_gpu_tier/spectral.rs | 0.05 (eigenvalue band fraction) | Finite grid discretisation Δε = 8/2000 = 0.004 |
| validate_gpu_tier/spectral.rs | 0.95 (eigenvalue percentage) | Bloch theory, 5% edge effects |
| validate_gpu_tier/spectral.rs | 0.02 (Xoshiro mean) | SE = σ/√N ≈ 0.0029, threshold ≈ 7 SE |
| validate_nucleus_pipeline.rs | 0.1 (γ parity) | PRNG mismatch, ~10% of typical γ |
| validate_real_ghcnd_et0.rs | [0.3, 3.5] (PM/Hargreaves ratio) | FAO-56 §4 agroclimate zones |
| validate_real_ghcnd_et0.rs | 10.0 (mean absolute diff) | Guard against data pipeline failures |
| three_tier_parity_physics.rs | 0.05 (band edges) | 12× grid spacing for Brent bisection |

### Test Coverage Expansion (V90)

| Module | Before | After | New Tests |
|--------|--------|-------|-----------|
| fao56/pipeline.rs | 0% | 99.60% | 6 (MC, seasonal, determinism) |
| bootstrap.rs | ~50% | 58.69% | 5 (edge cases, seed divergence) |
| stats/regression.rs | ~55% | 67.79% | 5 (exponential, log, quadratic) |
| anderson.rs | — | +3 | 3 (Marchenko-Pastur, spectral_diagnostics_auto) |

## New barraCuda Delegations (V90)

### Wired

| API | groundSpring Location | Delegation |
|-----|----------------------|------------|
| `ops::covariance_f64_wgsl::CovarianceF64` | stats/correlation.rs `covariance_gpu()` | Direct `sample_covariance()`, fallback to `CorrelationF64::correlation_full` |
| `stats::spectral_density::marchenko_pastur_bounds` | anderson.rs `marchenko_pastur_upper()` | Direct delegation with CPU fallback |

### Available for Future Wiring

| barraCuda API | Use Case | Priority |
|---------------|----------|----------|
| `ops::fft::{Fft1D, Fft1DF64, Rfft}` | Spectral reconstruction, correlator analysis | P1 |
| `ops::autocorrelation_f64_wgsl::AutocorrelationF64` | WDM transport coefficients (raw velocity data) | P2 |
| `pipeline::gpu_view::{GpuView, GpuViewF64}` | Zero-copy GPU-resident chains for MC ensembles | P2 |
| `stats::spectral_density::empirical_spectral_density` | Anderson RMT diagnostics | P2 |
| `ops::peak_detect_f64::PeakDetectF64` | Disorder sweep edge detection | P3 |

## Ecosystem Observations (V90)

### barraCuda v0.3.3

- **708 WGSL shaders**, 1,026 Rust files, 3,014+ tests
- FFT now fully implemented: `Fft1D`, `Fft1DF64`, `Fft2D`, `Fft3D`, `Fft3DF64`, `Rfft` (Cooley-Tukey radix-2)
- `AutocorrelationF64` GPU op (new since V89)
- `CovarianceF64` direct GPU op (new since V89)
- R²/covariance API improvements
- DF64 divisor fix, NVK f64 probe, unwrap/expect removal
- ODE zero-copy evolution
- Pure math mode: `cargo check --no-default-features` → no GPU, just math

### toadStool S128

- **18,028 tests**, 47 JSON-RPC methods
- `PrecisionRoutingAdvice` with `precision_routing()` on `GpuAdapterInfo`
- `SubstrateCapabilityKind::Fft` — FFT now a discoverable capability
- `f64_shared_memory_reliable` always false (naga bug, aligns with groundSpring V84 finding)
- Spring absorption tracker: groundSpring V85 absorbed, P3 items tracked
- groundSpring V80 metalForge (30 workloads, 187 checks) referenced

### coralReef Phase 9

- **Sovereign WGSL → native binary compiler** — NVIDIA SM70-SM89, AMD RDNA2/GFX1030
- **Userspace GPU dispatch** via DRM ioctl (no C deps, no vendor lock-in)
- **f64 transcendentals**: sqrt, rcp, exp2, log2, sin, cos (Newton-Raphson on NVIDIA MUFU seeds)
- 801 tests, A+ grade
- Targets ≤1 ULP precision (aligns with groundSpring `tol::ANALYTICAL`)
- coral-gpu unified compile + dispatch API — future wgpu replacement for compute

## Evolution Requests

### To barraCuda (unchanged from V89, P0 still blocks GPU parity)

| Priority | Request |
|----------|---------|
| **P0** | Fix SumReduceF64/VarianceReduceF64 regression on Hybrid devices (ed82625) |
| **P1** | Expose multinomial_sample_cpu outside cfg(feature = "gpu") |
| **P2** | PRNG alignment: xorshift64 → xoshiro128** migration path |
| **P2** | GPU test coverage patterns (mock/stub device for CI) |

### To toadStool

| Priority | Request |
|----------|---------|
| **P2** | Initialize log subscriber for groundSpring warnings |
| **P3** | Wire SubstrateCapabilityKind::Fft for FFT routing when groundSpring wires FFT ops |

### To coralReef

No changes requested. Phase 9 sovereign pipeline is aligned.

## Delegation Inventory

95+ active delegations (56 CPU + 37 GPU + 2 new in V90).

## What V90 Changed (file summary)

| File | Change |
|------|--------|
| crates/groundspring/Cargo.toml | +temp-env dev dependency |
| crates/groundspring/tests/biomeos_integration.rs | unsafe → temp_env RAII |
| crates/groundspring/src/stats/correlation.rs | CovarianceF64 GPU wired |
| crates/groundspring/src/anderson.rs | marchenko_pastur_upper(), spectral_diagnostics_auto() |
| crates/groundspring-validate/src/validate_real_ghcnd_et0.rs | Inline math → stats delegation |
| crates/groundspring-validate/src/validate_uncertainty_bridge.rs | Inline math → stats delegation |
| crates/groundspring-validate/src/validate_fao56.rs | Inline math → stats delegation |
| crates/groundspring-validate/src/validate_et0_anderson.rs | Inline math → stats delegation |
| crates/groundspring-validate/src/validate_aggregate_stability.rs | Inline math → stats delegation |
| crates/groundspring-validate/src/validate_signal_specificity.rs | Inline math → stats delegation |
| crates/groundspring-validate/src/validate_vendor_parity.rs | Inline math → stats delegation |
| crates/groundspring-validate/src/validate_precision_drift.rs | Inline math → stats delegation |
| crates/groundspring-validate/src/validate_quasispecies.rs | Inline math → stats delegation |
| crates/groundspring/src/fao56/pipeline.rs | +6 tests (MC, seasonal, determinism) |
| crates/groundspring/src/bootstrap.rs | +5 tests (edge cases, seed divergence) |
| crates/groundspring/src/stats/regression.rs | +5 tests (exponential, log, quadratic) |
| metalForge/forge/src/bin/validate_gpu_tier/spectral.rs | Tolerance documentation |
| metalForge/forge/src/bin/validate_nucleus_pipeline.rs | Tolerance documentation |
| crates/groundspring/tests/three_tier_parity_physics.rs | Tolerance documentation |
| specs/BARRACUDA_EVOLUTION.md | Updated to V90 state |
| specs/BARRACUDA_REQUIREMENTS.md | FFT gap → AVAILABLE |
| specs/PAPER_REVIEW_QUEUE.md | FFT gap → AVAILABLE |

---

*This handoff is unidirectional: groundSpring → ecosystem. groundSpring has no reverse
dependencies on toadStool, coralReef, or other springs.*
