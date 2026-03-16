# GPU Sovereign Bring-Up Guide — Lessons from Volta VFIO

**Date**: March 15, 2026 (updated after mmiotrace session)
**Source**: hotSpring experiments 058–061, interpreter probe + mmiotrace
**Hardware**: 2× Titan V (GV100, SM70), RTX 5060 (GB206, SM120)
**Primals**: coralReef (driver), toadStool (hardware), barraCuda (dispatch)
**Chat**: [VFIO interpreter probe](28732f32-750e-4053-a1ae-a8d39a738d7a)

---

## Purpose

This document captures everything we've learned about bringing a GPU from
cold silicon to sovereign dispatch using pure Rust — no kernel driver, no
firmware blobs, no proprietary libraries. It's written for primals to evolve
against. The patterns are vendor-agnostic; the specifics are NVIDIA Volta.

---

## Part 1: What We Learned

### 1.1 GPU Power Is Active, Not Passive

A GPU is not a static peripheral. It actively manages its own power:

| Event | Time | Effect |
|-------|------|--------|
| Driver unbind | Immediate | PCIe runtime PM → D3hot (BAR0 → `0xFFFFFFFF`) |
| D3hot idle | ~2 seconds | Internal clock gating (PMC_ENABLE → `0x40000020`) |
| D3cold allowed | Variable | VRAM controller powered off (all VRAM → `0xBAD0ACxx`) |

**Implication**: Any VFIO operation on a cold GPU will fail silently — reads
return garbage, writes land nowhere. The GPU must be warmed before use.

### 1.2 The Five-Layer Warm-Up Sequence

We discovered that GPU bring-up requires five distinct layers, each depending
on the one below:

```
Layer 0: PCIe Power     — D3 → D0 via PMCSR config write
Layer 1: Engine Clocks  — PMC_ENABLE → 0xFFFFFFFF (glow plug)
Layer 2: BAR2 Aperture  — V2 MMU page table in VRAM, BAR2_BLOCK set
Layer 3: PFIFO/PBDMA    — interrupt enables, fault buffers, scheduler ready
Layer 4: Channel Load   — instance block, runlist, INST_BIND, context switch
```

Missing any layer causes failures at the layer above — but the errors look
like they belong to the upper layer. This is the core debugging challenge.

### 1.3 BAR2 Self-Warm Eliminates Nouveau Dependency

**Experiment 060 proved**: We can build a complete V2 MMU page table in VRAM
via PRAMIN (BAR0 window at `0x700000`) and program BAR2_BLOCK from pure Rust.
This achieves byte-identical results to nouveau warm-up:

- 12/54 experiments schedule (identical set)
- 0 faulted (identical)
- 3 expected CHSW failures (identical)

The glow plug sequence (PMC_ENABLE write + BAR2 page table setup) takes ~60ms
from cold and produces *cleaner* state than nouveau (no stale channel contexts).

### 1.4 Desktop Volta Has No PMU Firmware

NVIDIA does not ship signed PMU firmware for desktop Volta (Titan V).
Nouveau uses a stub. **All power management is pure BAR0 register writes**.
This is ideal for sovereign control — there is no firmware black box.

This is NOT true for Turing+ (T4, RTX 20xx, 30xx, 40xx, 50xx) which use GSP
(GPU System Processor) firmware. Each architecture era requires a different
bring-up strategy.

### 1.5 D3hot Does NOT Kill HBM2 Training (Corrected 2026-03-15)

**CRITICAL CORRECTION**: Our earlier conclusion was wrong. D3hot does NOT
erase HBM2 training. The memory controller state persists through D3hot —
BAR0 is simply disabled (reads return `0xFFFFFFFF`). Writing D0 to the PCI
PMCSR register immediately restores BAR0 access and **VRAM is alive**.

D3cold IS destructive — the VRAM controller loses power and HBM2 training
is lost (reads return `0xBAD0ACxx`). D3cold requires a full power cycle
(PCI remove → rescan) to trigger boot ROM devinit and retrain HBM2.

The earlier experiments showed VRAM errors because we were reading PRAMIN
while the GPU was in D3hot (BAR0 disabled). The `0xBAD0_ACxx` pattern was
a red herring from failed BAR0 reads, not actual VRAM state.

**The solution**: A single PCI config write restores full GPU functionality:
```
PMCSR[1:0] = 0b00  → D0 (BAR0 enabled, VRAM accessible)
```

`vfio-pci` unconditionally transitions to D3hot on bind, and `disable_idle_d3=Y` does
NOT prevent this.

**Current workaround**: Lock power state before VFIO bind:
```
echo on > /sys/bus/pci/devices/<BDF>/power/control
echo 0 > /sys/bus/pci/devices/<BDF>/d3cold_allowed
```
This is fragile — vfio-pci's `probe()` calls `pm_runtime_put()` which can
override the lock.

