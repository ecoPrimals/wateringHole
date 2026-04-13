# biomeOS v3.04 — Composition Elevation + Deep Debt Cleanup VII

**Date**: April 12, 2026
**Primal**: biomeOS
**Version**: v3.04
**License**: AGPL-3.0-or-later

---

## Summary

v3.04 elevates biomeOS composition capabilities to unblock chimera compositions
and garden deployments. Multi-primal graph execution (5+ nodes) is proven
end-to-end, `lifecycle.composition` dashboard is enriched for spring visibility,
`composition.health` standard is implemented, and all remaining deep debt is
resolved.

**Tests**: 7,783 passed, 0 failed
**Clippy**: Zero warnings (`clippy::pedantic + nursery`, `-D warnings`)
**Fmt**: Clean
**cargo-deny**: Passing
**cargo doc**: Clean

---

## Composition Elevation (primalSpring MEDIUM priority — RESOLVED)

### 1. Multi-primal Graph Execution Proven End-to-End (BLOCKING — RESOLVED)

15 integration tests in `crates/biomeos-atomic-deploy/tests/nucleus_composition_e2e.rs`:

| Level | Tests | Validates |
|-------|-------|-----------|
| L1: TOML parsing | 4 | `nucleus_complete.toml` loads, 11 nodes, 5+ primal starts, capabilities populated, dependency integrity |
| L2: Topological sort | 3 | Correct phase count, NUCLEUS architectural ordering (Tower before Node/Nest), parallel phases exist |
| L3: Synthetic e2e execution | 3 | Full executor flow with "log.info" ops, all nodes complete, parallel phase speedup |
| L4: gate2 deploy graph | 4 | `gate2_nucleus.toml` parsing, sort, parallel deployment (NestGate/Toadstool/Squirrel), 5+ primal starts |
| L5: Failure handling | 1 | Critical node failure aborts downstream, preserves upstream results |

`topological_sort` visibility elevated from `pub(crate)` to `pub` for integration test access.

### 2. `lifecycle.composition` Dashboard Completeness (BLOCKING — RESOLVED)

Enriched JSON-RPC response now includes:
- Per-primal: `capabilities`, `health` (latency, failures, uptime), `state_details` (started_at, reason), `depends_on`, `depended_by`
- Aggregated: `capabilities_live` (deduplicated across all primals), `dependency_graph` (edges array)
- Springs can now see what's running, what failed, what degraded

### 3. `composition.health` Standard (LOW debt — RESOLVED)

New route following `COMPOSITION_HEALTH_STANDARD.md`:
- Methods: `composition.health`, `composition.tower_health`, `composition.node_health`, `composition.nest_health`, `composition.nucleus_health`
- Response shape: `{ healthy, deploy_graph, subsystems: { tower, node, nest, mesh }, capabilities_count }`
- Subsystem status inferred from primal `LifecycleState` (ok/degraded/unavailable)
- Deploy graph inferred from active primal count

### 4. gate2/Pixel Deploy Validation (LOW debt — RESOLVED)

4 dedicated tests validate `gate2_nucleus.toml` for parsing, topological sort,
parallel deployment of NestGate/Toadstool/Squirrel, and 5+ primal start operations.

---

## Deep Debt Cleanup VII

### Hardcoding Elimination

| File | Before | After |
|------|--------|-------|
| `handlers/lifecycle.rs` | `["beardog", "songbird"]` string literals | `[primal_names::BEARDOG, primal_names::SONGBIRD]` from `biomeos-types` |
| `primal_communication.rs` | `"beardog".to_string()` fallback | `primal_names::BEARDOG.to_string()` |

Zero hardcoded primal name strings remain in production code.

### Dependency Governance

- `blake3`: Added `default-features = false` to workspace pin — enforces pure Rust implementation, prevents C/assembly build path

### Deep Debt Audit (All Clean)

| Dimension | Status |
|-----------|--------|
| Unsafe code | 0 blocks in production |
| TODO/FIXME/HACK | 0 in production |
| Production mocks | 0 (all isolated to `#[cfg(test)]`) |
| `.unwrap()`/`.expect()` in production | 0 (all inside `#[cfg(test)]`) |
| Files >1000 LOC | 0 (largest: 919) |
| Banned crates | 0 in lockfile (`deny.toml` enforced) |
| `extern "C"` / `#[link` | 0 project-authored FFI |
| Hardcoded primal names in production | 0 |

### CI Fix

- Removed stale `src` from `ci.yml` file-size check path (only `crates` exists at repo root)

### Doc Alignment

- All 6 root docs updated to v3.04 / April 12, 2026 / 7,783 tests
- `SECURITY.md` supported versions: v3.x (was v2.x only)
- `DOCUMENTATION.md` handoff index updated through v3.04
- CHANGELOG entry added

---

## For Downstream Springs

### What Changed (API surface)

1. **`lifecycle.composition`** now returns enriched response with `capabilities_live`, `dependency_graph`, per-primal `capabilities`, `health`, `state_details`, `depends_on`, `depended_by`
2. **New routes**: `composition.health`, `composition.tower_health`, `composition.node_health`, `composition.nest_health`, `composition.nucleus_health` — all return standard health shape
3. **`topological_sort`** is now `pub` (was `pub(crate)`) — available for integration testing

### What's Unblocked

- **chimera compositions**: Graph execution of 5+ node NUCLEUS validated
- **garden deployments**: `lifecycle.composition` provides full dashboard data
- **primalSpring**: Can launch full NUCLEUS via biomeOS graph execution and validate correctness

---

## Quality Gates

| Gate | Status |
|------|--------|
| Tests | 7,783 passed (0 failed) |
| Clippy | PASS (pedantic + nursery, `-D warnings`) |
| Fmt | PASS |
| Docs | PASS (0 missing_docs) |
| cargo-deny | PASS |
| LOC limit | PASS (max 919, limit 1000) |
| Unsafe | 0 in production |
| TODO/FIXME | 0 in production |
| Mocks | 0 in production |
| Hardcoded names | 0 in production |
| SPDX headers | 100% |
