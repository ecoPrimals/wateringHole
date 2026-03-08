# coralReef — Phase 10 Iteration 12: Compiler Gaps + Math Coverage + Cross-Spring Wiring

**Date**: March 8, 2026
**Primal**: coralReef
**From**: Iteration 11 (Deep Debt Reduction) → Iteration 12 (Gap Closure + Math + Wiring Guide)

---

## Summary

Iteration 12 closes 2 of 4 compiler gaps, adds 6 naga math/bit operations, fixes
cross-register-file coercion in the copy lowering pass, and publishes a wiring
guide for springs to test the sovereign GPU pipeline on Titan V / RTX 3090.

## Metrics

| Metric | Value |
|--------|-------|
| Total tests | 991 |
| Passing | **955** (was 954) |
| Ignored | **36** (was 37) |
| Clippy warnings | 0 |
| Production `unwrap()`/`todo!()` | 0 |
| `#[deny(unsafe_code)]` crates | 6/8 |
| AMD E2E status | Verified (RX 6950 XT) |
| NVIDIA E2E status | Fully wired, awaiting hardware validation |

## Key Changes

### 1. Compiler Gap: GPR→Pred Coercion (FIXED — semf_batch now passes)

`translate_if` and `break_if` in `func_control.rs` now coerce GPR condition
values to Pred via `OpISetP { cmp_op: Ne, srcs: [gpr, 0] }` before feeding
them to `OpBra.cond`. Previously, any if-condition that wasn't already in Pred
file caused an encoder assertion. This pattern mirrors the existing coercion in
`translate_select`.

**Files**: `crates/coral-reef/src/codegen/naga_translate/func_control.rs`

### 2. Compiler Gap: const_tracker Negated Immediates (FIXED)

`ConstTracker` now stores `Src` (including modifiers) instead of bare `SrcRef`.
Negated immediates like `fneg(Imm32(1.0))` are tracked as rematerializable
constants. The spiller can now fill these values without assertion failures.

Guard: modified constants are not tracked for Pred-file destinations (different
modifier semantics).

**Files**: `crates/coral-reef/src/codegen/const_tracker.rs`,
`crates/coral-reef/src/codegen/spill_values/types.rs`,
`crates/coral-reef/src/codegen/legalize.rs`

### 3. Cross-File Copy Lowering (NEW)

`lower_copy_swap.rs` now handles:
- **Pred→GPR**: `OpSel { cond: pred, srcs: [1, 0] }` (materializes boolean as integer)
- **True/False→GPR**: `OpMov` with immediate `1` / `0`
- **GPR.bnot→Pred**: `OpISetP { Eq, gpr, 0 }` (integer-to-predicate with negation)
- **Modified Pred→Pred**: Evaluates effective boolean and emits `lop2_to`

**Files**: `crates/coral-reef/src/codegen/lower_copy_swap.rs`

### 4. Math Function Coverage (6 new naga→IR→encode paths)

| Function | naga variant | IR Op | Status |
|----------|-------------|-------|--------|
| `tan(x)` | `MathFunction::Tan` | sin/cos + rcp (f32) or f64 lower | ✅ NEW |
| `countOneBits(x)` | `MathFunction::CountOneBits` | `OpPopC` | ✅ NEW |
| `reverseBits(x)` | `MathFunction::ReverseBits` | `OpBRev` | ✅ NEW |
| `firstLeadingBit(x)` | `MathFunction::FirstLeadingBit` | `OpFlo` (signed) | ✅ NEW |
| `countLeadingZeros(x)` | `MathFunction::CountLeadingZeros` | `OpFlo` (shift) | ✅ NEW |
| `is_signed_int_expr()` | Helper | — | ✅ NEW |

**Files**: `crates/coral-reef/src/codegen/naga_translate/func_math.rs`,
`crates/coral-reef/src/codegen/naga_translate/expr.rs`

### 5. Type Helper: `is_signed_int_expr`

New helper on `FuncTranslator` to determine if an expression handle resolves to
`ScalarKind::Sint`. Used by `FirstLeadingBit` to select signed vs unsigned FLO.

## Remaining Gaps

### P1 — Register Allocator SSA Tracking

**Blocks**: `su3_gauge_force_f64`, `wilson_plaquette_f64`
**Error**: `Unknown SSA value %rN (file=GPR) — not in active regs or evicted set`
**Root cause**: Complex array-indexed values across loop boundaries are not
properly tracked by the RA's liveness analysis. Requires extending `BlockLiveness`
for array-backed live-in values.

### P1 — Pred→GPR Encoder Coercion Chain

**Blocks**: `batched_hfb_hamiltonian_f64`, `coverage_logical_predicates`
**Error**: `Invalid ALU register file` (Pred register in ISetP ALU source)
**Root cause**: After const_tracker and lower_copy fixes, some paths still produce
`OpISetP` instructions with Pred-file values in ALU source positions. Needs a
legalize pass that inserts `OpSel { pred, 1, 0 }` before any ALU op that has a
Pred source in a GPR slot.

