# ToadStool S203h Handoff — benchScale: TCP Idle Timeout

**Date**: April 14, 2026
**Primal**: ToadStool
**Session**: S203h
**Status**: DELIVERED — benchScale exp082 resolved

## Finding

primalSpring benchScale validation (April 14, 2026): no idle timeout on TCP
connections. exp082 half-open test held a connection open for 10s with no
activity — ToadStool kept it alive indefinitely. Low severity but in
multi-gate WAN deployments stale connections could accumulate.

## Resolution

### 1. TCP Idle Timeout Constant

`core/config/defaults/network.rs`:
- `TCP_IDLE_TIMEOUT_SECS = 300` (5 minutes)
- Override via `TOADSTOOL_TCP_IDLE_TIMEOUT_SECS` environment variable

### 2. JSON-RPC TCP Handler (`pure_jsonrpc/connection/tcp.rs`)

All three read paths now wrapped with `tokio::time::timeout(idle_timeout, ...)`:
- **Initial read**: first-line protocol detection (HTTP vs NDJSON)
- **HTTP keep-alive loop**: waiting for next HTTP request between keep-alive requests
- **NDJSON loop**: waiting for next JSON-RPC line

On timeout, the connection is closed gracefully (debug log, no error propagation).
The timer resets after each successful request — active connections are never killed.

### 3. tarpc TCP Handler (`tarpc_server/connection.rs`)

New `serve_on_tarpc_channel_with_idle_timeout` function:
- Iterates the tarpc channel's RPC stream via `rpcs.next()`
- Each `.next()` call wrapped in `tokio::time::timeout(idle_timeout, ...)`
- Timer resets after each RPC — only truly idle connections are closed

### 4. TCP_NODELAY

`set_nodelay(true)` applied to all accepted TCP streams (both JSON-RPC and tarpc
accept loops) for lower latency.

### 5. Tests

- `test_tcp_idle_timeout_default`: verifies default 300s from constant
- `test_tcp_idle_timeout_env_override`: verifies `TOADSTOOL_TCP_IDLE_TIMEOUT_SECS=42`

## Verification

- `cargo test -p toadstool-server --lib`: 646 tests, 0 failures (+2 new)
- `cargo clippy -p toadstool-server --all-targets`: 0 warnings
- `cargo check --workspace`: clean

## Impact

- Half-open TCP connections now auto-close after 5 minutes of inactivity
- Active connections with regular traffic are never affected (timer resets per request/RPC)
- Configurable via env var for different deployment topologies
- Unix socket connections (primary IPC path) are unaffected — this is TCP-only
