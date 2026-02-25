# groundSpring → ToadStool Handoff V4

**Date**: February 25, 2026
**From**: groundSpring (validation spring)
**To**: ToadStool / BarraCUDA team
**Supersedes**: V3 (archived)
**ToadStool baseline**: Sessions 51–62 (Feb 24, 2026)

## Summary

V4 reports completion of Phase 1c (paper queue experiment buildout) and Phase 2a
(barracuda CPU delegation + performance benchmarks). Key changes since V3:

- **3 new experiments complete** — Exp 006 (Gillespie SSA), Exp 007 (RAWR bootstrap),
  Exp 008 (Anderson localization). Total: 119/119 PASS across 8 validation binaries.
- **3 new barracuda delegations** — `bootstrap_mean` (CPU), `lyapunov_exponent` +
  `lyapunov_averaged` (barracuda-gpu). Total: 6 functions delegated.
- **New feature gate** — `barracuda-gpu` enables `barracuda/gpu` for spectral module.
- **Performance benchmarks** — Pure Rust is **24× faster** than Python (52s → 2.2s).
  Signal Specificity 30.9×, Anderson Localization 29.8×, RAWR 7.3×.
- **3 new Rust modules** — `gillespie`, `bootstrap`, `anderson` (18 new unit tests).
- **whitePaper/experiments/** created — 8 per-experiment summary documents.

---

## Part 1: What groundSpring Now Consumes from BarraCUDA

### CPU-delegated (6 total — 3 new since V3)

| groundSpring function | BarraCUDA target | Feature gate | Status |
|---|---|---|---|
| `stats::pearson_r` | `stats::pearson_correlation` | `barracuda` | Wired (V2) |
| `stats::spearman_r` | `stats::correlation::spearman_correlation` | `barracuda` | Wired (V3) |
| `stats::sample_std_dev` | `stats::correlation::std_dev` | `barracuda` | Wired (V3) |
| `bootstrap::bootstrap_mean` | `stats::bootstrap_mean` | `barracuda` | **NEW** — Result struct mapping |
| `anderson::lyapunov_exponent` | `spectral::anderson::lyapunov_exponent` | `barracuda-gpu` | **NEW** — transfer matrix |
| `anderson::lyapunov_averaged` | `spectral::anderson::lyapunov_averaged` | `barracuda-gpu` | **NEW** — multi-realization |

### GPU-ready (Tier A pending adapter — unchanged from V3)

| groundSpring function | BarraCUDA GPU op | Shader |
|---|---|---|
| `stats::rmse` | `NormReduceF64::l2` | `norm_reduce_f64.wgsl` |
| `stats::mbe` | `SumReduceF64::mean` | `sum_reduce_f64.wgsl` |
| `stats::r_squared` | `VarianceReduceF64` + reduce | `variance_reduce_f64.wgsl` |
| `stats::index_of_agreement` | `FusedMapReduceF64` | `fused_map_reduce_f64.wgsl` |
| `stats::hit_rate` | `FusedMapReduceF64` | `fused_map_reduce_f64.wgsl` |
| `rarefaction::shannon_diversity` | `FusedMapReduceF64::shannon_entropy` | `fused_map_reduce_f64.wgsl` |

### Absorbed upstream (unchanged from V3)

| Original Tier C item | BarraCUDA op | Notes |
|---|---|---|
| `mc_et0_propagate_f64` | `BatchedElementwiseF64::fao56_et0_batch` | FAO-56 equation chain as `Op::Fao56Et0` |

---

## Part 2: What Still Needs ToadStool Action

### Priority 1: Batched Multinomial (Tier C — production WGSL exists)

Unchanged from V3. Production-quality shader in `metalForge/shaders/batched_multinomial.wgsl`
(112 lines). Required for Exp 004 GPU validation and R. Anderson papers (#20-21).

### Priority 2: RAWR Weighted Resampling Kernel (NEW — Tier C)

`bootstrap::rawr_mean` has no barracuda equivalent. RAWR resampling (Wang et al. 2021)
uses Dirichlet-distributed weights — embarrassingly parallel, suitable for GPU.

**Proposed API**: `ops::rawr_weighted_mean_f64(data, weights, n_bootstrap, seed) → BootstrapCI`

**CPU reference**: `groundspring::bootstrap::rawr_mean` (Exp 007: 11/11 PASS)

### Priority 3: PRNG Alignment (Tier B — unchanged)

Xorshift64 ↔ xoshiro128** stream mismatch. Migration roadmap in
`specs/BARRACUDA_EVOLUTION.md` §PRNG Alignment.

### Priority 4: Grid Search 3D Dispatch (Tier B — unchanged)

`seismic::grid_search_inversion` — needs workgroup dispatch + min-reduce.

### Priority 5: Gillespie CPU Fallback (NEW — informational)

`barracuda::ops::bio::GillespieGpu` is GPU-only. groundSpring's
`gillespie::birth_death_ssa` is the CPU reference (Exp 006: 12/12 PASS).
If a CPU fallback is desired in barracuda, groundSpring's implementation
can serve as the reference.

---

## Part 3: New Modules for Absorption Consideration

### `gillespie` module

| Function | Signature | Notes |
|---|---|---|
| `birth_death_ssa` | `(alpha, beta, initial, t_max, seed) → Trajectory` | Exact SSA with `Trajectory { times, states }` |
| `steady_state_mean` | `(alpha, beta) → f64` | Analytical: α/β |
| `time_averaged_mean` | `(trajectory) → f64` | Weighted by inter-event times |
| `time_averaged_variance` | `(trajectory) → f64` | Weighted second moment |

**barracuda target**: `GillespieGpu::simulate()` (GPU path exists, no CPU fallback).

### `bootstrap` module

| Function | Signature | Notes |
|---|---|---|
| `bootstrap_mean` | `(data, n_reps, confidence, seed) → BootstrapResult` | **Delegated** to barracuda |
| `rawr_mean` | `(data, n_reps, confidence, seed) → BootstrapResult` | Local (no barracuda RAWR) |

**barracuda target**: `stats::bootstrap_mean` (CPU done). RAWR kernel needed.

### `anderson` module

| Function | Signature | Notes |
|---|---|---|
| `anderson_potential` | `(n_sites, disorder, seed) → Vec<f64>` | Uniform disorder |
| `lyapunov_exponent` | `(potential, energy) → f64` | **Delegated** to barracuda-gpu |
| `localization_length` | `(gamma) → f64` | ξ = 1/γ (stays local) |
| `lyapunov_averaged` | `(n, W, E, n_real, seed) → f64` | **Delegated** to barracuda-gpu |

**barracuda target**: `spectral::anderson::*` (requires `barracuda/gpu` feature).

---

## Part 4: Three-Tier Control Matrix

| # | Experiment | CPU (119/119) | GPU | metalForge |
|---|-----------|:-------------:|:---:|:----------:|
| 1 | Sensor noise decomposition | **36/36 PASS** | Pending (Tier A) | — |
| 2 | Observation gap | **13/13 PASS** | Pending (Tier A) | — |
| 3 | Error propagation FAO-56 | **15/15 PASS** | Pending (adapter) | — |
| 4 | Sequencing noise | **15/15 PASS** | Blocked (Tier C: multinomial) | — |
| 5 | Seismic inversion | **9/9 PASS** | Blocked (Tier B: grid search) | — |
| 6 | Signal specificity | **12/12 PASS** | **Ready** (`GillespieGpu`) | — |
| 7 | RAWR resampling | **11/11 PASS** | Ready (embarrassingly parallel) | — |
| 8 | Anderson localization | **8/8 PASS** | **Ready** (`spectral::anderson`) | — |

---

## Part 5: Performance Benchmarks — Rust vs Python

| Experiment | Python (s) | Rust (s) | Speedup |
|---|---|---|---|
| Exp 006: Signal Specificity (Gillespie SSA) | 26.2 | 0.85 | **30.9×** |
| Exp 007: RAWR Resampling (bootstrap) | 4.4 | 0.60 | **7.3×** |
| Exp 008: Anderson Localization (transfer matrix) | 21.4 | 0.72 | **29.8×** |
| **Total** | **52.0** | **2.17** | **24.0×** |

The 7.3× RAWR speedup (vs 30× for others) reflects NumPy's vectorized array
operations — RAWR's inner loop is a weighted dot product that NumPy handles
efficiently. Gillespie and Anderson involve per-step branching that Python
cannot vectorize. **GPU dispatch will further accelerate all three.**

Benchmark script: `scripts/bench_rust_vs_python.py`
JSON results: `data/bench_rust_vs_python.json`

---

## Part 6: V3 Issues — Resolution Status

| V3 Issue | Status |
|---|---|
| 1. NaN propagation in `pearson_correlation` | Resolved (V2) |
| 2. Variance semantics | **RESOLVED** (V3) — `population_variance()` |
| 3. Feature gate ergonomics | **EVOLVED** — now two gates: `barracuda` (CPU) and `barracuda-gpu` (spectral) |
| 4. PRNG alignment | Open — migration roadmap documented |
| 5. f64 precision | Confirmed — all delegations use f64 |
| 6. ValidationHarness convergence | Stable — both APIs match |
| 7. Shared tolerance constants | Open |

---

## Part 7: What NOT to Duplicate

All items from V3 plus:

| Primitive | Module | Why |
|---|---|---|
| Bootstrap (CPU) | `stats::bootstrap_mean` | groundSpring delegates |
| Anderson lyapunov | `spectral::anderson` | groundSpring delegates |
| GillespieGpu | `ops::bio::gillespie` | GPU path exists |
| BatchedOdeRK4 + bio ODEs | `numerical::ode_bio` | 5 ODE systems ready |

---

## Part 8: Faculty Paper Queue — GPU Readiness Update

**GPU-ready papers** (barracuda primitives exist, CPU baseline complete):

| Paper | Experiment | GPU primitive | Speedup opportunity |
|---|---|---|---|
| #9 Massie c-di-GMP | Exp 006 (12/12) | `GillespieGpu` | 30.9× (CPU vs Python) → further with GPU |
| #15 Bourgain-Kachkovskiy | Exp 008 (8/8) | `spectral::anderson` + `BatchIprGpu` | 29.8× (CPU vs Python) → further with GPU |
| #12 Wang RAWR | Exp 007 (11/11) | Embarrassingly parallel | 7.3× → GPU batch dispatch |

**GPU-ready but CPU queued**: #10, #11, #14, #16 (barracuda ops exist, need CPU baseline first)

**GPU-blocked**: #6-7 (FFT gap), #4/20-21 (batched multinomial Tier C)

---

## Part 9: Insights for ToadStool Evolution

### RAWR Weighted Resampling

RAWR (Wang et al. 2021) generates Dirichlet-distributed weights w_i ~ Exp(1),
normalizes to sum=1, then computes weighted mean Σ(w_i × x_i). This is
embarrassingly parallel and a natural GPU kernel:

```
@compute @workgroup_size(64, 1, 1)
fn rawr_resample(@builtin(global_invocation_id) gid: vec3<u32>) {
    // 1. Generate n Exp(1) variates via -ln(U) from xoshiro PRNG
    // 2. Normalize weights to sum=1
    // 3. Compute weighted mean
    // 4. Store result for this bootstrap replicate
}
```

Dispatch: `(ceil(n_bootstrap / 64), 1, 1)`. Each invocation does one replicate.
This is the same pattern as `batched_multinomial.wgsl`.

### Gillespie CPU Fallback

groundSpring's `gillespie::birth_death_ssa` is a clean, tested CPU
implementation of exact SSA. If barracuda wants a CPU fallback for
`GillespieGpu` (for testing or non-GPU environments), this implementation
is a validated reference (12/12 checks, 5 unit tests, 30.9× faster than Python).

### Feature Gate Pattern

The two-gate pattern (`barracuda` for CPU-available ops, `barracuda-gpu` for
GPU-feature-gated ops) works well. ToadStool may want to consider making
`spectral::anderson` CPU functions available without the `gpu` feature,
since `lyapunov_exponent` and `lyapunov_averaged` are pure CPU.

---

## Part 10: groundSpring Quality Gates

| Gate | Result |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --all-targets` | PASS (0 warnings) |
| `cargo clippy --features barracuda` | PASS (0 warnings) |
| `cargo doc --no-deps` | PASS |
| `cargo test` | 108/108 PASS (+ 1 doc test) |
| `cargo test --features barracuda` | 108/108 PASS |
| Validation binaries | **119/119 PASS** across 8 binaries |
| Library line coverage | 99.7% |
| Unsafe code | Forbidden (workspace lint) |
| Max file size | <1000 lines per file |
| SPDX headers | All `.rs` files |
| License | AGPL-3.0-or-later |
| Open data | All 24 papers use public repositories |
| Python tests | 34/34 PASS (`pytest`) |
| Performance | 24× faster than Python |

---

## Handoff Checklist

- [x] 3 new experiments complete (Exp 006-008): 31 new checks, 18 new unit tests
- [x] `bootstrap_mean` wired to barracuda CPU (`#[cfg(feature = "barracuda")]`)
- [x] `lyapunov_exponent` + `lyapunov_averaged` wired to barracuda-gpu
- [x] `barracuda-gpu` feature gate added to Cargo.toml
- [x] Performance benchmarks: 24× faster than Python (3 experiments)
- [x] RAWR kernel gap documented as new Priority 2
- [x] Gillespie CPU reference offered for barracuda fallback
- [x] Three-tier control matrix updated (119/119 CPU, 8 experiments)
- [x] Faculty paper queue GPU readiness updated
- [x] whitePaper/experiments/ created (8 documents)
- [x] All quality gates passing
- [x] V3 archived

---

## Files Changed Since V3

### New files
- `crates/groundspring/src/gillespie.rs` — Gillespie SSA module
- `crates/groundspring/src/bootstrap.rs` — Bootstrap + RAWR module
- `crates/groundspring/src/anderson.rs` — Anderson localization module
- `crates/groundspring-validate/src/validate_signal_specificity.rs`
- `crates/groundspring-validate/src/validate_rawr.rs`
- `crates/groundspring-validate/src/validate_anderson.rs`
- `control/signal_specificity/` — Python baseline + benchmark JSON
- `control/rawr_resampling/` — Python baseline + benchmark JSON
- `control/anderson_localization/` — Python baseline + benchmark JSON
- `scripts/bench_rust_vs_python.py` — Performance benchmark
- `data/bench_rust_vs_python.json` — Benchmark results
- `whitePaper/experiments/*.md` — 8 experiment summaries

### Modified files
- `crates/groundspring/Cargo.toml` — `barracuda-gpu` feature
- `crates/groundspring/src/lib.rs` — 3 new module declarations
- `crates/groundspring-validate/Cargo.toml` — 3 new `[[bin]]` entries
- All documentation files updated with current counts
