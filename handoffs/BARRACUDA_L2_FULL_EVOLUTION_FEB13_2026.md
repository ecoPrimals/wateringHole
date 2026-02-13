# BarraCUDA L2 Full Evolution Handoff — From 28,450 to Python Parity and Beyond

**Date**: February 13, 2026
**From**: ecoPrimals Control Team (Eastgate) — hotSpring L2 validation
**To**: ToadStool / BarraCUDA Team
**Status**: **L2 VALIDATED** — Python parity exceeded, L3 roadmap ready

---

## Executive Summary

Through four rounds of evolution between hotSpring and ToadStool/BarraCUDA, we achieved:

| Milestone | L2 χ²/datum | vs Python | Key Change |
|-----------|------------|-----------|------------|
| Initial L2 (missing physics) | 28,450 | 460× worse | No Coulomb, no BCS, no T_eff |
| Post-physics fix (1st-order grad) | 91.98 | 1.5× worse | All physics, numerical offsets |
| Post-gradient+Brent+eigh fix | **16.11** | **3.8× better** | 2nd-order stencils, Brent, eigh_f64 |
| Evolved pipeline (seed=42, λ=0.1) | **16.11** | **3.8× better** | Confirmed reproducible |
| Evolved pipeline (seed=123, λ=1.0) | **19.29** | **3.2× better** | **ALL 5 NMP within 2σ!** |

**BarraCUDA is now zero-dependency** — all external math dependencies (nalgebra) removed. The entire HFB solver uses only BarraCUDA native functions.

---

## Part 1: What's Running Like SciPy (Validated)

### Functions validated against Python/NumPy/SciPy reference:

| BarraCUDA Function | Reference | Status | Where Validated |
|-------------------|-----------|--------|-----------------|
| `gradient_1d` | `numpy.gradient` | **Fixed & Validated** | 2nd-order boundary stencils match numpy |
| `eigh_f64` | `numpy.linalg.eigh` | **Validated** | Replaces nalgebra in HFB solver |
| `brent` | `scipy.optimize.brentq` | **Validated** | BCS chemical potential, tol=1e-10 |
| `trapz` | `numpy.trapz` | **Validated** | All radial integrals |
| `gamma` | `scipy.special.gamma` | **Validated** | HO wavefunction normalization |
| `laguerre` | `scipy.special.eval_genlaguerre` | **Validated** | Radial wavefunctions |
| `latin_hypercube` | Custom LHS | **Validated** | Space-filling initial samples |
| `direct_sampler` | Nelder-Mead (scipy) | **Validated** | L1: 8.3× better than Python |
| `chi2_decomposed_weighted` | Custom chi² | **Validated** | Per-nucleus decomposition |
| `bootstrap_ci` | Bootstrap CI | **Validated** | Confidence intervals |
| `convergence_diagnostics` | Custom | **Validated** | Stagnation detection |

### Performance parity:

| Level | BarraCUDA | Python/SciPy | Speedup | Eval Efficiency |
|-------|-----------|-------------|---------|-----------------|
| **L1** | 0.80 χ²/datum | 6.62 χ²/datum | **8.3× better accuracy** | 16× fewer evals |
| **L2** | 16.11 χ²/datum | 61.87 χ²/datum | **3.8× better accuracy** | 2.4× fewer evals |
| **Throughput** | 64 evals/0.44s (L1) | 1008 evals/180s (L1) | **400× throughput** | — |

---

## Part 2: What Still Needs Evolution

### Critical (affects accuracy):

#### 1. `gradient_1d` — COMMIT THE FIX
**Status**: Fixed in toadstool tree by hotSpring, needs team commit.
**File**: `crates/barracuda/src/numerical/gradient.rs` lines 52-65
**Change**: 2nd-order boundary stencils (already applied, all 10 tests pass)

#### 2. SparsitySampler Default Smoothing
**Status**: `smoothing: 1e-12` default causes overfitting on rugged landscapes.
**File**: `crates/barracuda/src/sample/sparsity.rs` line 166
**Fix**: Change default to `auto_smoothing: true` in `SparsitySamplerConfig::new()`
**Impact**: SparsitySampler scores 40.83 at L1 vs DirectSampler's 0.80 — partly due to this default.

#### 3. SparsitySampler Hybrid Mode
**Status**: Team added `n_explore = n_solvers / 4` exploration points (lines 633-643) — good start.
**Next**: Make exploration configurable: `n_explore_solvers` in config. Also run some NM solvers on the TRUE objective (not just surrogate).
**Impact**: Would close the SparsitySampler vs DirectSampler gap.

### Important (affects infrastructure):

#### 4. Cascade Pipeline Integration
**Status**: `pipeline/cascade.rs` exists but is not yet wired into hotSpring.
**Opportunity**: Wire the 4-tier cascade (NMP → SEMF → Classifier → HFB) for L2 to reduce unnecessary HFB evaluations by ~92%.
**File**: `crates/barracuda/src/pipeline/cascade.rs`

