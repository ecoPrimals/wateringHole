# barraCuda v0.3.3 Cross-Spring Absorption Handoff

**Date**: 2026-03-08
**From**: barraCuda
**To**: hotSpring, groundSpring, neuralSpring, wetSpring, airSpring, toadStool, coralReef

---

## Summary

Comprehensive cross-spring absorption cycle. Pulled all 5 springs + wateringHole,
reviewed latest handoffs, and resolved P0/P1/P2 items requested across the ecosystem.

---

## P0 — Critical Fix

### `SumReduceF64` / `VarianceReduceF64` Fp64Strategy Routing

**Bug**: Both modules always used native f64 WGSL shaders with `var<workgroup> shared_data: array<f64, 256>`.
On Hybrid-precision devices (NVK/Titan V, consumer GPUs), shared-memory f64 accumulators
silently return zeros. Every other f64 op in barraCuda already had `Fp64Strategy` routing
to DF64 variants — these two were missed.

**Fix**: Created two new DF64 shader variants:
- `shaders/reduce/sum_reduce_df64.wgsl` — sum/max/min using `vec2<f32>` workgroup memory
- `shaders/reduce/variance_reduce_df64.wgsl` — Welford variance using `vec2<f32>` workgroup memory

Added `Fp64Strategy` routing in both Rust wrappers (`sum_reduce_f64.rs`, `variance_reduce_f64.rs`).
Hybrid devices auto-select the DF64 path; Native/Sovereign/Concurrent use native f64 unchanged.

**Affects**: groundSpring V96, neuralSpring S131 (both reported this independently).

**Canary**: `variance_gpu(&[1.0, 2.0, 3.0, 4.0, 5.0], &dev)` should now return >0.1 on all devices.

---

## P1 — High Priority

### Re-export Builder Types (wetSpring P1)

Spring-facing types now accessible at `barracuda::` level:
- `barracuda::HmmForwardArgs`
- `barracuda::Dada2DispatchArgs`, `barracuda::Dada2Buffers`, `barracuda::Dada2Dimensions`
- `barracuda::GillespieModel`
- `barracuda::PrecisionRoutingAdvice`
- `barracuda::Rk45DispatchArgs`

### `barracuda::math::{dot, l2_norm}` (wetSpring P1)

Re-exported from `stats::metrics`. wetSpring's 15+ binaries using local 5-line
implementations can now drop them.

### `fused_ops_healthy()` Canary (neuralSpring P1)

`device::test_harness::fused_ops_healthy(&device)` — runs a minimal variance probe
and returns `false` if shared-memory reductions fail. Available in `test_prelude`.

---

## P2 — Medium Priority

### NVK Zero-Output Detection (airSpring V071)

`GpuDriverProfile::f64_zeros_risk()` returns `true` for NVK + Full/Throttled FP64 devices.
Springs can use this to skip or guard f64 shared-memory reduction tests.

### `GpuViewF64` Ops (groundSpring P2)

Stepping-stone API for zero-readback chains:
- `view.mean_variance(ddof)` → `[f64; 2]`
- `view.sum()` → `f64`
- `GpuViewF64::correlation(a, b)` → `f64`

Currently downloads then dispatches; full buffer-to-buffer path in 0.3.4.

### Test Utilities (neuralSpring P2)

- `test_harness::is_software_adapter(&device)` — detects llvmpipe/lavapipe/swiftshader
- `test_harness::baseline_path(relative)` — `CARGO_MANIFEST_DIR`-relative paths
- Both re-exported in `test_prelude`

---

## Verified Already Absorbed

All shader absorption targets from neuralSpring confirmed present in barraCuda:
- `hmm_backward_log_f64.wgsl` ✅
- `hmm_viterbi_f64.wgsl` ✅
- `mean_reduce.wgsl` / `mean_reduce_f64.wgsl` ✅
- `chi_squared_f64.wgsl` / `fused_chi_squared_f64.wgsl` ✅
- `kl_divergence` → `kldiv_loss_f64.wgsl` ✅
- `linear_regression_f64.wgsl` ✅
- `matrix_correlation_f64.wgsl` ✅
- yukawa `cell_idx` branch fix ✅ (already upstream, branch-based wrapping)

