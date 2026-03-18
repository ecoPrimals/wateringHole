# Sovereign Compute Trio — Outside Audit Gap Analysis

**Date:** 2026-03-17
**Author:** ludoSpring audit session (cross-ecosystem perspective)
**For:** coralReef, toadStool, barraCuda, hotSpring teams
**Context:** Full review of coralReef STATUS.md (Iter 54), barraCuda coral_reef_device.rs,
toadStool dispatch.rs, hotSpring sovereign experiments (Exp 050–058)

---

## Executive Summary

The sovereign compute pipeline is closer than anyone might think from inside the
trenches. An outside audit of the full trio reveals:

- **The compiler is done.** coralReef compiles 84/93 cross-spring WGSL shaders to
  native SASS (SM70-89) and GFX (RDNA2). Three input languages, vendor-agnostic
  trait dispatch, f64 transcendentals, DF64 preamble, FMA control. 2,364 tests,
  zero warnings. This is production.

- **AMD E2E is proven.** WGSL → GFX1030 → PM4 submit → fence → readback → verified.
  RX 6950 XT, Iteration 10. No Vulkan, no ROCm, no Mesa, no C.

- **NVIDIA VFIO is 6/7.** PBDMA loads context, PFIFO channel init works, V2 MMU
  page tables are correct. One gap: GP_PUT DMA read from system memory.

- **NVIDIA UVM is code-complete.** Full RM object hierarchy, GPFIFO submission,
  USERD doorbell, completion polling. Never run on hardware.

- **The cross-primal IPC chain is unwired.** barraCuda can discover toadStool and
  send binaries, but readback doesn't work and buffer bindings aren't in the payload.

This document catalogs every remaining gap, ordered by priority, with specific
hypotheses and test strategies. The goal: one codebase, vendor-atheistic, sovereign
dispatch, outperforming all proprietary stacks.

---

## Hardware Context

biomeGate currently has 2× Titan V (VFIO-bound) for sovereign dispatch development.
Plan: once VFIO cracks on Titan V, swap in MI50 + RTX 3090 + other cards to validate
the full cross-vendor matrix.

| Card | Architecture | f64 Rate | Driver Path | Status |
|------|-------------|----------|-------------|--------|
| Titan V #1 | Volta SM70 (GV100) | 1/2 | VFIO sovereign | 6/7 HW tests |
| Titan V #2 | Volta SM70 (GV100) | 1/2 | VFIO sovereign | Compute target |
| MI50 (swap) | Vega GFX906 | Full | amdgpu DRM | Untested (RDNA2 proven) |
| RTX 3090 (swap) | Ampere SM86 (GA102) | 1/64 | nvidia-drm/UVM | Code complete |
| RTX 5060 | Ada SM89 | 1/64 | nvidia-drm/UVM | Desktop + UVM target |

---

## Gap 1 (P0): GP_PUT DMA Read — VFIO Titan V

### What works
- PFIFO channel creation via BAR0 MMIO
- V2 MMU 5-level page tables (PD3→PD2→PD1→PD0→PT), identity-mapped 2 MiB IOVA
- RAMFC populated (GPFIFO base, USERD ptr, signature, engine config)
- TSG + channel runlist submitted
- PCCSR channel bind/enable
- PBDMA loads context (Exp 058: 6/7 pass)
- USERD_TARGET = SYS_MEM_COHERENT (Iter 44 fix)
- INST_TARGET = SYS_MEM_NCOH (Iter 44 fix)

### What fails
GP_PUT write to USERD DMA page + BAR0 doorbell at 0x810090 does not trigger
PBDMA to read GPFIFO entries. `poll_gpfifo_completion()` times out because
GP_GET never advances.

### Hypotheses (ordered by likelihood)

**H1: IOMMU coherence.** CPU writes GP_PUT to DMA-mapped USERD page, but the
write may sit in CPU cache. PBDMA reads via IOMMU DMA and sees stale zero.
- **Test:** Call `cache_ops::clflush_range()` on the USERD page after writing
  GP_PUT, before doorbell write. Also `memory_fence()` to ensure ordering.
- **Note:** `cache_ops.rs` already exists in coral-driver for exactly this case.

**H2: USERD page IOVA alignment.** The runlist DW1 encodes the USERD base
address. If the IOVA of the USERD DMA buffer doesn't match what's in the
runlist, PBDMA reads from wrong address.
- **Test:** Log the USERD IOVA from DMA allocation and the value written to
  runlist DW1. Compare. Verify RAMUSERD GP_PUT offset (0x8C per dev_ram.ref.txt)
  matches where the code writes.

