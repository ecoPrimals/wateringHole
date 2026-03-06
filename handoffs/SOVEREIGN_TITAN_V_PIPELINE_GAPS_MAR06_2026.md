# Sovereign Titan V Pipeline — Evolution Gaps

**Date**: March 6, 2026
**From**: hotSpring (v0.6.17)
**To**: barraCuda, toadStool, coralReef teams
**Priority**: Critical — this is the endgame architecture

## The Goal

Run the NVIDIA Titan V (GV100, Volta SM70) at **full native f64 speed**
through a pipeline that has **never heard of NVIDIA**. Zero proprietary
drivers, zero PTXAS, zero nvcc, zero CUDA runtime. Pure Rust, open-source,
sovereign compute.

The Titan V is not on the proprietary driver by design. It runs on
**nouveau** (open-source kernel driver) + **NVK** (Mesa Vulkan) + **NAK**
(Rust shader compiler). The stack we are building replaces the parts
that are slow (NAK for f64) with our own sovereign implementations.

## Current Hardware State

```
PCI 21:00.0 — NVIDIA GeForce RTX 3090 (GA102)
  Driver: nvidia-proprietary 580.119.02
  Vulkan: yes, PTXAS backend
  f64:    1/32 rate (consumer), DF64 preferred

PCI 4b:00.0 — NVIDIA TITAN V (GV100)
  Driver: nouveau (open-source kernel)
  Vulkan: NVK (Mesa 25.1.5, NAK compiler)
  f64:    1/2 rate (native, FULL hardware support)
```

Both GPUs are visible to `wgpu` via Vulkan. The 3090 gets PTXAS (fast f64
via DF64). The Titan V gets NAK (slow f64 — **9-149x gap** vs PTXAS).

## The Performance Gap and Why

NAK (the Rust shader compiler inside Mesa/NVK) generates poor SM70 code
for f64 operations:

| Shader | PTXAS (proprietary) | NAK (open-source) | Gap |
|--------|:-------------------:|:------------------:|:---:|
| Yukawa force (f64) | 1.0× | 9× slower | 9× |
| Complex f64 (sqrt+exp+trig) | 1.0× | 149× slower | 149× |
| Simple f64 (add/mul) | 1.0× | 2-3× slower | 2-3× |

The gap is NOT in the hardware — the Titan V has world-class f64 silicon
(7 TFLOPS). The gap is in the **compiler**: NAK lacks SM70 instruction
scheduling, dual-issue, register allocation optimization, and f64
transcendental lowering that PTXAS has.

## What Each Primal Owns

### The Pipeline (today — broken)

```
WGSL → naga → WGSL text → NAK → (bad) SASS → GPU
                          ^^^^
                    9-149× performance gap
```

### The Pipeline (sovereign — goal)

```
WGSL → naga → SovereignCompiler → SPIR-V → coralReef → (optimal) SASS
                                                              ↓
                                            coralDriver → nouveau/GPU
```

No NVIDIA software touches the shader at any point.

## Evolution Gaps by Primal

### coralReef — Priority: CRITICAL

coralReef is the lynchpin. It compiles WGSL/SPIR-V → native SASS for
SM70 and has DFMA-based f64 transcendentals (sqrt, rcp, exp2, log2,
sin, cos) at full f64 precision. But it cannot **execute** the result.

| Component | Status | Grade |
|-----------|--------|:-----:|
| WGSL/SPIR-V → naga IR | ✅ Complete | A+ |
| naga → NAK SSA IR | ✅ Complete | A+ |
| f64 lowering (DFMA transcendentals) | ✅ Complete | A+ |
| SM70 encoder (SASS emission) | ✅ Core done | A |
| QMD v2.2 (Volta queue descriptors) | ✅ Defined | A |
| **coralDriver (userspace dispatch)** | ❌ Not started | — |

**coralDriver is the #1 blocker.** It needs:

1. **nouveau ioctl interface** — open/map GPU memory via DRM
2. **Command buffer construction** — build pushbuf with QMD + SASS
3. **Fence/sync** — wait for GPU completion, read back results
4. **Memory management** — VRAM allocation, buffer upload/readback

Scaffolding source: NVK's `nvk_cmd_dispatch.c` and nouveau's
`nv50_compute.c` show the ioctl patterns. coralReef already has the
QMD structures (`QMDV02_02_*` for Volta) — just needs the execution
plumbing.

### barraCuda — Priority: HIGH

barraCuda currently **disables its best weapons** on NVK:

| Feature | On proprietary | On NVK | Gap |
|---------|:--------------:|:------:|:---:|
| SovereignCompiler (FMA fusion, dead expr elim) | ✅ SPIR-V passthrough | ❌ Disabled | SovereignCompiler output goes to PTXAS, not NAK |
| DF64 precision | ✅ Full pipeline | ❌ Pipeline validation fails | Complex DF64 shaders produce invalid NAK output |
| SPIR-V passthrough | ✅ Direct to PTXAS | ❌ Excluded for NVK | NAK cannot handle sovereign SPIR-V modules |
| Allocation limit | No limit | ~1.2 GB guard | nouveau PTE fault risk |

