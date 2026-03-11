# hotSpring → Upstream Bug & Deep Debt Guidance

**Date**: 2026-03-09
**From**: hotSpring v0.6.29 (848 tests, 115 binaries, 0 clippy, 0 TODO/FIXME)
**To**: barraCuda, coralReef, toadStool teams
**Priority**: Ordered by impact on hotSpring production workloads

---

## P0: Blocking Production

### 1. ReduceScalarPipeline returns zeros [barraCuda]

**Impact**: All energy monitoring in batched MD path reports KE=0, PE=0.
**Workaround**: hotSpring's generic engine uses CPU-side `download_f64()` + sum.
**Location**: `barracuda::pipeline::ReduceScalarPipeline::sum_f64()`
**Reproduction**: `cargo run --release --bin bench_md_parity` — observe `KE=0.0000, PE=0.0000`.
**Root cause**: Unknown — likely bind group layout or readback mapping issue in the reduce shader.
**Guidance**: The reduction shader compiles and dispatches without error; the output buffer reads back as all zeros. Check the `reduce_f64.wgsl` bind group layout, output buffer mapping, and workgroup size vs element count. Compare against the known-working `ComputeDispatch<WgpuDevice>` pattern.

### 2. coral-driver nvidia-drm dispatch ioctl [coralReef]

**Impact**: Sovereign dispatch blocked on NVIDIA GPUs (proprietary + NVK).
**Error**: `DRM ioctl returned 22` (EINVAL) from `CoralReefDevice::dispatch_compute()`.
**Location**: `coral-driver/src/drm.rs` (nvidia-drm kernel interface).
**What works**: `CoralReefDevice::with_auto_device()` succeeds, hardware detected. `compile_wgsl()` produces valid SASS for SM70/SM86. Kernel cache works.
**What fails**: Buffer allocation and/or kernel dispatch via DRM ioctl.
**Guidance**: The NVIDIA DRM kernel module exposes limited ioctls compared to the proprietary userspace driver. UVM (Unified Virtual Memory) buffer management is the likely gap. AMD (amdgpu) is reportedly E2E ready — validate there first, then port buffer management patterns to nvidia-drm.

---

## P1: Performance

### 3. Per-dispatch overhead vs batched encoding [barraCuda]

