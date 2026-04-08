# hotSpring Sovereign Pipeline Regroup Handoff

**Date:** March 30, 2026
**From:** hotSpring (biomeGate workstation)
**To:** All primal and spring teams
**Scope:** Sovereign GPU pipeline status, validation matrix, DRM-from-both-sides strategy

## What We Solved (Experiments 058-125)

### VFIO Infrastructure (Layers 1-6)
- L1-L3: Device binding, BAR0/BAR2 access, PMC enable — all PASS on Titan V
- L4: PFIFO init + PBDMA discovery — PASS, including warm-handoff mode that preserves engine state
- L5: MMU fault buffer — PROVEN (Exp 076, DMA roundtrip verified)
- L6: PBDMA context load — PASS with stale interrupt clearing fix

### ACR Boot Chain (Layers 7-8)
- SEC2 falcon binding: 8-step bind sequence from nouveau source analysis (Exp 083-085)
- WPR format: W1-W7 fixed, ACR processes WPR payload (Exp 087)
- HS mode: achieved via PDE slot discovery — sole determinant (Exp 110 consolidation matrix)
- Root cause definitive: WPR2 registers hardware-locked by FWSEC (Exp 122)

### Warm Handoff Livepatch (Exp 125)
Kernel livepatch module NOPs four nouveau functions during teardown:
1. `nvkm_mc_reset` — preserves IMEM/DMEM
2. `gf100_gr_fini` — preserves FECS/GPCCS running state
3. `nvkm_falcon_fini` — preserves falcon CPU
4. `gk104_runl_commit` — prevents FECS self-reset from empty runlist

Dynamic control: disabled during nouveau init, enabled before teardown. `coralctl warm-fecs` orchestrates the full cycle.

### coral-ember Fixes
- `reset_method` sysfs race: kernel ignores 0-byte writes; fixed to write `\n` instead
- PBDMA warm mode: clear stale interrupt flags without force-clearing PBDMA state
- PFIFO warm init: skip empty runlist flush and runlist preempt (these cause FECS to disable GR)
- Privileged sysfs writes via `coralreef-sysfs-write` helper for livepatch control

## What's Blocked

| Blocker | Why | Paths Forward |
|---------|-----|---------------|
| FECS HS mode on Volta | ACR boots FECS in High Security mode; host STARTCPU blocked | Livepatch warm handoff (Exp 125, ready to test) |
| WPR2 hardware-locked | FWSEC sets WPR2 registers at VBIOS time; cannot be modified from host | Cold boot sovereign FECS not possible on Volta |
| K80 not UEFI-POSTed | nouveau rejects uninitialized GPU ("unknown chipset") | Needs VBIOS DEVINIT or proprietary driver init first |
| nouveau PMU firmware | Desktop Volta PMU firmware not distributed by NVIDIA | DRM compute channel alloc fails without PMU |

## Validation Matrix (New: specs/SOVEREIGN_VALIDATION_MATRIX.md)

Maps every pipeline layer (L1-L11) against dispatch paths and hardware substrates:

| Path | Titan V Status | Key Finding |
|------|---------------|-------------|
| VFIO warm handoff | **FRONTIER** (L9-L11) | Livepatch deployed, ready to test |
| nvidia-drm + UVM | UNTESTED (code-complete) | NvUvmComputeDevice done, needs proprietary driver loaded |
| nouveau DRM | BLOCKED (no PMU firmware) | Channel alloc fails |
| NVK/wgpu | **PROVEN** (4-tier QCD) | Fallback compute works today |
| AMD DRM | PROVEN (6/6 tests PASS) | RX 6950 XT decommissioned, code preserved |

## Upstream Integration Points

### For toadStool Team (S168+)
- `shader.dispatch` correctly delegates to coralReef `compute.dispatch.execute`
- When VFIO dispatch works, the full pipeline lights up without toadStool changes
- The `dispatch_mode: "vfio"` path will auto-select when BDF is on vfio-pci

### For barraCuda Team (Sprint 23+)
- f64 precision fix is critical — sovereign dispatch will use f64-native shaders
- `SovereignDevice` RPC contract (`compute.dispatch.submit`) matches our VFIO handler
- IPC math/tensor methods provide composition graph for sovereign compute

### For coralReef Team (Iter 70+)
- Warm-handoff code in coral-driver: `PfifoInitConfig::warm_handoff()`, `VfioChannel::create_warm()`, `NvVfioComputeDevice::open_warm()`, `restart_warm_falcons()`
- Ember changes: `sysfs_write_direct` newline fix, reset_method timing in `swap.rs`
- Glowplug changes: `rpc_warm_fecs` with dynamic livepatch control, `sysfs_write_privileged` helper
- Livepatch source: `scripts/livepatch/livepatch_nvkm_mc_reset.c` (4 NOPed functions)

## Experiment Archive

Experiments 001-057 archived to `experiments/archive/` — completed physics validation, benchmarks, and NPU work. Results absorbed into `whitePaper/baseCamp/`. Active experiments: 058+ (VFIO pipeline), 110+ (consolidation/resolution), 123-126 (K80, VM captures, livepatch, DRM tracing).

## Next Steps

1. Test livepatch warm handoff (`coralctl warm-fecs` + `vfio_dispatch_warm_handoff`)
2. If blocked: nvidia+UVM proprietary tracing (load nvidia for Titan V, trace RM init)
3. Continue physics on NVK/wgpu fallback regardless
4. K80 PIO FECS boot (Kepler has no security barriers)
