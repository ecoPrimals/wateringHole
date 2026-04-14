# NestGate v4.7.0-dev — Session 43n Handoff

**Date**: April 14, 2026
**Session**: 43n — Semantic router streaming parity + idle timeout (LD-04)
**Triggered by**: primalSpring benchScale validation (April 14, 2026)

---

## primalSpring Audit Triage

The benchScale validation reported two findings:

### Finding 1: Streaming methods return "Method not found"

**Root cause**: The 5 streaming storage methods were wired in both the isomorphic IPC
adapter and legacy `JsonRpcUnixServer` dispatch (Session 43h/43l), but were **never
registered in the semantic router** (`SemanticRouter::call_method`). Any client using
the tarpc path or semantic method routing received -32601 "Method not found".

The `capabilities.list` response from the semantic router also omitted these methods,
advertising only 32 methods instead of 37.

| Method | UDS Adapter | Legacy Server | Semantic Router (before) | Semantic Router (after) |
|--------|------------|---------------|-------------------------|------------------------|
| `storage.store_blob` | WIRED | WIRED | **MISSING** | **WIRED** |
| `storage.retrieve_blob` | WIRED | WIRED | **MISSING** | **WIRED** |
| `storage.retrieve_range` | WIRED | WIRED | **MISSING** | **WIRED** |
| `storage.object.size` | WIRED | WIRED | **MISSING** | **WIRED** |
| `storage.namespaces.list` | WIRED | WIRED | **MISSING** | **WIRED** |

**Fix**: Added filesystem-backed handlers to `semantic_router/storage.rs` matching the
UDS implementation behavior (base64 encoding, `_blobs/` path layout, 4 MiB max chunk,
underscore-prefix filtering for namespaces). Updated `semantic_router/capabilities.rs`
to advertise all 5 methods.

### Finding 2: Idle timeout — half-open connections stay alive indefinitely

**Root cause**: All 3 keep-alive read loops (`json_rpc_keep_alive_loop` in isomorphic
server, `json_rpc_loop` in legacy server, `handle_tcp_connection` in TCP fallback)
performed bare `reader.read_until(b'\n', ...)` with no timeout. A client that connects
and stops sending data holds the connection open forever.

**Fix**: Wrapped all 3 read operations with `tokio::time::timeout(Duration::from_secs(300))`.
Connections idle for 5 minutes are automatically closed with a debug log. The 300s timeout
is generous enough for legitimate interactive sessions while preventing resource exhaustion
from abandoned connections.

| Server Path | Timeout | Location |
|------------|---------|----------|
| Isomorphic UDS | 300s | `isomorphic_ipc/server.rs::IDLE_TIMEOUT` |
| Legacy `JsonRpcUnixServer` | 300s | `unix_socket_server/mod.rs::IDLE_TIMEOUT` |
| TCP fallback | 300s | `isomorphic_ipc/tcp_fallback.rs::TCP_IDLE_TIMEOUT` |

---

## Items for primalSpring to Update

1. **benchScale exp095**: `storage.retrieve_range`, `storage.object.size`, and
   `storage.namespaces.list` should now return valid results via semantic router path.
   Re-run validation against NestGate at this commit.

2. **exp082 (idle timeout)**: Half-open connections will now close after 5 minutes.
   Verify with a connect-then-idle test pattern.

3. **PRIMAL_GAPS.md**: Remove "streaming methods not registered" and "idle timeout"
   from NestGate findings. Remaining tracked items: coverage 80→90%, 187 deprecated
   config migration markers.

---

## Verification

- **Build**: `cargo check --workspace` PASS
- **Clippy**: `cargo clippy --workspace --all-targets --all-features -- -D warnings` PASS (0 warnings)
- **Format**: `cargo fmt --check` PASS
- **Tests**: 11,994 passing (+175), 0 failures, 460 ignored
- **Crosscheck**: `cargo test --test capability_registry_crosscheck` — 11/11 PASS

---

## Files Changed

| File | Change |
|------|--------|
| `nestgate-rpc/src/rpc/semantic_router/storage.rs` | +5 streaming method handlers + 15 tests |
| `nestgate-rpc/src/rpc/semantic_router/mod.rs` | +5 dispatch arms in `call_method` |
| `nestgate-rpc/src/rpc/semantic_router/capabilities.rs` | +5 methods in `capabilities.list` response |
| `nestgate-rpc/src/rpc/isomorphic_ipc/server.rs` | Idle timeout on UDS keep-alive loop |
| `nestgate-rpc/src/rpc/unix_socket_server/mod.rs` | Idle timeout on legacy keep-alive loop |
| `nestgate-rpc/src/rpc/isomorphic_ipc/tcp_fallback.rs` | Idle timeout on TCP keep-alive loop |
| `nestgate-rpc/src/rpc/unix_socket_server/tests.rs` | +1 idle timeout test |
| Root docs (`STATUS.md`, `README.md`, `CONTEXT.md`, `CHANGELOG.md`) | Test counts, session ref |
