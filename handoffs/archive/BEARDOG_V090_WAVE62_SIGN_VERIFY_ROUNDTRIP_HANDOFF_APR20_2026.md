# BearDog v0.9.0 — Wave 62 Handoff

## From: BearDog primal team
## Date: April 20, 2026
## Trigger: primalSpring v0.9.17 Phase 45 audit (guidestone certification)

---

## What Changed

Two issues identified by primalSpring Phase 45 guidestone certification:

### 1. `crypto.sign` now returns `public_key` (BD-PG-01 — RESOLVED)

**Before:** `crypto.sign` returned `{signature, algorithm, key_id}`. The public key
was derived internally but discarded (`_public_key`). Callers had no way to perform
sign→verify roundtrip without independently re-deriving the key from `key_id`.

**After:** Response now includes `public_key` (standard base64, 32 bytes decoded):

```json
{
  "signature": "<base64>",
  "algorithm": "Ed25519",
  "key_id": "default_signing_key",
  "public_key": "<base64>"
}
```

Callers can now feed `signature` and `public_key` directly into `crypto.verify`.

### 2. Ed25519 encoding standardized to standard base64 (BD-PG-02 — RESOLVED)

**Before:** `crypto.sign` / `crypto.generate_keypair` returned standard base64,
but capability announcements and ionic bond signatures used hex encoding. Consumers
had to guess which encoding was in use.

**After:** All Ed25519 output paths use standard base64:
- `primal_signing::sign_with_primal_identity` → base64 (was hex)
- `capabilities.list` announcement → `signature` and `public_key` in base64
- `crypto.ionic_bond.propose` → `proposer_signature` in base64
- `crypto.sign_contract` → `signature` and `public_key` in base64

**Backward compatibility:** `verify_ed25519_signature` (ionic bond internal)
accepts both standard base64 and hex. External callers sending hex-encoded
acceptor signatures will still work.

---

## Files Changed

| File | Change |
|------|--------|
| `handlers/crypto/asymmetric.rs` | Added `public_key` to sign response |
| `handlers/primal_signing.rs` | hex→base64 for `sign_with_primal_identity` |
| `handlers/ionic_bond/crypto.rs` | `verify_ed25519_signature` accepts base64+hex; updated docs |
| `beardog-types/src/ionic_bond.rs` | `SignContractResponse` doc comments updated |
| `handlers/crypto/asymmetric_tests.rs` | Roundtrip test uses response `public_key` |
| `handlers/ionic_bond/tests.rs` | All tests updated to base64 |
| `CHANGELOG.md`, `STATUS.md`, `ROADMAP.md` | Wave 62 entries |

## Quality Gates

- `cargo fmt` — clean
- `cargo clippy -D warnings` — 0 errors
- `cargo test --workspace` — 14,786+ tests, 0 failures (1 pre-existing env-dependent skip in `beardog-ipc`)
- 55 targeted crypto/bond/signing tests — all pass

## For Spring Teams

- `crypto.sign` responses now include `public_key` — update guidestone to use it
  directly instead of calling `crypto.ed25519_generate_keypair` or re-deriving
- Ed25519 fields in capability announcements and ionic bonds are now standard
  base64 — update any hex decode paths to use base64 decode
- `crypto.verify` already accepts both `base64` and `hex` via the `encoding` param

---

**License**: AGPL-3.0-or-later
