# barraCuda v0.3.5 — toadStool S152 + coralReef Iter 42 Rewire Handoff

**Date**: 2026-03-13
**From**: barraCuda
**Type**: Cross-primal rewire — absorb toadStool S152 and coralReef Iter 42 evolution

---

## Summary

Systematic rewire of barraCuda documentation and code comments to reflect the
significant evolution in toadStool (S147→S152) and coralReef (Iter 37→Iter 42)
since barraCuda's last cross-primal sync. All stale session pins, blocker
descriptions, and capability references updated.

## Key Cross-Primal State Changes Absorbed

### toadStool S152 (all 12 sovereign infra gaps resolved)

| Gap | Description | Status |
|-----|-------------|--------|
| 1 | Dispatch client (`compute.dispatch.*`) | Resolved |
| 3 | Error recovery | Resolved (S151) |
| 4 | DMA buffers | Resolved (S151) |
| 5 | Multi-arch classifier | Resolved (S152) |
| 6 | Unified PCI discovery | Resolved (S151) |
| 7 | Test coverage / mock layers | Resolved (S152) |
| 8 | OS keyring | Resolved (S152) |
| 9 | Cross-gate pooling | Resolved (S152) |
| 10 | Thermal safety | Resolved (S151) |
| 11 | VFIO bind/unbind | Resolved (S151) |
| 12 | Multi-GPU init | Resolved (S152) |

Only Gap 2 (VFIO hardware validation) remains — blocked on PFIFO channel init.

### coralReef Iter 42

- `GpuContext::from_vfio(bdf)` API available for barraCuda `from_vfio_device`
- `GpuContext::from_vfio_with_sm(bdf, sm)` for explicit SM override
- `NvVfioComputeDevice::sync()` via GP_GET polling
- DRM dispatch E2E proven on Titan V + RTX 3090
- 6/7 VFIO hardware tests pass; dispatch blocked on PFIFO channel init
- 1669+35 tests, 64% coverage

### hotSpring v0.6.31

- `sovereign_resolves_poisoning()` wired into MD entry points
- Gap 1 (dispatch_binary) confirmed closed via barraCuda `82ff983`
- Gap 4 (RegisterAccess bridge) confirmed closed via toadStool S147

## barraCuda Changes Made

### Code (`coral_reef_device.rs`)

- Backend maturity table updated: VFIO → "API available" (was "Active design"),
  nouveau → "E2E verified" (was "Partial"), nvidia-drm → "UVM partial"
- `from_vfio_device` stub: blocker text updated from "blocked on coral-gpu
  VFIO support and toadStool VfioGpuInfo type" to "coral-gpu not yet
  publishable as dependency; API exists (GpuContext::from_vfio)"
- Comments updated with coralReef Iter 42 and toadStool S152 references

### Documentation (6 files)

| File | Changes |
|------|---------|
| `SOVEREIGN_PIPELINE_TRACKER.md` | Layer 2/4 progress bars updated; cross-primal dependency matrix (toadStool items Planned→Done); P0/P1 status updates; NVIDIA status updated |
| `PURE_RUST_EVOLUTION.md` | Layer 2/4 progress bars; Layer 4 section rewritten for S152 completion |
| `STATUS.md` | "What's Not Working Yet" updated with current blockers; cross-primal pins table added (toadStool S152, coralReef Iter 42, hotSpring v0.6.31); RHMC marked done |
| `SPRING_ABSORPTION.md` | Source pin updated: toadStool S147→S152, hotSpring v0.6.27→v0.6.31, coralReef Iter 42 added |
| `specs/ARCHITECTURE_DEMARCATION.md` | VFIO section expanded with S150-S152 capabilities (DMA, MSI-X, thermal, multi-GPU, cross-gate, multi-arch) |

## Remaining Blockers (barraCuda perspective)

| Blocker | Owner | Notes |
|---------|-------|-------|
| `coral-gpu` not publishable as standalone crate | coralReef | API exists (Iter 42); publishing blocked |
| PFIFO channel init for VFIO dispatch | coralReef | 6/7 tests pass; dispatch needs channel create/enable |
| DF64 NVK E2E verification | barraCuda | Needs NVK + NAK hardware |
| Kokkos parity validation | barraCuda | Needs matching hardware; projected ~4,000 steps/s |

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy -D warnings` | Pass |
| `cargo doc -D warnings` | Pass |

## Files Modified

6 files, net +29 lines (67 added, 38 removed)
