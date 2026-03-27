# airSpring V0.6.8 — barraCuda 0.3.1 Standalone Rewire Handoff

**Date**: March 3, 2026
**airSpring Version**: 0.6.8
**barraCuda Version**: 0.3.1 (standalone primal — `ecoPrimals/barraCuda`)
**ToadStool Session**: S93
**License**: AGPL-3.0-or-later

---

## Summary

airSpring has been rewired from the deprecated ToadStool-embedded barracuda copy
(`phase1/toadstool/crates/barracuda` v0.2.x) to the standalone barraCuda primal
(`ecoPrimals/barraCuda/crates/barracuda` v0.3.1).

This follows the S89 extraction and the wateringHole rewiring guidance
(`BARRACUDA_S89_UNTANGLE_AND_HANDOFF_MAR03_2026.md`).

## Changes Made

### Cargo.toml Path Updates

```toml
# barracuda/Cargo.toml — old:
barracuda = { path = "../../phase1/toadstool/crates/barracuda" }
# barracuda/Cargo.toml — new:
barracuda = { path = "../../barraCuda/crates/barracuda" }

# metalForge/forge/Cargo.toml — old:
barracuda = { path = "../../../phase1/toadstool/crates/barracuda" }
# metalForge/forge/Cargo.toml — new:
barracuda = { path = "../../../barraCuda/crates/barracuda" }
```

### Code Changes

**Zero.** All `use barracuda::*` imports, trait implementations, shader references,
and validation targets remain identical. The rewire is a pure path swap, consistent
with hotSpring's validated experience (716/716 tests, path swap only).

### akida-driver

The NPU hardware driver (`akida-driver`) remains at its ToadStool location
(`phase1/toadstool/crates/neuromorphic/akida-driver`). This is correct — it is a
hardware driver, not part of barraCuda's universal math engine.

## Validation Results

| Gate | Result |
|------|--------|
| `cargo check` (both crates) | **PASS** |
| `cargo fmt --check` (both crates) | **PASS** — 0 diffs |
| `cargo clippy --all-targets -W pedantic` (both crates) | **PASS** — 0 warnings |
| `cargo doc --no-deps` | **PASS** — 0 warnings |
| `cargo test --workspace` | **1132 PASS** — 0 failures |
| `cargo llvm-cov --lib --summary-only` | **95.11% line** / **95.81% function** |

## Architecture Alignment

barraCuda 0.3.1 embodies the S89+ architecture:

- **"Math is universal, precision is silicon"** — barraCuda provides pure math
  primitives; ToadStool dispatches across hardware.
- **Springs depend on barraCuda directly**, not through ToadStool.
- **767 WGSL shaders** — f64 canonical, universal precision (F16/F32/F64/DF64).
- **No cross-primal dependencies** — barraCuda is a standalone sovereign math engine.

## airSpring barracuda API Surface (stable across rewire)

| Module | Usage |
|--------|-------|
| `device::WgpuDevice` | GPU device wrapper |
| `ops::batched_elementwise_f64` | ET₀, WB, VG, Thornthwaite, GDD, dual Kc, sensor cal |
| `ops::kriging_f64` | Spatial interpolation |
| `ops::fused_map_reduce_f64` | Seasonal reductions |
| `ops::moving_window_stats` | IoT stream smoothing |
| `ops::bio::diversity_fusion` | Shannon, Simpson, Bray-Curtis |
| `optimize::brent` / `brent_gpu` | VG inverse, infiltration |
| `pde::richards` / `richards_gpu` | Richards PDE |
| `pde::crank_nicolson` | CN f64 diffusion |
| `stats::*` | pearson, regression, rmse, bootstrap, jackknife, norm_ppf |
| `tolerances` | 47 named constants (re-exported) |
| `validation::ValidationHarness` | All 63+ validation binaries |
| `pipeline::StatefulPipeline` | Cross-spring water balance |

## New Primitives Available (not yet wired)

