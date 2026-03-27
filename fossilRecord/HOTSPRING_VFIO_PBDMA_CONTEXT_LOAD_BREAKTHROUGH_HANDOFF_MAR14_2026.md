# hotSpring — VFIO PBDMA Context Load Breakthrough

**Source**: hotSpring substrate-level VFIO debugging on biomeGate
**Date**: March 14, 2026
**Hardware**: Titan V (GV100, SM70) at `0000:4b:00.0`
**Kernel**: 6.17.9-76061709-generic
**coralReef**: Phase 10, Iteration 44+, crate `coral-driver` with `--features vfio`
**Prior handoffs**: `HOTSPRING_VFIO_PFIFO_COMPLETE_DIAGNOSTIC_MATRIX_HANDOFF_MAR13_2026.md` (now archived — its conclusion "runlist submissions are silently ignored" is **proven wrong**)
**Chat**: [VFIO PBDMA breakthrough](28732f32-750e-4053-a1ae-a8d39a738d7a)

---

## Executive Summary

Three critical discoveries unlock the GV100 Volta PFIFO scheduler for VFIO
dispatch. The hardware scheduler **does** load our RAMFC channel context into
PBDMA2 — confirmed by writing a distinctive signature (0xDEAD) to the VRAM
instance block and observing it appear in PBDMA2's operational registers.

| Discovery | Register | What It Does |
|-----------|----------|-------------|
| **GV100 runlist preempt** | `0x002638` | Write `BIT(runl_id)` to force scheduler re-evaluation. Clears stale PBDMA contexts left by nouveau after unbind. NOT `0x002634` (which is the older per-channel preempt). |
| **Runlist ACK** | `0x002A00` | After runlist submission, the scheduler fires PFIFO_INTR bit 30 (RUNLIST). Software MUST read `0x002A00` and write `BIT(runl_id)` to acknowledge. Without this, the scheduler will not dispatch channels to PBDMAs. |
| **PBDMA register layout = RAMFC offsets** | `PBDMA_BASE + 0x008..0x0F8` | PBDMA operational registers map 1:1 to RAMFC instance block offsets. When the scheduler loads context, RAMFC fields appear at their same offsets in the PBDMA register space. |

**Current blocker**: PBDMA2 has our context loaded (zero errors, zero faults)
but does not read GP_PUT from USERD in system memory. Suspected IOMMU DMA
path issue — the PBDMA's USERD polling may not traverse the system IOMMU for
host memory reads.

**Next steps**: VRAM USERD test (write GP_PUT to VRAM via PRAMIN), then dual
Titan V mmiotrace to capture nouveau's complete PBDMA dispatch sequence.

---

## The Three Discoveries In Detail

### 1. GV100 Runlist Preempt (0x002638)

From nouveau `gv100.c`:
```c
void gv100_runl_preempt(struct nvkm_runl *runl)
{
    nvkm_wr32(device, 0x002638, BIT(runl->id));
}
```

This is distinct from the older preempt register at `0x002634`. Writing
`BIT(runlist_id)` forces the scheduler to preempt the current runlist
processing and re-evaluate. On a warm GPU after nouveau unbind, PBDMA1 retains
nouveau's stale channel context (STATE=0x07800000, SIGNATURE=0x3ACE). Without
the preempt, the scheduler cannot evict this stale context and load ours.

For runlist 1 (GR engine): write `0x2` to `0x002638`.

### 2. Runlist Completion ACK (0x002A00)

From nouveau `gk104.c`:
```c
void gk104_fifo_intr_runlist(struct nvkm_fifo *fifo)
{
    u32 mask = nvkm_rd32(device, 0x002a00);
    nvkm_runl_foreach_cond(runl, fifo, mask & BIT(runl->id)) {
        nvkm_wr32(device, 0x002a00, BIT(runl->id));
    }
}
```

After a runlist submission (`gk104_runl_commit` writes to `0x002270` and
`0x002274`), the scheduler processes the runlist and fires PFIFO_INTR bit 30
(0x40000000). The interrupt handler must:

1. Read `0x002A00` to get the bitmask of completed runlists
2. Write `BIT(runl_id)` to `0x002A00` for each completed runlist
3. Clear PFIFO_INTR bit 30 by writing `0x40000000` to `0x002100`

Without this acknowledgment, the scheduler remains in a "waiting for software"
state and will not dispatch channels to PBDMAs.

### 3. PBDMA Registers Map to RAMFC Offsets

The PBDMA's operational register space mirrors the RAMFC layout:

| RAMFC Offset | PBDMA Offset | Field | Our Value |
|-------------|-------------|-------|-----------|
| 0x008 | BASE+0x008 | USERD_LO | 0x00002001 (IOVA 0x2000, target=COH) |
| 0x010 | BASE+0x010 | SIGNATURE | 0x0000FACE (validated by PBDMA) |
| 0x030 | BASE+0x030 | ACQUIRE | 0x7FFFF902 |
| 0x048 | BASE+0x048 | GP_BASE_LO | 0x00001000 (GPFIFO GPU VA) |
| 0x04C | BASE+0x04C | GP_BASE_HI | 0x00070000 (limit2=7) |
| 0x084 | BASE+0x084 | PB_HEADER | 0x60400000 |
| 0x094 | BASE+0x094 | SUBDEVICE | 0x30000FFF |
| 0x0E8 | BASE+0x0E8 | CHID | 0x00000000 (channel 0) |
| 0x0F4 | BASE+0x0F4 | CONFIG | 0x00001100 |
| 0x0F8 | BASE+0x0F8 | CHANNEL_INFO | 0x10003080 |

Confirmation evidence: CONFIG changed from default 0x00000100 to our 0x00001100,
CHANNEL_INFO changed from default 0x00003080 to our 0x10003080, and SIGNATURE
appeared as 0x0000DEAD when we wrote that value to the VRAM instance block.

---

## Experiment Q: Full Protocol

### Setup
- Instance block in VRAM at offset 0x3000 (written via PRAMIN window)
- GPFIFO ring at system memory IOVA 0x1000
- USERD page at system memory IOVA 0x2000
- Page tables (PD3/PD2/PD1/PD0/PT0) at IOVAs 0x5000-0x9000
- Engine context binding: inst[0x0AC] bit 16, inst[0x210]=PT0_IOVA|4

### Sequence
```
1. Set BAR0_WINDOW=0 → PRAMIN maps VRAM[0..64K]
2. Copy instance block to VRAM via PRAMIN (4-byte writes)
3. Add engine context binding (inst[0x0AC], inst[0x210/0x214])
4. Prepare GPFIFO entry + USERD GP_PUT=1 in host memory
5. GV100 runlist preempt: w(0x002638, BIT(runlist_id))
6. PCCSR INST_BIND: w(pccsr::inst(ch), VRAM_PTR | BIND)
7. PCCSR ENABLE: w(pccsr::channel(ch), ENABLE_SET)
8. Submit runlist: w(0x002270, rl_base), w(0x002274, rl_submit)
9. Wait for PFIFO_INTR bit 30 (RUNLIST)
10. Read 0x002A00, write BIT(runl_id) to acknowledge
11. Clear PFIFO_INTR
12. Ring doorbell: w(0x810090, channel_id)
```

### Results
- PCCSR = 0x00000003 (ENABLED + SCHEDULED)
- PBDMA2 RAMFC registers match our instance block exactly
- PBDMA2 INTR = 0x00000000 (no errors)
- PFIFO_INTR = 0x00000000 (clean after ACK)
- PBDMA does NOT advance GP_FETCH — USERD GP_PUT not being read

---

## Discoveries Along the Way

### SIGNATURE Validation (PBDMA INTR bit 31)

PBDMA validates the RAMFC SIGNATURE field. Writing 0x0000DEAD instead of
0x0000FACE triggers PBDMA INTR bit 31, which is:

```
gk104_runq_intr_0_names: { 0x80000000, "SIGNATURE" }
```

This is a SIGNATURE mismatch error, **not** CTXNOTVALID. The PBDMA enforces
that SIGNATURE=0xFACE. Useful for confirming fresh context loads (change
signature → observe the error → confirm load) but must revert to FACE for
clean operation.

### Engine Context Binding (gv100_ectx_bind)

From nouveau `gv100.c`:
```c
void gv100_ectx_bind(struct nvkm_engn *engn, struct nvkm_cctx *cctx,
                      struct nvkm_chan *chan)
{
    u64 addr = cctx->vctx->vma->addr | 4ULL;
    nvkm_wo32(chan->inst, 0x210, lower_32_bits(addr));
    nvkm_wo32(chan->inst, 0x214, upper_32_bits(addr));
    nvkm_mo32(chan->inst, 0x0ac, 0x00010000, 0x00010000);
}
```

Without this binding, the PBDMA may fire CTXNOTVALID (HCE INTR at offset
0x148, bit 31). We set bit 16 at inst[0x0AC] and write a placeholder address
to inst[0x210/0x214].

### PBDMA State 0x07800000

PBDMA1 consistently shows STATE=0x07800000 after nouveau unbind. This
represents a frozen/halted PBDMA with nouveau's stale channel loaded. The
scheduler cannot use PBDMA1 until its stale context is preempted (via
0x002638). PBDMA2, in contrast, starts in a clean default state (STATE=0)
and is available for new channel dispatch.

### INST_BIND Fault is Transient

