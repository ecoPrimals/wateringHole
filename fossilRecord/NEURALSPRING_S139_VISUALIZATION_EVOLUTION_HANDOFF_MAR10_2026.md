# neuralSpring S139 — Visualization Evolution + Upstream Gap Closure

**Date**: 2026-03-10
**From**: neuralSpring S139
**To**: petalTongue, barraCuda, toadStool, coralReef, groundSpring
**License**: AGPL-3.0-or-later

## Summary

neuralSpring S139 expanded from 12 to **16 petalTongue scenario tracks**,
wiring the S138 capabilities (streaming parsers, BLAST pipeline, Kokkos
benchmark) into human-readable, actionable visualizations. This is the
bridge between "pipeline works" and "scientist can see it."

## What Was Delivered

### 4 New Scenario Builders

| Scenario | Module | DataChannel Types | Nodes |
|----------|--------|-------------------|-------|
| **Search Results** | `scenarios/search_results.rs` | Bar, Gauge, TimeSeries, Distribution | `search_pipeline`, `kmer_index`, `hit_analysis` |
| **Streaming I/O Quality** | `scenarios/streaming_io.rs` | Distribution, TimeSeries, Bar, Gauge | `fastq_quality`, `fasta_lengths`, `vcf_variants` |
| **Kokkos GPU Parity** | `scenarios/kokkos_parity.rs` | Heatmap, Bar, Gauge, TimeSeries | `parity_overview`, `parallel_for_ops`, `parallel_reduce_ops`, `domain_ops` |
| **Industry Coverage** | `scenarios/industry_coverage.rs` | Heatmap, Bar, Gauge | `coverage_overview`, `domain_progress`, `implementation_detail` |

### Key Design Decisions

1. **All builders call real domain logic** — not synthetic data. The search
   scenario runs a real seed-and-extend pipeline. The streaming scenario
   parses real FASTQ/FASTA/VCF records. The industry scenario reflects
   actual `INDUSTRY_TOOL_GAP_ANALYSIS.md` status.

2. **Kokkos parity uses reference baselines from groundSpring V100**.
   These will be replaced with measured values once `bench_kokkos_parity`
   runs on the same hardware. The dashboard structure (gap %, overhead
   ratio, per-pattern breakdown) is stable.

3. **Industry coverage is a living dashboard** — tool inventory is a
   simple data structure that evolves with the codebase. Adding a new
   tool = one line in `tool_inventory()`.

### Ecosystem Dashboard Binary

`src/bin/neuralspring_ecosystem_dashboard.rs`:
- Renders all 16 tracks via `full_study()` to petalTongue
- Streams live gauge updates (search stats, Kokkos overhead, coverage %)
- Supports `MODE=dump` for offline JSON export
- Fallback to headless mode when petalTongue is unavailable

### Test Coverage

- 12 new scenario tests (structure, channel types, JSON roundtrips)
- Total scenario tests: 39 (was 27)
- All clippy-pedantic clean, `cargo fmt` clean

## Upstream Requests

### petalTongue

1. **Conditional coloring for Heatmap**: The Kokkos parity heatmap needs
   diverging colors (green ≤1.0×, yellow 1.0–2.0×, red >2.0×). Current
   Heatmap renderer uses sequential palette only.

2. **ThresholdRange on Heatmap cells**: We push thresholds but they only
   apply to Gauge today. Extending to Heatmap would make the parity
   dashboard immediately actionable.

3. **Grammar expression support for composite layouts**: The ecosystem
   dashboard pushes 16 tracks as a flat graph. A grammar-level
   `facet_wrap` or `small_multiples` directive would let petalTongue
   auto-layout the 4 new tracks as a grouped panel.

### groundSpring

1. **Run `bench_kokkos_parity` on Kokkos hardware**: The benchmark binary
   is ready (`src/bin/bench_kokkos_parity.rs`). Running it on the same
   machine as the Kokkos-CUDA baselines would produce the first real
   overhead measurements. The dashboard scenario will auto-update.

2. **Export Kokkos baselines as JSON**: Currently the reference values in
   `kokkos_parity.rs::reference_benchmarks()` are hand-transcribed. A
   machine-readable export from groundSpring would enable automated
   comparison.

### barraCuda

1. **Batch Smith-Waterman dispatch**: The search pipeline's extension
   phase currently uses CPU SW. A `SmithWatermanBatchGpu` that accepts
   a buffer of `(query_window, target_window)` pairs would GPU-accelerate
   the pipeline without per-hit dispatch overhead.

2. **GPU k-mer index lookup**: Phase 1 seeding is CPU-bound. A GPU kernel
   that performs parallel k-mer hash lookups against a device-side index
   would unlock throughput for large databases.

### toadStool

1. **Pipeline graph orchestration for search**: The BLAST pipeline has
   3 stages (seed → extend → score) that map naturally to
   `pipeline_graph` DAG nodes. Once toadStool exposes this as a cargo
   dependency, neuralSpring can replace its local orchestration.

## Pins

- neuralSpring: S139
- barraCuda: `a898dee`
- toadStool: `bfe7977b`
- coralReef: `d29a734`
- petalTongue: v1.3.0+ (DataBinding schema)

## Zero API Breakage

All existing 12 scenarios, `PetalTonguePushClient`, `StreamSession`,
and `TrainingVisualizer` unchanged. New scenarios are additive.

## What a Scientist Sees

```
petaltongue ui --scenario sandbox/scenarios/neuralspring-full-study.json
```

They get a 16-track graph showing:
- Neural network training spectral diagnostics (live streaming)
- Protein folding primitive inventory
- BLAST-like search results with hit scores and seed density
- FASTQ quality distributions, FASTA statistics, VCF variant density
- GPU performance vs Kokkos baselines (gap chart, overhead gauges)
- Industry tool coverage heatmap (what's done, what's next)

All rendered with the `neural-dark` theme (electric blue/magenta).

## Deep Debt Eliminated (S139)

### Hardcoding → Capability-Based

1. **`config.rs` module**: Centralized all primal identity strings,
   environment variable names, and petalTongue domain/theme constants.
   Single source of truth — no more scattered `"neuralspring"`, `"neural"`,
   `"PETALTONGUE_SOCKET"` strings across modules.

2. **Environment variables**: `PETALTONGUE_SOCKET`, `XDG_RUNTIME_DIR`,
   `NEURALSPRING_REQUIRE_GPU`, `NEURALSPRING_BACKEND` all reference
   `config::ENV_*` constants.

3. **Primal family name**: `config::PRIMAL_FAMILY` derived from
   `env!("CARGO_PKG_NAME")` at build time. petalTongue domain is
   `config::PETALTONGUE_DOMAIN` and theme is `config::PETALTONGUE_THEME`.

### Magic Numbers → Named Constants

4. **Streaming buffer capacities**: `LINE_BUF_CAPACITY` (256) and
   `VCF_LINE_BUF_CAPACITY` (512) in `streaming/mod.rs` replace inline
   magic numbers across FASTA, FASTQ, and VCF parsers.

5. **Backpressure threshold**: `StreamSession::BACKPRESSURE_THRESHOLD`
   (0.1) replaces inline `0.1` in `stream.rs`.

### Unnecessary Allocations Eliminated

6. **`search_results.rs`**: Eliminated `db_encoded.clone()` by reordering
   operations — build k-mer index first (borrows), then move into
   pipeline (consumes). Saves one full database copy.

### Test Coverage

- 1048 lib tests (was 1045, +3 from `config.rs`)
- Zero clippy warnings from new code
- All pre-existing tests pass
