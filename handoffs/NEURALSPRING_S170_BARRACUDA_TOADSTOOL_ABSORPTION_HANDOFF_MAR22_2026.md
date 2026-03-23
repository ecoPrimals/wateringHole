# neuralSpring S170 → barraCuda / toadStool Absorption Handoff

**Date:** March 22, 2026  
**From:** neuralSpring S170  
**To:** barraCuda team, toadStool team  
**License:** AGPL-3.0-or-later

---

## Executive Summary

neuralSpring S170 is the largest downstream consumer of barraCuda’s GPU math engine, validating **1,195+** scientific computations against barraCuda kernels and WGSL. This handoff documents: (1) the **API surface** neuralSpring consumes, (2) **breakages and deprecations** from barraCuda **v0.3.7**, (3) **absorption opportunities** for toadStool and upstream consolidation, (4) **shader provenance** and catalog gaps, and (5) **patterns** in neuralSpring worth sharing (dispatch facade, niche self-knowledge, discovery, CPU/GPU `Dispatcher`).

**Upstream asks (barraCuda):**

- Document the **`DeviceCapabilities` migration path** from deprecated `GpuDriverProfile::from_device()`, with equivalents for `fp64_strategy()`, `precision_routing()`, `needs_pow_f64_workaround()`, and `f64_zeros_risk()`.
- Consider re-exposing a **`device()` (or `wgpu_device()`) accessor** on `MultiHeadEsn` for downstream convenience after its removal in v0.3.7.
- Provide a **stable shader catalog** (names + content hashes) so consumers are not forced to track provenance via comments alone.

---

## Part 1: barraCuda API Surface Consumed by neuralSpring

### 1a. Device & driver

| Area | Symbols / usage |
|------|-----------------|
| Construction & compile | `WgpuDevice::new()`, `compile_shader()`, `compile_shader_f64()`, `compile_shader_df64()`, `compile_shader_universal()` |
| Profile (deprecated) | `GpuDriverProfile::from_device()` — **deprecated** in v0.3.7; neuralSpring uses `#[expect(deprecated)]` pending migration to `DeviceCapabilities` |
| Methods used today | `fp64_strategy()`, `precision_routing()`, `needs_pow_f64_workaround()`, `f64_zeros_risk()` |

**Request:** Publish a migration guide: `DeviceCapabilities` (or successor) with documented equivalents for all four methods above, plus timeline for removal of `GpuDriverProfile`.

### 1b. Tensor

| Category | API |
|----------|-----|
| Construction | `Tensor::from_data()`, `Tensor::from_data_pod()`, `Tensor::new()` |
| GPU tensor ops | `gelu_wgsl`, `log_wgsl`, `exp_wgsl`, `softmax_wgsl`, matmul variants (as used by neuralSpring’s pipelines) |

### 1c. Ops (GPU kernels)

| Domain | Types / entry points |
|--------|----------------------|
| **Bio** | `HmmBatchForwardF64`, `HillGateGpu`, `SwarmNnGpu`, `PairwiseL2Gpu`, `MultiObjFitnessGpu`, `DiversityFusionGpu` |
| **Linalg** | `BatchedEighGpu` |
| **Stats** | `VarianceF64`, `CorrelationF64`, `FusedMapReduceF64`, chi-squared, KL divergence (as wired in neuralSpring validation) |
| **Dispatch** | `gelu_dispatch`, `matmul_dispatch`, `softmax_dispatch`, `variance_dispatch` |
| **FFT / attention** | `MultiHeadAttention` |

### 1d. `esn_v2` (breaking change)

| Change | Downstream impact |
|--------|-------------------|
| `MultiHeadEsn::wgpu_device()` removed | neuralSpring now holds `Arc<WgpuDevice>` separately wherever an ESN-backed path needs the device |

**Request:** Consider restoring a thin **`device()`** accessor on `MultiHeadEsn` (returning `Arc<WgpuDevice>` or equivalent) so consumers do not duplicate device ownership or risk drift between ESN state and dispatch device.

