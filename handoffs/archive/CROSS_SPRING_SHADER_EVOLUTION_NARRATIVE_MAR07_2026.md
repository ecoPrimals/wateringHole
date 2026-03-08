# Cross-Spring Shader Evolution Narrative

**Date**: March 7, 2026
**Session**: S130 (toadStool cross-spring rewiring)
**Primals**: toadStool (hardware), barraCuda (math/shaders), coralReef (compiler)

## Overview

This document records how shader patterns, precision techniques, and
scientific primitives flow between the five springs (hotSpring, wetSpring,
neuralSpring, airSpring, groundSpring) through the barraCuda/toadStool/coralReef
pipeline. It serves as the ecosystem-wide narrative of cross-spring evolution.

## The Sovereign Shader Pipeline

```
Spring domain code (WGSL)
    → barraCuda (ComputeDispatch + PrecisionStrategy)
    → toadStool (shader.compile.* JSON-RPC proxy)
    → coralReef (shader.compile.spirv / shader.compile.wgsl)
    → Native GPU binary (SASS/GFX)
```

toadStool S130 evolved `shader.compile.*` stubs into real coralReef proxy
handlers with capability-based discovery. The pipeline now dynamically detects
coralReef availability and falls back to naga-only compilation when unavailable.

## Cross-Spring Flows

### hotSpring → All Springs: Precision Foundation

**What**: DF64 double-float arithmetic (df64_core.wgsl, df64_transcendentals.wgsl),
Kahan summation, FMA control patterns.

**Timeline**: S49 (f32→f64 evolution), S71 (15 DF64 transcendentals completed).

**Impact**: hotSpring's lattice QCD precision requirements drove the creation of
~48-bit mantissa GPU arithmetic. This became the precision backbone for ALL
springs — neuralSpring attention layers, wetSpring bioinformatics, airSpring
hydrology, and groundSpring condensed matter all consume DF64 primitives.

### hotSpring → neuralSpring: FMA → Attention Shaders

**What**: FMA control and Kahan summation patterns adopted by coralForge
streaming attention (gelu_f64, layer_norm_f64, softmax_f64, sdpa_scores_f64).

**Impact**: The catastrophic cancellation prevention from lattice QCD directly
improved numerical stability in transformer attention mechanisms.

### hotSpring → wetSpring: Molecular Dynamics → Biomaterials

**What**: stress_virial_f64.wgsl (off-diagonal stress tensor), esn_readout_f64.wgsl
(echo state network readout).

**Impact**: MD simulation outputs from hotSpring feed directly into wetSpring's
bio-material mechanical property validation and temporal bio-signal modeling.

### neuralSpring → wetSpring + groundSpring: Statistics

**What**: fused_kl_divergence_f64.wgsl, fused_chi_squared_f64.wgsl,
matrix_correlation_f64.wgsl, linear_regression_f64.wgsl.

**Impact**: Information-theoretic validation primitives from neuralSpring
(originally for model evaluation) are consumed by wetSpring for cross-entropy
metrics and groundSpring for Anderson model fitness scoring.

### neuralSpring → airSpring: Linear Regression → Calibration

**What**: linear_regression_f64.wgsl adopted for trend analysis.

**Impact**: airSpring uses neuralSpring's GPU linear regression for ET₀ trend
analysis and crop coefficient calibration in the FAO56 pipeline.

### wetSpring → neuralSpring: Bioinformatics → Neuroevolution

**What**: smith_waterman_banded_f64.wgsl (sequence alignment),
gillespie_ssa_f64.wgsl (stochastic simulation).

**Impact**: Bioinformatics primitives from wetSpring are consumed by
neuralSpring's neuroevolution fitness evaluation — Smith-Waterman for
architecture similarity scoring, Gillespie SSA for stochastic search.

### wetSpring → airSpring + hotSpring: Fused Reduction

**What**: fused_map_reduce_f64.wgsl.

**Impact**: General-purpose fused map-reduce primitive from wetSpring,
adopted by airSpring for gridded hydrology reductions and hotSpring for
MD observable aggregation.

### airSpring → wetSpring: Hydrology → Bio-Ecosystem

**What**: hargreaves_et0_f64.wgsl, seasonal_pipeline.wgsl,
moving_window_f64.wgsl.

**Impact**: FAO56 evapotranspiration, seasonal crop pipeline, and moving-window
statistics from airSpring hydrology feed wetSpring's environmental parameter
estimation and temporal bio-signal smoothing.

### groundSpring → neuralSpring + hotSpring: Condensed Matter

**What**: anderson_lyapunov_f64.wgsl (Anderson localization Lyapunov exponent).

**Impact**: Disorder sweep validation from condensed matter physics, referenced
by neuralSpring for metalForge experiment validation and hotSpring for
transport property verification.

### groundSpring → ALL Springs: Chi-Squared Universal Test

**What**: chi_squared_f64.wgsl.

**Impact**: Universal goodness-of-fit test consumed by ALL springs for their
respective scientific validation domains.

### groundSpring → ALL Springs: f64 Shared-Memory Bug → PrecisionRoutingAdvice

**What**: V84-V85 discovered naga/SPIR-V f64 shared-memory reductions return
zeros on ALL tested GPUs.

**Timeline**: S128 (groundSpring V84-V85 absorption).

**Impact**: This led to toadStool's `PrecisionRoutingAdvice` enum
(`F64Native`, `F64NativeNoSharedMem`, `Df64Only`, `F32Only`) and the
`f64_shared_memory_reliable` flag on `GpuAdapterInfo`. ALL springs benefit
from correct precision routing based on actual GPU capabilities.

## toadStool S130 Implementation

### New Files
- `crates/server/src/coral_reef_client.rs` — CoralReefClient with
  capability-based discovery (env vars → XDG manifest → socket fallback)
- `crates/core/toadstool/src/cross_spring_provenance.rs` — Cross-spring
  provenance tracking with `SpringContribution`, `cross_spring_matrix()`,
  and `provenance_json()` for the `toadstool.provenance` JSON-RPC method

### Evolved Files
- `crates/server/src/pure_jsonrpc/handler/mod.rs` — `shader.compile.*`
  handlers evolved from stubs to real coralReef proxy with naga fallback
- `crates/core/config/src/ports.rs` — Added `SHADER_COMPILER` capability
- `crates/core/toadstool/src/semantic_methods.rs` — Added `toadstool.provenance`

### New Tests
- `crates/server/tests/shader_compile_proxy_tests.rs` — 12 tests for
  parameter validation, fallback, capabilities, provenance
- `crates/server/tests/shader_compile_benchmark_validation.rs` — 6 tests
  for cross-spring WGSL sample acceptance, response timing, throughput
- `crates/core/toadstool/tests/cross_spring_provenance_tests.rs` — 13 tests
  for provenance completeness, matrix structure, domain coverage

## Introspection API

Any primal can call `toadstool.provenance` to get the full cross-spring
flow matrix as JSON, enabling ecosystem-wide visibility into how patterns
propagate between springs.

## What This Does NOT Cover

- barraCuda provenance.rs expansion (barraCuda team)
- coralReef compiler improvements (coralReef team)
- Actual GPU dispatch benchmarks (barraCuda team)
- coralReef Expression::As blocker (coralReef team)
- DF64 NVK end-to-end verification (barraCuda team)

---
*Last Updated: March 7, 2026 — S130*
