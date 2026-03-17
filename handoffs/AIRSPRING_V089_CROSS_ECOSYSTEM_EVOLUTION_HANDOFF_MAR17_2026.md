# airSpring V0.8.9 — Cross-Ecosystem Evolution Handoff

**Date**: March 17, 2026
**From**: airSpring V0.8.9
**Scope**: Cross-ecosystem absorption of patterns from 7 springs + 4 primals
**Status**: All 10 plan items complete. Zero clippy warnings. Both crates green.

---

## Absorbed Patterns (with provenance)

### P0: Structural Identity and Safety

#### 1. Canonical `PRIMAL_NAME` / `PRIMAL_DOMAIN` (healthSpring V34)

- Added `pub const PRIMAL_NAME: &str = "airspring"` and `PRIMAL_DOMAIN: &str = "ecology"` to `lib.rs`
- `niche::NICHE_NAME` now delegates to `crate::PRIMAL_NAME` (single source of truth)
- Replaced hardcoded `"airspring"` strings in `validate_nucleus.rs`, `validate_biome_graph.rs`
- `niche.rs` test asserts against `crate::PRIMAL_NAME` instead of literal

**Source**: healthSpring V34 handoff — `PRIMAL_NAME`/`PRIMAL_DOMAIN` pattern

#### 2. `OnceLock` GPU Probe Caching (toadStool S158)

- Added `static GPU_DEVICE: OnceLock<Option<Arc<WgpuDevice>>>` to `gpu/device_info/mod.rs`
- `try_f64_device()` now uses `get_or_init()` — single probe per process lifetime
- Redirected 10+ test-local `try_device()` functions across `gpu/*.rs` to use the centralized `try_f64_device()`
- `water_balance.rs` production `gpu_only()` also uses the centralized probe
- Prevents SIGSEGV from concurrent `wgpu::Instance` creation in `cargo test` parallel threads

**Source**: toadStool S158 handoff — SIGSEGV fix via `OnceLock` GPU probe caching

#### 3. `cast` Module — Safe Numeric Casts (neuralSpring S162, healthSpring V33)

- Created `barracuda/src/cast.rs` with `usize_f64()`, `f64_usize()`, `usize_u32()`, `i32_f64()`, `u32_f64()`, `f64_u32()`
- Debug-panics on out-of-range casts, silent in release
- Migrated ~30 high-value library sites in `eco/`, `gpu/`, `io/`, `ipc/`, `primal_science/`
- Removed unfulfilled `#[expect(clippy::cast_precision_loss)]` from `ipc/timeseries.rs`
- Removed redundant `#[expect(clippy::cast_possible_truncation)]` from `gpu/richards.rs` (3 sites)

**Source**: neuralSpring S162 `safe_cast` module + healthSpring V33 centralized cast pattern

### P1: IPC and Discovery Evolution

#### 4. `DispatchOutcome<T>` as Library Type (wetSpring V126, groundSpring V112)

- Created `ipc/dispatch_outcome.rs` with generic `DispatchOutcome<T>` enum
- Added `is_ok()`, `is_recoverable()`, `ok()` helper methods
- Exported from `ipc` module via `pub use`
- `airspring_primal` binary now imports from library instead of defining locally
- Dead-code `#[expect]` removed (all variants documented and public)

**Source**: wetSpring V126 handoff — `DispatchOutcome<T>` library type pattern

#### 5. coralReef + Squirrel Discovery (healthSpring V34)

- Added `primal_names::CORALREEF` constant
- Added `primal_names::domains::SHADER` and `domains::INFERENCE` capability domains
- Added `biomeos::discover_shader_compiler()` — three-tier resolution (env override → named socket scan → capability probe)
- Added `biomeos::discover_inference_primal()` — same three-tier pattern for Squirrel
- Added `biomeos::discover_primal_by_capability()` — generic capability-based primal discovery
- Tests for all new constants and domains

**Source**: healthSpring V34 handoff — `discover_shader_compiler()` / `discover_inference_primal()` pattern

### P2: Code Quality Evolution

#### 6. `eprintln!` → Structured Tracing (neuralSpring S162)

- Migrated `airspring_primal/main.rs` server fatal error path to `tracing::error!`
- Kept `eprintln!` in CLI error paths (tracing not initialized before `run()`)
- Kept `eprintln!` in test SKIP diagnostics (correct for test stderr)
- Kept `eprintln!` in validation binary diagnostics (stderr is correct channel)
- Assessment: ~300 `eprintln!` sites are almost entirely in test + validation code (correct usage)

