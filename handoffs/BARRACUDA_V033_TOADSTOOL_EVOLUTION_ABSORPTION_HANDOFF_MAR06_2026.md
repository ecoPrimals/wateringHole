# barraCuda v0.3.3 → toadStool/barracuda Evolution Handoff

**Date**: March 6, 2026
**From**: barraCuda (standalone)
**To**: toadStool barracuda team
**Purpose**: Absorb barraCuda v0.3.3 evolution into toadStool's barracuda crate

---

## Overview

barraCuda v0.3.3 has completed a deep debt cycle that includes critical bug fixes,
spring absorption, and idiomatic Rust evolution. toadStool should absorb these changes
to stay synchronized. The path swap remains a single Cargo.toml line:

```toml
# toadStool's Cargo.toml — swap path:
barracuda = { path = "../../barraCuda/crates/barracuda" }
```

---

## Critical: Absorb These First

### 1. DF64 Hybrid Fallback Bug Fix (SILENT ZEROS)

**Severity**: Critical — produces incorrect results on Hybrid devices.

10 ops had `Err(_) => SHADER.to_string()` fallback that silently uses native f64 on
Hybrid devices where native f64 produces zeros.

**Files changed**: `covariance_f64_wgsl.rs`, `weighted_dot_f64.rs`, `hermite_f64_wgsl.rs`,
`digamma_f64_wgsl.rs`, `cosine_similarity_f64.rs`, `beta_f64_wgsl.rs`,
`bessel_i0_f64_wgsl.rs`, `bessel_j0_f64_wgsl.rs`, `bessel_j1_f64_wgsl.rs`,
`bessel_k0_f64_wgsl.rs`.

**Pattern**: `shader_for_device` returns `Result<&'static str>` instead of `&'static str`.
Call sites use `?` operator.

### 2. GPU f64 Computational Accuracy Probe

**File**: `device/test_pool.rs`

New `GPU_F64_COMPUTES: OnceLock<bool>` with `f64_computation_probe(&device)` that dispatches
`f64(3.0) * f64(2.0) + f64(1.0)` and verifies result is `7.0`.

`get_test_device_if_f64_gpu_available()` now requires: real hardware + `SHADER_F64` +
computation probe passes. This correctly gates 58 tests on software rasterizers.

**toadStool action**: This probe satisfies the `has_reliable_f64()` requirement from the
toadStool S97 handoff. Use the same three-gate pattern in toadStool's device selection.

### 3. Bounded GPU Poll Timeout

**File**: `device/wgpu_device/mod.rs`

`poll_safe()` and `submit_and_poll_inner()` use `PollType::Wait { timeout }` with configurable
`BARRACUDA_POLL_TIMEOUT_SECS` (default 120s). Timeout surfaces as `execution_failed` error.

**toadStool action**: Apply the same bounded timeout in any toadStool code that calls
`device.poll()`. Especially important for llvm-cov and CI environments.

### 4. Tokio Runtime Graceful Detection

**File**: `device/coral_compiler.rs`

`spawn_coral_compile` now uses `tokio::runtime::Handle::try_current()` before spawning.
If no runtime is active, it returns gracefully instead of panicking. Fixed ~113 test failures.

**toadStool action**: Apply the same pattern anywhere `tokio::spawn` is used outside
guaranteed async contexts.

---

## New Capabilities to Absorb

### 5. LSCFRK Gradient Flow Module

**New file**: `numerical/lscfrk.rs`
**Module registration**: `numerical/mod.rs` updated

Standalone Lie group integrator coefficients:
- `derive_lscfrk3(c2, c3)` — `const fn` coefficient derivation
- `LSCFRK3_W6`, `LSCFRK3_W7`, `LSCFRK4_CK` — static coefficient sets
- `FlowMeasurement` struct, `find_t0`, `find_w0`, `compute_w_function`

10 tests included. Zero lattice dependency — reusable for any ODE.

### 6. NautilusBrain Force Anomaly

**File**: `nautilus/brain.rs`
**Also**: `nautilus/shell.rs` (dynamic readout dimension)

