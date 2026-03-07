# coralReef — Phase 10 Iteration 6: Deep Debt Internalization Handoff

**Date**: March 7, 2026
**From**: coralReef
**To**: hotSpring, groundSpring, neuralSpring, wetSpring, airSpring, barraCuda, toadStool

---

## Summary

coralReef Phase 10 — Iteration 6 completes deep debt internalization and
modern idiomatic Rust evolution. AMD driver fully wired (BO list, CS submit,
fence sync). All error types zero-allocation. IPC semantic naming and
differentiated error codes. Nouveau scaffolds evolved to explicit errors.
Zero production `unwrap()`/`todo!()`. 856 tests, 836 passing, zero failures.

## Metrics

| Metric | Iteration 5 | Iteration 6 | Delta |
|--------|-------------|-------------|-------|
| Total tests | 832 | 856 | **+24** |
| Passing | 811 | 836 | **+25** |
| Ignored | 21 | 20 | **-1** |
| Corpus passing SM70 | 14 | 14 | — |
| Clippy warnings | 0 | 0 | — |
| Production `unwrap()`/`todo!()` | ~75 | **0** | **-75** |

## Deep Debt Internalization

### Error Type Evolution

All error enums (`DriverError`, `CompileError`, `GpuError`, `PrimalError`) evolved
from `String` fields to `Cow<'static, str>`. Zero heap allocation for static error
messages. 26+ call sites updated with `.into()` for `format!()` → `Cow::Owned`.

### AMD Driver — Full IOCTL Implementation

| Component | Before | After |
|-----------|--------|-------|
| `submit_command` | Scaffold (returned `Ok(0)`) | Full IOCTL: BO list create, IB submission, fence return |
| `sync_fence` | Scaffold (returned `Ok(())`) | Full IOCTL: `DRM_AMDGPU_WAIT_CS` with 5-second timeout |
| `AmdDevice::dispatch` | Scaffold | GEM alloc, PM4 upload, BO list, submit, fence track, cleanup |
| `AmdDevice::sync` | Scaffold | Uses `sync_fence` with stored `last_fence` |

New kernel structs: `AmdgpuBoListEntry`, `AmdgpuBoListIn`, `AmdgpuCsChunk`,
`AmdgpuCsChunkIb`, `AmdgpuCsIn`, `AmdgpuWaitCsIn` — all `#[repr(C)]`.

### Unsafe Code Evolution

| Change | Before | After |
|--------|--------|-------|
| `kernel_ptr<T>(r: &T) -> u64` | Inline `std::ptr::from_ref(r) as u64` | Centralized helper, documented safety |
| `read_ioctl_output<T, R>(arg: &T) -> R` | Inline `std::ptr::read(from_ref(arg).cast())` | `const unsafe fn`, centralized safety |
| `drm_ioctl_typed` | `pub unsafe fn` | `pub(crate) unsafe fn` — FFI sealed within crate |
| `BufferHandle` | `pub u32` | `pub(crate) u32` — driver owns validity |

### NVIDIA Nouveau — Scaffolds Evolved

All scaffold functions (`create_channel`, `destroy_channel`, `gem_new`, `dispatch`, `sync`)
now return `Err(DriverError::Unsupported(...))` with clear messages. No silent success.
Tests verify all paths return `Unsupported`.

### IPC Evolution (wateringHole Compliance)

| Aspect | Before | After |
|--------|--------|-------|
| JSON-RPC methods | `compiler.compile`, `compiler.health` | `shader.compile.spirv`, `shader.compile.wgsl`, `shader.compile.status`, `shader.compile.capabilities` |
| tarpc trait | `CoralReefTarpc` | `ShaderCompileTarpc` with `spirv()`, `wgsl()`, `status()`, `capabilities()` |
| Error codes | Generic `-32000` | Differentiated: `-32001` InvalidInput, `-32002` NotImplemented, `-32003` UnsupportedArch |

### Rust Idiom Modernization

- All non-wildcard `#[allow(clippy::...)]` → `#[expect(clippy::..., reason = "...")]` (Rust 2024)
- `std::collections::HashMap` → `FxHashMap` in compiler hot paths (`naga_translate`)
- Redundant `impl Drop for DrmDevice` removed (`File` already closes on drop)
- `as` casts → `usize::try_from().expect()` / `u32::try_from().expect()` where safe

### Test Coverage Expansion

| Module | New Tests | Focus |
|--------|-----------|-------|
| `lifecycle.rs` | 6 | `PrimalState::is_running`, all `PrimalError` variants, `Error` trait |
| `health.rs` | 3 | Additional health state transitions |
| `gpu_arch.rs` | 10 | `NvArch` properties, `AmdArch` properties, `GpuTarget::From`, `IntelArch::Display` |
| `ipc/mod.rs` | 3 | tarpc capabilities/wgsl, JSON-RPC differentiated error codes |
| `nv/ioctl.rs` | 2 | Unsupported error verification |

## Checks

| Check | Status |
|-------|--------|
| `cargo check --workspace` | PASS |
| `cargo test --workspace` | PASS (856 tests, 20 ignored) |
| `cargo clippy --workspace --all-targets -- -W clippy::pedantic -W clippy::nursery` | PASS (0 warnings) |
| `cargo fmt --check` | PASS |
| `cargo doc --workspace --no-deps` | PASS (0 warnings) |

## IPC Contract (for toadStool / barraCuda)

### JSON-RPC 2.0

| Method | Description |
|--------|-------------|
| `shader.compile.spirv` | Compile SPIR-V bytes → native binary |
| `shader.compile.wgsl` | Compile WGSL source → native binary |
| `shader.compile.status` | Health/readiness probe |
| `shader.compile.capabilities` | Supported architectures and features |

### tarpc (high-performance path)

Trait `ShaderCompileTarpc` with methods: `spirv()`, `wgsl()`, `status()`, `capabilities()`.
TCP and Unix socket transports. `bytes::Bytes` zero-copy payloads.

### Error Codes

| Code | Meaning |
|------|---------|
| `-32001` | Invalid input (bad SPIR-V, empty source) |
| `-32002` | Feature not implemented |
| `-32003` | Unsupported target architecture |

---

*coralReef — sovereign Rust GPU compiler. 856 tests. Zero production unwrap.
Zero-alloc errors. AMD driver wired. IPC semantic. All pure Rust.*
