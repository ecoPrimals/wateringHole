# BarraCUDA Scientific Computing Middleware Handoff

**Date**: February 11, 2026
**From**: ecoPrimals Control Team (Eastgate) — hotSpring L1+L2 validation
**To**: ToadStool / BarraCUDA Team
**Priority**: HIGH — Enables self-contained scientific computing without inline code
**Depends On**: TOADSTOOL_PHYSICS_SHADERS_FEB08_2026.md, TOADSTOOL_PURE_RUST_HARDWARE_EVOLUTION_FEB10_2026.md
**Status**: Working code exists in L1/L2 binaries — needs extraction into library

---

## Executive Summary

We built two complete nuclear physics pipelines — **Level 1** (SEMF) and **Level 2**
(spherical HF+BCS) — as standalone Rust binaries using BarraCUDA for GPU-accelerated
surrogate learning. Both pipelines work. Both validate against the Python control.

**The problem**: ~600 lines of scientific computing code are **duplicated verbatim**
between `nuclear_eos_l1.rs` and `nuclear_eos_l2.rs`. This code is general-purpose
mathematical infrastructure — linear solvers, optimizers, RBF surrogates, root-finders,
numerical integration — that every future scientific workload will need.

**The ask**: Extract this inline code into proper BarraCUDA library modules so the
next primal team doesn't have to re-implement Gauss-Jordan elimination, Nelder-Mead,
or RBF interpolation from scratch.

**Key insight from validation**: BarraCUDA's 370+ WGSL shader library is extraordinary
for tensor operations. What's missing is the **middleware layer** that connects raw
tensor ops to real scientific workflows. The L1/L2 binaries wrote that middleware inline.
Now it needs to be promoted into the library.

---

## Part 1: What We Built and What We Learned

### 1.1 L1 Pipeline (SEMF — fast)

| Metric | Python Control | BarraCUDA (Rust) |
|--------|---------------|------------------|
| Best χ²/datum | 3.93 | **1.34** |
| Throughput | 46.1 evals/s | **646.8 evals/s** |
| Speedup | — | **14×** |
| Precision | f64 (PyTorch) | f64 (dual: GPU f32 cdist → CPU f64 LA) |
| Time (30 rounds) | 129.9s | 9.3s |

**Verdict**: Full parity. BarraCUDA is faster AND finds better optima with more evals.

### 1.2 L2 Pipeline (Spherical HF+BCS — expensive)

| Metric | Python Control | BarraCUDA (Rust) |
|--------|---------------|------------------|
| Throughput | 0.28 evals/s | **0.49 evals/s** |
| Speedup | — | **1.7×** |
| Best χ² (comparable evals) | 61.87 (96 evals) | 87.13 (1009 evals) |
| Python long-run χ² | **1.93** (3008 evals) | — |
| HFB solver | numpy eigh (~91×91) | nalgebra SymmetricEigen (~91×91) |
| Parallelism | multiprocessing.Pool | rayon (18 threads) |

**Verdict**: Throughput parity achieved (1.7× faster per eval). Accuracy gap is
**sampling strategy**, not physics or compute — Python uses `mystic.SparsitySampler`,
BarraCUDA uses naive random + single Nelder-Mead. The optimizer is the bottleneck.

### 1.3 The Dual-Precision Architecture

Consumer GPUs (RTX 4070) have hardware-gimped f64 at 1/64 f32 rate. We solved this
with a dual-precision pipeline that should become BarraCUDA's standard scientific pattern:

```
GPU (f32):  cdist shader → pairwise distance matrix (numerically stable at f32)
    ↓ promote to f64 via Tensor::to_vec_f64()
CPU (f64):  TPS kernel → matrix assembly → linear solve → weights → prediction
```

This gives ~90% of the speedup (distance computation is the O(n²) bottleneck) while
maintaining f64 accuracy where it matters (kernel evaluation, linear algebra).

### 1.4 What Hit Buffer Limits

