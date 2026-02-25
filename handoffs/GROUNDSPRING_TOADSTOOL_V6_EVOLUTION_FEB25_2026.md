# groundSpring → ToadStool Handoff V6: Complete Rewiring & Cross-Spring Evolution

**Date**: February 25, 2026
**From**: groundSpring (validation spring — measurement noise characterization)
**To**: ToadStool / BarraCUDA team
**Supersedes**: V5 (code audit + catch-up)
**ToadStool baseline**: Sessions 51–62 + DF64 expansion (Feb 24–25, 2026)

---

## Summary

V6 reports **complete rewiring** of groundSpring to modern barracuda.
All CPU-delegatable functions are wired. Performance benchmarks confirm
negligible overhead. Cross-spring shader provenance is fully documented.

### What Changed Since V5

- **5 new CPU delegations**: `covariance`, `norm_cdf`, `norm_ppf`,
  `chi2_statistic`, `analytical_localization_length`
- **Total**: 11 active delegations (was 6 at V4)
- **122 unit tests** + 119/119 validation checks PASS in all 3 modes
- **Benchmarks**: <2% overhead for compute-heavy binaries
- **Cross-spring evolution** documented with full provenance

### Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all -- --check` | Clean |
| `cargo clippy --all-targets -- -W clippy::pedantic -W clippy::nursery` | 0 warnings (all features) |
| `cargo test --workspace` (local) | 122/122 PASS + 1 doc |
| `cargo test --workspace --features barracuda-gpu` | 122/122 PASS + 1 doc |
| 8 validation binaries (local) | 119/119 PASS |
| 8 validation binaries (barracuda-gpu) | 119/119 PASS |

---

## Part 1: Complete Delegation Inventory

### 11 Active Delegations

| # | groundSpring Function | BarraCUDA Target | Gate | Origin |
|---|----------------------|-----------------|------|--------|
| 1 | `stats::pearson_r` | `stats::pearson_correlation` | `barracuda` | hotSpring |
| 2 | `stats::spearman_r` | `stats::correlation::spearman_correlation` | `barracuda` | wetSpring S57 |
| 3 | `stats::sample_std_dev` | `stats::correlation::std_dev` | `barracuda` | hotSpring |
| 4 | `stats::covariance` | `stats::correlation::covariance` | `barracuda` | hotSpring |
| 5 | `stats::norm_cdf` | `stats::norm_cdf` | `barracuda` | neuralSpring |
| 6 | `stats::norm_ppf` | `stats::norm_ppf` | `barracuda` | neuralSpring |
| 7 | `stats::chi2_statistic` | `stats::chi2_decomposed` | `barracuda` | wetSpring V18 |
| 8 | `bootstrap::bootstrap_mean` | `stats::bootstrap_mean` | `barracuda` | hotSpring |
| 9 | `anderson::lyapunov_exponent` | `spectral::lyapunov_exponent` | `barracuda-gpu` | hotSpring |
| 10 | `anderson::lyapunov_averaged` | `spectral::lyapunov_averaged` | `barracuda-gpu` | hotSpring |
| 11 | `anderson::analytical_localization_length` | `special::anderson_transport::localization_length` | `barracuda` | hotSpring |

### GPU-Pending (6 — need GPU adapter, not CPU delegation)

| Function | BarraCUDA GPU Op | WGSL Shader |
|----------|-----------------|-------------|
| `stats::rmse` | `NormReduceF64::l2` | `norm_reduce_f64.wgsl` |
| `stats::mbe` | `SumReduceF64::mean` | `sum_reduce_f64.wgsl` |
| `stats::r_squared` | `VarianceReduceF64` + reduce | `variance_reduce_f64.wgsl` |
| `stats::index_of_agreement` | `FusedMapReduceF64` | `fused_map_reduce_f64.wgsl` |
| `stats::hit_rate` | `FusedMapReduceF64` | `fused_map_reduce_f64.wgsl` |
| `rarefaction::shannon_diversity` | `FusedMapReduceF64::shannon_entropy` | `fused_map_reduce_f64.wgsl` |

### Stays Local (no GPU benefit)

| Function | Reason |
|----------|--------|
| `decompose::*` | 2-3 scalar ops |
| `seismic::haversine_km` | Single scalar trig |
| `seismic::travel_time_1d` | One sqrt + division |
| `validate::ValidationHarness` | Harness, not compute |
| `prng::Xorshift64` | CPU reference (Phase 2b aligns to xoshiro) |

---

## Part 2: What barracuda Should Absorb from groundSpring

### Priority 1: `batched_multinomial.wgsl` (WGSL ready)

112-line production shader in `metalForge/shaders/`. Batched multinomial
sampling for rarefaction — binary search over cumulative probabilities with
per-replicate PRNG state. No equivalent exists in barracuda.

