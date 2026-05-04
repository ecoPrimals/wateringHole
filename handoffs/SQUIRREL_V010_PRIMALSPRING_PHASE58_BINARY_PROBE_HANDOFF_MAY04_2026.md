# Squirrel v0.1.0 — primalSpring Phase 58 Audit Response

**Date**: May 4, 2026  
**Session**: AX  
**Quality Gates**: fmt ✓ | clippy 0 warnings ✓ | 7,213 tests ✓ | deny ✓

---

## Audit Items

### 1. Phase 3 transport encryption — binary probe handling (HIGH) → RESOLVED

**Problem**: Squirrel closed the connection on unexpected binary data during BTSP probe.
When primalSpring (or any client) sent non-BTSP binary data to a BTSP-guarded socket,
`maybe_handshake` treated non-`{` bytes as a binary BTSP ClientHello, which failed
and triggered `warn!` + `send_error_frame` — the probing client doesn't speak BTSP,
so the error frame is useless and the connection is dropped.

**Fix**: Added first-byte heuristic in `maybe_handshake`:
- `0x00` first byte → legitimate BTSP binary frame (length prefix); handshake proceeds
- `{` first byte → JSON-line auto-detect (existing path)
- Any other byte → `BtspError::BinaryProbe`; `accept_with_btsp` handles at `debug` level,
  closes connection gracefully without sending a BTSP error frame

**Note on "responds in plaintext"**: The negotiate *response* is plaintext NDJSON by
protocol design — the client must read it to learn the cipher before switching. All
*subsequent* messages use encrypted framing. This is correct behavior.

### 2. `inference.register_provider` production path (MEDIUM) → ALREADY COMPLETE

Investigated and confirmed fully wired:
- JSON-RPC dispatch → `handle_inference_register_provider` → `AiRouter::register_remote_provider`
- Creates `RemoteInferenceAdapter`, upserts into live provider list (`RwLock<Vec<Arc<AiProvider>>>`)
- Wire integration tests exist in `crates/main/tests/inference_register_provider_tests.rs`
- Supports both Unix socket and Ollama-style HTTP endpoint registration
- Springs send `inference.register_provider` with `provider_id`, `socket` or `endpoint`, `capabilities`

### 3. `discovery.register` naming — GAP-06 (COSMETIC) → ALREADY CLOSED

Confirmed closed in session AV (May 3, 2026). `CONSUMED_CAPABILITIES` uses
canonical `ipc.register`, `ipc.heartbeat`, `ipc.find_provider`. Zero production
`discovery.register` string literals remain.

---

## Files Modified

- `crates/main/src/rpc/btsp_handshake/btsp_handshake_wire.rs` — added `BinaryProbe` variant to `BtspError`
- `crates/main/src/rpc/btsp_handshake/mod.rs` — first-byte heuristic in `maybe_handshake`
- `crates/main/src/rpc/jsonrpc_server.rs` — `accept_with_btsp` handles `BinaryProbe` gracefully
- `crates/main/src/rpc/btsp_handshake/btsp_handshake_tests.rs` — 3 new tests (HTTP probe, TLS probe, 0x00 still routes to BTSP)
- `CHANGELOG.md`, `CURRENT_STATUS.md`, `README.md` — updated
