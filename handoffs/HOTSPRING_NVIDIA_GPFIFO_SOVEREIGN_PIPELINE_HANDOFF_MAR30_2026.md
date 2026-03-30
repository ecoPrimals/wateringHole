# hotSpring → coralReef / biomeGate: NVIDIA GPFIFO Pipeline Operational

**Date:** 2026-03-30
**From:** hotSpring (strandgate — RTX 3090, RX 6950 XT)
**To:** coralReef (all teams), biomeGate (Titan V / Tesla K80 GPU cracking)
**Status:** NVIDIA command submission pipeline fully operational on RTX 3090

---

## Summary

The NVIDIA GPFIFO command submission pipeline is now **fully operational** on the
RTX 3090 (SM86, Ampere) through coralReef's sovereign `coral-driver`. This is the
first time the sovereign pipeline has successfully submitted and completed GPU work
on a modern NVIDIA GPU without CUDA or nouveau involvement.

The fix required reverse-engineering NVIDIA's 580.x GSP-RM channel initialization
sequence via `LD_PRELOAD` ioctl interception of CUDA's proprietary driver.

## Key Fixes (coralReef `648e042`)

### 1. NV906F_CTRL_CMD_BIND (0x906F0101) — CRITICAL

The compute engine was allocated as a child of the channel but never **bound** to
it. Without BIND, the GPU's PBDMA ignores all push buffer work. The 580.x bind
params struct is `{h_engine: u32, class: u32, class: u32, engine_type: u32}` (16
bytes) — different from the 4-byte `{engine_type: u32}` in open-source headers.

### 2. TSG Scheduling via NVA06C_CTRL_CMD_GPFIFO_SCHEDULE (0xA06C0101)

We were calling `GPFIFO_SCHEDULE` on the **channel** (0xA06F0103) which always
returned `INVALID_ARGUMENT`. CUDA schedules on the **TSG** (channel group, 0xA06C),
not individual channels. Params: `{bEnable: u8}` (3 bytes with padding).

### 3. GET_WORK_SUBMIT_TOKEN via Volta Class (0xC36F0108)

Using Kepler class (0xA06F0108) returns `NOT_SUPPORTED`. Using the channel's own
Ampere class (0xC56F0108) also fails. Only the Volta base class (0xC36F) works.
Returns a small integer token (e.g., 0x2E) — NOT the `cid` from channel allocation.

### 4. VRAM USERD with CUDA-Matching Flags

System memory USERD failed because the 47-bit physical address exceeded the GPU's
DMA range (~40-bit). VRAM allocation with CUDA's exact flags works:

```
flags  = 0x0001C101  (MAP_NOT_REQUIRED | IGNORE_BANK | ALIGNMENT_FORCE | PERSISTENT | KERNEL_PRIV)
attr   = 0x11800000  (GPU_CACHEABLE | PAGE_SIZE_HUGE)
attr2  = 0x00100005  (PAGE_SIZE_HUGE_2MB | GPU_CACHEABLE | 32BIT_ADDRESSABLE)
format = 6
size   = 0x200000    (2 MiB)
align  = 0x200000    (2 MiB)
```

### 5. Error Notifier Configuration

CUDA uses `owner=device_handle` (not client), `mem_type=13` (NVOS32_TYPE_NOTIFIER),
with specific attrs matching system memory notifier pattern.

### 6. 48-byte NVOS64_PARAMETERS for RM_ALLOC

The 580.x driver requires the 48-byte `NVOS64_PARAMETERS` struct for `RM_ALLOC`,
not the 32-byte `NVOS21_PARAMETERS` from older drivers.

### 7. FERMI_CONTEXT_SHARE_A (0x9067) Under TSG

Required on 580.x GSP-RM for proper channel initialization. Must be allocated
before any channels in the group.

### 8. GPFIFO Entry Encoding Fix

The push buffer VA was incorrectly right-shifted by 2 bits. The hardware expects
the 4-byte-aligned VA directly in the lower 42 bits of the GPFIFO entry.

