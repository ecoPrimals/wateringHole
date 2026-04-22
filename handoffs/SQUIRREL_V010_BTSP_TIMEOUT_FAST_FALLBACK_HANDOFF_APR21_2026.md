# Squirrel v0.1.0 — BTSP Handshake Timeout Fast Fallback

**Date**: April 21, 2026
**From**: Squirrel v0.1.0-alpha.52+
**Audit**: primalSpring PG-14 follow-up — BTSP handshake timeout adds ~5s latency

## Problem

primalSpring's BTSP ClientHello is correctly auto-detected by Squirrel's PG-14
first-byte peek. The handshake proceeds but times out after 5 seconds when the
BTSP provider (BearDog) is unavailable, then the connection is silently dropped.
The client must wait for its own timeout and reconnect with cleartext JSON-RPC.
Total latency hit: ~5 seconds per guidestone run.

Since Squirrel is Nest-tier (`tower_delegated`, BTSP not required), this timeout
is pure overhead with no security benefit.

## Fix (3 changes)

### 1. Timeout reduction (5s → 1.5s, configurable)

`HANDSHAKE_TIMEOUT` constant replaced with `handshake_timeout()` function that
reads `BTSP_HANDSHAKE_TIMEOUT_MS` from the environment (default: 1500ms).
Cached via `OnceLock` for zero-cost repeated access.

1.5s is generous for local UDS IPC while keeping failure fast enough to be
invisible in guidestone timing.

### 2. Error frame on failure

`accept_with_btsp()` now calls `send_error_frame()` before dropping the
connection on any handshake error (timeout, provider unavailable, etc.). The
client receives a BTSP `HandshakeErrorMsg` frame immediately and can retry with
cleartext instead of waiting for its own socket read timeout.

### 3. Connection timeout tightened

IPC client connection timeout is now `min(handshake_timeout, 2s)` instead of
a fixed 2 seconds, so deployments that set sub-2s handshake timeouts get
proportionally faster fallback.

## Files changed

| File | Change |
|------|--------|
| `crates/main/src/rpc/btsp_handshake/btsp_handshake_wire.rs` | `HANDSHAKE_TIMEOUT` const → `handshake_timeout()` fn with `OnceLock` + env |
| `crates/main/src/rpc/btsp_handshake/mod.rs` | All `HANDSHAKE_TIMEOUT` usages → `handshake_timeout()`, new `send_error_frame()` pub fn |
| `crates/main/src/rpc/jsonrpc_server.rs` | `accept_with_btsp` error arm sends error frame before drop |
| `crates/main/src/rpc/btsp_handshake/btsp_handshake_tests.rs` | +2 tests |

## Tests

- **32 BTSP handshake tests passing** (was 30, +2 new)
- `handshake_timeout_default_is_1500ms` — verifies default ≤ 5s
- `send_error_frame_writes_btsp_error_msg` — verifies error frame roundtrip
- Full workspace: **7,167 tests**, 0 failures
- `cargo clippy --workspace -D warnings -W pedantic -W nursery` — clean

## Deployment notes

- **No breaking changes**: default behavior is identical but 3.5s faster on failure
- **Tuning**: set `BTSP_HANDSHAKE_TIMEOUT_MS=500` for aggressive fallback in
  compositions where BearDog is known to be absent
- **Phase 3 readiness**: when BearDog is available, the handshake completes well
  within 1.5s on local IPC — no tuning needed

## Blocked items (unchanged)

- Three-tier genetics (mito-beacon): blocked on `ecoPrimal >= 0.10.0`
- Content curation via BLAKE3: blocked on NestGate content-addressed storage API
- Phase 3 cipher negotiation: blocked on BearDog `btsp.negotiate` server-side
