# barraCuda — Wave 157a Deep Debt + ComputeDispatch P0 (strandGate)

**Date**: Aug 7, 2026
**Gate**: strandGate
**Team**: Compute Trio — barraCuda
**Wave**: 157a

---

## Summary

Three commits this wave:
1. Error constructor helper migration Phase 3 + magic number centralization +
   protocol negotiation zero-alloc + G68 Platform Substrate audit (20 files).
2. Deprecated batch unwiring + pool2d dedup + env var centralization (9 files).
3. **ComputeDispatch P0 migration** — all 92 `*_wgsl.rs` ops migrated from manual
   BGL→pipeline boilerplate to `ComputeDispatch` builder (92 files, −10,771 LOC).

Total: 95 files changed. 4,990 tests pass. Zero clippy warnings.

## Changes

### Error Constructor Migration (Phase 3)

Remaining verbose `BarracudaError` struct literal patterns → helper calls:

| Pattern | Files | Helper |
|---------|-------|--------|
| `InvalidOperation { op, reason }` | `snn.rs`, `esn_v2/model.rs`, `esn_v2/multi_head.rs`, `ops/mha/mod.rs` | `invalid_op()` |
| `InvalidInput { message }` | `cpu_executor/storage.rs`, `npu_executor.rs` | `invalid_input()` |
| `Device("...".into())` | `sovereign_device.rs`, `sovereign_dispatch_wire.rs`, `fhe_poly_add.rs`, `complex/div.rs` | `device()` |
| `Gpu("...".to_string())` | `gpu_executor/storage.rs`, `interpolate/cubic_spline.rs` | `gpu()` |
| `DeviceLost("...".into())` | `bipartition_encode.rs`, `vpc_simulate.rs`, `foce_gradient.rs` | `device_lost()` |

### New Error Helper: `device_ctx()`

Added `BarracudaError::device_ctx(context, err)` — mirrors existing `gpu_ctx()` for
the `Device` variant. Used in `sovereign_dispatch_wire.rs` for TCP connect wrapping.

### `gpu_ctx()` Bulk Migration

Migrated 40 `Gpu(format!("ctx: {e}"))` patterns in `dispatch/domain_ops.rs` to
`gpu_ctx("ctx", e)`. Eliminates per-call `format!` allocation when wrapping errors.

### Magic Number Centralization

| Constant | Value | File |
|----------|-------|------|
| `SOFTPLUS_UPPER_THRESHOLD` | `20.0` | `activations.rs` |
| `DEFAULT_FITTS_HICK_B` | `0.155` | `ipc/methods/math.rs` |

### Protocol Negotiation Zero-Alloc

Replaced `name.trim().to_ascii_lowercase().as_str()` (allocates `String` per connection)
with `trimmed.eq_ignore_ascii_case()` in `IpcProtocol::from_negotiation_name()`.

### G68 Platform Substrate Audit

barraCuda confirmed **CLEAN** for G68:
- All `#[cfg(unix)]` is in the transport layer (legacy symlinks, systemd notify, UDS)
- G66 provides `platform_default()` / `from_env_or_default()` for agnostic transport
- No L1 symlinks outside transport, no L2 permissions, no L3 raw device APIs
- Verdict: legitimate platform gating, not silicon deism

### ComputeDispatch P0 Migration (Commit 3)

All 92 `*_wgsl.rs` ops migrated from manual BGL→pipeline→encoder→submit
boilerplate to `ComputeDispatch::new().shader().storage_read().storage_rw()
.uniform().dispatch_1d().submit()` builder pattern:

- 12 simple unary math (sin, cos, tan, exp, sqrt, log, abs, sign, trunc,
  floor, ceil, round)
- 34 activation/special ops (bessels, erf, gamma, trig inverses, etc.)
- 16 parameterized ops (pow, clamp, pool1d, cumsum, norm, etc.)
- 16 multi-constructor ops (pad variants, interpolate, PRNG, polynomials)
- 14 complex multi-binding ops (gather, sparse_matvec, rnn_cell, trace)

All ops now use `create_uniform_buffer()` for shader parameter structs
(correct UNIFORM usage instead of STORAGE from `create_buffer_f32_init`).

92 files changed, −10,771 LOC net.

## Quality Gates

- `cargo clippy --workspace`: 0 warnings
- `cargo test --workspace`: 4,990 passed, 0 failed, 191 ignored
- Files >800L: 0 (max 783L, test file)
- Production `unwrap()`: 0
- Production `unsafe`: 0 (all crates `#![forbid(unsafe_code)]`)
- `todo!/unimplemented!/FIXME/HACK`: 0
- Hardcoded primal names: 0
- `Result<T, String>`: 0
- `println!` in lib: 0

## Remaining Structural Debt

| Item | Scope | Priority |
|------|-------|----------|
| Non-WGSL ComputeDispatch | ~225 ops in `ops/` still manual BGL (f64, linalg, MD) | P1 |
| CPU executor `shader_unary/binary` | Migration scaffolding exists, not yet called | P2 |