**Impact**: 1.8× slower on wgpu when using `ComputeDispatch::submit()` vs batched encoder (140 vs 257 steps/s at N=2000).
**Context**: The `GpuBackend` trait's `dispatch_compute` does a full command-buffer submit per call. The original wgpu MD path batches 3-4 kernels per step into one compute pass.
**Guidance**: Consider adding a `BatchedComputeDispatch<B>` that accumulates dispatches and submits them in one command buffer. For wgpu, this maps to the existing compute pass batching. For sovereign, it could either batch kernel launches or fall back to sequential dispatch (sovereign's per-dispatch overhead is already much lower than Vulkan).

### 4. Kokkos-CUDA gap: 11-12× [barraCuda + toadStool]

**Impact**: barraCuda 140-257 steps/s vs Kokkos 2897 steps/s at N=2000 on RTX 3090.
**Root causes** (from Exp 054 N-scaling analysis):
- **Dispatch overhead**: barraCuda submits via Vulkan command buffers; Kokkos launches CUDA kernels directly. ~3-5× at small N.
- **Arithmetic throughput**: Native f64 on Ampere is 1:64 vs FP32. DF64 (f32-pair) is the fix but currently poisoned through naga. Sovereign bypass unlocks this.
- **Algorithm**: AllPairs is O(N²); Kokkos uses Verlet (O(N·M)). hotSpring has Verlet but the generic engine only supports AllPairs currently.
- **Scaling exponent**: barraCuda α≈2.30 vs Kokkos α≈1.38.
**Guidance**: The single largest win is sovereign DF64 dispatch (bypasses naga poisoning, unlocks FP32 core throughput). Second is batched dispatch. Third is Verlet list in the generic engine.

---

## P2: Correctness

### 5. naga WGSL→SPIR-V DF64 transcendental codegen bug [upstream naga / wgpu]

**Impact**: `exp_df64()` and `sqrt_df64()` produce zero output when compiled through naga → SPIR-V on ALL Vulkan backends (NVIDIA proprietary, NVK, llvmpipe).
**Diagnosis**: hotSpring Exp 055. The DF64 transcendental functions use multi-component f32-pair arithmetic that naga's SPIR-V backend miscompiles. Simple DF64 arithmetic (add, mul, div) works correctly; it's the iterative transcendentals that break.
**Workaround**: hotSpring gates DF64 transcendentals with `has_nvvm_df64_poisoning_risk()` and falls back to native f64. coralReef's sovereign path bypasses naga entirely.
**Guidance**: This should be filed as a naga bug (gfx-rs/wgpu). The minimal reproducer: compile `df64_transcendentals.wgsl` (exp_df64 function) through naga to SPIR-V, dispatch on any Vulkan GPU, read back forces — all zeros. The same WGSL compiled through coralReef → SASS produces correct output.

---

## P3: Feature Gaps

### 6. Verlet/CellList in generic engine [hotSpring, pending barraCuda]

**Impact**: The backend-agnostic `MdEngine<B>` only supports AllPairs force method. Verlet needs `VerletListGpu` to be generic over `GpuBackend` (currently wgpu-only). CellList needs `CellListGpu` similarly.
**Guidance**: `VerletListGpu` uses raw wgpu pipeline/bind-group/dispatch patterns. Migrating to `ComputeDispatch<B>` would make it backend-agnostic. Same for `CellListGpu`'s 3-pass build (cell_bin, prefix_sum, cell_scatter).

### 7. AMD GPU validation [hotSpring + coralReef]

**Impact**: coralReef reports amdgpu DRM dispatch is E2E ready, but hotSpring has no AMD hardware to validate. The generic engine should work on RDNA2+ via sovereign dispatch.
**Guidance**: If anyone has RDNA2+ hardware, run `cargo run --release --features sovereign-dispatch --bin bench_sovereign_dispatch`. The wgpu path should also work via RADV.

### 8. toadStool `PrecisionHint` integration [toadStool]

**Impact**: hotSpring's `PrecisionBrain` runs locally; toadStool S145 absorbed it with `PrecisionHint` routing. The two should converge — hotSpring's local version does actual dispatch probes while toadStool's is config-driven.
**Guidance**: Consider adding a `probe_dispatch` method to toadStool's PrecisionBrain that does what hotSpring does: compile a test shader, dispatch, read back, check for zeros. This catches naga poisoning at runtime rather than relying on config.

---

## Cross-Spring Shader Evolution (for reference)

| Shader | Origin | Absorbed By | Sovereign Status |
|--------|--------|-------------|-----------------|
| df64_core.wgsl | hotSpring | barraCuda → all | Validated (Iter 33) |
| df64_transcendentals.wgsl | hotSpring | barraCuda, coralReef | Validated (Iter 33) |
| yukawa_force_f64.wgsl | hotSpring | barraCuda md/ | Validated |
| smith_waterman_f64.wgsl | wetSpring | barraCuda bio/ | Ready |
| hmm_viterbi_f64.wgsl | neuralSpring | barraCuda bio/ | Ready |
| matrix_correlation_f64.wgsl | neuralSpring | barraCuda stats/ | Ready |
| perlin_2d_f64.wgsl | ludoSpring | barraCuda procedural/ | Ready |
| PrecisionBrain | hotSpring v0.6.25 | barraCuda a012076 | N/A (Rust, not shader) |

All 805 barraCuda WGSL shaders can route through `ComputeDispatch<CoralReefDevice>`
once DRM dispatch matures.

---

## hotSpring Health Summary

| Metric | Value |
|--------|-------|
| Lib tests | 848/848 pass |
| Binaries | 115 |
| WGSL shaders | 85 (local) |
| Clippy warnings | 0 (lib + bins) |
| TODO/FIXME | 0 |
| unsafe | 0 |
| Validation suites | 39/39 pass |
| barraCuda pin | `875e116` |
| coralReef sync | Iter 33 |
| toadStool sync | S146 |
