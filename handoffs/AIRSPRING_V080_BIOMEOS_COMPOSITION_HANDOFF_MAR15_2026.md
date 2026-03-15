# airSpring V0.8.1 — biomeOS Composition + neuralAPI Integration Handoff

> **Date**: March 15, 2026
> **From**: airSpring
> **To**: biomeOS, rhizoCrypt, loamSpine, sweetGrass, NestGate, barraCuda, ToadStool
> **Status**: 847 lib + 41 integration, 41 capabilities, 4 deploy graphs, neuralAPI citizen

---

## Summary

airSpring v0.8.1 is the first Spring to implement the full Provenance Trio
integration pattern from `SPRING_PROVENANCE_TRIO_INTEGRATION_PATTERN.md`,
plus NestGate content-addressed caching, Cross-Spring Time Series v1 format,
biomeOS graph-based deployment, and **neuralAPI Pathway Learner integration**.

**Zero compile-time coupling** to trio crates. All interaction via biomeOS
`capability.call`. Graceful degradation when any partner is unavailable.

**neuralAPI citizen**: Emits structured metrics on every dispatch, declares
operation dependencies and cost estimates, reports composition status via
heartbeat. biomeOS can learn, optimize, and rewire.

---

## What We Implemented

### 1. Provenance Trio (`ipc/provenance.rs`)

- `begin_experiment_session()` → `capability.call("dag", "create_session", ...)`
- `record_experiment_step()` → `capability.call("dag", "append_event", ...)`
- `record_gpu_step()` — specialized DAG vertex for GPU shader chain tracking
- `complete_experiment()` → dehydrate → commit → attribute (three-phase)
- `is_available()` — runtime trio reachability check

### 2. NestGate Content-Addressed Routing (`NestGateProvider`)

Three-tier: NestGate cache → biomeOS capability → BiomeosProvider fallback.
Cache key format: `airspring:weather:{lat:.4}:{lon:.4}:{start}:{end}`.
Cached in Cross-Spring Time Series v1 for offline reproducibility.

### 3. Cross-Spring Time Series v1

`WeatherResponse::to_cross_spring_v1()` / `from_cross_spring_v1()`.
Schema: `ecoPrimals/time-series/v1`. Forward-compatible variable matching.

### 4. Primal Binary (41 capabilities)

New: `provenance.begin`, `provenance.record`, `provenance.complete`,
`provenance.status`, `capability.list`, `data.cross_spring_weather`.

### 5. Deploy Graphs (4 total)

- `airspring_provenance_pipeline.toml` — experiment with full provenance lifecycle
- `airspring_niche_deploy.toml` — 8-node niche (Tower + Trio + NestGate + ToadStool)
- `metalForge/deploy/airspring_deploy.toml` — updated with trio nodes
- Existing: eco pipeline + cross-primal soil microbiome

### 6. neuralAPI Pathway Learner Integration (v0.8.1)

- **Structured metrics**: Every dispatch emits `[metrics] primal_id=airspring operation=X latency_ms=Y success=Z`. When `BIOMEOS_METRICS_SOCKET` is set, active reporting via Unix socket.
- **Operation dependencies**: `capability.list` exposes what each method needs (e.g., `science.et0` requires `weather_data`). biomeOS auto-detects parallelization.
- **Cost estimates**: `capability.list` exposes typical latency_ms, cpu intensity, memory_bytes per operation. biomeOS scheduler optimizes resource allocation.
- **Domain registration**: Startup registers `ecology`, `provenance`, `data`, and `capability` domains with semantic mappings.
- **Heartbeat composition**: `lifecycle.status` includes provenance_trio/nestgate/toadstool availability for dynamic graph rewiring.
- **Graph evolution**: Provenance pipeline uses `ConditionalDag` coordination with `budget_ms` fields. Niche deploy includes Pathway Learner hints.

---

## What We Need from You

### rhizoCrypt / loamSpine / sweetGrass

- Validate that airSpring's capability.call arguments match your expected wire format
- Our `session_type` is `{"Experiment": {"spring_id": "airspring"}}`
- Our agent DID is `did:key:airspring` (placeholder — need real key generation)
- Test: start trio → call `provenance.begin` via airSpring primal → verify DAG created

### NestGate

- Validate `storage.get` / `storage.store` with our key format
- Test content-addressed deduplication with `airspring:weather:*` keys
- Verify JSON value round-trip for Cross-Spring Time Series v1 payloads

### biomeOS

- Execute `graphs/airspring_provenance_pipeline.toml` end-to-end
- Deploy `graphs/airspring_niche_deploy.toml` and verify startup order
- Consider evolving `airspring_provenance_pipeline.toml` into a generic
  `spring_provenance_experiment.toml` template for other Springs
- `capability.list` reports composition status, operation_dependencies, and cost_estimates — feed these to Pathway Learner
- Heartbeat includes composition status for dynamic graph rewiring
- Structured metrics emitted on every dispatch — scrape or listen on `BIOMEOS_METRICS_SOCKET`

### barraCuda / ToadStool

- No new requirements. GPU compute provenance tracks shader invocations in DAGs.
- Future: when ToadStool exposes `compute.provenance` capability, we can merge
  GPU execution traces with experiment DAGs automatically.

---

## Composition Patterns Validated

| Pattern | Reference | Status |
|---------|-----------|--------|
| Provenance Trio Integration | `SPRING_PROVENANCE_TRIO_INTEGRATION_PATTERN.md` | Implemented |
| Spring-as-Provider | `SPRING_AS_PROVIDER_PATTERN.md` | Implemented (ecology domain) |
| Cross-Spring Data Flow | `CROSS_SPRING_DATA_FLOW_STANDARD.md` | Implemented (time-series/v1) |
| Spring-as-Niche Deployment | `SPRING_AS_NICHE_DEPLOYMENT_STANDARD.md` | Implemented (niche deploy graph) |
| neuralAPI Primal Requirements | `07_PRIMAL_REQUIREMENTS.md` | Implemented (all 3 enhancements) |
| neuralAPI Graph Execution | `03_GRAPH_EXECUTION.md` | Implemented (ConditionalDag, budget_ms) |
| neuralAPI Pathway Learner | `06_BIOMEOS_IMPLEMENTATION.md` | Ready (metrics, deps, costs) |
