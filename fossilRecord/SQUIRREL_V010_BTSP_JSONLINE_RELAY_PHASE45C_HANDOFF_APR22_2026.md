# Squirrel v0.1.0 — BTSP JSON-line Relay (Phase 45c Integration)

**Date**: April 22, 2026
**From**: Squirrel team
**Ref**: `PRIMALSPRING_PHASE45C_BTSP_DEFAULT_UPSTREAM_HANDOFF_APR2026.md`

---

## What Changed

Integrated primalSpring Phase 45c upstream changes to Squirrel's BTSP handshake
with additional cleanup and fixes.

### JSON-line BTSP Auto-Detection

The `maybe_handshake()` first-byte peek now reads the **full first line** when
the first byte is `{`. If the line contains both `"protocol"` and `"btsp"`, it
is parsed as a JSON-line `ClientHello` and the handshake runs in JSON-line mode.
Otherwise the line is treated as plain JSON-RPC (PG-14 fallback path).

Previously, any `{` first-byte was immediately classified as plain JSON-RPC.

### BearDog Field Alignment

- `btsp.session.create`: Sends `family_seed` as base64-encoded value (was `family_seed_ref: "env:FAMILY_SEED"`).
- `btsp.session.create` response: Parses `session_id` with `session_token` fallback.
- `btsp.session.verify`: Sends `session_token` (not `session_id`) and `response` (not `client_response`).
- Challenge: Sourced from BearDog's `btsp.session.create` response (was locally generated random). Prevents HMAC verification failures.

### Consistent JSON-line Framing

`btsp_handshake_after_client_hello()` extracted as a shared function accepting
`json_line_mode: bool`. When true, `ServerHello`, `ChallengeResponse` read, and
`HandshakeComplete` all use newline-delimited JSON framing via new wire helpers.

### Wire Helpers

- `write_json_line<S, T>()` — serialize + `\n` + flush
- `read_json_line_msg<S, T>()` — read until `\n`, deserialize (respects `MAX_FRAME_SIZE`)

### PlainJsonRpc Error Evolution

`BtspError::PlainJsonRpc` now carries the full consumed first line (`first_line: String`),
eliminating the need for the server to reconstruct the first line from a single byte.
`jsonrpc_server.rs` simplified accordingly.

### Cleanup

- Removed unused `rand::RngCore` import (challenge no longer generated locally).
- Extracted `resolve_family_seed()` helper to keep `btsp_handshake_after_client_hello()` under the 100-line clippy limit.
- Test assertions widened to accept both `ProviderUnavailable` and `Protocol` errors (machine-dependent — whether stale sockets exist).

---

## Files Modified

| File | Change |
|------|--------|
| `crates/main/src/rpc/btsp_handshake/mod.rs` | JSON-line detection in `maybe_handshake()`, extracted `btsp_handshake_after_client_hello()` with `json_line_mode`, `resolve_family_seed()` helper |
| `crates/main/src/rpc/btsp_handshake/btsp_handshake_wire.rs` | `write_json_line()`, `read_json_line_msg()`, `PlainJsonRpc { first_line }` |
| `crates/main/src/rpc/btsp_handshake/btsp_handshake_tests.rs` | New `maybe_handshake_json_line_btsp_routes_to_handshake` test, updated assertions |
| `crates/main/src/rpc/jsonrpc_server.rs` | `PlainJsonRpc { first_line }` destructuring, simplified `handle_universal_connection_with_first_line()` |

---

## Metrics

- **7,168** tests passing (was 7,167)
- **0** clippy warnings (`-D warnings -W pedantic -W nursery`)
- **0** cargo deny issues
- **90.1%** region coverage (unchanged)
