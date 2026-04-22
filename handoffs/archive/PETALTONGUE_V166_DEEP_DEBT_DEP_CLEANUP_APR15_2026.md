# petalTongue — Deep Debt Audit & Dependency Cleanup

**Date**: April 15, 2026
**Sprint**: petalTongue v1.6.6 (continued)
**Trigger**: Comprehensive deep debt pass — dependencies, hardcoding, unsafe, mocks, large files

---

## Full Audit Results

| Dimension | Status | Details |
|-----------|--------|---------|
| **Files >800 LOC** | CLEAN | Largest: 637 (test file). No production file exceeds 600 LOC |
| **Unsafe code** | CLEAN | Zero `unsafe` blocks. All 18 crates enforce `#![forbid(unsafe_code)]` |
| **Hardcoded values** | CLEAN | All network constants env-overridable. Socket discovery uses XDG + `/tmp` fallback (standard Unix) |
| **Mocks in production** | CLEAN | All mocks gated `#[cfg(test)]` or `#[cfg(feature = "mock")]` |
| **`dyn` usage** | CLEAN | Only `Box<dyn Fn…>` callbacks and `&dyn Error` — both idiomatic |
| **TODO/FIXME/HACK** | CLEAN | Zero markers in any `.rs` file |
| **`async-trait`** | CLEAN | Zero first-party usage. Transitive only via tarpc → opentelemetry_sdk |
| **`reqwest` / `ring`** | CLEAN | Not in any Cargo.toml or Cargo.lock |

## Changes Made

### Headless egui leak (architectural fix)

`petal-tongue-headless` pulled the entire egui/eframe/glow stack through two paths:

1. **Direct**: `petal-tongue-graph` dep with default features → `egui-render` → egui/egui_extras/egui_plot
2. **Indirect**: `petal-tongue-ui-core` dep → `petal-tongue-graph` (default features) → same egui stack

**Fix**:
- `petal-tongue-headless/Cargo.toml`: `default-features = false` on `petal-tongue-graph`
- `petal-tongue-ui-core/Cargo.toml`: removed `petal-tongue-graph` entirely (dead dependency — never imported in source, only mentioned in doc comments)

**Result**: `cargo tree -p petal-tongue-headless -i egui` → "did not match any packages"

### tarpc feature trimming

Changed from `features = ["full"]` to explicit:
`["serde1", "tokio1", "serde-transport", "serde-transport-bincode", "tcp", "unix"]`

Drops `serde-transport-json` (unused — tarpc client uses Bincode codec).

**Note**: `opentelemetry` 0.18 + `async-trait` are hard dependencies of tarpc 0.34 core, not feature-gated. Cannot be trimmed without replacing tarpc.

### Minor cleanup

- `petal-tongue-wasm/Cargo.toml`: removed duplicate `serde_json` in `[dev-dependencies]` (already in `[dependencies]`)

## Verification

| Target | clippy | Tests | Cross-check |
|--------|--------|-------|-------------|
| x86_64-unknown-linux-gnu | 0 warnings | 6,144 pass | — |
| x86_64-apple-darwin | — | — | 0 errors, 0 warnings |
| aarch64-apple-darwin | — | — | 0 errors, 0 warnings |

## Files Changed

- `Cargo.toml` (workspace root — tarpc features)
- `crates/petal-tongue-headless/Cargo.toml` (graph default-features = false)
- `crates/petal-tongue-ui-core/Cargo.toml` (removed dead graph dep)
- `crates/petal-tongue-wasm/Cargo.toml` (removed dup dev-dep)
