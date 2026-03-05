# ecoPrimals — Cross-Spring Shader & Primitive Evolution

> How the ecoPrimals Springs collectively evolved BarraCUDA into the library
> groundSpring depends on for statistical validation.

**Last Updated**: March 5, 2026

---

## Overview

groundSpring delegates 11 functions to barracuda. Those barracuda functions
were not built in isolation — they were refined and battle-tested through
absorption from **four Springs**, each bringing domain-specific requirements
that hardened the shared library.

```
hotSpring (nuclear physics)     → f64 precision, spectral theory, DF64
wetSpring (metagenomics)        → bio-stats, Shannon entropy, log_f64 fix
neuralSpring (ML/agents)        → spectral diagnostics, dispatch, xoshiro PRNG
airSpring (agriculture/hydro)   → Richards PDE, stats metrics, f64-canonical local compute
groundSpring (noise validation) → error handling patterns, validation harness
                                  ↓
                          BarraCUDA S93 + DF64
                     21,500+ tests, 845+ WGSL shaders
```

---

## hotSpring → Precision Foundation

hotSpring's nuclear physics work (lattice QCD, nuclear structure) established
the f64 precision infrastructure that ALL statistical operations depend on.

| Contribution | Session | groundSpring Benefit |
|-------------|---------|---------------------|
| `df64_core.wgsl` | S58 | Future GPU bootstrap precision |
| `Fp64Strategy` + `split_workgroups` | S58 | Correct f64 GPU dispatch strategy |
| `spectral/anderson.rs` | S26 | **Direct delegation**: `lyapunov_exponent`, `lyapunov_averaged` |
| `sum_reduce_f64.wgsl` | S46 | Foundation for RMSE/MBE GPU ops |
| `special/anderson_transport.rs` | S52 | **Direct delegation**: `localization_length` |
| CG solver shaders (6 kernels) | S46-48 | Pattern: iterative GPU solver with convergence |
| 195 nuclear physics validation checks | — | Validates the precision path we depend on |

**Why it matters**: hotSpring discovered that FP64 operations on consumer GPUs
(RTX 4070) need careful workgroup sizing to avoid precision loss. This
discovery propagated to all barracuda f64 ops, including the `stats::*`
functions groundSpring delegates to.

---

## wetSpring → Bio-Statistical Primitives

wetSpring's metagenomics work (16S, metabolomics, diversity) contributed the
statistical and biological primitives groundSpring uses.

| Contribution | Session | groundSpring Benefit |
|-------------|---------|---------------------|
| `FusedMapReduceF64` (Shannon/Simpson) | S15 | Future GPU `shannon_diversity` target |
| `log_f64()` coefficient fix (~1e-3 → 1e-15) | S15 | Accuracy of Shannon entropy calculations |
| `GillespieGpu` | S27 | Future GPU for `birth_death_ssa` |
| `ridge_regression` | S15 | Available for regularized fitting |
| 5 ODE biosystems | S58 | Pattern: CPU reference → GPU promotion |
| `bray_curtis_f64` | S15 | Diversity metric for rarefaction context |
| 728 Rust tests + 95 experiments | — | Validates the statistical paths |

**Why it matters**: wetSpring discovered a precision issue in `log_f64()`
polynomial coefficients where the GPU log was ~1e-3 off from CPU. The fix
propagated to `FusedMapReduceF64::shannon_entropy`, which groundSpring will
eventually delegate `shannon_diversity` to.

---

## neuralSpring → ML/Spectral Infrastructure

neuralSpring's neural network and agent work contributed the dispatch
infrastructure and spectral diagnostics.

| Contribution | Session | groundSpring Benefit |
|-------------|---------|---------------------|
| `empirical_spectral_density` | S54 | Future Anderson spectral diagnostics |
| `marchenko_pastur_bounds` | S54 | Random matrix theory bounds |
| `dispatch/domain_ops.rs` (device: Option) | S52 | Blueprint for GPU dispatch |
| `boltzmann_sampling` (Metropolis MCMC) | S56 | Future MC uncertainty propagation |
| `prng_xoshiro` GPU PRNG | S43 | PRNG alignment target for Phase 2b |
| `TensorSession` (matmul, relu, softmax) | S20 | ML pipeline infrastructure |
| 2,480+ validation checks | — | Validates dispatch and spectral infra |
| 15 sovereign folding df64 WGSL shaders | S88 | df64 core streaming validated for ML workloads |
| `compile_shader_f64_hybrid` pattern | S88 | Reusable df64 preamble concatenation |
| Two-tier tolerance discovery (arith vs trans) | S88 | df64 precision characterization |

