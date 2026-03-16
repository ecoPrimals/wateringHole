# hotSpring — Interpreter Probe & Sovereign Bring-Up Gaps Handoff

**Source**: hotSpring VFIO interpreter probe on biomeGate (March 13–15, 2026)
**Target**: toadStool, coralReef, barraCuda
**Hardware**: 2× Titan V (GV100, SM70) + RTX 5060 on `vfio-pci`
**coralReef**: Phase 10, Iteration 47+, `coral-driver` crate with `--features vfio`
**Builds on**: `HOTSPRING_GLOWPLUG_SOVEREIGN_POWER_TRIO_HANDOFF_MAR14_2026.md`
**Chat**: [VFIO interpreter probe](28732f32-750e-4053-a1ae-a8d39a738d7a)
**Guide**: `GPU_SOVEREIGN_BRING_UP_GUIDE.md` (comprehensive findings)

---

## Executive Summary

The 7-layer interpreter probe now runs end-to-end on GV100 via VFIO. BAR2
self-warm glow plug achieved full nouveau parity (Experiment 060). Three
critical bugs were found in the scheduler activation path. The PBDMA loads
channel context (SIGNATURE = 0xFACE) but GP_GET doesn't advance — the GPU
is loaded but not fetching. Seven specific gaps remain between current state
and sovereign compute dispatch.

---

## Current State: What Works

| Capability | Status | Evidence |
|-----------|--------|----------|
| PCIe D3→D0 power-up | ✅ | PMCSR write, BAR0 reads valid |
| Engine clock warm-up | ✅ | PMC_ENABLE 0x40000020 → 0x5fecdff1 |
| BAR2 page table (self-warm) | ✅ | 12/54 matrix experiments schedule |
| V2 MMU 5-level page tables | ✅ | Identity-mapped 2MB in SPT |
| VRAM read/write via PRAMIN | ✅ | Verified at 0x0, 0x20000, 0x26000 |
| PBDMA topology discovery | ✅ | PBDMA_MAP=0x0020000E, PBDMAs 1,2,3,21 |
| GR runlist mapping | ✅ | GR→RL1→PBDMA3 (bitmask decode) |
| Instance block in VRAM | ✅ | INST_BIND loads, PCCSR_INST valid |
| Direct PBDMA context load | ✅ | SIG=0xFACE, GP_BASE=0x1000, USERD=0x2002 |

---

## Current State: What Doesn't Work

| Capability | Status | Evidence |
|-----------|--------|----------|
| Scheduler-driven channel load | ❌ | Sentinels unchanged in L4 A–E, L5 |
| GP_GET advancement | ❌ | Stays 0 despite GP_PUT=1 and context loaded |
| USERD writeback | ❌ | Host USERD GP_GET = 0xDEAD (sentinel) |
| GPFIFO consumption | ❌ | No entries consumed |
| NOP method execution | ❌ | L6 is a stub |

---

## Three Critical Bugs Found

### Bug 1: Runlist Register Address (coralReef)

**File**: `probe.rs` L4/L5 runlist submission
**Current code**:
```rust
self.w(pfifo::RUNLIST_BASE, vram_rl_addr >> 12);  // 0x2270 = RL0
self.w(pfifo::RUNLIST_SUBMIT, (gr_rl << 20) | 2); // wrong encoding
```

**Correct (GV100)**:
```rust
let rl_base = 0x2270 + gr_rl as usize * 0x10;
let rl_submit = rl_base + 4;
self.w(rl_base, lower_32(vram_addr >> 12));
self.w(rl_submit, upper_32(vram_addr >> 12) | (entry_count << 16));
```

**Source**: nouveau `gv100_runl_commit()` — per-runlist at stride 0x10.
The `registers.rs` constants are labeled "gk104" which uses a single global
register pair with rl_id encoded in the value. GV100 is architecturally
different.

### Bug 2: MMU Fault Buffer Setup (coralReef)

**File**: `probe.rs` L3 fault buffer configuration
**Current approach**: Write to VRAM addresses via PRAMIN
**Result**: `BUF1_LO` reads back 0x0 (write rejected), `BUF0_LO` reads back 0x2

