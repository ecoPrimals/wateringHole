# BearDog v0.9.0 — Wave 80: Dead Code Removal, Deprecated Symbols & Flaky Test Fix

**Date**: May 2, 2026
**Primal**: BearDog (Tower Atomic — Security/Crypto)
**Wave**: 80

---

## Summary

Deep code quality pass. Removed 6 genuinely dead production code items, 2 deprecated symbols with zero callers, and fixed a long-standing flaky test. Result: zero test failures across the full workspace for the first time.

## Changes

### Dead Production Code Removed (6 items)

| Item | File | Reason |
|------|------|--------|
| `HsmSource` enum | `beardog-security/.../entropy_orchestrator/types.rs` | Orphaned duplicate of orchestrator's own `HsmSource` enum |
| `DeployConfig` struct | `beardog-deploy/src/main.rs` | Unused placeholder, never constructed |
| `probe_service_endpoint` method | `beardog-core/.../ecosystem_integration.rs` | Unused helper, never called |
| `genetics` field | `beardog-core/src/primal_sovereignty.rs` | Constructed in `new()` but never read |
| `crypto_config` field | `beardog-core/src/primal_sovereignty.rs` | Constructed in `new()` but never read |
| `hierarchy_manager` field | `beardog-core/src/primal_sovereignty.rs` | Constructed in `new()` but never read |

### Deprecated Symbols Removed (2 items)

| Symbol | Location | Callers |
|--------|----------|---------|
| `BearDogResult<T>` type alias | `beardog-errors/src/lib.rs` + root `src/lib.rs` | Zero production callers |
| `PrimalTypeMigrationHelper` struct | `beardog-core/.../primal_types/io.rs` | Zero non-test callers |

### Flaky Test Fixed

`test_handle_key_export_roundtrip_uses_default_home_env` in `beardog-cli` was intermittently failing because the `HOME` mutex was acquired and released in tiny scopes while `handle_key_export` and `handle_key_import` ran outside the lock. Concurrent tests corrupted the `process_env` overlay.

Fix: hold the lock for the entire test duration + add `#[serial_test::serial]`. Same fix applied to `test_handle_key_export_errors_when_home_unset` and `test_handle_key_import_errors_when_home_unset`.

### Additional Cleanup

- `SovereigntyConfig` type alias inlined to `PrimalSovereigntyConfig` (alias removed)
- Unused `debug` import removed from `ecosystem_integration.rs`
- 2 `doc_markdown` clippy warnings fixed in BTSP negotiation handler

## CI Results

- `cargo check --workspace`: clean, zero warnings
- `cargo fmt --check`: clean
- `cargo clippy --workspace`: clean
- `cargo test --workspace`: **14,800+ passed, 0 failed** (zero failures for the first time)

## Remaining `#[expect(dead_code)]` in Production

11 instances remain in 3 files — all are reserved scaffolding for future features:
- `ultimate_performance.rs` (4) — SIMD/queue optimization types
- `performance_optimizer.rs` (6) — ecosystem capability pool/cache fields
- `fido2/multi_credential_provider/mod.rs` (1) — stored FIDO2 config for CTAP2
