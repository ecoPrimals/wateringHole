<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.15 — BYOB Graph Coordination Handoff

**Date**: March 18, 2026
**Primal**: Squirrel (AI coordination)
**Domain**: `ai`
**License**: scyBorg (AGPL-3.0-only + ORC + CC-BY-SA 4.0)

## Summary

BYOB graph coordination sprint: Squirrel now speaks primalSpring's `[graph]` +
`[[graph.node]]` TOML format natively. Two BYOB deploy graphs define Squirrel's
niche composition. `graph.parse` and `graph.validate` RPC endpoints enable
primalSpring to send deploy graphs for introspection. Squirrel is ready to
participate in live NUCLEUS atomics and coordination validation.

## Changes

### Added

- **`NicheDeployGraph` / `NicheGraphMeta` / `NicheGraphNode`** — wire-compatible
  with primalSpring `deploy.rs` types; parse, validate, query capabilities
- **`graphs/squirrel_ai_niche.toml`** — Sequential niche: BearDog → Songbird →
  Squirrel → ToadStool → NestGate → petalTongue
- **`graphs/ai_continuous_tick.toml`** — 10 Hz continuous: AI dispatch → result
  aggregation → petalTongue visualization push
- **`graph.parse` / `graph.validate`** JSON-RPC handlers in `handlers_graph.rs`
- **3 consumed capabilities**: `coordination.validate_composition`,
  `coordination.deploy_atomic`, `composition.nucleus_health`
- **2 optional dependencies**: primalSpring (coordination), petalTongue (visualization)
- **10 new deploy graph tests** — compile-time TOML parsing, structural validation,
  capability queries, dependency detection, JSON roundtrip

### Impact on primalSpring

primalSpring's `primalspring_deploy.toml` node 8 (Squirrel) currently uses
`health_method = "ai.health"` — Squirrel does not expose `ai.health`. It exposes:
- `health.liveness` (lightweight, preferred)
- `health.readiness` (checks subsystems)
- `system.health` (full health report)

**Recommendation**: primalSpring should update node 8 to use `health_method = "health.liveness"`.

### Impact on petalTongue

Squirrel's `ai_continuous_tick.toml` includes a `viz_push` node that depends on
petalTongue's `visualization.render` + `visualization.render.stream` capabilities.
petalTongue already exposes these. This graph enables real-time AI → visualization
coordination when both are running.

## Quality Gate

| Metric | Value |
|--------|-------|
| Tests | 5,440 passing / 0 failures |
| Clippy | CLEAN (`pedantic + nursery + deny(warnings)`) |
| Formatting | `cargo fmt --check` passes |
| Unsafe | 0 in production |
| Exposed capabilities | 23 |
| Consumed capabilities | 32 |
| Dependencies | 6 (2 required, 4 optional) |
| BYOB deploy graphs | 2 (structurally validated at compile time) |

## Patterns Worth Adopting

1. **`NicheDeployGraph` types** — Any primal consuming primalSpring graphs should
   implement wire-compatible types rather than depending on primalSpring directly.
2. **`graph.parse` / `graph.validate` RPC** — Springs that participate in BYOB
   should expose graph introspection endpoints.
3. **Compile-time graph validation** — Use `include_str!` in tests to catch TOML
   drift at compile time, not at runtime.

## Next Steps Toward Full Atomics

1. **primalSpring**: Update Squirrel node `health_method` from `"ai.health"` to
   `"health.liveness"` in `primalspring_deploy.toml`
2. **primalSpring**: Wire `exp044_squirrel_ai_coordination` to call Squirrel's
   `graph.validate` with the niche graph
3. **petalTongue**: Wire `ai_continuous_tick.toml` as a validation experiment
4. **Live NUCLEUS**: Start BearDog + Songbird locally, run Squirrel server,
   have primalSpring's `validate_live()` probe all nodes
5. **biomeOS graph executor**: Eventually execute these graphs via `biomeos deploy`

## Dependencies

| Primal | Capabilities Used | Required |
|--------|-------------------|----------|
| BearDog | `crypto.*`, `auth.*`, `secrets.*`, `relay.*` | Yes |
| Songbird | `discovery.*` | Yes |
| ToadStool | `compute.*` | No |
| NestGate | `storage.*`, `model.*` | No |
| primalSpring | `coordination.*`, `composition.*` | No |
| petalTongue | `visualization.*`, `interaction.*` | No |
| rhizoCrypt | `dag.*` | No |
| sweetGrass | `anchoring.*`, `attribution.*` | No |
| Domain Springs | `mcp.tools.list`, `health.*` | No |