**Sovereign solution needed**: Rust-native HBM2 memory controller init. This
is the largest remaining gap (see Part 3).

### 1.6 mmiotrace Proves Nouveau Does NOT POST (Experiment 061)

Captured 206,375 MMIO operations during nouveau bind via Linux `mmiotrace`:
- **18,928 BAR0 writes**, 39,489 reads across 359 unique register offsets
- **Zero PMU FALCON writes** — nouveau does not upload firmware
- **Zero FBPA, LTC, PCLOCK, PMU writes** — no memory controller init
- **No devinit status reads** — nouveau doesn't even check if POST happened

Nouveau assumes UEFI already initialized the GPU. Its 18K writes are all
software setup: MMU page tables, interrupt routing, display init, channel
context. **Nouveau cannot POST a cold GPU.**

This explains why oracle register cloning failed (Experiment 061): the
registers we copied from nouveau's warm state were software config, not the
hardware POST sequence. HBM2 training lives below nouveau's layer.

### 1.7 VBIOS Init Scripts Are the Rosetta Stone

The VBIOS (read from GPU PROM at BAR0+0x300000) contains:
- **BIT 'I' init scripts** at offset 0x4934 (plaintext opcodes)
- **Boot scripts** at offset 0x76A2 (18,100 bytes, PMU-format opcodes)
- **Opcode table** at offset 0x48F4 (macro/function dispatch)
- **PMU DEVINIT firmware** — encrypted (hardware-decrypted by FALCON)

The PMU firmware is just an interpreter for the init scripts. The actual
register-write sequences for HBM2 training are encoded in the plaintext
scripts. ~50 opcodes documented in envytools and nouveau `init.c`.

Two paths to sovereign POST:
1. **FALCON upload**: Upload encrypted firmware to FALCON hardware, which
   decrypts and executes it. The FALCON then interprets the init scripts.
2. **Host-side interpreter**: Interpret the plaintext init scripts directly
   from Rust, bypassing the FALCON entirely. ~2000 lines of interpreter code.

### 1.8 The Interpreter Architecture Works

The 7-layer probe chain (L0 BAR → L1 Identity → L2 Power → L3 Engines →
L4 DMA → L5 Channel → L6 Dispatch) correctly identifies failure points
at each layer. Each layer produces typed evidence that the next layer
consumes. Rust's type system enforces layer dependencies at compile time.

Key architectural insight: **the same interpreter pattern applies to any
GPU vendor**. Layers 0–2 are nearly universal. Layers 3+ diverge per
architecture but the discovery protocol (probe → collect evidence → decide
next probe) is identical.

### 1.9 Specific Bugs Discovered

| Bug | Layer | Root Cause | Fix |
|-----|-------|------------|-----|
| PFIFO_ENABLE reads 0 | L2 | GV100 has no 0x2200 register; PFIFO via PMC bit 8 | Check PMC_ENABLE + PBDMA_MAP |
| BAR2_BLOCK invalid | L3 | Cold GPU has no page tables | Glow plug BAR2 self-warm |
| PBDMA-to-runlist mapping wrong | L3 | PBDMA_RUNL_MAP is a bitmask, not a direct ID | Check `mask & (1 << rl_id)` |
| Runlist register = RL0 not RL1 | L4 | Used gk104 global 0x2270, not GV100 per-RL 0x2280 | Per-runlist at stride 0x10 |
| Runlist submit encoding wrong | L4 | Used `(rl_id << 20) \| count` | Should be `(count << 16) \| upper_addr` |
| MMU fault buffer setup fails | L3 | Wrote to VRAM addresses, hardware expects different format | Use sysmem DMA buffers |
| PBDMA loads context, GP_GET stuck | L4 | Missing scheduler activation or MMU fault stall | Under investigation |
| PRAMIN VRAM returns 0xBAD0ACxx | L4 | D3cold powered off FB controller | Lock d3cold_allowed=0 |

---

## Part 2: Making the Matrix and Glow Plug More Robust

### 2.1 Interpreter Improvements Needed

**Fault buffer setup (critical)**: The current L3 fault buffer setup writes
to VRAM via PRAMIN but the registers reject the values. The diagnostic runner
(`runner.rs`) uses system memory DMA buffers — this is the correct approach.
Both replayable (BUF0) and non-replayable (BUF1) fault buffers should be
DMA-allocated and configured before any scheduler operation.

**Runlist submission (critical)**: Two bugs compound:
1. GV100 uses per-runlist registers at `0x2270 + rl_id * 0x10`, not global
2. Submit value is `upper_32_bits(addr >> 12) | (count << 16)`, not `(rl_id << 20) | count`

The interpreter should try both RL0 and RL1 submission to discover which
runlist the GR PBDMA actually services.

