# barraCuda V0.3.5 — Sovereign Dispatch Routing Evolution

**Date**: 2026-03-11
**Scope**: Pure Rust compile/driver route — Device enum, Auto routing, kernel cache

## Summary

Wires the sovereign dispatch path (coralReef → DRM) into barraCuda's unified
device abstraction, closing the routing gap between the `CoralReefDevice`
backend (which already implements `GpuBackend`) and the rest of the device
selection/routing infrastructure.

## Changes

### 1. Device Enum — `Device::Sovereign` Variant

`device_types.rs` now includes `Device::Sovereign` for explicit routing to
the coralReef → native SASS/GFX → DRM pipeline. This bypasses wgpu/Vulkan/Metal
entirely.

### 2. DeviceContext — Sovereign Variant

`DeviceContext::Sovereign(CoralReefDevice)` (feature-gated behind
`sovereign-dispatch`) enables lazy initialization of the sovereign backend.

`DeviceContext::for_device(Device::Sovereign)` calls
`CoralReefDevice::with_auto_device()` and verifies `has_dispatch()`.

### 3. Auto Routing — Sovereign-First

When `sovereign-dispatch` is enabled, `DeviceContext::for_device(Device::Auto)`
tries the sovereign path before falling back to wgpu → CPU. This means the
pure Rust path is preferred when hardware is available.

### 4. Availability Probe

- `sovereign_available()` — public function in `device` module
- `is_sovereign_available()` — internal capability probe for `build_device_info`
- `DeviceSelection::Sovereign` + `is_sovereign()` query
- `Device::available_devices()` includes `Sovereign` when probe succeeds

### 5. Kernel Cache for CoralReefDevice

`dispatch_compute()` now caches compiled kernels by shader source hash.
Repeated dispatches of the same shader skip recompilation — critical for
iterative workloads (PDE solvers, Monte Carlo, training loops).

### 6. Capability Wiring

`build_device_info(Device::Sovereign)` reports `Compute`, `WGSL`, and
`ParallelExecution` capabilities when sovereign hardware is detected.

## Architecture After This Change

```
Device::Auto
  → try_sovereign()          [sovereign-dispatch enabled + hardware found]
    → CoralReefDevice::with_auto_device()
    → DeviceContext::Sovereign(dev)
  → WgpuDevice::new()        [wgpu fallback]
    → DeviceContext::GPU(dev)
  → DeviceContext::CPU        [CPU fallback]

Device::Sovereign (explicit)
  → try_sovereign()
  → CoralReefDevice → coral-gpu → DRM → GPU

Device::GPU (explicit)
  → WgpuDevice → wgpu → Vulkan/Metal/DX12 → GPU
```

## Remaining Gaps (coralReef-side, not barraCuda)

| Gap | Owner | Status |
|-----|-------|--------|
| NVIDIA UVM dispatch | coralReef | Research phase |
| Nouveau E2E dispatch | coralReef | Kernel 6.17+ validation |
| Intel backend | coralReef | Not implemented |
| `deformed_potentials_f64` panic | coralReef | SSARef truncation |

## Quality Gates

- `cargo fmt --all -- --check` ✅
- `cargo clippy --workspace -- -D warnings` ✅
- Routing tests: 11/11 ✅
- Core tests: 60/60 ✅
- WGSL shaders: 805
