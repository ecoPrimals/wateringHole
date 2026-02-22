# wetSpring → ToadStool: Tier A Shader Handoff + CPU Math Feature Proposal

**Date:** 2026-02-21
**From:** wetSpring (life science + analytical chemistry Spring)
**To:** ToadStool / BarraCUDA core team
**License:** AGPL-3.0-or-later
**Context:** wetSpring v0.1.0 — 552 tests, 93.5% coverage, 1,501/1,501 checks,
63 experiments, 15 ToadStool primitives consumed, 9 local WGSL shaders validated

> **UPDATE Feb 22:** 8 of these 9 shaders have been absorbed by ToadStool
> (sessions 31d+31g) and wetSpring has been rewired. See companion document:
> `wetSpring/wateringHole/handoffs/WETSPRING_TOADSTOOL_REWIRE_FEB22_2026.md`
> for rewire outcomes, bugs found, and cross-spring evolution notes.
> Only the ODE sweep shader remains local (blocked on `enable f64;`).

---

## Executive Summary

wetSpring has **9 validated WGSL shaders** (all Tier A — handoff ready) covering
life science domains not yet in ToadStool: HMM, ODE sweeps, DADA2 denoising,
quality filtering, ANI, SNP calling, dN/dS, pangenome classification, and
Random Forest batch inference. All shaders pass GPU validation against CPU
baselines with documented tolerances.

Additionally, wetSpring identifies **4 local CPU math implementations** that
duplicate `barracuda::special` and `barracuda::numerical` functions. These
cannot currently switch because barracuda lacks a CPU-only feature gate.
We propose a `math` feature for barracuda.

---

## Part 1: Tier A WGSL Shaders — Ready for Absorption

### 1.1 HMM Batch Forward (`hmm_forward_f64.wgsl`)

| Field | Value |
|-------|-------|
| **Source** | `barracuda/src/shaders/hmm_forward_f64.wgsl` |
| **Rust wrapper** | `bio/hmm_gpu.rs` → `HmmGpu::forward_batch()` |
| **CPU reference** | `bio/hmm.rs` → `forward()` |
| **Validation** | Exp047: 13/13 GPU checks PASS |
| **Tolerance** | `GPU_VS_CPU_LOG_SPACE = 1e-6` (log-space transcendental) |
| **Dispatch** | `(ceil(T/64), N_seq, 1)` — T observations, N sequences |
| **Bindings** | 0: params (uniform), 1: observations (storage), 2: transitions (storage), 3: emissions (storage), 4: alpha (storage rw), 5: log_likelihood (storage rw) |
| **Polyfill** | `ShaderTemplate::for_driver_auto(src, true)` — forced `log_f64` on Ada |
| **Absorption target** | `ops::bio::HmmBatchForwardF64` |
| **Notes** | Log-space arithmetic prevents underflow. Forward-only (no backward/Viterbi GPU). |

### 1.2 ODE Parameter Sweep (`batched_qs_ode_rk4_f64.wgsl`)

| Field | Value |
|-------|-------|
| **Source** | `barracuda/src/shaders/batched_qs_ode_rk4_f64.wgsl` |
| **Rust wrapper** | `bio/ode_sweep_gpu.rs` → `OdeSweepGpu::sweep()` |
| **CPU reference** | `bio/ode.rs` → `rk4_step()` |
| **Validation** | Exp049: 7/7 GPU checks PASS |
| **Tolerance** | `GPU_VS_CPU_ENSEMBLE = 1e-6` |
| **Dispatch** | `(ceil(B/64), 1, 1)` — B parameter combos |
| **Bindings** | 0: params (uniform), 1: initial_conditions (storage), 2: parameter_sets (storage), 3: results (storage rw) |
| **Polyfill** | `for_driver_auto(src, true)` — forced `pow_f64` on Ada |
| **Absorption target** | Fix upstream `BatchedOdeRK4F64` (`enable f64;` removal + `pow` polyfill) |
| **Notes** | Local workaround for upstream naga issue. Identical math, just patched WGSL. |

### 1.3 DADA2 E-Step (`dada2_e_step.wgsl`)

