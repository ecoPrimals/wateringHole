# BearDog v0.9.0 Wave 74 — Lazy Purpose-Key Derivation & Purpose-Based Encrypt/Decrypt

**Date**: April 28, 2026
**Resolves**: primalSpring v0.9.21 Phase 55b audit (P1 — blocks end-to-end encryption)

---

## What Shipped

### 1. Lazy Purpose-Key Derivation in `secrets.retrieve`

When a secret matching `nucleus:{family}:purpose:{name}` is requested and
doesn't exist, BearDog now **auto-derives** the purpose key from `FAMILY_SEED`
(or `BEARDOG_FAMILY_SEED`) and stores it encrypted in the secrets store.

```json
{"jsonrpc":"2.0","method":"secrets.retrieve","params":{"name":"nucleus:myfam:purpose:storage"},"id":1}
```

Returns the base64-encoded 32-byte purpose key as the `value` field. Subsequent
calls return the cached value. Derivation is deterministic:
`HMAC-SHA256(family_seed_bytes, hex("purpose-v1:" + purpose))`.

**Impact**: NestGate and Squirrel can call `secrets.retrieve` without requiring
`nucleus_crypto_bootstrap.sh` to have run first. Zero manual key setup.

### 2. `crypto.encrypt` with `purpose` Parameter

```json
{"jsonrpc":"2.0","method":"crypto.encrypt","params":{"data":"<b64>","purpose":"storage"},"id":2}
```

Returns the **NUCLEUS standard envelope**:
```json
{"v":1,"ct":"<b64>","n":"<b64>","alg":"chacha20-poly1305","purpose":"storage"}
```

The `ct` field contains ciphertext||tag (standard AEAD format), compatible with
NestGate's encrypt-at-rest envelope.

### 3. `crypto.decrypt` with `purpose` Parameter

```json
{"jsonrpc":"2.0","method":"crypto.decrypt","params":{"ct":"<b64>","n":"<b64>","purpose":"storage"},"id":3}
```

Also accepts `ciphertext`/`nonce` field names for backward compatibility.

Returns: `{"plaintext":"<b64>","algorithm":"chacha20-poly1305","purpose":"storage"}`

### Backward Compatibility

Existing key-based calls (`crypto.encrypt` with `key` param) are **unchanged**.
Purpose-based routing only activates when `purpose` is present in params.

---

## Consumer Integration

### NestGate — Encrypt-at-Rest Key Resolution

```
secrets.retrieve("nucleus:{family}:purpose:storage")
```
Returns a 32-byte key (base64). Use as `NESTGATE_ENCRYPTION_KEY` or directly
in `storage.store`/`retrieve` transparent encryption.

### Squirrel — Inference Payload Encryption

```
crypto.encrypt({"data": "<inference_b64>", "purpose": "inference"})
crypto.decrypt({"ct": "...", "n": "...", "purpose": "inference"})
```

### Requirements

- `FAMILY_SEED` or `BEARDOG_FAMILY_SEED` env var must be set
- Without it, purpose-key operations return an error with clear message

---

## CI Status

- `cargo fmt` — clean
- `cargo clippy --workspace -- -D warnings` — 0 warnings
- `cargo deny check` — 4/4 pass
- `cargo test --workspace` — all pass (1 pre-existing flaky)
- 9 new tests (5 secrets lazy derivation, 4 purpose encrypt/decrypt)
