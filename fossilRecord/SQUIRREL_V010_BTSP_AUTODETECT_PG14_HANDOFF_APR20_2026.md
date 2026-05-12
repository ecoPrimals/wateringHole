# Squirrel v0.1.0 — BTSP Auto-Detect (PG-14 Resolution) Handoff

**Date**: April 20, 2026
**From**: Squirrel alpha.52+
**Resolves**: wetSpring PG-14 — plain JSON-RPC clients get connection reset on BTSP-guarded socket

## Problem

When `FAMILY_ID` is set (production / NUCLEUS mode), Squirrel's UDS accept
path ran the BTSP handshake unconditionally. Clients sending plain JSON-RPC
(springs doing `health.liveness` probes, composition tooling) hit the BTSP
4-byte BE length-prefix reader first — the `{` byte (0x7B) is not a valid
BTSP frame header — causing the handshake to fail and the connection to be
dropped (observed as "connection reset" by springs).

## Solution — First-Byte Auto-Detect

Matches the ecosystem pattern established by ToadStool (LD-04), BearDog,
petalTongue, and skunkBat:

1. **`maybe_handshake()`** reads the first byte from the stream with a
   timeout (same `HANDSHAKE_TIMEOUT`)
2. If the byte is `{` (0x7B) → **plain JSON-RPC** client detected. Returns
   `BtspError::PlainJsonRpc`. The connection proceeds unauthenticated.
3. Any other byte → **BTSP binary framing**. The consumed byte is passed to
   `btsp_handshake_server()` which feeds it into
   `read_frame_with_first_byte()` to reconstruct the 4-byte length prefix.

## Wire Changes

- **New BTSP wire functions**: `read_frame_with_first_byte()`,
  `read_message_with_first_byte()` in `btsp_handshake_wire.rs`
- **New error variant**: `BtspError::PlainJsonRpc`
- **New accept method**: `JsonRpcServer::accept_with_btsp()` centralizes
  BTSP + auto-detect + fallback for both primary and filesystem socket accept
  paths (deduplicates logic)
- **Prefix replay**: `handle_universal_connection_with_prefix()` reconstructs
  the full first JSON-RPC line by reading the rest after the consumed `{` byte

## Files Changed

| File | Change |
|------|--------|
| `crates/main/src/rpc/btsp_handshake/mod.rs` | Auto-detect in `maybe_handshake()`, updated `btsp_handshake_server()` to accept peeked byte |
| `crates/main/src/rpc/btsp_handshake/btsp_handshake_wire.rs` | `read_frame_with_first_byte`, `read_message_with_first_byte`, `BtspError::PlainJsonRpc` |
| `crates/main/src/rpc/jsonrpc_server.rs` | `accept_with_btsp()`, `handle_universal_connection_with_prefix()`, deduplicated accept loops |
| `crates/main/src/rpc/btsp_handshake/btsp_handshake_tests.rs` | 5 new tests (30 total in module) |

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 7,165 passing / 0 failures |
| Coverage | 90.1% region |
| Clippy | CLEAN (`-D warnings`) |
| `cargo fmt` | PASS |
| `.rs` files | ~1,039 |
| Lines | ~337k |

## Upstream Blocks (Unchanged)

1. **Three-tier genetics** — blocked on `ecoPrimal >= 0.10.0` (`mito_beacon_from_env()`)
2. **BLAKE3 content curation** — blocked on NestGate content-addressed storage API stability
3. **Phase 3 cipher negotiation** — blocked on BearDog `btsp.negotiate` server-side
