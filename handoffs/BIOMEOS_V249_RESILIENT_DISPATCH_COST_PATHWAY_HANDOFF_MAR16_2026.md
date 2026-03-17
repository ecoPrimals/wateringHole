# biomeOS v2.49 — Resilient Dispatch + Cost-Aware Pathway Learner

**Date**: 2026-03-16
**Author**: biomeOS agent
**Previous**: v2.48 Cross-Ecosystem Absorption + Capability Registry Evolution
**Status**: All tests pass (5,161+), 0 clippy warnings, 0 files >1000 LOC

---

## Summary

This session executed deep debt solutions absorbed from the ecosystem review:
circuit-breaker protected RPC dispatch, cost-aware PathwayLearner optimization,
health liveness/readiness capability domain, and manifest-based primal discovery.

## Changes Executed

### 1. Circuit Breaker in Neural Executor (from healthSpring V32 + coralReef Iter 52)

- **`biomeos-core/src/retry.rs`**: Added `CircuitBreaker::execute<F,Fut,T,E>()` —
  generic-error circuit breaker method that works natively with `anyhow::Error`.
  `call()` now delegates to `execute()` internally.
- **`biomeos-atomic-deploy/src/executor/context.rs`**: Added per-primal
  `circuit_breakers: Arc<Mutex<HashMap<String, Arc<CircuitBreaker>>>>` with
  lazy `get_circuit_breaker(primal)` accessor.
- **`biomeos-atomic-deploy/src/neural_executor.rs`**: Both `node_rpc_call` and
  `node_capability_call` now wrap RPC operations in `breaker.execute()`. After
  5 consecutive failures to a primal, subsequent calls fail fast for 30s.

### 2. Cost-Aware Pathway Learner (from groundSpring V112 + neuralSpring S161)

- **`biomeos-graph/src/node.rs`**: Added `cost_estimate_ms: Option<u64>` and
  `operation_dependencies: Vec<String>` to `GraphNode`.
- **`biomeos-atomic-deploy/src/neural_graph.rs`**: Same fields on the atomic-deploy
  `GraphNode`. `convert_deployment_node()` extracts both from TOML.
- **`biomeos-graph/src/pathway_learner.rs`**: Two new optimization strategies:
  - `find_reorder_candidates()` — moves expensive (>100ms) nodes with no dependents
    to earlier phases for I/O overlap.
  - `find_cache_candidates()` — identifies pure nodes (no `operation_dependencies`,
    >99% success, >10 runs) for output caching.

### 3. Health Domain in Capability Registry (from healthSpring V32 + rhizoCrypt S16)

- **`config/capability_registry.toml`**: Added `[domains.health]` as the 25th domain.
  5 translations: `health.liveness`, `health.readiness`, `health.check`,
  `health.metrics`, `health.status`. Provider = `"*"` (every primal should implement).
- Registry grows to 285+ translations across 25 domains.

### 4. Manifest-Based Primal Discovery Fallback (from petalTongue iter-7)

- **`biomeos-core/src/socket_discovery/result.rs`**: Added `PrimalManifest` struct
  (serde) and `DiscoveryMethod::Manifest` variant.
- **`biomeos-core/src/socket_discovery/engine.rs`**: Added `discover_via_manifest()`
  method. Checks `$XDG_RUNTIME_DIR/ecoPrimals/manifests/{primal}.json` then
  `/tmp/ecoPrimals/manifests/{primal}.json`. Verifies socket connectivity.
- Inserted between family-tmp and capability-registry in both discovery chains.
- Works without Neural API — essential for bootstrap and single-primal deployments.

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 5,159 | 5,161+ |
| Clippy warnings | 0 | 0 |
| Capability domains | 24 | 25 |
| Capability translations | 280+ | 285+ |
| Files >1000 LOC | 0 | 0 |
| Circuit breakers | 0 | per-primal in ExecutionContext |

## New Tests (14)

- `test_circuit_breaker_execute_generic_error`
- `test_circuit_breaker_execute_opens_on_failures`
- `test_circuit_breaker_execute_half_open_recovery`
- `reorder_detects_expensive_non_dependent_nodes`
- `reorder_ignores_cheap_nodes`
- `cache_detects_pure_high_success_nodes`
- `cache_ignores_nodes_with_operation_dependencies`
- `test_circuit_breaker_created_lazily`
- `test_circuit_breaker_per_primal`
- `test_circuit_breaker_shared_across_clones`
- `graph_node_cost_estimate_ms_from_toml`
- `graph_node_operation_dependencies_from_toml`
- `convert_deployment_node_carries_cost_estimate`
- `test_primal_manifest_serde_roundtrip`
- `test_primal_manifest_optional_fields`

## Remaining Evolution Paths

1. **Rollback strategy** — `GraphExecutor::rollback()` is still a placeholder
2. **PathwayLearner auto-apply** — suggestions are generated but not auto-applied
3. **Manifest writer SDK** — primals don't yet write manifests at startup
4. **RetryPolicy per-node** — `Constraints::retry` exists but isn't wired to `RetryPolicy::execute()`
5. **Cost estimate collection** — `cost_estimate_ms` is declared in TOML but not yet auto-learned from metrics
