# NestGate v4.7.0-dev — Session 43d Deep Debt Evolution & Debris Cleanup

**Date**: April 12, 2026  
**Primal**: NestGate (storage & discovery)  
**Session**: 43d (continuation of Session 43 compliance audit)

---

## Summary

Full-spectrum deep debt evolution pass: dangerous `as` casts, large file refactors,
clone optimization, dead code elimination (36 unwired files / 12,971 lines), `#[serial]`
elimination, installer tracing migration, and comprehensive audit verification.

## Changes Delivered

### Safety: Dangerous `as` Cast Evolution (10 files)

| File | Cast | Fix |
|------|------|-----|
| `response_builder.rs` | `total as f64 / ... .ceil() as u32` | `div_ceil` + `u32::try_from` |
| `dataset_handlers.rs` | `((page-1)*per_page) as usize` | `saturating_mul` + `usize::try_from` |
| `storage.rs` | Same pagination pattern | Same fix |
| `crud_helpers.rs` | `count as u32` | `u32::try_from(...).unwrap_or(u32::MAX)` |
| `health.rs` | `snapshots.len() as u32` | `u32::try_from` |
| `production.rs` | `connections.len() as u32` | `u32::try_from` |
| `metrics.rs` | `engines.len() as u32` | `u32::try_from` |
| `system.rs` | `engines.len() as u32` | `u32::try_from` |
| `helpers.rs` | `snapshot_count as u32` | `u32::try_from` |
| `tier_evaluation.rs` | `f64 as u32` | `.clamp(0.0, f64::from(u32::MAX))` |

### Structure: Smart File Refactors (2 files → 6 modules)

| Before | After | Strategy |
|--------|-------|----------|
| `metadata_backend.rs` (781 lines) | `mod.rs` (264) + `file_backend.rs` (154) + `tests.rs` (378) | Extract FileMetadataBackend + test module |
| `primal_self_knowledge.rs` (728 lines) | `mod.rs` (173) + `types.rs` (134) + `knowledge.rs` (439) | Extract types + core knowledge impl |

### Performance: Clone Hotspot Optimization (pool_setup)

- 3 enums evolved to `Copy` (`DeviceType`, `SpeedClass`, `ConfigDeviceType`)
- Index-based sort replaces `Vec<&StorageDevice>` clone
- Tier mapping uses `copied()` iteration
- 12 `.clone()` call sites eliminated

### Hygiene: Dead Code Elimination

- **36 unwired `.rs` files deleted** (12,971 lines) across 8 crates
- **2 empty directories removed** (`nestgate-zfs/data/`, `nestgate-zfs/config/`)
- Files had no `mod` declaration — confirmed never compiled

### Test Infrastructure

- Last 2 `#[serial]` tests → `temp_env::with_vars`; `serial_test` dep removed from `nestgate-config`
- `nestgate-installer` println! → `tracing::info!`/`warn!` (wizard stdout retained, documented)
- `#[allow(deprecated)]` in `service.rs` → `#[allow(deprecated, reason = "...")]` with migration path

### Audit Findings (verified clean)

| Check | Result |
|-------|--------|
| Production `unwrap()`/`expect()` | **ZERO** — all 2084 hits are in `#[cfg(test)]` modules |
| `dev-stubs` feature leakage | **CLEAN** — never in default features, properly `#[cfg]`-gated |
| Hardcoded ports/URLs in production | **CLEAN** — all in test code |
| `production_placeholders.rs` | **Real impl** — calls `nestgate_zfs` directly (name misleading, code functional) |

## Verification

```
cargo fmt --all --check       PASS
cargo clippy --workspace      PASS (zero warnings, -D warnings)
cargo doc --workspace         PASS (zero warnings)
cargo test --workspace        PASS (11,794 passing, 0 failures, 451 ignored)
```

## Metrics Delta

| Metric | Before | After |
|--------|--------|-------|
| Tests passing | 11,792 | 11,794 |
| Dead unwired files | 36 | 0 |
| Dead lines | +12,971 | 0 |
| `#[serial]` tests | 2 | 0 |
| Dangerous `as` casts | ~10 hot-path | 0 |
| Largest module (production) | 781 LOC | 439 LOC |

## Remaining Debt

| Item | Priority | Notes |
|------|----------|-------|
| Coverage 81.7% → 90% | P1 | Multi-session effort |
| 202 deprecated APIs | P2 | All have callers; canonical-config migration |
| ~336 widening `as` casts | P3 | Safe (u32→u64 etc); not a risk |
| Dual `rustix` versions | P3 | 0.38.x + 1.1.x; unify when tempfile aligns |
| Round-named test files | P3 | 10 files; wired from lib.rs, naming only |

## Proposed Compliance Matrix Updates

NestGate row in `ECOSYSTEM_COMPLIANCE_MATRIX.md`:

- **Dead code**: `PASS` → verified zero unwired modules (36 orphans removed)
- **File size**: `PASS` → all modules under 500 LOC (was 750)
- **`#[serial]`**: `PASS` → zero remaining
- **`as` casts**: `PASS` → all dangerous narrowing evolved
