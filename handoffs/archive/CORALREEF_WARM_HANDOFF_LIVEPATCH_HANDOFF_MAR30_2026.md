# coralReef Warm Handoff + Livepatch Handoff

**Date:** March 30, 2026
**From:** hotSpring (biomeGate workstation)
**To:** coralReef team (Iter 70+)
**Scope:** All warm-handoff code changes in coral-driver, coral-ember, coral-glowplug, and the kernel livepatch module

## Summary

The warm handoff preserves FECS firmware state across a `nouveau` -> `vfio-pci` driver swap, enabling sovereign VFIO compute dispatch on Titan V (GV100) without cold-booting FECS (which is blocked by WPR2 hardware locks). The approach uses a kernel livepatch to NOP destructive nouveau teardown functions and a series of coral-driver fixes for PFIFO warm initialization.

## Code Changes by Crate

### coral-driver (`crates/coral-driver/`)

**`src/vfio/channel/pfifo.rs`:**
- `PfifoInitConfig::warm_handoff()` — new config mode: `pbdma_force_clear=false`, `flush_empty_runlists=false`, `preempt_runlists=false`
- Warm mode clears stale PBDMA interrupt flags (`b + 0x108 = 0xFFFF_FFFF`) without force-clearing PBDMA state
- Empty runlist flush and runlist preempt conditionally skipped (these cause FECS to disable GR engine)

**`src/vfio/channel/mod.rs`:**
- `VfioChannel::create_warm()` — creates channel using warm_handoff PFIFO config

**`src/nv/vfio_compute/mod.rs`:**
- `NvVfioComputeDevice::open_warm()` — opens device using `create_warm` channel, calls `restart_warm_falcons()`

**`src/nv/vfio_compute/init.rs`:**
- `restart_warm_falcons()` — diagnoses FECS state (CPUCTL, SCTL, PC, EXCI), re-applies GR engine enables, calls `setup_gr_context_warm()`. Warns if FECS is in HRESET (livepatch should prevent this).

### coral-ember (`crates/coral-ember/`)

**`src/sysfs.rs`:**
- `sysfs_write_direct()` — fixed: kernel ignores 0-byte writes to sysfs. Now writes `b"\n"` when value is empty, which correctly clears sysfs attributes like `reset_method`.

**`src/swap.rs`:**
- `bind_vfio()` — writes empty string to `reset_method` immediately after vfio-pci bind (before settle sleep), preventing the PCI bus reset that obliterates GPU state.

### coral-glowplug (`crates/coral-glowplug/`)

**`src/bin/coralctl/handlers_device/mod.rs`:**
- `rpc_warm_fecs()` — full warm-fecs cycle:
  1. Step 0: Disable livepatch (via `sysfs_write_privileged`)
  2. Step 1: Swap BDF to nouveau (loads ACR, boots FECS firmware)
  3. Step 2: Wait for GR init (configurable settle time)
  4. Step 2b: Enable livepatch (all 4 NOPs active)
  5. Step 3: Swap BDF to vfio (nouveau teardown with NOPs preserving FECS)
- `sysfs_write_privileged()` — helper that uses `sudo -n coralreef-sysfs-write` for root-only sysfs paths (livepatch enabled attribute)

### Kernel Livepatch (`scripts/livepatch/livepatch_nvkm_mc_reset.c`)

NOPs four nouveau functions when enabled:
1. `nvkm_mc_reset` — PMC engine reset
2. `gf100_gr_fini` — GR engine teardown
3. `nvkm_falcon_fini` — falcon CPU halt
4. `gk104_runl_commit` — runlist submission (prevents FECS self-reset from empty runlist during channel teardown)

Build: `make -C /lib/modules/$(uname -r)/build M=/path/to/livepatch modules`
Deploy: `deploy_all.sh` handles build, install, depmod, modprobe

## Key Bug Fixes

| Bug | Root Cause | Fix |
|-----|-----------|-----|
| PCI bus reset obliterates GPU state | `vfio-pci` performs bus reset during bind | Write empty `reset_method` immediately after bind |
| Empty string sysfs write ignored | `std::fs::write(path, "")` = 0 bytes, kernel ignores | Write `b"\n"` instead when value is empty |
| PBDMA stale interrupts | Previous driver leaves interrupt flags set | Clear `0xFFFF_FFFF` to PBDMA intr registers in warm mode |
| FECS disables GR engine | Empty runlist flush + preempt during PFIFO init | Skip both in warm_handoff config |
| FECS self-resets during teardown | nouveau commits empty runlist (count=0) | Livepatch NOPs `gk104_runl_commit` |
| Livepatch sysfs write fails as user | `/sys/kernel/livepatch/*/enabled` is root-only | Use `coralreef-sysfs-write` helper via sudo |

## Test Path

```bash
# 1. Deploy everything (requires pkexec once)
pkexec bash scripts/deploy_all.sh

# 2. Run warm-fecs cycle
coralctl warm-fecs 0000:03:00.0 --settle 12

# 3. Run dispatch test
CORALREEF_VFIO_BDF=0000:03:00.0 CORALREEF_VFIO_SM=70 \
  cargo test --test hw_nv_vfio -p coral-driver --features vfio -- \
  vfio_dispatch_warm_handoff --ignored
```

## What Iter 70 Should Absorb

1. The warm PFIFO config pattern (`PfifoInitConfig::warm_handoff()`) for any future warm-swap scenarios
2. The `sysfs_write_direct` newline fix — affects any sysfs path clearing
3. The `reset_method` timing in `swap.rs` — critical for any vfio-pci bind
4. The livepatch source and Makefile as reference for future kernel-level patches
5. The `sysfs_write_privileged` pattern for CLI tools that need root sysfs access
