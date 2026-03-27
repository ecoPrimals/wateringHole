# toadStool S153 — Trio Rewire + VFIO Bridge Handoff

**Date**: March 13, 2026
**Session**: S153
**Pins**: hotSpring v0.6.31, coralReef Iteration 42, barraCuda v0.35

---

## Summary

Cross-primal rewire after reviewing barraCuda v0.35 (VFIO-primary architecture,
sovereign dispatch, 806 pure WGSL shaders), coralReef Iteration 42 (VFIO sync,
`from_vfio` API, BAR0 hardware validation), and hotSpring gap closure guidance.

Key deliverables: `compute.hardware.vfio_devices` JSON-RPC method that provides
the `VfioGpuInfo` bridge barraCuda needs to wire `CoralReefDevice::from_vfio_device`,
`ecoprimals-mode` CLI for science/gaming GPU mode switching, and doc reconciliation
across all three primals.

---

## Changes

### 1. VfioGpuInfo Discovery Bridge (`compute.hardware.vfio_devices`)

New JSON-RPC method that returns VFIO-bound GPU descriptors:

```json
{
  "devices": [{
    "pci_address": "0000:01:00.0",
    "vendor_id": 4318,
    "device_id": 7553,
    "iommu_group": 42,
    "driver": "vfio-pci",
    "power_state": "D0",
    "supports_reset": true,
    "vendor_name": "NVIDIA"
  }],
  "count": 1
}
```

This unblocks barraCuda's `CoralReefDevice::from_vfio_device(pci_address, vendor_id,
iommu_group)` — barraCuda can discover VFIO GPUs via toadStool IPC and pass the
descriptor to `coral_gpu::GpuContext::from_vfio(bdf)`.

**File**: `crates/server/src/pure_jsonrpc/handler/hw_learn.rs`

### 2. ecoprimals-mode CLI

New `toadstool mode` subcommand for single-GPU science/gaming switching:

- `toadstool mode science [--bdf BDF]` — bind GPU to `vfio-pci`
- `toadstool mode gaming [--bdf BDF]` — unbind from `vfio-pci`, restore display driver
- `toadstool mode status [--bdf BDF]` — show current mode, driver, power state

Auto-detects first NVIDIA GPU when `--bdf` is omitted. Persists original driver
for clean restore.

**File**: `crates/cli/src/commands/mode.rs`

### 3. Doc Reconciliation

- All root docs updated to pin coralReef Iteration 42, hotSpring v0.6.31
- SOVEREIGN_COMPUTE_GAPS.md updated with VfioGpuInfo bridge note
- JSON-RPC method count: 96+
- Verified all toadStool-owned gaps (1-12) correctly marked resolved

---

## Trio Interface Status

### toadStool → barraCuda

| Interface | Status |
|-----------|--------|
| `compute.hardware.vfio_devices` JSON-RPC | **NEW** — provides VfioGpuInfo descriptors |
| GPU discovery manifests (`$XDG_RUNTIME_DIR/ecoPrimals/`) | Working |
| `PrecisionRoutingAdvice` (from `GpuDriverProfile`) | Working (S128) |

### toadStool → coralReef

| Interface | Status |
|-----------|--------|
| `compute.dispatch.submit` (binary → coralReef dispatch) | Working (S152) |
| VFIO device lifecycle (bind/unbind/permissions) | Working (S151) |
| `RegisterAccess` trait alignment | Working — both use `u64` offsets |

### barraCuda → coralReef

| Interface | Status |
|-----------|--------|
| `CoralReefDevice::from_vfio_device` | **Stub** — blocked on `coral-gpu` crate publish |
| `GpuContext::from_vfio(bdf)` | **Ready** (coralReef Iter 42) |
| `dispatch_binary` / `dispatch_kernel` | Working via coral cache |
| Sovereign compiler (FMA fusion, dead expr, df64_rewrite) | Working |

### Remaining Cross-Primal Gap

The only gap blocking end-to-end VFIO dispatch:

1. **barraCuda `from_vfio_device`** returns `Err` — needs `coral-gpu` crate to be
   publishable (coralReef owns this)
2. **PFIFO channel init via BAR0** — coralReef's nop shader dispatch test hits
   `FenceTimeout` because GPU PFIFO channel is never created through VFIO path.
   toadStool's hw-learn can trace nouveau channel creation to distill the init sequence.
3. **VFIO hardware validation** (Gap 2) — all software is ready; needs physical test rig

---

## Gap Reconciliation

Handoffs from Mar 12 listed several gaps as open that toadStool has already resolved:

| Gap | Handoff Status | Actual Status |
|-----|---------------|---------------|
| Gap 4: RegisterAccess bridge | Listed as open | **Resolved S150** — `Bar0Access` implements `hw_learn::applicator::RegisterAccess` |
| Gap 5: Multi-arch classifier | "Only knows GV100" | **Resolved S152** — `GpuGen` enum with Volta/Turing/Ampere register tables |
| Gap 6: Unified PCI discovery | "NVIDIA only" | **Resolved S151** — `PciFilter` supports AMD (0x1002), Intel (0x8086), Brainchip (0x1e64) |
| Huge page DMA | Listed as TODO | **Resolved S152** — `allocate_huge()` with MAP_HUGETLB 2MB/1GB |
| ecoprimals-mode CLI | Listed as TODO | **Resolved S153** — `toadstool mode science/gaming/status` |

---

## Test Status

20,262+ tests passing, 0 failures. ~150K production lines. 96+ JSON-RPC methods.
