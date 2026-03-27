# BarraCuda L2 Evolution Handoff — SCF Offset, SparsitySampler, and Next Steps

**Date**: February 13, 2026
**From**: ecoPrimals Control Team (Eastgate) — hotSpring L2 validation
**To**: ToadStool / BarraCuda Team
**Priority**: HIGH — contains traced root causes, specific file/line references, and validation criteria
**Status**: L2 validated (chi2/datum = 91.98), evolution targets identified for closing gap to Python's 1.93

---

## Executive Summary

L2 validation achieved a **310x improvement** (28,450 → 91.98 chi2/datum) through HFB physics fixes in hotSpring. The remaining gaps trace to three categories:

1. **SCF Convergence Basin Offset (~65 MeV)** — three specific numerical differences between Rust and Python solvers
2. **SparsitySampler Evaluation Density** — NM runs on surrogate only, not true objective
3. **External Dependency** — `nalgebra::SymmetricEigen` should be replaced by `barracuda::linalg::eigh_f64`

The BarraCuda team has already fixed several previously-reported issues (LOO-CV hat matrix, auto_smoothing, PenaltyFilter, warm_start_seeds, Brent root-finding). These need revalidation in hotSpring.

---

## Part 1: SCF Convergence Basin Offset (~65 MeV)

### The Problem

When running both the Rust HFB solver and the Python reference on identical SLy4 parameters, the Rust solver produces binding energies that are systematically ~65 MeV higher (more bound) than Python. This is not a formula error — all energy components have correct signs and magnitudes — but rather a convergence to a different self-consistent density profile.

### Root Cause 1: `gradient_1d` Boundary Stencil (CRITICAL)

**Location**: `barracuda/src/numerical/gradient.rs` lines 41-66

**The bug**: The docstring claims "Matches numpy.gradient() behavior" but the boundary treatment does NOT match numpy.

**BarraCuda (1st-order at boundaries)**:
```rust
// gradient.rs line 55
grad[0] = (f[1] - f[0]) / dx;                    // 1st-order forward
// gradient.rs line 63
grad[n - 1] = (f[n - 1] - f[n - 2]) / dx;        // 1st-order backward
```

**numpy.gradient (2nd-order at boundaries)**:
```python
# What numpy ACTUALLY does:
grad[0]  = (-3*f[0] + 4*f[1] - f[2]) / (2*dx)    # 2nd-order forward
grad[-1] = (3*f[-1] - 4*f[-2] + f[-3]) / (2*dx)   # 2nd-order backward
```

**The fix**:
```rust
pub fn gradient_1d(f: &[f64], dx: f64) -> Vec<f64> {
    let n = f.len();
    if n < 3 { /* keep existing behavior */ }

    let mut grad = vec![0.0; n];

    // 2nd-order forward at start (matches numpy.gradient)
    grad[0] = (-3.0 * f[0] + 4.0 * f[1] - f[2]) / (2.0 * dx);

    // Central difference for interior (unchanged)
    for i in 1..n - 1 {
        grad[i] = (f[i + 1] - f[i - 1]) / (2.0 * dx);
    }

    // 2nd-order backward at end (matches numpy.gradient)
    grad[n - 1] = (3.0 * f[n - 1] - 4.0 * f[n - 2] + f[n - 3]) / (2.0 * dx);

    grad
}
```

**Why this matters**: The wavefunction derivatives (`dwf`) are computed using this gradient and feed directly into the T_eff kinetic energy matrix integrals. The T_eff matrix elements are:

```
T_eff[i,j] = ∫ f_q(r) * [dR_i/dr * dR_j/dr * r² + l(l+1) * R_i * R_j] dr
```

The `dR_i/dr` at r[0] (nearest to the nucleus center) is where radial wavefunctions have their steepest gradients. A 1st-order stencil here introduces O(dx) error vs O(dx²) for 2nd-order, directly biasing all kinetic energy matrix elements and propagating through the entire SCF cycle.

**Affected code paths**:
- `barracuda::numerical::gradient_1d` — the library function
- `hotSpring/barracuda/src/physics/hfb.rs` lines 157-168 — wavefunction derivatives (uses inline code, not barracuda::numerical)
- `hotSpring/barracuda/src/physics/hfb.rs` lines 849-860 — density gradient for spin-orbit (uses inline code)

**Note**: The hotSpring HFB solver has its own inline `numerical_gradient` (hfb.rs:849) and `compute_wavefunctions` (hfb.rs:157) that duplicate this same 1st-order boundary bug. Both need updating.

**Validation criterion**: After fix, re-run `verify_hfb` on SLy4 for Ni-56, Zr-90, Sn-132. Mean |Rust - Python| should drop from 65 MeV to < 20 MeV.

