# barraCuda v0.3.5 — Sovereign Wiring & Zero-Copy Evolution Handoff

**Date**: 2026-03-15
**Primal**: barraCuda v0.3.5
**Chat**: [Sovereign wiring zero-copy sprint](09872e56-3e65-4bf4-82f9-eb0b07d5737c)

---

## Executive Summary

Deep debt sprint completing the CoralReefDevice → toadStool dispatch pipeline,
zero-copy evolution across 5 data paths, pedantic lint promotion, RwLock
evolution for the tensor store, and Edition 2024 safety fixes. The sovereign
compute pipeline is now wired end-to-end: barraCuda compiles WGSL via coralReef
IPC, discovers toadStool via capability manifests, and dispatches compiled
binaries for GPU execution.

---

## Changes

### CoralReefDevice → toadStool Dispatch (P0 — Complete)

| Before | After |
|--------|-------|
| `dispatch_binary()` returned `Err("not yet implemented")` | Calls `submit_to_toadstool()` via JSON-RPC to `compute.dispatch.submit` |
| No toadStool discovery | `detect_dispatch_addr()` scans `$XDG_RUNTIME_DIR/ecoPrimals/*.json` for `compute.dispatch` capability |
| No buffer staging | `staged_buffers: Mutex<HashMap<u64, BytesMut>>` with upload/download |
| No `Default` impl | `Default` derived via discovery functions |

**Files changed**: `crates/barracuda/src/device/coral_reef_device.rs`

### Zero-Copy Evolution (5 Sites)

| Component | Before | After |
|-----------|--------|-------|
| `CpuTensorStorage::data` | `Vec<u8>` | `bytes::BytesMut` — zero-copy `read_to_cpu()` |
| `CpuExecutor::pack_f32` | `Vec<u8>` allocation | `BytesMut::from(bytemuck::cast_slice())` |
| `CompileResponse` | `.binary` consumed as `Vec<u8>` | `.into_bytes()` → `bytes::Bytes` |
| `EventCodec::encode()` | Returns `Vec<u8>` | Returns `bytes::Bytes` via `BytesMut` builder |
| `EventCodec::encode_simple()` | Returns `Vec<u8>` | Returns `bytes::Bytes` |

**Files changed**: `cpu_executor/storage.rs`, `cpu_executor/executor.rs`,
`cpu_executor/tests.rs`, `coral_compiler/types.rs`, `coral_compiler/mod.rs`,
`npu/event_codec.rs`

### Lint & Quality Evolution

- `#![warn(clippy::pedantic)]` → `#![deny(clippy::pedantic)]` in both crates
- `clippy::map_entry` fix in `dispatch_compute` (Entry API)
- `clippy::new_without_default` fix (Default impl for CoralReefDevice)
- `clippy::missing_errors_doc` fix (`# Errors` sections added)
- `dead_code` lint: `#[cfg_attr(not(test), expect(dead_code, reason = "..."))]`
  for fields used only in tests
- Tensor store `Mutex<HashMap>` → `RwLock<HashMap>` for concurrent read access

### Edition 2024 Safety

`std::env::set_var` is unsafe in Edition 2024. Tests that called `set_var`
were refactored to verify constants and graceful discovery behavior instead of
mutating process environment.

### Naming: coralNAK → coralReef

All active documentation (STATUS.md, WHATS_NEXT.md, REMAINING_WORK.md) updated
to reflect coralReef as the unified primal compiler and driver. CHANGELOG
fossil record preserved (entries prior to this sprint retain original naming).

---

## Cross-Primal Notes

### For toadStool
- barraCuda now dispatches to `compute.dispatch.submit` via JSON-RPC
- Discovery expects capability manifest at `$XDG_RUNTIME_DIR/ecoPrimals/*.json`
  with `"compute.dispatch"` in the capabilities array
- Fallback: `BARRACUDA_DISPATCH_ADDR` environment variable

### For coralReef
- `CompileResponse::into_bytes()` provides zero-copy binary handoff
- coralReef is now referenced as "unified primal compiler and driver" across
  all barraCuda documentation

### For hotSpring
- Tensor store now uses `RwLock` — concurrent reads during dispatch won't block
  on the tensor store lock

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy --workspace --all-targets --all-features -- -D warnings` | Pass |
| `cargo test -p barracuda --lib` | Pass |
| `cargo test -p barracuda-core` | Pass |
| `cargo doc --workspace --no-deps` | Pass (zero warnings) |
| `#![forbid(unsafe_code)]` | Both crates |
| `#![deny(clippy::pedantic)]` | Both crates |

---

## Remaining P0/P1

- P0 toadStool dispatch: **Done** (this sprint)
- P0 VFIO hardware revalidation on Titan V: Blocked on coralReef Iter 44 USERD/INST fix
- P1 DF64 NVK end-to-end verification: Blocked on hardware
- P1 coralReef sovereign compiler evolution: In progress (coralReef Phase 10)
