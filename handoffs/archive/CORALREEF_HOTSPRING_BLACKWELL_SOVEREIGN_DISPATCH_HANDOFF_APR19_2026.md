# coralReef + hotSpring: Blackwell Sovereign Dispatch Handoff

**Date:** April 19, 2026
**Spring:** hotSpring v0.6.32
**Primals:** coralReef (coral-driver, coral-kmod), barraCuda
**Target:** RTX 5060 (Blackwell GB206, SM120)
**License:** AGPL-3.0-or-later

---

## Context

Continuation of the sovereign compile parity work (Apr 18 handoff). Full HMC
pipeline compiles to SASS on SM35/SM70/SM120. This session focused on resolving
**GAP-HS-031** — Blackwell dispatch failures (`SM Warp Exception: Invalid Address
Space`, ESR 0x10) — via `coral-kmod` kernel module evolution and NVIDIA RM/UVM
ABI debugging.

---

## Findings

### 1. UVM_PAGEABLE_MEM_ACCESS Struct ABI Bug (Fixed)

**Severity:** Critical (silent data misread)
**Files:** `coral-driver/src/nv/uvm/structs.rs`, `coral-driver/src/nv/uvm/mod.rs`

`UvmPageableMemAccessParams` was **4 bytes** but the NVIDIA kernel expects **8 bytes**:

```c
// NVIDIA uvm_ioctl.h
typedef struct {
    NvBool pageableMemAccess; // OUT (1 byte + 3 pad)
    NV_STATUS rmStatus;       // OUT (4 bytes)
} UVM_PAGEABLE_MEM_ACCESS_PARAMS;  // 8 bytes
```

Our struct only had `rm_status: u32` at offset 0, which was reading the
`pageableMemAccess` output field instead of the actual `rmStatus`. The value
`0x00000001` reported as "failure" was actually `pageableMemAccess = true` —
**the ioctl was always succeeding**.

**Fix:** Added `pageable_mem_access: u8` + `_pad: [u8; 3]` before `rm_status`.
Method signature changed to `fn pageable_mem_access(&self) -> DriverResult<bool>`.
Size assertion test added (`assert_eq!(size_of::<UvmPageableMemAccessParams>(), 8)`).

**Pattern for other primals:** When binding C kernel ABIs, always verify struct
sizes match the kernel headers. `NvBool` = `NvU8` = 1 byte, not `u32`.

### 2. VRAM Page Size Mismatch (Fixed)

**Severity:** High (caused FAULT_PDE on every dispatch)
**File:** `coral-kmod/coral_rm_proxy.c` (`coral_rm_alloc_gpu_buffer`)

The kmod's VRAM allocation used `PAGE_SIZE_BOTH` + `PAGE_SIZE_HUGE_2MB` attributes
for 4KB data buffers. This caused the RM to set up 2MB-granularity page directory
entries, but the actual allocation was only 4KB — resulting in `FAULT_PDE
ACCESS_TYPE_VIRT_WRITE` on every first dispatch.

**Fix:** Changed to `PAGE_SIZE_4KB` in `mp.attr` and removed `PAGE_SIZE_HUGE_2MB`
from `mp.attr2`. GPU VAs now spaced at 4KB (0x1000) instead of 2MB (0x200000).

**Before:** `FAULT_PDE` (page directory entry missing)
**After:** `FAULT_PTE` (page table entry — lower level, closer to resolution)

### 3. Remaining: SM Warp Exception Root Cause

**Status:** Diagnosed, not yet fixed
**Severity:** Critical for Blackwell dispatch

The `SM Warp Exception: Invalid Address Space` (ESR 0x10) is **not a memory
mapping issue** — it persists even with system memory via userspace DMA mapping
(no kmod). The root cause chain:

1. `UVM_REGISTER_GPU_VASPACE` fails with `NV_ERR_GPU_IN_FULL` (0x5D)
2. Without UVM VA space registration, replayable page faults can't be serviced
3. `GPU_PROMOTE_CTX` fails from userspace with `INSUFFICIENT_PERMISSIONS` (0x1B)
4. `GR_CTXSW_SETUP_BIND` with `vMemPtr=0` relies on GSP demand-paging context
   buffers, but demand-paging requires UVM fault handling (step 1)
5. SM hits "Invalid Address Space" on first CBUF/context access

**CUDA avoids this** because it has a working UVM fault path (full UVM registration
succeeds for CUDA contexts). Our kmod has kernel privilege to call `GPU_PROMOTE_CTX`
but currently skips it for Blackwell.

**Next step:** Re-enable `GPU_PROMOTE_CTX` in coral-kmod to eagerly allocate GR
context buffers from kernel context, bypassing the demand-paging dependency on UVM.

---

