# hotSpring → barraCuda / toadStool: Science Ladder Absorption Handoff

**Date:** March 6, 2026
**From:** hotSpring v0.6.17+ (gradient flow, gradient flow reproduction, science ladder)
**To:** barraCuda v0.3.3+, toadStool S94b+, coralReef
**License:** AGPL-3.0-only

---

## What hotSpring Evolved (March 6, 2026)

### 1. Derived LSCFRK Integrators (absorb into barraCuda)

hotSpring discovered that the LSCFRK3 gradient flow integrator
coefficients are fully derivable from two free parameters via four algebraic
order conditions. A `const fn derive_lscfrk3(c2, c3)` now solves these at
compile time — zero magic numbers.

**Source:** `hotSpring/barracuda/src/lattice/gradient_flow.rs`
**What to absorb:**
- `derive_lscfrk3()` — const fn derivation of 3-stage 3rd-order 2N-storage RK coefficients
- `Lscfrk` struct — generic coefficient container for any 2N-storage scheme
- `lscfrk_step()` — generic Lie group integrator (Algorithm 6 from published authors (2021))
- `LSCFRK4CK` — Carpenter-Kennedy 4th-order coefficients (numerical, cannot be derived in closed form)
- `run_flow()` — Wilson gradient flow with E(t), t²⟨E⟩, t₀, w₀ measurement
- `find_t0()`, `find_w0()`, `compute_w_function()` — scale setting utilities

**Design principle for barraCuda:** Encode derivations, not results. If a coefficient
has an algebraic origin, the code should contain the algebra, not the number.

### 2. Asymmetric Lattice Validation (26-36× GPU speedup)

GPU HMC validated on 8 lattice geometries from 4⁴ through 32³×8. Linear volume
scaling confirmed. No shader changes required — the `dims` uniform system works.

### 3. N_f=4 Dynamical Fermion Infrastructure

Complete GPU pipeline: staggered Dirac → CG solver → pseudofermion → fermion
force → dynamical HMC trajectory. All in `gpu_hmc/dynamical.rs`.

**Gap for barraCuda:** Multi-shift CG for RHMC (fractional flavors). CPU
implementation exists in `lattice/rhmc.rs`. GPU version would unblock N_f=2, 2+1.

### 4. Adaptive HMC Parameters

`production_finite_temp.rs` implements runtime dt adaptation based on acceptance
rate. This should be a barraCuda-level feature, not spring-specific.

### 5. 7 New Binaries

`bench_backends`, `production_finite_temp`, `production_gradient_flow`,
`compare_flow_integrators`, `validate_gradient_flow`, `production_dynamical` —
all registered in Cargo.toml. Total: 92 binaries, 716 tests.

---

## Science Ladder Status

| Level | What | hotSpring | barraCuda Gap |
|-------|------|-----------|---------------|
| 0 | Quenched HMC | ✅ | None |
| 1 | Gradient flow + scale setting | ✅ | Absorb flow primitives |
| 2 | LSCFRK3 integrator convergence | ✅ | Absorb `derive_lscfrk3` |
| 3 | N_f=4 staggered dynamical | ✅ Infra | None (uses existing GPU CG) |
| 4 | N_f=2 RHMC | Pending | GPU multi-shift CG |
| 5 | N_f=2+1 | Pending | Mass tuning + GPU RHMC |

---

## Precision Relevance

Gradient flow observables (W(t), t₀, w₀) require numerical differentiation of
t²⟨E(t)⟩. This is precision-sensitive. barraCuda's `compile_shader_universal()`
precision system (f16/f32/f64/DF64) should support flow shaders when they move
to GPU. DF64 is the minimum viable precision for production scale setting.

---

## Sovereign Pipeline Note

Gradient flow is an ideal coralReef target when coralDriver lands:
- Flow force computation is embarrassingly parallel (per-link, per-site)
- Heavy f64 arithmetic (SU(3) matrix exponentials, staple sums)
- Titan V's native f64 silicon would eliminate the DF64 overhead entirely
- Same WGSL → naga → coralReef → SASS pipeline as other lattice shaders

---

*The full derivation chain, from order conditions through 2N-storage conversion,
is documented in gradient_flow.rs with line-by-line algebra. The tests verify
both that the derivation reproduces published values and that all four order
conditions hold to machine precision.*
