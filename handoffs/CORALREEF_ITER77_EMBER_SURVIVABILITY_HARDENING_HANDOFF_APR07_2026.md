# Handoff: Ember Survivability Hardening — Iter 77

**Date:** April 7, 2026
**From:** hotSpring GPU solving session
**Repos:** coralReef (Iter 77), hotSpring (Exp 140-151)
**Teams:** coralReef, hotSpring, all primal/spring teams using GPU compute

---

## What Changed

### Three-Phase Ember Survivability Hardening

Ember is now a **crash-proof sacrificial GPU interface**. When GPU hardware faults
occur, ember dies cleanly (via `abort()`) and glowplug resurrects it with a GPU
warm cycle. The system never locks up.

**Phase 1 — Eliminate Critical Lockup Vectors (6 items):**

| Vector | Fix |
|--------|-----|
| C1: `preflight_check` raw MMIO on main thread | Refactored to `preflight_gate` (pure in-memory) + fork-isolated PRI ACK/BOOT0 in child |
| C2: `with_mmio_watchdog` thread-level (can't protect core stalls) | Replaced with `fork_isolated_mmio` in all `mmio_read/write/batch` |
| C3: Parent-side `disable_bus_master_via_sysfs` in recovery | Removed from all parent paths; bus master toggle moved into fork children |
| C4: `sync_all()` in `trace()` before fork | Removed — best-effort append only |
| C5: `post_swap_quiesce` raw BAR0 without fork isolation | Wrapped in `fork_isolated_mmio` with 2s timeout (lib.rs, startup.rs, swap_bind.rs) |
| C6: `std::process::exit` runs global cleanup | Replaced with `std::process::abort()` — no destructors, no I/O stalls |

**Phase 2 — Harden Moderate Debt (4 items):**

| Debt | Fix |
|------|-----|
| M1: `sysfs_write_direct` bypasses timeout protection | Replaced with `sysfs_write` (guarded) in swap_bind.rs |
| M2: `is_d3cold`/`read_power_state` unguarded sysfs reads | New `guarded_sysfs_read` with 2s timeout |
| M3: `tracing::error!` blocks if journald backlogged | Fire-and-forget background threads for fault-path tracing |
| M4: Glowplug health loop sysfs during experiments | Addressed via guarded reads |

**Phase 3 — Evolve Glowplug Resurrection (3 items):**

| Gap | Fix |
|-----|-----|
| G1-G2: Restart doesn't warm cycle GPU | `resurrect_ember()` performs sysfs nouveau bind/unbind before restart |
| G3: FdVault not wired | Periodic fd checkpoint (30s), vault-aware resurrection (skip warm if vault has fds) |
| G4: No live warm cycle RPC | `ember.warm_cycle` RPC: release → nouveau bind/unbind → reacquire |

### Validation Results

- **8 consecutive exp145 crash probes** — zero lockups
- Cold VRAM (`0xbad0ac0X`) detected and reported as clean error
- Ember stays alive and responsive throughout all tests
- 170 coral-ember tests pass, 285 coral-glowplug lib tests pass

### Files Changed (coralReef)

**coral-ember:**
- `src/ipc/handlers_mmio/mod.rs` — `preflight_gate` (was `preflight_check`), `update_fault_counter`
- `src/ipc/handlers_mmio/low_level.rs` — fork-isolated `mmio_read/write/batch`
- `src/ipc/handlers_mmio/falcon.rs` — `preflight_gate` import update
- `src/ipc/handlers_mmio/pramin.rs` — `preflight_gate` import, removed `sync_all()`
- `src/isolation.rs` — zero-I/O recovery, removed parent sysfs writes, removed `sync_all()` from trace
- `src/hold.rs` — `abort()` in `check_voluntary_death`, fire-and-forget tracing in `emergency_quiesce`
- `src/lib.rs` — `abort()` in shutdown watchdog, fork-isolated `post_swap_quiesce`
- `src/startup.rs` — fork-isolated `post_swap_quiesce`
- `src/swap/swap_bind.rs` — guarded sysfs writes, fork-isolated `post_swap_quiesce`
- `src/sysfs.rs` — `guarded_sysfs_read` with timeout
- `src/ipc.rs` — `ember.warm_cycle` dispatch
- `src/ipc/handlers_device.rs` — `warm_cycle` handler implementation

**coral-glowplug:**
- `src/ember_lifecycle.rs` — `sysfs_warm_cycle`, FdVault integration, `checkpoint_fds`, vault-aware `resurrect_ember`, `managed_bdfs`
- `src/main.rs` — `managed_bdfs` wiring, `resurrect_ember()` instead of `spawn_ember()`

### Impact on Other Teams

**Any primal/spring using GPU compute via ember RPCs:**
- No API changes — all existing RPCs work exactly as before
- Faults now return clean error responses instead of hanging
- `ember.warm_cycle` is a new optional RPC for resetting GPU state between experiments

**coralReef compiler team:**
- No changes to compilation pipeline or dispatch
- coralGpu users are unaffected (wgpu/nouveau/amdgpu paths don't use ember)

**hotSpring:**
- Exp 145 ACR boot runs safely (reports cold VRAM as error, no lockup)
- Exp 150 crash vector hunt — RESOLVED
- GPU warm cycle needed before PRAMIN-heavy experiments on cold GPU

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────────┐
│                   glowplug (immortal)                    │
│  - Heartbeat monitor (3s interval)                       │
│  - FdVault: periodic fd checkpoint from ember            │
│  - Resurrection: kill → warm cycle → spawn               │
│    (skip warm cycle if vault has live fds)               │
└──────────────┬──────────────────────────────┬────────────┘
               │ systemctl start/stop         │ fd checkpoint
               ▼                              ▼
┌─────────────────────────────────────────────────────────┐
│                    ember (sacrificial)                    │
│  - All MMIO: fork_isolated_mmio (child dies, not us)     │
│  - Zero I/O in recovery paths                            │
│  - abort() on total fault (no cleanup stalls)            │
│  - ember.warm_cycle RPC (release → nouveau → reacquire)  │
│  - Emergency quiesce: drop BAR0 + mark faulted           │
└──────────────┬──────────────────────────────┬────────────┘
               │ fork()                       │ sysfs
               ▼                              ▼
┌──────────────────────┐    ┌──────────────────────────────┐
│  Child process       │    │  GPU Hardware                 │
│  - BAR0 read/write   │    │  - VFIO binding               │
│  - Bus master toggle │    │  - nouveau warm cycle          │
│  - Dies on timeout   │    │  - PCIe SBR (escalation)       │
└──────────────────────┘    └──────────────────────────────┘
```
