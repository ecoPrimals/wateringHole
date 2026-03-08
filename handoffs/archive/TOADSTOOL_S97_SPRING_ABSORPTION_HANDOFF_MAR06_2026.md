# SPDX-License-Identifier: AGPL-3.0-or-later

# toadStool S97 — Spring Absorption Handoff

**Date**: March 6, 2026
**From**: toadStool S97 (6,176 lib tests, 0 clippy warnings, ~85% line coverage)
**To**: barraCuda team (compute math), ecoPrimals ecosystem
**License**: AGPL-3.0-or-later

---

## Executive Summary

toadStool S97 completes a Spring Absorption pass focused on GPU adapter discovery evolution,
NPU dispatch generalization, and science IPC namespace. This handoff documents what changed
and what barraCuda should consume.

---

## 1. GPU Adapter Discovery Evolution

### 1.1 NVK Volta f64 Probe

**Problem**: airSpring and hotSpring report that NVK on Volta GPUs (Titan V, Tesla V100,
Quadro GV100) claims `has_f64_shaders: true` but f64 compute returns zeros.

**Solution**: New `f64_compute_unreliable: bool` field on `GpuAdapterInfo`. Set when driver
is NVK AND device name contains Volta GPU names.

**API for barraCuda**:
- `adapter_info.has_reliable_f64()` → `true` only when f64 is both supported AND reliable
- `adapter_info.f64_compute_unreliable` → direct flag check
- `HardwareFingerprint` omits `SubstrateCapabilityKind::F64Native` for NVK Volta

**Action**: barraCuda's `GpuDriverProfile` should consult `has_reliable_f64()` instead of
raw `supports_shader_f64` when deciding between native f64 and DF64 fallback.

### 1.2 Subgroup Size Detection

New fields on `GpuAdapterInfo`:
- `min_subgroup_size: u32` — minimum warp/wavefront size
- `max_subgroup_size: u32` — maximum warp/wavefront size

**Action**: barraCuda's workgroup tuning (`preferred_workgroup_size()`) can use subgroup
size for more precise tuning instead of vendor heuristics.

### 1.3 2D Dispatch Threshold

New method: `adapter_info.max_2d_dispatch() -> (u32, u32)`

Returns max 2D dispatch dimensions. Useful for hotSpring lattice ops that use 2D workgroup
layouts.

---

## 2. NPU Evolution (hotSpring Absorption)

### 2.1 ProxyFeature + AdaptiveSimulationController

Absorbed from hotSpring's `npu_worker.rs` pattern:

- `ProxyFeature` struct — named typed measurement (name, value, target, weight)
- `ProxyFeatureSet` type alias — `Vec<ProxyFeature>`
- `AdaptiveSimulationController` trait — higher-level than `NpuParameterController`:
  - `observe_features(&[ProxyFeature])`
  - `suggest_params() -> Option<ParameterSuggestion<Params>>`
  - `is_warmed_up()`
  - `reset()`

### 2.2 NpuInferenceRequest

- `NpuInferenceRequest` struct — typed inference request (model, input, batch_size_hint, priority)
- `dispatch_request()` default method on `NpuDispatch` trait

**Action**: Springs implementing NPU-driven parameter tuning (hotSpring's Nautilus Brain)
can use these generic primitives instead of custom implementations.

---

## 3. Science IPC Namespace

10 new `science.*` JSON-RPC methods registered in both the semantic registry and the handler:

| Method | Routes to |
|--------|-----------|
| `science.compute.submit` | `compute.submit` |
| `science.compute.status` | `compute.status` |
| `science.compute.result` | `compute.result` |
| `science.compute.cancel` | `compute.cancel` |
| `science.gpu.dispatch` | `compute.submit` (GPU-routed) |
| `science.gpu.capabilities` | GPU device query + precision info |
| `science.npu.dispatch` | `compute.submit` (NPU-routed) |
| `science.npu.capabilities` | NPU runtime capability report |
| `science.substrate.discover` | GPU + NPU + CPU substrate discovery |
| `science.substrate.probe` | Capability-specific substrate probe |

**Action**: Springs (wetSpring, airSpring, etc.) can now use `science.*` methods for
scientific compute IPC without coupling to barraCuda directly. toadStool mediates.

---

## 4. ecoBin Compliance

- `ring` C FFI completely removed from `Cargo.lock` (reqwest dev-dep removed)
- `zstd` C FFI replaced with `ruzstd` (pure Rust) in secure_enclave tests/benches
- `zstd-sys` remains only as transitive dep of `wasmtime-cache` (upstream concern)

---

## 5. Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --workspace --all-targets` | PASS — 0 warnings |
| `cargo test --workspace --lib` | PASS — 6,176 passed, 0 failed |
| Production unwrap/expect/panic/todo | 0 |
| Files > 1000 lines | 0 |
| SPDX headers | 100% |

---

## 6. Recommendations for barraCuda Team

1. **Consume `has_reliable_f64()`**: Replace raw `supports_shader_f64` checks with
   `adapter_info.has_reliable_f64()` for NVK Volta safety.
2. **Subgroup-aware workgroup tuning**: Use `min_subgroup_size` / `max_subgroup_size`
   for more precise `preferred_workgroup_size()` instead of vendor heuristics.
3. **ComputeBackend trait**: hotSpring requests a `ComputeBackend` trait for swappable
   backends (barraCuda, Kokkos, Python). Consider adding to barraCuda's public API.
4. **DF64 fused ops zero bug**: wetSpring V97c reports `VarianceF64`, `CorrelationF64`,
   `CovarianceF64`, `WeightedDotF64` return zeros on `Fp64Strategy::Hybrid` GPUs (RTX 4070).
   These ops need DF64-awareness.
5. **wgpu 28 PollType migration**: Document `PollType::Wait` struct variant in BREAKING_CHANGES.md.

---

## 7. Superseded Handoffs

| File | Reason |
|------|--------|
| `TOADSTOOL_S93_DF64_HANDOFF_MAR03_2026.md` | Still valid (DF64 transfer) |
| `TOADSTOOL_BARRACUDA_S88_SPRING_ABSORPTION_HANDOFF_MAR02_2026.md` | Superseded by this |
| `TOADSTOOL_BARRACUDA_S87_DEEP_DEBT_EVOLUTION_HANDOFF_MAR02_2026.md` | Superseded by this |

---

*This handoff is unidirectional: toadStool → barraCuda/ecosystem. No response expected.*