### 1e. Precision (v0.3.7)

| Item | Behavior in neuralSpring |
|------|---------------------------|
| `Precision::F16` added | Routed to the **f32 compilation path** until native f16 WGSL support is first-class upstream |
| Universal compile | `compile_shader_universal()` covers **F16, F32, Df64, F64** |

**Gap:** There is no dedicated `compile_shader_f16()`; consumers must route through the universal API or mirror f32 behavior explicitly.

### 1f. Shaders / provenance (RPC)

| API | Purpose |
|-----|---------|
| `cross_spring_shaders()`, `cross_spring_matrix()` | Feed **`science.cross_spring_provenance`** JSON-RPC for cross-spring shader and matrix lineage |

---

## Part 2: metalForge Bridge (`forge`)

| Concern | Detail |
|---------|--------|
| Shader strings | Re-exports WGSL **source strings** from `barracuda::ops::bio::*` (and related modules) into neuralSpring’s forge layer |
| Device bridge | `WgpuDevice` bridges neuralSpring’s `Gpu` abstraction and barraCuda’s device type |
| Capabilities | Uses `WORKGROUP_SIZE_1D` from `barracuda::device::capabilities` |

**Opportunity:** Reduce duplicated shader re-exports — treat **barraCuda as the single source of truth** for WGSL identity and versioning; neuralSpring (or biomeOS SDK) should consume stable exports rather than parallel catalogs.

---

## Part 3: WGSL Shaders (absorption candidates)

neuralSpring’s **metalForge / forge** layer catalogs and re-exports on the order of **~20** WGSL shaders that originate from or are validated against barraCuda. Representative themes (non-exhaustive):

- HMM forward, batch IPR, spatial payoff  
- Multi-objective fitness, pairwise L2  
- k-mer counting, taxonomy classification  
- Additional bio/stats kernels aligned with barraCuda ops above  

**Absorption angle:** toadStool can ingest these as **reference implementations** or fold them into a **canonical shader pack** versioned with barraCuda, reducing fork drift across springs.

---

## Part 4: Known Issues for the barraCuda Team

| # | Issue | Effect |
|---|--------|--------|
| 1 | `GpuDriverProfile` deprecation | Clean builds with **`-D warnings`** require `#[expect(deprecated)]` at call sites until migration is documented and implemented |
| 2 | `MultiHeadEsn` lost device accessor | Forces consumers to **thread a separate** `Arc<WgpuDevice>` (or duplicate device setup) |
| 3 | `Precision::F16` without a dedicated `compile_shader_f16()` | Consumers must **route through** `compile_shader_universal()` or the f32 path explicitly |
| 4 | No stable shader catalog (names + hashes) | neuralSpring tracks provenance largely via **comments** and bridge re-exports; cross-spring audits are harder than they need to be |

---

## Part 5: Recommendations for toadStool Absorption

| # | Pattern / artifact | Recommendation |
|---|---------------------|------------------|
| 1 | **`gpu_dispatch/mod.rs`** | Precision routing, pow workaround, and f64 strategy logic could lift into a shared **`barracuda::dispatch`** facade reused by springs |
| 2 | **`niche.rs` self-knowledge** | Capabilities, costs, and dependency metadata — reusable across **all springs** as a standard “niche” module |
| 3 | **5-tier socket discovery** in `discovery.rs` | Candidate for a **shared biomeOS SDK** helper (env → XDG → `/run/user` → temp → `socket-registry.json`) |
| 4 | **`Dispatcher` struct** | GPU primary with **CPU fallback** — a pattern toadStool could **standardize** for spring crates that must run on CPU-only CI |

---

## Quality Metrics (reference)

| Metric | Value (S170-era) |
|--------|------------------|
| Scientific computations validated | **1,195+** |
| Role vs. ecosystem | Largest downstream **GPU math** consumer of barraCuda among springs (by validation count) |

---

Part of [ecoPrimals](https://github.com/syntheticChemistry) · AGPL-3.0-or-later
