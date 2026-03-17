# ToadStool/BarraCuda S86 — ComputeDispatch Evolution + Deep Debt Handoff

**Date**: March 2, 2026  
**From**: ToadStool S84–S86  
**To**: ToadStool/BarraCuda team (next session)  
**License**: AGPL-3.0-or-later  
**Covers**: Sessions 84–86 (March 2, 2026)

---

## Executive Summary

- **33 GPU ops migrated** to `ComputeDispatch` builder across 3 sessions (111→144 total)
- **Full ops audit** revealed ~139 remaining legacy files (up from previous ~57 estimate) — subdirectory ops (bio/, md/, lattice/, complex/, linalg/) were undercounted
- **Production stubs evolved**: wgpu_backend.rs magic numbers → real device.limits() queries; deployment.rs → capability-discovery documentation; experimental.rs → real FPGA/neuromorphic/quantum probes
- **God file refactored**: hydrology.rs (690L) → hydrology/ directory (CPU/GPU domain split)
- **2,866 barracuda tests pass**, 0 failures, 13 ignored — stable across all 3 sessions
- All quality gates green: check, clippy, fmt, doc

---

## Part 1: ComputeDispatch Migration (111→144)

### S84 Batch 5 (+9 ops)

| Op | File | Notes |
|----|------|-------|
| MatMul Tiled | `ops/matmul_tiled.rs` | 170L boilerplate → 10L |
| GEMM F64 | `ops/linalg/gemm_f64.rs` | One-shot path only; GemmCachedF64 kept manual |
| GIoU Loss | `ops/giou_loss.rs` | Object detection |
| Focal Loss | `ops/focal_loss.rs` | Imbalanced classification |
| Tversky Loss | `ops/tversky_loss.rs` | Medical imaging |
| Huber Loss | `ops/huber_loss.rs` | Robust regression |
| Hinge Loss | `ops/hinge_loss.rs` | SVM-style |
| Contrastive Loss | `ops/contrastive_loss.rs` | Self-supervised NT-Xent |
| Chamfer Distance | `ops/chamfer_distance.rs` | Point cloud similarity |

**Decision**: Skipped `pipeline/reduce.rs` and `staging/stateful.rs` — these intentionally cache pre-compiled pipelines; ComputeDispatch would be a performance regression.

### S85 Batch 6 (+12 ops)

| Op | File | Notes |
|----|------|-------|
| Cosine Similarity | `ops/cosine_similarity.rs` | Pairwise vectors |
| Covariance | `ops/covariance_wgsl.rs` | Kept staging readback |
| Cross Product | `ops/cross_product.rs` | Batched 3D |
| PSNR | `ops/psnr.rs` | Image quality |
| SSIM | `ops/ssim.rs` | Wang et al. |
| Diag | `ops/diag.rs` | Extract/create diagonal |
| Global AvgPool | `ops/global_avgpool.rs` | H×W→1×1 |
| Box IoU | `ops/box_iou.rs` | Object detection |
| Focal Loss Alpha | `ops/focal_loss_alpha.rs` | Per-class weights, 5 bindings |
| Rotary Embedding | `ops/rotary_embedding.rs` | RoPE for transformers |
| ALiBi | `ops/alibi.rs` | Position encoding |
| Flatten | `ops/flatten.rs` | Configurable dims |

### S86 Batch 7 (+12 ops)

| Op | File | Notes |
|----|------|-------|
| Determinant | `ops/determinant.rs` | LU decomposition |
| MSE Loss | `ops/mse_loss.rs` | Mean squared error |
| Dice | `ops/dice.rs` | Segmentation |
| Quantize | `ops/quantize.rs` | FP32→INT8/INT4 |
| Dequantize | `ops/dequantize.rs` | INT8/INT4→FP32 |
| BCE Loss | `ops/bce_loss.rs` | Binary cross-entropy |
| Permute | `ops/permute.rs` | N-D dimension permutation |
| MoveDim | `ops/movedim.rs` | Dimension reordering |
| LogSumExp | `ops/logsumexp.rs` | Numerically stable |
| Index Add | `ops/index_add.rs` | Scatter-add |
| Tensor Split | `ops/tensor_split.rs` | Split along dimension |
| Concat | `ops/concat.rs` | Concatenation |

---

## Part 2: Full Ops Audit — Remaining Legacy Files

Comprehensive audit of `crates/barracuda/src/ops/` found **~139 files** still using raw `create_bind_group_layout` / `create_compute_pipeline`. Previous estimates undercounted subdirectory ops.

### Remaining by Category

