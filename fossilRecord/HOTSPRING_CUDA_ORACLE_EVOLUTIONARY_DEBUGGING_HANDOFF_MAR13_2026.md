# hotSpring — CUDA-as-Oracle Evolutionary Debugging Strategy

**Source**: hotSpring substrate-level VFIO debugging on biomeGate
**Date**: March 13, 2026
**Hardware**: Titan V (GV100, SM70) at `0000:4b:00.0` + RTX 3090 (GA102) at `0000:21:00.0`
**Kernel**: 6.17.9-76061709-generic, `CONFIG_MMIOTRACE=y`
**Driver**: NVIDIA 580.126.18 (3090), vfio-pci (Titan V)
**coralReef**: Phase 10 Iteration 43+, all channel encoding fixes applied

---

## The Evolutionary Insight

We are now positioned to use CUDA as a **diagnostic oracle** — not a dependency,
not a crutch, but a calibration reference for our independent sovereign stack.

This was not possible as a one-shot. Here's the evolutionary sequence that
made it possible:

### Phase 1: Open Source as Primordial Substrate

We built the foundational understanding using open source:
- nouveau's open-gpu-doc → PFIFO, RAMFC, PCCSR, runlist format
- naga → WGSL → SPIR-V shader pipeline
- Linux DRM/VFIO → userspace GPU control

This gave us the **conceptual vocabulary**: what a channel IS, what a PDE
encodes, what a runlist contains. NVIDIA doesn't sell this understanding.
The open source community reverse-engineered it over decades.

### Phase 2: Rust Reimplementation as Fitness Test

By rebuilding every layer in pure Rust:
- coralReef: WGSL → native SASS compilation, DRM dispatch, V2 MMU
- barraCuda: precision strategy, DF64, shader math
- toadStool: device management, VFIO backend, hardware discovery

Each compilation error, each encoding bug, each `0xBAD0DA00` sentinel
taught us something. PDE encoding `addr >> 4` vs `addr >> 12 << 4`,
GPFIFO entry format, PMC engine enable after FLR — none of this is
documented anywhere. We found it by reasoning about the math and
comparing against nouveau register-by-register.

### Phase 3: CUDA as Calibration Reference (NOW)

Because we've done the independent work, we can now use CUDA's register
state as a validation oracle. We know WHAT to look for and WHY each
register matters. The NVIDIA driver becomes a reference measurement,
not a black box. We're reading its output like a scientist calibrating
their own instrument against a reference standard.

**Key distinction**: A dependency is "I need CUDA to run." What we have
is "I can read CUDA's register state to validate my own implementation,
because I already built it independently." The sovereign stack runs
without CUDA. CUDA is optional diagnostic tooling.

This is hardware atheism in practice: the math is the authority, not
the vendor. We can interrogate the vendor's implementation because we
understand the domain independently.

---

## BAR0 Reference Capture: What We Learned

### Attempt 1: 3090 (Ampere) BAR0 Comparison — FAILED (Informatively)

We wrote a BAR0 register probe (`scripts/read_bar0_regs.py`) and read
key PFIFO/PBDMA/PCCSR/USERMODE registers from both GPUs:

**RTX 3090 (nvidia driver loaded):**
```
PMC_ENABLE:                     0x52000000
PFIFO_PBDMA_MAP:               0xbadf1100  ← sentinel
PFIFO_INTR:                    0xbadf1100  ← sentinel
SCHED_EN:                      0xbadf1100  ← sentinel
PCCSR_INST[0]:                 0xbadf1100  ← sentinel
USERMODE_NOTIFY_CHAN_PENDING:   0xbadf1100  ← sentinel
```

**Result**: Almost ALL PFIFO/PBDMA/PCCSR registers read as `0xbadf1100`
or `0xbadf5040` — Ampere-specific sentinels for **GSP-managed domains**.

**Finding**: On Ampere (GA102+), the GPU System Processor firmware
manages all PFIFO/channel/PBDMA operations. The host CPU cannot read
these registers directly. The entire PFIFO subsystem is behind GSP.
This means:

1. We **cannot** learn Volta-specific PFIFO init from the 3090
2. The 3090's architecture is fundamentally different (GSP-based)
3. We need a **Volta reference** — i.e., the Titan V itself under nvidia

### Attempt 2: Titan V (VFIO) BAR0 from Python — FAILED (Expected)

```
All registers: 0xFFFFFFFF
```

Expected: VFIO-bound devices' BARs are only accessible through the
VFIO fd (mmap on the container), not via sysfs `resource0` from a
non-VFIO process.

### Correct Approach: Titan V Under nvidia Driver

Since the 3090 uses GSP and can't teach us about Volta PFIFO, we need
to bind the **Titan V itself** to the nvidia driver temporarily:

1. Unbind Titan V from vfio-pci
2. Bind to nvidia driver (same driver already loaded for 3090)
3. Read BAR0 registers → see a **healthy Volta** PFIFO state
4. Optionally: mmiotrace to capture the full init register sequence
5. Compare register-by-register against coralReef's VFIO init
6. Rebind to vfio-pci, apply fixes, validate

This gives us the **exact Volta register values** for a properly
initialized GV100 — same silicon, same architecture, different driver.

---

## Current FenceTimeout Diagnostics (Post All Fixes)

