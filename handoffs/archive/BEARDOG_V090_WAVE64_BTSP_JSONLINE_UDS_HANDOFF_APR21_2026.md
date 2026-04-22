<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 64: BTSP JSON-Line Wire-Format Recognition on UDS

**Date**: April 21, 2026
**From**: BearDog team
**Resolves**: primalSpring Phase 45b BTSP escalation (`btsp:Tower:security` FAIL)

---

## Problem

primalSpring's BTSP client sends a JSON-line `ClientHello` on UDS:

```json
{"protocol":"btsp","version":1,"client_ephemeral_pub":"<b64>"}
```

BearDog's UDS accept loop peeks the first byte (`{` = 0x7B), classifies it as
JSON-RPC, and routes to the NDJSON handler. The handler tries to deserialize it
as `JsonRpcRequest` (requires `"jsonrpc"` and `"method"` fields) → parse error
→ connection closed → "Broken pipe" on reconnect.

## Fix

### 1. First-line BTSP detection (`unix_socket_ipc/server.rs`)

After reading the full first line in the NDJSON handler path, check for BTSP
markers before JSON-RPC routing:

```rust
if let BtspSecurityMode::Production { ref family_seed } = self.security_mode
    && let Ok(obj) = serde_json::from_str::<serde_json::Value>(first_line.trim())
    && obj.get("protocol").and_then(|v| v.as_str()) == Some("btsp")
    && obj.get("jsonrpc").is_none()
{
    // Route to JSON-line BTSP handshake
}
```

### 2. JSON-line handshake (`btsp_handshake/handshake.rs`)

New `continue_server_handshake_jsonline(stream, client_hello, family_seed)`:
- Takes an already-parsed `ClientHello` (step 1 consumed by detection)
- Steps 2–4 use newline-delimited JSON (not length-prefixed binary)
- ServerHello includes `session_id`; HandshakeComplete includes `status:"ok"`
- Returns `BtspSession` with negotiated cipher and derived keys

### 3. Post-handshake routing

- `Null` cipher → `handle_jsonrpc_ndjson_loop` (plain NDJSON JSON-RPC)
- Encrypted cipher → `handle_jsonrpc_btsp` (length-prefixed encrypted frames)

## Files Changed

| File | Change |
|------|--------|
| `crates/beardog-tunnel/src/btsp_handshake/handshake.rs` | +`continue_server_handshake_jsonline`, `write_jsonline`, `read_jsonline`, `send_error_jsonline`, 3 tests |
| `crates/beardog-tunnel/src/btsp_handshake/mod.rs` | Export `continue_server_handshake_jsonline` |
| `crates/beardog-tunnel/src/unix_socket_ipc/server.rs` | BTSP ClientHello detection, `handle_btsp_jsonline_connection`, `handle_jsonrpc_ndjson_loop` |

## Wire Protocol (JSON-line framed, 4 steps)

1. Client → Server: `{"protocol":"btsp","version":1,"client_ephemeral_pub":"<b64>"}`
2. Server → Client: `{"version":1,"server_ephemeral_pub":"<b64>","challenge":"<b64>","session_id":"<uuid>"}`
3. Client → Server: `{"response":"<b64-hmac>","preferred_cipher":"null"}`
4. Server → Client: `{"status":"ok","session_id":"<uuid>","cipher":"null"}`

Key derivation unchanged: `HKDF-SHA256(ikm=FAMILY_SEED, salt="btsp-v1", info="handshake")`.

## Quality

- 14,789+ tests, 0 failures (1 known flaky pre-existing)
- `cargo clippy -D warnings` clean
- `cargo fmt` clean
- `cargo deny check` 4/4 pass

## Next

primalSpring guidestone Layer 1.5 should flip `btsp:Tower:security` from FAIL to PASS.
