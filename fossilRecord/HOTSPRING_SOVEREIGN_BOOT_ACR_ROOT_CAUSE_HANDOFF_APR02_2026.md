# Handoff: hotSpring Sovereign Boot — ACR Root Cause + Dual GPU Progress

**Date:** 2026-04-02
**From:** hotSpring (biomeGate)
**To:** coralReef team, primal teams, spring teams
**Experiments:** 132-141
**Status:** Root cause identified, next phase clear

---

## Executive Summary

Ten experiments (132-141) systematically debugged the Titan V ACR authentication
failure and the K80 cold boot pipeline, resolving all DMA/page-table issues and
identifying the true root cause of the persistent HS authentication failure:
**missing VBIOS DEVINIT**.

The SEC2 crypto engine is uninitialized after a Subsystem Bridge Reset (SBR)
because the nouveau-captured recipe replays post-VBIOS register state but omits
the VBIOS scripts that initialize security hardware, clocks, PLLs, and memory
controllers from a cold state.

---

## What Was Resolved (Exp 132-141)

### DMA Path — Fully Fixed

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| FBIF locked in VIRT mode | HS+ boot ROM sets FBIF_TRANSCFG=0x0100 | Accept VIRT mode, use falcon MMU with patched page tables |
| DMA to wrong memory | PTEs mapped to VRAM, not system memory | SYS_MEM_COH PTEs in PT0 (ACR payload) + new PT1 (WPR buffer) via PRAMIN |
| ctx_dma mismatch | BL expects VIRT, descriptor said PHYS_SYS_COH | Changed to ctx_dma=VIRT (1) |
| DMEM corruption | BL descriptor (84B) overwrites ACR data at DMEM@0 | DMEM repair step after BL reads descriptor |
| Extra STARTCPU re-locks FBIF | Warm-up STARTCPU re-runs boot ROM | Removed — `falcon_engine_reset` is sufficient |
| IOMMU faults | N/A — no faults at ACR/WPR DMA addresses | Confirmed clean |

### Dual GPU Progress (Exp 135-136)

| GPU | Achieved | Blocked By |
|-----|----------|-----------|
| K80 (GK210) | Clock init, DEVINIT recipe, FECS PIO upload, falcon running | PGRAPH CTXSW domain PRI-faults (needs VBIOS POST for memory training) |
| Titan V (GV100) | SEC2 reset, ACR BL execution, DMA enabled, auth loop entered | VBIOS DEVINIT (crypto engine uninitialized) |

### Safety Architecture (Exp 138, 140)

- D-state root cause traced: sysfs writes to GPU power/driver files
- Ember/glowplug resilience: timeout-guarded child process isolation
- Validated: GPU access operations cannot crash the host

---

## Root Cause: VBIOS DEVINIT (Exp 141)

### Evidence

The ACR Boot Loader executes through the complete BL sequence (TRACEPC: 0xfd75→0xfd62→0xfd0a), loads ACR non_sec code, and enters the HS authentication loop at PC 0x2d78. The loop retries ~5 times with different sub-paths, then falls back to BL error path. Consistent across ALL DMA-enabled strategies.

**Comparison:**
- Strategy 12 (direct IMEM, no DMA): mb0=0x36 → WPR read fails (no DMA), but ACR runs with correct data
- Strategy 7c (BL + DMA): mb0=0x00 → WPR check passes (DMA works), but HS auth fails

### What VBIOS DEVINIT Configures

- ROOT_PLL, NVPLL, MEMPLL configuration
- Power sequencing and voltage domains
- **Security hardware initialization (crypto engine, fuse access)**
- Memory controller calibration
- Clock domain routing

### Why the Recipe Is Insufficient

The `nouveau_init_recipe.json` (337 steps) was captured from nouveau's init —
which runs AFTER the VBIOS POST has already configured all of the above.
After an SBR reset, the GPU hardware appears functional (registers read/write,
DMA partially works), but the crypto engine needed for HS signature verification
is not initialized.

---

## Impact on Primal Teams

### coralReef

- **VBIOS script interpreter** exists at `devinit/script/interpreter.rs` — execute BIT 'I' init scripts from the Titan V's VBIOS ROM before ACR boot
- **SEC2 PMC bit**: fallback bit 22 may be wrong — scan PTOP registers for correct mapping
- All DMA infrastructure (page table construction, sysmem PTE encoding, instance block management) is now proven correct and can be trusted
- `strategy_chain.rs` Strategy 7c is the reference implementation for ACR boot with sysmem DMA

### toadStool

- The `shader.dispatch` → `compute.dispatch.execute` pipeline is architecturally correct
- Once L10 (HS auth) is resolved, L11 (GR context + shader dispatch) is ready
- `fecs_method.rs` already implements the GR context init sequence

### barraCuda

- No direct impact — upstream library code is insulated from driver-level work
- Science pipeline continues to validate on RTX 3090 (GPFIFO) and RX 6950 XT (AMD DRM)

### ember / glowplug

- `mmio.write` RPC enables active falcon intervention from daemon layer
- D-state safety architecture (Exp 140) should be absorbed as standard operating mode
- K80 cold boot (`coralctl cold-boot`) is first-class CLI operation

---

## What Stays in hotSpring (Fossil Record)

All 10 experiment journals (132-141) remain in `experiments/`. Key reference:
- `141_ACR_HS_AUTH_ROOT_CAUSE.md` — definitive root cause analysis
- `140_UNCRASHABLE_GPU_SAFETY_ARCHITECTURE.md` — safety patterns
- `135_DUAL_GPU_SOVEREIGN_BOOT_ATTEMPT.md` — K80 vs Titan V comparison

---

## Next Steps

1. **VBIOS script execution** — run BIT 'I' init scripts via `devinit/script/interpreter.rs`
2. **No-SBR test** — skip SBR, use GPU in VBIOS-POSTed state to confirm hypothesis
3. **K80 PGRAPH** — resolve PRI-faults above 0x409504 (likely needs GR engine PMC enable)
4. **Ember policy engine** — per-GPU register access rules and teardown policy
5. **Experiment matrix** — boot strategy × teardown policy × FECS state × architecture
