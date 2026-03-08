# barraCuda v0.3.3 — Deep Debt Evolution Sprint Handoff

**Date**: March 8, 2026
**From**: barraCuda
**To**: All Springs, toadStool, coralReef

---

## Summary

This sprint resolves the P0 f64 shared-memory routing gap across all reduce
ops, extracts hardcoded primal identity to a single constant, and evolves
`SpringDomain` from a hardcoded enum to a runtime-extensible capability type.

## Changes

### P0: Fp64Strategy Routing — All f64 Reduce Ops

**Problem**: `SumReduceF64` and `VarianceReduceF64` correctly routed through
`shader_for_device()` to select DF64 shaders on Hybrid hardware (Ada Lovelace
RTX 4070, NVK). Four reduce ops and `ReduceScalarPipeline` did NOT, producing
zeros on Hybrid GPUs when using `var<workgroup>` f64.

**Fixed ops**:
- `ProdReduceF64` — product and log-product reduction
- `NormReduceF64` — L1, L2, Linf, Frobenius, p-norm reduction
- `FusedMapReduceF64` — configurable map+reduce (Shannon, Simpson, etc.)
- `ReduceScalarPipeline` — two-pass scalar pipeline (also fixed `compile_shader` bypass)

**New shaders**:
- `shaders/reduce/prod_reduce_df64.wgsl`
- `shaders/reduce/norm_reduce_df64.wgsl`
- `shaders/reduce/fused_map_reduce_df64.wgsl`

All use `shared_hi`/`shared_lo` f32-pair workgroup memory with `df64_add`/`df64_mul`.

### P1: PRIMAL_NAME Constant

`const PRIMAL_NAME: &str = "barraCuda"` in `barracuda-core/src/lib.rs` replaces
5 scattered string literals across `bin/barracuda.rs`, `rpc.rs`, `lib.rs`,
`ipc/methods.rs`. Self-knowledge in one definition.

### P2: SpringDomain Capability Evolution

`SpringDomain` evolved from a hardcoded 6-variant enum to
`struct SpringDomain(pub &'static str)`. barraCuda no longer embeds
compile-time knowledge of other primals in its type system. Associated
constants (`HOT_SPRING`, `WET_SPRING`, etc.) preserve ergonomics.

New domains are runtime-extensible: `SpringDomain("myNewDomain")`.

## Impact on Springs

- **All springs using f64 reduce ops**: Product, norm, and fused-map-reduce
  operations now correctly produce non-zero results on Hybrid hardware.
- **Springs referencing `SpringDomain`**: Update `SpringDomain::HotSpring` to
  `SpringDomain::HOT_SPRING` (associated constants instead of enum variants).

## Phase 2: Systematic f64 Pipeline Evolution (March 8, 2026)

### Critical: 14 f64 Ops — Silent Data Corruption Fix

**Problem**: 14 ops upload real f64 data (`bytemuck::cast_slice(x)` where x is
`&[f64]`) but compile the shader via `compile_shader()` or `GLOBAL_CACHE` which
always downcasts f64→f32. On f64-capable GPUs, the 4-byte f32 shader
misinterprets 8-byte f64 data — silent data corruption.

**Fixed ops** (2 direct callers → `compile_shader_f64()`):
- `TranseScoreF64` — TransE knowledge graph scoring
- `TriangularSolve::f64` — triangular system solver (both solve + transpose)

**Fixed ops** (12 GLOBAL_CACHE callers → `create_f64_data_pipeline()`):
- `VarianceF64Wgsl` — fused Welford mean+variance (3 dispatch methods)
- `CorrelationF64Wgsl` — Pearson correlation (2 dispatch methods)
- `CovarianceF64Wgsl` — covariance with ddof
- `HermiteF64Wgsl` — Hermite polynomial evaluation
- `BesselI0F64`, `BesselJ0F64`, `BesselJ1F64`, `BesselK0F64` — Bessel functions
- `BetaF64Wgsl` — Beta function
- `DigammaF64Wgsl` — Digamma (psi) function
- `CosineSimilarityF64` — all-pairs cosine similarity
- `WeightedDotF64` — weighted dot product

### Pipeline Cache f64-Native Path

New `get_or_create_pipeline_f64_native()` method with separate `shaders_f64`
and `pipelines_f64` cache maps. `create_f64_data_pipeline()` auto-selects
native or downcast path based on `SHADER_F64` device capability.

### Zero-Copy Evolution

- `CpuTensorStorageSimple`: `Vec<u8>` → `Bytes` — `read_to_cpu()` is now
  ref-count bump, not full buffer clone
- `CosineSimilarityF64::similarity()`: eliminated 2× `to_vec()` via flat dispatch

### Pipeline Cache Hot-Path Optimization

- `DeviceFingerprint`: `format!("{:?}:")` → `std::mem::discriminant()` hashing
- `PipelineKey`: `String` entry point → `u64` hash

### Hardcoding Audit

- Legacy discovery filename: `coralreef-core.json` → `shader-compiler.json`
- Zero hardcoded primal names, ports, or URLs in production code
- `compile_shader()` doc corrected to describe f64-canonical always-downcast design

## Impact on Springs

- **All springs using f64 special functions** (Bessel, Hermite, Beta, Digamma):
  Now produce correct results on f64-capable GPUs instead of silent garbage.
- **Springs using cosine similarity, covariance, correlation in f64**: Same fix.
- **CPU-side consumers**: `read_to_cpu()` is now zero-copy; no API change needed.

## Validation

- `cargo fmt --check`: PASS (0 diffs)
- `cargo clippy --all-targets`: PASS (0 warnings)
- `cargo test -p barracuda --lib`: 3,091 passed, 1 flaky (GPU contention), 13 ignored
- `cargo test -p barracuda-core --lib`: 50 passed, 0 failed
- Zero `unsafe` blocks, zero TODO/FIXME/HACK in codebase

## Pin

barraCuda HEAD at time of handoff.
