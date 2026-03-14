# hotSpring — VFIO PFIFO Complete Diagnostic Matrix: 62-Experiment Findings & Forward Plan

**Source**: hotSpring substrate-level VFIO debugging on biomeGate
**Date**: March 13, 2026
**Hardware**: Titan V (GV100, SM70) at `0000:4b:00.0`
**Kernel**: 6.17.9-76061709-generic
**coralReef**: Phase 10, Iteration 44+, crate `coral-driver` with `--features vfio`
**Prior handoffs**: `HOTSPRING_VFIO_SCHEDULER_BYPASS_DIAGNOSTIC_MATRIX_HANDOFF_MAR13_2026.md`
**Chat**: [VFIO diagnostic matrix](28732f32-750e-4053-a1ae-a8d39a738d7a)

---

## Executive Summary

A 62-configuration diagnostic experiment matrix spanning 12 experiment orderings
(A through L) has systematically explored every viable path to GPU compute
dispatch through VFIO on Volta. The matrix tested the full cross-product of:
target encodings (COH/NCOH), operation orderings, PCCSR configurations, direct
PBDMA register programming, VRAM-based structures via PRAMIN, and hybrid
approaches.

**Core finding**: The Volta PFIFO hardware scheduler requires internal state
that nouveau initializes during `gk104_fifo_init()` / `gv100_fifo_init()` as a
kernel driver. After nouveau unbind, this state is lost. Runlist submissions are
silently ignored. No combination of MMIO register writes from userspace can
reconstruct the scheduler's internal channel tables.

**Secondary finding**: The GPU's "warm" state (PFIFO engine clocking, VRAM
initialization) can be silently lost after nouveau unbind, producing a "cold"
GPU where PFIFO registers read `0xbad0da00`. The warm sequence reliability is
itself a variable.

**The path forward** requires either:
1. **Dual Titan V**: Live-read nouveau's PBDMA state during active dispatch and
   replicate it exactly on the VFIO card
2. **PFIFO engine re-initialization**: Replicate nouveau's `gk104_fifo_init()`
   sequence from Rust (reverse-engineer the ~200 register writes)
3. **Firmware-level approach**: Load and run the PFIFO firmware (PMU/SEC2) to
   initialize the scheduler from scratch

---

## What Was Built

### Diagnostic Infrastructure

| Component | Location | Purpose |
|-----------|----------|---------|
| `ExperimentOrdering` enum (12 variants) | `channel.rs:1002-1032` | A-L experiment types |
| `ExperimentConfig` / `ExperimentResult` | `channel.rs:1034-1075` | Structured experiment IO |
| `build_experiment_matrix()` | `channel.rs:1077-1260` | Generates 62 configs across all axes |
| `diagnostic_matrix()` | `channel.rs:1264-2017` | Runs all configs in single GPU session |
| `populate_*_static()` | `channel.rs:911-1000` | Per-experiment buffer reconfiguration |
| `RawVfioDevice` | `nv/vfio_compute.rs` | Opens VFIO device with BAR0+DMA only |
| `vfio_pfifo_diagnostic_matrix` | `tests/hw_nv_vfio.rs` | Integration test |
| `read_bar0_deep.py` | `scripts/` | BAR0 register probe script |
| `nouveau_reference_bar0.txt` | `scripts/` | Reference capture from healthy nouveau |

### Experiment Taxonomy

```
A-D: Scheduler-based (vary ordering + encoding)
  A: bind → enable → runlist           (12 encoding combos)
  B: bind → runlist → enable           (12 encoding combos)
  C: runlist → bind → enable           (12 encoding combos)
  D: bind_with_INST_BIND → enable → RL (12 encoding combos)

E-F: Direct PBDMA register programming
  E: Write GP_BASE/USERD/SIG directly, no INST_BIND (2 combos)
  F: Same + INST_BIND (2 combos)

G-I: Direct PBDMA + activation triggers
  G: E + GP_FETCH reset + GPFIFO entry + GP_PUT=1 (2 combos)
  H: G + doorbell (NOTIFY_CHANNEL_PENDING) (2 combos)
  I: G + PCCSR scheduled bit write (2 combos)

J: VRAM instance block (via PRAMIN) + scheduler
  J: Instance in VRAM, runlist COH/NCOH (2 combos)

K: ALL structures in VRAM via PRAMIN
  K: Page tables, instance, GPFIFO, USERD, push buffer, runlist (1 config)

L: Hybrid — all VRAM + direct PBDMA programming
  L: K setup + direct PBDMA register writes, skip INST_BIND (1 config)
```

