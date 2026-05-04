# petalTongue v1.6.6 — BTSP Phase 3 Transport Switch (13/13 Complete)

**Date**: May 3, 2026
**Status**: Shipped to main (plasmidBin auto-harvests)
**Triggered by**: primalSpring Phase 3 interop gap report — petalTongue was the last primal without the transport switch

---

## Summary

Fixed the BTSP Phase 3 interop gap: after `btsp.negotiate` returns a non-null
cipher, petalTongue now transitions the connection from plaintext NDJSON to
encrypted frame I/O using ChaCha20-Poly1305 AEAD. Previously the connection
stayed in plaintext mode regardless of the negotiate result.

**petalTongue is the 13th and final primal to ship Phase 3 — the ecosystem
transport switch is now complete.**

## The Bug

1. Client sends `btsp.negotiate` → server returns `{"cipher":"chacha20-poly1305",...}`
2. Client derives `SessionKeys`, switches to encrypted framing
3. Client sends encrypted frame: `[4B len BE u32][12B nonce][ciphertext + tag]`
4. **petalTongue continued reading as plaintext NDJSON** — saw encrypted bytes as garbage
5. petalTongue responded in plaintext; client parsed `{` as a 2 GB frame header

Root cause: `perform_server_handshake_split` and `relay_json_line_handshake_split`
both called `btsp.negotiate` and returned cipher info, but `handle_uds_with_btsp`
and `handle_tcp_with_btsp` always fell through to `handle_connection_split`
(plaintext NDJSON loop) regardless of the cipher.

## The Fix

### New: `btsp/phase3.rs` (571 lines, 10 tests)

Phase 3 encrypted session using **random 12-byte nonces** per frame (matching
primalSpring wire format and BearDog W81 reference pattern).

#### `SessionKeys` — HKDF-SHA256 directional key derivation

```
salt = client_nonce || server_nonce    (both 32 bytes, base64 on wire)
ikm  = session_key                    (from btsp.session.verify)
HKDF-SHA256(salt, ikm, info="btsp-session-v1-c2s") → client_to_server key (32B)
HKDF-SHA256(salt, ikm, info="btsp-session-v1-s2c") → server_to_client key (32B)
```

#### `Phase3Session` — ChaCha20-Poly1305 AEAD

```
encrypt_frame(plaintext) → [12B random nonce][ciphertext + Poly1305 tag]
decrypt_frame(frame)     → split nonce(12) | ciphertext, AEAD decrypt
```

#### Frame I/O

```
read_encrypted_frame:  [4B BE len] → read(len) → decrypt → plaintext
write_encrypted_frame: encrypt → [4B BE len][payload] → flush
```

#### `handle_encrypted_stream` — Encrypted JSON-RPC dispatch loop

Replaces `handle_connection_split` after successful Phase 3 negotiate.
Each inbound frame is decrypted, parsed as JSON-RPC, dispatched, and
the response is encrypted and written back.

#### `try_phase3_negotiate` — Post-handshake nonce exchange

Reads the first post-handshake line. If it's `btsp.negotiate` with a
`client_nonce`, generates `server_nonce`, responds with
`{cipher, server_nonce}`, and returns the nonce material for key derivation.

### Modified: `btsp/server.rs` + `btsp/json_line.rs`

Both handshake functions now return `HandshakeResult` (session_token +
cipher + session_key) instead of just the session token. The `session_key`
is extracted from `btsp.session.verify`'s response (base64-decoded).

### Modified: `btsp/types.rs`

Added `HandshakeResult` struct.

### Modified: `btsp/error.rs`

Added `KeyDerivationFailed` and `Phase3Crypto` error variants.

### Modified: `unix_socket_server.rs`

Both `handle_uds_with_btsp` and `handle_tcp_with_btsp` now check:
1. Was the cipher non-null? (`chacha20-poly1305` or `chacha20_poly1305`)
2. Is a session_key available from the handshake?
3. If yes → `try_phase3_upgrade_split` → derive keys → encrypted stream
4. If no → fall back to plaintext NDJSON (null cipher or missing key)

