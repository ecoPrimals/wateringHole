# petalTongue v1.6.7 — Native `async fn` in Traits + Deep Debt Audit

**Date:** April 25, 2026
**Scope:** Trait modernization, lint hygiene, comprehensive debt audit
**Status:** Complete — zero warnings, 98 test suites passing

---

## Problem

13 production modules used manual `fn -> impl Future<Output = T> + Send`
desugaring for async trait methods, requiring `#![allow(clippy::manual_async_fn)]`
suppressions throughout. This was a holdover from pre-RPITIT Rust when trait
methods needed explicit future return types for `Send` bounds. Since all `dyn`
trait objects were already eliminated in favor of enum dispatch, the explicit
`+ Send` bound was no longer needed at the trait level.

## Solution

Converted all manual async desugaring to native `async fn` in traits (RPITIT):

**Traits converted:** `ComputeProvider`, `GUIModality`, `Sensor`,
`DiscoveryBackend`, `PrimalLifecycle`, `PrimalHealth`, `AudioBackend`,
`DisplayBackend`, `UIBackend`, `VisualizationDataProvider`

**Side fix:** `render_multi` in `engine.rs` simplified from `tokio::spawn` to
sequential awaits — the old spawned tasks contended on the same write lock and
could never run in parallel anyway.

## Comprehensive Audit Results

| Category | Result |
|----------|--------|
| Files >800 LOC | **0** (max: 637, test file) |
| `unsafe` blocks/fns | **0** (workspace: `unsafe_code = "forbid"`) |
| TODO/FIXME/HACK/XXX | **0** |
| `#[allow(` in production | **0** (all in `#[cfg(test)]` modules) |
| `dyn` in production types | **4** (2 callback closures, 2 `&dyn Error` — idiomatic) |
| External C/FFI deps | **0** direct (`openssl`, `reqwest`, `ring`, `native-tls`, `cc`: none) |
| Clippy warnings | **0** (pedantic + nursery) |
| Production `unwrap()` | **0** (`unwrap_used = "deny"`) |
| macOS cross-arch | **Pass** (x86_64-apple-darwin) |

## Files Changed

21 files, net −100 lines:

- `Cargo.toml` — workspace lint for `async_fn_in_trait`
- `crates/petal-tongue-core/src/compute.rs` — `ComputeProvider` trait + impl
- `crates/petal-tongue-core/src/modality.rs` — `GUIModality` trait + impl
- `crates/petal-tongue-core/src/sensor/types.rs` — `Sensor` trait
- `crates/petal-tongue-core/src/capability_discovery.rs` — `DiscoveryBackend`
- `crates/petal-tongue-core/src/lifecycle.rs` — `PrimalLifecycle`, `PrimalHealth`
- `crates/petal-tongue-core/src/gpu_compute_provider.rs` — enum dispatch impl
- `crates/petal-tongue-core/src/biomeos_discovery/backend.rs` — impl
- `crates/petal-tongue-core/src/biomeos_discovery/mod.rs` — allow removal
- `crates/petal-tongue-core/src/sensor/registry.rs` — impl
- `crates/petal-tongue-core/src/engine.rs` — `render_multi` simplification
- `crates/petal-tongue-core/src/engine_tests.rs` — test impls
- `crates/petal-tongue-ui/src/audio/traits.rs` — `AudioBackend`
- `crates/petal-tongue-ui/src/display/traits.rs` — `DisplayBackend`
- `crates/petal-tongue-ui/src/sensors/{mod,audio,keyboard,mouse,screen}.rs`
- `crates/petal-tongue-ui/src/sensor_discovery.rs`
- `crates/petal-tongue-discovery/src/traits.rs` — `VisualizationDataProvider`

## Verification

- `cargo clippy --workspace --all-targets --all-features -- -D warnings` → 0
- `cargo test --workspace --all-features` → 98 suites, 0 failures
- `cargo check --target x86_64-apple-darwin` → pass

## Implications for primalSpring

petalTongue's trait surface is now fully modern Rust. No `#[async_trait]`, no
manual async desugaring, no `dyn` trait objects for core interfaces. All async
dispatch is static (enum dispatch + RPITIT). The codebase has zero suppressions
in production code paths — `#[allow(` exists only in test modules.
