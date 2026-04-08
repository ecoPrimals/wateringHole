# NestGate v4.7.0 — Deep Debt: Silent Failures, Overstep, Smart Refactor

**Date**: April 4, 2026
**Commit**: 2956dc6f
**Tests**: 11,685 passing, 0 failures, 463 ignored
**Clippy**: CLEAN (`-D warnings`)

---

## Changes

### Overstep Shedding
- `nestgate-network` removed from workspace. Deprecated since 4.7.0 with zero dependents. Code retained on disk as fossil record per policy.

### Silent Failure → Proper Error Propagation (Production Safety)

Previously, multiple ZFS operations returned `Ok(vec![])` or `Ok(HashMap::new())` when external commands failed — silently swallowing permission errors, missing binaries, and corrupted pools.

**Fixed:**
- `nestgate-zfs::dataset::list_datasets` — returns `Err` with stderr on `zfs list` failure
- `nestgate-zfs::dataset::get_dataset_properties` — returns `Err` with details + actual error (was "actual_error_details" placeholder)
- `nestgate-zfs::pool_helpers::get_pool_properties` — returns `Err` with stderr (was "error details" placeholder)
- `nestgate-api` remote ZFS implementation — 10 instances of `Ok(empty)` on JSON parse/missing-key → proper `Err` with serde/context details
- `nestgate-api` metrics collector — differentiates "zpool not found" (debug, empty OK) from "zpool returned error" (warn, empty OK)

### Smart Refactoring
- Extracted 500 lines of tests from `compliance/manager.rs` to `manager_tests.rs` using `#[path]` pattern (741 → 240 lines; 30 tests preserved, all passing)

### Audit Findings (Confirmed Clean)
| Area | Status |
|------|--------|
| External C/C++ deps | Zero in normal tree (only `cc` via fuzz/libfuzzer-sys) |
| Unsafe code | ZERO `unsafe` blocks; all 22 crate roots `#![forbid(unsafe_code)]` |
| Dev stubs | Properly gated: `cfg(test)` + `dev-stubs` feature (not default) |
| TODO/FIXME/HACK markers | Zero in crate sources |
| Production mocks | Concentrated in `dev_stubs/` (gated), `mock_builders` (gated), not in release builds |

---

## Remaining Debt (ordered by impact)
1. **Remote ZFS implementation** (714 lines): large but well-scoped trait impl; mechanical repetition
2. **`handler_config.rs`** (709 lines): config schema + defaults; tests embedded
3. **`performance_engine/engine.rs`** (748 lines): could extract bottleneck analysis submodule
4. **Metrics collector stubs** (`collector.rs`): "not implemented" for time-series/aggregation — awaiting TSDB
5. **Temporal storage device stubs**: "FUTURE" placeholders for device enumeration