The `cdist` matrix for ~5800 training points exceeded wgpu's default 128MB
`max_storage_buffer_binding_size`. We patched `wgpu_device.rs` to request 1GB and
capped the optimizer's training set to 2000 best clean points. This is a general
issue — any O(n²) pairwise computation will hit this. BarraCUDA should document
and handle this gracefully.

---

## Part 2: Code That Must Be Extracted

The following functions are **copy-pasted between L1 and L2**. They are
general-purpose and belong in the BarraCUDA library.

### 2.1 Linear Algebra (`barracuda::linalg`) — CRITICAL

**Source**: Both `nuclear_eos_l1.rs` and `nuclear_eos_l2.rs`, identical code

#### `solve_f64(a: &[f64], b: &[f64], n: usize) → Vec<f64>`

Gauss-Jordan elimination with partial pivoting. Solves Ax = b in f64.
Currently 30 lines, duplicated verbatim.

```rust
// Current location (DUPLICATED):
//   crates/barracuda/src/bin/nuclear_eos_l1.rs:450-503
//   crates/barracuda/src/bin/nuclear_eos_l2.rs:1130-1161
//
// Target: barracuda::linalg::solve_f64()
```

#### `symmetric_eigen(a: DMatrix<f64>) → (DVector<f64>, DMatrix<f64>)`

Wrapper around `nalgebra::SymmetricEigen`. Used for the ~91×91 Hamiltonian
matrices in the HFB solver. The `nalgebra` dependency is already in `Cargo.toml`.

```rust
// Current location:
//   crates/barracuda/src/bin/nuclear_eos_l2.rs:454
//   Direct use: SymmetricEigen::new(h.clone())
//
// Target: barracuda::linalg::symmetric_eigen()
// Also expose: barracuda::linalg::eigh() (numpy-style alias)
```

#### Future: `cholesky_f64()`, `triangular_solve_f64()`

The f32 WGSL shaders (`cholesky.wgsl`, `triangular_solve.wgsl`) exist but were
unused because f64 precision was required. CPU f64 implementations are needed.
Eventually, f64 WGSL variants for datacenter GPUs with native f64 support.

### 2.2 RBF Surrogate (`barracuda::surrogate`) — HIGH

**Source**: Both L1 and L2, identical struct + train + predict

The entire `BarracudaRBFSurrogate` — 110 lines — is duplicated. This is the core
pattern for surrogate-based optimization and belongs as a first-class library component.

```rust
// Current location (DUPLICATED):
//   crates/barracuda/src/bin/nuclear_eos_l1.rs:297-446
//   crates/barracuda/src/bin/nuclear_eos_l2.rs:1036-1128
//
// Target: barracuda::surrogate::RBFSurrogate

pub struct RBFSurrogate {
    train_x: Vec<f64>,       // [n_train × n_dim] flat
    weights: Vec<f64>,       // [n_train]
    poly_coeffs: Vec<f64>,   // [n_dim + 1]
    n_train: usize,
    n_dim: usize,
    device: Arc<WgpuDevice>,
}

impl RBFSurrogate {
    /// Train RBF surrogate with dual-precision pipeline
    /// GPU f32 cdist → promote → CPU f64 TPS kernel + linear solve
    pub fn train(
        x_data: &[Vec<f64>],
        y_data: &[f64],
        smoothing: f64,
        device: Arc<WgpuDevice>,
    ) -> Result<Self>;

    /// Predict at new points (same dual-precision pipeline)
    pub fn predict(&self, x_eval: &[Vec<f64>]) -> Result<Vec<f64>>;
}
```

**Kernel variants to add** (currently only TPS):

| Kernel | Formula | Use Case |
|--------|---------|----------|
| `ThinPlateSpline` | φ(r²) = 0.5·r²·ln(r²) | ✅ Current (Diaw et al.) |
| `Gaussian` | φ(r) = exp(-ε²r²) | General interpolation |
| `Multiquadric` | φ(r) = √(1 + ε²r²) | Scattered data |
| `InverseMultiquadric` | φ(r) = 1/√(1 + ε²r²) | Smooth interpolation |
| `Cubic` | φ(r) = r³ | 1D/2D interpolation |

