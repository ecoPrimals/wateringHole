# biomeOS v2.42 — Neural API Evolution Handoff

**Date**: March 15, 2026
**From**: biomeOS deep session (audit → execution → Neural API evolution)
**Status**: Implemented, tested, ready for push

---

## Summary

biomeOS v2.42 closes the critical Neural API gaps identified during the
v2.41 deep audit and whitepaper/implementation comparison. The five major
changes enable ludoSpring's RPGPT engine and cross-spring composition:

1. **Unified graph schema** — `[[nodes]]` and `[[graph.nodes]]` formats
   both parse into the same `Graph` type. ContinuousExecutor graphs
   (like `game_engine_tick.toml`) can now be loaded by the Neural API
   server alongside transactional graphs (like `rootpulse_commit.toml`).

2. **Continuous execution via JSON-RPC** — Four new methods
   (`graph.start_continuous`, `graph.pause_continuous`,
   `graph.resume_continuous`, `graph.stop_continuous`) expose the
   ContinuousExecutor for programmatic session management. Game sessions,
   dashboards, and audio pipelines can be started/paused/stopped via IPC.

3. **ConditionalDag execution** — Nodes with `condition` and `skip_if`
   fields are now evaluated before execution. In continuous graphs,
   conditions are checked per-tick, enabling optional primals (e.g.,
   Squirrel AI narration only when available).

4. **Tick-level fallback** — `fallback = "skip"` on graph nodes marks
   them as optional. Failures and timeouts on optional nodes are silently
   handled (debug log, no budget overrun) so the game loop continues.

5. **PathwayLearner wired** — Every graph execution now records per-node
   and per-graph metrics to redb. The PathwayLearner can analyze this
   data via `graph.suggest_optimizations` JSON-RPC to propose
   parallelization, prewarming, batching, caching, and reordering.

---

## Capability Registry

Three new domains added:
- `measurement.*` (groundSpring) — 21 translations
- `physics.*` (hotSpring) — 17 translations
- `health_extended` (healthSpring Track 6+7) — 11 translations

Total: 19 domains, 260+ capability translations.

---

## Test Results

- Library tests: 4,215 passed, 0 failed
- Binary tests: 285 passed, 0 failed
- Doc tests: 42 passed, 0 failed
- Clippy: PASS (workspace, 0 errors)
- Formatting: PASS (cargo fmt --check clean)

---

## What ludoSpring Needs Next

The RPGPT engine can now:
- Load `game_engine_tick.toml` via `graph.execute` or `graph.start_continuous`
- Use conditional nodes for optional AI narration
- Mark non-critical primals as `fallback = "skip"`
- Query optimization suggestions after enough execution data accumulates

Still needed for full RPGPT composition:
- **Mixed coordination**: transactional subgraphs (provenance commit)
  within continuous sessions (game loop). Currently separate execution
  paths — the continuous session must manually invoke a transactional
  graph at session boundaries.
- **Pipeline (streaming) coordination**: Not yet implemented. Useful for
  telemetry pipelines and pharmacology simulations.

---

## Whitepaper Docs Updated

- `neuralAPI/README.md` — Implementation status, emergent systems table
- `neuralAPI/SUMMARY.md` — Quick reference with five coordination patterns
- `neuralAPI/10_ROADMAP.md` — Phase tracking with spring readiness
- `RootPulse/README.md` — Cross-domain provenance patterns
