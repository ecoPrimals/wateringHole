# barraCuda v0.3.11 — Sprint 22h: Deep Debt Evolution & Dependency Purge

**Date**: March 29, 2026
**Primal**: barraCuda
**Sprint**: 22h
**Tests**: 4,059 pass / 0 fail (cargo nextest)
**Gates**: fmt ✓ | clippy pedantic+nursery ✓ | doc ✓ | deny ✓

---

## Summary

Deep debt resolution sprint focused on dependency purge, shader idiomacy, code
consolidation, and pipeline wiring. Systematic execution against codebase audit
findings.

---

## Changes

### Subgroup Reduce Wired into ReduceScalarPipeline

`pipeline/reduce.rs::shader_for_device()` now implements three-tier reduction
shader selection:

| Tier | Shader | Condition | Barriers (RTX 3090) |
|------|--------|-----------|---------------------|
| 1 | `sum_reduce_subgroup_f64.wgsl` | `has_subgroups && f64_builtins` | 3 |
| 2 | DF64 f32-pair workgroup tree | `df64_workgroup_reduce` verified | 8 |
| 3 | Scalar f64 sequential | Always (fallback) | N/A |

Previously only tiers 2 and 3 existed. The subgroup shader was absorbed and
tested in Sprint 22g but not wired into the live reduction pipeline.

### `enable f64;` Removed from 47 WGSL Shaders

The `compile_shader_f64()` preamble injection handles the `enable f64;`
directive at compile time. Having it in source files was redundant and
inconsistent with newer absorbed shaders. All 47 remaining instances removed.
Only comment references remain (documenting the pattern).

### `num-traits` Dependency Eliminated

Replaced `num_traits::Float` with a local `CpuFloat` trait in
`shaders/precision/cpu.rs`. The trait provides `Default + Add + Sub + Mul +
mul_add` for `f32` and `f64` — the exact subset used by the 6 CPU reference
functions (elementwise_add, elementwise_mul, elementwise_fma, dot_product,
kahan_sum, reduce_sum). One fewer external dependency in `Cargo.toml`.

### LcgRng Consolidated to crate::rng

The `LcgRng` type was defined in `spectral::anderson` and imported by
`spectral::lanczos`. Moved to `crate::rng` (the centralized PRNG module) as a
public type with `const fn new()`. Both spectral modules now import from the
single source of truth. Added tests for uniform range and determinism.

### Hardcoded Log Prefixes Evolved

`coral_compiler/jsonrpc.rs::wgsl_to_spirv()` performs local naga WGSL→SPIR-V
conversion (no IPC). The `"coralReef: WGSL parse failed"` style log messages
were misleading — replaced with `"naga WGSL parse failed"` to accurately
describe the operation.

### const fn Promotions

- `lcg_step()`, `lcg_step_u32()` — pure arithmetic, always safe as const
- `LcgRng::new()`, `LcgRng::next_u64()` — wrapping arithmetic only

---

## Dependency Audit Summary

| Dependency | Action | Rationale |
|------------|--------|-----------|
| `num-traits` | **Removed** | Only used for `Float` trait on 6 functions; local `CpuFloat` trait is simpler |
| `rand` | **Kept** | Used in NN, evolution, thermostats — statistical quality required |
| `wgpu`/`naga`/`bytemuck` | **Kept** | Core GPU stack |
| `tokio`/`serde`/`serde_json` | **Kept** | IPC and async runtime |
| `rayon` | **Kept** | CPU data parallelism |
| `blake3` (pure) | **Kept** | Provenance hashing, no C assembly |
| `half` | **Kept** | IEEE f16 conversion |
| `bytes` | **Kept** | Zero-copy buffer patterns |
| `pollster` | **Kept** | Sync wgpu enumeration |
| `thiserror` | **Kept** | Standard error derives |

### Large File Assessment

| File | Lines | Decision |
|------|-------|----------|
| `coral_compiler/mod.rs` | 822 | **Keep** — ~435 production + ~387 comprehensive tests. Well-structured (client, helpers, submodules). |
| `spectral/anderson.rs` | 702 | **Extracted LcgRng** — remaining code is single coherent physics domain with tests already in separate file. |
| `tolerances.rs` | 731 | **Keep** — data file (tolerance constants). Splitting would fragment the registry. |
| `compute_graph.rs` | 688 | **Keep** — single pipeline abstraction. |

---

## Files Modified

| File | Change |
|------|--------|
| `pipeline/reduce.rs` | Added `SHADER_SUBGROUP_F64`, 3-tier `shader_for_device()` |
| `shaders/precision/cpu.rs` | `num_traits::Float` → local `CpuFloat` trait |
| `shaders/mod.rs` | Updated module doc comment |
| `rng.rs` | Added `LcgRng` type + tests + `const fn` promotions |
| `spectral/anderson.rs` | Removed local `LcgRng`, imports from `crate::rng` |
| `spectral/lanczos.rs` | Imports `LcgRng` from `crate::rng` instead of `anderson` |
| `device/coral_compiler/jsonrpc.rs` | Log prefix `"coralReef:"` → `"naga"` |
| `crates/barracuda/Cargo.toml` | Removed `num-traits` dependency |
| 47 `.wgsl` files | Removed `enable f64;` directives |

## Docs Updated

- `CHANGELOG.md` — Sprint 22h entry
- `STATUS.md` — dependency grade, test count, sprint note
- `WHATS_NEXT.md` — recently completed section
- `PURE_RUST_EVOLUTION.md` — dependency purge note
- `specs/REMAINING_WORK.md` — test count

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy --all-features -W pedantic -W nursery` | Zero new warnings in changed files |
| `cargo check` | Pass |
| `cargo nextest run -p barracuda` | 4,059 pass / 0 fail |

---

## What's Next for barraCuda

- PrecisionBrain → coralReef → SovereignDevice end-to-end integration test
- DF64 NVK end-to-end verification on hardware
- Test coverage push toward 90%
- Tensor core GEMM routing via toadStool VFIO
