# ToadStool Sessions 40-41 — Evolution & Four-Spring Shader Ingestion

**Date**: February 22, 2026  
**Scope**: Richards PDE solver, moving window GPU stats, f64 shader bug fix, API exposure for Springs, archive cleanup

---

## Sessions Summary

### Session 40 — New Capabilities

| Feature | Detail |
|---------|--------|
| **Richards PDE solver** | 1D unsaturated zone water flow: van Genuchten-Mualem soil hydraulics, Picard iteration, Crank-Nicolson time discretization, Thomas tridiagonal solver. `barracuda::pde::solve_richards()` |
| **Moving window statistics GPU op** | Sliding mean/variance/min/max over IoT sensor streams. WGSL shader `moving_window.wgsl` + Rust wrapper with CPU fallback for small inputs. `barracuda::ops::MovingWindowStats` |
| **Dependency audit** | Confirmed workspace is already pure Rust. Only `libc` usage is in akida-driver VFIO ioctls (kernel FFI, not replaceable). |
| **Dead code sweep** | All 38 `#[allow(dead_code)]` annotations verified legitimate (device fields pending GPU dispatch, feature-gated code). |

### Session 41 — Bug Fixes & API Exposure

| Fix | Detail |
|-----|--------|
| **6 f64 shader compile bugs** | `batched_ode_rk4`, `batch_pair_reduce_f64`, `batch_tolerance_search_f64`, `kmd_grouping_f64`, `hill_f64`, `gemm_f64` — all used `compile_shader()` instead of `compile_shader_f64()`, preventing f64 preamble injection for naga/Vulkan. Fixed. |
| **cpu_conv_pool promoted** | `conv2d`, `max_pool2d`, `avg_pool2d` changed from `pub(crate)` to `pub` — unblocks neuralSpring LeNet-5 validation. |
| **25 bio ops re-exported** | All bio operations now accessible at crate root: `barracuda::PairwiseL2Gpu`, `barracuda::TaxonomyFcGpu`, etc. |
| **Archive cleanup** | Removed stale `e2e_primal_discovery_workflow.rs` (dead API). Archived 20 superseded docs to `docs/archive/`, `docs/audits/archive/`, `docs/planning/archive/`. Fixed false "not yet implemented" in `serve_tcp_debug`. |

---

## Cumulative Four-Spring Shader Ingestion

All four Springs have contributed shaders and capabilities that are now fully wired into barracuda:

### hotSpring → barracuda (11 HFB nuclear physics shaders)

| Shader | Module |
|--------|--------|
| `bcs_bisection_f64.wgsl` | `physics::hfb` |
| `batched_hfb_density_f64.wgsl` | `physics::hfb` |
| `batched_hfb_energy_f64.wgsl` | `physics::hfb` |
| `batched_hfb_hamiltonian_f64.wgsl` | `physics::hfb` |
| `batched_hfb_potentials_f64.wgsl` | `physics::hfb` |
| `deformed_bcs_f64.wgsl` | `physics::hfb_deformed` |
| `deformed_density_f64.wgsl` | `physics::hfb_deformed` |
| `deformed_energy_f64.wgsl` | `physics::hfb_deformed` |
| `deformed_hamiltonian_f64.wgsl` | `physics::hfb_deformed` |
| `deformed_potential_f64.wgsl` | `physics::hfb_deformed` |
| `deformed_wavefunction_f64.wgsl` | `physics::hfb_deformed` |

### neuralSpring → barracuda (4 bio ML shaders)

| Shader | Rust Op |
|--------|---------|
| `pairwise_l2.wgsl` | `PairwiseL2Gpu` |
| `multi_obj_fitness.wgsl` | `MultiObjFitnessGpu` |
| `swarm_nn_forward.wgsl` | `SwarmNnGpu` |
| `hill_gate.wgsl` | `HillGateGpu` |

### wetSpring → barracuda (3 bioinformatics shaders)

| Shader | Rust Op |
|--------|---------|
| `kmer_histogram.wgsl` | `KmerHistogramGpu` |
| `taxonomy_fc.wgsl` | `TaxonomyFcGpu` (f64) |
| `unifrac_propagate.wgsl` | `UniFracPropagateGpu` (f64, 2 entry points) |

### airSpring → barracuda (2 new capabilities, S40)

| Feature | Module |
|---------|--------|
| Richards PDE solver (precision agriculture, unsaturated flow) | `barracuda::pde::richards` |
| Moving window statistics (IoT sensor streams) | `barracuda::ops::MovingWindowStats` |

---

## Current Quality Gates

| Metric | Value |
|--------|-------|
| WGSL shaders | 593 (zero orphans — all wired to Rust) |
| Tests (barracuda) | 2,173 |
| Tests (workspace) | 5,965+ |
| Clippy warnings | 0 |
| Bio ops (GPU pipelines) | 25 |
| HFB physics shaders | 11 (spherical + deformed) |
| f64 precision ops | All 6 fixed to use `compile_shader_f64()` |
| Coverage | common 87%, config 89%, core 79%, server 77% |

---

## API Surface for Springs

Springs can now use these public APIs without reaching into internals:

```rust
// Bio ops (all 25 at crate root)
use barracuda::{PairwiseL2Gpu, TaxonomyFcGpu, UniFracPropagateGpu, ...};

// PDE solvers
use barracuda::pde::{solve_richards, RichardsConfig, SoilParams, RichardsBc};

// CPU conv/pool (for neuralSpring LeNet-5)
use barracuda::cpu_conv_pool::{conv2d, max_pool2d, avg_pool2d};

// Moving window stats (for airSpring IoT)
use barracuda::ops::MovingWindowStats;

// Math utilities
use barracuda::math::{exp_f64, log_f64, sin_f64, cos_f64, ...};
```

---

## Next Priority Items

| Item | Priority | For |
|------|----------|-----|
| Conv2D/MaxPool2D GPU executor wiring | P0 | neuralSpring LeNet-5 full GPU path |
| PCoA `BatchedEighGpu` naga fix | P1 | wetSpring principal coordinates |
| W-001 ACO/NAK transcendental upstream | P2 | All f64 GPU users |
| Test coverage 65% → 90% | P2 | All |
