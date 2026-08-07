# barraCuda — Wave 157a Error Idiom Evolution Phase 3 (strandGate)

**Date**: Aug 7, 2026
**Gate**: strandGate
**Team**: Compute Trio — barraCuda
**Wave**: 157a

---

## Summary

Error constructor helper migration Phase 3 + magic number centralization +
protocol negotiation zero-alloc optimization + G68 Platform Substrate audit.
20 files changed across `barracuda` and `barracuda-core` crates. All remaining
verbose error constructor patterns migrated to helpers. 5,011 tests pass.
Zero clippy warnings.

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

## Quality Gates

- `cargo clippy --workspace`: 0 warnings
- `cargo test --workspace`: 5,011 passed, 0 failed, 191 ignored
- Files >800L: 0 (max 783L, test file)
- Production `unwrap()`: 0
- Production `unsafe`: 0 (all crates `#![forbid(unsafe_code)]`)
- `todo!/unimplemented!/FIXME/HACK`: 0
- Hardcoded primal names: 0
- `Result<T, String>`: 0
- `println!` in lib: 0

## Upstream Context

Absorbed 8 upstream commits since Wave 155u:
- `8380e088` C2 dual-socket pattern
- `dbfb5790` 214 needless_borrow clippy fixes
- `7a11e4e4` GPU buffer alignment + 13 test promotions
- `78696b5e` 182-file cargo fmt + G65 readiness
- `7e823414` 68 dependency bumps
- `d92f571a` G65 protocol negotiation
- `525674ff` G65 peek libc→rustix
- `5c01bab0` G66 transport abstraction

## Remaining Structural Debt

| Item | Scope | Priority |
|------|-------|----------|
| ComputeDispatch migration | ~92 `*_wgsl.rs` ops using manual BGL→pipeline | P0 (−10K LOC) |
| GPU dispatch match collapse | Unary table + pool2d helper in `gpu_executor/dispatch.rs` | P1 |
| Deprecated batch activations | Wire IPC `activation.gelu` to shader dispatch | P1 |
| CPU executor `shader_unary/binary` | Migration scaffolding exists, not yet called | P2 |
