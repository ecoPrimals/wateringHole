# coralReef — Phase 10 Iteration 21 Handoff (Cross-Spring Absorption Wave 2)

**Date**: March 8, 2026
**From**: coralReef
**To**: All springs (hotSpring, groundSpring, neuralSpring, wetSpring, airSpring)

---

## Summary

Iteration 21 is a major cross-spring absorption wave. 38 new test entries added
to the cross-spring corpus: 9 self-contained hotSpring shaders (nuclear physics,
lattice QCD, MD), 17 neuralSpring shaders (10 coralForge Evoformer df64 + 7
bio/evolution f32), and 12 existing fixtures wired into corpus tracking.

df64 comparison operators (`df64_gt`, `df64_lt`, `df64_ge`) added to built-in
preamble. `local_elementwise_f64` retired (airSpring v0.7.2 deleted upstream).
`chi_squared_f64` keyword fix (`shared` → `wg_scratch`).

## Absorbed Shaders

### From hotSpring (9 new + 6 wired)

| Shader | Domain | Status |
|--------|--------|--------|
| `spin_orbit_pack_f64` | Nuclear (spin-orbit) | **PASS** |
| `batched_hfb_density_f64` | Nuclear (HFB) | **PASS** |
| `batched_hfb_energy_f64` | Nuclear (HFB) | IGNORED — f64 pow/log2 gap |
| `esn_readout` | MD (Echo State Network) | **PASS** |
| `esn_reservoir_update` | MD (ESN) | IGNORED — Tanh not supported |
| `su3_kinetic_energy_f64` | Lattice QCD | **PASS** |
| `su3_link_update_f64` | Lattice QCD | **PASS** |
| `staggered_fermion_force_f64` | Lattice QCD | **PASS** |
| `dirac_staggered_f64` | Lattice QCD | **PASS** |
| `xpay_f64` | Lattice (BLAS) | **PASS** (wired) |
| `yukawa_force_f64` | MD | **PASS** (wired) |
| `vv_kick_drift_f64` | MD (Verlet) | **PASS** (wired) |
| `polyakov_loop_f64` | Lattice QCD | IGNORED — needs Complex64 |
| `wilson_action_f64` | Lattice QCD | IGNORED — needs c64_new |
| `lattice_init_f64` | Lattice QCD | IGNORED — needs su3 include |

### From neuralSpring (17 new + 6 wired)

| Shader | Domain | Status |
|--------|--------|--------|
| `torsion_angles_f64` | Evoformer (df64) | IGNORED — repair_ssa gap |
| `triangle_mul_outgoing_f64` | Evoformer (df64) | **PASS** |
| `triangle_mul_incoming_f64` | Evoformer (df64) | **PASS** |
| `triangle_attention_f64` | Evoformer (df64) | **PASS** |
| `outer_product_mean_f64` | MSA (df64) | **PASS** |
| `msa_row_attention_scores_f64` | MSA (df64) | **PASS** |
| `msa_col_attention_scores_f64` | MSA (df64) | **PASS** |
| `attention_apply_f64` | Attention (df64) | **PASS** |
| `ipa_scores_f64` | IPA (df64) | **PASS** |
| `backbone_update_f64` | IPA (df64) | **PASS** |
| `hill_gate` | Signal (f32) | **PASS** |
| `batch_fitness_eval` | EA (f32) | **PASS** |
| `multi_obj_fitness` | Pareto (f32) | **PASS** |
| `swarm_nn_scores` | Swarm (f32) | **PASS** |
| `locus_variance` | PopGen (f32) | **PASS** |
| `head_split` | MHA (f32) | **PASS** |
| `head_concat` | MHA (f32) | **PASS** |
| `batch_ipr` | Anderson (f32) | **PASS** (wired) |
| `wright_fisher_step` | PopGen (f32) | **PASS** (wired) |
| `logsumexp_reduce` | HMM (f32) | **PASS** (wired) |
| `chi_squared_f64` | Stats (f64) | **PASS** (keyword fix) |
| `pairwise_l2` | MODES (f32) | **PASS** (wired) |
| `linear_regression` | Stats (f32) | **PASS** (wired) |

### Retired

| Shader | Reason |
|--------|--------|
| `local_elementwise_f64` | airSpring v0.7.2 retired; upstream: `batched_elementwise_f64` |

## Test Status

- **1174 passing**, 30 ignored (was 1142/25)
- **63% line coverage**
- Zero clippy warnings, zero fmt issues

## Cross-Spring Shaders

- **86 cross-spring WGSL shaders** total (was 47)
- **79 compiling SM70** (was 40)

## New Blockers Found

| Blocker | Shaders | Notes |
|---------|---------|-------|
| External Complex64 include | polyakov_loop, wilson_action | Need complex_f64.wgsl prepend |
| External SU(3) include | lattice_init | Need su3 function library |
| f64 pow→log2 gap | batched_hfb_energy | log2 lowering expects 2-component SSA |
| Math::Tanh | esn_reservoir_update | Tanh not yet in math function table |
| repair_ssa gap | torsion_angles | Branched df64_gt causes undefined value |

## Pin Version

All springs should update their coralReef pin to **Phase 10 Iteration 21**.

---

*AGPL-3.0-only*
