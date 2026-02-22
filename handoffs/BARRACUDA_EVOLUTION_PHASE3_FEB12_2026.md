# BarraCuda & ToadStool — Phase 3 Evolution Handoff

**Date**: February 12, 2026
**From**: ecoPrimals Control Team (Eastgate) — hotSpring validation & evolution analysis
**To**: ToadStool / BarraCuda Team
**Priority**: HIGH — Foundational for L3 nuclear physics and all scientific workloads
**Depends On**: All previous handoffs (validated and incorporated)
**Context**: hotSpring heterogeneous L2 pipeline complete, 121/121 library validation tests passed

---

## Executive Summary

BarraCuda has evolved into an extraordinary platform: **436 WGSL shaders**, **540 Rust modules**,
**1,658 tests**, and **~16,800 lines** of scientific computing middleware. The shader-first
architecture is sound. The ML/DL layer is production-grade. The scientific computing modules
work correctly — all validation tests pass.

The evolution now shifts from **breadth** (more shaders) to **depth**:

1. **f64 CPU bridges** for existing GPU linalg ops
2. **Auto-dispatch** so users never worry about CPU vs GPU routing
3. **Heterogeneous pipeline orchestration** for multi-device workflows
4. **Missing math** only as workloads demand it

This document prioritizes what to build next based on real-world findings from
hotSpring nuclear EOS (L1, L2, heterogeneous L2), MD validation, and special function testing.

---

## Part 1: What's Validated — No Changes Needed

These modules passed 121/121 tests against analytical references and Python scipy controls.
They are **production-ready**:

### Special Functions (69/69 tests) ✅

| Function | CPU f64 | GPU f32 | Max Error |
|----------|---------|---------|-----------|
| `gamma(x)` | ✅ | — | < 1e-12 |
| `factorial(n)` | ✅ | — | exact |
| `laguerre(n, α, x)` | ✅ | — | < 1e-12 |
| `erf(x)` | ✅ | ✅ | < 1e-7 |
| `erfc(x)` | ✅ | ✅ | < 1e-7 |
| `bessel_j0(x)` | ✅ | ✅ | < 1e-6 |
| `bessel_j1(x)` | ✅ | ✅ | < 1e-6 |
| `bessel_i0(x)` | ✅ | ✅ | < 1e-6 |
| `bessel_k0(x)` | ✅ | ✅ | < 1e-6 |
| `lgamma(x)` | ✅ | ✅ | < 1e-10 |
| `digamma(x)` | ✅ | — | < 1e-10 |
| `beta(a, b)` | ✅ | — | < 1e-10 |
| `hermite(n, x)` | ✅ | ✅ | exact (integer) |
| `legendre(n, x)` | ✅ | ✅ | < 1e-12 |
| `assoc_legendre(n, m, x)` | ✅ | — | < 1e-12 |

### Linear Algebra (10/10 tests) ✅

| Operation | Status | Notes |
|-----------|--------|-------|
| LU decomposition | ✅ | PA = LU verified, determinant, inverse |
| QR decomposition | ✅ | A = QR verified, Q orthogonality |
| SVD | ✅ | A = UΣVᵀ verified, singular values |
| Tridiagonal solver | ✅ | Thomas algorithm, 1e-14 accuracy |

### Optimizers & Numerical Methods (22/22 tests) ✅

| Method | Status | Notes |
|--------|--------|-------|
| BFGS | ✅ | Rosenbrock → (1,1) to 1e-6 |
| Nelder-Mead | ✅ | Bounded, unbounded, high-dim |
| Multi-start NM | ✅ | Global search with LHS |
| Bisection | ✅ | Root-finding to machine precision |
| RK45 ODE | ✅ | Exponential decay, SHO |
| Crank-Nicolson | ✅ | Heat equation, energy conservation |
| Normal CDF/PDF/PPF | ✅ | Against scipy.stats.norm |
| Pearson correlation | ✅ | Perfect/anti/zero correlation |
| Sobol sequences | ✅ | Dimensionality, bounds, uniformity |

