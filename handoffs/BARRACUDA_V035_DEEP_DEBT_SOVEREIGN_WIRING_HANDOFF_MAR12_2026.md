# barraCuda v0.3.5 — Deep Debt & Sovereign Wiring Handoff

**Date**: 2026-03-12
**Commit**: `66182d9`
**Scope**: Sovereign dispatch wiring, capability-based discovery, smart refactoring, external dep audit

## Summary

Closed **Gap 1** from the Sovereign Compute Trio Wiring Gaps analysis.
The coral compiler cache is now wired to `CoralReefDevice::dispatch_compute`,
enabling cached native binaries to be dispatched without recompilation.
All hardcoded primal identifiers evolved to capability-based constants.
Smart refactoring of large files. Comprehensive external dependency audit.

## Changes

### 1. Coral Cache → Dispatch Wiring (Gap 1 Closure)

- `CoralReefDevice::dispatch_compute` now checks `NATIVE_BINARY_CACHE`
  (populated by `spawn_coral_compile`) before calling `ctx.compile_wgsl()`.
- New `try_coral_cache()` helper iterates architectures (`sm_70`..`gfx1100`)
  to find pre-compiled binaries for the given shader source.
- On cache hit, constructs `CompiledKernel` and inserts into local cache.
- `dispatch_binary` and `dispatch_kernel` methods implemented on
  `CoralReefDevice` for raw binary and full-metadata dispatch paths.

### 2. PRIMAL_NAMESPACE Constant

- `PRIMAL_NAMESPACE: &str = "barracuda"` added to `barracuda-core/src/lib.rs`.
- Replaced hardcoded `"barracuda"` in: `rpc.rs`, `ipc/methods.rs`,
  `ipc/transport.rs` (socket paths), `bin/barracuda.rs` (PID file paths).

### 3. ODE Solver Refactoring

- `ode_generic.rs` (890 lines) split into `ode_generic/mod.rs` (613 lines)
  + `ode_generic/wgsl_templates.rs` (290 lines).
- WGSL RK4 template codegen cleanly separated from solver trait/struct logic.

### 4. External Dependencies Audit

- `pollster`: Justified — minimal `block_on` for sync wgpu enumeration.
- `futures`: Justified — transitive dep of `tarpc`, required for stream API.
- `half`: Justified — IEEE 754 binary16 for quantized tensor support.
- All confirmed pure Rust, no C deps.

### 5. Production Safety Audit

- All `unwrap()`/`expect()` confirmed: test-only, doc examples, or
  ownership-invariant guards with provably-unreachable panic paths.
- Zero inappropriate uses in production code.

## Impact for Other Primals

### coralReef
- Gap 1 closure means compiled binaries are now consumed by barraCuda's
  dispatch path. The compile→cache→dispatch pipeline is complete.
- Remaining gaps: 2 (NVIDIA proprietary), 3 (FECS), 4 (RegisterAccess),
  5 (multi-arch classifier), 6 (cross-gen learning).

### toadStool
- `PRIMAL_NAMESPACE` pattern ready for adoption by other primals.

### Springs
- No breaking changes. All 3,348 tests continue to pass.

## Files Modified

- `crates/barracuda/src/device/coral_reef_device.rs` (dispatch wiring)
- `crates/barracuda-core/src/lib.rs` (PRIMAL_NAMESPACE)
- `crates/barracuda-core/src/rpc.rs` (namespace constant)
- `crates/barracuda-core/src/ipc/methods.rs` (namespace constant)
- `crates/barracuda-core/src/ipc/transport.rs` (socket path)
- `crates/barracuda-core/src/bin/barracuda.rs` (PID file path)
- `crates/barracuda/src/numerical/ode_generic/mod.rs` (refactored)
- `crates/barracuda/src/numerical/ode_generic/wgsl_templates.rs` (new)
