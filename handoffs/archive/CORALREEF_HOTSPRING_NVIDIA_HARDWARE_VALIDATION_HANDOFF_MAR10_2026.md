# coralReef → hotSpring: NVIDIA Hardware Validation Request

**Date:** March 10, 2026  
**From:** coralReef Phase 10, Iteration 30  
**To:** hotSpring (Titan V + RTX 3090 test rig)  
**License:** AGPL-3.0-only  

---

## Executive Summary

coralReef's compilation layer is fully sovereign — 1487 tests passing, all 3
NVVM poisoning patterns bypassed, 84/93 cross-spring shaders compiling,
multi-device compile API live, FMA contraction enforcement working. The
compilation side needs no hardware.

The **dispatch layer** has two remaining NVIDIA gaps that require hardware
we don't have locally. hotSpring's Titan V + RTX 3090 test rig can unblock
both.

---

## What We Need

### Gap 1: Nouveau Channel EINVAL on Volta (P1 — Titan V)

**Problem**: `DRM_NOUVEAU_CHANNEL_ALLOC` returns `EINVAL (22)` on GV100
(Titan V). This blocks the entire nouveau dispatch pipeline. Our diagnostic
suite (Iteration 29) tries 4 channel configurations and probes firmware,
but we have no Volta hardware to run it on.

**Hypothesis**: Either (a) firmware is missing/wrong version, (b) the
kernel nouveau module needs a specific version, or (c) the channel alloc
struct layout differs for Volta vs newer GPUs.

**What to run**:

```bash
cd coralReef
cargo test --test hw_nv_nouveau -p coral-driver --features nouveau -- --ignored --nocapture 2>&1 | tee nouveau_diag.log
```

**What to capture** (the test outputs all of this):

| Data point | Why we need it |
|-----------|---------------|
| Channel alloc attempts (bare/compute/NVK/alt-class) | Tells us which configurations the kernel accepts |
| Channel alloc hex dump (92 bytes) | Verifies our struct layout matches the kernel ABI |
| Firmware probe results (16 files for gv100) | Missing firmware is the most likely EINVAL cause |
| GPU identity via sysfs | Confirms PCI ID → SM70 mapping works |
| GEM alloc without channel | Tells us if the issue is channel-specific or driver-wide |

**Also capture environment**:

```bash
uname -r
modinfo nouveau | head -20
ls -la /dev/dri/renderD*
ls -la /lib/firmware/nvidia/gv100/ 2>/dev/null
dmesg | grep -i 'nouveau\|drm' | tail -50
```

### Gap 2: nvidia-drm UVM Compute Dispatch (P2 — RTX 3090)

**Problem**: The proprietary NVIDIA driver (`nvidia-drm`) provides device
identification but not compute dispatch through DRM alone. Compute requires
the UVM (Unified Virtual Memory) subsystem via `/dev/nvidia-uvm`.

**Current state**: We have a working `RmClient` proof-of-concept (steps 1-2
of 8 in the UVM pipeline). Steps 3-8 need a system with the proprietary
driver loaded.

**8-step UVM dispatch pipeline**:

| Step | Operation | Status |
|------|-----------|--------|
| 1 | Open `/dev/nvidiactl`, create RM client (`NV_ESC_RM_ALLOC`) | Implemented + tested |
| 2 | Open `/dev/nvidia0`, attach to GPU device | Implemented + tested |
| 3 | Open `/dev/nvidia-uvm`, initialize (`UVM_INITIALIZE`) | Implemented, needs HW test |
| 4 | Register GPU with UVM (`UVM_REGISTER_GPU`) | **Not implemented** |
| 5 | Allocate GPU memory via RM, map through UVM | **Not implemented** |
| 6 | Create compute channel via RM | **Not implemented** |
| 7 | Build and submit push buffer with QMD | QMD builder ready (SM86 v3.0) |
| 8 | Fence sync via UVM semaphore | **Not implemented** |

**What to run** (if proprietary driver is loaded):

```bash
# Test RM client allocation (steps 1-2)
cargo test uvm -p coral-driver -- --ignored --nocapture 2>&1 | tee uvm_diag.log

# Test nvidia-drm probing
cargo test --test hw_nv_probe -p coral-driver -- --ignored --nocapture 2>&1 | tee nv_probe.log

# Test nvidia-drm buffer operations
cargo test --test hw_nv_buffers -p coral-driver --features nvidia-drm -- --ignored --nocapture 2>&1 | tee nv_buffers.log
```

**What to capture**:
- Whether `/dev/nvidiactl`, `/dev/nvidia0`, `/dev/nvidia-uvm` exist
- Whether RM client allocation succeeds (root + device + subdevice)
- `UVM_INITIALIZE` ioctl result (step 3)
- Any errors or permission issues

