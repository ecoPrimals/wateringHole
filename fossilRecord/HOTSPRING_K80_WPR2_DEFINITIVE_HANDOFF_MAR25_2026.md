# hotSpring → Ecosystem Handoff: K80 Strategy + WPR2 Definitive Root Cause

**Date:** March 25, 2026
**From:** hotSpring (GPU cracking laboratory)
**To:** coralReef, toadStool, barraCuda, all springs
**Experiments:** 110-123 (consolidation matrix → K80 sovereign compute)
**License:** AGPL-3.0-only

---

## Executive Summary

After 123 experiments on the Titan V (GV100), we have a **definitive root cause** for the sovereign compute blocker on Volta: WPR2 hardware protection is fundamentally inaccessible from the host. A Tesla K80 (Kepler, zero firmware security) is arriving 2026-03-26 to validate the entire pipeline without security barriers.

---

## What Changed Since Last Handoff

### 1. Exp 110: Consolidation Matrix (Definitive HS Truth Table)
12-combination sweep of 6 ACR boot variables. **PDE slot position is the SOLE determinant of HS mode.** All other variables (VRAM PTEs, bind target, blob_size, IMEM preload, TLB flush) have zero effect. This eliminated the entire Exp 095-109 search space.

### 2. Exp 112: HS Mode Achieved (Dual-Phase Boot)
First sovereign HS mode entry (SCTL=0x3002) with zero MMU faults. Legacy PDEs → HS auth via physical fallback → immediate PDE hot-swap to correct virtual. Firmware TRAPs (cause=0x20) during DMA — PMU dependency (Exp 113).

### 3. Exp 114-121: WPR Copy Stall Investigation
Seven experiments probing the persistent WPR copy stall from multiple angles:
- LS mailbox path (Exp 114): BOOTSTRAP_FALCON acknowledged, FECS/GPCCS stuck
- Direct PIO (Exp 115): Hardware security enforcement on GV100
- blob_size=0 from firmware binary (Exp 116): ACR doesn't process WPR
- WPR2 valid during nouveau at 12GB VRAM (Exp 117), destroyed on swap (Exp 118)
- Cold boot WPR2 invalid (Exp 119), sovereign DEVINIT not needed (Exp 120)
- Minimal ACR same stall (Exp 121) — ruled out PRI ring interference

### 4. Exp 122: WPR2 Resolution (Definitive Root Cause)
Three-pronged attack:
- **122A:** ALL WPR2 registers hardware-locked. Host cannot write.
- **122B:** WPR2 at ~12GB VRAM (top of memory). FBPA partitions offline.
- **122C:** FWSEC not in accessible VBIOS PROM. Loaded by GPU internal ROM.

**Root cause chain:** FWSEC (inaccessible) → WPR2 (12GB) → driver swap (destroys) → FBPA (offline) → ACR firmware cannot write to WPR2 region → copy stall.

### 5. K80 Strategy (Exp 123-K)
Tesla K80 (GK210, Kepler, PCI 10de:102d):
- **Zero firmware security** — no FWSEC, no WPR2, no ACR, no signed firmware
- FECS/GPCCS load via direct PIO IMEM/DMEM upload
- Validates L1-L9 + L11 without L10 security barriers
- If K80 sovereign compute works → Titan V problem is precisely L10 only

### 6. RTX 5070 Discovery
Parasitic probe revealed the "RTX 5060" is actually a **GB206 (RTX 5070)**, confirmed via BOOT0=0x1b6000a1 (chipset 0x1B6, SM 120, Blackwell).

---

## Impact on Each Primal

### coralReef
**New modules built:**
- `nv::kepler_falcon` — Falcon v1 PIO upload protocol (IMEM/DMEM/start) with mock-tested upload sequences
- `nv::identity` — Kepler support added: SM 35-37, PCI 0x102D, BOOT0 0x0F0-0xFF, compute class 0xA1C0
- `exp123t_parasitic_probe` — sysfs BAR0 probe that works with ANY driver binding

