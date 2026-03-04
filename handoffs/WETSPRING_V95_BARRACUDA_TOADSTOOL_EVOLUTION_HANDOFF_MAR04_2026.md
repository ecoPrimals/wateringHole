# wetSpring V95 → barraCuda/ToadStool Evolution Handoff

**Date:** 2026-03-04
**From:** wetSpring V95 (ecoPrimals)
**To:** barraCuda + ToadStool teams
**License:** AGPL-3.0-or-later
**Covers:** wetSpring V90–V95 (2026-03-02 → 2026-03-04)

---

## Executive Summary

- wetSpring now consumes **150+ barraCuda primitives** (up from 144 at V93)
- **6 new GPU ops** wired as lean wrappers: `BatchToleranceSearchF64`, `KmdGroupingF64`,
  `JackknifeMeanGpu`, `BootstrapMeanGpu`, `KimuraGpu`, `HargreavesBatchGpu`
- **2 new CPU delegations**: `rk45_solve` (adaptive ODE) and `gradient_1d`
- **47 GPU modules**, all lean (zero local WGSL, zero local math)
- **1,261 tests**, 94.69% line coverage, 0 clippy warnings (pedantic)
- **Exp305**: 59/59 cross-spring validation checks, full provenance documentation
- RK45 adaptive achieves **18.5× fewer steps** than fixed-step RK4 at same accuracy

---

## Part 1: What wetSpring Now Consumes

### GPU Ops (47 lean wrappers)

All GPU modules delegate to barraCuda ops via `Arc<WgpuDevice>`. No local WGSL.

**New in V95:**

| Wrapper | barraCuda Op | Domain |
|---------|-------------|--------|
| `tolerance_search_gpu` | `BatchToleranceSearchF64` | Mass spec PFAS screening |
| `kmd_grouping_gpu` | `KmdGroupingF64` | Kendrick mass defect |
| `stats_extended_gpu` | `JackknifeMeanGpu` | Resampling statistics |
| | `BootstrapMeanGpu` | Resampling statistics |
| | `KimuraGpu` | Population genetics |
| | `HargreavesBatchGpu` | Hydrology ET₀ |

**Existing (44 wrappers):**
FusedMapReduceF64, BrayCurtisF64, BatchedEighGpu, BatchedOdeRK4F64 (5 systems),
GemmF64/GemmCachedF64, KrigingF64, KmerHistogramGpu, UniFracPropagateGpu,
VarianceF64, CorrelationF64, CovarianceF64, WeightedDotF64, FelsensteinGpu,
GillespieGpu, SmithWatermanGpu, TreeInferenceGpu, DiversityFusionGpu,
MultiHeadEsn, PeakDetectF64, PairwiseHammingGpu, BatchFitnessGpu,
plus 20+ bio-domain ops (ANI, SNP, dN/dS, pangenome, HMM, DADA2, etc.)

### CPU Delegations (~30)

**New in V95:**

| Function | barraCuda Module | Notes |
|----------|-----------------|-------|
| `rk45_integrate` | `numerical::rk45::rk45_solve` | Adaptive Dormand-Prince 5(4), 54 steps vs 1000 fixed |
| `gradient_1d` | `numerical::gradient_1d` | Central differences, O(dx²) |

**Existing:** `norm_ppf`, `norm_cdf`, `erf`, `ln_gamma`, `regularized_gamma`,
`ridge_regression`, `graph_laplacian`, `nmf`, `anderson_eigenvalues`,
`lanczos_eigenvalues`, `boltzmann_sampling`, `sobol_scaled`, `latin_hypercube`,
`shannon`, `simpson`, `jackknife_mean_variance`, `bootstrap_mean`,
`kimura_fixation_prob`, `hargreaves_et0`, `trapz`, `numerical_hessian`,
`dot`, `l2_norm`, `level_spacing_ratio`, etc.

---

## Part 2: What wetSpring Learned (Relevant to barraCuda Evolution)

### 2a: RK45 vs RK4 — Adaptive Stepping is Transformative

wetSpring bio ODE systems (quorum sensing, phage defense, cooperation,
bistable switches, capacitor signaling) currently use fixed-step RK4 via
`BatchedOdeRK4F64`. After wiring `rk45_solve`:

- Exponential decay: **54 adaptive steps vs 1000 fixed** (18.5× fewer)
- Logistic growth: adaptive achieves same K=1 endpoint with far fewer evaluations
- Lotka-Volterra 2D: 82 µs in release mode

