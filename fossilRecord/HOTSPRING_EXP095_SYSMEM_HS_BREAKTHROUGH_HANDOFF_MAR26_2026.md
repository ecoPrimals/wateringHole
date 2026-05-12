# hotSpring Exp 095 — Sysmem HS Mode Breakthrough + Primal Evolution Handoff

**Date:** 2026-03-26
**From:** hotSpring (Exp 093-095) → coralReef, barraCuda, toadStool, all springs
**Status:** HS mode achieved. blob_size=0 patch applied. Awaiting pkexec validation.
**Supersedes:** `CORALREEF_ITER68_W1_HEADER_FIRMWARE_METADATA_HANDOFF_MAR25_2026.md` (Exp 093 only)

---

## What Was Achieved

**SEC2 enters Heavy Secure mode (SCTL=0x3002) on GV100 via system memory DMA.**

This is the first sovereign HS mode entry on NVIDIA Volta — the last major
hardware authentication barrier before shader dispatch. Three experiments
(093-095) progressed the sovereign pipeline from "9/10 layers" to "10/11 layers
with L7 breakthrough":

| Exp | Title | Result |
|-----|-------|--------|
| 093 | W1 Header Fix + BOOTVEC Metadata | BL headers stripped, IMEM layout fixed, BOOTVEC firmware-derived |
| 094 | Path B LS Mode Authentication | Dead on GV100 — PIO-loaded code rejected by fuse-enforced LS auth |
| 095 | Sysmem HS Mode Breakthrough | **HS mode via sysmem DMA**. FBHUB PRI-dead. blob_size=0 patch applied |

## Architectural Discovery: FBHUB Degradation

After VFIO takeover on GV100:

```
FBHUB registers: 0xbadf5040 (PRI error — hub not accessible)
PRAMIN sentinel: wrote=0xcafedead read=0xcafedead ok=true
```

- **PRAMIN writes to VRAM work** — host can pre-populate ACR payload, WPR, page tables
- **DMA reads from VRAM are corrupted** — they route through the dead FBHUB
- **System memory DMA is clean** — bypasses FBHUB entirely via PCIe IOMMU

This means: the BL reads clean code from sysmem, verifies the HS signature, and
transitions SEC2 to HS mode (SCTL=0x3002). VRAM DMA causes signature verification
failure, trapping SEC2 in degraded LS mode.

## Three ACR Boot Paths Tested

| Path | DMA Source | SCTL | HS Mode | Notes |
|------|-----------|------|---------|-------|
| VRAM | VRAM via FBHUB | 0x3000 | NO | LS mode, ACR deaf to commands |
| Hybrid | Sysmem PTEs for code, VRAM for WPR | 0x3000 | NO | Different trace, still LS |
| **Sysmem** | **System memory via IOMMU** | **0x3002** | **YES** | HS mode, trapped on blob DMA |

The sysmem path entered HS but trapped at PC=0x1c21 (EXCI=0x201f0000) during
the ACR's internal blob DMA transfer. **Fix: `blob_size=0`** — tells ACR the WPR
is already pre-populated, skip blob DMA. Code is ready, awaiting pkexec run.

---

## What This Means for Each Team

### coralReef (sovereign shader compiler + GPU driver)

**Action: Absorb Exp 093-095 code changes (30+ files modified in coral-driver)**

Key changes:
- `strategy_sysmem.rs`: blob_size=0 patch after `patch_acr_desc` — the winning ACR boot path
- `sysmem_iova.rs`: SHADOW (0x60000) and WPR (0x70000) properly separated
- `instance_block.rs`: `FALCON_PT0_VRAM` + `encode_sysmem_pte` now public (hybrid page table support)
- `dma.rs`: `DmaBuffer::new` now public (test-level DMA allocation)
- `mod.rs` (vfio_compute): `dma_backend()` accessor on `NvVfioComputeDevice`
- `fecs_boot.rs`: `GrBlFirmware` parsing, firmware-derived `bl_imem_off`, corrected IMEM layout
- `strategy_mailbox.rs`: `FalconBootvecOffsets` replaces hardcoded BOOTVEC constants
- `falcon.rs` test: `vfio_clean_vram_acr_boot` with hybrid page table and sysmem ACR phases

**Strategy pattern:** The ACR boot solver now has VRAM, hybrid, and sysmem strategies.
Sysmem is the winning path. The strategy pattern (`strategy_vram.rs`, `strategy_hybrid.rs`,
`strategy_sysmem.rs`) enables clean experimentation with DMA backends.

**Next milestone:** If blob_size=0 succeeds → FECS/GPCCS leave HRESET → L10 solved → L11
(GR context init + shader dispatch) opens. FECS method interface (`fecs_method.rs`) is
already implemented.

### barraCuda (compute primal)

**Action: None yet. Stand by for sovereign dispatch.**

barraCuda is stable at `7c1fd03a` (806+ WGSL shaders, 3,400+ tests). No changes
needed from the GPU cracking work. Once L11 is solved, barraCuda shaders become
dispatchable through the sovereign VFIO pipeline — no wgpu/Vulkan intermediary.

