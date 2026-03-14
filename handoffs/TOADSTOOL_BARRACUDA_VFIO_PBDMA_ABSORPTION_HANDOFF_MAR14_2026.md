# toadStool / barraCuda — VFIO PBDMA Context Load Absorption Handoff

**Source**: hotSpring VFIO debugging session on biomeGate (March 13-14, 2026)
**Target teams**: toadStool (GPU hardware management), barraCuda (math dispatch)
**Hardware**: Titan V (GV100, SM70, Volta) on `vfio-pci`
**coralReef**: Phase 10, Iteration 44+ (`coral-driver` crate, `--features vfio`)
**Chat**: [VFIO PBDMA breakthrough](28732f32-750e-4053-a1ae-a8d39a738d7a)

---

## Executive Summary

The VFIO PFIFO channel creation path on Volta (GV100) has been debugged to
the point where the **hardware scheduler loads our RAMFC channel context into
a PBDMA engine**. This is the first successful context load on the sovereign
dispatch path. Three critical register-level discoveries make this possible.

One gap remains: the PBDMA does not read GP_PUT from the USERD buffer in
system memory (suspected IOMMU DMA path issue). Hardware reconfiguration
(GTX 1050 + 2x Titan V) is planned to close this gap via mmiotrace oracle.

---

## For toadStool: Register Discoveries

### Discovery 1: GV100 Runlist Preempt (0x002638)

Volta uses a **per-runlist** preempt register at `0x002638`, distinct from
the older per-channel preempt at `0x002634`.

```
Register: 0x002638
Write:    BIT(runlist_id)    // e.g. 0x2 for runlist 1
Effect:   Forces scheduler to evict current PBDMA context and re-evaluate
Source:   gv100_runl_preempt() in nouveau gv100.c
```

**Why toadStool needs this**: After unbinding nouveau, PBDMA1 retains a stale
channel context (STATE=0x07800000). Without issuing the preempt at 0x002638,
the scheduler cannot evict the stale context and load a new channel. Any
toadStool PFIFO initialization on Volta must include this preempt step.

### Discovery 2: Runlist Completion ACK (0x002A00)

After submitting a runlist (via `0x002270`/`0x002274`), the scheduler fires
PFIFO_INTR bit 30 (0x40000000). Software **must** acknowledge:

```
1. Read  0x002A00                    → bitmask of completed runlists
2. Write 0x002A00 with BIT(runl_id)  → acknowledge specific runlist
3. Write 0x002100 with 0x40000000    → clear PFIFO_INTR bit 30
```

**Why toadStool needs this**: Without this ACK loop, the scheduler stalls in
a "waiting for software" state and will never dispatch channels to PBDMAs.
This is the single most important discovery — it was the breakthrough that
enabled the first successful context load.

Source: `gk104_fifo_intr_runlist()` in nouveau `gk104.c`.

### Discovery 3: PBDMA Register Layout = RAMFC Offsets

PBDMA operational registers at `PBDMA_BASE + offset` map 1:1 to RAMFC
instance block offsets. When the scheduler loads a channel, the RAMFC fields
appear at matching offsets in the PBDMA register space.

**Full RAMFC offset table (GV100)**:

| RAMFC Offset | PBDMA Offset | Field | Notes |
|-------------|-------------|-------|-------|
| 0x000 | BASE+0x000 | RAMFC_BASE | Low 32 bits |
| 0x004 | BASE+0x004 | RAMFC_BASE_HI | High 32 bits |
| 0x008 | BASE+0x008 | USERD_LO | Bits [31:9]=addr, [3:2]=target (PBDMA encoding: 0=VID, 1=COH, 2=NCOH) |
| 0x00C | BASE+0x00C | USERD_HI | Upper address bits |
| 0x010 | BASE+0x010 | SIGNATURE | **Must be 0x0000FACE** (enforced by PBDMA) |
| 0x030 | BASE+0x030 | ACQUIRE | Semaphore acquire |
| 0x048 | BASE+0x048 | GP_BASE_LO | GPFIFO base address (low) |
| 0x04C | BASE+0x04C | GP_BASE_HI | Bits [31:28]=aperture, [10:0]=limit |
| 0x084 | BASE+0x084 | PB_HEADER | Push buffer header |
| 0x094 | BASE+0x094 | SUBDEVICE | |
| 0x0E4 | BASE+0x0E4 | REF | Reference |
| 0x0E8 | BASE+0x0E8 | CHID | Channel ID |
| 0x0F4 | BASE+0x0F4 | CONFIG | Configuration |
| 0x0F8 | BASE+0x0F8 | CHANNEL_INFO | |

