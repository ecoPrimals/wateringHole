# Songbird v0.2.1 — Wave 185 Handoff

**Date**: May 2, 2026
**Primal**: Songbird (Network)
**Wave**: 185
**Focus**: Deep debt cleanup — timeout centralization, JSON-RPC constructors, hardcoded elimination

---

## Summary

Wave 185 performed deep debt elimination targeting three categories: scattered Duration
literals, repeated JSON-RPC version strings, and primal-specific naming in diagnostics.

## Changes

### Timeout Centralization
- Added 11 new constants to `songbird-types/src/defaults/timeouts.rs`:
  `DEFAULT_STARTUP_TIMEOUT`, `DEFAULT_SOCKET_IO_TIMEOUT`, `DEFAULT_CONNECTIVITY_CHECK_TIMEOUT`,
  `DEFAULT_CIRCUIT_BREAKER_TIMEOUT`, `DEFAULT_RATE_LIMIT_WINDOW`, `DEFAULT_CLEANUP_INTERVAL`,
  `DEFAULT_RETRY_INITIAL_BACKOFF`, `DEFAULT_RETRY_MAX_BACKOFF`, `DEFAULT_ACCEPT_POLL_INTERVAL`
- Replaced 15+ hardcoded `Duration::from_secs/millis` literals across 13 production files

### JSON-RPC Version Constant
- Added `JSONRPC_VERSION` constant and `JsonRpcResponse::success()`/`::error()` constructors
  to `crates/songbird-orchestrator/src/ipc/pure_rust_server/protocol.rs`
- Eliminated 9 scattered `"2.0".to_string()` struct constructions

### Capability-Based Naming
- `doctor.rs`: "ToadStool (Storage)" → "Compute provider (GPU/shader)"
- `examples/future/*.rs`: Added `reason` strings to 4 bare `#[allow(dead_code)]`

### Dependency Reconciliation
- Confirmed `ring` is not in active dependency tree; `cargo deny check bans` passes

## Verification

- 28 btsp_phase3 tests pass
- 23 pure_rust_server tests pass
- 0 new clippy warnings
- 0 regressions

## Status

- BTSP Phase 3: FULL (all 3 transport paths)
- Tests: 7,803 lib passed, 0 failures, 22 ignored
- Clippy: 0 warnings
- Unsafe: 0
- Files >800L: 0
