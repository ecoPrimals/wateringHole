# biomeOS v3.16 — primalSpring Phase 43 Gap Resolution + Deep Debt Cleanup

**Date**: April 15, 2026
**Primal**: biomeOS
**From**: biomeOS team
**Scope**: primalSpring downstream audit response (Phase 43), deep debt evolution

---

## primalSpring Audit Response (5/5 Gaps Resolved)

### Gap 1: Graph-level genetics tier declaration — IMPLEMENTED

- `GeneticsTier` enum with ordered variants: `None < Tag < MitoBeacon < Nuclear`
- Added `genetics_tier: Option<GeneticsTier>` to `GraphMetadata`
- Executor preflight validates tier and logs structured warning (ready for BearDog `genetics.tier_available` probe)
- `GeneticsTierValidationReport` in `ExecutionReport`
- `nucleus_complete.toml` → `genetics_tier = "nuclear"`
- `tower_atomic_bootstrap.toml` → `genetics_tier = "mito_beacon"`
- Tests: serde roundtrip, ordering, FromStr, TOML parsing, executor preflight report

### Gap 2: Tick-loop scheduling — CONFIRMED COMPLETE

Already implemented in prior sessions:
- `TickClock`: fixed-timestep accumulator, frame-skip protection, 60Hz default
- `ContinuousExecutor::run()`: per-node budget enforcement, feedback edges, timeout/fallback
- `graph.execute` auto-redirects to `start_continuous` for continuous coordination graphs
- Lifecycle: start/pause/resume/stop via `SessionCommand` channel + `TickCompleted` events

### Gap 3: Deploy class auto-resolution — IMPLEMENTED

- `AtomicComposition` enum: `Tower`, `Node`, `Nest`, `Nucleus`
- Added `composition: Option<AtomicComposition>` to `GraphMetadata`
- `DeploymentGraph::resolve_composition()` infers minimal composition from node capabilities:
  - ai/orchestration → Nucleus
  - storage/persistence → Nest
  - compute/gpu → Node
  - default → Tower
- Explicit `composition = "nucleus"` in TOML overrides inference
- Tests: explicit TOML, all 4 inference classes, mixed capability priority

### Gap 4: capability.call routing contract — IMPLEMENTED

- Spec: `specs/CAPABILITY_CALL_ROUTING_CONTRACT.md` (Route → Resolve → Forward)
- `RoutingPhase` enum with structured phase tracking
- `_routing_trace` in `capability.call` responses when `_routing_trace: true` in params
- Covers: cross-gate, Tower Atomic relay, translation, and direct routing paths
- Springs can now inspect routing decisions for debugging and observability

### Gap 5: async-trait migration — DOCUMENTED AS BLOCKED

72 instances remain — all are `dyn Trait` objects (`Arc<dyn SecurityProvider>`, etc.) requiring boxed futures. Migration requires architectural change. Lowest priority per audit.

---

## Deep Debt Cleanup

### Production file refactoring
- `capability.rs` 873 → 553 LOC (extracted `capability_call.rs` for Route→Resolve→Forward)

### Test file splits (3 files over 900L)
- `capability_tests.rs` 1005 → 481 + 236 + 312 (by handler group)
- `realtime_tests.rs` 965 → 503 + 474 (core vs handler tests)
- `action_handler_tests.rs` 939 → 407 + 536 (baseline vs socket integration)

### Hardcoded values → constants
- `production_tcp_bind_addr()` — `const fn` for TCP bind addresses
- New constants: `DEFAULT_STATSD_UDP_ENDPOINT`, `DEFAULT_ZIPKIN_HTTP_ENDPOINT`, `DEFAULT_REGISTRY_HTTP_URL`
- Named port constants: `ports::STATSD`, `ports::ZIPKIN_HTTP`, `ports::REGISTRY_HTTP`
- All production bind sites use `constants::` module
- All string-literal primal names → `primal_names::{BEARDOG, SONGBIRD, ...}` in translation_loader, primal_spawner, btsp_client

### Dependencies verified
- blake3 `pure` feature: `build.rs` short-circuits, no C compiled, `cc` not banned
- 0 unsafe blocks, 0 production mocks, 0 TODOs
- `cargo deny check` passes (18-crate ban list, advisories ok, licenses ok)

---

## Verification

| Gate | Status |
|------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --workspace --all-targets` | PASS (1 pre-existing pedantic warning) |
| `cargo doc --workspace --no-deps` | PASS |
| `cargo deny check` | PASS (advisories ok, bans ok, licenses ok, sources ok) |
| `cargo test --workspace` | **7,811 passed**, 0 failures, 113 ignored |
| Production files >800 LOC | **0** |

---

## Wire Contract Reference

- `specs/CAPABILITY_CALL_ROUTING_CONTRACT.md` — Route → Resolve → Forward semantics
- `primalSpring/docs/DISCOVERY_WIRE_CONTRACT.md` — biomeOS Neural API section
- `graphs/README.md` — dual-format ownership, 42 deploy graphs

## Key Files Changed

| File | Change |
|------|--------|
| `crates/biomeos-graph/src/graph.rs` | `GeneticsTier`, `AtomicComposition`, `GraphMetadata` extensions |
| `crates/biomeos-atomic-deploy/src/executor/types.rs` | `GeneticsTierValidationReport` |
| `crates/biomeos-atomic-deploy/src/neural_executor.rs` | Genetics preflight validation |
| `crates/biomeos-atomic-deploy/src/handlers/capability.rs` | Refactored to 553 LOC |
| `crates/biomeos-atomic-deploy/src/handlers/capability_call.rs` | Extracted call + translations |
| `crates/biomeos-atomic-deploy/src/handlers/capability_routing.rs` | `RoutingPhase`, trace builder |
| `crates/biomeos-types/src/constants/mod.rs` | New endpoint/port constants, `const fn` bind addr |
| `specs/CAPABILITY_CALL_ROUTING_CONTRACT.md` | New spec |
| `graphs/nucleus_complete.toml` | `genetics_tier = "nuclear"` |
| `graphs/tower_atomic_bootstrap.toml` | `genetics_tier = "mito_beacon"` |
