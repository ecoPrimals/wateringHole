# rhizoCrypt Wave 155n — G31 Batch Provenance Pipeline

**Date**: Aug 3, 2026 | **Wave**: 155n | **Head**: `0356187`

## Summary

G31 batch provenance pipeline foundation for rhizoCrypt. Adds batch-optimized
append, concurrent multi-session dehydration, and a coordinated pipeline ingest
method to support 10× faster bulk ingestion (38 datasets, PDB 220K structures).

## What Shipped

| Component | Change |
|-----------|--------|
| `append_vertices_batch()` | Single session lock for N vertices (amortized lock overhead) |
| `append_batch` RPC auto-routing | Same-session batches use optimized path automatically |
| `dehydrate_batch()` | Concurrent multi-session dehydration via JoinSet |
| `dag.dehydration.trigger_batch` | JSON-RPC + tarpc for batch dehydration |
| `dag.pipeline.ingest` | Coordinated create + batch append + optional dehydrate |
| `notify_dehydration_batch()` | Single JSON-RPC with array of summaries (N→1 round-trips) |
| `BatchDehydrateResult` | Per-session success/failure reporting |
| `PipelineIngestRequest/Response` | Wire types for coordinated ingest |
| METHOD_CATALOG | 2 new methods (39 total) |
| Capability registry | 2 new capabilities + provenance wire aliases |

## Architecture

```
Bulk ingestion (before G31):
  client → N × (create_session → append_event × M → dehydrate → notify)
  = N × (1 + M + 2) round-trips per dataset

Bulk ingestion (after G31):
  client → 1 × pipeline.ingest(events=M, dehydrate=true)
  = 1 round-trip per dataset (session created server-side)

Multi-session dehydration:
  client → 1 × dehydration.trigger_batch(session_ids=[...])
  = 1 round-trip, concurrent execution server-side
```

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,914 (+14) |
| Source files | 225 `.rs` |
| Lines | ~63,520 |
| Coverage | 93.83% |
| Clippy | 0 warnings |
| cargo deny | CLEAN |
| Cross-compile | 4 targets, zero warnings |
| Methods | 39 (METHOD_CATALOG) |
| Head | `0356187` |

## Deep Debt (Wave 155n late)

- **12 pre-existing test failures fixed**: BTSP FAMILY_ID env leaked from gate deployment into tests
- 7 deps updated to latest patches, pedantic clippy sweep clean
- `#[allow]`/`#[expect]` audit: all justified with reason strings
- Zero debt markers, zero hardcoded values, zero mocks in production

## What Remains for G31

rhizoCrypt's batch foundation is **SHIPPED**. Remaining for full G31:

1. **loamSpine**: batch commit API for multi-summary permanent storage
2. **sweetGrass**: `contribution.record_dehydration_batch` endpoint to consume batch notifications
3. **Orchestration**: biomeOS pipeline graph wiring batch ingest across all three primals
4. **Validation**: westGate PDB 220K structure bulk ingest at production scale

## Upstream Status

| Item | Status |
|------|--------|
| Batch append (single lock) | **SHIPPED** |
| Batch dehydration (concurrent) | **SHIPPED** |
| Pipeline ingest (coordinated) | **SHIPPED** |
| Batch provenance notify | **SHIPPED** |
| METHOD_CATALOG + registry | **SHIPPED** |
| 14 tests | **PASSING** |
| Cross-primal batch orchestration | Needs loamSpine + sweetGrass + biomeOS |
