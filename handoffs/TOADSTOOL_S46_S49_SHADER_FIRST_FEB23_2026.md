# ToadStool Sessions 46-49 — Shader-First Architecture Complete

**Date**: February 23, 2026  
**Scope**: Cross-project shader absorption, f32→f64 evolution, CPU fallback elimination, linalg/RBF/PPPM GPU wiring, lattice QCD GPU orchestration, f64 transcendental polyfill validation

---

## Mandate

All math originates as WGSL shaders at f64 precision for universal portability. No CPU-only workloads in production. Barracuda does not care about hardware -- it cares that all math is an f64 shader. ToadStool routes to the best substrate at runtime based on live capability info.

---

## Sessions Summary

### S46 — Cross-Project Absorption

All four Springs fully absorbed into barracuda:

| Spring | Absorbed | Detail |
|--------|----------|--------|
| hotSpring | 11 HFB physics + heat current | Spherical + axially-deformed nuclear physics shaders |
| neuralSpring | 4 bio ML + PRNG | stencil cooperation, wright-fisher, logsumexp, HMM forward |
| wetSpring | 5 ODE shaders | All at f64. `BatchedOdeRK4` generic in place |
| airSpring | Uses toadStool shaders | No local shaders -- GPU bridge consumer |

### S47 — Lattice QCD GPU Shaders

14 new WGSL compute shaders for full lattice QCD:

| Shader | Purpose |
|--------|---------|
| `lattice_init_f64.wgsl` | Cold/hot start (identity + random near-identity) |
| `wilson_action_f64.wgsl` | Per-site Wilson action S = Σ(1 - ReTr P/3) |
| `polyakov_loop_f64.wgsl` | Temporal Wilson line per spatial site |
| `hmc_leapfrog_f64.wgsl` | Momentum kick + link update + momentum generation |
| `kinetic_energy_f64.wgsl` | Per-link T = -0.5·ReTr(π²) |
| `pseudofermion_heatbath_f64.wgsl` | Gaussian noise for φ = D†η |
| `pseudofermion_force_f64.wgsl` | Per-link dS_F/dU from CG solution |
| `lcg_f64.wgsl` | GPU PRNG (xorshift32 + Box-Muller, u32-only) |
| `su3_extended_f64.wgsl` | Reunitarize, exp_cayley, random algebra |
| + staggered Dirac, complex_dot, axpy, xpay, norm2 | Supporting algebra |

CPU lattice code (`constants.rs`, `cpu_complex.rs`, `cpu_su3.rs`, `wilson.rs`, `cpu_dirac.rs`, `pseudofermion.rs`) all gated `#[cfg(test)]` as validation reference.

### S48 — Lattice QCD GPU Orchestration

| Module | Purpose |
|--------|---------|
| `GpuCgSolver` | Host-side CG loop: D†D application via dual Dirac dispatch, inner products via complex_dot + reduce, convergence check on host |
| `GpuHmcTrajectory` | Full dynamical fermion HMC: pseudofermion heatbath → Hamiltonian → leapfrog → Metropolis accept/reject |

### S49 — f32→f64 Evolution + Shader-First Enforcement

**13 f32 shaders evolved to f64** (Naga-validated):

| Domain | Shaders |
|--------|---------|
| Bio/Game Theory | stencil_cooperation, wright_fisher_step, hill_gate, locus_variance, multi_obj_fitness, swarm_nn_forward, batch_fitness_eval |
| Numerical/ML | rk45_adaptive, logsumexp, hmm_forward_log, prng_xoshiro |
| ESN | esn_reservoir_update, esn_readout |

**S49c-d: Force field + MD GPU enforcement:**

| Area | Change |
|------|--------|
| `VelocityVerletF64` | Full GPU dispatch (3 entry points), CPU removed |
| `MsdGpu` | New MSD observable shader + wrapper |
| `CubicSpline` | Shader evolved to native f64, `eval_many_gpu()` added |
| `RdfHistogramF64` | Wired to GPU shader, CPU fallback removed |
| `cdist_f64.wgsl` | New f64 pairwise distance shader (Euclidean/Manhattan/Cosine) |
| Coulomb, Morse, Born-Mayer, Yukawa | All CPU fallbacks removed — always GPU dispatch |

**S49e: Comprehensive CPU fallback elimination:**

- **27+ threshold-gated CPU fallbacks removed** across crank_nicolson, cyclic_reduction, batched_elementwise, moving_window, correlation, covariance, fused_map_reduce, rk_stage, bray_curtis, all 4 bessel ops, laguerre, hermite, legendre, spherical_harmonics, weighted_dot, cosine_similarity
- **6 always-CPU ops wired to GPU**: KineticEnergy, Variance, Covariance, Correlation, Digamma, Beta — all had WGSL shaders but never dispatched them. Now fully GPU.
- **5 shaders evolved to native f64**: variance, covariance, correlation, digamma, beta (from `array<vec2<u32>>` bitcast to `array<f64>`)

**S49f: Linalg + RBF + PPPM GPU wiring:**