### MD Forces & Integrators (20/20 tests) ✅

| Kernel | Status | Key Validations |
|--------|--------|-----------------|
| Lennard-Jones | ✅ | Newton's 3rd law, equilibrium, momentum conservation |
| Coulomb | ✅ | Inverse-square law, attraction/repulsion, 4.2e-8 error |
| Morse | ✅ | Equilibrium (F≈0), stretch/compress, Newton's 3rd |
| Velocity-Verlet | ✅ | Free particle, constant force |

---

## Part 2: The f64 Linalg Bridge — Priority #1

### The Problem

`barracuda::linalg` exports only `solve_f64`. The GPU ops (`cholesky`, `eigh`, `LU`,
`QR`, `SVD`, `tridiagonal`) exist in `ops/linalg/` as shader wrappers but are **f32-only**
and aren't accessible as CPU f64 functions through the public API.

hotSpring's HFB solver still depends on `nalgebra::SymmetricEigen` because
`barracuda::linalg` has no `symmetric_eigen_f64`.

### What's Needed

Expand `barracuda::linalg/mod.rs` to re-export CPU f64 wrappers for every
operation that already has a GPU shader:

```rust
// barracuda::linalg — Target API
pub mod solve;          // ✅ exists (solve_f64)
pub mod cholesky;       // NEW: cholesky_f64(a, n) → L
pub mod eigh;           // NEW: eigh_f64(a, n) → (eigenvalues, eigenvectors)
pub mod lu;             // NEW: lu_f64(a, n) → (P, L, U)
pub mod qr;             // NEW: qr_f64(a, m, n) → (Q, R)
pub mod svd;            // NEW: svd_f64(a, m, n) → (U, S, Vt)
pub mod tridiagonal;    // NEW: tridiagonal_solve_f64(a, b, c, d) → x
pub mod inverse;        // NEW: inverse_f64(a, n) → A⁻¹
pub mod determinant;    // NEW: determinant_f64(a, n) → det
pub mod triangular;     // NEW: triangular_solve_f64(L, b) → x

pub use solve::solve_f64;
pub use cholesky::cholesky_f64;
pub use eigh::eigh_f64;
pub use lu::{lu_decompose_f64, lu_solve_f64, lu_det_f64};
pub use qr::{qr_decompose_f64, qr_least_squares_f64};
pub use svd::{svd_decompose_f64, svd_pinv_f64};
pub use tridiagonal::tridiagonal_solve_f64;
pub use inverse::inverse_f64;
pub use determinant::determinant_f64;
pub use triangular::triangular_solve_f64;
```

### Implementation Pattern

Each function should follow the dual-precision auto-dispatch pattern:

```rust
/// Symmetric eigendecomposition.
///
/// - CPU path (f64): Pure Rust Jacobi iteration, handles matrices up to ~500×500
/// - GPU path (f32): WGSL eigh shader via `ops::linalg::eigh`
///
/// Auto-dispatches based on matrix size. Threshold: N < 128 → CPU.
pub fn eigh_f64(a: &[f64], n: usize) -> Result<(Vec<f64>, Vec<f64>)> {
    // CPU implementation — replaces nalgebra::SymmetricEigen
    // Jacobi iteration or Householder tridiagonalization + QR algorithm
}

pub fn eigh_gpu(a: &[f32], n: usize, device: &WgpuDevice) -> Result<(Vec<f32>, Vec<f32>)> {
    // Wrapper around ops::linalg::eigh WGSL shader
}
```

### Why This Matters

- Eliminates `nalgebra` as an external dependency for downstream crates
- Every scientific workload can express `barracuda::linalg::eigh_f64` instead of
  pulling in a separate linear algebra library
- Foundation for the generalized eigenvalue problem Ax = λBx (needed for L3 HFB)

### Effort Estimate: 3-5 days

