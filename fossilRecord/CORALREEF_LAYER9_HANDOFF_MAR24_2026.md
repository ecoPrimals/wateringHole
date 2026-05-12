# coralReef Handoff: Layer 9 — FECS/GPCCS Halt Release + Remaining Evolution

**From:** hotSpring (Exp 082-087 campaign)
**Date:** 2026-03-24
**Priority:** HIGH — next sovereign pipeline blocker
**Context:** Layers 7+8 solved, 8/10 sovereign layers proven

---

## What hotSpring Solved (Exp 082-087)

### Layer 7: SEC2 Falcon Binding + DMA (Exp 083-085)

Seven binding bugs (B1-B7) found via nouveau source analysis and cross-driver
comparison. `falcon_bind_context()` encapsulates the full 8-step bind sequence.
bind_stat=5 on both Titans.

| Fix | Description |
|-----|-------------|
| B1 | Register offset: 0x668 → 0x054 |
| B2 | Missing bit 30 enable flag |
| B3 | SYS_MEM_COH_TARGET: 3 → 2 (coherent) |
| B4 | Missing DMAIDX clear |
| B5 | UNK090 bit 16 trigger |
| B6 | ENG_CONTROL bit 3 activation |
| B7 | CHANNEL_TRIGGER LOAD + INTR_ACK clear |

### Layer 8: WPR/ACR Payload (Exp 087)

Seven WPR construction bugs (W1-W7) found via byte-level comparison with
nouveau's `gp102_acr_wpr_build`. Fixes applied to `firmware.rs` + `wpr.rs`.

| Fix | Description |
|-----|-------------|
| W1 (CRITICAL) | Strip 64B headers from gr/{fecs,gpccs}_bl.bin before WPR concat |
| W2 (CRITICAL) | bl_imem_off = start_tag << 8 (FECS=0x7E00, GPCCS=0x3400) |
| W3 | bl_code_size uses code section (512), not full file (576) |
| W4 | BLD DMA offsets use correct BL size |
| W5 | bl_data_size = 84 (sizeof flcn_bl_dmem_desc_v2) |
| W6 | bin_version from sig file (version=2) |
| W7 | Remove depmap area corruption in signature copy |

New `GrBlFirmware` struct parses nvfw_bin_hdr + nvfw_hs_bl_desc from GR BL files.

### Cross-Driver Profiling (Exp 086)

BAR0 sysfs profiler captured 50+ registers across vfio/nouveau/nvidia on both Titans.

**Key insight:** WPR is an interface problem (we were mis-programming), not a
hardware security gate. Post-nouveau is the optimal starting state for sovereign boot.

---

## Layer 9: The Active Frontier

### Symptoms

After W1-W7 fixes, ACR successfully:
1. Parses WPR header table
2. Finds FECS and GPCCS LSB entries
3. Loads BL code to correct IMEM address (0x7E00 / 0x3400)
4. Sets ALIAS_EN on target falcons (HS mode configuration)

But FECS and GPCCS end up **HALTED** (cpuctl=0x12) instead of **RUNNING** (0x00).

```
SEC2 pre-command:                cpuctl=0x00000000 mb0=0xcafebeef
After BOOTSTRAP_FALCON(FECS):   mb0=0x00000001    mb1=0x00000002
After BOOTSTRAP_FALCON(GPCCS):  mb0=0x00000001    mb1=0x00000003
FECS cpuctl:  0x00000012  (HALTED + ALIAS_EN)
GPCCS cpuctl: 0x00000012  (HALTED + ALIAS_EN)
```

### Possible Causes

1. **BL halted after loading app code** — falcon BL may complete loading and then
   halt, waiting for a host signal (FECS_CTXSW_MAILBOX write or HRESET toggle)
2. **App code entry point wrong** — BL loaded code but jumped to wrong address
3. **HS mode page table missing** — secure falcon may need additional WPR config
4. **GPCCS must start before FECS** — dependency ordering may matter
5. **GR engine init required first** — FECS may need GR engine powered and ready

### Research Leads

1. **nouveau `gm200_gr_init_400()`** — post-ACR falcon start sequence. This is
   where nouveau transitions FECS from "ACR bootstrapped" to "running GR context"
2. **`nvkm_falcon_start()`** — the HRESET release + PC set sequence
3. **`FECS_CTXSW_MAILBOX` registers** — FECS host↔falcon communication protocol
4. **`gv100_gr_init()`** — GV100-specific GR engine initialization
5. **`acr_r367_bootstrap_hs_acr()`** — nouveau's post-WPR-load ACR completion handler

### Recommended Approach

1. Read nouveau's GR init sequence (`nvkm/engine/gr/gf100.c`, `gv100.c`)
2. Capture FECS register state during nouveau's GR init window (extend Exp 086 profiler)
3. Try clearing HALTED bit (write cpuctl with bit 4 clear) after ACR bootstrap
4. Check if mb0=1 means "success" or "error" by comparing with nouveau's ACR response handling

---

## Remaining Evolution Work for coralReef

### Code Changes in Working Tree

Two files modified (not yet committed):
- `crates/coral-driver/src/nv/vfio_compute/acr_boot/firmware.rs` — GrBlFirmware struct
- `crates/coral-driver/src/nv/vfio_compute/acr_boot/wpr.rs` — W1-W7 fixes

### Outstanding Handoffs (Still Active)

| Handoff | Scope | Status |
|---------|-------|--------|
| `CORALREEF_TRACE_INTEGRATION_HANDOFF.md` | Native mmiotrace in Ember swap lifecycle | Delivered, not implemented |
| `CORALREEF_OPEN_TARGET_REAGENT_HANDOFF.md` | Open target acceptance, Personality::Custom | Delivered, not implemented |
| `CORALREEF_WPR_FIX_HANDOFF.md` | W1-W7 WPR construction | **APPLIED + VALIDATED** |

### Architecture Evolution Items

1. **BarOps/VfioOps/DmaOps traits** — extract hardware interaction traits for testability
2. **KNOWN_TARGETS removal** — replace allowlist with open acceptance + validation
3. **Trace-as-default** — every driver swap captures register state automatically
4. **Legacy driver reagent support** — version-indexed nvidia modules as test substrates

---

## Full Analysis

- `hotSpring/experiments/087_WPR_FORMAT_ANALYSIS.md` — W1-W7 detailed analysis + hardware validation
- `hotSpring/experiments/086_CROSS_DRIVER_FALCON_PROFILE.md` — cross-driver profiling results
- `hotSpring/experiments/085_B5B7_BIND_TRIGGER_VALIDATION.md` — Layer 7 breakthrough
- `hotSpring/specs/GPU_CRACKING_GAP_TRACKER.md` — full gap tracker with Layer 9 (Gap 10)