**Why it matters**: neuralSpring's `domain_ops.rs` dispatch pattern
(`device: Option<&Arc<WgpuDevice>>`) is the blueprint for how groundSpring's
6 pending GPU metrics should be wired — `None` for CPU, `Some(device)` for GPU.
Session 88's df64 core streaming evolution validates that the hotSpring/ToadStool
df64 pattern generalizes to ML workloads (attention, normalization, activations)
with consistent precision characteristics.

---

## airSpring → Agricultural Science & Hydrology Primitives

airSpring's agricultural science work (FAO-56 ET₀, Richards PDE, soil physics,
coupled hydrology) contributed domain-specific fixes, validated the
`compile_shader_universal()` pattern for per-silicon precision, and proved
the Write → Absorb → Lean cycle for ecological systems.

| Contribution | Session | Ecosystem Benefit |
|-------------|---------|-------------------|
| Richards PDE solver | S40 | Absorbed upstream — unsaturated flow on GPU |
| Stats metrics (RMSE, R², MBE, IoA) | S64 | Absorbed upstream — all Springs benefit |
| `pow_f64` fractional exponent fix | TS-001 | Fixed ET₀ atmospheric pressure calc for all consumers |
| `acos` precision boundary fix | TS-003 | Fixed solar geometry for neuralSpring and groundSpring |
| Reduce buffer N≥1024 fix | TS-004 | Fixed fused reduce for wetSpring diversity |
| 6 f64-canonical local WGSL ops | V0.6.9 | SCS-CN, Stewart, Makkink, Turc, Hamon, Blaney-Criddle — ready for absorption |
| `compile_shader_universal()` validation | V0.6.9 | Confirmed f64→f32 downcast pattern works for 6 ops across RTX 4070 + Titan V |
| NVK/Mesa f64 reliability finding | V0.6.9 | 10% dispatch failure rate on Titan V NVK — documented for hardware matrix |
| `json_f64_required` hotSpring pattern | V0.6.9 | Structured exit(1) for validation binaries — adopted from hotSpring |
| 852 lib + 33 integration tests | — | Validates agricultural science paths in BarraCuda |
| 78 experiments, 1237/1237 Python baselines | — | 57 papers reproduced with full provenance |

**Why it matters**: airSpring proved that the `compile_shader_universal()` pattern
enables a single f64-canonical WGSL shader to run correctly on both pro GPUs
(Titan V, native f64) and consumer GPUs (RTX 4070, f32 downcast), with
tolerance-documented precision loss. This validates the BarraCuda promise:
"Math is universal, precision is silicon."

---

## groundSpring → Validation Patterns

groundSpring contributes back to the ecosystem primarily through **patterns
and learnings** rather than GPU shaders:

| Contribution | Benefit to Ecosystem |
|-------------|---------------------|
| `if let Ok` + always-compiled CPU fallback | Adopted as wateringHole standard for barracuda delegation |
| `ValidationHarness` pattern | ToadStool absorbed as `barracuda::validation::ValidationHarness` |
| Capability-based primal discovery | wateringHole standard: scan for capability, not primal name |
| Three-mode validation (local / barracuda / barracuda-gpu) | Proves correctness across feature configurations |
| Zero-overhead benchmark methodology | Proves barracuda delegation is free for compute-heavy code |
| Tolerance documentation standard | Every tolerance justified with mathematical basis |
| 2 production WGSL shaders | `batched_multinomial.wgsl`, `mc_et0_propagate.wgsl` (pending absorption) |

---

## Multi-Spring Convergence

Several barracuda modules benefited from **multiple Springs discovering the
same need independently**:

| Module | Springs | Evolution |
|--------|---------|-----------|
| **f64 precision** | hotSpring + wetSpring + neuralSpring | Three Springs found precision issues; all fixes merged |
| **bio ops** | wetSpring + neuralSpring | Complementary biological simulation primitives |
| **spectral analysis** | hotSpring + neuralSpring | Physics + ML perspectives on spectral methods |
| **PRNG** | neuralSpring + wetSpring + groundSpring | GPU xoshiro128** shared across stochastic workloads |
| **validation patterns** | All four Springs | `ValidationHarness`, tolerance docs, struct extraction |

---

## groundSpring Delegation Lineage

Each of groundSpring's 11 delegations has a traceable cross-spring history:

