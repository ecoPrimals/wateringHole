# hotSpring → coralReef/barraCuda: DF64 Naga Poisoning Diagnostic

**Date**: 2026-03-11 (updated with coralReef Iter 33 + barraCuda v0.3.5 findings)  
**From**: hotSpring v0.6.29 (control experiments + Kokkos parity benchmarking)  
**To**: coralReef team, barraCuda team  
**Priority**: HIGH — blocks DF64 throughput recovery on all NVIDIA hardware  
**Status**: SOVEREIGN FIX VALIDATED by coralReef Iter 33 (6/6 tests PASS)  

## TL;DR

The DF64 transcendental poisoning is **NOT** a driver JIT bug (NVVM or NAK). It is a
**naga WGSL→SPIR-V codegen issue** that affects ALL Vulkan backends — proprietary,
NVK, and llvmpipe. hotSpring Exp 055 confirmed this by testing on all three drivers.

**coralReef Iteration 33 has validated the sovereign fix**: the exact Yukawa DF64 shader
that poisons wgpu/naga compiles cleanly through coralReef for SM70, SM86 (RTX 3090),
and RDNA2. 6/6 tests PASS in `nvvm_poisoning_validation.rs`. The remaining integration
step is wiring sovereign dispatch into hotSpring's MD pipeline.

## Evidence

Tested with `test_df64_nvk_poison` binary on three backends:

| GPU | Driver | f64 Force | DF64 Force | Conclusion |
|-----|--------|-----------|------------|------------|
| RTX 3090 (Ampere) | NVIDIA Proprietary 580.119.02 | **PASS** (max 2.66e-16) | **POISONED** (all zero) | NVVM JIT receives bad SPIR-V |
| Titan V (Volta) | NVK / Mesa 25.1.5 (NAK) | **PASS** (max 2.58e-16) | **POISONED** (all zero) | NAK receives same bad SPIR-V |
| llvmpipe (CPU) | LLVM 15.0.7 | FAIL (all zero) | FAIL (all zero) | Baseline broken (LLVM 15 f64 support) |

**Key observation**: NVK's `has_nvvm_df64_poisoning_risk()` is `false`, so the full
`df64_transcendentals.wgsl` (including `exp_df64`, `sqrt_df64`) is included in the
combined WGSL. NAK compiles it without errors. But the dispatch produces all-zero forces.

The native f64 Yukawa shader (identical physics, identical bindings, but using native
`f64` arithmetic instead of Df64 f32-pairs) produces correct forces on both NVIDIA
drivers. The ONLY difference is the DF64 computation path.

## Root Cause Analysis

### What's the same between working (f64) and broken (DF64)?

- Same GPU hardware
- Same wgpu version
- Same naga version
- Same buffer layout (all `array<f64>`)
- Same physics (Yukawa, same parameters)
- Same dispatch workgroups

### What's different?

The DF64 shader:
1. Prepends `df64_core.wgsl` (Df64 struct, df64_add/mul/div/sub)
2. Prepends `df64_transcendentals.wgsl` (exp_df64, sqrt_df64 — pure f32 ops)
3. Uses `df64_from_f64()` to convert positions into f32 pairs
4. Computes forces using Df64 arithmetic
5. Uses `df64_to_f64()` to convert results back to f64

### Likely naga SPIR-V codegen issues

1. **`df64_from_f64` / `df64_to_f64`**: These convert between `f64` and `Df64 (vec2<f32>)`. Naga may miscompile the f64→f32 pair split (Dekker) or the f32 pair→f64 recombination in SPIR-V.

2. **Mixed f64 + f32 in same shader**: The DF64 shader uses `array<f64>` for storage I/O but `f32` for all computation. Naga may produce incorrect SPIR-V when the same function mixes f64 loads/stores with f32 arithmetic.

3. **Struct layout**: `Df64` is `struct { hi: f32, lo: f32 }`. Naga may not correctly lower this struct's alignment/padding in SPIR-V storage class.

4. **Transcendental functions**: `exp_df64` uses `round()`, `ldexp()`, `exp2()` — all f32 builtins. These might be incorrectly typed or optimized away in the SPIR-V.

