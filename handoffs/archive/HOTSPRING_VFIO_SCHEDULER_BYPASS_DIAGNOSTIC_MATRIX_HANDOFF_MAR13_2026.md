# hotSpring — VFIO PFIFO Scheduler Bypass: Diagnostic Matrix Findings & Forward Plan

**Source**: hotSpring substrate-level VFIO debugging on biomeGate
**Date**: March 13, 2026
**Hardware**: Titan V (GV100, SM70) at `0000:4b:00.0`
**Kernel**: 6.17.9-76061709-generic
**coralReef**: Phase 10 Iteration 44, pulled `d3ac3ad` (USERD_TARGET fix)
**Prior handoffs**: `HOTSPRING_VFIO_PFIFO_PROGRESS_GP_PUT_HANDOFF_MAR09_2026.md`, `HOTSPRING_CUDA_ORACLE_EVOLUTIONARY_DEBUGGING_HANDOFF_MAR13_2026.md`
**Chat**: [VFIO diagnostic matrix](28732f32-750e-4053-a1ae-a8d39a738d7a)

---

## Executive Summary

A 48-configuration diagnostic experiment matrix and a nouveau BAR0 reference
capture have definitively shown that the VFIO PFIFO dispatch failure is **not
an encoding problem**. The GV100 hardware PFIFO scheduler is not processing
runlist submissions after nouveau unbind. No combination of target encoding
(COH/NCOH), operation ordering, or PCCSR configuration produces a scheduled
channel.

The forward path is to **bypass the hardware scheduler** and program PBDMAs
directly from Rust — a "sovereign scheduler" approach that is more aligned
with coralReef's hardware-atheistic architecture.

---

## What Was Built

### 1. Nouveau BAR0 Reference Capture

Bound the Titan V to nouveau, captured all PFIFO/PBDMA/PCCSR/MMU registers
via `scripts/read_bar0_deep.py`, saved to `scripts/nouveau_reference_bar0.txt`.
This is the first complete register snapshot of a healthy Volta PFIFO.

### 2. Diagnostic Experiment Matrix

Added to `coral-driver/src/vfio/channel.rs`:
- `ExperimentConfig`, `ExperimentResult`, `ExperimentOrdering` — structured experiment types
- `build_experiment_matrix()` — generates 48 configs across 4 axes
- `diagnostic_matrix()` — runs all configs in a single GPU session (~7 seconds total)
- `populate_*_static()` — parameterized buffer population for per-experiment reconfiguration

Added to `coral-driver/src/nv/vfio_compute.rs`:
- `RawVfioDevice` — opens VFIO device with BAR0 + DMA without creating a channel

Added to `tests/hw_nv_vfio.rs`:
- `vfio_pfifo_diagnostic_matrix` — integration test that runs the full matrix

### 3. Enhanced BAR0 Probe Script

Updated `scripts/read_bar0_deep.py` with:
- MMU replayable fault buffer registers (`0x100E24`–`0x100E34`)
- MMU non-replayable fault buffer registers (`0x100E44`–`0x100E54`)
- PFIFO_ENABLE (`0x2200`), PFIFO_FB_TIMEOUT (`0x2254`)
- PBDMA2/PBDMA3 full operational register sets
- PFIFO scheduler state registers (`0x2508`, `0x2510`)

---

## Findings

### Critical Finding 1: The Scheduler Is Not Processing Runlist Submissions

All 48 experiments produced identical PBDMA state — `USERD: 40208002_00000008`
(nouveau residual) — regardless of configuration. The scheduler is not loading
our channel context into any PBDMA. The runlist writes to `0x2270`/`0x2274` are
silently ignored.

```
Orderings A/B/C (no INST_BIND):  PCCSR=0x00000001, no faults, NEVER scheduled
Ordering D (with INST_BIND):     PCCSR=0x11000001, ALWAYS faults
Target encoding variations:      ZERO effect across all combinations
```

### Critical Finding 2: PFIFO_ENABLE = 0 Is Normal on GV100