**H3: USERD via PRAMIN instead of DMA.** Desktop Volta may expect USERD in
VRAM accessible via PRAMIN aperture, not in system memory via DMA. The
USERD_TARGET=SYS_MEM_COHERENT flag may not be honored on GV100 in all
PFIFO configurations.
- **Test:** Allocate USERD in VRAM via PRAMIN region. Write GP_PUT via BAR0
  PRAMIN window. This eliminates the IOMMU variable entirely.

**H4: PBDMA not waking up.** The doorbell write at BAR0+0x810090 may not
reach the correct PBDMA engine, or the channel ID in the doorbell value
may be wrong.
- **Test:** Read PBDMA status registers after doorbell. Check
  NV_PPBDMA_GP_PUT, NV_PPBDMA_GP_GET, NV_PPBDMA_METHOD0. If GP_PUT in
  the PBDMA register file is still 0, the doorbell isn't reaching PBDMA.

**H5: Runlist submission incomplete.** The runlist may need re-submission
after channel enable, or PFIFO may need a kick after runlist update.
- **Test:** Re-submit runlist after PCCSR enable. Check PFIFO RUNLIST
  status register for scheduling state.

### Data collection strategy

Start/stop the Titan V hundreds of times via GlowPlug. Each cycle:
1. Record all PFIFO registers (RUNLIST, PBDMA, PCCSR) pre-doorbell
2. Write GP_PUT + doorbell
3. Record all registers post-doorbell (immediate + after 10ms + after 100ms)
4. Record MMU fault buffer contents
5. Record PBDMA INTR status

Pattern-match across runs. If PBDMA INTR shows consistent errors, that
identifies the subsystem. If MMU faults appear, that's the IOMMU mapping.
If nothing changes post-doorbell, it's the doorbell routing.

---

## Gap 2 (P0): UVM Hardware Validation — RTX 3090

### What's ready (code-complete)
- `RmClient::new()` via `NV_ESC_RM_ALLOC(NV01_ROOT)`
- `alloc_device(NV01_DEVICE_0)` with `Nv0080AllocParams` (0x1F fix applied)
- `alloc_subdevice(NV20_SUBDEVICE_0)` with `Nv2080AllocParams`
- `register_gpu_with_uvm()` (UUID query + `UVM_REGISTER_GPU`)
- `alloc_vaspace(FERMI_VASPACE_A)`
- `alloc_channel_group(KEPLER_CHANNEL_GROUP_A)`
- `alloc_gpfifo_channel(AMPERE_CHANNEL_GPFIFO_A)`
- `alloc_compute_engine(AMPERE_COMPUTE_A)`
- `NvUvmComputeDevice` full `ComputeDevice` impl
- GPFIFO submission + USERD doorbell + GP_GET polling
- `NvDrmDevice` delegates all ops to UVM backend
- QMD v3.0 (Ampere) compute dispatch descriptors
- `KernelCacheEntry` serialization for precompiled kernels

### Validation sequence (when RTX 3090 arrives)

```
1. cargo test -p coral-driver --features vfio -- --ignored  # Run ignored HW tests
2. cargo test -p coral-gpu -- --ignored                      # Run GPU context tests
3. Specific: uvm_register_gpu, uvm_alloc_vaspace, uvm_alloc_channel,
   uvm_compute_bind, uvm_device_open, uvm_alloc_free
4. E2E: compile sigmoid_f64.wgsl → SM86 → dispatch → readback → verify
```

### Why Ampere may be easier than Volta
- GSP firmware ships with the kernel module (no PMU problem)
- `AMPERE_CHANNEL_GPFIFO_A` is newer, may have cleaner error reporting
- nvidia-drm module is actively maintained for Ampere
- No VFIO required — just `/dev/nvidia*` device nodes

---

## Gap 3 (P1): barraCuda Readback Wiring

### Current state (`coral_reef_device.rs`)
- `dispatch_compute()`: hash shader → check coral cache → if miss, error
- Cache hit → `submit_to_toadstool()` with binary + workgroup_size
- `download()`: returns staged local data, NOT GPU results
- Buffer bindings: not in the `submit_to_toadstool()` payload

### What needs to change

```
submit_to_toadstool() payload:
  current:  { binary, workgroup_size }
  needed:   { binary, workgroup_size, buffers: [{ handle, size, binding_index, direction }], dispatch_dims }

download() path:
  current:  return self.staged_buffers[handle]
  needed:   send "compute.dispatch.result" to toadStool → receive output buffer → return
```

