# barraCuda → Springs: NVVM Poisoning Guard + Cross-Spring Absorption

**Date:** March 10, 2026
**From:** barraCuda v0.3.4
**To:** All springs
**License:** AGPL-3.0-only
**Covers:** hotSpring v0.6.25 NVVM poisoning discovery + 6-spring evolution review

---

## Executive Summary

- **NVVM device poisoning guard implemented** in barraCuda's compilation pipeline — proprietary NVIDIA DF64 transcendentals are now stripped before compilation to prevent unrecoverable device death
- **DF64 safety probing** absorbed into `F64BuiltinCapabilities` — `df64_arith` and `df64_transcendentals_safe` fields now available to all springs
- **6-spring review completed**: hotSpring v0.6.25, groundSpring V99, neuralSpring S139, wetSpring V105, airSpring v0.7.5, healthSpring V14

---

## Part 1: NVVM Device Poisoning — Resolved

### What Changed in barraCuda

1. **New workaround**: `Workaround::NvvmDf64TranscendentalPoisoning` — activated for ALL proprietary NVIDIA architectures (not just Ada)
2. **Compilation guard**: `compile_shader_df64()` now checks `has_nvvm_df64_poisoning_risk()` before including `df64_transcendentals.wgsl` in the preamble. When risk is detected, only `df64_core.wgsl` arithmetic is included.
3. **Probe integration**: `F64BuiltinCapabilities` extended with `df64_arith` and `df64_transcendentals_safe` fields, populated during both heuristic seeding and runtime probing
4. **Driver profile method**: `GpuDriverProfile::has_nvvm_df64_poisoning_risk()` — O(1) lookup for poisoning risk
5. **Strategy helper**: `GpuDriverProfile::df64_transcendentals_safe()` — probe-aware DF64 transcendental safety

### Impact on Springs

| Spring | Action Required |
|--------|-----------------|
| **hotSpring** | Your `PrecisionBrain` can now delegate DF64 safety to barraCuda's probe. Consider removing local `transcendentals_safe` heuristic in favour of `F64BuiltinCapabilities::df64_transcendentals_safe`. |
| **groundSpring** | RTX 4070 Ada reclassification is aligned — `Workaround::NvvmAdaF64Transcendentals` (existing) + `NvvmDf64TranscendentalPoisoning` (new) both fire on proprietary NVIDIA Ada. |
| **neuralSpring** | 11 fused GPU tests gated by canary variance probe — barraCuda's DF64 guard prevents the root cause. Test gating may be relaxable. |
| **wetSpring** | `GillespieGpu` NVVM skip on RTX 4070 is now upstream-protected. DF64 shader validation gaps (zero output) should be retested with guard active. |
| **airSpring** | NVK zero-output detection pattern is complementary (different root cause: NVK Mesa, not NVVM). Both guards coexist. |
| **healthSpring** | `pow(f64, f64)` polyfill via `exp(n * log(c))` remains needed for native f64 path. DF64 path now guards against transcendental poisoning. |

---

## Part 2: Cross-Spring Absorption Review

### Completed Absorptions (This Sprint)

| Item | Source | What Was Done |
|------|--------|---------------|
| NVVM poisoning guard | hotSpring v0.6.25 | `NvvmDf64TranscendentalPoisoning` workaround + compilation guard |
| DF64 safety probing | hotSpring v0.6.25 | `df64_arith` + `df64_transcendentals_safe` in probe capabilities |
| `df64_transcendentals_safe()` | hotSpring v0.6.25 | Strategy helper on `GpuDriverProfile` |

### Absorption Queue (P1 — Next Sprint)

| Item | Source | Priority | Status |
|------|--------|----------|--------|
| `seed_extend` GPU op | wetSpring V105 | P2 | Open |
| `profile_alignment` | wetSpring V105 | P2 | Open |
| `foce_estimate` / `saem_estimate` | healthSpring V14 | P1 | **✓ Resolved** — `FoceGradientGpu` + `VpcSimulateGpu` |
| Smith-Waterman GPU shader | neuralSpring S139 | P2 | Open (CPU SW exists) |
| `peak_integrate_batch` | wetSpring V105 | P2 | Open |
| Activate `barracuda::activations::*` | neuralSpring S139 | P1 | **✓ Resolved** — public at `barracuda::activations::*` |
| `BatchReconcileGpu` | wetSpring V105 | P1 | **✓ Resolved** — `BipartitionEncodeGpu` |

### Absorption Queue (P2 — Future)

| Item | Source | Priority | Notes |
|------|--------|----------|-------|
| `AutocorrelationF64` | airSpring v0.7.5 | P2 | Temporal autocorrelation for time series |
| `Fft1DF64` | airSpring v0.7.5 | P2 | Spectral analysis |
| `precision_eval.rs` | hotSpring v0.6.25 | P2 | Per-shader precision/throughput profiler |
| `transfer_eval.rs` | hotSpring v0.6.25 | P2 | PCIe bandwidth profiler |
| Kokkos parity benchmarks | neuralSpring S139 | P2 | Performance validation framework |
| `GpuView<T>` persistent buffers | wetSpring V105 | P2 | Reduce upload overhead (3.7× Kokkos gap) |
| `NvkZeroGuard` wrapper | airSpring v0.7.5 | P2 | Generic zero-output detection + CPU fallback |

---

## Part 3: Spring Issues Directed at barraCuda

| Issue | Source | Status |
|-------|--------|--------|
| Ada Lovelace reclassify as `F64NativeNoSharedMem` | groundSpring V97 | ✓ Addressed (probe-based, not heuristic) |
| `Fp64Strategy` Hybrid/Native branching in `SumReduceF64` | groundSpring V96 | **✓ Resolved** — `PrecisionBrain` routing |
| FFT in `SubstrateCapabilityKind` | groundSpring V95 | Open |
| Expose scalar activations as public API | neuralSpring V92 | **✓ Resolved** — `barracuda::activations::*` |
| `ComputeDispatch` BGL builder pattern | wetSpring V105 | **✓ Resolved** — `BglBuilder` |
| `CsrMatrix` from-triplets builder | wetSpring V105 | **✓ Resolved** — `from_triplets_summed()` |
| coralReef remove `local_elementwise_f64.wgsl` | airSpring v0.7.5 | coralReef action |
| NVK device probe cache flag | airSpring v0.7.5 | ✓ Addressed (probe cache with `df64_transcendentals_safe`) |

---

## Part 4: Metrics

```
barraCuda v0.3.4:
  - 3,500+ tests (27 new probe/workaround tests passing)
  - 0 clippy warnings
  - 0 unsafe blocks
  - AGPL-3.0-only
  - NVVM poisoning: guarded on all proprietary NVIDIA architectures
  - DF64 safety: probe-based, heuristic-seeded
  - 712+ WGSL f64 shaders
  - 1,055+ Rust source files
```
