# neuralSpring → ToadStool/BarraCUDA Handoff V61 — Universal Precision Sync

**Date**: February 27, 2026
**From**: neuralSpring (ML/neuroevolution + sovereign folding)
**To**: ToadStool/BarraCUDA team
**License**: AGPL-3.0-or-later
**Covers**: Session 91 — ToadStool S66–S68 evolution review, universal precision adoption, matmul rewiring
**Supersedes**: V60 (Dispatch Parity & Mixed-Hardware Handoff)

---

## Executive Summary

- **194 binaries**, **182/182 validate\_all** (all green), **669 lib tests**, **3219+ checks**
- **+2 upstream BarraCUDA rewires**: primal Evoformer `matmul_2d`/`matmul_3d` → `barracuda::dispatch::matmul_dispatch`
- **Universal precision adopted**: `compile_shader_universal(source, Precision)` exposed in `gpu.rs`; `Precision` enum re-exported
- **ToadStool S68 alignment**: ZERO f32-only shaders confirmed, 700 WGSL f64-canonical, dual-layer precision verified
- **NUCLEUS Tower**: 22/22 PASS with rewired matmul path
- **Total upstream rewires**: 44 functions + 6 shader sources

---

## Part 1: New Upstream BarraCUDA APIs Wired

### Primal Evoformer Matmul Rewiring (`src/bin/neuralspring_primal.rs`)

| Helper | Before | After |
|--------|--------|-------|
| `matmul_3d(a, w, batch, rows, in_dim, out_dim)` | CPU-only nested loop | `barracuda::dispatch::matmul_dispatch(a_slice, w, rows, in_dim, out_dim, None)` per batch, CPU fallback on error |
| `matmul_2d(a, w, rows, in_dim, out_dim)` | Delegated to `matmul_3d` | Direct `barracuda::dispatch::matmul_dispatch`, falls back to `matmul_3d` |

These helpers compose the Evoformer block in the primal binary (`science.evoformer_block` JSON-RPC handler).
Non-square matrix support (m, k, n) is fully exercised.

### Universal Precision API (`src/gpu.rs`)

| API | Purpose |
|-----|---------|
| `GpuF64::compile_shader_universal(source, precision)` | Compile one f64-canonical shader at any precision: F16, F32, F64, or Df64 |
| `pub use barracuda::shaders::precision::Precision` | Re-export precision enum for callers |

Existing `compile_shader_f64_hybrid` retained for backward compatibility (equivalent to `compile_shader_universal(source, Precision::Df64)`).

---

## Part 2: ToadStool S66–S68 Evolution Review

### Key Evolutions Audited

| Session | Achievement | neuralSpring Impact |
|---------|-------------|---------------------|
| S66 | Cross-spring absorption (stats::regression, hydrology, bootstrap::rawr_mean), `compile_shader_df64` pipeline, 6 DF64 math shaders | Already aligned in S78–79 |
| S67 | Universal precision: `Precision::Df64`, `compile_shader_universal`, 12 universal templates, `downcast_f64_to_f32` | Adopted: `compile_shader_universal` + `Precision` exposed |
| S68 | ZERO f32-only shaders (296 deleted, 291 converted), dual-layer precision (op_preamble + naga rewrite), 122 shader tests | Confirmed alignment. neuralSpring's sovereign folding shaders are f64-canonical |
| S68+ | GPU device-lost resilience, stale docs archived | No neuralSpring action needed |

### ToadStool Metrics (S68)

| Metric | Value |
|--------|-------|
| WGSL shaders | 700 (497 f32 via LazyLock downcast, 182 f64 native, 19 Df64, 2 Df64 infra) |
| BarraCUDA tests | 2,608 |
| Shader tests | 122 (unit + e2e + chaos + fault) |
| Clippy warnings | 0 |
| f32-only shaders | 0 |

---

## Part 3: Precision Architecture Alignment

neuralSpring's precision usage now aligns with ToadStool's dual-layer model:

| Layer | ToadStool | neuralSpring |
|-------|-----------|-------------|
| Buffer I/O | `array<f64>` in all shaders | `upload_f64` / `readback_f64` via `GpuF64` |
| Compute | `compile_shader_universal` routes to F16/F32/F64/Df64 | `compile_shader_f64_hybrid` (Df64) for folding; `compile_shader_universal` now available for precision-per-use |
| Hardware | `Fp64Strategy` (Native 1:2 vs Hybrid 1:64) | `GpuDriverProfile` integrated in Dispatcher |

### What's NOT Rewired (Intentionally Local)

| Module | Reason |
|--------|--------|
| `sovereign_folding::*` (gelu, layer\_norm, softmax\_rows, sdpa, triangle ops) | CPU reference implementations for validation — independent of barracuda for correctness verification |
| `structure_module::*` (ipa\_scores, backbone\_update, torsion\_angles) | CPU reference for AlphaFold2 structure module validation |
| `spectral_commutativity::mat_mul` | Independent CPU matmul reference for dispatch parity testing |
| `transformer::gelu`, `transformer::softmax` | CPU fallback for Dispatcher — defense-in-depth |

---

## Part 4: Quality Metrics

| Metric | V60 (S89) | V61 (S91) | Delta |
|--------|-----------|-----------|-------|
| Binaries | 177 | 194 | +17 |
| validate\_all | 177/177 | 182/182 | +5 |
| Lib tests | 668 | 669 | +1 |
| Total checks | 3111+ | 3219+ | +108 |
| Upstream rewires | 42 | 44 | +2 |
| Clippy warnings | 0 | 0 | 0 |
| barracuda import files | 90+ | 102 | +12 |
| barracuda reference files | 124 | 170+ | +46 |
| Cross-spring provenance checks | — | 57/57 | +57 |

---

## Part 5: What ToadStool Should Know

### Absorption Targets (neuralSpring → ToadStool)

| Priority | Item | Why |
|----------|------|-----|
| HIGH | `barracuda::nn::SimpleMLP` with JSON weight loading | Would replace ~400 LOC across 3 WDM surrogates |
| MEDIUM | Folding-specific dispatch ops (evoformer\_block, structure\_module) | Would allow ToadStool to compose folding pipelines natively |
| LOW | NUCLEUS Tower awareness in `barracuda::dispatch` | Domain heuristics for protein folding workload sizes |

### ToadStool Evolution Requests

1. **`matmul_dispatch` batched variant**: `matmul_batch_dispatch(a, w, batch, m, k, n, device)` would avoid per-batch dispatch overhead in `matmul_3d`
2. **Precision recommendation API**: Given a `WgpuDevice`, recommend optimal `Precision` for a workload class (compute-bound vs memory-bound)

---

---

## Part 6: Cross-Spring Evolution Provenance (`validate_modern_cross_spring` — 57/57)

New comprehensive validator exercises BarraCUDA functions from all five springs:

| Spring | Checks | What It Validates |
|--------|--------|-------------------|
| hotSpring | 5 | `Fp64Strategy`, DF64 eigh, `split_workgroups`, non-square `matmul_dispatch` |
| wetSpring | 10 | Shannon, Bray-Curtis, alpha diversity, Simpson, Pearson, NMF, ridge regression |
| airSpring | 11 | Linear/quadratic/exponential regression, RMSE, R², NSE, MAE, Hargreaves ET₀, Spearman |
| groundSpring | 8 | `bootstrap_ci`, `bootstrap_mean`, `rawr_mean`, `norm_cdf`, `norm_pdf`, `norm_ppf` |
| neuralSpring | 10 | Dispatcher softmax/GELU/variance/HMM, graph\_laplacian, effective\_rank |
| ToadStool S68 | 13 | Precision enum, dispatch config, LU/QR decomposition, gradient, trapz, Hessian, chi², ridge, backend info |

Each check traces its provenance chain: source spring → ToadStool absorption session → neuralSpring usage.
Benchmark table included: 6 ops with GPU/CPU timing and provenance tags.

---

*V61 handoff — neuralSpring S91, ToadStool S68. 44 upstream rewires, universal precision adopted, 182/182 validate\_all, 3219+ checks. Cross-spring provenance: 57/57 across all 5 springs.*
