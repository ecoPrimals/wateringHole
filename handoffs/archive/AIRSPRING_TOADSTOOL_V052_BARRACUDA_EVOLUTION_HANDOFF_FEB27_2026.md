# airSpring → ToadStool V0.5.2 Handoff: BarraCuda Evolution & Absorption Summary

**Date**: February 27, 2026
**From**: airSpring v0.5.2 (584 lib tests, 55 binaries, 73/73 real-data atlas stream)
**To**: ToadStool S68+ / BarraCuda team
**License**: AGPL-3.0-or-later
**Previous**: V030 (Anderson coupling, CPU benchmark, documentation sweep)
**Supersedes**: `AIRSPRING_TOADSTOOL_V052_OPS_5_8_HANDOFF_FEB27_2026.md` (narrow ops-only handoff, archived)

---

## Part 1: Executive Summary

airSpring has completed its full validation arc — 45 experiments across precision
agriculture, environmental systems, and cross-spring coupling, with 584 lib tests,
55 binaries, 1109/1109 Python baselines, and 73/73 real-data validation on 80-year
Open-Meteo ERA5 station data (12 stations, 4800 crop-year results, mass balance
~2e-13 mm). This handoff synthesizes the full BarraCuda delegation inventory,
the 4 new Tier B ops for ToadStool absorption, architecture learnings from the
seasonal pipeline and atlas streaming, and the evolution roadmap.

**Key numbers**:
- 45 experiments, 1109/1109 Python, 584 lib + 31 forge tests
- 25+ active CPU delegations + 11 Tier A GPU + 4 Tier B GPU wired (ops 5-8)
- 3 pipeline orchestrators: seasonal pipeline, atlas stream, MC ET₀
- 18 metalForge workloads, 29/29 cross-system routing (GPU+NPU+CPU)
- 25.9× faster than Python (geometric mean, 8/8 parity)
- 73/73 real-data validation (12 stations, 4800 crop-year results)
- 3 inter-primal handoffs (ToadStool ops, NestGate data, biomeOS graphs)

---

## Part 2: BarraCuda Delegation Inventory

### Active CPU Delegations

| # | airSpring Module | BarraCuda Target | Wired In |
|---|---|---|---|
| 1 | `testutil::r_squared` | `stats::pearson_correlation` | v0.3.6 |
| 2 | `testutil::spearman_r` | `stats::correlation::spearman_correlation` | v0.3.6 |
| 3 | `testutil::bootstrap_rmse` | `stats::bootstrap_ci` | v0.3.6 |
| 4 | `testutil::rmse` | `stats::metrics::rmse` | v0.4.3 (S64) |
| 5 | `testutil::mbe` | `stats::metrics::mbe` | v0.4.3 (S64) |
| 6 | `eco::correction::fit_ridge` | `linalg::ridge::ridge_regression` | v0.3.6 |
| 7 | `eco::correction::fit_linear` | `stats::regression::fit_linear` | v0.4.6 (S66) |
| 8 | `eco::correction::fit_quadratic` | `stats::regression::fit_quadratic` | v0.4.6 (S66) |
| 9 | `eco::correction::fit_exponential` | `stats::regression::fit_exponential` | v0.4.6 (S66) |
| 10 | `eco::correction::fit_logarithmic` | `stats::regression::fit_logarithmic` | v0.4.6 (S66) |
| 11 | `eco::diversity` | `stats::diversity` (Shannon, Simpson, Bray-Curtis) | v0.4.3 (S64) |
| 12 | `eco::richards::inverse_van_genuchten_h` | `optimize::brent` | v0.4.4 |
| 13 | `gpu::mc_et0::parametric_ci` | `stats::normal::norm_ppf` | v0.4.4 |
| 14 | `validation::ValidationHarness` | `validation::ValidationHarness` | v0.3.6 |
| 15 | `tolerances::*` | `tolerances::*` | v0.3.6 |

### 11 Active GPU Delegations (Tier A)

| # | airSpring Module | BarraCuda Primitive | Status |
|---|---|---|---|
| 16 | `gpu::et0::BatchedEt0` | `ops::batched_elementwise_f64` (op=0) | GPU-FIRST |
| 17 | `gpu::water_balance::BatchedWaterBalance` | `ops::batched_elementwise_f64` (op=1) | GPU-STEP |
| 18 | `gpu::kriging::KrigingInterpolator` | `ops::kriging_f64::KrigingF64` | INTEGRATED |
| 19 | `gpu::reduce::SeasonalReducer` | `ops::fused_map_reduce_f64` | GPU N≥1024 |
| 20 | `gpu::stream::StreamSmoother` | `ops::moving_window_stats` | WIRED |
| 21 | `gpu::richards::BatchedRichards` | `pde::richards::solve_richards` | WIRED |
| 22 | `gpu::isotherm::fit_*_nm/global` | `optimize::nelder_mead` + `multi_start` | WIRED |
| 23 | `gpu::mc_et0` (GPU shader) | `mc_et0_propagate_f64.wgsl` | WIRED |
| 24 | CN f64 cross-val | `pde::crank_nicolson::CrankNicolson1D` | WIRED |
| 25 | `eco::diversity` | `stats::diversity` (via barracuda) | LEANING |
| 26 | `eco::richards` VG params | `pde::richards::SoilParams` (8 named) | LEANING |

