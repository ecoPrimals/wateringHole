# SweetGrass v0.7.14 — DI Pattern + Unsafe Elimination + Dynamic Reconnection

**Date**: March 16, 2026
**Version**: v0.7.13 → v0.7.14
**Theme**: Dependency injection, test safety, dynamic client reconnection
**License**: AGPL-3.0-only
**Supersedes**: `SWEETGRASS_V0713_NICHE_RESILIENCE_ABSORPTION_HANDOFF_MAR16_2026.md` (archived)

---

## Summary

Systematic elimination of all `unsafe { std::env::set_var }` / `remove_var` from
test modules via Dependency Injection (DI) pattern. Production functions that read
environment variables now delegate to DI-friendly variants accepting reader closures.
Tests inject mock readers instead of mutating global process state. Dynamic client
reconnection added to `AnchorManager` and `EventHandler` for resilient inter-primal
communication. Resilience module made compile-time safe.

---

## Changes

### 1. DI-Based Environment Reading

**Pattern**: Every function that reads `std::env` now has a `_with_reader()` variant
that accepts `impl Fn(&str) -> Option<String>`.

| Module | Production Function | DI Variant |
|--------|-------------------|------------|
| `sweet-grass-core::primal_info` | `SelfKnowledge::from_env()` | `SelfKnowledge::from_reader(reader)` |
| `sweet-grass-service::bootstrap` | `infant_bootstrap_with_config()` | `infant_bootstrap_with_config_and_reader(config, reader)` |
| `sweet-grass-service::handlers::health` | `check_integrations()` | `check_integrations_with_reader(reader)` |
| `sweet-grass-service::uds` | `resolve_socket_path()` | `resolve_socket_path_with(config)` |

**Impact**: All associated test modules (`primal_info.rs`, `bootstrap.rs`, `health.rs`,
`uds.rs`) now use mock readers — zero `unsafe`, zero `#[serial]`.

### 2. Dynamic Client Reconnection

| Component | Change |
|-----------|--------|
| `AnchorManager::anchoring_client` | `Arc<dyn AnchoringClient>` → `parking_lot::RwLock<Arc<dyn AnchoringClient>>` |
| `EventHandler::session_client` | `Arc<dyn SessionEventsClient>` → `parking_lot::RwLock<Arc<dyn SessionEventsClient>>` |
| `AnchorManager::reconnect()` | New — uses `discovery.find_one()` to hot-swap client |
| `EventHandler::reconnect()` | New — uses `discovery.find_one()` to hot-swap client |

**Impact**: `discovery` fields (previously `#[expect(dead_code)]`) are now functional.
Clients can be dynamically replaced at runtime when connections fail.

### 3. Resilience Compile-Time Safety

- `with_resilience()` refactored to use `try_once()` helper for first attempt
- Eliminated `Option<E>` + `unwrap()` pattern — `last_err` always initialized
- Removed `#[allow(clippy::unwrap_used)]` — code is provably safe at compile time

### 4. UDS Explicit-Path API

- `start_uds_listener_at(path)` — bind to explicit path (no env lookup)
- `cleanup_socket_at(path)` — clean up explicit socket path
- Tests use `tempfile::tempdir` + explicit paths — no global state

---

## Metrics

| Metric | v0.7.13 | v0.7.14 |
|--------|---------|---------|
| Tests | 941 | 933 |
| Unsafe blocks in tests | ~20 | 0 |
| `#[serial]` attributes | ~15 | 0 (in refactored modules) |
| Clippy warnings | 0 | 0 |
| Net LOC change | — | -197 (333 added, 530 removed) |
| Max file | 808 lines | 808 lines |

Test count decreased because 8 redundant env-based tests were consolidated into
DI-based equivalents that cover the same code paths more robustly.

---

## Remaining Unsafe Env Tests (5 files)

These test files still use `unsafe { std::env::set_var }` and are candidates for
the same DI treatment in a future session:

1. `sweet-grass-factory/src/factory/tests.rs`
2. `sweet-grass-service/src/server/tests.rs`
3. `sweet-grass-integration/src/discovery/tests.rs`
4. `sweet-grass-core/src/config/tests.rs`
5. `sweet-grass-store-postgres/tests/integration.rs`

---

## Ecosystem Cross-References

| Pattern | Source | Absorbed By |
|---------|--------|-------------|
| DI env reading | biomeOS V239 `temp_env` pattern | sweetGrass v0.7.14 (reader closures) |
| Dynamic reconnection | loamSpine `ResilientAdapter` | sweetGrass v0.7.14 (`reconnect()`) |
| `parking_lot::RwLock` hot-swap | rhizoCrypt session manager | sweetGrass v0.7.14 (anchor + listener) |
| Compile-time resilience safety | groundSpring error handling | sweetGrass v0.7.14 (`try_once()`) |

---

## Upstream Signals

1. **biomeOS**: sweetGrass v0.7.14 anchoring/listener clients now support dynamic
   reconnection — biomeOS can expect more graceful degradation during primal restarts
2. **rhizoCrypt/loamSpine**: Trio partners should expect sweetGrass to attempt
   reconnection on IPC failures rather than permanent failure
3. **All primals**: DI reader pattern is recommended for any test that mutates
   `std::env` — eliminates `unsafe` and `#[serial]` requirements

---

## Quality

- 933 tests, 0 failures
- Zero clippy warnings (pedantic + nursery)
- Zero unsafe code (production AND tests for refactored modules)
- Zero `#[serial]` in refactored modules
- All files under 1000 LOC (max: 808)
- AGPL-3.0-only