**PBDMA diagnostic expansion**: When direct PBDMA programming loads context
but GP_GET doesn't advance, the interpreter should:
1. Read `PBDMA_STATUS` (offset 0x118) and decode all fields
2. Read `PBDMA_METHOD0` (0x1C0) for faulted method address
3. Read `PBDMA_GP_STATE` (0x04C) for fetch state
4. Read MMU `FAULT_STATUS` (0x100A2C) for translation faults
5. Try a PBDMA reset (clear + re-enable) after context load

**Multi-PBDMA sweep**: Instead of only testing `gr_pbdma`, try all active
PBDMAs. Some PBDMAs may be functional while others are faulted from stale state.

### 2.2 Glow Plug Improvements

**Warmth sentinel**: Add continuous monitoring of GPU temperature and
PMC_ENABLE. If the GPU cools (PMC_ENABLE reverts to `0x40000020`), re-warm
automatically. The vfio-pci driver's device release sequence can restore
cold-boot PCI config defaults, silently undoing our warm-up.

**Idempotent warm-up**: The glow plug should be safe to call at any point.
If the GPU is already warm, it should detect this and skip. If partially
warm (e.g., PMC enabled but BAR2 invalid), it should only fix the missing
layers.

**Power state classification**: Before any operation, classify the GPU:
```
fn classify_gpu_state(bar0: &MappedBar) -> GpuState {
    let boot0 = bar0.read_u32(0x000).unwrap_or(0);
    let pmc = bar0.read_u32(0x200).unwrap_or(0);
    let bar2 = bar0.read_u32(0x1714).unwrap_or(0);
    let pbdma_map = bar0.read_u32(0x2004).unwrap_or(0);

    match (boot0, pmc, bar2, pbdma_map) {
        (0xFFFFFFFF, _, _, _) => GpuState::D3Hot,
        (0, _, _, _)         => GpuState::PoweredOff,
        (_, p, _, _) if p == 0x40000020 => GpuState::ClockGated,
        (_, _, b, _) if b == 0x40000000 || b == 0 => GpuState::NeedBAR2,
        (_, _, _, m) if m == 0 || m == 0xBAD0DA00 => GpuState::NeedPFIFO,
        _ => GpuState::Warm,
    }
}
```

### 2.3 Vendor-Agnostic Architecture

The interpreter's layer structure is naturally vendor-agnostic:

| Layer | NVIDIA Volta | AMD RDNA | Intel Arc |
|-------|-------------|----------|-----------|
| L0 BAR | BAR0 MMIO | BAR0 MMIO | BAR0 MMIO |
| L1 Identity | PMC_BOOT_0 | ASIC_ID | PCI Device ID |
| L2 Power | PMC_ENABLE | MMHUB | GT_SLICE |
| L3 Engines | PBDMA_MAP, PTOP | SDMA, MEC | BCS, RCS |
| L4 DMA | VFIO IOMMU | VFIO IOMMU | VFIO IOMMU |
| L5 Channel | PFIFO/PCCSR | MES/HQD | ExecList |
| L6 Dispatch | GPFIFO | PM4 ring | MI commands |

**The VFIO IOMMU layer (L4) is truly universal** — every PCIe GPU goes
through the same IOMMU mapping. L0–L2 are 80% identical across vendors.
L3+ diverges significantly but follows the same probe→evidence→decide pattern.

To make the interpreter multi-vendor:
1. Parameterize register offsets via a `GpuRegisterMap` trait
2. Make layer types generic: `EngineTopology<V: Vendor>`
3. Keep the probe chain logic in a generic `ProbeInterpreter<V>`
4. Vendor-specific register maps discovered at L1 (after identity)

### 2.4 Dynamic Programming for Reverse Engineering

The interpreter embodies a dynamic programming approach to reverse engineering:
- **Each failure** narrows the search space (e.g., "sysmem bind works but VRAM doesn't")
- **Each success** unlocks the next layer of probing
- **Evidence accumulates** across runs — the ProbeReport is a fossil record

To strengthen this:
1. **Persist ProbeReports** to disk (JSON) between runs
2. **Diff reports** across GPU models to identify architecture-specific behavior
3. **Auto-expand** the test matrix when a layer partially succeeds (e.g., if
   INST_BIND works for VRAM but not sysmem, probe all target encodings)
4. **Regression detection** — if a layer that previously passed now fails,
   flag it as a GPU state regression (likely power/thermal)

---

## Part 3: What's Missing for Sovereign GPU Management

### 3.1 The Full Bring-Up Stack

For coralReef's compile system to dispatch compute shaders on a cold GPU
without any kernel driver assistance, these capabilities must exist in Rust:

