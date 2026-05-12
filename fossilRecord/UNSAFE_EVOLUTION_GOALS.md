# Ecosystem Unsafe Evolution Goals

**Date**: April 5, 2026 — S186
**Scope**: toadStool (primary), ecosystem-wide evolution paths
**Status**: Pinned for incremental evolution

---

## Current State

After S185-186 unsafe audit and evolution, toadStool has **~36 unsafe blocks**
and **~15 unsafe impls** across the workspace. Every block has a `// SAFETY:`
comment. Every block is proven necessary for its current use case.

The remaining unsafe falls into categories with distinct evolution paths.

---

## Irreducible: Kernel / Hardware Trust Boundaries

These are **permanently required** — they're the boundary between Rust's type
system and the Linux kernel or hardware registers. No amount of Rust evolution
can eliminate them, but they can be further centralized.

| Category | Blocks | Location | Why |
|----------|:------:|----------|-----|
| ioctl dispatch (`do_ioctl`) | 6 | hw-safe, v4l2, hw-learn | `ioctl(2)` is inherently a kernel trust boundary |
| `unsafe impl Ioctl` | 6 impls | hw-safe, nvpmu, hw-learn | rustix trait contract for ioctl commands |
| mmap/munmap | 4 | hw-safe | OS memory mapping syscall |
| mlock/munlock | 4 | hw-safe | OS memory locking syscall |
| alloc_zeroed/dealloc | 3 | hw-safe | Aligned heap allocation (no safe stable API) |
| `OwnedFd::from_raw_fd` | 1 | hw-safe | Kernel returns raw fd integers |
| volatile read/write | 4+1fn | hw-safe | Hardware register access |
| `ExclusivePtr` Send+Sync | 2 impls | hw-safe | Raw pointer thread safety |
| `ContiguousBytes` defaults | 2 | hw-safe | from_raw_parts centralization |
| madvise(MADV_DONTDUMP) | 1 | secure_enclave | OS advisory syscall |

**Total irreducible**: ~26 blocks + ~8 impls

---

## Evolves with Ecosystem Primals

These unsafe blocks **will be eliminated** when coralReef and barracuda
replace the CUDA/OpenCL backends with pure-Rust wgpu compute:

| Category | Blocks | Impls | Drops when |
|----------|:------:|:-----:|------------|
| CUDA kernel launch (cudarc) | 1 | — | coralReef wgpu backend |
| OpenCL kernel enqueue (ocl) | 1 | — | coralReef wgpu backend |
| `GpuPtr` Send+Sync | — | 2 | barracuda safe buffer model |
| `UnifiedBuffer` Send+Sync | — | 2 | barracuda safe buffer model |
| GPU `from_raw_parts` | 2 | — | barracuda safe buffer model |

**Drops**: -4 blocks, -4 impls when coralReef + barracuda mature.

---

## Evolves with Rust Language

These could be eliminated by future Rust stabilizations:

| Category | Blocks | Rust feature | Status |
|----------|:------:|-------------|--------|
| aligned alloc/dealloc | 3 | `allocator_api` | Nightly since 2019; no stabilization date |
| volatile read/write | 4+1fn | `VolatileCell<T>` (RFC 3611) | Pre-RFC / discussion |

---

## Evolves with Crate Ecosystem

| Category | Blocks | Crate alternative | Notes |
|----------|:------:|-------------------|-------|
| `device_mmap` mmap/munmap | 2 | `memmap2::MmapRaw` | Verify MAP_SHARED + fd offset support |
| `aligned_alloc` alloc/dealloc | 3 | `aligned-vec` crate | Safe aligned allocation; evaluate dependency trade-off |

---

## Evolution Priorities

1. **coralReef wgpu backend** — highest impact: eliminates CUDA/OpenCL FFI unsafe
   AND the GPU pointer Send/Sync impls. Pure Rust compute dispatch.
2. **barracuda safe buffer model** — eliminates GPU `from_raw_parts` and
   remaining GPU thread-safety impls.
3. **memmap2 for DeviceMmap** — low risk, moderate impact: -2 blocks.
4. **Rust `allocator_api` stabilization** — watch nightly; would eliminate 3 blocks.
5. **Typed mlock/madvise wrappers** — accept `&impl ContiguousBytes` instead of
   raw pointers; moves safety proof to type invariant.

---

## Goal

**Zero application-layer unsafe.** All remaining unsafe lives exclusively in
`hw-safe` (the single containment zone) and in external FFI crates (cudarc, ocl)
that coralReef/barracuda will replace. The irreducible kernel trust boundaries
(~26 blocks) are inherent to sovereign hardware access and represent the
minimum cost of talking directly to silicon without vendor SDKs.

---

*Pinned by westgate — S186 unsafe evolution audit*
