# groundSpring → ToadStool Handoff V3

**Date**: February 25, 2026
**From**: groundSpring (validation spring)
**To**: ToadStool / BarraCUDA team
**Supersedes**: V2 (archived), V1 (archived)
**ToadStool baseline**: Sessions 51–62 (Feb 24, 2026)

## Summary

V3 catches groundSpring up to ToadStool's S51–S62 absorption wave. Key changes
since V2:

- **FAO-56 ET₀ superseded** — `BatchedElementwiseF64::fao56_et0_batch()` exists
  in barracuda (absorbed ~S49). Our `mc_et0_propagate.wgsl` Tier C prototype is
  no longer needed for the equation chain itself.
- **Shannon entropy GPU-ready** — `FusedMapReduceF64::shannon_entropy()` convenience
  method exists. Tier A rewire for `rarefaction::shannon_diversity` is unblocked.
- **Population variance resolved** — `VarianceReduceF64::population_variance()` and
  `population_std()` now exist. Our variance semantics mismatch (V2 Part 5, item 2)
  is resolved.
- **Spearman correlation wired** — `stats::spearman_r` added, delegates to
  `barracuda::stats::correlation::spearman_correlation` under `#[cfg(feature = "barracuda")]`.
- **5 biological ODE systems** (S58) — `CapacitorOde`, `CooperationOde`, `MultiSignalOde`,
  `BistableOde`, `PhageDefenseOde` unblock Waters/Srivastava/Fernandez paper reproductions.
- **NMF** (S58) — Euclidean + KL divergence in `linalg::nmf`, useful for R. Anderson metagenomics.
- **Anderson transport + disordered Laplacian** (S56) — unblocks Kachkovskiy papers.

---

## Part 1: What groundSpring Now Consumes from BarraCUDA

### CPU-delegated (Tier A done)

| groundSpring function | BarraCUDA target | Status |
|---|---|---|
| `stats::pearson_r` | `stats::pearson_correlation` | Wired, NaN-safe |
| `stats::spearman_r` | `stats::correlation::spearman_correlation` | **NEW** — wired, NaN-safe |

### GPU-ready (Tier A pending adapter)

| groundSpring function | BarraCUDA GPU op | Shader |
|---|---|---|
| `stats::rmse` | `NormReduceF64::l2` | `norm_reduce_f64.wgsl` |
| `stats::mbe` | `SumReduceF64::mean` | `sum_reduce_f64.wgsl` |
| `stats::r_squared` | `VarianceReduceF64` + reduce | `variance_reduce_f64.wgsl` |
| `stats::index_of_agreement` | `FusedMapReduceF64` | `fused_map_reduce_f64.wgsl` |
| `stats::hit_rate` | `FusedMapReduceF64` | `fused_map_reduce_f64.wgsl` |
| `rarefaction::shannon_diversity` | `FusedMapReduceF64::shannon_entropy` | `fused_map_reduce_f64.wgsl` |

### Absorbed upstream (no longer Tier C)

| Original Tier C item | BarraCUDA op | Notes |
|---|---|---|
| `mc_et0_propagate_f64` | `BatchedElementwiseF64::fao56_et0_batch` | FAO-56 full equation chain as `Op::Fao56Et0`. 9 inputs per batch: tmax, tmin, rh_max, rh_min, wind, Rs, elev, lat, doy. CPU reference + GPU dispatch. |

---

## Part 2: What Still Needs ToadStool Action

### Priority 1: Batched Multinomial (Tier C — WGSL prototype exists)

The only remaining Tier C kernel. Required for rarefaction GPU validation.

**Prototype**: `metalForge/shaders/batched_multinomial.wgsl` (67 lines)

```
@group(0) @binding(0) var<storage, read> abundances: array<f64>;
@group(0) @binding(1) var<storage, read> params: Params;  // {K, depth, n_reps, seed}
@group(0) @binding(2) var<storage, read_write> output: array<f64>;
```

Dispatch: `ceil(n_reps / 64)` workgroups. Each thread does one replicate,
drawing `depth` balls via xoshiro128** + cumulative-sum binary search.

**CPU reference**: `groundspring::rarefaction::multinomial_sample`

### Priority 2: PRNG Alignment (Tier B)

groundSpring uses `Xorshift64`, barracuda uses `xoshiro128**`. For bit-exact
GPU↔CPU determinism, groundSpring needs to migrate to xoshiro. Roadmap in
`specs/BARRACUDA_EVOLUTION.md` §PRNG Alignment.

### Priority 3: Grid Search 3D Dispatch (Tier B)

`seismic::grid_search_inversion` — lat × lon × depth search. Needs workgroup
dispatch + min-reduce. No existing barracuda op; could be built from
`SumReduceF64` primitives with custom map.

---

## Part 3: Three-Tier Control Matrix

