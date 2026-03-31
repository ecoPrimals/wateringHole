# coralReef Iteration 70e — CoralIR Cranelift JIT Backend + Dual-Path Validation

**Date**: March 30, 2026
**Primal**: coralReef (sovereign GPU compiler)
**Phase**: 10 — Iteration 70e
**Triggered by**: JIT backend evolution from Iter 70d CPU interpreter foundation

---

## Summary

coralReef now has a Cranelift-based JIT backend (`coral-reef-jit`) that translates
CoralIR directly to native x86-64/aarch64 machine code for CPU shader execution.
This is "Path B" in the dual-path validation architecture: Path A (Naga IR
interpreter from Iter 70d) provides reference results, Path B (Cranelift JIT)
provides high-performance native execution. Consumers can compare both paths
for tolerance-based shader correctness validation.

The IR translation layer was polished for idiomatic Rust, brought under the 1000-line
limit, and expanded with comprehensive test coverage.

---

## New Crate: `coral-reef-jit`

### Architecture

```
CoralIR Shader
     │
     ▼
FunctionTranslator  (translate.rs, 994 lines)
├── Op → CLIF instruction mapping
├── System register mapping  (builtins.rs)
├── Comparison codes          (cmp_codes.rs)
└── Buffer memory management  (memory.rs)
     │
     ▼
Cranelift JITModule
├── compile() → native function pointer
├── workgroup dispatch (1D/2D/3D)
└── BindingBuffers ownership model
     │
     ▼
execute_jit() entry point  (lib.rs)
├── tracing instrumentation
├── execution time reporting
└── mutable buffer results
```

### Op Coverage

| Category | Ops |
|----------|-----|
| Float arithmetic | FAdd, FSub, FMul, FFma, FMnMx, FNeg, FAbs |
| Integer arithmetic | IAdd, IMul (with `unify_int_widths` for mixed i32/i64) |
| Comparisons | FSetP (all FloatCC), ISetP (all IntCC) via extracted `cmp_codes.rs` |
| Memory | Ld, St (via binding buffer pointer offsets) |
| Control flow | Bra, Exit |
| Type conversion | F2F, F2I, I2F, I2I |
| Rounding | FRnd (NearestEven→nearest, Zero→trunc, NegInf→floor, PosInf→ceil) |
| Transcendentals | exp2f, log2f, sinf, cosf, tanhf, sqrtf via `call_libm` helper |
| System registers | GlobalInvocationId, WorkGroupId, LocalInvocationId |
| Phi nodes | PhiSrcs/PhiDsts via Cranelift `Variable` system |
| Misc | Mov, Undef (→ iconst 0), Sel (conditional select) |

### Known Limitation

CoralIR lowers WGSL `var` mutable loop variables into register-addressed memory
loads (e.g., `Ld [R0+offset]`). On GPU, R0 (zero register) + offset addresses
local scratchpad memory. In the JIT, this translates to a null pointer dereference.
The `for_loop_accumulation` test is `#[ignore]` pending local scratch memory
emulation — a future evolution path.

---

## Idiomatic Polish (translate.rs 1101→994 lines)

| Change | Impact |
|--------|--------|
| `cmp_codes.rs` extraction | Comparison code conversion (`float_cmp_to_cc`, `int_cmp_to_cc`) with `#[must_use]` |
| `entry_block_params()`/`bindings_ptr()`/`offset_ptr()` helpers | CBuf resolution deduplication |
| Unified `call_libm` with `Result` | Error propagation instead of `expect()` |
| `unify_int_widths` helper | Mixed i32/i64 arithmetic deduplication |
| `apply_rnd_mode` helper | All FRndMode variants mapped correctly |
| Dead `BindingLayout` removed from `memory.rs` | Dead code elimination |
| JIT fn pointer hoisted outside dispatch loop | Performance: avoids redundant `transmute` per invocation |
| `SysRegMapping` derives `Debug, Clone, Copy` | Idiomatic enum |
| `tracing::instrument` on `execute_jit` | Observability |
| Cranelift 0.130.0 API migration | `Variable::new` → `builder.declare_var(ty)` |

---

## Test Coverage

27 tests (23 integration + 4 unit):

| Test | Category |
|------|----------|
| `add_two_buffers` | Arithmetic |
| `subtract_buffers` | Arithmetic |
| `fused_multiply_add` | Arithmetic |
| `negative_float_values` | Arithmetic |
| `multiply_by_scalar_immediate` | Arithmetic + CBuf |
| `min_max_clamp` | Control flow |
| `conditional_select` | Control flow |
| `two_dimensional_workgroups` | Workgroup dispatch |
| `three_dimensional_workgroups` | Workgroup dispatch |
| `larger_buffer_64_elements` | Workgroup dispatch |
| `in_place_square` | In-place mutation |
| `dual_path_conditional_consistency` | Dual-path validation |
| `barracuda_leaky_relu_validation` | barraCuda-style validation |
| `empty_shader_no_bindings` | Edge case |
| `execution_reports_nonzero_time` | Execution metrics |
| `for_loop_accumulation` | Loop patterns (`#[ignore]`) |
| `workgroup_size_extraction_defaults_to_one` | Unit test |
| `round_trip_preserves_data` | Memory unit test |
| `empty_bindings` | Memory unit test |

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo clippy -p coral-reef-jit -- -D warnings` | PASS (0 warnings) |
| `cargo fmt --check -p coral-reef-jit` | PASS |
| `cargo test -p coral-reef-jit` | PASS (23 integration + 4 unit, 1 `#[ignore]`) |
| `cargo test -p coralreef-core` | PASS (no regressions) |
| All production files < 1000 LOC | PASS (translate.rs: 994) |

---

## Ecosystem Impact

- **barraCuda**: Can now use Cranelift JIT for fast CPU-side shader validation (Path B) alongside Naga interpreter (Path A). `barracuda_leaky_relu_validation` test demonstrates the pattern.
- **toadStool**: Dual-path validation available for shader dispatch confidence checks.
- **hotSpring**: CoralIR JIT provides a CPU execution path for shader debugging without GPU hardware.

---

## Next Steps

1. **Local scratch memory emulation** — allocate per-invocation scratch buffer to unblock `for` loop patterns
2. **Wire JIT execution into JSON-RPC** — `shader.execute.jit` method for high-performance CPU execution
3. **Expand Op coverage** — remaining CoralIR ops (Shf, Prmt, Bar, Vote, etc.)
4. **Coverage push** — target 90% on `coral-reef-jit` via additional edge case tests

---

*4070+ tests passing, ~122 ignored hardware-gated, ~66% workspace line coverage.
Zero clippy warnings. Zero fmt drift. Zero files over 1000 LOC.
All pure Rust. Sovereignty is a runtime choice.*