### 4 Tier B GPU Orchestrators (Pending ToadStool Absorption)

| # | airSpring Module | BarraCuda Target | Op | Stride |
|---|---|---|---|---|
| 27 | `gpu::sensor_calibration::BatchedSensorCal` | `batched_elementwise_f64` (op=5) | 5 | 1 |
| 28 | `gpu::hargreaves::BatchedHargreaves` | `batched_elementwise_f64` (op=6) | 6 | 4 |
| 29 | `gpu::kc_climate::BatchedKcClimate` | `batched_elementwise_f64` (op=7) | 7 | 4 |
| 30 | `gpu::dual_kc::BatchedDualKc` | `batched_elementwise_f64` (op=8) | 8 | 9 |

### 3 Pipeline Orchestrators (CPU-chained, upgrade to GPU per-stage)

| # | airSpring Module | Description | Status |
|---|---|---|---|
| 31 | `gpu::seasonal_pipeline` | ET₀→Kc adjust→WB→Yield chained | CPU chained |
| 32 | `gpu::atlas_stream` | Station-batch 80yr streaming | CPU chained |
| 33 | `gpu::mc_et0` (CPU path) | MC uncertainty propagation | CPU mirror |

---

## Part 3: Ops 5-8 Absorption Specification

**What ToadStool needs to do**: Add 4 `case` blocks to
`batched_elementwise_f64.wgsl` and 4 enum variants to
`batched_elementwise_f64.rs`. No new shaders needed — these reuse the
existing `BatchedElementwiseF64` infrastructure.

**Estimated effort**: Low — each op is 5-15 lines of WGSL math.

### Op 5: SoilWatch 10 Sensor Calibration

**Stride**: 1 | **Input**: `[raw_count]` | **Output**: VWC (cm³/cm³)

```wgsl
case 5u: {
    let raw = input[base + 0u];
    output[batch_idx] = fma_f64(
        fma_f64(fma_f64(f64(2e-13), raw, f64(-4e-9)), raw, f64(4e-5)),
        raw, f64(-0.0677));
}
```

**Rust reference**: `eco::sensor_calibration::soilwatch10_vwc()`
**Validation**: 9 lib tests in `gpu::sensor_calibration`

### Op 6: Hargreaves-Samani ET₀

**Stride**: 4 | **Input**: `[tmax, tmin, lat_rad, doy]` | **Output**: ET₀ (mm/day)

```wgsl
case 6u: {
    let tmax = input[base + 0u];
    let tmin = input[base + 1u];
    let lat_rad = input[base + 2u];
    let doy_f = input[base + 3u];
    let dr = f64(1.0) + f64(0.033) * cos_f64(f64(6.283185307) * doy_f / f64(365.0));
    let delta = f64(0.4093) * sin_f64(f64(6.283185307) * doy_f / f64(365.0) - f64(1.405));
    let ws = acos_f64(f64(-1.0) * tan_f64(lat_rad) * tan_f64(delta));
    let ra_mj = f64(37.586) * dr * (
        ws * sin_f64(lat_rad) * sin_f64(delta) +
        cos_f64(lat_rad) * cos_f64(delta) * sin_f64(ws));
    let ra_mm = ra_mj * f64(0.408);
    let tmean = (tmax + tmin) * f64(0.5);
    let td = max(tmax - tmin, f64(0.0));
    output[batch_idx] = max(f64(0.0023) * (tmean + f64(17.8)) * sqrt_f64(td) * ra_mm, f64(0.0));
}
```

**Rust reference**: `eco::evapotranspiration::hargreaves_et0()`
**Validation**: 11 lib tests in `gpu::hargreaves`

### Op 7: Kc Climate Adjustment (FAO-56 Eq. 62)

**Stride**: 4 | **Input**: `[kc_table, u2, rh_min, crop_height_m]` | **Output**: Adjusted Kc

```wgsl
case 7u: {
    let kc_table = input[base + 0u];
    let u2 = input[base + 1u];
    let rh_min = input[base + 2u];
    let h = input[base + 3u];
    let adj = fma_f64(f64(0.04), u2 - f64(2.0), f64(-0.004) * (rh_min - f64(45.0)))
            * pow_f64(h / f64(3.0), f64(0.3));
    output[batch_idx] = max(kc_table + adj, f64(0.0));
}
```

