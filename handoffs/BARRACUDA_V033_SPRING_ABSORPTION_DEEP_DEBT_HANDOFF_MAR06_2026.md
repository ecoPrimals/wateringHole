# barraCuda v0.3.3 — Spring Absorption + Deep Debt Evolution Handoff

**Date**: March 6, 2026
**From**: barraCuda
**To**: All Springs, toadStool, coralReef
**Session**: Deep audit → deep debt resolution → spring absorption → idiomatic Rust evolution

---

## Summary

barraCuda absorbed capabilities from hotSpring, validated alignment with wetSpring/airSpring/
groundSpring/toadStool handoffs, resolved deep testing debt, and evolved to modern idiomatic
Rust. 3,014 library tests pass with zero failures.

---

## What Changed

### 1. DF64 Hybrid Fallback Bug Fixed (10 ops)

**Root cause**: On `Fp64Strategy::Hybrid` devices, if `rewrite_f64_infix_full()` failed, ops
silently fell back to the native f64 shader — which produces zeros on Hybrid devices.

**Fix**: All 10 ops now return `BarracudaError::ShaderCompilation` instead of silent zeros.

| Op | File |
|----|------|
| covariance | `ops/covariance_f64_wgsl.rs` |
| weighted_dot | `ops/weighted_dot_f64.rs` |
| hermite | `ops/hermite_f64_wgsl.rs` |
| digamma | `ops/digamma_f64_wgsl.rs` |
| cosine_similarity | `ops/cosine_similarity_f64.rs` |
| beta | `ops/beta_f64_wgsl.rs` |
| bessel_i0 | `ops/bessel_i0_f64_wgsl.rs` |
| bessel_j0 | `ops/bessel_j0_f64_wgsl.rs` |
| bessel_j1 | `ops/bessel_j1_f64_wgsl.rs` |
| bessel_k0 | `ops/bessel_k0_f64_wgsl.rs` |

**Impact for Springs**: If you use these ops on Hybrid devices, you'll now get a clear error
instead of garbage. Variance and correlation already had dedicated DF64 shaders and were not
affected.

### 2. GPU f64 Computational Accuracy Probe

`get_test_device_if_f64_gpu_available()` now requires three conditions:
1. Real hardware (not CPU/software)
2. `SHADER_F64` feature flag
3. **Computational probe**: dispatches `f64(3.0) * f64(2.0) + f64(1.0)` and verifies result is `7.0`

This gates 58 tests that were failing on software rasterizers (llvmpipe/lavapipe) which claim
`SHADER_F64` but produce incorrect results.

**Impact for toadStool**: This replaces `has_reliable_f64()` with a concrete computation probe.
toadStool can use the same pattern for its own f64 gating.

### 3. Bounded GPU Poll Timeout

`poll_safe()` and `submit_and_poll_inner()` now use `PollType::Wait { timeout }` with a
configurable timeout (default 120s, env `BARRACUDA_POLL_TIMEOUT_SECS`).

**Impact for llvm-cov**: The GPU hang under coverage instrumentation is mitigated. Timeouts
surface as `BarracudaError::execution_failed` instead of indefinite hangs.

### 4. LSCFRK Gradient Flow Integrators (absorbed from hotSpring)

New module: `numerical/lscfrk.rs`

| Item | Description |
|------|-------------|
| `derive_lscfrk3(c2, c3)` | `const fn` — algebraic derivation of all 3-stage 3rd-order 2N-storage coefficients |
| `LSCFRK3_W6` | Lüscher (JHEP 2010) — standard lattice QCD |
| `LSCFRK3_W7` | Bazavov & Chuna (arXiv:2101.05320) — ~2× more efficient for w₀ |
| `LSCFRK4_CK` | Carpenter-Kennedy 4th-order, 5-stage |
| `find_t0(measurements)` | Linear interpolation for t²⟨E(t)⟩ = 0.3 |
| `find_w0(measurements)` | W(t) = t d/dt[t²E(t)] = 0.3 → √t_cross |
| `compute_w_function(measurements)` | (t_mid, W) pairs for plotting |

All are **standalone** — no lattice or gauge-field dependency. Any ODE on a Lie group can
reuse these coefficients.

**Impact for hotSpring**: Import from barraCuda instead of maintaining local copies:
```rust
use barracuda::numerical::{LSCFRK3_W7, find_t0, find_w0};
```

### 5. NautilusBrain Force Anomaly Detection (absorbed from hotSpring MdBrain)

| Addition | Description |
|----------|-------------|
| `force_anomaly(current, window)` | Domain-agnostic 10σ energy anomaly detector |
| `recent_delta_h: Vec<f64>` | Rolling window tracked via `observe()` |
| `has_force_anomaly()` | Public API for anomaly checking |
| 4th training head | Target vector extended to include anomaly signal |
| `NautilusShell::evolve_generation()` | Dynamic readout dimension (was hardcoded to 3) |