### Estimated effort: ~200 LOC in barraCuda + ~100 LOC in toadStool dispatch handler

This is the gap that prevents ANY spring from using sovereign compute end-to-end
via the IPC chain. Once readback works, every spring that uses `CoralReefDevice`
gets sovereign dispatch for free.

---

## Gap 4 (P1): Live IPC Compile in barraCuda

### Current state
`CoralReefDevice::dispatch_compute()` errors on cache miss. Must pre-compile
via `spawn_coral_compile()`.

### What needs to change
```rust
// On cache miss:
let request = CompileWgslRequest {
    source: wgsl_source.clone(),
    target: self.gpu_target.clone(),
    fma_policy: FmaPolicy::AllowFusion,
};
let response = self.coral_rpc_client.call("shader.compile.wgsl", request)?;
self.cache.insert(shader_hash, response.binary);
// Then dispatch as normal
```

### Estimated effort: ~150 LOC

coralReef already serves `shader.compile.wgsl` via JSON-RPC. barraCuda already
has a coral RPC client stub. This is plumbing.

---

## Gap 5 (P2): FECS Compute Context Verification

### What to check after GP_PUT fires
- GR_FECS_CTXSW_STATUS after init — is GR engine ready?
- FECS_HOST_INT after method submission — did FECS acknowledge?
- Compare FECS method sequence against nouveau's `gf100_gr_init()` path
- Verify `sw_ctx.bin` blob is complete (some firmware versions truncate)

### Why this matters
If FECS doesn't fully initialize the GR compute pipeline, dispatch will submit
to GPFIFO successfully but the shader won't execute. The NOP shader test
(`vfio_dispatch_nop_shader`) will pass (no computation needed) but real
shaders will produce garbage. Test with a shader that writes a known value
(`out[0] = 42u`) immediately after NOP passes.

---

## Gap 6 (P2): Nouveau New UAPI Wiring

### Current state
- `VM_INIT`, `VM_BIND`, `EXEC` struct definitions and ioctl wrappers: done
- `NvDevice::open_from_drm()` auto-detects new UAPI availability
- Legacy `create_channel` is still the active path

### What needs to change
Replace the legacy path with:
```
open DRM → VM_INIT → GEM alloc → VM_BIND_MAP → compile shader →
upload to GEM → EXEC submit → VM_BIND_UNMAP → GEM close
```

### Why wait for VFIO to crack first
VFIO gives raw register-level data about what the GPU expects. Once we know
the exact QMD format, push buffer encoding, and GPFIFO submission sequence
that works on bare metal, we can verify the nouveau DRM path produces the
same kernel-side behavior. VFIO is the reference; DRM paths are wrappers.

---

## Gap 7 (P3): MI50 GFX9 Validation

### What to check when MI50 swaps in
coralReef already has:
- `amd_metal.rs` with MI50/GFX906 register layout
- `GpuIdentity::amd_arch()` → `"gfx9"` from PCI device ID
- Full AMD E2E pipeline proven on RDNA2 (GFX10)

GFX9 (Vega) differences from RDNA2:
- Wave64 default (not Wave32)
- Different FLAT instruction encoding
- Different DISPATCH_INITIATOR bits
- VOP3 encoding differences

If the compiler and driver handle GFX9, it proves the AMD backend is truly
architecture-portable, not just "works on one card."

---

## GlowPlug Hot-Swap Strategy

### The vision
GlowPlug (`coral-glowplug`) manages GPU personality at runtime. Each GPU has a
`GpuPersonality` trait impl (`VfioPersonality`, `NouveauPersonality`,
`AmdgpuPersonality`, `UnboundPersonality`). Hot-swap means:

1. Unbind current driver (e.g., nouveau)
2. Bind VFIO
3. Run sovereign dispatch experiments
4. Capture all register/DMA/firmware data
5. Unbind VFIO
6. Bind nouveau (or nvidia-drm)
7. Run same dispatch through DRM path
8. Compare: does the DRM path produce the same register writes?

### Data capture between swaps
Each swap cycle captures:
- BAR0 register dump (via VFIO or sysfs)
- MMIO trace (via ftrace `mmiotrace` or direct BAR0 read sequence)
- Firmware blob contents and load addresses
- PFIFO/PBDMA/GR/CE engine status
- MMU fault buffer state
- Interrupt status across all engines