**Code ready for K80 arrival:** identity module recognizes GK210, PIO loader tested, probe binary compiled.

**Titan V next steps:** Parasitic compute (sysfs BAR0 while nouveau active) deferred to after K80 validates the compute dispatch path. FBPA initialization NOT the issue (nouveau's GV100 FB hook is `gm200_fb_init`, just MMU buffer setup — no "enable FBPA" sequence exists).

### toadStool
- K80 will appear as two PCI devices (dual-GPU). PcieTransport should handle both.
- New GPU personality: Kepler compute (0xA1C0). Channel class: 0xA16F.
- ResourceOrchestrator: K80 GPUs have 12GB GDDR5 each (NOT HBM2). Different memory bandwidth profile.

### barraCuda
- K80 compute capability 3.7 — supports most WGSL operations but:
  - No native f64 atomics (use CAS loop)
  - Shared memory limited to 48KB per SM (vs 96KB on Volta)
  - 2496 CUDA cores per die × 2 dies = 4992 total cores
- First target: simple compute dispatch (atomic add kernel)
- DF64 should work identically (f32-pair arithmetic)

### All Springs
The K80 validation means sovereign compute for science workloads becomes possible on pre-Maxwell GPUs — these are cheap and abundant on the used market. A fleet of K80s at ~$50 each could provide ~5 TFLOPS f64 for lattice QCD.

---

## Primal Evolution Notes

### Naming Convention
- K80 experiments use `123-K` prefix (GPU-specific sub-experiment numbering)
- Titan V parasitic uses `123-T` prefix
- Future GPU-specific experiments: `NNN-{gpu_code}` (e.g., `124-K`, `124-T`)

### Identity Module Pattern
The `nv::identity` module is now the authoritative GPU identity source:
- `boot0_to_sm()`: Hardware BOOT0 → SM version (covers Kepler through Blackwell)
- `chipset_variant()`: Finer-grained chip identification
- `sm_to_compute_class()`: SM → compute engine class
- `nvidia_sm()`: PCI device ID → SM version
New GPUs: add to these four functions. Single source of truth.

### RegisterAccess Trait Pattern
The `RegisterAccess` trait (read_u32/write_u32) is the universal hardware access abstraction. Both `Bar0Access` (sysfs) and `MappedBar` (VFIO) implement it. The new `kepler_falcon` module uses `dyn RegisterAccess` — it works with any backend. This pattern should be followed by all new hardware interaction code.

---

## Closed Approaches (Fossil Record)

| Approach | Experiment | Result |
|----------|-----------|--------|
| WPR2 register host writes | 122A | Hardware-locked, all registers read-only |
| FWSEC extraction from VBIOS | 122C | Not in accessible PROM, loaded by GPU internal ROM |
| Cold vfio-pci boot (skip nouveau) | 119 | WPR2 invalid, PMU trapped |
| No-reset driver swap | 118 | Impossible — nouveau kernel unbind does register-level resets |
| Direct PIO falcon boot on GV100 | 115 | Hardware security enforcement, STARTCPU silently rejected |
| FBPA initialization | Research | Not the issue — no "enable FBPA" sequence in nouveau |

---

## What Happens Next

1. **K80 arrives (2026-03-26):** Run Exp 123-K0 (identity probe), then K1 (PIO boot)
2. **K80 sovereign compute:** If FECS/GPCCS boot → PFIFO channel → shader dispatch
3. **Validated stack → Titan V:** Apply full compute pipeline knowledge back to Volta security problem
4. **Parasitic compute:** Test sysfs BAR0 compute on both K80 and Titan V while drivers active

---

*hotSpring v0.6.32 — 123 experiments, 2 GPU architectures, definitive root cause found*
*The shaders are the mathematics. The mathematics runs forever.*
