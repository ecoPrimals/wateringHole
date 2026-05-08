# Squirrel v0.1.0 — BTSP Phase 3 FULL: Encrypted Framing + Key Derivation

**Date**: May 2, 2026
**From**: Squirrel
**To**: primalSpring, all primals
**Type**: Phase 3 convergence — encrypted framing readiness

---

## Summary

Squirrel is now the **10th of 13 NUCLEUS primals** with FULL BTSP Phase 3 implementation.
The `btsp.negotiate` handler has been evolved from NULL-only stub to complete encrypted
framing with HKDF key derivation, directional session keys, and transport-level upgrade.

## What Changed

### Encrypted Framing Primitives

- `encrypt_frame(key, plaintext)` → `[4B len BE u32][12B nonce][ciphertext + 16B Poly1305 tag]`
- `decrypt_frame(key, payload)` → plaintext (or `FrameError`)
- `read_encrypted_frame` / `write_encrypted_frame` — async frame I/O
- ChaCha20-Poly1305 via `chacha20poly1305` crate (pure Rust, no unsafe)
- Typed `FrameError` enum: `Encryption`, `Decryption`, `FrameTooLarge`, `FrameTooShort`, `Io`, `KeyDerivation`

### Key Derivation

```
salt = client_nonce || server_nonce
c2s_key = HKDF-SHA256(ikm=handshake_key, salt, info="btsp-session-v1-c2s")
s2c_key = HKDF-SHA256(ikm=handshake_key, salt, info="btsp-session-v1-s2c")
```

### Secure Key Erasure

- `SessionKeys` derives `Zeroize`/`ZeroizeOnDrop` from the `zeroize` crate
- Keys are securely zeroed from memory on drop
- Debug impl redacts key bytes

### Wire Format Alignment

- **Nonce encoding**: `server_nonce` base64-encoded (matching BearDog/sweetGrass/biomeOS convergence)
- **Nonce size**: 32-byte server nonces (matching ecosystem standard)
- **`ciphers[]` array param**: accepts both `"preferred_cipher"` (string) and `"ciphers"` (array)

### BtspSession Evolution

- `handshake_key` now captured from `btsp.session.verify` response (Phase 2)
- `client_ephemeral_pub` stored for Phase 3 context
- Phase 2 → Phase 3 key material threading complete

### Transport Upgrade Wiring

- `handle_jsonrpc_loop` detects `btsp.negotiate` → `chacha20-poly1305` response
- Seamlessly transitions to `handle_encrypted_connection` (encrypted frame loop)
- Server reads with `c2s_key`, writes with `s2c_key` (directional)

## Wire Format

```
Client → Squirrel:
{"jsonrpc":"2.0","method":"btsp.negotiate","params":{
  "session_id":"<from handshake>",
  "preferred_cipher":"chacha20-poly1305",
  "client_nonce":"<base64 32 bytes>",
  "bond_type":"Covalent"
},"id":1}

Squirrel → Client (keyed):
{"jsonrpc":"2.0","result":{
  "cipher":"chacha20-poly1305",
  "server_nonce":"<base64 32 bytes>",
  "allowed":true
},"id":1}

Squirrel → Client (fallback — no handshake_key):
{"jsonrpc":"2.0","result":{
  "cipher":"null",
  "server_nonce":"<base64 32 bytes>",
  "allowed":true
},"id":1}
```

## Dependencies Added

- `chacha20poly1305 = "0.10"` — AEAD cipher
- `hkdf = "0.12"` — key derivation
- `sha2 = "0.10"` — HKDF hash

## Test Coverage

- 21 Phase 3 tests: key derivation determinism, directional key separation,
  encrypt/decrypt roundtrip, wrong-key rejection, truncated frame, frame too
  large/short, async I/O roundtrip, multiple sequential frames, nonce uniqueness,
  base64 nonce format, `ciphers[]` array, negotiate with/without handshake_key
- Full workspace: 7,213 lib tests passing, 0 failures
- Clippy PASS (0 warnings, pedantic+nursery, `-D warnings`)
- `cargo deny` PASS

## Validation

primalSpring's Phase 3 client tests should auto-validate once the updated binary
is harvested by plasmidBin. The `btsp.negotiate` handler returns `chacha20-poly1305`
with base64 nonces matching the primalSpring wire expectations. NULL cipher fallback
preserved for backward compatibility when `handshake_key` is not available.

---

*Squirrel v0.1.0 | AGPL-3.0-or-later | ecoPrimals Project*
