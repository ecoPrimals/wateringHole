<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Iteration 72: GPU-Agnostic Evolution Handoff

**Date**: April 4, 2026
**Primal**: coralReef
**Iteration**: 72
**Phase**: 10 — GPU-Agnostic Auto-Detection + Deep Debt Evolution

---

## Summary

coralReef's GPU auto-detection now works with any NVIDIA (Kepler SM35 through
Blackwell SM120) or AMD (GCN5 through RDNA4) GPU. The system no longer assumes
Titan V, SM70, or any specific card. RTX 4070 (Ada Lovelace, SM89) confirmed
working. Test infrastructure evolved from hardware-specific to GPU-agnostic.

## What Changed

### PCI Identity Fix (coral-driver)

Ada Lovelace device IDs `0x2684–0x28FF` were incorrectly classified as Ampere
SM86 in the `nvidia_sm()` identity table. RTX 4070 (PCI `0x2786`), RTX 4080
(`0x2704`), RTX 4060 Ti (`0x2803`), and RTX 4060 (`0x2882`) all now correctly
map to SM89. The Ada Lovelace range is consolidated as `0x2600..=0x28FF`.

**File**: `crates/coral-driver/src/nv/identity.rs`

### GPU Auto-Detection (coral-gpu)

| Change | File | Detail |
|--------|------|--------|
| nvidia-drm fallback | `context.rs` | Uses `sm_from_sysfs_or()` instead of hardcoded `Sm86` when UVM init fails |
| AMD arch detection | `driver.rs` | New `amd_arch_from_sysfs()`: PCI identity → `AmdArch` (gcn5/rdna1/rdna2/rdna3/rdna4) |
| `sm_to_nvarch` expanded | `driver.rs` | Maxwell (50–53), Pascal (60–62), Hopper (90), Blackwell (100); unknown SMs `tracing::warn` |
| VFIO SM range | `driver.rs` | `vfio_sm_from_device_id` covers `0x2400..=0x28FF` for full Ada range |
| `sm_to_compute_class` | `driver.rs` | Delegates to `coral_driver::nv::identity::sm_to_compute_class` (Kepler–Blackwell) |
| `from_descriptor_with_path` | `context.rs` | AMD `arch=None` auto-detects from sysfs; nvidia-drm `arch=None` uses sysfs SM |
| `open_driver` amdgpu | `context.rs` | Auto-detects AMD arch from first amdgpu render node |
| PCIe topology | `pcie.rs` | Uses `amd_arch_from_sysfs` for AMD devices |

### GPU-Agnostic Test Infrastructure (coral-gpu)

| Change | File |
|--------|------|
| `discover_local_gpu()` helper | `src/tests/local_gpu.rs` |
| `require_gpu!()` macro | `src/tests/local_gpu.rs` |
| 4 discovery tests (skip if no GPU) | `tests/local_gpu_discovery.rs` |
| nouveau tests generalized | `coral-driver/tests/hw_nv_nouveau.rs` — removed "Titan V / SM70" from reasons; `open()` auto-detects |

### Script Cleanup

| Old | New | Change |
|-----|-----|--------|
| `rebind-titanv-vfio.sh` | `rebind-gpu-vfio.sh` | BDF via arg or `$CORALREEF_VFIO_BDF`, any GPU |
| `rebind-titanv-nouveau.sh` | `rebind-gpu-nouveau.sh` | BDF via arg or `$CORALREEF_VFIO_BDF`, any GPU |

### Root Doc Updates

Updated `WHATS_NEXT.md`, `README.md`, `COMPILATION_DEBT_REPORT.md` with Iter 72
metrics: 4269 tests, SM89 confirmed, GPU-agnostic language.

## Metrics

| Metric | Value |
|--------|-------|
| Tests passing | 4269 |
| Tests failed | 0 |
| Tests ignored | 153 (hardware-gated) |
| Clippy warnings | 0 (pedantic + nursery) |
| Doc warnings | 0 |
| Files > 1000 LOC | 0 |
| Line coverage | 64.0% workspace / 80.8% non-hardware |

## Confirmed GPU Auto-Detection

```
/dev/dri/renderD128 driver=nvidia-drm vendor=0x10de device=0x2786
nvidia_sm=Some(89) → GpuTarget::Nvidia(NvArch::Sm89)
compiled 160 bytes for sm89 ✓
```

## Remaining Work

1. **UVM hardware validation** — RTX 4070 identity confirmed; UVM dispatch pipeline needs testing
2. **`VfioHardware`/`PciSysfs` traits** — next abstraction layer for VFIO ioctl mocking
3. **Coverage push** — GPU-agnostic tests enable hardware coverage on any developer machine
4. **Intel GPU backend** — `IntelArch::Dg2Alchemist` + `XeLpg` placeholders exist

## Cross-Primal Impact

- **barraCuda**: `GpuContext::auto()` now correctly selects SM89 on Ada Lovelace workstations
- **hotSpring**: Hardware-gated tests can run on any NVIDIA/AMD GPU, not just Titan V
- **toadStool**: GPU discovery reports correct architecture for ecosystem routing
