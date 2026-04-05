# ToadStool S185-S186 — Unsafe Evolution Handoff

**Date**: April 5, 2026
**Sessions**: S185, S186, S186b
**Primal**: toadStool
**Commits**: `3a1c8714`, `6c03677d`, `ba2e74e8`

---

## Summary

Comprehensive unsafe audit and evolution across three commits. Reduced unsafe
surface from ~59 blocks to ~36 blocks and from ~20 impls to ~15 impls.
Created reusable safe abstractions that eliminate per-type unsafe patterns.

## S185: Audit + Remove Redundant + OwnedFd

- Full audit of all ~90 unsafe sites in production code, categorized by
  purpose (VFIO, V4L2, DRM, MMAP, FFI, RAW_PTR, SEND_SYNC, OTHER)
- Removed 4 redundant `unsafe impl Send/Sync` for `LockedMemory` (2) and
  `Bar0Access` (1 Send) — auto-derived from internal components
- Added compile-time `Send+Sync` trait assertions to 5 types
- Evolved akida-driver DMA from `RawFd` → `OwnedFd` (`try_clone().into()`)
- Deprecated `dma_map_fd`/`dma_unmap_fd` in hw-safe (RawFd variants)

## S186: Centralized Ioctl + MMIO Dispatch

- **`do_ioctl` helpers**: Single-site unsafe dispatch for all ioctl calls
  - VFIO setup: 8 blocks → 1 (`do_ioctl<I: Ioctl>`)
  - VFIO DMA: 2 blocks → 1
  - V4L2: 8 blocks → 3 (`v4l2_get`, `v4l2_update`, `v4l2_set`)
  - DRM: 1 block → 1 (`do_ioctl`)
- **Generic volatile MMIO**: `read_reg<T>` / `write_reg<T>` replaces
  per-width (u32/u64) methods. 4 blocks → 2.
- Net: -17 unsafe blocks

## S186b: ExclusivePtr + ContiguousBytes + nvpmu OwnedFd

- **`ExclusivePtr`**: Thread-safe `NonNull<u8>` newtype with `Send + Sync`.
  AlignedAlloc, HugePageMemory, DeviceMmap store `ExclusivePtr` and auto-derive
  thread safety. -6 `unsafe impl Send/Sync` eliminated.
- **`ContiguousBytes`**: Unsafe trait with safe default `as_bytes()`/`as_bytes_mut()`.
  Centralizes all `from_raw_parts` into 2 blocks (trait defaults). AlignedAlloc,
  HugePageMemory, DeviceMmap implement it. -6 unsafe blocks.
- **nvpmu OwnedFd**: Evolved `DmaAllocator`/`DmaBuffer` from `RawFd` → `OwnedFd`
  with `try_clone()` per buffer. Deprecated `dma_map_fd`/`dma_unmap_fd` calls
  eliminated. -2 unsafe blocks.

## Quality Gate

| Gate | Result |
|------|--------|
| `cargo check --workspace` | Clean |
| `cargo clippy --workspace --all-targets -- -D warnings` | 0 warnings |
| `cargo test --workspace` | **21,853 tests, 0 failures** |
| `cargo fmt --all -- --check` | 0 diffs |

## Files Changed

### S185
- `hw-safe/locked_memory.rs` — removed redundant Send/Sync
- `nvpmu/bar0.rs` — removed redundant Send
- `hw-safe/aligned_alloc.rs` — compile-time assertion
- `hw-safe/huge_page.rs` — compile-time assertion
- `hw-safe/device_mmap.rs` — compile-time assertion
- `akida-driver/backends/vfio/dma.rs` — OwnedFd evolution
- `akida-driver/backends/vfio/mod.rs` — OwnedFd plumbing
- `hw-safe/vfio_dma.rs` — deprecated RawFd variants

### S186
- `hw-safe/vfio_setup.rs` — do_ioctl helper
- `hw-safe/vfio_dma.rs` — do_ioctl helper
- `display/v4l2/ioctl.rs` — v4l2_get/update/set helpers
- `hw-learn/applicator/nouveau_drm.rs` — do_ioctl helper
- `hw-safe/volatile_mmio.rs` — read_reg<T>/write_reg<T>

### S186b
- `hw-safe/exclusive_ptr.rs` — NEW: ExclusivePtr newtype
- `hw-safe/contiguous.rs` — NEW: ContiguousBytes trait
- `hw-safe/lib.rs` — registered new modules
- `hw-safe/aligned_alloc.rs` — ExclusivePtr + ContiguousBytes
- `hw-safe/huge_page.rs` — ExclusivePtr + ContiguousBytes
- `hw-safe/device_mmap.rs` — ExclusivePtr + ContiguousBytes
- `nvpmu/dma.rs` — OwnedFd evolution

## Remaining Irreducible Unsafe

See `UNSAFE_EVOLUTION_GOALS.md` in this directory for the ecosystem-level
evolution roadmap for the remaining ~36 blocks + ~15 impls.

---

*Handoff by westgate — S185-186 unsafe evolution complete*
