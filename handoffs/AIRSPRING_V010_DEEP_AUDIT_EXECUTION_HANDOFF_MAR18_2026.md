# airSpring V0.10.0 — Deep Audit Execution Handoff

**Date:** 2026-03-18
**From:** airSpring V0.10.0
**To:** ecoPrimals ecosystem
**License:** AGPL-3.0-or-later
**Covers:** Deep audit execution, provenance expansion, OrExit migration, tolerance centralization, Rust 2024 lint evolution, smart refactors
**Supersedes:** AIRSPRING_V090_AUDIT_EXECUTION_HANDOFF_MAR18_2026.md, AIRSPRING_V010_CROSS_ECOSYSTEM_ABSORPTION_HANDOFF_MAR18_2026.md

---

## Executive Summary

airSpring v0.10.0 completes a comprehensive deep audit and execution pass,
resolving all identified technical debt. Key achievements:

- **Provenance**: 11→63 Python baseline records (every CI validation binary traced)
- **Safety**: OrExit zero-panic across all 91 validation binaries (~180 call sites)
- **Tolerances**: All hardcoded thresholds centralized to named `Tolerance` constants
- **Refactoring**: `data/provider.rs` (781→4 modules), `gpu/evolution_gaps.rs` (→resolved_issues.rs)
- **Rust 2024**: `#[allow]`→`#[expect]` migration complete
- **Quality**: 908 lib + 299 integration + 61 forge, 0 clippy, 0 unsafe, 0 C deps

---

## 1. Provenance Registry Expansion (11→63 Baselines)

`barracuda/src/provenance.rs` now contains 63 `PythonBaseline` entries covering
every CI validation binary. Each record includes:

- `binary`: validation binary name
- `script`: Python control script path
- `commit`: short hash of the Python baseline run
- `date`: ISO date of baseline generation
- `category`: `PythonParity | GpuParity | Analytical | Published`

14 new commit epoch constants added. Test assertion: `python_baselines().len() >= 60`.

**Cross-spring pattern:** wetSpring uses identical `PythonBaseline` struct. Upstream
absorption candidate for `barracuda::validation::provenance`.

---

## 2. OrExit Zero-Panic Migration

All 91 validation binaries migrated from `.expect()`/`.unwrap()` to the `OrExit`
pattern (`eprintln!` + `exit(1)`). ~180 call sites converted across 25+ binaries.

Top files by conversion count:

| Binary | Conversions |
|--------|:-----------:|
| `cross_validate.rs` | 24 |
| `validate_gpu_live.rs` | 30 |
| `validate_et0.rs` | 21 |
| `validate_yield.rs` | 17 |
| `validate_nass_yield.rs` | 17 |
| `validate_cover_crop.rs` | 14 |
| `validate_anderson.rs` | 14 |

`.unwrap_or()`, `.unwrap_or_else()`, `.unwrap_or_default()` left untouched (safe fallbacks).

**metalForge binaries** include local `OrExit` trait (can't import from `airspring_barracuda`).

---

## 3. Tolerance Centralization

All hardcoded numeric thresholds in validation binaries replaced with named
`Tolerance` constants from `airspring_barracuda::tolerances`:

| Binary | Before | After |
|--------|--------|-------|
| `validate_lysimeter` | `0.80` | `IA_CRITERION.abs_tol` |
| `validate_lysimeter` | `1.0` | `RMSE_MAXIMUM.abs_tol` |
| `validate_atlas` | `0.85` | `R2_MINIMUM.abs_tol` |
| `validate_richards` | `0.01` | `SOIL_HYDRAULIC.abs_tol` |
| `validate_diversity` | `0.01` | `BIO_DIVERSITY_SHANNON.abs_tol` |

---

## 4. Smart Module Refactoring

| Module | Before | After | Strategy |
|--------|--------|-------|----------|
| `data/provider.rs` | 781 LOC | 4 modules (provider + songbird + biomeos + nestgate) | Extracted 3 provider impls to submodules, kept trait + shared helpers |
| `gpu/evolution_gaps.rs` | 731 LOC | 635 + resolved_issues.rs (~100) | Extracted historical BarraCuda issues + types |

Public API unchanged — backward-compatible re-exports.

---

## 5. Patterns for Cross-Spring Adoption

### 5a. `deny.toml` C-Dependency Ban (14 crates)
Enforces zero C deps at build time. Template available for all springs.

### 5b. `#[expect(reason)]` vs `#[allow(reason)]`
`#[expect]` for known-to-fire lints (compile error if unfulfilled).
`#[allow]` for blanket test module suppressions.

### 5c. Determinism Contract Documentation
Nautilus brain is structurally deterministic. No RNG seed needed. Document
this pattern for springs using bingoCube/nautilus.

### 5d. Data Provenance Accession IDs
All data sources carry formal identifiers (ECMWF CDS, SCAN, AmeriFlux DOI,
NASS API, SRA BioProject, NOAA GHCND).

---

## 6. Test Results

| Metric | Value |
|--------|-------|
| Library tests | 908 |
| Integration tests | 299 |
| Forge tests | 61 |
| Property tests | 22 |
| Validation binaries | 91 (all zero-panic) |
| Python baselines | 63 (all with provenance) |
| Named tolerances | 63 (4 submodules) |
| Clippy warnings | 0 (pedantic + nursery) |
| Unsafe code | 0 |
| C dependencies | 0 |
| TODO/FIXME/HACK | 0 |
