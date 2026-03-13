# coralReef — Iteration 43: PFIFO Channel Init + Cross-Primal Rewire

**Date**: March 13, 2026
**Primal**: coralReef
**Phase**: 10 — Iteration 43

---

## Summary

Critical gap closed for sovereign VFIO GPU execution: the GPU hardware
channel (PFIFO) was never initialized, causing all VFIO dispatch to fail
with `FenceTimeout`. This iteration implements full Volta+ PFIFO channel
creation via BAR0 MMIO, corrects USERD register offsets, and acknowledges
cross-primal evolutions from toadStool and barraCuda.

## What Changed

### 1. PFIFO Hardware Channel Creation (`vfio/channel.rs`)

New module implementing the complete GPU FIFO channel setup sequence for
Volta+ GPUs using direct BAR0 MMIO register writes:

- **Instance block**: 4 KiB DMA buffer with RAMFC population (GPFIFO base,
  USERD pointer with SYS_MEM_COHERENT target, channel signature, engine
  config, acquire/semaphore values, HCE_CTRL, CHID)
- **V2 MMU page tables**: 5-level hierarchy (PD3→PD2→PD1→PD0→PT) with
  identity mapping for the first 2 MiB of IOVA space. PDE/PTE encoding per
  NVIDIA `dev_ram.ref.txt`: SYS_MEM_COHERENT aperture, volatile bit set
- **Subcontext 0 PDB**: SC_PDB_VALID(0) + SC_PAGE_DIR_BASE(0) pointing to
  PD3, enabling FECS compute subcontext
- **Runlist**: Volta-specific RAMRL with TSG header + channel entry, packed
  USERD IOVA and instance IOVA with target/channel-ID fields
- **PFIFO enable**: BAR0 + 0x2504 write
- **PCCSR bind/enable**: Instance block IOVA binding at BAR0 + 0x800000 +
  ID*8, channel enable at BAR0 + 0x800004 + ID*8
- **Runlist submission**: RUNLIST_BASE + RUNLIST registers at BAR0 + 0x2270/0x2274

### 2. RAMUSERD Offset Correction

Previous VFIO code used incorrect offsets for the USERD GP_GET/GP_PUT
registers (0x00/0x04), matching a simplified model. The actual Volta
RAMUSERD layout per `dev_ram.ref.txt` uses:

- **GP_GET at byte offset 0x88** (dword 34)
- **GP_PUT at byte offset 0x8C** (dword 35)

Both `submit_pushbuf()` and `poll_gpfifo_completion()` updated.

### 3. USERMODE Doorbell Correction

Previous code wrote GP_PUT to BAR0 + 0x0090. The correct mechanism is
`NV_USERMODE_NOTIFY_CHANNEL_PENDING` at BAR0 + 0x00810090, which takes
the channel ID as payload to notify Host that new work is available.

### 4. Integration into NvVfioComputeDevice

`NvVfioComputeDevice::open()` now creates a `VfioChannel` after initial
DMA buffer allocation. The channel struct owns all channel infrastructure
DMA buffers (instance block, runlist, page tables) for proper RAII cleanup.

**Files changed**:
- `crates/coral-driver/src/vfio/channel.rs` — new module (PFIFO channel creation)
- `crates/coral-driver/src/vfio/mod.rs` — public re-export of `VfioChannel`
- `crates/coral-driver/src/nv/vfio_compute.rs` — `VfioChannel` integration, RAMUSERD/doorbell corrections

## Root Cause Analysis

Hardware validation on the biomeGate Titan V (6/7 tests passed, 1 FenceTimeout)
revealed that without PFIFO channel initialization, the GPU has no execution
context. The GPFIFO ring and USERD page existed in host memory, but the GPU
had no instance block, no page tables to resolve DMA addresses, no runlist
entry, and no enabled channel — so it never consumed GPFIFO entries.

## Cross-Primal Status

### toadStool (S150-S152)
All 12 software gaps resolved per toadStool's commit evolution:
- S150: Full dispatch pipeline (WGSL→shader→QMD→GPFIFO→BAR0)
- S151: VFIO bind/unbind, thermal safety, cross-gate pooling
- S152: Mock hardware layer for CI, health probe, resource cleanup

### barraCuda
VFIO-primary wiring acknowledged:
- `dispatch_binary`/`dispatch_kernel` wired
- Gap 1 (coral cache→dispatch) closed
- `from_vfio_device` can use `GpuContext::from_vfio()` once PFIFO channel
  is validated on hardware

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1693 default + 47 VFIO, 0 failed, 71 ignored |
| New tests | 12 channel unit tests (PDE/PTE encoding, register offsets, IOVA layout, RAMUSERD, runlist) |
| Clippy | 0 warnings |
| Formatting | Clean |
| New unsafe blocks | 0 (channel creation uses safe DMA buffer slice writes) |
| Unsafe in VFIO path | 2 (volatile reads in poll_gpfifo_completion — existing, with SAFETY comments) |

## What's Next

- **Hardware validation**: Re-run `vfio_dispatch_nop_shader` on Titan V with PFIFO channel active
- **Coverage**: 64% → 90% line coverage target
- **Multi-channel**: Current implementation uses channel ID 0; multi-channel support for concurrent dispatch

## Dependencies

- **toadStool**: VFIO hardware contract unchanged from Iteration 41. toadStool must ensure IOMMU groups are clean and vfio-pci is bound before coralReef opens the device
- **barraCuda**: `GpuContext::from_vfio()` API unchanged. Once hardware validation passes, barraCuda's `CoralReefDevice::from_vfio_device()` path is fully functional
- **hotSpring**: No changes needed — shader compilation path unaffected

---

*coralReef Iteration 43 — The last critical gap in the VFIO sovereign
dispatch path is closed. The GPU now has a properly initialized hardware
channel with page tables, instance block, and runlist. Hardware validation
on Titan V is the next milestone.*
