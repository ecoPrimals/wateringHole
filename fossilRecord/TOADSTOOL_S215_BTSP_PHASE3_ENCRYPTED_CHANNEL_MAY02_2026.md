# ToadStool S215 — BTSP Phase 3: Encrypted Channel (ChaCha20-Poly1305)

**Date**: May 2, 2026
**From**: toadStool S215
**Status**: BTSP Phase 3 server-side implemented — `btsp.negotiate` handler + encrypted framing
**License**: AGPL-3.0-or-later

---

## What landed

toadStool now supports BTSP Phase 3 encrypted channels. After a Phase 1
JSON-line handshake, clients can upgrade to ChaCha20-Poly1305 encrypted
framing by sending `btsp.negotiate` as the first post-handshake JSON-RPC
call.

### Implementation summary

| Component | File | What |
|-----------|------|------|
| Session keys | `btsp/phase3.rs` | `Phase3SessionKeys` — HKDF-SHA256 derivation, ChaCha20-Poly1305 encrypt/decrypt |
| Negotiate handler | `btsp/json_line.rs` | `try_handle_negotiate()` — parses negotiate request, derives keys, returns cipher + server_nonce |
| Encrypted framing | `btsp/framing.rs` | `read_encrypted_frame()` / `write_encrypted_frame()` |
| Server integration | `connection/unix.rs` | `handle_post_handshake_session()` + `handle_encrypted_session()` |
| Daemon integration | `daemon/jsonrpc_server.rs` | `daemon_encrypted_loop()` |

### Wire compatibility

- **Request** (from primalSpring client):
  ```json
  {"jsonrpc":"2.0","method":"btsp.negotiate","params":{
    "session_id":"<from handshake>",
    "ciphers":["chacha20-poly1305"],
    "client_nonce":"<base64-32-bytes>"
  },"id":1}
  ```

- **Response** (from toadStool):
  ```json
  {"jsonrpc":"2.0","result":{
    "cipher":"chacha20-poly1305",
    "server_nonce":"<base64-32-bytes>"
  },"id":1}
  ```

- **Key derivation**: `HKDF-SHA256(ikm=handshake_key, salt=client_nonce||server_nonce)`
  - `info="btsp-session-v1-c2s"` → client-to-server key
  - `info="btsp-session-v1-s2c"` → server-to-client key

- **Encrypted frame**: `[4B len BE u32][12B AEAD nonce][ciphertext + 16B Poly1305 tag]`

- **Null cipher fallback**: If client doesn't send `client_nonce` or requests
  unsupported cipher, server returns `{"cipher":"null"}` — stays on plaintext NDJSON.

### What this unblocks

- primalSpring's `negotiate_phase3()` will auto-detect the upgrade on next
  plasmidBin fetch of toadStool binary
- primalSpring's `#[ignore]` integration tests (`phase3_negotiate_with_live_toadstool`,
  `phase3_transport_full_roundtrip`) should validate automatically
- All JSON-RPC traffic after negotiate is end-to-end encrypted

### Scope limitations

- **tarpc path not encrypted**: tarpc uses its own codec; Phase 3 wrapping for
  tarpc would require a custom transport layer. JSON-RPC NDJSON paths (which
  primalSpring's `CompositionContext` uses) are the primary target.
- **AES-256-GCM not yet supported**: Only ChaCha20-Poly1305. Can be added to
  `Phase3SessionKeys` when needed.
- **No AAD on AEAD**: Matches primalSpring client behavior (no additional
  authenticated data). Note: `BTSP_PROTOCOL_STANDARD.md` specifies AAD =
  frame length — this is a spec-vs-implementation gap inherited from the
  primalSpring reference.

### Quality gates

- 22,429 tests, 0 failures
- 0 clippy warnings
- 0 fmt violations
- `cargo deny check bans` passes
- 7 new Phase 3 unit tests (key derivation roundtrip, encrypt/decrypt, tamper
  detection, short input rejection, deterministic handshake key, nonce generation)
