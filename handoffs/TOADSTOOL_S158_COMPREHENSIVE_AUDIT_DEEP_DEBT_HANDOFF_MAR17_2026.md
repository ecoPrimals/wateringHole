# ToadStool S158 — Comprehensive Audit + Deep Debt Execution

**Date**: March 17, 2026
**Session**: S158
**Author**: toadStool team

---

## Summary

Full codebase and documentation audit against wateringHole standards (UniBin, ecoBin v3.0,
sovereignty, Semantic Method Naming, licensing, Lysogeny Protocol). Execution of all
identified debt items with quality gates verified green throughout.

Critical fix: SIGSEGV in parallel test harness caused by concurrent `wgpu::Instance`
creation — resolved with `OnceLock` GPU probe caching.

## Changes

### P0: SIGSEGV Fix — GPU Probe Race Condition
- `crates/core/toadstool/src/self_identity.rs`: `detect_gpu()` now cached via
  `std::sync::OnceLock` — GPU hardware probe runs exactly once per process lifetime
- Root cause: parallel `cargo test` created multiple `wgpu::Instance` objects concurrently,
  triggering Vulkan driver segfault on Linux/NVIDIA
- Scoped thread ensures safe join semantics; `unwrap_or(false)` fallback on thread panic

### License Compliance — All Crates Inherit Workspace
- 17 `Cargo.toml` files updated: hardcoded `license = "AGPL-3.0-only"` → `license.workspace = true`
- Affected: `hw-learn`, `nvpmu`, 15 showcase packages
- Ensures single-point license management from workspace root

### `#![forbid(unsafe_code)]` Expansion
- 9 additional crates upgraded from `deny` to `forbid`: client, cli, integration-tests,
  server, testing, toadstool-core, core/common, core/config, core/toadstool
- **29 total crates** now `forbid(unsafe_code)` (was 22)
- 3 crates (`auto_config`, `core/common`, `distributed`) remain `deny` — these require
  `unsafe { std::env::set_var() }` in test modules, which `forbid` prevents even with
  `#[allow(unsafe_code)]`

### Hardcoding Evolution — Test Constants
- `crates/testing/src/fixtures.rs`: Added `TEST_HOST`, `TEST_ENDPOINT`,
  `TEST_REMOTE_ENDPOINT`, `TEST_REGISTRY_ENDPOINT` to centralized `TestConstants`
- `crates/server/src/ollama.rs`: Moved `TEST_OLLAMA_UNUSED_PORT` inside `#[cfg(test)]`
- `crates/distributed/src/songbird_integration/connection.rs`: Local test constants for
  gRPC/AMQP/HTTP endpoints
- `crates/distributed/src/songbird_integration/load_balancing.rs`: `TEST_MOCK_ENDPOINT`
- `crates/runtime/gpu/src/distributed/tower_manager.rs`: `TEST_TOWER_ADDR_1/2`

### Documentation Policy — `warn(missing_docs)` Deferred
- Attempted blanket `#![warn(missing_docs)]` on 33 crates — reverted due to conflict
  with `-D warnings` CI gate (266+ undocumented items)
- Strategy: staged rollout per `DEBT.md` — add `warn(missing_docs)` as crates reach
  documentation completion, not before

### Debris Cleanup
- `examples/squirrel_mcp_coordination_demo.rs`: Removed 420+ lines of dead commented-out
  code. Fixed SPDX header (`AGPL-3.0-or-later` → `AGPL-3.0-only`). Retained placeholder
  main with status message.
- `crates/core/hw-learn/scripts/capture_mmiotrace.sh`: Updated stale CLI reference
  (`hw-learn diff` → JSON-RPC method calls via toadstool daemon)

### Audit Findings — No Action Required
- **TODOs/FIXMEs**: Zero in `.rs` files
- **NOTE(async-dyn)**: 50+ occurrences, all valid (async fn in dyn trait still needs `#[async_trait]`)
- **Session markers** (S155/S155b): Historical, intentional — left as fossil record
- **TEMPORARY in gpu_concurrent_comprehensive_tests.rs**: Active investigation, tracked
- **Deprecated APIs** (`get_socket_path_for_service`, `get_primal_default_port`): All
  production callers migrated; remaining uses are tests/docs/deprecated wrappers

## Metrics

| Metric | Before (S157b) | After (S158) |
|--------|-----------------|--------------|
| SIGSEGV in full suite | Intermittent | **Fixed** |
| `forbid(unsafe_code)` crates | 22 | **29** |
| License-workspace compliance | 39/56 crates | **56/56 crates** |
| Cargo.toml with explicit license | 17 | **0** (all inherit) |
| Test suite | 21,156+ pass | **21,156+ pass** |
| Clippy pedantic+nursery | 0 warnings | **0 warnings** |
| Format diffs | 0 | **0** |
| Doc warnings | 0 | **0** |
| Commented-out code | 420+ lines | **0** |

## Inter-Primal Impact

None. No protocol or API changes. All fixes were internal (safety, licensing, test
constants, debris cleanup). The SIGSEGV fix only affects toadStool's own test harness.

## Blocking Issues

- **Pre-existing flaky test**: `resolve_family_id_biomeos_fallback` fails intermittently
  in full suite due to env var race condition. Passes in isolation. Not a regression.

## Next Steps

- **P1**: Test coverage → 90% (currently ~83%, gap in hardware-dependent code)
- **P1**: `warn(missing_docs)` staged rollout — document crates incrementally
- **P2**: Expand integration tests for compute triangle (toadStool/barraCuda/coralReef)
- **P2**: Property-based testing for GPU dispatch and UniBin serialization
- **P3**: Resolve `resolve_family_id_biomeos_fallback` flakiness (env var isolation)
