<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# barraCuda v0.3.11 — 15-Tier Precision Continuum Handoff

**Date**: March 30, 2026
**From**: barraCuda (Sprint 23+)
**To**: coralReef, toadStool, all springs, primalSpring
**Version**: barraCuda v0.3.11
**Status**: Complete — all quality gates green, 4,307 tests passing

---

## Summary

barraCuda now defines a **15-tier precision continuum** spanning 1-bit binary
to ~104-bit double-double floating point. This replaces the previous
4-variant `PrecisionTier` enum (F32/DF64/F64/F64Precise) with a full
numeric ladder that covers inference, training, and scientific compute.

barraCuda owns the **universal math definitions**: enums, types, tolerances,
WGSL `op_preamble` code, and routing logic. coralReef owns compilation at
each tier. toadStool owns hardware routing to silicon features.

---

## What Changed in barraCuda

### `PrecisionTier` enum (15 variants)

| Tier | Mantissa | Storage | Direction | Hardware |
|------|----------|---------|-----------|----------|
| `Binary` | 1-bit | 1-bit packed | Scale-down | All GPUs (f32 core) |
| `Int2` | 2-bit | 2-bit packed | Scale-down | All GPUs (f32 core) |
| `Quantized4` | ~3.5-bit | 4-bit block | Scale-down | All GPUs (f32 core) |
| `Quantized8` | ~7-bit | 8-bit block | Scale-down | All GPUs (f32 core) |
| `Fp8E5M2` | 2-bit | 8-bit IEEE | Scale-down | All GPUs (f32 core) |
| `Fp8E4M3` | 3-bit | 8-bit IEEE | Scale-down | All GPUs (f32 core) |
| `Bf16` | 7-bit | 16-bit | Scale-down | All GPUs (f32 core) |
| `F16` | 10-bit | 16-bit IEEE | Scale-down | Native f16 or f32 |
| `Tf32` | 10-bit | 32-bit internal | Scale-down | Tensor cores only |
| `F32` | 23-bit | 32-bit IEEE | Baseline | All GPUs |
| `DF64` | ~48-bit | 2×f32 | Scale-up | All GPUs (f32 pairs) |
| `F64` | 52-bit | 64-bit IEEE | Scale-up | `SHADER_F64` required |
| `F64Precise` | 52-bit | 64-bit IEEE | Scale-up | `SHADER_F64` + FMA control |
| `QF128` | ~96-bit | 4×f32 | Scale-up | All GPUs (f32 quad-double) |
| `DF128` | ~104-bit | 2×f64 | Scale-up | `SHADER_F64` required |

### `Precision` enum (13 variants — shader generation)

Maps to WGSL `op_preamble` code: `Binary`, `Int2`, `Q4`, `Q8`, `Fp8E5M2`,
`Fp8E4M3`, `Bf16`, `F16`, `F32`, `F64`, `Df64`, `Qf128`, `Df128`.

`Tf32` is omitted — it is an internal tensor core format, not a shader
compilation target.

### `DType` enum (15 variants — tensor storage)

`Binary`, `I2`, `I4`, `I8`, `F8E4M3`, `F8E5M2`, `Bf16`, `F16`, `F32`,
`F64`, `I32`, `I64`, `U32`, `U64`, `Bool`.

### `PhysicsDomain` enum (15 variants)

Added `Inference`, `Training`, `Hashing` to the existing 12 physics domains.
Each domain routes to an optimal tier via `PrecisionBrain`.

### Tolerances (15 tier-specific constants)

`Tolerance::for_precision_tier(tier)` returns the tier-specific tolerance
with `abs_tol`, `rel_tol`, and justification. All 42+ tolerance constants
maintained.

### coralReef Strategy Mapping

`precision_to_coral_strategy()` maps each `Precision` variant to a coralReef
compilation strategy string:

| Precision | Strategy String |
|-----------|----------------|
| `Binary` | `"binary"` |
| `Int2` | `"int2"` |
| `Q4` | `"q4_block"` |
| `Q8` | `"q8_block"` |
| `Fp8E5M2` | `"fp8_e5m2"` |
| `Fp8E4M3` | `"fp8_e4m3"` |
| `Bf16` | `"bf16_emulated"` |
| `F16` | `"f16"` |
| `F32` | `"f32"` |
| `F64` | `"f64"` |
| `Df64` | `"double_float"` |
| `Qf128` | `"quad_float"` |
| `Df128` | `"double_double_f64"` |

---

## What coralReef Needs To Do

1. **Accept the strategy strings** listed above in `shader.compile.wgsl`
   and `shader.compile.spirv` requests.
