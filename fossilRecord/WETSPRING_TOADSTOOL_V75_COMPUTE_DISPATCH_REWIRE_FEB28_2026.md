# wetSpring → toadStool / barracuda — V75 ComputeDispatch Rewire + New Op Adoption

**Date:** February 28, 2026
**From:** wetSpring
**To:** toadStool / barracuda core team
**Covers:** ComputeDispatch adoption (6 GPU modules), BatchedMultinomialGpu, PairwiseL2Gpu, FstVariance
**ToadStool Pin:** S68+ (`e96576ee`) — no new commits since V70
**License:** AGPL-3.0-only

---

## Executive Summary

- **82 ToadStool primitives** consumed (was 79: +`ComputeDispatch`, +`BatchedMultinomialGpu`, +`PairwiseL2Gpu`)
- **6 GPU modules** refactored from manual BGL to `ComputeDispatch` builder (~400 lines removed)
- **`rarefaction_gpu`** evolved from `FusedMapReduceF64` composition to dedicated `BatchedMultinomialGpu` + `DiversityFusionGpu`
- **2 new modules** adopted: `pairwise_l2_gpu` (L2 distances), `fst_variance` (Weir-Cockerham FST)
- **0 regressions**: 955 lib + 60 integration + 20 doc + 113 forge tests PASS
- **clippy pedantic** CLEAN (both crates, all targets)

---

## Changes

### 1. ComputeDispatch Adoption

Replaced manual bind-group layout / pipeline / bind-group / encoder / dispatch boilerplate
with `barracuda::device::ComputeDispatch` builder pattern in 6 GPU modules:

| Module | Before | After |
|--------|--------|-------|
| `gemm_cached.rs` | Manual BGL + pipeline cache | `ComputeDispatch::new().shader(GemmF64::WGSL).f64().uniform().storage_read().storage_rw().dispatch().submit()` |
| `bistable_gpu.rs` | Manual BGL + pipeline | `ComputeDispatch::new().shader(&wgsl).f64().uniform().storage_read().storage_rw().dispatch().submit()` |
| `capacitor_gpu.rs` | Manual BGL + pipeline | Same pattern |
| `cooperation_gpu.rs` | Manual BGL + pipeline | Same pattern |
| `multi_signal_gpu.rs` | Manual BGL + pipeline | Same pattern |
| `phage_defense_gpu.rs` | Manual BGL + pipeline | Same pattern |

**Impact:** Removed `pipeline` and `bgl` fields from all structs. `new()` became `const fn`
(no shader compilation at init). Buffer creation still explicit (data-dependent sizes).

**Note:** `storage_bgl_entry` / `uniform_bgl_entry` imports removed from these modules.
Other modules that delegate to high-level ToadStool ops (e.g. `FusedMapReduceF64::run()`,
`BatchedOdeRK4F64`, `BrayCurtisF64`) already handle BGL internally — no change needed.

### 2. BatchedMultinomialGpu Adoption (rarefaction_gpu)

`rarefaction_gpu` evolved from composing `FusedMapReduceF64` + CPU `subsample_community`
to using dedicated ToadStool ops:

```text
Before: CPU subsample_community() → FusedMapReduceF64 for diversity
After:  BatchedMultinomialGpu::sample() → DiversityFusionGpu::compute()
```

- All bootstrap replicates sampled in one GPU dispatch (xoshiro128** PRNG)
- Fused Shannon + Simpson + evenness per replicate in one GPU pass
- CPU fallback preserved for < 50 species (dispatch overhead threshold)

### 3. PairwiseL2Gpu (new module)

New `bio::pairwise_l2_gpu` module wrapping `barracuda::ops::bio::PairwiseL2Gpu`:

- Computes condensed N×(N-1)/2 Euclidean distances on GPU
- Uses f32 internally for broad GPU compatibility
- Returns f64 results (converted from f32)
- Validation in `validate_diversity_gpu` binary

### 4. FstVariance (new module)

New `bio::fst_variance` module re-exporting `barracuda::ops::bio::fst_variance`:

- Weir-Cockerham FST decomposition (CPU-only, gated behind `gpu` feature)
- `FstResult` struct with FST, FIS, FIT
- Available for population genetics experiments

---

## Primitive Count (82)

| Category | Count | Examples |
|----------|:-----:|---------|
| special | 3 | erf, ln_gamma, regularized_gamma_p |
| stats | 11 | mean, percentile, pearson, spearman, shannon, hill, monod, fit_linear |
| numerical | 8 | trapz, BatchedOdeRK4 + 5 ODE systems |
| linalg | 5 | graph_laplacian, ridge_regression, nmf, CsrMatrix |
| device | 8 | WgpuDevice, ComputeDispatch, BufferPool, TensorContext, GpuDriverProfile |
| ops (math) | 8 | FusedMapReduceF64, GemmF64, BrayCurtisF64, KrigingF64, PeakDetectF64, TranseF64, SparseGemmF64, BatchedEighGpu |
| ops (bio) | 31 | Felsenstein, SW, Gillespie, TreeInference, KmerHist, DiversityFusion, ANI, DnDs, Dada2, HMM, Pangenome, Quality, RF, SNP, Taxonomy, UniFrac, PairwiseHamming, PairwiseJaccard, PairwiseL2, SpatialPayoff, BatchFitness, LocusVariance, BatchedMultinomial, FstVariance |
| spectral | 5 | anderson_3d, lanczos, level_spacing_ratio, GOE_R, POISSON_R |
| precision | 2 | Precision enum, BandwidthTier |
| validation | 1 | Validator (local, not ToadStool's ValidationHarness) |

---

## Absorption Candidates Remaining

### 1. `bio::esn` → `barracuda::ml::esn`
Unchanged from V70. 776-line ESN is training-focused; ToadStool `esn_v2` is inference.

### 2. `BatchReconcileGpu`
Still needed. `reconciliation_gpu` uses `FusedMapReduceF64` for cost aggregation
but CPU DP for the core algorithm. Full GPU DP kernel (one workgroup per gene family)
doesn't exist in either codebase.

### 3. Newly Available Ops (Not Yet Needed)

| Op | Status |
|----|--------|
| `WrightFisherGpu` | Available — no population genetics experiments yet |
| `StencilCooperationGpu` | Available — different model from cooperation ODE |
| `HillGateGpu` | Available — no synthetic biology experiments |
| `MultiObjFitnessGpu` | Available — no multi-objective optimization |
| `NcbiCache` | Available — wetSpring uses NestGate instead |

---

## Revalidation Results

| Suite | Count | Result |
|-------|:-----:|--------|
| `wetspring-barracuda` lib | 955 | ALL PASS |
| `wetspring-barracuda` integration | 60 | ALL PASS |
| `wetspring-barracuda` doc tests | 20 | ALL PASS |
| `wetspring-forge` lib | 113 | ALL PASS |
| clippy pedantic (barracuda) | — | CLEAN |
| clippy pedantic (forge) | — | CLEAN |

---

## Supersedes

- `WETSPRING_TOADSTOOL_V70_S68_PRECISION_EVOLUTION_FEB28_2026.md` (primitive count updated, ComputeDispatch adopted)