**Rust reference**: `eco::crop::adjust_kc_for_climate()`
**Validation**: 8 lib tests in `gpu::kc_climate`

### Op 8: Dual Kc Evaporation Layer (Ke Step)

**Stride**: 9 | **Input**: `[kcb, kc_max, few, mulch_factor, de_prev, rew, tew, p_eff, et0]` | **Output**: Ke

```wgsl
case 8u: {
    let kcb = input[base + 0u];
    let kc_max = input[base + 1u];
    let few = input[base + 2u];
    let mulch = input[base + 3u];
    let de_prev = input[base + 4u];
    let rew = input[base + 5u];
    let tew = input[base + 6u];
    let p_eff = input[base + 7u];
    let et0 = input[base + 8u];
    var kr = f64(1.0);
    if de_prev > rew { kr = max((tew - de_prev) / max(tew - rew, f64(0.001)), f64(0.0)); }
    let ke_full = kr * (kc_max - kcb);
    let ke_limit = max(few * (kc_max - kcb), f64(0.0));
    output[batch_idx] = min(ke_full, ke_limit) * mulch;
}
```

**Rust reference**: `eco::dual_kc::step()` (Ke component)
**Validation**: 2 GPU-specific tests in `gpu::dual_kc`

### Rust Enum Changes

```rust
#[repr(u32)]
pub enum Op {
    Fao56Et0 = 0,
    WaterBalance = 1,
    Custom = 2,
    ShannonBatch = 3,
    SimpsonBatch = 4,
    SensorCalibration = 5,  // NEW
    HargreavesEt0 = 6,      // NEW
    KcClimateAdjust = 7,    // NEW
    DualKcKe = 8,            // NEW
}
```

---

## Part 4: Architecture Learnings

### Seasonal Pipeline: Zero-Round-Trip Chaining

`gpu::seasonal_pipeline` chains ET₀ → Kc adjust → water balance → Stewart yield
as a single logical pipeline. Currently CPU-chained (each stage runs sequentially),
but architecturally designed for GPU per-stage dispatch:

```
WeatherDay[] → BatchedEt0(op=0) → et0[]
    → BatchedKcClimate(op=7) → kc_adj[]
    → BatchedWaterBalance(op=1) → wb_state[]
    → yield_ratio_single() → YieldResult
```

**Key insight**: The pipeline never reads back to CPU between stages — it chains
output buffers as input to the next stage. Once ToadStool absorbs ops 5-8, this
becomes a true GPU pipeline with zero round-trip overhead.

**Validated**: 73/73 PASS on real 80-year data (12 Michigan stations × 5 crops ×
80 seasons = 4800 crop-year results).

### Atlas Streaming: Station-Batch Architecture

`gpu::atlas_stream` discovers CSV files at runtime, parses them into `WeatherDay`
structs, filters to growing season (DOY 121-273), and batches by station. Each
station-batch is processed through the seasonal pipeline independently.

**Key insight**: This is a natural fit for `UnidirectionalPipeline` — fire-and-forget
streaming where each station batch is submitted and results collected asynchronously.
The streaming pattern eliminates the need to hold all 80 years × 100 stations in
memory simultaneously.

### metalForge Cross-System Routing

metalForge now routes 18 eco workloads across GPU, NPU, and CPU substrates with
architecture-aware dispatch:

| Substrate | Workloads | Status |
|-----------|-----------|--------|
| GPU (Vulkan/wgpu) | ET₀ (op=0), WB (op=1), kriging, reduce, stream, richards, isotherm, MC ET₀ | Live (Titan V, RTX 4070) |
| NPU (AKD1000) | crop stress, irrigation, anomaly classifiers | Live (3 experiments) |
| CPU fallback | All 18 workloads | Always available |
| Tier B (pending) | sensor cal (op=5), Hargreaves (op=6), Kc climate (op=7), dual Kc (op=8) | CPU-only until absorption |

29/29 cross-system routing checks pass. `ShaderOrigin::Absorbed` vs `ShaderOrigin::Local`
tracks which workloads have upstream GPU primitives vs CPU-only local implementations.

---

## Part 5: What ToadStool Should Absorb (Priority Order)

### Priority 1: Ops 5-8 (Low effort, high impact)

Four `case` blocks in `batched_elementwise_f64.wgsl`. Unlocks GPU dispatch for
the full agricultural pipeline. airSpring orchestrators auto-activate — zero
effort on our side.

### Priority 2: SeasonalPipeline GPU Chaining