| Register | Nouveau (healthy) | Our VFIO path | Implication |
|---|---|---|---|
| PFIFO_ENABLE (0x2200) | 0x00000000 | We toggled 0→1 | **0 is normal on GV100** |
| PCCSR_INST[0] | 0x802ffe48 (BIND=1, VRAM) | No BIND | Scheduler needs BIND=1 |
| PCCSR_CHAN[0] | 0x00000003 (enabled+scheduled) | 0x00000001 (enabled only) | Never scheduled |
| SCHED_DISABLE (0x2630) | 0x00000000 | 0x00000000 | Scheduler claims enabled |
| SCHED_EN (0x2504) | 0xbad00200 | 0xbad00200 | **Register does not exist on Volta** |

### Critical Finding 3: Encoding Is Irrelevant

The matrix tested 3 axes of encoding variation:
- PCCSR_INST target: COH(2) vs NCOH(3) — no difference
- Runlist entry targets: 3 combinations of USERD/INST COH/NCOH — no difference
- Runlist base target (0x2270): COH(2) vs NCOH(3) — no difference

All produce the same `PCCSR=0x00000001` with frozen PBDMA state. The encoding
fixes from iterations 43–44 are correct but irrelevant to the scheduling failure.

### Critical Finding 4: INST_BIND Always Faults for System Memory

When INST_BIND (bit 31) is set in PCCSR_INST, the GPU attempts an immediate
context load. With system memory targets (COH or NCOH), this always produces
`PBDMA_FAULTED + ENG_FAULTED` (PCCSR = 0x11000001). This happens regardless of
target encoding. Nouveau's INST_BIND works because its instance block is in VRAM.

### Critical Finding 5: Nouveau's Unbind Kills Scheduler State

After nouveau unbind → vfio-pci bind:
- `SCHED_DISABLE = 0` (scheduler claims enabled)
- `PFIFO_ENABLE = 0` (same as under nouveau — normal)
- No PFIFO interrupts, no errors, no faults
- But runlist submissions are silently ignored

The PFIFO scheduler hardware appears to have internal state (channel tables,
runlist pointers) that nouveau's unbind clears and that cannot be reconstructed
from userspace via MMIO alone.

### MMU Fault Buffer State

```
Replayable  (buf0): LO=0x00012000  HI=0x00000000  SIZE=0x00000000
Non-replayable (buf1): LO=0x00000000  HI=0x40001800  SIZE=0x00000000
```

Both buffers have SIZE=0 even under nouveau. The fault buffer setup appears
minimal or unused for basic channel operation.

---

## Architecture: Why the Scheduler Is the Wrong Battle

### Volta PFIFO Architecture

```
                     ┌──────────────────────────────────┐
                     │         PFIFO Hardware            │
                     │                                   │
  Runlist ──────────►│  ┌─────────┐    ┌──────────────┐ │
  (0x2270/0x2274)    │  │Scheduler│───►│ PBDMA 1      │ │──► GPU Engine (GR)
                     │  │ (HW)    │    │ context load  │ │
                     │  └─────────┘    │ GPFIFO fetch  │ │
                     │       │         │ cmd decode    │ │
                     │  Internal       └──────────────┘ │
                     │  state tables                    │
                     │  (opaque)                         │
                     └──────────────────────────────────┘
```

The scheduler's internal state tables are not documented in open-gpu-doc.
Nouveau initializes them via `gk104_fifo_init()` + `gv100_fifo_init()` as a
kernel driver with full hardware access. After unbind, these tables are stale.

### Proposed: Direct PBDMA Programming (Sovereign Scheduler)

```
                     ┌──────────────────────────────────┐
                     │         PFIFO Hardware            │
                     │                                   │
  (bypass)           │  ┌─────────┐                     │
                     │  │Scheduler│ (idle, ignored)     │
                     │  └─────────┘                     │
                     │                                   │
  Rust code ────────►│  ┌──────────────┐                │
  (BAR0 MMIO)        │  │ PBDMA 1      │                │──► GPU Engine (GR)
                     │  │ GP_BASE      │                │
                     │  │ USERD        │                │
                     │  │ GP_PUT       │                │
                     │  └──────────────┘                │
                     └──────────────────────────────────┘
```

Instead of: Runlist → Scheduler → PBDMA (broken)
We do:      Rust → PBDMA registers directly (no scheduler needed)