The algorithms already exist in `ops/linalg/*.rs` (f32). The task is:
1. Port each to f64 in pure Rust
2. Add to `linalg/mod.rs` with proper re-exports
3. Add unit tests comparing against known values
4. Add auto-dispatch threshold (benchmark CPU vs GPU)

---

## Part 3: Auto-Dispatch System — Priority #2

### The Problem

During hotSpring L1, we discovered that GPU dispatch for **single-point** surrogate
predictions in the Nelder-Mead inner loop caused a **90× slowdown**. We had to manually
build a CPU-only fast path (`predict_single`).

Every function needs intelligent routing, not just the surrogate.

### What's Needed

A `dispatch` module or pattern that every math function follows:

```rust
// barracuda::dispatch (or integrated into each module)

/// Dispatch threshold configuration
pub struct DispatchConfig {
    /// Input size below which CPU is used
    pub cpu_threshold: usize,
    /// Whether GPU is available
    pub gpu_available: bool,
    /// Whether to force CPU (useful for f64-critical paths)
    pub force_cpu: bool,
}

impl Default for DispatchConfig {
    fn default() -> Self {
        Self {
            cpu_threshold: 1024,  // default, overridden per function
            gpu_available: true,
            force_cpu: false,
        }
    }
}
```

### Per-Function Pattern

```rust
// In barracuda::special::erf
pub fn erf(x: &[f64]) -> Vec<f64> {
    erf_cpu(x)  // always f64 CPU for scalar/small
}

pub fn erf_batch(x: &[f32], device: &WgpuDevice) -> Vec<f32> {
    if x.len() < ERF_GPU_THRESHOLD {
        x.iter().map(|&v| erf_cpu(&[v as f64])[0] as f32).collect()
    } else {
        erf_gpu(x, device)  // WGSL shader
    }
}

const ERF_GPU_THRESHOLD: usize = 512;  // determined by benchmarking
```

### Benchmark Suite

Add a `benches/` directory with criterion benchmarks for every function with dual paths:

```
benches/
├── special_functions.rs    # erf, bessel, gamma at various sizes
├── linalg.rs               # cholesky, eigh, LU at various matrix sizes
├── numerical.rs            # trapz, gradient at various grid sizes
└── surrogate.rs            # RBF train/predict at various N
```

This empirically establishes the crossover point for each function.

### Effort Estimate: 2-3 days

---

## Part 4: Evaluation Cache Persistence — Priority #3

### The Problem

hotSpring's heterogeneous L2 pipeline benefits enormously from warm-starting:
L1 data informs L2 classifier training. But the `EvaluationCache` is in-memory only.
Between runs, all data is lost.

### What's Needed

```rust
// In barracuda::optimize::eval_record

impl EvaluationCache {
    /// Serialize cache to JSON for persistence across runs
    pub fn save(&self, path: &Path) -> Result<()> { ... }

    /// Load cache from a previous run for warm-starting
    pub fn load(path: &Path) -> Result<Self> { ... }

    /// Merge another cache (e.g., L1 results into L2 warm-start)
    pub fn merge(&mut self, other: &EvaluationCache) { ... }

    /// Export as training data format (x_data, y_data)
    pub fn to_training_data(&self) -> (Vec<Vec<f64>>, Vec<f64>) { ... }
}
```

This requires adding `serde::{Serialize, Deserialize}` derives to `EvaluationRecord`
and `EvaluationCache`. The `serde` dependency already exists in many downstream crates.

### Why This Matters

- Enables iterative improvement across sessions
- L1 results become warm-start data for L2
- L2 results become training data for NPU classifiers
- Expensive evaluations are never wasted

### Effort Estimate: 1 day

---

## Part 5: Missing Scientific Functions — Priority #4

### Functions Identified by hotSpring Validation

These are the specific functions that were needed during real workloads but don't
yet exist in BarraCuda:

#### HIGH Priority (needed for L3 nuclear physics + general science)

