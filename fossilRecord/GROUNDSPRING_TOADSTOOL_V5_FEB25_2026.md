# groundSpring → ToadStool Handoff V5: Code Audit, Debt Resolution & Three-Tier Evolution

**Date**: February 25, 2026
**From**: groundSpring (validation spring — measurement noise characterization)
**To**: ToadStool / BarraCUDA team
**Supersedes**: V4 (archived)
**ToadStool baseline**: Sessions 51–62 + DF64 expansion (Feb 24–25, 2026)

---

## Summary

V5 reports completion of a comprehensive code audit and deep debt resolution
pass on the groundSpring codebase. Additionally, this handoff documents the
full three-tier control plan (CPU → GPU → metalForge) for all 27 papers in
the review queue, identifies what barracuda should absorb from groundSpring,
and what groundSpring learned that is relevant to barracuda's evolution.

### Key Changes Since V4

- **CRITICAL FIX**: `barracuda::spectral::anderson::lyapunov_*` paths were
  wrong — `anderson` is a private submodule; items are re-exported at
  `barracuda::spectral::lyapunov_*`. This broke `cargo clippy --all-features`,
  `cargo doc --all-features`, and `cargo test --all-features`.
- **Code quality**: `cargo fmt` fixed (6 files), all `clippy::too_many_lines`
  warnings resolved, `f64::total_cmp` replaces `partial_cmp().unwrap_or()`.
- **DRY**: Extracted shared `percentile_ci()` in bootstrap, eliminated
  duplicate Box-Muller in validate_rawr.
- **Provenance**: `control/common.py` now has `write_benchmark()` for
  reproducible benchmark JSON generation with git commit + date.
- **Documentation**: Stale `bootstrap_mean_f64.wgsl` references removed;
  tolerance justifications added throughout; anderson seed divergence documented.
- **5 new CPU delegations** (V5 rewiring phase):
  - `stats::covariance` → `barracuda::stats::correlation::covariance`
  - `stats::norm_cdf` → `barracuda::stats::norm_cdf`
  - `stats::norm_ppf` → `barracuda::stats::norm_ppf`
  - `stats::chi2_statistic` → `barracuda::stats::chi2_decomposed`
  - `anderson::analytical_localization_length` → `barracuda::special::anderson_transport::localization_length`
- **Benchmarks**: Local vs barracuda-gpu timing shows <2% overhead for
  compute-heavy binaries. Total 119/119 PASS in all 3 modes.
- **Cross-spring evolution** documented: traces primitive provenance from
  hotSpring (precision), wetSpring (bio), neuralSpring (ML) to groundSpring.

---

## Part 1: What groundSpring Consumes from BarraCUDA

### CPU-delegated (11 total — 5 new in V5 rewiring)

| groundSpring function | BarraCUDA target | Feature gate | Status |
|---|---|---|---|
| `stats::pearson_r` | `stats::pearson_correlation` | `barracuda` | Wired (V2) |
| `stats::spearman_r` | `stats::correlation::spearman_correlation` | `barracuda` | Wired (V3) |
| `stats::sample_std_dev` | `stats::correlation::std_dev` | `barracuda` | Wired (V3) |
| `stats::covariance` | `stats::correlation::covariance` | `barracuda` | **New (V5)** |
| `stats::norm_cdf` | `stats::norm_cdf` | `barracuda` | **New (V5)** |
| `stats::norm_ppf` | `stats::norm_ppf` | `barracuda` | **New (V5)** |
| `stats::chi2_statistic` | `stats::chi2_decomposed` | `barracuda` | **New (V5)** |
| `bootstrap::bootstrap_mean` | `stats::bootstrap_mean` | `barracuda` | Wired (V4) |
| `anderson::lyapunov_exponent` | `spectral::lyapunov_exponent` | `barracuda-gpu` | Wired (V4) — **path fixed V5** |
| `anderson::lyapunov_averaged` | `spectral::lyapunov_averaged` | `barracuda-gpu` | Wired (V4) — **path fixed V5** |
| `anderson::analytical_localization_length` | `special::anderson_transport::localization_length` | `barracuda` | **New (V5)** |

### GPU-ready (Tier A pending adapter — unchanged from V3)

