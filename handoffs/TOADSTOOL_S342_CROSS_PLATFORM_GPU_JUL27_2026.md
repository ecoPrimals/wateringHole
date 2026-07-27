# ToadStool S342 — Cross-Platform GPU Discovery + SAFETY Docs

**Date**: Jul 27, 2026 | **Session**: S342 | **Wave**: 155b

## Summary

Wired wgpu adapter enumeration into the self-knowledge pipeline as
cross-platform GPU fallback. Fixed doctor false positives and documented
unsafe MMIO operations.

## Changes

### Cross-Platform GPU Discovery (capabilities/gpu.rs)

`query_gpu_devices()` now falls back to `wgpu::Instance::enumerate_adapters()`
when platform-native detection finds no GPUs:
- Linux: sysfs/DRM + `/proc/driver/nvidia` (unchanged)
- macOS: System Profiler (unchanged)
- **All platforms (new)**: wgpu adapter enumeration — DX12, Vulkan, Metal

CPU-type wgpu adapters are filtered out. Vendor ID → label mapping covers
NVIDIA (0x10DE), AMD (0x1002), Intel (0x8086), Apple (0x106B),
Microsoft (0x1414), Qualcomm (0x5143).

### Doctor GPU Check Fix (doctor/checks.rs)

`check_gpu_available()` no longer returns `true` unconditionally on
non-Linux. Platform-specific checks:
- Windows: `vulkan-1.dll` or `d3d12.dll` in System32
- macOS: Metal.framework
- Other: returns `false`

### Unsafe SAFETY Documentation

5 MMIO operations in `rm_trigger/main.rs` quench loop and
`nv/registers/pmc.rs` given individual `// SAFETY:` comments
(previously covered by a group comment).

### Lint Attribute Evolution

2 production `#[allow]` without `reason` → `#[expect]` with reasons:
- `sandbox/manager.rs`: `used_underscore_binding` (reserved param)
- `connection/unix.rs`: `needless_pass_by_value` (consumed into response)

## Quality Gates

- 9,232 lib tests, 0 failures
- Zero clippy warnings (`-D warnings` on Rust 1.96)
- Zero fmt diff

## Cross-Platform Gap Analysis

Wave 155b identifies "Cross-platform hardware discovery (Windows GPU
probing)" as toadStool's next work. Status after S342:

| Layer | Cross-platform? |
|-------|-----------------|
| capabilities/gpu.rs | **Yes** (wgpu fallback added S342) |
| sysmon::discover_gpus | Linux-only (by design — reads procfs/sysfs) |
| dispatch routing/state | Linux-only (VFIO/DRM kernel APIs) |
| doctor check_gpu_available | **Yes** (fixed S342) |
| resource_validator | **Yes** (wgpu probe with timeout) |

Next: Windows-native enrichment (WMI `Win32_VideoController` for VRAM,
DXGI adapter enumeration) to complement wgpu's name+vendor-only data.
