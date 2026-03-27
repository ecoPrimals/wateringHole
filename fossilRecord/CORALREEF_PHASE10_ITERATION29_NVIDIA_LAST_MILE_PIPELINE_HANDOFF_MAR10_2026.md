# coralReef → Ecosystem: Phase 10 Iteration 29 — NVIDIA Last Mile Pipeline

**Date:** March 10, 2026  
**From:** coralReef Phase 10, Iteration 29  
**To:** toadStool / barraCuda / hotSpring / All Springs  
**License:** AGPL-3.0-only  
**Covers:** Iteration 28 → Iteration 29  

---

## Executive Summary

- **Multi-GPU foundation fixed**: `enumerate_all()` now opens each render node by its specific path — arrays of identical GPUs (e.g. 4× RTX 3050 on PCIe) produce distinct contexts targeting distinct physical devices
- **NVIDIA EINVAL diagnostic instrumentation**: Full diagnostic suite for channel creation failures — bare/compute/NVK-style/alt-class attempts, firmware probing, struct hex dumps, GPU identity via sysfs
- **Buffer lifecycle safety**: NvDevice defers temp buffer cleanup to `sync()` (matching AMD pattern), eliminating potential use-after-free at kernel level
- **SM auto-detection**: GPU chipset probed from sysfs, mapped to SM version (Volta through Ada Lovelace) — no more hardcoded SM70
- **UVM RM client proof-of-concept**: `RmClient` with `NV_ESC_RM_ALLOC` for root client, device, and subdevice allocation — foundation for nvidia-drm compute path
- **1447 tests passing, 0 failed, 76 ignored; zero clippy warnings**

---

## Part 1: Multi-GPU Foundation

### The bug (fixed)

`enumerate_all()` called `open_driver(&info.driver)` which internally called `open_by_driver("nouveau")` — always opening the **first** matching render node. Multiple GPUs with the same driver all mapped to the same physical device.

### The fix

- Added `AmdDevice::open_path(path)`, `NvDevice::open_path(path, sm)`, `NvDrmDevice::open_path(path)` to each backend
- `enumerate_all()` now calls `open_driver_at_path(&info.driver, &info.path)` — each render node opens its own distinct device
- `from_descriptor_with_path()` enables ecosystem discovery to target specific render nodes

### Impact for springs

Any spring using `coral-gpu::GpuContext::enumerate_all()` will now correctly discover and target all GPUs on the system. This is the foundation for multi-GPU arrays — critical for PCIe daisy-chain topologies.

---

## Part 2: Nouveau EINVAL Diagnostics

### Diagnostic functions added

| Function | Purpose |
|----------|---------|
| `diagnose_channel_alloc(fd, class)` | Tries bare (0 subchan), compute-only, NVK multi-engine, alternate compute classes — reports pass/fail for each |
| `dump_channel_alloc_hex(class)` | Raw hex dump of `NouveauChannelAlloc` for kernel debugging |
| `check_nouveau_firmware(chip)` | Probes 16 firmware files per chip in `/lib/firmware/nvidia/{chip}/` |
| `probe_gpu_identity(path)` | Reads PCI vendor/device from sysfs, maps to SM version |
| `GpuIdentity::nvidia_sm()` | PCI device ID → SM version (Volta=70, Turing=75, Ampere GA100=80, GA10x=86, Ada=89) |

### Struct ABI verification

| Struct | Verified Size | Notes |
|--------|---------------|-------|
| `NouveauChannelAlloc` | 92 bytes | 20 header + 64 subchan array + 8 trailer |
| `NouveauChannelFree` | 8 bytes | |
| `NouveauGemNew` | 48 bytes | |
| `NouveauGemPushbuf` | 64 bytes | |
| `NouveauSubchan` | 8 bytes | handle + grclass |

### Auto-diagnostics on failure

`NvDevice::open_from_drm()` now runs the full diagnostic suite when channel creation fails — logging each configuration attempt, checking firmware, and probing GPU identity via sysfs. This gives springs detailed failure context without manual debugging.

---

## Part 3: Buffer Lifecycle Safety

NvDevice previously freed shader, QMD, and pushbuf GEM handles immediately after `pushbuf_submit()`. The GPU may still be reading these buffers.

**Fix**: Added `inflight: Vec<BufferHandle>` to NvDevice. Dispatch pushes temp handles into inflight. `sync()` drains and frees after fence. `Drop` drains inflight before destroying buffers and channel. This matches the AMD pattern exactly.

---

## Part 4: SM Auto-Detection

### Problem

`NvDevice::open()` hardcoded SM70. `coral-gpu` hardcoded `NvArch::Sm70` for nouveau. Wrong compute class selected for Turing/Ampere/Ada GPUs.

### Fix

- `NvDevice::open()` probes sysfs via `probe_gpu_identity()`, maps to SM version
- `coral-gpu` uses `sm_to_nvarch()` and `sm_from_sysfs()` for both `open_driver` and `enumerate_all`
- Supports mixed-generation GPU arrays (e.g. Volta + Ampere on same system)

---

## Part 5: UVM RM Client (Proof of Concept)

Foundation for the nvidia-drm proprietary driver compute path:

| Operation | Ioctl | Status |
|-----------|-------|--------|
| Root client allocation | `NV_ESC_RM_ALLOC(NV01_ROOT)` | Implemented + tested |
| Device allocation | `NV_ESC_RM_ALLOC(NV01_DEVICE_0)` | Implemented + tested |
| Subdevice allocation | `NV_ESC_RM_ALLOC(NV20_SUBDEVICE_0)` | Implemented + tested |
| Object free | `NV_ESC_RM_FREE` | Implemented |
| RAII cleanup | `Drop` for `RmClient` | Implemented |

This is the first step in the NVIDIA proprietary dispatch pipeline (Step 1-2 of the 8-step UVM compute path documented in `uvm.rs`).

---

## Verification

| Check | Status |
|-------|--------|
| `cargo check --workspace` | PASS |
| `cargo test --workspace` | PASS (1447 passing, 0 failed, 76 ignored) |
| `cargo clippy --workspace --all-targets` | PASS (0 warnings) |
| `cargo fmt --check` | PASS |
| Unsafe blocks | 17 in coral-driver (kernel ABI only); 0 in 8/9 crates |

---

## Known Gaps (Iteration 30 candidates)

| Gap | Priority | Detail |
|-----|----------|--------|
| Nouveau EINVAL on Volta | P1 | Channel creation rejected on GV100 — likely firmware or kernel version; diagnostic suite ready for on-site investigation |
| nvidia-drm UVM compute dispatch | P2 | RM client allocated; next: `UVM_REGISTER_GPU`, buffer mapping, channel creation, command submission |
| Coverage 63% → 90% | P2 | Structural floor from encoder match arms |
| AMD Discriminant encoding gap | P3 | 5 spring shaders blocked on SPIR-V Discriminant expression |

---

## For hotSpring / Springs

The multi-GPU foundation means springs testing on multi-GPU systems will now correctly enumerate and target each GPU independently. SM auto-detection means the correct compute class is selected without manual configuration.

The EINVAL diagnostic suite is specifically designed for the Titan V on-site test — run `cargo test --test hw_nv_nouveau --features nouveau -- --ignored` to get detailed diagnostic output.

---

*coralReef Iteration 29 — building the foundation for sovereign multi-GPU compute, instrument by instrument, note by note.*
