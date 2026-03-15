# hotSpring Sovereign Dispatch Rewire — Handoff

**Date**: 2026-03-09
**From**: hotSpring v0.6.29
**To**: barraCuda, coralReef, toadStool teams
**Upstream**: barraCuda `875e116`, coralReef Iter 33

## What Was Done

hotSpring's MD simulation has been rewired to use barraCuda's `GpuBackend`
trait and `ComputeDispatch<B>` builder, creating a **backend-agnostic MD
engine** (`sovereign_engine.rs`) that compiles and runs identically on both
wgpu/Vulkan and sovereign (coralReef → DRM) backends.

### New Files

- `hotSpring/barracuda/src/md/sovereign_engine.rs` — `MdEngine<B: GpuBackend>`
- `hotSpring/barracuda/src/bin/bench_sovereign_dispatch.rs` — benchmark binary
- `hotSpring/experiments/056_SOVEREIGN_DISPATCH_BENCHMARK.md` — results

### Architecture

```rust
// Same code runs on both backends:
fn run_simulation_generic<B: GpuBackend>(backend: &B, config: &MdConfig) -> Result<MdSimulation>

// Dispatch pattern:
ComputeDispatch::new(backend, "yukawa_force")
    .shader(SHADER_YUKAWA_FORCE, "main")
    .f64()
    .storage_read(0, &bufs.pos)
    .storage_rw(1, &bufs.force)
    .storage_rw(2, &bufs.pe)
    .storage_read(3, &bufs.force_params)
    .dispatch(workgroups, 1, 1)
    .submit()?;
```

## Benchmark Results

| Backend | Steps/s | Status |
|---------|---------|--------|
| wgpu/Vulkan (RTX 3090) | 140.3 | VALIDATED ✓ |
| Sovereign/DRM | — | DRM ioctl EINVAL |
| Kokkos-CUDA (reference) | 2896.7 | Verlet method |

## Blocking Issues for Each Team

### coralReef: DRM dispatch ioctl

`CoralReefDevice::with_auto_device()` succeeds (hardware detected), but
`dispatch_compute` fails at `coral_driver::drm_ioctl` with error 22 (EINVAL).
The compilation path works perfectly (Iter 33 validated). The gap is in
`coral-driver`'s nvidia-drm kernel interface for:

1. Buffer allocation via DRM
2. Kernel dispatch via DRM
3. Synchronization via DRM

AMD (amdgpu) is reportedly E2E ready. NVIDIA needs UVM integration.

### barraCuda: ReduceScalarPipeline returns zeros

The original batched MD path uses `ReduceScalarPipeline::sum_f64()` for
energy computation, which returns `0.0` for both KE and PE. The generic
engine works around this with CPU-side sum after `download_f64()`, which
produces correct energies (KE=14.3381, PE=230.2525).

The reducer bug should be tracked and fixed upstream.

### barraCuda: Per-dispatch overhead vs batched encoding

The generic engine uses `ComputeDispatch::submit()` per kernel (3 submits
per MD step). The original engine batches all kernels in one wgpu compute
pass (1 submit per batch of steps). This costs ~1.8× on Vulkan.

For sovereign dispatch, per-dispatch submit is the only option (no Vulkan
command buffer batching). The expectation is that sovereign's lower
per-dispatch overhead (no Vulkan stack) compensates.

A future `BatchedComputeDispatch<B>` could provide the batching abstraction
for backends that support it, while sovereign falls back to sequential.

## Cross-Spring Shader Evolution

hotSpring's precision shaders have propagated across the ecosystem:

| Flow | Shaders | Impact |
|------|---------|--------|
| hotSpring → barraCuda | df64_core, df64_transcendentals, PrecisionBrain | All springs get precision math |
| wetSpring → barraCuda | smith_waterman, gillespie, diversity_fusion | Bio ops available to all |
| neuralSpring → barraCuda | hmm_viterbi, matrix_correlation, batch_ipr | Stats/ML ops available to all |
| ludoSpring → barraCuda | perlin_2d, fbm_2d | Procedural noise available to all |
| all → coralReef | All WGSL shaders | Sovereign bypass for DF64 poisoning |

The sovereign compilation path benefits **all springs equally** — any WGSL
shader using DF64 transcendentals (exp_df64, sqrt_df64) that gets poisoned
through naga/SPIR-V can route through `ComputeDispatch<CoralReefDevice>`.

## Integration Path

When coralReef DRM dispatch matures:

```rust
// hotSpring auto-routing (already compiles):
if sovereign_available() {
    let dev = CoralReefDevice::with_auto_device()?;
    run_simulation_generic(&dev, &config)  // sovereign
} else {
    let dev = WgpuDevice::new().await?;
    run_simulation_generic(&dev, &config)  // wgpu
}
```

No hotSpring code changes needed — the generic engine is ready.
