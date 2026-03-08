# airSpring V0.6.9 → BarraCuda/ToadStool: Upstream Absorption Handoff

**Date**: March 4, 2026
**From**: airSpring (ecology/agriculture validation)
**To**: BarraCuda team (sovereign math engine) + ToadStool team (hardware dispatch)
**airSpring**: v0.6.9 (852 lib + 1133 integration tests, 80 binaries)
**BarraCuda**: v0.3.1 standalone (`ecoPrimals/barraCuda`)

---

## Executive Summary

airSpring v0.6.9 successfully promoted 6 local GPU shaders from fixed f32 to
**f64-canonical universal precision** via `compile_shader_universal()`. During
validation we discovered a significant GPU hardware finding that affects the
precision probe cache. This handoff reports the finding and proposes absorption
of airSpring's agricultural shaders.

---

## Part 1: What airSpring Now Consumes

### compile_shader_universal — First Domain Consumer

airSpring is the first Spring to use `compile_shader_universal()` for
domain-specific shaders (the 6 agricultural ops). The integration pattern:

```rust
let source = F64_SHADER_SOURCE.replace("enable f64;\n", "");
let module = device.compile_shader_universal(&source, precision, Some("label"));
```

**Why we strip `enable f64;`**: The f64-canonical `.wgsl` file retains `enable f64;`
as its canonical form. We strip it before passing to `compile_shader_universal`
because:
- `downcast_f64_to_f32()` does NOT strip `enable f64;` (it only substitutes types)
- `compile_shader_f64()` strips it internally, but the F32/Df64 paths go through
  `downcast_f64_to_f32` first
- Stripping before the call ensures clean compilation on all paths

**Suggested improvement for BarraCuda**: Have `compile_shader_universal()` strip
`enable f64;` internally before dispatching to any compilation path. This would
make the API friendlier — consumers shouldn't need to know about this quirk.

### Full Primitive Inventory (v0.6.9)

| Category | Count | Key Primitives |
|----------|------:|----------------|
| Tier A GPU ops | 25 | ops 0-13, kriging, reduce, stream, richards, isotherm, mc_et0, uncertainty stack |
| GPU-universal (NEW) | 6 | SCS-CN runoff, Stewart yield, Makkink/Turc/Hamon/Blaney-Criddle ET₀ |
| CPU delegates | 5 | ridge, brent, diversity, hydrology batch, crop coefficient |
| Validation | 1 | ValidationHarness (all 80 binaries) |
| **Total** | **37** | |

---

## Part 2: What airSpring Learned (for BarraCuda)

### CRITICAL: f64 Compute Shader Reliability on NVK/Mesa

**Hardware**: NVIDIA Titan V (GV100) via NVK/Mesa Vulkan driver
**BarraCuda probe**: `has_f64_shaders() = true`, f64 builtins detected
**Reality**: f64 compute shaders produce **all-zero output**

Diagnostic methodology:
1. Old f32 shader (direct compile) → PASS
2. f64 source downcast to f32 (stripped `enable f64;`, direct compile) → PASS
3. f64 source (`compile_shader_universal(Precision::F32)`) → PASS
4. f64 source (`compile_shader_f64`, f64 buffers) → **FAIL (all zeros)**
5. f64 source (raw `create_shader_module` with `enable f64;`, f64 buffers) → **FAIL (all zeros)**

**Root cause**: NVK/Mesa driver advertises f64 capability (the shader compiles
without error) but the compute pipeline produces incorrect results. This is
consistent with groundSpring V37's NVK discovery.

**Recommendation for BarraCuda probe cache**:
- Add `compute_f64_verified: bool` field to `GpuDriverProfile`
- Run a tiny f64 compute shader (e.g., `2.0 * 3.0 = 6.0`) during probe
- Cache the result: if output ≠ expected, mark `compute_f64_verified = false`
- `Fp64Strategy` should factor this in — a GPU with `has_f64_shaders` but
  `!compute_f64_verified` should default to Df64 or F32, not F64
