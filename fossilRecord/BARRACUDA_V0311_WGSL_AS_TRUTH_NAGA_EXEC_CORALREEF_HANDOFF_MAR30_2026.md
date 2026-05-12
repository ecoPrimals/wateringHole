# barraCuda v0.3.11 — WGSL-as-Truth + NagaExecutor + coralReef Sovereign Compilation Handoff

**Date**: March 30, 2026
**Sprint**: 24
**Author**: barraCuda team (AI-assisted)
**Status**: Complete — all quality gates green

---

## Summary

Major test architecture restructure + new CPU shader interpreter + coralReef sovereign compilation IPC contract. The thesis: **the WGSL shader IS the math** — validate it on CPU, not by duplicating logic in Rust.

## What Changed

### Phase 1: Test Architecture Restructure (337 files)

- **Migrated** ~337 GPU op test files from `get_test_device_if_gpu_available()` (which skips on CI/llvmpipe) to `get_test_device()` (which always provides a CPU device)
- **2,770 tests now run on CPU/llvmpipe** — was ~0 coverage for GPU-gated ops on CI
- **17 modules correctly re-gated** to GPU-only (`adagrad`, `expand`, `filter`, `gather_nd`, `iou_loss`, `matmul`, `md/integrators/rk4`, `md/integrators/velocity_verlet`, `mosaic`, `nadam`, `perceptual_loss`, `rmsprop`, `scatter_nd`, `sgd`, `sparse_matmul_quantized`, `sparse_matvec_wgsl`, `unique`) — these require GPU-specific features (atomics, complex memory patterns) not supported by llvmpipe
- **New semantic aliases**: `get_test_device_for_shader_validation()`, `get_test_device_for_f64_shader_validation()` with prelude exports `test_shader_device()`, `test_f64_shader_device()`

### Phase 2: NagaExecutor — CPU Shader Interpreter (new crate)

New crate: `barracuda-naga-exec` (pure Rust, `#![forbid(unsafe_code)]`)

Parses WGSL via naga, interprets the compute entry point on CPU. No GPU, no Vulkan, no Mesa.

**Supported IR subset:**
- Types: f32, f64, u32, i32, bool, vec2/3/4, arrays, structs, atomic<T>
- Expressions: literals, binary/unary ops, all math builtins, casts, access, compose, splat, select
- Statements: block, store, emit, return, if/else, loop, break, continue, barriers, atomics
- Globals: `var<storage>`, `var<uniform>`, `var<workgroup>`
- Builtins: `global_invocation_id`, `local_invocation_id`, `local_invocation_index`
- Barriers: `workgroupBarrier()` via multi-phase execution (correct for standard reduction patterns)
- Atomics: `atomicAdd`, `atomicMax`, `atomicMin`, `atomicLoad`, `atomicStore`, `Exchange`

**Key advantage over llvmpipe:** Native f64 (llvmpipe lacks f64 transcendentals), 10-100x faster for small workloads, deterministic (no driver variance), zero external dependencies.

16 tests including f64 transcendentals, shared memory reverse, atomic accumulation.

### Phase 3: coralReef Sovereign Compilation IPC Contract

**barraCuda-side changes** (coralReef team implements the server side):

- **10 new wire types** in `coral_compiler/types.rs`: `CompileCpuRequest`, `CompileCpuResponse`, `ExecuteCpuRequest`, `ExecuteCpuResponse`, `ValidateRequest`, `ValidateResponse`, `BufferBinding`, `ExpectedBinding`, `ValidationTolerance`, `ValidationMismatch`
- **5 new methods** on `CoralCompiler`: `supports_cpu_execution()`, `supports_validation()`, `compile_cpu()`, `execute_cpu()`, `validate_shader()`
- **Capability discovery** extended: `discover_cpu_shader_compiler()`, `discover_shader_validator()`
- **`ShaderValidationBackend` enum**: CoralReef → Llvmpipe fallback chain (NagaExecutor will be inserted as middle layer)
- **IPC methods**: `shader.compile.cpu`, `shader.execute.cpu`, `shader.validate`

### Wiring

- `assert_shader_math!` macro — validate f32 shader math in one line, no GPU
- `assert_shader_math_f64!` macro — validate f64 shader math, no GPU
- `barracuda-naga-exec` is a dev-dependency of `barracuda`

## 4-Layer Validation Architecture

| Layer | Backend | Precision | Speed | Dependencies |
|-------|---------|-----------|-------|--------------|
| 1 | llvmpipe (wgpu) | f32 | Slow | Mesa |
| 2 | NagaExecutor | f32+f64 | Fast | None |
| 3 | coralReef CPU | f32+f64 | Fast | coralReef primal |
| 4 | Real GPU | f32+f64 | Varies | GPU hardware |

CI runs layers 1+2 always. Layer 3 when coralReef is available. Layer 4 on hardware.

## Quality Gates

| Gate | Result |
|------|--------|
| `cargo fmt --all --check` | PASS |
| `cargo clippy -p barracuda -- -W clippy::pedantic` | PASS |
| `cargo clippy -p barracuda-naga-exec -- -W clippy::pedantic` | PASS |
| `cargo doc --no-deps` | PASS |
| `cargo test -p barracuda-naga-exec` | 16 passed, 0 failed |
| `cargo test -p barracuda --lib` | 2,770 passed, 0 failed, 13 ignored |
| Total | **2,786 tests, 0 failures** |

## Files Changed (this sprint)

**New crate:**
- `crates/barracuda-naga-exec/Cargo.toml`
- `crates/barracuda-naga-exec/src/lib.rs`
- `crates/barracuda-naga-exec/src/error.rs`
- `crates/barracuda-naga-exec/src/value.rs`
- `crates/barracuda-naga-exec/src/executor.rs`

**Modified (barraCuda):**
- `Cargo.toml` (workspace members)
- `crates/barracuda/Cargo.toml` (dev-dep)
- `crates/barracuda/src/device/test_harness.rs` (ShaderValidationBackend, sovereign validator)
- `crates/barracuda/src/device/test_pool/mod.rs` (semantic aliases)
- `crates/barracuda/src/device/test_pool/prelude.rs` (exports, macros)
- `crates/barracuda/src/device/coral_compiler/mod.rs` (5 new methods, global_coral())
- `crates/barracuda/src/device/coral_compiler/types.rs` (10 new wire types)
- `crates/barracuda/src/device/coral_compiler/discovery.rs` (CPU/validate discovery)
- ~337 op test files (migration to CPU device)

## coralReef Team Action Items

A blurb was provided to the parallel coralReef team in the prior session. Key deliverables:

1. **`shader.execute.cpu`** — Accept WGSL + input buffers, return output buffers (via NagaExecutor or Cranelift)
2. **`shader.validate`** — Accept WGSL + inputs + expected outputs + tolerances, return validation report
3. **`shader.compile.cpu`** — Compile WGSL to native CPU binary (x86_64/aarch64 via Cranelift)
4. Update capability manifest to advertise `shader.compile.cpu`, `shader.execute.cpu`, `shader.validate`

barraCuda's discovery will automatically detect these when they land.

## plasmidBin

`infra/plasmidBin/coralreef/metadata.toml` updated with Phase 3 planned capabilities (commented, for coralReef team reference).

## What's Next

- Wire NagaExecutor as Layer 2 in the `ShaderValidationBackend` fallback chain
- Deprecate redundant CPU reference functions (`shannon_entropy_cpu`, `hill_dose_response_cpu`, etc.)
- Cross-validate: any two layers agreeing = high confidence
- Phase 4+: coralReef as Rust compiler, Rust-to-GPU compilation (long horizon)
