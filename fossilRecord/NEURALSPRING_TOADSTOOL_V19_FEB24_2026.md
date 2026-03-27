# neuralSpring → ToadStool/BarraCUDA — V19 Summary (February 24, 2026)

**Session**: 51 (Code Quality Evolution)
**Full handoff**: `neuralSpring/wateringHole/handoffs/NEURALSPRING_V19_SESSION51_HANDOFF_FEB24_2026.md`
**ToadStool HEAD**: `9abd6857` (Sessions 50–53: 16 commits since `b41ee5f4`)

---

## What Changed

Code quality evolution + ToadStool sync (b41ee5f4 → 9abd6857).

- **`gpu_dispatch.rs` → `gpu_dispatch/` module**: CPU fallback implementations
  (variance, pearson, chi_squared, hmm_backward_step, hmm_viterbi_step,
  replicator_step) extracted to `cpu_fallback.rs`. Absorption candidates for
  `barracuda::stats` / `barracuda::bio`.
- **Clippy pedantic**: All 7 warning categories resolved (float_cmp, cast_lossless,
  identity_op, manual_midpoint, redundant_closure, doc_markdown, redundant_pub_crate).
- **Hardcoding**: 7 inline `1e-14` guards → `tolerances::ZERO_DETECTION`.
- **Coverage**: 92.9% line coverage, 459 lib tests, 0 warnings, 0 doc warnings.
- **Deps**: All pure Rust confirmed. No `-sys` crates except wgpu transitive.

## Absorption Candidates for BarraCUDA

### Priority 1 — General-Purpose Primitives

| Primitive | Source | Target |
|-----------|--------|--------|
| `graph_laplacian(adjacency)` | `agent_coordination.rs` | `ops::linalg` |
| `effective_rank(eigenvalues)` | `neural_pgm.rs` | `ops::linalg` |
| `empirical_spectral_density(eigenvalues, bins)` | `weight_spectral.rs` | `ops::stats` |
| `numerical_hessian(f, x, h)` | `loss_landscape.rs` | `ops::numerical` |
| `level_spacing_ratio(eigenvalues)` | `weight_spectral.rs` | `ops::stats` |

### Priority 2 — Testing Patterns

| Pattern | Why Absorb |
|---------|------------|
| `gpu_or_cpu(name, gpu_fn, cpu_fn)` | All Springs use this dispatch pattern |
| `exit_no_gpu()` | CI standardization across Springs |
| `baseline_path(rel)` | All Springs need CARGO_MANIFEST_DIR-relative data |
| `require!` macro | `.expect()` replacement — reusable across Springs |

### GPU Shader Candidates (baseCamp)

| Function | GPU Approach | Priority |
|----------|-------------|----------|
| `weight_to_hamiltonian` | Tensor matmul | High |
| `numerical_hessian` | GPU parallel FD | High |
| `belief_propagation_chain` | Batch GEMV | Medium |
| `interaction_graph` | Pairwise distance | Medium |

## Known Issues (Unchanged)

- **S-14**: Naive matmul hang (small square). Workaround: A×B^T pattern.
- **S-15**: Matmul hang ≤ 0.1 magnitude. Root-caused: driver bug. Workaround: data ≥ 0.5.

## ToadStool Sync Results

Pulled 16 commits (S50–53). Key items absorbed by ToadStool:
- **H-003**: domain_ops dispatch (9 wrappers mirroring our gpu_dispatch pattern)
- **M-001**: `argmax_dim`, `softmax_dim` — closes 2 API gaps
- **`level_spacing_ratio`** — neuralSpring rewired to `barracuda::spectral` upstream
- **`barracuda::tolerances`** — ToadStool created own tolerance module
- **`fst_variance_decomposition`** — Weir-Cockerham FST (complementary to our pairwise FST)
- **4,176 tests**, 0 clippy, all files under 1000 lines

## Session 52 Addendum — Cross-Spring Benchmarking

6 additional shaders confirmed absorbed: xoshiro, logsumexp, stencil, wright_fisher,
rk45, swarm_nn. Only `head_split` + `head_concat` remain local.

### Benchmark (RTX 4070, Vulkan, `--release`, 20 iterations)

| Op | Origin | µs |
|----|--------|----|
| BatchFitnessGpu 1024×64 | neuralSpring | 1,337 |
| PairwiseL2Gpu 128×16 | neuralSpring | 1,542 |
| SpatialPayoffGpu 32×32 | neuralSpring | 1,450 |
| PairwiseHammingGpu 64×100 | neuralSpring | 1,682 |
| BatchIprGpu 32×64 | neuralSpring | 2,027 |
| HmmBatchForwardF64 4s×50t×32b | wetSpring | 2,141 |
| BatchedEighGpu 12×12×40 | hotSpring | 6,629 |

**validate_all**: 137/138 PASS (1 pre-existing logsumexp driver issue).

## Cumulative Status

459 lib tests | 92.89% coverage | 36 modules | 138 binaries | bC 24/25 | gT 23/25 |
mF 15/15 | gP 15/15 | xD 15/15 | 0 clippy | 0 doc warnings | 0 unsafe | AGPL-3.0 |
2 local shaders remaining (head_split + head_concat)

---

## Session 52b — S-17: HillGate f64 `pow()` Root Cause & Fix

**Problem**: `hill_gate_f64.wgsl` native `pow(f64, f64)` crashes on RTX 4070
(NVVM) and TITAN V (NAK). `apply_transcendental_workaround` patches
`exp`/`log` but misses `pow`.

**Fix**: `pow(` → `pow_f64(` in shader source. Auto-injected polyfill achieves
machine-epsilon accuracy (max diff 2.22e-16). Proven by `validate_hillgate_f64_fix`
(18/18 PASS on both GPUs).

**Action**: Add `.replace("pow(", "pow_f64(")` to `patch_exp_log_in_code`.
Also fix `hill_f64.wgsl` (element-wise Hill) — same pattern.

**Also fixed**: `validate_gpu_signal` had f32/f64 buffer mismatch + was
unconditionally skipping. Now 9/9 PASS on both GPUs using polyfill path.

**Cumulative**: 459 lib tests | 92.89% coverage | 139 binaries | gpu_signal
now PASS (was SKIP) | 137/138 validate_all PASS

---

*neuralSpring V19 → ToadStool. Sessions 51–52b: S-17 HillGate fix + code quality + sync + benchmarks. Full details in spring-local handoff.*