### Discovery 4: SIGNATURE Validation

PBDMA validates the SIGNATURE field at RAMFC offset 0x010. If the value
is not `0x0000FACE`, PBDMA fires INTR bit 31 (`SIGNATURE` error).

This is useful as a diagnostic: writing `0xDEAD` to the SIGNATURE field
and observing the PBDMA error confirms that the scheduler loaded a fresh
context from your instance block (not a stale remnant from nouveau).

PBDMA INTR bit names (from `gk104_runq_intr_0_names`):
```
Bit 31: SIGNATURE    (not CTXNOTVALID — that's a different register)
Bit 24: LB_ERROR
Bit 21: PB_CRC
Bit 20: METHOD
...
```

### Discovery 5: Engine Context Binding (gv100_ectx_bind)

PBDMA requires GR engine context binding before it will process GPFIFO
entries. From nouveau `gv100.c`:

```
inst[0x210] = lower_32(ctx_addr | 4)    // engine context address, bit 2 set
inst[0x214] = upper_32(ctx_addr | 4)    // upper 32 bits
inst[0x0AC] |= 0x00010000               // set bit 16 (bind flag)
```

Without this, the PBDMA may fire CTXNOTVALID via the HCE INTR register
(at PBDMA offset 0x148, bit 31).

### PBDMA-to-Runlist Mapping (GV100)

```
PBDMA_MAP = 0x0020000e
  PBDMA 1  → runlist 1  (base = 0x41000)
  PBDMA 2  → runlist 1  (base = 0x42000)
  PBDMA 3  → runlist 2  (base = 0x43000)
  PBDMA 21 → runlist 4  (base = 0x55000)

ENGN0 (GR) → runlist 1
```

### Runlist Submission Format (GK104/GV100)

```
RUNLIST_BASE (0x002270): (target << 28) | (phys_addr >> 12)
  target: 0=VRAM, 2=SYS_MEM_COH, 3=SYS_MEM_NCOH

RUNLIST (0x002274): (runl_id << 20) | channel_count
  No trigger bit — the write itself triggers processing.
```

### Runlist Channel Entry Format (16 bytes)

```
DW0: [31:12]=USERD_PTR_LO, [11:10]=USERD_TARGET (PCCSR encoding: 0=VRAM, 2=COH, 3=NCOH),
     [0]=TYPE (0=channel, 1=TSG)
DW1: [31:0]=INST_PTR_LO [31:4] (instance block address bits [31:4], 4K aligned)
DW2: [31:17]=USERD_PTR_HI, [16:0]=INST_PTR_HI
DW3: [31:20]=CHID, [19:12]=RUNQUEUE_SELECTOR
```

**Critical encoding difference**: Runlist entry USERD_TARGET uses **PCCSR
encoding** (0=VRAM, 2=COH), while RAMFC USERD_LO uses **PBDMA encoding**
(0=VID, 1=COH). These are NOT the same! The runlist tells the scheduler
where USERD is; the RAMFC tells the PBDMA where USERD is.

---

## For barraCuda: Dispatch Pipeline Readiness

### What "PBDMA Context Loaded" Means

The GPFIFO dispatch pipeline has these stages:

```
1. Channel creation (instance block, RAMFC, page tables)  ✅ DONE
2. Runlist submission (scheduler accepts channel)          ✅ DONE
3. Scheduler dispatches to PBDMA (RAMFC → PBDMA regs)     ✅ DONE ← breakthrough
4. PBDMA reads GP_PUT from USERD                          ❌ BLOCKED
5. PBDMA fetches GPFIFO entries                            ❌ BLOCKED
6. PBDMA processes push buffer methods                     ❌ BLOCKED
7. GR engine executes compute shader                       ❌ BLOCKED
```

