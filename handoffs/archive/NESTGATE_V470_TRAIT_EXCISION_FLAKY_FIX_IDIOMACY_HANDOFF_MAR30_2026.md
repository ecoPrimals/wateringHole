# NestGate v4.7.0-dev — Deprecated Trait Excision, Flaky Test Fix & Idiomacy Evolution

**Date**: March 30, 2026  
**Primal**: nestgate (storage & discovery)  
**Session type**: Deep debt execution — deprecated trait excision, flaky test stabilization, hardcoding evolution, allow-block reduction, dependency cleanup

---

## What Was Done

### Deprecated Trait Excision (~2,300 lines removed)

Three parallel trait systems (`deprecated`, `canonical_hierarchy`, `canonical`) had evolved into closed dependency cycles with zero production consumers. Analysis proved the `deprecated` and `canonical_hierarchy` layers were orphaned — only the `canonical/` traits are consumed by production code.

| Deleted | Lines | Reason |
|---------|-------|--------|
| `canonical_provider_unification.rs` | 798 | Deprecated re-exports; all consumers migrated to `canonical/` |
| `security_migration.rs` | 558 | Adapter layer with no callers |
| `security_migration_tests.rs` | 553 | Tests for deleted adapters |
| `canonical_hierarchy/` (7 files) | ~400 | Duplicate hierarchy — canonical/ is the real one |
| `migration/` (7 files) | ~500 | Storage migration adapters with no consumers |
| `traits/mod.rs` cleanup | ~80 | Removed stale module declarations, migration comments |

Zero production behavior change. All `#[deprecated]` notes in surviving files updated to reference `canonical::CanonicalSecurity` instead of deleted modules.

### Clippy Zero (6 warnings → 0)

- Unused import in `capability_resolver/tests.rs`
- `map_or` → `is_none_or` simplification
- `.err().expect()` → `.expect_err()` (2 instances)
- Strict `f64` comparison → epsilon-based in `diagnostics/metrics.rs`
- Double-nested `mod tests` in `capability_resolver/tests.rs`
- Redundant `.clone()` in `universal_zfs_types/errors.rs`

### Flaky Test Evolution (env race conditions → isolated)

Replaced raw `std::env::set_var`/`remove_var` with `temp_env::with_var` + `#[serial_test::serial]` across 8 test functions in 5 files:

| File | Tests fixed |
|------|-------------|
| `fault_injection_tests.rs` | `test_fault_conflicting_config` (was leaking `NESTGATE_HTTP_PORT="not_a_number"`) |
| `config/runtime/test_support.rs` | `test_config_guard_isolation`, `test_concurrent_config_isolation`, `test_config_from_env` |
| `config/agnostic_config.rs` | `test_config_builder_with_environment` |
| `constants/capability_port_discovery.rs` | `test_sync_discovery_invalid_env`, `test_async_discovery_fallback` |
| `config/environment_error_tests.rs` | `test_config_clone_independence` |
| `defaults.rs` | 5 port default tests |

### Hardcoded Primal Names → Self-Knowledge Constant

Replaced `"nestgate"` string literals with `DEFAULT_SERVICE_NAME` in 8 production files:

- `nestgate-rpc`: unix_socket_server health responses (3 methods), isomorphic_ipc responses (2 fields), model_cache_handlers (2 methods)
- `nestgate-core`: self_knowledge metadata
- `nestgate-security`: JWT issuer field
- `nestgate-observe`: tracing config service_name

### Allow-Block Reduction

- **nestgate-api**: 67 crate-level allows → 31 (22 production + 16 test-only via `cfg_attr`)
- **nestgate-core**: Nuclear `#![allow(clippy::all, clippy::pedantic, clippy::nursery, clippy::restriction)]` in test cfg → 12 targeted test-only lints

### Dependency Cleanup

Removed 4 orphaned workspace dependencies from root `Cargo.toml`:
- `gethostname` (replaced by `rustix::system::uname`)
- `ipnetwork` (unused)
- `tungstenite` + `tokio-tungstenite` (unused)

### Debris Cleanup

- Removed 2 empty directories: `nestgate-zfs/{data,config}`
- Removed dead `capability_auth` compat module + `SecurityModularizationComplete` marker
- Removed 4 stale `TEMP_DISABLED` comments

---

## Current Measured State

```
Build:       25/25 workspace members, 0 errors
Clippy:      ZERO production warnings (--all-targets)
Format:      CLEAN (cargo fmt --check)
Tests:       All lib tests passing, 0 failures
Docs:        ZERO warnings (cargo doc --workspace --no-deps)
Coverage:    ~80% line (llvm-cov)
Prod files:  ALL under 800 lines
Traits:      Single canonical hierarchy (canonical/); deprecated layers excised
Flaky tests: ZERO env-polluting tests remaining
```

---

## Remaining Debt (Prioritized)

| Priority | Item | Status |
|----------|------|--------|
| P1 | Coverage to 90% (~10pp gap) | ~80% — wateringHole minimum met |
| P2 | Wire `data.*` and `nat.*` semantic routes | Pending |
| P3 | `#[allow(dead_code)]` reduction (~95 remaining) | Incremental |
| P3 | Remaining production `placeholder` text in non-response code | ~45 files |
| P4 | Multi-filesystem substrate testing | Infra-dependent |
| P4 | Cross-gate replication | Design phase |
| P4 | Config template consolidation (15 production*.toml variants) | Consolidate to 1 canonical |

---

## Artifacts

- **Handoff**: This file
- **Changelog**: `primals/nestgate/CHANGELOG.md` Session 10
- **Status**: `primals/nestgate/STATUS.md`
- **Coverage**: `cargo llvm-cov --workspace --lib --summary-only`
- **Fossil record**: `wateringHole/fossilRecord/nestgate/`
