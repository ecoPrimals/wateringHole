# ludoSpring V16 — Composition Recipe Handoff

**Date:** April 3, 2026
**From:** ludoSpring V16
**To:** primalSpring, esotericWebb, all springs and gardens
**License:** AGPL-3.0-or-later

---

## Summary

V16 bridges the gap between "ludoSpring validates internally" and "gardens can
replicate this as a pattern." It adds a typed `deploy` module compatible with
primalSpring's `DeployGraph` TOML schema, a `deploy::recipe` module that codifies
the full wave-ordered composition validation cycle, and a reference experiment
(exp072) that demonstrates the pattern end-to-end.

This is the **replication bridge**: any spring or garden follows the same graph-driven
sequence to validate its own primal composition, without importing ludoSpring or
primalSpring code.

---

## What Changed

### Deploy Module (`barracuda/src/deploy/`)

New module with primalSpring-compatible types, independently implemented:

- `DeployGraph`, `GraphMeta`, `GraphNode` — same TOML schema, independent code
- `parse_graph()` / `load_graph()` — TOML → typed graph
- `validate_structure()` — name, deps, health methods, binary checks
- `topological_waves()` — Kahn's algorithm for startup ordering
- `graph_required_capabilities()`, `graph_spawnable_primals()` — introspection
- Tests that parse ludoSpring's own graphs and validate structure

### Composition Recipe (`barracuda/src/deploy/recipe.rs`)

Library-level API codifying the replicable pattern:

- `validate_composition(toml_str)` — full cycle: parse → validate → discover → walk → report
- `validate_composition_from_graph(graph)` — from already-parsed graph
- `CompositionReport` — per-node health status, capability satisfaction, readiness summary
- `NodeStatus` — wave, capability, discovered, healthy for each graph node

### exp072 — Composition Integration Runner

Reference experiment demonstrating the full pattern:

1. Parse and validate both tower and nucleated deploy graphs
2. Compute topological waves, verify biomeOS in wave 0
3. Walk waves: discover each node by `by_capability`, probe health
4. Run game science locally (20-tick session lifecycle)
5. Run game science over IPC (begin_session → evaluate_flow → session_state → complete_session)
6. Compare local vs IPC results for parity
7. Produce composition readiness report

### exp067 Upgrade

Upgraded from raw `toml::Value` parsing to typed `deploy::DeployGraph`. Now
validates structure, topological waves, required capabilities, and spawnable
primals using the deploy module API.

### `toml` Dependency

Added `toml = "0.8"` to `barracuda/Cargo.toml` (pure Rust, ecoBin compliant).

---

## The Replication Bridge

### How Springs Replicate

A sibling spring (e.g. hotSpring validating physics compositions):

1. Writes its own deploy graphs using the same TOML schema
2. Implements `DeployGraph`/`GraphNode` types (or copies from ludoSpring)
3. Calls `validate_composition()` to verify its composition
4. Substitutes its domain science for game science in step 6

### How Gardens Replicate

A garden (e.g. esotericWebb):

1. Already has deploy graphs (`graphs/webb_*.toml`) in the same format
2. Already has `PrimalBridge` for discovery and IPC
3. Can call `game.*` methods on ludoSpring via IPC (if running)
4. Falls back to local science modules (flow, engagement, DDA) if ludoSpring unavailable
5. Uses the same session lifecycle contract

### What esotericWebb Specifically Needs

- `niches/esoteric-webb.yaml` still lists ludospring as **required** but
  `bridge/domains.rs` doesn't route to it (GAP-016 superseded). Reconcile
  niche spec with actual V6 consumption pattern.
- `graphs/esotericwebb_full.toml` lists ludospring as a node — valid as optional
  composition, not a hard dependency.
- GAP-021 (game science primal) remains open. ludoSpring's IPC surface (`game.*`)
  is the candidate implementation. When ready, esotericWebb can route through
  `PrimalBridge` instead of local science.

---

## Gaps Surfaced

### For primalSpring

- ludoSpring now has independent `DeployGraph` types. Consider extracting graph
  types into a shared `deploy_schema` crate that both springs and gardens can
  depend on (optional — independent impls work, shared types reduce drift).
- `AtomicHarness` integration: ludoSpring experiments could spawn compositions
  using primalSpring's harness if a cross-spring test binary is built.

### For esotericWebb

- Reconcile `esoteric-webb.yaml` ludospring entry with V6 domains.rs routing.
- When GAP-021 is ready, wire `PrimalBridge` to `game.*` methods for flow,
  engagement, DDA over IPC.

### For barraCuda

- `exp068` validates local-vs-primal math parity but only runs when barraCuda
  primal is live. Consider adding this to CI integration tests.

---

## Stats

| Metric | Value |
|--------|-------|
| New files | 5 (deploy/mod.rs, deploy/recipe.rs, exp072, graphs/README update, this handoff) |
| Modified files | 5 (Cargo.toml ×2, lib.rs, exp067/main.rs, README.md) |
| LOC added | ~650 |
| New deploy module tests | 7 |
| New recipe tests | 2 |
| exp072 checks | ~25 (structural + wave + local + IPC + report) |
