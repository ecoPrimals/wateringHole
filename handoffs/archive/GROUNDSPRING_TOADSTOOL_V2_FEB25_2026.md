# groundSpring → ToadStool Handoff V2: Comprehensive Absorption Request

**Date:** February 25, 2026
**From:** groundSpring (measurement noise characterization biome)
**To:** ToadStool / BarraCUDA team
**Phase:** 1a complete — 88/88 validation checks, 83 unit tests, 99.7% library coverage
**License:** AGPL-3.0-or-later

---

## Summary

groundSpring is the reality layer in ecoPrimals: noise characterization,
inverse problems, and error propagation across scientific domains. This
handoff documents what ToadStool needs to absorb, what already works, what
we learned about barracuda's API during integration, and what the 19-paper
extension queue needs from ToadStool.

### What Changed Since V1

1. **Barracuda Tier A infrastructure complete** — `pearson_r` wired to
   `barracuda::stats::pearson_correlation` with NaN-safe fallback
2. **Variance semantics documented** — population vs sample std dev reconciled
3. **Three-tier control matrix** — per-experiment CPU/GPU/metalForge status
4. **19 queued papers** mapped to barracuda primitives with blocker analysis
5. **baseCamp faculty briefings** — 5 faculty, 19 papers, all open data
6. **Data provenance complete** — all 5 benchmark JSONs have DOIs, SRA accessions,
   `data_origin`, `prng_algorithm` fields

---

## Part 1: What groundSpring Already Consumes from BarraCUDA

### CPU-Only Imports (no `gpu` feature required)

| Import | groundSpring Usage | Works? |
|--------|-------------------|:------:|
| `barracuda::stats::pearson_correlation` | `stats::pearson_r` via `#[cfg(feature = "barracuda")]` | **Yes** |

### Observations from Integration

1. **NaN handling**: `pearson_correlation` returns `Ok(NaN)` when one variable
   has zero variance. groundSpring wraps with `if r.is_nan() { 0.0 } else { r }`.
   *Suggestion*: Consider returning `Err` for degenerate inputs, or document
   the NaN behavior in `pearson_correlation`'s doc comment.

2. **Variance semantics**: `barracuda::stats` uses sample variance (÷ N−1);
   groundSpring uses population variance (÷ N) for RMSE decomposition.
   groundSpring now provides both `std_dev` (population) and `sample_std_dev`
   (Bessel-corrected). This is not a bug — just a semantic difference that
   consumers must be aware of.

3. **Build clean**: `cargo build --features barracuda` with `default-features = false`
   compiles clean against barracuda 0.2.0 (CPU-only, no GPU deps).
   Dependencies: `num-traits`, `half`, `rayon`, `rand`, `serde`, `serde_json`,
   `tokio`, `async-trait`, `log`, `tracing`, `etcetera`, `akida-driver`,
   `toadstool-core`.

4. **Feature gate pattern**: groundSpring uses the pattern:
   ```rust
   #[cfg(feature = "barracuda")]
   { barracuda::stats::pearson_correlation(x, y).unwrap_or(0.0) }
   #[cfg(not(feature = "barracuda"))]
   { /* local implementation */ }
   ```
   This preserves the CPU reference as the default and validation target.

---

## Part 2: What ToadStool Needs to Absorb

### Priority 1: Tier C New Kernels (2 shaders, WGSL written)

These are the highest-value absorption items. WGSL prototypes are complete
and CPU-validated.

#### `ops::mc_et0_propagate_f64` — Monte Carlo FAO-56

**Purpose**: Batched Monte Carlo through the FAO-56 Penman-Monteith equation
chain. N parallel invocations, each perturbing base weather inputs with
normally-distributed sensor noise and computing one ET₀ sample.

**File**: `groundSpring/metalForge/shaders/mc_et0_propagate.wgsl` (133 lines)

**Binding Layout**:

| Binding | Type | Contents | Size |
|---------|------|----------|------|
| 0 | `storage<read>` | Base inputs: `[tmax,tmin,rhmax,rhmin,wind,sun,lat,alt,doy]` | 9 × f64 |
| 1 | `storage<read>` | Uncertainties: `[σ_tmax,σ_tmin,σ_rh,σ_rh,σ_wind_frac,σ_sun_frac]` | 6 × f64 |
| 2 | `storage<read>` | PRNG seeds: xoshiro state per invocation | N × 4 × u32 |
| 3 | `storage<read_write>` | Output: one ET₀ per sample | N × f64 |

