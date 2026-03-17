# WETSPRING V127 — IPC Resilience, Stable Numerics, Anderson Spectral Absorption Handoff

**Date:** 2026-03-17
**From:** wetSpring V127
**To:** barraCuda, toadStool, All Springs
**License:** AGPL-3.0-or-later
**Covers:** V126 → V127 (IPC resilience, 4-format capabilities, Anderson spectral, stable numerics, leverage guide)

---

## Executive Summary

- **IPC resilience module** — `RetryPolicy` + `CircuitBreaker` for structured fault tolerance (sweetGrass pattern)
- **4-format capability parsing** — Format C (`method_info`) and Format D (`semantic_mappings`) support
- **Centralized result extraction** — `extract_rpc_result()` complements `extract_rpc_error()`
- **Batch Anderson spectral** — `anderson_spectral` module wraps `barracuda::spectral` for ecology
- **Stable numerics** — `ln_1p`, `exp_m1`, `log_sum_exp`, Kahan summation for biology computation
- **GemmCached transpose** — `execute_ex(trans_a, trans_b)` for Tikhonov regularization
- **Leverage guide** — `wateringHole/WETSPRING_LEVERAGE_GUIDE.md` published
- **1,443+ tests**, zero warnings, zero unsafe, zero TODO/FIXME

---

## Part 1: What Changed (V126 → V127)

### IPC Resilience (`ipc::resilience`)

New module providing structured fault tolerance:

| Type | Description | Config |
|------|-------------|--------|
| `RetryPolicy` | Exponential backoff with max delay cap | `quick()`: 3 attempts, 100ms; `standard()`: 5 attempts, 500ms |
| `CircuitBreaker` | Failure threshold → open → cooldown → half-open probe | `default_config()`: 5 failures, 30s cooldown |

Key design: only `IpcError::is_retriable()` errors are retried. `Codec`, `RpcReject`, and `SocketPath` errors short-circuit immediately. Circuit breaker prevents retry storms against unhealthy primals.

**Absorption candidate for sweetGrass**: This pattern was learned from sweetGrass; the implementation is wetSpring-local but follows the same state machine. sweetGrass could absorb this as a reusable crate.

### 4-Format Capability Parsing

Extended `extract_capabilities()` (already had Format A flat + Format B domains) to support:

| Format | Key | What |
|--------|-----|------|
| C | `method_info` | Per-method metadata: description, cost estimate |
| D | `semantic_mappings` | Domain alias → method name mapping |

New types: `MethodInfo { method, description, cost }`. `CapabilityInfo` gains `method_info` and `semantic_mappings` fields.

**Absorption candidate for protocol**: This 4-format standard should be adopted by all primals. Consider moving `extract_capabilities()` to a shared crate.

### Batch Anderson Spectral (`bio::anderson_spectral`)

New module wrapping `barracuda::spectral` for ecology-specific patterns:

| Function | What |
|----------|------|
| `analyze_single(lattice_l, w, n_lanczos, seed)` | Single-point Anderson analysis |
| `sweep(lattice_l, w_values, n_lanczos, seed)` | Batch disorder sweep |
| `estimate_w_c(sweep_points)` | Linear interpolation of GOE↔Poisson crossing |
| `pielou_to_disorder(pielou_j, w_max)` | Ecology→physics mapping |

**For barraCuda**: This demonstrates the ecology→spectral bridge. The `sweep()` function is embarrassingly parallel — a future `anderson_sweep_gpu` kernel could vectorize the entire sweep on GPU. The Pielou→W mapping is domain-specific and stays in wetSpring.

### Stable Numerics (`bio::numerics`)

New module for numerically stable biological computation:

| Function | What | Why |
|----------|------|-----|
| `stable_ln1p(x)` | ln(1+x) via `f64::ln_1p()` | Avoids cancellation for perturbation analysis |
| `stable_expm1(x)` | exp(x)-1 via `f64::exp_m1()` | Avoids cancellation in ODE near-equilibrium |
| `log_sum_exp(a, b)` | ln(exp(a)+exp(b)) | Overflow-safe log-probability combination |
| `log_sum_exp_slice(values)` | Vectorized log-sum-exp | HMM forward, taxonomy scoring |
| `relative_diff(a, b)` | |a-b|/max(|a|,|b|,ε) | Zero-safe tolerance comparison |
| `kahan_sum(values)` | Compensated summation | O(1) error for large diversity arrays |

