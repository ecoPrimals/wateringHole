# Handoff: Sacrificial Ember Architecture + GPU Solving Status

**Date:** April 6, 2026
**From:** hotSpring GPU solving session
**Repos:** coralReef (Iter 76+), hotSpring (Exp 140-150)
**Teams:** coralReef, hotSpring, all primal/spring teams using GPU compute

---

## What Changed

### Sacrificial Ember Architecture (coralReef)

Ember is now a **disposable GPU interface**. When hardware faults occur, ember dies and glowplug resurrects it. The system no longer locks up.

**Key mechanisms implemented:**

1. **Fork-isolated MMIO** — All BAR0 operations run in expendable child processes. If the child hangs (GPU stuck), the parent kills it and triggers SBR.

2. **Bus master kill switch** — After any SBR or watchdog timeout, GPU bus master is disabled via sysfs (PCI command register bit 2). Prevents GPU from issuing DMA that could corrupt system memory.

3. **Emergency quiesce** — `HeldDevice::emergency_quiesce()` atomically: disables bus master, drops BAR0 mapping, marks device faulted.

4. **Voluntary death** — When all held devices are faulted, ember exits cleanly (exit code 1). systemd `Restart=on-failure` triggers restart, glowplug detects and manages the lifecycle.

5. **SIGTERM handler** — Clean shutdown: disables bus master on all devices, removes Unix socket, exits.

6. **Bypass paths closed** — `ember.vfio_fds` deprecated (returns error). Test harness `open_vfio()` panics if ember unavailable (no fallback to direct VFIO). All GPU access routes through MMIO gateway RPCs.

### Test Results

- coral-ember: 170 pass, 4 ignored (unimplemented handlers: `ember.fecs.state`, `ember.livepatch.status`)
- coral-glowplug: 461 pass, 0 failures
- ipc_dispatch integration: 17 pass, 0 failures
- 2 pre-existing vendor_lifecycle failures (Intel Xe — unrelated)

### Files Changed (coralReef)

- `crates/coral-ember/src/isolation.rs` — bus master kill switch, SIGTERM handler
- `crates/coral-ember/src/hold.rs` — `emergency_quiesce()`, `all_faulted()`, `check_voluntary_death()`
- `crates/coral-ember/src/lib.rs` — SIGTERM wiring, graceful shutdown in watchdog
- `crates/coral-ember/src/ipc/handlers_device.rs` — `vfio_fds` deprecated
- `crates/coral-ember/src/ipc/handlers_mmio/falcon.rs` — fork isolation + emergency quiesce
- `crates/coral-ember/src/ipc/handlers_mmio/low_level.rs` — watchdog + emergency quiesce
- `crates/coral-ember/src/ipc/handlers_mmio/pramin.rs` — fork isolation + emergency quiesce
- `crates/coral-ember/src/ipc/tests.rs` — test fixes for deprecation, cascade fixes
- `crates/coral-ember/tests/ipc_dispatch.rs` — test fixes for deprecation
- `crates/coral-glowplug/src/ember_lifecycle.rs` — simplified resurrection, state machine fixes
- `crates/coral-glowplug/src/main.rs` — lifecycle integration
- `crates/coral-driver/tests/hw_nv_vfio/helpers.rs` — removed direct VFIO fallback
- `crates/coral-driver/tests/hw_nv_vfio/exp145_v1_acr_boot.rs` — MMIO gateway architecture
- `crates/coral-driver/src/vfio/device/dma_safety.rs` — `prepare_dma_bar0_only` extraction

---

## GPU Solving Status

### Titan V (GV100) — SEC2 ACR Boot

**Current state:** SEC2 falcon starts and executes bootloader code, but does not achieve HS (Hardware Secure) mode. `SCTL=0x3000` (SECFS + HALT), `HS=false`.

**What works:**
- PRAMIN writes succeed (with warm GPU)
- Instance block construction + virtual DMA binding
- BL code uploaded to IMEM (PIO), survives STARTCPU
- DMEM data section + BL descriptor uploaded
- STARTCPU via fork-isolated `ember.falcon.start_cpu`
- Server-side `falcon_poll` through ember
- Full experiment lifecycle (glowplug watchdog, cleanup_dma)
- **System does NOT lock up** — validated April 6, 2026

**What doesn't work yet:**
- SEC2 halts after BL execution without transitioning to HS mode
- BROM registers (`ModSel`, `UcodeId`, `EngIdMask`, `ParaAddr0`) return `0xbadf5040` (not implemented/accessible)
- FECS/GPCCS return PRI errors (not yet enabled)

**Root cause investigation trail:**
- Exp 141: VBIOS DEVINIT suspected as blocker
- Exp 142-143: Contradicted — ACR fails even on BIOS-POSTed GPU
- Exp 144: PMC bit 5 discovery (SEC2 is at bit 5 on GV100, not bit 22)
- Exp 150: PRAMIN identified as crash vector, led to sacrificial architecture

**Next steps for GPU solving:**
- Debug why BL code halts (TRACEPC shows execution path, halts around PC=0x03fb)
- Investigate EXCI=0x001f000f (exception info post-boot)
- Compare BROM behavior: nouveau sets specific BROM registers before STARTCPU
- Try enabling PMU before SEC2 (PMU dependency from Exp 113)
- Warm GPU → SEC2 boot → check if BROM state changes

### Tesla K80 (GK210) — Kepler Cold Boot

**Current state:** Cold boot pipeline wired into `coralctl`. K80 needs BIOS POST for VRAM initialization. Kepler lacks firmware security (no ACR), making it a simpler target for sovereign compute validation.

**Next steps:**
- Validate K80 cold boot with warm cycle
- Use K80 as comparison target for Titan V investigation

---

## Relevance to Other Teams

### For coralReef polish teams
- The `vfio_fds` RPC is deprecated — do not add new callers. Use `ember.mmio.*`, `ember.pramin.*`, `ember.falcon.*` RPCs.
- Two `vendor_lifecycle` tests fail (Intel Xe settle time, sysfs power state). These are pre-existing and unrelated to the sacrificial architecture.
- Three `ipc::tests` are `#[ignore]` for unimplemented handlers (`ember.fecs.state`, `ember.livepatch.status`). Wire handlers when ready.

### For spring teams using GPU compute
- All GPU operations MUST route through ember. Direct VFIO access is blocked.
- If ember is unreachable, the test harness will panic with a clear message.
- The experiment lifecycle (`experiment_start`/`experiment_end` via glowplug) pauses health probes during active experiments. Use it.

### For primal teams (toadStool, barraCuda)
- The sovereign compute pipeline (GPFIFO on RTX 3090, scratch/local on AMD) is stable.
- SEC2 ACR boot on Volta is the current frontier — help wanted on BROM register initialization.
- The triangle architecture (coralReef↔toadStool↔barraCuda) is healthy.

---

## Architecture Diagram

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Experiment A │    │ Experiment B │    │  IDE / Tool  │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │ JSON-RPC (Unix socket)
                   ┌──────▼──────┐
                   │    EMBER    │  ← sacrificial canary
                   │  (held GPUs)│
                   └──┬─────┬───┘
                      │     │
              ┌───────▼┐   ┌▼───────┐
              │ fork() │   │ fork() │  ← expendable children
              │ child  │   │ child  │
              └───┬────┘   └────┬───┘
                  │             │
              ┌───▼───┐   ┌────▼──┐
              │ BAR0  │   │ BAR0  │
              │Titan V│   │ K80   │
              └───────┘   └───────┘

On fault: child dies → SBR → bus master OFF → device faulted
All faulted: ember exits(1) → glowplug restarts ember
```