**Dispatch**: `(ceil(N/64), 1, 1)` with workgroup `(64, 1, 1)`

**CPU Reference**: `validate-fao56` binary — 15/15 PASS

**Equation chain inside kernel**: `saturation_vp → slope_vp → psychrometric →
net_shortwave → net_longwave → reference_et0`. All sub-functions are
embedded in the kernel (not standalone ops).

**f64 requirement**: Statistical precision demands f64. The ET₀ equation
chain accumulates rounding errors across 6 nonlinear sub-functions;
f32 produces unacceptable drift at the 4th decimal.

#### `ops::batched_multinomial_f64` — Parallel Rarefaction

**Purpose**: Run `replicates × depths` multinomial draws in parallel for
rarefaction analysis. Each invocation handles one replicate at one depth.

**File**: `groundSpring/metalForge/shaders/batched_multinomial.wgsl` (67 lines)

**Binding Layout**:

| Binding | Type | Contents | Size |
|---------|------|----------|------|
| 0 | `storage<read>` | Cumulative abundances | n_taxa × f64 |
| 1 | `storage<read>` | Config: `[n_taxa, depth, base_seed]` | 3 × u32 |
| 2 | `storage<read_write>` | Output counts | replicates × n_taxa × u32 |

**Dispatch**: `(ceil(replicates/64), 1, 1)` with workgroup `(64, 1, 1)`

**CPU Reference**: `validate-rarefaction` binary — 15/15 PASS

**Algorithm**: For each of `depth` draws: generate uniform random via
xoshiro, binary search cumulative abundance array, increment taxon count.

### Priority 2: Tier A Rewire (6 functions, GPU ops exist)

These functions can be wired to existing barracuda GPU ops once
groundSpring has the `gpu` feature enabled.

| groundSpring Function | barracuda GPU Op | Shader | Rewire Pattern |
|-----------------------|-----------------|--------|----------------|
| `stats::rmse` | `norm_reduce_f64` | `norm_reduce_f64.wgsl` | RMSE = L2(obs−mod) / √n |
| `stats::mbe` | `sum_reduce_f64` | `sum_reduce_f64.wgsl` | MBE = mean(mod − obs) |
| `stats::r_squared` | `variance_f64_wgsl` + reduce | `variance_f64.wgsl` | R² = 1 − SS_res/SS_tot |
| `stats::index_of_agreement` | `fused_map_reduce_f64` | `fused_map_reduce_f64.wgsl` | Map: abs diffs, Reduce: sum |
| `stats::hit_rate` | `fused_map_reduce_f64` | `fused_map_reduce_f64.wgsl` | Map: binary agree, Reduce: mean |
| `rarefaction::shannon_diversity` | `fused_map_reduce_f64` (Shannon) | `fused_map_reduce_f64.wgsl` | H' = −Σ(p·ln p) |

**Blocker**: These ops require the `gpu` feature on barracuda, which requires
a GPU adapter. groundSpring cannot test these without GPU hardware access
through the barracuda API.

### Priority 3: Tier B Adapt (3 items, need alignment)

| Item | barracuda Target | Action | Blocker |
|------|-----------------|--------|---------|
| PRNG alignment | `PrngXoshiro` | Replace xorshift64 → xoshiro256** | Baselines must be regenerated |
| Grid search dispatch | Parallel 3D grid | One invocation per grid cell | New dispatch pattern needed |
| Batched multinomial | `PrngXoshiro` + binary search | Combine PRNG + search in one kernel | Tier C kernel above |

---

## Part 3: Three-Tier Control Matrix

| # | Experiment | CPU | GPU | metalForge |
|---|-----------|:---:|:---:|:----------:|
| 1 | Sensor noise (36 checks) | **PASS** | Tier A pending | After GPU |
| 2 | Observation gap (13 checks) | **PASS** | Tier A pending | After GPU |
| 3 | Error propagation (15 checks) | **PASS** | Tier C pending | After GPU |
| 4 | Sequencing noise (15 checks) | **PASS** | Tier C pending | After GPU |
| 5 | Seismic inversion (9 checks) | **PASS** | Tier B pending | After GPU |
| **Total** | **88/88** | **0/88** | **0/88** |

