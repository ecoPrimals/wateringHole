# toadStool S175 — Unsafe Code Reduction Phase 1+2

**Date**: April 3, 2026
**Session**: S175 (unsafe reduction evolution, continuation of S174 audit)
**Status**: All quality gates green. 21,617 tests, 0 failures.
**Previous**: `TOADSTOOL_S172_4_DEEP_DEBT_EXECUTION_HANDOFF_APR02_2026.md`

---

## Summary

Executed Phase 1 (community crate adoption) and Phase 2 (GPU backend collapse) of the
unsafe code reduction roadmap. Consumer `unsafe {}` blocks reduced 80% (56→11). Total
unsafe: 59 actual (48 in containment zones, 11 in consumer/driver code). All unsafe is
now either in dedicated containment modules (`hw-safe`, `v4l2::ioctl`) or irreducible
hardware FFI in driver crates.

---

## Changes

### Phase 1: V4L2 Ioctl Containment

| Item | Before | After |
|------|--------|-------|
| `v4l2/device.rs` | 9 inline `unsafe { ioctl(...) }` blocks | **0** — pure safe Rust |
| `v4l2/ioctl.rs` | — | **NEW** — 8 safe wrapper functions (containment zone) |
| `v4l2/types.rs` | — | **NEW** — `#[repr(C)]` kernel ABI structs isolated |

### Phase 2: GPU Backend Collapse

| Item | Before | After |
|------|--------|-------|
| `VulkanBackend::with_device()` | `unsafe fn` | Safe `fn` (no unsafe in body) |
| `OpenClBackend::with_context()` | `unsafe fn` | Safe `fn` (no unsafe in body) |
| `VulkanAllocation` Send/Sync | 2 `unsafe impl` | Absorbed by `GpuPtr` |
| `OpenClAllocation` Send/Sync | 2 `unsafe impl` | Absorbed by `GpuPtr` |
| `WebGpuAllocation` Send/Sync | 2 `unsafe impl` | Absorbed by `GpuPtr` |
| `GpuPtr` | — | **NEW** — `#[repr(transparent)]` newtype, single `Send+Sync` |
| `vulkan.rs` `#![allow(unsafe_code)]` | Present | **Removed** |
| `opencl.rs` `#![allow(unsafe_code)]` | Present | **Removed** |

### Phase 2: HugePageMemory RAII

| Item | Before | After |
|------|--------|-------|
| `hw-safe/huge_page.rs` | — | **NEW** — RAII for mmap_anonymous+MAP_HUGETLB+mlock |
| `nvpmu/dma.rs` unsafe blocks | ~9 | 2 |
| `DmaBuffer` fields | `vaddr: *mut u8`, `locked: Option<LockedMemory>`, `huge_page: bool` | `mem: DmaMemory` enum |
| Manual munlock/munmap in Drop | Present | **Removed** — `HugePageMemory` handles cleanup |

### Clippy Fixes (incidental)

- `vfio_err` in akida-driver and nvpmu: pass-by-value → pass-by-ref
- `ioctl_err` in v4l2/device.rs: pass-by-value → pass-by-ref
- `nvpmu/dma.rs`: `if let Err` → `?` operator
- `v4l2/types.rs`: `pub _pad` → `_pad` (pub_underscore_fields)

## Unsafe Census (S175)

### Containment Zones (48 blocks)

| File | Blocks | Purpose |
|------|--------|---------|
| `hw-safe/vfio_setup.rs` | 9 | VFIO container/group ioctls |
| `hw-safe/vfio_dma.rs` | 6 | DMA map/unmap ioctls |
| `hw-safe/volatile_mmio.rs` | 6 | BAR0 volatile reads/writes |
| `hw-safe/huge_page.rs` | 6 | Huge page mmap/mlock/munmap |
| `hw-safe/device_mmap.rs` | 5 | Device file descriptor mmap |
| `hw-safe/aligned_alloc.rs` | 5 | Page-aligned heap allocation |
| `hw-safe/locked_memory.rs` | 2 | mlock/munlock RAII |
| `hw-safe/safe_mmap.rs` | 1 | memmap2-based safe mmap |
| `v4l2/ioctl.rs` | 8 | V4L2 ioctl wrappers |

