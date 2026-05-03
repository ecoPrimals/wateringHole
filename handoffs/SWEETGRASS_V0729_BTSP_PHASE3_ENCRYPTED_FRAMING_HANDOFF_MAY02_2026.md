# sweetGrass v0.7.29 — BTSP Phase 3: Server-Side Encrypted Framing

**Date**: May 2, 2026
**Primal**: sweetGrass (Nest — Provenance/Attribution)
**Triggered by**: primalSpring Phase 56c — Stadial Convergence + BTSP Phase 3

## Summary

sweetGrass now implements BTSP Phase 3 server-side `btsp.negotiate` handler
with ChaCha20-Poly1305 AEAD encrypted framing. After a successful Phase 1–2
handshake, Phase 3-capable clients (primalSpring) can negotiate an encrypted
channel. NULL cipher fallback ensures zero breakage for existing clients.

## What Changed

### New Module: `btsp/phase3.rs`
- `SessionKeys` — HKDF-SHA256 directional key derivation (`c2s`/`s2c`)
  with `Zeroize`/`ZeroizeOnDrop` for secure key erasure
- `Phase3Cipher` enum — `ChaCha20Poly1305` / `Null` with wire-name serde
- `NegotiateParams` / `NegotiateResult` — JSON-RPC wire types matching
  primalSpring's `negotiate_phase3()` format
- `generate_server_nonce()` — 32-byte CSPRNG via `OsRng`
- `select_cipher()` — server cipher preference (prefers ChaCha20-Poly1305)
- `encrypt(plaintext)` → `nonce(12) || ciphertext || tag(16)`
- `decrypt(frame)` → plaintext

### New Struct: `HandshakeOutcome`
- Wraps `HandshakeComplete` + `Option<[u8; 32]>` handshake key
- `session_key` extracted from BearDog's `btsp.session.verify` response
- `None` when BearDog doesn't return `session_key` (older versions)

### New Handler: `try_phase3_negotiate()`
- Shared by UDS and TCP paths
- Inspects first post-handshake message for `method: "btsp.negotiate"`
- If negotiate: validates params, selects cipher, generates server nonce,
  derives `SessionKeys`, responds, returns keys for encrypted loop
- If not negotiate: returns `None`, caller falls through to plaintext

### New Transport Loops
- `run_encrypted_frame_loop()` — `read_frame` → decrypt → process → encrypt → `write_frame`
- `run_plaintext_frame_loop()` — extracted from inline code, reused by UDS/TCP

### API Changes
- `perform_server_handshake` / `perform_server_handshake_jsonline` now return
  `HandshakeOutcome` instead of `HandshakeComplete`
- `exchange_challenge` extracts `session_key` from verify result

### Dependencies Added
- `chacha20poly1305 = "0.10"` — pure Rust AEAD (no `ring`, no `unsafe`)
- `hkdf = "0.12"` — HKDF-SHA256 (digest 0.10-compatible with existing `sha2`)
- `zeroize = "1"` — secure key erasure with derive macros
- `cargo deny check`: clean (no new ban violations)

## Wire Format Compatibility

primalSpring Phase 3 client sends:
```json
{"jsonrpc":"2.0","method":"btsp.negotiate","params":{
  "session_id":"<from handshake>",
  "ciphers":["chacha20-poly1305"],
  "client_nonce":"<base64 32 bytes>"
},"id":1}
```

sweetGrass responds:
```json
{"jsonrpc":"2.0","result":{
  "cipher":"chacha20-poly1305",
  "server_nonce":"<base64 32 bytes>"
},"id":1}
```

Encrypted frame format (post-negotiate):
```
[4B length BE u32][12B nonce][ciphertext + 16B Poly1305 tag]
```

## Key Derivation

```
salt = client_nonce || server_nonce
c2s_key = HKDF-SHA256(ikm=handshake_key, salt, info="btsp-session-v1-c2s")
s2c_key = HKDF-SHA256(ikm=handshake_key, salt, info="btsp-session-v1-s2c")
```

Server uses `s2c_key` to encrypt, `c2s_key` to decrypt (reversed on client).

## Graceful Degradation

- BearDog doesn't return `session_key` → `handshake_key = None` → null cipher
- Client doesn't send `btsp.negotiate` → plaintext mode (current behavior)
- Client offers only unknown ciphers → null cipher response
- primalSpring handles all fallback paths gracefully

## Metrics

- Tests: 1,492 pass (20 Phase 3 unit tests + 10 transport switch verification tests)
- Source files: 199 `.rs` (55,829 LOC), max 757 lines
- Transport refactor: `btsp/transport.rs` extracted, `tcp_jsonrpc/tests.rs` extracted
- Phase 3 transport switch verified: 10 integration tests proving negotiate → encrypted frame loop roundtrip (single, sequential, tamper rejection, full negotiate-then-encrypt flow)
- Clippy: 0 warnings (`pedantic` + `nursery`)
- `cargo deny check`: advisories ok, bans ok, licenses ok, sources ok

## Validation

primalSpring has `#[ignore]` integration tests that will auto-validate once
sweetGrass binary supports `btsp.negotiate`:
- `phase3_negotiate_with_live_sweetgrass`
- `phase3_transport_full_roundtrip`

Push to main → plasmidBin auto-harvests → primalSpring fetches → tests validate.

---

**License:** AGPL-3.0-or-later
