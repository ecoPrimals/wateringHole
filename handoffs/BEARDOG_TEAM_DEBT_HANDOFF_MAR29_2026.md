# BearDog Team Debt Handoff

**Date:** 2026-03-29
**From:** primalSpring ecosystem audit
**To:** Dedicated BearDog team
**Scope:** All known debt categorized by severity and type

---

## Recent Fixes (this session)

These items were resolved during the primalSpring v0.8.0 audit:

- `genetic.derive_lineage_beacon_key` registered in `method_list.rs` (was missing, method count 92->93)
- Empty/zero/short lineage seeds now rejected in `handle_derive_lineage_beacon_key`
- `federation.verify_family_member` label corrected from `genetic_lineage_hkdf` to `family_id_equality`
- `encryption.encrypt/decrypt` docs no longer claim "HSM-backed" (software SHA-256 KDF)

---

## Blocking (ship / integration risk)

### B-1: Vault and USM Secrets Backends Not Implemented

`SecretsProvider::Vault` and `SecretsProvider::UniversalSecretsManagement` always
return explicit "not yet implemented" errors. Only environment-based secrets work.
Any production deployment enabling these providers will fail at runtime.

**Location:** `crates/beardog-production/src/config_management/runtime.rs` (~334-348)
**Impact:** Blocks production deployments needing externalized secrets
**Effort:** Medium — interface is defined, needs Vault/USM client implementation

### B-2: Security API Gaps (Key Rotation, Expiration)

Integration tests are explicitly disabled with notes that key rotation and key
expiration tracking are not in the current API, plus a SecurityMetrics reorg
is pending.

**Location:** `crates/beardog-security/src/tests/security_integration_tests.rs` (lines 240-247, 283)
**Impact:** No automated key lifecycle management
**Effort:** Medium-High — API design + implementation + test suite

### B-3: RSA Marvin Advisory (RUSTSEC-2023-0071)

`deny.toml` suppresses the RSA Marvin timing attack advisory with rationale that
RSA is legacy/interop only. This is a standing risk decision, not a resolution.

**Location:** `deny.toml` (lines 7-11)
**Impact:** Low (RSA is interop-only), but requires periodic re-evaluation
**Action:** Document the risk acceptance; re-evaluate when `rsa` crate updates

### B-4: Ed25519 Property Tests Blocked

Ed25519 key-pair derivation "enhancement" and dependent signature roundtrip test
are `#[ignore]`, blocking property-based crypto validation.

**Location:** `crates/beardog-tunnel/tests/property_crypto_roundtrips.rs` (lines 118, 190)
**Impact:** Reduced confidence in Ed25519 edge cases
**Effort:** Low-Medium — implement the enhancement, unblock tests

---

## Significant (architecture, ops, or quality)

### S-1: Workspace Layout — Two `beardog` Packages

Root `Cargo.toml` excludes `crates/beardog` from workspace members. There is a
full library crate at `crates/beardog/` (comment about breaking circular deps
with tunnel). A team inheriting this needs a clear mental model: root binary
crate vs `crates/beardog` library.

**Location:** Root `Cargo.toml` exclude list (lines 8-18), `crates/beardog/Cargo.toml`
**Action:** Document the relationship or consolidate

### S-2: println-to-tracing Migration

Production-adjacent code paths still use `println!`/`eprintln!` instead of
`tracing`. Key areas:

- `crates/beardog-cli/src/handlers/*.rs` (CLI output — lower priority)
- `crates/beardog-tunnel/src/diagnostics/` (diagnostic tools)
- `crates/beardog-tunnel/src/modes/doctor.rs` (doctor mode)
- `crates/beardog-installer/` (installer)
- `crates/beardog-integration/src/heartbeat.rs` (integration)
- `crates/beardog-workflows/src/workflows/performance_benchmarks.rs`

**Note:** CLI user-facing output and `#[cfg(test)]` blocks are acceptable.
Focus on library/server code paths.
**Effort:** Low per file, medium total surface

### S-3: AI / Hybrid Intelligence Placeholders

Comments describe modules as "temporarily adjusted" with placeholder capability
initialization and placeholder entropy in `sovereign_rng.rs`. The AI vertical
is explicitly not finished.

**Location:**
- `crates/beardog-core/src/ai/hybrid_intelligence/core.rs` (~30-32, ~420-422)
- `crates/beardog-core/src/ai/sovereign_rng.rs` (~290, ~417)
**Impact:** AI features are stubs — not blocking crypto core

### S-4: Aggressive MSRV

Workspace `rust-version = "1.93.0"` with edition 2024. This constrains CI,
distro toolchains, and contributors. Deliberate policy but a real onboarding
friction point.

**Location:** Root `Cargo.toml` (lines 20-23)

### S-5: Dependency Notes

- `serde_yaml` marked deprecated upstream; successor tracked (`yaml-serde`)
- `serial_test` version drift between workspace (3.0) and root dev-deps (3.2)
- Commented deferred crypto (AES legacy modes)

**Location:** Root `Cargo.toml` (~126-175, 281-299)

---

## Minor (track, not emergencies)

### M-1: Platform / IPC Gaps

iOS test: "XPC documented, awaiting Pure Rust bindings"
`crates/beardog-tunnel/src/platform/mod.rs` (~329-332)

### M-2: External Environment Tests

- UPA endpoint test: `#[ignore = "Requires a UPA endpoint"]` — `crates/beardog-integration/src/upa_client.rs` (408)
- BTSP contact exchange: `#[ignore = "Requires HSM initialization"]` — `crates/beardog-tunnel/tests/btsp_contact_exchange_tests.rs`
- Hardware suite: 4 tests requiring real SoftHSM2/Android/FIDO2 — `tests/hardware_agnostic_suite.rs`
- 1MB slow crypto test: `crates/beardog-tunnel/.../comprehensive_tests.rs`

### M-3: Clippy Policy Maintenance

Workspace-wide clippy allows (style, async Send, casts) plus many per-site
`#[expect(...)]` in production code. Not blocking but an ongoing maintenance
contract for new team members to understand.

---

## Positive Signals

- Zero `TODO`/`FIXME`/`HACK` markers in `.rs` files
- Zero `unimplemented!`/`todo!()` macros
- `unsafe_code = "forbid"` at workspace level — verified clean
- Root `README.md` and `CONTEXT.md` exist and are current
- 93 crypto RPC methods registered and tested
- Comprehensive negative test coverage in own suite (wrong-family, wrong-key, tampered ciphertext)

---

## Recommended Priority Order

1. **B-4:** Unblock Ed25519 property tests (low effort, high confidence gain)
2. **B-2:** Design and implement key rotation/expiration API
3. **S-2:** Targeted println-to-tracing pass on non-CLI code
4. **B-1:** Implement Vault secrets backend
5. **S-1:** Document or resolve the dual-package workspace layout
6. **B-3:** Re-evaluate RSA advisory when `rsa` crate updates