| Function | Module | Use Case | Effort |
|----------|--------|----------|--------|
| Generalized eigenvalue Ax = λBx | `linalg::gen_eigh` | HFB overlap matrix (L3) | 3-4 days |
| Incomplete gamma γ(a,x) | `special::inc_gamma` | Chi-squared CDF, Poisson CDF | 1-2 days |
| Newton-Raphson root-finding | `optimize::newton` | Nonlinear equations, implicit methods | 1 day |
| Brent's method | `optimize::brent` | Faster 1D root-finding than bisection | 1 day |
| Cubic spline interpolation | `numerical::spline` | EOS tables, smooth data | 2 days |

#### MEDIUM Priority (scientific completeness)

| Function | Module | Use Case | Effort |
|----------|--------|----------|--------|
| Arbitrary-order Bessel Jₙ | `special::bessel_jn` | Nuclear wavefunctions | 1-2 days |
| Modified Bessel Iₙ, Kₙ | `special::bessel_in/kn` | Nuclear density functionals | 1-2 days |
| Gauss-Legendre quadrature | `numerical::gauss_legendre` | High-accuracy integrals | 1-2 days |
| Simpson's rule | `numerical::simpson` | Higher-accuracy 1D integrals | 0.5 day |
| Conjugate gradient | `optimize::cg` | Large sparse linear systems | 2-3 days |
| Differential evolution | `optimize::de` | Global optimizer (gradient-free) | 2-3 days |
| Chi-squared distribution | `stats::chi2` | Goodness-of-fit testing | 1 day |

#### LOW Priority (L3 and advanced workloads)

| Function | Module | Use Case | Effort |
|----------|--------|----------|--------|
| Spherical Bessel jₙ, yₙ | `special::sph_bessel` | Scattering theory (L3) | 1-2 days |
| Airy functions Ai, Bi | `special::airy` | Quantum tunneling | 1-2 days |
| Hypergeometric ₁F₁, ₂F₁ | `special::hypergeo` | Coulomb wavefunctions | 2-3 days |
| Elliptic integrals K, E | `special::elliptic` | Deformed nuclear shapes | 1-2 days |
| Halton sequences | `sample::halton` | Low-discrepancy sampling | 0.5 day |
| KDE | `stats::kde` | Distribution estimation | 1-2 days |
| Gaussian Process regression | `surrogate::gp` | More sophisticated surrogate | 3-5 days |
| Bayesian optimization | `optimize::bayesian` | Expensive-function opt | 3-5 days |
| Wavelet transforms | `transform::wavelet` | Multi-scale analysis | 3-5 days |

---

## Part 6: Heterogeneous Pipeline Orchestration — Priority #5

### What hotSpring Taught Us

The heterogeneous L2 pipeline manually orchestrates four tiers:

```
Tier 1: NMP pre-screen (CPU, ~1μs/candidate)     → 79% rejection
Tier 2: SEMF proxy    (CPU, ~0.1ms/candidate)     → 13% rejection
Tier 3: Classifier    (CPU/NPU, ~10μs/candidate)  → 0% (low recall bypassed)
Tier 4: Full HFB      (CPU parallel, ~0.2s/eval)  → 8% pass rate
         ↓
    RBF Surrogate (GPU cdist + CPU kernel)
         ↓
    Multi-start NM on NMP-aware surrogate
         ↓
    Generate candidates → filter through cascade → repeat
```

This pipeline achieved 7.2× speedup over plain SparsitySampler with better accuracy.
But the orchestration logic was **hand-coded** in hotSpring's `nuclear_eos_l2_hetero.rs`.

### What BarraCuda Could Provide

A `barracuda::pipeline` module for declarative heterogeneous compute:

