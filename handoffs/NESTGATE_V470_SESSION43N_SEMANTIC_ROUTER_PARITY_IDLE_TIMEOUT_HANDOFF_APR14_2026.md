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

### Finding 2: Half-open connections stay alive indefinitely → event-driven lifecycle

**Root cause**: All 3 keep-alive read loops performed bare `reader.read_until(b'\n', ...)`
with no idle detection. A client that connects and stops sending data holds the
connection open forever.

**Fix (evolved)**: Replaced brute-force `tokio::time::timeout()` wrapping with proper
`tokio::select!`-based event loops. This is fundamentally different:

- **`tokio::select!`** multiplexes I/O readiness and idle detection as discrete events
- **Resettable idle timer** via `pin!(sleep)` + `.reset()` — models "time since last
  activity" as explicit connection state, resets on every request
- **Graceful close**: before disconnecting, the server sends a `connection.closing`
  JSON-RPC notification with `reason`, `idle_timeout_secs`, and `requests_served`,
  giving clients the opportunity to reconnect or flush pending work
- **Extensible**: adding shutdown channels or rate-limit events is a single `select!`
  arm addition — no restructuring needed

| Server Path | Idle Limit | Pattern | Location |
|------------|-----------|---------|----------|
| Isomorphic UDS | 300s | `select!` + `pin!(sleep)` | `isomorphic_ipc/server.rs::CONNECTION_IDLE_LIMIT` |
| Legacy `JsonRpcUnixServer` | 300s | `select!` + `pin!(sleep)` | `unix_socket_server/mod.rs::CONNECTION_IDLE_LIMIT` |
| TCP fallback | 300s | `select!` + `pin!(sleep)` | `isomorphic_ipc/tcp_fallback.rs::CONNECTION_IDLE_LIMIT` |

---

## Items for primalSpring to Update

1. **benchScale exp095**: `storage.retrieve_range`, `storage.object.size`, and
   `storage.namespaces.list` should now return valid results via semantic router path.
   Re-run validation against NestGate at this commit.

2. **exp082 (idle timeout)**: Connections now receive a `connection.closing` JSON-RPC
   notification before teardown after 5 minutes idle. Clients can listen for this
   notification to distinguish idle-close from network failure. Verify with a
   connect-then-idle test pattern.

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
