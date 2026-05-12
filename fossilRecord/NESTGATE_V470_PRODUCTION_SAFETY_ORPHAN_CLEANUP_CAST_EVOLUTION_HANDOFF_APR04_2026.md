# NestGate v4.7.0-dev — Production Safety, Orphan Cleanup & Cast Evolution

**Date**: April 4, 2026  
**Primal**: NestGate (Storage / Permanence)  
**Session**: 23  
**Trigger**: Deep debt execution — production mocks, orphan files, unsafe casts  

---

## Critical Fix — ProductionZfsService Silent Success

`ProductionZfsService::create_snapshot()`, `clone_dataset()`, and `bulk_create_snapshots()`
were returning **`Ok(...)` with synthetic metadata** without performing any ZFS operations.
A caller would believe a snapshot was created when no `zfs snapshot` was ever executed.

**Fix**: All three now return `Err(InvalidInput)` with a message directing callers to
native ZFS CLI or the ZFS REST API. This is the same pattern used by `destroy_snapshot`,
`create_pool`, `destroy_pool`, `create_dataset`, and `destroy_dataset`.

---

## Orphan File Deletion (26 files, 10,208 lines)

Module-tree audit found `.rs` files on disk that were never declared via `mod` in any
parent module. They were never compiled by `rustc`.

| Directory | Files | Lines |
|-----------|-------|-------|
| `hardware_tuning/` | 5 (incl. stub_helpers.rs) | 2,392 |
| `workspace_management/` | 3 | 1,076 |
| `compliance/` | 1 | 187 |
| `zfs/universal_zfs/backends/native/` | 3 | 1,293 |
| `handlers/` top-level | 6 | 2,173 |
| `load_testing/` | 4 | 1,894 |
| `performance_dashboard/` | 1 | 325 |
| `fail_safe/` | 2 | 925 |
| `nestgate-zfs performance_engine/` | 1 | 353 |
| **Total** | **26** | **10,208** |

---

## DevelopmentZfsService Gating

`DevelopmentZfsService` (fast mock ZFS, no real `zpool`/`zfs` calls) was always compiled
in production builds. Now gated behind `#[cfg(any(test, feature = "dev-stubs"))]`:
- Struct, Default impl, and trait impl all gated
- Re-export and constructor function gated in `mod.rs`
- Zero production consumers existed — only test code used it

---

## `as u32` Cast Evolution (12 locations)

All narrowing `as u32` casts in production code replaced with safe alternatives:

| Pattern | Replacement |
|---------|-------------|
| `.len() as u32` / `.count() as u32` | `u32::try_from(...).unwrap_or(u32::MAX)` |
| `(float) as u32` (pagination) | `u64::div_ceil()` + `u32::try_from` |
| `f64 as u32` (access_frequency) | NaN/negative guard + explicit `#[allow]` |
| `logical_cpu_count() as u32` | `u32::try_from(...).unwrap_or(4)` |

---

## Storage Probe Naming Fix

`collect_real_storage_datasets()` was setting all dataset names to the literal
string `"localself.base_url"` — a copy-paste artifact. Fixed to derive names
from the actual directory path (e.g. `"local/home"`, `"local/var"`).

---

## Verification

```
cargo fmt --all -- --check    → PASS
cargo clippy --workspace --all-features -- -D warnings → PASS
cargo test --workspace        → 12,236 passed, 0 failed, 471 ignored
```

1 known flaky test (`build_succeeds_with_ports_only_endpoints_empty_without_endpoint_sources`)
passes on retry — env-dependent race condition, not related to these changes.

---

## Remaining Deep Debt (diminishing returns)

| Category | Status |
|----------|--------|
| `#[allow(deprecated)]` suppressions | Active config migration — expected |
| `as f64` ratio casts | Safe widening — no truncation risk |
| `as i32` for `.powi()` retry attempts | Bounded by retry count — no practical overflow |
| `.as_ptr() as usize` SIMD alignment | Intentional pointer arithmetic — documented |
| `dev-stubs` feature tree | Properly gated |
| `mock-metrics` feature | Properly gated |