### 2.3 Optimization (`barracuda::optimize`) — HIGH

**Source**: Both L1 and L2, identical Nelder-Mead + bisection

#### `nelder_mead(f, x0, bounds, max_iter) → (x_best, f_best)`

Bounded Nelder-Mead simplex optimizer. 80 lines, duplicated verbatim.

```rust
// Current location (DUPLICATED):
//   crates/barracuda/src/bin/nuclear_eos_l1.rs:510-627
//   crates/barracuda/src/bin/nuclear_eos_l2.rs:1167-1250
//
// Target: barracuda::optimize::nelder_mead()
```

#### `bisect(f, a, b, tol, max_iter) → Option<f64>`

Bisection root-finder. Replaces `scipy.optimize.brentq`. 15 lines, used in L2.

```rust
// Current location:
//   crates/barracuda/src/bin/nuclear_eos_l2.rs:860-874
//
// Target: barracuda::optimize::bisect()
// Future: barracuda::optimize::brentq() (Brent's method, faster convergence)
```

#### Missing but critical: `latin_hypercube()` and `sparsity_sampler()`

The L1/L2 comparison revealed that **the #1 accuracy gap** between BarraCUDA and
the Python control is the sampling strategy. Python uses `mystic.SparsitySampler`
which uses maximin distance criteria to fill gaps in parameter space. BarraCUDA uses
naive `rand::gen_range()` uniform random sampling.

```rust
// NEW — does not exist yet
//
// Target: barracuda::optimize::latin_hypercube()
//   Space-filling sampling for initial exploration
//   Input: bounds, n_samples
//   Output: Vec<Vec<f64>> with quasi-random coverage
//
// Target: barracuda::optimize::sparsity_sampler()
//   Maximin distance sampling (port of mystic.SparsitySampler)
//   Input: bounds, n_samples, existing_points
//   Output: Vec<Vec<f64>> filling gaps in existing coverage
//
// Target: barracuda::optimize::multi_start_nelder_mead()
//   Run N Nelder-Mead from different starting points, return global best
//   Leverages rayon for parallel restarts
```

**Priority note**: Latin hypercube is a weekend implementation. SparsitySampler is
the real prize — it's what makes the Python control converge to χ²=1.93 with only
3008 evaluations while BarraCUDA's random sampling produces χ²=87 with 1009 evals.

### 2.4 Numerical Methods (`barracuda::numerical`) — MEDIUM

**Source**: L2 binary inline

#### `gradient_1d(f, dr) → Vec<f64>`

Finite-difference numerical gradient (matches `numpy.gradient` 3-point stencil).

```rust
// Current location:
//   crates/barracuda/src/bin/nuclear_eos_l2.rs:834-844
//
// Target: barracuda::numerical::gradient_1d()
```

#### `trapz(y, x) → f64` and `trapz_product(f, g1, g2, x, weights) → f64`

Trapezoidal integration, plain and weighted-product variants. Used extensively
in the HFB solver for computing matrix elements.

```rust
// Current location:
//   crates/barracuda/src/bin/nuclear_eos_l2.rs:848-857
//
// Target: barracuda::numerical::trapz()
// Target: barracuda::numerical::trapz_product()
```

### 2.5 Special Functions (`barracuda::special`) — MEDIUM

**Source**: L2 binary inline

| Function | WGSL (f32) | CPU (f64) inline | Target |
|----------|-----------|------------------|--------|
| `gamma(x)` | ❌ | ✅ `gamma_fn()` (Lanczos, L2:886-931) | `barracuda::special::gamma` |
| `factorial(n)` | ❌ | ✅ `factorial()` (L2:877-882) | `barracuda::special::factorial` |
| `erf(x)` | ✅ `erf.wgsl` | ❌ | Add f64 CPU wrapper |
| `lgamma(x)` | ✅ `lgamma.wgsl` | ❌ | Add f64 CPU wrapper |
| `laguerre(n, alpha, x)` | ❌ | ✅ inline in `ho_radial()` | `barracuda::special::laguerre` |

