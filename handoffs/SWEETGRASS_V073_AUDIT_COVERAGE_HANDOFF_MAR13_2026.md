# SweetGrass v0.7.3 — Comprehensive Audit + 94% Coverage Handoff

**Date**: March 13, 2026
**From**: SweetGrass (v0.7.3)
**To**: All primal teams
**License**: AGPL-3.0-only

---

## Summary

SweetGrass v0.7.3 completes a comprehensive codebase audit and test coverage
push. 176 new tests bring the total to 746, achieving 94% line coverage
(target: 90%). All quality gates pass: zero clippy warnings, zero TODOs,
zero unsafe, zero production unwraps, all files under 1000 LOC.

---

## What Changed

### Test Coverage (570 → 746 tests, 85% → 94% line coverage)

| Area | Tests Added | Coverage Focus |
|------|-------------|----------------|
| JSON-RPC dispatch | 40+ | All 20 methods: braid, anchoring, attribution, provenance, compression, contribution, health |
| Server RPC | 10+ | `top_contributors`, `export_graph_provo`, `anchor_braid`, `verify_anchor`, `agent_contributions` |
| Factory config | 8+ | `StorageConfig`/`BootstrapConfig` explicit paths, backend selection |
| Discovery | 5+ | `CachedDiscovery` expiration/invalidation, env var fallback |
| Core model | 30+ | Activity/Braid builder methods, Privacy variants, Agent display/conversion |
| Store filters | 10+ | Time range, braid type, tag, ecoPrimals fields, sort variants |
| Contribution factory | 2+ | `parse_loam_entry`, `from_session` with loam entry |
| Attribution | 7+ | Config, batch, role inference, cycle protection, max depth |

### Bug Fix

- **`get_batch` ordering** — The default `BraidStore::get_batch` implementation
  used `buffer_unordered`, which does not preserve result order. Changed to
  `buffered` so results match input ID order. This fix is in
  `sweet-grass-store/src/traits.rs` and affects all backends using the default
  implementation.

### Code Quality

- **JSON-RPC test extraction** — `handlers/jsonrpc/mod.rs` (1103 LOC) split
  into `mod.rs` (280 LOC) + `tests.rs` (824 LOC) for 1000 LOC compliance
- **Zero TODOs/FIXMEs** in Rust source (verified by `scripts/check.sh`)

---

## No API Changes

All v0.7.2 APIs remain unchanged. No new methods, no breaking changes.
This is a quality-only release.

---

## For All Primal Teams

If you use the `get_batch` default trait implementation from `sweet-grass-store`,
the ordering fix ensures results now come back in the same order as the input IDs.
Previously, results could arrive in arbitrary order due to `buffer_unordered`.

---

## SweetGrass v0.7.3 Metrics

| Metric | Value |
|--------|-------|
| Version | 0.7.3 |
| Tests | 746 passing |
| Line coverage | 94.22% |
| Region coverage | 92.87% |
| Crates | 9 |
| Protocols | JSON-RPC 2.0 + tarpc + REST + UDS |
| License | AGPL-3.0-only |
| Unsafe code | 0 (`#![forbid(unsafe_code)]` all crates) |
| Production unwraps | 0 |
| Clippy | 0 warnings (pedantic + nursery) |
| Max file | 824 lines (limit: 1000) |
| TODOs in source | 0 |

---

## Supersedes

Extends `SWEETGRASS_V072_PROVENANCE_TRIO_IPC_HANDOFF_MAR13_2026.md`.
All v0.7.2 methods and contracts remain valid.
