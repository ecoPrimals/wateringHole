<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.4 — Spring Absorption Handoff

**Date**: March 16, 2026
**From**: Squirrel AI Primal
**Session**: Spring absorption review + execution

---

## Summary

Reviewed all 7 springs (hotSpring, groundSpring, neuralSpring, wetSpring,
airSpring, healthSpring, ludoSpring) for patterns to absorb. Pulled latest,
synced wateringHole handoffs, and executed 8 absorption items.

## Changes

### New Modules

- **`niche.rs`** — Niche self-knowledge (groundSpring/wetSpring/airSpring pattern)
  - `CAPABILITIES` (20 methods), `CONSUMED_CAPABILITIES` (14 external)
  - `COST_ESTIMATES`, `DEPENDENCIES`, `SEMANTIC_MAPPINGS`, `FEATURE_GATES`
  - JSON functions: `operation_dependencies()`, `cost_estimates_json()`, `semantic_mappings_json()`
  - `capability.discover` response now includes all niche data

- **`capabilities/songbird.rs`** — Songbird service mesh registration (wetSpring pattern)
  - `discover_socket()` — 3-tier fallback (env → XDG → /tmp)
  - `register()` — sends `discovery.register` with niche data
  - `start_heartbeat_loop()` — 30s `discovery.heartbeat`
  - Wired into main server startup alongside biomeOS lifecycle

- **`orchestration/deploy_graph.rs`** — Deployment graph types (ludoSpring exp054)
  - `DeploymentGraphDef`, `GraphNode`, `TickConfig` — wire-compatible
  - `execution_order()` with topological sort and cycle detection
  - `requires_squirrel()` — check if graph needs AI capabilities

- **`SocketConfig` in `unix_socket.rs`** — Injectable socket config (airSpring pattern)
  - `SocketConfig` struct with `from_env()` constructor
  - `_with` variants for all resolution functions
  - Tests without `temp_env` or `#[serial]`

### Workspace Lints

- `deny(clippy::expect_used, clippy::unwrap_used)` added to `[workspace.lints.clippy]`
- All 22 crates now inherit `[lints] workspace = true`
- Removed conflicting per-crate `[lints.clippy]` sections

### Testing

- **proptest** added — 10 round-trip tests for all JSON-RPC types + niche JSON
- `PartialEq` derived on all JSON-RPC request/response types
- Total tests: 4,552 (up from 4,465)

### Cleanup

- Fixed pre-existing doctests in `squirrel-mcp-auth` and `universal-error`
- Removed broken doc references (MODEL_SPLITTING_MOVED, unified-plugin-system)
- Deleted orphaned `run_examples.bat` (Windows-only)

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 4,465 | 4,552 (+87) |
| Niche self-knowledge | None | 20 caps, 14 consumed, costs, deps |
| Songbird registration | None | discovery.register + heartbeat |
| Property tests | 0 | 10 |
| Deployment graph types | None | DeploymentGraphDef + topo sort |
| SocketConfig DI tests | 0 | 8 |
| Workspace lint inheritance | 11/22 | 22/22 |
| deny(unwrap/expect) | No | Yes |

## Spring Patterns Absorbed

| Pattern | Source | Squirrel Module |
|---------|--------|-----------------|
| Niche self-knowledge | groundSpring, wetSpring, airSpring | `niche.rs` |
| deny(unwrap/expect) | hotSpring, groundSpring | `Cargo.toml` workspace lints |
| SocketConfig DI | airSpring | `unix_socket.rs` |
| capability.list with costs | airSpring, wetSpring, groundSpring | `jsonrpc_handlers.rs` |
| proptest round-trip | wetSpring, groundSpring | `tests/proptest_roundtrip.rs` |
| Songbird announcement | wetSpring, healthSpring | `capabilities/songbird.rs` |
| DeploymentGraphDef | ludoSpring exp054 | `orchestration/deploy_graph.rs` |

## Patterns Tracked (Not Yet Absorbed)

| Pattern | Source | When |
|---------|--------|------|
| Provenance tracking | hotSpring, wetSpring | When rhizoCrypt integration starts |
| Vault (consent-gated storage) | wetSpring | Phase 2 clinical data routing |
| PrecisionBrain / HardwareCalibration | hotSpring | ToadStool's domain |
| Composable raid orchestration | ludoSpring exp054-066 | When multi-primal compositions needed |

## Known Issues

1. Coverage at 66% — needs targeted expansion for cli, auth, mcp crates
2. Context methods use stub storage — NestGate integration planned
3. `test_load_from_json_file` flaky under full workspace (env var pollution)
4. reqwest 0.11 → 0.12 migration incomplete

## Sovereignty / Human Dignity

- All changes AGPL-3.0-only compliant
- Zero chimeric dependencies from springs (local protocol types only)
- No hardcoded primal names — capability-based discovery throughout
- Niche self-knowledge enables Pathway Learner without centralized control
