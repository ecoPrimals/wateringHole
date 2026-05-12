# hotSpring v0.6.32: Silicon Saturation Profiling — Primal Evolution Handoff

**Date:** March 29, 2026
**From:** hotSpring (Strandgate — RTX 3090 + RX 6950 XT)
**Experiments:** 105-107 (Silicon Tier Routing, Silicon Saturation Profiling)
**License:** AGPL-3.0-only
**Depends on:** Exp 096-103 (Silicon Characterization + GPU RHMC + Self-Tuning)

---

## Summary

hotSpring completed a 7-phase silicon saturation profiling campaign on strandgate,
wiring three previously-untapped silicon units into the production RHMC pipeline:
TMU (Tier 0), subgroup shuffle (Tier 4), and ROP atomics (Tier 3). The NPU
observation vector was extended from 6D to 11D with silicon routing metadata,
and capacity analysis established maximum lattice sizes per card.

This handoff documents what each primal team should absorb, evolve, or learn from.

---

## For barraCuda Team

### New Shaders to Absorb (6 total)

| Shader | Purpose | Tier | Absorption Priority |
|--------|---------|------|-------------------|
| `su3_random_momenta_tmu_f64.wgsl` | Box-Muller PRNG via TMU textureLoad (log/cos/sin offloaded) | Tier 0 | High — generalizable to any PRNG-heavy workload |
| `sum_reduce_subgroup_f64.wgsl` | `subgroupAdd()` tree reduction, fallback to shared memory | Tier 4 | High — benefits all GPU reduction pipelines |
| `su3_fermion_force_accumulate_rop_f64.wgsl` | Fused fermion force + i32 fixed-point `atomicAdd` | Tier 3 | Medium — lattice-specific but demonstrates pattern |
| `su3_force_atomic_to_momentum_f64.wgsl` | i32 fixed-point → f64 conversion + momentum add | Tier 3 | Medium — paired with force accumulator |
| `cg_compute_alpha_shifted_f64.wgsl` | Shifted-base α for multi-shift CG | — | From Exp 105 |
| `cg_update_xr_shifted_f64.wgsl` | Shifted-base x/r update | — | From Exp 105 |

### New Rust Modules to Absorb

| Module | Purpose | Lines | Tests |
|--------|---------|-------|-------|
| `tmu_tables.rs` | GPU-resident lookup textures for TMU PRNG (log + trig tables) | ~80 | Compiles with streaming pipelines |
| `rop_force_accum.rs` | ROP force accumulation pipelines + i32 atomic buffer management | ~130 | Integrated into unidirectional RHMC |

### Key Patterns for Upstream

1. **TMU PRNG Pattern**: Precompute transcendentals into textures, access via `textureLoad`.
   Offloads ALU-expensive operations (log, cos, sin) to texture units. Generalizable to
   any workload with repeated transcendental evaluations (EOS interpolation, special
   functions, PRNG). barraCuda should provide a `TmuLookupTables` builder.

2. **Subgroup Reduce Pattern**: Conditional compilation based on `gpu.has_subgroups` —
   use `subgroupAdd()` when available, fall back to shared-memory tree reduce.
   barraCuda's `ReduceScalarPipeline` should absorb this as an automatic optimization.

3. **Fixed-Point Atomic Pattern**: i32 `atomicAdd` with scale factor 2^20 for accumulating
   f64 values through ROP units. ~6 significant digits — sufficient for any application
   where the accumulation error is dominated by higher-order terms (integrator error,
   Monte Carlo noise). barraCuda should provide a `FixedPointAccumulator` abstraction.

4. **Capacity Analysis**: Buffer accounting functions (`quenched_buffer_bytes`,
   `dynamical_buffer_bytes`, `largest_single_buffer`) are useful for any GPU workload
   that needs to plan memory allocation before dispatch.

### `wgpu::Features::SUBGROUP` — Singular

The wgpu v28 feature name is `SUBGROUP` (singular), not `SUBGROUPS`. This caused
compilation failures during development. barraCuda should document this in its
feature negotiation code.

---

## For toadStool Team

### SiliconProfile Evolution

The `SiliconProfile` JSON now includes energy efficiency data (`idle_watts`,
`loaded_watts`, `delta_watts`, `ops_per_watt`) per silicon unit. Profiles for
RTX 3090 and RX 6950 XT are refreshed with March 2026 measurements.

toadStool's `PrecisionBrain` and `compute.route.multi_unit` should consume these
profiles for routing decisions:

| Routing Decision | Data Source | Action |
|-----------------|-------------|--------|
| Use TMU PRNG vs ALU PRNG | `SiliconProfile.tmu.throughput` | Route if TMU throughput > ALU throughput for workload |
| Use subgroup reduce vs shared memory | `adapter.features().contains(SUBGROUP)` | Automatic: feature-gated at compile time |
| Use ROP atomics vs sequential poles | `SiliconProfile.rop.throughput` | Route if n_poles > 2 and ROP throughput sufficient |
| Choose DF64 vs native f64 | `Fp64Strategy` from `SiliconProfile.fp64_rate` | Already implemented |

