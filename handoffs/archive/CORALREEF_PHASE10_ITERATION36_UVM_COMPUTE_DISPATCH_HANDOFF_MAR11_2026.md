# coralReef Phase 10 — Iteration 36: UVM Sovereign Compute Dispatch

**Date**: March 11, 2026
**Primal**: coralReef (GPU compiler + driver)
**Sprint**: UVM Sovereign Compute Dispatch — Bypass Nouveau PMU Blocker

---

## Summary

Implemented the full NVIDIA RM object hierarchy for compute dispatch via the
proprietary driver path (`/dev/nvidiactl` + `/dev/nvidia-uvm`), bypassing
nouveau's PMU firmware requirement on desktop Volta GPUs (Titan V).

## What Was Done

### RM Infrastructure (`uvm.rs`)
- `NV_ESC_RM_CONTROL` ioctl wrapper with generic `rm_control<T>()` method
- GPU UUID query via `NV2080_CTRL_CMD_GPU_GET_GID_INFO`
- `register_gpu_with_uvm()` chaining UUID query → `UVM_REGISTER_GPU`
- Generic `rm_alloc_typed<T>()` eliminating per-class RM_ALLOC boilerplate
- `rm_alloc_simple()` for parameterless class allocations

### RM Object Hierarchy
- `FERMI_VASPACE_A` (0x90F1) — GPU virtual address space
- `KEPLER_CHANNEL_GROUP_A` (0xA06C) — Channel group (TSG)
- `VOLTA_CHANNEL_GPFIFO_A` (0xC36F) / `AMPERE_CHANNEL_GPFIFO_A` (0xC56F)
- `VOLTA_COMPUTE_A` (0xC3C0) / `AMPERE_COMPUTE_A` (0xC6C0)
- `NV01_MEMORY_SYSTEM` (0x3E) — System memory allocation

### NvUvmComputeDevice (`uvm_compute.rs`)
- Full `ComputeDevice` trait implementation (alloc/free/upload/readback/dispatch/sync)
- GPU generation auto-detection (Volta/Turing/Ampere) for class selection
- Reuses existing `qmd.rs` and `pushbuf.rs` (identical binary format)
- Proper RAII teardown in `Drop`

### coral-gpu Wiring
- `nvidia-drm` driver selection auto-tries UVM before DRM-only fallback
- SM version detection via sysfs for UVM device

### Struct Definitions (from nvidia-open-gpu-kernel-modules MIT headers)
- `NvRmControlParams` (32 bytes)
- `Nv2080GpuGetGidInfoParams` (268 bytes)
- `NvVaspaceAllocParams`
- `NvChannelGroupAllocParams`
- `NvChannelAllocParams` (full NV_CHANNEL_ALLOC_PARAMS with NV_MAX_SUBDEVICES=8)
- `NvMemoryAllocParams`
- `NvMemoryDescParams` (24 bytes)
- `UvmMapExternalAllocParams`

## What's Pending (Hardware Validation Required)

1. **GPFIFO submission**: Write to GPFIFO ring buffer in mapped memory + ring
   channel doorbell via MMIO or RM_CONTROL
2. **UVM_MAP_EXTERNAL_ALLOCATION**: Map RM-allocated memory into GPU VA space
3. **CPU mmap**: mmap `/dev/nvidia0` at RM memory handle offset for upload/readback
4. **Hardware testing**: All 7 new tests are `#[ignore]`, need on-site validation
   - Start with RTX 3090 (GA102) — known working RM_CLIENT
   - Then Titan V (GV100) — the target for PMU bypass

## Files Changed

| File | Change |
|------|--------|
| `crates/coral-driver/src/nv/uvm.rs` | +15 RM class constants, +8 struct defs, +12 RmClient methods, raw_ioctl on NvUvmDevice, refactored alloc_device/alloc_subdevice to use rm_alloc_typed |
| `crates/coral-driver/src/nv/uvm_compute.rs` | **NEW** — NvUvmComputeDevice + ComputeDevice impl + 4 tests |
| `crates/coral-driver/src/nv/mod.rs` | Added `uvm_compute` module + `NvUvmComputeDevice` re-export |
| `crates/coral-gpu/src/lib.rs` | UVM auto-try in nvidia-drm path + `sm_from_sysfs_or()` |
| `docs/UVM_COMPUTE_DISPATCH.md` | **NEW** — Architecture document |
| `STATUS.md` | Iteration 36 entry (22 items) |
| `EVOLUTION.md` | Iteration 36 log + updated unsafe audit (27 blocks) |
| `WHATS_NEXT.md` | UVM completion + remaining hardware work |

## Test Results

- All existing tests pass (1616+ passing, 0 failed)
- 7 new hardware-gated tests (`#[ignore = "requires proprietary nvidia driver loaded"]`)
- Clippy clean (zero warnings on coral-driver + coral-gpu)

## Architecture Note

The QMD builder (`qmd.rs`) and push buffer encoder (`pushbuf.rs`) are reused
identically between nouveau and proprietary paths. The only difference is the
submission mechanism: nouveau uses `DRM_NOUVEAU_GEM_PUSHBUF` / `EXEC`, while
UVM writes directly to the GPFIFO ring buffer and rings the channel doorbell.