| Field | Value |
|-------|-------|
| **Source** | `barracuda/src/shaders/dada2_e_step.wgsl` |
| **Rust wrapper** | `bio/dada2_gpu.rs` → `Dada2Gpu::e_step()` |
| **CPU reference** | `bio/dada2.rs` → `e_step()` |
| **Validation** | 88 checks via `validate_16s_pipeline_gpu` |
| **Tolerance** | `GPU_VS_CPU_ENSEMBLE = 1e-6` |
| **Dispatch** | `(ceil(N_reads/64), N_centers, 1)` |
| **Absorption target** | `ops::bio::BatchPairReduceF64` (generalized pairwise reduction) |

### 1.4 Quality Filter (`quality_filter.wgsl`)

| Field | Value |
|-------|-------|
| **Source** | `barracuda/src/shaders/quality_filter.wgsl` |
| **Rust wrapper** | `bio/quality_gpu.rs` → `QualityGpu::filter_batch()` |
| **CPU reference** | `bio/quality.rs` → `filter_reads()` |
| **Validation** | 88 checks via `validate_16s_pipeline_gpu` |
| **Tolerance** | Exact (integer comparison) |
| **Absorption target** | `ops::bio::ParallelFilterT` |

### 1.5 ANI Batch (`ani_batch_f64.wgsl`)

| Field | Value |
|-------|-------|
| **Source** | `barracuda/src/shaders/ani_batch_f64.wgsl` |
| **Rust wrapper** | `bio/ani_gpu.rs` → `AniGpu::pairwise_batch()` |
| **CPU reference** | `bio/ani.rs` → `pairwise_ani()` |
| **Validation** | Exp058: 7/7 GPU checks PASS |
| **Tolerance** | `GPU_VS_CPU_PAIRWISE = 1e-10` |
| **Dispatch** | `(ceil(N_pairs/64), 1, 1)` |
| **Absorption target** | `ops::bio::AniBatchF64` |

### 1.6 SNP Calling (`snp_calling_f64.wgsl`)

| Field | Value |
|-------|-------|
| **Source** | `barracuda/src/shaders/snp_calling_f64.wgsl` |
| **Rust wrapper** | `bio/snp_gpu.rs` → `SnpGpu::call_batch()` |
| **CPU reference** | `bio/snp.rs` → `call_snps()` |
| **Validation** | Exp058: 5/5 GPU checks PASS |
| **Tolerance** | `GPU_VS_CPU_PAIRWISE = 1e-10` |
| **Absorption target** | `ops::bio::SnpCallingF64` |

### 1.7 dN/dS Batch (`dnds_batch_f64.wgsl`)

| Field | Value |
|-------|-------|
| **Source** | `barracuda/src/shaders/dnds_batch_f64.wgsl` |
| **Rust wrapper** | `bio/dnds_gpu.rs` → `DnDsGpu::batch()` |
| **CPU reference** | `bio/dnds.rs` → `pairwise_dnds()` |
| **Validation** | Exp058: 9/9 GPU checks PASS |
| **Tolerance** | `GPU_VS_CPU_LOG_SPACE = 1e-6` (Nei-Gojobori uses `log()`) |
| **Polyfill** | `for_driver_auto(src, true)` — forced `log_f64` on Ada |
| **Absorption target** | `ops::bio::DnDsBatchF64` |

### 1.8 Pangenome Classify (`pangenome_classify.wgsl`)

| Field | Value |
|-------|-------|
| **Source** | `barracuda/src/shaders/pangenome_classify.wgsl` |
| **Rust wrapper** | `bio/pangenome_gpu.rs` → `PangenomeGpu::classify_batch()` |
| **CPU reference** | `bio/pangenome.rs` → `classify_genes()` |
| **Validation** | Exp058: 6/6 GPU checks PASS |
| **Tolerance** | Exact (integer classification) |
| **Absorption target** | `ops::bio::PangenomeClassifyGpu` |

### 1.9 RF Batch Inference (`rf_batch_inference.wgsl`)

| Field | Value |
|-------|-------|
| **Source** | `barracuda/src/shaders/rf_batch_inference.wgsl` |
| **Rust wrapper** | `bio/random_forest_gpu.rs` → `RandomForestGpu::predict_batch()` |
| **CPU reference** | `bio/random_forest.rs` → `predict()` |
| **Validation** | Exp063: 13/13 GPU checks PASS |
| **Tolerance** | Exact (integer vote) |
| **Dispatch** | `(ceil(N_samples/64), N_trees, 1)` — SoA layout |
| **Absorption target** | `ops::bio::RfBatchInferenceGpu` |
| **Notes** | Consider merging with existing `TreeInferenceGpu` → ensemble extension |