```
┌─────────────────────────────────────────────┐
│ Dispatch (coral compile → GPU execution)     │ ← L6: GPFIFO consumption
├─────────────────────────────────────────────┤
│ Channel lifecycle (create/bind/schedule)     │ ← L5: scheduler activation
├─────────────────────────────────────────────┤
│ MMU configuration (fault buffers, TLB)       │ ← L3-L4: page tables + faults
├─────────────────────────────────────────────┤
│ PFIFO/PBDMA initialization                   │ ← L3: interrupts, PBDMA map
├─────────────────────────────────────────────┤
│ BAR2 aperture (V2 page table in VRAM)        │ ✅ DONE (glow plug)
├─────────────────────────────────────────────┤
│ Engine clock domains (PMC_ENABLE)            │ ✅ DONE (glow plug)
├─────────────────────────────────────────────┤
│ PCIe power (D3 → D0)                        │ ✅ DONE (PMCSR write)
├─────────────────────────────────────────────┤
│ Framebuffer/VRAM controller (HBM2 init)      │ ❌ MISSING (relies on nouveau)
└─────────────────────────────────────────────┘
```

### 3.2 Gap Analysis

#### Gap 1: HBM2/Framebuffer Controller Init — **SOLVED** (2026-03-15)

**Status**: RESOLVED. HBM2 training survives D3hot. D0 force via PMCSR = fix.

**Corrected root cause**: vfio-pci bind → D3hot disables BAR0 access, but
HBM2 training is NOT lost. The `0xBAD0_ACxx` errors we saw were from reading
BAR0 while the device was in D3hot (BAR0 disabled), not from actual VRAM
state. Writing D0 to PMCSR restores BAR0 access and VRAM is immediately alive.

**What we tried** (Experiment 061):
- Oracle register cloning (1529 regs): Misdiagnosis — was writing to D3hot card
- PCIe SBR: Resets device but doesn't re-execute boot ROM devinit
- mmiotrace of nouveau: Confirmed nouveau doesn't POST — relies on UEFI
- D3cold power cycle (PCI remove/rescan): **Works** — boot ROM re-trains HBM2
- **D0 force via PMCSR**: **THE SOLUTION** — single config write restores all

**Solution implemented in coral-driver**:

```rust
devinit::force_pci_d0(bdf)  // Write PMCSR[1:0]=00 → D0
```

Called automatically in `RawVfioDevice::open()` before VFIO device setup.
GlowPlug also handles D3Hot state with automatic D0 force.

**Full pipeline verified**: bind vfio-pci → force D0 → VFIO open → GlowPlug
warm → BAR2 configured → Warm state → Ready for dispatch.

**Fallback paths** (for true HBM2 loss after D3cold):

1. **D3cold power cycle**: PCI remove → rescan → boot ROM re-POSTs
2. **VBIOS script writes**: 577 register writes extracted from boot scripts
   (237 HBM2-critical across FBPA/CLK/PCLOCK/LTC)
3. **Oracle register clone**: Copy from warm card of same model
4. **PMU FALCON upload**: Encrypted firmware — blocked on Volta, may work
   on Maxwell/Pascal

**Long term**: The VBIOS script scanner generalizes across GPU models and
vendors. The D0 force approach works for any PCI device with PM capability.

#### Gap 2: MMU Fault Buffer Configuration (HIGH)

**Status**: Partially implemented, not working correctly.

The PFIFO scheduler requires functional MMU fault buffers before it will
schedule channels. Without them, any MMU fault during context load causes
a silent stall. The registers at `0x100E24+` need:
- System memory DMA buffers (not VRAM)
- Correct aperture encoding in low register bits
- Enable bit in the HI register or PUT register

The diagnostic runner (`runner.rs`) has a partially working implementation.
The interpreter (`probe.rs`) L3 setup fails because it uses VRAM addresses.

#### Gap 3: Correct Runlist Submission (HIGH)

**Status**: Buggy — uses wrong registers and wrong encoding.

GV100 runlist submission is per-runlist at stride 0x10:
```
BASE  = 0x2270 + runlist_id * 0x10   ← lower_32(vram_addr >> 12)
SUBMIT = 0x2274 + runlist_id * 0x10  ← upper_32(vram_addr >> 12) | (entry_count << 16)
```

Current code uses RL0's registers (0x2270/0x2274) even for RL1, and encodes
the submit value incorrectly.

#### Gap 4: PBDMA Activation After Context Load (HIGH)

**Status**: Under investigation.

Direct PBDMA programming (Attempt F) loads our RAMFC context — SIGNATURE,
GP_BASE, USERD all read back correctly. But GP_GET stays 0 despite GP_PUT=1.
The PBDMA is stalled.

Hypotheses:
1. MMU translation fault when PBDMA tries to read GPFIFO at GPU VA 0x1000
   (no fault buffer to report it → silent stall)
