<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->

# neuralSpring S138 — Industry Gap Evolution Handoff

**Date**: March 10, 2026
**From**: neuralSpring S138
**To**: barraCuda, toadStool, coralReef
**Status**: Code committed, upstream action items identified

---

## What neuralSpring Built This Session

### 1. Streaming I/O Parsers (`src/streaming/`)

| Parser | Module | Tests | Spec |
|--------|--------|-------|------|
| FASTA | `streaming::fasta::FastaReader` | 16 | R-01, R-03, R-05 |
| FASTQ | `streaming::fastq::FastqReader` | 15 | R-01, R-03, R-05 |
| VCF v4.x | `streaming::vcf::VcfReader` | 15 | R-01, R-03, R-05 |

All accept `impl BufRead`, yield via `Iterator`, O(`record_size`) memory.
Round-trip fidelity tests included. FASTA includes `encode_dna()` for
direct GPU kernel input (A=0, C=1, G=2, T=3, N=4).

### 2. BLAST-Like Seed-and-Extend Pipeline (`src/search/`)

| Component | Module | Tests | Status |
|-----------|--------|-------|--------|
| K-mer index | `search::kmer_index::KmerIndex` | 8 | CPU, production-ready |
| CPU Smith-Waterman | `search::seed_extend::cpu_smith_waterman` | 4 | Reference implementation |
| Search pipeline | `search::seed_extend::CpuSearchPipeline` | 7 | CPU reference, GPU-ready |

Pipeline architecture: k-mer seed → diagonal dedup → windowed SW extension → score filter.
CPU reference implementation validates correctness before GPU acceleration.

### 3. Kokkos Parity Benchmark Harness (`src/bin/bench_kokkos_parity.rs`)

Benchmarks 9 barraCuda GPU ops at production scale with timing output
formatted for direct comparison against groundSpring's Kokkos-CUDA
baseline. Categorizes each op as `parallel_for`, `parallel_reduce`, or
`domain` to isolate dispatch overhead from compute performance.

### 4. Spec Documents

| Document | Purpose |
|----------|---------|
| `specs/INDUSTRY_TOOL_GAP_ANALYSIS.md` | Comprehensive tool classification |
| `specs/BLAST_LIKE_SEARCH_SCOPE.md` | BLAST pipeline design (12–18 days) |
| `specs/MSA_PIPELINE_SCOPE.md` | AlphaFold MSA generation (27–40 days) |

---

## What barraCuda Needs to Build

### Priority 1: Batch Smith-Waterman Dispatch

The `SmithWatermanGpu::align()` currently handles a single query-target
pair per call. BLAST-like search generates 100–10,000 seed hits per query,
each requiring an SW extension.

**Request**: `SmithWatermanGpu::align_batch(&[(query, target)]) -> Vec<SwResult>`
that packs multiple pairs into a single `CommandEncoder` submission.

**Impact**: Eliminates per-hit dispatch overhead (~186µs × N_hits).
At 1,000 hits, saves ~186ms per query — the difference between
dispatch-overhead-bound (current) and compute-bound (target).

### Priority 2: Substitution Matrix in SW Shader

The current shader uses an externally-provided substitution matrix via
storage buffer. For protein BLAST, we need BLOSUM62 (20×20) as a
built-in option.

**Request**: `SwConfig::with_blosum62()` constructor that pre-loads
the standard matrix. No shader change needed — just a convenience API.

### Priority 3: K-mer Seed Lookup on GPU

`KmerHistogramGpu` counts k-mers. BLAST needs k-mer *lookup* against
a pre-built index (hash table on GPU).

**Request**: `KmerSeedGpu` primitive that takes a query + index and
returns `Vec<SeedHit>`. This moves Phase 1 (SEED) from CPU to GPU.

**Impact**: For large databases (UniRef90: ~100M sequences), CPU seeding
becomes the bottleneck. GPU seeding with the existing `KmerHistogramGpu`
architecture can process all query k-mers in parallel.

---

## What toadStool Needs to Build

### Pipeline Graph for Multi-Stage Bio Workflows

The BLAST pipeline has 3 dependent stages (seed → extend → score).
The MSA pipeline has 5+ stages (profile → search → collect → re-estimate → iterate).

**Request**: `pipeline_graph` support for:
1. **Conditional edges**: skip extension if no seeds found
2. **Fan-out/fan-in**: one query fans out to N database chunks, results merge
3. **Iterative loops**: JackHMMER converges after 3–5 iterations

The current `pipeline_graph` (absorbed from neuralSpring S139) supports
linear DAGs. Bio pipelines need loops and conditional branching.

### Kokkos GPU Benchmarks for neuralSpring Workloads

`bench_kokkos_parity.rs` produces timing for 9 barraCuda ops.
ToadStool should run the equivalent Kokkos-CUDA kernels and publish
comparison numbers to `wateringHole/`.

**Kernels to benchmark**:
- BatchFitness (10K×32) — parallel_for
- PairwiseHamming (200×1000) — parallel_reduce
- PairwiseJaccard (200×500) — parallel_reduce
- PairwiseL2 (200×64) — parallel_reduce
- LocusVariance (10×500) — parallel_reduce
- SpatialPayoff (128×128) — parallel_for
- HillGate (40K) — parallel_for
- MultiObjFitness (10K×30×3) — parallel_for
- SmithWaterman (256×256, bw=64) — anti-diagonal wavefront

---

## What coralReef Needs to Build

### WGSL Compilation for Bio Pipeline Shaders

The BLAST seed-and-extend pipeline will eventually need fused shaders:
- Seed lookup + extension window extraction in a single dispatch
- Batch SW with result filtering (score < threshold → skip readback)

coralReef's sovereign pipeline (`SubstrateKind::Sovereign`) should be
able to compile these fused WGSL shaders to native GPU binaries,
bypassing the wgpu dispatch overhead for hot-path bio operations.

**Request**: Confirm that `coral-gpu::compile_to_native()` handles
the shader patterns used by `SmithWatermanGpu` (anti-diagonal wavefront,
multiple storage buffers, f64 support).

---

## Validation State

```
Total streaming tests: 46 (FASTA 16, FASTQ 15, VCF 15)
Total search tests:    19 (kmer_index 8, seed_extend 11)
All clippy-pedantic:   clean
All cargo fmt:         clean
All cargo check:       clean
```

---

## Pins

| Component | Version |
|-----------|---------|
| neuralSpring | S138 (this session) |
| barraCuda | a898dee (unchanged) |
| toadStool | bfe7977b (unchanged) |
| coralReef | d29a734 (unchanged) |

---

## Zero API Breakage

This session added new modules only. No existing APIs were modified.
All 1014+ existing tests remain unaffected.