---

## Phase 3 — Spring Absorption Cycle (Mar 8 evening)

### `hill_activation` / `hill_repression` (neuralSpring absorption)

**Source**: neuralSpring `primitives.rs` — thin wrappers around `barracuda::stats::hill`.
**Absorbed to**: `barracuda::stats::metrics` — `hill_activation(x, amplitude, k, n)` and
`hill_repression(x, amplitude, k, n)`. Re-exported at `barracuda::stats::{hill_activation, hill_repression}`.
9 unit tests including complement property (activation + repression = amplitude).

### Ada Lovelace `F64NativeNoSharedMem` Reclassification (groundSpring P0)

**Problem**: RTX 4000-series on proprietary drivers classified as `Df64Only` (Throttled rate),
but basic f64 compute works — only shared-memory f64 reductions fail.
**Fix**: `precision_routing()` now returns `F64NativeNoSharedMem` for Ada + proprietary.
`f64_zeros_risk()` extended to cover Ada + proprietary.
4 unit tests (Ada risk, NVK risk, Ampere no-risk, Ada routing).

### `shared_mem_f64` Runtime Probe (groundSpring P1)

**Problem**: Shared-memory f64 reduction failures detectable only by driver/arch heuristics.
**Fix**: New probe shader dispatches 4 threads writing f64 to `var<workgroup>`, barriers,
thread 0 sums — expected 10.0, tolerance 1e-14. `F64BuiltinCapabilities.shared_mem_f64` field.
`precision_routing()` now checks cached probe result via `cached_shared_mem_f64_for_key()`.
`needs_shared_mem_f64_workaround()` method. Native count 9 → 10.
Heuristic seed conservatively marks NVK as `shared_mem_f64: false`.

---

## Quality Gates

- `cargo fmt --check` ✅
- `cargo clippy --workspace -- -D warnings` ✅ (zero warnings)
- `cargo test -p barracuda --lib` ✅ (3,118 tests — 3,104 pass, 1 flaky GPU contention, 13 ignored)
- `cargo test -p barracuda-core` ✅
- 712 WGSL shaders

---

## Remaining Cross-Spring Items (Not Addressed)

| Item | Priority | Notes |
|------|----------|-------|
| RHMC multi-shift CG solver | P2 | hotSpring L4 |
| Adaptive HMC dt from acceptance rate | P2 | hotSpring |
| `ComputeBackend` trait | P3 | hotSpring |
| `ComputeDispatch` tarpc for NUCLEUS | P3 | wetSpring |
| `BandwidthTier` in device profile | P3 | wetSpring |
| `domain-genomics` feature extraction | P3 | wetSpring |
| Full buffer-to-buffer `GpuView` ops | P3 | 0.3.4 target |
| Tridiagonal eigensolver | P3 | neuralSpring Papers 022-023 |
| coralForge AlphaFold DF64 shaders | P3 | neuralSpring — 15 shaders |

---

## Spring Action Items

- **ALL SPRINGS**: Update barraCuda pin to HEAD — f64 pipeline fix, Ada reclassification,
  shared_mem_f64 probe, hill kinetics all available
- **groundSpring**: Ada Lovelace P0 resolved — `precision_routing()` now returns
  `F64NativeNoSharedMem`. `shared_mem_f64` probe available for runtime verification.
  Drop local `tridiag_eigh` once `BatchedTridiagEigh` GPU op lands.
- **neuralSpring**: Drop local `primitives::hill_activation` / `hill_repression` — use
  `barracuda::stats::{hill_activation, hill_repression}`. Absorb `fused_ops_healthy()` canary.
  `chi_squared_f64` and `kl_divergence_f64` ops already absorbed.
- **wetSpring**: Drop local `dot`/`l2_norm` implementations; use `barracuda::math::{dot, l2_norm}`
- **wetSpring**: Use `barracuda::Rk45DispatchArgs` for `BatchedOdeRK45F64` adoption
- **airSpring**: Use `f64_zeros_risk()` for NVK guard in metalForge tests.
  Remove orphan `local_elementwise_f64.wgsl` from coralReef corpus.
