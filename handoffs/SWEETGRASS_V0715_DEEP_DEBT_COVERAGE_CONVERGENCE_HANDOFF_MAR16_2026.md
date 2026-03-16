# SweetGrass v0.7.15 — Deep Debt Evolution + Coverage Expansion + Convergence Specification

**Date**: March 16, 2026
**Version**: v0.7.14 → v0.7.15
**Theme**: Complete unsafe elimination, coverage expansion, content convergence architecture
**License**: AGPL-3.0-only
**Supersedes**: `SWEETGRASS_V0714_DI_UNSAFE_ELIMINATION_RECONNECTION_HANDOFF_MAR16_2026.md` (archived)

---

## Summary

Completed all remaining DI migrations to eliminate unsafe environment mutations
from the entire test suite. Expanded test coverage across redb error paths, entity
decode, session DAG traversal, PROV-O export, and PostgreSQL integration (queries,
schema, activities, concurrency). Smart-refactored memory store module. Hardened
`deploy.sh` by removing hardcoded credentials. Authored the Content Convergence
specification — a collision-preserving provenance index that captures what data
lies at hash convergence points.

---

## Changes

### 1. Complete Unsafe Elimination (5 Additional Files)

v0.7.14 eliminated unsafe from 4 files. v0.7.15 completes the remaining 5:

| Module | Technique |
|--------|-----------|
| `sweet-grass-factory/src/factory/tests.rs` | `mock_reader` + `config_from_reader` |
| `sweet-grass-service/src/server/tests.rs` | `with_max_concurrent_requests()` builder |
| `sweet-grass-core/src/config/tests.rs` | `load_with_reader` + `apply_env_overrides_from_reader` |
| `sweet-grass-store-postgres/src/store/tests.rs` | `PostgresConfig::from_reader` |
| `sweet-grass-integration/src/discovery/tests.rs` | `create_discovery_with_reader` |

**Result**: Zero unsafe blocks in the entire workspace — production AND all tests.

### 2. Coverage Expansion

| Module | Tests Added | Coverage Focus |
|--------|-------------|----------------|
| `sweet-grass-store-redb/src/error.rs` | ~20 | All error variants, `Display`, `is_not_found`, `is_retriable`, all `From` impls |
| `sweet-grass-core/src/entity.rs` | ~10 | `EntityReference` constructors, `InlineEntity::decode` Hex, `DecodeError` display |
| `sweet-grass-compression/src/session.rs` | ~15 | `SessionVertex` builder, `Session` DAG ops, `max_depth`, serialization roundtrip |
| `sweet-grass-query/src/provo.rs` | ~10 | `ProvoExport` builder, graph export, JSON-LD roundtrip, timestamp, derivation |

### 3. PostgreSQL Integration Tests

Four new test modules in `crates/sweet-grass-store-postgres/tests/integration/`:

| Module | Tests | Coverage |
|--------|-------|----------|
| `queries.rs` | Filters, ordering, pagination, `by_agent`, `derived_from`, `count` |
| `schema.rs` | Migration idempotency, table existence |
| `activities.rs` | `put_activity`, `get_activity`, `activities_for_braid` |
| `concurrency.rs` | Parallel puts, reads during writes, batch operations |

All use `testcontainers` for isolated PostgreSQL instances.

### 4. Smart Refactoring

| File | Before | After |
|------|--------|-------|
| `memory/mod.rs` | 717 LOC | 246 LOC (tests → `memory/tests.rs`) |
| `factory/mod.rs` | Consolidated `create_*_backend()` methods | `config_from_reader()` + `from_config_with_name()` |

### 5. deploy.sh Hardening

- Removed hardcoded `DATABASE_URL` default (`postgresql://postgres:postgres@localhost:5432/sweetgrass`)
- Script now fails fast if `DATABASE_URL` not set when postgres backend selected
- Default port changed from `8080` to `0` (auto-allocate)

### 6. Content Convergence Specification

New `specs/CONTENT_CONVERGENCE.md` proposes evolving the content hash index from
collision-lossy (`HashMap<ContentHash, BraidId>`) to collision-preserving
(`HashMap<ContentHash, ContentConvergence>`).

Key concepts:
- **`ContentConvergence`**: Captures primary Braid + all convergent arrivals
- **`ConvergentArrival`**: Agent, timestamp, derivation path for each convergent path
- **Linear ↔ branching duality**: LoamSpine-style linear append meets rhizoCrypt-style DAG branching at convergence points
- **Cross-hatched letter analogy**: Multiple provenance layers on the same content surface

Ecosystem coordination:
- ISSUE-013 in `wateringHole/SPRING_EVOLUTION_ISSUES.md`
- `wateringHole/CONTENT_CONVERGENCE_EXPERIMENT_GUIDE.md` for Spring participation
- Complements rhizoCrypt ISSUE-012 (Content Similarity Index)

---

## Metrics

| Metric | v0.7.14 | v0.7.15 |
|--------|---------|---------|
| Tests | 933 | 1,001 |
| Unsafe blocks (total workspace) | 0 (4 files done) | 0 (all 9 files done) |
| Clippy warnings | 0 | 0 |
| Specifications | 10 | 11 |
| Max file | 808 lines | 842 lines |
| PostgreSQL integration modules | 2 | 6 |

---

## Ecosystem Cross-References

| Pattern | Source | Absorbed By |
|---------|--------|-------------|
| DI env reading (extended) | biomeOS V239 `temp_env` | sweetGrass v0.7.15 (config, factory, postgres, discovery) |
| Smart refactor (tests extraction) | sweetGrass v0.7.11 pattern | sweetGrass v0.7.15 (memory tests) |
| Content convergence | Hash collision research + cross-hatched letter analogy | sweetGrass v0.7.15 (spec), ISSUE-013 |
| testcontainers integration | loamSpine postgres tests | sweetGrass v0.7.15 (4 new modules) |

---

## Upstream Signals

1. **All Springs**: Content Convergence experiment guide published. Phase A (audit
   convergence candidates) can begin now. See `CONTENT_CONVERGENCE_EXPERIMENT_GUIDE.md`.
2. **rhizoCrypt**: ISSUE-013 complements ISSUE-012 (Content Similarity Index).
   Cross-layer analysis opportunity: do rhizoCrypt-similar vertices produce
   sweetGrass-convergent Braids?
3. **loamSpine**: Convergence spec acknowledges loamSpine's linear append model
   as one side of the linear↔branching duality.
4. **biomeOS**: Zero unsafe across entire workspace. All test modules are thread-safe
   via DI — no `#[serial]` needed.

---

## Quality

- 1,001 tests, 0 failures
- Zero clippy warnings (pedantic + nursery)
- Zero unsafe code (production AND all tests)
- All files under 1000 LOC (max: 842)
- 11 specification documents
- AGPL-3.0-only
