# neuralSpring → ToadStool/BarraCUDA Handoff V67 — Deep Debt + Cross-Spring Evolution

**Date**: March 1, 2026
**From**: neuralSpring (Session 100)
**To**: ToadStool/BarraCUDA team
**License**: AGPL-3.0-or-later
**Supersedes**: V63 (WDM AlphaFold3 GPU Tensor)

---

## Executive Summary

neuralSpring Session 100 completes deep debt execution and cross-spring evolution rewiring:

- **746 lib tests** (up from 685), **218 binaries**, **3550+ total checks**
- **Zero clippy pedantic+nursery warnings** across all targets
- **4 unused deps removed** (biomeos-primal-sdk, uuid, chrono, log)
- **Hardcoded primal names → capability-based discovery** at runtime
- **Cross-spring rewire**: hotSpring `proxy.rs` diagnostics absorbed, GPU ESN via `barracuda::tensor::Tensor` ops
- **V67 ToadStool handoff** written to neuralSpring `wateringHole/handoffs/`

## BarraCUDA Integration (130+ imports, 20+ submodules, 44 rewires)

### What neuralSpring Exercises

| BarraCUDA Module | Usage | Import Sites |
|------------------|-------|-------------|
| `device::WgpuDevice` | GPU device for all ops | 40+ |
| `tensor::Tensor` | Universal CPU/GPU tensor | 50+ |
| `ops::bio::*` | 15+ bio GPU ops | 30+ |
| `ops::linalg::BatchedEighGpu` | Eigendecomposition | 5+ |
| `ops::mha::MultiHeadAttention` | Attention | 2 |
| `ops::fft::*` | FFT validation | 4 |
| `ops::fused_map_reduce_f64` | GPU reductions | 5 |
| `stats::*` | 30+ statistical functions | 20+ |
| `spectral::BatchIprGpu` | Anderson localization | 8+ |
| `dispatch::*` | Cross-dispatch routing | 6+ |
| `shaders::precision` | DF64 precision | 3+ |
| `nn::simple_mlp` | MLP inference | 2 |

### Cross-Spring Provenance

| Origin Spring | Contribution | Absorbed Into |
|---------------|-------------|--------------|
| **hotSpring** `proxy.rs` | `spectral_bandwidth`, `spectral_condition_number`, `classify_phase` | neuralSpring `weight_spectral.rs` — candidates for `barracuda::spectral` promotion |
| **hotSpring** df64 | f64 precision on FP32 GPUs | barracuda `compile_shader_df64` (already upstream) |
| **hotSpring** ESN | GPU echo state network | neuralSpring `wdm_esn::classify_via_barracuda` via Tensor ops |
| **wetSpring** bio stats | shannon, simpson, chao1, bray_curtis | barracuda::stats (already upstream) |
| **wetSpring** DiversityFusionGpu | Fused Shannon+Simpson+Pielou | barracuda::ops::bio (already upstream) |
| **neuralSpring** batch fitness | GPU batch fitness eval | barracuda::ops::bio (absorbed) |
| **neuralSpring** pairwise ops | L2, Jaccard, Hamming | barracuda::ops::bio (absorbed) |

## Absorption Opportunities for ToadStool

### Priority 1: `esn_v2` Shape Bug

`barracuda::esn_v2::ESN::train()` stores readout as `[reservoir_size, output_size]` but `set_readout_weights()` expects `[output_size, reservoir_size]`. neuralSpring works around this with direct Tensor ops in `classify_via_barracuda`. Fix would unblock all springs using the higher-level ESN API.

### Priority 2: Spectral Diagnostic Promotions

Three zero-dependency scalar functions from hotSpring `proxy.rs` that neuralSpring now uses:

```rust
pub fn spectral_bandwidth(eigenvalues: &[f64]) -> f64      // λ_max − λ_min
pub fn spectral_condition_number(eigenvalues: &[f64]) -> f64 // |λ_max| / |λ_min|
pub fn classify_phase(lsr: f64) -> SpectralPhase            // Extended/Critical/Localized
```

These belong in `barracuda::spectral` alongside `level_spacing_ratio` and `empirical_spectral_density`.

### Priority 3: Test Patterns

neuralSpring S100 added 19 tests that could inform BarraCUDA's own test suite:
- Anderson localization: disorder sweep monotonicity, eigenvalue finiteness, two-particle symmetry
- GPU dispatch: weight spectral, numerical Hessian, belief propagation normalization, graph symmetry

## Quality State

| Metric | Value |
|--------|-------|
| Lib tests | 746 |
| Validation binaries | 218 |
| Clippy warnings | 0 (pedantic + nursery) |
| Unsafe code | 0 (forbidden) |
| Mocks in production | 0 |
| Files > 1000 LOC | 0 |
| Unused deps | 0 |
| Total checks | 3550+ |

---

*See `neuralSpring/wateringHole/handoffs/NEURALSPRING_TOADSTOOL_V67_S100_DEEP_DEBT_CROSS_SPRING_HANDOFF_MAR01_2026.md` for the detailed version.*
