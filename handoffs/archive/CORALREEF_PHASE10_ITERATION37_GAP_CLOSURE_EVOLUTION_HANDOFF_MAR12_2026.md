# coralReef Phase 10 — Iteration 37: Gap Closure + Deep Debt Evolution

**Date**: March 12, 2026
**Primal**: coralReef (GPU compiler + driver)
**Sprint**: Gap closure — wiring gaps, unsafe evolution, dispatch pipeline completion

---

## Summary

Closed remaining wiring gaps from the sovereign compute evolution audit.
The NVIDIA UVM dispatch pipeline is now complete end-to-end in code (GPFIFO
submission, USERD doorbell, completion polling). NvDrmDevice evolved from a
stub to a functional delegator. The `dispatch_binary` API surface is wired
for barraCuda kernel cache integration. Deep debt solutions applied:
`bytemuck::Zeroable`, centralized PCI constants, capability-based AMD
detection, smart refactoring of the UVM module.

## What Was Done

### Gap 1: dispatch_binary Wiring (barraCuda Integration)
- `KernelCacheEntry` struct (`serde::Serialize` + `serde::Deserialize`) for on-disk kernel caching
- `CompiledKernel::to_cache_entry()` / `from_cache_entry()` conversion methods
- `GpuContext::dispatch_precompiled()` — dispatch raw binary with explicit metadata
- `GpuTarget::arch_name()` — canonical string identifier per architecture (`"sm86"`, `"rdna2"`, etc.)
- `NvArch::short_name()`, `AmdArch::short_name()`, `IntelArch::short_name()` — per-arch identifiers

### Gap 2: GPFIFO Submission + Completion
- `submit_gpfifo()` writes GPFIFO entry to CPU-mapped ring buffer
- Updates `gp_put` index and writes to USERD `GP_PUT_OFFSET` doorbell register
- `poll_gpfifo_completion()` polls `GP_GET` from USERD until catch-up or timeout
- `NvUvmComputeDevice::dispatch()` orchestrates full pipeline: upload shader → build QMD → upload QMD → construct PushBuf → submit GPFIFO → doorbell
- CPU-mapped USERD and GPFIFO ring memory via `rm_map_memory()`
- `gpu_map_buffer()` wrapper for real GPU virtual address acquisition

### Deep Debt: Unsafe Evolution
- `bytemuck::Zeroable` + `bytemuck::Pod` derives on 5 UVM `#[repr(C)]` structs
- `unsafe { std::mem::zeroed() }` → safe `Self::zeroed()` in all Default impls
- `NvMemoryDescParams`, `NvChannelAllocParams`, `NvMemoryAllocParams`, `UvmGpuMappingAttributes`, `UvmMapExternalAllocParams`

### Deep Debt: Hardcoding Elimination
- `PCI_VENDOR_NVIDIA` (0x10DE), `PCI_VENDOR_AMD` (0x1002), `PCI_VENDOR_INTEL` (0x8086) constants
- `GpuIdentity::amd_arch()` — PCI device ID → architecture string (capability-based)
- `discovery.rs` uses `probe_gpu_identity()` + `amd_arch()` for dynamic AMD detection
- Diagnostic example `diag_ioctl.rs` uses symbolic `VOLTA_COMPUTE_A` instead of magic `0xC3C0`

### Deep Debt: Smart Refactoring
- `uvm.rs` monolith (727 LOC) → `uvm/mod.rs` (897) + `uvm/structs.rs` (592) + `uvm/rm_client.rs` (987)
- `raw_nv_ioctl` helper extracted from repeated unsafe ioctl pattern in `rm_client.rs`
- Compute class constants unified: `pushbuf.rs` re-exports from `uvm/mod.rs` (single source of truth)
- `NV_STATUS` codes refactored into documented `nv_status` module

### Production Mock Evolution
- `NvDrmDevice` evolved from stub to delegator: holds `Option<NvUvmComputeDevice>`
- On open, probes GPU SM version and initializes UVM backend if available
- All `ComputeDevice` trait methods delegate to UVM backend

## Files Changed

| File | Change |
|------|--------|
| `crates/coral-driver/src/nv/uvm/mod.rs` | Refactored from `uvm.rs`: constants, `nv_status` module, device infrastructure |
| `crates/coral-driver/src/nv/uvm/structs.rs` | All `#[repr(C)]` structs with `bytemuck::Zeroable` + safe `Default` |
| `crates/coral-driver/src/nv/uvm/rm_client.rs` | RM client methods + `raw_nv_ioctl` helper + rm_map_memory/dma |
| `crates/coral-driver/src/nv/uvm_compute.rs` | GPFIFO submission, USERD doorbell, completion polling, full dispatch |
| `crates/coral-driver/src/nv/nvidia_drm.rs` | Stub → delegator with `Option<NvUvmComputeDevice>` |
| `crates/coral-driver/src/nv/identity.rs` | PCI vendor constants + `amd_arch()` |
| `crates/coral-driver/src/nv/pushbuf.rs` | Re-exports compute class constants from `uvm` |
| `crates/coral-gpu/src/lib.rs` | `KernelCacheEntry`, `dispatch_precompiled()`, serde wiring |
| `crates/coral-reef/src/gpu_arch.rs` | `arch_name()`, `short_name()` per architecture |
| `crates/coralreef-core/src/discovery.rs` | Capability-based AMD detection via `amd_arch()` |

## Test Results

- 1635 passing, 0 failed, 63 ignored (+19 passing, +8 ignored vs Iteration 36)
- All existing tests pass — zero regressions
- New hardware-gated tests for UVM dispatch pipeline
- Clippy clean (zero warnings workspace-wide)

## What's Pending (Hardware Validation)

1. **RTX 3090 UVM dispatch** — Full pipeline code-complete, needs on-site validation
2. **Titan V nouveau** — PMU firmware blocker; UVM path may bypass on Volta too
3. **barraCuda integration** — `KernelCacheEntry` API surface ready for consumption

## Handoff Notes for Other Primals

### barraCuda
- `KernelCacheEntry` is the serialization format for on-disk kernel caching
- `GpuContext::dispatch_precompiled(binary, gpr_count, shared_mem_bytes, ...)` is the dispatch entry point
- `GpuTarget::arch_name()` returns the cache key string (e.g., `"sm86"`)
- `CompiledKernel::to_cache_entry()` / `from_cache_entry()` for round-trip serialization

### toadStool
- Gap 3 (FECS channel submission for Volta) and Gap 4 (RegisterAccess trait unification) remain toadStool ownership
- coralReef's `FirmwareInventory` + `compute_viable()` feeds into toadStool's hwLearn

### hotSpring / wetSpring
- UVM dispatch path unblocks RTX 3090 hardware validation
- Same QMD + PushBuf format shared between nouveau and UVM paths
