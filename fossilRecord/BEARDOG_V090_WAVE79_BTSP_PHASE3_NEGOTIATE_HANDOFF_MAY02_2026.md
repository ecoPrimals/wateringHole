<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 79: BTSP Phase 3 `btsp.negotiate` Server-Side Implementation

**Date**: May 2, 2026
**Primal**: BearDog (Tower — Security/Crypto)
**Trigger**: primalSpring Phase 56c audit — BTSP Phase 3 evolution request

---

## Summary

Implemented the `btsp.negotiate` JSON-RPC method handler for BTSP Phase 3 encrypted
post-handshake channel negotiation. This is the server-side counterpart to
primalSpring's `negotiate_phase3()` client implementation.

## What Was Implemented

### `btsp.negotiate` Method

**Wire format (client → server):**
```json
{
  "jsonrpc": "2.0",
  "method": "btsp.negotiate",
  "params": {
    "session_id": "<from Phase 1 handshake>",
    "ciphers": ["chacha20-poly1305"],
    "client_nonce": "<base64-encoded 32 bytes>"
  },
  "id": 1
}
```

**Wire format (server → client):**
```json
{
  "cipher": "chacha20-poly1305",
  "server_nonce": "<base64-encoded 32 bytes>"
}
```

**NULL cipher fallback (unsupported cipher):**
```json
{
  "cipher": "null",
  "server_nonce": ""
}
```

### Cipher Selection Priority

1. `chacha20-poly1305` (ChaCha20-Poly1305 AEAD)
2. `hmac-plain` (HMAC integrity without encryption)
3. `null` (plaintext fallback — zero breakage)

### Phase 3 Session Key Derivation

```
HKDF-SHA256(
  ikm  = handshake_key,
  salt = client_nonce || server_nonce,
  info = "btsp-session-v1-c2s" → client_to_server key (32 bytes)
  info = "btsp-session-v1-s2c" → server_to_client key (32 bytes)
)
```

The `handshake_key` is re-derived deterministically from `FAMILY_SEED` via
`derive_handshake_key()` — same HKDF path as Phase 1 handshake.

Server-side keys: encrypt = server_to_client, decrypt = client_to_server
(mirrored from primalSpring client-side).

### Wire Compatibility

Accepts both parameter forms:
- `"ciphers": ["chacha20-poly1305"]` (primalSpring canonical, array)
- `"preferred_cipher": "chacha20-poly1305"` (audit blurb form, single string)

## Files Changed

| File | Change |
|------|--------|
| `crates/beardog-tunnel/src/btsp_handshake/crypto.rs` | Added `derive_phase3_session_keys()` and `Phase3SessionKeys` type |
| `crates/beardog-tunnel/src/unix_socket_ipc/handlers/btsp/negotiation.rs` | Added `handle_phase3_negotiate()`, cipher selection, family seed loader, 8 tests |
| `crates/beardog-tunnel/src/unix_socket_ipc/handlers/btsp/mod.rs` | Registered `btsp.negotiate` in `methods()` and `handle()` routing |
| `crates/beardog-tunnel/src/unix_socket_ipc/handlers/capabilities.rs` | Added `btsp_phase3` capability group, cost estimate, dependency |
| `crates/beardog-tunnel/src/unix_socket_ipc/handlers/btsp_tests.rs` | Updated method count assertion (35 → 36) |
| `crates/beardog-tunnel/src/unix_socket_ipc/handlers/crypto_handler_tests.rs` | Fixed pre-existing conflicting method count assertions (97 vs 102) |

## Test Results

- **12 new Phase 3 tests** (all passing):
  - Cipher selection: prefers chacha20, hmac fallback, null fallback, empty list
  - Handler: happy path, null cipher for unsupported, missing params/session_id/client_nonce, missing FAMILY_SEED, preferred_cipher alias, key derivation verification
  - Crypto: deterministic, directional, nonzero, nonce sensitivity
- **133 total BTSP tests** passing
- **Full workspace**: 2,127+ tests passing, 0 new failures (1 pre-existing flaky in beardog-cli)
- **CI**: fmt clean, clippy clean, deny 4/4 pass

## Validation Path

primalSpring has two `#[ignore]` integration tests that will auto-validate:
- `phase3_negotiate_with_live_beardog`
- `phase3_transport_full_roundtrip`

Push to main → plasmidBin auto-harvests → primalSpring fetches → tests validate.

## Reference Implementations

- **primalSpring client**: `ecoPrimal/src/ipc/btsp_handshake.rs` `negotiate_phase3()`
- **primalSpring Phase 3 types**: `ecoPrimal/src/btsp/phase3.rs` (SessionKeys, NegotiateResponse, Phase3Cipher)
- **petalTongue server**: `crates/petal-tongue-ipc/src/btsp/json_line.rs` (reference server)

## What's Next

The `btsp.negotiate` handler derives session keys but the actual encrypted framing
switch (length-prefixed AEAD frames replacing NDJSON) is a follow-up. Current Phase 2
NULL cipher transport continues to work for all connections. The key material is
correctly derived and ready for framing integration when the ecosystem converges.