Extracted `run_uds_handshake` helper to keep `handle_uds_with_btsp` under
100 lines (clippy `too_many_lines`).

## Wire Format (Phase 3 encrypted frame)

```
[4 bytes: length (big-endian u32)]  →  length of blob that follows
[12 bytes: random nonce]            →  CSPRNG, unique per frame
[ciphertext + 16 bytes Poly1305 tag]
```

Plaintext inside each frame: one JSON-RPC object (UTF-8, no trailing newline required).

## Connection Flow

```
Client connects → BTSP Phase 2 handshake (4-step) → HandshakeResult with session_key
  → check cipher from handshake
  → IF chacha20-poly1305 AND session_key present:
      → try_phase3_negotiate()
        → read first line: btsp.negotiate { session_id, client_nonce }
        → generate server_nonce, respond { cipher, server_nonce }
        → SessionKeys::derive(session_key, client_nonce, server_nonce, is_server=true)
        → Phase3Session::new(keys)
        → handle_encrypted_stream() ← ALL subsequent messages encrypted
      → IF first line is NOT btsp.negotiate:
        → process normally, continue NDJSON
  → ELSE (null cipher or no key):
      → handle_connection_split() ← plaintext as before
```

## Dependencies Added

| Crate | Version | Purpose |
|-------|---------|---------|
| `chacha20poly1305` | 0.10 | ChaCha20-Poly1305 AEAD (pure Rust) |
| `hkdf` | 0.12 | HKDF-SHA256 key derivation |
| `sha2` | 0.10 | SHA-256 for HKDF |
| `rand` | 0.8 | CSPRNG for nonces |
| `zeroize` | 1 | Zero secrets on drop |

All pure Rust, compatible with existing `aes-gcm 0.10` (digest 0.10 ecosystem).

## Test Results

- 10 new Phase 3 unit tests (key derivation, roundtrip, nonce uniqueness, tamper detection, short frame, wrong key, cross-direction, frame I/O, multi-message)
- 607+ petal-tongue-ipc lib tests pass
- Full workspace tests pass
- Zero clippy warnings (pedantic + nursery)
- Zero doc warnings (`-D warnings`)

## Files Changed

| File | Change |
|------|--------|
| `Cargo.toml` (workspace) | Added `chacha20poly1305`, `hkdf`, `sha2` to workspace deps |
| `crates/petal-tongue-ipc/Cargo.toml` | Added Phase 3 crypto dependencies |
| `crates/petal-tongue-ipc/src/btsp/phase3.rs` | **NEW** — SessionKeys, Phase3Session, encrypted frame I/O, negotiate handler, 10 tests |
| `crates/petal-tongue-ipc/src/btsp/mod.rs` | Export phase3 module, HandshakeResult |
| `crates/petal-tongue-ipc/src/btsp/types.rs` | Added HandshakeResult struct |
| `crates/petal-tongue-ipc/src/btsp/error.rs` | Added KeyDerivationFailed, Phase3Crypto variants |
| `crates/petal-tongue-ipc/src/btsp/server.rs` | Return HandshakeResult, extract session_key |
| `crates/petal-tongue-ipc/src/btsp/json_line.rs` | Return HandshakeResult, extract session_key |
| `crates/petal-tongue-ipc/src/unix_socket_server.rs` | Phase 3 transport switch for both UDS and TCP |

## Downstream Impact

- **primalSpring**: Phase 3 encrypted transport should work end-to-end on next plasmidBin fetch
- **Ecosystem**: 13/13 primals now ship Phase 3 transport switch — the interop gap is closed
- **NULL cipher fallback**: Unaffected — connections without Phase 3 continue on plaintext NDJSON

---

*Ref: `BEARDOG_V090_WAVE81_BTSP_PHASE3_ENCRYPTED_FRAME_TRANSITION_HANDOFF_MAY03_2026.md` for the Tower reference fix*
*Ref: `BTSP_PROTOCOL_STANDARD.md` for the ecosystem wire format standard*
