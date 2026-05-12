# NestGate v4.7.0-dev — EnvSource Evolution, Hardcode Elimination & Error Typing

**Date**: April 5, 2026 (Session 31)
**Primal**: NestGate
**Scope**: Deep debt resolution — continued EnvSource injection, hardcoded value elimination, concrete error typing, stale feature removal, temp_env migration, documentation alignment

---

## Summary

Continuation of the EnvSource concurrent-testing evolution (Session 30) with expansion to
remaining environment-coupled modules. Eliminated scattered string literals for ecosystem paths,
localhost addresses, and `Box<dyn Error>` signatures. Removed stale feature flags and production
mock exposure. Aligned all root documentation with current metrics.

---

## Changes Executed

### 1. `#[allow(` → `#[expect(` Migration (final)
- **auth_manager.rs**: 3× `#[allow(dead_code)]` → `#[expect(dead_code, reason = "...")]`
- **lifecycle_comprehensive_tests.rs**: 21× `#[allow(deprecated)]` → `#[expect(deprecated)]`
- **Result**: **0** `#[allow(` remaining in `code/`

### 2. Stale Feature Flags Removed
- **nestgate-performance**: Removed empty `simd`, `zero-copy`, `lock-free`, `adaptive`, `custom-allocators` features (no `cfg(feature)` usage in src/)
- **nestgate-canonical**: Removed empty `unified-config`, `zero-cost-patterns`, `simd-integration`, `performance-monitoring`
- **Root Cargo.toml**: Removed empty `streaming-rpc = []` (real feature lives on nestgate-api)

### 3. Production Mock Gating
- `ZfsManager::mock()` gated behind `#[cfg(any(test, feature = "dev-stubs"))]`
- Related `new_for_testing` helpers on pool/dataset/snapshot/tier/metrics managers similarly gated

### 4. Hardcoded "biomeos" Elimination
- Added `ECOSYSTEM_NAME` constant + `ecosystem_path_segment()` in `nestgate-config::constants::system`
- Replaced 5 scattered `"biomeos"` string literals in `socket_config.rs`, `capability_discovery.rs`, `atomic/discovery.rs`, `discover.rs`
- Runtime-overridable via `BIOMEOS_SERVICE_NAME` env var

### 5. `Box<dyn Error>` → `NestGateError`
- **jsonrpc_server/mod.rs**: `build_module`, `start`, `register_storage_methods`, `register_capability_methods`, `register_monitoring_methods` — all return `NestGateError` now
- Added `map_jsonrpc_registration()` helper to normalize jsonrpsee's `RegisterMethodError`
- **performance/monitor/analysis.rs**: `analyze_trends` returns `NestGateError`
- **Result**: 0 `Box<dyn Error>` in production function signatures

### 6. Hardcoded localhost/127.0.0.1 → Constants
- `detector.rs`: Uses `LOCALHOST_NAME`, `LOCALHOST_IPV4` from hardcoding module
- `capability_based.rs`, `agnostic_config.rs`: Uses `LOCALHOST` constant
- `health.rs`: Uses `LOCALHOST_NAME` from nestgate-core constants

### 7. EnvSource Injection Expansion
- **SystemConfig**: Added `from_env_source(&dyn EnvSource)` — 15 Mutex+EnvGuard tests rewritten to MapEnv
- **EnvironmentConfig** + sub-configs (Network, Storage, Discovery, Monitoring, Security): `from_env_source` variants
- **SocketConfig**: `from_env_source` for concurrent IPC config testing
- **ProductionReadinessValidator**: `new_with_env(Arc<dyn EnvSource>)` for mock analysis injection
- **integration_comprehensive_tests.rs**: 10 tests rewritten from env mutation to MapEnv; concurrent discovery test un-ignored
- **temp_env reduction**: 110 → 71 uses across workspace

### 8. Documentation & Debris Cleanup
- All root `.md` files: test count aligned to ~11,812
- `DOCUMENTATION_INDEX.md`: date → April 5; workspace count → 23/20
- `LICENSING.md`: table cell → AGPL-3.0-or-later
- `CHANGELOG.md`: Session 31 entry added
- `ARCHITECTURE_OVERVIEW.md`: nestgate-network/automation marked archived
- `TESTING.md`, `CLONE_OPTIMIZATION_GUIDE.md`: stale nestgate-network references annotated
- `.pre-commit-config.sh`: Fixed clippy check to use exit code (was broken grep logic)
- Deleted orphaned `fuzz/fuzz_targets/fuzz_target_1.rs`

---

## Current Metrics

| Metric | Value |
|--------|-------|
| Tests passing | ~11,812 |
| Tests ignored | ~463 |
| Test failures | 0 |
| Clippy warnings | 0 |
| `#[allow(` in code/ | 0 |
| `#[expect(` (legitimate) | Per-use with reasons |
| `#[deprecated]` markers | 188 (migration guideposts) |
| `#[serial]` attributes | 5 (env-process-shim: 4, tracing init: 1) |
| `temp_env` uses | 71 (down from 110; long tail across ~20 files) |
| `Box<dyn Error>` in signatures | 0 (doc examples only) |
| Production mocks exposed | 0 (all behind cfg gates) |
| Hardcoded "biomeos" in prod | 0 (constant + env override) |
| Stale feature flags | 0 removed |
| Coverage | ~80% line (target: 90%) |

---

## Remaining Work (next session)

### High Priority
1. **temp_env long tail (71 uses)**: Spread across ~20 files at 3-4 uses each. Each requires adding `from_env_source` to the tested production function. Diminishing returns per file but adds up to fully concurrent test suite.
2. **Coverage to 90%**: Current ~80%. Key gaps likely in nestgate-zfs (ZFS-dependent paths), nestgate-security (cert operations), nestgate-rpc (socket operations).

### Medium Priority
3. **Disabled fuzz targets**: `fuzz_config_parsing`, `fuzz_unified_config_example`, `fuzz_zfs_commands` reference removed `unified_final_config` module — need rewriting against current API.
4. **nestgate-installer validation.rs**: Orphan file not declared in lib.rs — delete or wire up.
5. **Specs referencing nestgate-network**: Historical specs mention archived crate — annotate or move to fossilRecord.

### Low Priority
6. **`sysinfo` C dependency**: Used as non-Linux fallback. Linux paths use `/proc` directly. Could be feature-gated more tightly or replaced with pure-Rust alternative.
7. **`String` params that could be `&str`**: ~10 functions in API/RPC service traits — API-breaking change, defer to major version.

---

## Compliance Matrix Impact

Previous NestGate grade: **C** (rollup)

This session improves:
- **T1 Build**: Stale features removed, clippy clean, fmt clean → maintains **B**
- **T2 UniBin**: `ECOSYSTEM_NAME` env override, localhost constants → incremental **D→D+**
- **T4 Discovery**: Hardcoded biomeos → constant, env-resolved → incremental **C→C+**
- **T7 Testing**: EnvSource injection, concurrent tests, temp_env reduction → maintains **A**

No tier regression.
