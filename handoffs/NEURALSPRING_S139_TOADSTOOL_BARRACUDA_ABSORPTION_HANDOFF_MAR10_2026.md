# neuralSpring S139 — toadStool/barraCuda Absorption + Evolution Handoff

**Date**: 2026-03-10
**From**: neuralSpring S139 (1048 lib + 71 forge + 9 integration tests, 233 binaries, 0 clippy)
**To**: barraCuda team, toadStool team
**License**: AGPL-3.0-or-later
**Synced against**: barraCuda `a898dee`, toadStool `bfe7977b`, coralReef `d29a734`
**Builds on**: S138 (industry gap), S137 (upstream rewire), S136 (deep audit), S135 (visualization)

---

## Executive Summary

neuralSpring S136–S139 delivered:

1. **Streaming bioinformatics parsers** (FASTA, FASTQ, VCF) — O(record_size) memory, 39 tests
2. **CPU-reference BLAST-like search pipeline** — k-mer seeding + seed-and-extend + Smith-Waterman, 19 tests
3. **Kokkos GPU parity benchmark harness** — 9 ops × production scale, structured for barraCuda comparison
4. **16 petalTongue visualization scenarios** — 4 new (search, streaming I/O, Kokkos, industry coverage)
5. **`config.rs` centralization** — primal identity, env vars, petalTongue config (zero scattered strings)
6. **Deep debt elimination** — magic numbers, hardcoding, unnecessary clones, backpressure threshold

---

## What barraCuda Should Absorb

### 1. Batch Smith-Waterman GPU Shader

neuralSpring has a CPU-reference Smith-Waterman scoring implementation in `src/search/seed_extend.rs`.
The BLAST-like pipeline needs GPU acceleration for production-scale alignment:

- **API**: `SmithWatermanBatchGpu::score(query: &[u32], targets: &[&[u32]], config: &ScoringConfig) -> Vec<AlignmentScore>`
- **Scoring matrix**: BLOSUM62 (protein) + DNA match/mismatch (nucleotide)
- **Parallelism**: One workgroup per query-target pair, thread-per-cell for DP matrix
- **Priority**: P1 — blocks GPU BLAST pipeline

### 2. GPU K-mer Seed Lookup

neuralSpring has a CPU `KmerIndex` (`src/search/kmer_index.rs`) that maps k-mers to database positions.
GPU acceleration would enable real-time seeding at genome scale:

- **API**: `KmerSeedGpu::lookup(queries: &[u32], index: &KmerIndex) -> Vec<SeedHit>`
- **Strategy**: Hash table in GPU storage buffer, parallel probe per query k-mer
- **Priority**: P2 — enables GPU-resident BLAST pipeline

### 3. Kokkos Parity Baselines

`bench_kokkos_parity.rs` compares 9 barraCuda GPU operations against Kokkos-CUDA baselines.
The benchmark harness is ready but needs **groundSpring** to run the Kokkos side and export
baselines as JSON. Operations benchmarked:

| Op | Scale | barraCuda API |
|----|-------|--------------|
| MatMul | 1024×1024 | `Tensor::matmul` |
| Transpose | 4096×4096 | `Tensor::transpose` |
| Element-wise (ReLU) | 1M elements | `Tensor::relu_wgsl` |
| Reduction (sum) | 1M elements | `ReduceScalarPipeline::sum_f64` |
| FFT 1D | 65536 points | `Fft1DF64::execute` |
| Batched eigensolve | 100 × 32×32 | `eigh_householder_qr` |
| SpMV | 10K × 10K sparse | (proposed) |
| Histogram | 10M values | (proposed) |
| Sort | 1M keys | (proposed) |

**Action**: groundSpring team run Kokkos benchmarks on matching hardware, export as JSON.
neuralSpring will consume and visualize via `kokkos_parity_study()` petalTongue scenario.

---

## What toadStool Should Absorb

### 1. Pipeline Graph for Bio Workflows

neuralSpring S138 introduced `BLAST_LIKE_SEARCH_SCOPE.md` and `MSA_PIPELINE_SCOPE.md` defining
bio-specific pipeline patterns that need toadStool's `pipeline_graph`:

- **Conditional edges**: Skip Smith-Waterman if seed count below threshold
- **Fan-out/fan-in**: Parallel alignment of multiple query sequences
- **Iteration**: Iterative refinement loops (SATé-style)
- **Priority**: P1 — toadStool S139 already absorbed `pipeline_graph` DAG from neuralSpring S134

