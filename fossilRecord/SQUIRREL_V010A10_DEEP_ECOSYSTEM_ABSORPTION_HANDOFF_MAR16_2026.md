<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.10 — Deep Ecosystem Absorption Handoff

**Date**: 2026-03-16
**Version**: 0.1.0-alpha.10
**Tests**: 4,925 passing / 0 failed
**Source**: All springs + primals (toadStool S157b, coralReef Iter 52, biomeOS v2.48,
neuralSpring V112, groundSpring V112, loamSpine v0.9.3, sweetGrass v0.7.19,
barraCuda v0.3.5, petalTongue v1.6.6, airSpring v0.8.7, rhizoCrypt v0.13, hotSpring v0.6.32)

## Summary

Deep absorption of ecosystem-wide consensus patterns from all 12 component latest
handoffs. Focus on IPC resilience, structured error handling, zero-panic entry points,
and cross-primal discovery robustness.

## New API Surfaces

### `OrExit<T>` (universal-patterns)
- Trait extension on `Result<T, E>` and `Option<T>`
- `.or_exit("context")` → prints fatal message to stderr, exits with structured code
- `.or_exit_code("context", code)` → explicit exit code
- Centralized `exit_codes` module: SUCCESS(0), ERROR(1), CONFIG(2), NETWORK(3),
  PERMISSION(4), RESOURCE(5), INTERRUPTED(130)

### `DispatchOutcome<T>` (universal-patterns)
- `Ok(T)` / `ProtocolError { code, message }` / `ApplicationError { code, message }`
- Protocol errors = wire/routing (retry after fix)
- Application errors = business logic (do NOT retry)
- Convenience: `method_not_found()`, `invalid_params()`, `map()`, `into_result()`

### `CircuitBreaker` + `RetryPolicy` + `ResilientCaller` (universal-patterns)
- Circuit breaker: closed → open (after N failures) → half-open (after cooldown)
- Retry policy: exponential backoff with cap and jitter
- `ResilientCaller::call(f, is_retryable)` — combines both for IPC calls

### Health Probes v3.0 (PRIMAL_IPC_PROTOCOL)
- `health.liveness` → `{ alive: true, version, timestamp }`
- `health.readiness` → `{ ready: bool, checks: { capability_registry, ai_router } }`
- `system.health` retained for backward compat (full report)

### 4-Format Capability Parsing
- Flat array: `{ capabilities: [...] }`
- Legacy object: `{ methods: { ... } }`
- Nested: `{ result: { capabilities: [...] } }`
- Double-nested: `{ result: { result: { capabilities: [...] } } }`

### `PrimalManifest` Discovery
- Scans `$XDG_RUNTIME_DIR/ecoPrimals/*.json`
- `write_manifest()` / `remove_manifest()` for lifecycle
- `is_alive()` checks PID or socket existence
- `discover_by_capability()` / `discover_by_name()`

### `extract_rpc_error()` + `RpcError`
- Extracts code, message, data from JSON-RPC error responses
- `is_method_not_found()`, `is_internal()`, `is_server_error()`

### `ValidationHarness`
- Multi-check runner: `check()`, `check_async()`, `skip()`, `warn()`
- `summary()` / `to_json()` for human and machine output
- Counts: passed/failed/skipped/warnings/total

## New Tests (63 total added)
- 23 unit tests across or_exit, dispatch_outcome, circuit_breaker
- 14 manifest_discovery tests
- 12 validation_harness tests
- 7 JSON-RPC wire-format proptest fuzz
- 5 extract_rpc_error + 4-format parsing tests
- 2 primal_names tests updated

## Metrics
| Metric | Value |
|--------|-------|
| Tests | 4,925 passing (+63 from alpha.9) |
| Build | GREEN |
| Clippy | CLEAN (lib) |
| Property tests | 17 (up from 10) |
| New modules | 5 (or_exit, dispatch_outcome, circuit_breaker, manifest_discovery, validation_harness) |
| New JSON-RPC methods | 2 (health.liveness, health.readiness) |

## Ecosystem Interop Notes

- CLI `exit_codes` now re-export from `universal-patterns::exit_codes` — other
  primals can depend on the same constants
- `CircuitBreaker` parameters (5 failures, 30s cooldown) match petalTongue defaults
- `RetryPolicy` defaults (3 retries, 100ms initial, 5s max, 2x multiplier) match
  rhizoCrypt/sweetGrass ecosystem pattern
- Manifest discovery uses same `$XDG_RUNTIME_DIR/ecoPrimals/` path as rhizoCrypt
- `DispatchOutcome` is serde-serializable for wire transport if needed
- 4-format capability parsing ensures interop with primals at any evolution stage

## Codebase Hygiene Pass (same session)

### Removed
- Root `benches/` directory (9 orphan benchmark files not wired to any crate)
- 4 orphan bench files from `crates/main/benches/` (only `ecosystem_benchmarks` is wired)
- `crates/core/context/src/sync_tests_additional.rs` (orphan, never declared in lib.rs)
- `crates/core/plugins/src/tests/` (orphan directory, never declared in lib.rs)
- `crates/core/plugins/src/simple_test.rs` (orphan stub, never referenced)
- `crates/config/config.example.toml` (stale — described a different project)
- `crates/tools/ai-tools/src/config.example.toml` (legacy direct-API config)

### Fixed
- Crate count: 22 → 21 in README.md, CURRENT_STATUS.md (actual workspace members)
- 8 broken doc links cleaned: removed references to archived/deleted documents
  (`ERROR_UNIFICATION_STRATEGY.md`, `PRIMAL_COMMUNICATION_ARCHITECTURE.md`,
  `CAPABILITY_AI_MIGRATION_GUIDE.md`, `WEB_PLUGIN_MIGRATION.md`,
  `adapter-implementation-guide.md`, etc.)
- CURRENT_STATUS.md JSON-RPC table: added `health.liveness` + `health.readiness`
- universal-error README.md: license corrected from `MIT OR Apache-2.0` to `AGPL-3.0-only`
- Known Issue #10 resolved: orphan benchmark files removed

## Next Steps (P4)

- Wire `OrExit<T>` into CLI `main()` and doctor subcommand
- Wire `CircuitBreaker` into `IpcClient` for production use
- Wire `PrimalManifest` into server startup (write) and shutdown (remove)
- Wire `ValidationHarness` into `squirrel doctor` subcommand
- Wire `DispatchOutcome` into JSON-RPC method dispatch
- Replace remaining ~150 hardcoded primal name literals with `primal_names::*`
- Migrate remaining ~800 `unwrap()`/`expect()` in production code
