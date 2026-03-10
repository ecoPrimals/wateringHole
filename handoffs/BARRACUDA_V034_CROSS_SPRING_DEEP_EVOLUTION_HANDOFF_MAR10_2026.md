# barraCuda → Springs: Cross-Spring Deep Evolution & Absorption

**Date:** March 10, 2026
**From:** barraCuda v0.3.4
**To:** All springs
**License:** AGPL-3.0-only
**Covers:** 6-spring absorption execution, precision routing evolution, pharmacometrics, bioinformatics

---

## Executive Summary

- **PrecisionBrain + HardwareCalibration absorbed** from hotSpring v0.6.25 — domain-aware precision routing with NVVM poisoning safety, adapted to barraCuda's `GpuDriverProfile` and probe cache (no redundant device probing)
- **PhysicsDomain taxonomy** — 12 physics/science domains with per-domain minimum precision tiers, FMA sensitivity, and throughput classification
- **Pharma GPU ops absorbed** from healthSpring V14 — FOCE gradient computation and VPC Monte Carlo simulation with embedded RK4 + PRNG
- **BipartitionEncodeGpu absorbed** from wetSpring V105 — Robinson-Foulds bit-vector encoding for phylogenetic distance
- **Lanczos extended** — configurable convergence, two-pass Gram-Schmidt reorthogonalization, `lanczos_extremal()` for k-largest eigenvalues
- **CsrMatrix::from_triplets_summed** absorbed from wetSpring V105 — duplicate entry summation for FEM assembly
- **OdeTrajectory** — full trajectory recording with time series extraction and interpolation
- **Tolerance registry evolved** — 36 tolerances with runtime introspection (`all_tolerances()`, `by_name()`, `tier()`)
- **3,280 tests passing**, 0 failures, 13 ignored, zero clippy warnings, zero unsafe

---

## Part 1: New Modules

### `device::precision_tier` — Precision Tier Classification

```rust
pub enum PrecisionTier { F32, DF64, F64, F64Precise }
pub enum PhysicsDomain {
    LatticeQcd, GradientFlow, Dielectric, KineticFluid, Eigensolve,
    MolecularDynamics, NuclearEos, PopulationPk, Bioinformatics,
    Hydrology, Statistics, General,
}
```

Springs can query `domain.minimum_tier()`, `domain.fma_sensitive()`, `domain.throughput_bound()` to determine requirements before dispatch.

### `device::hardware_calibration` — Safe Per-Tier Probing

`HardwareCalibration` synthesizes tier capabilities from existing `GpuDriverProfile` and probe cache. **Does not re-dispatch hardware probes** — prevents device poisoning risk. Springs should use `from_device()` or `from_profile()`.

Key queries: `tier_safe(tier)`, `tier_arith_only(tier)`, `best_f64_tier()`, `best_any_tier()`.

### `device::precision_brain` — Domain→Tier Routing

`PrecisionBrain` provides O(1) routing from `PhysicsDomain` to optimal `PrecisionTier`:

```rust
let brain = PrecisionBrain::new(&calibration, &profile);
let advice = brain.route_advice(PhysicsDomain::PopulationPk);
// advice.tier = F64, advice.arith_only = false, advice.fallback = Some(DF64)
```

`compile()` orchestrates shader compilation through the routed tier. All 12 spring domains are mapped.

---

## Part 2: New GPU Operations

### `ops::pharma::foce_gradient` — FOCE Gradient (healthSpring V14)

Per-subject First-Order Conditional Estimation gradients for population PK model fitting. 7-binding BGL. New `foce_gradient_f64.wgsl` shader. `FoceGradientGpu::compute()` handles buffer creation, dispatch, and readback.

### `ops::pharma::vpc_simulate` — VPC Monte Carlo (healthSpring V14)

Visual Predictive Check simulation with embedded one-compartment oral PK model, RK4 integrator, LCG PRNG, and Box-Muller normal sampling. New `vpc_simulate_f64.wgsl`. `VpcSimulateGpu::simulate()` runs N subjects × M simulations in parallel.

### `ops::bio::bipartition_encode` — Bipartition Encoding (wetSpring V105)

Converts tree bipartition membership arrays into packed `u32` bit-vectors for Robinson-Foulds distance computation. New `bipartition_encode.wgsl`. `BipartitionEncodeGpu::encode()`.

---

## Part 3: Evolved Existing Modules

### `spectral::lanczos` — Extended Lanczos

- `lanczos_with_config()` with `LanczosConfig` (configurable convergence threshold, progress callback)
- Two-pass Gram-Schmidt reorthogonalization for numerical stability at N > 1,000
- `lanczos_extremal(n, k)` for efficient k-largest eigenvalue extraction

### `linalg::sparse::csr` — CsrMatrix from-triplets

`CsrMatrix::from_triplets_summed(rows, cols, vals, nrows, ncols)` automatically sums duplicate `(row, col)` entries. Critical for finite-element assembly patterns where multiple elements contribute to the same matrix entry.

### `numerical::ode_generic` — ODE Trajectory