---

## Part 4: Faculty Extension Queue — GPU Requirements

19 queued papers across 6 faculty, all using open data.

### Existing barracuda primitives that cover queued papers

| barracuda Primitive | Papers Covered | Status |
|--------------------|---------------|--------|
| `GillespieGpu` | 9, 10, 11 (Waters c-di-GMP) | Exists |
| `BatchedOdeRK4` | 9, 10 (ODE sweeps) | Exists |
| `BatchedEighGpu` | 10 (bifurcation), 15-18 (spectral) | Exists |
| `SmithWatermanGpu` | 20, 21 (R. Anderson metagenomics) | Exists |
| `BrayCurtisF64` | 20, 21 (community dissimilarity) | Exists |
| `PangenomeClassifyGpu` | 20, 21 (taxonomy) | Exists |
| Anderson 1D/2D/3D | 15-18 (Kachkovskiy spectral theory) | Exists |
| Lanczos eigensolve | 15-18 (spectral theory) | Exists |
| Almost-Mathieu | 16 (quasiperiodic operators) | Exists |
| Level statistics | 15-18 (Wigner-Dyson vs Poisson) | Exists |
| `bootstrap_*` | 7, 12, 13 (error estimation) | Exists (CPU) |

### New primitives needed for queued papers

| Primitive | Papers | Priority | Notes |
|-----------|--------|----------|-------|
| **FFT (real, complex)** | 6, 7 (Bazavov spectral) | **HIGH** | Shared need with hotSpring (PPPM) |
| **RAWR weighted resampling** | 12, 13 (Liu) | MEDIUM | Embarrassingly parallel |
| **3D grid dispatch** | 5, 8 (seismic + freeze-out) | MEDIUM | Standard GPU pattern |

### Papers blocked by missing primitives

- **Papers 6, 7 (Bazavov)**: Blocked by FFT gap. These are the highest-precision
  papers in the queue (subpercent lattice QCD). FFT is also needed by hotSpring
  for PPPM electrostatics — **joint priority**.
- **Papers 4, 20-21**: Blocked by `batched_multinomial` Tier C absorption (above).

### Papers GPU-ready (barracuda primitives exist)

Papers 9, 10, 12, 14, 15, 16 can proceed to GPU tier once CPU baselines
are established. No new barracuda primitives needed.

---

## Part 5: Lessons Learned for ToadStool Evolution

### 1. NaN propagation in CPU stats

`pearson_correlation` returns `Ok(NaN)` for zero-variance input. This is
mathematically correct (0/0) but surprising for consumers expecting `Err`.
**Recommendation**: Add a `#[must_use]` doc note or return `Err(InvalidInput)`
for degenerate cases. Other CPU stats functions (`covariance`, `correlation_matrix`)
likely have the same behavior.

### 2. Variance semantics should be explicit

barracuda `stats` uses sample variance (÷ N−1) everywhere, which is correct
for inferential statistics but wrong for population metrics (RMSE decomposition,
Shannon diversity normalization). **Recommendation**: Consider adding
`variance_population` alongside `variance` in barracuda stats, or at minimum
document the Bessel correction clearly.

### 3. Feature gate ergonomics

The `default-features = false` pattern works well for CPU-only consumers.
However, there's no way to use GPU ops without also pulling in `wgpu`,
`pollster`, and `bytemuck` as deps. **Recommendation**: Consider a `gpu-stats`
feature that provides GPU reduce/map ops without the full tensor/pipeline API,
for consumers that only need statistical reductions.

### 4. PRNG alignment is a cross-spring concern

groundSpring, wetSpring, and potentially neuralSpring all have local PRNGs.
Aligning to `PrngXoshiro` requires regenerating baselines. **Recommendation**:
Provide a `barracuda::prng::Xoshiro256` CPU-side wrapper that produces
identical streams to the WGSL kernel, so springs can regenerate baselines
before GPU testing.

### 5. f64 precision is non-negotiable for statistics