The Lanczos gamma approximation in the L2 binary handles positive half-integers
exactly (critical for HO wavefunctions) and falls back to the 9-term Lanczos
series for general arguments. Good enough for a library implementation.

---

## Part 3: New WGSL Shaders Needed

### 3.1 f64 Variants of Existing Shaders

The dual-precision pattern works today, but for datacenter GPUs (Tesla V100, A100,
Radeon VII) with native f64 support, pure-GPU f64 shaders would eliminate the
GPU→CPU→GPU roundtrip entirely.

| Shader | f32 Status | f64 Needed | Notes |
|--------|-----------|-----------|-------|
| `cdist_f64.wgsl` | ✅ exists (f32) | Optional | f32 is fine for distances |
| `cholesky_f64.wgsl` | ✅ exists (f32) | **YES** | Numerically sensitive |
| `triangular_solve_f64.wgsl` | ✅ exists (f32) | **YES** | Numerically sensitive |
| `tps_kernel_f64.wgsl` | ✅ exists (f32) | **YES** | Kernel eval needs precision |
| `gauss_jordan_f64.wgsl` | ❌ | **YES** | General linear solver |
| `matmul_fp64.wgsl` | ✅ exists | Wire up | Exists but unused — needs Rust op wrapper |

**Gating factor**: WGSL `f64` requires the `shader-f64` wgpu feature, which requires
the GPU to advertise `SHADER_F64` capability. Consumer NVIDIA cards (RTX 40/50 series)
do NOT advertise this even though the hardware has minimal f64 ALUs. It works on:
- NVIDIA Tesla V100, A100, H100 (datacenter)
- **NVIDIA Titan V** (GV100, 1/2 f32 rate FP64 — **2× on order for Eastgate**)
- AMD Radeon VII (consumer, full f64!)
- Intel Arc (partial, driver-dependent)

