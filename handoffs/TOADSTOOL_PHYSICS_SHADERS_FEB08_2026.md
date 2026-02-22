# ToadStool Physics Shaders Handoff
## February 8, 2026

**From**: ecoPrimals/hotSpring Control Experiment Team  
**To**: ToadStool Maintainers  
**Priority**: HIGH — New shaders required for Phase B scientific computing  
**Depends On**: Previous handoff (TOADSTOOL_REAL_HARDWARE_WIRING_FEB07_2026.md)  
**Status**: Specifications ready, implementation can begin

---

## Executive Summary

The hotSpring control experiments (81/81 quantitative checks pass) have produced
a concrete shopping list of BarraCuda shaders and operations needed to run
real scientific computing workloads across CPU, GPU, and NPU.

**This is the Phase A → Phase B transition.** Python proved the physics is correct.
BarraCuda now needs to prove it can do the same math on any chip.

The surrogate learning workflow is the first target: we have a working Python
implementation (9 objectives validated, physics EOS converged in 11 rounds).
BarraCuda needs 4 new capabilities to replicate it on GPU, with inference on NPU.

---

## Context: What hotSpring Proved

### Sarkas MD Control (12 cases, 60/60 checks)
- `force_pp.update()` is **97.2% of runtime** → primary GPU offload target
- The inner loop is: pairwise distance → force lookup → acceleration accumulate
- Maps directly to `cdist.wgsl` → force kernel → reduction
- 5 upstream Python bugs found (silent failures) — BarraCuda eliminates this class

### TTM Control (6/6 checks)
- Zbar solver needs `scipy.optimize.root` equivalent → requires ODE/rootfinding
- Cylindrical diffusion needs 1D finite-difference stencil → simple shader
- Saha ionization lookup needs interpolation → tabulated function shader

### Surrogate Learning Control (15/15 checks + iterative workflow)
- RBF surrogate training is the immediately actionable workload
- 75% of the math already exists in BarraCuda (cdist, exp, matmul, sum)
- 4 new shaders close the gap completely

---

## New Shaders Required

### Priority 1: Surrogate Learning Pipeline (4 weeks)

These enable BarraCuda to train and evaluate RBF surrogates — the same workload
that Python/SciPy currently does. Once implemented, we can show:
- Same training data → same surrogate → same predictions
- GPU training, NPU inference, CPU fallback — identical results

#### 1.1 Cholesky Decomposition (`cholesky.wgsl`) — 2 weeks

**What**: Decompose symmetric positive-definite matrix K = LLᵀ  
**Why**: RBF kernel matrix solve (K·w = y → solve via Cholesky)  
**Ancestor**: `inverse.wgsl` (same matrix traversal pattern)  
**Size**: Typically N ≤ 30,000 (training set size)

```
Input:  K[N×N] symmetric positive-definite (kernel matrix)
Output: L[N×N] lower triangular

Algorithm:
  for j = 0..N:
    L[j,j] = sqrt(K[j,j] - Σ L[j,k]² for k<j)
    for i = j+1..N:
      L[i,j] = (K[i,j] - Σ L[i,k]*L[j,k] for k<j) / L[j,j]

GPU strategy:
  - Column-parallel: each column j is sequential (dependency)
  - Within column: rows i > j are parallel (independent)
  - Blocked variant for large N (tile into 32×32 or 64×64 blocks)
```

**Deliverable**: `crates/barracuda/src/ops/linalg/cholesky.wgsl`  
**Test**: A = LLᵀ (reconstruction error < 1e-6), known SPD matrices  
**Rust op**: `Cholesky::new(tensor) → (L, L_transpose)`

#### 1.2 Triangular Solve (`triangular_solve.wgsl`) — 1 week

**What**: Solve Lx = b (forward substitution) and Lᵀx = b (back substitution)  
**Why**: After Cholesky, solve for RBF weights: Lz = y, then Lᵀw = z  
**Ancestor**: `inverse.wgsl` (column operations)