PBDMA registers are read/write at known offsets:
- `GP_BASE_LO/HI` (+0x040/044): GPFIFO ring base address
- `GP_PUT` (+0x054): next GPFIFO entry for PBDMA to process
- `GP_FETCH` (+0x048): PBDMA's current fetch pointer
- `USERD_LO/HI` (+0x0D0/0D4): USERD page address
- `SET_CHANNEL_INFO` (+0x0AC): channel configuration
- `CHANNEL_STATE` (+0x0B0): channel state
- `SIGNATURE` (+0x0C0): channel signature (0xFACE)
- `TARGET` (+0x0A8): memory aperture target

For single-channel compute dispatch, this is simpler and more sovereign
than fighting the hardware scheduler.

---

## Forward Plan

### Phase 1: Direct PBDMA Experiment (Next Session)

Add experiment ordering "E" to the diagnostic matrix:
1. Skip runlist submission entirely
2. Write PBDMA registers directly:
   - `GP_BASE_LO/HI` = GPFIFO IOVA
   - `USERD_LO/HI` = USERD IOVA with SYS_MEM_COH target
   - `SET_CHANNEL_INFO` = channel ID
   - `SIGNATURE` = 0xFACE
   - `GP_PUT` = 0 (or match USERD GP_PUT)
3. Write GPFIFO entry + USERD GP_PUT = 1
4. Check if PBDMA's GP_FETCH advances (meaning it's processing)

**Key register to watch**: `GP_FETCH` (+0x048). If it advances beyond 0 after
we write GP_PUT, the PBDMA is alive and processing. If it stays at 0, we need
to investigate PBDMA enable/reset registers.

### Phase 2: Dual Titan V Reference Rig (Hardware Upgrade)

When the second Titan V arrives:
- **Card A**: nouveau (reference oracle) — always has a healthy PFIFO
- **Card B**: vfio-pci (sovereign dispatch) — testing target

Benefits:
- Live register comparison without rebind cycles
- mmiotrace nouveau's dispatch sequence on Card A while testing on Card B
- Read PBDMA state during active dispatch to see exactly what registers
  the scheduler populates
- Capture the PBDMA register values for a working compute dispatch and
  replicate them directly on Card B

### Phase 3: Replication Harness (Multi-GPU, Multi-Architecture)

The diagnostic matrix infrastructure generalizes:
- `ExperimentConfig` is architecture-independent
- `diagnostic_matrix()` pattern works for any GPU with BAR0 MMIO access
- `RawVfioDevice` provides the low-level access without driver coupling

When MI50s arrive, the same framework applies:
- Discover AMD's SDMA/GFX engine registers via BAR0
- Build an experiment matrix for AMD's command processor
- Use ROCm-bound MI50 as reference, VFIO-bound MI50 as test target
- The "sovereign scheduler" pattern (direct engine programming) applies
  to AMD too — their SDMA engines are similarly register-programmable

### Phase 4: Sovereign Scheduler Library

If direct PBDMA programming works, extract it into a reusable component:

```rust
pub trait SovereignScheduler {
    fn bind_channel(&self, bar0: &MappedBar, pbdma_id: usize, ctx: &ChannelContext);
    fn submit(&self, bar0: &MappedBar, pbdma_id: usize, gpfifo_entry: u64);
    fn poll_completion(&self, userd: &[u8]) -> bool;
}

struct VoltaDirectPbdma;   // Direct register writes
struct AmdDirectSdma;      // AMD equivalent
```

This replaces the hardware scheduler with a Rust trait — testable,
debuggable, portable.

---

## Test Infrastructure Summary

### Running the Diagnostic Matrix

```bash
# 1. Warm GPU with nouveau
pkexec bash -c '
GPU=0000:4b:00.0; AUD=0000:4b:00.1
echo "" > /sys/bus/pci/devices/$GPU/reset_method
echo $GPU > /sys/bus/pci/drivers/vfio-pci/unbind
echo $AUD > /sys/bus/pci/drivers/vfio-pci/unbind
echo "" > /sys/bus/pci/devices/$GPU/driver_override
echo $GPU > /sys/bus/pci/drivers/nouveau/bind; sleep 3
echo $GPU > /sys/bus/pci/drivers/nouveau/unbind; sleep 1
echo vfio-pci > /sys/bus/pci/devices/$GPU/driver_override
echo vfio-pci > /sys/bus/pci/devices/$AUD/driver_override
echo $GPU > /sys/bus/pci/drivers/vfio-pci/bind
echo $AUD > /sys/bus/pci/drivers/vfio-pci/bind
chmod 666 /dev/vfio/36'

# 2. Run matrix
CORALREEF_VFIO_BDF=0000:4b:00.0 CORALREEF_VFIO_SM=70 \
cargo test --test hw_nv_vfio --features vfio \
  -- --ignored --test-threads=1 --nocapture vfio_pfifo_diagnostic_matrix
```