| Category | Count | Examples |
|----------|-------|---------|
| Root-level ops | ~60 | mosaic, stft, istft, cutmix, grid_mask, topk, conv1d/2d/3d, batch_matmul |
| bio/ ops | ~16 | rf_inference, snp, ani, wright_fisher, spatial_payoff, pairwise_jaccard |
| md/ ops | ~22 | morse, coulomb, berendsen, langevin, nose_hoover, velocity_verlet, pbc |
| lattice/ ops | ~8 | hmc_trajectory, lattice_init, higgs_u1, dirac, polyakov, pseudofermion |
| complex/ ops | ~10 | abs, add, mul, div, sub, conj, sqrt, log, exp, pow |
| linalg/ ops | ~9 | batched_eigh, triangular_solve, lu_gpu, svd_gpu, complex/abs,add |
| Other subdirs | ~14 | triplet_loss, nadam, adamw, mha, rmsprop, adadelta, expand, adam, sgd, attention |

### Recommended Next Batches

**Batch 8 (simple elementwise)**: sin_wgsl, cos_wgsl, exp_wgsl, log_wgsl, abs_wgsl, sqrt_wgsl, ceil_wgsl, floor_wgsl, round_wgsl, neg_wgsl, sign_wgsl, frac_wgsl — all identical 1-binding pattern.

**Batch 9 (complex/ suite)**: All 10 complex ops — identical pattern, batch-migrate in one pass.

**Batch 10 (activation functions)**: swish_wgsl, silu_wgsl, gelu_approximate_wgsl, hardswish_wgsl, mish_wgsl, celu_wgsl, selu_wgsl, softplus_wgsl, prelu_wgsl — same pattern.

**toadStool action**: The simple elementwise ops (batches 8–10) are the lowest-hanging fruit — ~32 ops with near-identical patterns that could be batch-migrated in a single session.

---

## Part 3: Production Stub & Magic Number Evolution

| Target | Before | After |
|--------|--------|-------|
| `wgpu_backend.rs` num_units | Hardcoded `1000` | `device.limits().max_compute_workgroups_per_dimension` |
| `wgpu_backend.rs` memory_capacity | Hardcoded per-type (16/4/8 GB) | `limits.max_buffer_size.max(fallback)` per type |
| `wgpu_backend.rs` memory_bandwidth | Hardcoded `500_000_000_000` | Varies by device type (discrete: 500G, integrated: 50G, CPU: 25G) |
| `wgpu_backend.rs` optimal_batch_size | Hardcoded `10_000` | Varies (discrete: 65K, integrated: 16K, CPU: 4K) |
| `deployment.rs` 10 methods | Stale "MODERNIZED" comments | Capability-discovery documentation |
| `experimental.rs` | `Ok(Vec::new())` | Real probes: FPGA (Xilinx XRT, Intel Quartus), neuromorphic (Akida VFIO, SpiNNaker), quantum (Qiskit, Cirq) |
| `frameworks.rs` execute | Echo input as output | `Err("not yet implemented — use barracuda Tensor operations")` |
| `hydrology.rs` | 690-line god file | hydrology/ directory: mod.rs (~310L CPU) + gpu.rs (~280L GPU) |

---

## Part 4: Architecture Observations

### ComputeDispatch NOT Suitable For

These files should remain manual wgpu:
- `pipeline/reduce.rs` — pre-compiled pipeline cache for repeated reductions
- `staging/stateful.rs` — cached pipelines for iterative GPU-resident computation
- `batched_encoder.rs` — multi-pass shared encoder
- `autotune.rs` — dynamic bind groups for performance tuning

**toadStool action**: Consider a `ComputeDispatch::cached()` or `CachedDispatch` variant for ops that need pre-compiled pipeline reuse. This would cover ~5 infrastructure files.

### God Files Remaining (>500 lines)

| File | Lines | Domain |
|------|-------|--------|
| `ops/mod.rs` | ~722 | Mostly `pub mod` declarations — acceptable |
| `device/wgpu_device/creation.rs` | ~646 | Device creation — complex but cohesive |
| `numerical/ode_generic.rs` | ~625 | Generic ODE solver — cohesive |
| `device/driver_profile/mod.rs` | ~632 | Driver detection — cohesive |
| `esn_v2/model.rs` | ~565 | ESN model — cohesive |
| `pipeline/mod.rs` | ~543 | Pipeline orchestration — cohesive |
| `cli/zero_config/service_discovery.rs` | ~545 | mDNS discovery — cohesive |
| `cli/network_config/configurator/core.rs` | ~647 | Network configurator — cohesive |

These are all cohesive domain modules. No further splitting recommended.

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo check --workspace` | ✅ 0 errors |
| `cargo test -p barracuda --lib` | ✅ 2,866 passed, 0 failed, 13 ignored |
| `cargo clippy --workspace` | ✅ 0 warnings |
| `cargo fmt --all -- --check` | ✅ 0 diffs |

---

## Reproduction

```bash
cd ecoPrimals/phase1/toadStool
cargo check --workspace
cargo test -p barracuda --lib -- 2>&1 | tail -5
```

---

*This handoff supersedes TOADSTOOL_BARRACUDA_S82_DEEP_DEBT_EVOLUTION_HANDOFF_MAR02_2026.md*