```
Input:  L[N×N] lower triangular, b[N]
Output: x[N] such that Lx = b

Algorithm (forward sub):
  x[0] = b[0] / L[0,0]
  for i = 1..N:
    x[i] = (b[i] - Σ L[i,j]*x[j] for j<i) / L[i,i]

GPU strategy:
  - Batch: solve multiple RHS in parallel (b is often [N×M])
  - Each RHS is sequential (dependency chain)
  - Wavefront parallel for large N
```

**Deliverable**: `crates/barracuda/src/ops/linalg/triangular_solve.wgsl`  
**Test**: L·(solve(L, b)) == b (residual < 1e-6)  
**Rust op**: `TriangularSolve::new(L, b, lower=true) → x`

#### 1.3 RBF Kernel Evaluation (`rbf_kernel.wgsl`) — 3 days

**What**: Compute kernel matrix K[i,j] = φ(‖xᵢ - xⱼ‖) for various kernels  
**Why**: RBF surrogate training and evaluation  
**Ancestor**: `cdist.wgsl` (pairwise distance) + `exp`/`pow` (element-wise)

```
Input:  X[N×d], Y[M×d], kernel_type, epsilon
Output: K[N×M]

Kernels:
  thin_plate_spline: φ(r) = r² · log(r)     (paper's default)
  gaussian:          φ(r) = exp(-ε²r²)
  multiquadric:      φ(r) = sqrt(1 + ε²r²)
  inverse_mq:        φ(r) = 1/sqrt(1 + ε²r²)
  cubic:             φ(r) = r³

GPU strategy:
  - Compose cdist + element-wise kernel application
  - Fused shader: distance + kernel in single pass (avoid N×M intermediate)
  - Each (i,j) pair is independent → fully parallel
```

**Deliverable**: `crates/barracuda/src/ops/interpolation/rbf_kernel.wgsl`  
**Test**: Known RBF interpolation problems with analytic solutions  
**Rust op**: `RbfKernel::new(X, Y, kernel="thin_plate_spline", epsilon=1.0) → K`

#### 1.4 RBF Interpolator (Rust composition) — 1 week

**What**: Full RBF interpolation: train (fit weights) + evaluate (predict)  
**Why**: Replaces `scipy.interpolate.RBFInterpolator` on GPU  
**Ancestor**: Composition of 1.1 + 1.2 + 1.3

```rust
pub struct RbfInterpolator {
    training_points: Tensor,  // [N×d]
    weights: Tensor,          // [N]
    kernel: RbfKernelType,
    epsilon: f32,
}

impl RbfInterpolator {
    pub fn fit(X: &Tensor, y: &Tensor, kernel: RbfKernelType) -> Self {
        let K = RbfKernel::new(X, X, kernel, epsilon);    // 1.3
        let L = Cholesky::new(&K);                         // 1.1
        let weights = TriangularSolve::solve(&L, y);       // 1.2 (2x)
        Self { training_points: X.clone(), weights, kernel, epsilon }
    }

    pub fn predict(&self, X_new: &Tensor) -> Tensor {
        let K = RbfKernel::new(X_new, &self.training_points, self.kernel, self.epsilon);
        K.matmul(&self.weights)  // existing matmul op
    }
}
```

**Deliverable**: `crates/barracuda/src/ops/interpolation/rbf.rs`  
**Test**: Train on sin(x), predict at intermediate points, error < 1e-4  
**Validation**: Same training data as Python `RBFInterpolator` → same predictions (< 1e-6 diff)

---

### Priority 2: MD Force Pipeline (6 weeks, after Priority 1)

These enable BarraCuda to reproduce the Sarkas MD inner loop on GPU,
replacing the 97.2%-of-runtime Numba kernel with a WGSL shader.

#### 2.1 Force Kernels (already designed, see EVOLUTION_CHALLENGE_ACCEPTED.md)

