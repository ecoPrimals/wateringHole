# BearDog v0.9.0 — Waves 66–67: crypto.public_key + Deep Debt Audit

**Date:** April 22, 2026
**Primal:** BearDog v0.9.0
**Waves:** 66–67
**Commits:** `66adcebf0` (Wave 66), `2c2c30492` (Wave 67)
**Type:** Feature + Deep Debt

---

## Wave 66 — primalSpring Audit: crypto.public_key, Sign→Verify Roundtrip

### Problem

primalSpring's guidestone SKIPped `crypto:ed25519_verify` because `crypto.sign`
"doesn't expose public_key". The fix was already in place (Wave 62), but:
1. Router-level tests re-derived the key locally instead of using the response
2. No standalone `crypto.public_key` method existed for key retrieval without signing

### Changes

- **`crypto.public_key` method** — New handler in `asymmetric.rs`. Params: `key_id`
  (default `"default_signing_key"`), `purpose` (default `"general"`). Returns
  `{ public_key, algorithm, key_id }`. Registered in aliases router, method list,
  and capabilities.
- **IPC roundtrip tests updated** — `route_crypto_sign_and_verify_alias` and
  `route_ed25519_sign_verify_roundtrip` now use `public_key` from the sign response.
- **4 new tests** — `route_crypto_public_key_matches_sign_response`,
  `route_crypto_public_key_default_key_id`, `test_public_key_default`,
  `test_public_key_matches_sign`.
- **96 crypto methods** registered (was 95).

### For Spring Teams

- `crypto.sign` responses include `public_key` — use it directly for verification
- `crypto.public_key` is available for standalone key retrieval
- primalSpring can unSKIP `crypto:ed25519_verify`

---

## Wave 67 — Deep Debt: Hardcoded Primal Name Cleanup, Full Audit

### Changes

- **2 hardcoded `biomeOS` references removed** from production tracing messages:
  - `primal_discovery.rs` — "biomeOS sockets" → "platform sockets"
  - `discovery.rs` — "biomeOS owns network discovery" → "orchestrator layer owns network discovery"

### Full Audit Results

| Dimension | Status |
|-----------|--------|
| Unsafe code | 0 (`#![forbid(unsafe_code)]` on 28 crate roots) |
| TODO/FIXME/HACK | 0 |
| `#[async_trait]` | 0 (fully eliminated from code + lockfile) |
| Production files >800 LOC | 0 |
| Production mocks ungated | 0 (3 files, all `#[cfg(test)]`) |
| Hardcoded primal names | 0 (was 2, cleaned) |
| Hardcoded ports | 0 runtime (all env/config-driven) |
| `cargo deny` | 4/4 PASS |
| `Box<dyn Error>` | Tests/docs only |
| `#[allow()]` | All justified |

## Quality

| Gate | Status |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --workspace -- -D warnings` | PASS (0 warnings) |
| `cargo deny check` | PASS (4/4) |
| `cargo test --workspace` | 14,925+ tests, 0 failures (1 known flaky pre-existing) |