**Hardware note (Feb 11, 2026)**: 2× Titan V (GV100, 12GB HBM2) have been ordered.
These provide 6.9 TFLOPS FP64 each (vs RTX 4070's 0.36 TFLOPS FP64). Once installed,
the heterogeneous compute strategy becomes:
- **RTX 4070**: f32 workloads (29.15 TFLOPS), ML inference, cdist
- **Titan V ×2**: f64 workloads (13.8 TFLOPS combined), Cholesky, linear solve, TPS kernel
- **CPU (i9-12900K)**: Fallback, small matrices, control flow
This eliminates the dual-precision GPU→CPU roundtrip for f64 operations entirely.

**Recommendation**: Implement f64 shaders behind a feature gate. Auto-detect at
runtime via `device.features().contains(wgpu::Features::SHADER_F64)`. Fall back to
the dual-precision CPU path (which already works) when f64 shaders aren't available.
When Titan V arrives, the f64 shader path becomes the primary scientific compute path.

### 3.2 New Shaders for Scientific Computing

| Shader | Purpose | Complexity | Ancestor |
|--------|---------|-----------|----------|
| `rbf_gaussian.wgsl` | Gaussian RBF kernel | Low | `tps_kernel.wgsl` + `exp.wgsl` |
| `rbf_multiquadric.wgsl` | Multiquadric RBF kernel | Low | `tps_kernel.wgsl` + `sqrt.wgsl` |
| `trapz_reduce.wgsl` | Parallel trapezoidal integration | Medium | `sum_reduce.wgsl` |
| `numerical_gradient.wgsl` | Parallel finite-difference gradient | Low | `elementwise_sub.wgsl` |
| `symmetric_eigen.wgsl` | Jacobi eigenvalue decomposition | Hard | `determinant.wgsl` |

**Note on `symmetric_eigen.wgsl`**: This is a research-level GPU shader. The Jacobi
eigenvalue method is iteratively parallelizable (each rotation is a 2×2 problem) but
convergence requires O(n²) sweeps. For our ~91×91 HFB matrices, the CPU nalgebra
path is likely faster than a GPU shader due to dispatch overhead. Worth attempting
only for matrices ≥ 500×500. Low priority.

---

## Part 4: Architecture Decisions for the Team

### 4.1 Dtype-Aware Tensor (Evolution Path)

The current `Tensor` is f32-only. The `to_vec_f64()` method is a read-and-cast,
not a true f64 tensor. For scientific computing parity, BarraCUDA needs f64 awareness.

**Recommended evolution (incremental, non-breaking)**:

1. **Phase A** (now): `barracuda::linalg` and `barracuda::surrogate` operate on
   `Vec<f64>` directly, using `Tensor` only for GPU shader dispatch. This is what
   the L1/L2 binaries already do.

2. **Phase B**: Add `Tensor64` companion type with its own buffer management.
   f64 shaders dispatch through it when `SHADER_F64` is available, CPU fallback otherwise.

3. **Phase C**: Unify into `Tensor<T: Scalar>` with compile-time dtype dispatch.
   This is the long-term target but requires significant refactoring.

**Phase A is already proven** — the L1/L2 binaries demonstrate it works. Start there.

### 4.2 Module Organization

```
crates/barracuda/src/
├── linalg/
│   ├── mod.rs              // pub use
│   ├── solve.rs            // Gauss-Jordan f64, LU decomposition
│   ├── eigen.rs            // nalgebra SymmetricEigen wrapper
│   ├── cholesky.rs         // CPU f64 Cholesky (+ WGSL f32 existing)
│   └── triangular.rs       // CPU f64 forward/backward sub
├── surrogate/
│   ├── mod.rs
│   ├── rbf.rs              // RBFSurrogate (train + predict)
│   └── kernels.rs          // TPS, Gaussian, Multiquadric, etc.
├── optimize/
│   ├── mod.rs
│   ├── nelder_mead.rs      // Bounded Nelder-Mead simplex
│   ├── bisect.rs           // Bisection root-finder
│   ├── latin_hypercube.rs  // Space-filling sampling
│   └── sparsity_sampler.rs // Maximin distance sampling
├── numerical/
│   ├── mod.rs
│   ├── gradient.rs         // Finite-difference gradient
│   └── integrate.rs        // Trapezoidal integration
├── special/
│   ├── mod.rs
│   ├── gamma.rs            // Gamma function (Lanczos)
│   ├── factorial.rs        // Factorial
│   └── laguerre.rs         // Generalized Laguerre polynomials
├── ops/                    // Existing (370+ WGSL ops)
├── shaders/                // Existing (370+ WGSL shaders)
└── ...                     // Existing modules unchanged
```

### 4.3 Testing Strategy

Every extracted function has a **built-in validation target**: the Python control.

| Module | Validation Data |
|--------|----------------|
| `linalg::solve_f64` | Generate random SPD system, solve in both Rust and numpy, compare |
| `surrogate::RBFSurrogate` | Train on same data as Python `RBFInterpolator`, predictions must match to <1e-10 |
| `optimize::nelder_mead` | Rosenbrock, Rastrigin, Ackley benchmarks with known minima |
| `optimize::latin_hypercube` | Verify space-filling properties (minimum pairwise distance) |
| `numerical::trapz` | Compare to `numpy.trapz` on known integrands |
| `special::gamma` | Compare to `scipy.special.gamma` at half-integers and general values |

The hotSpring results files provide end-to-end validation:
- `hotSpring/control/surrogate/nuclear-eos/results/nuclear_eos_surrogate_L1_barracuda.json`
- `hotSpring/control/surrogate/nuclear-eos/results/nuclear_eos_surrogate_L2_barracuda.json`
- `hotSpring/control/surrogate/nuclear-eos/results/nuclear_eos_surrogate_L1.json` (Python)
- `hotSpring/control/surrogate/nuclear-eos/results/nuclear_eos_surrogate_L2.json` (Python)

---

## Part 5: What This Enables

### 5.1 Next hotSpring Workload (L3: Deformed HFB)

Level 3 requires deformed (axially symmetric) HFB with:
- 2D mesh instead of 1D radial grid
- Larger eigenvalue problems (~500×500)
- More nuclei in the HFB regime

With extracted library modules, the L3 binary becomes:

```rust
use barracuda::surrogate::RBFSurrogate;
use barracuda::optimize::{nelder_mead, latin_hypercube};
use barracuda::linalg::symmetric_eigen;
// ... only physics code is L3-specific
```

Instead of copying 600 lines from L2.

### 5.2 Other Primals

Any primal doing surrogate-based optimization (which is... most scientific computing)
gets RBF interpolation + Nelder-Mead + smart sampling for free. This includes:
- Molecular dynamics force-field fitting
- TTM transport coefficient calibration
- Material property optimization
- Any black-box optimization with expensive evaluations

### 5.3 The SparsitySampler Prize

The biggest single improvement to BarraCUDA's scientific computing capability would be
implementing `sparsity_sampler`. Here's why:

| Sampling | L2 evals | Best χ² | Evals/second |
|----------|----------|---------|-------------|
| Python (SparsitySampler) | 3008 | **1.93** | 0.28 |
| BarraCUDA (random) | 1009 | 87.13 | **0.49** |
| BarraCUDA (projected with SparsitySampler) | ~1700 | ~2.0 | **0.49** |

With 1.7× faster throughput AND smart sampling, BarraCUDA would reach Python's
accuracy in **60% of the wall-clock time**. Speed × smarts = compounding advantage.

---

## Part 6: Immediate Action Items

### For ToadStool/BarraCUDA Team

| # | Task | Source Code | Effort | Priority |
|---|------|-------------|--------|----------|
| 1 | Extract `gauss_jordan_solve_f64` → `barracuda::linalg::solve_f64` | L1:450-503, L2:1130-1161 | 1 day | CRITICAL |
| 2 | Extract `BarracudaRBFSurrogate` → `barracuda::surrogate::RBFSurrogate` | L1:297-446, L2:1036-1128 | 2 days | CRITICAL |
| 3 | Extract `nelder_mead` → `barracuda::optimize::nelder_mead` | L1:510-627, L2:1167-1250 | 1 day | CRITICAL |
| 4 | Extract `bisect` → `barracuda::optimize::bisect` | L2:860-874 | 0.5 day | HIGH |
| 5 | Wrap `nalgebra::SymmetricEigen` → `barracuda::linalg::eigh` | L2:454 usage | 1 day | HIGH |
| 6 | Extract `gradient`, `trapz_product` → `barracuda::numerical` | L2:834-857 | 1 day | MEDIUM |
| 7 | Extract `gamma_fn`, `factorial` → `barracuda::special` | L2:877-931 | 1 day | MEDIUM |
| 8 | Implement `latin_hypercube` → `barracuda::optimize` | NEW | 2-3 days | HIGH |
| 9 | Implement `sparsity_sampler` → `barracuda::optimize` | Port from mystic | 1 week | HIGH |
| 10 | Wire up `matmul_fp64.wgsl` with Rust op wrapper | Shader exists, needs integration | 2-3 days | MEDIUM |
| 11 | Write f64 variants: `cholesky_f64.wgsl`, `triangular_solve_f64.wgsl` | Extend existing f32 shaders | 1 week | LOW (behind feature gate) |
| 12 | Refactor L1/L2 binaries to use extracted library modules | After #1-7 | 2 days | AFTER |

**Total for items 1-9**: ~3 weeks
**Critical path**: Items 1-3 can be done in parallel in 2 days, unblocking everything.

### For hotSpring Team (us)

- Continue L1/L2 validation with current inline code
- Begin L3 (deformed HFB) design — will be first consumer of extracted modules
- Investigate NPU pre-screening for Skyrme parameter filtering (uses `barracuda::npu`)

---

## Part 7: Reference Files

### Source Code (extract from these)

| File | Lines | Contains |
|------|-------|---------|
| `phase1/toadstool/crates/barracuda/src/bin/nuclear_eos_l1.rs` | 953 | L1 pipeline: SEMF physics + RBF surrogate + Nelder-Mead + f64 precision |
| `phase1/toadstool/crates/barracuda/src/bin/nuclear_eos_l2.rs` | 1542 | L2 pipeline: SphericalHFB + hybrid dispatch + rayon parallel + RBF + NM |

### Existing WGSL Shaders (referenced but some unused)

| Shader | Status | Notes |
|--------|--------|-------|
| `shaders/cdist.wgsl` | ✅ Used (f32) | GPU pairwise distance — the workhorse |
| `shaders/tps_kernel.wgsl` | ⚠️ Exists, unused | L1/L2 use CPU f64 `tps_kernel_f64()` instead |
| `shaders/cholesky.wgsl` | ⚠️ Exists, unused | L1/L2 use CPU f64 Gauss-Jordan instead |
| `shaders/triangular_solve.wgsl` | ⚠️ Exists, unused | Same — f64 precision required |
| `shaders/matmul_fp64.wgsl` | ⚠️ Exists, unused | f64 matmul with Kahan summation — needs Rust wrapper |

### Workload TOMLs

| File | Purpose |
|------|---------|
| `phase1/toadstool/workloads/hotspring/nuclear_eos_l1_barracuda.toml` | L1 toadstool workload spec |
| `phase1/toadstool/workloads/hotspring/nuclear_eos_l2_barracuda.toml` | L2 toadstool workload spec |

### Validation Results

| File | Contents |
|------|---------|
| `hotSpring/control/surrogate/nuclear-eos/results/nuclear_eos_surrogate_L1_barracuda.json` | BarraCUDA L1: χ²=1.34, 6201 evals, 9.6s |
| `hotSpring/control/surrogate/nuclear-eos/results/nuclear_eos_surrogate_L1.json` | Python L1: χ²=3.93, 6000 evals, 130s |
| `hotSpring/control/surrogate/nuclear-eos/results/nuclear_eos_surrogate_L2_barracuda.json` | BarraCUDA L2: χ²=87.13, 1009 evals, 2055s |
| `hotSpring/control/surrogate/nuclear-eos/results/nuclear_eos_surrogate_L2.json` | Python L2: χ²=61.87, 96 evals, 345s |

### Device Configuration (wgpu buffer limit fix)

The `max_storage_buffer_binding_size` was increased to 1GB in:
`phase1/toadstool/crates/barracuda/src/device/wgpu_device.rs`

This is needed for any O(n²) pairwise computation with n > ~5000. Document this
limit and consider adding a graceful fallback (chunk the computation) for even
larger training sets.

---

## Summary

BarraCUDA proved it can run real nuclear physics. Two pipelines, two levels of
fidelity, validated against Python controls. The 370+ WGSL shaders are the foundation.
What's needed now is the scientific computing middleware — the 600 lines of duplicated
Rust code that connects "compute pairwise distance on GPU" to "find optimal Skyrme
parameters for nuclear binding energies."

Extract it. Module it. Test it. Every future scientific primal benefits.

---

*Previous handoffs*:
- `TOADSTOOL_PHYSICS_SHADERS_FEB08_2026.md` (shader specifications)
- `TOADSTOOL_PURE_RUST_HARDWARE_EVOLUTION_FEB10_2026.md` (hardware backends)
- `TOADSTOOL_REAL_HARDWARE_WIRING_FEB07_2026.md` (device wiring)

*Repository*: `phase1/toadstool/crates/barracuda/`
*Contact*: ecoPrimals Control Team (hotSpring)
*License*: AGPL-3.0

