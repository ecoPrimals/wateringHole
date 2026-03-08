# airSpring → biomeOS V0.5.2 Handoff: Agricultural Workload Graph

**Date**: February 27, 2026
**From**: airSpring v0.5.2
**To**: biomeOS / NUCLEUS team
**License**: AGPL-3.0-or-later

---

## Part 1: Executive Summary

airSpring has validated a complete agricultural pipeline (ET₀ → Kc → Water
Balance → Yield) on real 80-year data through GPU-ready orchestrators. The
pipeline is ready to be exposed as a biomeOS graph workload, enabling NUCLEUS
coordination across Tower (BearDog + Songbird), Node (ToadStool GPU), and
Nest (NestGate data) atomics.

**What biomeOS needs**: A TOML graph definition that wires NestGate data
acquisition → airSpring compute → result storage. airSpring provides the
compute capability; biomeOS provides the orchestration.

---

## Part 2: airSpring Capabilities for biomeOS

### Capability: `compute.agriculture.seasonal_pipeline`

**Description**: Run ET₀ → Kc climate adjust → Water Balance → Yield for a
station's growing season weather data.

**Input**:
```json
{
  "station_id": "east_lansing",
  "year": 2024,
  "crop_type": "corn",
  "weather_data_path": "/path/to/east_lansing_1945-01-01_2024-12-31_daily.csv"
}
```

**Output**:
```json
{
  "station_id": "east_lansing",
  "year": 2024,
  "crop_name": "Corn (grain)",
  "n_days": 153,
  "total_et0_mm": 645.2,
  "total_actual_et_mm": 489.1,
  "total_precipitation_mm": 412.3,
  "total_irrigation_mm": 0.0,
  "stress_days": 12,
  "mass_balance_error_mm": 2.1e-13,
  "yield_ratio": 0.87
}
```

**Rust entry point**: `gpu::atlas_stream::AtlasStream::process_batch()`
**Validated**: 73/73 PASS on 12 real stations, 4,800 crop-year results

### Capability: `compute.agriculture.batched_et0`

**Description**: Batch FAO-56 Penman-Monteith ET₀ for N station-days.

**Rust entry point**: `gpu::et0::BatchedEt0::compute_gpu()`
**GPU status**: Tier A — GPU-FIRST via `batched_elementwise_f64` (op=0)

### Capability: `compute.agriculture.sensor_calibration`

**Description**: Batch SoilWatch 10 raw count → VWC conversion.

**Rust entry point**: `gpu::sensor_calibration::BatchedSensorCal::compute_gpu()`
**GPU status**: Tier B — CPU fallback, GPU pending ToadStool op=5

### Capability: `compute.agriculture.mc_et0_uncertainty`

**Description**: Monte Carlo ET₀ uncertainty propagation (N=10,000 trials).

**Rust entry point**: `gpu::mc_et0::mc_et0_gpu()`
**GPU status**: Tier B — CPU fallback, GPU pending shader

---

## Part 3: Proposed biomeOS Graph

```toml
[graph]
id = "airspring_seasonal_atlas"
description = "Michigan 80yr Crop Water Atlas via airSpring seasonal pipeline"
coordination = "Sequential"

# Step 1: Verify NestGate has weather data
[[nodes]]
id = "check_weather_data"
output = "weather_available"
capabilities = ["storage"]

[nodes.operation]
name = "capability_call"
capability = "data.weather.michigan.daily"

[nodes.operation.params]
action = "check_availability"
station_list = "atlas_stations.json"
date_range = "1945-2024"

[nodes.constraints]
timeout_ms = 5000

# Step 2: Download missing stations (if any)
[[nodes]]
id = "acquire_weather"
depends_on = ["check_weather_data"]
output = "weather_paths"
capabilities = ["storage", "network"]

[nodes.operation]
name = "capability_call"
capability = "data.weather.michigan.daily"

[nodes.operation.params]
action = "download_missing"
station_list = "atlas_stations.json"
date_range = "1945-2024"
rate_limit_delay_s = 20

[nodes.constraints]
timeout_ms = 86400000

# Step 3: Run seasonal pipeline on all stations
[[nodes]]
id = "run_seasonal"
depends_on = ["acquire_weather"]
output = "season_results"
capabilities = ["compute", "gpu"]

[nodes.operation]
name = "capability_call"
capability = "compute.agriculture.seasonal_pipeline"

[nodes.operation.params]
weather_data_dir = "{{weather_paths}}"
crops = ["corn", "soybean", "wheat", "potato", "alfalfa"]
year_range = "1945-2024"

[nodes.constraints]
timeout_ms = 300000
prefer_substrate = "gpu"

# Step 4: Store results with provenance
[[nodes]]
id = "store_results"
depends_on = ["run_seasonal"]
output = "atlas_complete"
capabilities = ["storage"]

[nodes.operation]
name = "capability_call"
capability = "data.store"

[nodes.operation.params]
data = "{{season_results}}"
format = "csv"
provenance = "airspring_v052_atlas_stream"
```

