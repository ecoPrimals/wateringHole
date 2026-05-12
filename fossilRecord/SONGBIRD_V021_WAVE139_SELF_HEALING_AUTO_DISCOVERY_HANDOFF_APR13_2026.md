# Songbird Wave 139 Handoff — Self-Healing Socket Auto-Discovery

**Primal**: Songbird (Network Orchestration & Discovery)  
**Version**: v0.2.1-wave139  
**Date**: April 13, 2026  
**Classification**: Polish — resolves primalSpring auto-discovery gap

---

## Problem

Socket auto-discovery (LD-08, Wave 138) scans biomeos socket directories and
registers discovered primals into the `ipc.resolve` / `capability.resolve`
registry at startup (Stage 2c). However, Songbird often starts before peer
primals — the initial scan finds no sockets, and the registry remains empty
until primals call `ipc.register` or the launcher manually seeds via Phase 5.

**primalSpring audit note**: "A periodic re-scan (e.g. every 30s) or
socket-watch (`inotify`) would make registration self-healing without launcher
assistance."

## Solution

Added a **periodic re-scan background task** (spawned in Stage 6) that re-runs
the socket auto-discovery scan every 30 seconds. Primals that appear after
Songbird starts are automatically registered within one interval.

### Implementation

- `SOCKET_RESCAN_INTERVAL_SECS = 30` — configurable constant
- `start_periodic_socket_rescan()` on `StartupOrchestrator`:
  - Clones `Arc<RwLock<ServiceRegistry>>` from the broker
  - Spawns `tokio::spawn` loop: `sleep(30s)` → `discover_and_register_biomeos_primals()`
  - Logs registrations at `info!` level, no-ops silently when nothing new appears
- `#[cfg(not(unix))]` no-op stub for portability
- Module doc on `socket_auto_discovery.rs` updated to describe both invocation paths

### Design Decision: Timer vs inotify

Timer-based (30s interval) chosen over `inotify` because:
1. **Portable** — works on any Unix, no Linux-specific dependency
2. **Simple** — no new crate dependency, 20 lines of code
3. **Sufficient** — 30s latency is acceptable; launcher Phase 5 still seeds
   immediately for startup-critical paths
4. **Resilient** — survives filesystem quirks (overlayfs, NFS, tmpfs race conditions)

`inotify` could reduce latency to sub-second but adds `notify` crate
dependency, platform-specific code paths, and complexity for marginal benefit.

## Verification

- `cargo check --workspace`: zero warnings
- `cargo clippy --workspace -- -D warnings`: zero warnings
- `cargo fmt --check`: clean
- `cargo doc --workspace --no-deps`: zero warnings
- `cargo test --workspace --lib`: 7,320 passed, 0 failed, 22 ignored

## Ecosystem Impact

### wetSpring PG-03 Status

wetSpring PG-03 ("Capability Discovery Is Name-Based — Blocked by: Songbird
implementing `capability.resolve`") is now **RESOLVED** by the collective
Songbird Waves 134/137b/138/139:

- Wave 134: `capability.resolve` single-step routing implemented
- Wave 137b: `ipc.resolve` accepts `capability` parameter (dual-mode)
- Wave 138: Socket auto-discovery seeds the registry at startup (LD-08)
- **Wave 139**: Periodic re-scan makes the registry self-healing

### primalSpring Stale Entries

The Songbird section in `primalSpring/docs/PRIMAL_GAPS.md` references Wave 133
and lists SB-03 (sled default-on) as open. Current state:

- SB-03 **FULLY RESOLVED** Wave 135 — sled completely eliminated, 1,482 lines deleted
- Songbird at Wave 139, 7,320 tests, Wire Standard L3, 67+ methods
- `capability.resolve` fully operational since Wave 134

---

*This handoff is filed to `ecoPrimals/infra/wateringHole/handoffs/` per the
NUCLEUS_SPRING_ALIGNMENT.md feedback protocol.*
