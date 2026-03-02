# ToadStool S80 — Cross-Spring Absorption + Nautilus Handoff

**Date**: March 2, 2026
**Sessions**: 79–80
**From**: ToadStool S80
**To**: ecoPrimals ecosystem (all springs, baseCamp)
**Supersedes**: TOADSTOOL_V69_SPRING_ABSORPTION_HANDOFF_FEB27_2026.md
**ToadStool Pin**: S80
**License**: AGPL-3.0-or-later

---

## Executive Summary

- **barracuda::nautilus** absorbed from bingoCube — standalone evolutionary reservoir computing (7 files, 22 tests, CPU-only)
- **ai.nautilus.\* JSON-RPC** — 8 methods wired into daemon for live prediction, training, screening, edge detection, and brain import/export
- **BatchedEncoder** — fused multi-op GPU pipelines via single `queue.submit()` (46-78× potential speedup)
- **ComputeDispatch migration** — 95/250 ops migrated (was 76 at S78)
- **GpuDriverProfile sin/cos workarounds** — Taylor-series preamble for NVK driver imprecision
- **ESN MultiHeadEsn** — 36-head with HeadGroup variants, head_disagreement() uncertainty, ExportedWeights aligned with hotSpring
- All quality gates green: clippy 0, fmt 0, doc 0

---

## Part 1: Nautilus Absorption (from bingoCube/hotSpring)

### barracuda::nautilus Module (7 files)

| File | Purpose | Tests |
|------|---------|-------|
| `board.rs` | L×L grid, column-range constraints, discrete/continuous input, BLAKE3 projection | 6 |
| `evolution.rs` | Elitism/Tournament/Roulette selection, column-swap crossover, mutation preserving invariants | 4 |
| `population.rs` | Board ensembles, Pearson correlation fitness evaluation | 3 |
| `readout.rs` | Ridge regression via `solve_f64_cpu` (gpu feature) / `ridge_regression` (cpu-only) | — |
| `shell.rs` | Layered evolutionary history, `GenerationRecord`, `InstanceId`, lineage, merge | 5 |
| `brain.rs` | `NautilusBrain` — observe, train, predict, screen, detect edges, drift monitor | 4 |
| `mod.rs` | Re-exports | — |

### ai.nautilus.* JSON-RPC (8 methods)

| Method | Description |
|--------|-------------|
| `ai.nautilus.status` | Brain status (observation count, shell generation, drift) |
| `ai.nautilus.observe` | Feed physics observation (beta, observable values) |
| `ai.nautilus.train` | Evolve shell on accumulated observations |
| `ai.nautilus.predict` | Predict dynamical observables for a beta value |
| `ai.nautilus.screen` | Score candidate beta values by information content |
| `ai.nautilus.edges` | Detect concept edges via leave-one-out analysis |
| `ai.nautilus.shell.export` | Serialize brain state to JSON |
| `ai.nautilus.shell.import` | Restore brain from serialized JSON |

**Integration**: `barracuda` added as optional CPU-only CLI dependency (`default-features = false`). Feature-gated: `nautilus = ["dep:barracuda"]`, included in `full`.

---

## Part 2: GPU Pipeline Evolution

### BatchedEncoder

Single `CommandEncoder` for multi-op GPU pipelines. Eliminates per-op `queue.submit()` overhead.

```rust
let mut encoder = BatchedEncoder::new(&device)?;
encoder.add_pass()
    .shader("linear_f64.wgsl")
    .storage_read(0, &weights_buf)
    .storage_read(1, &input_buf)
    .storage_rw(2, &output_buf)
    .uniform(3, &params_buf)
    .workgroups(wg_x, 1, 1)
    .build()?;
encoder.submit(&device.queue);
```

**Used by**: `fused_mlp` (MLP forward pass across layers in single submit).

### Batch Nelder-Mead GPU

N independent Nelder-Mead optimizations in parallel. Batched simplex shader entry points in `simplex_ops_f64.wgsl`:
- `batched_compute_centroid`, `batched_reflect`, `batched_expand`, `batched_contract`, `batched_shrink`

