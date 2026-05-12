# NestGate V4.7.0 — GAP-MATRIX-04 Resolution: ZFS JSON-RPC/UDS Bridge

**Date**: April 8, 2026  
**Scope**: `nestgate-rpc`, `nestgate-api`  
**Resolves**: GAP-MATRIX-04 (Medium) — IPC Model Divergence

---

## Problem

primalSpring's live validation identified that NestGate's ZFS management
operations were only reachable via HTTP REST endpoints (`/api/v1/zfs/*`),
breaking the ecosystem's uniform JSON-RPC over UDS model that every other
primal follows. `socat`/`PrimalClient` tooling could reach `health.*`,
`storage.*`, and `capabilities.*` on the UDS socket, but ZFS pool, dataset,
and snapshot operations were invisible to the ecosystem's standard probing
path.

## Solution: Option 1 (Preferred)

Added `zfs.*` JSON-RPC methods directly to the UDS dispatch table, following
`SEMANTIC_METHOD_NAMING_STANDARD.md` (`{domain}.{operation}` format).

### 7 New Methods

| Method | Description | Params |
|--------|-------------|--------|
| `zfs.pool.list` | List all pools with size/alloc/free/health | — |
| `zfs.pool.get` | Status for a single pool | `{"pool": "name"}` |
| `zfs.pool.health` | Health summary, flags unhealthy pools | — |
| `zfs.dataset.list` | List all datasets (optionally scoped) | `{"pool": "name"}` (optional) |
| `zfs.dataset.get` | Get single dataset by name | `{"dataset": "name"}` |
| `zfs.snapshot.list` | List snapshots (optionally scoped) | `{"dataset": "name"}` (optional) |
| `zfs.health` | ZFS/zpool userland availability + version | — |

### Architecture Note

A cyclic dependency (`nestgate-rpc` -> `nestgate-zfs` -> `nestgate-core` ->
`nestgate-discovery` -> `nestgate-rpc`) prevents `nestgate-rpc` from importing
`nestgate-zfs` directly. The UDS handlers use `tokio::process::Command` to
call `zpool`/`zfs` CLI, the same stable interface that `ZfsOperations` wraps
internally. The HTTP JSON-RPC handler in `nestgate-api` uses `ZfsOperations`
directly since it can depend on `nestgate-zfs` without cycles.

### Graceful Degradation

All handlers check for `zpool`/`zfs` availability before executing. When
userland tools are missing (e.g., containers, non-ZFS hosts), they return
structured errors (`service_unavailable`) rather than crashing.

## Files Changed

| File | Change |
|------|--------|
| `nestgate-rpc/src/rpc/unix_socket_server/zfs_handlers.rs` | **NEW** — 7 JSON-RPC handlers + 8 unit tests |
| `nestgate-rpc/src/rpc/unix_socket_server/mod.rs` | 7 dispatch arms + `mod zfs_handlers` |
| `nestgate-rpc/src/rpc/model_cache_handlers.rs` | `UNIX_SOCKET_SUPPORTED_METHODS` + `discover_capabilities` |
| `nestgate-rpc/src/rpc/isomorphic_ipc/unix_adapter/unix_adapter_handlers.rs` | `capabilities_response()` |
| `nestgate-api/src/nestgate_rpc_service/json_rpc_handler.rs` | `handle_zfs_method()` + 7 semantic names |
| `CAPABILITY_MAPPINGS.md` | Added `zfs.*` domain (Section 1b, matrix row) |
| `CHANGELOG.md` | Session 35 entry |

## Verification

- `cargo clippy --workspace --all-features -- -D warnings` — 0 warnings
- `cargo test --workspace --all-features` — all passing
- `cargo fmt --all --check` — clean

## Remaining Work (Not in Scope)

- **Workspace operations via JSON-RPC**: workspace handlers shell out to
  `zfs` + `UuidManager`; need a proper backend service first.
- **Analytics/load-testing/communication**: dashboard-only surfaces. Per
  `PRIMAL_IPC_PROTOCOL.md`, HTTP REST is acceptable for dashboards.
- **Unify three JSON-RPC surfaces**: `JsonRpcServer` (jsonrpsee, not wired),
  `NestGateJsonRpcHandler` (HTTP), and UDS dispatch should converge.
- **501 stub operations** (`create_pool`, `delete_pool`, etc.): when built,
  add to both REST and UDS simultaneously.