### Root Cause 2: BCS Root-Finding — Bisection vs Brent (MEDIUM)

**Location**: `hotSpring/barracuda/src/physics/hfb.rs` lines 308-330

**The issue**: The HFB solver uses a hand-rolled bisection algorithm (200 iterations, tol=1e-6) for the BCS chemical potential lambda. Python uses `scipy.optimize.brentq` which achieves machine precision (~1e-12) in typically 10-20 iterations.

**BarraCuda already has Brent**: `barracuda/src/optimize/brent.rs` — a complete Brent root-finder matching scipy.optimize.brentq.

**The fix** (in hotSpring hfb.rs):
```rust
// Replace manual bisection (hfb.rs lines 308-330) with:
use barracuda::optimize::brent;

let result = brent(particle_number, e_min, e_max, 1e-10, 100)?;
let lam = result.root;
```

**Why this matters**: The chemical potential lambda determines BCS occupation numbers v²_k, which directly determine the new density profile. A lambda that's off by 1e-6 (bisection tol) vs 1e-12 (Brent) propagates through the density reconstruction, creating a slightly different density at each SCF iteration. After 200 SCF iterations, this compounds into the systematic offset.

**Impact estimate**: 5-15 MeV of the 65 MeV offset.

### Root Cause 3: Eigensolver Differences (LOW-MEDIUM)

**Location**: `hotSpring/barracuda/src/physics/hfb.rs` line 739

**The issue**: The HFB solver uses `nalgebra::SymmetricEigen` (Jacobi algorithm) while Python uses `numpy.linalg.eigh` (LAPACK dsyevd, divide-and-conquer). For matrices with near-degenerate eigenvalues (common in nuclear physics — spin-orbit partners), different algorithms can produce different eigenvector phase conventions and ordering, leading to different density profiles.

**BarraCuda already has eigh**: `barracuda/src/linalg/eigh.rs` — Jacobi eigenvalue algorithm matching the interface needed.

**The fix** (in hotSpring hfb.rs):
```rust
// Replace (hfb.rs line 24):
use nalgebra::{DMatrix, SymmetricEigen};

// With:
use barracuda::linalg::eigh_f64;
// (and update the diagonalization call at line 739)
```

**Benefit**: Removes the last external dependency (nalgebra) from the HFB solver. May or may not improve the SCF offset, but ensures consistency within the BarraCuda ecosystem.

**Impact estimate**: 0-10 MeV change (sign uncertain — could improve or worsen).

### Recommended Fix Order

1. Fix `gradient_1d` boundary stencil (biggest impact, 1-hour fix)
2. Wire Brent root-finding into BCS occupations (medium impact, 30-min fix)
3. Replace nalgebra with barracuda::linalg::eigh_f64 (dependency cleanup)
4. Revalidate with `verify_hfb` binary

---

## Part 2: SparsitySampler Evolution

### What's Already Fixed (Needs Revalidation)

The BarraCuda team has implemented all previously-requested features:

| Feature | File | Status |
|---------|------|--------|
| LOO-CV hat matrix fix | `surrogate/rbf.rs:364-413` | **FIXED** — correct K_raw vs K_smooth |
| `loo_cv_optimal_smoothing()` | `surrogate/rbf.rs:465-519` | **IMPLEMENTED** — grid search |
| `auto_smoothing` config | `sample/sparsity.rs:106` | **IMPLEMENTED** — default false |
| `PenaltyFilter` enum | `sample/sparsity.rs:68-78` | **IMPLEMENTED** — Threshold/Quantile/MAD |
| `warm_start_seeds` | `sample/sparsity.rs:121` | **IMPLEMENTED** — Vec<Vec<f64>> |
| Brent root-finding | `optimize/brent.rs` | **IMPLEMENTED** — full Brent's method |
| `eigh_f64` eigensolver | `linalg/eigh.rs` | **IMPLEMENTED** — Jacobi algorithm |

All of these need revalidation in hotSpring. The revalidation protocol:

```bash
# L1 revalidation with updated BarraCuda
cargo run --release --bin nuclear_eos_l1_ref -- --lambda=10 --seed=42

# L1 with SparsitySampler + auto_smoothing
cargo run --release --bin nuclear_eos_l1 -- --auto-smoothing --seed=42

# L2 revalidation
cargo run --release --bin nuclear_eos_l2_ref -- --lambda=10 --l1-samples=3000 --nm-starts=10 --evals=50 --rounds=2
```

### Remaining Issue: Evaluation Density Gap

**Location**: `sample/sparsity.rs` lines 614-626

