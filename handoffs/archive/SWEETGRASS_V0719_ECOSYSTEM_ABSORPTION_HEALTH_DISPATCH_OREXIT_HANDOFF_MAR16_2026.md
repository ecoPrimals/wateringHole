# SweetGrass v0.7.19 — Ecosystem Absorption: Health Probes, DispatchOutcome, OrExit

**Date**: 2026-03-16
**Primal**: sweetGrass
**Version**: 0.7.18 → 0.7.19
**Type**: Ecosystem absorption, protocol compliance, quality evolution

## Summary

Comprehensive absorption of ecosystem patterns identified during the
hotSpring/ecoSprings/phase1/phase2/wateringHole review:

1. **wateringHole protocol v3.0 health probes** — `health.liveness` + `health.readiness`
2. **IpcErrorPhase classification helpers** — retry gating, circuit breaker integration
3. **DispatchOutcome** — protocol vs application error separation
4. **OrExit trait** — zero-panic binary validation
5. **eprintln → tracing** — structured logging throughout binary

## Changes

### P0: Health Probes (wateringHole PRIMAL_IPC_PROTOCOL v3.0)

Added `health.liveness` and `health.readiness` as JSON-RPC methods and tarpc
service methods, aligned with coralReef and healthSpring implementations.

- `health.liveness` — zero-cost probe (no store query), returns `{ "alive": true }`
- `health.readiness` — store availability check, returns `{ "ready": bool }`
- Both exposed via tarpc `SweetGrassRpc` trait

**Files**: `handlers/jsonrpc/health.rs`, `handlers/jsonrpc/mod.rs`, `rpc.rs`, `server/mod.rs`

### P0: IpcErrorPhase Classification Helpers

Added methods to `IpcErrorPhase` for retry gating and error classification:

- `is_retriable()` — Connect, Write, Read, HttpStatus(502..=504)
- `is_timeout_likely()` — Read, HttpStatus(504)
- `is_method_not_found()` — JsonRpcError(-32601)
- `is_application_error()` — JsonRpcError(*), HttpStatus(400|404|422)

Aligned with rhizoCrypt `should_retry()` and loamSpine `is_recoverable()`.

**Files**: `sweet-grass-integration/src/error.rs`

### P1: DispatchOutcome

New `DispatchOutcome` enum separating protocol errors from application errors:

- `Success(Value)` — handler returned a result
- `ProtocolError { code, message }` — request never reached a handler
- `ApplicationError { code, message }` — handler ran but returned domain error

`process_single` now uses `dispatch_classified()` which returns `DispatchOutcome`.

**Files**: `handlers/jsonrpc/mod.rs`

### P1: #[allow] → #[expect(reason)] Migration

Audited all `#[allow]` attributes. Retained `#[allow]` only for items that are
conditionally compiled (feature-gated test mocks). All other suppressions use
`#[expect(reason)]` per groundSpring/wetSpring/rhizoCrypt standard.

### P2: OrExit Trait

New `exit` module with:

- `OrExit<T>` trait for `Result<T, E>` and `Option<T>`
- Centralized `exit_code` module (SUCCESS=0, GENERAL_ERROR=1, CONFIG_ERROR=2, NETWORK_ERROR=3)
- Binary entrypoint (`service.rs`) refactored to use `OrExit` for address parsing

**Files**: `sweet-grass-service/src/exit.rs`, `bin/service.rs`

### Binary Cleanup

- `eprintln!` → `tracing::error!` throughout binary entrypoint
- Exit codes centralized via `exit::exit_code` module

## Metrics

| Metric | v0.7.18 | v0.7.19 | Delta |
|--------|---------|---------|-------|
| JSON-RPC methods | 22 | 24 | +2 |
| tarpc methods | 16 | 18 | +2 |
| Tests passing | 1,017 | 1,030 | +13 |
| Clippy warnings | 0 | 0 | — |
| `eprintln!` in prod | 2 | 0 | -2 |
| `#[allow]` (reducible) | 4 | 0 | -4 |

## Upstream Impact

### wateringHole Standards Compliance

- ✅ `PRIMAL_IPC_PROTOCOL` v3.0 — health.liveness + health.readiness
- ✅ `UNIBIN_ARCHITECTURE_STANDARD` — OrExit, centralized exit codes
- ✅ `SEMANTIC_METHOD_NAMING_STANDARD` — health.{liveness,readiness}

### Ecosystem Alignment

- **coralReef**: health probe pattern absorbed
- **rhizoCrypt**: IpcErrorPhase helpers + DispatchOutcome pattern absorbed
- **loamSpine**: is_recoverable() classification pattern absorbed
- **biomeOS**: OrExit trait absorbed
- **groundSpring/wetSpring**: #[expect(reason)] migration pattern absorbed

## Next Priorities

1. IPC chaos tests (fault injection from coralReef)
2. Structured tracing spans for IPC calls
3. `deny.toml` dependency audit refresh
4. Integration test coverage for tarpc health probes