```rust
use barracuda::pipeline::{Pipeline, Stage, Filter};

let pipeline = Pipeline::builder()
    .filter("nmp_screen", WorkloadHint::SmallWorkload, |params| {
        nmp_prescreen(params, &constraints).is_pass()
    })
    .filter("semf_proxy", WorkloadHint::SmallWorkload, |params| {
        semf_chi2(params, &exp_data) < threshold
    })
    .filter("classifier", WorkloadHint::PreScreen, |params| {
        classifier.predict(params)
    })
    .evaluate("hfb", WorkloadHint::LinearSolve, |params| {
        hfb_objective(params, &exp_data)
    })
    .surrogate(RBFKernel::ThinPlateSpline)
    .optimizer(MultiStartNM::new(8, 100, 1e-8))
    .cache(EvaluationCache::load_or_new("cache.json"))
    .build();

let result = pipeline.run(bounds, n_rounds, candidates_per_round)?;
```

### Why This Matters

- Makes the heterogeneous pattern reusable across workloads
- Enables the `WorkloadHint` system to route each stage to optimal hardware
- Cascade statistics tracked automatically
- Cache persistence built-in

### Effort Estimate: 5-7 days (but can be iterative)

---

## Part 7: f64 Tensor & Hardware Evolution

### Context

Two Titan V GPUs are incoming. These provide native f64 at 1/2 rate (vs 1/32 on
consumer GPUs). Combined with the RTX 4070 (fast f32) and Akida NPU (pre-screening):

```
RTX 4070:   f32 champion (12 TFLOPS f32, 0.375 TFLOPS f64)
Titan V ×2: f64 capable  (7.4 TFLOPS f32, 3.7 TFLOPS f64 each)
Akida NPU:  pre-screening (1mW, event-driven binary classification)
```

### Evolution Tasks

| Task | Description | Priority | Effort |
|------|-------------|----------|--------|
| **f64 WGSL shaders** | Port `matmul_fp64.wgsl` pattern to all linalg/special shaders | HIGH (when Titan V arrives) | 2-3 weeks |
| **Multi-GPU DevicePool** | Route f32 to RTX 4070, f64 to Titan V | MEDIUM | 1-2 weeks |
| **f64 Tensor** | Generic `Tensor<T>` or `Tensor64` for end-to-end f64 | MEDIUM | 1-2 weeks |
| **GPU precision config** | `barracuda::config::Precision::F64` selects f64 shaders | MEDIUM | 1 week |
| **VFIO NPU driver** | Pure Rust Akida driver (no C kernel module) | MEDIUM | 2-3 weeks |
| **NPU model pipeline** | Train → quantize → compile → deploy from Rust | MEDIUM | 2-3 weeks |
| **Async compute streams** | Overlap CPU work with GPU dispatch | LOW | 1-2 weeks |

### f64 Shader Strategy

The `matmul_fp64.wgsl` already demonstrates the emulated f64 pattern (split into
hi/lo f32). For Titan V with native f64 support, shaders can use WGSL f64 extensions
directly. The architecture should support both:

```rust
pub enum PrecisionMode {
    F32,                    // Standard: all shaders use f32
    F64Emulated,            // No f64 hardware: split hi/lo emulation
    F64Native,              // Titan V / datacenter: native f64 in WGSL
    Mixed { threshold: usize }, // Auto: f64 for small (CPU), f32 for large (GPU)
}
```

---

## Part 8: LOO-CV for Surrogate Quality — Priority #6

### The Problem

During validation, the RBF surrogate always reports RMSE = 0.0000 at training points
(exact interpolation is expected). There's no way to assess surrogate quality without
evaluating at new points.

### What's Needed

The `loo_cv.wgsl` shader already exists. Wire it up:

```rust
// In barracuda::surrogate::RBFSurrogate
impl RBFSurrogate {
    /// Leave-one-out cross-validation RMSE
    ///
    /// For each training point, predicts using a model trained on all others.
    /// Uses the LOO-CV shader for GPU acceleration on large datasets.
    pub fn loo_cv_rmse(&self) -> f64 { ... }

    /// LOO-CV with per-point errors (for identifying outliers)
    pub fn loo_cv_errors(&self) -> Vec<f64> { ... }
}
```