---

## Full Test Script

Save this as `run_nvidia_diag.sh` and run on the test rig:

```bash
#!/bin/bash
set -euo pipefail

echo "=== Environment ==="
uname -r
cat /proc/version
echo "---"
ls -la /dev/dri/renderD* 2>/dev/null || echo "No renderD nodes"
ls -la /dev/nvidia* 2>/dev/null || echo "No nvidia devices"
echo "---"
modinfo nouveau 2>/dev/null | head -10 || echo "nouveau not loaded"
modinfo nvidia 2>/dev/null | head -10 || echo "nvidia not loaded"

echo "=== GPU Identity (sysfs) ==="
for d in /sys/class/drm/renderD*/device; do
  echo "--- $d ---"
  cat "$d/vendor" "$d/device" 2>/dev/null || echo "no vendor/device"
done

echo "=== Firmware ==="
for chip in gv100 tu102 ga102; do
  echo "--- $chip ---"
  ls /lib/firmware/nvidia/$chip/ 2>/dev/null | head -20 || echo "not found"
done

echo "=== DRM messages ==="
dmesg | grep -i 'nouveau\|nvidia\|drm' | tail -50

echo "=== Nouveau Diagnostics ==="
cargo test --test hw_nv_nouveau -p coral-driver --features nouveau -- --ignored --nocapture 2>&1 || true

echo "=== NV Probe ==="
cargo test --test hw_nv_probe -p coral-driver -- --ignored --nocapture 2>&1 || true

echo "=== UVM Diagnostics ==="
cargo test uvm -p coral-driver -- --ignored --nocapture 2>&1 || true

echo "=== Multi-GPU ==="
cargo test --test hw_nv_probe -p coral-driver -- --ignored multi_gpu --nocapture 2>&1 || true

echo "=== NVVM Bypass Verification ==="
cargo test --test nvvm_bypass 2>&1 || true

echo "=== Done ==="
```

**Run**: `bash run_nvidia_diag.sh 2>&1 | tee coralreef_nvidia_diag_$(date +%Y%m%d).log`

**Send back**: The `.log` file. That's all we need.

---

## What coralReef Has Ready (No Hardware Needed)

These features are fully tested and waiting for hardware validation:

| Feature | Status | What hardware validation adds |
|---------|--------|------------------------------|
| SM auto-detection via sysfs | Tested with mock | Confirms PCI ID → SM mapping on real Volta + Ampere |
| Multi-GPU enumeration | Tested with mock | Confirms distinct contexts for Titan V + RTX 3090 |
| QMD v2.1 (Volta) + v3.0 (Ampere) | Built and tested | Confirms dispatch descriptor layout on real hardware |
| Push buffer encoding | Fixed (Iteration 9) | Confirms `mthd_incr` field order with kernel |
| Struct ABI (92/8/48/64/8 bytes) | Size-verified | Confirms alignment with actual kernel structs |
| NVVM bypass (14 tests) | All passing | Confirms our SASS compiles correctly for Volta + Ampere |
| FMA contraction enforcement | All passing | Confirms `NoContraction` semantics on real hardware output |
| Multi-device compile | All passing | Confirms cross-vendor compilation for Titan V (SM70) + RTX 3090 (SM86) |
| `PCIe` topology awareness | Implemented | Confirms `PCIe` switch grouping on multi-GPU rig |

---

## coralReef Current State (Iteration 30)

| Metric | Value |
|--------|-------|
| Tests | 1487 passing, 0 failed, 76 ignored |
| Clippy | Zero warnings |
| NVVM bypass | 14/14 all patterns × all architectures |
| Cross-spring shaders | 84/93 compiling SM70 |
| IPC endpoints | `shader.compile.{wgsl,spirv,wgsl.multi,status,capabilities}` |
| FMA policies | Auto, Fused, Separate — enforced in codegen |
| Unsafe blocks | 17 in coral-driver only; 0 in 8/9 crates |
| AMD E2E | Verified on RX 6950 XT |
| NVIDIA E2E | Compilation complete; dispatch blocked on nouveau EINVAL / UVM |

---

## Priority for hotSpring

1. **Nouveau EINVAL diagnostics** — run the diagnostic suite on Titan V. This is the single most valuable data point. If firmware is the issue, we can document the fix. If it's a struct layout issue, the hex dump will tell us.

2. **Environment data** — kernel version, driver version, firmware listing. Even without running tests, this helps narrow hypotheses.

3. **UVM probing** — if the proprietary driver is also loaded, the UVM tests tell us if steps 1-3 work and what step 4 needs.

4. **Multi-GPU enumeration** — confirms `PCIe` topology awareness works on a real multi-GPU system.

---

*coralReef compiles. hotSpring dispatches. Together we close the sovereign loop.*