| groundSpring function | BarraCUDA GPU op | Shader |
|---|---|---|
| `stats::rmse` | `NormReduceF64::l2` | `norm_reduce_f64.wgsl` |
| `stats::mbe` | `SumReduceF64::mean` | `sum_reduce_f64.wgsl` |
| `stats::r_squared` | `VarianceReduceF64` + reduce | `variance_reduce_f64.wgsl` |
| `stats::index_of_agreement` | `FusedMapReduceF64` | `fused_map_reduce_f64.wgsl` |
| `stats::hit_rate` | `FusedMapReduceF64` | `fused_map_reduce_f64.wgsl` |
| `rarefaction::shannon_diversity` | `FusedMapReduceF64::shannon_entropy` | `fused_map_reduce_f64.wgsl` |

### Absorbed upstream (unchanged)

| Original Tier C item | BarraCUDA op | Notes |
|---|---|---|
| `mc_et0_propagate_f64` | `BatchedElementwiseF64::fao56_et0_batch` | FAO-56 equation chain as `Op::Fao56Et0` |

---

## Part 2: What Still Needs ToadStool Action

### Priority 1: Batched Multinomial (Tier C — production WGSL exists)

Production-quality shader in `metalForge/shaders/batched_multinomial.wgsl`
(112 lines). Required for Exp 004 GPU validation and R. Anderson papers (#20-21).

### Priority 2: RAWR Weighted Resampling Kernel (Tier C)

`bootstrap::rawr_mean` has no barracuda equivalent. RAWR resampling (Wang et al. 2021)
uses Dirichlet-distributed weights — embarrassingly parallel, suitable for GPU.

**Proposed API**: `ops::rawr_weighted_mean_f64(data, weights, n_bootstrap, seed) → BootstrapCI`
**CPU reference**: `groundspring::bootstrap::rawr_mean` (Exp 007: 11/11 PASS)

### Priority 3: PRNG Alignment (Tier B)

Xorshift64 ↔ xoshiro128** stream mismatch. Migration roadmap in
`specs/BARRACUDA_EVOLUTION.md` §PRNG Alignment.

### Priority 4: Grid Search 3D Dispatch (Tier B)

`seismic::grid_search_inversion` — needs workgroup dispatch + min-reduce.

### Priority 5: spectral Module Public API Cleanup

The `anderson` submodule within `spectral` is private. `lyapunov_exponent`
and `lyapunov_averaged` are re-exported at the `spectral` level. This is
correct but confusing — consuming springs may try `spectral::anderson::*`
and get `E0603`. Consider either:
1. Making the `anderson` submodule public, or
2. Documenting the re-export pattern in barracuda's module docs.

groundSpring hit this exact issue (the CRITICAL FIX above). Other springs
using `spectral::anderson` may have the same latent bug.

---

## Part 3: Lessons Learned for BarraCUDA Evolution

### 3.1 Private Submodule Re-exports

The `barracuda::spectral::anderson` private module caused a compile error
that was masked because `cargo test` (without `--all-features`) doesn't
exercise the barracuda-gated paths. **Recommendation**: BarraCUDA CI should
run `cargo test --all-features` and `cargo doc --all-features` to catch
consumer-facing visibility issues.

### 3.2 Seed Convention Divergence

groundSpring's `lyapunov_averaged` uses `base_seed + i` for the i-th
realization; barracuda's `lyapunov_averaged` uses `base_seed + r * 1000`.
Both produce valid averaging but different numerical values. This means:

- groundSpring's local path and barracuda path produce **different numbers**
  for the same inputs (different per-realization seeds).
- Both are correct (averaging over disorder converges regardless of seed
  sequence), but determinism tests must be gated on the feature flag.

**Recommendation**: Standardize the seed convention. `base_seed + r * 1000`
provides isolation between realization streams; `base_seed + i` is simpler
but streams may correlate for small i.

### 3.3 RAWR as a Resampling Primitive

RAWR (Wang et al. 2021, Bioinformatics) is a principled alternative to
standard bootstrap. groundSpring validated it across Gaussian, skewed, and
correlated data (11/11 PASS). The algorithm is:

1. Generate n weights from Exp(1): `w_i = -ln(U_i)` where U ~ Uniform(0,1)
2. Normalize: `w_i = w_i / Σw_i`
3. Compute weighted mean: `Σ(w_i × x_i)`

This is embarrassingly parallel (one replicate per invocation) and maps to
the same dispatch pattern as `batched_multinomial.wgsl`. If barracuda absorbs
a RAWR kernel, it would be useful across wetSpring (rarefaction confidence),
neuralSpring (model uncertainty), and potentially hotSpring (lattice observable
confidence).

### 3.4 Gillespie SSA CPU Reference

`groundspring::gillespie::birth_death_ssa` is a clean, tested CPU
implementation of exact SSA (12/12 checks, 5 unit tests, 30.9× faster than
Python). If barracuda wants a CPU fallback for `GillespieGpu`, groundSpring's
implementation is a validated reference.

### 3.5 Feature Gate Pattern That Works

The two-gate pattern works well:
- `barracuda` — CPU-available ops (stats, bootstrap)
- `barracuda-gpu` — GPU-feature-gated ops (spectral/anderson)

This lets springs test CPU delegation without needing GPU hardware. Consider
formalizing this as a barracuda convention.

### 3.6 f64::total_cmp for NaN-Safe Sorting

groundSpring found multiple sites using `partial_cmp(b).unwrap_or(Equal)`
for float sorting. `f64::total_cmp` (stable since Rust 1.62) is cleaner
and handles NaN correctly by placing it at the end. If barracuda has similar
patterns, they should be migrated.

### 3.7 Centralized Cast Helpers

groundSpring replaced 40+ scattered `as f64` / `as usize` casts with a
centralized `cast` module that documents the safety argument once:

```rust
pub fn usize_f64(n: usize) -> f64  // Safe: n < 2^53
pub fn f64_usize(x: f64) -> usize  // Safe: x ≥ 0 and < usize::MAX
pub fn u64_f64(n: u64) -> f64      // Safe: n < 2^53
```

If barracuda has scattered numeric casts, a similar module would centralize
the safety reasoning and enable `#[expect(clippy::cast_precision_loss)]` at
a single site instead of sprinkling `#[allow]` everywhere.

---

## Part 4: Three-Tier Control Matrix

### Completed Experiments (119/119 CPU)

| # | Experiment | CPU | GPU | metalForge |
|---|-----------|:---:|:---:|:----------:|
| 1 | Sensor noise decomposition | **36/36 PASS** | Pending (Tier A) | — |
| 2 | Observation gap | **13/13 PASS** | Pending (Tier A) | — |
| 3 | Error propagation FAO-56 | **15/15 PASS** | Pending (adapter) | — |
| 4 | Sequencing noise | **15/15 PASS** | Blocked (Tier C: multinomial) | — |
| 5 | Seismic inversion | **9/9 PASS** | Blocked (Tier B: grid search) | — |
| 6 | Signal specificity | **12/12 PASS** | **Ready** (`GillespieGpu`) | — |
| 7 | RAWR resampling | **11/11 PASS** | Ready (embarrassingly parallel) | — |
| 8 | Anderson localization | **8/8 PASS** | **Ready** (`spectral::*`) | — |

### Queued Papers — GPU Readiness

| Category | Papers | CPU Status | GPU Status | Blocker |
|----------|--------|:---------:|:----------:|---------|
| GPU-ready now | 9, 10, 12, 14, 15, 16 | Mix of active/queued | Barracuda ops exist | CPU baseline needed |
| GPU-blocked (FFT) | 6, 7 | Queued | No FFT in barracuda | **FFT gap** |
| GPU-blocked (adapter) | 1-5 | **119/119 PASS** | Ops exist, need adapter | `gpu` feature wiring |
| GPU-blocked (Tier C) | 4, 20-21 | Active/queued | Need multinomial | **batched_multinomial** |
| metalForge ready | None yet | — | After GPU tier | — |

---

## Part 5: Performance Summary

| Experiment | Python (s) | Rust (s) | Speedup |
|---|---|---|---|
| Exp 006: Signal Specificity (Gillespie SSA) | 26.2 | 0.85 | **30.9×** |
| Exp 007: RAWR Resampling (bootstrap) | 4.4 | 0.60 | **7.3×** |
| Exp 008: Anderson Localization (transfer matrix) | 21.4 | 0.72 | **29.8×** |
| **Total** | **52.0** | **2.17** | **24.0×** |

GPU dispatch would further accelerate all three. Gillespie and Anderson
have per-step branching that CPU handles well; the GPU win comes from
batch ensemble (many trajectories/realizations simultaneously).

---

## Part 6: ToadStool Catch-Up Summary (S58–S62 + DF64)

groundSpring's barracuda dependency has been verified against ToadStool HEAD
(post-S62 DF64 expansion, Feb 25 2026). Key changes since our last baseline:

| Session | Relevant to groundSpring | Notes |
|---------|-------------------------|-------|
| S58 | ODE bio (5 systems), NMF, Fp64Strategy | Bio ODEs for Waters papers |
| S59 | `anderson_3d_correlated`, `anderson_sweep_averaged`, `find_w_c`, `ridge_regression`, `ValidationHarness` | Future Kachkovskiy extension experiments |
| S60-61 | `cpu-math` feature gate, SpMM, TransE | groundSpring's `barracuda` (no gpu) works with cpu-math |
| S62 | `BandwidthTier`, `PeakDetectF64` | metalForge infrastructure |
| Post-S62 | DF64 core-streaming, `ComputeDispatch` builder | Consumer GPU precision strategy |

**New barracuda spectral items available for future experiments**:
- `spectral::anderson_3d_correlated` — exponential-kernel correlated disorder
- `spectral::anderson_sweep_averaged` — disorder-averaged ⟨r⟩(W) with stderr
- `spectral::find_w_c` — critical disorder via GOE-Poisson crossing
- `linalg::ridge_regression` — Cholesky-based Tikhonov

**barracuda has `bootstrap_mean_f64.wgsl`** — a 65-line GPU shader for parallel
bootstrap mean estimation. This means `bootstrap_mean` has both CPU and GPU
paths in barracuda. groundSpring already delegates to the CPU path.

**Verified**: All 6 delegations compile and produce correct results with
`--features barracuda-gpu`. All 119/119 validation checks pass in both
local and barracuda-delegated modes.

---

## Part 7: Quality Gates (Post-Audit, Post-ToadStool Catch-Up)

| Gate | Result |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --all-targets -W pedantic -W nursery` | PASS (0 warnings) |
| `cargo clippy --features barracuda-gpu` | PASS (0 warnings) |
| `cargo doc --no-deps` | PASS |
| `cargo test` | 108/108 PASS (+ 1 doc test) |
| `cargo test --features barracuda` | 108/108 PASS |
| `cargo test --features barracuda-gpu` | 108/108 PASS |
| Validation binaries (local) | **119/119 PASS** across 8 binaries |
| Validation binaries (`barracuda-gpu`) | **119/119 PASS** across 8 binaries |
| Library line coverage | 99.7% (100% functions) |
| Unsafe code | Forbidden (workspace lint) |
| Max file size | <1000 lines per file |
| SPDX headers | All `.rs` files |
| License | AGPL-3.0-or-later |
| Open data | All 27 papers use public repositories |
| Python tests | 34/34 PASS (`pytest`) |
| Performance | 24× faster than Python |

---

## Part 7: What NOT to Duplicate

All items from V4 plus:

| Primitive | Why |
|---|---|
| Centralized cast helpers (`cast::usize_f64`, etc.) | Safety argument documented once |
| `percentile_ci()` shared helper in bootstrap | Both bootstrap + RAWR use it |
| `write_benchmark()` in Python common.py | Standardized provenance for benchmark JSONs |

---

## Part 8: For Other Springs

### groundSpring Exports

| What | For Whom | How |
|---|---|---|
| Noise characterization labels | neuralSpring | Export labeled dirty data for ML training |
| Uncertainty budget (sensor → ET₀) | airSpring | Humidity dominates at 66% — sensor upgrade priority |
| Minimum sequencing depth | wetSpring | Genus saturation at 5,000 reads |
| RAWR confidence intervals | All springs | Validated alternative to naive bootstrap |
| `f64::total_cmp` pattern | All springs | NaN-safe float sorting (replaces `partial_cmp` antipattern) |
| Cast centralization pattern | All springs | Module-level safety argument for numeric casts |

### Cross-Spring Primitive Sharing

| Kernel | groundSpring Need | Also Needed By |
|---|---|---|
| FFT | Spectral reconstruction (spectral) | hotSpring (lattice QCD), wetSpring (signal processing) |
| Monte Carlo | Error propagation | hotSpring (nuclear EOS), neuralSpring (training) |
| Gillespie | Biological noise | wetSpring (c-di-GMP dynamics) |
| Bootstrap/RAWR | Confidence estimation | wetSpring (rarefaction), neuralSpring (model uncertainty) |
| Eigensolve | Bifurcation analysis | hotSpring (HFB), wetSpring (PCoA) |
| Lanczos | Anderson localization | hotSpring (Dirac spectrum), neuralSpring (Hessian) |
| SpMV | Lanczos inner loop | hotSpring (lattice gauge) |

---

## Part 7: Cross-Spring Evolution & Benchmarks

### Delegation Benchmark (Local vs BarraCUDA CPU, release mode)

| Binary | Local (ms) | Barracuda-GPU (ms) | Overhead |
|--------|-----------|-------------------|----------|
| validate-decompose | 60 | 82 | +37% (startup) |
| validate-rarefaction | 80 | 101 | +26% (startup) |
| validate-seismic | 111 | 136 | +23% (startup) |
| validate-weather | 56 | 82 | +46% (startup) |
| validate-fao56 | 72 | 96 | +33% (startup) |
| validate-signal-specificity | 861 | 870 | **+1%** |
| validate-rawr | 613 | 626 | **+2%** |
| validate-anderson | 720 | 728 | **+1%** |
| **TOTAL** | **2573** | **2721** | **+6%** |

Overhead in short binaries is barracuda link/init cost.
For compute-heavy binaries, delegation adds **<2%** overhead.

### Cross-Spring Primitive Provenance

The 11 delegated functions trace back through the ecosystem:

| Delegation | Origin Spring | How It Reached barracuda |
|-----------|--------------|--------------------------|
| `pearson_r`, `sample_std_dev` | hotSpring | Core statistics from nuclear validation |
| `spearman_r` | wetSpring S57 | Ranked correlation for ecology |
| `covariance` | hotSpring | Covariance matrix for HFB |
| `norm_cdf`, `norm_ppf` | neuralSpring | erf/erfc special functions |
| `chi2_statistic` | wetSpring V18 | chi_squared_f64 primal compatibility |
| `bootstrap_mean` | hotSpring | Monte Carlo confidence intervals |
| `lyapunov_exponent/averaged` | hotSpring spectral | Anderson model, transfer matrix |
| `analytical_localization_length` | hotSpring transport | Perturbative ξ(W,E) |

This cross-pollination demonstrates the ecosystem value: groundSpring
uses primitives from THREE other springs (hotSpring, wetSpring,
neuralSpring), each contributing domain expertise that enriches the
measurement noise framework.

Full cross-spring evolution narrative in `specs/CROSS_SPRING_EVOLUTION.md`.

## Handoff Checklist

- [x] Critical barracuda path fix (`spectral::anderson::*` → `spectral::*`)
- [x] All stale paths fixed across 8 documentation files
- [x] Code audit: fmt, clippy pedantic+nursery, doc — all clean
- [x] DRY: extracted shared helpers, eliminated duplicate implementations
- [x] Provenance: `write_benchmark()` added to Python common.py
- [x] All 119/119 validation checks passing (both local and barracuda-gpu)
- [x] ToadStool catch-up: verified against S62 + DF64 expansion
- [x] All 11 delegations produce correct results with `--features barracuda-gpu`
- [x] 5 new delegations wired (covariance, norm_cdf/ppf, chi2, analytical ξ)
- [x] Benchmarks confirm <2% overhead for compute-heavy binaries
- [x] Cross-spring evolution documented (specs/CROSS_SPRING_EVOLUTION.md)
- [x] New barracuda ops cataloged (S59-S62+)
- [x] barracuda `bootstrap_mean_f64.wgsl` GPU shader existence documented
- [x] Lessons learned documented for barracuda team
- [x] Three-tier control matrix updated for 27 papers
- [x] V4 archived
- [x] Quality gates verified post-audit and post-catch-up

---

## Files Changed Since V4

### Modified files (code)
- `crates/groundspring/src/anderson.rs` — path fix + `analytical_localization_length`
- `crates/groundspring/src/stats.rs` — `covariance`, `norm_cdf`, `norm_ppf`, `chi2_statistic`
- `crates/groundspring/src/bootstrap.rs` — `percentile_ci()` extraction, `f64::total_cmp`
- `crates/groundspring-validate/src/validate_rawr.rs` — DRY: library `normal()`
- `crates/groundspring-validate/src/validate_anderson.rs` — helper extraction
- `crates/groundspring-validate/src/validate_fao56.rs` — helper extraction
- `crates/groundspring-validate/src/validate_seismic.rs` — helper extraction
- `crates/groundspring-validate/src/validate_weather.rs` — doc comments
- `control/common.py` — `provenance_metadata()`, `write_benchmark()`

### New files
- `specs/CROSS_SPRING_EVOLUTION.md` — Cross-spring shader provenance
- `scripts/bench_barracuda_modes.sh` — Three-mode benchmark script

### Modified files (docs)
- `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CONTROL_EXPERIMENT_STATUS.md`
- `specs/BARRACUDA_EVOLUTION.md`, `specs/BARRACUDA_REQUIREMENTS.md`
- `metalForge/ABSORPTION_MANIFEST.md`, `metalForge/README.md`
- `whitePaper/STUDY.md`, `whitePaper/README.md`
- `whitePaper/experiments/008_anderson_localization.md`
