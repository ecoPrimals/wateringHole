# barraCuda v0.3.6 — Vendor-Agnostic Evolution Handoff

**Date**: March 21, 2026
**Sprint**: 14
**Primal**: barraCuda (sovereign math engine)
**Status**: Complete — all 7 phases executed, quality gates green

---

## Summary

barraCuda is now fully vendor-atheistic. Zero vendor names in type systems,
zero PCI vendor ID branching in ops, zero ISA target strings, zero
driver-specific heuristics in production routing. All classification uses
device-class semantics (`DiscreteGpu`/`IntegratedGpu`/`Software`) derived
from wgpu `DeviceType` at runtime.

This sprint also deprecated `GpuDriverProfile` (dead code — all consumers
migrated to `DeviceCapabilities`) and expanded test coverage by +75 tests
to 4,052+ total.

---

## API Changes (Cross-Primal Impact)

### Removed from public API

| Old | Replacement | Notes |
|-----|-------------|-------|
| `GpuVendor` | `DeviceClass` | `DiscreteGpu`, `IntegratedGpu`, `Software`, `Unknown` |
| `GpuDriver` | removed | f64 support now via `f64_builtins_available: bool` |
| `prefer_nvidia()` | `prefer_discrete()` | Capability-based, not vendor-based |
| `prefer_amd()` | `prefer_discrete()` | Same |
| `BandwidthTier::NvLink` | `HighBandwidthP2P` / `HighBandwidthInterconnect` | Detects data-center GPUs from any vendor |
| `SubstrateType::NvidiaGpu` | `SubstrateType::DiscreteGpu` | wgpu `DeviceType` classification |
| `SubstrateType::AmdGpu` | `SubstrateType::DiscreteGpu` | Same |
| `SubstrateType::IntelGpu` | `SubstrateType::IntegratedGpu` | Same |
| `SubstrateType::AppleGpu` | `SubstrateType::IntegratedGpu` | Same |
| `arch_to_coral()` | `AdapterDescriptor` IPC | coralReef determines ISA targets |
| `GpuDriverProfile` | `DeviceCapabilities` | Deprecated, `#[deprecated]` attribute |

### New public types

| Type | Location | Purpose |
|------|----------|---------|
| `DeviceClass` | `multi_gpu::topology` | Vendor-agnostic device classification |
| `AdapterDescriptor` | `coral_compiler::types` | IPC payload for coralReef ISA target determination |
| `DeviceCapabilities::fp64_strategy()` | `capabilities::wgpu_caps` | Probe-based f64 execution strategy |
| `DeviceCapabilities::precision_routing()` | `capabilities::wgpu_caps` | Probe-based precision routing advice |
| `DeviceCapabilities::latency_model()` | `capabilities::wgpu_caps` | Architecture-aware ILP scheduling model |

### coralReef integration change

`barraCuda` no longer passes ISA target strings to coralReef. Instead:

1. `barraCuda` sends `AdapterDescriptor` (vendor_id, device_name, device_type)
2. coralReef queries its own `shader.compile.capabilities` for supported architectures
3. `best_target_for_adapter()` selects the appropriate target
4. coralReef compiles for the selected architecture

Springs consuming coralReef compiled binaries should not be affected — the
change is internal to the barraCuda↔coralReef IPC contract.

---

## Phase Breakdown

| Phase | Description | Files Modified |
|-------|-------------|----------------|
| 1 | Capability-based workgroup sizing (ops/add, mul, fma) | 4 |
| 2 | ISA target string removal, AdapterDescriptor | 5 |
| 3a | DeviceCapabilities enrichment with f64 probes | 3 |
| 3b | Consumer migration from GpuDriverProfile | 30+ |
| 3c | GpuDriverProfile deprecation, public API cleanup | 10+ |
| 4 | Latency model vendor-aware selection | 2 |
| 5 | SubstrateType, topology, transfer, probe cleanup | 20+ |

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo clippy --workspace --all-targets -- -D warnings` | Pass (zero warnings) |
| `cargo fmt --all -- --check` | Pass |
| `cargo test -p barracuda --lib` | 3,649 pass / 0 fail |
| `cargo test -p barracuda-core --all-features` | 118 pass / 0 fail |
| `cargo doc --workspace --no-deps` | Pass |

---

## Impact on Other Primals

- **coralReef**: Now receives `AdapterDescriptor` instead of bare ISA strings.
  coralReef Phase 10+ already handles adapter-based target selection. No changes
  needed in coralReef.
- **toadStool**: `SubstrateType` variants changed. If toadStool deserializes
  `SubstrateType` from barraCuda, update to handle `DiscreteGpu`/`IntegratedGpu`
  instead of `NvidiaGpu`/`AmdGpu`.
- **Springs**: Any spring using `prefer_nvidia()` or `GpuVendor` must migrate to
  `prefer_discrete()` and `DeviceClass`. The old types are no longer re-exported
  from `barracuda::`.
- **All primals**: `GpuDriverProfile` is `#[deprecated]`. Code importing it will
  get compiler warnings. Migrate to `DeviceCapabilities::from_device()`.

---

## Test Coverage

| Module | Tests Added | Coverage |
|--------|-------------|----------|
| DeviceCapabilities | +41 | fp64_strategy, precision_routing, latency, eigensolve |
| coral_compiler | +14 | cache, shader_hash, serde, precision mapping |
| ODE bio params | +12 | to_flat/from_flat round-trips |
| Substrate | +8 | Display, serde, capability queries |
| **Total** | **+75 → 4,052+** | |