Once ops 0-8 are all GPU-resident, the seasonal pipeline can chain GPU buffers
without CPU readback. This is the "zero-round-trip" architecture that makes
100-station × 80-year atlas processing viable on GPU.

### Priority 3: UnidirectionalPipeline for Atlas Streaming

The atlas stream pattern (fire-and-forget station batches) maps naturally to
`staging::UnidirectionalPipeline`. Currently the barracuda `UnidirectionalPipeline`
exists but airSpring hasn't wired it because ops 5-8 aren't GPU-resident yet.

### Not Needed

- `gpu::sensor_calibration`, `gpu::hargreaves`, `gpu::kc_climate`, `gpu::dual_kc`
  Rust wrappers stay local (domain-specific API surface)
- `eco::*` modules stay local (FAO-56 domain logic)
- `io::csv_ts` stays local (airSpring-specific IoT CSV parser)

---

## Part 6: Validation Commands

```bash
# All lib tests (584 pass, 0 failures)
cd airSpring/barracuda && cargo test --lib

# Atlas stream on real 80yr data (73/73 PASS)
cargo run --release --bin validate_atlas_stream

# Pure GPU validation (16/16 PASS)
cargo run --release --bin validate_pure_gpu

# metalForge cross-system dispatch (29/29 PASS)
cd ../metalForge/forge && cargo run --release --bin validate_dispatch

# Clippy pedantic (0 warnings)
cd ../../barracuda && cargo clippy --lib

# Full suite (all 55 binaries)
bash ../run_all_baselines.sh
```

---

## Part 7: Evolution Roadmap

### Phase A: Per-Stage GPU (after ops 5-8 absorption)

Each pipeline stage dispatches independently to GPU:
- `BatchedEt0(op=0)` → GPU
- `BatchedKcClimate(op=7)` → GPU
- `BatchedWaterBalance(op=1)` → GPU
- `yield_ratio_single()` → CPU (trivial, not worth GPU dispatch)

**Expected speedup**: 5-10× for atlas-scale (100 stations × 80 years)

### Phase B: GPU Pipelined (zero round-trip)

Chain GPU buffers between stages without CPU readback:
```
GPU buffer → op=0 → GPU buffer → op=7 → GPU buffer → op=1 → readback
```

**Expected speedup**: 20-50× (eliminates PCIe transfers between stages)

### Phase C: Streaming Atlas (UnidirectionalPipeline)

Fire-and-forget station batches to GPU:
```
Station 1 → submit → [GPU processing]
Station 2 → submit → [GPU processing]
...
Station 100 → submit → [GPU processing]
← collect all results asynchronously
```

**Expected speedup**: 100× at atlas scale (overlap CPU parsing with GPU compute)

### Phase D: NUCLEUS Deployment

biomeOS deployment graph routes atlas computation across NUCLEUS atomics:
- NestGate acquires Open-Meteo data (80yr, rate-limit-aware)
- ToadStool/BarraCuda runs seasonal pipeline on GPU node
- Results stored via NestGate with provenance
- biomeOS coordinates via TOML graph (see `AIRSPRING_BIOMEOS_V052_WORKLOAD_GRAPH_HANDOFF`)

---

## Cross-Spring Contributions Back

| Fix | Impact | When |
|-----|--------|------|
| TS-001: `pow_f64` fractional exponent | All Springs using VG/exponential math | S54 |
| TS-003: `acos` precision boundary | All Springs using trig in f64 shaders | S54 |
| TS-004: reduce buffer N≥1024 | All Springs using `FusedMapReduceF64` | S54 |
| Richards PDE solver | Absorbed upstream as `pde::richards` | S40 |
| Stats metrics (rmse, mbe, NSE, IA, R²) | Absorbed upstream as `stats::metrics` | S64 |
| 6 metalForge modules | Absorbed upstream (regression, hydrology, moving_window, isotherm, VG, metrics) | S64+S66 |

---

## Related Handoffs

| Handoff | Target | Content |
|---------|--------|---------|
| `AIRSPRING_NESTGATE_V052_DATA_PROVIDER_HANDOFF` | NestGate team | Open-Meteo/NOAA/NASS data acquisition, rate-limit handling, provenance |
| `AIRSPRING_BIOMEOS_V052_WORKLOAD_GRAPH_HANDOFF` | biomeOS team | TOML deployment graph, NUCLEUS atomic mapping, 18 workload routing |

---

*airSpring v0.5.2 — 45 experiments, 584 lib + 31 forge tests, 55 binaries,
73/73 real-data atlas stream (12 stations, 4800 results), 11 Tier A + 4 Tier B
GPU orchestrators, 25.9× Rust-vs-Python, metalForge 18 workloads 29/29 cross-system.
Pure Rust + BarraCuda. AGPL-3.0-or-later.*
