# coralReef Iteration 70d — CPU Backend + barraCuda Shader Validation

**Date**: March 30, 2026
**Primal**: coralReef (sovereign GPU compiler)
**Phase**: 10 — Iteration 70d
**Triggered by**: barraCuda team proposal for Sovereign Compiler Evolution: CPU Compilation + Shader Validation

---

## Summary

coralReef now supports CPU-side shader execution and tolerance-based validation.
Three new JSON-RPC methods are available on all IPC transports (newline-delimited UDS/TCP,
jsonrpsee HTTP, tarpc bincode). barraCuda and toadStool can validate GPU outputs against
CPU reference executions without leaving the primal IPC surface.

---

## New Capabilities

### `shader.compile.cpu`

Parses and validates WGSL source via Naga, returns compilation confirmation.
Consumers can check whether a shader is valid before executing.

- **Transport**: newline JSON-RPC, jsonrpsee HTTP, tarpc
- **Input**: `CompileCpuRequest { wgsl_source, entry_point? }`
- **Output**: `CompileResponse { success, size, errors }`

### `shader.execute.cpu`

Executes a WGSL compute shader on the host CPU using a Naga IR tree-walk interpreter.
Supports native f64 arithmetic — the primary motivation for CPU execution.

- **Transport**: newline JSON-RPC, jsonrpsee HTTP, tarpc
- **Input**: `ExecuteCpuRequest { wgsl_source, entry_point?, workgroups, bindings, uniforms }`
- **Output**: `ExecuteCpuResponse { bindings, execution_time_ns }`
- **Supported**: storage buffers (read/write), uniform buffers, `global_invocation_id`,
  `local_invocation_id`, `workgroup_id`, `num_workgroups`; scalar f32/f64/u32/i32/bool;
  vectors; 25+ math functions; binary/unary/cast/comparison operators; loops with break_if

### `shader.validate`

Compares CPU execution output against expected GPU output using configurable tolerances.
Returns per-binding mismatch reports with element indices and actual vs expected values.

- **Transport**: newline JSON-RPC, jsonrpsee HTTP, tarpc
- **Input**: `ValidateRequest { wgsl_source, entry_point?, workgroups, bindings, uniforms, expected, tolerance }`
- **Output**: `ValidateResponse { valid, mismatches }`
- **Tolerance model**: `absolute_tolerance` (default 1e-6) + `relative_tolerance` (default 1e-4)

### Capability Advertisement

`shader.compile.capabilities` response now includes:
- `cpu_archs: ["{current_arch}"]`
- `supports_cpu_execution: true`
- `supports_validation: true`

Discovery manifest (`capabilities.list`) includes all three new methods.

---

## Architecture

### coral-reef-cpu crate

New workspace member: pure Rust, `#![forbid(unsafe_code)]`, `#![warn(missing_docs)]`.

| Module | Lines | Role |
|--------|-------|------|
| `types.rs` | ~170 | Wire types (requests, responses, errors, tolerances) |
| `interpret/mod.rs` | 612 | Orchestration: parse, validate, dispatch workgroups, eval_expr |
| `interpret/eval.rs` | 687 | Pure evaluation: literals, binary/unary, math, cast, pointer I/O |
| `validate.rs` | ~170 | Tolerance comparison engine |

Dependencies: `naga` (wgsl-in), `bytes`, `serde`, `serde_json`, `thiserror`, `tracing`.

### IPC Wiring (coralreef-core)

- `service/cpu.rs`: service handlers mapping `CpuError` → `CompileError`
- `ipc/newline_jsonrpc.rs`: dispatch arms for 3 new methods
- `ipc/jsonrpc.rs`: `CoralReefRpc` trait extended
- `ipc/tarpc_transport.rs`: `ShaderCompileTarpc` trait extended
- `capability.rs`: 3 new `Capability` entries

---

## barraCuda Integration Path

barraCuda can now validate GPU shader outputs against CPU reference:

1. **Compile**: `shader.compile.wgsl` → GPU binary (existing)
2. **Dispatch**: toadStool / coral-driver → GPU execution → output bindings
3. **Validate**: `shader.validate` → pass GPU output as `expected`, tolerance-compare against CPU

The CPU interpreter supports the compute shader subset used by barraCuda's sigmoid,
ReLU, and tensor operations. f64 transcendentals (exp, log, pow, sin, cos, etc.)
execute with native CPU precision.

### What works now
- `shader.compile.cpu` — parse/validate any WGSL compute shader
- `shader.execute.cpu` — execute with bindings and workgroup dispatch
- `shader.validate` — tolerance comparison for f32 outputs

### Follow-on (not blocking)
- Cranelift JIT backend behind `cpu-jit` feature flag (Phase 2 from proposal)
- Switch statement support in interpreter (logged as tracing::warn)
- Struct-typed bindings (currently flattened to scalar arrays)

---

## Build Health

| Check | Status |
|-------|--------|
| `cargo fmt --check` | **PASS** |
| `cargo clippy --all-features -D warnings` | **PASS** (0 warnings) |
| `cargo test --all-features` | **PASS** (3270+ tests, 0 failures) |
| Production files >1000 LOC | **0** (interpret.rs split: 1170 → 612 + 687) |
| `#![forbid(unsafe_code)]` on coral-reef-cpu | **Yes** |

---

## Audience

- **barraCuda**: CPU validation path is ready. Call `shader.validate` via JSON-RPC on coralReef's UDS.
- **toadStool**: Compile→dispatch→validate chain is wired. The sovereign dispatch step is toadStool's responsibility.
- **ludoSpring**: exp085 test 8/8 (sigmoid_output_matches_cpu) can now use `shader.validate` for the comparison step.
- **primalSpring**: Three new capabilities to probe during composition validation sweeps.
- **biomeOS**: Neural API can auto-discover the new capabilities via `capabilities.list`.
