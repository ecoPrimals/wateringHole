# NestGate v4.7.0-dev — Blocking Pattern Elimination & EnvSource Concurrency

**Date**: April 6, 2026 (Session 32)
**Primal**: NestGate
**Scope**: Blocking-pattern removal, sleep-based synchronization elimination, EnvSource dependency-injection expansion, lint hygiene (`#[expect]` → `#[allow]` in tests), hardcoding evolution, concurrent test infrastructure

---

## Summary

This session continued deep debt elimination focused on blocking patterns, sleep-based synchronization, and EnvSource dependency injection evolution. Test code now avoids `block_on`, removes `std::thread::sleep` from async tests, drops `FROM_ENV_MUTEX` and process env mutation in socket config tests in favor of `MapEnv`, and extends `from_env_source` / env delegates across eight additional modules.

---

## Changes Executed

### 1. EnvSource Dependency Injection (8 new modules)

- **network_defaults_v2_config.rs**: `from_env_source` + `from_env` delegate
- **defaults_config.rs**: `NetworkDefaultsConfig` `from_env_source`
- **port_defaults_config.rs**: `PortConfig` `from_env_source`
- **migration.rs**: `DiscoveryOrEnv` holds `Arc<dyn EnvSource>`
- **hardware_detector.rs**: `detect_capabilities_from_env`, `is_development_environment_from_env`
- **atomic/discovery.rs**: `local_primal_id_from_env`, `discover_primal_socket_from_env`
- **primal_self_knowledge.rs**: `initialize_with_env(Arc<dyn EnvSource>)`
- **capability_based_config.rs**: `initialize_with_env(Arc<dyn EnvSource>)`

### 2. Blocking Pattern Elimination

- Converted **7** test `block_on` patterns to `#[tokio::test]` async (pool/manager, tcp_fallback, server, universal_zfs_types, errors, round6 coverage)
- Eliminated `std::thread::sleep` from **4** async test files (circuit_breaker, async_failure, concurrent_operations ×2)
- Removed **FROM_ENV_MUTEX** and all process env mutation from `socket_config_tests` — fully concurrent via `MapEnv`
- Migrated **6** integration test files from `env_process::set_var` to `MapEnv`

### 3. Lint Hygiene

- Fixed ~**839** unfulfilled `#[expect()]` lint warnings by converting to `#[allow()]` in test/example files
- Completed **temp_env** elimination except **6** legitimate uses in `env_process_shim`

### 4. Hardcoding Evolution

- Replaced hardcoded localhost literals with `LOCALHOST_NAME` / `LOCALHOST_IPV4` constants
- Updated production placeholder docs for `RealZfsOperations`, manager, orchestrator

---

## Current Metrics

| Metric | Value |
|--------|-------|
| Tests passing | 11,820 |
| Tests ignored | 463 |
| Test failures | 0 |
| Clippy warnings | 0 (pedantic + nursery, `-D warnings`) |
| `rustfmt` | Clean |
| `#[serial]` remaining | 1 (legitimate — setup_logging global subscriber) |
| `temp_env` remaining | 6 (legitimate — `env_process_shim` infrastructure) |
| `block_on` in tests | 0 (was 7) |
| `std::thread::sleep` in async tests | 0 (was 3) |
| `FROM_ENV_MUTEX` | 0 (was 1) |

---

## Remaining Work (next session)

### High / structural

1. **ENV_TEST_LOCK / EnvGuard** in `tests/common/env_isolation.rs` — legacy; still used by **3** test files
2. **live_integration_framework.rs** — still uses `env_process::set_var`; needs deeper refactor

### Medium

3. **~120** `tokio::time::sleep` sites in tests — most are legitimate timeout/retry patterns; audit opportunistically
4. **Production** `tokio::time::sleep` in retry/backoff/monitoring — legitimate; no blanket removal

### Low / upstream

5. **bincode** (unmaintained) and **opentelemetry_api** (unmaintained) via **tarpc** — upstream fix needed
6. **round6_discovery_coverage.rs** — not wired into `lib.rs` module tree

---

## Commits

- `5c5eee5c`: evolve: eliminate blocking patterns, env mutex, and sleep-sync antipatterns
