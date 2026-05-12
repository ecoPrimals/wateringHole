<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 43: Deep Debt Sweep — Unused Deps, Dead Features, Commented Imports, Smart Refactor

**Date**: April 13, 2026
**Primal**: BearDog (cryptographic service provider)
**Scope**: Workspace dependency hygiene, dead feature removal, code comment cleanup, smart file refactoring

---

## 1. Summary

Comprehensive audit across all 29 crates targeting: unused workspace dependencies, dead Cargo features, commented-out import debris, large file refactoring, and production wildcard imports. Zero unsafe code confirmed. Remaining `#[allow(` attributes documented as justified (cfg-dependent, deprecated re-exports, multi-lint test modules).

---

## 2. Unused Workspace Dependencies Removed

| Dependency | Version | Reason |
|-----------|---------|--------|
| `mockall` | 0.12 | Declared in `[workspace.dependencies]`, referenced by zero crates |
| `rmp-serde` | 1.1 | Declared in `[workspace.dependencies]`, referenced by zero crates |
| `figment` | 0.10 | Declared in `[workspace.dependencies]`, referenced by zero crates |
| `config` | 0.14 | Declared in `[workspace.dependencies]`, referenced by zero crates |

---

## 3. Dead Cargo Feature Removed

| Crate | Feature | Evidence |
|-------|---------|----------|
| `beardog-adapters` | `mdns-discovery` | Zero `#[cfg(feature = "mdns-discovery")]` gates in source; zero cross-crate enablement |

---

## 4. Commented-Out Import Lines Cleaned

16 lines across 14 files — debris from earlier refactoring waves. All were `// Removed unused import: ...` comments.

| Crate | Files |
|-------|-------|
| `beardog-monitoring` | `metrics/core.rs`, `advanced_metrics/core.rs`, `monitoring/metrics.rs`, `metrics/export.rs`, `advanced_metrics/types.rs` |
| `beardog-types` | `canonical/monitoring/mod.rs`, `canonical/monitoring/logging.rs`, `canonical/config/validation_comprehensive_tests.rs`, `canonical/config/hsm/mobile.rs` |
| `beardog-threat` | `threat/types/core.rs`, `threat/handlers/response.rs`, `threat/handlers/enrichment.rs`, `threat/handlers/analysis.rs` |
| `beardog-traits` | `unified/providers.rs` |
| `beardog-core` | `ecosystem/ai_first_responses.rs`, `ecosystem_integration/types.rs` |

---

## 5. Smart File Refactor

**`security.rs` (971 → 555 LOC)** — The security handler's inline test module (416 lines, 14 tests) was extracted to `security_tests.rs` using `#[cfg(test)] #[path = "security_tests.rs"] mod tests;`. The handler now contains only routing and crypto logic. Pattern matches `ionic_bond/tests.rs`.

---

## 6. Production Wildcard Import Eliminated

**`ios_secure_enclave/operations.rs`**: `use super::types::*` replaced with 6 explicit imports:
`BiometricPolicy`, `KeyAgreementCapable`, `SecureEnclaveAlgorithm`, `SecureEnclaveAlgorithmType`, `SecureEnclaveConstraint`, `SecureEnclaveKeyMaterial`.

---

## 7. Audit Findings — No Action Needed

| Finding | Status |
|---------|--------|
| Unsafe code | Zero — `forbid(unsafe_code)` workspace + per-crate |
| `todo!()` / `unimplemented!()` | Zero |
| TODO/FIXME/HACK comments | Zero |
| `pub use ::*` in module re-export files | Standard Rust pattern for crate API surface; not production logic wildcards |
| Remaining `#[allow(` (~500) | Justified: deprecated re-exports (unfulfillable expect), cfg-dependent lints, multi-lint test modules |

---

## 8. Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace -- -D warnings` | 0 warnings |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | 0 warnings |
| `cargo test --workspace` | All passing, 0 failures |