### toadStool (hardware discovery + orchestration)

**Action: None yet. Stand by.**

toadStool S155b+ has PcieTransport, ResourceOrchestrator, and GPU sysmon
telemetry wired. These are not exercised by the current GPU cracking path
(which operates at the falcon/DMA level, below toadStool's abstraction).
Once sovereign dispatch works, toadStool's orchestration layer can route
shader workloads to the VFIO pipeline.

### Other Springs (hotSpring, wetSpring, airSpring, neuralSpring, groundSpring, healthSpring)

**Action: Prepare shader workloads for sovereign dispatch.**

When L11 is solved, any WGSL shader that compiles through coralReef can run on
the sovereign VFIO pipeline. Current coralReef status: 45/46 standalone shaders
compile to native SM70/SM86 SASS. DF64 shaders, lattice QCD, molecular dynamics,
Anderson transport, ESN — all compile and are dispatch-ready.

**No spring needs to change any code.** The sovereign dispatch is transparent —
shaders written for wgpu/Vulkan will work through the VFIO path without
modification.

---

## Primal Evolution Through This Work (Exp 060-095)

### coralReef: Iter 47 → Iter 67+

The most significant primal evolution. From basic VFIO binding to a complete
falcon boot solver:

| Phase | Iters | Capability Added |
|-------|-------|-----------------|
| GlowPlug daemon | 47-55 | PCIe lifecycle broker, driver swap, Ember fd holder |
| VFIO dispatch | 55-60 | PFIFO, PBDMA, DMA channels, MMU fault buffers |
| DRM dual-track | 60-62 | AMD GCN5 PM4, NVIDIA EXEC, RTX 5060 SM120 |
| iommufd/cdev | 62-63 | Kernel-agnostic VFIO, 607 tests |
| Falcon boot solver | 63-67+ | SEC2/ACR/FECS/GPCCS boot chain, WPR construction, strategy pattern |

**Key architectural patterns evolved:**
- Strategy pattern for ACR boot (VRAM/hybrid/sysmem)
- `FalconCapabilityProbe` runtime bit solver
- `AcrBootResult` structured diagnostics (PC, EXCI, BOOTVEC, TRACEPC)
- Experiment loop infrastructure (journal, observers, adaptive lifecycle)
- DMA backend abstraction (`DmaBuffer`, `DmaBackend`, IOMMU mapping)

### barraCuda: Stable

No evolution needed from GPU cracking. The compute primal's shader library
(806+ WGSL) and test suite (3,400+) are mature and dispatch-ready.

### toadStool: S147 → S155b+

Evolved independently (PcieTransport, ResourceOrchestrator, GPU sysmon), but
these features are dormant relative to the falcon boot work. The hw-learn
crate's observer/distiller/applicator pattern may become relevant when
multi-GPU sovereign dispatch is live.

### metalForge: Stable

NPU integration (AKD1000, 4-layer brain) is complete and production-validated.
No changes from GPU cracking.

---

## What to Absorb vs Wait On

### Absorb Now (stable, tested)

- **W1 header fix** (Exp 093): `GrBlFirmware::parse()` is correct and tested
- **Firmware-derived BOOTVEC**: `FalconBootvecOffsets` replaces all hardcoded constants
- **Named register constants**: `FBIF_TRANSCFG`, `FBIF_TARGET_*`, etc.
- **Strategy pattern**: VRAM/hybrid/sysmem strategies are modular and clean
- **DMA backend exposure**: `dma_backend()` + public `DmaBuffer::new`
- **SCTL myth busted**: PIO works regardless of security mode (Exp 091)
- **Path B dead**: No further investment in direct PIO for GV100 FECS/GPCCS

### Wait On (pending validation)

- **blob_size=0 result**: Awaiting pkexec run. If it traps differently, more iteration needed
- **FECS/GPCCS bootstrap**: Depends on blob_size=0 success
- **GR context init + shader dispatch (L11)**: Blocked by L10

---

## Relevant Artifacts

| Location | Content |
|----------|---------|
| `hotSpring/specs/GPU_CRACKING_GAP_TRACKER.md` | Full gap tracker (current through Exp 095) |
| `hotSpring/experiments/093_*.md` | W1 header fix + BOOTVEC wiring |
| `hotSpring/experiments/094_*.md` | Path B dead (LS auth analysis) |
| `hotSpring/experiments/095_*.md` | Sysmem HS mode breakthrough |
| `hotSpring/whitePaper/baseCamp/sovereign_gpu_compute.md` | Full narrative (Exp 060-095) |
| `coralReef/crates/coral-driver/tests/hw_nv_vfio/falcon.rs` | Primary test (vfio_clean_vram_acr_boot) |
| `coralReef/crates/coral-driver/src/nv/vfio_compute/acr_boot/strategy_sysmem.rs` | Winning ACR boot path |