## Correct Channel Initialization Sequence (580.x GSP-RM)

```
Root Client → Device → Subdevice → VOLTA_USERMODE_A (doorbell)
→ FERMI_VASPACE_A → VRAM for USERD (2 MiB) → System mem for GPFIFO
→ Error notifier (type=13, owner=device)
→ TSG (KEPLER_CHANNEL_GROUP_A) → FERMI_CONTEXT_SHARE_A under TSG
→ AMPERE_CHANNEL_GPFIFO_A under TSG (with h_ctxshare, h_err, h_userd)
→ AMPERE_COMPUTE_B under channel → NV906F_BIND (engine to channel)
→ NVA06C_GPFIFO_SCHEDULE on TSG → GET_WORK_SUBMIT_TOKEN (0xC36F)
→ Write GP_PUT to USERD → Ring doorbell (USERMODE+0x90 with token)
```

## Impact on biomeGate (Titan V / Tesla K80)

**This directly unblocks GPU cracking work:**

1. **Channel initialization is architecture-independent** — the BIND, TSG schedule,
   context share, and VRAM USERD patterns apply to Volta (Titan V) and Kepler (K80)
   with the same code paths (class IDs change but the sequence is identical)

2. **The 580.x quirks are driver-version issues**, not GPU-specific — biomeGate's
   Titan V with the same driver version will use identical RM commands

3. **The remaining Titan V blocker is solely L10** (WPR2/FWSEC) — all dispatch
   infrastructure above L10 is now proven working on SM86

4. **K80 has zero security barriers** — with the correct channel init sequence
   now known, K80 sovereign compute should be straightforward once falcon PIO boot
   completes (already implemented in `nv::kepler_falcon`)

## AMD Status

coralReef's sovereign compiler also progressed:
- 24/24 QCD production shaders compile (WGSL → native AMD GFX10.3 ISA) in 102ms
- 38/39 dispatch tests pass on AMD RDNA2
- Remaining: EXEC masking for divergent wavefront control flow
- Key fixes: VOPC operand swap, f64 division precision (Newton-Raphson), uniform
  buffer load ordering, @builtin(num_workgroups), PM4 user data layout

## Files Changed

### coral-driver (NVIDIA)
- `src/nv/uvm/rm_client/alloc.rs` — BIND, TSG schedule, WST, VRAM alloc, error notifier
- `src/nv/uvm/rm_client/mod.rs` — NVOS64 struct handling
- `src/nv/uvm/structs.rs` — NvRmAllocParams (48-byte), NvCtxShareAllocParams
- `src/nv/uvm/mod.rs` — FERMI_CONTEXT_SHARE_A constant
- `src/nv/uvm_compute.rs` — Channel init sequence, BIND integration, cleanup
- `tests/hw_nv_buffers.rs` — Updated from "expect error" to "expect success"

### coral-reef (AMD compiler)
- `src/codegen/amd/encoding.rs` — VOPC operand swap fix
- `src/codegen/amd/shader_model.rs` — Shader model updates
- `src/codegen/lower_f64/newton.rs` — f64 division refinement
- `src/codegen/naga_translate/expr.rs` — Uniform load ordering
- `src/codegen/ops/system.rs` — num_workgroups builtin

## Test Results

- **350** coral-driver unit tests pass (0 failures)
- **4/4** NVIDIA E2E tests pass (device open, alloc/free, sync, SM86 compilation)
- **14/15** hardware-requiring tests pass (1 pre-existing BAR0 issue)
- NOP smoke test: GP_GET advances after doorbell ring ✓

## Next Steps

- [ ] biomeGate: Apply channel init sequence to Titan V / K80 path
- [ ] Dispatch actual compute shaders (not just NOP) on NVIDIA
- [ ] AMD: Fix EXEC masking for divergent control flow
- [ ] Wire QCD physics validation through sovereign pipeline (both vendors)
- [ ] Profile silicon utilization on sovereign path vs wgpu/Vulkan path
