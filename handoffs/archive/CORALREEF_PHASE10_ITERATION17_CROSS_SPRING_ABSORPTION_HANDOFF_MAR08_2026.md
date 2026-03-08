# coralReef — Phase 10 Iteration 17 Handoff

**Date**: March 8, 2026
**From**: coralReef
**To**: All springs (hotSpring, groundSpring, neuralSpring, wetSpring, airSpring)

---

## Summary

Iteration 17 is a cross-spring absorption iteration. 20 new WGSL shaders
imported from hotSpring and neuralSpring, expanding the compiler test corpus
from 27 to 47 shaders (32 compiling to native SASS on SM70). Full codebase
audit confirms no mocks in production, no hardcoded primal names in logic,
and all dependencies are pure Rust (except libc for DRM kernel ABI).

## Test Status

- **1134 passing**, 33 ignored, 0 failures
- **63% line coverage** (target 90%)
- Zero clippy warnings, zero fmt issues, zero production `unwrap()`/`todo!()`

## Absorbed Shaders

### From hotSpring (10 shaders)

| Shader | Domain | Path |
|--------|--------|------|
| `cg_compute_alpha_f64` | CG scalar: α = rz/pAp | lattice/ |
| `cg_compute_beta_f64` | CG scalar: β = rz_new/rz_old | lattice/ |
| `cg_update_p_f64` | CG vector: p = r + β·p | lattice/ |
| `cg_update_xr_f64` | CG vector: x += α·p, r -= α·ap | lattice/ |
| `complex_dot_re_f64` | Complex dot Re(a·conj(b)) | lattice/ |
| `yukawa_force_verlet_f64` | Yukawa with Verlet neighbor list | md/ |
| `yukawa_force_celllist_indirect_f64` | Yukawa with indirect indexing | md/ |
| `su3_momentum_update_f64` | SU(3) P += dt·F | lattice/ |
| `vacf_batch_f64` | Batched VACF dot product | md/ |
| `su3_flow_accumulate_f64` | Gradient flow K-buffer accumulate | lattice/ |

### From neuralSpring (10 shaders)

| Shader | Domain | Path |
|--------|--------|------|
| `xoshiro128ss` | PRNG: rotl/shift/xor (u32/f32) | metalForge/ |
| `hmm_viterbi` | HMM Viterbi log-domain decoding | metalForge/ |
| `hmm_backward_log` | HMM backward logsumexp | metalForge/ |
| `pairwise_hamming` | Hamming distance (u32 integer diff) | metalForge/ |
| `pairwise_jaccard` | Jaccard distance (set-based f32) | metalForge/ |
| `rk45_adaptive` | Dormand-Prince RK45 adaptive ODE | metalForge/ |
| `matrix_correlation` | Pearson correlation (shared memory) | metalForge/ |
| `stencil_cooperation` | Fermi imitation dynamics (2D stencil) | metalForge/ |
| `spatial_payoff` | Prisoner's dilemma payoff stencil | metalForge/ |
| `swarm_nn_forward` | Batch NN forward + argmax | metalForge/ |

### Compiler Limitations Found

| Shader | Issue | Category |
|--------|-------|----------|
| `xoshiro128ss` | Non-local pointer argument in function call | naga_translate |
| `swarm_nn_forward` | RA SSA tracking: loop-carried phi mismatch | register allocator |

## Code Quality Changes

- SM75 `gpr.rs` refactored: 1025 → 935 LOC (Vec helpers → const slices)
- `local_elementwise_f64` documented as retired (airSpring v0.7.2)
- All docs updated to Iteration 17 across coralReef and wateringHole

## Audit Results (Clean)

| Category | Result |
|----------|--------|
| Mocks in production | None found |
| Hardcoded primal names in logic | None (docs/comments only) |
| Hardcoded IP addresses in production | None (`127.0.0.1:0` OS-assigned only) |
| External deps with C/FFI | libc only (DRM kernel ABI, unavoidable) |
| Unsafe code | 9 blocks in coral-driver + 2 in nak-ir-proc (all RAII-wrapped) |
| Files over 1000 lines | None (sm75 gpr.rs fixed: 1025→935) |

## Pin Version

All springs should update their coralReef pin from Iteration 10/16 to
**Iteration 17**.

---

*AGPL-3.0-only*
