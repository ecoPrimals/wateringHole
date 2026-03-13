# toadStool S151 — Sovereign Debt Closure Handoff

**Date**: March 12, 2026
**Session**: S151
**Pins**: hotSpring v0.6.31, coralReef Iter 41, barraCuda v0.35

---

## Summary

Closed 5 sovereign compute gaps (3, 4, 6, 10, 11) and executed deep unsafe
evolution across the workspace. Error recovery, DMA buffers, unified PCI
discovery, thermal safety, and VFIO bind/unbind automation all resolved.

---

## Changes

### 1. Error Recovery / Rollback (Gap 3)

`RegisterSnapshot` captures full BAR0 state before init. `apply_with_recovery()`
rolls back on failure. `NvPmuError::PartialInit` reports rollback status and
which registers were affected.

**File**: `crates/core/nvpmu/src/init.rs`

### 2. DMA Buffer Support (Gap 4)

`DmaAllocator` + `DmaBuffer` ported from akida-driver. Page-aligned allocation,
`mlock` for non-swappable memory, IOMMU mapping with automatic cleanup on drop.

**File**: `crates/core/nvpmu/src/dma.rs`

### 3. Unified PCI Discovery (Gap 6)

`pci_discovery::discover_pci_devices()` with `PciFilter` for vendor, class, and
device IDs. Vendor constants for NVIDIA (0x10de), Brainchip (0x1e64), AMD (0x1002),
Intel (0x8086). Shared scanner works for GPU, NPU, and any PCI accelerator.

**File**: `crates/core/common/src/pci_discovery.rs`

### 4. Thermal Safety Enforcement (Gap 10)

`check_thermal_for_bdf()` gates `apply` and `auto_init`. `gpu.telemetry` JSON-RPC
method returns per-GPU temperature, power, and safety status. `auto_init` captures
`RegisterSnapshot` and rolls back if thermal limits are exceeded during init.

**Files**: `crates/core/nvpmu/src/hwmon.rs`, `crates/server/src/pure_jsonrpc/handler/hw_learn.rs`

### 5. VFIO Bind/Unbind Automation (Gap 11)

`bind_vfio()` / `unbind_vfio()` with safety checks for DRM consumers and IOMMU
group integrity. `current_binding()` queries driver state. `BindResult` tracks
previous→current driver transitions.

**File**: `crates/core/nvpmu/src/vfio_bind.rs`

### 6. V4L2 Unsafe Evolution

6 `MaybeUninit::zeroed().assume_init()` patterns replaced with `Default::default()`.
All remaining unsafe blocks documented with `// SAFETY:` comments.

**File**: `crates/runtime/display/src/v4l2/device.rs`

### 7. init.rs → RegisterAccess Evolution

All init functions now accept `dyn RegisterAccess` (works with both `Bar0Access`
and `VfioBar0Access`). No more concrete type coupling.

**File**: `crates/core/nvpmu/src/init.rs`

---

## Impact on Other Primals

| Primal | Impact |
|--------|--------|
| coralReef | `DmaBuffer` available for VFIO channel DMA; thermal gating protects shared GPU |
| barraCuda | No direct impact — math dispatch unchanged |
| hotSpring | Thermal enforcement means GPU init won't proceed if hwmon reports unsafe temps |

---

## Gaps Remaining After S151

- Gap 1: Dispatch client (no `compute.dispatch.*` yet)
- Gap 2: VFIO hardware validation (needs physical rig)
- Gap 5: Multi-arch register classification
- Gap 7: Test coverage → 90%
- Gap 8: OS keyring integration
- Gap 9: Cross-toadStool GPU pooling
- Gap 12: Multi-GPU init orchestration

---

## Test Status

20,015 tests passing, 0 failures.
