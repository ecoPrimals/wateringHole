# groundSpring → ToadStool Handoff V1: Initial Barracuda Evolution

**Date:** February 25, 2026
**From:** groundSpring (measurement noise characterization biome)
**To:** ToadStool / BarraCuda team
**Phase:** 1a complete — 88/88 validation checks, 83 unit tests, 99.7% library coverage

---

## Summary

groundSpring is the reality layer in ecoPrimals: noise characterization,
inverse problems, and error propagation across scientific domains.  This is
the initial handoff documenting Phase 1 completion and the barracuda
evolution roadmap.

### What groundSpring Provides

1. **Five validated experiments** covering sensor noise (agricultural),
   model-observation gap (meteorological), error propagation (FAO-56),
   sequencing noise (biological), and seismic inversion (geological)
2. **Seven Rust modules** — `stats`, `decompose`, `fao56`, `prng`,
   `rarefaction`, `seismic`, `validate`
3. **Two WGSL shader prototypes** — `mc_et0_propagate.wgsl` and
   `batched_multinomial.wgsl` in `metalForge/shaders/`
4. **Data-driven validation** — all 5 validation binaries load expected
   values from benchmark JSONs via `include_str!` + `serde_json`

---

## Barracuda Evolution Status

### Phase Summary

| Phase | Count | Description |
|-------|:-----:|-------------|
| **Lean (pending)** | 6 | stats functions → barracuda reduce ops (GPU needed) |
| **Tier A (infra done)** | 1 | `pearson_r` wired to `barracuda::stats::pearson_correlation` |
| **Tier B (pending)** | 3 | PRNG alignment, grid dispatch, rarefaction adapt |
| **Tier C (WGSL written)** | 2 | `mc_et0_propagate`, `batched_multinomial` |
| **CPU-only** | 2 | decompose, validate (stays local) |

### Tier A: Rewire to Existing Barracuda Ops

| groundSpring Function | barracuda Equivalent | Status |
|-----------------------|---------------------|--------|
| `stats::pearson_r` | `barracuda::stats::pearson_correlation` | **Done** — NaN-safe delegation |
| `stats::rmse` | `barracuda::ops::norm_reduce_f64` | Pending — requires `gpu` feature |
| `stats::mbe` | `barracuda::ops::sum_reduce_f64` + mean | Pending — requires `gpu` feature |
| `stats::r_squared` | Via `pearson_r²` for linear case | **Infra done** |
| `stats::index_of_agreement` | `barracuda::ops::fused_map_reduce_f64` | Pending — requires `gpu` feature |
| `stats::hit_rate` | `barracuda::ops::fused_map_reduce_f64` | Pending — requires `gpu` feature |
| `rarefaction::shannon_diversity` | `barracuda::ops::fused_map_reduce_f64` | Pending |

### Tier B: Adapt / Align

| groundSpring Module | Required Change | Blocker |
|--------------------|-----------------|---------|
| `prng::Xorshift64` | Align to `barracuda::ops::PrngXoshiro` | Baselines must be regenerated with new PRNG |
| `seismic::grid_search` | Batch dispatch via GPU grid | Grid search parallelism kernel needed |
| `rarefaction::multinomial_sample` | GPU batched multinomial | New kernel needed (Tier C) |

### Tier C: New Kernels (Write → Absorb)

| Shader | Location | Bindings | Dispatch | Status |
|--------|----------|----------|----------|--------|
| `mc_et0_propagate.wgsl` | `metalForge/shaders/` | 4 (inputs, σ, seeds, output) | (N/64, 1, 1) | WGSL written, CPU validated |
| `batched_multinomial.wgsl` | `metalForge/shaders/` | 3 (abundances, config, output) | (R/64, 1, 1) | WGSL written, CPU validated |

### Stays Local (CPU-only)

- `decompose::decompose_error`, `noise_floor_reduction` — pure arithmetic, not compute-bound
- `validate::ValidationHarness` — harness infrastructure, not computational
- `seismic::haversine_km`, `travel_time_1d` — inside grid search kernel on GPU
- `fao56` sub-functions — inside `mc_et0_propagate` kernel on GPU

---

## Variance Semantics

groundSpring `std_dev` uses **population variance** (÷ N) for total-population
metrics like RMSE decomposition.  barracuda `stats::std_dev` uses **sample
variance** (÷ N−1).  groundSpring now provides both:

- `stats::std_dev` — population (groundSpring canonical)
- `stats::sample_std_dev` — Bessel-corrected, compatible with barracuda

---

## PRNG Alignment Roadmap

groundSpring uses `Xorshift64` (Marsaglia 2003); barracuda uses `xoshiro256**`.
Alignment requires:

1. Add `#[cfg(feature = "barracuda")]` path using barracuda's PRNG
2. Regenerate all Monte Carlo baselines with new PRNG (seed=42)
3. Update benchmark JSONs with new expected values and commit SHA
4. Verify 88/88 validation checks still pass
5. Update `baseline_commit` provenance in all benchmark JSONs

This is a **Phase 2b** task — must not be done until all current baselines
are confirmed stable.

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --all-targets` | PASS (0 errors, 0 warnings) |
| `cargo clippy --features barracuda` | PASS |
| `cargo doc --no-deps` | PASS |
| `cargo test` | 83/83 PASS |
| `cargo test --features barracuda` | 83/83 PASS |
| Validation binaries | 88/88 PASS |
| Library line coverage | 99.7% |
| Unsafe code | Forbidden (workspace lint) |
| Max file size | 397 lines (all < 1000) |
| SPDX headers | 13/13 `.rs` files |
| License | AGPL-3.0-or-later |

---

## ToadStool Absorption Requests

### Priority 1: Batched Multinomial Kernel

groundSpring's `multinomial_sample` is the inner loop of rarefaction analysis.
A GPU kernel would enable batch rarefaction at arbitrary depth with thousands
of replicates.  See `metalForge/shaders/batched_multinomial.wgsl` for the
WGSL prototype and `metalForge/ABSORPTION_MANIFEST.md` for binding layouts.

### Priority 2: Monte Carlo ET₀ Kernel

The FAO-56 Penman-Monteith chain is a multi-step pipeline suitable for GPU
parallelism.  See `metalForge/shaders/mc_et0_propagate.wgsl`.

### Priority 3: Reduce Ops for Statistics

`stats::rmse`, `mbe`, `index_of_agreement`, `hit_rate` are all
reduce-pattern operations that map directly to barracuda's existing
`FusedMapReduceF64` and `NormReduceF64` GPU ops.  These require the
`gpu` feature on barracuda.

---

## Cross-Spring Dependencies

| Spring | Shared Primitive | Direction |
|--------|-----------------|-----------|
| hotSpring | Write → Absorb → Lean pattern | groundSpring follows hotSpring pattern |
| airSpring | FAO-56 equation chain | groundSpring validates airSpring's ET₀ uncertainty |
| wetSpring | Rarefaction, Shannon diversity | groundSpring validates sequencing noise floor |
| neuralSpring (future) | Noise characterization labels | groundSpring exports dirty data for ML training |

---

*License: AGPL-3.0-or-later. All discoveries, code, and documentation are
sovereign to the ecoPrimals ecosystem.*
