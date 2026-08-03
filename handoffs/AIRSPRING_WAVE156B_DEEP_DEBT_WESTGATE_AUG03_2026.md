# airSpring Wave 156b — Deep Debt Resolution + Workspace Consolidation

**Date**: Aug 3, 2026
**Gate**: westGate (Data NAS)
**Wave**: 156b
**Primal**: airSpring
**Commit**: pending (cascade push)

---

## Summary

Full deep-debt resolution session on airSpring. Workspace consolidated to root
`Cargo.toml` (WORKSPACE_DEPENDENCY_STANDARD), all production stubs evolved to
pure-Rust, hardcoded primal names eliminated, GPU test patterns centralized,
large files refactored, docs updated for westGate deployment context.

## Deep Debt Completed

### Workspace Consolidation

Created root `Cargo.toml` defining 5-member workspace:
- `barracuda` (main science library)
- `metalForge/forge` (dispatch/routing)
- `experiments/exp001_local_science_parity`
- `experiments/exp002_composition_parity`
- `experiments/exp003_foundation_target_validation`

Shared `[workspace.dependencies]` (16 deps), `[workspace.package]`, and
`[workspace.lints.clippy]` — all member `Cargo.toml` files reference workspace.
Single `Cargo.lock` at root.

### Stub Evolution — Pure-Rust Fitting

`barracuda/src/eco/correction.rs` had `cfg(not(feature = "local"))` stubs
returning `None` for curve fitting. All 5 replaced with pure-Rust implementations:
- `fit_linear` — normal equations (OLS)
- `fit_quadratic` — Cramer's rule 3×3
- `fit_exponential` — log-transformed OLS
- `fit_logarithmic` — log-domain OLS
- `fit_ridge` — Tikhonov regularization (normal equations)

No feature gates remain on any math function. 17/17 correction tests pass.

### Hardcoding Elimination

| Location | Change |
|----------|--------|
| `ipc/provenance.rs` | `"rhizoCrypt"` etc. → `primal_names::RHIZOCRYPT` |
| `bin/validate_gate_composition.rs` | `find_socket("airspring")` → `PRIMAL_NAME` |
| `data/open_meteo.rs` | Removed stale "ureq fallback" doc refs |
| `metalForge/forge/neural.rs` | `"biomeos"` → `BIOMEOS_SOCKET_SUBDIR` const |
| `data/provider.rs` | `"primal"` → `SOCKET_DIR_SEGMENT` const |

### GPU Test Centralization

Added `gpu_or_skip!` macro in `testutil/mod.rs`. Replaced 52/60 inline
`eprintln!("SKIP: ...")` blocks across 23 GPU test modules with the macro.
8 remaining are intentional special-case skips (shader panics, driver quirks).

### File Size Compliance

| File | Before | After | Method |
|------|--------|-------|--------|
| `eco/richards.rs` | 826L | 796L | Helper extraction (`picard_iterate`, Thomas algorithm) |
| `nucleus.rs` | 829L | 272+612L | Split to `nucleus/mod.rs` + `nucleus/mesh.rs` |

Zero files over 800L target.

### Unsafe Review

`EnvGuard` in `testutil/env_guard.rs` uses `unsafe` for `env::set_var`/`remove_var`
(Rust 2024). Confirmed correct: test-only, `#[serial]`, RAII guard, production
builds have `#![forbid(unsafe_code)]`. No changes needed.

## Metrics

| Metric | Value |
|--------|-------|
| Lib tests (barracuda) | **1,089 passed** |
| Forge tests | **68 passed** |
| Total | **1,157** |
| Clippy | **0 warnings** (pedantic + nursery) |
| Fmt | **Clean** |
| Rustdoc | **0 warnings** |
| Line coverage | **84.30%** |
| Function coverage | **87.83%** |
| Files >800L | **0** |
| TODOs in production | **0** |
| Stubs in production | **0** |
| Hardcoded primals | **0** |
| Unsafe in production | **0** |

## For Upstream

- **overwatch**: Coverage at 84.30% (below 90% target) — GPU test skips on
  headless/CI reduce coverage. CPU-only coverage is higher. Upstream guidance
  requested on CI GPU strategy (eastGate runner vs. coverage exemptions).
- **barraCuda**: `gpu_or_skip!` pattern could be adopted upstream for consistent
  GPU test skipping ecosystem-wide.
- **primalSpring**: `WORKSPACE_DEPENDENCY_STANDARD` applied — airSpring can serve
  as reference implementation for other primals migrating to workspace roots.
- **biomeOS**: westGate deployment blocked on executor ops (executor binary
  shipped, needs systemd/ops wiring). No code gaps on airSpring side.

## Gaps for Upstream Teams

| Gap | Owner | Status |
|-----|-------|--------|
| biomeOS live deploy on westGate | biomeOS team | Executor shipped, needs ops |
| CI GPU runner for coverage | overwatch | Discuss at next sync |
| tarpc optional transport | primalSpring | wateringHole standard, not yet prioritized |
| ecoBin compliance audit | overwatch | 98 binaries, UniBin pattern in place |
