# ToadStool v69 — Cross-Spring Absorption Handoff

**Date**: February 27, 2026
**Session**: 69
**Author**: toadStool dev (automated)
**Status**: All quality gates passing (0 clippy, 0 fmt, 0 doc warnings)

---

## Summary

Absorbed handoffs from all 5 springs (hotSpring, neuralSpring, wetSpring, airSpring, groundSpring) and wateringHole standard reviews. 16 new WGSL shaders, 3 new Rust GPU ops, probe-informed f64 strategy, ESN multi-head infrastructure, ODE universal precision templates.

---

## Changes by Spring

### hotSpring (V0614, V0615)
- **f32 buffer system**: `create_f32_rw_buffer()`, `create_f32_output_buffer()`, `upload_f32()`, `read_back_f32()` on `WgpuDevice`.
- **ESN 11-head**: `ESN_MULTI_HEAD_COUNT=11`, `ESNConfig::multi_head(input_size)`, `ExportedWeights::migrate_to_multi_head()`.
- **Remaining**: GPU ESN dispatch pattern (reservoir update + readout shader wiring), intra-scan adaptive steering, rust-toolchain.toml alignment.

### neuralSpring (V59)
- **12 new WGSL shaders**:
  - Attention: `triangle_mul_outgoing_f64`, `triangle_mul_incoming_f64`, `msa_row_attention_scores_f64`, `msa_col_attention_scores_f64`, `ipa_scores_f64`, `triangle_attention_f64`
  - Structure: `backbone_update_f64`, `torsion_angles_f64`
  - HMM: `hmm_backward_log_f64`, `hmm_viterbi_f64`
  - Stats: `matrix_correlation_f64`, `linear_regression_f64`
- **Remaining**: Rust op dispatch wiring for all 12 shaders, remaining 9 AlphaFold2 shaders (outer product mean, pair transition, template embedding, recycling, FAPE loss, pLDDT, structure violation, confidence, ensemble averaging).

### wetSpring (V65)
- **ODE universal precision**: `wgsl_rk4_template_universal()` generates `Scalar`/`op_*` WGSL. `OdeSystem::wgsl_derivative_universal()` optional trait method. `ExponentialDecay` has universal variant.
- **Remaining**: Migrate existing ODE systems (QS, phage_defense, etc.) to universal derivatives. `ComputeDispatch` builder adoption for batched ODE. DF64 GEMM bind-group compatibility. Unidirectional streaming. `BandwidthTier` in metalForge. `SparseGemmF64`.

### airSpring (V030)
- **Anderson coupling shader**: `anderson_coupling_f64.wgsl` — GPU construction of Anderson Hamiltonian H=-tΔ+V for d-dimensional cubic lattice. Single-thread-per-site diagonal + off-diagonal output.
- **Remaining**: Rust op wrapper, benchmark suite as GPU validation target, metalForge workload catalog entry.

### groundSpring (V35, V37)
- **Runtime f64 probe**: `F64BuiltinCapabilities.basic_f64` probes whether device can compile basic f64 WGSL. `fp64_strategy_probed()` overrides heuristic when probe fails.
- **sin/cos workaround methods**: On both `F64BuiltinCapabilities` and `GpuDriverProfile`.
- **3 grid search ops**: `grid_fit_2d()`, `grid_search_3d()`, `band_edges_parallel()` — all wired via `ComputeDispatch` builder (first production use).
- **Multinomial/Wright-Fisher audit**: Added `enable f64;` directive; Xoshiro128** PRNG alignment confirmed.
- **Remaining**: DF64 fallback as default for all shaders, PRNG alignment audit across all bio ops, unidirectional streaming with resident memory, NAK workgroup tuning.

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | 0 diffs |
| `cargo clippy --workspace --all-targets -- -D warnings` | 0 warnings |
| `cargo doc --workspace --no-deps` | 0 warnings |
| New tests | 10 passing (6 probe, 1 ODE universal, 3 layout) |
| WGSL shader count | 643+ |

---

## New Files

