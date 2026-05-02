# barraCuda Sprint 51 — BTSP Phase 3 `btsp.negotiate` Server Handler

**Date**: 2026-05-02
**Version**: 0.3.12
**Sprint**: 51
**Trigger**: primalSpring Phase 3 audit — `btsp.negotiate` server-side implementation

---

## Summary

Implemented `btsp.negotiate` JSON-RPC server handler for BTSP Phase 3 encrypted
channel support. After a Phase 1 handshake (already operational), clients can now
send `btsp.negotiate` to upgrade from NULL cipher to ChaCha20-Poly1305 encrypted
framing. barraCuda validates the session, derives keys via HKDF-SHA256, and
seamlessly switches the connection to encrypted frames — zero application-layer
disruption.

## Changes

### New: `btsp.negotiate` Server Handler

- **`btsp.rs`**: `negotiate_phase3()` function + `NegotiateResult` struct
  - Validates `session_id` against connection's authenticated session
  - Generates 12-byte random server nonce via `rand::rng()`
  - Derives 32-byte session key via HKDF-SHA256(ikm=handshake_key, salt=server_nonce, info="btsp-v1-phase3")
  - Returns `{"cipher":"chacha20-poly1305","server_nonce":"<hex>"}`
  - Graceful NULL fallback when: no key material from Phase 1, unsupported cipher requested, or session validation fails
  - `BtspCipher::from_wire` extended to accept `chacha20-poly1305` (hyphenated wire name)
  - `BtspCipher::wire_name()` added for canonical wire serialization
  - Session key now always captured from Phase 1 verify (even with NULL cipher) for Phase 3 availability

### Transport Integration

- **`transport.rs`**: `handle_connection` now threads `Option<BtspSession>` from handshake
  - `try_negotiate_upgrade()` intercepts `btsp.negotiate` at the transport layer
  - On successful keyed negotiate: sends response on plaintext, flushes, then switches to `handle_btsp_connection` (encrypted framing via `BtspFrameReader`/`BtspFrameWriter`)
  - On NULL fallback: sends response, continues plaintext NDJSON

### Code Health

- **`register_with_discovery` extracted** from `transport.rs` to `discovery.rs` — discovery logic belongs with discovery module (transport.rs 799→787 lines)
- **File sizes**: transport.rs 787L, btsp.rs 795L, discovery.rs 406L — all under 800L limit
- **59 registered JSON-RPC methods** (was 58)
- **`hkdf 0.12`** added to workspace dependencies (pure Rust, RustCrypto)

### Test Coverage

10 new tests:
- `negotiate_phase3_happy_path_chacha`: full key derivation, 12-byte nonce, 32-byte derived key
- `negotiate_phase3_null_fallback_no_key_material`: NULL cipher when session_key empty
- `negotiate_phase3_null_fallback_unsupported_cipher`: NULL cipher for "null" request
- `negotiate_phase3_invalid_session_id`: error on mismatched session
- `negotiate_phase3_missing_session_id`: error on empty/missing session_id
- `negotiate_phase3_derived_key_deterministic_with_same_nonce`: random nonces differ across invocations
- `negotiate_phase3_wire_name_roundtrip`: Null/HmacPlain/ChaCha20Poly1305 names
- `negotiate_phase3_cipher_from_wire_hyphenated`: `chacha20-poly1305` accepted
- `btsp_negotiate_dispatch_requires_session`: dispatch returns -32600 without session
- 288 barracuda-core tests pass, 2,107 barracuda tests pass, 16 naga-exec tests pass

### Quality Gates

- `cargo fmt --all --check`: clean
- `cargo clippy -- -D warnings`: clean
- `RUSTDOCFLAGS="-D warnings" cargo doc --no-deps`: clean
- `cargo deny check licenses`: clean
- `cargo deny check bans`: clean

## Wire Format

```
Client → barraCuda:
  {"jsonrpc":"2.0","method":"btsp.negotiate","params":{
    "session_id": "<from Phase 1 handshake>",
    "preferred_cipher": "chacha20-poly1305",
    "bond_type": "Covalent"
  },"id":...}

barraCuda → Client (success):
  {"jsonrpc":"2.0","result":{
    "cipher": "chacha20-poly1305",
    "server_nonce": "<24-char hex>"
  },"id":...}

barraCuda → Client (fallback):
  {"jsonrpc":"2.0","result":{"cipher":"null"},"id":...}
```

After successful keyed response, all subsequent frames use:
`[4B len BE u32][12B nonce][ciphertext + Poly1305 tag]`

## Reference Alignment

- petalTongue (PT-09): server-side reference in `crates/petal-tongue-ipc/src/btsp/json_line.rs`
- primalSpring client: `ecoPrimal/src/ipc/btsp_handshake.rs` `negotiate_phase3()`
- primalSpring integration tests: `phase3_negotiate_with_live_beardog`, `phase3_transport_full_roundtrip` (currently `#[ignore]`, will auto-validate when barraCuda binary deployed)

## Remaining BTSP Phase 3 Items

- AES-256-GCM cipher variant: deferred (ChaCha20-Poly1305 is the primary cipher)
- Client-side BTSP: deferred to sourDough scaffold
- `client_nonce` HKDF input: spec references `client_nonce || server_nonce` for HKDF info — currently using `server_nonce` as salt with fixed info label; will align when primalSpring integration tests exercise the full roundtrip
