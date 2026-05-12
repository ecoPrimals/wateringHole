# petalTongue v1.6.7 — Sprint 8: dyn Elimination & Modern Rust Evolution

**Date**: April 16, 2026
**Sprint**: 8
**Scope**: Complete `dyn` trait object elimination, `async-trait` removal, large file refactoring, deep debt closure

---

## Summary

Sprint 8 evolved petalTongue to fully modern idiomatic Rust by eliminating all
custom `dyn` trait objects (22 traits), removing the `async-trait` crate entirely
(native `async fn` in traits), refactoring 11 large production modules, and
closing remaining deep debt gaps.

## Key Changes

### dyn Trait Object Elimination (22 traits)

All custom `dyn Trait` usage replaced with enum dispatch or generics:

**8 async traits** — `#[async_trait]` removed, native `async fn` / `impl Future`:
- `ComputeProvider` → `ComputeProviderImpl` enum (Gpu + CpuFallback)
- `GUIModality` → generic `ModalityRegistry<M>` + `NullModality` ZST
- `DiscoveryBackend` → generic `CapabilityDiscovery<B>`
- `Sensor` → `SensorImpl` enum (Mouse + Keyboard + Screen + Audio)
- `AudioBackend` → `AudioBackendImpl` enum (Direct + Socket + Software + Silent)
- `DisplayBackend` → `DisplayBackendImpl` enum (5 backends)
- `UIBackend` → `UIBackendImpl` enum (Egui)
- `VisualizationDataProvider` → `KnownVisualizationProvider` enum (9 providers)

**14 non-async traits** — enum dispatch:
- `PanelInstance`, `PanelFactory`, `ToolPanel`, `TufteConstraint`, `DataStream`
- `AdaptiveUIRenderer`, `SensoryUIRenderer`, `PropertyAdapter`, `SchemaMigration`
- `StatePersistence`, `InputAdapter`, `InversePipeline`, `MathObject`, `TelemetrySubscriber`

**Remaining `dyn`** (6 — irreducible, idiomatic Rust):
- `&dyn std::error::Error` (2) — standard error interface
- `Box<dyn std::error::Error + Send + Sync>` (2) — IPC boundary
- `Box<dyn Fn(...)>` (2) — closure callbacks

### async-trait Removal
- **Before**: 47 `#[async_trait]` annotations, direct `async-trait` dependency
- **After**: 0 annotations, 0 direct dependency (only transitive via axum)
- All `Pin<Box<dyn Future>>` type aliases eliminated

### Module Refactoring (11 modules)
All refactored by domain concern, not mechanical splitting:
- `panel_registry` (814→5 files), `btsp` (639→6 files), `cli_mode` (638→5 files)
- `braille` (615→4 files), `biomeos_discovery` (612→5 files)
- `handlers` CLI (612→4 files), `metrics_dashboard` (611→4 files)
- `interaction` graph (608→5 files), `adaptive_rendering` (605→5 files)
- `instance` (602→5 files), TUI `state` (601→4 files)

### Deep Debt Closure
- Hardcoded `"biomeos"` path → `ecosystem_runtime_dir_name()` (env-configurable)
- 1 production `.unwrap()` → `.expect()` with rationale
- All 19 crate roots + main.rs: `#![forbid(unsafe_code)]`

## Quality Gates

| Gate | Status |
|------|--------|
| Tests | 6,100+ passed (0 failed) |
| Clippy | PASS (pedantic + nursery, `-D warnings`) |
| Docs | PASS (`missing_docs = "deny"`) |
| Unsafe | 0 (`#![forbid(unsafe_code)]` workspace-wide) |
| TODO/FIXME | 0 |
| Production unwrap | 0 |
| dyn custom traits | 0 |
| async-trait annotations | 0 |
| Production files >600 LOC | 0 |
| Edition | 2024 (all crates) |

## For primalSpring

- `async-trait` audit item **resolved**: 0 instances (was 47)
- CHANGELOG doc drift **resolved**: reflects real BTSP Phase 2 enforcement
- All production files under 600 LOC (was "6 files >700 LOC")
- UDS first-byte peek and BTSP Phase 2 enforcement remain resolved from Sprint 7

## Remaining Backlog

- BTSP Phase 2 consumer wiring (cross-primal dep on BearDog)
- BTSP Phase 3 encryption
- aarch64 musl cross-compile for headless
- tarpc feature-gating
- Audio backend wire protocols (PipeWire/PulseAudio)
