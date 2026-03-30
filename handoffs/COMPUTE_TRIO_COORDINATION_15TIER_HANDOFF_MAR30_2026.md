<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# Compute Trio Coordination — 15-Tier Precision Integration Handoff

**Date**: March 30, 2026
**From**: barraCuda v0.3.11 (Sprint 23+)
**To**: coralReef team, toadStool team
**Purpose**: Coordinate the trio's integration of the 15-tier precision continuum

---

## Context

barraCuda has expanded from 4 precision tiers (F32/DF64/F64/F64Precise) to a
15-tier continuum (Binary→DF128). The math definitions, tolerances, and WGSL
`op_preamble` code are complete and tested (4,307 tests). coralReef and
toadStool need to absorb their respective portions.

---

## For coralReef: Compilation Strategy Absorption

### New Strategy Strings

barraCuda sends these via `shader.compile.wgsl` and `shader.compile.spirv`:

| Strategy | Tier | Compilation Notes |
|----------|------|-------------------|
| `"binary"` | Binary (1-bit) | f32 shader with bitwise ops. No special backend. |
| `"int2"` | Int2 (2-bit) | f32 shader with 2-bit pack/unpack. No special backend. |
| `"q4_block"` | Q4 block-quantized | f32 shader with block dequantization preamble. |
| `"q8_block"` | Q8 block-quantized | f32 shader with block dequantization preamble. |
| `"fp8_e5m2"` | FP8 E5M2 | f32 compute with fp8 pack/unpack helpers. |
| `"fp8_e4m3"` | FP8 E4M3 | f32 compute with fp8 pack/unpack helpers. |
| `"bf16_emulated"` | BF16 | f32 compute with bf16↔f32 bitcast pack/unpack. |
| `"f16"` | F16 | Native f16 if `SHADER_F16` available, else f32 fallback. |
| `"f32"` | F32 | Standard f32 compilation. Already supported. |
| `"double_float"` | DF64 | f32 double-float pair. Already supported. |
| `"f64"` | F64 | Native f64. Already supported. |
| `"quad_float"` | QF128 | f32-only Bailey quad-double. Large preamble, pure f32 arithmetic. |
| `"double_double_f64"` | DF128 | f64 double-double. Same compilation path as f64 but with 2×f64 preamble. |

### Key Observations for coralReef

1. **All sub-f32 strategies are f32 compilations.** barraCuda injects the
   pack/unpack and dequantization helpers in the `op_preamble`. coralReef
   compiles the result as standard f32 WGSL. No new ISA backend needed.

2. **QF128 is pure f32.** The Bailey quad-double algorithm uses only f32
   multiply and add. The preamble is large (~200 lines) but the compilation
   target is vanilla f32. This gives ~96-bit mantissa on GPUs with zero
   f64 hardware — useful for consumer GPUs.

3. **DF128 follows existing f64 path.** If coralReef can compile f64,
   it can compile DF128 (double-double on f64 pairs).

4. **Strategy string validation.** coralReef should report unsupported
   strategies in `shader.compile.capabilities`. barraCuda's `PrecisionBrain`
   will avoid routing to tiers whose strategy isn't available.

### Recommended Absorption Order

```
Phase 1 (already done): f32, f64, double_float
Phase 2: bf16_emulated, f16, q4_block, q8_block
Phase 3: fp8_e4m3, fp8_e5m2, quad_float
Phase 4: double_double_f64, binary, int2
```

Phase 2 is the highest-impact expansion — BF16 and Q4 cover the majority
of inference and training workloads.

---

## For toadStool: Hardware Capability Expansion

### Silicon Features to Expose

| Feature | Used By | How barraCuda Uses It |
|---------|---------|----------------------|
| f16 native support | F16, BF16 tiers | `HardwareCalibration` marks F16 as native vs emulated |
| f64 native support | F64, F64Precise, DF128 | `HardwareCalibration` marks f64 tiers as available |
| Tensor core presence | TF32 tier | `PrecisionBrain` can route TF32 workloads |
| Tensor core BF16 mode | BF16 tier | Native BF16 matmul instead of f32 emulation |
| RT core presence | Future tiers | Reserved for hardware-accelerated operations |
| Compute capability / SM version | All tiers | Used for throughput estimation |
| VRAM size | All tiers | Batch size routing |
| PCIe topology | Multi-GPU tiers | Work distribution |

### Priority for toadStool

| Priority | Capability | Rationale |
|----------|-----------|-----------|
| P0 | f16/f64 native (already done) | Core routing |
| P1 | Tensor core detection | TF32 and native BF16 matmul |
| P1 | SM/compute capability reporting | Throughput estimation |
| P2 | RT core detection | Future acceleration |
| P2 | Native BF16 support flag | Distinguish emulated vs hardware BF16 |

### Hardware Calibration Integration

barraCuda's `HardwareCalibration::from_capabilities()` currently probes via
wgpu features (`SHADER_F16`, `SHADER_F64`). When toadStool provides richer
hardware reports via IPC, `HardwareCalibration` should prefer toadStool's
report and fall back to wgpu probing.

```
Preferred: toadStool.hardware.capabilities → HardwareCalibration
Fallback:  wgpu Features → HardwareCalibration
```

---

## Trio Contract Summary

```
barraCuda                          coralReef                          toadStool
────────                          ─────────                          ─────────
PrecisionTier (15 variants)  →    strategy strings (13)         →    silicon features
Precision (13 variants)      →    compilation targets            →    dispatch routing
DType (15 variants)          →    storage format awareness       →    DMA layout
Tolerance (15 constants)     →    (validation, not compilation)  →    (not applicable)
PrecisionBrain               →    capability query               →    hardware report
op_preamble WGSL             →    compile input                  →    (not applicable)
```

### IPC Flow

```
barraCuda → coralReef
  shader.compile.wgsl { source, strategy: "bf16_emulated" }
  shader.compile.capabilities → { strategies: ["f32","f64","double_float",...] }

barraCuda → toadStool (via SovereignDevice)
  compute.dispatch.submit { binary, workgroups, ... }
  compute.hardware.capabilities → { f16: true, f64: true, tensor_cores: false, ... }
```

---

## Learned Lessons for the Trio

1. **Math first, compilation second, hardware third.** barraCuda defines
   the mathematical intent. coralReef translates to silicon. toadStool
   executes on silicon. This ordering prevents hardware assumptions from
   leaking into math code.

2. **Universal availability matters.** Scale-down tiers (Binary through
   BF16) all compute in f32. This means they work on every GPU, including
   llvmpipe. coralReef doesn't need special backends for these tiers.

3. **QF128 is the highest-precision universally-available tier.** It runs
   on any f32 GPU and provides ~96-bit mantissa. This is barraCuda's
   answer to "what if the GPU has no f64 hardware at all?"

4. **Strategy strings are the contract.** barraCuda and coralReef
   coordinate via strategy strings, not enum variants. This allows
   coralReef to evolve its compilation strategies independently.

5. **Tolerances are per-tier.** When validating compilation correctness,
   use `Tolerance::for_precision_tier(tier)` to get appropriate bounds.
   A Q4 result that's within Q4 tolerance is correct even if it differs
   significantly from f64 reference.

---

*The math is universal. The compilation is sovereign. The hardware is silicon.*