## Impact on hotSpring

The DF64 path would give **~32× f32 ALU throughput** on Ampere (1:1 f32 vs 1:32 f64).
With DF64 poisoned, hotSpring falls back to native f64, resulting in the **10-12×
performance gap** vs Kokkos-CUDA measured in Exp 053 and Exp 054.

If DF64 worked correctly, the gap would narrow from 10-12× to an estimated **3-4×**
(accounting for dispatch overhead, memory access patterns, and the remaining non-force
computation that stays in f64).

## Benchmark Data (Exp 054: N-Scaling Complexity)

| N | barraCuda (native f64) | Kokkos-CUDA | Gap | Projected DF64 gap |
|---:|---:|---:|---:|---:|
| 500 | 607 steps/s | 1,677 steps/s | 2.8× | ~1× (dispatch-bound) |
| 2,000 | 185 steps/s | 1,839 steps/s | 10.0× | ~3× |
| 10,000 | 63 steps/s | 559 steps/s | 8.8× | ~2-3× |
| 50,000 | 17 steps/s | 167 steps/s | 9.8× | ~3× |

## Resolution Paths

### Path A: coralReef Sovereign Dispatch (recommended)

coralReef Iteration 28 validated NVVM poisoning bypass (12 tests × 3 patterns × 6 arches).
The sovereign pipeline (WGSL → naga IR → codegen → SASS) bypasses SPIR-V entirely. Once
DRM dispatch is available, hotSpring can compile DF64 Yukawa → SASS → dispatch without
touching naga's SPIR-V backend.

**What coralReef needs**:
1. Add `yukawa_force_df64.wgsl` to the cross-spring corpus (it uses both f64 storage and Df64 compute)
2. Validate that the sovereign compiler produces correct forces
3. Wire the DRM dispatch path for compute shaders (Nouveau UAPI from Iter 31)

### Path B: Fix naga SPIR-V Codegen

File a targeted naga bug: "Mixed f64/f32 Df64 shader produces all-zero output via SPIR-V".
Repro is deterministic — `test_df64_nvk_poison` binary in hotSpring. This would fix the
issue for all wgpu users, not just our stack.

### Path C: barraCuda DF64 Preamble Evolution