2. PBDMA needs an explicit "start fetch" kick after manual context load
3. The channel isn't in the correct state for the PBDMA to begin fetching

The fix for Gap 2 (fault buffers) may resolve this — once the MMU can report
faults, either the fetch will succeed or we'll see the specific fault.

#### Gap 5: Channel Context Lifecycle (MEDIUM)

**Status**: Not implemented.

For multi-channel or long-running dispatch, the driver needs:
- Context save (PBDMA → RAMFC writeback) before channel switch
- Context restore (RAMFC → PBDMA) on channel resume
- Preemption support (GV100 uses TSG-level preempt at 0x2638)
- Error recovery after PBDMA or engine faults

#### Gap 6: Clock/Power Domain Management (LOW)

**Status**: Designed, not implemented.

The five-state power model (Sovereign/Warm/Glow/Sleep/Off) is designed but
only Glow→Warm (PMC_ENABLE write) is implemented. Missing:
- Warm→Sovereign (channel pre-load)
- Warm→Glow (selective engine gating)
- Glow→Sleep (D3hot transition)
- Bus-level clock gating (0x1C00 — untapped by nouveau)
- Fine-grained per-engine control (GR vs CE vs NVDEC)

#### Gap 7: Multi-Architecture Abstraction (MEDIUM)

**Status**: Volta-only.

The interpreter and glow plug are hardcoded for GV100. To support:
- **Pascal (GP100)**: Similar PFIFO, different runlist format
- **Turing (TU102)**: GSP firmware required, different scheduler
- **Ampere (GA102)**: GSP + different channel format
- **RDNA2/3 (AMD)**: Completely different engine topology (SDMA, MEC, PM4)

The layered interpreter architecture supports this — but register maps,
runlist formats, and scheduler protocols need per-architecture implementations.

### 3.3 Priority Order for Sovereign Dispatch

1. ~~**FB controller / HBM2 init**~~ (Gap 1) — **SOLVED**. D0 force via PMCSR
   restores VRAM after vfio-pci bind. No VBIOS scripts or FALCON needed for
   normal operation. VBIOS scripts retained as fallback for D3cold recovery.
2. **Fix runlist submission** (Gap 3) — correct registers + encoding
3. **Fix MMU fault buffers** (Gap 2) — system memory DMA + proper config
4. **Verify GP_GET advances** (Gap 4) — with 2+3 fixed, re-test
5. **Implement NOP dispatch** (L6) — submit a real GPFIFO entry with NOP methods
6. **Implement compute dispatch** — QMD submission for actual shader execution
7. **Multi-arch** (Gap 7) — generalize for RTX 5060 and AMD MI50

### 3.4 Tools Proven

| Tool | Purpose | Status |
|------|---------|--------|
| mmiotrace | Capture driver MMIO sequences | Proven (206K ops captured) |
| VBIOS PROM reader | Read VBIOS from BAR0+0x300000 | Working |
| BIT table parser | Find init scripts/PMU firmware | Working |
| Oracle register diff | Compare warm vs cold state | Working (but insufficient alone) |
| Diagnostic matrix | Automated multi-config testing | Working (54 experiments) |
| BAR2 glow plug | Self-warm from cold | Working (nouveau parity) |

**Important**: Save mmiotrace data to persistent storage (`hotSpring/data/`),
not `/tmp/`. Reboot wipes all `/tmp/` data. Lost 206K-line capture this way.

---

## Part 4: Register Quick Reference

### Power Management
| Register | Offset | Cold | Warm | Write |
|----------|--------|------|------|-------|
| PMC_ENABLE | 0x0200 | 0x40000020 | 0x5fecdff1 | 0xFFFFFFFF |
| PFIFO_ENABLE | 0x2200 | 0xBAD0DA00 | N/A (GV100) | N/A |
| GPU_TEMP | 0x20460 | ~38°C | ~46°C | R/O |

### PFIFO/Scheduler
| Register | Offset | Purpose |
|----------|--------|---------|
| PBDMA_MAP | 0x2004 | Active PBDMAs (bitmask) |
| PFIFO_INTR | 0x2100 | Interrupt status |
| PFIFO_INTR_EN | 0x2140 | Interrupt enable mask |
| RL_BASE(id) | 0x2270+id×0x10 | Runlist base address |
| RL_SUBMIT(id) | 0x2274+id×0x10 | Runlist submit trigger |
| SCHED_DISABLE | 0x2630 | Scheduler disable (0=run) |

### BAR Aperture
| Register | Offset | Purpose |
|----------|--------|---------|
| BAR0_WINDOW | 0x1700 | PRAMIN window steering |
| BAR1_BLOCK | 0x1704 | BAR1 instance block pointer |
| BIND_STATUS | 0x1710 | BAR1/BAR2 bind pending |
| BAR2_BLOCK | 0x1714 | BAR2 instance block pointer |