| Kernel | Formula | Status |
|--------|---------|--------|
| Coulomb | F = q₁q₂/r² | ✅ Designed |
| Yukawa | F = (q₁q₂/r²)·exp(-κr)·(1 + κr) | ✅ Designed |
| Lennard-Jones | F = 24ε[(σ/r)⁶ - 2(σ/r)¹²]/r | ✅ Designed |
| Morse | F = 2Dα[exp(-2α(r-r₀)) - exp(-α(r-r₀))] | ✅ Designed |
| Born-Mayer | F = A·exp(-r/ρ)/ρ | ✅ Designed |

**Deliverable**: `crates/barracuda/src/ops/md/forces/` (one .wgsl per kernel)  
**Ancestor**: `erf.wgsl` (exponential series), `cdist.wgsl` (distance computation)

#### 2.2 Neighbor List Construction — 2 weeks

**What**: Cell-list or Verlet-list for O(N) force evaluation  
**Why**: Sarkas uses cell lists (the `head`/`ls` arrays in `force_pp.update`)  
**Ancestor**: `histc.rs` (binning), `argsort.wgsl` (sorting), `searchsorted.rs`

```
Input:  positions[N×3], box_lengths[3], cutoff_radius
Output: neighbor_list[N × max_neighbors], neighbor_count[N]

GPU strategy:
  - Hash particles into cells (spatial hashing)
  - Sort by cell index (existing argsort)
  - Scan for cell boundaries (existing searchsorted pattern)
  - Each particle: iterate over 27 neighbor cells
```

**Deliverable**: `crates/barracuda/src/ops/md/neighbor_list.wgsl`  
**Test**: Known configurations, compare neighbor counts to brute-force

#### 2.3 Velocity-Verlet Integrator — 3 days

**What**: Symplectic time integration for MD  
**Why**: Core MD timestep (position + velocity update with forces)  
**Ancestor**: Basic arithmetic (add, multiply, scalar)

```
v(t + dt/2) = v(t) + (dt/2) * F(t)/m
r(t + dt)   = r(t) + dt * v(t + dt/2)
[compute F(t + dt)]
v(t + dt)   = v(t + dt/2) + (dt/2) * F(t + dt)/m
```

**Deliverable**: `crates/barracuda/src/ops/md/verlet.wgsl`  
**Test**: Harmonic oscillator energy conservation (< 1e-8 drift per 10⁶ steps)

#### 2.4 PBC + Minimum Image — already exists, verify

**What**: Periodic boundary conditions for MD  
**Status**: ✅ Already implemented (see previous handoff)  
**Test**: Verify with Sarkas reference data

---

### Priority 3: Surrogate NPU Inference Path (2 weeks, after Priority 1)

#### 3.1 RBF Model Export to Akida Format

**What**: Convert trained RBF surrogate to Akida-compatible model  
**Why**: Microsecond inference on NPU for fast surrogate evaluation  
**Approach**: 
- RBF prediction = pairwise distance + kernel eval + weighted sum
- This is equivalent to a 1-hidden-layer network: input → RBF units → linear output
- Quantize RBF centers + weights → Akida SNN or ANN format
- Deploy via `akida_driver::InferenceExecutor`

```
Python training → export weights → Rust loads → Akida inference
                                              ↘ GPU inference (same weights)
                                              ↘ CPU inference (same weights)
```

**Deliverable**: `crates/barracuda/src/ops/interpolation/rbf_export.rs`  
**Test**: NPU prediction matches GPU prediction within quantization tolerance

#### 3.2 Cross-Hardware Validation Benchmark

**What**: Same RBF surrogate, same test points, three substrates  
**Output**: JSON with predictions + timing + power for CPU, GPU, NPU

```json
{
  "test_case": "physics_eos_surrogate",
  "training_points": 12,
  "dimensions": 3,
  "test_points": 100,
  "results": {
    "cpu":  { "predictions": [...], "time_us": 45,    "power_w": 125 },
    "gpu":  { "predictions": [...], "time_us": 2,     "power_w": 150 },
    "npu":  { "predictions": [...], "time_us": 0.8,   "power_w": 2   }
  },
  "max_prediction_diff": 1.2e-6,
  "verdict": "IDENTICAL results, different hardware"
}
```

