# petalTongue v1.6.6 — Ecosystem Absorption: IPC Resilience, Health Triad, NDJSON, OrExit

**Date**: March 16, 2026
**Primal**: petalTongue v1.6.6
**Session**: Cross-ecosystem absorption from 7 springs + 13 primals
**Status**: Complete — all checks pass

---

## Executive Summary

Pulled and reviewed all 7 springs (hotSpring, groundSpring, neuralSpring, wetSpring, airSpring, healthSpring, ludoSpring) and all 13 primals (phase1, phase2, ecosystem-level). Identified 12 absorption opportunities across P0/P1/P2 priorities. Executed all.

**Tests**: 5,404 → 5,447 (+43 new tests)
**All checks pass**: fmt, clippy (pedantic+nursery), doc, test

---

## What Was Absorbed

### P0 — High Priority

#### 1. `IpcErrorPhase` structured IPC errors
- **Source**: rhizoCrypt v0.13, loamSpine v0.9.2, sweetGrass v0.7.18, healthSpring V31
- **New module**: `petal-tongue-ipc/src/ipc_errors.rs`
- `IpcErrorPhase` enum: Connect, Write, Read, InvalidJson, JsonRpcError, Timeout, Serialization
- Methods: `is_recoverable()`, `is_retriable()`, `is_timeout()`, `is_method_not_found()`

#### 2. `extract_rpc_error()` centralized RPC error extraction
- **Source**: wetSpring V124, airSpring V086, healthSpring V31
- `extract_rpc_error(response: &Value) -> Option<(i64, String)>`

#### 3. NDJSON `StreamItem` for pipeline streaming
- **Source**: rhizoCrypt v0.13, sweetGrass v0.7.18, biomeOS v2.47
- `StreamItem` enum: Data, Progress, End, Error
- Methods: `is_terminal()`, `to_ndjson_line()`, `parse_ndjson_line()`

#### 4. `OrExit<T>` zero-panic trait
- **Source**: wetSpring V123, neuralSpring V110, healthSpring V31
- **New module**: `petal-tongue-core/src/or_exit.rs`
- Impls for `Result<T, E>` and `Option<T>`

### P1 — Medium Priority

#### 5. Health IPC triad
- **Source**: coralReef I51, toadStool S156
- Added `health.liveness` (alive probe) and `health.readiness` (graph + viz state check)
- Added to `capability.list` methods array

#### 6. Enriched `capability.list` response
- **Source**: healthSpring V31
- Added `operation_dependencies` DAG and `cost_estimates` (cpu_ms, gpu_eligible)

#### 7. Dual-format capability parsing
- **Source**: neuralSpring V110, groundSpring V110, wetSpring V123, airSpring V085
- **New module**: `petal-tongue-discovery/src/capability_parse.rs`
- Parses both flat string arrays and nested object arrays
- Wired into neural_api_provider, songbird_client, unix_socket_provider

#### 8. CircuitBreaker + RetryPolicy
- **Source**: rhizoCrypt v0.13
- **New module**: `petal-tongue-ipc/src/resilience.rs`
- `RetryPolicy`: exponential backoff, configurable attempts/delays
- `CircuitBreaker`: Closed/Open/HalfOpen states, failure threshold, recovery timeout

#### 9. Generic discovery helpers
- **Source**: loamSpine v0.9.2, sweetGrass v0.7.17
- **New module**: `petal-tongue-ipc/src/discovery_helpers.rs`
- `socket_env_var()`, `address_env_var()`, `resolve_primal_socket()`
- Injectable env reader variant for test isolation (DI config pattern)

### Already Complete (from previous sessions)

- `#[expect(reason)]` migration — already done across core files
- `Arc<str>` zero-copy IDs
- proptest for JSON-RPC + core types
- Cross-primal e2e tests
- `deny.toml` supply-chain hygiene
- `temp-env` for safe env testing

---

## New Files

| File | Lines | Purpose |
|------|-------|---------|
| `petal-tongue-ipc/src/ipc_errors.rs` | ~230 | IpcErrorPhase, extract_rpc_error, StreamItem |
| `petal-tongue-ipc/src/resilience.rs` | ~240 | CircuitBreaker, RetryPolicy |
| `petal-tongue-ipc/src/discovery_helpers.rs` | ~136 | Socket/address env helpers, primal socket resolution |
| `petal-tongue-core/src/or_exit.rs` | ~65 | OrExit<T> trait |
| `petal-tongue-discovery/src/capability_parse.rs` | ~103 | Dual-format capability parsing |

---

## Verification

| Check | Status |
|-------|--------|
| `cargo fmt --check` | **PASS** |
| `cargo clippy --all-features --all-targets -- -D warnings` | **PASS** |
| `cargo test --all-features --workspace` | **PASS** (5,447 passed, 0 failed) |
| All files < 1000 lines | **PASS** |

---

**License**: AGPL-3.0-or-later