| Primitive | Module | Potential Use |
|-----------|--------|---------------|
| `gpu_required()` / `exit_no_gpu()` | `validation` | GPU CI gating |
| `require()` / `require!` | `validation` | Result handling in binaries |
| `BIO_DIVERSITY_SHANNON/SIMPSON` | `tolerances` | Diversity validation |
| `NelderMeadGpu` / `BatchedNelderMeadGpu` | `optimize` | GPU isotherm fitting |
| `BatchedStatefulF64` | `pipeline` | GPU-resident water balance |
| `LbfgsGpu` | `optimize` | Smooth optimization |

## Pending Upstream Absorptions

| Primitive | Source | Status |
|-----------|--------|--------|
| `barracuda::npu` (NpuDispatch trait) | wetSpring V61 | Proposed |
| `barracuda::nn` (MLP, LSTM, ESN) | neuralSpring V24 | Proposed |
| `compile_shader_df64_streaming` | neuralSpring V24 | Proposed |

## Deep-Debt Execution (Post-Rewire)

### Capability-Based Discovery

- `nucleus.rs`: `components()` → `capabilities()` returning `["crypto.tls", "mesh.discovery",
  "compute.dispatch"]` instead of hardcoded primal names.
- `validate_nucleus_pipeline.rs`: `primal.forward` → `capability.forward`; `primal.discover`
  → `capability.discover`.
- `validate_nucleus.rs`: `BIOMEOS_EXPECTED_PRIMALS` → `BIOMEOS_EXPECTED_CAPABILITIES`.
- `validate_biome_graph.rs`: checks for capabilities instead of primal names in deployment TOML.

### API Modernization

- `to_toadstool()` → `to_barracuda()` in `gpu/et0.rs` and `gpu/water_balance.rs` (6 callers).
- Magic numbers extracted to named constants: `READ_TIMEOUT_SECS`, `WRITE_TIMEOUT_SECS`,
  `HEARTBEAT_INTERVAL_SECS` in `airspring_primal.rs`; `BRENT_INVERSE_*` in `van_genuchten.rs`.
- `primal_science.rs`: `unwrap()` → `let Some(last) = ... else { return error }`.

### New Primitives Wired

- `validation::exit_no_gpu()` and `gpu_required()` re-exported and used in GPU validation
  binaries for CI-aware handling.
- 3 bio diversity tolerance constants added: `BIO_DIVERSITY_SHANNON`, `BIO_DIVERSITY_SIMPSON`,
  `BIO_BRAY_CURTIS`.

### Evolution Documentation Updated

- `evolution_gaps.rs`: S87-S93 history, `BarraCuda` in tier tables, `ToadStool` backticked.
- `device_info.rs`: Historical provenance note for pre-S89 session references.
- `water_balance.rs`: `BatchedStatefulF64` GPU-resident state evolution path documented.
- `isotherm.rs`: `BatchedNelderMeadGpu` batch fitting evolution path documented.

### Stale Reference Cleanup

- Cargo.toml: `ToadStool` references in comments → `barraCuda`.
- `doc_markdown` lints: all `ToadStool`, `BearDog` references backticked.

### Quality Gates (Post Deep-Debt)

| Gate | Result |
|------|--------|
| `cargo fmt --check` | **0 diffs** (both crates) |
| `cargo clippy -W pedantic` | **0 warnings** (both crates) |
| `cargo doc --no-deps` | **0 warnings** |
| `cargo test --workspace` | **1132 passed** (barracuda) + **62 passed** (metalForge) |
| `cargo llvm-cov --lib --summary-only` | **94.91% line** / **95.81% function** coverage |

## Next Steps

1. Wire `BatchedStatefulF64` for GPU-resident water balance (needs custom shader pipeline binding).
2. Wire `BatchedNelderMeadGpu` for batch isotherm fitting when multi-sample use case arises.
3. Track barraCuda CHANGELOG for new hydrology/bio primitives to absorb.
4. Evolve `ureq` → Songbird when Tower Atomic is available.