2. **Implement compilation** for each strategy. Quantized and sub-f32 tiers
   compute in f32 after dequantization — coralReef compiles them as f32
   with the appropriate pack/unpack preamble already injected by barraCuda.
3. **BF16 emulation**: barraCuda emits bf16↔f32 pack/unpack helpers in the
   `op_preamble`. coralReef compiles as standard f32. No special backend needed.
4. **QF128**: Bailey quad-double uses only f32 arithmetic. No f64 hardware
   needed. coralReef compiles as f32 with the large `op_preamble`.
5. **DF128**: Double-double on f64 pairs. Requires `SHADER_F64`.
   Same compilation path as existing f64 shaders.
6. **Report supported strategies** in `shader.compile.capabilities` response.

### Priority for coralReef

| Priority | Strategy | Rationale |
|----------|----------|-----------|
| P0 | `f32`, `f64`, `double_float` | Already supported |
| P1 | `bf16_emulated`, `f16` | High demand for inference |
| P1 | `q4_block`, `q8_block` | GGML-class inference |
| P2 | `fp8_e4m3`, `fp8_e5m2` | Training gradient exchange |
| P2 | `quad_float` | Extended precision without f64 |
| P3 | `double_double_f64` | Maximum precision |
| P3 | `binary`, `int2` | Extreme quantization |

---

## What toadStool Needs To Do

1. **Expose tensor core availability** in hardware capability reports.
   barraCuda's `PrecisionBrain` can then route `Tf32` workloads to
   tensor-core-equipped hardware.
2. **Report f16/f64 native support** per GPU. barraCuda already queries
   `SHADER_F16` and `SHADER_F64` features; toadStool should confirm
   these at the VFIO level.
3. **Route RT core workloads** for future tiers that leverage
   hardware-specific acceleration (e.g., BF16 native tensor core ops).
4. **Report silicon capabilities** needed for each tier:
   - Binary/Int2/Q4/Q8/FP8/BF16: f32 cores (universally available)
   - F16: native f16 preferred, f32 fallback
   - TF32: tensor cores only
   - F64/F64Precise/DF128: f64 FP units

---

## What Springs Need To Do

**Nothing changes for most springs.** The existing `PrecisionBrain::recommend()`
API remains identical — it now has 15 tiers to choose from instead of 4.

Springs that want to leverage new tiers:

1. **Inference workloads**: Use `PhysicsDomain::Inference` to get Q4/Q8
   routing automatically.
2. **Training workloads**: Use `PhysicsDomain::Training` to get BF16
   routing automatically.
3. **Hashing/masking**: Use `PhysicsDomain::Hashing` to get Binary routing.
4. **Extended precision**: Existing `PhysicsDomain::LatticeQcd` and
   `PhysicsDomain::Spectral` can now cascade to QF128/DF128 when hardware
   supports it.

### New Helper Methods on `PrecisionTier`

```rust
tier.bytes_per_element()     // storage size
tier.requires_f64()          // needs SHADER_F64?
tier.requires_f16()          // needs SHADER_F16?
tier.universally_available() // works on any f32 GPU?
tier.is_scale_up()           // precision > f32?
tier.is_scale_down()         // precision < f32?
tier.is_quantized()          // block-quantized format?
```

---

## Validation

- 4,307 tests passing (up from 4,206 pre-expansion)
- `cargo fmt --all -- --check` clean
- `cargo clippy --workspace --all-targets --all-features -- -D warnings` clean
- `cargo doc --workspace --no-deps` with `-D warnings` clean
- `cargo nextest run --workspace` all pass
- `HardwareCalibration` asserts 15 tiers
- Tolerance ordering verified at compile time via `const` assertions

---

## Files Changed

| File | What |
|------|------|
| `device/precision_tier.rs` | `PrecisionTier` 4→15 variants, `PhysicsDomain` +3 |
| `shaders/precision/mod.rs` | `Precision` 4→13 variants, 8 new `op_preamble` constants |
| `unified_math.rs` | `DType` 7→15 variants |
| `tolerances.rs` | 15 new precision-tier tolerance constants |
| `device/hardware_calibration.rs` | Probes all 15 tiers |
| `device/precision_brain.rs` | Routes all 15 domains, compiles all 15 tiers |
| `device/coral_compiler/types.rs` | Strategy mapping for all 13 Precision variants |
| `gpu_executor/dispatch.rs` | `bytes_to_f32_vec` handles all DType variants |

---

*Math is universal. Precision is silicon. barraCuda defines the continuum;
coralReef compiles it; toadStool runs it.*