`OdeTrajectory` records full ODE solution paths:
- `time_series(batch, var_idx)` — extract single variable across all timesteps
- `state_at(batch, t)` — interpolated state at arbitrary time
- `final_state(batch)` — terminal state vector

### `tolerances` — Runtime Introspection

6 new tolerances: `PHARMA_FOCE`, `PHARMA_VPC`, `PHARMA_NCA`, `SIGNAL_FFT`, `SIGNAL_QRS`. 36 total.
- `all_tolerances()` — slice of all registered `(&str, f64)` pairs
- `by_name(name)` — O(n) lookup
- `tier(name)` — `"tight"`, `"moderate"`, `"loose"`, `"adaptive"` classification

---

## Part 4: Resolved Spring Issues

| Issue | Source | Status |
|-------|--------|--------|
| `ComputeDispatch` BGL builder pattern | wetSpring V105 | **Resolved** — `BglBuilder` in previous sprint |
| `CsrMatrix` from-triplets builder | wetSpring V105 | **Resolved** — `from_triplets_summed()` |
| Expose scalar activations as public API | neuralSpring V92 | **Resolved** — `barracuda::activations::*` (previous sprint) |
| `foce_estimate` / `saem_estimate` GPU ops | healthSpring V14 | **Resolved** — `FoceGradientGpu` + `VpcSimulateGpu` |
| `BatchReconcileGpu` / bipartition encoding | wetSpring V105 | **Resolved** — `BipartitionEncodeGpu` |
| `Fp64Strategy` Hybrid/Native branching | groundSpring V96 | **Resolved** — `PrecisionBrain` routing |

### Remaining Open Issues

| Issue | Source | Priority | Notes |
|-------|--------|----------|-------|
| `seed_extend` GPU op | wetSpring V105 | P2 | BLAST-like seed-and-extend alignment |
| `profile_alignment` | wetSpring V105 | P2 | Position-weight matrix for MSA |
| Smith-Waterman GPU shader | neuralSpring S139 | P2 | Already have CPU SW; GPU batch variant |
| `peak_integrate_batch` | wetSpring V105 | P2 | Fused GPU peak detection + trapezoidal |
| `AutocorrelationF64` | airSpring v0.7.5 | P2 | Temporal autocorrelation |
| `Fft1DF64` | airSpring v0.7.5 | P2 | Spectral analysis |
| `precision_eval.rs` | hotSpring v0.6.25 | P3 | Per-shader precision profiler |
| `transfer_eval.rs` | hotSpring v0.6.25 | P3 | PCIe bandwidth profiler |

---

## Part 5: Impact on Springs

| Spring | What Changed | Action |
|--------|-------------|--------|
| **hotSpring** | `PrecisionBrain` and `HardwareCalibration` are now barraCuda-native. NVVM poisoning guard + probe-based tier capabilities fully integrated. | Consider delegating precision routing to barraCuda's `PrecisionBrain` instead of maintaining a local copy. |
| **groundSpring** | `Fp64Strategy` branching resolved via `PrecisionBrain` routing. `CsrMatrix::from_triplets_summed` available for FEM assembly. Lanczos extended for large-scale eigenproblems. | Test `lanczos_extremal()` for tridiagonal eigenvalue extraction. |
| **neuralSpring** | Scalar activations (`sigmoid`, `relu`, `gelu`, `swish`, `mish`, `softplus`, `leaky_relu`) public at `barracuda::activations::*`. Hill activation/repression for GRN. | Drop local activation function implementations, use `barracuda::activations::*`. |
| **wetSpring** | `CsrMatrix::from_triplets_summed`, `BipartitionEncodeGpu`, `OdeTrajectory` all available. BGL builder from previous sprint. | Evolve local bipartition encoding to use `BipartitionEncodeGpu`. Test `OdeTrajectory::time_series()` for species trajectory extraction. |
| **airSpring** | `OdeTrajectory` with time series extraction for hydrology ODEs. Tolerance registry expanded with tier introspection. | Test `OdeTrajectory::state_at()` for interpolated catchment state queries. |
| **healthSpring** | `FoceGradientGpu` and `VpcSimulateGpu` now barraCuda-native. Tolerance registry includes `PHARMA_FOCE`, `PHARMA_VPC`, `PHARMA_NCA`. | Evolve local FOCE/VPC GPU dispatch to use `barracuda::ops::pharma::*`. f64 `pow()` polyfill (`exp(n * log(c))`) still needed for native f64 path. |

---

## Part 6: Metrics

```
barraCuda v0.3.4:
  - 3,280 tests passing (0 fail, 13 ignored)
  - 0 clippy warnings (pedantic, all clean)
  - 0 unsafe blocks
  - 797+ WGSL shaders
  - 1,050+ Rust source files
  - 36 registered validation tolerances
  - 12 physics domain classifications
  - NVVM poisoning: guarded on all proprietary NVIDIA architectures
  - PrecisionBrain: O(1) domain→tier routing for all springs
  - Version bumped: 0.3.3 → 0.3.4
  - AGPL-3.0-only
```
