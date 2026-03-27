# airSpring V0.10.0 — barraCuda / toadStool Evolution Handoff

**Date:** 2026-03-22
**From:** airSpring V0.10.0
**To:** barraCuda + toadStool teams
**License:** AGPL-3.0-or-later
**Supersedes:** AIRSPRING_V010_BARRACUDA_TOADSTOOL_EVOLUTION_HANDOFF_MAR19_2026.md

---

## Executive Summary

airSpring completed a deep evolution pass that exercised barraCuda 0.3.7's API
surface. Key finding: `GpuDriverProfile` is deprecated but still importable via
`barracuda::device::driver_profile` — airSpring has fully migrated to
`DeviceCapabilities`. This handoff documents migration patterns, absorption
candidates, and ecosystem learnings from 946 lib tests across 25+ GPU ops.

---

## Part 1: DeviceCapabilities Migration (Action Required: None)

airSpring was the last consumer of `GpuDriverProfile` via `barracuda::device::*`.
Migration complete:

| Old API | New API | Notes |
|---------|---------|-------|
| `GpuDriverProfile::from_device(d)` | `DeviceCapabilities::from_device(d)` | Drop-in |
| `profile.fp64_strategy()` | `caps.fp64_strategy()` | Identical signature |
| `profile.precision_routing()` | `caps.precision_routing()` | Identical signature |
| `profile.fp64_rate` | **Dropped** | Driver-internal; consumers use `fp64_strategy()` |

**Impact on barraCuda:** Can now fully remove the `#[deprecated]` re-export path
from `barracuda::device` if no other springs consume it.

**Recommendation:** Grep ecosystem for remaining `GpuDriverProfile` imports before
removing the deprecated path.

---

## Part 2: barraCuda Dependency Health

### Current Consumption (unchanged from V0.10.0 Mar 19 handoff)

| Category | Primitives |
|----------|-----------|
| **Stats** | `pearson_correlation`, `spearman_correlation`, `rmse`, `mbe`, `mean`, `percentile`, `bootstrap_ci`, `std_dev`, `norm_ppf`, `diversity::*`, `hydrology::*` |
| **GPU Ops** | `BatchedElementwiseF64` (20 ops), `FusedMapReduceF64`, `KrigingF64`, `MovingWindowStats`, `CorrelationF64`, `VarianceF64`, `AutocorrelationF64`, `DiversityFusionGpu` |
| **PDE** | `pde::richards`, `RichardsGpu` |
| **Optimize** | `brent`, `brent_gpu`, `nelder_mead` |
| **Validation** | `ValidationHarness` |
| **Device** | `WgpuDevice`, `DeviceCapabilities`, `PrecisionRoutingAdvice` |

### Duplication: None

Zero local WGSL shaders. Zero local math that duplicates barraCuda. Two intentional
test-only divergences (`nash_sutcliffe`, `index_of_agreement` conventions).

---

## Part 3: Absorption Candidates for barraCuda

### 3a. `f64_i8` Cast Helper (NPU Quantization)

```rust
pub fn f64_i8(v: f64) -> i8 {
    debug_assert!(
        v.is_finite() && v >= f64::from(i8::MIN) && v <= f64::from(i8::MAX),
        "f64_i8: {v} out of range"
    );
    v as i8
}
```

**Why:** Any spring doing NPU int8 quantization needs this. The `as i8` cast
truncates silently; the debug_assert catches NaN/overflow in dev builds.
airSpring's `cast` module now has 12 safe cast helpers.

**Action:** Consider absorbing into `barracuda::cast` if other springs adopt NPU quantization.

### 3b. Transport Enum (IPC) — *unchanged from Mar 19 handoff*

Platform-agnostic `Transport::Unix | Transport::Tcp` with `resolve_transport(primal)`.
Every spring reimplements Unix-only `send()`. Absorb into shared IPC module.

### 3c. Proptest Scientific Invariant Pattern

airSpring added 7 proptest invariants for physical laws (positivity, monotonicity,
conservation, boundedness). Pattern is reusable:

```rust
proptest! {
    #[test]
    fn physical_quantity_non_negative(input in valid_range()) {
        let result = compute(input);
        prop_assert!(result >= 0.0);
    }
}
```

**Action:** Consider adding proptest invariant examples to `ValidationHarness` docs.

---

## Part 4: Ecosystem Learnings for toadStool

### 4a. `#[expect]` in Cross-Binary Test Modules

Test utility modules shared across multiple test binaries (`tests/common/mod.rs`)
must use `#[allow]` not `#[expect]` because `#[expect]` evaluates per compilation
unit. A macro unused in one binary but used in another triggers "unfulfilled expectation."

**Rule:** `#[expect]` for per-module lints. `#[allow(reason)]` for shared test utilities.

### 4b. Edge-Case in Quantization (Division by Zero)

`quantize_i8(val, lo, hi)` with `lo == hi` produces `0.0 / 0.0 = NaN`.
`.clamp(0.0, 1.0)` does NOT catch NaN (NaN propagates through comparisons).
Guard the division explicitly:

```rust
if range <= 0.0 { return 0; }
```

### 4c. Smart Refactoring Heuristic

When a file exceeds 500 lines, evaluate by responsibility not line count:
1. Is the most-imported type extractable? (e.g., error types → `error.rs`)
2. Is there a platform-abstraction layer? (e.g., Unix/TCP → `transport.rs`)
3. Is the remaining code cohesive? If yes, keep it in `mod.rs`.

Don't split files that are cohesive single-responsibility (e.g., `ipc/provenance.rs`
at 613 lines — config + session lifecycle for one domain).

---

## Part 5: GPU Evolution Status (unchanged)

| Tier | Count | Status |
|------|-------|--------|
| **A** (GPU-integrated) | 24 | All via upstream barraCuda ops |
| **B** (Orchestrator) | 2 | `seasonal_pipeline`, `atlas_stream` |
| **C** (CPU-only) | 2 | `anderson`, `et0_ensemble` |

No new WGSL shaders needed from barraCuda.

---

## Part 6: Quality Snapshot

| Metric | Value |
|--------|-------|
| Library tests | 946 (all features) |
| Integration tests | 20 (GPU-gated) |
| Forge tests | 61 |
| Proptest invariants | 7 |
| Clippy warnings | 0 (pedantic + nursery, all targets) |
| Unsafe code | 0 (`#![forbid(unsafe_code)]`) |
| C dependencies | 0 |

---

## License

AGPL-3.0-or-later