### WGSL Shaders (16)
```
crates/barracuda/src/shaders/attention/triangle_mul_outgoing_f64.wgsl
crates/barracuda/src/shaders/attention/triangle_mul_incoming_f64.wgsl
crates/barracuda/src/shaders/attention/msa_row_attention_scores_f64.wgsl
crates/barracuda/src/shaders/attention/msa_col_attention_scores_f64.wgsl
crates/barracuda/src/shaders/attention/ipa_scores_f64.wgsl
crates/barracuda/src/shaders/attention/triangle_attention_f64.wgsl
crates/barracuda/src/shaders/misc/backbone_update_f64.wgsl
crates/barracuda/src/shaders/misc/torsion_angles_f64.wgsl
crates/barracuda/src/shaders/bio/hmm_backward_log_f64.wgsl
crates/barracuda/src/shaders/bio/hmm_viterbi_f64.wgsl
crates/barracuda/src/shaders/stats/matrix_correlation_f64.wgsl
crates/barracuda/src/shaders/stats/linear_regression_f64.wgsl
crates/barracuda/src/shaders/spectral/anderson_coupling_f64.wgsl
crates/barracuda/src/shaders/grid/grid_fit_2d_f64.wgsl
crates/barracuda/src/shaders/grid/grid_search_3d_f64.wgsl
crates/barracuda/src/shaders/grid/band_edges_parallel_f64.wgsl
```

### Rust Files (1)
```
crates/barracuda/src/ops/grid/grid_search_ops.rs
```

### Modified Rust Files (6)
```
crates/barracuda/src/device/probe.rs           — basic_f64 probe + sin/cos workarounds
crates/barracuda/src/device/driver_profile.rs  — fp64_strategy_probed() + sin/cos probed
crates/barracuda/src/device/wgpu_device/buffers.rs — f32 buffer helpers
crates/barracuda/src/esn_v2/config.rs          — multi-head constants + constructor
crates/barracuda/src/esn_v2/model.rs           — ExportedWeights::migrate_to_multi_head()
crates/barracuda/src/numerical/ode_generic.rs  — universal precision template + trait method
```

---

## Remaining Cross-Spring Debt (Full Re-Audit Feb 27, 2026)

> **NOTE**: Re-audit confirmed most Spring-requested shaders already exist in
> barracuda. The hotSpring lattice suite (polyakov, su3_math, prng_pcg,
> gauge_force_df64, wilson_plaquette_df64, hmc_force_df64, CG shaders,
> sum_reduce, df64_core, df64_transcendentals, heat_current), neuralSpring
> Priority 1 (gelu, softmax, layer_norm, sdpa_scores, attention_apply, sigmoid,
> outer_product), Priority 2 (chi_squared, kl_divergence), wetSpring Tier A
> bio shaders (dada2_e_step, quality_filter, snp_calling, dnds_batch,
> pangenome_classify, ani_batch, rf_batch_inference), ESN shaders
> (reservoir_update, readout), and batched_qs_ode_rk4 are all present.
> False positives removed from remaining debt.

### P1 — Rust Op Wiring (dispatch for existing + S69 shaders)
- Wire all 12 S69 neuralSpring shaders to Rust dispatch functions (triangle_mul ×2, triangle_attention, msa_row/col_attention, ipa_scores, backbone_update, torsion_angles, hmm_backward_log, hmm_viterbi, matrix_correlation, linear_regression)
- Wire anderson_coupling_f64.wgsl to Rust dispatch
- Wire existing shaders lacking dispatch: chi_squared_f64 dispatch, kl_divergence_f64 fused dispatch, hmm_backward_dispatch, hmm_viterbi_dispatch, boltzmann_dispatch, eigh_dispatch

### P2 — Remaining Shaders (truly missing after audit)
- **hotSpring**: stress_virial_f64.wgsl, vacf_batch_f64.wgsl (MD observables — RDF histogram, MSD already covered)
- **hotSpring lattice**: NeighborMode::PrecomputedBuffer variant for existing gauge_force/plaquette/kinetic_energy shaders (shaders exist, need neighbor-buffer binding mode)
- **neuralSpring AlphaFold2 (9 advanced)**: outer_product_mean_f64 (MSA→pair bridge, distinct from existing outer_product_f64), pair_transition, template_embedding, recycling, FAPE_loss, pLDDT, structure_violation, confidence, ensemble_averaging
- **wetSpring**: GPU Lanczos kernel (SpMV + tridiagonalization), DF64 Lanczos variant
- **airSpring batch ops** (new op codes for existing batched_elementwise_f64 framework): Hargreaves ET₀ (op=6), Dual Kc (op=8), VG θ/K, Thornthwaite, GDD scan/accumulate, sensor calibration
- **airSpring composite**: BatchedCropPipeline (fused ET₀→Kc→WB→yield dispatch)