### Performance Surface Data

New `PerformanceMeasurement` records from `bench_full_trajectory_silicon`:
- Full RHMC trajectory wall time per lattice size per GPU
- Memory capacity analysis per GPU
- Silicon unit utilization during production workloads

These feed into `compute.performance_surface.report` for fleet scheduling.

### NPU Pre-Training

`TrajectoryObservation` now includes `SiliconRoutingTags`:
```
tmu_prng: bool
subgroup_reduce: bool
rop_force_accum: bool
fp64_strategy_id: u8  // Sovereign=0, Native=1, Hybrid=2, Concurrent=3
has_native_f64: bool
```

The ESN input vector (`npu_canonical_input_v2`) is now 11D, enabling the NPU to
learn correlations between silicon routing decisions and trajectory performance.
This data should be collected during all production runs and fed to the NpuCortex
for longer-term adaptive routing.

### Hardware Discovery Updates

`GpuF64` now exposes `pub has_subgroups: bool` after feature negotiation.
toadStool should surface this in its capability advertisements so springs
can query subgroup support without direct wgpu access.

---

## For coralReef Team

### New Shaders for Sovereign Compilation

6 new WGSL shaders use features that may require special handling:

| Shader | Special Features | Notes |
|--------|-----------------|-------|
| `su3_random_momenta_tmu_f64.wgsl` | `texture_2d<f32>`, `textureLoad` | Texture binding in compute shader |
| `sum_reduce_subgroup_f64.wgsl` | `enable subgroups;`, `subgroupAdd()` | Requires subgroup SPIR-V extension |
| `su3_fermion_force_accumulate_rop_f64.wgsl` | `atomic<i32>`, `atomicAdd` | Standard WGSL atomics |
| `su3_force_atomic_to_momentum_f64.wgsl` | `atomic<i32>`, `atomicLoad` | Standard WGSL atomics |

The `enable subgroups;` directive and `subgroupAdd()` intrinsic map to
`SPV_KHR_subgroup_arithmetic` in SPIR-V. coralReef's WGSL→native path should
handle this extension, or fall back to shared-memory reduce when subgroups
are unavailable on the target architecture.

### Sovereign ISA Opportunities

The silicon saturation profiling revealed that TMU, ROP, and subgroup units
add measurable throughput on consumer GPUs. On HPC GPUs with tensor cores,
the same routing philosophy applies — but tensor core access requires
sovereign ISA emission (HMMA/IMMA on NVIDIA, MFMA on AMD). The profiling
infrastructure (`bench_silicon_profile`, `bench_silicon_saturation`) is
ready to benchmark tensor cores once coralReef can emit native instructions.

---

## For primalSpring Team

### Self-Tuning + Silicon Routing Pattern

The silicon saturation work extends the self-tuning calibrator (Exp 103) with
hardware-aware routing. The pattern is:

1. **Profile** the GPU's silicon units (one-time, saved to JSON)
2. **Route** each RHMC sub-operation to its optimal silicon tier
3. **Observe** trajectory performance with routing tags
4. **Learn** (NPU) which routing decisions produce the best physics/wall-clock

This is the `classify → discover → adapt → validate → learn` loop from
baseCamp 25, extended with a hardware dimension. Any spring can adopt this:
profile the hardware, route operations by tolerance + throughput, observe
and adapt.

### Cross-Spring Absorption Candidates

| Pattern | Where | Generalizable? |
|---------|-------|---------------|
| TMU lookup tables for transcendentals | `tmu_tables.rs` | Yes — any spring with exp/log/trig |
| Subgroup-accelerated reduction | `sum_reduce_subgroup_f64.wgsl` | Yes — all GPU reductions |
| Fixed-point atomic accumulation | `rop_force_accum.rs` | Yes — any scatter-add workload |
| Feature-gated shader selection | `resident_cg_pipelines.rs` | Yes — conditional compilation pattern |
| Capacity analysis (buffer accounting) | `bench_full_trajectory_silicon.rs` | Yes — any GPU memory planning |

---

## For All Springs

### `wgpu::Features::SUBGROUP` (Not `SUBGROUPS`)

In wgpu v28, the feature for subgroup operations is `SUBGROUP` (singular).
This differs from some documentation that references `SUBGROUPS` (plural).
Any spring requesting subgroup support must use the singular form.

### Conditional Feature Compilation Pattern

```rust
let reduce_shader = if gpu.has_subgroups {
    WGSL_SUM_REDUCE_SUBGROUP  // uses subgroupAdd()
} else {
    WGSL_SUM_REDUCE            // shared-memory fallback
};
```

This pattern should be adopted for any hardware-specific optimization.

