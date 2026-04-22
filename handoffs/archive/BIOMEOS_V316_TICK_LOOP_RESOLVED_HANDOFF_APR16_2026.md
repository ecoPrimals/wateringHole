# biomeOS v3.16 — Tick-Loop Scheduling: Resolved (primalSpring Response)

**Date**: April 16, 2026
**Primal**: biomeOS
**From**: biomeOS team
**To**: primalSpring
**Re**: "Tick-loop scheduling — 60Hz continuous composition budget. Currently one-shot only."

---

## Status: RESOLVED — Stale Audit Item

The primalSpring April 16 audit identifies tick-loop scheduling as "the single remaining major open item" and describes biomeOS as "one-shot execution only." This is **stale**. The tick-loop subsystem is implemented, wired into JSON-RPC routing, auto-redirected from `graph.execute`, and covered by 49 passing tests.

---

## Implementation Evidence

### TickClock (fixed-timestep accumulator)
- **File**: `crates/biomeos-graph/src/continuous.rs` lines 27–134
- Configurable via `TickConfig` (default 60 Hz, `target_hz: 60.0`)
- Accumulator with spiral-of-death protection (`max_accumulator` clamp)
- `advance()` drains full tick steps, warns on multi-tick skip

### ContinuousExecutor
- **File**: `crates/biomeos-graph/src/continuous.rs` lines 193–456
- `run()` loop: non-blocking `SessionCommand` recv → `TickClock::advance()` → per-tick node walk → per-node budget enforcement via `tokio::time::timeout`
- State machine: `Running` → `Paused` → `Running` → `Stopping` → `Stopped`
- Budget warning at `budget_warning_ms`, hard timeout at `2× budget`
- `GraphEvent` broadcasts: `SessionStarted`, `TickCompleted`, `SessionStateChanged`

### JSON-RPC Wiring
- **Routing table** (`neural_api_server/routing.rs` lines 161–168):
  - `graph.start_continuous` / `neural_api.start_continuous`
  - `graph.pause_continuous` / `neural_api.pause_continuous`
  - `graph.resume_continuous` / `neural_api.resume_continuous`
  - `graph.stop_continuous` / `neural_api.stop_continuous`
- **Handler**: `handlers/graph/continuous.rs` — loads TOML graph, validates `CoordinationPattern::Continuous`, spawns `ContinuousExecutor::run` on tokio, stores session for lifecycle control

### Auto-Redirect
- `graph.execute` checks `graph.is_continuous()` and redirects to `start_continuous` (`handlers/graph/execute.rs` lines 50–52)

### SessionCommand Lifecycle
- `Pause`, `Resume`, `Stop` sent via `mpsc` channel
- Handler dispatches to stored session `command_tx`
- Executor `try_recv` handles in main loop (non-blocking)

---

## Test Coverage: 49 Tests

### biomeos-graph (23 tests)
- TickClock: basic advance, multi-tick, accumulator clamp, reset, sleep-advance, Hz target match
- ContinuousExecutor: creation, stop, pause/resume, optional node skip, conditional node skip, feedback edges, budget parsing

### biomeos-atomic-deploy (26 tests)
- JSON-RPC level: start/pause/resume/stop success + error cases
- Session not found, missing params, wrong coordination type, invalid TOML
- Translation loading, status query, execute-redirects-continuous
- Graph branches: priority, basename resolution, missing session errors

All 49 tests **pass** (verified `cargo test` April 16, 2026).

---

## What Was "One-Shot Only" — Historical Context

The original `graph.execute` handler was sequential-only. The continuous subsystem was added across multiple sessions:
1. `TickClock` + `ContinuousExecutor` in `biomeos-graph`
2. `graph.start_continuous` handler + routing in `biomeos-atomic-deploy`
3. Auto-redirect from `graph.execute` for continuous coordination graphs
4. Parity fixes: translation loading, capability registration, routing aliases

The primalSpring checklist likely predates these additions.

---

## Remaining Open Items for biomeOS

| Item | Priority | Notes |
|------|----------|-------|
| `serde-saphyr` 0.0.x | Watch | Pre-1.0 semver; track releases |
| `rtnetlink` native subtree | Acceptable | Linux-specific, appropriate for RTNETLINK |
| `biomeos-types` tokio dep | Low | Transitively needed via tarpc |

**No major open items remain.**

---

**Tests**: 7,801 passing | **Continuous tests**: 49 passing | **Clippy**: 0 warnings | **async-trait**: eliminated | **Tick-loop**: fully implemented + wired