### P2 — Missing Math (need polynomial lowering)

`asin`, `acos`, `atan`, `atan2`, `sinh`, `cosh`, `tanh`, `firstTrailingBit`

---

## Cross-Spring Wiring Guide: Testing coralReef on Titan V / RTX 3090

### Prerequisites

1. `coralReef` repo cloned on the target machine
2. NVIDIA GPU present: Titan V (SM70) or RTX 3090 (SM86)
3. `amdgpu` or `nouveau` DRM accessible (check `/dev/dri/renderD128`)
4. Rust toolchain (stable 1.92+)

### Quick Validation (No Hardware Required)

```bash
cd coralReef
cargo test --workspace
# Expected: 955 passed, 36 ignored, 0 failed
```

### NVIDIA Hardware E2E Test

The hardware integration test is in `crates/coral-driver/tests/hw_nv_e2e.rs`.
It requires a real NVIDIA GPU accessible via the `nouveau` DRM driver.

```bash
# Check for nouveau DRM device
ls /dev/dri/renderD*

# Run the NVIDIA hardware E2E test (ignored by default — needs real GPU)
cargo test --test hw_nv_e2e -- --include-ignored

# Or run all hardware tests (AMD + NVIDIA)
cargo test -- --include-ignored hw_
```

### IPC Contract for Spring Integration

coralReef exposes a compiler service via IPC. The contract:

**Request**: `shader.compile.wgsl`
```json
{
  "source": "<WGSL source string>",
  "arch": "sm70" | "sm86" | "gfx1030",
  "f64_strategy": "native" | "software_lower"
}
```

**Response**:
```json
{
  "binary": "<base64-encoded GPU binary>",
  "info": {
    "num_gprs": 32,
    "shared_mem": 0,
    "slm_size": 0
  }
}
```

### For groundSpring

groundSpring performs lattice QCD calculations. Key shaders that exercise the
pipeline:

- `su3_gauge_force_f64.wgsl` — SU(3) gauge force (BLOCKED: RA SSA tracking)
- `wilson_plaquette_f64.wgsl` — Wilson plaquette (BLOCKED: RA SSA tracking)
- Simpler f64 kernels (matrix multiply, reduction) should work now

**Recommended test**: Write a simple f64 dot product or matrix-vector multiply
WGSL shader and dispatch via `coral-gpu` or `coral-driver` directly.

### For neuralSpring

neuralSpring performs neural network inference. Relevant capabilities:

- f32 transcendentals: sin, cos, exp, log, sqrt, rsqrt, tan (all working)
- f64 transcendentals: sin, cos, exp2, log2, sqrt (all working via polynomial lower)
- Bitwise: countOneBits, reverseBits, firstLeadingBit, countLeadingZeros (NEW)
- FMA, pow, min, max, clamp, abs, floor, ceil, round (all working)

**Recommended test**: Compile an activation function kernel (ReLU, GELU, SiLU)
targeting SM70 or SM86.

### For wetSpring

wetSpring performs fluid dynamics. Key patterns:

- Array indexing + boundary checks (arrayLength now works with comparisons)
- f64 arithmetic chains (add, sub, mul, fma — all verified)
- Conditional branches with float comparisons (GPR→Pred coercion fixed)

**Recommended test**: Compile a simple stencil or finite-difference kernel.

### Dispatch via coral-gpu (Rust API)

```rust
use coral_gpu::{GpuDevice, ShaderSource, DispatchConfig};

let device = GpuDevice::open()?;          // auto-detects GPU
let shader = ShaderSource::Wgsl(wgsl_src);
let binary = device.compile(shader)?;
let result = device.dispatch(binary, &buffers, dispatch_dims)?;
```

### Dispatch via coral-driver (Low-Level)

```rust
use coral_driver::nv::NvDevice;

let dev = NvDevice::open("/dev/dri/renderD128")?;
let buf = dev.alloc_buffer(size, MemoryDomain::GTT)?;
dev.dispatch(shader_binary, &shader_info, &[buf], dims)?;
let data = dev.read_buffer(&buf)?;
```

---

## Action Items for Springs

1. **All springs**: Run `cargo test --workspace` to verify baseline
2. **groundSpring**: Test simple f64 kernels; complex lattice shaders blocked on RA
3. **neuralSpring**: Test activation function compilation targeting SM70/SM86
4. **wetSpring**: Test stencil kernels with boundary checks
5. **All springs**: Report any `NotImplemented("math function ...")` errors — these
   indicate missing naga→IR paths that can be wired quickly

## Pin Versions

| Spring | Version |
|--------|---------|
| coralReef | Phase 10 Iteration 12 |
| groundSpring | V96 |
| neuralSpring | V89/S131 |
| wetSpring | V97e |
| airSpring | V0.7.3 |
| barraCuda | V0.33 |
