# cellMembrane Wave 150x — Crash-Loop Breaker + nestgate Unit Fix

**Date:** 2026-07-24
**Wave:** 150x
**Author:** cellMembrane (sporeGate)
**Posture:** SERVICE CRASH-LOOP DIVERGENCE RESOLVED

---

## Context

Wave 150x revealed a systemd crash-loop divergence on eastGate:

| Service | Restarts | Rate | Cause |
|---------|----------|------|-------|
| `membrane-nucleus@nestgate` | 17,920+ | every 3s | Binary CLI evolved — `--socket` flag rejected (exit 2) |
| `biomeos-beacon` | 11,161+ | every 5s | Binary doesn't exist (exit 203) |

Combined ~890 restarts/hour ran for 15+ hours undetected. AT&T gateway throttled
eastGate for excessive outgoing connections from the rapid spawn churn.

**Root cause:** No primal detected or intervened. `Restart=always` + `RestartSec=3`
ran indefinitely with no crash-loop detection, no CLI contract validation, and no
resource anomaly detection.

---

## Deliverables

### 1. Crash-Loop Breaker (P0)

**Types** (`cellmembrane-types/src/process.rs`):
- `CrashLoopAction` enum: `Disabled`, `Logged`, `FailedToDisable`
- `CrashLoopEntry` struct: unit, restart_count, sub_state, action
- `CrashLoopReport` struct: loops, threshold, scanned + methods (`has_loops`, `disabled_count`)
- `CRASH_LOOP_RESTART_THRESHOLD` constant: 5 (default)

**Implementation** (`membrane-shadow/src/gate/crash_loop.rs`):
- `scan_and_break()` — sync variant for bootstrap/preflight contexts
- `scan_and_break_async()` — async variant for cascade/temporal contexts
- `scan_only()` — dry-run (report only, no disable)
- `discover_membrane_units()` — filters `systemctl list-units` by service registry
- `query_unit_restart_info()` — parses `NRestarts` and `SubState` via `systemctl show`
- `disable_unit()` / `disable_unit_async()` — `systemctl stop + disable`
- `format_report()` — human-readable summary

**Dispatch** (`membrane-shadow/src/dispatch/gate.rs`):
- New command: `membrane gate.crash-loop [--dry-run] [--threshold N]`
- Returns `CrashLoopReport` as JSON data with formatted summary

**Integration points:**
- `gate.status` health probes — adds `service.crash-loop` probe (scan_only)
- `temporal.cascade` post-sync — scans after restart, auto-disables crash-looping services

### 2. nestgate Service Unit Fix (P0)

**Problem:** nestgate binary CLI evolved and no longer accepts `--socket` flag.
Service template generated `ExecStart=/opt/membrane/nestgate server --socket /path`
which exits 2 on every attempt.

**Fix:**
- Added `ServerContract::ServerNoSocket` variant — generates `ExecStart=.../binary server`
  (socket path via env var / convention)
- Updated nestgate registry entry: `SocketOnly` → `ServerNoSocket`
- Updated sporePrint unit template: passes socket path via `NESTGATE_SOCKET` env var
- Updated tests to assert `--socket` is NOT present in nestgate units

---

## Changed Files

| File | Change |
|------|--------|
| `cellmembrane-types/src/process.rs` | `CrashLoopAction`, `CrashLoopEntry`, `CrashLoopReport`, threshold const, tests |
| `cellmembrane-types/src/lib.rs` | Re-export crash-loop types |
| `cellmembrane-types/src/service/mod.rs` | `ServerContract::ServerNoSocket` variant |
| `cellmembrane-types/src/service/registry.rs` | nestgate: `SocketOnly` → `ServerNoSocket` |
| `membrane-shadow/src/gate/crash_loop.rs` | **NEW** — crash-loop breaker module |
| `membrane-shadow/src/gate/mod.rs` | Register `crash_loop` module |
| `membrane-shadow/src/gate/health.rs` | Integrate crash-loop probe into `gate.status` |
| `membrane-shadow/src/gate/sporeprint.rs` | nestgate unit: `--socket` → env var |
| `membrane-shadow/src/dispatch/gate.rs` | `gate.crash-loop` command dispatch |
| `membrane-shadow/src/temporal/post_sync.rs` | Post-cascade crash-loop scan |
| `membrane-shadow/src/gate/nucleus.rs` | RestartSec=3→5, add StartLimitBurst |
| `membrane-shadow/src/provision/bootstrap.rs` | Restart=always→on-failure, burst limits |
| `deploy/systemd/*.service` (7 files) | Restart=always→on-failure, burst limits |
| `deploy/systemd/user/membrane-nucleus-nosocket@.service` | **NEW** — ServerNoSocket template |

---

### 3. Systemd Restart=always Elimination (deep debt)

**Problem:** All systemd units used `Restart=always` + `RestartSec=3`, the exact
configuration that caused 17,920 restarts in 15 hours.

**Fix:** All units (code-generated and deploy templates) hardened:
- `Restart=always` → `Restart=on-failure` (only restart on non-zero exit)
- `RestartSec` standardized to 5s (was 3s in many places)
- Added `StartLimitIntervalSec=120` + `StartLimitBurst=10` (max 10 restarts per 2 min)

**Scope:** 12 files changed — 5 Rust-generated unit templates, 7 deploy templates.
Also added `membrane-nucleus-nosocket@.service` for `ServerNoSocket` primals.

---

## Health Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,146 (was 1,136) |
| Clippy warnings | 0 |
| `cargo fmt` drift | 0 |
| Production `unwrap()` | 0 |
| `unsafe` blocks | 0 (`#![forbid(unsafe_code)]`) |
| Files >800L | 2 (gateway.rs 833, harvest.rs 804 — structurally sound) |
| `Restart=always` units | 0 (was 8+ across codebase) |
| Disk reclaimed | 2.2 GiB (cargo clean) |

---

## For Upstream Teams

| Item | Owner | Action |
|------|-------|--------|
| biomeos-beacon service unit | biomeOS (flockGate) | Point to depot binary or disable until built |
| skunkBat process spawn rate anomaly | skunkBat (flockGate) | ThreatDetector category for rapid restarts |
| CLI contract validation | cellMembrane | Future: test depot binaries against unit args before deploy |
| Outbound connection monitoring | skunkBat | Future: detect anomalous outgoing connection rates |
