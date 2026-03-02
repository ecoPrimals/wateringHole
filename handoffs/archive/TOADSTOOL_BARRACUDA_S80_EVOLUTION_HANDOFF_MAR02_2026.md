# ToadStool/BarraCUDA Team — S80 Evolution Handoff

**Date**: March 2, 2026
**From**: ToadStool S80 (sessions 68–80)
**To**: toadStool/barracuda team (continued evolution)
**License**: AGPL-3.0-or-later

---

## Executive Summary

BarraCUDA has evolved from a GPU compute library to a comprehensive scientific middleware platform. This handoff documents the current state, architectural patterns, and recommended evolution paths for the team continuing this work.

---

## Part 1: Current Architecture (S80)

### Shader-First Architecture (844 WGSL Shaders)

Every parallelizable math operation originates as WGSL. BarraCUDA does not care about hardware — ToadStool routes to the best substrate at runtime.

- **Zero orphans** — every WGSL file wired to Rust dispatch
- **Zero f32-only** — all f64 canonical, with `LazyLock` downcast to f32/f16
- **37 DF64** — double-float f32-pair arithmetic for consumer GPUs
- **15 folding** — protein structure prediction pipeline
- **28 transcendental polyfills** — exp, log, pow, sin, cos, etc. via pure WGSL

### Dual-Layer Universal Precision

```
Layer 1 (source): op_preamble — op_add/op_mul/Scalar alias → all precisions
Layer 2 (compiler): naga-guided df64_rewrite — infix → bridge functions → DF64
```

- `compile_shader_universal()` — one shader → f16/f32/f64/df64
- `compile_op_shader()` — abstract ops at ALL precisions without transformation
- `compile_shader_f64()` — auto-injects polyfills
- `compile_shader_df64()` — auto-injects DF64 core + transcendentals
- `downcast_f64_to_f32/f16/df64()` — text-transform with sentinel protection

### ComputeDispatch Builder (95/250 migrated)

Fluent pipeline creation: ~80 lines of BGL/BG/pipeline boilerplate → ~5 lines.

```rust
ComputeDispatch::new(&device, &shader_source)
    .storage_read(0, &input_buf)
    .storage_rw(1, &output_buf)
    .uniform(2, &params_buf)
    .workgroups(wg_x, 1, 1)
    .dispatch()
    .await?;
```

**~155 legacy ops remaining** — each migration is ~75 lines removed per op.

### BatchedEncoder (S80)

Fuses multiple GPU dispatches into a single `CommandEncoder` → single `queue.submit()`.

```rust
let mut encoder = BatchedEncoder::new(&device)?;
encoder.add_pass()
    .shader(SHADER_SOURCE)
    .storage_read(0, &buf_a)
    .storage_rw(1, &buf_b)
    .workgroups(wg_x, 1, 1)
    .build()?;
encoder.add_pass()
    .shader(SHADER_SOURCE_2)
    .storage_read(0, &buf_b)
    .storage_rw(1, &buf_c)
    .workgroups(wg_x, 1, 1)
    .build()?;
encoder.submit(&device.queue);
```

**Used by**: `fused_mlp`, available for MLP/Transformer/MD multi-step pipelines.

### Sovereign Compiler

naga-IR optimizer: FMA fusion → dead expression elimination → df64 infix rewrite → SPIR-V passthrough. Bypasses NAK entirely on NVK.

### Fp64Strategy

Auto-selects between Native f64 (compute-class GPUs) and Hybrid DF64 (consumer GPUs). Runtime probe via `basic_f64` compile test.

---

## Part 2: New Modules (S79–S80)

### barracuda::nautilus (7 files, 22 tests)

Standalone evolutionary reservoir computing absorbed from bingoCube.

| Component | Key Type | Purpose |
|-----------|----------|---------|
| Board | `Board`, `BoardConfig`, `ReservoirInput` | L×L grid, column-range constraints, BLAKE3 projection |
| Evolution | `SelectionMethod`, `EvolutionConfig` | Elitism/Tournament/Roulette, column-swap crossover |
| Population | `Population`, `FitnessRecord` | Board ensembles, Pearson fitness |
| Readout | `LinearReadout` | Ridge regression |
| Shell | `NautilusShell`, `GenerationRecord`, `InstanceId` | Layered history, lineage, merge |
| Brain | `NautilusBrain`, `DriftMonitor` | High-level API: observe, train, predict, screen, edges |

### barracuda::nn::fused_mlp

MLP forward pass via BatchedEncoder. Supports linear layers + ReLU activation. Single `queue.submit()` across all layers.

### barracuda::pipeline::StatefulPipeline

Generic `StatefulPipeline<S>` + `PipelineStage<S>` trait for day-over-day state tracking. `WaterBalanceState` as concrete example.

### barracuda::optimize::batched_nelder_mead_gpu

N independent Nelder-Mead optimizations in parallel on GPU. Uses batched simplex shader entry points.

