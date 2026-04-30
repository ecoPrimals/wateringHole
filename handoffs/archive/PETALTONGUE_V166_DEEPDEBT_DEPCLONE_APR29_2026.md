# petalTongue v1.6.6 — Deep Debt: Dependency Consolidation + Clone Elimination

**Date**: April 29, 2026  
**Scope**: Workspace dependency consolidation, hardcoded value extraction, hot-path clone elimination  
**Tests**: 6,054+ passing (98 suites), 0 failures, 0 Clippy warnings

---

## 1. Dependency Consolidation (6 crates → workspace)

**Problem**: `axum`, `tower-http`, `tower`, `tokio-stream` used literal version
pins in the root `Cargo.toml` `[dependencies]` instead of workspace references.
`aes-gcm` and `zeroize` in `petal-tongue-entropy` were also local pins.

**Fix**: All 6 crates added to `[workspace.dependencies]` with version + features.
Package-level `[dependencies]` now use `{ workspace = true }`.

| Crate | Version | Features | Used by |
|-------|---------|----------|---------|
| `axum` | 0.7 | `tokio` | root binary (web mode) |
| `tower-http` | 0.5 | `fs`, `trace` | root binary (web mode) |
| `tower` | 0.4 | `util` | root binary (web mode) |
| `tokio-stream` | 0.1 | `sync` | root binary (web mode) |
| `aes-gcm` | 0.10 | — | petal-tongue-entropy |
| `zeroize` | 1 | `derive` | petal-tongue-entropy |

**Files**: `Cargo.toml`, `crates/petal-tongue-entropy/Cargo.toml`

---

## 2. Hardcoded Value Extraction

| Value | Before | After | File |
|-------|--------|-------|------|
| `/var/run/ecoPrimals` | Inline string literal | `constants::ALTERNATIVE_RUN_DIR` | `unix_socket_provider.rs` |
| `"nucleus"` primal type | Inline `== "nucleus"` | `capability_names::primal_types::NUCLEUS` | `dynamic_scenario_provider.rs`, `scenario_provider.rs` |
| `10` (staleness secs) | Magic number in UI panel | `constants::PROPRIOCEPTION_STALENESS_SECS` | `proprioception_panel.rs` |

**New constants**:
- `petal_tongue_core::constants::ALTERNATIVE_RUN_DIR` — alternative socket search path
- `petal_tongue_core::constants::PROPRIOCEPTION_STALENESS_SECS` — UI staleness threshold
- `petal_tongue_core::capability_names::primal_types::NUCLEUS` — coordinator type for topology

---

## 3. Hot-Path Clone Elimination

### Texture upload/attach (`visualization/mod.rs`)

**Before**: `serde_json::from_value(req.params.clone())` duplicated the entire JSON
payload (potentially megabytes for texture data) before deserialization.

**After**: `let id = req.id; serde_json::from_value(req.params)` — takes ownership
of `req.params` directly. All error-path `id` references use Rust's flow-sensitive
ownership (early returns move `id`; non-returning paths keep it alive). Zero `.clone()`.

### Sparkline renderer (`metrics_dashboard/render.rs`)

Removed redundant nested `if points.len() >= 2` check (identical to outer guard).
The `points.clone()` for line vs. area shapes remains (egui `Shape::line` requires
ownership) but the code is streamlined.

---

## Comprehensive Audit Summary

| Dimension | Status |
|-----------|--------|
| `unsafe` code | Zero (18 doc-comment mentions only) |
| `dyn` in production | Zero (all hits in doc comments) |
| `#[allow(]` in production | Zero (all in test modules or justified `#[expect]`) |
| TODO/FIXME/HACK | Zero in all `.rs` and `.md` files |
| Mocks in production | Zero (gated behind `#[cfg(test)]` or `feature = "mock"`) |
| Largest file | 710 LOC (`visualization/mod.rs`) |
| Dependency version skew | Zero (all 6 remaining holdouts consolidated) |
| Stale features | `examples` feature has no `cfg` but is used in `required-features` (acceptable) |

---

## Verification

- **Clippy**: 0 warnings (`--all-targets -- -D warnings`)
- **Tests**: 6,054+ passing (98 suites), 0 failures
- **Build**: Clean on all targets
