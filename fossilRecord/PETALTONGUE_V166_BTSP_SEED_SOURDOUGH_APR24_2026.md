# petalTongue — BTSP family_seed Base64 Encoding Fix

**Date:** April 24, 2026
**From:** primalSpring Phase 45c audit finding (two rounds)
**Status:** Resolved — base64 encoding now applied per corrected SOURDOUGH standard

---

## Audit Finding

primalSpring reported `load_family_seed()` must base64-encode the raw hex
`FAMILY_SEED` before sending to BearDog. BearDog's `btsp.session.create`
handler explicitly base64-decodes the `family_seed` parameter. Sending raw
hex caused HMAC mismatch (guidestone error: "BTSP verification failed: unknown").

## Resolution (Two Commits)

### Commit af2b2e8 (first pass — trim only)
Initial investigation found a contradicting SOURDOUGH doc that said "pass raw,
do NOT base64-encode." Applied trim fix and doc comment correction only.

### Commit 96ae4b3 (second pass — base64 encoding)
primalSpring confirmed the SOURDOUGH doc guidance was stale and has been
corrected. BearDog explicitly base64-decodes the param. All 4 other relay
primals (ToadStool, NestGate, barraCuda, Songbird) and all passing primals
(Squirrel, coralReef, sweetGrass) base64-encode. Applied the encoding fix.

## Fix Applied

`load_family_seed()` in `crates/petal-tongue-ipc/src/btsp/types.rs`:
1. Read `BEARDOG_FAMILY_SEED` > `FAMILY_SEED` from env
2. Trim whitespace
3. Base64-encode the trimmed bytes via `base64::engine::general_purpose::STANDARD`
4. Return the encoded string

6 tests updated to use raw string inputs and verify base64 output:
- Priority: BEARDOG_FAMILY_SEED preferred over FAMILY_SEED
- Fallback: FAMILY_SEED used when BEARDOG_FAMILY_SEED absent
- Encoding: raw hex → correct base64 output
- Trim: whitespace removed before encoding
- Edge cases: empty-after-trim returns None, unset returns None

## Verification

- `cargo clippy --workspace --all-targets --all-features -- -D warnings` → 0
- `cargo test -p petal-tongue-ipc --all-features` → all 6 seed tests pass
- `cargo check --target x86_64-apple-darwin` → pass