**Correct approach**: Allocate system memory DMA buffer and configure:
```rust
let fault_buf = DmaBuffer::new(container_fd, 4096, FAULT_BUF_IOVA)?;
let addr = FAULT_BUF_IOVA;
w(FAULT_BUF0_LO, lower_32(addr >> 12));  // PPN format
w(FAULT_BUF0_HI, upper_32(addr >> 12));
w(FAULT_BUF0_SIZE, 64);                  // 64 entries
w(FAULT_BUF0_PUT, 0x8000_0000);          // enable bit 31
```

**Impact**: Without fault buffers, the scheduler cannot handle MMU faults
during context load. This may cause silent PBDMA stalls.

### Bug 3: PBDMA-to-Runlist Bitmask Decode (coralReef, FIXED)

**File**: `probe.rs` L3 engine discovery
**Was**: `rl_mask == rl_id` (direct comparison)
**Fixed to**: `rl_mask & (1 << rl_id) != 0` (bitmask check)
**Result**: Correctly identifies PBDMA3 as GR PBDMA for runlist 1

---

## Interpreter Diagnostic Evidence

### PFIFO INTR = 0x100 After Runlist Submit

Bit 8 of PFIFO_INTR fires after attempts D and E (which submit runlists).
This could be:
- `RUNLIST_EVENT` — scheduler processed (or rejected) the runlist
- `PBDMA_INTR` aggregate — a PBDMA signaled an error
- `SCHED_ERROR` — scheduler couldn't process the runlist

**Action**: Decode this interrupt and clear before retry.

### PBDMA_ST = 0x8202C022 (Constant)

The PBDMA status register never changes across any attempt, including
direct context programming. This decodes to:
- Bit 31: BUSY
- Other bits: need GV100 PBDMA_STATUS decode reference

This may indicate the PBDMA is stuck in a prior error state from
nouveau or from earlier test runs.

**Action**: Try full PBDMA reset (clear INTR, clear PBDMA_FAULTED in PCCSR,
toggle PMC PBDMA bit) before context load.

### PCCSR Channel Status = 1 (PENDING)

Channel status stays PENDING (not IDLE, not ON_PBDMA). This means the
scheduler acknowledged the channel enable but never dispatched it to a PBDMA.
Likely causes: no valid runlist, or runlist submitted to wrong RL register.

---

## Work Items

### P0 — coralReef (immediate)

1. **Fix runlist registers**: Use per-runlist at 0x2270+id×0x10 for GV100
2. **Fix runlist encoding**: `upper_32(addr >> 12) | (count << 16)`
3. **Fix fault buffers**: Use DMA buffer in system memory, proper register format
4. **Re-test interpreter**: With all three fixes, check if scheduler activates
5. **Decode PFIFO INTR bit 8**: Read and clear before retry

### P1 — coralReef (next)

6. **PBDMA reset sequence**: Full reset before context load
7. **Multi-PBDMA sweep**: Try all active PBDMAs, not just gr_pbdma
8. **L6 NOP dispatch**: Submit a real GPFIFO entry with NOP methods
9. **Warmth sentinel**: Detect and re-warm if GPU cools during test

### P1 — toadStool

10. **Absorb glow plug** into `nvpmu` as `GpuPowerController`
11. **Implement PowerManager** with five-state model
12. **Begin FB controller** reverse engineering for HBM2 init
13. **Build hardware profiles** from interpreter ProbeReports

### P2 — barraCuda

14. **Dispatch pre-warm hint** integration
15. **Architecture-aware ISA selection** from GpuIdentity

---

## Key Source Files

| File | What |
|------|------|
| `coralReef/.../diagnostic/interpreter/probe.rs` | 7-layer interpreter probe |
| `coralReef/.../diagnostic/interpreter/layers.rs` | Layer type definitions |
| `coralReef/.../diagnostic/runner.rs` | Diagnostic matrix runner |
| `coralReef/.../channel/pfifo.rs` | Glow plug + BAR2 setup |
| `coralReef/.../channel/registers.rs` | BAR0 register map |
| `coralReef/.../channel/page_tables.rs` | V2 MMU page table encoding |
| `wateringHole/GPU_SOVEREIGN_BRING_UP_GUIDE.md` | Comprehensive findings guide |
| `hotSpring/experiments/060_BAR2_SELF_WARM_GLOW_PLUG.md` | BAR2 self-warm results |

---

*March 15, 2026 — Context loaded. Three bugs found. Seven gaps to sovereign dispatch.*