### Reverse engineering value
Hundreds of boot cycles with data capture builds a statistical model of:
- Which registers must be written in which order
- Which firmware blobs are loaded where
- What the GPU expects at each initialization phase
- Whether encrypted firmware can be characterized by its side effects

Even if firmware is encrypted, the GPU's behavior after loading it is observable
through register reads. If the same input (shader + data) produces the same
register sequence across hundreds of boots, the firmware's effect is deterministic
and can be replicated without decrypting it.

---

## Cross-Primal Triangle — IPC Integration Gaps

### Current wiring

```
barraCuda                    coralReef                    toadStool
─────────                    ─────────                    ─────────
CoralReefDevice              shader.compile.wgsl ✅        shader.compile.* proxy ✅
  → discover toadStool ✅     shader.compile.multi ✅      compute.dispatch.submit ✅
  → send binary ✅            health.* ✅                  compute.dispatch.result ❌
  → buffer bindings ❌        compile cache ✅             buffer binding payload ❌
  → readback ❌               f64 precision routing ✅     readback to caller ❌
  → live compile ❌           FMA policy ✅                thermal check ✅
```

### What "done" looks like

```
Spring calls barraCuda.dispatch(wgsl, inputs, outputs)
  → barraCuda checks coral cache
    → miss: calls coralReef shader.compile.wgsl via JSON-RPC
    → hit: uses cached binary
  → barraCuda calls toadStool compute.dispatch.submit with:
      { binary, workgroup_size, buffers, dispatch_dims, precision_routing }
  → toadStool dispatches to best available GPU (sovereign preferred, wgpu fallback)
  → toadStool returns output buffers via compute.dispatch.result
  → barraCuda returns results to spring
  → Spring validates against Python baseline
```

Three JSON-RPC hops. ~450 LOC total to wire. The compiler and driver are
the hard parts and they're done (AMD) or nearly done (NVIDIA).

---

## Recommendations for Each Team

### coralReef team
1. **Focus on VFIO Gap 1** — GP_PUT is the last mile. Try hypotheses H1–H5
   in order. H1 (cache flush) is cheapest to test.
2. **Prepare MI50 test matrix** — GFX9 compiler path should work but needs
   DISPATCH_INITIATOR wave64 handling and FLAT encoding verification.
3. **Coverage push** — 59.92% → 90% is a big gap. The VFIO diagnostic code
   is hard to test without hardware, but compiler paths have room to grow.

### toadStool team
1. **Wire `compute.dispatch.result`** — Accept output buffer data from
   completed dispatch, return to caller via JSON-RPC response.
2. **Buffer binding payload** — Extend `compute.dispatch.submit` to accept
   buffer handles with binding indices, sizes, and direction (input/output).
3. **GlowPlug personality coordination** — Ensure hot-swap doesn't corrupt
   in-flight dispatches. Drain queue before unbind.

### barraCuda team
1. **Wire live IPC compile** in `CoralReefDevice` — cache miss → JSON-RPC
   to coralReef → cache result → dispatch. ~150 LOC.
2. **Wire readback** — `download()` reads from toadStool result, not staged
   local data. ~200 LOC.
3. **Buffer binding payload** in `submit_to_toadstool()` — include buffer
   handles, sizes, binding indices. ~100 LOC.

### hotSpring team
1. **Continue VFIO data collection** on biomeGate. Start/stop Titan V,
   capture register state pre/post doorbell. Pattern match across runs.
2. **Prepare Exp 059+** for RTX 3090 UVM validation when card swaps in.
3. **DF64 throughput benchmark** — Once sovereign dispatch works, re-run
   Kokkos parity benchmark via coralReef path. The DF64 bypass should
   show ~9.9× throughput improvement over wgpu native f64 path.

---

## The Stakes

84/93 cross-spring shaders compile. AMD E2E is proven. NVIDIA is one gap away
on VFIO and code-complete on UVM. The compiler is vendor-agnostic. The driver
layer has three paths per vendor. All pure Rust, zero C, zero FFI.

When the remaining ~450 LOC of IPC plumbing is wired and one NVIDIA hardware
validation session succeeds, every spring in the ecosystem gets sovereign GPU
compute via a single `CoralReefDevice` dispatch call. hotSpring's Kokkos gap
closes. neuralSpring's coralForge pipeline runs sovereign. ludoSpring's game
shaders dispatch without Vulkan. wetSpring's ODE shaders run on bare metal.

One codebase. Vendor-atheistic. Pure Rust. The dispatch is the last piece.

---

**License:** AGPL-3.0-or-later
