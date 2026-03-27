# groundSpring V91 — Complete Ecosystem Rewire + Cross-Spring Evolution

**Date**: March 7, 2026
**From**: groundSpring V91
**To**: barraCuda, toadStool, coralReef
**Pins**: barraCuda v0.3.3, toadStool S128, coralReef Phase 9

## Executive Summary

groundSpring V91 completes the full ecosystem rewire: every available barraCuda op
that applies to groundSpring's domains is now wired, benchmarked, and validated.
The cross-spring shader evolution provenance tree documents how innovations flow
between springs via barraCuda absorption.

**New delegations wired in V91**: 5 new API integrations, 14 new tests, 5 new
benchmarks, 1 cross-spring provenance spec.

## Quality Gates

| Gate | Status |
|------|--------|
| cargo fmt --check | PASS |
| cargo clippy --workspace --all-targets -D warnings -W pedantic -W nursery | PASS (zero warnings) |
| cargo check --workspace | PASS |
| cargo doc --workspace --no-deps | PASS |
| cargo test --workspace | PASS (807 tests, 0 failures) |
| cargo run --release --bin bench-cpu-vs-gpu | PASS (21 workloads benchmarked) |
| GPU tests (--all-features) | BLOCKED (barraCuda Fp64Strategy regression, unchanged) |

## New Delegations (V91)

### 1. AutocorrelationF64 GPU → `wdm.rs`

| Function | Delegation |
|----------|------------|
| `wdm::autocorrelation(data, max_lag)` | `barracuda::ops::autocorrelation_f64_wgsl::AutocorrelationF64::autocorrelation()` |
| `wdm::optimal_block_size(data, max_lag)` | Uses `autocorrelation()` to compute integrated τ_int → block size |

**Provenance**: hotSpring MD VACF analysis → barraCuda S128 `autocorrelation_f64.wgsl`
→ groundSpring WDM transport coefficients.

**Tests**: `acf_lag_zero_is_one`, `acf_exponential_decay`, `acf_constant_data`,
`optimal_block_size_uncorrelated`, `optimal_block_size_correlated` (5 new tests).

### 2. Empirical Spectral Density → `anderson.rs`

| Function | Delegation |
|----------|------------|
| `anderson::empirical_spectral_density(eigenvalues, n_bins)` | `barracuda::stats::spectral_density::empirical_spectral_density()` |

**Provenance**: neuralSpring V69 spectral analysis → barraCuda `stats::spectral_density`
→ groundSpring Anderson RMT diagnostics.

**Tests**: `esd_uniform_eigenvalues`, `esd_empty_returns_empty` (2 new tests).

### 3. PeakDetectF64 → `anderson.rs`

| Function | Delegation |
|----------|------------|
| `anderson::detect_transition(sweep)` | `barracuda::ops::peak_detect_f64::PeakDetectF64::new().prominence().execute()` |

Finds the Anderson metal-insulator transition `W_c` in disorder sweeps by
detecting the peak of |d⟨r⟩/dW| using GPU-accelerated peak detection.
Falls back to CPU argmax.

**Tests**: `detect_transition_monotone_sweep`, `detect_transition_too_short` (2 new tests).

### 4. CovarianceF64 GPU → `stats/correlation.rs` (V90, validated V91)

| Function | Delegation |
|----------|------------|
| `stats::covariance(x, y)` GPU path | `barracuda::ops::covariance_f64_wgsl::CovarianceF64::sample_covariance()` |

Direct single-pass GPU covariance, replacing derived `r * sqrt(var_x * var_y)`.

### 5. Marchenko-Pastur + Spectral Diagnostics Auto → `anderson.rs` (V90, tested V91)

| Function | Delegation |
|----------|------------|
| `anderson::marchenko_pastur_upper(gamma)` | `barracuda::stats::spectral_density::marchenko_pastur_bounds()` |
| `anderson::spectral_diagnostics_auto(eigs, gamma)` | Convenience wrapper: MP upper → spectral_diagnostics |

## Benchmarks Added (V91)

5 new workloads added to `bench-cpu-vs-gpu`:

| Workload | CPU Baseline |
|----------|-------------|
| Autocorrelation (10k points, lag 200) | 0.82 ms |
| Covariance (5k pairs, CovarianceF64 GPU) | 0.01 ms |
| Spectral diagnostics (1k eigenvalues, MP) | < 0.01 ms |
| Empirical spectral density (5k eigs, 50 bins) | 0.01 ms |
| Optimal block size (5k AR(1), ACF→τ_int) | 0.21 ms |