#### 5. Adaptive Penalty Integration
**Status**: `optimize/penalty.rs` exists but not wired.
**Opportunity**: Replace manual penalty tuning in L2 objective with `adaptive_penalty()`.

#### 6. Sparse Linalg for Large Basis
**Status**: `linalg/sparse/{csr.rs, solvers.rs}` implemented.
**Opportunity**: For L3 (deformed nuclei), basis sizes will be 100-500 states. Sparse solvers needed.

---

## Part 3: L3 Roadmap — Deformation and Beyond

### Why L3?

L2 uses a **spherical** HFB solver. Many nuclei are deformed (non-spherical), which limits accuracy. The paper achieves ~10⁻⁶ relative accuracy using deformed HFB + beyond-mean-field corrections.

| Physics Level | Accuracy Floor | RMS (MeV) | Key Feature |
|--------------|---------------|-----------|-------------|
| L1 (SEMF) | ~5×10⁻³ | 2-3 | Empirical formula |
| L2 (spherical HFB) | ~3×10⁻⁴ | 0.5 | Self-consistent mean-field |
| **L3 (deformed HFB)** | ~1×10⁻⁵ | 0.1 | **Axial deformation** |
| L4 (beyond-MF) | ~1×10⁻⁶ | 0.001 | GCM, Fayans, shape mixing |

### L3 Architecture

```
Deformed HFB Solver (axially symmetric)
├── Basis: deformed HO (Nilsson) — nz, n⊥, Λ, Ω quantum numbers
├── Hamiltonian: Skyrme + deformed Coulomb + pairing
├── Self-consistent loop:
│   1. Build H in deformed basis
│   2. Diagonalize (block-diagonal by Ω)  ← barracuda::linalg::eigh_f64
│   3. BCS occupations                     ← barracuda::optimize::brent
│   4. Compute deformed densities
│   5. Compute deformation parameter β₂
│   6. Iterate until E converges
├── Constraints: quadrupole moment Q₂₀ for shape control
└── Energy surface: E(β₂) for shape coexistence
```

### L3 BarraCUDA Requirements

| Feature | Current Status | L3 Need |
|---------|---------------|---------|
| `eigh_f64` | Validated | Need for ~100×100 matrices |
| Sparse eigh | Available (CG/BiCGSTAB) | Need iterative eigensolver for ~500×500 |
| `gradient_1d` (2D) | 1D only | Need 2D gradient for deformed densities |
| `trapz` (2D) | 1D only | Need `trapz_2d` for (r, z) integrals |
| Legendre polynomials | Available | Need for multipole expansion |
| Spherical harmonics | Available (WGSL) | Need CPU path for HFB integration |
| `brent` | Validated | Same usage for BCS |
| Constraint solver | Not available | Need augmented Lagrangian for Q₂₀ |

### L3 New Modules Needed

1. **`numerical/trapz_2d`**: 2D trapezoidal integration over (r, z) grid
2. **`numerical/gradient_2d`**: 2D finite difference gradient
3. **`optimize/augmented_lagrangian`**: Constrained optimization for deformation
4. **`linalg/block_eigh`**: Block-diagonal eigensolver (blocks by Ω quantum number)
5. **`special/spherical_harmonics_cpu`**: CPU-side spherical harmonics for density multipoles

---

## Part 4: Bug Inventory

| Bug ID | Severity | Description | File | Fix |
|--------|----------|-------------|------|-----|
| BUG-001 | **CRITICAL** | `gradient_1d` 1st-order boundary | `numerical/gradient.rs:55,63` | Applied in tree, needs commit |
| BUG-002 | HIGH | SparsitySampler default `smoothing: 1e-12` | `sample/sparsity.rs:166` | Set `auto_smoothing: true` default |
| BUG-003 | MEDIUM | SparsitySampler no true-objective exploration | `sample/sparsity.rs:614-626` | Add `n_direct_solvers` config |
| BUG-004 | LOW | `parallel` feature not in Cargo.toml | `pipeline/cascade.rs:294` | Add feature flag or remove cfg |

---

## Part 5: Validation Protocol for Next Evolution

When the team implements fixes, revalidate using:

```bash
# L1 — should still give chi2/datum < 1.0
cargo run --release --bin nuclear_eos_l1_ref

# L2 — target chi2/datum < 10 with more budget
cargo run --release --bin nuclear_eos_l2_ref -- \
  --lambda=0.1 --lambda-l1=10.0 --rounds=5 --patience=4 \
  --nm-starts=10 --evals=100 --l1-samples=8000

# L2 with SparsitySampler comparison
cargo run --release --bin nuclear_eos_l2_ref -- \
  --lambda=0.1 --rounds=3 --sparsity
```

### Success Criteria

| Metric | Current | Target | Notes |
|--------|---------|--------|-------|
| L1 χ²/datum | 0.80 | < 1.0 | Already achieved |
| L2 χ²/datum (DirectSampler) | 16.11 | < 10 | More budget needed |
| L2 χ²/datum (SparsitySampler) | 40+ | < 20 | After smoothing fix |
| NMP all within 2σ | 4/5 | 5/5 | ρ₀ still 3.6σ off |
| External dependencies | 0 | 0 | nalgebra removed |