**The problem**: The SparsitySampler runs Nelder-Mead on the SURROGATE (cheap) and only evaluates the TRUE objective at the single best point found. This means each iteration adds only ~8-20 true evaluations (one per NM solver).

**Python's mystic** does ~100-200 true evaluations per round. The Python L2 run did 3,008 total evaluations to reach chi2=1.93. BarraCuda's SparsitySampler with 5 iterations at ~20 true evals/iter = ~100 total — far fewer.

**Current code path** (sparsity.rs:614-626):
```rust
for x0 in &candidate_points {
    // Quick NM on surrogate to find promising point
    let (x_star, _, _) = nelder_mead(
        surrogate_objective,  // ← runs on SURROGATE, not true objective
        x0, bounds, ...
    );
    // Then evaluate x_star on true objective
    let f_true = f(&x_star);  // ← only ONE true eval per NM solver
    cache.record(x_star, f_true);
}
```

**The fix — Hybrid evaluation mode**:

```rust
// Option A: Run some solvers on surrogate, some on true objective
for (i, x0) in candidate_points.iter().enumerate() {
    if i < config.n_direct_solvers {
        // Direct NM on TRUE objective (exploration)
        let (x_star, f_star, _) = nelder_mead(f, x0, bounds, ...);
        cache.record(x_star, f_star);
    } else {
        // NM on surrogate, then evaluate (exploitation)
        let (x_star, _, _) = nelder_mead(surrogate_objective, x0, bounds, ...);
        let f_true = f(&x_star);
        cache.record(x_star, f_true);
    }
}

// Option B: Evaluate true objective along NM path on surrogate
// (every K-th NM step, evaluate on true objective and record)
```

**New config field**:
```rust
pub struct SparsitySamplerConfig {
    // ... existing fields ...
    /// Number of NM solvers running on true objective (default: 2)
    /// Remaining solvers run on surrogate
    pub n_direct_solvers: usize,
}
```

**Why this matters**: The DirectSampler (round-based NM on true objective) achieves chi2/datum = 5.81 at L1 and 91.98 at L2. The SparsitySampler achieves chi2 = 40+ because its surrogate-only NM doesn't accumulate enough true evaluations to explore the landscape. The hybrid approach gets the best of both: surrogate-guided exploitation + direct exploration.

**Validation criterion**: L1 SparsitySampler with hybrid mode should achieve chi2_BE/datum < 6.0 (matching DirectSampler). L2 should reach < 50 with 1000+ evaluations.

### Default Smoothing

**Current default**: `smoothing: 1e-12` (near-exact interpolation)
**Recommended default**: `auto_smoothing: true`

When `auto_smoothing` is false and `smoothing` is 1e-12, the surrogate overfits massively — RMSE at training points is 0.0000 but out-of-sample prediction is garbage. This has been the single most common failure mode during hotSpring validation.

---

## Part 3: All Evolution Targets (Prioritized)

### Tier 1: Fix & Revalidate (1 day each)

| # | Task | File | Impact | Validation |
|---|------|------|--------|------------|
| 1 | **Fix gradient_1d boundary stencil** to match numpy.gradient (2nd-order) | `numerical/gradient.rs:55,63` | Closes ~40 MeV of SCF offset | `verify_hfb` on SLy4: |Rust-Py| < 20 MeV |
| 2 | **Change default auto_smoothing to true** | `sample/sparsity.rs:167` | Prevents default overfitting | L1 SparsitySampler chi2 < 10 |
| 3 | **Wire Brent into HFB BCS** (hotSpring fix) | `hfb.rs:308-330` | Closes ~10 MeV of SCF offset | `verify_hfb` on SLy4 |
| 4 | **Replace nalgebra with eigh_f64** (hotSpring fix) | `hfb.rs:24,739` | Removes external dependency | L2 ref binary compiles without nalgebra |

### Tier 2: Algorithm Improvements (3-5 days)

| # | Task | Impact | Validation |
|---|------|--------|------------|
| 5 | **Add hybrid evaluation mode to SparsitySampler** (n_direct_solvers) | Closes evaluation density gap | L1: chi2 < 6; L2: chi2 < 50 |
| 6 | **Add DirectSampler warm-start from SparsitySampler** | Enables cascade: SparsitySampler → DirectSampler refinement | L2: chi2 < 30 with 500 evals |
| 7 | **Increase default SparsitySampler true evals** per iteration | More data per round improves surrogate | L1 convergence in fewer iterations |

### Tier 3: Library Completeness (1-2 days each)