Stage 3 is now confirmed working. Stages 4-7 are blocked on the USERD DMA
read issue. Once GP_PUT is readable by the PBDMA, the remaining stages
should follow automatically — there is no known additional gap.

### Remaining Gap: USERD DMA Read

The PBDMA has our GPFIFO base address and all channel parameters loaded.
It should poll USERD offset 0x8C (GP_PUT) to detect pending work. We wrote
GP_PUT=1 to host memory at IOVA 0x208C. But the PBDMA does not advance
GP_FETCH.

**Hypothesis**: PBDMA's DMA reads from system memory may not traverse the
IOMMU correctly in the VFIO configuration. The VFIO container maps host
physical pages into IOVA space, but the PBDMA's polling reads may use a
different DMA path than explicit data transfers (which work — DMA upload/
readback passes).

**Current test**: Moving USERD into VRAM (via PRAMIN write at VRAM offset
0x0000) and pointing RAMFC USERD_LO to VRAM (target=0). If the PBDMA reads
GP_PUT from VRAM and starts fetching, this confirms the IOMMU DMA path
issue and we know all PBDMA-accessed buffers need to be in VRAM.

### Projected Timeline

| Milestone | Est. Date | Depends On |
|-----------|----------|-----------|
| VRAM USERD test result | March 15 | Current code changes |
| Hardware swap (1050 + 2x Titan V) | March 15-16 | Physical swap |
| Nouveau mmiotrace on oracle Titan V | March 16-17 | Dual Titan V online |
| GP_PUT fix identified | March 17-18 | mmiotrace analysis |
| 7/7 `vfio_dispatch_nop_shader` | March 18-20 | GP_PUT fix |
| First barraCuda shader via VFIO | March 20+ | 7/7 test pass |

---

## Dual Titan V Strategy

### Hardware Plan

```
Current:  GTX 1050 (display) + RTX 3090 (display/compute) + Titan V (VFIO)
Planned:  GTX 1050 (headless display) + Titan V #1 (nouveau oracle) + Titan V #2 (VFIO target)
```

### Oracle Strategy

Titan V #1 stays on nouveau. We run mmiotrace during nouveau's channel
creation to capture the exact register sequence the hardware scheduler
uses on Volta. This gives us:

1. Complete PBDMA register initialization sequence
2. USERD polling mechanism and timing
3. Doorbell → GP_FETCH advancement trigger
4. Engine context binding details for GR

We then replicate this exact sequence on Titan V #2 via VFIO.

### Why Not CUDA Oracle?

CUDA adds layers of abstraction (RM, GSP firmware on Turing+). On Volta,
there is no GSP — CUDA talks to the hardware more directly, but the driver
source is closed. nouveau's source is open and maps to specific register
addresses. mmiotrace captures the exact BAR0 writes regardless of driver
complexity.

---

## GV100-Specific Register Reference

