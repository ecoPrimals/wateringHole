# barraCuda v0.35 — Sovereign Pipeline Deep Debt Handoff

**Date**: March 13, 2026
**Type**: Deep debt sprint — sovereign pipeline gaps
**Scope**: DF64 shaders, RHMC absorption, WGSL optimizer annotations, doc alignment

---

## Summary

Executed the sovereign pipeline deep debt plan targeting everything barraCuda
can action today (not blocked on coralReef publishability or hardware access).

---

## Changes

### 1. Hand-Written DF64 Weighted Dot Shader (P1)

Created `crates/barracuda/src/shaders/reduce/weighted_dot_df64.wgsl` — 6 compute
kernels matching the f64 version but using f32-pair (DF64) workgroup accumulators:

- `weighted_dot_simple` — single-thread sequential (no shared memory)
- `weighted_dot_parallel` — tree reduction with `s_sum_hi`/`s_sum_lo` arrays
- `final_reduce` — partial sum finalization with DF64 accumulators
- `weighted_dot_batched` — M simultaneous dot products
- `dot_parallel` — unweighted dot with DF64 reduction
- `norm_squared_parallel` — ||v||² with DF64 reduction

Updated `weighted_dot_f64.rs::shader_for_device()` — Hybrid devices now use
the hand-written DF64 shader (no auto-rewrite failure risk). The `DF64_COMBINED`
string is computed once via `LazyLock`.

Covariance f64 shader confirmed safe with auto-rewrite: thread-local accumulators
only, no `var<workgroup> array<f64, N>`. Added doc note to shader header.

### 2. RHMC Multi-Shift CG Absorption from hotSpring (P2)

Created two new modules in `crates/barracuda/src/ops/lattice/`:

**`rhmc.rs`** (production + test-gated):
- `RationalApproximation` — partial fraction representation with `eval()`, `generate()`,
  `n_poles()`, and 4 preset constructors (`fourth_root_8pole`, `inv_fourth_root_8pole`,
  `sqrt_8pole`, `inv_sqrt_8pole`)
- `multi_shift_cg_solve` — solves (D†D + σ_i)x_i = b for all shifts simultaneously
  with a single Krylov space (test-gated, CPU reference)
- `MultiShiftCgResult` — convergence info struct
- Remez exchange algorithm for optimal residue fitting
- Gaussian elimination with partial pivoting
- 5 tests (rational approx eval, multi-shift CG base system, zero RHS)

**`rhmc_hmc.rs`** (test-gated CPU reference):
- `RhmcFermionConfig` — per-sector mass, power, rational approximations
- `RhmcConfig` — multi-sector HMC configuration with `nf2()` and `nf2p1()` presets
- `rhmc_heatbath` — φ = (D†D)^{-p/2} η via rational approximation + multi-shift CG
- `rhmc_fermion_action` — S_f = φ† r(p)(D†D) φ
- `rhmc_fermion_force` — dS_f/dU summed over all poles
- 5 tests (config constructors, heatbath nonzero, action positive, force size)

### 3. WGSL Optimizer Annotation Expansion (P2)

Added `// @ilp_region begin` / `// @ilp_region end` annotations to high-value
DF64 computation blocks:

- `variance_reduce_df64.wgsl` — `merge_welford_df64()`: delta, d2, ca_cb independent
- `mean_variance_df64.wgsl` — `merge_welford_df64()`: same ILP pattern
- `weighted_dot_df64.wgsl` — parallel kernel: three independent buffer loads;
  reduction loop: two independent shared memory loads. Also batched variant.
- `covariance_f64.wgsl` — pass 1: independent x/y accumulation streams

### 4. Documentation Updates

- `SOVEREIGN_PIPELINE_TRACKER.md`: P1 DF64 shaders → Done, P2 RHMC/annotations → Done
- `PURE_RUST_EVOLUTION.md`: Layer 1 recent evolution section added
- `SPRING_ABSORPTION.md`: Item 11 (RHMC) → Done
- `WHATS_NEXT.md`: New completed entry, P1/P2 items struck through
- Shader counts: 805 → 806 across all 13 doc files
- Test counts: 3,688 → 3,698 across all affected docs

---

## Quality Gates

| Gate | Result |
|------|--------|
| `cargo fmt --all -- --check` | ✅ Clean |
| `cargo clippy --workspace --all-targets -- -D warnings` | ✅ Clean |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | ✅ Clean |
| `cargo deny check` | ✅ advisories ok, bans ok, licenses ok, sources ok |
| `cargo nextest run --workspace --no-fail-fast` | ✅ 3,698 pass, 0 fail, 15 skip |

---

## Test Delta

+10 tests from RHMC absorption:
- `rhmc::tests::rational_approx_evaluates_correctly`
- `rhmc::tests::inv_fourth_root_evaluates_correctly`
- `rhmc::tests::sqrt_evaluates_correctly`
- `rhmc::tests::multi_shift_cg_solves_base_system`
- `rhmc::tests::multi_shift_cg_zero_rhs`
- `rhmc_hmc::tests::rhmc_config_nf2_has_one_sector`
- `rhmc_hmc::tests::rhmc_config_nf2p1_has_two_sectors`
- `rhmc_hmc::tests::rhmc_heatbath_produces_nonzero_field`
- `rhmc_hmc::tests::rhmc_fermion_action_positive`
- `rhmc_hmc::tests::rhmc_fermion_force_has_correct_size`

---

## What Remains Blocked

| Item | Blocker |
|------|---------|
| `CoralReefDevice` functional activation | `coral-gpu` not publishable as crate |
| DF64 NVK end-to-end verification | Hardware access |
| BAR0 hardware validation | Root/udev + hardware |
| Kokkos GPU parity benchmarks | Matching hardware |
| coralNAK extraction | Org repo fork |

---

## Files Changed

### New Files
- `crates/barracuda/src/shaders/reduce/weighted_dot_df64.wgsl`
- `crates/barracuda/src/ops/lattice/rhmc.rs`
- `crates/barracuda/src/ops/lattice/rhmc_hmc.rs`

### Modified Files
- `crates/barracuda/src/ops/weighted_dot_f64.rs` — DF64 shader wiring
- `crates/barracuda/src/ops/lattice/mod.rs` — module registration
- `crates/barracuda/src/shaders/special/covariance_f64.wgsl` — DF64 safety note
- `crates/barracuda/src/shaders/reduce/variance_reduce_df64.wgsl` — ILP annotations
- `crates/barracuda/src/shaders/reduce/mean_variance_df64.wgsl` — ILP annotations
- 13 documentation files — shader/test count updates, sprint summary
