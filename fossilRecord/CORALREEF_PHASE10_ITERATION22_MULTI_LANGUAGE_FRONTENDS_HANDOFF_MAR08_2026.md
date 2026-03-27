# coralReef Phase 10 — Iteration 22: Multi-Language Frontends & Fixture Reorganization

**Date**: March 8, 2026
**Author**: coralReef compiler team
**Iteration**: 22

---

## Summary

coralReef now accepts three shader input languages: WGSL, SPIR-V, and GLSL 450
compute shaders. The test fixture directory has been reorganized to separate
compiler-owned test shaders from pinned spring corpus snapshots.

## Changes

### 1. Fixture Reorganization

- **Before**: 107 `.wgsl` files flat in `tests/fixtures/wgsl/`
- **After**: 21 compiler-owned fixtures in `fixtures/wgsl/` (referenced by
  `codegen_coverage.rs`), 86 spring corpus snapshots in `fixtures/wgsl/corpus/`
  (referenced by `wgsl_corpus.rs`)
- `wgsl_corpus.rs` macro updated: `include_str!(concat!("fixtures/wgsl/corpus/", $file))`
- No changes to `codegen_coverage.rs` paths

### 2. GLSL 450 Compute Frontend

- `naga` dependency: added `glsl-in` feature
- `parse_glsl()` in `codegen/naga_translate/mod.rs` — uses `naga::front::glsl::Frontend`
  with `ShaderStage::Compute`
- `Frontend` trait: new `compile_glsl()` method (alongside existing `compile_wgsl`
  and `compile_spirv`)
- Public API: `compile_glsl()`, `compile_glsl_with()`, `compile_glsl_full()`,
  `compile_glsl_full_with()` in `lib.rs`

### 3. GLSL Test Corpus (5 fixtures)

All 5 compile to SM70 SASS:

| Fixture | Exercises |
|---------|-----------|
| `basic_alu.comp` | Integer + float ALU, FMA, type conversions, bitwise |
| `control_flow.comp` | Loops, branches, barriers, break, shared memory |
| `shared_reduction.comp` | Workgroup reduction via shared memory |
| `transcendentals.comp` | exp, log, sin, cos, sqrt, pow, abs, min, max, clamp, floor, ceil |
| `buffer_rw.comp` | SSBO read/write, struct layout, vec3/vec4, early return |

### 4. SPIR-V Roundtrip Tests

WGSL → naga → SPIR-V → `compile()` roundtrip — no binary fixtures needed.

| Status | Count | Details |
|--------|-------|---------|
| Passing | 4 | alu_float_fma, alu_int_signed, data_vectors, vv_half_kick |
| Ignored | 6 | 2 Discriminant expression, 4 non-literal constant initializer |

SPIR-V frontend gaps documented:
- `Discriminant` expression not yet translated (affects switch-like patterns)
- Non-literal constant initializers not yet supported (affects struct init patterns)

## Test Counts

| Metric | Before (It. 21) | After (It. 22) | Delta |
|--------|-----------------|-----------------|-------|
| Passing | 1174 | 1189 | +15 |
| Ignored | 30 | 36 | +6 |
| GLSL tests | 0 | 5 | +5 |
| SPIR-V roundtrip | 0 | 10 | +10 |

## What Springs Should Know

- **barraCuda**: Can now send GLSL 450 compute shaders to coralReef via
  `compile_glsl()`. No df64 preamble injection for GLSL — barraCuda must
  include all needed functions inline.
- **All springs**: WGSL corpus fixtures now live in `fixtures/wgsl/corpus/`.
  If importing new shaders for testing, place them there.
- **SPIR-V path**: 4/10 roundtrip tests pass. Non-literal constant initializer
  and Discriminant expression are the two main gaps — future translator work.

## Files Changed

- `crates/coral-reef/Cargo.toml` — `glsl-in` naga feature
- `crates/coral-reef/src/codegen/naga_translate/mod.rs` — `parse_glsl()`
- `crates/coral-reef/src/frontend.rs` — `compile_glsl()` on `Frontend` trait
- `crates/coral-reef/src/lib.rs` — public `compile_glsl*()` API
- `crates/coral-reef/tests/wgsl_corpus.rs` — corpus/ path update
- `crates/coral-reef/tests/glsl_corpus.rs` — new GLSL test harness
- `crates/coral-reef/tests/spirv_roundtrip.rs` — new SPIR-V roundtrip test
- `crates/coral-reef/tests/fixtures/glsl/*.comp` — 5 new GLSL fixtures
- `crates/coral-reef/tests/fixtures/wgsl/corpus/` — 86 files moved here
- `STATUS.md`, `EVOLUTION.md`, `ABSORPTION.md`, `README.md` — updated