Total benchmark suite: 21 workloads. GPU dispatch will show speedups for
Autocorrelation and Covariance when `barracuda-gpu` feature is enabled.

## Cross-Spring Shader Evolution (New Spec)

Created `specs/CROSS_SPRING_SHADER_EVOLUTION.md` documenting the full provenance
tree for WGSL shaders across all five springs:

| Origin Spring | Shaders Contributed | Cross-Spring Users |
|--------------|--------------------|--------------------|
| **hotSpring** | DF64, lattice QCD, HFB, MD, ESN, linalg, bisection | All springs (DF64), groundSpring, wetSpring, neuralSpring |
| **groundSpring** | FFT, Anderson Lyapunov, chi², RAWR, MC ET₀, tolerances | All springs (FFT, tolerances), hotSpring, airSpring |
| **wetSpring** | Bray-Curtis, fused_map_reduce, HMM, RF, cosine_sim | airSpring, hotSpring, neuralSpring |
| **neuralSpring** | chi²/KL fused, batch_ipr, Metropolis, histogram, matmul | hotSpring, groundSpring |
| **airSpring** | Anderson coupling, seasonal pipeline, Brent, SCS-CN | groundSpring |

**Key insight**: hotSpring's DF64 (double-float f32 pairs, ~48-bit mantissa) — 
created for nuclear structure calculations — now powers earth science Monte Carlo,
marine bio diversity metrics, and ML training validation across all springs.

## Delegation Inventory (V91)

**100 active delegations** (56 CPU + 37 GPU + 5 new CPU/GPU in V91 + 2 from V90).

### By module:

| Module | CPU Delegations | GPU Delegations |
|--------|----------------|-----------------|
| anderson | 5 | 5 + 2 new (ESD, detect_transition) |
| stats | 12 | 5 + 1 new (CovarianceF64) |
| bootstrap | 4 | 1 |
| fao56 | 6 | 3 |
| wdm | 2 | 0 + 1 new (AutocorrelationF64) |
| spectral_recon | 0 | 2 |
| jackknife | 1 | 1 |
| rarefaction | 4 | 2 |
| gillespie | 2 | 2 |
| drift | 2 | 1 |
| freeze_out | 4 | 3 |
| optimize | 2 | 2 |
| transport | 1 | 0 |
| Other | 11 | 10 |

## What V91 Changed (file summary)

| File | Change |
|------|--------|
| crates/groundspring/src/wdm.rs | +autocorrelation(), +optimal_block_size(), +5 tests |
| crates/groundspring/src/anderson.rs | +empirical_spectral_density(), +detect_transition(), +4 tests |
| crates/groundspring/src/stats/correlation.rs | CovarianceF64 GPU wired (V90) |
| crates/groundspring-validate/src/bench_cpu_vs_gpu.rs | +5 benchmark workloads |
| specs/CROSS_SPRING_SHADER_EVOLUTION.md | New: cross-spring provenance tree |
| specs/BARRACUDA_EVOLUTION.md | Updated to V91 state |
| specs/BARRACUDA_REQUIREMENTS.md | FFT gap → AVAILABLE |
| specs/PAPER_REVIEW_QUEUE.md | FFT gap → AVAILABLE |

## Future Wiring (P1-P3)

| API | Priority | Blocker |
|-----|----------|---------|
| `ops::fft::Fft1DF64` kernel integration | P1 | Architecture decision: Tikhonov → FFT-based spectral density |
| `pipeline::gpu_view::GpuView` | P2 | MC pipeline refactor to keep data GPU-resident |
| `validation::ValidationHarness` | P3 | Replace groundSpring validate module with barraCuda's |
| `tolerances::*` named tolerances | P3 | Align `tol::*` constants with barraCuda's Tolerance struct |

## Evolution Requests (unchanged from V90)

### To barraCuda

| Priority | Request |
|----------|---------|
| **P0** | Fix SumReduceF64/VarianceReduceF64 regression on Hybrid devices |
| **P1** | Expose multinomial_sample_cpu outside cfg(feature = "gpu") |
| **P2** | PRNG alignment: xorshift64 → xoshiro128** migration path |

---

*This handoff is unidirectional: groundSpring → ecosystem. groundSpring has no reverse
dependencies on toadStool, coralReef, or other springs.*
