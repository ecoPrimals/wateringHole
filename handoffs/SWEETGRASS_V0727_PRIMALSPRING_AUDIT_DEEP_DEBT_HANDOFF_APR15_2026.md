<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# SweetGrass v0.7.27 — primalSpring Audit Resolution + Deep Debt Evolution

**Date**: April 15, 2026
**Primal**: sweetGrass
**Version**: 0.7.27
**Previous handoffs**: `SWEETGRASS_V0727_CAPABILITY_NAMING_DI_REFACTOR_HANDOFF_APR13_2026.md`, `SWEETGRASS_V0727_COVERAGE_90_ASYNC_EVOLUTION_HANDOFF_APR12_2026.md`, `SWEETGRASS_V0727_NESTGATE_COMPOSITION_EVOLUTION_HANDOFF_APR12_2026.md` (all archived)

---

## Summary

Resolves both primalSpring post-Phase 43 audit items for sweetGrass and
completes a comprehensive deep debt evolution pass. Two audit items
were explicitly called out by primalSpring:

1. **Postgres full-path testing — needs Docker CI** — RESOLVED
2. **Coverage 87% → 90% target** — RESOLVED (90.4%)

Additionally: smart refactoring, hardcoding elimination, DI evolution,
outdated migration cleanup, and root documentation refresh.

---

## primalSpring Audit Items

### 1. Postgres Docker CI (RESOLVED)

`.github/workflows/test.yml` updated: both `test` and `coverage` jobs
now use `--include-ignored` to run `#[ignore]`-marked PostgreSQL
integration tests that require Docker. These tests were previously
skipped in CI.

`migrations_test.rs` rewritten to use the **production** migration path
(`PostgresStore::connect()` + `run_migrations()`) instead of
`sqlx::migrate!("./migrations")`. Assertions validate against the
`_sweetgrass_migrations` table and production schema columns.

### 2. Coverage 87% → 90%+ (RESOLVED: 90.4%)

Targeted pure-Rust, unit-testable components for surgical coverage:

| Module | Before | After | Strategy |
|--------|--------|-------|----------|
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
| Tests | **1,463** (1,405 local + 58 Docker CI) |
| Coverage | **90.4%** line (llvm-cov) |
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
cargo fmt --all -- --check     ✓
cargo clippy --all-targets     ✓ (0 warnings)
cargo doc --no-deps            ✓ (0 warnings)
cargo test --workspace         ✓ (1,405 passed, 0 failed, 58 ignored)
cargo deny check               ✓
cargo llvm-cov                 ✓ 90.4% (gate: 90%)
```

---

## For primalSpring

Both sweetGrass audit items from the post-Phase 43 provenance trio blurb
are resolved:

1. ✅ Postgres full-path testing with Docker CI
2. ✅ Coverage 90.4% (target was 90%)

## For Trio Partners (rhizoCrypt, loamSpine)

- `braid/context.rs` DI-friendly URI resolvers are reusable for any primal
  needing JSON-LD vocabulary configuration
- `bootstrap.rs` hostname-based advertise pattern recommended for adoption
- Migration test pattern (production path, not `sqlx::migrate!`) should be
  mirrored in any primal with embedded migrations

## Remaining Known Debt (Low)

| Area | Status |
|------|--------|
| Postgres coverage in local runs | Needs Docker; CI handles it |
| async-trait for 6 dyn traits | Awaiting `trait_variant` ecosystem maturity |
| sled deprecation | Feature-gated, redb is primary |
| BTSP Phase 3 | Ecosystem-wide, barraCuda leading |
| `server/tests.rs` at 876 lines | Next refactor candidate if it grows |

---

*Previous handoffs archived in `handoffs/archive/SWEETGRASS_V0727_*`*
