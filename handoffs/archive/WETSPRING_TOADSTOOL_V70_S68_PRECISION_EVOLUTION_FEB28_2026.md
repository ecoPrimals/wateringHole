# wetSpring → toadStool / barracuda — V71 S68+ Complete Rewire + Cross-Spring Evolution

**Date:** February 28, 2026
**From:** wetSpring
**To:** toadStool / barracuda core team
**Covers:** V71 complete rewire, DF64 host protocol, precision-flexible GEMM, cross-spring evolution benchmark
**ToadStool Pin:** S68+ (`e96576ee`)
**License:** AGPL-3.0-only

---

## Executive Summary

- **79 ToadStool primitives** consumed (barracuda always-on, zero fallback code)
- **0 local WGSL** shaders (fully lean — all 8 original bio shaders absorbed)
- **0 local derivative/regression** math (delegated to upstream)
- **700 WGSL shaders** upstream, all f64-canonical (ZERO f32-only remain)
- **Universal precision** verified: `compile_shader_universal` routes F16/F32/F64/Df64
- **Device-lost resilience** consumed: `GpuF64::is_lost()` via `WgpuDevice::is_lost()`
- **6 GPU bio ODE modules** + `GemmCached` annotated for Df64 promotion path
- **953 lib tests** PASS, **113 forge tests** PASS, clippy pedantic CLEAN
- **1 passthrough** remaining (`reconciliation_gpu` — needs `BatchReconcileGpu`)

---

## S66-S68+ Evolution Review

### What Changed in ToadStool (24 commits, S66-S68+)

| Session | Commits | Key Evolution |
|---------|:-------:|---------------|
| S66 | 3 | `compile_shader_df64`, universal DF64 math, f64 gap-fills, cross-spring absorption |
| S67 | 2 | Universal precision architecture: `Precision` enum (F16/F32/F64/Df64), "math is universal, precision is silicon" |
| S68 Waves 1-11 | 11 | ALL 497 f32-only shaders evolved to f64 canonical — ZERO remain |
| S68 | 5 | Dual-layer precision (op_preamble + naga IR rewrite), DF64 pipeline, audit + 122 tests, root doc cleanup |
| S68+ | 3 | CPU feature-gate regression fix, root docs archived, GPU device-lost resilience |

**Total**: 1,041 files changed, 16,375 insertions, 11,385 deletions (vs S65 baseline).

### API Changes

**No breaking changes.** All evolution is additive:

| New API | Purpose | wetSpring Status |
|---------|---------|------------------|
| `compile_shader_universal(source, precision)` | Single entry for all precisions | Already consumed (all GPU bio modules) |
| `compile_op_shader(source, precision)` | Abstract `op_add`/`op_mul` preamble | Available, not yet needed |
| `compile_template(template, precision)` | `{{SCALAR}}`-templated shaders | Available, not yet needed |
| `compile_shader_df64(source)` | DF64 pipeline (core + transcendentals) | Available via `compile_shader_universal(Df64)` |
| `Precision::Df64` | Double-float f32-pair (~48-bit mantissa) | Available, host buffer protocol needed for promotion |
| `Precision::F16` | Half-precision (inference) | Available, not needed for science workloads |
| `WgpuDevice::is_lost()` | GPU device-lost detection | Consumed via `GpuF64::is_lost()` |
| `downcast_f64_to_df64()` | f64→DF64 shader transformation | Transparent (used internally by `compile_shader_universal`) |
| `op_preamble()` | Precision-specific `op_add`/`op_mul` | Available via `compile_op_shader` |

### Existing APIs (Unchanged)

| API | Status |
|-----|--------|
| `storage_bgl_entry` / `uniform_bgl_entry` | Still recommended (no replacement) |
| `WgpuDevice::from_existing()` | Unchanged |
| `GpuDriverProfile::from_device()` | Unchanged |
| `Fp64Strategy::Native` / `Hybrid` | Unchanged |
| `BatchedOdeRK4::generate_shader()` | Unchanged |
| `BandwidthTier::detect_from_adapter_name()` | Unchanged |

