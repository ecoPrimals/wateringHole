# NestGate v4.7.0 — Concurrent Test Evolution: EnvSource Injection

**Date**: April 4, 2026
**Scope**: Eliminate `#[serial]` / `temp_env` / `thread::sleep` anti-patterns by injecting `EnvSource` trait throughout configuration layer
**Verification**: Clippy CLEAN, fmt PASS, 12,085 tests (0 failures), `#[serial]` reduced from ~36 to 5 (all legitimate)

---

## Problem

Tests that manipulate `std::env::set_var` / `std::env::remove_var` require `#[serial]` to avoid concurrent race conditions. These sleeps-and-serial patterns mask production concurrency bugs and prevent the test suite from running at full parallelism.

## Solution: EnvSource Trait + MapEnv

### Phase 1 — `nestgate-types::EnvSource` trait

New trait in `nestgate-types/src/env_source.rs`:
- `EnvSource: Send + Sync` with `get()`, `get_or()`, `vars()` methods
- `ProcessEnv` — delegates to `std::env` (production default)
- `MapEnv` — in-memory `HashMap<String, String>` (test isolation)
- `env_parsed<T>()` free function (dyn-compatible alternative to generic trait method)
- Re-exported from `nestgate-core::{ EnvSource, MapEnv, ProcessEnv, env_parsed }`

### Phase 2 — ConfigBuilder

`nestgate-config::ConfigBuilder` gained:
- `env: Arc<dyn EnvSource>` field (default: `ProcessEnv`)
- `.with_env(impl EnvSource + 'static)` builder method
- `api_endpoint()` moved from accessor-time env read → eager resolution in `build()`
- All 6 `#[serial]` tests converted to `MapEnv`

### Phase 3 — ExternalServicesConfig

- `from_env_source(&dyn EnvSource)` — replaces all `std::env::var()` and `std::env::vars()` calls
- `from_env()` delegates with `ProcessEnv`
- All 6 `#[serial]` tests converted

### Phase 4 — Port discovery, CLI, database, canonical config

- `discover_*_port_with_env()` / `discover_*_port_sync_with_env()` in `capability_port_discovery.rs`
- `port_from_env_source()` / `bind_from_env_source()` in `nestgate-bin/commands/env.rs`
- `DatabaseConfig::from_env_source()` in `nestgate-config/runtime/database.rs`
- `NestGateCanonicalConfig::from_env_source()` in `nestgate-config/canonical_primary/mod.rs`
- ~14 `#[serial]` tests converted across these modules

### Phase 5 — critical_path_coverage_dec16

Rewrote all env-mutating tests to use `MapEnv`. Concurrent config access tests now run against isolated in-memory env.

### Phase 6 — Sleep rationalization

- `transport_integration_test.rs`: blind 100ms sleep → active `socket_path.exists()` poll with 5ms micro-delays
- `metrics_tests.rs`: 50ms sleep → `tokio::task::yield_now().await`
- All other `sleep()` calls audited and categorized as legitimate (timeout assertions, cache TTL, backoff simulation)

### Phase 7 — capability_discovery EnvSource threading

- `discover_service_with_env()` / `discover_from_environment_with_env()` in `capability_discovery.rs`
- `discover_with_fallback_env()` — full fallback chain now respects injected env
- `ConfigBuilder::discover_endpoint()` and `discover_port()` thread `self.env` through to capability discovery
- `ServiceDetector::new_with_env()` in `nestgate-discovery/detector.rs` — scan ports from injected env
- Eliminated the last 2 `#[serial]` tests in `nestgate-discovery`
- Fixed final flaky tests (`migrate_port_returns_hardcoded_fallback_when_isolated`, `migrate_endpoint_returns_hardcoded_fallback_when_isolated`) caused by process-env pollution from capability discovery bypassing `MapEnv`

## Remaining `#[serial]` (5 total, all legitimate)

| File | Count | Reason |
|------|-------|--------|
| `nestgate-env-process-shim/src/lib.rs` | 4 | Tests that deliberately validate actual process-env mutation shim |
| `nestgate-bin/src/cli/tests.rs` | 1 | `setup_logging_initializes_subscriber_once` — process-global tracing subscriber |

## Metrics

- **Tests**: 12,085 passing, 0 failures, 468 ignored
- **`#[serial]` annotations**: 36 → 5 (86% reduction)
- **`temp_env` usages**: eliminated from all converted modules
- **Process-env calls in config layer**: replaced with `EnvSource` throughout
- **Clippy**: CLEAN (`-D warnings`)
- **fmt**: PASS

## Files Changed

### Created
- `nestgate-types/src/env_source.rs`

### Modified (production)
- `nestgate-types/src/lib.rs` — re-export
- `nestgate-core/src/lib.rs` — re-export
- `nestgate-config/src/config/agnostic_config.rs` — ConfigBuilder env injection
- `nestgate-config/src/config/external/services_config.rs` — from_env_source
- `nestgate-config/src/config/capability_discovery.rs` — discover_*_with_env
- `nestgate-config/src/constants/capability_port_discovery.rs` — _with_env variants
- `nestgate-config/src/config/runtime/database.rs` — from_env_source
- `nestgate-config/src/config/canonical_primary/mod.rs` — from_env_source
- `nestgate-bin/src/commands/env.rs` — _from_env_source variants
- `nestgate-discovery/src/capabilities/discovery/detector.rs` — new_with_env
- `nestgate-api/tests/transport_integration_test.rs` — sleep → poll
- `nestgate-api/src/handlers/performance_dashboard/metrics_tests.rs` — sleep → yield_now
- `nestgate-observe/src/observability/metrics.rs` — pre-existing clippy fix
- `nestgate-zfs/tests/orchestrator_integration_edge_cases.rs` — pre-existing doc fix

### Modified (tests)
- `nestgate-bin/src/cli/tests.rs` — 12 serial → MapEnv
- `nestgate-core/tests/critical_path_coverage_dec16.rs` — 6 serial → MapEnv

### Modified (docs)
- `STATUS.md`, `CHANGELOG.md`, `README.md`, `CONTRIBUTING.md`, `START_HERE.md`, `QUICK_REFERENCE.md`, `CONTEXT.md`, `QUICK_START.md`, `tests/README.md`, `tests/DISABLED_TESTS_REFERENCE.md`

---

*Last Updated: April 4, 2026*