**Use case**: GPU-scale rarefaction (100k+ replicates) for Exp 004
(sequencing depth analysis). Also useful for wetSpring metagenomics.

**Binding layout**: documented in `metalForge/ABSORPTION_MANIFEST.md`

### Priority 2: `rawr_weighted_mean_f64` kernel (spec only)

RAWR (Wang et al. 2021 ISMB) generates Dirichlet(1,...,1) weights via
normalized Exp(1) variates, then computes weighted dot product per replicate.
Embarrassingly parallel — each workgroup handles one replicate.

**CPU reference**: `bootstrap::rawr_mean` in groundSpring
**No barracuda equivalent exists.** Bootstrap_mean has both CPU and GPU
paths in barracuda, but RAWR uses a fundamentally different resampling
strategy (Bayesian bootstrap vs standard bootstrap).

### Priority 3: `mc_et0_propagate.wgsl` MC wrapper (WGSL ready)

149-line production shader. The FAO-56 equation chain itself is already
absorbed upstream (`BatchedElementwiseF64::fao56_et0_batch`), but the
Monte Carlo uncertainty propagation wrapper (Box-Muller perturbation +
batch dispatch) is the absorption target.

### Priority 4: PRNG alignment (Phase 2b)

groundSpring uses `Xorshift64` (Marsaglia 2003); barracuda uses
`xoshiro128**`. Different generators produce different streams, preventing
bitwise-identical CPU/GPU comparisons for stochastic experiments.

**Migration path**: Feature-gate PRNG, create `Xoshiro128` wrapper,
regenerate all baselines with compatible Python xoshiro implementation.

### Priority 5: `spectral::anderson` public API cleanup

The `anderson` submodule is private; `lyapunov_exponent` and
`lyapunov_averaged` are re-exported at `spectral::*`. This is
architecturally correct but confusing — groundSpring hit `E0603`
when trying `spectral::anderson::lyapunov_*`. Other springs using
`spectral::anderson` will hit the same issue.

**Recommendation**: Either make `anderson` public or document the
re-export pattern prominently in barracuda's module-level docs.

---

## Part 3: Cross-Spring Shader Evolution

### How groundSpring Benefits from Other Springs

| Origin Spring | What groundSpring Uses | Impact |
|--------------|----------------------|--------|
| **hotSpring** | Spectral theory (Lyapunov, Anderson transport), DF64 precision, core stats (pearson, std_dev, covariance, bootstrap) | Exp 008 GPU acceleration, f64-critical statistics on consumer GPUs |
| **wetSpring** | Shannon entropy GPU, Spearman correlation, chi-squared, Gillespie GPU, bio ODEs | Exp 004 GPU rarefaction, Exp 006 GPU SSA (future), model validation |
| **neuralSpring** | erf/erfc special functions (→ norm_cdf, norm_ppf), validation harness pattern | Confidence intervals, goodness-of-fit testing |
| **airSpring** | FAO-56 ET₀ batch op | Supersedes our Tier C shader |

### How Other Springs Benefit from groundSpring

| Contribution | Who Benefits | Status |
|-------------|-------------|--------|
| RAWR resampling spec | All springs (validated alternative to bootstrap) | Spec written, awaiting kernel |
| Batched multinomial WGSL | wetSpring (rarefaction), neuralSpring (sampling) | Production-ready |
| MC error propagation pattern | airSpring (sensor uncertainty), hotSpring (MC nuclear) | Documented |
| Noise labeling for ML | neuralSpring (training data) | Future |
| `f64::total_cmp` pattern | All springs (NaN-safe sorting) | Lesson documented |
| Centralized cast pattern | All springs (usize↔f64 safety) | Lesson documented |

### Cross-Pollination Graph

```
                    ┌─────────────┐
             ┌──────│  hotSpring   │──────┐
             │      │ (precision)  │      │
             │      └──────┬──────┘      │
             │             │DF64         │Spectral
             ▼             ▼             ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │neuralSpring│  │ BarraCUDA  │  │groundSpring│
    │  (ML/opt)  │──│  (shared)  │──│  (noise)   │
    └────────────┘  └──────┬─────┘  └────────────┘
             ▲             │             ▲
             │             │Bio          │Shannon
             │      ┌──────┴──────┐      │
             └──────│  wetSpring   │──────┘
                    │ (biology)    │
                    └─────────────┘
```

---

## Part 4: Performance Benchmarks

### Local vs BarraCUDA CPU Delegation (release mode, best-of-3)

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
For compute-heavy binaries (>500ms), delegation adds <2% overhead.
This confirms CPU delegation has negligible performance penalty.

### Rust vs Python (median of 3 trials)

