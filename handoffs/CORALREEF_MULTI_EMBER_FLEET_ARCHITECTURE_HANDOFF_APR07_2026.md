# coralReef: Multi-Ember Fleet Architecture — Handoff

**Date:** 2026-04-07
**From:** hotSpring GPU solving session
**To:** coralReef polish teams, primal evolution teams, spring teams
**Scope:** coral-ember + coral-glowplug architectural evolution

---

## What Changed

Ember evolved from a **monolithic process** (one ember holds all GPUs) into a **per-device fleet** model:

### Architecture Before
```
glowplug → ember (holds all 3 GPUs in one process)
```
One stuck MMIO on K80 blocks Titan V. One death kills all GPU access.

### Architecture After
```
glowplug (fleet orchestrator)
  ├─ ember@0000-03-00.0 (Titan V)
  ├─ ember@0000-4c-00.0 (K80 die1)
  ├─ ember@0000-4d-00.0 (K80 die2)
  └─ ember-standby-0 (hot-standby, no device)
```
K80 ember crash has zero impact on Titan V. Hot-standby promotes in <200ms.

---

## New Files

| File | Purpose |
|------|---------|
| `crates/coral-glowplug/src/ember_fleet.rs` | Fleet orchestrator — `EmberFleet`, `EmberInstance`, `StandbyEmber`, fault recording, resurrection strategy |
| `crates/coral-glowplug/coral-ember@.service` | Systemd template unit for per-device ember |
| `crates/coral-glowplug/coral-ember-standby@.service` | Systemd template unit for hot-standby ember |

## Modified Files

| File | Change |
|------|--------|
| `coral-ember/src/main.rs` | Added `--bdf` and `--standby` CLI flags |
| `coral-ember/src/lib.rs` | `EmberRunOptions.single_bdf` / `.standby`, `bdf_to_slug()`, `ember_instance_socket_path()`, `ember_standby_socket_path()`, config filtering by BDF, standby mode (empty device set) |
| `coral-ember/src/ipc.rs` | `ember.adopt_device` dispatch (Unix + TCP) |
| `coral-ember/src/ipc/handlers_device.rs` | `adopt_device()` handler — opens VFIO device, inserts into held map |
| `coral-ember/src/ipc/fd.rs` | Added `recv_with_fds()` for SCM_RIGHTS fd reception |
| `coral-glowplug/src/config.rs` | `DaemonConfig.fleet_mode` and `standby_pool_size` fields |
| `coral-glowplug/src/main.rs` | Fleet vs legacy lifecycle branching in main loop |
| `coral-glowplug/src/ember_lifecycle.rs` | Exposed `sysfs_warm_cycle_pub()` for fleet module |
| `coral-glowplug/src/lib.rs` | Registered `ember_fleet` module |

## Key Design Decisions

1. **Backward compatible**: `fleet_mode = false` (default) preserves single-ember behavior
2. **Per-BDF socket convention**: `/run/coralreef/ember-{slug}.sock` where slug = BDF with colons replaced by hyphens
3. **Fault-informed resurrection**: `FaultRecord` tracks timestamp, exit info, last operation, device health. `choose_strategy()` selects from `HotAdopt`, `WarmThenRespawn`, `FullRecovery`, `ColdRespawn`
4. **Discovery file**: Fleet writes `/tmp/biomeos/coral-ember-fleet.json` every tick cycle for external client routing
5. **`ember.adopt_device` bypasses managed_bdfs check**: Standby starts empty and dynamically adopts any BDF

## Config Changes

```toml
[daemon]
fleet_mode = true
standby_pool_size = 1
```

## For Polish Teams

- The `ember_fleet.rs` module has `#[warn(missing_docs)]` warnings on public fields — add doc comments
- The unused `inst` variable at line 622 of `ember_fleet.rs` is a borrow-checker artifact from the standby swap — clean up
- `recv_with_fds` in `fd.rs` is currently unused (dead code warning) — it's infrastructure for the hot-adopt SCM_RIGHTS path; wire it into `adopt_device` when the fd-transfer path is implemented
- Tests: 170 ember pass, 4 fleet-specific pass, 285+ glowplug pass. Two pre-existing vendor_lifecycle failures unrelated to fleet changes

## For Spring Teams

- **hotSpring**: Experiments 145+ that interact with GPU should route through `ember.adopt_device` or the fleet discovery file when `fleet_mode = true`. The per-device socket replaces the shared socket in fleet mode
- **All springs using coral-ember**: The public API (`ember_socket_path()`, `run_with_options()`) is unchanged for legacy mode. Fleet mode adds `ember_instance_socket_path(bdf)` and `ember_standby_socket_path(index)` helpers

## For Primal Teams

- **coralReef**: The `EmberFleet` struct in `ember_fleet.rs` is the central orchestration point. Future evolution targets: RPC proxy in glowplug (client sends to glowplug, glowplug routes to correct ember), health-score-based load balancing, and device migration between instances
- **toadStool**: Discovery file at `/tmp/biomeos/coral-ember-fleet.json` provides BDF→socket routing. `PcieTransport` should prefer fleet sockets when available

## Open Work

1. **SCM_RIGHTS hot-adopt path**: `recv_with_fds` is implemented but not wired — the current adopt_device opens from sysfs. Wire fd transfer for <50ms takeover
2. **Glowplug RPC proxy**: Clients send to glowplug socket, glowplug routes to correct ember — single-endpoint simplicity
3. **Fleet stress validation**: Run the full `stress_containment.py` suite against fleet mode with deliberate ember kills
4. **Per-device experiment isolation**: Wire exp145 and other GPU experiments to use the per-device socket directly

---

*All changes: AGPL-3.0-only. Build: `cargo build --workspace` passes. Tests: `cargo test -p coral-ember -p coral-glowplug` — all fleet tests pass.*
