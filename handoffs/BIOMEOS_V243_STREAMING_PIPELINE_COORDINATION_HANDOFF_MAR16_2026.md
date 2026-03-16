# biomeOS v2.43 — Streaming Pipeline Coordination

**Date**: March 16, 2026
**From**: biomeOS
**To**: All primals and springs
**Status**: SHIPPED

---

## Summary

biomeOS v2.43 adds **Pipeline coordination** — the fifth and final execution pattern.
Graphs with `coordination = "pipeline"` wire nodes with bounded `tokio::sync::mpsc`
channels, enabling true streaming: items flow through the pipeline as soon as each
node produces them, without waiting for the entire upstream phase to complete.

This is an **evolution step for all primals**. The NDJSON framing that already
underlies all IPC naturally supports streaming — a primal that produces a stream
simply writes multiple response lines. No new protocol is needed.

---

## Five Coordination Patterns (Complete)

| Pattern | JSON-RPC Method | Data Flow | Use Case |
|---------|----------------|-----------|----------|
| Sequential | `graph.execute` | Phase-by-phase, dependency order | Deployment, setup |
| Parallel | `graph.execute` | Independent nodes concurrently | Health checks, batch ops |
| ConditionalDag | `graph.execute` | DAG with `condition`/`skip_if` | Branching workflows |
| **Pipeline** | `graph.execute_pipeline` | **Streaming mpsc channels** | **ETL, telemetry, FASTQ, pharmacology** |
| Continuous | `graph.start_continuous` | Fixed-timestep tick loop | Game engines, simulations, monitoring |

---

## What Changed (v2.43)

### PipelineExecutor (`biomeos-graph::pipeline`)

- Each node in a Pipeline graph runs as an independent tokio task
- Nodes connected by bounded `mpsc::channel<StreamItem>` (default capacity 64)
- Source node (first in chain) is re-called with `Data(Null)` until it returns `End`
- Transform nodes process items one-at-a-time from their input channel
- `StreamItem` envelope: `Data(Value)`, `End`, `Error { node_id, message }`
- Per-node throughput: `items_processed`, `items_errored`, `avg_item_ms`
- Backpressure: bounded channels prevent fast producer from overwhelming slow consumer

### AtomicClient Streaming (`biomeos-core`)

- New `call_stream()` method: sends one JSON-RPC request, reads multiple NDJSON lines
- Returns `mpsc::Receiver<StreamItem>` — consumer reads items as they arrive
- Works over all transports: Unix sockets, TCP, abstract sockets
- Backward-compatible: single-response primals work through same path

### JSON-RPC 2.0 Notification Compliance

- Server now correctly skips responses for notifications (requests with no `id`)
- Per JSON-RPC 2.0 Section 4.1
- Enables fire-and-forget patterns (telemetry push, event broadcasting)

### Graph Handler Integration

- `graph.execute_pipeline` / `neural_api.execute_pipeline` — new JSON-RPC method
- `graph.execute` auto-redirects Pipeline graphs
- Pipeline nodes route through capability translation registry → NeuralRouter
- Returns full `PipelineResult` with per-node throughput

### Sample Pipeline Graphs

- `streaming_telemetry_pipeline.toml` — groundSpring sensor → filter → store (3 nodes)
- `pharmacology_etl_pipeline.toml` — compound fetch → descriptors → Lipinski → docking (4 nodes)

---

## How Springs Use Pipeline Coordination

### Writing a Pipeline Graph

```toml
[graph]
id = "my-spring-pipeline"
name = "My Spring ETL Pipeline"
version = "1.0.0"
coordination = "pipeline"

[[graph.nodes]]
id = "source"
name = "Data Source"
capability = "my_domain.fetch_data"
required = true

[[graph.nodes]]
id = "transform"
name = "Transform"
capability = "my_domain.process"
depends_on = ["source"]
required = true

[[graph.nodes]]
id = "sink"
name = "Store Results"
capability = "storage.store"
depends_on = ["transform"]
required = true
```

### Supporting Streaming in Your Primal

A primal that produces a stream writes multiple NDJSON lines per request:

```
Client sends:  {"jsonrpc":"2.0","method":"my_domain.fetch_data","params":{...},"id":1}\n
Server writes: {"type":"Data","payload":{"record":1}}\n
Server writes: {"type":"Data","payload":{"record":2}}\n
Server writes: {"type":"Data","payload":{"record":3}}\n
Server writes: {"type":"End"}\n
```

The `AtomicClient::call_stream()` on the consumer side reads each line as a `StreamItem`.

For primals that return a single result, no changes are needed — the standard
JSON-RPC response is automatically wrapped as `Data` + `End`.

### Optional Nodes (`fallback = "skip"`)

Pipeline nodes with `fallback = "skip"` are optional — if they error or timeout,
the pipeline continues with the next item instead of failing:

```toml
[[graph.nodes]]
id = "optional-enrichment"
capability = "expensive.enrichment"
depends_on = ["core-transform"]
fallback = "skip"
budget_ms = 2000
```

---

## biomeOS Role: The Composition Primal

biomeOS is functionally the **composition primal** — the super-service that orchestrates
all other primals. While it sits at the same level as other primals (sovereign,
self-contained, JSON-RPC first), its unique role is:

1. **Neural API**: Routes capability calls between primals based on semantic names
2. **Graph Execution**: Orchestrates multi-primal workflows via TOML graphs
3. **Five Coordination Patterns**: Sequential, Parallel, ConditionalDag, Pipeline, Continuous
4. **Capability Discovery**: Runtime discovery — primals register, consumers discover
5. **Niche Deployment**: Composes primals into deployable biomes (BYOB)
6. **Lifecycle Management**: Monitors, resurrects, coordinates shutdown

Springs and primals **never embed each other's code**. They communicate through
capability-based JSON-RPC. biomeOS composes them into systems.

---

## Quality

| Metric | Value |
|--------|-------|
| Tests | 4,224 passed, 0 failed, 28 ignored |
| Clippy | Clean (workspace) |
| Fmt | Clean |
| Deploy Graphs | 40 total (+ 2 Pipeline) |
| Capability Domains | 19 |
| Translations | 260+ |

---

## What Primals Should Do

1. **No action required** for primals that return single responses — everything is backward-compatible
2. **For streaming**: Write multiple NDJSON lines per request (see above)
3. **Register capabilities** with `capability.register` so Pipeline graphs can discover you
4. **Test Pipeline graphs** that use your capabilities: `graph.execute_pipeline {"graph_id": "..."}`
5. **Consider `fallback = "skip"`** for expensive optional enrichment steps
