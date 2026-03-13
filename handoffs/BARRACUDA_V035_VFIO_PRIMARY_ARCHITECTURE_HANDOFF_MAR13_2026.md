# barraCuda v0.3.5 — VFIO Primary Architecture Handoff

**Date**: March 13, 2026
**Type**: Architecture evolution handoff
**Scope**: VFIO-primary dispatch path adoption across documentation and code

---

## Summary

VFIO via toadStool is now the **primary** GPU dispatch path for barraCuda's
sovereign pipeline. This handoff documents the architecture documentation
evolution and code preparation for VFIO integration.

### Architectural Shift

**Before**:
```
barraCuda → wgpu → Vulkan → Mesa/NVK → nouveau → GPU
```

**After (VFIO primary)**:
```
barraCuda → CoralReefDevice → coral-gpu → GPFIFO → GPU (via VFIO/toadStool)
```

**After (wgpu fallback)**:
```
barraCuda → WgpuDevice → wgpu → Vulkan/Metal/DX12 → GPU
```

### Why VFIO

- Zero kernel driver in data path
- Hardware-enforced device exclusivity (IOMMU)
- Deterministic scheduling (user-space GPFIFO)
- IOMMU DMA remapping isolation
- Dual-use: VFIO for compute, passback for gaming
- Projected ~4,000 steps/s (VFIO + DF64) vs Kokkos 2,630 steps/s

---

## Changes Made

### Architecture Documentation (7 files)

1. **`SOVEREIGN_PIPELINE_TRACKER.md`**: Layer 4 upgraded from "Planned" to
   "Active design". Added VFIO Primary Dispatch Path section (strategy, security
   enclave stack, Kokkos parity projections, huge page DMA). Updated P0 to
   document dual-backend architecture. Added VFIO items to P1 (from_vfio_device,
   is_vfio_gpu_available, doc updates). Added "barraCuda needs from toadStool"
   cross-primal matrix section.

2. **`PURE_RUST_EVOLUTION.md`**: Layer 4 upgraded to "Active design" with VFIO
   description. Stack diagrams updated to show VFIO primary / wgpu fallback
   dual-path. Layer 4 section rewritten to document VFIO vs DRM comparison and
   component status (coral-driver BAR0 done, toadStool RegisterAccess done).

3. **`WHATS_NEXT.md`**: VFIO architecture adoption added to P1. Kokkos parity
   moved from P2 to P1 (unblocked by VFIO strategy). P4 updated to reference
   VFIO primary path.

4. **`specs/BARRACUDA_SPECIFICATION.md`**: Vendor-agnostic description updated
   to show dual dispatch paths. Shader compilation pipeline updated with
   CoralReefDevice/WgpuDevice branch. dispatch_binary documented as fast path.

5. **`specs/ARCHITECTURE_DEMARCATION.md`**: Added "VFIO GPU Dispatch" section
   to toadStool layer documenting VFIO lifecycle, IOMMU, huge pages,
   RegisterAccess, and VfioGpuInfo. Key property section updated to note
   toadStool's VFIO ownership.

6. **`STATUS.md`**: Added VFIO strategy, from_vfio_device, is_vfio_gpu_available,
   VfioGpuInfo, and Kokkos parity projections to "What's Working" section.

7. **`CONTRIBUTING.md`**: Added Architecture Note section explaining dual-path
   dispatch (VFIO primary, wgpu fallback) and development requirements.

### Code Evolution (3 files)

1. **`backend.rs`**: Module doc updated from "WgpuDevice implements it today;
   CoralReefDevice will implement it when..." to documenting CoralReefDevice as
   the primary VFIO backend and WgpuDevice as the fallback.

2. **`coral_reef_device.rs`**: Module doc rewritten with VFIO-primary architecture
   diagram, DRM fallback diagram, and backend maturity table (VFIO/GPFIFO active
   design, amdgpu E2E, nouveau partial). Added `from_vfio_device(pci_address,
   vendor_id, iommu_group)` constructor stub (feature-gated, returns Err pending
   coral-gpu VFIO backend). Documents contract: toadStool manages bind/unbind,
   barraCuda never touches VFIO lifecycle.

3. **`device_info.rs`**: Added `VfioGpuInfo` struct (pci_address, vendor_id,
   device_id, iommu_group). Added `is_vfio_gpu_available()` and
   `discover_vfio_gpus()` functions that scan `/sys/kernel/iommu_groups/` for
   GPUs bound to `vfio-pci` (NVIDIA 0x10de, AMD 0x1002, Intel 0x8086).
   Sovereign device info now reflects VFIO availability in its name.

---

## Quality Gate Results

| Gate | Result |
|------|--------|
| `cargo fmt --all -- --check` | Pass |
| `cargo clippy --workspace --all-targets -- -D warnings` | Pass (0 warnings) |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | Pass (0 warnings) |
| `cargo deny check` | Pass (advisories, bans, licenses, sources) |
| `cargo nextest run -p barracuda --lib` | 3,346 pass, 0 fail, 13 skip |
| `cargo nextest run -p barracuda-core` | 69 pass, 0 fail, 0 skip |

---

## What Is NOT In Scope

- Actual VFIO dispatch implementation (blocked on coral-gpu + toadStool VFIO GPU backend)
- BearDog encryption integration (BearDog team)
- `ecoprimals-mode` CLI tool (toadStool)
- Huge page DMA buffer allocation (toadStool)
- toadStool RegisterAccess trait wiring (toadStool + coralReef Gap 4)

---

## Cross-Primal Dependencies

### barraCuda needs from toadStool (new)
- `VfioGpuInfo` descriptor type for VFIO GPU device handoff
- VFIO device bind/unbind lifecycle management
- Huge page DMA buffer descriptors

### barraCuda needs from coralReef (unchanged)
- `coral-gpu` as `cargo add` dependency (still blocked)
- `coral-gpu` VFIO backend (new — enables `from_vfio_device`)

---

## Next Steps

1. **toadStool**: Implement VFIO GPU backend with `VfioGpuInfo` type
2. **coralReef**: Add VFIO dispatch path to `coral-gpu` crate
3. **barraCuda**: Wire `from_vfio_device` to `coral_gpu::GpuContext::from_vfio()` when available
4. **Kokkos parity**: Run RHMC lattice QCD benchmarks on VFIO hardware
