# biomeOS v3.38 — BTSP Phase 3 FULL: Encrypted Framing + Spec Alignment

**Date**: May 2, 2026
**From**: biomeOS
**To**: primalSpring, all primals
**Type**: Phase 3 convergence + deep debt

---

## Summary

biomeOS is now the **9th of 13 NUCLEUS primals** with FULL BTSP Phase 3 implementation.
The `btsp.negotiate` handler has been evolved from key-derivation-only (v3.37) to full
encrypted framing readiness with spec-aligned wire format.

## What Changed

### Phase 3 Wire Format Alignment

- **Nonce encoding**: `server_nonce` now base64-encoded (was hex), matching
  BearDog/sweetGrass/primalSpring convergence pattern
- **Nonce size**: 32-byte server nonces (was 12), matching BearDog/sweetGrass
- **Client nonce auto-detection**: accepts both base64 and hex `client_nonce`
  for backward compatibility with barraCuda-style clients
- **`ciphers[]` array param**: accepts both `"preferred_cipher"` (string) and
  `"ciphers"` (array) wire formats used across the ecosystem

### Encrypted Framing Primitives

- `encrypt_frame(key, plaintext)` → `[4B len BE u32][12B nonce][ciphertext + 16B Poly1305 tag]`
- `decrypt_frame(key, payload)` → plaintext (or `FrameError`)
- ChaCha20-Poly1305 via `chacha20poly1305` crate (pure Rust, no unsafe)
- Typed `FrameError` enum: `Encryption`, `Decryption`, `FrameTooLarge`, `FrameTooShort`

### Secure Key Erasure

- `SessionKeys` now derives `Zeroize`/`ZeroizeOnDrop` from the `zeroize` crate
- Keys are securely zeroed from memory on drop

### Deep Debt: Flaky Graph List Tests Fixed

- 7 graph CRUD list tests were flaky due to concurrent temp directory sibling
  contamination (the `runtime_graphs` sibling dir would pick up other tests' TOML files)
- Fixed by isolating `graphs_dir` into a subdirectory within each test's temp dir

## Wire Format

```
Client → biomeOS:
{"jsonrpc":"2.0","method":"btsp.negotiate","params":{
  "session_id":"<from handshake>",
  "preferred_cipher":"chacha20-poly1305",
  "client_nonce":"<base64 32 bytes>",
  "bond_type":"Covalent"
},"id":1}

biomeOS → Client (keyed):
{"jsonrpc":"2.0","result":{
  "cipher":"chacha20-poly1305",
  "server_nonce":"<base64 32 bytes>",
  "allowed":true
},"id":1}

biomeOS → Client (fallback):
{"jsonrpc":"2.0","result":{
  "cipher":"null",
  "server_nonce":"<base64 32 bytes>",
  "allowed":true
},"id":1}
```

## Key Derivation

```
salt = client_nonce || server_nonce
c2s_key = HKDF-SHA256(ikm=handshake_key, salt, info="btsp-session-v1-c2s")
s2c_key = HKDF-SHA256(ikm=handshake_key, salt, info="btsp-session-v1-s2c")
```

## Dependencies Added

- `zeroize = "1.7"` (with derive feature) — secure key erasure

## Test Coverage

- 25 Phase 3 tests (up from 13): encrypt/decrypt roundtrip, wrong-key rejection,
  truncated frame, unique nonces, base64/hex auto-detection, `ciphers[]` array,
  32-byte base64 nonce format
- 7 flaky graph list tests fixed
- Full workspace: 6,826+ lib tests passing, 0 failures
- Clippy PASS (0 warnings, pedantic+nursery, `-D warnings`)

## Validation

primalSpring's Phase 3 client tests should auto-validate once the updated binary
is harvested by plasmidBin. The `btsp.negotiate` handler returns `chacha20-poly1305`
with base64 nonces matching the primalSpring wire expectations.

---

*biomeOS v3.38 | AGPL-3.0-or-later | ecoPrimals Project*
