<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 39: wetSpring Alignment Handoff

**Date**: April 13, 2026
**Status**: Complete — all quality gates pass
**Triggered by**: Cross-spring validation against wetSpring's modern systems

---

## 1. Gap Analysis (wetSpring → BearDog)

Validated wetSpring's consumed capabilities against BearDog's actual RPC surface:

| Capability | wetSpring Expects | BearDog Status |
|------------|------------------|----------------|
| `crypto.sign_ed25519` | `niche.rs` CONSUMED_CAPABILITIES | PASS (existing) |
| `crypto.verify_ed25519` | `niche.rs` CONSUMED_CAPABILITIES | PASS (existing) |
| `crypto.blake3_hash` | `niche.rs` CONSUMED_CAPABILITIES | PASS (existing + `crypto.hash` alias) |
| `security.verify_consent` | `vault_ipc.rs` → Neural API | **NEW** (Wave 39) |
| `security.issue_consent_token` | Token lifecycle | **NEW** (Wave 39) |
| `probe_capability("security")` | `composition_tower_health` | PASS (identity + capability handlers) |
| BTSP `security_model` | Deploy graph nodes | PASS (Phase 2+3) |
| `identity.get` | Wire Standard L2 | PASS (existing) |

---

## 2. Consent Gate Implementation

### `security.verify_consent`

**Wire contract** (matches wetSpring `vault_ipc.rs` expectations):

```json
← { "method": "security.verify_consent", "params": { "owner_id": "alice", "scope": "vault:read:genome", "token": "<base64>" } }
→ { "valid": true, "owner_id": "alice", "scope": "vault:read:genome", "verified_at": "...", "verified_by": "beardog" }
```

**Cryptography**: HMAC-SHA256(key, `owner_id:scope`) where key = BLAKE3(`family_id:consent-hmac-key`).

- Family-scoped: tokens issued by family-A are rejected by family-B.
- Deterministic: same family always produces the same key.
- No persistence: stateless verification (token carries proof).

### `security.issue_consent_token`

Companion method to mint tokens:

```json
← { "method": "security.issue_consent_token", "params": { "owner_id": "alice", "scope": "vault:read:genome" } }
→ { "token": "<base64>", "owner_id": "alice", "scope": "vault:read:genome", "issued_at": "...", "issued_by": "beardog" }
```

### Neural API Routing

`register_with_neural_api()` now includes `security` capability domain with 5 operations. Neural API routes `capability.call("security", "verify_consent", args)` to BearDog's `security.verify_consent` method — exactly matching wetSpring's `verify_consent_via_beardog()` call pattern.

---

## 3. Tests Added (6)

| Test | Validates |
|------|-----------|
| `test_issue_and_verify_consent_roundtrip` | Issue → verify cycle succeeds |
| `test_verify_consent_rejects_bad_token` | Forged tokens fail |
| `test_verify_consent_rejects_wrong_scope` | Scope-bound (vault:read ≠ vault:write) |
| `test_verify_consent_different_family_rejects` | Cross-family tokens fail |
| `test_verify_consent_missing_params` | Graceful error for missing/partial params |
| `test_security_handler_includes_consent_methods` | Method registration verified |

---

## 4. Capabilities Surface Updated

- `provided_capabilities` → security type bumped to v1.1 with consent methods
- `discover_capabilities` → flat list includes `consent.verify` + `consent.issue`
- `cost_estimates` → both consent methods: low CPU, 1ms latency
- Neural API auto-registration → `security` domain registered with 5 operations

---

## 5. Code Health

| Metric | Value |
|--------|-------|
| Tests | 14,780+ passing, 0 failed |
| Coverage | 90.51% (llvm-cov) |
| Clippy | 0 warnings (pedantic) |
| Format | Clean |
| Docs | 0 warnings |
| Rust Files | 2,150 |
| JSON-RPC Methods | 99 |
| `#[allow(` | 86 |
| `#[expect(` | 642 |

---

## 6. Files Modified

| File | Change |
|------|--------|
| `crates/beardog-tunnel/src/unix_socket_ipc/handlers/security.rs` | +`security.verify_consent`, +`security.issue_consent_token`, +6 tests |
| `crates/beardog-tunnel/src/unix_socket_ipc/handlers/capabilities.rs` | +consent capability, +cost estimates, +discover_capabilities entries |
| `crates/beardog-ipc/src/neural_registration.rs` | +`security` capability domain registration |
| `README.md`, `STATUS.md`, `ARCHITECTURE.md`, `CONTEXT.md`, `CHANGELOG.md` | Metrics and Wave 39 entry |

---

## 7. Remaining Low-Priority Debt

- **Ionic bond persistence** — NestGate/loamSpine integration for durable bonds (blocked on NestGate)
- **HSM/BTSP Phase 3 signing path** — Stubbed (awaiting hardware fleet)
- **wetSpring YAML niche drift** — `niches/wetspring-ecology.yaml` lists `crypto.encrypt` / `crypto.sign` / `identity.verify` while `niche.rs` uses `crypto.sign_ed25519` / `crypto.verify_ed25519` / `crypto.blake3_hash`. This is a wetSpring-side alignment task.
- **PUF → device identity chain** — `specs/DATA_TYPES.md` references BearDog for PUF attestation (P2 future)
