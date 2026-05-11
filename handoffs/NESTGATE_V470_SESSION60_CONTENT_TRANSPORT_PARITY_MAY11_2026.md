# NestGate Session 60 — content.* Transport Parity + lifecycle.status

**Date**: May 11, 2026  
**Scope**: CRITICAL transport parity fix — `content.*` methods routed through ALL transport paths  
**Commit**: Session 60 (nestgate 4.7.0-dev)

---

## Problem

primalSpring audit identified that `content.*` methods (put, get, exists, list, publish, resolve, promote, collections) were implemented only on the primary `unix_socket_server` dispatch path. Three other transport surfaces returned "Method not found":

1. **SemanticRouter** (`call_method`) — tarpc-oriented callers
2. **Isomorphic IPC** (`UnixSocketRpcHandler`) — separate dispatch table
3. **HTTP API** (`NestGateRpcHandler` + `NestGateJsonRpcHandler`) — `nestgate-api` crate

This blocked: petalTongue `backend=nestgate`, projectNUCLEUS Pillars 1-3, sovereign content pipeline.

## Solution

### Architecture

Rather than duplicating content handler logic across 4 transport surfaces, we:

1. **Promoted visibility** — `content_handlers` module changed from `mod` to `pub(crate) mod`; handler functions from `pub(super)` to `pub` (module already restricts to crate).

2. **Created `content_ops` public facade** — `nestgate-rpc::rpc::content_ops` module provides stateless functions (`put`, `get`, `exists`, etc.) that cache a shared `StorageState` via `OnceLock`. Accessible from any downstream crate via `nestgate_core::rpc::content_ops`.

3. **Wired all surfaces**:
   - **SemanticRouter**: New `semantic_router/content.rs` module with 8 match arms
   - **UnixSocketRpcHandler**: 8 handler functions in `unix_adapter_handlers.rs` delegating through `content_state()`
   - **NestGateRpcHandler** (HTTP): Direct calls to `nestgate_core::rpc::content_ops`
   - **NestGateJsonRpcHandler** (`/jsonrpc`): Prefix match on `content.*` → `handle_content_method()`

### lifecycle.status

Also implemented across all 4 surfaces:
- Classified as Public in `method_gate.rs` (already was)
- Added to `is_btsp_exempt_method` list
- Added to `UNIX_SOCKET_SUPPORTED_METHODS` (67 total, up from 66)
- All `capabilities.list` surfaces now advertise it

### Files Changed

**nestgate-rpc** (10 files):
- `unix_socket_server/content_handlers.rs` — visibility `pub(super)` → `pub`
- `unix_socket_server/mod.rs` — `mod content_handlers` → `pub(crate) mod`
- `unix_socket_server/dispatch.rs` — added `lifecycle.status` handler
- `semantic_router/mod.rs` — added `content.*` + `lifecycle.status` match arms
- `semantic_router/content.rs` — **new** content domain delegation module
- `semantic_router/health.rs` — added `lifecycle_status()` function
- `semantic_router/capabilities.rs` — added content + lifecycle to method list
- `isomorphic_ipc/unix_adapter/mod.rs` — added content + lifecycle dispatch arms
- `isomorphic_ipc/unix_adapter/unix_adapter_handlers.rs` — added content handlers + capabilities
- `rpc/content_ops.rs` — **new** public stateless facade
- `rpc/mod.rs` — registered `content_ops` module, `lifecycle.status` in BTSP exempt list
- `model_cache_handlers.rs` — added `lifecycle.status` to UNIX_SOCKET_SUPPORTED_METHODS

**nestgate-api** (2 files):
- `transport/handlers.rs` — added content + lifecycle dispatch, `handle_lifecycle_status()`
- `nestgate_rpc_service/json_rpc_handler.rs` — added content + lifecycle routing

## Verification

- `cargo check --workspace` — PASS
- `cargo clippy -p nestgate-rpc -- -D warnings` — zero warnings
- `cargo fmt --check` — clean
- `cargo test --workspace` — all tests pass, zero regressions

## What This Unblocks

- **petalTongue** `backend=nestgate` — `content.resolve` now reachable through composed transport paths
- **projectNUCLEUS** Pillars 1-3 — `nestgate_content_parity.sh` can validate
- **primalSpring** contract tests — `s_nestgate_content_pipeline`, Content Gate 1-3

## Remaining Items (Not In Scope)

- `storage.list` BTSP scoping (Phase 2b, low risk — opaque hashes only)
- Pre-existing clippy warnings in `nestgate-api/handlers/zfs/native_async/traits.rs` (16 missing doc warnings, unrelated)
