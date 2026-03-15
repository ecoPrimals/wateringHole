# hotSpring v0.6.24 — Modern Primal Rewire Handoff

**Date:** March 9, 2026
**From:** hotSpring v0.6.24 (769 lib tests, 0 failures, 0 clippy errors)
**To:** toadStool (S138) / barraCuda (v0.3.3, `27011af`) / coralReef (Phase 10, Iter 25)
**License:** AGPL-3.0-only

## Executive Summary

Full rewire of hotSpring to latest barraCuda HEAD (`cdd748d` → `27011af`, 19 commits,
577 files changed, +11,419/-6,729 lines). Handles all breaking changes from the
`Fp64Strategy::Sovereign` addition, `compile_shader_universal()` removal, and
integrates barraCuda's hardware-level `PrecisionRoutingAdvice` into hotSpring's
domain-level precision routing. All benchmarks validated.

**Math is universal. Precision is silicon. barraCuda owns both.**

## Changes

### 1. Dependency Pin Update

```
- barracuda = { git = "...", rev = "cdd748d" }
+ barracuda = { git = "...", rev = "27011af" }
```

### 2. Fp64Strategy::Sovereign (10 match arms)

New `Sovereign` variant added to `Fp64Strategy` for coralReef sovereign compilation.
Routes like `Native` in all hotSpring dispatch paths — sovereign compilation produces
real f64 GPU code, so it follows the native f64 shader path.

**Files changed:**
- `lattice/gpu_hmc/mod.rs` — 4 match arms (force, plaquette, kinetic energy, label)
- `md/celllist.rs` — 2 match arms (label, force pipeline)
- `md/simulation/mod.rs` — 2 match arms (label, force pipeline)
- `md/simulation/verlet.rs` — 2 match arms (label, force pipeline)

### 3. compile_shader_universal() → compile_shader_df64()

`compile_shader_universal(source, Precision::Df64, label)` was removed upstream.
Replaced with `compile_shader_df64(source, label)` which does the same thing
(prepends df64_core + df64_transcendentals, runs ILP optimizer).

**File:** `gpu/mod.rs` — `compile_full_df64_pipeline()`

### 4. force_anomaly Delegation

Local 15-line sliding-window anomaly detection in `md/brain.rs` now delegates to
`barracuda::nautilus::brain::force_anomaly(current, window)`. The local function
extracts `total_energy / n_particles` and passes to upstream.

### 5. PrecisionRoutingAdvice Integration

`precision_routing.rs` now queries `gpu.driver_profile().precision_routing()` for
hardware-level advice (`F64Native`, `F64NativeNoSharedMem`, `Df64Only`, `F32Only`),
then intersects with physics domain requirements. The `PrecisionRoutingAdvice` struct
now carries `hw_advice: HwPrecisionAdvice` alongside the domain-level tier.

### 6. Version Bump

`0.6.23` → `0.6.24`

## Verification

| Check | Result |
|-------|--------|
| `cargo check --lib` | PASS |
| `cargo check` (all bins) | PASS |
| `cargo test --lib` | **769/769 pass**, 0 fail, 6 ignored |
| `cargo clippy --lib` | 10 warnings (all pre-existing), 0 errors |
| `bench_cross_spring_evolution` | ALL PASS — all cross-spring pathways exercised |
| `bench_precision_tiers` | **7/7 checks pass** — f32/DF64/f64 validated |
| `bench_dispatch_overhead` | **8/8 checks pass** — 25.5× batch amortization |

## Cross-Spring Shader Evolution Provenance

The cross-spring benchmark validated these multi-spring shader pathways:

| Op | Origin | Used By | Status |
|----|--------|---------|--------|
| Special functions (gamma, erf, bessel) | hotSpring → toadStool S25-S68 | all springs | PASS |
| Level spacing ratio | hotSpring Anderson → toadStool S78 | wetSpring bio-spectral, neuralSpring RMT | PASS |
| VACF (batched ACF shader) | hotSpring MD → toadStool S70+ | hotSpring transport | PASS |
| Autocorrelation GPU | hotSpring + wetSpring time-series | all springs spectral analysis | PASS |
| Mean+Variance GPU | Kokkos reduce → hotSpring Welford | all springs observable stats | PASS |
| Correlation GPU | Kokkos 5-acc Pearson → wetSpring bio-stats | groundSpring, neuralSpring, hotSpring | PASS |
| Chi-squared GPU | groundSpring V74 → barraCuda S93 | hotSpring nuclear χ² fits, wetSpring | PASS |
| Linear regression GPU | neuralSpring baseCamp V18 → toadStool S25 | batched regression | PASS |
| Matrix correlation GPU | neuralSpring baseCamp V18 → toadStool S25 | correlation matrices | PASS |
| Stress virial GPU | hotSpring MD → toadStool S70+ | MD transport | PASS |
| Nelder-Mead GPU | neuralSpring → toadStool S79 | HMC parameter tuning | PASS |

## What Remains

| Item | Priority | Status |
|------|----------|--------|
| `GpuView<T>` for MD | P1 | Ready in barraCuda, not yet wired |
| Buffer-resident CG | P1 | `encode_reduce_to_buffer()` available |
| Edition 2024 | P2 | barraCuda migrated, hotSpring pending |
| `SubstrateCapabilityKind` dispatch | P2 | toadStool S96+ ready |
| coralReef sovereign pipeline | P3 | AMD E2E proven, NVIDIA blocked on coralDriver |
| Asymmetric lattice production | P1 | 64³×8, 96³×12 for finite-T |
| toadStool `AdaptiveSimulationController` | P2 | May complement NPU steering |
