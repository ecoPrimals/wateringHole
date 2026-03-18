# primalSpring v0.3.1 — Full Atomics + Cross-Spring Wiring

**Date:** March 18, 2026
**Scope:** Server dispatch completion, per-tier deploy graphs, Squirrel + petalTongue wiring, BYOB template
**Tests:** 222 passing | clippy -D warnings clean | cargo fmt clean

## Summary

primalSpring now has complete server dispatch for all 22 registered capabilities. Every method in `capability_registry.toml` has a corresponding handler in the JSON-RPC server. Per-tier deploy graphs match `AtomicType::graph_name()` references, resolving the gap where graph names existed in code but no TOML files backed them. Cross-spring experiments for Squirrel (MCP tool discovery) and petalTongue (Grammar of Graphics visualization) are wired to degrade gracefully when primals are offline and exercise full IPC when live.

## New Server Dispatch Methods

| Method | Handler | Description |
|--------|---------|-------------|
| `identity.get` | inline | sourDough compliance: id, display_name, version, capabilities, phase, family_id |
| `coordination.probe_primal` | `handle_probe_primal` | Probe single primal health via socket discovery |
| `coordination.deploy_atomic` | `handle_deploy_atomic` | Validate deploy graph + composition for atomic tier |
| `coordination.bonding_test` | `handle_bonding_test` | Test multi-gate bonding readiness |
| `composition.tower_health` | `handle_composition_health(Tower)` | Tower atomic health aggregation |
| `composition.node_health` | `handle_composition_health(Node)` | Node atomic health aggregation |
| `composition.nest_health` | `handle_composition_health(Nest)` | Nest atomic health aggregation |
| `composition.nucleus_health` | `handle_composition_health(FullNucleus)` | Full NUCLEUS health aggregation |
| `nucleus.start` | `handle_nucleus_lifecycle("start")` | Queue NUCLEUS start via deploy graph |
| `nucleus.stop` | `handle_nucleus_lifecycle("stop")` | Queue NUCLEUS stop via deploy graph |
| `capability.list` | alias for `capabilities.list` | biomeOS standard alias |

## Per-Tier Deploy Graphs

| Graph | File | Nodes |
|-------|------|-------|
| Tower Atomic | `graphs/tower_atomic_bootstrap.toml` | BearDog → Songbird → Validate |
| Node Atomic | `graphs/node_atomic_compute.toml` | Tower + ToadStool → Validate |
| Nest Atomic | `graphs/nest_deploy.toml` | Tower + NestGate → Validate |
| Full NUCLEUS | `graphs/nucleus_complete.toml` | Tower + Provenance Trio + Node + Nest + Squirrel + primalSpring |

All graphs use `health.liveness` probes, `by_capability` routing, and `sequential` coordination.

## Cross-Spring Wiring

### Squirrel (exp044)
- Discovery + health probe
- `mcp.tools.list` → tool count + tool names
- `system.status` → system health routing
- `tool.list` → available tools inventory
- Graceful skip when Squirrel offline

### petalTongue (exp043)
- Discovery + health probe + capability check
- `visualization.render.grammar` → Grammar of Graphics atomic health bar chart
- `visualization.render.dashboard` → multi-panel topology dashboard
- Graceful skip when petalTongue offline

## BYOB Graph Template

`graphs/spring_byob_template.toml` — copy-and-customize template for any spring graduating to a full atomic primal. Includes:
- Tower Atomic base (always required)
- Commented optional extensions (compute, storage, AI, visualization)
- Spring node placeholder with capability routing
- Validation node
- sourDough compliance checklist

## Refactoring

- Extracted `parse_atomic_type()` and `error_response()` helpers to eliminate repetitive match/error boilerplate across handlers
- Replaced verbose `match Some/None` patterns with `let...else` (clippy `manual_let_else`)
- Added `#[expect(clippy::too_many_lines)]` on `dispatch_request` with reason (table-driven dispatch reads better monolithic)

## What Other Springs Should Absorb

1. **BYOB graph pattern**: Copy `spring_byob_template.toml`, fill in domain capabilities
2. **Server dispatch completeness**: Every `capability_registry.toml` entry should have a handler
3. **Cross-spring graceful degradation**: Discover → probe → skip pattern for optional primals
4. **Composition health per-tier**: Springs that coordinate should expose per-tier health aggregation
5. **`identity.get`**: Required for sourDough compliance — every primal must implement this