Writing PCCSR_INST with INST_BIND always produces a transient fault
(PCCSR=0x11000000: PBDMA_FAULTED + ENG_FAULTED). This happens for both VRAM
and system memory targets. The fault clears automatically when the runlist is
submitted. This is normal GV100 behavior, not an error.

### Runlist Format Verified

GV100 runlist commit (`gk104_runl_commit`):
```c
nvkm_wr32(device, 0x002270, (target << 28) | (addr >> 12));
nvkm_wr32(device, 0x002274, (runl->id << 20) | count);
```

No trigger bit. Our format is correct.

---

## PBDMA-to-Runlist Mapping (GV100)

From one-shot probes:
```
PBDMA_MAP = 0x0020000e  (PBDMAs 1, 2, 3, 21 active)
PBDMA 1 → runlist 1
PBDMA 2 → runlist 1
PBDMA 3 → runlist 2
PBDMA 21 → runlist 4

ENGN0 (GR) → runlist 1
Target PBDMA: 1 (base=0x42000)
```

---

## Current Blocker: USERD DMA Read

The PBDMA has our RAMFC context loaded into its operational registers. It
knows the GPFIFO address (GP_BASE=0x1000), the USERD address
(USERD_LO=0x2001 → IOVA 0x2000 with SYS_MEM_COHERENT target), and all other
channel parameters.

The PBDMA should poll USERD at offset 0x8C (GP_PUT) to check for pending
work. We wrote GP_PUT=1 to host memory at IOVA 0x208C. But the PBDMA does
not advance GP_FETCH.

**Hypothesis**: The PBDMA's DMA reads from system memory targets may not
traverse the IOMMU, or may require a specific IOMMU configuration that
VFIO's default container setup does not provide.

**Test**: Write USERD to VRAM via PRAMIN (at offset 0x0000) and point the
RAMFC USERD_LO to VRAM (target=0). If the PBDMA reads GP_PUT from VRAM and
starts fetching, this confirms the IOMMU DMA path issue.

---

## Forward Plan

### Immediate (before hardware swap)
1. Complete VRAM USERD test in experiment Q
2. If PBDMA fetches with VRAM USERD: confirms IOMMU issue, need all
   PBDMA-accessed buffers in VRAM

### After hardware swap (GTX 1050 + 2x Titan V)
3. **Dual Titan V strategy**: Titan V #1 on nouveau (oracle), Titan V #2 on
   VFIO (target)
4. **mmiotrace** nouveau's full channel dispatch on Titan V #1 to capture:
   - PBDMA register writes during context load
   - USERD polling mechanism
   - GP_FETCH advancement triggers
5. Replicate exact nouveau PBDMA sequence on VFIO Titan V #2
6. Close the USERD GP_PUT gap and achieve 7/7 `vfio_dispatch_nop_shader`

### Infrastructure built
| Component | Location | Status |
|-----------|----------|--------|
| Experiment Q (VramFullDispatch) | `channel.rs` | Working — context loads |
| Preempt + ACK loop | `channel.rs` | Working — scheduler dispatches |
| Full PBDMA register dump | `channel.rs` | Working — 0x00-0x1FF scan |
| warm_and_test.sh | `scripts/` | Working — reliable warm boot |
| capture_nouveau_mmiotrace.sh | `scripts/` | Ready for dual Titan V |
| nouveau_reference_bar0.txt | `scripts/` | BAR0 reference captured |

---

## Nouveau Source References

| Function | File | What It Does |
|----------|------|-------------|
| `gk104_runl_commit` | `gk104.c` | Writes RUNLIST_BASE (0x2270) and RUNLIST (0x2274) |
| `gv100_runl_preempt` | `gv100.c` | Writes BIT(runl_id) to 0x002638 |
| `gk104_fifo_intr_runlist` | `gk104.c` | Reads 0x002A00, writes BIT(runl_id) to acknowledge |
| `gk104_runl_pending` | `gk104.c` | Reads 0x002284 + runl_id*8, checks bit 20 |
| `gk104_fifo_init` | `gk104.c` | Clears PFIFO interrupts (0x2100), enables (0x2140) |
| `gk104_fifo_init_pbdmas` | `gk104.c` | Writes PMC_DEVICE_ENABLE (0x204), PBDMA intr routing (0x2A04) |
| `gv100_chan_ramfc_write` | `gv100.c` | Writes all RAMFC fields to instance block |
| `gv100_ectx_bind` | `gv100.c` | Binds GR engine context at inst[0x210/0x214/0x0AC] |
| `gv100_runq_intr_1_ctxnotvalid` | `gv100.c` | Handles CTXNOTVALID (HCE INTR bit 31) |
| `gk104_runq_intr_0_names` | `gk104.c` | PBDMA INTR bit definitions (bit 31 = SIGNATURE) |