### ESN MultiHeadEsn (S79)

36-head ESN with 6 `HeadGroup` variants. `head_disagreement()` uncertainty metric. `ExportedWeights` aligned with hotSpring conventions.

### GpuDriverProfile Workarounds (S80)

`NvkSinCosF64Imprecise` workaround: Taylor-series preamble for NVK. Injected via `for_driver_profile()` shader compilation path. `asin`/`acos` protected.

---

## Part 3: Recommended Evolution Paths

### P0: ComputeDispatch Migration (incremental)

~155 legacy ops. Each migration is mechanical — find manual BGL/BG/pipeline code, replace with `ComputeDispatch::new()`. Target: 10-15 ops per session.

**Priority order**: Most-used ops first (matmul, conv2d, attention), then long-tail.

### P1: BatchedEncoder Adoption

Expand `BatchedEncoder` to more multi-op pipelines:
- MD force → position update → observable measurement
- Lattice QCD: plaquette → force → leapfrog → accept/reject
- Transformer: attention → FFN → layernorm

### P2: DF64 as Default Path

Make `df64_rewrite` the default precision strategy for consumer GPUs (1:64 FP64:FP32). Currently DF64 activates only when `Fp64Strategy::Hybrid` is selected. Consumer GPUs should default to DF64 with native f64 reserved for reductions.

### P3: metalForge Stage/Pipeline Topology

Design `Stage<In,Out>`, `Chain`, `FanIn`, `FanOut`, `Graph` structures for multi-kernel compute pipelines. This is the next architectural layer above `BatchedEncoder` and `StatefulPipeline`.

### P4: Test Coverage → 90%

41.86% → 90% target. Major gaps in barracuda GPU ops and neuromorphic drivers. Most coverage gains will come from:
- GPU op unit tests (many ops have shaders but minimal Rust-side testing)
- Edge cases in ComputeDispatch-migrated ops
- Nautilus module (currently 22 tests, could be expanded)

### P5: Physics Ops (Deferred)

- Pseudofermion HMC (477 lines, wateringHole V69)
- Omelyan integrator (wateringHole V69)
- Richards PDE with 12 USDA textures (wateringHole V69)

---

## Part 4: Patterns & Conventions

### Adding a New GPU Op

1. Write WGSL shader in `src/shaders/` (f64 canonical)
2. Create `LazyLock<String>` for f32 downcast in Rust module
3. Use `ComputeDispatch::new()` for pipeline creation
4. Add CPU reference implementation gated behind `#[cfg(test)]`
5. Add tests comparing GPU output to CPU reference

### Shader Compilation

```rust
use barracuda::shaders::precision::compile_shader_f64;

let compiled = compile_shader_f64(WGSL_SOURCE, &device_caps)?;
```

For DF64:
```rust
use barracuda::shaders::precision::compile_shader_df64;

let compiled = compile_shader_df64(WGSL_SOURCE, &device_caps)?;
```

### Error Handling

- All errors via `BarracudaError` (thiserror)
- No blind `.unwrap()` — use `.ok_or_else()` or `.unwrap_or_default()`
- GPU device loss handled via `catch_unwind` + `is_lost()` check

### Quality Gates (must pass before commit)

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo doc --no-deps --workspace
cargo test -p barracuda --lib
```

---

## Part 5: Key Files

| Area | Files |
|------|-------|
| Device management | `src/device/wgpu_device/`, `src/device/unified.rs`, `src/device/capabilities/` |
| Shader precision | `src/shaders/precision/mod.rs`, `polyfill.rs`, `compiler.rs` |
| ComputeDispatch | `src/dispatch/config.rs` |
| BatchedEncoder | `src/device/batched_encoder.rs` |
| Nautilus | `src/nautilus/` (board, evolution, population, readout, shell, brain) |
| Driver workarounds | `src/device/driver_profile/workarounds.rs` |
| F64 polyfills | `src/shaders/math/math_f64.wgsl` (28 functions) |
| DF64 core | `src/shaders/math/df64_core.wgsl`, `df64_transcendentals.wgsl` |
| Sovereign compiler | `src/shaders/precision/compiler.rs` |
| Op modules | `src/ops/` (200+ ops across linalg, bio, MD, special, etc.) |

---

## Metrics Snapshot (S80)

| Metric | Value |
|--------|-------|
| WGSL shaders | 844 |
| DF64 shaders | 37 |
| Folding shaders | 15 |
| Transcendental polyfills | 28 |
| ComputeDispatch ops | 95/250 |
| barracuda lib tests | 2,800+ |
| Workspace tests | 5,500+ |
| Unsafe blocks | 2 (SPIRV cache, aligned alloc) |
| Clippy warnings | 0 |
| Doc warnings | 0 |
| God files remaining | 0 (all < 1000 lines) |

---

*This handoff captures the current state for team continuity. The codebase is clean, all quality gates pass, and the architecture supports incremental evolution.*
