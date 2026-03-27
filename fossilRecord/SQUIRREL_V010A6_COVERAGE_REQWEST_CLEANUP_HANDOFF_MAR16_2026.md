<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.6 — Coverage Expansion, reqwest Migration, Debris Cleanup

**Date**: March 16, 2026
**From**: Squirrel AI Primal
**Session**: Test coverage expansion, reqwest 0.12 migration, codebase cleanup

---

## Summary

Expanded test coverage across 4 under-tested crates (+92 new tests), re-enabled
16 previously disabled tests, migrated all 9 remaining crates from reqwest 0.11
to 0.12, fixed 12 flaky async tests, and cleaned orphaned files/directories.
This completes the full 12-item deep debt resolution plan from alpha.5.

## Changes

### Test Coverage Expansion

- **Auth crate** — 51 new tests
  - `errors.rs` (19): all error variants, Display, From impls (serde_json, uuid, anyhow, reqwest)
  - `types.rs` (21): LoginRequest, User, Permission, AuthContext, Session, serde round-trips
  - `session.rs` (6): extend, user sessions, invalidation, session stats
  - `lib.rs` (5): initialization, env var resolution via temp-env

- **Plugins crate** — 31 new tests
  - `manager.rs` (9): register/unregister, get by id/name, status transitions, error paths
  - `types.rs` (7): PluginType/Status/State/DataFormat serde, ResourceLimits/Config defaults
  - `discovery.rs` (6): manifest deserialization, placeholder plugin, empty dir, error paths
  - `default_manager.rs` (9): registry CRUD, metrics, initialize/shutdown lifecycle

- **Config crate** — 10 new tests
  - `merge_config` (4): non-overlapping, precedence, partial override, default merge
  - `health_check` (5): constructors, defaults, all methods, clone
  - `ConfigLoader::load()` (1): full pipeline with temp file + env overrides

### Re-enabled Tests (16)

- **MCP propagation tests** (14): removed `disabled_until_rewrite` feature gate,
  fixed API mismatches for current MCPError types
- **Rate limiter test** (1): fixed nested runtime — `Arc<RateLimiter>` instead of block_on
- **Resource manager test** (1): updated for current API (connection_pools removed)

### Async Test Fixes (12)

- `universal_adapter_tests.rs` — converted 12 tests from `#[tokio::test]` with
  `Handle::current().block_on()` inside `temp_env` closures to `#[test] fn` with
  explicit `Runtime::new()`, eliminating "Cannot start a runtime" panics

### reqwest 0.12 Migration (9 crates)

All optional reqwest upgraded from 0.11 to 0.12:
- squirrel-mcp, squirrel-core, squirrel-plugins, squirrel-mcp-config
- squirrel-mcp-auth, squirrel-sdk, squirrel-cli, squirrel-ai-tools
- universal-patterns

Zero source code changes needed — all API usage compatible. Now on rustls 0.23
with pluggable crypto providers.

### Debris Cleanup

- **Deleted root `tests/`** — 24 files + chaos/ and integration/ subdirectories.
  Never compiled (workspace has no root [package]). Canonical tests in `crates/main/tests/`.
- **Deleted root `config/`** — development.toml, production.toml, testing.toml.
  ConfigLoader uses squirrel.toml, not these files.
- **Deleted `crates/main/tests/chaos/time_manipulation.rs`** — 10-line stub, not in mod.rs
- **Removed 7 orphaned config test files** — referenced removed `core` module
- **Deleted `test_primal_analyze_e2e_mock`** — HTTP handlers removed, test was no-op

### Documentation Updates

- `docs/CRYPTO_MIGRATION.md` — updated for reqwest 0.12 completion
- `specs/current/DEPLOYMENT_GUIDE.md` — Rust 1.70+ → 1.85+
- `specs/development/AI_DEVELOPMENT_GUIDE.md` — removed Python/Node/Docker prerequisites
- `README.md` — fixed crate count (22 → 21), removed tests/ and config/ from tree
- `CURRENT_STATUS.md` — 4,667 tests, 21 crates, reqwest 0.12 status
- `CHANGELOG.md` — full alpha.6 entry

## Metrics

| Metric | alpha.5 | alpha.6 |
|--------|---------|---------|
| Tests | 4,600+ | 4,667 passing |
| Auth crate tests | 19 | 70 |
| Plugins crate tests | 22 | 53 |
| Config crate tests | 102 | 112 |
| reqwest version | 0.11 (9 crates) | 0.12 (all 10) |
| Re-enabled tests | — | +16 |
| Orphaned files | 32+ | 0 |
| Debt items completed | 10/12 | 12/12 |

## Debt Resolution Summary (Complete)

| Item | Status |
|------|--------|
| primal_names.rs centralized constants | Done (alpha.5) |
| JSON-RPC 2.0 batch support | Done (alpha.5) |
| capability.list handler | Done (alpha.5) |
| Context in-memory persistence | Done (alpha.5) |
| Production mock cleanup | Done (alpha.5) |
| #[allow] → #[expect] migration | Done (alpha.5) |
| Handler refactoring by domain | Done (alpha.5) |
| Unsafe env::set_var → temp_env | Done (alpha.5) |
| Hardcoded socket → primal_names | Done (alpha.5) |
| Test coverage expansion | Done (alpha.6) |
| reqwest 0.11 → 0.12 | Done (alpha.6) |
| Root docs + cleanup | Done (alpha.6) |

## Known Issues

1. `test_load_from_json_file` flaky under full workspace runs (env var pollution)
2. `chaos_07_memory_pressure` flaky under parallel test load (environment-sensitive)
3. `model_splitting/` stub module — waiting on ToadStool integration

## Sovereignty / Human Dignity

- All changes AGPL-3.0-only compliant
- Zero chimeric dependencies
- reqwest 0.12 with pluggable crypto — rustls-rustcrypto path viable when stable
- No hardcoded primal names — capability-based discovery throughout
