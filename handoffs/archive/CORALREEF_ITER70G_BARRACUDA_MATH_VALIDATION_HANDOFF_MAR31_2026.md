# coralReef Iter 70g — barraCuda Math Validation + Interpreter/JIT Gap Closure

**Date**: March 31, 2026
**Priority**: P1 — CRITICAL (unlocks cross-primal math validation)
**Scope**: CoralIR interpreter shared memory, cooperative scheduling, WGSL fixture vendoring

---

## Summary

coralReef's CoralIR interpreter and sovereign Cranelift JIT now validate the full
range of barraCuda compute shader patterns — from elementwise activations through
shared-memory tiled matrix multiplication. This was achieved by closing three
major interpreter gaps: for-loop support with mutable locals, `var<workgroup>`
shared memory, and cooperative barrier scheduling.

The validation used a **short-term dev-dependency pattern**: barraCuda's WGSL
shader patterns were absorbed as inline test WGSL, validated through the
triple-path pipeline (CoralIR interpreter + sovereign JIT + expected values),
then vendored as standalone `.wgsl` fixtures. No runtime barraCuda dependency
exists — ongoing validation uses JSON-RPC IPC (`shader.validate`,
`shader.execute.cpu`).

## What Changed

### CoralIR Interpreter (`coral-reef-cpu`)

- **Cooperative workgroup scheduling**: `execute_workgroup` runs all invocations
  within a workgroup in lock-step, pausing at `workgroupBarrier()` until all
  threads synchronize. Uses snapshot-based shared memory reads with per-thread
  write buffers to correctly model GPU memory visibility semantics.

- **Shared memory ops**: `Op::Ld` and `Op::St` for `MemSpace::Shared` route
  through the cooperative scheduler's write buffer (self-writes visible
  immediately) and snapshot (cross-thread reads see previous barrier phase).
  `Op::Atom` operates directly on shared memory for immediate global visibility.

- **For-loop mutable locals**: Fixed Naga translation to correctly initialize
  local variables via `apply_local_var_inits` (translates `LocalVariable::init`
  through `ensure_expr` to produce correct SSA, avoiding SM50 constant
  propagation issues).

- **Funnel shift**: Added `Op::Shf` handler for tree-reduce bit manipulation.

- **Module extraction**: `workgroup.rs` submodule contains cooperative scheduling
  logic (`execute_workgroup`, `step_invocation`, `InvocationState`). `mem_ops.rs`
  contains memory access helpers. `mod.rs` stays under 1000 lines.

### CoralIR Codegen (`coral-reef`)

- **Shared memory layout**: `compute_shared_mem_layout` computes byte offsets
  for all `var<workgroup>` globals. `FuncTranslator` tracks shared pointers
  via `shared_ptrs: HashSet` and routes loads/stores to `MemSpace::Shared`.

- **SM50 compatibility**: Modified `Src::as_imm_not_i20` / `as_imm_not_f20`
  to gracefully handle modified immediate sources (e.g., `INeg(imm32(val))`)
  by returning `Some(i)` instead of asserting, allowing the legalization pass
  to force register copies.

### Sovereign JIT (`coral-reef-jit`)

- **Phi type coercion**: JIT phi-variable handling now bitcasts incoming values
  when types mismatch the declared phi type, fixing loop-carried variable issues.

- **Shared memory deferred**: `Op::Ld`/`Op::St` for `MemSpace::Shared` return
  `JitError::UnsupportedOp` — JIT shared memory is future work (interpreter
  provides the validation path for now).

## Validated Shaders (22 Fixtures)

Vendored in `coral-reef-jit/tests/fixtures/barracuda/`:

| Tier | Category | Shaders | Validation Path |
|------|----------|---------|-----------------|
| 0 | Activation | relu, sigmoid, leaky_relu, elu, silu, hardsigmoid, hardtanh | Triple-path (interp + JIT + expected) |
| 0 | Elementwise | add, sub, mul, fma | Triple-path |
| 0 | Unary | abs, sqrt, sign | Triple-path |
| 1 | Loop accumulator | scalar_dot_product, scalar_sum_reduce, scalar_mean, scalar_variance | Triple-path |
| 2 | Shared reduction | sum_reduce_workgroup, max_reduce_workgroup | Interpreter-only (JIT deferred) |
| 3 | Tiled shared | layer_norm, tiled_matmul_2x2 | Interpreter-only (JIT deferred) |

**Tolerance**: All f32 shaders validated within `1e-5` absolute + relative.

## Test Count

- **46 tests** in `coral-reef-jit` (was 12 pre-evolution)
- **12 unit tests** in `coral-reef-jit` core
- Zero clippy warnings (`clippy::pedantic` + `clippy::nursery`, `-D warnings`)

## IPC Validation Path for barraCuda

barraCuda uses coralReef for math validation via JSON-RPC (no compile-time dep):

```json
{"jsonrpc": "2.0", "method": "shader.validate", "params": {
    "wgsl_source": "<shader>",
    "workgroups": [1, 1, 1],
    "bindings": [...],
    "expected": [{"group": 0, "binding": 0, "data": "<base64>", "tolerance": {"abs": 1e-5, "rel": 1e-5}}]
}, "id": 1}
```

Returns `{pass: true/false, mismatches: [...]}`.

For raw execution:
```json
{"jsonrpc": "2.0", "method": "shader.execute.cpu", "params": {
    "wgsl_source": "<shader>",
    "workgroups": [1, 1, 1],
    "bindings": [...],
    "strategy": "interpret"
}, "id": 2}
```

## Remaining Gaps

| Gap | Status | Notes |
|-----|--------|-------|
| JIT shared memory | Deferred | `MemSpace::Shared` returns `UnsupportedOp` in JIT; interpreter validates |
| `MemSpace::Local` | Deferred | No barraCuda shaders exercise local scratch directly |
| Atomics (Tier 4) | Deferred | `Op::Atom` works in interpreter; JIT deferred |
| Warp ops (shuffle, vote) | Deferred | Not needed for barraCuda math patterns |
| f64 shared memory | Untested | Codegen supports it; no test fixture yet |

## Cross-References

- Previous handoff: `CORALREEF_ITER70D_CPU_BACKEND_BARRACUDA_EVOLUTION_HANDOFF_MAR30_2026.md`
- CoralIR coevolution plan: `CORALREEF_ITER70F_CORALIR_COEVOLUTION_SOVEREIGN_JIT_HANDOFF_MAR30_2026.md`
- barraCuda formula gaps: `BARRACUDA_FORMULA_GAPS_HANDOFF_MAR31_2026.md`
- Sovereign compute evolution: `SOVEREIGN_COMPUTE_EVOLUTION.md`
