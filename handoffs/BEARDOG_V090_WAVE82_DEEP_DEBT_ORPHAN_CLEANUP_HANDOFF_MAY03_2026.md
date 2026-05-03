<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 82: Deep Debt — Orphan Code Removal, Stale Lints & Workspace Hygiene

**Date**: May 3, 2026
**Primal**: BearDog (Tower — Security/Crypto)
**Wave**: 82
**Type**: Deep debt cleanup

---

## Summary

Wave 82 is a focused deep debt pass: orphan file deletion, deprecated zero-caller symbol removal, stale lint annotation cleanup, workspace dependency centralization, and doc hygiene. Net -783 LOC.

## Changes

### Orphan Code Deleted

- `crates/beardog-types/src/canonical/config/discovery.rs` (716 lines) — existed on disk but was never declared in any `mod.rs`. Never compiled, never tested. Contained deprecated `ConsolidatedDiscoveryConfig`, `LegacyDiscoveryProtocol`, `HealthCheckConfig`, `RetryConfig`, `LoadBalancingConfig` structs that were superseded by canonical domain types.

### Deprecated Zero-Caller Type Aliases Removed

From `beardog-production/src/config_management/mod.rs`:
- `ConnectionPoolConfig` — aliases canonical `domains::network::ConnectionPoolConfig`
- `LoggingConfig` — aliases canonical `domains::system::LoggingConfig`
- `LogFormat` — aliases canonical `domains::system::LogFormat`
- `LoadBalancerConfig` — aliases canonical `domains::network::connection::LoadBalancerConfiguration`
- `MigrationConfig` — aliases canonical `domains::database::MigrationConfig`
- `BackupConfig` — aliases canonical `production::operations::BackupConfig`

All production code already uses the canonical paths directly. Stale `CanonicalMigrationConfig` import also removed.

### Lint Hygiene

- 2 stale `#[expect(dead_code)]` removed — `SIMDCapabilities` struct (fields dead, not struct itself) and `MockCloudHsm::with_failures()` (now has callers). Replaced with `#[allow(dead_code, reason = "...")]` where field-level suppression still needed.
- 8 `#[allow]` without `reason` attribute given proper `reason` — all `#[allow]` now carry `reason` per modern Rust style.
- `base64-url` centralized to `[workspace.dependencies]` — was the last crate-local version pin.
- HSM management methods documented as "software-only mode" with `reason` on `allow(dead_code)`.
- Session lifetime constant `DEFAULT_EXTENDED_SESSION_LIFETIME_SECS` given `reason` on test-only `allow(dead_code)`.

### Documentation

- All root docs (README, STATUS, ROADMAP, ARCHITECTURE, CONTEXT, START_HERE, SECURITY, docs/README, ROOT_INDEX) updated to May 3, 2026.
- Wave 81 + 82 added to STATUS recent improvements and ROADMAP recently completed.
- `.github/README.md` corrected — referenced non-existent `beardog-ci.yml`, now correctly references `ci.yml` and `notify-plasmidbin.yml`.

## CI Results

- **cargo fmt**: clean
- **cargo clippy --workspace**: 0 warnings
- **cargo clippy --workspace --all-targets**: 0 unfulfilled lint expectations
- **cargo test --workspace --lib**: 12,610 passed, 0 failed

## Files Changed

| File | Change |
|------|--------|
| `Cargo.toml` | Added `base64-url = "3.0"` to workspace deps |
| `crates/beardog-security/Cargo.toml` | `base64-url` → `workspace = true` |
| `crates/beardog-types/src/canonical/config/discovery.rs` | **DELETED** (716 lines) |
| `crates/beardog-production/src/config_management/mod.rs` | 6 deprecated aliases + stale import removed |
| `crates/beardog-utils/src/ultimate_performance.rs` | Stale `#[expect]` → `#[allow]` with reason |
| `crates/beardog-tunnel/src/tunnel/hsm/hsm_provider_mocks.rs` | Stale `#[expect]` removed |
| `crates/beardog-tunnel/src/tunnel/session.rs` | `reason` added to session constant allow |
| `crates/beardog-core/src/ecosystem/primal_interface/hsm_management.rs` | Docs clarified, `reason` added |
| `crates/beardog-security/src/tests/recovery_tests/types.rs` | 4 `#[allow]` given `reason` |
| `crates/beardog-types/src/canonical/config/tests/modernization/meta_tests.rs` | 2 `#[allow]` given `reason` |
| `crates/beardog-types/src/tests/coverage_gap_tests_5.rs` | `#[allow]` given `reason` |
| `crates/beardog-types/src/tests/coverage_gap_tests_7.rs` | `#[allow]` given `reason` |

## Downstream Impact

- No API changes — all removed items had zero callers
- No wire format changes
- No behavioral changes
- Binary size reduction from dead code elimination

## Audit Confirmed Clean

- 0 files >800 LOC (production)
- 0 unsafe code blocks
- 0 production mocks outside `#[cfg(test)]`
- 0 hardcoded peer primal names in runtime logic
- 0 TODO/FIXME/HACK
- 0 `Box<dyn Error>` in production
- 0 async-trait remnants
- 0 unfulfilled lint expectations
