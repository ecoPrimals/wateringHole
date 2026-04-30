<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 77 Handoff: `crypto.derive_public_key` for biomeOS Coordination Keys

**Date**: April 30, 2026
**From**: BearDog Team
**To**: biomeOS, primalSpring, all consuming primals
**Audit source**: primalSpring v0.9.24 (April 30, 2026)

---

## New Method: `crypto.derive_public_key`

biomeOS Neural API calls `crypto.derive_public_key` with `{"purpose": "coordination"}`
at startup to cache a coordination public key for graph signing. This was returning
method-not-found on the current binary. Now implemented.

### Wire Format

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "crypto.derive_public_key",
  "params": {
    "purpose": "coordination"
  },
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "public_key": "<base64-ed25519-32-bytes>",
    "algorithm": "Ed25519",
    "purpose": "coordination",
    "derivation": "HMAC-SHA256-purpose-v1 → Ed25519"
  },
  "id": 1
}
```

### Derivation Path

1. `purpose_key = HMAC-SHA256(FAMILY_SEED, hex("purpose-v1:" + purpose))` — 32-byte key
2. `signing_key = Ed25519::from_bytes(purpose_key)` — treat as Ed25519 seed
3. `public_key = signing_key.verifying_key()` — 32-byte Ed25519 public key

Same HMAC-SHA256-purpose-v1 convention as `crypto.derive_purpose_key`. The public key
is deterministic for a given `FAMILY_SEED` + `purpose` pair.

### Requirements

- `FAMILY_SEED` or `BEARDOG_FAMILY_SEED` env var must be set (returns error otherwise).
- `purpose` parameter is required (returns error with guidance if missing).

### biomeOS Integration

biomeOS `derive_coordination_key()` calls:
```rust
client.call("crypto.derive_public_key", json!({"purpose": "coordination"}))
```
The `public_key` field in the response is the hex-encodable Ed25519 public key
cached in `NeuralApiServer::coordination_pubkey`.

---

## BTSP Phase 3

Deferred per primalSpring v0.9.24 audit. Phase 2 handshake (HMAC-SHA256 challenge-
response) is sufficient for current composition validation. Phase 3 (ChaCha20-Poly1305
encrypted channel) remains on the roadmap.

---

## Method Count

| Handler | Before | After |
|---------|--------|-------|
| CryptoHandler | 96 | 97 |
| Total (all handlers) | 101 | 102 |

---

## CI Status

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace -- -D warnings` | 0 warnings |
| `cargo deny check` | 4/4 pass |
| `cargo test --workspace` | 0 new failures (1 pre-existing flaky in beardog-ipc) |
| New tests | 7 passing |
