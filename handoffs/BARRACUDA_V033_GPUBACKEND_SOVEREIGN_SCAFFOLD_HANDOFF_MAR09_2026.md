# barraCuda v0.3.3 — GpuBackend Trait + Sovereign Dispatch Scaffold

**Date**: March 9, 2026
**From**: barraCuda
**To**: coralReef, toadStool, all springs
**Type**: Architecture Evolution Handoff

---

## Summary

barraCuda now has a backend-agnostic GPU compute interface (`GpuBackend` trait)
and a scaffolded `CoralReefDevice` behind the `sovereign-dispatch` feature flag.
This is the foundation for sovereign dispatch — when `coral-gpu` lands as a
crate, barraCuda can dispatch directly through coralReef without the Vulkan stack.

---

## What Changed

### GpuBackend trait (`device::backend`)

9 required methods covering the minimal compute surface:

| Method | Purpose |
|--------|---------|
| `name()` | Device identity |
| `has_f64_shaders()` | f64 capability |
| `is_lost()` | Device health |
| `alloc_buffer(label, size)` | Empty storage buffer |
| `alloc_buffer_init(label, contents)` | Initialized storage buffer |
| `alloc_uniform(label, contents)` | Uniform buffer |
| `upload(buffer, offset, data)` | Host → device |
| `download(buffer, size)` | Device → host |
| `dispatch_compute(desc)` | Full compile → bind → dispatch → submit cycle |

12 default convenience methods for typed f32/f64/u32 operations via bytemuck.

Blanket `impl<B: GpuBackend> GpuBackend for Arc<B>` — ops holding `Arc<WgpuDevice>`
work transparently.

### ComputeDispatch<'a, B: GpuBackend = WgpuDevice>

Now generic over backend. Defaults to `WgpuDevice` so all existing callers
(50+ ops) compile unchanged — type parameter is inferred. `submit()` delegates
to `GpuBackend::dispatch_compute()`.

### CoralReefDevice scaffold

Behind `sovereign-dispatch` feature flag. Implements `GpuBackend` with stub
methods returning clear errors pointing to `SOVEREIGN_PIPELINE_TRACKER.md`.
Zero unsafe. Ready for `coral-gpu::GpuContext` wrapping when the crate is
available.

### SOVEREIGN_PIPELINE_TRACKER.md

New root tracking doc covering P0 blocker (CoralReefDevice), libc/musl → rustix
evolution path (toadStool-led), cross-primal dependency matrix, and
cross-compilation target matrix.

---

## What coralReef Needs To Do

1. **Publish `coral-gpu` as standalone crate**: This unblocks `CoralReefDevice`
   functional implementation in barraCuda.
2. **Stabilize `GpuContext` API**: The 6 methods barraCuda wraps are
   `compile_wgsl`, `alloc`, `upload`, `dispatch`, `sync`, `readback`.
3. **NVIDIA hardware validation**: SM70 codegen exists but dispatch is untested.
   AMD RDNA2 (GFX1030) is E2E verified.

## What toadStool Needs To Do

1. **Lead libc → rustix migration** for `coral-driver` DRM ioctls (follow
   akida-driver pattern already proven in toadStool).
2. **Validate tokio/mio rustix backend** is active on ecosystem targets.

## What Springs Should Know

- The `GpuBackend` trait is the new compute contract. Springs that want to
  contribute backend-specific optimizations can implement or extend it.
- `ComputeDispatch` works identically — no migration needed for existing code.
- When `sovereign-dispatch` is enabled, springs can test the coralReef path
  on AMD RDNA2 hardware (once `coral-gpu` is available).

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy --all-targets` | Pass (zero warnings) |
| `cargo clippy --all-targets --features sovereign-dispatch` | Pass (zero warnings) |
| `cargo test -p barracuda --lib` | 3097 pass, 0 fail |
| `cargo doc --no-deps` | Pass |

---

## Files Changed

| File | Change |
|------|--------|
| `crates/barracuda/src/device/backend.rs` | New — `GpuBackend` trait + `Arc<B>` blanket impl |
| `crates/barracuda/src/device/wgpu_backend.rs` | New — `GpuBackend` impl for `WgpuDevice` |
| `crates/barracuda/src/device/coral_reef_device.rs` | New — `CoralReefDevice` scaffold |
| `crates/barracuda/src/device/compute_pipeline.rs` | `ComputeDispatch` → generic over `GpuBackend` |
| `crates/barracuda/src/device/mod.rs` | Added module registrations + re-exports |
| `crates/barracuda/Cargo.toml` | Added `sovereign-dispatch` feature flag |
| `SOVEREIGN_PIPELINE_TRACKER.md` | New — sovereign pipeline tracking doc |
| `CHANGELOG.md` | GpuBackend + sovereign dispatch entry |
| `STATUS.md`, `README.md`, `START_HERE.md`, `PURE_RUST_EVOLUTION.md` | Updated |
| `specs/REMAINING_WORK.md`, `WHATS_NEXT.md` | Cross-references to tracker |
