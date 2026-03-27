# ToadStool → Ecosystem Handoff: Sessions 64-65 (Cross-Spring Absorption + Smart Refactoring)

**Date**: February 25, 2026
**From**: ToadStool / BarraCUDA (ecoPrimals/phase1/toadStool)
**To**: All Springs + ecosystem primals
**ToadStool baseline**: Sessions 64-65 (Feb 25, 2026)

---

## Summary

Session 64 absorbed cross-spring handoffs (8 lattice shaders, 2 stats modules, chrono
elimination). Session 65 performed smart refactoring of the 3 largest production files,
eliminating structural duplication without losing any test coverage.

### Key Numbers

| Metric | Before (S63) | After (S65) | Delta |
|--------|-------------|-------------|-------|
| WGSL shaders | 687 | 694 | +7 (lattice QCD) |
| Barracuda tests | 2,440 | 2,490 | +50 |
| `#[allow(dead_code)]` | 17 | 13 | -4 resolved |
| `compute_graph.rs` | 819 lines | 522 lines | -36% |
| `esn_v2/model.rs` | 861 lines | 482 lines | -44% |
| `tensor/mod.rs` | 808 lines | 529 lines | -35% |
| `special/gamma.rs` | 685 lines | 463 lines | -32% |
| `numerical/rk45.rs` | 579 lines | 352 lines | -39% |
| Production panics | 1 (`coulomb_f64` expect) | 0 | fixed |
| Hardcoded thresholds | 7 in kernel_router | 0 (named constants) | fixed |
| External deps eliminated | instant | instant + chrono | +chrono |
| Clippy warnings | 0 | 0 | — |

---

## Session 64: Cross-Spring Absorption

### Lattice Shader Absorption (hotSpring V0613/V0614)
- **8 new WGSL shaders** absorbed into `shaders/lattice/`: `su3_math_f64`, `prng_pcg_f64`, `su3_f64`, `su3_gauge_force_df64`, `su3_kinetic_energy_df64`, `axpy_f64`, `complex_dot_re_f64`, `xpay_f64`
- Wired via `ops/lattice/absorbed_shaders.rs` with `include_str!` and doc-comment provenance

### Statistics Module (airSpring V006 + groundSpring V7)
- **`barracuda::stats::metrics`**: RMSE, MBE, Nash-Sutcliffe, R², Index of Agreement, hit_rate, mean, percentile, dot, l2_norm (18 unit tests)
- Consolidated from airSpring `testutil/stats.rs` and groundSpring `stats/metrics.rs`

### Diversity Module (wetSpring V41)
- **`barracuda::stats::diversity`**: Shannon, Simpson, Chao1, Pielou evenness, Bray-Curtis (pairwise + condensed + full matrix), rarefaction curves, AlphaDiversity (16 unit tests)

### Deep Debt Resolved
- `chrono` eliminated → `std::time::SystemTime`
- 3 `#[allow(dead_code)]` resolved (BroydenMixer, KrigingF64, KernelRouter accessors)
- neuralSpring blocked items confirmed live: `WGSL_MEAN_REDUCE`, `argmax_dim()`, `softmax_dim()`

---

## Session 65: Smart Refactoring

### compute_graph.rs (819→522, -36%)
**Pattern**: 4 near-identical `compile_*_shader()` methods and 3 near-identical `encode_*_op()` methods — each creating BGL entries, bind groups, pipeline layout, pipeline, and dispatch pass from scratch.

**Fix**: Extracted `compile_shader(source, label)` and `compile_elementwise(body, label)` (2 methods replace 4). Extracted `dispatch_pass(encoder, shader, bgl_entries, buffers, size)` (1 generic method replaces 3). Reused existing `storage_bgl_entry()`/`uniform_bgl_entry()` from `device::compute_pipeline` instead of hand-rolling 15+ `BindGroupLayoutEntry` declarations.

Also resolved `device_name` `#[allow(dead_code)]` → `pub fn device_name()`.

### esn_v2/model.rs (861→482, -44%)
**Pattern**: 478 lines of production code + 383 lines of tests in a single file.

**Fix**: Tests extracted to `esn_v2/model_tests.rs` via `#[cfg(test)] #[path = "model_tests.rs"] mod tests;`. All 20 async tests pass. Production code untouched.

### tensor/mod.rs (808→529, -35%)
**Pattern**: 526 lines of production code + 282 lines of tests, including a verbatim duplicate test (`test_tensor_laplacian_context_debug`, self-annotated "EXACT COPY of test_tensor_3d_roundtrip_minimal").

**Fix**: Tests extracted to `tensor/tensor_tests.rs`. Duplicate merged into parameterized `test_tensor_3d_roundtrip` covering shapes 2×2×2, 3×3×3, 4×4×4. All tests pass.

---

## For Springs: What Changed

### New Public APIs
- `barracuda::stats::metrics::{rmse, mbe, nash_sutcliffe, r_squared, index_of_agreement, hit_rate, mean, percentile, dot, l2_norm}`
- `barracuda::stats::diversity::{shannon, simpson, chao1, pielou_evenness, alpha_diversity, bray_curtis, bray_curtis_condensed, bray_curtis_matrix, rarefaction_curve, observed_features, AlphaDiversity}`
- `barracuda::ops::lattice::absorbed_shaders::{WGSL_SU3_MATH_F64, WGSL_SU3_LATTICE_F64, WGSL_PRNG_PCG_F64, WGSL_SU3_GAUGE_FORCE_DF64, WGSL_SU3_KINETIC_ENERGY_DF64, WGSL_AXPY_F64, WGSL_COMPLEX_DOT_RE_F64, WGSL_XPAY_F64}`
- `ComputeGraph::device_name()`, `KrigingF64::device()`, `BroydenMixer::device()`/`vec_dim()`, `KernelRouter::has_tpu()`

### Breaking Changes
- None. All refactoring is internal (test file locations, private method signatures).

### For neuralSpring
- `WGSL_MEAN_REDUCE`, `argmax_dim()`, `softmax_dim()` confirmed live in barracuda public API — no upstream blockers.

### Remaining Phase 5+ Reserved Dead Code (13 items)
- `griffin_lim.rs`: n_fft, hop_length (full STFT/ISTFT)
- `fhe_key_switch.rs`: pipeline_accumulate (accumulation pass)
- `device/tpu.rs`: TpuBackend variants (feature-gated)
- `vision.rs`: device (future GPU transforms)
- `timeseries.rs`: device (future NN training)
- `staging/ring_buffer.rs`: staging_buffer (Phase 5 async readback)
- `staging/unidirectional.rs`: device, output_throttler (Phase 5 bandwidth sim)
- `device/akida.rs`: PcieDevice (defensive)