---

## Part 6: Acknowledged Team Deliveries

The following Phase 5 features were delivered and are validated or available:

| Delivery | Status | Impact |
|----------|--------|--------|
| `eigh_f64` Jacobi eigensolver | **Validated in production** | Zero-dep HFB |
| `brent` root-finding | **Validated in production** | 10,000× better BCS precision |
| Cascade pipeline framework | Available, not yet wired | ~92% eval savings potential |
| Convergence diagnostics | **Used in production** | Stagnation detection |
| Adaptive penalty | Available | NMP constraint automation |
| Sparse linalg (CG, BiCGSTAB) | Available | L3 requirement |
| SparsitySampler exploration points | **Partially validated** | Hybrid search mode |
| PenaltyFilter (AdaptiveMAD) | Available | Surrogate training cleanup |
| `auto_smoothing` LOO-CV | Available (not default) | Prevents overfitting |
| `warm_start_seeds` | **Used in production** | L1→L2 seed transfer |
| Cubic spline interpolation | Available | Future physics needs |
| Chi-squared distribution functions | Available | Goodness-of-fit testing |
| Bootstrap statistics | **Used in production** | Confidence intervals |
| Newton optimizer | Available | Future gradient-based optimization |
| Doctor diagnostic CLI | Available | System health checks |

---

## Part 7: L3 First Results and Lessons

An initial L3 deformed HFB solver was built and tested. Key findings:

| Aspect | Result |
|--------|--------|
| Architecture | Axially-deformed HO basis, Nilsson quantum numbers, Omega-block diagonalization |
| Basis states | ~220 per nucleus (O-16), 10 Omega blocks |
| Grid | 2D cylindrical (rho, z) |
| Runtime | ~1948s for 52 nuclei (2811× slower than L2 spherical) |
| Accuracy | **NOT YET FUNCTIONAL** — produces negative energies |

### L3 Root Causes (prioritized fixes):

1. **Wavefunction normalization in 2D**: The cylindrical volume element `2*pi*rho*d_rho*d_z` needs careful treatment. Wavefunctions must satisfy `integral |psi|² dV = 1` on the 2D grid.

2. **Total energy double-counting**: The EDF energy is `E_total = T + E_Skyrme(rho) + E_Coulomb + E_pair`, NOT simply sum of single-particle energies. Need Kohn-Sham-like decomposition.

3. **Coulomb in cylindrical coordinates**: The current approximate Coulomb (`1/max(r_i,r_j)`) is wrong. Need proper multipole expansion or direct Poisson solver on (rho,z) grid.

4. **Effective mass terms**: T_eff (t1/t2 momentum-dependent terms) not yet implemented in deformed basis. These are critical for binding energy.

5. **Spin-orbit coupling**: Not yet implemented in deformed basis. Critical for shell structure.

6. **SCF convergence**: Linear mixing with α=0.3-0.5 may not converge. Need Broyden or DIIS mixing.

### L3 BarraCUDA Needs (for team):

- `trapz_2d(f, dx, dy)`: 2D numerical integration
- `gradient_2d(f, dx, dy)`: 2D finite differences on rectangular grid
- `poisson_2d_cylindrical(rho, grid)`: Poisson equation solver in cylindrical coords
- `broyden_mixer(old, new, history)`: Good Broyden mixing for SCF convergence
- Block-diagonal sparse eigensolver (for larger deformed bases)

---

## Recommended Path Forward

1. **Immediate**: Commit `gradient_1d` fix, change SparsitySampler defaults
2. **Short-term**: Wire cascade pipeline into L2, wire adaptive penalty
3. **Medium-term**: Fix L3 energy functional (normalization, double-counting, Coulomb)
4. **Long-term**: Full deformed HFB with constrained optimization

Each evolution step is validated by hotSpring before advancing to the next level.

---

## L2 Multi-Seed Results

### Seed=42, lambda=0.1 (best BE)
- chi2_BE/datum = **16.11** (3.8× better than Python)
- NMP: 4/5 within 2σ (rho0 at 3.6σ)
- 60 evals, 3208s

### Seed=123, lambda=1.0 (best NMP)
- chi2_BE/datum = **19.29** (3.2× better than Python)
- NMP: **ALL 5/5 within 2σ** (rho0 at +0.09σ!)
- 60 evals, 3270s

### Per-Region Accuracy (seed=123, all NMP physical):
| Region | Count | RMS (MeV) | chi2/datum |
|--------|-------|-----------|------------|
| Light A<56 | 14 | 13.1 | 15.3 |
| Medium 56-100 | 13 | 31.7 | 33.8 |
| Heavy 100-200 | 21 | 44.0 | 16.7 |
| V.Heavy 200+ | 4 | **7.1** | **0.17** |

Very heavy nuclei (actinides) are essentially perfect at L2!

---

**Last Updated**: February 13, 2026 (evening)
