# SweetGrass v0.7.18 — Deep Execution: tarpc 0.37 + Structured IPC + Pipeline Integration

**Date**: March 16, 2026
**Version**: v0.7.17 → v0.7.18
**Theme**: tarpc ecosystem alignment, structured IPC errors, NDJSON streaming, pipeline attribution
**License**: AGPL-3.0-only
**Supersedes**: `SWEETGRASS_V0717_ECOSYSTEM_ABSORPTION_LINT_CAPABILITY_HANDOFF_MAR16_2026.md` (archived)

---

## Summary

Major ecosystem alignment release. Upgraded tarpc to 0.37 (matching rhizoCrypt,
biomeOS, barraCuda, coralReef). Added structured IPC error phases for
observability. Implemented NDJSON streaming types for pipeline coordination.
Wired provenance-trio-types pipeline into a new `pipeline.attribute` handler.

## Changes

### tarpc 0.34 → 0.37

- Aligned with rhizoCrypt (0.37), biomeOS, barraCuda, coralReef
- Includes `tokio-serde` 0.9, `opentelemetry` 0.30
- Zero breaking changes for sweetGrass's usage (serde_transport, BaseChannel, Context)
- loamSpine remains at 0.34 — upgrade recommended for trio alignment

### Structured IPC Errors

- `IpcErrorPhase` enum: Connect, Write, Read, InvalidJson, HttpStatus(u16), NoResult, JsonRpcError(i64)
- `IntegrationError::Ipc { phase, message }` variant with `IntegrationError::ipc()` constructor
- Aligned with rhizoCrypt `IpcErrorPhase` and healthSpring V28 standard
- All tarpc clients (signing, anchoring, listener) migrated from flat `Rpc(String)` to structured phases

### NDJSON Streaming Types

- `StreamItem` enum: Data, Progress, End, Error (with recoverable flag)
- `to_ndjson_line()` / `parse_ndjson_line()` for wire format
- Aligned with rhizoCrypt `streaming::StreamItem`
- Ready for toadStool → rhizoCrypt → sweetGrass NDJSON pipeline

### Pipeline Attribution Handler

- New JSON-RPC method: `pipeline.attribute`
- Consumes `provenance_trio_types::PipelineRequest`
- Creates attribution braids per agent contribution
- Returns `provenance_trio_types::PipelineResult` with `braid_ref`
- 22 total JSON-RPC methods (was 21)

### Smart Refactoring

- `store-postgres/store/mod.rs`: 714 → 516 lines
- `row_mapping.rs` extracted: row_to_braid, row_to_activity, parse_activity_type, i64/u64 conversions

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,017 passing (was 1,004) |
| Clippy | 0 warnings |
| Unsafe | 0 blocks |
| Docs | clean build |
| JSON-RPC methods | 22 |
| tarpc version | 0.37 |
| Edition | 2024 |
| MSRV | 1.87 |

## Upstream Impact

| Primal | Impact |
|--------|--------|
| rhizoCrypt | `pipeline.attribute` enables rhizoCrypt → sweetGrass attribution step in provenance pipeline |
| loamSpine | Recommend tarpc 0.34 → 0.37 upgrade for trio alignment |
| biomeOS | NDJSON streaming types enable future real-time pipeline monitoring |
| toadStool | StreamItem compatibility for toadStool → rhizoCrypt → sweetGrass NDJSON flow |
| provenance-trio-types | `PipelineRequest`/`PipelineResult` now consumed in production |

## What's Next for sweetGrass

1. **Content Convergence Phase 1** — Implement `convergence.query`, `convergence.agents`, `convergence.statistics`
2. **Squirrel AI attribution** — Wire squirrel AI contribution tracking into attribution braids
3. **NDJSON streaming endpoints** — Expose `StreamItem`-based endpoints for real-time pipeline monitoring
4. **Cross-Spring Provenance Indexing** — Index provenance across multiple Springs
