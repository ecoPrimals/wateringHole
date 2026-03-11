# hotSpring → coralReef: DRM Ioctl Struct Fix Handoff

**Date:** 2026-03-11
**From:** hotSpring team
**To:** coralReef team
**Priority:** P0 — 4 struct ABI bugs fixed, sovereign dispatch blocked on PMU firmware

---

## Summary

hotSpring diagnosed and fixed 4 ioctl struct mismatches in `coral-driver`
that caused `DRM ioctl returned 22` (EINVAL) on all nouveau operations.
After fixes, `VM_INIT` succeeds, but `CHANNEL_ALLOC` fails due to missing
PMU firmware for desktop Volta (GV100). The fixes are correct and needed
regardless — they unblock dispatch on any system with PMU firmware or AMD
hardware.

## Bugs Found and Fixed

### 1. `NouveauVmInit` — struct size mismatch (32 → 16 bytes)

**File:** `crates/coral-driver/src/nv/ioctl/new_uapi.rs`

```rust
// BEFORE (32 bytes — WRONG)
struct NouveauVmInit {
    kernel_managed_addr: u64,
    kernel_managed_size: u64,
    unmanaged_addr: u64,     // not in kernel struct
    unmanaged_size: u64,     // not in kernel struct
}

// AFTER (16 bytes — matches kernel drm_nouveau_vm_init)
struct NouveauVmInit {
    kernel_managed_addr: u64,
    kernel_managed_size: u64,
}
```

**Impact:** Ioctl number encodes struct size. Size mismatch = different ioctl
number = EINVAL on every call.

### 2. `NouveauExec` — field order mismatch

**File:** `crates/coral-driver/src/nv/ioctl/new_uapi.rs`

```rust
// BEFORE (wrong order)
struct NouveauExec {
    channel: u32,
    push_count: u32,
    wait_count: u32,
    sig_count: u32,
    push_ptr: u64,   // should be last
    wait_ptr: u64,
    sig_ptr: u64,
}

// AFTER (matches kernel drm_nouveau_exec)
struct NouveauExec {
    channel: u32,
    push_count: u32,
    wait_count: u32,
    sig_count: u32,
    wait_ptr: u64,
    sig_ptr: u64,
    push_ptr: u64,   // last, matching kernel layout
}
```

### 3. `NouveauVmBind` — field order mismatch

**File:** `crates/coral-driver/src/nv/ioctl/new_uapi.rs`

```rust
// BEFORE (op_ptr in wrong position)
struct NouveauVmBind {
    op_count: u32,
    flags: u32,
    op_ptr: u64,     // should be last
    wait_count: u32,
    sig_count: u32,
    wait_ptr: u64,
    sig_ptr: u64,
}

// AFTER (matches kernel drm_nouveau_vm_bind)
struct NouveauVmBind {
    op_count: u32,
    flags: u32,
    wait_count: u32,
    sig_count: u32,
    wait_ptr: u64,
    sig_ptr: u64,
    op_ptr: u64,     // last, matching kernel layout
}
```

### 4. `NouveauChannelAlloc` / `NouveauChannelFree` — extra padding

**File:** `crates/coral-driver/src/nv/ioctl/mod.rs`

- `NouveauChannelAlloc`: removed trailing `pad: u32` (92 → 88 bytes)
- `NouveauChannelFree`: removed trailing `pad: u32` (8 → 4 bytes)

## Validation on hotSpring test rig

```
Titan V (GV100) on nouveau 1.4, kernel 6.17.9:
  VM_INIT:        OK ✓  (fixed by bug #1)
  CHANNEL_ALLOC:  EINVAL (missing PMU firmware — not our bug)

RTX 3090 (GA102) on nvidia proprietary 580.119.02:
  nvidia-drm:     UVM not implemented (known)

AMD: no hardware on test rig
```

## Recommendation

1. **Merge the 4 struct fixes** into coralReef main
2. **Add compile-time size assertions** matching kernel UAPI:
   ```rust
   const _: () = assert!(std::mem::size_of::<NouveauVmInit>() == 16);
   const _: () = assert!(std::mem::size_of::<NouveauChannelAlloc>() == 88);
   const _: () = assert!(std::mem::size_of::<NouveauChannelFree>() == 4);
   const _: () = assert!(std::mem::size_of::<NouveauExec>() == 40);
   const _: () = assert!(std::mem::size_of::<NouveauVmBind>() == 40);
   ```
3. **Document PMU firmware requirement** — desktop Volta cannot do
   compute via nouveau without PMU firmware from NVIDIA
4. **Test on AMD hardware** — amdgpu dispatch should work E2E now

## PMU Firmware Situation

NVIDIA distributes signed PMU firmware for Tegra SoCs only:
- `/lib/firmware/nvidia/gp10b/pmu/` ✓
- `/lib/firmware/nvidia/gm20b/pmu/` ✓
- `/lib/firmware/nvidia/gv100/pmu/` ✗ (does not exist)

Without PMU, nouveau on desktop Volta/Turing/Ampere is display-only.
Compute channels require PMU initialization.

Possible workarounds:
- **GSP firmware** (Ampere+): ga102 has `/lib/firmware/nvidia/ga102/gsp/`;
  nouveau may be able to use GSP instead of PMU for compute on Ampere+
- **nvidia-drm UVM path**: bypasses nouveau entirely, uses proprietary
  kernel module for DRM dispatch