### Why This Matters

- Tells us if the surrogate is actually learning the landscape
- Identifies when more training data is needed
- Detects overfitting / underfitting
- Enables adaptive stopping: "surrogate quality is good enough, stop sampling"

### Effort Estimate: 1 day

---

## Part 9: Recommended Phased Roadmap

### Phase A — Bridge & Polish (1-2 weeks)

| # | Task | Priority | Effort | Unlocks |
|---|------|----------|--------|---------|
| 1 | f64 linalg bridges (eigh, cholesky, LU, QR, SVD, tridiagonal) | 🔴 HIGH | 3-5 days | Eliminate nalgebra dependency |
| 2 | Auto-dispatch benchmarks + thresholds | 🔴 HIGH | 2-3 days | Smart CPU/GPU routing |
| 3 | EvaluationCache serialization (save/load/merge) | 🔴 HIGH | 1 day | Warm-start across runs |
| 4 | LOO-CV wiring for RBFSurrogate | 🟡 MEDIUM | 1 day | Surrogate quality metric |

### Phase B — Scientific Depth (2-3 weeks)

| # | Task | Priority | Effort | Unlocks |
|---|------|----------|--------|---------|
| 5 | Incomplete gamma + chi-squared distribution | 🟡 MEDIUM | 1-2 days | Statistical testing |
| 6 | Newton-Raphson + Brent root-finding | 🟡 MEDIUM | 1-2 days | Faster convergence |
| 7 | Cubic spline interpolation | 🟡 MEDIUM | 2 days | EOS tables |
| 8 | Gauss-Legendre quadrature | 🟡 MEDIUM | 1-2 days | High-accuracy integrals |
| 9 | Conjugate gradient optimizer | 🟡 MEDIUM | 2-3 days | Large sparse systems |
| 10 | Generalized eigenvalue Ax = λBx | 🟡 MEDIUM | 3-4 days | L3 HFB overlap |

### Phase C — Hardware Exploitation (when Titan V arrives)

| # | Task | Priority | Effort | Unlocks |
|---|------|----------|--------|---------|
| 11 | f64 Tensor type | 🟡 MEDIUM | 1-2 weeks | End-to-end f64 |
| 12 | f64 WGSL shader variants | 🟡 MEDIUM | 2-3 weeks | Full GPU f64 |
| 13 | Multi-GPU DevicePool | 🟡 MEDIUM | 1-2 weeks | RTX + Titan V routing |
| 14 | Pipeline orchestration API | 🟡 MEDIUM | 5-7 days | Declarative heterogeneous compute |

### Phase D — Advanced (as workloads demand)

| # | Task | Priority | Effort | Unlocks |
|---|------|----------|--------|---------|
| 15 | Arbitrary-order Bessel Jₙ, Iₙ, Kₙ | 🟢 LOW | 2-3 days | Nuclear wavefunctions |
| 16 | Spherical Bessel, Airy, hypergeometric, elliptic | 🟢 LOW | 5-7 days | L3 advanced physics |
| 17 | Differential evolution + Bayesian optimization | 🟢 LOW | 5-7 days | Global optimization |
| 18 | Gaussian Process surrogate | 🟢 LOW | 3-5 days | Better surrogate models |
| 19 | VFIO NPU driver + model pipeline | 🟢 LOW | 4-6 weeks | Pure Rust NPU |

### Critical Path

```
Week 1-2: Phase A (bridge, dispatch, cache)
Week 3-4: Phase B (scientific functions)
Week 5+:  Phase C (when hardware arrives)
Ongoing:  Phase D (workload-driven)
```

---

## Part 10: Validation Strategy

### How hotSpring Will Validate

Every new BarraCuda function will be validated in hotSpring using the established
pattern:

```
hotSpring/barracuda/src/bin/validate_*.rs
```