---

## Part 4: NUCLEUS Atomic Mapping

### Local Deployment (Eastgate)

```
Tower Atomic:
  BearDog → Crypto/TLS for NestGate data downloads
  Songbird → Discovery (find other gates on LAN)

Node Atomic (Tower + ToadStool):
  ToadStool → GPU dispatch for ET₀, water balance (RTX 4070)
  airSpring → seasonal_pipeline, atlas_stream as compute workload

Nest Atomic (Tower + NestGate):
  NestGate → Content-addressed blob store for 80yr CSVs
  Provenance → Download metadata (source, checksum, timestamp)
```

### LAN Deployment (future)

```
Eastgate (Node + NPU):
  ToadStool GPU (RTX 4070) → batch ET₀, water balance
  AKD1000 NPU → real-time crop stress classification
  airSpring → seasonal pipeline workloads

Westgate (Heavy Nest):
  NestGate → 76TB ZFS cold storage for ERA5-Land, PRISM, Sentinel-2
  BearDog → Encrypted blob replication

Southgate (Node):
  ToadStool GPU (RTX 3090) → large-batch Richards PDE, kriging
  airSpring → compute-heavy workloads routed here

Strandgate (Heavy Node):
  Dual EPYC + RTX 3090 + 2x AKD1000 → multi-substrate
  metalForge → cross-system dispatch (GPU+NPU+CPU)
```

---

## Part 5: metalForge Workload Catalog

airSpring provides 18 workloads to metalForge for substrate routing:

| Workload | Preferred Substrate | Capabilities | Status |
|----------|-------------------|--------------|--------|
| `fao56_et0_batch` | GPU | F64, ShaderDispatch | Tier A |
| `water_balance_batch` | GPU | F64, ShaderDispatch | Tier A |
| `kriging_soil_moisture` | GPU | F64, MatrixOps | Tier A |
| `seasonal_reduce` | GPU | F64, ShaderDispatch | Tier A |
| `stream_smooth` | GPU | F64, ShaderDispatch | Tier A |
| `richards_pde` | GPU | F64, PdeSolver | Tier A |
| `isotherm_fitting` | GPU | F64, Optimizer | Tier A |
| `ridge_regression` | CPU | F64, LinearAlgebra | Tier A |
| `mc_et0_uncertainty` | GPU | F64, RngKernel | Tier A |
| `hargreaves_et0_batch` | GPU | F64, ShaderDispatch | Tier B (local) |
| `kc_climate_batch` | GPU | F64, ShaderDispatch | Tier B (local) |
| `sensor_calibration_batch` | GPU | F64, ShaderDispatch | Tier B (local) |
| `seasonal_pipeline` | GPU | F64, ShaderDispatch | Tier B (local) |
| `crop_stress_classifier` | NPU | Int8, SpikeInference | Live |
| `irrigation_decision` | NPU | Int8, SpikeInference | Live |
| `anomaly_detector` | NPU | Int8, SpikeInference | Live |
| `weather_ingest` | CPU | Network, JsonParse | CPU-only |
| `csv_timeseries_parse` | CPU | FileIO, Streaming | CPU-only |

The biomeOS graph should route workloads to the correct substrate using
metalForge's `route_workload()` priority chain: GPU → NPU → CPU.

---

## Part 6: Validation Commands

```bash
# Atlas stream on real 80yr data (73/73 PASS)
cd airSpring/barracuda && cargo run --release --bin validate_atlas_stream

# metalForge cross-system routing (29/29 PASS)
cd airSpring/metalForge/forge && cargo run --release --bin validate_dispatch

# Pure GPU orchestrator validation (16/16 PASS)
cd airSpring/barracuda && cargo run --release --bin validate_pure_gpu
```

---

## Part 7: What airSpring Does NOT Need from biomeOS

- airSpring does NOT need biomeOS to run — all validation binaries work standalone
- The biomeOS graph is an orchestration layer, not a dependency
- airSpring's `cargo run --release --bin validate_atlas_stream` is the reference
- biomeOS adds: automated data acquisition, cross-gate compute dispatch,
  provenance tracking, and NUCLEUS coordination

**No biomeOS code changes needed** — biomeOS adds a new graph TOML and
airSpring registers its capabilities. The graph wires NestGate data to
airSpring compute.