**For barraCuda**: `log_sum_exp` and `kahan_sum` are generic math — candidates for absorption into `barracuda::numerical`. `stable_ln1p`/`stable_expm1` are thin wrappers over std but document the biology context.

### GemmCached Transpose

New `execute_ex(a, b, m, k, n, batch_size, trans_a, trans_b)` for GPU GEMM with implicit transpose. CPU-side transpose before dispatch. Primary use: Tikhonov regularization `(AᵀA + λI)⁻¹Aᵀb` without materializing Aᵀ separately.

**For barraCuda**: The CPU-side transpose is a stopgap. barraCuda's `GemmF64::execute_gemm_ex` with native WGSL transpose support would eliminate the copy. Prioritize if Savitzky-Golay or least-squares become latency-sensitive.

---

## Part 2: barraCuda Primitive Consumption (V127 state)

### CPU Primitives (unchanged)

| Category | Primitives |
|----------|-----------|
| **stats** | shannon, simpson, chao1, bray_curtis, pielou_evenness, rarefaction_curve, alpha_diversity, bootstrap_ci, mean, percentile, variance, welford |
| **numerical** | CooperationOde, rk45_solve, trapz, gradient_1d |
| **linalg** | ridge_regression, jacobi_eigh |
| **special** | erf, ln_gamma, regularized_gamma_p |
| **spectral** | anderson_3d, lanczos, lanczos_eigenvalues, level_spacing_ratio, spectral_bandwidth, classify_spectral_phase, anderson_sweep_averaged, find_w_c, GOE_R, POISSON_R |

### GPU Primitives (150+, unchanged)

| Category | Primitives |
|----------|-----------|
| **ops** | FusedMapReduceF64, BrayCurtisF64, GemmF64, AniBatchF64, DnDsBatchF64 |
| **bio** | QualityFilterGpu, HmmBatchForwardF64, PairwiseHammingGpu, PairwiseJaccardGpu |
| **spatial** | BatchFitnessGpu, LocusVarianceGpu, DiversityFusionGpu, BatchedMultinomialGpu |
| **ODE** | BatchedOdeRK4<S>::generate_shader() (5 systems) |
| **linalg** | KrigingF64, BatchedEighGpu, PCoA ordination |

### New V127 Wiring

| Module | barraCuda Primitive | Usage |
|--------|-------------------|-------|
| `anderson_spectral` | `spectral::anderson_3d`, `lanczos`, `lanczos_eigenvalues`, `level_spacing_ratio`, `spectral_bandwidth`, `GOE_R`, `POISSON_R` | Batch Anderson ecology analysis |

---

## Part 3: Patterns Worth Absorbing

### For barraCuda

1. **`log_sum_exp` / `kahan_sum`** → `barracuda::numerical` — these are generic math, not biology-specific
2. **`anderson_sweep_gpu`** — vectorized Anderson sweep kernel (currently CPU-sequential via `sweep()`)
3. **Native GEMM transpose** — `GemmF64::execute_gemm_ex` with WGSL-level transpose to replace CPU-side copy in `execute_ex()`

### For sweetGrass

1. **`RetryPolicy` + `CircuitBreaker`** — wetSpring implemented the sweetGrass pattern locally. Consider extracting to a shared `resilience` crate that all primals can depend on.

### For All Springs

1. **4-format capability parsing** — Format C/D are now implemented in wetSpring. Recommend all primals adopt the same `extract_capabilities()` with 4-format support.
2. **`extract_rpc_result()`** — every primal does ad-hoc `val["result"]` extraction. Centralized version prevents bugs.
3. **Leverage guide pattern** — every primal should publish a `{PRIMAL}_LEVERAGE_GUIDE.md` describing standalone, trio, and composition patterns.

---

## Part 4: Quality Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,443+ (0 failures non-GPU) |
| Validation binaries | 306 |
| Benchmark binaries | 23 |
| Experiments | 376 |
| Validation checks | 5,707+ |
| Named tolerances | 214 |
| barraCuda CPU primitives | 18 categories |
| barraCuda GPU primitives | 150+ |
| Local WGSL shaders | 0 (fully lean) |
| Unsafe blocks | 0 (`#![forbid(unsafe_code)]`) |
| Clippy warnings | 0 (pedantic + nursery) |
| TODO/FIXME | 0 |
| Mocks in production | 0 |
| Capability domains | 16 (24 methods) |
| IPC methods | 23 |