| Experiment | Python (s) | Rust (s) | Speedup |
|------------|-----------|---------|---------|
| Exp 006: Signal Specificity | 26.2 | 0.85 | **30.9×** |
| Exp 007: RAWR Resampling | 4.4 | 0.60 | **7.3×** |
| Exp 008: Anderson Localization | 21.4 | 0.72 | **29.8×** |
| **Total** | **52.0** | **2.17** | **24.0×** |

---

## Part 5: Lessons for BarraCUDA Evolution

### 1. Private submodule re-exports need documentation

`barracuda::spectral::anderson` is private but re-exports at `spectral::*`.
groundSpring spent debugging time on `E0603`. Add a doc comment or make
the submodule public.

### 2. Seed convention divergence is a footgun

Local groundSpring: `base_seed + i` per realization.
Barracuda spectral: `base_seed + r * 1000` per realization.
Results diverge when feature gate is active. Document per-function.

### 3. RAWR is a valuable resampling primitive

Wang et al. 2021 RAWR (Bayesian bootstrap via Dirichlet weights) is
competitive or better than standard bootstrap across all our test cases.
Worth adding to `barracuda::stats` alongside `bootstrap_mean`.

### 4. `f64::total_cmp` replaces the `partial_cmp().unwrap_or()` antipattern

Rust stable has `f64::total_cmp` since 1.62. All NaN-safe float sorting
should use it. Eliminates an entire class of "comparison is always Equal"
bugs.

### 5. The `cpu-math` feature gate pattern works perfectly

groundSpring's `barracuda` feature (no gpu) compiles cleanly with the
`cpu-math` gate. No `wgpu` dependency pulled in. This is the correct
pattern for spring-local CPU delegation.

### 6. Centralized cast helpers prevent `#[allow]` proliferation

A `cast` module with `usize_f64`, `f64_usize`, `u64_f64` — each with
a safety argument in the doc comment — is cleaner than per-site
`#[allow(clippy::cast_precision_loss)]`.

### 7. Analytical vs numerical comparison tests need wide tolerances

`analytical_localization_length` (perturbative) differs from
`lyapunov_exponent` (numerical) by O(1) constant factors, especially
when PRNG differs. Tests comparing them need ratio tolerance (0.2..5.0)
not absolute tolerance.

---

## Part 6: Three-Tier Control Matrix (27 papers)

> See `specs/PAPER_REVIEW_QUEUE.md` for the full matrix. Summary:

| Tier | Description | Papers | Status |
|------|-------------|--------|--------|
| CPU | Rust matches Python | 8 experiments, 27 papers queued | **8/8 done** (119/119 PASS) |
| GPU | BarraCUDA GPU matches CPU | 6 GPU-pending reduce ops | Blocked on GPU adapter |
| metalForge | Cross-substrate agreement | Future | After GPU tier |

---

## Part 7: Files Changed Since V5

### New files
- `specs/CROSS_SPRING_EVOLUTION.md` — Cross-spring shader provenance
- `scripts/bench_barracuda_modes.sh` — Three-mode benchmark script
- This handoff (V6)

### Modified (code)
- `crates/groundspring/src/stats.rs` — `covariance`, `norm_cdf`, `norm_ppf`, `chi2_statistic` + 14 new tests
- `crates/groundspring/src/anderson.rs` — `analytical_localization_length` + 3 new tests

### Modified (docs)
- README.md, CHANGELOG.md, CONTRIBUTING.md, CONTROL_EXPERIMENT_STATUS.md
- specs/BARRACUDA_EVOLUTION.md, specs/BARRACUDA_REQUIREMENTS.md, specs/README.md
- specs/PAPER_REVIEW_QUEUE.md, specs/CROSS_SPRING_EVOLUTION.md
- metalForge/ABSORPTION_MANIFEST.md
- whitePaper/README.md, whitePaper/STUDY.md, whitePaper/METHODOLOGY.md
- whitePaper/experiments/README.md, whitePaper/experiments/008_anderson_localization.md
- whitePaper/baseCamp/anderson.md

---

## Handoff Checklist

- [x] All 11 CPU delegations wired and tested
- [x] 122/122 unit tests + 119/119 validation checks (local + barracuda-gpu)
- [x] Clippy pedantic+nursery: 0 warnings (all feature combinations)
- [x] Benchmarks: <2% overhead for compute-heavy binaries
- [x] Cross-spring evolution documented
- [x] Absorption targets specified (3 shaders + RAWR kernel)
- [x] Lessons for barracuda team documented (7 items)
- [x] Three-tier control matrix complete for 27 papers
- [x] All stale references fixed (delegation counts, test counts, paths)
- [x] V5 superseded

---

*groundSpring Phase 2a: complete. Ready for Phase 2b (PRNG alignment) and Phase 3 (full GPU pipeline).*
