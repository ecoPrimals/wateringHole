# barraCuda v0.3.5 — IPC-First Architecture Evolution

**Date**: March 13, 2026
**Type**: Architectural evolution handoff
**Scope**: barraCuda → IPC-first sovereign pipeline (no compile-time primal deps)

---

## Summary

barraCuda's sovereign GPU backend (`CoralReefDevice`) has been evolved from a
compile-time `coral-gpu` dependency model to an **IPC-first architecture**.
All inter-primal communication now flows through JSON-RPC 2.0 at runtime:

```
barraCuda (WGSL math)
  → [JSON-RPC] coralReef (WGSL → native SASS/GFX binary)
    → [JSON-RPC] toadStool (dispatch binary → VFIO/DRM → GPU)
      → GPU hardware (any PCIe GPU — NVIDIA, AMD, Intel)
```

This makes barraCuda a **deployment-agnostic math library** — one crate serves
any deployment target, with the GPU backend determined entirely at runtime by
which primals are available.

---

## What Changed

### Code Changes

| File | Change |
|------|--------|
| `crates/barracuda/Cargo.toml` | Removed `coral-gpu` optional dep; `sovereign-dispatch` feature no longer depends on `dep:coral-gpu` |
| `.cargo/config.toml` | Removed `[patch.crates-io]` entries for coral-gpu/coral-reef/coral-driver |
| `crates/barracuda/src/device/coral_reef_device.rs` | Full rewrite: IPC-first, no `coral_gpu::` references; `from_vfio_device` removed; buffer IDs managed locally pending toadStool IPC |
| `crates/barracuda/src/device/mod.rs` | Removed `pub use coral_gpu;` re-export |
| `crates/barracuda/src/device/backend.rs` | Docs updated: CoralReefDevice described as IPC-first |
| `crates/barracuda/src/device/unified.rs` | Sovereign variant doc updated |
| `crates/barracuda/src/device/capabilities/device_info.rs` | Removed `VfioGpuInfo`, `is_vfio_gpu_available()`, `discover_vfio_gpus()` — all VFIO detection moved to toadStool |
| `crates/barracuda/src/device/capabilities/mod.rs` | Removed VFIO re-exports |

### Documentation Changes

| File | Change |
|------|--------|
| `STATUS.md` | CoralReefDevice described as IPC-first; false "coral-gpu publishable" P0 removed; VFIO detection noted as toadStool responsibility |
| `SOVEREIGN_PIPELINE_TRACKER.md` | Dispatch chain rewritten as IPC-first; P0 blockers corrected; dependency matrix reflects IPC not compile-time deps; from_vfio_device/is_vfio_gpu_available rows removed |
| `PURE_RUST_EVOLUTION.md` | coral-gpu row → IPC to coralReef; dispatch chain updated |
| `WHATS_NEXT.md` | from_vfio_device → IPC-first; VfioGpuInfo → toadStool owns |
| `README.md` | sovereign-dispatch feature description updated |
| `CONTRIBUTING.md` | Dispatch chain updated |
| `specs/BARRACUDA_SPECIFICATION.md` | Dispatch chain updated |
| `specs/ARCHITECTURE_DEMARCATION.md` | VfioGpuInfo → toadStool IPC |

---

## Architectural Principles Applied

1. **IPC-first**: No compile-time coupling between primals. Each primal discovers
   others at runtime via `PRIMAL_NAMESPACE` capability scan.

2. **barraCuda = pure math**: Produces WGSL shaders with precision metadata.
   Never touches GPU hardware, VFIO, DRM, or PCI devices directly.

3. **coralReef = compiler**: Accepts WGSL via `shader.compile.wgsl` JSON-RPC,
   returns native GPU binaries (SASS for NVIDIA, GFX for AMD).

4. **toadStool = dispatcher**: Accepts binaries via `compute.dispatch.submit`
   JSON-RPC, routes to best hardware path (VFIO/DRM), manages all hardware
   lifecycle (bind/unbind, DMA, thermal, multi-GPU).

5. **One library for any deployment**: `barraCuda` + `sovereign-dispatch` works
   identically whether the target is VFIO, DRM, remote GPU, or future backends.

---

## Dissolved Blockers

| Previous Blocker | Resolution |
|------------------|------------|
| `coral-gpu` not publishable as `cargo add` dep | False assumption — IPC-first means no compile-time dep needed |
| `from_vfio_device` constructor pending | Removed — barraCuda never sees VFIO; toadStool handles hardware |
| `VfioGpuInfo` type in barraCuda | Removed — VFIO detection is toadStool's responsibility |

---

## Remaining Work

| Item | Owner | Status |
|------|-------|--------|
| toadStool `compute.dispatch.submit` IPC endpoint | toadStool | API design done (S152); integration pending |
| CoralReefDevice → toadStool IPC wiring | barraCuda | Scaffold done; IPC client pending |
| PFIFO channel init for VFIO dispatch | coralReef | 6/7 VFIO tests pass |
| DF64 NVK hardware verification | barraCuda | Planned |

---

## Quality Gates

- `cargo fmt --all -- --check` ✅
- `cargo clippy --workspace --all-targets -- -D warnings` ✅
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` ✅
- `cargo check --workspace` ✅

---

## Cross-Primal Pins

| Primal | Version/Session | Key IPC endpoint |
|--------|-----------------|------------------|
| toadStool | S152 | `compute.dispatch.submit`, `compute.hardware.capabilities` |
| coralReef | Iter 43 | `shader.compile.wgsl`, `shader.compile.capabilities` |
| hotSpring | v0.6.31 | Consumer of barraCuda's precision routing |