---

## Part 2: naga/NVVM Findings (Shared with hotSpring)

These affect all f64 WGSL shaders on Ada Lovelace GPUs:

| Finding | Impact | Workaround |
|---------|--------|------------|
| `enable f64;` not supported by naga | All shaders | Omit directive; use `ShaderTemplate` |
| NVVM `exp()`/`log()`/`pow()` crash on f64 | Shaders 1.1, 1.2, 1.7 | `for_driver_auto(src, true)` forced polyfill |
| `GpuDriverProfile::needs_f64_exp_log_workaround()` returns `false` for Ada | All RTX 40-series | Force `true` as second arg |
| naga f32 → f64 literal promotion fails | All f64 shaders | Use explicit `f64(0.0)` casts |

**Proposed fix:** `GpuDriverProfile` should detect Ada Lovelace (sm_89) and
return `true` for `needs_f64_exp_log_workaround()`.

---

## Part 3: CPU Math Feature Proposal

### Problem

wetSpring has 4 local math functions that barracuda already provides:

| Local Function | barracuda Equivalent |
|----------------|---------------------|
| `erf()` in `bio/pangenome.rs:222` | `barracuda::special::erf()` |
| `ln_gamma()` in `bio/dada2.rs:431` | `barracuda::special::ln_gamma()` |
| `regularized_gamma_lower()` in `bio/dada2.rs:399` | `barracuda::special::regularized_gamma_p()` |
| `integrate_peak()` in `bio/eic.rs:165` | `barracuda::numerical::trapz()` |

### Why We Can't Switch Today

barracuda's `Cargo.toml` requires `wgpu`, `akida-driver`, `toadstool-core` as
mandatory dependencies. Importing barracuda for CPU math forces the full
GPU/NPU stack into CPU-only builds.

### Proposal

Add feature-gated modules to barracuda:

```toml
[features]
default = ["gpu"]
math = []  # numerical, special, stats, optimize, sample — no wgpu
gpu = ["dep:wgpu", "dep:toadstool-core", "dep:akida-driver", "math"]
```

This lets Springs declare:
```toml
barracuda = { path = "...", features = ["math"] }
```

And get CPU math without GPU stack. hotSpring could also benefit (lighter
CI for CPU-only test runs).

---

## Part 4: Evolution Status

### Write → Absorb → Lean Ledger

| Phase | Count | Examples |
|-------|:-----:|---------|
| **Lean** (absorbed, consuming upstream) | 11 GPU modules | diversity, pcoa, spectral, SW, Gillespie, DT, Felsenstein |
| **Write** (local WGSL, validated, handoff ready) | 9 shaders | This document |
| **CPU math** (local impl, barracuda has equivalent) | 4 functions | Blocked on `math` feature |
| **CPU-only** (no GPU path planned) | 15 modules | chimera, derep, kmer, newick, GBM |
| **Blocked** (needs new upstream primitive) | 3 modules | kmer (lock-free hash), UniFrac (tree traversal), taxonomy (NPU) |

### Code Quality Gates (all pass)

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy -W pedantic -W nursery` | 0 warnings |
| `cargo doc --no-deps` | 0 warnings |
| `cargo-llvm-cov` | 93.5% line coverage |
| `unsafe` in production | 0 |
| `.unwrap()` in production | 0 |
| Tolerance provenance | 22 named constants, all justified |
| Data path discovery | `validation::data_dir()` (env override) |
| SPDX headers | All `.rs` and `.wgsl` files |

---

## Appendix: Validation Binary Matrix

| Binary | Checks | CPU/GPU | Experiment |
|--------|:------:|---------|------------|
| `validate_gpu_hmm_forward` | 13 | GPU | Exp047 |
| `validate_gpu_ode_sweep` | 12 | GPU | Exp049-050 |
| `validate_16s_pipeline_gpu` | 88 | GPU | Exp016 |
| `validate_gpu_track1c` | 27 | GPU | Exp058 |
| `validate_gpu_rf` | 13 | GPU | Exp063 |
| `validate_cross_substrate` | 20 | GPU | Exp060 |
| `validate_toadstool_bio` | 14 | GPU | Exp045 |
| **Total GPU** | **260** | | |
| **Total CPU** | **1,241** | | |
| **Grand Total** | **1,501** | | |