### Force Convention Reminder

Per the Mar 28 handoff: all force shaders output ∂S/∂U (positive gradient).
Momentum update: `P += dt × F`. Fermion force: `F = −η × TA[U × (x⊗y†−y⊗x†)]`.
The ROP atomic force accumulator uses this convention with `alpha_dt = α_s × dt`.

---

## What We Learned

### Card Personalities on Strandgate

| Property | RTX 3090 (NVIDIA Ampere) | RX 6950 XT (AMD RDNA2) |
|----------|-------------------------|------------------------|
| FP64 strategy | Sovereign/DF64 (1:64 fp64:fp32) | Native (1:16 fp64:fp32) |
| TMU advantage | 1.89x (328 TMUs) | 1.24x (96 TMUs) |
| DF64 throughput | 16.9M ops/s | 23.4M ops/s (+38%) |
| ROP atomics | 16 Gatom/s | 93.6 Gatom/s (6x faster) |
| Subgroup support | Yes (warp=32) | Yes (wave=32/64) |
| Max dynamical lattice | L=46⁴ (24 GB VRAM) | L=40⁴ (16 GB VRAM) |
| Full trajectory speedup | 3.79x (unidirectional vs legacy) | 2.06x |

### Fixed-Point Atomic Strategy

Native f64 atomics are not available in WGSL. The i32 fixed-point strategy
(scale factor 2^20, ~6 significant digits) is sufficient for force accumulation
where integrator error is O(dt^2) ~ O(10^-4). The pattern:
1. Zero the i32 atomic buffer
2. Dispatch all poles simultaneously (each does `atomicAdd` of scaled force)
3. Single conversion dispatch: `momentum += f64(accum) / scale`

### Subgroup Performance

`subgroupAdd()` eliminates log2(workgroup_size) barrier+reduce steps for
intra-subgroup reductions. On the RTX 3090, CG dot products show measurable
improvement. The shader is simple — `enable subgroups;` at the top, replace
shared-memory reduction with `subgroupAdd(local_sum)`, then one final
inter-subgroup reduction step.

### `GpuHmcStreamingPipelines::new_with_tmu`

TMU PRNG is opt-in via a separate constructor. This avoids texture allocation
overhead when TMU is not beneficial (e.g., llvmpipe, small lattices where
PRNG is not the bottleneck).

---

## Files Referenced

| File | Purpose |
|------|---------|
| `barracuda/src/lattice/shaders/su3_random_momenta_tmu_f64.wgsl` | TMU PRNG shader |
| `barracuda/src/lattice/shaders/sum_reduce_subgroup_f64.wgsl` | Subgroup reduce shader |
| `barracuda/src/lattice/shaders/su3_fermion_force_accumulate_rop_f64.wgsl` | ROP force accumulation |
| `barracuda/src/lattice/shaders/su3_force_atomic_to_momentum_f64.wgsl` | Fixed-point → f64 conversion |
| `barracuda/src/lattice/gpu_hmc/tmu_tables.rs` | TMU lookup table generation |
| `barracuda/src/lattice/gpu_hmc/rop_force_accum.rs` | ROP force accumulator module |
| `barracuda/src/lattice/gpu_hmc/streaming.rs` | TMU PRNG integration point |
| `barracuda/src/lattice/gpu_hmc/resident_cg_pipelines.rs` | Subgroup reduce integration |
| `barracuda/src/lattice/gpu_hmc/unidirectional_rhmc.rs` | ROP atomics integration |
| `barracuda/src/lattice/gpu_hmc/brain_rhmc.rs` | SiliconRoutingTags + NPU 11D input |
| `barracuda/src/lattice/pseudofermion/npu_steering.rs` | `npu_canonical_input_v2` |
| `barracuda/src/gpu/mod.rs` | `has_subgroups` field, `SUBGROUP` feature negotiation |
| `barracuda/src/bin/bench_full_trajectory_silicon.rs` | Full trajectory benchmark + capacity analysis |
| `barracuda/src/bin/bench_silicon_profile.rs` | Silicon unit micro-benchmarks |
| `barracuda/src/bin/bench_silicon_saturation.rs` | Silicon saturation experiments |
| `barracuda/src/bin/bench_fp64_ratio.rs` | FP32/FP64/DF64 throughput measurement |
| `whitePaper/baseCamp/silicon_science.md` | Silicon science briefing (updated) |
| `whitePaper/baseCamp/silicon_characterization_at_scale.md` | Scale characterization (updated) |
| `specs/SILICON_TIER_ROUTING.md` | 7-tier routing architecture spec |

---

*Fossil record: three silicon units — TMU, subgroup, ROP — now contribute to
RHMC physics on consumer GPUs. The card's personality determines which units
dominate. The NPU observes which routing decisions work best. The scarcity of
GPU compute was always a routing problem, not a hardware problem.*