### Consumer/Driver Code (11 blocks)

| File | Blocks | Purpose |
|------|--------|---------|
| `nvpmu/dma.rs` | 2 | DMA allocator IOVA management |
| `nvpmu/vfio.rs` | 1 | VFIO group fd handling |
| `akida-driver/vfio/dma.rs` | 2 | Akida DMA allocation |
| `nouveau_drm.rs` | 1 | DRM ioctl for Nouveau |
| `unified_memory/buffer/access.rs` | 2 | `from_raw_parts` for GPU buffers |
| `cuda_impl/kernels.rs` | 1 | CUDA kernel launch |
| `opencl_impl/backend.rs` | 1 | OpenCL buffer mapping |
| `isolated_memory.rs` | 1 | `madvise(MADV_DONTDUMP)` |

### Progression

| Session | Grep | Actual | Consumer | Containment |
|---------|------|--------|----------|-------------|
| S173 | 101 | ~95 | ~56 | ~39 |
| S174 | 79 | 77 | ~29 | ~48 |
| **S175** | **61** | **59** | **11** | **48** |

## Files Changed

### New Files
- `crates/core/hw-safe/src/huge_page.rs`
- `crates/runtime/display/src/v4l2/ioctl.rs`
- `crates/runtime/display/src/v4l2/types.rs`

### Modified Files
- `crates/core/hw-safe/src/lib.rs` — `pub mod huge_page` + re-export
- `crates/core/nvpmu/src/dma.rs` — HugePageMemory adoption, DmaMemory enum
- `crates/core/nvpmu/src/vfio.rs` — vfio_err pass-by-ref
- `crates/neuromorphic/akida-driver/src/backends/vfio/mod.rs` — vfio_err pass-by-ref
- `crates/runtime/display/src/v4l2/mod.rs` — new submodule wiring
- `crates/runtime/display/src/v4l2/device.rs` — all unsafe eliminated, imports from types/ioctl
- `crates/runtime/gpu/src/unified_memory/backend.rs` — GpuPtr newtype
- `crates/runtime/gpu/src/unified_memory/backends/vulkan.rs` — safe constructor, GpuPtr usage
- `crates/runtime/gpu/src/unified_memory/backends/opencl.rs` — safe constructor, GpuPtr usage

### Documentation
- `README.md` — unsafe counts updated, S175 entry, footer
- `NEXT_STEPS.md` — status line, coverage checkbox fix
- `DEBT.md` — S175 resolved debt section

## Verification

```
cargo check --workspace            # clean
cargo fmt --check                  # clean
cargo clippy --workspace           # 0 warnings
  --all-targets -- -D warnings
```

## Remaining Active Debt

| ID | Crate | Description |
|----|-------|-------------|
| D-TARPC-PHASE3 | integration/protocols | tarpc binary transport not wired |
| D-EMBEDDED-PROGRAMMER | runtime/specialty | Placeholder ISP/ICSP programmer impls |
| D-EMBEDDED-EMULATOR | runtime/specialty | Placeholder MOS6502/Z80 emulator impls |
| D-COV | workspace | Test coverage ~80-85%, target 90% |

## CoralReef Roadmap (Future)

Remaining 11 consumer unsafe blocks are the irreducible floor for direct hardware access.
The path to further reduction is `CoralReef`'s `coral-driver` absorbing vendor-specific GPU
FFI unsafe from toadStool (same pattern as bearDog absorbing `ring` crypto). When CoralReef
lands, toadStool becomes a pure orchestrator with near-zero consumer unsafe.

---

Part of [ecoPrimals](https://github.com/ecoPrimals) — sovereign compute for science and human dignity.