**barraCuda action:** Consider adding `BatchedOdeRK45F64` GPU shader for
adaptive stepping. The per-trajectory adaptive step size control is a natural
fit for GPU dispatch (independent trajectories, no synchronization needed).

### 2b: Bootstrap CI API Observation

`bootstrap_mean()` returns `BootstrapCI` which is great for the full
confidence interval. For large-scale resampling (10K+ samples × 1000 bootstrap),
the `BootstrapMeanGpu::dispatch()` returns raw resampled means — the CI
computation then happens CPU-side. This is the right design for GPU dispatch.

### 2c: Precision Dispatch Per Hardware

wetSpring's `GpuF64` wraps `GpuDriverProfile` for hardware-aware precision:
- Native f64 on Titan V, V100, MI250X
- DF64 (double-float f32 pair) on consumer GPUs (RTX 4070, RDNA2+)
- F32 downcast for inference-only paths

The `optimal_precision()` method works well. No issues observed.

### 2d: Cross-Spring Shader Evolution Patterns

wetSpring documented the full provenance chain showing how shaders flow
between springs via barraCuda:

```
Python baseline → Rust validation → GPU acceleration → barraCuda absorption
→ cross-spring availability → sovereign pipeline
```

Key pattern: hotSpring contributes precision (f64 polyfills, DF64),
neuralSpring contributes ML dispatch (GEMM, batch ops), groundSpring
contributes mathematical physics (spectral, sampling), wetSpring contributes
biology (diversity, ODE, phylogeny, mass spec). All flow through barraCuda.

---

## Part 3: Absorption Requests (wetSpring → barraCuda)

### P1 — High Value

| Request | Justification | wetSpring Use Case |
|---------|---------------|-------------------|
| `BatchedOdeRK45F64` GPU shader | RK45 adaptive is 18× more efficient than fixed RK4 | Bio ODE systems (QS, cooperation, phage) |
| `ComputeDispatch` tarpc integration | Enable remote GPU dispatch for NUCLEUS cluster | metalForge cross-node routing |
| DF64 GEMM public API | Consumer GPU GEMM at near-f64 precision | Spectral cosine, taxonomy classification |

### P2 — Medium Value

| Request | Justification |
|---------|---------------|
| `BandwidthTier` integration | Tier-aware buffer size selection for heterogeneous GPU clusters |
| `domain-genomics` crate extraction | Separate genomics ops from general math for dependency slimming |
| Adaptive tolerance for `KmdGroupingF64` | Auto-select KMD tolerance based on mass resolution |

### P3 — Future

| Request | Notes |
|---------|-------|
| Multi-GPU dispatch for ODE sweeps | Parameter sweep across GPU fleet |
| FHE ops for secure genomics | FHE integration for privacy-preserving genomic queries |

---

## Part 4: Absorption Offers (wetSpring → barraCuda)

wetSpring has validated these patterns that could be absorbed:

| Pattern | File | Description |
|---------|------|-------------|
| `rk45_integrate` wrapper | `bio/ode.rs` | Wraps `Rk45Result` into `OdeResult` with flat y-history |
| Bio KMD screen | `bio/kmd_gpu.rs` | PFAS-specific KMD screening with CF2 unit defaults |
| Tolerance search scoring | `bio/tolerance_search_gpu.rs` | CPU fallback with linear score interpolation |
| Multi-signal ODE convergence | `bio/ode.rs` | Guard for fixed-step RK4 stability in bistable systems |

---

## Part 5: Quality Gate Summary

| Check | Status | Count |
|-------|--------|-------|
| `cargo test --workspace --lib` | PASS | 1,261 tests |
| `cargo clippy --pedantic` | PASS | 0 warnings |
| `cargo fmt --check` | PASS | Clean |
| `cargo doc --no-deps` | PASS | 0 warnings |
| `cargo llvm-cov` | PASS | 94.69% line coverage |
| Exp305 validation | PASS | 59/59 checks |

## Part 6: Files Changed (V95)

### New
- `barracuda/src/bio/tolerance_search_gpu.rs`
- `barracuda/src/bio/kmd_grouping_gpu.rs`
- `barracuda/src/bio/stats_extended_gpu.rs`
- `barracuda/src/bin/validate_cross_spring_s93.rs`

### Modified
- `barracuda/src/bio/mod.rs` — 3 new GPU module registrations
- `barracuda/src/bio/ode.rs` — `rk45_integrate` + 2 tests
- `barracuda/src/special.rs` — `gradient_1d` + 2 tests
- `barracuda/Cargo.toml` — Exp305 binary registration
- 50+ bio module files — doc evolution (ToadStool → barraCuda)