### MMU Fault Buffers
| Register | Offset | Purpose |
|----------|--------|---------|
| FAULT_BUF0_LO | 0x100E24 | Replayable fault buffer addr |
| FAULT_BUF0_HI | 0x100E28 | Replayable fault buffer hi/enable |
| FAULT_BUF1_LO | 0x100E44 | Non-replayable fault buffer addr |
| FAULT_BUF1_HI | 0x100E48 | Non-replayable fault buffer hi/enable |
| FAULT_STATUS | 0x100A2C | Current fault status |

### Channel Control (PCCSR)
| Register | Offset | Purpose |
|----------|--------|---------|
| INST(id) | 0x800000+id×8 | Instance block pointer + INST_BIND |
| CHANNEL(id) | 0x800004+id×8 | Enable/status/fault bits |

### Doorbell
| Register | Offset | Purpose |
|----------|--------|---------|
| NOTIFY_CHANNEL_PENDING | 0x810090 | Write channel_id to wake scheduler |

---

## Part 5: Evolution Guidance for Primals

### For toadStool
- **Absorb the glow plug** into `nvpmu` as `GpuPowerController`
- **Implement `PowerManager`** with the five-state model
- **Build hardware learning** around the interpreter's ProbeReport — each
  GPU model's working configuration becomes a learned profile
- **FB controller init** is your highest-value contribution — this is what
  breaks full sovereignty

### For barraCuda
- **Dispatch pre-warm hint**: Signal coralReef/toadStool to warm before batch
- **Power-aware scheduling**: Prefer warm GPUs in multi-GPU configs
- **Architecture-aware dispatch**: Use interpreter's GpuIdentity to select
  the correct ISA target (SM70 vs SM86 vs RDNA2)

### For coralReef
- **Fix the three critical bugs** (runlist, fault buffers, PBDMA activation)
- **Extract glow plug** into a reusable `fn glow_plug(bar0: &MappedBar)`
- **Persist ProbeReports** for cross-GPU comparison
- **Integrate with toadStool's PowerManager** when available

### For All Primals
- The interpreter is a **universal GPU diagnostic tool** — it should evolve
  to support AMD, Intel, and future architectures
- Each layer's types form a **vocabulary** that primals share: `BarTopology`,
  `GpuIdentity`, `PowerState`, `EngineTopology` are not NVIDIA-specific
- The probe→evidence→decide pattern is **dynamic programming for hardware**:
  optimal substructure (each layer depends only on the layer below) and
  overlapping subproblems (same probes reused across GPU models)

---

## Part 6: GlowPlug Metal Explorer — Vendor-Agnostic GPU Capability Discovery

**Added**: March 15, 2026

### 6.1 Architecture

The GlowPlug and diagnostic matrix have evolved from NVIDIA-specific warm-up
tooling into a vendor-agnostic GPU metal capability exploration system:

```
Layer 0: PCI Discovery     — pci_discovery.rs (any PCI device)
Layer 1: BAR Cartography   — bar_cartography.rs (register space scan)
Layer 2: Power Domain Map  — gpu_vendor.rs GpuMetal trait
Layer 3: Memory Topology   — memory.rs MemoryTopology
Layer 4: Engine Discovery  — nv_metal.rs / amd_metal.rs
Layer 5: Metal Capabilities — cartography + differential probing
```

### 6.2 New Modules

| Module | Purpose |
|--------|---------|
| `pci_discovery.rs` | Vendor-agnostic PCI config parsing, PM control, BAR enumeration, capability chain walk |
| `bar_cartography.rs` | Systematic BAR0 register space scanner with RO/RW/WO/Trigger/Dead classification |
| `gpu_vendor.rs` | `GpuMetal` trait: identity, power_domains, memory_regions, engine_list, warmup_sequence |
| `nv_metal.rs` | NVIDIA Volta implementation of `GpuMetal` with domain hints and warmup steps |
| `amd_metal.rs` | AMD Vega/MI50 stub — ready for hardware when it arrives |

### 6.3 Key Capabilities

- **`force_pci_d0()`** moved to `pci_discovery.rs` — works on ANY PCI device
- **`GlowPlug.with_metal()`** — accepts a `Box<dyn GpuMetal>` for vendor-agnostic warm-up
- **`GlowPlug.probe_bounds()`** — empirically maps what state survives each power transition
- **BAR0 cartography** — scans register space, groups into domains, classifies access patterns
- **Metal discovery experiments** — `PowerStateSweep`, `RegisterCartography`, `MemoryPathMatrix`, `ClockDomainSweep`, `EngineProbe`
- **JSON persistence** — scan results saved to `hotSpring/data/metal_maps/` for cross-card comparison

### 6.4 Running the Metal Explorer

