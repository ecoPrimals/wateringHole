# barraCuda v0.3.5 → hotSpring: P0 Fixes + Batched Dispatch

**Date**: 2026-03-11
**From**: barraCuda v0.3.5 (0649cd0)
**To**: hotSpring, coralReef, all Springs
**Priority**: HIGH — unblocks hotSpring energy computation + Kokkos parity

## Changes

### P0: Fix ReduceScalarPipeline::sum_f64() returning zeros

**Root cause**: `var<workgroup> shared_data: array<f64, 256>` is miscompiled
by naga's WGSL→SPIR-V codegen. All Vulkan backends produce zeros for f64
workgroup shared memory (confirmed by hotSpring Exp 055 on NVIDIA proprietary,
NVK/NAK, and llvmpipe). Global-memory f64 is unaffected.

**Fix**: `shader_for_device()` now always selects the DF64 (f32-pair)
accumulation shader for workgroup reduction. The DF64 reduce path uses
`shared_hi/shared_lo: array<f32, 256>` with Dekker-pair conversion at the
storage boundary — no f64 in `var<workgroup>`.

**Precision impact**: DF64 accumulation gives ~48-bit mantissa (vs 52-bit
for native f64). The 4-bit difference is acceptable for sum/max/min
reductions in MD energy computation.

**Files changed**: `crates/barracuda/src/pipeline/reduce.rs`

### Rename: has_nvvm_df64_poisoning_risk() → has_df64_spir_v_poisoning()

The DF64 transcendental poisoning is NOT an NVVM-specific issue. hotSpring
Exp 055 confirmed it affects all naga→SPIR-V backends. The rename reflects
the true root cause (naga codegen, not driver JIT):

- `Workaround::NvvmDf64TranscendentalPoisoning` → `Df64SpirVPoisoning`
- `has_nvvm_df64_poisoning_risk()` → `has_df64_spir_v_poisoning()`
- Detection now applies unconditionally (all Vulkan backends)

**Files changed**: `driver_profile/workarounds.rs`, `driver_profile/mod.rs`,
`hardware_calibration.rs`, `probe/mod.rs`, `wgpu_device/compilation.rs`

### P1: BatchedComputeDispatch<B>

New builder for recording multiple compute passes into a single GPU
submission. Addresses the 1.8× dispatch overhead measured by hotSpring
on RTX 3090 (3 submits per MD step → 1 submit per batch).

**API**:
```rust
let mut batch = BatchedComputeDispatch::new(&device);
batch.push(
    ComputeDispatch::new(&device, "force")
        .shader(FORCE_SHADER, "main").f64()
        .storage_read(0, &pos).storage_rw(1, &force)
        .dispatch_1d(n)
)?;
batch.push(
    ComputeDispatch::new(&device, "kick_drift")
        .shader(KD_SHADER, "main").f64()
        .storage_rw(0, &pos).storage_rw(1, &vel)
        .dispatch_1d(n)
)?;
batch.submit()?;
```

**Implementation**:
- `GpuBackend::dispatch_compute_batch` — default: sequential fallback
- `WgpuDevice` override: single `CommandEncoder` with multiple compute passes
- `Arc<B>` blanket: delegates to inner backend's batch implementation
- `ComputeDispatch::build()` — extract descriptor without submitting

**Files changed**: `backend.rs`, `compute_pipeline.rs`, `wgpu_backend.rs`, `mod.rs`

## Upstream Pin

```toml
barracuda = { git = "https://github.com/ecoPrimals/barraCuda.git", rev = "0649cd0" }
```

## Validation

- `cargo check` ✓
- `cargo fmt --all -- --check` ✓
- `cargo clippy --workspace -- -D warnings` ✓
- Routing tests: 11/11 pass
- Driver profile tests: 21/21 pass
- Reduce pipeline tests: 40/40 pass
- barracuda-core tests: 60/60 pass

## hotSpring Integration Steps

1. Update `barracuda` rev pin to `0649cd0`
2. Remove CPU-side sum workaround — `ReduceScalarPipeline::sum_f64()` should
   now return correct KE/PE values
3. Migrate `sovereign_engine.rs` dispatches to `BatchedComputeDispatch` for
   force+kick+drift batching (expected 1.5-1.8× improvement)
4. Replace `has_nvvm_df64_poisoning_risk()` → `has_df64_spir_v_poisoning()`
   if used directly

## Remaining Gaps (unchanged)

- DF64 transcendentals (exp, sqrt, log) still poisoned via naga SPIR-V
  → sovereign dispatch (coralReef) is the resolution path
- Kokkos gap: shared-memory tiled force kernels (P2)
- `create_pipeline_from_binary` on WgpuDevice (P1 for sovereign integration)

## Cross-References

- hotSpring Exp 055: `HOTSPRING_DF64_NAGA_POISONING_DIAGNOSTIC_HANDOFF_MAR11_2026.md`
- coralReef Iter 33: `CORALREEF_PHASE10_ITERATION33_NVVM_POISONING_VALIDATION_HANDOFF_MAR11_2026.md`
- Previous: `BARRACUDA_V035_SOVEREIGN_ROUTING_EVOLUTION_HANDOFF_MAR11_2026.md`
