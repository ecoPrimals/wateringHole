# barraCuda v0.3.5 — Health Absorption & Deep Evolution Handoff

**Date**: March 10, 2026
**From**: barraCuda
**To**: All springs, toadStool, coralReef

---

## Summary

barraCuda v0.3.5 completes the second deep absorption sprint, absorbing healthSpring V19
CPU and GPU primitives, fixing two P0 correctness bugs, and adding cross-spring stable
special functions.

## P0 Fixes (Correctness)

| Fix | Impact |
|-----|--------|
| `enable f64;` stripped from f32 downcast path | Ada Lovelace (SM89) GPUs no longer produce zero-returning shaders when f64-canonical sources are downcasted. `downcast_f64_to_f32()` now removes the directive. |
| HMM batch forward binding mismatch | New `hmm_batch_forward_f64.wgsl` with correct 7-binding layout (params, log_trans, log_emit, log_pi, observations, log_alpha_out, log_lik_out). One thread per sequence, sequential over T steps. |

## New GPU Shaders (6 added, total: 803)

| Shader | Domain | Source |
|--------|--------|--------|
| `michaelis_menten_batch_f64.wgsl` | PK simulation | healthSpring V19 |
| `scfa_batch_f64.wgsl` | Microbiome | healthSpring V19 |
| `beat_classify_batch_f64.wgsl` | Biosignal | healthSpring V19 |
| `stable_f64.wgsl` | Special functions | Cross-spring ISSUE-011 |
| `tridiag_eigh_f64.wgsl` | Spectral | groundSpring request |
| `hmm_batch_forward_f64.wgsl` | Bio | P0 binding fix |

## New CPU Modules

### `health::pkpd`
- `MichaelisMentenParams`, `PHENYTOIN_PARAMS`
- `mm_pk_simulate()`, `mm_css_infusion()`, `mm_apparent_half_life()`
- `mm_auc()`, `mm_auc_analytical()`, `mm_nonlinearity_ratio()`

### `health::microbiome`
- `ScfaParams`, `SCFA_HEALTHY_PARAMS`, `SCFA_DYSBIOTIC_PARAMS`
- `scfa_production()` → `ScfaResult` (acetate, propionate, butyrate)
- `antibiotic_perturbation()` — exponential kill model
- `gut_serotonin_production()`, `tryptophan_availability()`

### `health::biosignal`
- `eda_scl()`, `eda_phasic()`, `eda_detect_scr()`
- `StressAssessment`, `assess_stress()`, `compute_stress_index()`
- `BeatClass`, `BeatTemplate`, `classify_beat()`, `classify_all_beats()`
- `normalized_correlation()` — template matching primitive
- `rolling_average()` — O(n) centered window (21x faster than naive convolution)
- `convolve_1d()` — valid 1D convolution

### `special::stable_gpu`
- `log1p_f64()`, `expm1_f64()`, `erfc_f64()`, `bessel_j0_minus1_f64()`
- Cross-spring ISSUE-011 catastrophic cancellation avoidance

### `device::fma_policy`
- `FmaPolicy::Contract`/`Separate`/`Default`
- `domain_requires_separate_fma()` — Lattice QCD, gradient flow, nuclear EOS
- coralReef Iteration 30 integration

### `spectral::tridiag_eigh_gpu`
- `BatchedTridiagEighGpu` — QL with Wilkinson shifts on GPU
- One thread per independent tridiagonal system

### `stats::hydrology` extensions
- `fao56_et0_with_ea()` — direct actual vapour pressure input
- `hamon_et0_brock()` — Brock (1981) daylight formula variant

## Metrics

| Metric | v0.3.4 | v0.3.5 |
|--------|--------|--------|
| WGSL shaders | 797 | 803 |
| Lib tests | 3,280 | 3,341+ |
| Rust source files | 1,050+ | 1,060+ |
| Clippy pedantic | ✅ | ✅ |

## Spring Impact

- **healthSpring**: All V19 GPU shaders + CPU primitives absorbed. Springs can remove local copies.
- **airSpring**: `fao56_et0_with_ea()` closes the CPU-GPU gap. `hamon_et0_brock()` standardizes formula.
- **groundSpring**: `BatchedTridiagEighGpu` unblocks spectral batch problems.
- **neuralSpring**: `enable f64;` PTXAS fix resolves Ada Lovelace regression.
- **All springs**: `stable_f64.wgsl` provides cross-spring stable special functions.
- **coralReef**: `FmaPolicy` integration ready for Iteration 30 reproducibility controls.

## Next Sprint Candidates

- Batch Smith-Waterman GPU shader
- GPU k-mer seed lookup
- Merge Pairs GPU (wetSpring)
- SIMD-optimized `convolve_1d` (AVX2/NEON)
- Biosignal radix-2 FFT
- WFDB parser for arrhythmia databases