```bash
# Full BAR0 cartography on a VFIO-bound GPU
CORALREEF_VFIO_BDF=0000:4a:00.0 cargo test --test hw_nv_vfio --features vfio \
  -- --ignored vfio_metal_cartography --nocapture

# PCI device discovery (no VFIO required)
CORALREEF_VFIO_BDF=0000:4a:00.0 cargo test --test hw_nv_vfio --features vfio \
  -- --ignored vfio_pci_discovery --nocapture

# Power bounds probing (D3hot survival, clock gating)
CORALREEF_VFIO_BDF=0000:4a:00.0 cargo test --test hw_nv_vfio --features vfio \
  -- --ignored vfio_power_bounds --nocapture
```

### 6.5 Cross-Card Comparison Strategy

When the MI50 cards arrive:
1. Run `vfio_metal_cartography` on each card
2. Compare JSON outputs in `hotSpring/data/metal_maps/`
3. Shared patterns (PCI PM, BAR layout) confirm vendor-agnostic code
4. Divergent patterns (register offsets, engine topology) guide `AmdVegaMetal` implementation
5. Undocumented responsive registers → candidates for unadvertised capabilities

---

## Part 7: Volta Secure Boot Barrier (March 15, 2026 — PCLOCK Deep Probe)

### 7.1 The Problem: Clock Gates Block Host-Side Initialization

After implementing PRI bus backpressure monitoring and progressive domain enable,
we performed a deep probe of the entire PCLOCK register range (0x130000–0x138000)
on the Titan V. The results reveal a **fundamental architectural barrier**:

| Domain | PRI Error | Meaning | Registers Affected |
|--------|-----------|---------|-------------------|
| PCLOCK sub-block | `0xBADF5040` | PLL not locked | 1,765 registers |
| LTC / FBPA0 | `0xBADF3000` | Hub-level clock gate | 2,560 registers |
| FBPA2 / FBPA3 | `0xBADF1100` | BLCG/SLCG power gate | 3,584 registers |
| PBUS | `0xBAD00200` | PRI timeout | Entire domain |

The PLL configuration registers (0x137000–0x13701F) are **behind the PLL's own
clock gate**. To configure the PLL, you need the PLL to already be running. This
chicken-and-egg problem is normally solved by the **PMU FALCON** — it has a
separate internal bus that bypasses the PRIV ring clock gate enforcement.

### 7.2 What IS Accessible

Despite the barrier, 283 registers in the PCLOCK range ARE readable:

| Range | Count | Purpose |
|-------|-------|---------|
| 0x136200–0x136E84 | ~200 | Root PLL configurations (always-on domain) |
| 0x137020 | 1 | PCLOCK bypass control (writable) |
| 0x137050 | 1 | NVPLL control (writable, changed 0x08→0x09) |
| 0x137100 | 1 | MEMPLL control (writes accepted, reads back 0) |
| 0x137400–0x1374F8 | ~20 | Additional config registers |
| 0x137620–0x137670 | ~15 | Status/counter registers |
| 0x137C00–0x137F44 | ~15 | High-end config (incl. 0x137C10=0x00031031) |

The root PLLs at 0x136xxx show a repeating pattern at stride 0x200 with
coefficient values like `0x026F0002` — these are PLL M/N dividers in an
always-on power domain. They provide reference clocks to downstream PLLs.

### 7.3 PTHERM Clock Gating Is Writeable

The PTHERM clock gating registers (0x020200–0x020208) were successfully
disabled (0x22580044 → 0x00000000), but this had **no effect** on domain
health. The gating is enforced at the PRIV ring level, not at PTHERM.

### 7.4 Oracle Strategy

Since host-side PLL programming is blocked by secure boot, the most practical
path to sovereign VRAM access is the **oracle differential**:

1. **Next reboot**: Bind only ONE Titan V to `vfio-pci`; let `nouveau` claim the other
2. **Capture**: Read all BAR0 registers from the nouveau-warm card via sysfs
3. **Replay**: Apply the warm register state to the cold VFIO card via GlowPlug
4. **Verify**: Check which domain transitions unlock VRAM
5. **Distill**: Identify the minimal register sequence for sovereign bring-up

The existing `differential_training()` and `apply_oracle_registers()` functions
in GlowPlug are ready for this. The PCLOCK registers that ARE accessible
(0x137020, 0x137050, 0x137100) may be the key — their correct values from the
oracle could program enough of the clock tree to bring PLLs alive.

### 7.5 Implications for AMD MI50

The MI50 uses HBM2 but with AMD's GFX9 architecture, which has a different
clock/power management model. AMD's open-source amdgpu driver provides
complete register documentation, so the MI50 may not have the same secure
boot barrier. This makes the MI50 a potentially easier target for fully
sovereign HBM2 access.