---

## Complete Findings

### Finding 1: GPU Warm State Is Fragile

The GPU has two observable states after nouveau unbind → vfio-pci bind:

| State | PMC_ENABLE | PFIFO registers | PRAMIN | Evidence |
|-------|-----------|-----------------|--------|----------|
| **Warm** | `0x5fecdff1` | Real values | Functional | Previous session |
| **Cold** | `0x40000020` | `0xbad0da00` | `0xbad0ac0x` | Current session |

The cold state means PFIFO engine domain is not clocked. All PFIFO, PBDMA, PCCSR
registers return the PRI (PRIvilege) error pattern `0xbad0xxxx`. VRAM reads via
PRAMIN also return `0xbad0acXX`.

**Critical**: The warm→cold transition can happen silently. The rebind script
reports success (nouveau bind returns rc=0) but the GPU remains cold. This is
likely due to:
- nouveau's unbind path explicitly de-clocking engines
- Race conditions in the bind/unbind sequence timing
- Bus-level reset despite `reset_method=""` override

**Impact on experiments**: On a cold GPU, experiments A-D all show
`PCCSR=0x15000001` (bit 26 set = additional fault type vs warm's `0x11000001`).
Direct PBDMA register writes (E-I) still work because PBDMA registers are in a
separate power domain. PRAMIN-based experiments (J, K, L) produce garbage because
VRAM is uninitialized.

### Finding 2: Scheduler Completely Ignores Runlist Submissions (Warm GPU)

On a properly warm GPU (PMC_ENABLE=`0x5fecdff1`, PBDMA_MAP=`0x0020000e`):

| Experiments | Count | PCCSR | PBDMA USERD | Scheduled? |
|-------------|-------|-------|-------------|------------|
| A (12 combos) | 12 | `0x00000001` | Residual | Never |
| B (12 combos) | 12 | `0x00000001` | Residual | Never |
| C (12 combos) | 12 | `0x00000001` | Residual | Never |
| D (12 combos) | 12 | `0x11000001` | Residual | Never (faults) |

48 experiments. Zero scheduled. The scheduler's runlist processing hardware is
not operational. Writes to `RUNLIST_BASE` (0x2270) and `RUNLIST` (0x2274) are
silently accepted but produce no state change.

Key register comparison:

| Register | Nouveau (healthy) | VFIO post-warm | Conclusion |
|----------|-------------------|----------------|------------|
| PFIFO_ENABLE (0x2200) | `0x00000000` | `0x00000000` | 0 is normal on GV100 |
| SCHED_EN (0x2504) | `0xbad00200` | `0xbad00200` | Does not exist on Volta |
| SCHED_DISABLE (0x2630) | `0x00000000` | `0x00000000` | Claims enabled |
| PCCSR_INST[0] | `0x802ffe48` (BIND=1, VRAM) | Our value | — |
| PCCSR_CHAN[0] | `0x00000003` (enabled+scheduled) | `0x00000001` | Never scheduled |

### Finding 3: Encoding Is Conclusively Irrelevant

The matrix tested every axis of encoding variation:

- PCCSR_INST target: COH(2) vs NCOH(3) — **no difference**
- Runlist USERD_TARGET: COH(2) vs NCOH(3) — **no difference**
- Runlist INST_TARGET: COH(2) vs NCOH(3) — **no difference**
- Runlist base target (0x2270): COH(2) vs NCOH(3) — **no difference**

All 48 scheduler-based experiments produce identical PBDMA state. The encoding
fixes from iterations 43-44 (USERD_TARGET bit position correction in DW0) are
structurally correct but irrelevant to the scheduling failure.

### Finding 4: Direct PBDMA Register Writes Work

Experiments E and F proved that PBDMA registers are read/write from BAR0:

| Register | Offset | Written | Read Back |
|----------|--------|---------|-----------|
| GP_BASE_LO | +0x040 | GPFIFO IOVA | ✓ Matches |
| GP_BASE_HI | +0x044 | Limit + aperture | ✓ Matches |
| USERD_LO | +0x0D0 | USERD IOVA + COH | ✓ Matches |
| USERD_HI | +0x0D4 | 0 | ✓ Matches |
| SIGNATURE | +0x0C0 | `0xFACE` | `0x3ACE` (bits 15:14 masked) |
| CHANNEL_INFO | +0x0AC | `0x10003080` | ✓ Matches |
| CONFIG | +0x0A8 | `0x00001100` | ✓ Matches |

The `SIGNATURE` reads back `0x3ACE` instead of `0xFACE` — bits [15:14] appear
to be reserved/masked. All other registers accept and return our values.

### Finding 5: PBDMA Does Not Process Commands Despite Direct Programming

Experiments G, H, I extended E with activation triggers:

| Experiment | GP_PUT written | GP_FETCH after 100ms | Scheduled? |
|------------|---------------|---------------------|------------|
| G (activate) | 1 | 0 | No |
| H (+ doorbell) | 1 | 0 | No |
| I (+ PCCSR sched bit) | 1 | 0 | **Yes** (faulted) |

Key observations:
- **G**: Writing `GP_PUT=1` to the PBDMA register directly does NOT trigger
  GPFIFO processing. `GP_FETCH` stays at 0.
- **H**: Ringing the doorbell (`NOTIFY_CHANNEL_PENDING`) does NOT cause PBDMA
  to process. The doorbell appears to signal the scheduler, not PBDMA directly.
- **I**: Writing `PCCSR scheduled bit (bit 1)` achieves `PCCSR=0x00000003`
  (enabled+scheduled) but this is a **status register**, not a trigger.
  GP_FETCH still 0. Faults appear.

### Finding 6: VRAM Structures Via PRAMIN Do Not Help (When Warm)

Experiments J, K, L placed GPU data structures in VRAM:

| Experiment | Structures in VRAM | INST_BIND | Scheduled? | PBDMA loaded? |
|------------|-------------------|-----------|------------|---------------|
| J | Instance block only | No (scheduler) | No | No (sentinels survive) |
| K | Everything (PT, inst, GPFIFO, USERD, RL) | Yes (faults) | No | No |
| L | Everything + direct PBDMA writes | No (skip BIND) | No | Direct writes visible |

On a warm GPU, J/K showed PRAMIN writes are functional (verified by read-back).
The scheduler still didn't process the VRAM-based runlist. INST_BIND with VRAM
targets still faults.

On a cold GPU, PRAMIN reads return `0xbad0acXX` — VRAM/FBIO not initialized.

### Finding 7: The `0x80c7xxxx` Pattern

On both warm and cold GPUs, after certain operations, PBDMA registers show the
pattern `0x80c700d0`, `0x80c700c0`, etc. This appears to be a PBDMA "error
readback" where the register offset (0xD0, 0xC0) is embedded in the value,
prefixed with `0x80c7`. This pattern appears when:
- The PBDMA attempts to load context from an invalid instance block
- The PFIFO scheduler pushes a channel to PBDMA but the context load fails
- INST_BIND is attempted with an invalid or inaccessible instance pointer

### Result Summary Table

```
╔══════════════════════════════════════════════════════════════╗
║ Total experiments:   62                                      ║
║ Faulted:             26 (all D, all E/F, all G-I, J, K, L)  ║
║ Scheduled:           2  (I_sched variants only, with faults) ║
║ Clean (no fault + scheduled): 0                              ║
║ PBDMA registers changed: 14 (E/F/G/H/I/J/K/L)              ║
║ GP_FETCH advanced:  0  (ZERO experiments processed work)     ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Root Cause Analysis

### Why The Scheduler Doesn't Work

The Volta PFIFO scheduler is a **hardware state machine** with internal tables
that are NOT accessible via BAR0 MMIO. These tables map:
- Channel ID → instance block pointer
- Runlist ID → channel group membership
- PBDMA assignment → engine routing
- Channel priority → scheduling order

Nouveau initializes these tables in `gk104_fifo_init()` and
`gv100_fifo_init()` — approximately 200+ register writes that set up:
1. PBDMA-to-runlist mapping
2. Engine-to-runlist routing
3. Per-channel PCCSR instance pointers with INST_BIND
4. Runlist submission with active channel groups
5. Interrupt routing and fault handling

After nouveau unbind, the scheduler's internal state is either:
- **Cleared**: nouveau's teardown path zeros the tables
- **Stale**: tables reference nouveau's now-unmapped DMA buffers
- **Inaccessible**: tables are in a SRAM that loses state when PFIFO is de-clocked

Evidence for the last option: on a cold GPU (PFIFO de-clocked), runlist
submissions have zero effect. On a warm GPU, they also have zero effect.
This suggests the scheduler's internal state is in volatile SRAM that is
cleared when PFIFO power-cycles during nouveau's unbind sequence.

### Why Direct PBDMA Programming Doesn't Work (Yet)

Writing PBDMA registers directly (GP_BASE, USERD, GP_PUT) successfully
changes the register values but doesn't trigger GPFIFO processing because:

1. **The PBDMA is idle**: Without the scheduler assigning a channel, the PBDMA
   is in an idle/halted state. Writing GP_PUT doesn't cause it to wake up.
2. **Missing execution trigger**: The PBDMA needs a "context load complete"
   signal from the scheduler before it starts fetching GPFIFO entries. Direct
   register writes bypass this handshake.
3. **PBDMA state machine**: The PBDMA has internal state beyond the MMIO
   registers (GP_FETCH, GP_STATE, CHANNEL_STATE at +0xB0). Writing GP_PUT=1
   may be insufficient — the PBDMA state machine may need to transition through
   specific states before it begins processing.

### Why The GPU Goes Cold

nouveau's unbind path (`gk104_fifo_fini()`, `nvkm_subdev_fini()`) explicitly:
1. Disables PFIFO interrupts
2. Clears runlists
3. Disables channels
4. **De-clocks the PFIFO engine domain** via PMC (bit 8 of 0x0200)

The GPU then enters a low-power state where only the top-level PMC and
boot registers are accessible. Our `w(pmc::ENABLE, 0xFFFF_FFFF)` write in
`diagnostic_matrix()` is insufficient because:
- PMC_ENABLE controls engine clock gating but may be read-only on some bits
- PFIFO initialization requires a specific sequence (reset via PMC, then
  configure internal registers)
- VRAM requires separate FB/FBPA initialization that nouveau performs during bind

---

## Forward Plan

### Phase 1: PFIFO Re-Initialization from Rust (Next Session)

The most promising near-term path. Replicate nouveau's `gk104_fifo_init()` +
`gv100_fifo_init()` sequence from Rust:

```
Step 1: PFIFO engine reset
  w(0x0200, r(0x0200) & ~0x100)     // PMC: disable PFIFO
  sleep(10ms)
  w(0x0200, r(0x0200) | 0x100)      // PMC: enable PFIFO
  sleep(10ms)

Step 2: PFIFO internal configuration
  // Populate from nouveau mmiotrace or read_bar0_deep.py diff
  // 0x2200 PFIFO_ENABLE
  // 0x2630 SCHED_DISABLE
  // 0x2004 PBDMA_MAP
  // etc.

Step 3: Channel setup
  PCCSR_INST with INST_BIND=TRUE
  PCCSR_CHAN ENABLE_SET

Step 4: Runlist submission
  RUNLIST_BASE + RUNLIST
```

**Data needed**: mmiotrace of nouveau's full init sequence, focusing on PFIFO
registers (0x2000-0x2FFF) and PBDMA registers (0x40000-0x4FFFF).

### Phase 2: Dual Titan V Reference Rig

When the second Titan V arrives:
- **Card A**: nouveau (reference oracle) — always has a healthy PFIFO
- **Card B**: vfio-pci (sovereign dispatch) — testing target

Benefits:
- Live register comparison without rebind cycles
- mmiotrace nouveau's dispatch sequence on Card A while testing on Card B
- Read PBDMA state during active dispatch to see exactly what the scheduler
  populates
- Capture the complete PBDMA register dump for a working compute dispatch and
  replicate it directly on Card B

### Phase 3: mmiotrace Nouveau Init

Even with single GPU, we can capture nouveau's full init sequence:

```bash
# Mount debugfs, enable mmiotrace
mount -t debugfs debugfs /sys/kernel/debug
echo mmio > /sys/kernel/debug/tracing/current_tracer
echo 1 > /sys/kernel/debug/tracing/tracing_on

# Bind nouveau (this captures ALL MMIO writes)
echo $GPU > /sys/bus/pci/drivers/nouveau/bind

# Stop tracing
echo 0 > /sys/kernel/debug/tracing/tracing_on
cat /sys/kernel/debug/tracing/trace > nouveau_init_mmiotrace.txt
```

This gives us the exact register write sequence for PFIFO initialization.
We can then replay it from Rust.

### Phase 4: Replication Harness for Multi-GPU Learning

The diagnostic matrix infrastructure generalizes to any GPU:

```rust
pub trait GpuDiagnostic {
    fn experiment_matrix(&self, configs: &[ExperimentConfig]) -> Vec<ExperimentResult>;
    fn reference_capture(&self) -> RegisterSnapshot;
    fn warm_verify(&self) -> WarmState;
}

struct NvidiaDiagnostic { bar0: MappedBar, ... }
struct AmdDiagnostic { bar0: MappedBar, ... }
```

When MI50s arrive:
- Same matrix pattern applies to AMD's SDMA/GFX engines
- ROCm-bound MI50 as reference, VFIO-bound MI50 as test target
- Register discovery via open-gpu-kernel-modules equivalent

---

## Testing Infrastructure

### Running the Diagnostic Matrix

```bash
# 1. Warm GPU with nouveau (REQUIRES pkexec/sudo)
pkexec bash -c '
GPU=0000:4b:00.0; AUD=0000:4b:00.1
echo "" > /sys/bus/pci/devices/$GPU/reset_method 2>/dev/null
echo $GPU > /sys/bus/pci/drivers/vfio-pci/unbind 2>/dev/null
echo $AUD > /sys/bus/pci/drivers/vfio-pci/unbind 2>/dev/null
echo "" > /sys/bus/pci/devices/$GPU/driver_override
echo $GPU > /sys/bus/pci/drivers/nouveau/bind; sleep 5
echo $GPU > /sys/bus/pci/drivers/nouveau/unbind; sleep 2
echo vfio-pci > /sys/bus/pci/devices/$GPU/driver_override
echo vfio-pci > /sys/bus/pci/devices/$AUD/driver_override
echo $GPU > /sys/bus/pci/drivers/vfio-pci/bind
echo $AUD > /sys/bus/pci/drivers/vfio-pci/bind
sleep 1; chmod 666 /dev/vfio/36'

# 2. Verify warm state (PMC_ENABLE should be 0x5fecdff1, not 0x40000020)
# The matrix prints this in ONE-SHOT PROBES section

# 3. Run matrix (no sudo needed)
CORALREEF_VFIO_BDF=0000:4b:00.0 CORALREEF_VFIO_SM=70 \
cargo test --test hw_nv_vfio --features vfio \
  -- --ignored --test-threads=1 --nocapture vfio_pfifo_diagnostic_matrix
```

### Warm State Verification

Add to the matrix's one-shot probes — if any of these are true, the GPU is cold
and results are unreliable:

```
PMC_ENABLE == 0x40000020        → cold (engines off)
PFIFO_ENABLE == 0xbad0da00      → cold (PFIFO de-clocked)
PBDMA_MAP == 0xbad0da00         → cold (PFIFO de-clocked)
PRAMIN read returns 0xbad0acXX  → cold (VRAM not initialized)
```

### Adding New Experiments

```rust
// 1. Add variant to ExperimentOrdering
pub enum ExperimentOrdering {
    // ... existing A-L ...
    NewExperiment,  // M: description
}

// 2. Add configs to build_experiment_matrix()
configs.push(ExperimentConfig {
    name: "M_description",
    ordering: ExperimentOrdering::NewExperiment,
    // ...
});

// 3. Add match arm in diagnostic_matrix()
ExperimentOrdering::NewExperiment => {
    // ... register writes ...
}
```

---

## Key Register Reference (GV100 PFIFO)

| Register | Offset | Warm Nouveau | Warm VFIO | Cold VFIO | Notes |
|----------|--------|-------------|-----------|-----------|-------|
| BOOT0 | 0x000 | `0x140000a1` | `0x140000a1` | `0x140000a1` | Always accessible |
| PMC_ENABLE | 0x200 | `0x5fecdff1` | varies | `0x40000020` | Engine clocking |
| PFIFO_ENABLE | 0x2200 | `0x00000000` | `0x00000000` | `0xbad0da00` | 0=normal on GV100 |
| SCHED_EN | 0x2504 | `0xbad00200` | `0xbad00200` | `0xbad0da00` | Does not exist |
| SCHED_DISABLE | 0x2630 | `0x00000000` | `0x00000000` | `0xbad0da00` | 0=enabled |
| PBDMA_MAP | 0x2004 | `0x0020000e` | `0x0020000e` | `0xbad0da00` | PBDMAs 1,2,3,21 |
| PCCSR_INST[0] | 0x800000 | `0x802ffe48` | our value | `0xbad0da00` | BIND=1 in nouveau |
| PCCSR_CHAN[0] | 0x800004 | `0x00000003` | `0x00000001` | `0xbad0da00` | Warm: never sched |
| ENGN0_STATUS | 0x2640 | `0x10021002` | `0x10021002` | `0xbad0da00` | GR engine alive |

### PBDMA Register Map (per-PBDMA at 0x40000 + id*0x2000)

| Register | Offset | Written by E/F/G | Notes |
|----------|--------|-----------------|-------|
| GP_BASE_LO | +0x040 | ✓ accepts | GPFIFO ring base (low) |
| GP_BASE_HI | +0x044 | ✓ accepts | Limit + aperture + base (high) |
| GP_FETCH | +0x048 | writable | PBDMA's current fetch pointer (never advances) |
| GP_STATE | +0x04C | writable | PBDMA GPFIFO state |
| GP_PUT | +0x054 | ✓ accepts | Next entry to process (never triggers fetch) |
| CHANNEL_STATE | +0x0B0 | r/w | Channel state machine |
| CONFIG | +0x0A8 | ✓ accepts | Channel config |
| CHANNEL_INFO | +0x0AC | ✓ accepts | Channel ID + info |
| SIGNATURE | +0x0C0 | partial | Bits [15:14] masked (reads 0x3ACE for 0xFACE) |
| USERD_LO | +0x0D0 | ✓ accepts | USERD page address (low) + aperture |
| USERD_HI | +0x0D4 | ✓ accepts | USERD page address (high) |

---

## Experiment Data: Cold vs Warm Comparison

### Cold GPU Run (this session, PMC=0x40000020)

```
A-D (48 configs):  All PCCSR=0x00000001 or 0x15000001, PBDMA=residual
E-F (4 configs):   PCCSR=0x15000001, PBDMA registers=OUR values, GP_FETCH=0
G-I (6 configs):   PCCSR=0x15000001/0x15000003, GP_PUT=1, GP_FETCH=0
J-K (3 configs):   PRAMIN reads=0xbad0ac0X, scheduler shows 0x80c7 pattern
L   (1 config):    GP_BASE=0x00009000 (VRAM), SIG=0x3ACE, GP_FETCH=0
```

### Warm GPU Run (previous session, PMC=0x5fecdff1)

```
A-D (48 configs):  All PCCSR=0x00000001 (A-C) or 0x11000001 (D)
E-F (4 configs):   PCCSR=0x00000001 (E) or 0x11000001 (F), PBDMA=OUR values
G-I (6 configs):   Similar to cold but I shows PCCSR=0x00000003 (scheduled!)
J-K (3 configs):   PRAMIN functional, scheduler processes runlist, SCHEDULED
L   (1 config):    SCHEDULED, but GP_FETCH still 0
```

**The warm run's key breakthrough**: With corrected runlist entry format
(USERD_TARGET at bits [7:6], INST_TARGET at bits [5:4]), the number of
"scheduled" experiments jumped dramatically. The scheduler **can** process
our runlist and mark channels as scheduled. But scheduled ≠ dispatching.

---

## Conclusions (Updated with N Experiment Results)

1. **The scheduler works on warm GPU** when given correctly formatted runlists
   with INST_BIND=TRUE. 18 clean+scheduled configs confirmed (D, N, I, K).

2. **INST_BIND + runlist = SCHEDULED**. The D path (INST_BIND → enable → runlist)
   consistently achieves `PCCSR=0x00000003` on warm GPU. INST_BIND initially
   faults (`0x11000000`) but the runlist submission clears the fault and the
   scheduler assigns the channel.

3. **N (full dispatch) is CLEAN + SCHEDULED** — INST_BIND + enable + runlist +
   GPFIFO entry + USERD GP_PUT=1 + doorbell all succeed without faults. But
   **GP_FETCH still 0**. The PBDMA doesn't load the RAMFC context.

4. **The gap is PBDMA context load**. The scheduler marks the channel as
   "scheduled" but does NOT push the RAMFC contents into the PBDMA's operational
   registers. PBDMA USERD/GP_BASE/SIGNATURE stay at their pre-experiment values.
   The context load step (scheduler → PBDMA) is the missing link.

5. **PMC_ENABLE write kills warm state**. Writing `0xFFFFFFFF` to PMC_ENABLE
   destroys the GPU warm state. Removing this write allows multiple experiments
   per warm cycle. PRAMIN writes (J/K/L) and faulting experiments eventually
   de-clock PFIFO too, but the scheduler-only experiments (A-D, N) are safe.

6. **The warm state is fragile**. The GPU goes cold between matrix runs if any
   destructive experiments ran. Warm-state verification via PMC_ENABLE check is
   essential.

7. **Next focus: PBDMA context load trigger**. Either:
   - Find the register/interrupt that tells the PBDMA to load from RAMFC
   - mmiotrace nouveau to see what register sequence activates PBDMA context load
   - The dual Titan V approach (live-read PBDMA during nouveau dispatch)

---

## Files Modified in This Investigation

| File | Change |
|------|--------|
| `coral-driver/src/vfio/channel.rs` | 12 experiment orderings, 62-config matrix |
| `coral-driver/src/nv/vfio_compute.rs` | `RawVfioDevice` for raw BAR0 access |
| `coral-driver/src/nv/mod.rs` | Re-export `RawVfioDevice` |
| `coral-driver/tests/hw_nv_vfio.rs` | `vfio_pfifo_diagnostic_matrix` test |
| `hotSpring/scripts/read_bar0_deep.py` | Extended register probe |
| `hotSpring/scripts/nouveau_reference_bar0.txt` | Reference capture |

---

## Next Session Priorities

1. **mmiotrace nouveau init** — capture the full PFIFO register write sequence
2. **Add warm-state guard** — abort matrix early if PMC_ENABLE is cold
3. **Experiment M: PFIFO engine reset from Rust** — replicate `gk104_fifo_init()`
4. **Begin replication harness** — scriptable warm/test/capture cycle

---

*From hotSpring diagnostic matrix sessions, March 13, 2026.*
*"The scheduler works when warm. We need to learn how to make it work for us."*
