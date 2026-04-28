<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 72: NUCLEUS Purpose Key Derivation & Signed Registrations

> April 28, 2026

## Summary

Resolves primalSpring v0.9.20 Phase 55 audit gaps:

1. **`crypto.derive_purpose_key`** — First-class NUCLEUS two-tier purpose key derivation. Single-family NUCLEUS deployments no longer need to chain raw `crypto.hmac_sha256` calls.
2. **`crypto.sign_registration`** — Signs `ipc.register` payloads so consumers can verify authentic service registrations through Songbird.

## New IPC Methods

### `crypto.derive_purpose_key`

Derives a purpose-specific 32-byte key from a parent family key using the NUCLEUS convention:

```
purpose_key = HMAC-SHA256(family_key, hex("purpose-v1:" + purpose))
```

**Wire format:**

```json
{
  "jsonrpc": "2.0",
  "method": "crypto.derive_purpose_key",
  "params": {
    "key": "<base64 family key>",
    "purpose": "storage"
  },
  "id": 1
}
```

**Response:**

```json
{
  "key": "<base64 derived 32-byte key>",
  "purpose": "storage",
  "method": "HMAC-SHA256-purpose-v1"
}
```

Purpose values align with `wateringHole/NUCLEUS_TWO_TIER_CRYPTO_MODEL.md`: `storage`, `dag`, `ledger`, `provenance`, `compute`, `tensor`, `shader`, `inference`, `visualization`, `coordination`, `security`, `discovery`.

### `crypto.sign_registration`

Signs a canonicalized `ipc.register` payload with Ed25519.

**Wire format:**

```json
{
  "jsonrpc": "2.0",
  "method": "crypto.sign_registration",
  "params": {
    "primal_id": "barracuda",
    "capabilities": ["tensor", "math", "stats"],
    "endpoint": "unix:///run/user/1000/biomeos/barracuda-fam.sock"
  },
  "id": 2
}
```

**Response:**

```json
{
  "signature": "<base64 Ed25519 signature>",
  "public_key": "<base64 Ed25519 public key>",
  "canonical": "ipc.register-v1:primal_id=barracuda,capabilities=[math,stats,tensor],endpoint=unix:///run/user/1000/biomeos/barracuda-fam.sock",
  "algorithm": "Ed25519"
}
```

Capabilities are sorted alphabetically in the canonical string. Consumers verify with `crypto.verify(public_key, base64(canonical), signature)`.

## Changes

| File | Change |
|------|--------|
| `crates/beardog-tunnel/src/unix_socket_ipc/handlers/crypto_handler/aliases_and_beardog.rs` | Added `crypto.derive_purpose_key` and `crypto.sign_registration` routes + handlers + 5 tests |
| `crates/beardog-tunnel/src/unix_socket_ipc/handlers/crypto_handler/method_list.rs` | Registered both new methods |
| `crates/beardog-tunnel/src/unix_socket_ipc/handlers/capabilities.rs` | Added cost estimates for both methods |
| `crates/beardog-tunnel/src/unix_socket_ipc/handlers/crypto_handler_tests.rs` | Method count 99 → 101 |

## For primalSpring

The `nucleus_crypto_bootstrap.sh` can now replace HMAC chains with a single `crypto.derive_purpose_key` call per atomic:

```bash
# Before (HMAC chain workaround):
purpose_data=$(echo -n "purpose-v1:storage" | xxd -p)
purpose_key=$(tower_call crypto.hmac '{"key":"'$family_key'","data":"'$(echo -n "$purpose_data" | base64)'"}' | jq -r .mac)

# After (first-class method):
purpose_key=$(tower_call crypto.derive_purpose_key '{"key":"'$family_key'","purpose":"storage"}' | jq -r .key)
```

For signed registrations, the composition launcher or self-registering primals can:

```bash
signed=$(tower_call crypto.sign_registration '{"primal_id":"barracuda","capabilities":["tensor","math"],"endpoint":"'$endpoint'"}')
# Pass signature + public_key alongside ipc.register
```

## CI

- `cargo fmt` clean
- `cargo clippy --workspace -- -D warnings` 0 warnings
- `cargo deny check` 4/4
- `cargo test --workspace` 14,928+ passing (1 pre-existing known flaky)