- `force_anomaly(current, window) -> f64` — 10σ anomaly detector
- `NautilusBrain.recent_delta_h: Vec<f64>` — `#[serde(default)]` for backward compat
- `has_force_anomaly()` method
- Training targets extended from 3 to 4 heads (anomaly signal)
- `NautilusShell::evolve_generation()` uses `targets.first().map_or(3, Vec::len)` for readout dimension

### 7. GPU-Resident Reduction

**File**: `pipeline/reduce.rs`

New methods on `ReduceScalarPipeline`:
- `encode_reduce_to_buffer(encoder, input)` — encode without submit
- `readback_scalar()` — deferred readback

Enables GPU-resident CG solvers without CPU round-trips.

### 8. Sovereign Validation Harness

**New file**: `shaders/sovereign/validation_harness.rs`
**Registration**: `shaders/sovereign/mod.rs`

Pure-Rust test module that:
1. Traverses all `.wgsl` files
2. Preprocesses (strips `enable f64;`/`f16;`)
3. Runs through naga parser → sovereign optimizer → validator
4. Classifies results (pass, needs-preprocessing, parse-error)

No GPU required. Catches shader regressions at test time.

---

## Idiomatic Rust Evolution

These are small but pervasive changes that improve code quality:

| File(s) | Change |
|---------|--------|
| `ops/lattice/cpu_complex.rs` | `#[allow]` → `#[expect]` with reason |
| `nn/config.rs`, `optimize/eval_record.rs`, `device/autotune.rs`, `device/pipeline_cache.rs` | Manual `impl Default` → `#[derive(Default)]` |
| `device/wgpu_device/mod.rs` | `map_or(true, ...)` → `is_none_or(...)` |
| `esn_v2/model.rs` | Redundant closure → `Tensor::to_vec` method reference |
| `ops/peak_detect_f64.rs` | `map_or(true, ...)` → `is_none_or(...)` |
| Various (5 files) | `Vec::new()` + `push` → iterator `.collect()` |
| Various (6 files) | `match Option` → combinators |

---

## Test Infrastructure

| Change | Location | Impact |
|--------|----------|--------|
| `unified_hardware` test: "unknown" → "gpu"/"npu" | `unified_hardware/mod.rs` | 1 test fixed |
| HMM shader assertion updated | `ops/bio/hmm.rs` | 1 test fixed |
| autocorrelation: bare device → f64-gated pool | `ops/autocorrelation_f64_wgsl.rs` | 2 tests fixed |

---

## What toadStool Should Know

### NVK SPIR-V Exclusion
NVK (Nouveau Vulkan) is excluded from SPIR-V passthrough paths. NVK claims Vulkan 1.3
but lacks reliable f64 SPIR-V support on Volta. barraCuda routes NVK through WGSL-only
paths. This is documented in `BREAKING_CHANGES.md`.

### wgpu 28 API
`device.poll()` returns `Result<PollStatus, PollError>`, not `PollStatus` directly.
Match on the `Result` and access `.is_queue_empty()` on the `PollStatus` variant.

### coralReef Phase 9
coralReef has completed Phase 9. barraCuda's `coral_compiler.rs` uses opportunistic
compilation via IPC. The coral client gracefully handles missing runtimes.

### Remaining P0 Items for barraCuda
1. Dedicated DF64 shaders for covariance + weighted_dot (auto-rewrite works but hand-written is more robust)
2. DF64 NVK end-to-end hardware verification (Yukawa kernels)
3. RHMC multi-shift CG absorption from hotSpring

---

## Verification

All quality gates green after these changes:

```
cargo fmt --all -- --check           ✓ clean
cargo clippy -p barracuda -- -W clippy::pedantic   ✓ zero library warnings
cargo check -p barracuda             ✓ compiles
cargo test -p barracuda --lib        ✓ 3,014 passed, 0 failed, 13 ignored
```

---

## Absorption Path

1. `git pull` or update path dependency to barraCuda HEAD
2. Verify `cargo check` passes (should be zero-change for toadStool consumers)
3. Run `cargo test` — expect 3,014+ passes
4. If toadStool has its own f64 gating: adopt the three-gate pattern
5. If toadStool calls `device.poll()` directly: apply bounded timeout pattern