**Evolution needed:**

1. **coralReef compilation path** (P1): When coralReef is available, route
   `SovereignCompiler` output to coralReef instead of relying on PTXAS/NAK.
   This means: naga IR → FMA fusion → SPIR-V → coralReef → SASS → coralDriver.

2. **Fix DF64 on NVK** (P2): The DF64 rewriter produces valid WGSL that NAK
   chokes on. Workarounds: simplify compound assignments, avoid transcendentals
   in DF64 shaders, or wait for coralReef to bypass NAK entirely.

3. **coralDriver dispatch path** (P3): Add `ComputeDispatch::CoralReef` variant
   alongside existing `Wgpu` dispatch. When coralDriver is available and
   the GPU is on nouveau, use coralReef + coralDriver instead of wgpu + NVK.

4. **Remove NVK exclusion** (P4): Once coralReef replaces NAK, the
   `has_spirv_passthrough()` NVK guard becomes unnecessary. The
   SovereignCompiler's SPIR-V goes to coralReef, not NAK.

### toadStool — Priority: MEDIUM

toadStool's role is discovery and capability reporting. It needs minimal
changes:

1. **Expose `is_sovereign_capable`** (P1): When coralReef + coralDriver exist,
   report that a GPU can be driven through the sovereign pipeline.

2. **coralDriver routing** (P2): When a GPU is sovereign-capable, toadStool
   should advertise it so barraCuda can choose the sovereign dispatch path.

3. **NVK allocation limits** (P3): Propagate the ~1.2 GB allocation guard
   in `GpuAdapterInfo` so upstream code respects it.

## The Execution Plan

### Phase 1: coralReef → coralDriver (Critical Path)

coralReef can already produce SM70 SASS. The only missing piece is
submitting it to the GPU. This requires:

```rust
// Pseudocode for coralDriver
struct CoralDevice {
    fd: RawFd,             // nouveau DRM fd
    channel: NouvChannel,  // pushbuf channel
}

impl CoralDevice {
    fn alloc_buffer(&self, size: usize) -> CoralBuffer;
    fn upload(&self, buf: &CoralBuffer, data: &[u8]);
    fn dispatch(&self, sass: &[u8], qmd: &Qmd, buffers: &[CoralBuffer]);
    fn sync(&self);
    fn readback(&self, buf: &CoralBuffer) -> Vec<u8>;
}
```

### Phase 2: barraCuda → coralReef Integration

Once coralDriver works, barraCuda wires it in:

```rust
// In ComputeDispatch
match self.dispatch_mode {
    DispatchMode::Wgpu => { /* existing path */ },
    DispatchMode::CoralReef => {
        let sass = coral_reef::compile_wgsl(&shader_source, opts);
        coral_driver.dispatch(&sass, &qmd, &buffers);
    },
}
```

### Phase 3: Full Sovereignty

- Titan V runs at full native f64 (7 TFLOPS)
- SovereignCompiler FMA fusion + coralReef DFMA transcendentals
- No NVIDIA software in the entire path
- Same binary runs on any GPU with a coralReef backend

## What This Unlocks

| Metric | Today (NVK/NAK) | Sovereign (coralReef) | vs Proprietary |
|--------|:----------------:|:---------------------:|:--------------:|
| f64 throughput (Titan V) | ~50 GFLOPS | ~7,000 GFLOPS | ~90% of PTXAS |
| f64 transcendentals | Taylor polyfill | DFMA-native | Equivalent |
| DF64 on RTX 3090 | ❌ (pipeline fail) | ✅ (coralReef path) | Same |
| Largest lattice (Titan V) | ~50K sites | 1.5M+ sites | Limited by 12 GB VRAM |
| Dependencies on NVIDIA | NVK/NAK (Mesa) | nouveau kernel only | Zero userspace |

## Cross-Spring Context

This architecture benefits all springs:

- **hotSpring**: Lattice QCD at full Titan V f64 speed
- **wetSpring**: Bio simulations on any GPU without proprietary drivers
- **neuralSpring**: ML training on sovereign GPU pipeline
- **groundSpring**: Orchestration routing to coralDriver when available

The f64 transcendentals in coralReef (sqrt, exp, sin, cos via DFMA)
originated in hotSpring precision requirements, evolved through barraCuda,
and now live in coralReef where all springs benefit.

## Summary

The Titan V is the test case that proves sovereignty. It has the best f64
hardware of any consumer GPU ever made, but today it runs at 1/149th speed
because NAK's compiler is weak. coralReef already knows how to generate
optimal SASS — it just needs coralDriver to submit it. That single piece
unlocks the full potential of every NVIDIA GPU on the open-source stack,
forever.

The Titan V has never heard of NVIDIA. And it doesn't need to.