- This affects all Springs that might request `Precision::F64` on NVK

### enable f64 Stripping in compile_shader_universal

As documented above, the consumer must currently strip `enable f64;` before
calling `compile_shader_universal()`. This is an API paper cut.

**Proposed fix**: In `compile_shader_universal()`, add:
```rust
let source = source.replace("enable f64;\n", "").replace("enable f64;", "");
```
before dispatching to any precision path. This makes the API idempotent —
f64-canonical sources with or without the directive compile correctly.

---

## Part 3: Absorption Candidates (airSpring → BarraCuda)

### Priority 1: Agricultural Science Ops (6 shaders)

airSpring's `local_elementwise_f64.wgsl` contains 6 domain-specific GPU operations
that are mathematically general enough for upstream absorption:

| Op | Function | Math | Absorption Path |
|----|----------|------|-----------------|
| 0 | SCS-CN Runoff | `Q = (P - 0.2S)² / (P + 0.8S)` where `S = 25400/CN - 254` | `barracuda::ops::hydrology` |
| 1 | Stewart Yield Response | `Y = Ym × Π(1 - ky × (1 - ETa/ETm))` | `barracuda::ops::agriculture` |
| 2 | Makkink ET₀ | `ET₀ = C₁ × (Δ/(Δ+γ)) × Rs / λ - C₂` | `barracuda::ops::hydrology` |
| 3 | Turc ET₀ | `ET₀ = a × T/(T+15) × (Rs + 50)`, humidity-adjusted | `barracuda::ops::hydrology` |
| 4 | Hamon ET₀ | `ET₀ = C × D² × Pt` (temperature-saturated vapor) | `barracuda::ops::hydrology` |
| 5 | Blaney-Criddle ET₀ | `ET₀ = p × (0.46T + 8.13)` (monthly daylight) | `barracuda::ops::hydrology` |

These use the same f64-canonical pattern as existing BarraCuda shaders and would
benefit all Springs doing hydrology (groundSpring already uses MC ET₀).

### Priority 2: Probe Cache Enhancement

As described in Part 2 — add compute-verified f64 probing to `GpuDriverProfile`.

### Priority 3: compile_shader_universal API Cleanup

Strip `enable f64;` internally as described in Part 2.

---

## Part 4: Cross-Spring Provenance (What Each Spring Contributed)

| Spring | Contribution to airSpring v0.6.9 | Benefit to BarraCuda |
|--------|----------------------------------|---------------------|
| **hotSpring** | f64 precision primitives (pow, exp, log, trig) | Validates universal precision on real science |
| **wetSpring** | Bio diversity shaders, kriging, moving window | Validates cross-domain shader reuse |
| **groundSpring** | MC ET₀ uncertainty propagation, NVK discovery | Confirms f64 reliability finding across Springs |
| **neuralSpring** | `compile_shader_universal` architecture, optimizers | First real consumer validates the API |
| **airSpring** | 6 agricultural ops, f64 compute finding, API feedback | New hydrology ops for upstream, probe cache improvement |

---

## Quality Gates (airSpring v0.6.9)

| Gate | Result |
|------|--------|
| `cargo fmt --check` | **PASS** |
| `cargo clippy --all-targets -W pedantic -W nursery -D warnings` | **PASS** (0 warnings) |
| `cargo test --lib` | **852 PASS** |
| `cargo test --tests` | **1133 PASS** |
| `cargo doc --no-deps` | **PASS** |

---

## Next Steps for BarraCuda Team

1. **Investigate NVK f64 compute** — Reproduce with a minimal shader on Titan V + NVK
2. **Add compute_f64_verified to probe cache** — Prevents silent precision failures
3. **Strip `enable f64;` in compile_shader_universal** — API paper cut removal
4. **Consider absorbing SCS-CN + ET₀ methods** — General hydrology ops benefit groundSpring too
5. **Update Fp64Strategy** — Factor compute_f64_verified into strategy selection

---

*airSpring v0.6.9 — "math is universal, precision is silicon."*