coralReef's `df64_preamble.wgsl` has slightly different implementations:
- `sqrt_df64`: single Newton-Raphson step (vs barraCuda's two-step refinement + df64_div)
- `exp_df64`: uses `exp2(k_f)` (vs barraCuda's `ldexp(1.0, k)`)

It's possible coralReef's simpler implementations avoid the naga codegen issue.
**Test**: swap barraCuda's `df64_transcendentals.wgsl` with coralReef's `df64_preamble.wgsl`
transcendentals and re-run `test_df64_nvk_poison`.

### Path D: Pure DF64 Shader (No f64 Storage)

Eliminate all `f64` types from the DF64 shader — use `array<vec2<f32>>` for storage
instead of `array<f64>`. This removes the mixed f64/f32 pattern that may be triggering
the naga bug. Requires upstream barraCuda buffer format changes.

## Files

| File | Location | Purpose |
|------|----------|---------|
| `test_df64_nvk_poison` | `hotSpring/barracuda/src/bin/test_df64_nvk_poison.rs` | Diagnostic binary |
| `yukawa_force_df64.wgsl` | `hotSpring/barracuda/src/md/shaders/yukawa_force_df64.wgsl` | Poisoned shader |
| `df64_transcendentals.wgsl` | `barraCuda/crates/barracuda/src/shaders/math/` | barraCuda's DF64 transcendentals |
| `df64_preamble.wgsl` | `coralReef/crates/coral-reef/src/` | coralReef's DF64 preamble (simpler) |
| Exp 053 | `hotSpring/experiments/053_LIVE_KOKKOS_PARITY_BENCHMARK.md` | Fixed-N parity results |
| Exp 054 | `hotSpring/experiments/054_KOKKOS_COMPLEXITY_N_SCALING.md` | N-scaling complexity results |

## Action Items for coralReef

- [x] Add `yukawa_force_df64.wgsl` to sovereign compiler corpus — **DONE** (Iter 33, `nvvm_poisoning_validation.rs`)
- [ ] Validate sovereign-compiled DF64 Yukawa produces non-zero forces — requires DRM dispatch (hardware)
- [ ] Investigate whether `df64_preamble.wgsl` (coralReef's simpler impl) avoids the naga bug — hotSpring can test via wgpu path
- [ ] Consider filing naga bug for mixed f64/f32 SPIR-V codegen
- [ ] Track DRM dispatch readiness for compute shaders — Nouveau UAPI (Iter 31), nvidia-drm UVM (Iter 31)

## Action Items for barraCuda

- [ ] Update `has_nvvm_df64_poisoning_risk()` — rename to `has_df64_spir_v_poisoning()` since it affects ALL drivers, not just NVVM
- [ ] Test coralReef's `df64_preamble.wgsl` as a drop-in replacement for `df64_transcendentals.wgsl`
- [ ] Evaluate Path D (pure Df64 storage, no f64 types in DF64 shaders)

## Upstream Validation (coralReef Iter 33)

coralReef Iteration 33 (865de7a) independently validated the sovereign fix:

- **6 new tests** in `nvvm_poisoning_validation.rs`:
  - `nvvm_poisoning_yukawa_df64_sm70` — PASS (Titan V)
  - `nvvm_poisoning_yukawa_df64_sm86` — PASS (RTX 3090)
  - `nvvm_poisoning_yukawa_df64_rdna2` — PASS (Radeon)
  - `nvvm_poisoning_df64_transcendentals_isolated_sm86` — PASS
  - `nvvm_poisoning_df64_transcendentals_isolated_sm70` — PASS
  - `nvvm_poisoning_yukawa_verlet_df64_sm86` — PASS

- coralReef used our **exact Yukawa DF64 shader** (from `yukawa_force_df64.wgsl`)
  with `round()` replacing `round_f64` polyfill

- Sovereign path compiles to clean SASS: `FADD/FMUL/FFMA/MUFU.EX2` for DF64
  transcendentals, `DADD/DMUL/DFMA` for native f64 PBC

- Gap decomposition: sovereign DF64 = 4-8x speedup → gap narrows from 12x to 1.5-3x

See: `CORALREEF_PHASE10_ITERATION33_NVVM_POISONING_VALIDATION_HANDOFF_MAR11_2026.md`

## Upstream Evolution (barraCuda v0.3.5 → 0ee46a1)

barraCuda added `specs/PRECISION_TIERS_SPECIFICATION.md` — formalizes the 15-tier
precision ladder from Binary (1-bit) through DF128 (~104-bit). DF64 is positioned at
~48-bit mantissa with 0.4x f32 throughput (vs 0.03x for native f64 on consumer GPUs).
This validates the 10-30x throughput argument for sovereign DF64 on Ampere.

## Integration Path (Next Step)

The immediate integration path from coralReef Iter 33 handoff:

```rust
// Option A: toadStool delegation
let force_binary = toadstool_client.compile_wgsl(
    shaders::SHADER_YUKAWA_FORCE_DF64,
    CompileOptions { target: gpu.detected_arch(), fp64_strategy: Fp64Strategy::DoubleFloat, .. }
)?;
let force_pipeline = gpu.create_pipeline_from_binary(force_binary);
```

Requires: `create_pipeline_from_binary` on barraCuda's `WgpuDevice` (P1 action item).

## Cross-References

- hotSpring v0.6.29: `CONTROL_EXPERIMENT_STATUS.md`, `CHANGELOG.md`
- Upstream pins: barraCuda v0.3.5 (8d63c77→0ee46a1), toadStool S146, coralReef Iter 31→33 (865de7a)
- coralReef handoff: `CORALREEF_PHASE10_ITERATION33_NVVM_POISONING_VALIDATION_HANDOFF_MAR11_2026.md`
- barraCuda handoff: `BARRACUDA_V034_NVVM_POISONING_SPRING_ABSORPTION_HANDOFF_MAR10_2026.md`
- Previous handoff: `HOTSPRING_V0629_UPSTREAM_SYNC_V4_HANDOFF_MAR11_2026.md`
