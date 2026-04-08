# biomeOS V2.79 — ludoSpring V35 Gap Resolution + Deep Debt Evolution

**Date**: March 30, 2026
**Scope**: P0 primal auto-discovery, P2 graph separation + continuous executor, P3 health endpoints, deep debt sweep
**Tests**: 5,700+ passing (0 failures) across 26 workspace crates
**Blocking debt**: 0

---

## Critical Gap Resolution (from ludoSpring V35 experiments)

### P0: Primal Auto-Discovery — RESOLVED

ludoSpring V35 discovered that running primals (beardog, toadStool, coralReef, songbird, squirrel) were invisible to the Neural API. `capability.list` returned only 5 bootstrap entries; `capability.call` for compute/ai/visualization/dag/security all failed.

**Solution**: Three convergent registration paths, all feeding the same `NeuralRouter`:

1. **Startup auto-discovery** — biomeOS scans `$XDG_RUNTIME_DIR/biomeos/` for `.sock` files, probes each via `capabilities.list` JSON-RPC, registers results. No startup ordering dependency.
2. **`capability.register` / `route.register`** — Already existed. Primals (or external systems) call these methods to register capabilities with any transport endpoint (Unix, TCP, HTTP).
3. **`topology.rescan`** — NEW. On-demand re-discovery for existing-system adaptation. Deploy biomeOS into a running environment, call `topology.rescan`, and all reachable primals are registered.

### P2: Nucleus vs. Runtime Graph Separation — RESOLVED

ludoSpring exp087 tried `graph.execute` with a composition TOML. biomeOS looked in `graphs/` and failed because consumer compositions don't belong alongside built-in graphs.

**Solution**: `GraphHandler` now manages two directories:
- `graphs/` — nucleus graphs (bootstrap, health, routing) — built-in
- `runtime_graphs/` — consumer compositions via `graph.save` API
- `resolve_graph_path()` searches runtime first, then nucleus
- `graph.list` returns `"tier": "runtime"` or `"tier": "nucleus"` per graph

### P2: Continuous Executor Wiring — RESOLVED

`graph.start_continuous` session lifecycle worked but node execution was a placeholder. ludoSpring exp088 needs 60Hz tick rate with capability routing.

**Solution**: Node executor closure now:
- Extracts `capability` from `GraphNode`
- Resolves provider via `NeuralRouter::get_capability_providers`
- Forwards JSON-RPC request via `router.forward_request`
- Handles optional nodes as `"degraded"`, required nodes propagate errors

### P3: Health Endpoints — RESOLVED

`health.liveness` missing per SEMANTIC_METHOD_NAMING_STANDARD.

**Solution**: Added `health.check`, `health.liveness`, `health.readiness` to Neural API routing table with full implementations.

---

## Deep Debt Evolution

| Category | Before | After |
|----------|--------|-------|
| `unused_async` warnings | 66 | 24 |
| `#[allow()]` instances | 3 | 0 (all `#[expect()]` with reason) |
| Non-Linux disk.rs | Placeholder (zeros) | Real `statvfs` via rustix |
| Clippy pedantic warnings | 1804 | 1127 |
| Production mocks | 0 | 0 (confirmed — all in test code) |
| TODO/FIXME/HACK | 0 | 0 (confirmed) |
| `todo!()`/`unimplemented!()` | 0 | 0 |
| Hardcoded primals | Constants in `primal_names.rs` | Same (correct pattern) |
| Hardcoded ports | Env-driven with defaults | Same (correct pattern) |
| Unsafe code | 2 (test-utils, mutex-guarded) | Same (Rust 2024 requirement) |
| C dependencies | 0 | 0 |
| Files >1000 LOC | 0 | 0 |

---

## Files Modified

### New methods
- `crates/biomeos-atomic-deploy/src/neural_api_server/routing.rs` — `TopologyRescan`, `HealthCheck`, `HealthLiveness`, `HealthReadiness` routes
- `crates/biomeos-atomic-deploy/src/neural_api_server/server_lifecycle.rs` — `rescan_primals()`, `health_check()`, `health_liveness()`, `health_readiness()`, `discover_and_register_primals()`, `probe_primal_capabilities()`
- `crates/biomeos-atomic-deploy/src/handlers/graph.rs` — `runtime_graphs_dir`, `resolve_graph_path()`, nucleus/runtime list separation, continuous executor wiring

### Evolved to sync
- `UniversalBiomeOSManager::new()`, `::with_default_config()`, `::initialize()`, `::start_monitoring()`, `::shutdown()`
- `PrimalDiscoveryService` methods (`probe_endpoint`, `discover_registry`, `discover_multicast`, etc.)
- `MetricsCollector` methods (pure redb I/O)
- Boot/deploy/federation helpers (FS-only operations)
- ~50+ call sites updated across entire workspace

### Root docs
- `README.md` — Updated to V2.79, corrected test counts, added auto-discovery/rescan to discovery row
- `CHANGELOG.md` — Added V2.79 entry

---

## Positive Signals

- **Sub-millisecond UDS latency confirmed** by ludoSpring exp088 — well within 16ms budget for 60Hz composition
- **Graph infrastructure is real** — `graph.execute`, `graph.execute_pipeline`, `graph.start_continuous` are all implemented and wired
- **Registration and discovery are symmetric** — any combination of auto-discovery, manual registration, and on-demand rescan produces the same router state
- **5,700+ tests, 0 failures** — deep debt evolution did not break existing functionality

---

## Remaining Items

| Item | Priority | Notes |
|------|----------|-------|
| `# Errors` doc sections | Low | 646 clippy warnings for missing `# Errors` — documentation-level, not functional |
| `unused_async` (24 remaining) | Low | Functions that spawn async blocks internally — structurally correct |
| 7 `#[deprecated]` markers | Low | In `biomeos-ui/primal_client.rs` and `biomeos-primal-sdk/discovery.rs` — have migration notes |
| `biomeos-api` flaky test | Low | `test_discover_all_primals_nonexistent_dir` — environment race in parallel test execution, passes in isolation |