---

## Rewire Applied

### GPU Bio Module Precision Annotations

All 6 GPU bio ODE modules (`phage_defense_gpu`, `multi_signal_gpu`, `cooperation_gpu`,
`bistable_gpu`, `capacitor_gpu`) and `gemm_cached` now document the S68+ precision
path in their module-level doc comments:

- Current: `Precision::F64` (f64 canonical, correct for scientific compute)
- Available: `Precision::Df64` for ~10× throughput on consumer FP32 cores
- Requirement for DF64 promotion: host buffer protocol adaptation (`vec2<f32>` storage)

### `gpu.rs` Module Doc Update

Updated to reflect:
- 700 WGSL shaders (was "30 primitives")
- Full precision matrix (F16/F32/F64/Df64)
- `optimal_precision()` routing documentation
- All consumed ToadStool GPU primitives listed

### Status Doc Cleanup

`CONTROL_EXPERIMENT_STATUS.md` updated:
- ToadStool alignment: S68+ with 700 WGSL, ZERO f32-only, universal precision
- Test counts: 953 barracuda lib tests (was 946)
- Precision metrics section added (S66-S68+ milestone table)
- Cross-spring evolution updated to S68+ with groundSpring contributions
- Handoff table updated with V70

---

## V71 Complete Rewire (Feb 28, 2026)

### New Modules

| Module | Purpose |
|--------|---------|
| `df64_host` | DF64 (double-float f32-pair) host-side pack/unpack for `Precision::Df64` wire format. 9 tests. Round-trip precision: 24,607,325× over f32 for π. |
| `GemmCached::with_precision()` | Precision-flexible GEMM constructor. `new()` defaults to F64 (backward compat). `with_precision(Precision::Df64)` compiles DF64 shader. |

### Cross-Spring Evolution Benchmark (Exp223)

46/46 checks PASS — exercises all 5 springs + ToadStool hub:

| Section | Spring(s) | Primitives Validated |
|---------|-----------|---------------------|
| §0 | ToadStool | Fp64Strategy, optimal_precision (→Df64 on RTX 4070), BandwidthTier (PCIe4x16, 31.5 GB/s), is_lost() |
| §1 | wetSpring | DF64 host protocol: 8 test values, slice round-trip, 24M× precision gain over f32 |
| §2 | hotSpring | erf, ln_gamma, norm_cdf, Anderson 3D spectral (1.53 ms) |
| §3 | wetSpring | CPU diversity (Shannon/Simpson/Pielou), GPU DiversityFusion (5×10k) |
| §4 | neuralSpring | graph_laplacian (row sums=0), numerical_hessian (Rosenbrock H[0,0]≈802), effective_rank=3.37 |
| §5 | airSpring + groundSpring | Pearson, MAE, RMSE, R², trapz(x²)≈1/3 |
| §6 | wetSpring | GEMM 256×128×256: cold 2.17ms, cached 1.77ms (1.2× amortization), new() == with_precision(F64) |
| §7 | wetSpring | NMF 20×10 (KL, k=3), ridge regression 20×5→2 |
| §8 | ALL | Cross-spring provenance table: who contributed → who benefits |

## Revalidation Results

| Suite | Count | Result |
|-------|:-----:|--------|
| `wetspring-barracuda` lib (--features gpu) | 962 | ALL PASS |
| `wetspring-forge` lib | 113 | ALL PASS |
| Exp223 cross-spring evolution | 46 | ALL PASS |
| clippy pedantic (barracuda) | — | CLEAN |
| clippy pedantic (forge) | — | CLEAN |

962 barracuda lib tests (was 953 — +9 from `df64_host` module). All 79 consumed
primitives compile and behave identically. No regressions.

---

## Precision Path Forward

### Current State

All wetSpring GPU modules use `compile_shader_universal` at `Precision::F64`:

```text
wetSpring ODE GPU module
  → BatchedOdeRK4::generate_shader()  [f64 WGSL]
  → device.compile_shader_universal(wgsl, Precision::F64)
  → ToadStool: driver workarounds + ILP optimizer + Sovereign compiler
  → wgpu::ShaderModule  [native f64]
```

### DF64 Promotion Path (Future)

To leverage DF64 (~10× throughput on consumer GPUs):

```text
wetSpring ODE GPU module
  → BatchedOdeRK4::generate_shader()  [f64 WGSL]
  → device.compile_shader_universal(wgsl, Precision::Df64)
  → ToadStool: downcast_f64_to_df64() → df64_core.wgsl prepend → ILP → Sovereign
  → wgpu::ShaderModule  [DF64 via vec2<f32>]
```

**Host-side changes required:**
1. Buffer creation: `vec2<f32>` storage instead of `f64`
2. Data upload: pack f64 → (hi, lo) f32 pairs
3. Data readback: unpack f32 pairs → f64
4. Buffer size: 2× f32 elements per f64 value (same byte count)

This is a protocol change, not an API change. `compile_shader_universal` handles
the shader transformation transparently. The host protocol adaptation should be
standardized once across all GPU modules.

---

## Absorption Candidates (Carried from V61)

### 1. `bio::esn` → `barracuda::ml::esn`

Echo State Network for NPU deployment validation. ToadStool has `esn_v2::ESN`
(GPU/NPU, hardware-agnostic); wetSpring local `bio::esn` (776 lines) is training-focused.
Candidate for convergence into shared `barracuda::ml::esn` with train/infer split.

### 2. NPU Inference Bridge → `barracuda::npu`

Standard int8 inference via DMA to AKD1000. 60 checks on real hardware.

### 3. `BatchReconcileGpu`

DTL reconciliation GPU primitive (one workgroup per gene family). `reconciliation_gpu`
remains a passthrough (CPU dispatch) until this lands upstream.

---

## New ToadStool Bio Ops Available (Not Yet Consumed)

| Op | Type | Potential wetSpring Use |
|----|------|------------------------|
| `BatchedMultinomialGpu` | Rarefaction | GPU-accelerated rarefaction curves |
| `WrightFisherGpu` | Population genetics | Wright-Fisher simulations |
| `StencilCooperationGpu` | Spatial QS | Stencil-based cooperation models |
| `HillGateGpu` | Synthetic biology | Two-input Hill AND gate |
| `fst_variance_decomposition` | FST | FST decomposition (CPU) |
| `MultiObjFitnessGpu` | Evolutionary algorithms | Multi-objective fitness |
| `NcbiCache` | NCBI caching | XDG-based cache (wetSpring uses NestGate instead) |

These are available but not yet needed by current experiments.

---

## Cross-Spring Provenance (Verified in Exp223)

```text
hotSpring  → erf, ln_gamma, Fp64Strategy, DF64 core, Anderson spectral
             → ALL springs get precision math; neuralSpring eigensolvers use erf
wetSpring  → bio ODE ×5, diversity, BrayCurtis, GEMM, NMF, ridge
             → neuralSpring uses FusedMapReduce; airSpring uses ridge for kriging
neuralSpring → graph_laplacian, numerical_hessian, effective_rank, pairwise ops
               → wetSpring community ecology; airSpring sensor correlation
airSpring  → Pearson, MAE, RMSE, R², Richards PDE, kriging
             → wetSpring paper validation; neuralSpring model evaluation
groundSpring → bootstrap rawr_mean, batched multinomial
               → wetSpring confidence intervals
ToadStool  → 700 WGSL (0 f32-only), universal precision, Sovereign compiler
             → ALL springs: device resilience, ILP optimizer, dispatch semaphore
```

## Supersedes

- `WETSPRING_TOADSTOOL_V61_BARRACUDA_EVOLUTION_FEB27_2026.md` (ToadStool pin updated)
- V33/V32/V31/V30 (historical, retained for provenance)
