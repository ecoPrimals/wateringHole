# hotSpring → Ecosystem Handoff: Exp 104 PDE Slot Fix + ACR Firmware Alive

**Date:** 2026-03-25
**From:** hotSpring (biomeGate)
**To:** coralReef team, toadStool team, primal ecosystem
**Experiments:** 099–104
**Status:** ACR firmware alive and running on GV100 — HS authentication is the final gate

---

## What Happened

Six experiments (099–104) systematically eliminated every DMA hypothesis blocking
the ACR secure boot chain on GV100 (Titan V). The root cause was found in Exp 104:
a **page table construction bug** in `strategy_sysmem.rs`.

### Root Cause: PDE Slot Position

GV100 MMU v2 uses **16-byte PDE entries** at all directory levels (PD3/PD2/PD1/PD0).
The directory pointer must be written to the **upper 8 bytes** (offset 8..16),
with the lower 8 bytes zeroed. Our code was writing to the **lower 8 bytes**
(offset 0..8) — the wrong slot.

The reference implementation in `instance_block.rs` (`build_vram_falcon_inst_block`)
was correct. The bug was in `strategy_sysmem.rs` only, in both the sysmem DMA buffers
and their VRAM mirrors.

### Impact of Fix

| Metric | Before Fix (Exp 100-103) | After Fix (Exp 104) |
|--------|-------------------------|---------------------|
| HS mode | Achieved (SCTL=0x3002) | Not achieved (SCTL=0x3000) |
| Trace PCs | 2 (crash at 0x0500) | **31** (full BL + ACR init) |
| DMEM readable | No (0xDEAD5EC2) | **Yes** — ACR descriptor intact |
| EMEM queues | Empty | **Initialized** — CMDQ/MSGQ configured |
| CPU state | Halted | **Running** (idle loop) |
| MAILBOX0 | Never written | Written during init |

### Why Old (Wrong) PDEs Achieved HS Mode

With the PDE pointer in the wrong slot, the GV100 MMU walker found an entry that
the authentication hardware interpreted as "valid" in some edge-case way. HS mode
was granted because authentication checks IMEM code signatures (not page tables).
But ALL virtual DMA after the HS transition failed because the walker couldn't
traverse the page table chain properly — causing the invariant crash at TRACEPC=0x0500.

With correct PDEs, virtual DMA works perfectly but HS authentication hasn't been
triggered yet. The firmware runs in LS mode through its entire initialization
sequence.

## Experiment Summary

| Exp | Hypothesis Tested | Outcome |
|-----|------------------|---------|
| 099 | Inherit nouveau firmware (skip ACR) | **Dead** — FLR wipes all falcon memory |
| 100 | IOMMU faults cause DMA trap | **Eliminated** — full IOVA coverage, trap persists |
| 101 | Page table location (VRAM vs sysmem) | VRAM PTs enable execution but prevent HS |
| 102 | DMEM loading, FBIF, ctx_dma, binding target | Trap **invariant** to all five configs |
| 103 | GPU memory controller, FLR state, IRQ | Same crash with/without FLR. Halt intentional. |
| 104 | PDE slot position | **ROOT CAUSE FOUND** |

## Remaining Gate: HS Authentication

The firmware runs fully in LS mode. Two active investigation paths:

1. **WPR2 indexed register (0x100CD4)** — firmware may validate WPR boundaries
   via this indexed register, which doesn't reflect our direct writes to
   0x100CEC/CF0. The write protocol for 0x100CD4 is different from direct writes.

2. **NS→HS transition trigger** — the BL code may need specific conditions to
   invoke the secure transition (WPR hardware validation, PMU presence, or
   BIOS-configured registers that we haven't set).

## Impact on Sovereign Pipeline

| Layer | Status | Notes |
|-------|--------|-------|
| 0-8 | ✅ Solved | PCIe through WPR/ACR payload |
| 9.5 | ✅ **NEW** | Page table format + ACR DMA working (Exp 104) |
| 10 | 🔶 Close | HS authentication pending |
| 11 | 🔓 Unblocked when L10 done | `fecs_method.rs` ready for GR context |

**10.5 of 11 sovereign pipeline layers solved.**

## coralReef Code Changes

All changes in `coral-driver/src/nv/vfio_compute/acr_boot/`:

- `strategy_sysmem.rs` — PDE slot fix (4 directory levels), IOMMU catch-all buffers,
  VRAM mirroring, DMEM/IMEM/FBHUB diagnostics, WPR2 indexed register probe
- `sysmem_iova.rs` — LOW_CATCH/HIGH_CATCH address constants
- `wpr.rs` — firmware code dump at crash PC and HS entry point
- `sec2_hal.rs` — IMEM read addressing fix (block → byte for Falcon v5)

New test files:
- `tests/hw_nv_vfio/exp100_dma_fix.rs`
- `tests/hw_nv_vfio/exp103_no_flr.rs`

## Lessons for the Ecosystem

1. **GV100 MMU v2 PDE format** is documented nowhere publicly. The 16-byte dual
   entry format with pointer in upper bytes was reverse-engineered from
   `instance_block.rs` and cross-referenced with nouveau `gv100_vmm_pgt_pfn`.

2. **IOMMU coverage matters** — even with correct page tables, unmapped IOVA
   ranges cause IO_PAGE_FAULT. The catch-all buffer pattern (LOW_CATCH +
   HIGH_CATCH + mid-gap fills) should be standard for any VFIO DMA setup.

3. **HS read protection** — `0xDEAD5EC2` on DMEM BAR0 reads in HS mode is a
   sentinel from the read protection hardware, not a DMEM wipe. The data is
   still there; it's just invisible to the host.

4. **FBIF/DMA configuration is invariant across HS transition** — the HS
   transition does NOT modify FBIF_TRANSCFG, ITFEN, DMACTL, or DMAIDX.
   These registers can be set once before STARTCPU and they persist.

## Next Steps

- Resolve HS authentication (Path T: WPR2 register protocol, Path U: NS→HS trigger)
- Once HS: ACR blob DMA → FECS/GPCCS bootstrap → Layer 11 shader dispatch
- Strandgate team continues DRM dispatch validation (RTX 3090/5060, RX 6950 XT)
