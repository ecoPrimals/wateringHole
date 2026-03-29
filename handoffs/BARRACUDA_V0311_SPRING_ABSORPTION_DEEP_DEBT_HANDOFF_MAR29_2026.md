<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# barraCuda v0.3.11 — Spring Absorption & Deep Debt Evolution

**Date**: 2026-03-29
**Sprint**: 22
**Version**: 0.3.11
**Scope**: hotSpring lattice QCD absorption (multi-shift CG, GPU-resident RHMC observables, fermion force sign fix), cross-spring shader/algorithm absorption (Perlin f32, LCG 32-bit, Lanczos eigenvectors), tolerance registry expansion
**Previous**: BARRACUDA_V0310_COMPLIANCE_COVERAGE_VALIDATION_FIRST_HANDOFF_MAR29_2026 (fossilRecord)

---

## Summary

Full spring review and absorption cycle. Primary absorption from hotSpring's Lattice QCD
GPU infrastructure: 5 multi-shift CG WGSL shaders (Jegerlehner zeta recurrence), 3 GPU-resident
observable shaders (Hamiltonian assembly, fermion action sum, Metropolis accept/reject), and
critical fermion force sign convention fix. Rust orchestration modules adapted to barraCuda's
WgpuDevice architecture. Secondary absorptions: f32 Perlin noise for ludoSpring, 32-bit LCG
for ludoSpring, Lanczos eigenvector pipeline for groundSpring. 6 new RHMC/lattice tolerance
constants. All quality gates green.

## Changes

### Critical Fix: Fermion Force Sign Convention

- **`staggered_fermion_force_f64.wgsl`** and **`pseudofermion_force_f64.wgsl`** corrected
  from `half_eta` (+η/2) to `neg_eta` (−η), aligning with hotSpring's validated
  `F = −d(x†D†Dx)/dU` derivation. The gauge force outputs ∂S_G/∂U (positive gradient)
  and momentum updates via `P += α_s·dt·F`, so the fermion contribution must be negative.
  Incorrect sign produced wrong HMC trajectories.

### hotSpring Lattice QCD Absorption

- **5 multi-shift CG WGSL shaders**: `ms_zeta_update_f64` (Jegerlehner Algorithm 1),
  `ms_x_update_f64`, `ms_p_update_f64`, `cg_compute_alpha_shifted_f64`,
  `cg_update_xr_shifted_f64`. All under AGPL-3.0-or-later with provenance headers.
- **`gpu_multi_shift_cg.rs`**: Orchestration module with `GpuMultiShiftCgPipelines`
  (pre-compiled pipelines for all 5 shaders), `GpuMultiShiftCgBuffers` (per-solve GPU
  allocation), `GpuMultiShiftCgConfig`, and `multi_shift_cg_generic()` — a closure-based
  CPU reference solver with no lattice type dependency.
- **3 GPU-resident WGSL shaders**: `hamiltonian_assembly_f64` (H = S_gauge + T + S_ferm,
  eliminates CPU readback), `fermion_action_sum_f64` (RHMC sector accumulation),
  `gpu_metropolis_f64` (accept/reject with 9-entry diagnostics).
- **`gpu_resident_observables.rs`**: O(1)-readback pipeline with `ResidentObservablePipelines`,
  `ResidentObservableBuffers`, `MetropolisResult` (9-entry GPU result parsing).

### Cross-Spring Absorptions

- **f32 Perlin 2D** (ludoSpring): `perlin_2d_f32.wgsl` shader, `PerlinNoiseGpuF32` struct,
  `perlin_2d_cpu_f32()` CPU reference. For real-time procedural generation without f64.
- **32-bit LCG contract** (ludoSpring): `lcg_step_u32()`, `state_to_f32()`,
  `uniform_f32_sequence()` using Knuth MMIX 32-bit constants. Game-speed PRNG.
- **Lanczos eigenvector pipeline** (groundSpring): `lanczos_with_basis()` retains Krylov
  basis vectors Q, `lanczos_eigenvectors()` computes Ritz vectors via Q×z back-transform,
  returns top-k eigenpairs sorted by |eigenvalue|.

### Tolerance Registry

- 6 new RHMC/lattice HMC constants: `LATTICE_CG_FORCE` (1e-6), `LATTICE_CG_METROPOLIS`
  (1e-8), `LATTICE_RHMC_APPROX_ERROR` (1e-3), `LATTICE_PLAQUETTE` (1e-6),
  `LATTICE_FERMION_FORCE` (1e-4), `LATTICE_METROPOLIS_DELTA_H` (1.0).
- Total registered tolerances: **42**.

## Quality Gates

- `cargo fmt --all --check` — clean
- `cargo clippy --workspace --all-targets --all-features -- -D warnings` — zero warnings
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` — clean
- `cargo test -p barracuda --lib --no-default-features` — 717 tests, 0 fail
- `cargo test -p barracuda-core --lib` — 214 tests, 0 fail
- `#![forbid(unsafe_code)]` in barracuda + barracuda-core
- Zero production `unwrap()`, zero TODO/FIXME/HACK
- Zero files over 1000 LOC
- All deps pure Rust

## Codebase Health

- **WGSL shaders**: 816 (all with SPDX headers)
- **Rust source files**: 1,090
- **Tests**: 3,650+ lib + 214 core + 8 e2e + integration + doctests
- **Tolerance constants**: 42
- **Unsafe code**: Zero in barracuda + barracuda-core; 1 targeted allow in barracuda-spirv

## Cross-Primal Pins

| Primal | Version/Session | Status |
|--------|-----------------|--------|
| toadStool | S163 | Dependency audit, zero-copy, code quality |
| coralReef | Phase 10 Iter 62 | Deep audit, coverage, hardcoding evolution |
| hotSpring | v0.6.32 | Multi-shift CG + GPU-resident observables absorbed |
| groundSpring | — | Lanczos eigenvectors absorbed |
| ludoSpring | — | f32 Perlin + 32-bit LCG absorbed |

## Next Steps

- P1: DF64 end-to-end NVK hardware verification
- P1: coralReef sovereign compiler evolution
- P1: Wire `gpu_multi_shift_cg` into full RHMC HMC trajectory (end-to-end lattice solve)
- P2: Coverage to 90% (requires f64-capable GPU hardware in CI)
- P2: `BatchedTridiagEigh` GPU op (groundSpring candidate)
- P3: Multi-GPU dispatch evolution
