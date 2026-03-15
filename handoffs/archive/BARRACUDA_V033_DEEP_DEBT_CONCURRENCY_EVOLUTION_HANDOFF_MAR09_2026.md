# barraCuda v0.3.3 — Deep Debt & Concurrency Evolution Handoff

**From**: barraCuda
**Date**: 2026-03-09
**Session**: Deep debt sprint — hot-path clones, hardcoding, spin-waits, test fragility, streaming pipeline

---

## Summary

26 files changed (+463 / −253 lines). Focused on evolving barraCuda to modern idiomatic fully concurrent Rust: eliminating hot-path allocations, replacing busy-spins with cooperative yielding, consolidating hardcoded values to capability-based constants, and completing the GPU→CPU streaming pipeline.

---

## Changes for All Springs

### Hot-Path Clone Elimination
- `multi_gpu::DeviceInfo::name`: `String` → `Arc<str>` — every device lease was heap-allocating
- `staging::RingBufferConfig::label`: `String` → `Option<Arc<str>>`
- `coral_compiler::CoralCompiler::state`: `Mutex` → `RwLock` with `Arc<str>` addresses — concurrent shader compiler reads no longer serialize

### Ring Buffer Back-Off
- `GpuRingBuffer::write()` evolved from million-iteration `spin_loop()` to staged back-off:
  256 spins → 4096 `yield_now()` calls. CPU-friendly, bounded wall-clock budget (~100ms).
  For async contexts, `try_write` with polling remains preferred.

### Streaming Pipeline Completion
- `GpuRingBuffer::read()` + `advance_write()`: GPU→CPU async readback via staging buffer
- `UnidirectionalPipeline::poll_results()` + `advance_output()`: CPU can now read completed GPU work
- Enables streaming test patterns via unidirectional pipelines

### Hardcoding Elimination
- 10 f64 ops evolved from hardcoded `256` to `WORKGROUP_SIZE_1D` constant
- VRAM cap, dispatch threshold, scoring weight magic numbers all extracted to named constants
- `max_allocation_size()` float round-trip eliminated — pure integer arithmetic

### Test Evolution
- `catch_unwind` in GPU tests (erf, erfc, expand, determinant) → `with_device_retry` (production recovery)
- `tokio::time::timeout` added to cross-vendor GPU verification tests
- `parse_shape()` IPC helper: `usize::try_from` instead of `as usize` casts

### API Changes
- `session::AttentionDims` config struct replaces 4-argument attention/head_split/head_concat
- `DeviceInfo::name` field type changed from `String` to `Arc<str>` (construct with `Arc::from("name")`)

### Dependency Audit
- All dependencies confirmed pure Rust — fully ecoBin compliant
- Zero `unsafe` blocks, zero `unsafe fn`, zero `unsafe impl` in entire codebase

---

## Quality Gates

All pass (re-verified after all changes):

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy --all-targets --all-features -D warnings` | Pass (zero warnings) |
| `cargo doc --no-deps --all-features` | Pass |
| `cargo deny check` | Pass (advisories, bans, licenses, sources) |

---

## For coralReef

No action required. IPC contract unchanged. `coral_compiler` module now uses `RwLock` internally for better read concurrency during shader compilation status checks.

## For toadStool

No action required. `DeviceInfo::name` type change is internal to barraCuda's multi-GPU pool.

## For hotSpring / wetSpring / neuralSpring / groundSpring / airSpring

- If consuming `session::attention()`, `head_split()`, or `head_concat()`: these now accept `&AttentionDims` instead of 4 separate `usize` params
- `WORKGROUP_SIZE_1D` constant is the single source of truth for 1D workgroup sizing — use it instead of hardcoding `256`

---

## Remaining P1

- DF64 NVK end-to-end verification (Yukawa kernels)
- coralNAK extraction (when org repo fork lands)
- Dedicated DF64 shaders for covariance + weighted_dot on Hybrid devices