| Address | Name | Width | Description |
|---------|------|-------|-------------|
| 0x002100 | PFIFO_INTR | 32 | PFIFO interrupt status (W1C) |
| 0x002140 | PFIFO_INTR_EN | 32 | PFIFO interrupt enable |
| 0x002270 | RUNLIST_BASE | 32 | Runlist physical address + target |
| 0x002274 | RUNLIST | 32 | Runlist ID + channel count (trigger) |
| 0x002284+8n | RUNLIST_PENDING(n) | 32 | Bit 20 = runlist n pending |
| 0x002634 | PREEMPT | 32 | Per-channel preempt (older) |
| 0x002638 | GV100_PREEMPT | 32 | Per-runlist preempt (Volta+) |
| 0x002A00 | RUNLIST_ACK | 32 | Runlist completion bitmask (R/W) |
| 0x002A04 | PBDMA_INTR_ROUTE | 32 | PBDMA interrupt routing |
| 0x800000+ch*8 | PCCSR_CHANNEL(ch) | 32 | Channel enable/status |
| 0x800004+ch*8 | PCCSR_INST(ch) | 32 | Instance block pointer + bind |
| 0x810090 | DOORBELL | 32 | Notify channel pending (usermode) |
| 0x040000+id*0x1000 | PBDMA_BASE(id) | — | PBDMA register block |
| PBDMA+0x008 | PBDMA_USERD_LO | 32 | Loaded USERD address |
| PBDMA+0x010 | PBDMA_SIGNATURE | 32 | Must be 0xFACE |
| PBDMA+0x048 | PBDMA_GP_BASE_LO | 32 | Loaded GPFIFO base |
| PBDMA+0x04C | PBDMA_GP_BASE_HI | 32 | Aperture + limit |
| PBDMA+0x080 | PBDMA_GP_FETCH | 32 | Current GP fetch pointer |
| PBDMA+0x084 | PBDMA_PB_HEADER | 32 | Current push buffer header |
| PBDMA+0x08C | PBDMA_GP_PUT | 32 | GP_PUT as seen by PBDMA |
| PBDMA+0x0E8 | PBDMA_CHID | 32 | Loaded channel ID |
| PBDMA+0x0F4 | PBDMA_CONFIG | 32 | Channel config |
| PBDMA+0x0F8 | PBDMA_CHANNEL_INFO | 32 | Channel info |
| PBDMA+0x108 | PBDMA_INTR | 32 | PBDMA interrupt status |
| PBDMA+0x110 | PBDMA_STATE | 32 | PBDMA operational state |
| PBDMA+0x148 | PBDMA_HCE_INTR | 32 | HCE interrupt (bit 31 = CTXNOTVALID) |

---

## Absorption Guidance

### For toadStool

1. **Add GV100 PFIFO initialization to toadStool's GPU management layer**:
   - The three-step protocol: preempt(0x2638) → runlist submit → ACK(0x2A00)
   - PCCSR channel enable sequence: INST_BIND → ENABLE_SET
   - PBDMA state monitoring (dump operational registers at RAMFC offsets)

2. **Encode the dual target encoding correctly**:
   - Runlist channel entry uses PCCSR encoding (0=VRAM, 2=COH)
   - RAMFC USERD_LO uses PBDMA encoding (0=VID, 1=COH)
   - Getting this wrong causes silent failures (PBDMA reads from wrong aperture)

3. **Add warm-state guard**: Volta without GSP can enter a "cold" state after
   nouveau unbind if power management de-clocks the PFIFO. Check that
   `NV_PMC_ENABLE` bit 8 is set and `PFIFO_INTR_EN` is non-zero.

### For barraCuda

1. **No immediate code changes needed** — the GPFIFO submission format and
   shader compilation pipeline are correct. The gap is at the hardware
   scheduling layer (toadStool/coralReef territory).

2. **When 7/7 passes**: The first barraCuda compute shader dispatched via
   VFIO will be a NOP shader (fence write only). After that, the full
   `MdEngine<VfioBackend>` integration can proceed.

3. **DF64 via VFIO**: The sovereign dispatch path eliminates the naga
   WGSL→SPIR-V codegen bug that causes NVVM device poisoning. DF64 shaders
   compiled directly to SASS via coralReef should deliver the full 9.9×
   throughput improvement without the transcendental poisoning workaround.

---

## Key Source Files

| File | What It Contains |
|------|-----------------|
| `coralReef/crates/coral-driver/src/vfio/channel.rs` | PFIFO channel creation, diagnostic matrix (experiments A-Q) |
| `coralReef/crates/coral-driver/tests/hw_nv_vfio.rs` | Integration test: `vfio_dispatch_nop_shader` (6/7 pass) |
| `coralReef/crates/coral-driver/src/nv/bar0.rs` | Safe BAR0 MMIO access module |
| `hotSpring/scripts/warm_and_test.sh` | Reliable warm-boot + test runner |
| `hotSpring/scripts/capture_nouveau_mmiotrace.sh` | mmiotrace capture for dual Titan V |
| `hotSpring/scripts/nouveau_reference_bar0.txt` | Captured BAR0 registers after nouveau bind |
| `hotSpring/experiments/058_VFIO_PBDMA_CONTEXT_LOAD.md` | Experiment journal for this session |

---

*March 14, 2026 — The scheduler dispatches. The PBDMA loads. The last mile is DMA.*