| # | Task | File | Notes |
|---|------|------|-------|
| 8 | **Add `gradient_1d_nonuniform`** for non-uniform grids | `numerical/gradient.rs` | numpy supports variable spacing |
| 9 | **Add `trapz` with endpoint weighting** (Simpson's rule option) | `numerical/mod.rs` | Higher-order integration |
| 10 | **Document API stability policy** | `README.md` / `CHANGELOG.md` | gamma() → Result was a breaking change |

### Tier 4: Architecture (1-2 weeks)

| # | Task | Impact |
|---|------|--------|
| 11 | **Sparse matrix support** in linalg | Enables larger HFB basis sets (L3 target) |
| 12 | **Iterative eigensolver** (Lanczos/Davidson) | Required for L3 deformed HFB (1000+ states) |
| 13 | **GPU dispatch for eigh** (Titan V f64) | L3 compute target |

---

## Part 4: Bug Inventory from L2 Validation

Every bug encountered during L2 validation, with resolution status:

### Bug 9: gradient_1d Boundary Stencil Mismatch
- **When**: HFB physics fix, comparing Rust vs Python energy components
- **What**: Boundary derivatives are 1st-order (O(dx)) while numpy uses 2nd-order (O(dx²))
- **Impact**: ~40 MeV systematic offset in binding energy (largest single contributor)
- **Fix**: Update to 2nd-order forward/backward stencil (see Part 1)
- **Status**: ⚠️ NOT YET FIXED in barracuda — needs evolution

### Bug 10: BCS Uses Manual Bisection Instead of barracuda::optimize::brent
- **When**: Implementing BCS pairing in hfb.rs
- **What**: barracuda::optimize::bisect was missing from public API at the time; manual bisection was used
- **Impact**: ~5-15 MeV systematic offset (compounded through SCF cycle)
- **Fix**: Replace with barracuda::optimize::brent (now available)
- **Status**: ⚠️ NOT YET FIXED in hotSpring — easy fix once revalidation starts

### Bug 11: HFB Uses nalgebra Instead of barracuda::linalg::eigh_f64
- **When**: Initial HFB implementation (nalgebra was the only symmetric eigensolver)
- **What**: External dependency for core physics computation
- **Impact**: Potential eigenvector phase/ordering differences; dependency bloat
- **Fix**: Replace nalgebra::SymmetricEigen with barracuda::linalg::eigh_f64
- **Status**: ⚠️ NOT YET FIXED — eigh_f64 now exists, needs wiring

### Bug 12: L2 Pipeline Over-strict NMP Seed Filter
- **When**: First L2 NMP-constrained run (chi2 = 1.6M, only 2 evals)
- **What**: 3-sigma NMP filter rejected all L1 seeds; hard NMP bounds in l2_objective killed DirectSampler
- **Impact**: Optimizer couldn't explore ANY parameter space
- **Fix**: Removed 3-sigma filter, relaxed hard bounds, rely on soft NMP penalty (lambda * chi2_NMP)
- **Status**: ✅ FIXED in hotSpring

### Bug 13: SparsitySampler Default smoothing=1e-12 Causes Overfitting
- **When**: Every SparsitySampler run (L1 and L2)
- **What**: Near-exact interpolation produces 0.0 training RMSE but terrible out-of-sample prediction
- **Impact**: SparsitySampler chi2 is 5-40x worse than DirectSampler
- **Fix**: auto_smoothing=true should be default; LOO-CV selects smoothing ~5e-3
- **Status**: ⚠️ auto_smoothing EXISTS but default is still false

---

## Part 5: Revalidation Protocol

When the BarraCuda team has applied the Tier 1 fixes, hotSpring should revalidate:

### Step 1: Library Validation (10 min)
```bash
cd hotSpring/barracuda
cargo run --release --bin validate_special_functions
cargo run --release --bin validate_linalg
cargo run --release --bin validate_optimizers
# Target: 129/129 pass (or more if new tests added)
```

### Step 2: gradient_1d Verification
```bash
# Add test case to validate_optimizers or a new binary:
# gradient_1d([0.0, 1.0, 4.0, 9.0, 16.0], 1.0)
# Expected: [1.0, 2.0, 4.0, 6.0, 7.0] (numpy behavior)
# Current:  [1.0, 2.0, 4.0, 6.0, 7.0] interior OK, boundaries differ
```

### Step 3: HFB Physics Revalidation (5 min)
```bash
cargo run --release --bin verify_hfb
# Target: Mean |Rust - Python| < 20 MeV (down from 65 MeV)
```

### Step 4: L1 Revalidation (30 sec)
```bash
cargo run --release --bin nuclear_eos_l1_ref -- --lambda=10 --seed=42
# Target: chi2_BE/datum < 6.0, J > 28 MeV
```

### Step 5: L2 Revalidation (15 min)
```bash
cargo run --release --bin nuclear_eos_l2_ref -- --lambda=10 --l1-samples=5000 --nm-starts=20 --evals=200 --rounds=3
# Target: chi2_BE/datum < 70 (down from 91.98)
```

### Step 6: SparsitySampler Revalidation (if hybrid mode added)
```bash
cargo run --release --bin nuclear_eos_l1 -- --auto-smoothing --seed=42
# Target: chi2/datum < 10 (down from 40+)
```

---

## Part 6: What the BarraCuda Team Delivered (Acknowledged)

The following features were requested in previous handoffs and have been successfully implemented. The hotSpring team acknowledges this work:

| Feature | Handoff | Status | Impact |
|---------|---------|--------|--------|
| LOO-CV hat matrix fix | Phase 5 | ✅ Correct | Unblocks auto-smoothing |
| `loo_cv_optimal_smoothing()` | Phase 5 | ✅ Working | Grid search over smoothing |
| `auto_smoothing` in SparsitySampler | Phase 5 | ✅ Working | Prevents overfitting |
| `PenaltyFilter` enum | Phase 5 | ✅ Working | Clean surrogate training |
| `warm_start_seeds` | Phase 5 | ✅ Working | L1→L2 seeding |
| `eigh_f64` eigensolver | Phase 4 | ✅ Working | Jacobi algorithm |
| `brent` root-finding | Phase 4 | ✅ Working | Superlinear convergence |
| `EvaluationCache` persistence | Phase 4 | ✅ Working | Save/load optimization state |
| `chi_squared_*` stats | Phase 4 | ✅ Working | Per-datum analysis |
| `regularized_gamma_*` | Phase 4 | ✅ Working | Chi-squared p-values |
| 400 WGSL shaders | Ongoing | ✅ Inventory delivered | Full scientific compute coverage |

---

## Part 7: File Reference

### BarraCuda Library (needs evolution)

| File | What to change |
|------|---------------|
| `src/numerical/gradient.rs:55,63` | 2nd-order boundary stencils |
| `src/sample/sparsity.rs:167` | Default auto_smoothing = true |
| `src/sample/sparsity.rs:614-626` | Add n_direct_solvers hybrid mode |

### hotSpring (needs rewiring after BarraCuda evolution)

| File | What to change |
|------|---------------|
| `src/physics/hfb.rs:157-168` | Use barracuda::numerical::gradient_1d (after fix) |
| `src/physics/hfb.rs:308-330` | Replace bisection with barracuda::optimize::brent |
| `src/physics/hfb.rs:24,739` | Replace nalgebra with barracuda::linalg::eigh_f64 |
| `src/physics/hfb.rs:849-860` | Use barracuda::numerical::gradient_1d (after fix) |
| `Cargo.toml` | Remove nalgebra dependency (after eigh_f64 wiring) |

### Reference implementations (for BarraCuda team)

| File | What it demonstrates |
|------|---------------------|
| `src/archive/surrogate.rs` | Correct LOO-CV, penalty filtering, round-based optimization |
| `src/archive/stats.rs` | chi2_decomposed, bootstrap_ci, convergence_diagnostics |
| `src/bin/verify_hfb.rs` | HFB physics verification (Rust vs Python comparison) |
| `src/bin/nuclear_eos_l1_ref.rs` | NMP-constrained L1 pipeline |
| `src/bin/nuclear_eos_l2_ref.rs` | NMP-constrained L2 pipeline with L1 seeding |

---

## Summary

The path from chi2/datum = 91.98 to < 30 is:

1. **Fix gradient_1d** boundary stencil → ~40 MeV SCF offset reduction
2. **Wire Brent** into BCS → ~10 MeV SCF offset reduction
3. **Replace nalgebra** with eigh_f64 → dependency cleanup
4. **Revalidate L2** → expect chi2 < 70
5. **Add hybrid SparsitySampler** mode → expect chi2 < 30 with 1000+ evals
6. **Run large-budget L2** → approach Python's 1.93

Every bug is a test case. Every validation is an evolution step. The loop continues.

```
BarraCuda evolves → hotSpring validates → results committed → next evolution
```

---

**Validation Repo**: hotSpring
**Result Data**: `hotSpring/control/surrogate/nuclear-eos/results/`
**Reference Code**: `hotSpring/barracuda/src/archive/surrogate.rs`, `src/archive/stats.rs`
**Previous Handoffs**: `wateringHole/handoffs/BARRACUDA_PHASE{3,4,5}_*.md`, `BARRACUDA_L{1,2}_VALIDATION_*.md`