**Source**: neuralSpring S162 handoff — zero `eprintln!` in library/server code

#### 7. `mul_add()` FMA Numerical Accuracy (barraCuda Sprint 7)

- Evolved 18 sites across 7 files to use `mul_add()` for fused multiply-add precision:
  - `eco/richards.rs` (8) — flux calculations, trapezoidal integration
  - `eco/evapotranspiration.rs` (1) — soil heat flux coefficient
  - `eco/thornthwaite.rs` (1) — Willmott coefficient
  - `eco/dual_kc.rs` (1) — Kr evaporation reduction
  - `eco/infiltration.rs` (1) — Green-Ampt infiltration rate
  - `eco/water_balance.rs` (2) — total available water
  - `gpu/mc_et0.rs` (4) — Monte Carlo wind/solar perturbation
- Preserved `#[expect(clippy::suboptimal_flops)]` in `eco/soil_moisture.rs` (Topp equation reference implementation)

**Source**: barraCuda Sprint 7 handoff — `mul_add()` evolution pattern

### P3: barraCuda Primitive Wiring

#### 8. GemmF64 Transpose + Cyclic Reduction

- `tridiagonal_solve` already wired in `eco/richards.rs` via `barracuda::linalg::tridiagonal_solve` (S52+)
- `cyclic_reduction_f64` already wired via `pde::richards` GPU solver (S62+)
- `GemmF64::execute_gemm_ex(trans_a=true)` available upstream; sensor calibration uses higher-level `stats_f64::linear_regression` which consumes GEMM internally
- Added `gemm_f64_transpose` entry to `gpu/evolution_gaps.rs` documenting availability

**Source**: groundSpring V113 `GemmF64` transpose handoff

#### 9. ValidationSink Assessment (ludoSpring V23)

- Assessed upstream `barracuda::validation::ValidationHarness`: does NOT support sinks
- `finish()` writes directly to tracing — no trait-based output abstraction
- Added `validation_sink` entry to `gpu/evolution_gaps.rs` proposing upstream absorption
- When upstream absorbs ludoSpring's `ValidationSink` trait, airSpring's 91 validation binaries benefit automatically

**Source**: ludoSpring V23 handoff — `ValidationSink` / `StderrSink` / `BufferSink` pattern

### P4: Documentation

#### 10. This Handoff

- Updated `EVOLUTION_READINESS.md` header with V0.8.9 status
- Handoff placed in `airSpring/wateringHole/handoffs/` and `ecoPrimals/wateringHole/handoffs/`

---

## Verification

```
cargo clippy --all-targets    # zero warnings (barracuda + metalForge)
cargo check                   # green
cargo test --lib              # green
```

## Files Changed (summary)

| Category | Files | Changes |
|----------|-------|---------|
| Identity | `lib.rs`, `niche.rs`, `primal_names.rs`, 2 binaries | `PRIMAL_NAME`/`PRIMAL_DOMAIN` constants |
| GPU Safety | `gpu/device_info/mod.rs`, 10 `gpu/*.rs` test modules, `water_balance.rs` | `OnceLock` GPU probe |
| Cast | `cast.rs` (new), ~15 library files | `usize_f64()`/`f64_usize()`/`usize_u32()` migrations |
| IPC | `ipc/dispatch_outcome.rs` (new), `ipc/mod.rs`, `airspring_primal/dispatch.rs`, `main.rs` | `DispatchOutcome<T>` |
| Discovery | `biomeos.rs`, `primal_names.rs` | coralReef/Squirrel discovery |
| Tracing | `airspring_primal/main.rs` | `eprintln!` → `tracing::error!` |
| FMA | 7 `eco/*.rs` + `gpu/mc_et0.rs` | 18 `mul_add()` sites |
| Documentation | `evolution_gaps.rs`, `EVOLUTION_READINESS.md` | GEMM, ValidationSink entries |
| Cleanup | `ipc/timeseries.rs`, `gpu/stream.rs`, `biomeos.rs` | Removed unfulfilled `#[expect]`, simplified bool |

## Upstream Proposals

1. **ValidationSink trait**: Propose barracuda upstream absorption of ludoSpring V23's `ValidationSink`/`StderrSink`/`BufferSink` pattern for testable harness output
2. **GemmF64 direct use**: Available when airSpring needs custom regression beyond `stats_f64::linear_regression`