| # | groundSpring fn | barracuda fn | Primary Origin | Validated By |
|---|----------------|--------------|---------------|-------------|
| 1 | `pearson_r` | `stats::pearson_correlation` | ToadStool core | wetSpring + neuralSpring |
| 2 | `spearman_r` | `stats::correlation::spearman_correlation` | S54 (neuralSpring baseCamp) | neuralSpring spectral diagnostics |
| 3 | `sample_std_dev` | `stats::correlation::std_dev` | ToadStool core | wetSpring diversity metrics |
| 4 | `covariance` | `stats::correlation::covariance` | ToadStool core | neuralSpring correlation matrices |
| 5 | `norm_cdf` | `stats::norm_cdf` | ToadStool core | All Springs (significance testing) |
| 6 | `norm_ppf` | `stats::norm_ppf` | ToadStool core | groundSpring bootstrap CI |
| 7 | `chi2_statistic` | `stats::chi2_decomposed` | ToadStool core | wetSpring goodness-of-fit |
| 8 | `bootstrap_mean` | `stats::bootstrap_mean` | ToadStool core | groundSpring RAWR validation |
| 9 | `lyapunov_exponent` | `spectral::lyapunov_exponent` | hotSpring S26 (Kachkovskiy) | hotSpring spectral checks |
| 10 | `lyapunov_averaged` | `spectral::lyapunov_averaged` | hotSpring S26 (Kachkovskiy) | hotSpring + groundSpring |
| 11 | `analytical_localization_length` | `special::localization_length` | wetSpring S52 (transport) | groundSpring Anderson checks |

---

## Benchmark: Cross-Spring Evolution Impact

The cross-spring evolution (S50–S62) eliminated the link/init overhead that
groundSpring V7 observed:

| Period | Total Runtime | Overhead vs Local |
|--------|-------------|-------------------|
| V7 (pre-S50) | 2721ms | **+6%** |
| V9 (post-S62) | 2076ms | **~0%** |

The S60-61 `cpu-math` modularization and dead-code elimination across sessions
reduced barracuda's binary size and startup cost, benefiting all consumer Springs.

---

## barraCuda v0.3.3 Evolution (March 2026)

The standalone extraction (v0.3.0) and subsequent evolution (v0.3.1 → v0.3.3)
marks a phase shift where cross-spring absorption accelerates:

### What evolved

| Feature | Origin | Consumers |
|---------|--------|-----------|
| **wgpu 22 → 28** | barraCuda core | All Springs (Device/Queue no longer Arc-wrapped) |
| **Fp64Strategy** (Native/Hybrid/Concurrent) | hotSpring DF64 discovery | All Springs — automatic shader selection per GPU |
| **DF64 fused shaders** (mean_variance, correlation) | hotSpring `df64_core.wgsl` + wetSpring Welford | Consumer GPU users get ~10x throughput |
| **TensorContext fast path** (15+ ops) | barraCuda refactoring | wetSpring (pooled buffers), groundSpring (stats) |
| **5-accumulator Pearson** | wetSpring correlation + hotSpring precision | Single dispatch for mean+var+cov+pearson_r |
| **32 bio ops in `ops/bio/`** | wetSpring (handoff v4-v8) + neuralSpring (metalForge) | All Springs via barraCuda |
| **Fused chi-squared GPU** | neuralSpring S69 | Available for enrichment analysis |
| **compile_shader_universal** | airSpring V0.6.9 | Ecosystem-wide: f64→f32 downcast |

### Cross-pollination chains

```
hotSpring → df64_core.wgsl → neuralSpring (folding), wetSpring (variance, Shannon)
wetSpring → HMM forward → neuralSpring (+ backward, viterbi) → shared hmm module
wetSpring → FusedMapReduceF64 → airSpring (ET₀), groundSpring (diversity)
neuralSpring → EA bio ops → wetSpring bio pipelines (pairwise_*, hill_gate)
airSpring → compile_shader_universal → all Springs (precision per silicon)
groundSpring → batched_multinomial → wetSpring (rarefaction GPU)
```

### Validation at wetSpring V97b

- 1,247 unit tests (1,047 lib + 200 forge): ALL PASS
- 26 CPU validation binaries: ALL PASS
- Cross-spring S93 (59/59): provenance audit verified
- Python vs Rust v3 (35/35): 15 domains bit-identical to SciPy/NumPy
- ToadStool S70 rewire (42/42): new stats primitives validated
