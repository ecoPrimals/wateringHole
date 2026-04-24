# Songbird v0.2.1 — Wave 164: BTSP Relay Silent-Fail Fix

**Date**: April 15, 2026
**Primal**: Songbird
**Version**: v0.2.1
**Wave**: 164
**Supersedes**: Wave 163 handoff (archived)

---

## Summary

Fixed the BTSP handshake relay silent-fail reported by primalSpring Phase 45c.
Songbird accepted BTSP ClientHello but returned zero bytes — no ServerHello.

### Root Cause

Wave 162 removed `stream.shutdown()` from `SecurityRpcClient::call_direct()` to
prevent the write-half FIN from racing with BearDog's response. However, the
remaining `read_to_end()` call blocks until EOF — and BearDog, like most JSON-RPC
servers, **keeps the socket open** for further requests. Without shutdown and
without EOF, `read_to_end()` hung forever. The BTSP handshake stalled at
`btsp.session.create`, Songbird never sent ServerHello, and the client saw EOF.

### Fix

Replaced `read_to_end()` with a shared `io_util::read_json_response()` helper
that reads in 4KB chunks with a per-chunk timeout and breaks as soon as a
complete JSON value is detected. Applied across all 4 JSON-RPC socket read sites:

| Call site | File | Timeout | Old pattern |
|-----------|------|---------|-------------|
| `call_direct()` | `security_rpc_client/rpc.rs` | 10s | `read_to_end()` |
| `call_neural_api()` | `security_rpc_client/rpc.rs` | 5s | inline chunked loop |
| `SecurityCryptoProvider::call()` | `crypto/security_provider/rpc.rs` | 10s | `shutdown()` + `read_to_end()` |
| `IpcHttpClient::request()` | `ipc_client/client/client_impl.rs` | 30s | `read_to_end()` |

`SecurityCryptoProvider::call()` also still had the original `stream.shutdown()`
bug from before Wave 162, plus was missing the newline terminator and flush.

### Files Changed

- `crates/songbird-http-client/src/io_util.rs` — **NEW**: shared `read_json_response()` helper
- `crates/songbird-http-client/src/lib.rs` — registered `io_util` module
- `crates/songbird-http-client/src/security_rpc_client/rpc.rs` — `call_direct()` and `call_neural_api()` use helper
- `crates/songbird-http-client/src/crypto/security_provider/rpc.rs` — removed `shutdown()`, uses helper
- `crates/songbird-http-client/src/ipc_client/client/client_impl.rs` — uses helper

### Verification

- `cargo fmt -- --check` — clean
- `cargo clippy --workspace -- -D warnings` — 0 warnings
- `cargo test --workspace --lib` — 497 passed, 0 failed

### Verification (runtime — for primalSpring)

```bash
echo '{"protocol":"btsp","version":1,"client_ephemeral_pub":"dGVzdA=="}' | \
  socat - UNIX-CONNECT:/run/user/1000/biomeos/songbird-nucleus01.sock
```

Should return a ServerHello JSON line (not empty). This gets guidestone to 10/13 BTSP.

### Ref

- `infra/wateringHole/handoffs/BTSP_WIRE_CONVERGENCE_APR24_2026.md`
- primalSpring Phase 45c audit
