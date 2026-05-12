<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# SweetGrass v0.7.27 — primalSpring Audit Resolution + Deep Debt Evolution

**Date**: April 16, 2026
**Primal**: sweetGrass
**Version**: 0.7.27
**Previous handoffs**: `SWEETGRASS_V0727_CAPABILITY_NAMING_DI_REFACTOR_HANDOFF_APR13_2026.md`, `SWEETGRASS_V0727_COVERAGE_90_ASYNC_EVOLUTION_HANDOFF_APR12_2026.md`, `SWEETGRASS_V0727_NESTGATE_COMPOSITION_EVOLUTION_HANDOFF_APR12_2026.md` (all archived)

---

## Summary

Resolves ALL primalSpring post-Phase 43 audit items for sweetGrass:

1. **Postgres full-path testing** — RESOLVED (critical `run_migrations()` bug fixed, 29 integration tests now pass)
2. **Coverage 87% → 90% target** — RESOLVED (91.7% with Postgres, 90.4% without Docker)
3. **async-trait** — Documented conscious trade-off (6 `dyn`-dispatched traits)

The critical fix: `sqlx::query()` → `sqlx::raw_sql()` in `run_migrations()`.
PostgreSQL's extended query protocol rejects multi-statement prepared statements;
the simple-query protocol handles DDL correctly. This was the root cause of all
29 testcontainers integration tests silently failing.

---

## primalSpring Audit Items

### 1. Postgres Full-Path (RESOLVED — critical bug fix)

**Root cause**: `run_migrations()` used `sqlx::query(sql)` which sends SQL via
PostgreSQL's extended query protocol (prepared statements). This protocol
rejects multi-statement SQL. The production migration (`MIGRATION_001_INIT`) is
a 100-line multi-statement DDL block.

**Fix**: `sqlx::query(sql)` → `sqlx::raw_sql(sql)`. The simple-query protocol
supports multi-statement DDL in a single string. Applied to both the migration
tracking table creation and the migration execution itself.

**CI configuration** (done in prior session): `.github/workflows/test.yml`
uses `--include-ignored` for both `test` and `coverage` jobs, with a Postgres
16-alpine service container.

**Verification**: All 82 Postgres tests pass (40 unit + 29 testcontainers
integration + 12 migration + 1 doctest).

### 2. Coverage 87% → 91.7% (RESOLVED)

Targeted pure-Rust, unit-testable components for surgical coverage, plus
the Postgres full-path tests now exercising the production migration and
store code:

| Module | Before | After | Strategy |
|--------|--------|-------|----------|
| `store-postgres/migrations.rs` | 0% | 81% | Production `run_migrations()` exercised |
| `store-postgres/store/mod.rs` | 31% | 72% | Full CRUD via testcontainers |
| `store-postgres/row_mapping.rs` | 55% | 85% | Row deserialization exercised |
| `store-nestgate/store.rs` | 57% | 89% | Query, index, error, edge case tests |
| `service/factory/mod.rs` | 76% | 86% | NestGate backend factory tests |
| `service/handlers/composition.rs` | 67% | 90%+ | All 4 handler + probe error tests |
| `store-nestgate/discovery.rs` | 77% | 90%+ | Family-scoped socket discovery tests |
| `integration/testing.rs` | 81% | 90%+ | Helper function coverage |

---

## Deep Debt Evolution

### Smart Refactoring: `braid/context.rs` Extraction

`braid/types.rs` (856 lines) reduced to 649 lines by extracting JSON-LD
context types into `braid/context.rs`:

- `JsonLdVersion`, `BraidContext` structs
- Vocabulary URI constants (`PROV_VOCAB_URI`, `XSD_VOCAB_URI`, etc.)
- DI-friendly `ecop_vocab_uri_with_reader()` / `ecop_base_uri_with_reader()`
- Custom `Serialize`/`Deserialize` implementations (human-readable vs binary)

Semantic split by JSON-LD concern, not mechanical line counting.

### Hardcoding Elimination: `bootstrap.rs` DI

`resolve_advertise_host()` and `advertise_address()` evolved to accept an
injectable reader closure. `0.0.0.0` wildcard is never announced — replaced
with hostname resolution via the `hostname` crate, overridable via
`PRIMAL_ADVERTISE_ADDRESS` env var. `if let Err` replaces verbose `match`.

### Outdated Migration Cleanup

Removed `migrations/20250101000000_initial.sql` — a stale SQL file with a
different schema than the production embedded migrations in `src/migrations.rs`.
`docker-compose.yml` mount to `docker-entrypoint-initdb.d` removed. Production
uses `PostgresStore::run_migrations()` (Rust-embedded, `_sweetgrass_migrations`
table).

### Root Documentation Refresh

- README: test count 1,427→1,463, max file 898→876, LOC 49,869→51,283, NestGate crate added to table
- CONTEXT: updated test count and coverage
- DEVELOPMENT: updated coverage table with NestGate, refreshed metrics
- ROADMAP: CI/CD marked done, coverage metric updated
- CHANGELOG: April 15 entry added

---

## Current Metrics

| Metric | Value |
|--------|-------|
| Tests | **1,559** (1,501 local + 58 Docker CI) |
| Coverage | **91.7%** line with Postgres / **90.4%** without Docker (llvm-cov) |
| Source files | **186** `.rs` (51,283 LOC) |
| Crates | **11** |
| JSON-RPC methods | **32** |
| Clippy | 0 warnings (pedantic + nursery) |
| `cargo doc` | 0 warnings |
| Unsafe | 0 (`#![forbid(unsafe_code)]` all 11 crate roots) |
| Max file size | 876 lines (limit: 1000) |
| SPDX headers | All 186 source files |
| Capability Wire Standard | **Full L3** |
| BTSP | Phase 2 |

---

## Gates (All Green)

```
cargo fmt --all -- --check                   ✓
cargo clippy --all-targets                   ✓ (0 warnings)
cargo doc --no-deps                          ✓ (0 warnings)
cargo test --workspace                       ✓ (1,501 passed, 0 failed, 58 ignored)
cargo test -p postgres -- --include-ignored  ✓ (82 passed, 0 failed)
cargo deny check                             ✓
cargo llvm-cov                               ✓ 91.7% with Postgres (gate: 90%)
```

---

## For primalSpring

All sweetGrass audit items from the post-Phase 43 provenance trio blurb
are resolved:

1. ✅ Postgres full-path testing — `run_migrations()` bug fixed, 82 tests pass, Docker CI configured
2. ✅ Coverage 91.7% with Postgres (target was 90%)
3. ✅ async-trait documented as conscious trade-off for 6 `dyn`-dispatched traits

## For Trio Partners (rhizoCrypt, loamSpine)

- `braid/context.rs` DI-friendly URI resolvers are reusable for any primal
  needing JSON-LD vocabulary configuration
- `bootstrap.rs` hostname-based advertise pattern recommended for adoption
- Migration test pattern (production path, not `sqlx::migrate!`) should be
  mirrored in any primal with embedded migrations

## Remaining Known Debt (Low)

| Area | Status |
|------|--------|
| async-trait for 6 dyn traits | Awaiting `trait_variant` ecosystem maturity |
| sled deprecation | Feature-gated, redb is primary |
| BTSP Phase 3 | Ecosystem-wide, barraCuda leading |
| `server/tests.rs` at 876 lines | Next refactor candidate if it grows |

---

*Previous handoffs archived in `handoffs/archive/SWEETGRASS_V0727_*`*
