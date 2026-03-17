# barraCuda v0.3.5 — Typed Errors, Nursery Lints & Coverage Sprint

**Date**: March 16, 2026
**Primal**: barraCuda
**Version**: 0.3.5
**Sprint**: Deep Debt Sprint 5

---

## Summary

Comprehensive audit and execution sprint eliminating all `Result<T, String>`
from production code, resolving clippy nursery warnings in `barracuda-core`,
and expanding test coverage for genomics and async GPU readback.

## Changes

### Typed Error Evolution (15 production sites → zero `Result<T, String>`)

| File | Methods | Error Variant |
|------|---------|---------------|
| `device/async_submit.rs` | 7 methods (`poll_until_ready`, `read_f32/f64/u32/bytes`, `read_f32/f64_blocking`) | `BarracudaError::device_lost()`, `BarracudaError::gpu()` |
| `device/coral_compiler/jsonrpc.rs` | `jsonrpc_call` | `BarracudaError::Internal()` |
| `shaders/sovereign/df64_rewrite/mod.rs` | 3 functions (`rewrite_f64_infix_to_df64`, `count_f64_infix_ops`, `rewrite_f64_infix_full`) | `BarracudaError::shader_compilation()` |
| `device/test_harness.rs` | 3 functions (`validate_wgsl_shader`, `validate_df64_shader`, `validate_shader_batch`) | `BarracudaError::shader_compilation()` |
| `barracuda-core/src/ipc/methods.rs` | 1 closure (`to_tensor`) | `barracuda::error::Result` |

Zero callers broken — `BarracudaError` implements `Display` and `Error`.

### Clippy Nursery Clean (barracuda-core)

- `option_if_let_else` (2 sites) → `map_or_else`
- `missing_const_for_fn` (2 sites) → `IpcServer::new()`, `BarraCudaServer::new()` promoted to `const fn`
- `or_fun_call` (1 site) → `map_or_else`
- `iter_on_single_items` (1 site) → `std::iter::once(0)`

### Test Coverage

- **async_submit**: 2 → 7 tests (queue/submit lifecycle, readback GPU roundtrips)
- **genomics**: 11 → 25 tests (RNA, empty, N-heavy, batch, error paths, edge cases)
- **Total**: 3,464 lib tests, 0 failures

## Quality Gates — All Green

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy --workspace --all-targets --all-features -- -D warnings` | Pass |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | Pass |
| Tests | 3,464 pass / 0 fail |

## wateringHole Standards Compliance

| Standard | Status |
|----------|--------|
| `STANDARDS_AND_EXPECTATIONS.md` — no `.unwrap()` in lib code | PASS |
| `STANDARDS_AND_EXPECTATIONS.md` — `Result<T,E>` everywhere | PASS (zero `Result<T, String>` in production) |
| `STANDARDS_AND_EXPECTATIONS.md` — `thiserror` for typed errors | PASS |
| `STANDARDS_AND_EXPECTATIONS.md` — clippy::pedantic + nursery | PASS |
| `ECOBIN_ARCHITECTURE_STANDARD.md` — pure Rust | PASS |
| `UNIBIN_ARCHITECTURE_STANDARD.md` — single binary | PASS |
| `PRIMAL_IPC_PROTOCOL.md` — JSON-RPC 2.0 + tarpc | PASS |
| File size limit (1000 lines) | PASS (max 794) |
| `#![forbid(unsafe_code)]` | PASS |
| AGPL-3.0-only | PASS |

## Sovereignty / Human Dignity

| Check | Status |
|-------|--------|
| Zero cloud dependencies | PASS |
| Zero vendor lock-in | PASS |
| Capability-based discovery | PASS |
| No telemetry | PASS |
| AGPL-3.0-only | PASS |

## Cross-Primal Impact

- **coralReef**: `jsonrpc_call` now returns `BarracudaError::Internal` instead of `String` — display format unchanged, callers use `match`/`.ok()` patterns unaffected
- **toadStool**: No interface changes — dispatch wiring unchanged
- **Springs**: `validate_wgsl_shader`/`validate_df64_shader` now return typed errors — callers use `.is_ok()`/`.is_err()` patterns unaffected
