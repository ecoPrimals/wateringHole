# BTSP Wire Convergence — April 24, 2026

**From:** primalSpring Phase 45c validation  
**For:** songbird, toadStool, barraCuda, nestgate teams  
**Status:** 164/168 guidestone (7/13 BTSP authenticated). 4 failures = upstream wire mismatches  

## Context

primalSpring guidestone validates BTSP handshakes against all 13 NUCLEUS
capabilities. After this round of upstream evolution, **7/13 authenticate
correctly**. The remaining 4 fail due to specific wire-format issues in
each primal's BearDog relay code.

**Working reference implementation:** coralReef (`crates/coralreef-core/src/ipc/btsp.rs`)
uses the correct BearDog wire format for `btsp.session.create` and `btsp.session.verify`.

## BearDog Wire Contract (ground truth)

### `btsp.session.create`

**Request:**
```json
{"jsonrpc":"2.0","method":"btsp.session.create","params":{"family_seed":"<base64>"},"id":1}
```

**Response:**
```json
{"jsonrpc":"2.0","result":{"challenge":"<base64>","server_ephemeral_pub":"<base64>","session_token":"<uuid>"},"id":1}
```

### `btsp.session.verify`

**Request:**
```json
{"jsonrpc":"2.0","method":"btsp.session.verify","params":{"session_token":"<uuid>","response":"<base64>","client_ephemeral_pub":"<base64>","preferred_cipher":"null"},"id":2}
```

**Response (success):**
```json
{"jsonrpc":"2.0","result":{"verified":true,"session_id":"<uuid>","cipher":"null"},"id":2}
```

**Response (failure):**
```json
{"jsonrpc":"2.0","result":{"verified":false,"error":"..."},"id":2}
```

Key: `verified` is a **bool**, not a string. There is no `status` field.

## Per-Primal Issues and Fixes

### Songbird — `writer.shutdown()` kills connection

**Error:** `BTSP: server closed connection (no ServerHello)`

**Root cause:** `SecurityRpcClient::call_direct()` in
`crates/songbird-http-client/src/security_rpc_client/rpc.rs` calls
`stream.shutdown().await` after writing the request to BearDog. This sends
TCP FIN which causes BearDog to close the connection before responding.

**Fix:** Remove `stream.shutdown().await` from `call_direct()`. Use a read
timeout instead of write-half shutdown to signal "done writing":

```rust
// REMOVE this line:
stream.shutdown().await?;
// KEEP the read:
stream.read_to_end(&mut buffer).await?;
```

**Verify:** After fix, `socat` test should return ServerHello:
```
echo '{"protocol":"btsp","version":1,"client_ephemeral_pub":"dGVzdA=="}' \
  | socat - UNIX-CONNECT:$SOCKET
```

---

### barraCuda — same `writer.shutdown()` issue

**Error:** `BTSP: server closed connection (no HandshakeComplete)`

**Root cause:** `security_provider_rpc()` in
`crates/barracuda-core/src/ipc/btsp.rs` calls `writer.shutdown().await`
after sending each BearDog RPC. The `btsp.session.create` call may succeed
(race condition) but `btsp.session.verify` response is lost.

**Fix:** Remove `writer.shutdown().await` from `security_provider_rpc()`.
The connection is already per-request (connect → write → read → drop), so
shutdown is unnecessary:

```rust
// REMOVE:
writer.shutdown().await.map_err(|e| { ... })?;
```

---

### toadStool — expects `status` field instead of `verified`

**Error:** `BTSP JSON-line protocol: missing string field status`

**Root cause:** `accept_json_line_handshake()` in
`crates/core/common/src/btsp/json_line.rs` line 310 reads:
```rust
let status = require_str_line(stream, verify_obj, "status").await?;
```

BearDog returns `{"verified": true, "session_id": "...", "cipher": "..."}`.
There is no `status` field.

**Fix:** Replace `status` check with `verified` check:
```rust
let verified = verify_obj.get("verified")
    .and_then(|v| v.as_bool())
    .unwrap_or(false);
if !verified {
    let reason = verify_obj.get("error")
        .and_then(|v| v.as_str())
        .unwrap_or("unknown");
    let msg = format!("verify failed: {reason}");
    let _ = send_error_line(stream, &msg).await;
    return Err(BtspJsonLineError::Protocol(msg));
}
```

---

### NestGate — `family_seed_ref` instead of `family_seed`

**Error:** `BTSP: server closed connection (no ServerHello)`

**Root cause:** `btsp_server_handshake/mod.rs` line 304 sends:
```json
{"family_seed_ref": "env:FAMILY_SEED", ...}
```

BearDog expects `family_seed` (actual base64 bytes), not `family_seed_ref`.
BearDog's `btsp.session.create` fails silently when the required param is
missing.

**Fix:** Replace `family_seed_ref` with actual base64-encoded seed:
```rust
let family_seed = resolve_family_seed()?;  // base64-encoded
json!({
    "family_seed": family_seed,
})
```

Also remove the extra `client_ephemeral_pub` and `challenge` params from
the create call — BearDog generates those server-side.

---

## Verification

After fixing, each primal should pass this `socat` test (NUCLEUS running
with `FAMILY_SEED` set):

```bash
echo '{"protocol":"btsp","version":1,"client_ephemeral_pub":"dGVzdA=="}' \
  | socat - UNIX-CONNECT:/run/user/$(id -u)/biomeos/${PRIMAL}-${FAMILY_ID}.sock
```

Expected: JSON line with `challenge`, `server_ephemeral_pub`, `version`.
If empty or JSON-RPC error → fix not applied correctly.

## Reference

- CoralReef BTSP relay: `crates/coralreef-core/src/ipc/btsp.rs`
- primalSpring client handshake: `ecoPrimal/src/ipc/btsp_handshake.rs`
- BearDog API: `btsp.session.create`, `btsp.session.verify`, `btsp.negotiate`
- Previous handoff: `PRIMALSPRING_PHASE45C_BTSP_DEFAULT_UPSTREAM_HANDOFF_APR2026.md`
