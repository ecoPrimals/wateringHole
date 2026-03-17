<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.9 — Ecosystem Absorption Handoff

**Date**: March 16, 2026
**From**: Squirrel AI Primal
**Status**: GREEN — 4,862 tests passing, clippy clean, docs clean

## Summary

Ecosystem-wide absorption pass: integrated cross-primal patterns from rhizoCrypt,
sweetGrass, coralReef, petalTongue, and wetSpring. Upgraded tarpc to 0.37, hardened
deny.toml, migrated to `#[expect(reason)]`, and added structured IPC error types,
NDJSON streaming, typed compute dispatch, and dual-format capability parsing.

## Changes

### P1 — Immediate (All Complete)

| Item | Detail |
|------|--------|
| `capability.list` format | Added flat `capabilities` array, `domains` list, `locality` (local/external) for ecosystem consensus |
| Structured IPC errors | `IpcErrorPhase` enum (Connect, Write, Read, JsonRpcError, NoResult) with `is_retryable()` — from rhizoCrypt v0.13 |
| `#[expect(reason)]` migration | 52 `#[allow(dead_code)]` → `#[expect(dead_code, reason = "...")]` with automatic cleanup of unfulfilled expectations |
| tarpc 0.37 | Upgraded from 0.34; `Context::deadline` updated from `SystemTime` to `Instant` |
| deny.toml hardened | `yanked = "deny"` (was "warn") |

### P2 — Near-term (All Complete)

| Item | Detail |
|------|--------|
| Generic `socket_env_var()` | `socket_env_var("rhizocrypt")` → `"RHIZOCRYPT_SOCKET"` — no per-primal code needed |
| Capability domain introspection | `capability.list` now includes `domains`, `locality.local`, `locality.external` |
| Cross-primal IPC e2e tests | 6 tests: health, capability list format, error propagation, concurrent, disconnect |
| Typed `compute.dispatch` client | `ComputeDispatchRequest::inference()` / `::embedding()` for ToadStool GPU routing |
| Dual-format capability parsing | `parse_capabilities_from_response()` handles both flat array and legacy methods-object |

### P3 — Strategic (All Complete)

| Item | Detail |
|------|--------|
| NDJSON streaming | `StreamItem` / `StreamKind` (data, progress, error, done, heartbeat) for pipeline coordination |
| DI config reader | `from_env_reader(key, default, reader_fn)` for testable env-driven config |
| LazyLock migration | Already complete — all `lazy_static`/`once_cell` replaced with `std::sync::OnceLock` |

## Metrics

| Metric | alpha.8 | alpha.9 |
|--------|---------|---------|
| Tests | 4,835 | 4,862 (+27) |
| tarpc | 0.34 | 0.37 |
| `#[allow(dead_code)]` in prod | 52 | 0 |
| deny.toml yanked | warn | deny |
| New modules | — | streaming, compute_dispatch |
| Cross-primal e2e tests | 0 | 6 |

## New Public API Surface

```
universal_patterns::streaming::{StreamItem, StreamKind}
universal_patterns::compute_dispatch::{ComputeDispatchRequest, ComputeDispatchResponse}
universal_patterns::ipc_client::{IpcErrorPhase, parse_capabilities_from_response}
universal_constants::network::{socket_env_var, address_env_var}
universal_constants::config_helpers::from_env_reader
```

## Known Issues (Unchanged)

1. `test_load_from_json_file` flaky (env var pollution — needs `#[serial]`)
2. Coverage at 69% (target 90%)
3. ~800 `unwrap()`/`expect()` in non-test production code
4. ~150 hardcoded primal name literals remaining

## Ecosystem Interop Notes

- Squirrel's `capability.list` now includes the `capabilities` flat array that
  sweetGrass, rhizoCrypt, and toadStool have standardized on.
- `IpcErrorPhase` enables retry-aware error handling matching rhizoCrypt's pattern.
- `ComputeDispatchRequest` types are wire-compatible with ToadStool's
  `compute.dispatch` JSON-RPC method.
- `StreamItem` NDJSON format is compatible with rhizoCrypt's streaming pipeline.
- Dual-format capability parsing means Squirrel can interoperate with primals
  that still use the legacy `methods`-object response format.
