# wetSpring → ToadStool/BarraCuda: Paper-Math Validation Chain (V92D+)

**Date:** March 2, 2026
**From:** wetSpring V92D+
**To:** ToadStool/BarraCuda team
**ToadStool pin:** S79 (`f97fc2ae`)

---

## Summary

wetSpring has completed the full paper-math validation chain proving:

1. **52 papers' equations are correct** in pure Rust via BarraCuda CPU
2. **CPU is faster than Python** (0.8 ms vs ~200 ms for equivalent scipy)
3. **Math is GPU-portable** via ToadStool dispatch (5 tracks validated)
4. **Streaming eliminates round-trips** (unidirectional pipeline, ~33% speedup)
5. **Cross-system works** (metalForge routes across GPU/CPU with NUCLEUS atomics)

```
Open Data → Paper v4 (45/45) → CPU v22 (40/40) → GPU v9 (35/35) → Streaming v9 (16/16) → metalForge v14 (28/28)
```

---

## What ToadStool Should Absorb

### Already Absorbed (93 primitives, all working)
- `barracuda::linalg::nmf` — NMF, cosine_similarity
- `barracuda::stats` — bootstrap_ci, jackknife, pearson, fit_linear, norm_cdf, chao1, shannon, simpson
- `barracuda::special` — erf, erfc
- `barracuda::linalg::ridge_regression`
- `barracuda::ops` — transe_score_f64, sparse_gemm_f64, peak_detect_f64
- `barracuda::spectral` — anderson_3d, lanczos, level_spacing_ratio

### GPU Promotion Opportunities (from CPU v22 domains)
| Domain | CPU Primitive | GPU Promotion | Effort |
|--------|-------------|---------------|--------|
| **Hill equation** | `d^n / (IC50^n + d^n)` | Batch vectorize on GPU | Trivial (map) |
| **PK decay** | `C0 * exp(-kt)` | Batch vectorize on GPU | Trivial (map) |
| **Anderson W→P(QS)** | `norm_cdf((Wc-W)/σ)` | Batch via GPU erf | Low (erf already in WGSL) |
| **Cooperation ODE** | `rk4_integrate` | GPU parameter sweep | Medium (sweep, not single) |
| **Bootstrap CI** | Resample + statistic | GPU parallel resampling | Medium (RNG on GPU) |
| **Jackknife** | Leave-one-out | GPU parallel leave-out | Medium |

### Streaming Pipeline Pattern
Exp294 validated this 5-stage pipeline that ToadStool should optimize as a
first-class streaming template:

```
Stage 1: Diversity batch (FusedMapReduceF64)      → GPU buffer
Stage 2: Bray-Curtis pairwise (BrayCurtisF64)     → GPU buffer
Stage 3: NMF factorization                        → GPU buffer
Stage 4: Anderson W-mapping (batch norm_cdf)       → GPU buffer → CPU readback
Stage 5: Statistics aggregation (CPU)
```

Key finding: 3 GPU-chained stages with 0 CPU round-trips. Streaming saves ~33%.

### metalForge Evolution
- 47 workloads registered, 45 absorbed, 2 CPU-only
- Sovereign mode proven: 45/47 route locally without NestGate/Songbird
- PCIe transfer benchmarks: RTX 4070 = 322µs/10MB, TITAN V = 640µs/10MB
- Cross-substrate transitions (GPU→CPU→GPU→CPU) stable in 5-stage pipeline

---

## Learnings Relevant to ToadStool Evolution

### 1. NMF Convergence
- KL-divergence objective converges faster than Frobenius for sparse bio matrices
- 4×4 drug-disease: 25 iterations, 5×5: 48 iterations — both < 0.02 ms on CPU
- `NmfResult.errors` vector is sufficient for convergence tracking (no need for `iterations` field)

### 2. Diversity Computation
- `wetspring_barracuda::bio::diversity` and `barracuda::stats` produce identical results
  (delegation works correctly — bio delegates to barracuda primitives)
- Uniform(4) analytical: Shannon=ln(4)=1.386294, Simpson=0.75, Chao1=4, Pielou=1.0 — all exact

### 3. Anderson Spectral
- W↔P(QS) anticorrelation confirmed: r = -0.924 across 5 ecological tracks
- Mapping: Shannon → W = 25×(1 - H/ln(S)) → P(QS) = Φ((Wc-W)/σ)
- Consistent across microbial, soil, skin, drug, and deep-sea communities

### 4. Pharmacology on GPU
- Hill equation is embarrassingly parallel — perfect GPU candidate
- PK exponential decay is embarrassingly parallel
- JAK selectivity ratios are pre-computed (no GPU needed, just lookup)
- Three-compartment Anderson model needs per-compartment norm_cdf — batch GPU candidate

### 5. Determinism
- All CPU computations are bitwise deterministic across reruns
- Shannon, Simpson, Bray-Curtis all pass bitwise identity checks
- Anderson spectral (same seed) produces bitwise identical eigenvalues

---

## Quality State

| Gate | Status |
|------|--------|
| `cargo fmt` | CLEAN |
| `cargo clippy --all-features -W pedantic` | 0 warnings |
| `cargo test --workspace` | 1,309 pass, 0 fail |
| TODO/FIXME/HACK in .rs | 0 |
| unsafe code | 0 |
| local WGSL | 0 |

---

## Numbers

| Metric | Before V92D+ | After V92D+ |
|--------|:------------:|:-----------:|
| Experiments | 272 | 277 |
| Validation checks | 7,220+ | 7,384+ |
| Binaries | 255 | 260 |
| Papers validated | 52+6 | 52+6 (now with full chain) |

All 52 papers now have: paper-math control → CPU parity → GPU portability → streaming → metalForge.
