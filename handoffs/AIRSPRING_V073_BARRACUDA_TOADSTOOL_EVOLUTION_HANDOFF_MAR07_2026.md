<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# airSpring V0.7.3 → BarraCuda/ToadStool: Evolution Handoff

**Date**: March 7, 2026
**From**: airSpring (ecology/agriculture validation)
**To**: BarraCuda team (sovereign math engine) + ToadStool team (hardware dispatch) + coralReef team (sovereign GPU compiler)
**airSpring**: v0.7.3 (848 lib + 186 forge tests, 86 binaries, 0 clippy pedantic warnings)
**BarraCuda**: v0.3.3 standalone (`ecoPrimals/barraCuda`)
**ToadStool**: S130+ (`ecoPrimals/phase1/toadstool`)
**coralReef**: Phase 10+ (`ecoPrimals/coralReef`)

---

## Executive Summary

airSpring has completed the full **Write → Absorb → Lean** cycle. All 6 local GPU
ops (SCS-CN, Stewart, Makkink, Turc, Hamon, Blaney-Criddle) have been absorbed
upstream into `BatchedElementwiseF64` (ops 14-19). `local_dispatch`, local WGSL
shaders, and the `wgpu` direct-compute path have been retired. airSpring now leans
entirely on barraCuda primitives for all 20 elementwise ops.

Additionally, `PrecisionRoutingAdvice` has been wired into airSpring's device
probing, and the upstream provenance registry (`barracuda::shaders::provenance`)
is integrated for cross-spring evolution tracking.

This handoff documents what we learned, what we contributed, and what would
benefit the upstream ecosystem.

---

## Part 1: Write → Absorb → Lean — Complete

### What Was Absorbed

| airSpring Local Op | Upstream Op | Domain | Formula |
|--------------------|:-----------:|--------|---------|
| SCS-CN runoff | op=17 | Hydrology | Q = (P − Ia)² / (P − Ia + S) |
| Stewart yield | op=18 | Agronomy | Ya/Ymax = 1 − Ky(1 − ETa/ETc) |
| Makkink ET₀ | op=14 | Evapotranspiration | ET₀ = 0.61·Δ/(Δ+γ)·Rs/λ − 0.12 |
| Turc ET₀ | op=15 | Evapotranspiration | ET₀ = 0.013·T/(T+15)·(Rs+50) |
| Hamon PET | op=16 | Evapotranspiration | PET = 0.55·(N/12)²·esat/100·25.4 |
| Blaney-Criddle ET₀ | op=19 | Evapotranspiration | ET₀ = p·(0.46·T + 8.13) |

### What Was Retired

- `barracuda/src/gpu/local_dispatch.rs` — deleted
- `barracuda/src/shaders/local_elementwise_f64.wgsl` — deleted
- `barracuda/src/shaders/local_elementwise.wgsl` — deleted
- Direct `wgpu` dependency purpose narrowed (still used for buffer I/O via bytemuck)

### Validation

All 6 ops validated via `BatchedElementwiseF64` with CPU↔GPU parity:
- ET₀ methods: tolerance ≤ 1e-6
- Runoff/yield: tolerance ≤ 1e-10
- Batch scaling: N=1, 10, 100, 1000 confirmed
- 848/848 lib tests pass (0 failures)

---

## Part 2: PrecisionRoutingAdvice Integration

airSpring's `gpu::device_info::DevicePrecisionReport` now includes the
`PrecisionRoutingAdvice` field from `barracuda::device::driver_profile`. This
captures the four-axis routing that `Fp64Strategy` alone does not:

| Advice | Meaning | airSpring Behavior |
|--------|---------|-------------------|
| `F64Native` | Full native f64 everywhere | Direct `BatchedElementwiseF64` dispatch |
| `F64NativeNoSharedMem` | Compute OK, shared-mem reductions broken | Reductions via DF64 or scalar f64 |
| `Df64Only` | DF64 (f32-pair, ~48-bit) for all f64 work | DF64 path for science accuracy |
| `F32Only` | f32 only | Not suitable for science pipelines — CPU fallback |

This enables airSpring to make informed dispatch decisions per-hardware, which is
especially valuable for the NVK/Mesa shared-memory reliability issue we discovered
in v0.7.1 (Titan V: compute shaders return zeros for variance/correlation ops).

### What We Learned

The NVK zero-output issue on Titan V (GV100) manifests specifically in
shared-memory reductions. `PrecisionRoutingAdvice::F64NativeNoSharedMem` captures
this exactly — native f64 compute works fine, but shared-memory atomics/reductions
are unreliable. This is the precision axis that `Fp64Strategy` misses.

**Recommendation for barraCuda**: Consider making `PrecisionRoutingAdvice` available
at the op dispatch level, so individual ops can route around shared-memory reductions
when running on affected hardware.

---

## Part 3: Upstream Provenance Registry

airSpring integrates `barracuda::shaders::provenance` via three query functions:

| Function | Purpose |
|----------|---------|
| `upstream_airspring_provenance()` | Shaders consumed by airSpring from upstream |
| `upstream_evolution_report()` | Full markdown cross-spring evolution report |
| `upstream_cross_spring_matrix()` | `(from, to)` → shader count dependency map |

These power the `bench_cross_spring_evolution` binary, which now prints the full
ecosystem provenance including which shaders from hotSpring, wetSpring,
neuralSpring, and groundSpring are consumed by airSpring workloads.

