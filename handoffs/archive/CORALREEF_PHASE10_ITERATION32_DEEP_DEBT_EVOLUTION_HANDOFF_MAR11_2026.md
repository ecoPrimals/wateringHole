# coralReef Phase 10 Iteration 32 — Deep Debt Evolution

**Date**: March 11, 2026
**Phase**: 10 — Multi-GPU Sovereignty & Cross-Vendor Parity
**Iteration**: 32
**From**: coralReef
**To**: All primals (hotSpring, groundSpring, neuralSpring, wetSpring, airSpring)

---

## Summary

Iteration 32 focuses on deep debt resolution: implementing missing math
functions, closing AMD encoding gaps, eliminating production placeholders,
smart refactoring, and expanding test coverage with 19 new integration tests.

## Changes

### New Math Functions (NV + AMD)

- **`firstTrailingBit(x)`** — lowered as `clz(reverseBits(x))` via
  `OpBRev` + `OpFlo`. Correctly uses `return_shift_amount: true` for
  count-leading-zeros semantics on the bit-reversed input.
- **`distance(a, b)`** — lowered as `length(a - b)` via component-wise
  `OpFAdd` with negated source, delegating to `translate_length`.

### AMD Encoding Fixes

- **`OpBRev`** — VOP1 `V_BFREV_B32`. Closes the "discriminant 31" gap
  that caused `CompileError::NotImplemented` on AMD for `reverseBits`
  and `firstTrailingBit`.
- **`OpFlo`** — VOP1 `V_FFBH_U32`/`V_FFBH_I32`. For the
  `return_shift_amount: false` case (firstLeadingBit semantics),
  emits `V_SUB_NC_U32(31, ffbh)` + `V_CMP_NE_U32` + `V_CNDMASK_B32`
  to preserve ~0 on zero inputs.

### Production Placeholder Elimination

- **`CallResult → OpUndef`** replaced with `CompileError::InvalidInput`
  (was silently emitting undefined values on a code path that should
  never be reached in valid naga IR).
- **`BindingArray` stride** changed from hardcoded `1` to recursive
  `array_element_stride(*base)` lookup.

### Smart Refactoring

- **`shader_info.rs`** (814 LOC) split into three focused modules:
  - `shader_io.rs` (168 LOC) — IO metadata (SysValInfo, VtgIoInfo, FragmentIoInfo)
  - `shader_model.rs` (337 LOC) — ShaderModel trait, ShaderModelInfo, occupancy helpers
  - `shader_info.rs` (306 LOC) — stage types, ShaderInfo, Shader, ISBE analysis

### Audits

- **Production mocks**: All mocks confirmed test-only. `coral-reef-stubs`
  is a real implementation crate (pure Rust replacements for C deps).
- **Dependencies**: 26/28 external deps are pure Rust. Only C transitive
  dep is `tokio → mio → libc` (tracked for rustix migration at mio#1735).
  No banned deps (openssl, ring, etc.). `naga` v28 from crates.io.
- **EVOLUTION markers**: All 9 markers still valid future work.

### Test Expansion (+47 tests)

19 new WGSL integration tests covering:
- Interpolation: `mix`, `step`, `smoothstep`, `sign`
- Trigonometry: `tan`, `atan`, `atan2`, `asin`, `acos`
- Exponential/hyperbolic: `exp`, `log`, `tanh`, `sinh`, `cosh`, `asinh`, `acosh`, `atanh`
- Atomics: `Add`, `Min`, `Max`, `And`, `Or`, `Xor`, `Exchange`
- Builtins: `WorkGroupId`, `NumWorkGroups`, `LocalInvocationIndex`
- Float modulo, uniform matrix loads, signed bit operations
- RDNA2 variants for all new paths

### Doc Updates

- All root docs updated: README, STATUS, EVOLUTION, WHATS_NEXT, ABSORPTION,
  CONTRIBUTING, START_HERE, HARDWARE_TESTING
- Test counts: 1509 → 1556 passing, 54 ignored (stable)
- Coverage: 63% → 64%
- `EVOLUTION.md`: `firstTrailingBit` marked complete, `Distance` added
- `genomebin/manifest.toml`: `shader.compile.wgsl.multi` capability added

## Metrics

| Metric | Before (Iter 31) | After (Iter 32) |
|--------|-------------------|------------------|
| Tests passing | 1509 | 1556 |
| Tests ignored | 54 | 54 |
| Line coverage | 63% | 64% |
| Clippy warnings | 0 | 0 |
| Production unwrap/todo | 0 | 0 |
| EVOLUTION markers | 9 | 9 |
| Max file LOC | 925 | 925 |

## Impact on Other Primals

- **hotSpring**: `firstTrailingBit` now compiles for both NV and AMD.
  Any shaders using bit scanning can now be absorbed.
- **groundSpring**: `distance()` now available for spatial computation shaders.
- **neuralSpring**: Atomic operations (Min, Max, And, Or, Xor, Exchange)
  now have expanded test coverage. `atomicSub` triggers a copy-prop
  assertion — tracked for Iteration 33.
- **All**: AMD RDNA2 parity improved — `reverseBits`, `firstTrailingBit`,
  `firstLeadingBit` all encode correctly now.

## Known Issues / Next Steps

- `atomicSub` triggers `assertion failed: src.is_unmodified()` in
  `opt_copy_prop` — the negation modifier on the subtract operand
  isn't handled by copy propagation. Workaround: use `atomicAdd` with
  negated value.
- Coverage 64% → 90% target: remaining gap is primarily auto-generated
  ISA tables, legacy SM20/32/50 encoder paths, hardware-dependent driver
  code, and constant folding (invisible in output).
- `quick-xml` 0.37 → 0.39 upgrade for `amd-isa-gen` tool.