### 7.6 Rust Advantage for Sovereign Memory

Once we achieve VRAM access (via oracle or MI50), the Rust type system
provides unique advantages for memory management:

- **Typestate pattern**: Compile-time enforcement of HBM2 training phases
  (Untrained → PhyEnabled → LinksTrained → DramReady → Verified)
- **Newtype wrappers**: `FbpaOffset(usize)`, `PfbOffset(usize)` prevent
  writing to wrong register domains
- **Ownership model**: Exclusive `&mut` access prevents concurrent
  register access races that plague C implementations
- **PRI bus monitor**: Transparent fault detection on every MMIO access,
  impossible in C without manual checks at every call site

---

## Part 8: D3hot→D0 VRAM Breakthrough and Sovereign Boot Architecture

**Date**: March 16, 2026

### 8.1 The Breakthrough

BIOS POST trains HBM2 at system boot. The training survives PCIe D3hot
(sleep state). vfio-pci puts GPUs in D3hot, making them look dead, but
a single sysfs write restores everything:

```bash
echo "on" > /sys/bus/pci/devices/BDF/power/control
```

Result: full 12GB HBM2 read/write, 15/18 domains alive, VBIOS readable,
all from pure Rust via VFIO. **24 of 26 hardware tests pass.**

### 8.2 The Fragility

VFIO close triggers a PM reset that destroys HBM2 training on GV100.
The card has no FLR support (`FLReset-`) and the PM D3 cycle wipes the
memory controller state. Only a system reboot restores it.

### 8.3 Sovereign Boot Architecture

The solution: a persistent driver that owns the GPU from boot to shutdown.

**Phase 1 — GlowPlug Daemon** (works today):
- systemd service starts at boot
- Binds GPU to vfio-pci, opens VFIO device, forces D0
- Holds fd open forever (VFIO never closes → HBM2 never dies)
- Exposes Unix socket for toadStool (fd passing via SCM_RIGHTS)

**Phase 2 — Sovereign Kernel Module** (coral-kmod):
- Minimal PCI driver that replaces vfio-pci
- NO device reset on fd close (preserves HBM2)
- Exposes /dev/coral0 for direct userspace access
- GPU-aware power management (D3hot only when safe)

**Phase 3 — Sovereign HBM2 Training** (full independence):
- Trains HBM2 from cold silicon in pure Rust
- No dependency on vendor BIOS or firmware
- Uses oracle data + JEDEC JESD235 standard
- Enables post-FLR recovery and suspend/resume

### 8.4 The Handoff Pattern

```
coral-kmod / glowplug daemon
  │  owns GPU from boot
  │  preserves HBM2 training
  │  manages power states
  │
  ├──→ toadStool (receives warm GPU via fd passing / /dev/coral0)
  │      │  dispatches compute work
  │      │  never worries about init
  │      │
  │      ├──→ hotSpring (MD simulations)
  │      ├──→ wetSpring (genomics)
  │      ├──→ neuralSpring (ML)
  │      └──→ airSpring (weather)
  │
  └──→ GlowPlug health monitor (periodic VRAM check, power watchdog)
```

### 8.5 GlowPlug as PCIe Device Broker

The architecture evolves further: GlowPlug becomes a **device lifecycle
broker** that manages hot-swap between driver personalities (VFIO, nouveau,
CUDA, amdgpu) while preserving hardware state. Key capabilities:

- **Hot-swap protocol**: snapshot → quiesce → unbind → bind → verify
- **State vault**: register snapshots compressed against oracle baseline
- **Personality system**: each driver backend is a loadable personality
- **toadStool integration**: toadStool asks "give me a device that can do X"
  and GlowPlug handles the hardware details
- **PCIe transfer coordination**: GPU↔GPU P2P, DMA-buf sharing, topology

This makes toadStool fully hardware-agnostic. Adding a new GPU vendor
means adding a new Personality variant, not rewriting dispatch logic.

See: `hotSpring/experiments/062_VFIO_D3HOT_VRAM_BREAKTHROUGH.md`
See: `hotSpring/experiments/063_SOVEREIGN_BOOT_DRIVER_ARCHITECTURE.md`
See: `hotSpring/experiments/064_GLOWPLUG_DEVICE_BROKER_ARCHITECTURE.md`

---

*March 15, 2026 — Layer by layer, from cold silicon to sovereign dispatch.*
*Updated: mmiotrace confirms nouveau never POSTs. VBIOS scripts are the path.*
*Updated: GlowPlug Metal Explorer — vendor-agnostic GPU capability discovery.*
*Updated: PCLOCK deep probe reveals Volta secure boot barrier. Oracle strategy is the path forward.*
*Updated: D3hot→D0 breakthrough — VRAM alive without any driver. Sovereign boot architecture planned.*
