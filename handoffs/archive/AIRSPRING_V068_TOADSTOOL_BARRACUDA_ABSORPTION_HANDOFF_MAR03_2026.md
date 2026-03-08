<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# airSpring V0.6.8 → ToadStool/barraCuda Absorption Handoff

**Date**: March 3, 2026
**From**: airSpring V0.6.8 (ecology/agriculture validation Spring)
**To**: ToadStool S93 (hardware dispatch) + barraCuda 0.3.1 (sovereign math)
**License**: AGPL-3.0-or-later

---

## Executive Summary

- airSpring rewired from `phase1/toadstool/crates/barracuda` → standalone `barraCuda/crates/barracuda` (v0.3.1)
- 1132/1132 tests pass, 94.91% line coverage, 0 clippy warnings (pedantic), 0 unsafe
- Capability-based discovery replaces hardcoded primal names in NUCLEUS validation
- 6 local WGSL shaders (SCS-CN, Stewart yield, 4× simple ET₀) ready for barraCuda absorption
- 3 evolution paths documented: `BatchedStatefulF64` water balance, `BatchedNelderMeadGpu` isotherm, GPU-local → f64 promotion

---

## 1. Primitives for Upstream Absorption

### 1.1 Local WGSL Shaders (6 ops — `gpu::local_dispatch`)

airSpring maintains 6 local WGSL shaders in `local_elementwise.wgsl` that should be
absorbed into barraCuda's `batched_elementwise_f64` as new ops:

| Local Op | Domain | Formula | Precision | Absorption Path |
|----------|--------|---------|-----------|-----------------|
| op=0 | SCS-CN runoff | `Q = (P - 0.2S)² / (P + 0.8S)` | f32 → **f64** | New `batched_elementwise_f64` op |
| op=1 | Stewart yield | `Ya = Ym × (1 - Ky × (1 - ETa/ETc))` | f32 → **f64** | New `batched_elementwise_f64` op |
| op=2 | Makkink ET₀ | `ET₀ = 0.61 × Δ/(Δ+γ) × Rs/λ - 0.12` | f32 → **f64** | New `batched_elementwise_f64` op |
| op=3 | Turc ET₀ | `ET₀ = 0.0133 × T/(T+15) × (23.8856Rs + 50)` | f32 → **f64** | New `batched_elementwise_f64` op |
| op=4 | Hamon ET₀ | `ET₀ = 0.55 × D² × esat/100` | f32 → **f64** | New `batched_elementwise_f64` op |
| op=5 | Blaney-Criddle ET₀ | `ET₀ = p × (0.46T + 8.13)` | f32 → **f64** | New `batched_elementwise_f64` op |

**Current state**: f32 shaders with CPU/GPU parity validated (Exp 075).
**Evolution**: Promote to f64 canonical shaders via barraCuda's `compile_shader_universal()`.

### 1.2 Domain-Specific Tolerances

airSpring defines 50 named tolerance constants in `tolerances.rs` that may inform
barraCuda's cross-domain tolerance library:

| Constant | abs_tol | rel_tol | Domain |
|----------|---------|---------|--------|
| `ET0_REFERENCE` | 0.01 | 1e-3 | FAO-56 ET₀ |
| `WATER_BALANCE_MASS` | 0.01 | 1e-6 | Water balance mass conservation |
| `RICHARDS_STEADY` | 0.001 | 1e-3 | Richards PDE steady-state |
| `BIO_DIVERSITY_SHANNON` | 1e-8 | 1e-8 | Shannon H' |
| `BIO_DIVERSITY_SIMPSON` | 1e-10 | 1e-10 | Simpson 1-D |
| `BIO_BRAY_CURTIS` | 1e-8 | 1e-8 | Bray-Curtis dissimilarity |

These are stricter than barraCuda's `HYDRO_*` defaults and reflect domain-specific
validation against FAO-56 worked examples.

### 1.3 Seasonal Pipeline Pattern

`gpu::seasonal_pipeline` chains ET₀ → Kc → water balance → yield across M fields.
The `BatchedStatefulF64` integration pattern is documented in `gpu/water_balance.rs`:

```
Day loop:
  1. Bind state_in() (depletion) + daily inputs to WB shader
  2. Dispatch compute pass
  3. Bind state_out() as next state_in() via swap()
  4. Only read back at season end
```

This eliminates per-day CPU readback and is the key performance bottleneck for
multi-field seasonal simulation.

---

## 2. Learnings for barraCuda/ToadStool Evolution

### 2.1 Capability-Based Discovery Works

airSpring migrated from hardcoded primal names to capability-based discovery:
- `primal.forward("toadstool", "health")` → `capability.forward("compute.dispatch", "health")`
- `primal.discover()` → `capability.discover()`
- `BIOMEOS_EXPECTED_PRIMALS` → `BIOMEOS_EXPECTED_CAPABILITIES`

**Recommendation**: All Springs should use `get_socket_path_for_capability()` (S90)
rather than `get_socket_path_for_service()`.

### 2.2 `to_toadstool()` → `to_barracuda()` Migration