## Test Results

| Metric | Before | After |
|--------|--------|-------|
| Total tests | 40 | 40 |
| Passed | 25 | 25 |
| Failed (Blackwell) | 15 | 15 |
| MMU Faults | FAULT_PDE (page dir) | FAULT_PTE (page table) |
| UVM_PAGEABLE_MEM_ACCESS | "FAILED: 0x01" (misread) | OK (supported=true) |
| Complex dot-product | PASS | PASS |
| SM Warp Exception | Present | Present (root cause identified) |

---

## Architecture Learnings for Ecosystem

### NVIDIA RM/UVM Dispatch Architecture (Blackwell / R580)

```
┌─────────────────────────────────────────────────────────────┐
│                    CUDA's Approach                           │
│  cuCtxCreate → UVM_INITIALIZE → UVM_REGISTER_GPU            │
│            → UVM_PAGEABLE_MEM_ACCESS (query support)        │
│  cuMemAlloc → UVM-managed pages (demand-paged by GPU faults)│
│  cuLaunch  → GSP auto-promotes context, UVM handles faults  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Sovereign Approach                        │
│  coral-kmod: INIT_COMPUTE → RM channel creation             │
│            → GPU_PROMOTE_CTX ← NEEDED (kernel privilege)    │
│            → ALLOC_GPU_BUFFER (VRAM + DMA map)              │
│  coral-driver: QMD build → GPFIFO submit → fence wait       │
└─────────────────────────────────────────────────────────────┘
```

### Key Differences from CUDA

1. **CUDA never calls RM_MAP_MEMORY_DMA** for data buffers — it relies on UVM
   demand-paging. Our sovereign path must either replicate UVM or use explicit
   RM DMA mappings with kernel-context privilege.

2. **GPU_PROMOTE_CTX is kernel-only** on R580 GSP-RM (returns
   `INSUFFICIENT_PERMISSIONS` from userspace). The kmod must call it.

3. **UVM_REGISTER_GPU_VASPACE fails** on desktop Blackwell with `GPU_IN_FULL` —
   CUDA likely uses a different VA space configuration or a separate UVM-managed
   address space.

4. **Page size matters** for RM allocations: requesting huge pages (2MB) for
   small buffers causes page directory incompatibilities. Always use
   `PAGE_SIZE_4KB` for data buffers.

### Composition Patterns for NUCLEUS

The sovereign GPU pipeline demonstrates the **metallic bonding** pattern from
the biomeOS composition model:

- **coral-ember** provides the kernel-side RPC surface (IPC over Unix socket)
- **coral-glowplug** manages lifecycle (modprobe, device creation, permission)
- **coral-kmod** is the kernel agent (privilege escalation boundary)
- **coral-driver** is the userspace orchestrator (QMD build, dispatch, readback)

This pattern generalizes: any primal needing kernel privilege (VFIO, MMIO,
special device access) can use the ember→glowplug→kmod→driver stack. The
kmod exposes a `/dev/` chardev with typed ioctls; the driver wraps it in
safe Rust.

For **neuralAPI from biomeOS**: the `shader.compile.wgsl` capability is
validated for cross-generation SASS output. Once dispatch is fixed, the
sovereign compile path can serve as the backend for `compute.dispatch`
capability in the NUCLEUS graph, replacing wgpu/Vulkan for bare-metal
deployment on known hardware.

---

## Files Changed (coralReef)

| File | Change |
|------|--------|
| `coral-driver/src/nv/uvm/structs.rs` | Fixed `UvmPageableMemAccessParams` (4→8 bytes) |
| `coral-driver/src/nv/uvm/mod.rs` | `pageable_mem_access()` returns `bool`, size test |
| `coral-driver/src/nv/uvm_compute/device.rs` | Updated caller to use new return type |
| `coral-kmod/coral_rm_proxy.c` | Fixed VRAM alloc flags: 4KB pages, no FIXED_ADDR |

## Files Changed (hotSpring)

| File | Change |
|------|--------|
| `barracuda/src/bin/bench_sovereign_parity.rs` | Minor updates |

---

## Handoff Targets

| Team | Action |
|------|--------|
| **coralReef** | Re-enable GPU_PROMOTE_CTX in kmod for Blackwell; allocate context buffers from kernel context |
| **hotSpring** | Update GAP-HS-031 with root cause chain; add Exp 177 journal |
| **primalSpring** | Pattern: ember→glowplug→kmod for any kernel-privilege primal |
| **biomeOS** | `compute.dispatch` capability blocked until Blackwell SM exception resolved |
| **neuralSpring** | Sovereign compile ready; dispatch fix will unblock ML shader execution |
| **toadStool** | Ember absorption path validated; kmod ioctl pattern ready for integration |