| # | Experiment | CPU (88/88) | GPU | metalForge |
|---|-----------|:-----------:|:---:|:----------:|
| 1 | Sensor noise decomposition | **36/36 PASS** | Pending | — |
| 2 | Observation gap | **13/13 PASS** | Pending | — |
| 3 | Error propagation FAO-56 | **15/15 PASS** | Pending (adapter for `fao56_et0_batch`) | — |
| 4 | Sequencing noise | **15/15 PASS** | Blocked (`batched_multinomial` Tier C) | — |
| 5 | Seismic inversion | **9/9 PASS** | Blocked (grid search Tier B) | — |

---

## Part 4: V2 Lessons Learned — Resolution Status

| V2 Issue | Status |
|---|---|
| 1. NaN propagation in `pearson_correlation` | Resolved — groundSpring wraps with `is_nan()` guard |
| 2. Variance semantics (population vs sample) | **RESOLVED** — `population_variance()` and `population_std()` now in barracuda |
| 3. Feature gate ergonomics | Working well — `#[cfg(feature = "barracuda")]` pattern is clean |
| 4. PRNG alignment (xorshift vs xoshiro) | Open — migration roadmap documented |
| 5. f64 precision | Confirmed — barracuda f64 shaders are comprehensive |
| 6. ValidationHarness convergence | Both APIs stable; method names differ but semantics match |
| 7. Shared tolerance constants | Open — no `GROUNDSPRING_*` constants in barracuda yet |

---

## Part 5: What NOT to Duplicate

BarraCUDA primitives that groundSpring MUST NOT reimplement:

| Primitive | Module | Why |
|---|---|---|
| Pearson/Spearman correlation | `stats::correlation` | Already delegating |
| Shannon/Simpson diversity (GPU) | `ops::FusedMapReduceF64` | Convenience methods |
| FAO-56 ET₀ (GPU) | `ops::BatchedElementwiseF64` | Full equation chain absorbed |
| L1/L2/Linf norms | `ops::NormReduceF64` | Pending adapter |
| Sum/mean/max/min | `ops::SumReduceF64` | Pending adapter |
| Variance (pop + sample) | `ops::VarianceReduceF64` | Semantics resolved |
| PRNG xoshiro128** | `ops::PrngXoshiro` | Pending alignment |
| Biological ODEs | `numerical::ode_bio` | 5 systems ready |
| NMF | `linalg::nmf` | Euclidean + KL |
| Bray-Curtis | `ops::BrayCurtisF64` | Ready |
| Smith-Waterman | `genomics::SmithWatermanGpu` | Ready |
| Anderson localization | `spectral` + `disordered_laplacian` | S56 absorption |
| Gillespie SSA | `GillespieGpu` | Ready |

---

## Part 6: Faculty Paper Queue — GPU Readiness Update

Post-S62, several papers moved from GPU-Blocked to GPU-Ready:

| Paper | Previous | Current | Enabler |
|---|---|---|---|
| Massie c-di-GMP (#9) | Pending | **Ready** | `CapacitorOde` + `CooperationOde` (S58) |
| Fernandez cell shape (#10) | Pending | **Ready** | `BistableOde` (S58) |
| Srivastava QS (#11) | Pending | **Ready** | `MultiSignalOde` (S58) |
| Bourgain-Kachkovskiy (#15) | Pending | **Ready** | `disordered_laplacian` (S56) |
| Jitomirskaya-Kachkovskiy (#16) | Pending | **Ready** | Anderson transport (S56) |
| R. Anderson mBio (#20) | Partial | **Partial+** | NMF (S58), but rarefaction GPU still Tier C |

**Still blocked**: Bazavov (#6-8) on FFT gap; R. Anderson (#20-21) on `batched_multinomial`.

---

## Part 7: groundSpring Quality Gates

| Gate | Result |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --all-targets` | PASS (0 warnings) |
| `cargo clippy --features barracuda` | PASS (0 warnings) |
| `cargo doc --no-deps` | PASS |
| `cargo test` | 90/90 PASS |
| `cargo test --features barracuda` | 90/90 PASS |
| Validation binaries | 88/88 PASS |
| Library line coverage | 99.7% |
| Unsafe code | Forbidden (workspace lint) |
| Max file size | 397 lines (all < 1000) |
| SPDX headers | All `.rs` files |
| License | AGPL-3.0-or-later |
| Open data | All 24 papers use public repositories |

---

## Handoff Checklist

- [x] `pearson_r` wired to barracuda CPU
- [x] `spearman_r` wired to barracuda CPU
- [x] FAO-56 Tier C marked superseded (absorbed as `BatchedElementwiseF64`)
- [x] Shannon entropy GPU path documented
- [x] Population variance resolution documented
- [x] 5 bio ODE systems noted for Waters/Srivastava/Fernandez papers
- [x] NMF noted for R. Anderson metagenomics
- [x] `batched_multinomial` remains sole Tier C request
- [x] V2 archived
- [x] Three-tier control matrix updated
- [x] Faculty paper queue GPU readiness updated
- [x] All quality gates passing