### Running the Nouveau Reference Capture

```bash
# Bind to nouveau, capture registers, rebind to vfio-pci
pkexec bash -c '
GPU=0000:4b:00.0
echo "" > /sys/bus/pci/devices/$GPU/reset_method
echo $GPU > /sys/bus/pci/drivers/vfio-pci/unbind
echo "" > /sys/bus/pci/devices/$GPU/driver_override
echo $GPU > /sys/bus/pci/drivers/nouveau/bind; sleep 3'

sudo python3 scripts/read_bar0_deep.py 0000:4b:00.0
```

### Adding New Experiments

```rust
// In channel.rs — add a new ordering variant:
pub enum ExperimentOrdering {
    // ... existing ...
    DirectPbdmaProgramming,  // NEW: bypass scheduler
}

// In the matrix match block, add the new case:
ExperimentOrdering::DirectPbdmaProgramming => {
    let pb = 0x040000 + target_pbdma * 0x2000;
    let _ = w(pb + 0x040, gpfifo_iova as u32);  // GP_BASE_LO
    let _ = w(pb + 0x044, (gpfifo_iova >> 32) as u32);  // GP_BASE_HI
    let _ = w(pb + 0x0D0, userd_iova as u32 | 1);  // USERD_LO + COH target
    let _ = w(pb + 0x0D4, (userd_iova >> 32) as u32);  // USERD_HI
    let _ = w(pb + 0x0AC, channel_id);  // SET_CHANNEL_INFO
    let _ = w(pb + 0x0C0, 0xFACE);  // SIGNATURE
    // Do NOT write GP_PUT yet — that's the dispatch trigger
}
```

---

## Files Modified

| File | Change |
|---|---|
| `coral-driver/src/vfio/channel.rs` | Diagnostic matrix types + functions |
| `coral-driver/src/nv/vfio_compute.rs` | `RawVfioDevice` for raw BAR0 access |
| `coral-driver/src/nv/mod.rs` | Re-export `RawVfioDevice` |
| `coral-driver/tests/hw_nv_vfio.rs` | `vfio_pfifo_diagnostic_matrix` test |
| `hotSpring/scripts/read_bar0_deep.py` | MMU fault buffers, PBDMA2/3, scheduler regs |
| `hotSpring/scripts/nouveau_reference_bar0.txt` | Reference capture from nouveau |

---

## Key Register Reference (GV100 PFIFO)

| Register | Offset | Nouveau Value | Our Value | Notes |
|---|---|---|---|---|
| PFIFO_ENABLE | 0x2200 | 0x00000000 | 0x00000000 | **0 is normal on GV100** |
| SCHED_EN | 0x2504 | 0xbad00200 | 0xbad00200 | Does not exist on Volta |
| SCHED_DISABLE | 0x2630 | 0x00000000 | 0x00000000 | 0 = scheduler enabled |
| PBDMA_MAP | 0x2004 | 0x0020000e | 0x0020000e | PBDMAs 1,2,3,21 |
| PMC_ENABLE | 0x0200 | 0x5fecdff1 | 0x5fecdff1 | Some engines gated |
| PCCSR_INST[0] | 0x800000 | 0x802ffe48 | 0x30000003 | BIND=1 vs BIND=0 |
| PCCSR_CHAN[0] | 0x800004 | 0x00000003 | 0x00000001 | Scheduled vs not |
| ENGN0_STATUS | 0x2640 | 0x10021002 | 0x10021002 | GR engine alive |

---

*From hotSpring diagnostic matrix session, March 13, 2026.*
*"The scheduler is the wrong battle. Program the PBDMA directly."*