airSpring renamed all `to_toadstool()` methods to `to_barracuda()`. Other Springs
should do the same when they rewire to standalone barraCuda.

### 2.3 Precision Per Hardware Is Sufficient

airSpring validates FAO-56 ET₀ (needs ~6 digits) on both:
- **Titan V**: native f64 (`Fp64Strategy::Native`)
- **RTX 4070**: DF64 (`Fp64Strategy::Hybrid`, ~48-bit mantissa)

Both pass all 1132 tests. The universal precision architecture is working correctly
for agricultural science workloads.

### 2.4 `exit_no_gpu()` CI Pattern

airSpring wired `barracuda::validation::exit_no_gpu()` into GPU validation binaries.
This enables CI modes:
- **Default**: skip gracefully (exit 0) when no GPU
- **`BARRACUDA_REQUIRE_GPU=1`**: fail hard (exit 1) for GPU CI nodes

### 2.5 Zero Breaking Changes on Rewire

The `phase1/toadstool/crates/barracuda` → `barraCuda/crates/barracuda` rewire
required zero code changes. All imports, traits, and shader references are stable.
hotSpring confirmed the same (716/716). This validates the extraction architecture.

---

## 3. airSpring barracuda API Surface

### Consumed from barraCuda (25 primitives)

| Module | Primitive | Usage |
|--------|-----------|-------|
| `device` | `WgpuDevice`, `Fp64Strategy`, `GpuDriverProfile` | GPU device management |
| `ops` | `batched_elementwise_f64` (ops 0-13) | ET₀, WB, VG, Kc, sensor, GDD |
| `ops` | `kriging_f64` | Spatial interpolation |
| `ops` | `fused_map_reduce_f64` | Seasonal reductions |
| `ops` | `moving_window_stats` | IoT stream smoothing |
| `ops` | `bio::diversity_fusion` | Shannon, Simpson, Bray-Curtis |
| `optimize` | `nelder_mead`, `multi_start_nelder_mead` | Isotherm fitting |
| `optimize` | `brent`, `brent_gpu` | VG inverse, infiltration |
| `pde` | `richards`, `richards_gpu` | 1D Richards PDE |
| `pde` | `crank_nicolson` | CN diffusion cross-validation |
| `stats` | `pearson_correlation`, `regression::fit_linear` | Sensor validation |
| `stats` | `bootstrap::bootstrap_ci`, `jackknife` | Uncertainty quantification |
| `stats` | `normal::norm_ppf` | MC ET₀ confidence intervals |
| `tolerances` | `check`, `Tolerance` | Named validation tolerances |
| `validation` | `ValidationHarness`, `exit_no_gpu`, `gpu_required` | Validation infrastructure |
| `pipeline` | `StatefulPipeline`, `WaterBalanceState` | Cross-spring WB |

### Contributed to barraCuda (historical)

| Contribution | Session | Status |
|-------------|---------|--------|
| Richards PDE (`solve_richards`) | S40 | Absorbed |
| `TS-001`: `pow_f64` fractional exponent fix | S54 | Absorbed |
| `TS-003`: `acos` precision boundary fix | S54 | Absorbed |
| `TS-004`: reduce buffer N≥1024 fix | S54 | Absorbed |
| `StatefulPipeline` pattern | S80 | Absorbed |
| `BatchedStatefulF64` concept | S83 (V045) | Absorbed |
| `stats::regression`, `hydrology`, `moving_window_f64` | S66 | Absorbed |

---

## 4. Action Items for ToadStool/barraCuda Team

### For barraCuda (Math Engine)

- [ ] Absorb 6 local WGSL shaders as `batched_elementwise_f64` ops 14-19 (f64 canonical)
- [ ] Consider adding airSpring's stricter agri-science tolerances to `tolerances.rs`
- [ ] Wire `BatchedStatefulF64` ↔ water balance shader for GPU-resident seasonal state
- [ ] Fix VG inverse shader bug (L49 in `van_genuchten_inverse_f64.wgsl`)

### For ToadStool (Hardware Dispatch)

- [ ] Use `get_socket_path_for_capability()` universally (deprecate service-name discovery)
- [ ] Ensure `compute.dispatch` capability advertised by Node atomics
- [ ] Track airSpring's `metalForge` NUCLEUS mesh patterns for cross-node pipeline routing

---

## 5. Quality Gates (airSpring V0.6.8, March 3, 2026)

| Gate | Result |
|------|--------|
| `cargo fmt --check` | 0 diffs (both crates) |
| `cargo clippy --all-targets -W pedantic` | 0 warnings (both crates) |
| `cargo doc --no-deps` | 0 warnings |
| `cargo test --workspace` (barracuda) | 1132 passed, 0 failed |
| `cargo test` (metalForge) | 62 passed, 0 failed |
| `cargo llvm-cov --lib --summary-only` | 94.91% line / 95.81% function |
| `#![forbid(unsafe_code)]` | Both crates |
| All files < 1000 lines | Yes (max: 950, bench binary) |
| barraCuda version | 0.3.1 standalone |