---

## Part 4: Cross-Spring Evolution Observations

### Shader Provenance — What airSpring Consumes

| Upstream Spring | What airSpring Uses | Domain Bridge |
|----------------|--------------------|----|
| **hotSpring** | `pow_f64`, `exp_f64`, `log_f64`, `trig_f64`, DF64 core, DF64 transcendentals | Precision math for VG, atmospheric, soil physics |
| **wetSpring** | `kriging_f64`, `fused_map_reduce`, `moving_window`, `diversity` metrics | Spatial interpolation, streaming stats, biodiversity indices |
| **neuralSpring** | `nelder_mead`, `multi_start`, `ValidationHarness` | Isotherm fitting, global optimization |
| **groundSpring** | `mc_et0_propagate_f64.wgsl`, xoshiro + Box-Muller | Monte Carlo ET₀ uncertainty propagation |

### Cross-Spring Evolution Notes

**For hotSpring team**: airSpring's Hamon formula divergence finding may be relevant.
Two formulations exist: Hamon (1963 ASCE) uses `esat = exp(21.233 − 5423/T_K)` while
Lu et al. (2005) uses `4.596·exp(0.0623·T_C)`. Our upstream op=16 implements the
1963 ASCE form. The ~20% difference between formulations is real physics, not a bug.
If hotSpring encounters similar divergence in precision shaders, this is documented in
airSpring's `gpu::simple_et0` tests.

**For wetSpring team**: airSpring validates the `diversity` metrics GPU path
(Shannon, Simpson, Pielou, Chao1, Bray-Curtis) via Paper 12 (immunological Anderson).
The dimensional promotion model (soil W → skin W → cytokine propagation) demonstrates
cross-domain reuse of diversity indices. Tissue cell-type diversity uses the same
`DiversityFusionGpu` as agroecosystem OTU diversity.

**For neuralSpring team**: The `AirSpringBrain` / `CytokineBrain` Nautilus reservoir
pattern (3-head feed-forward, no temporal recurrence) works well for agricultural
time-series prediction. DriftMonitor detects regime changes in ET₀ and cytokine
cascades using the same pattern.

**For coralReef team**: When airSpring ran local WGSL shaders via `compile_shader_universal`,
we found that the `enable f64;` stripping step is critical before downcast paths.
With coralReef's sovereign compiler, this should be handled at the IR level rather
than string manipulation. The 6 agricultural ops (now upstream) are good test cases
for verifying f64-canonical → native compilation correctness.

---

## Part 5: What Would Help airSpring Next

| Feature | Upstream | Benefit to airSpring |
|---------|----------|---------------------|
| `BatchedOdeRK45F64` | barraCuda (unreleased) | GPU Richards PDE without custom dispatch |
| `TensorContext` | barraCuda (unreleased) | Multi-field seasonal pipeline on GPU |
| `mean_variance_to_buffer` | barraCuda (unreleased) | GPU streaming statistics for atlas |
| Per-op precision routing | barraCuda | Route around shared-mem issues per-op |
| `shader.compile.wgsl` | ToadStool JSON-RPC | Dynamic shader compilation via toadStool proxy |
| Native f64 transcendentals | coralReef | Replace DF64 workarounds on NVK |

---

## Part 6: Quality State

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --all-targets` (pedantic) | 0 errors |
| `cargo test --lib` | 848/848 (0 failures) |
| `cargo doc --no-deps` | Clean |
| All files < 1000 LOC | Yes |
| Zero `unsafe` | Yes |
| Zero `unwrap()` in lib | Yes |
| SPDX AGPL-3.0-or-later | All files |

---

## Appendix: Files Changed (v0.7.2 → v0.7.3)

| File | Change |
|------|--------|
| `barracuda/src/gpu/device_info.rs` | Added `PrecisionRoutingAdvice` to probe, upstream provenance queries |
| `barracuda/src/gpu/runoff.rs` | Rewired to `BatchedElementwiseF64` op=17 |
| `barracuda/src/gpu/yield_response.rs` | Rewired to `BatchedElementwiseF64` op=18 |
| `barracuda/src/gpu/simple_et0.rs` | Rewired to `BatchedElementwiseF64` ops 14-16, 19 |
| `barracuda/src/gpu/mod.rs` | Removed `local_dispatch` module |
| `barracuda/src/gpu/evolution_gaps.rs` | Updated to v0.7.3 roadmap |
| `barracuda/src/bin/validate_cross_spring_evolution.rs` | PrecisionRouting + provenance |
| `barracuda/src/bin/validate_cross_spring_provenance.rs` | Upstream registry validation |
| `barracuda/src/bin/bench_cross_spring_evolution/modern.rs` | New: ops 14-19 benchmarks |
| `metalForge/forge/src/workloads.rs` | LocalElementwise → BatchedElementwiseF64 |
| `barracuda/EVOLUTION_READINESS.md` | Updated to v0.7.3 |
| `specs/GPU_PROMOTION_MAP.md` | Updated to v0.7.3 |

---

*airSpring v0.7.3 — Write→Absorb→Lean complete. All 20 ops upstream. PrecisionRouting
wired. Upstream provenance integrated. Zero local WGSL shaders remain. Pure lean on
barraCuda primitives. Ready for coralReef native compilation when available.*