`#[serde(default)]` on `recent_delta_h` ensures backward-compatible deserialization.

### 6. GPU-Resident Reduction Pipeline

New methods on `ReduceScalarPipeline`:

| Method | Description |
|--------|-------------|
| `encode_reduce_to_buffer(encoder, input)` | Encode two-pass reduction without submit/readback |
| `readback_scalar()` | Deferred readback after separate submit |

**Impact for hotSpring CG solver**: Enables GPU-resident conjugate gradient without CPU
round-trips between residual reductions.

### 7. Idiomatic Rust Evolution

| Pattern | Count | Change |
|---------|-------|--------|
| `#[allow(clippy::)]` → `#[expect(clippy::)]` | 1 | Rust 2024 idiom |
| Manual `impl Default` → `#[derive(Default)]` | 4 | NetworkConfig, EvaluationCache, AutoTuner, PipelineCache |
| `map_or(true, \|x\| ...)` → `is_none_or(\|x\| ...)` | 3 | Modern combinator |
| Redundant closure → method reference | 1 | `map(Tensor::to_vec)` |
| `Vec::new()` + `push` → iterator `collect()` | 5 files | Idiomatic construction |
| `match Option` → combinator | 6 files | `ok_or_else`, `map_or`, `if let Some` |

### 8. Test Infrastructure Fixes

| Fix | Tests Fixed |
|-----|-------------|
| `coral_compiler.rs`: graceful `tokio::runtime::Handle::try_current()` | ~113 |
| `unified_hardware` test assertion: "unknown" → "gpu"/"npu" | 1 |
| `hmm.rs` shader assertion: `log_sum_exp2` → `logsumexp` pattern | 1 |
| `autocorrelation_f64_wgsl.rs`: bare device → f64-gated pool | 2 |

### 9. Sovereign Validation Harness

New module: `shaders/sovereign/validation_harness.rs`

Pure-Rust test that traverses all WGSL shaders, preprocesses them, and runs through
naga parser → sovereign optimizer → validator. No GPU needed. Catches shader regressions
at compile/test time.

---

## API Contract Updates

### New public API

```rust
// LSCFRK integrators
use barracuda::numerical::{
    derive_lscfrk3, LscfrkCoefficients, FlowMeasurement,
    LSCFRK3_W6, LSCFRK3_W7, LSCFRK4_CK,
    find_t0, find_w0, compute_w_function,
};

// Force anomaly detection
use barracuda::nautilus::brain::force_anomaly;

// GPU-resident reduction
pipeline.encode_reduce_to_buffer(&mut encoder, &input_buffer);
pipeline.readback_scalar()?;
```

### Breaking changes

See `BREAKING_CHANGES.md` 0.3.3 section. Key items:
- DF64 Hybrid fallback removed (returns error instead of zeros)
- `device.poll()` returns `Result<PollStatus, PollError>` (wgpu 28)
- NVK excluded from SPIR-V passthrough paths

---

## Confirmed Already Absorbed

| Item | Source | Status |
|------|--------|--------|
| 6 airSpring ops (Makkink, Turc, Hamon, SCS-CN, Stewart, Blaney-Criddle) | airSpring v0.69 | Already in batched_elementwise_f64 |
| Polyakov loop shader | hotSpring | Already in barraCuda |
| SU(3) math shader | hotSpring | Already in barraCuda |
| `compile_shader_universal` | airSpring | Already in barraCuda |
| Chi-squared, Welford | groundSpring | Already in barraCuda |
| Subgroup size detection | toadStool | Already in barraCuda |
| wgpu 28 PollType migration | wetSpring | Already applied |

---

## Remaining P0 Absorption Candidates

| # | Item | Source | Complexity |
|---|------|--------|------------|
| 1 | Dedicated `covariance_df64.wgsl` | Internal | Medium — hand-write Welford DF64 variant |
| 2 | Dedicated `weighted_dot_df64.wgsl` | Internal | Medium — hand-write DF64 accumulation |
| 3 | RHMC multi-shift CG | hotSpring | High — multi-mass solver |
| 4 | Hasenbusch preconditioning | hotSpring | High — mass splitting |
| 5 | Adaptive HMC dt | hotSpring | Medium — step-size tuning |

---

## Verification

```
cargo fmt --all -- --check    ✓ clean
cargo clippy -p barracuda -- -W clippy::pedantic    ✓ zero library warnings
cargo test -p barracuda --lib    ✓ 3,014 passed, 0 failed
```