### 2. Streaming Pipeline for FASTA/FASTQ

neuralSpring's streaming parsers produce records one-at-a-time. toadStool's streaming dispatch
could batch these into GPU-friendly chunks:

- **Pattern**: `StreamingFastaReader → batch(N) → GPU quality filter → collect`
- **Backpressure**: Already modeled in `StreamSession::BACKPRESSURE_THRESHOLD`

---

## What neuralSpring Learned (Relevant to barraCuda/toadStool Evolution)

### Config Centralization Pattern

`src/config.rs` centralizes all identity and environment strings:

```rust
pub const PRIMAL_FAMILY: &str = env!("CARGO_PKG_NAME");
pub const PETALTONGUE_DOMAIN: &str = "neural";
pub const ENV_PETALTONGUE_SOCKET: &str = "PETALTONGUE_SOCKET";
pub const ENV_REQUIRE_GPU: &str = "NEURALSPRING_REQUIRE_GPU";
```

**Recommendation**: barraCuda and toadStool should adopt similar centralization.
Scattered hardcoded strings are a recurring debt pattern across all Springs.

### Streaming Parser Architecture

The FASTA/FASTQ/VCF parsers in `src/streaming/` demonstrate O(record_size) memory patterns:
- `String::with_capacity(LINE_BUF_CAPACITY)` with centralized constants
- Iterator-based yielding (no full-file load)
- Type-safe record structs with accessor methods

This pattern is reusable for any bioinformatics format barraCuda wants to support natively.

### Visualization as Validation

The 16 petalTongue scenarios run actual neuralSpring domain logic (search pipeline, streaming
parsers, Kokkos benchmarks) and visualize results. This "visualization as validation" pattern
caught a borrow-after-move bug in search_results.rs that unit tests missed — the scenario
forced a specific execution order that exposed the issue.

---

## Current barraCuda APIs neuralSpring Depends On

| API | Use | Tests |
|-----|-----|-------|
| `barracuda::nn::SimpleMlp` | WDM surrogates (nW-01, nW-02) | 66/66 |
| `barracuda::ops::bio::hmm_viterbi` | HMM Viterbi f64 dispatch | 11/11 |
| `barracuda::ops::bio::HmmBatchForwardF64` | HMM forward batch | 11/11 |
| `barracuda::linalg::eigh_householder_qr` | Eigensolver delegation | 9/9 |
| `barracuda::stats::*` | 24 paper modules | 203/203 |
| `barracuda::dispatch::domain_ops` | 7 dispatcher methods | 53/53 dispatch parity |
| `barracuda::shaders::provenance` | Cross-spring lineage | 7/7 |
| `barracuda::spectral::*` | Spectral theory stack | 17/17 |

**Total**: 46 upstream rewires, 130+ import files, 25+ submodules exercised.

---

## Sprint 2 APIs (Documented in V92, Not Yet at HEAD)

These neuralSpring APIs were documented for absorption but haven't landed in barraCuda HEAD:

| API | Status | Blocks |
|-----|--------|--------|
| `activations` (consolidated sigmoid/gelu/relu/softmax) | Documented | — |
| `rng::lcg_step` | Documented | Stochastic GPU pipelines |
| `tridiagonal_ql` | Documented | GPU eigensolver |
| `WrightFisherF32` | Documented | Population genetics GPU |
| `AttentionDims` | Documented | Structured MHA config |
| `fused_ops_healthy()` canary | Documented | Regression detection |

---

## Verification

| Check | Result |
|-------|--------|
| `cargo check` | PASS |
| `cargo test --lib` | 1048/1048 PASS |
| `cargo clippy --all-targets -- -D warnings` | 0 warnings |
| `cargo doc --no-deps` | 0 warnings |
| `cargo fmt --check` | clean |

---

## What Remains (P1/P2)

| Priority | Item | Owner |
|----------|------|-------|
| P1 | Batch Smith-Waterman GPU shader | barraCuda |
| P1 | GPU k-mer seed lookup | barraCuda |
| P1 | Kokkos baselines as JSON | groundSpring |
| P2 | toadStool streaming dispatch for bio parsers | toadStool |
| P2 | Sprint 2 API absorption landing | barraCuda |
| P2 | petalTongue Heatmap diverging color support | petalTongue |
| P3 | GPU MSA (multiple sequence alignment) | barraCuda + toadStool |
