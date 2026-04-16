<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Iteration 83 Handoff

**Date**: April 16, 2026
**Phase**: 10 — Drop jsonrpsee, Ecosystem-Standard NDJSON JSON-RPC
**Tests**: 4,509 passing, 0 failed, 153 ignored (hardware-gated). Zero clippy warnings.

---

## Summary

Removed `jsonrpsee` entirely from coralReef. JSON-RPC is now pure `serde_json` manual
dispatch over newline-delimited TCP and Unix sockets — the same pattern used by songBird
(`TowerAtomicServer`) and bearDog (`HandlerRegistry`).

## Ecosystem Pattern Note

**All three primals now share the same JSON-RPC architecture:**

| Primal    | Server dispatch       | Wire framing | Trait style     | jsonrpsee | async-trait |
|-----------|-----------------------|--------------|-----------------|-----------|-------------|
| songBird  | `JsonRpcHandler` match | NDJSON       | RPITIT          | No        | No          |
| bearDog   | `HandlerRegistry` scan | NDJSON       | `#[async_trait]` | No        | Direct dep  |
| coralReef | `dispatch_jsonrpc` match | NDJSON     | sync (spawn_blocking) | **No** | **No** |

### Pattern: Manual serde_json JSON-RPC dispatch

1. **Parse**: `serde_json::from_str::<JsonRpcRequest>(line)`
2. **Route**: `match request.method.as_str() { "domain.operation" => ... }`
3. **Respond**: `serde_json::to_string(&JsonRpcResponse { ... })` + `\n`
4. **Frame**: One JSON object per line (NDJSON), no HTTP

### Benefits over jsonrpsee

- Zero `async-trait` (no heap-allocated futures on dispatch hot path)
- Zero `hyper`/`http`/`tower` (no HTTP stack for primal-to-primal IPC)
- Zero proc macros (`#[rpc(server)]` → plain `match`)
- Compile-time improvement: fewer transitive crates
- Wire compatibility: BTSP first-byte peek works at stream level (no HTTP framing)
- Debuggable: `echo '{"jsonrpc":"2.0","method":"health.check","params":[],"id":1}' | nc localhost 9090`

### primal-rpc-client Update

Added `TcpLine` and `UnixLine` transport variants for NDJSON framing:

```rust
let client = RpcClient::tcp_line(addr);     // NDJSON over TCP
let client = RpcClient::unix_line(path);    // NDJSON over Unix socket
let client = RpcClient::tcp(addr);          // HTTP (legacy, still available)
```

Downstream primals using `primal-rpc-client` should prefer `tcp_line`/`unix_line` when
connecting to coralReef.

## Remaining Gaps

| Gap | Status | Owner |
|-----|--------|-------|
| Transitive libc (tokio/mio) | Permanent coexistence — mio#1735 DECLINED | Upstream |
| bearDog `#[async_trait]` on `MethodHandler` | bearDog-local decision | bearDog team |

## What Changed

- Deleted `crates/coralreef-core/src/ipc/jsonrpc.rs` (jsonrpsee HTTP server, 195 LOC)
- Promoted `start_newline_tcp_jsonrpc` as primary JSON-RPC transport
- Removed `jsonrpsee`, `jsonrpsee-http-client`, `jsonrpsee-core` from all Cargo.toml
- Simplified `cmd_server` CLI (removed `--port`, `--bind` flags)
- Added `Transport::TcpLine`/`UnixLine` + `RpcClient::tcp_line`/`unix_line` to `primal-rpc-client`
- Migrated ~30 tests + 2 e2e test files from HTTP to NDJSON transport