After applying all encoding corrections:
- PDE/PTE: `addr >> 4 | flags` (was `(addr >> 12) << 4 | flags`)
- GPFIFO entry: NVB06F format (`DW0 = VA[31:2] | TYPE, DW1 = VA[39:32] | LEN | SYNC`)
- PMC enable: `0xFFFFFFFF` to un-gate all clock domains
- PBDMA discovery: from `PBDMA_MAP` register (0x2004)
- Memory ordering: `write_volatile` + `SeqCst` fence before doorbell
- RUNQ: 0-based index into PBDMAs serving runlist 0

The test still fails with `FenceTimeout { ms: 5000 }`:

```
PMC_ENABLE:     0x5fecdff1      ← some engines didn't enable
SCHED_EN:       0xbad00200      ← SENTINEL — register may not exist on Volta!
SCHED_DISABLE:  0x00000000      ← scheduler enabled (correct)
PCCSR_INST[0]:  0xa0000003      ← instance block bound correctly
PCCSR_CHAN[0]:  0x11000001      ← channel enabled, bit28=1 (PBDMA_FAULTED?)
GP_GET:         0               ← GPU never processed any GPFIFO entry
GP_PUT:         1               ← host wrote 1 entry
PBDMA1_IDLE:    0x19821996      ← static — never changes across runs
DOORBELL_PROBE: 0x00000000      ← suspicious
MMU faults:     none
PBDMA interrupts: none
```

**Key observations:**
1. `SCHED_EN` (0x2504) reads as `0xbad00200` — this is a sentinel,
   meaning the register **does not exist on Volta**. Our write to it
   is silently dropped. Volta uses `SCHED_DISABLE` (0x2630) instead,
   which reads 0 (correct).
2. `PCCSR_CHAN[0]` bit 28 = 1 — may indicate PBDMA_FAULTED
3. PBDMA idle values are **static** across all test runs — they may
   be residual FLR state, not live PBDMA status
4. The PBDMA never wakes up to process GPFIFO entries

**Hypothesis**: After VFIO FLR, the GPU requires initialization beyond
what we've implemented. The PFIFO scheduler, PBDMA context loading,
and/or memory controller init may be missing. The nvidia driver
reference capture will reveal exactly which init steps we're missing.

---

## Dual-Use Architecture: toadStool GPU Mode Switching

The CUDA-as-oracle approach naturally extends into the dual-use
architecture — the same machine runs gaming AND science on the same GPU:

```
toadStool orchestrator
├─ toadstool gpu mode --device 4b:00.0 --mode science
│   → unbind nvidia → bind vfio-pci → coralReef sovereign dispatch
│   → QCD, molecular dynamics, physics validation
│
├─ toadstool gpu mode --device 4b:00.0 --mode gaming
│   → unbind vfio-pci → bind nvidia → Steam/Proton/Vulkan
│   → gaming, rendering, DLSS, ray tracing
│
└─ encrypted-at-rest via bearDog between mode switches
    → no MIG needed — software enclave at toadStool level
```

The rebind is two sysfs writes:
```bash
# Science → Gaming
echo 0000:4b:00.0 > /sys/bus/pci/drivers/vfio-pci/unbind
echo 0000:4b:00.0 > /sys/bus/pci/drivers/nvidia/bind

# Gaming → Science
echo 0000:4b:00.0 > /sys/bus/pci/drivers/nvidia/unbind
echo 0000:4b:00.0 > /sys/bus/pci/drivers/vfio-pci/bind
```

toadStool already has VFIO device management (Akida NPU pattern) and
tree-based process orchestration. Extending to GPU mode switching is
a natural evolution.

---

## Action Items

### Immediate: Reference Capture (hotSpring)

1. **Rebind Titan V to nvidia** — capture BAR0 register state of a
   healthy Volta GPU after full driver initialization
2. **Compare registers** — diff against coralReef's post-init state,
   identify every delta (PMC, PFIFO, PBDMA, PCCSR, USERMODE, MMU)
3. **Fix coralReef channel.rs** — add missing init steps based on delta
4. **Validate** — rebind to vfio-pci, run 7/7 VFIO tests
5. **(Optional) mmiotrace** — if register comparison isn't sufficient,
   capture the full nvidia driver init sequence via kernel mmiotrace.
   `CONFIG_MMIOTRACE=y` is already compiled in.

### Near-term: toadStool GPU Mode Manager

- Implement `toadstool gpu mode` CLI for gaming ↔ science switching
- Handle display server stop/start for display-attached GPUs
- Integrate bearDog encryption for at-rest GPU memory protection
- Support multi-GPU configurations (3090 gaming + Titan V science)

### Long-term: coralReef Rust Compiler Ingestion

Once VFIO dispatch works, the evolutionary path continues:
- coralReef ingests more of the init sequence into pure Rust
- Eventually: Rust compiler → GPU ISA (coralReef compiles Rust directly)
- Memory-safe shaders frontload an entire subclass of GPU bugs
- Hardware-atheistic: same math, any substrate

---

## Why This Matters

The evolutionary approach — open source → Rust → CUDA-as-oracle —
demonstrates that sovereign technology isn't built by avoiding existing
systems. It's built by **understanding them independently** and then
using them as validation references when needed.

The dual-use architecture means a researcher's gaming PC becomes a
scientific instrument between gaming sessions. toadStool manages the
lifecycle. coralReef provides the sovereign compute. barraCuda provides
the math. The hardware is fully utilized, not artificially segmented.

This is the same machine running Steam AND CERN-grade physics. No
special hardware. No vendor lock-in. Just math, Rust, and
well-understood silicon.

---

*From hotSpring substrate debugging, March 13, 2026.*
*"The math is the authority, not the vendor."*