**Deliverable**: `showcase/whitePaper/benchmarks/cross_hardware_rbf_surrogate.rs`  
**Validation**: All three substrates produce predictions within 1e-4 of each other

---

## Priority Summary and Dependencies

```
Week 1-2:  [1.3 RBF Kernel] ─────────────────┐
                                                ├──▶ [1.4 RBF Interpolator]
Week 2-4:  [1.1 Cholesky] → [1.2 Tri Solve] ─┘         │
                                                          │
Week 5:    [3.1 NPU Export] ◀─────────────────────────────┤
                                                          │
Week 5-6:  [3.2 Cross-Hardware Benchmark] ◀───────────────┘
                                                          
Week 5-10: [2.1 Forces] → [2.2 Neighbor List] → [2.3 Verlet]
           (can run in parallel with Priority 3)
```

**Critical path**: RBF Kernel → Cholesky → Tri Solve → RBF Interpolator → NPU Export  
**Total for surrogate pipeline**: ~5 weeks  
**Total including MD forces**: ~10 weeks

---

## What We Provide (Reference Data for Validation)

All reference data is in `hotSpring/control/` — use these to validate
BarraCuda implementations against the Python control:

### Surrogate Learning

| File | Contains | Use |
|------|----------|-----|
| `surrogate/results/full_iterative_workflow_results.json` | 9 objectives, convergence histories | χ² validation targets |
| `surrogate/results/physics_surrogate_LOO.json` | LOO cross-validation on 12 MD cases | RBF accuracy reference |
| `surrogate/results/benchmark_functions_results.json` | Single-round sampling results | Quick sanity check |
| `surrogate/scripts/full_iterative_workflow.py` | Complete Python implementation | Line-by-line reference |

### Sarkas MD

| File | Contains | Use |
|------|----------|-----|
| `sarkas/simulations/dsf-study/results/all_observables_validation.json` | 60 observable checks | Force kernel + integrator validation |
| `sarkas/simulations/dsf-study/results/dsf_all_lite_validation.json` | DSF peak frequencies/magnitudes | FFT + force validation |
| `sarkas/simulations/dsf-study/results/dsf_pppm_lite_validation.json` | PPPM validation | FFT 3D validation |

### TTM

| File | Contains | Use |
|------|----------|-----|
| `ttm/reproduction/local-model/local_model_summary.json` | 3 species equilibration | ODE solver reference |
| `ttm/reproduction/hydro-model/hydro_model_summary.json` | 3 species radial profiles | PDE solver reference |

### Grand Total

| File | Contains |
|------|----------|
| `comprehensive_control_results.json` | 81/81 quantitative checks, all experiments |

---

## The Pitch

BarraCuda already has 75% of what surrogate learning needs. The Cholesky
decomposition and RBF kernel shader close the gap. Once implemented:

1. **Train RBF surrogate on GPU** — same `cdist → kernel → solve` pipeline,
   but in WGSL instead of SciPy. Faster, deterministic, no Python fragility.

2. **Evaluate surrogate on NPU** — the trained model is tiny (12 points,
   3 dimensions for our physics EOS). Perfect for Akida's low-power inference.

3. **Run the same benchmark on CPU/GPU/NPU** — identical predictions,
   different substrates, measured speedups and power. This is the demo.

4. **Approach the paper authors with receipts** — "We reproduced your
   methodology without Code Ocean, and we run it on three different chips.
   Would you like to discuss reproducibility?"

The Python control is done. The math is mapped. The ancestors exist.
This is engineering, not research.

---

**Previous handoff**: `TOADSTOOL_REAL_HARDWARE_WIRING_FEB07_2026.md` (hardware wiring)  
**Strategy doc**: `hotSpring/NUCLEAR_EOS_STRATEGY.md` (full Phase A→B→C plan)  
**Contact**: ecoPrimals/hotSpring control experiment team  
**Status**: ✅ Specifications ready. Implementation can begin.