### P3 — Rust Ops / Modules
- **Lattice**: Pseudofermion HMC (477 lines), action_density(), Omelyan integrator
- **Domain ops**: SparseGemmF64 (CSR × dense for NMF), kimura_fixation GPU, jackknife_mean_variance GPU, fao56_et0 batch dispatch
- **ML/NN**: SimpleMLP (JSON weight loading), LstmReservoir, EsnClassifier, TensorSession::fused_mlp
- **Testing**: GpuTestHarness (shared device + mutex), require_gpu(), baseline_path()
- **NPU**: NpuDispatch trait (generic interface, referenced by airSpring/wetSpring/groundSpring)
- **Bio wrappers**: batched_multinomial_occupancy, wright_fisher_simulate, QsBiofilmOde, ConvergenceGuard
- **Tolerance**: Merge wetSpring 82-constant registry with barracuda 12 constants, tolerance_registry! macro
- **Richards PDE**: Carsel & Parrish VG lookup (12 USDA textures), Result<_, BarracudaError>
- **Parsers**: Streaming FASTQ/mzML/MS2 (wetSpring sovereign zero-copy I/O)

### P4 — metalForge Streaming
- Stage/Pipeline/Topology builder (hotSpring Forge v0.3-v0.5)
- PipelineBuilder with ChannelKind::Filtered
- Runtime reconfiguration (Pipeline::reconfigure())
- StageMetrics, SiliconEfficiency, auto-calibration
- `Fp64Strategy::Concurrent` (shader-level interleaving)
- NPU placement topology (A-F orderings)
- BandwidthTier + chained_transfer_cost (PCIe cost model)

### P5 — Architecture
- DF64 fallback as default for all shaders (groundSpring V35, both NAK and NVVM fail)
- Unidirectional streaming with resident memory (use_resident_memory flag)
- NAK workgroup tuning (64-wide Volta vs 256-wide Ada)
- MultiGpuPool (discover f64-capable adapters, split batches, merge)
- Buffer splitting for NVK (nouveau PTE limit ~1.2 GB)
- Device-lost recovery pattern (retry instead of skip)
- max_buffer_size sanity checking (NVK reports ~2^57 instead of VRAM)
- `anyhow` → `thiserror` in peripheral crates
- `manual_jsonrpc` → `pure_jsonrpc` serving layer
- BLAS small-matrix fast-path for matmul_dispatch (0.3× vs NumPy for small matrices)
- Ring buffer readback (GPU-resident for streaming disorder sweeps)

### P6 — Coverage & Testing
- barracuda 80.7% → 90% target
- GPU integration tests for all 16 new S69 shaders
- Cross-substrate parity testing harness (CPU/GPU/NPU)
- dispatch_overhead_benchmark in CI
- Three-mode validation (local / barracuda / barracuda-gpu)
- AMD RADV f64 transcendental testing (RX 6950 XT)

### P7 — NVK / Driver
- NVK device loss at 32⁴ (Mesa upstream bug)
- NAK exp/log f64 upstream fix (from_nir.rs:1092 assertion)
- Build Mesa NVK from git HEAD for regression testing
- Nouveau auto-load at boot (systemd/udev for Titan V)

### P8 — Documentation
- f32/f64 type boundary docs (which GPU ops expect which)
- Tolerance hierarchy docs (single-transcendental vs chained vs ensemble)
- PRNG type-safety audit across all f64 WGSL shaders
- erf precision docs (~5e-7 Abramowitz & Stegun, not machine epsilon)
- GPU_LOG_POLYFILL constant (1e-7 for chained transcendentals)
- Pre-normalization requirements (BatchIprGpu)
- Upper-triangle output convention (PairwiseJaccardGpu)
- Cross-spring shader lineage (whitePaper/CROSS_SPRING_SHADER_LINEAGE.md)
- Streaming pattern as first-class ToadStool usage pattern
