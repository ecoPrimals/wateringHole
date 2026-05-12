# BearDog v0.9.0 — Wave 81: BTSP Phase 3 Encrypted Frame I/O Transition

**Date**: May 3, 2026
**Status**: Shipped to main (plasmidBin auto-harvests)
**Triggered by**: primalSpring Phase 3 interop gap report (guidestone, May 2)

---

## Summary

Fixed the BTSP Phase 3 interop gap: after `btsp.negotiate` returns a non-null cipher,
BearDog now transitions the connection from plaintext NDJSON to encrypted frame I/O.
Previously the connection stayed in plaintext mode, causing `primalSpring` to read
`0x7B226A73` (`{"js`) as a 2 GB frame header.

BearDog is the Tower reference implementation — this fix pattern cascades to all other primals.

## The Bug

1. Client sends `btsp.negotiate` → server returns `{"cipher":"chacha20-poly1305","server_nonce":"<b64>"}`
2. Client derives `SessionKeys`, switches to encrypted framing
3. Client sends encrypted frame: `[4B len BE u32][12B nonce][ciphertext + tag]`
4. **BearDog continued reading as plaintext NDJSON** — saw encrypted bytes as garbage
5. BearDog responded in plaintext; client parsed `{` as a 2 GB frame header

Root cause: `handle_phase3_negotiate` derived keys to `let _keys = ...` and the NDJSON
loop had no mechanism to detect or transition.

## The Fix

### New: `Phase3Session` (`btsp_handshake/session.rs`)

Server-side encrypted session using **random 12-byte nonces** per frame (matching
primalSpring wire format). Unlike `BtspSession` (Phase 2, counter nonces), Phase 3
uses CSPRNG random nonces with no counter validation on decrypt.

```
encrypt_frame(plaintext) → [12B random nonce][ciphertext + Poly1305 tag]
decrypt_frame(frame)     → split nonce(12) | ciphertext, AEAD decrypt
```

### New: `handle_jsonrpc_phase3` (`connection_handlers.rs`)

Encrypted frame loop: `read_frame → decrypt → JSON-RPC dispatch → encrypt → write_frame`

### New: `try_phase3_upgrade` (`connection_handlers.rs`)

After writing any JSON-RPC response, both NDJSON loops check:
1. Was the request method `btsp.negotiate`?
2. Did the response select a non-null cipher?
3. If yes → parse nonces, load `FAMILY_SEED`, re-derive keys via HKDF-SHA256, transition

### Modified Loops

- `handle_jsonrpc_universal` — Phase 3 upgrade check after first-line response + in loop
- `handle_jsonrpc_ndjson_loop` — Phase 3 upgrade check after each response

## Wire Format (Phase 3 encrypted frame)

```
[4 bytes: length (big-endian u32)]  →  length of blob that follows
[12 bytes: random nonce]            →  CSPRNG, unique per frame
[ciphertext + 16 bytes Poly1305 tag]
```

Plaintext inside each frame: one JSON-RPC object (UTF-8, no trailing newline required).

## Key Derivation (server perspective)

```
salt = client_nonce || server_nonce    (both 32 bytes, base64 on wire)
ikm  = handshake_key                  (HKDF-SHA256 from family seed)

HKDF-SHA256(salt, ikm, info="btsp-session-v1-c2s") → client_to_server key (32B) → server decrypt_key
HKDF-SHA256(salt, ikm, info="btsp-session-v1-s2c") → server_to_client key (32B) → server encrypt_key
```

## Files Changed

| File | Change |
|------|--------|
| `crates/beardog-tunnel/src/btsp_handshake/session.rs` | Added `Phase3Session` struct with random-nonce encrypt/decrypt + 6 tests |
| `crates/beardog-tunnel/src/btsp_handshake/mod.rs` | Export `Phase3Session` |
| `crates/beardog-tunnel/src/unix_socket_ipc/connection_handlers.rs` | Added `handle_jsonrpc_phase3`, `try_phase3_upgrade`; modified NDJSON loops |

## Test Results

- 6 new Phase3Session unit tests (roundtrip, nonce uniqueness, tamper, short frame, multi-message, wrong key)
- 2,133 beardog-tunnel lib tests pass
- 12,610+ workspace lib tests pass
- Zero failures, zero clippy warnings

## Downstream Impact

- **primalSpring**: Phase 3 encrypted transport should work end-to-end on next plasmidBin fetch
- **All primals**: This is the reference fix pattern. After writing `btsp.negotiate` response, detect non-null cipher and transition to `[len][nonce][AEAD ciphertext]` framing
- **NULL cipher fallback**: Unaffected — primals without Phase 3 continue on plaintext NDJSON