### GpuDriverProfile sin/cos F64 Workarounds

NVK driver produces imprecise f64 sin/cos (uses MUFU — f32 precision in f64 register).

**Solution**: `NvkSinCosF64Imprecise` workaround → Taylor-series preamble injected into shaders:
- `sin_f64_safe(x)` — 7-term Taylor around origin
- `cos_f64_safe(x)` — 7-term Taylor around origin
- `asin`/`acos` protected from false replacement via substring analysis

---

## Part 3: ComputeDispatch Migration (76→95)

19 ops migrated in 4 batches:

| Batch | Ops |
|-------|-----|
| 2 | elastic_transform, gillespie, tree_inference, mixup, random_affine, random_perspective |
| 3 | lennard_jones_f64, cumsum_f64, label_smoothing, slice_assign, random_crop, lp_pool2d, unfold |
| 4 | global_maxpool, adaptive_avgpool2d, adaptive_maxpool2d, reduce, scan, embedding_wgsl |

~155 legacy ops remaining (incremental).

---

## Part 4: Additional Completions

| Item | Status |
|------|--------|
| `StatefulPipeline<S>` | Generic pipeline for day-over-day state + `WaterBalanceState` |
| `NeighborMode::PrecomputedBuffer` | 2D/3D/4D periodic lattice precomputation (6 tests) |
| `BatchedMultinomialGpu` alignment | `cumulative_probs` + `seed` config (groundSpring V37) |
| `SparseGemmF64` | Confirmed already exists (CSR×dense SpMM + spmm_f64.wgsl) |
| IPC multi-transport | Confirmed already exists (Unix/Abstract/TCP) |
| Socket resolution | 4 scattered call sites → `toadstool_common::primal_sockets` API |
| ESN MultiHeadEsn | 36-head, 6 HeadGroup variants, head_disagreement(), ExportedWeights aligned |

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all -- --check` | 0 diffs |
| `cargo clippy --workspace -- -D warnings` | 0 warnings |
| `cargo doc --no-deps --workspace` | 0 warnings |
| `cargo build --workspace` | Clean |
| barracuda tests | 2,800+ |
| Workspace tests | 5,500+ |

---

## Action Items for Springs

1. **hotSpring**: Nautilus Brain now in ToadStool — future brain evolution should reference `barracuda::nautilus` API. `ai.nautilus.*` methods available over Unix socket.
2. **neuralSpring**: `BatchedEncoder` available for fused MLP/Transformer pipelines. ESN `MultiHeadEsn` aligned with hotSpring conventions.
3. **wetSpring**: `StatefulPipeline` available for water balance and other day-over-day computations. `BatchedMultinomialGpu` signature aligned.
4. **airSpring**: `batched_nelder_mead_gpu` available for isotherm fitting and multi-start optimization.
5. **groundSpring**: `GpuDriverProfile` sin/cos workarounds active on NVK. `NeighborMode::PrecomputedBuffer` available for lattice simulations.
6. **baseCamp Paper 11**: ToadStool has absorbed the Nautilus Shell. bingoCube remains the canonical source for other primals (beardog, songbird handshakes).

---

## Remaining (Deferred)

| Item | Source | Reason |
|------|--------|--------|
| `BatchReconcileGpu` | wetSpring V61 | Full DTL reconciliation, no existing primitives |
| metalForge Stage/Pipeline topology | hotSpring/wateringHole | Design phase |
| NPU bandwidth model | neuralSpring V60 | Design phase |
| Pseudofermion HMC | wateringHole V69 | Physics ops (477 lines) |
| Omelyan integrator | wateringHole V69 | Physics ops |
| Richards PDE (12 USDA textures) | wateringHole V69 | Physics ops |
| Streaming FASTQ/mzML/MS2 | wateringHole V69 | Bio I/O |

---

## Reproduction

```bash
cd /path/to/ecoPrimals/phase1/toadStool

# Quality gates
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo doc --no-deps --workspace
cargo build --workspace

# Nautilus tests
cargo test -p barracuda --lib nautilus

# Full barracuda tests
cargo test -p barracuda --lib

# Full workspace
cargo test --workspace
```