Current validation suite:
- `validate_special_functions` — 69 tests against analytical/scipy
- `validate_linalg` — 10 tests against analytical
- `validate_optimizers` — 22 tests against known minima/solutions
- `validate_md` — 20 tests against analytical physics

New validation binaries will be added as new functions land:
- `validate_rootfinding` — Newton-Raphson, Brent vs bisection
- `validate_interpolation` — Cubic spline vs scipy.interpolate
- `validate_statistics` — Chi² distribution, incomplete gamma vs scipy
- `validate_gen_eigh` — Generalized eigenvalue vs scipy.linalg.eigh

### The Control Experiment Pattern

```
Python control (scipy/numpy)  ←→  BarraCuda (Rust/WGSL)
         ↓                              ↓
    reference results              candidate results
         ↓                              ↓
                 comparison.json
                      ↓
            accuracy + speedup metrics
```

hotSpring commits results as JSON to `control/surrogate/nuclear-eos/results/`
for longitudinal tracking.

---

## Part 11: Key Lessons from hotSpring

### 1. GPU Dispatch Overhead Matters

Single-point predictions in inner optimization loops must use CPU. The auto-dispatch
system (Part 3) prevents this from being a recurring issue.

### 2. The Surrogate Learning Accuracy Gap Is Algorithmic

BarraCuda's math is correct (121/121 tests). The remaining accuracy gap
(L2 χ²=51,713 vs Python's 61.87) comes from:
- Surrogate learning strategy (how samples are selected)
- Cascade filter tuning (NMP/SEMF thresholds)
- Classifier recall (needs more training data)

These are application-level tuning, not library bugs.

### 3. Pre-Screening Cascades Are Powerful

The heterogeneous L2 pipeline filters 91.9% of candidates before expensive HFB:
- Tier 1 (NMP): 79% rejection at ~1μs/candidate
- Tier 2 (SEMF): 13% rejection at ~0.1ms/candidate
- This saves ~5,500 HFB evaluations (~18 minutes of compute)

The cascade pattern should be a first-class library concept.

### 4. f64 vs f32 Trade-offs Are Workload-Specific

- Distance computation (cdist): f32 is fine → GPU shader
- Kernel evaluation: f64 needed → CPU
- Linear solve: f64 needed → CPU
- Force computation: f32 is fine → GPU shader
- Eigendecomposition: f64 needed → CPU (or Titan V)

The dual-precision architecture is correct. The key is making it invisible
to the user through auto-dispatch.

### 5. NMP-Aware Surrogates Improve Cascade Pass Rates

When the surrogate objective penalizes NMP-violating regions (returning 1e10),
the Nelder-Mead optimizer is guided away from unphysical regions. This improved
the cascade pass rate from 0.8% to 8.1% — a 10× improvement.

This pattern (physics-informed surrogate) should be documented as a best practice.

---

## Summary

BarraCuda's evolution is at an inflection point. The breadth is extraordinary
(436 shaders, 15 special functions, 5 MD force kernels, 4 optimizers, full FFT).
The correctness is proven (121/121 validation tests).

The next phase is about **depth and polish**:

1. **Bridge the f64 gap** — make `linalg` a complete f64 API
2. **Auto-dispatch everything** — users should never manually route CPU/GPU
3. **Persist evaluation data** — expensive computations should survive across runs
4. **Orchestrate heterogeneous pipelines** — multi-tier compute as a library concept
5. **Fill the remaining math** — incomplete gamma, splines, root-finders, as needed

The team has built something remarkable. These evolution steps will turn it from
a great foundation into a self-contained scientific computing platform that replaces
scipy + numpy + PyTorch for any Rust workload.

---

**Repository**: [hotSpring](https://github.com/syntheticChemistry/hotSpring)
**Validation Data**: `hotSpring/control/surrogate/nuclear-eos/results/`
**Validation Binaries**: `hotSpring/barracuda/src/bin/validate_*.rs`
**Previous Handoffs**: `wateringHole/handoffs/BARRACUDA_*.md`