groundSpring's FAO-56 equation chain, Shannon diversity, and RMSE decomposition
all require f64. The f32 transcendental polyfill pipeline (`compile_shader_f64()`)
is essential. **Recommendation**: Ensure the polyfill covers `exp`, `log`, `sqrt`,
`pow`, `sin`, `cos` at f64 — all are used in the `mc_et0_propagate` shader.

### 6. Validation harness convergence

barracuda's `validation.rs` and groundSpring's `validate.rs` implement the same
API surface (`check_abs`, `check_rel`, `check_upper`, `check_lower`, `check_bool`,
`finish`). groundSpring's was developed independently following the hotSpring
pattern. **Recommendation**: groundSpring should migrate to `barracuda::validation::ValidationHarness`
when the feature is enabled, to reduce code duplication.

### 7. Tolerance constants should be shared

barracuda's `tolerances.rs` defines named constants (`REDUCTION_SUM`, `LINALG_MATMUL`,
`BIO_HMM`, etc.). groundSpring's tolerance values are currently inline.
**Recommendation**: Add `STATS_RMSE`, `STATS_PEARSON`, `STATS_SHANNON` to
barracuda's tolerance constants for cross-spring consistency.

---

## Part 6: What NOT to Duplicate

BarraCUDA primitives that exist and MUST NOT be reimplemented in groundSpring:

| Category | Primitives |
|----------|-----------|
| Reduce | `norm_reduce_f64`, `sum_reduce_f64`, `variance_f64_wgsl` |
| Fused | `fused_map_reduce_f64` (MapOp::Shannon, etc.) |
| Correlation | `pearson_correlation`, `covariance`, `correlation_matrix` |
| Bootstrap | `bootstrap_mean`, `bootstrap_std`, `bootstrap_ci` |
| Distribution | `norm_cdf`, `norm_pdf`, `norm_ppf` |
| Special | `erf`, `erfc`, `gamma`, `ln_gamma`, `beta`, `digamma` |
| Bio | `SmithWatermanGpu`, `BrayCurtisF64`, `PangenomeClassifyGpu` |
| Spectral | Anderson 1D/2D/3D, Lanczos, Almost-Mathieu, level statistics |
| ODE | `BatchedOdeRK4`, `GillespieGpu` |
| PRNG | `PrngXoshiro` |
| Optimization | `nelder_mead_gpu` |

groundSpring's local implementations are **validation references** only.
When barracuda has the op, groundSpring delegates.

---

## Part 7: Handoff Checklist

### Tier C Shader Absorption (mc_et0_propagate)

- [x] WGSL file: `metalForge/shaders/mc_et0_propagate.wgsl` (133 lines)
- [x] CPU reference passes: `validate-fao56` 15/15 PASS
- [x] Binding layout documented (4 bindings, f64 throughout)
- [x] Dispatch geometry: `(ceil(N/64), 1, 1)`, workgroup `(64, 1, 1)`
- [x] f64 precision verified (6 nonlinear sub-functions, f32 drift unacceptable)
- [x] Handoff document: this file
- [ ] GPU tolerance comparison: pending absorption

### Tier C Shader Absorption (batched_multinomial)

- [x] WGSL file: `metalForge/shaders/batched_multinomial.wgsl` (67 lines)
- [x] CPU reference passes: `validate-rarefaction` 15/15 PASS
- [x] Binding layout documented (3 bindings)
- [x] Dispatch geometry: `(ceil(replicates/64), 1, 1)`, workgroup `(64, 1, 1)`
- [x] f64 precision verified (cumulative probability binary search)
- [x] Handoff document: this file
- [ ] GPU tolerance comparison: pending absorption

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --all-targets` | PASS (0 warnings) |
| `cargo clippy --features barracuda` | PASS (0 warnings) |
| `cargo doc --no-deps` | PASS |
| `cargo test` | 83/83 PASS (+ 1 doc test) |
| `cargo test --features barracuda` | 83/83 PASS |
| Validation binaries | 88/88 PASS |
| Library line coverage | 99.7% |
| Unsafe code | Forbidden |
| License | AGPL-3.0-or-later |
| Open data | All 24 papers use open data (zero proprietary) |

---

*License: AGPL-3.0-or-later. All discoveries, code, and documentation are
sovereign to the ecoPrimals ecosystem.*
