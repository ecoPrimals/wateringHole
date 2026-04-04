# ecoPrimals — Cross-Spring Shader & Primitive Evolution

> How the ecoPrimals Springs collectively evolved BarraCUDA into the library
> groundSpring depends on for statistical validation.

**Last Updated**: March 11, 2026

---

## Overview

groundSpring delegates 11 functions to barracuda. Those barracuda functions
were not built in isolation — they were refined and battle-tested through
absorption from **four Springs**, each bringing domain-specific requirements
that hardened the shared library.

```
hotSpring (nuclear physics)     → f64 precision, spectral theory, DF64, Kokkos parity, sovereign compile 46/46
wetSpring (metagenomics)        → bio-stats, Shannon entropy, log_f64 fix, O₂-modulated Anderson W, paper extension roadmap
neuralSpring (ML/agents)        → spectral diagnostics, dispatch, xoshiro PRNG, NUCLEUS GPU dispatch, composition DAG, 25 absorbed workloads
airSpring (agriculture/hydro)   → Richards PDE, stats metrics, f64-canonical local compute
groundSpring (noise validation) → error handling patterns, validation harness
                                  ↓
                          barraCuda v0.3.5 standalone
                     719 WGSL shaders, toadStool S146, coralReef Iter 33
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

**March 2026 update**: hotSpring discovered that GPU f64 arithmetic diverges
from CPU at ULP level due to FMA fusion and SPIR-V reordering. In algorithms
with catastrophic cancellation (W(z) = 1 + z·Z(z) for plasma dispersion),
this amplifies to percent-level errors. Fix: compute small quantities directly
via asymptotic expansion. See `GPU_F64_NUMERICAL_STABILITY.md` for the full
writeup and cross-spring impact analysis.

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
| 4,500+ validation checks | — | Validates dispatch and spectral infra |
| 15 sovereign folding df64 WGSL shaders | S88 | df64 core streaming validated for ML workloads |
| `compile_shader_f64_hybrid` pattern | S88 | Reusable df64 preamble concatenation |
| Two-tier tolerance discovery (arith vs trans) | S88 | df64 precision characterization |
| `chi_squared_f64.wgsl` → `FusedChiSquaredGpu` | S64→S145 | Round-trip: neuralSpring domain → upstream f64 fused → all springs |
| `kl_divergence_f64.wgsl` → `FusedKlDivergenceGpu` | S64→S145 | Round-trip: neuralSpring domain → upstream f64 fused → all springs |
| `PipelineGraph` DAG | S133 | Absorbed by toadStool → orchestration for all springs |
| NUCLEUS GPU dispatch (eigensolve, attention) | S145 | GPU capability routing for NUCLEUS pipeline |
| `enable f64;` PTXAS silent-zero fix | S142 | Critical Ada Lovelace workaround for all f64 springs |
| `composition_pipeline()` mixed-hardware DAG | S145 | GPU+CPU stage interleaving with transfer cost |

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

## Spectral GPU Evolution Status (March 10, 2026)

The `spectral/` module in barraCuda is the most cross-spring validated
component in the ecosystem: **417+ checks** across 4 springs, reproducing
11 papers in Kachkovskiy's domain. This section tracks GPU-specific evolution.

### barraCuda `spectral/` WGSL Shaders

| Shader | Precision | Consuming Springs | Status |
|--------|-----------|-------------------|--------|
| `anderson_lyapunov_f64.wgsl` | f64 | hotSpring, groundSpring | Deployed |
| `anderson_lyapunov_f32.wgsl` | f32 | — | Deployed (fallback) |
| `batch_ipr_f64.wgsl` | f64 | neuralSpring | Deployed |
| `lanczos_iteration_f64.wgsl` | f64 | hotSpring, groundSpring | Deployed (SpMV only) |
| `anderson_coupling_f64.wgsl` | f64 | groundSpring | Deployed |
| `fft_radix2_f64.wgsl` | f64 | — | Deployed |

### GPU Validation Parity (per spring)

| Spring | GPU Checks | Max N Validated | Key Metric |
|--------|:----------:|:---------------:|------------|
| hotSpring | 14/14 | N=4096 (SpMV), N=144 (Lanczos) | Parity 1.78e-15 / 1e-15 |
| groundSpring | Wired (4 experiments) | N varies | 47.4× speedup (Exp 009) |
| neuralSpring | All tiers pass | Paper 022-023 | 104× vs Python |
| wetSpring | N/A (application layer) | N ≤ 1000 | CPU sufficient |

### Remaining GPU Gaps

| Gap | Blocking | Priority | Owner |
|-----|----------|:--------:|-------|
| Fully GPU-resident Lanczos (dot/axpy/reorthog on GPU) | Large-N performance | P1 | barraCuda |
| `tridiag_eigh` GPU eigenvectors | groundSpring Exp 012 | P1 | barraCuda |
| Two-particle Anderson Hamiltonian (L² space) | Kachkovskiy Bourgain paper | P2 | barraCuda + groundSpring |
| GPU Lanczos at N > 10k | Kachkovskiy demo | P1 | hotSpring + barraCuda |
| SciPy `eigsh` comparison harness | Benchmark credibility | P0 | hotSpring |
| Kokkos spectral comparison | Vendor comparison | P2 | barraCuda |

See: `handoffs/SPECTRAL_GPU_CROSS_SPRING_KACHKOVSKIY_EVOLUTION_HANDOFF_MAR10_2026.md`

---

## coralReef Multi-Language Frontend Guidance (Iteration 23)

As of Iteration 23, coralReef accepts three shader input languages.
All three share the same pipeline: naga IR → codegen SSA IR → optimize →
legalize → register allocation → encode → native binary.

### Input Languages

| Language | API | Use Case |
|----------|-----|----------|
| **WGSL** | `compile_wgsl()` / `compile_wgsl_full()` | Primary — all barraCuda shaders, df64 preamble auto-prepend |
| **SPIR-V** | `compile()` / `compile_full()` | Binary interchange — pre-compiled modules, cross-tool pipelines |
| **GLSL 450** | `compile_glsl()` / `compile_glsl_full()` | Compute absorption — existing GPU libraries, CUDA↔GLSL ports |

### Math Function Coverage (Iteration 23)

Iteration 23 added 11 math functions that are critical for GLSL shaders
(naga's GLSL frontend passes these through as raw MathFunction variants,
unlike the WGSL frontend which pre-lowers them):

| Function | Status | Notes |
|----------|--------|-------|
| `tanh` | ✅ NEW | exp(2x)-based — unblocks ESN reservoir update (neuralSpring) |
| `fract` | ✅ NEW | `x - floor(x)` |
| `sign` | ✅ NEW | FSetP + Sel pattern |
| `dot` | ✅ NEW | FMul + FFma chain for N-component vectors |
| `mix` | ✅ NEW | `(b-a)*t + a` via FMA |
| `step` | ✅ NEW | FSetP + Sel |
| `smoothstep` | ✅ NEW | `t*t*(3-2*t)` with saturate clamp |
| `length` | ✅ NEW | `sqrt(dot(v,v))` via Rsq + Rcp |
| `normalize` | ✅ NEW | `v * rsq(dot(v,v))` |
| `cross` | ✅ NEW | 3-component FMul + FFma pattern |
| `trunc` | ✅ NEW | FRnd with zero mode (f32) / floor+sign restore (f64) |

**Previously supported**: abs, min, max, clamp, floor, ceil, round,
sqrt, inverseSqrt, sin, cos, exp, log, exp2, log2, pow, tan, fma,
countOneBits, reverseBits, firstLeadingBit, countLeadingZeros.

### Spring-Specific Guidance

**barraCuda**: Continue authoring WGSL as the canonical shader language.
Use `compile_wgsl()` for all new math. Use `compile_glsl()` only when
absorbing existing GLSL compute libraries from external sources. The
df64 preamble is only auto-prepended for WGSL — GLSL shaders must
include all needed functions inline. Tanh is now natively supported
in the compiler (no preamble needed for f32).

**hotSpring / neuralSpring**: GLSL 450 compute shaders from external
physics/ML libraries now compile with full math coverage (including
tanh, dot, mix, normalize, cross, length, smoothstep). The ESN
reservoir update shader (`esn_reservoir_update`) now compiles — tanh
activation was the blocker. Place GLSL fixtures in `tests/fixtures/glsl/`.

**groundSpring**: The SPIR-V roundtrip path (WGSL → naga → SPIR-V →
compile) validates binary-level reproducibility. Use this to verify that
sovereign compilation produces identical binaries from both text and
binary input representations.

**All springs**: When importing new shaders for coralReef testing:
- WGSL corpus snapshots go in `crates/coral-reef/tests/fixtures/wgsl/corpus/`
- Compiler-owned test shaders stay in `crates/coral-reef/tests/fixtures/wgsl/`
- GLSL compute fixtures go in `crates/coral-reef/tests/fixtures/glsl/`

### Known SPIR-V Frontend Gaps

| Gap | Effect | Workaround |
|-----|--------|------------|
| `Discriminant` expression | Switch-like patterns fail | Use WGSL path (chain-of-comparisons works) |
| Non-literal constant initializer | Struct/array const init fails | Use WGSL path or runtime initialization |

These are tracked as ignored tests in `spirv_roundtrip.rs`.

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

## barraCuda v0.3.5 Evolution (March 2026)

The standalone extraction (v0.3.0) and subsequent evolution (v0.3.1 → v0.3.5)
marks a phase shift where cross-spring absorption accelerates:

### What evolved

| Feature | Origin | Consumers |
|---------|--------|-----------|
| **wgpu 22 → 28** | barraCuda core | All Springs (Device/Queue no longer Arc-wrapped) |
| **Fp64Strategy** (Native/Hybrid/Concurrent) | hotSpring DF64 discovery | All Springs — automatic shader selection per GPU |
| **DF64 fused shaders** (mean_variance, correlation) | hotSpring `df64_core.wgsl` + wetSpring Welford | Consumer GPU users get ~10x throughput |
| **TensorContext fast path** (15+ ops) | barraCuda refactoring | wetSpring (pooled buffers), groundSpring (stats) |
| **5-accumulator Pearson** | wetSpring correlation + hotSpring precision | Single dispatch for mean+var+cov+pearson_r |
| **31 bio ops in `ops/bio/`** | wetSpring (handoff v4-v8) + neuralSpring (metalForge) | All Springs via barraCuda |
| **Fused chi-squared GPU** | neuralSpring S69 | Available for enrichment analysis |
| **3-tier precision model** | barraCuda lean-out (Mar 8) | F32/F64/Df64 aligned with coralReef `Fp64Strategy` |

### Cross-pollination chains

```
hotSpring → df64_core.wgsl → neuralSpring (folding), wetSpring (variance, Shannon)
wetSpring → HMM forward → neuralSpring (+ backward, viterbi) → shared hmm module
wetSpring → FusedMapReduceF64 → airSpring (ET₀), groundSpring (diversity)
neuralSpring → EA bio ops → wetSpring bio pipelines (pairwise_*, hill_gate)
airSpring → f64-canonical pattern → all Springs (precision per silicon)
groundSpring → batched_multinomial → wetSpring (rarefaction GPU)
```

### Validation at wetSpring V98

- 1,347 tests (1,047 lib + 200 forge + 100 doc): ALL PASS
- 296 validation/benchmark binaries, 8,604+ checks: ALL PASS
- V98 full chain: Paper Math v5 (32/32) → CPU v24 (67/67) → GPU v13 (25/25) → Streaming v11 (25/25) → metalForge v16 (24/24) = **173/173 PASS**
- 150+ barraCuda primitives consumed, zero local WGSL, zero unsafe code
- GPU Hybrid-aware: FusedMapReduceF64 validated on consumer GPU (RTX 4070)
- Cross-spring S93 (59/59): provenance audit verified
- Python vs Rust v3 (35/35): 15 domains bit-identical to SciPy/NumPy