| Area | Change |
|------|--------|
| `solve_f64` | GPU via `LinSolveF64` / `linsolve_f64.wgsl`. CPU renamed `solve_f64_cpu`, gated `#[cfg(test)]` |
| `cholesky_f64` | GPU via `CholeskyF64` / `cholesky_f64.wgsl`. CPU gated `#[cfg(test)]` |
| `RBFSurrogate` | Full GPU pipeline: `cdist_f64.wgsl` for distances + GPU solve for coefficients |
| `Pppm` (PPPM electrostatics) | GPU `Fft3DF64` replaced CPU FFT |
| Cascade updates | `sample/direct.rs`, `sample/sparsity/*`, `adaptive/mod.rs`, `dispatch/benchmark.rs` all take `Arc<WgpuDevice>` |

---

## f64 Transcendental Coverage

`compile_shader_f64()` ensures every GPU runs every f64 shader:

1. **Fossil substitution**: Legacy `abs_f64(` → native `abs(`, etc.
2. **Transcendental workaround**: On NVK/RADV/Ada drivers, patches `exp(` → `exp_f64(`, `log(` → `log_f64(`, `pow(` → `pow_f64(`
3. **Auto-injection**: If a shader calls `exp_f64()` but doesn't define it, `math_f64.wgsl` software implementation is injected

Available pure WGSL polyfills in `math_f64.wgsl`:
- `exp_f64`, `log_f64`, `pow_f64`
- `sin_f64`, `cos_f64`, `tan_f64`
- `sinh_f64`, `cosh_f64`, `tanh_f64`
- `atan_f64`, `atan2_f64`, `asin_f64`, `acos_f64`
- `cbrt_f64`, `gamma_f64`, `erf_f64`

Result: **All f64 math runs on GPU on every driver**, regardless of native hardware support.

---

## What Other Primals Can Utilize

### For Any Primal Needing Math

BarraCuda provides a complete f64 math library as GPU shaders. Any primal can submit workloads to ToadStool via JSON-RPC:

- **Linear algebra**: solve, cholesky, QR, SVD, LU, eigensolve, GEMM
- **Statistics**: variance, covariance, correlation, moving window stats
- **Special functions**: Bessel (J0/J1/Y0/Y1), Laguerre, Hermite, Legendre, spherical harmonics, digamma, beta, gamma, erf
- **Numerical**: Crank-Nicolson PDE, Richards flow, cubic spline, ODE RK4/RK45
- **Optimization**: RBF surrogate (train/predict/LOO-CV), adaptive sampling
- **Distance metrics**: Euclidean, Manhattan, Cosine, Bray-Curtis pairwise
- **Reductions**: norms (L1, L2, Linf, p-norm), fused map-reduce, weighted dot

### For neuralSpring

- All 13 bio/ESN shaders absorbed and evolved to f64
- `cpu_conv_pool` promoted to `pub` for LeNet-5 validation
- 25 bio ops re-exported at crate root
- ESN reservoir update + readout at f64

### For wetSpring

- All 5 ODE shaders at f64 with `BatchedOdeRK4` generic
- Richards PDE solver available
- Moving window stats for IoT streams

### For hotSpring

- 11 HFB nuclear physics shaders + heat current absorbed
- Lattice QCD: 14 GPU shaders + CG solver + full HMC trajectory
- PPPM electrostatics with GPU FFT
- All force fields GPU-dispatched

### For biomeOS / Squirrel

- ToadStool advertises all compute capabilities via `compute.discover_capabilities`
- Workloads submitted via `compute.submit` — ToadStool routes to optimal substrate
- Cross-gate distributed compute via `gate.*` methods
- Ollama model lifecycle management for local LLM inference

---

## Inventory

- **645+ WGSL f64 shaders** (zero orphans, all wired to Rust)
- **Zero CPU-only math** in production paths
- **14,000+ tests** passing, all quality gates green
- **f64 transcendental polyfills** on every GPU driver
- **Lattice QCD**: 14 shaders + CG solver + HMC trajectory
- **Linalg**: solve, cholesky, QR, SVD, LU — all GPU-dispatched
- **MD**: VV, RDF, MSD, PPPM (GPU FFT), all force fields GPU
- **Special functions**: Bessel, Laguerre, Hermite, Legendre, SH, digamma, beta — all GPU
- **RBF surrogate**: GPU cdist + GPU solve pipeline
- **13 f32→f64 evolutions** from Spring absorption

---

## Remaining Work

| Area | Status | Notes |
|------|--------|-------|
| `eigh_f64` GPU wrapper | Needs orchestration | Multi-pass WGSL shader exists, needs host loop |
| Conv2D/Pool stride/padding | D-S46-001 | WGSL exists but lacks full parametric support |
| W-001 NVK/RADV f64 transcendentals | Polyfill active | Upstream Mesa fix pending Titan V validation |
| W-003 NAK SM70 scheduling | Phase 1 done | SM70 latency tables written; hardware test pending |

---

*Handoff from ToadStool S46-S49, February 23, 2026*
