# coralReef → Ecosystem: Phase 10 Iteration 31 — Deep Debt + NVIDIA Pipeline Fixes

**Date:** March 10, 2026  
**From:** coralReef Phase 10, Iteration 31  
**To:** hotSpring / toadStool / barraCuda / All Springs  
**License:** AGPL-3.0-only  
**Covers:** Iteration 30 → Iteration 31 (includes hotSpring Exp 051 response)  

---

## Executive Summary

- **1509 tests passing, 0 failed, 54 ignored** (+22 passing, -22 ignored from Iter 30)
- **22 tests un-ignored**: RDNA2 spring absorption (7), repair_ssa fixes (3), f64 log2 (1), AMD FRnd (4), vec3<f64> (2), SPIR-V gaps (5)
- **Nouveau UAPI migration**: New kernel 6.6+ ioctl wrappers (`vm_init`, `vm_bind_map`, `vm_bind_unmap`, `exec_submit`) — ready for integration testing
- **UVM device alloc fix**: Root-caused `NV_ERR_OPERATING_SYSTEM` (0x1F) — missing `Nv0080AllocParams.device_id`. Fix implemented, needs hardware re-test
- **SU3 lattice preamble**: 10-function `su3_f64_preamble.wgsl` with auto-prepend + dependency chaining
- **SPIR-V translation gaps closed**: `Relational` expressions + non-literal constant initializers + critical edge phi handling

---

## Part 1: hotSpring Experiment 051 Response

### Findings Absorbed

hotSpring's Exp 051 (March 10, 2026) tested Iter 30 (`472e5b8`) against:
- **Titan V** (GV100 SM70) via nouveau/NVK  
- **RTX 3090** (GA102 SM86) via nvidia-drm proprietary

Key findings incorporated:

| Finding | Root Cause | Fix Applied |
|---------|-----------|-------------|
| Nouveau channel EINVAL (all 5 classes) | Legacy `DRM_NOUVEAU_CHANNEL_ALLOC` rejected on kernel 6.17+ Volta | New UAPI ioctls defined + wrappers implemented |
| UVM device alloc `0x1F` | `RM_ALLOC(NV01_DEVICE_0)` called without `Nv0080AllocParams` — RM can't identify target GPU | `alloc_device()` now passes `device_id` via proper alloc params |
| `multi_gpu_enumerates_both` expects AMD | Test asserted `has_amd` on 2×NVIDIA system | Renamed to `multi_gpu_enumerates_multiple`, handles any 2+ GPU topology |
| 45/46 sovereign compile parity | `complex_f64` is utility include, not standalone shader | Expected — no action needed |
| Both GPUs dispatch via wgpu/NVK Vulkan | NVK uses new UAPI (`VM_INIT/VM_BIND/EXEC`) | Our wgpu path already works; sovereign path now fully wired |

### Sovereign Pipeline State (post-Iter 31)

| Path | Status | Blocker |
|------|--------|---------|
| **wgpu/Vulkan** (both GPUs) | **Working** | None — NVK on Titan V, proprietary on RTX 3090 |
| **Nouveau sovereign** (Titan V) | **Fully wired** | `NvDevice::open_from_drm` auto-detects VM_INIT, alloc uses vm_bind_map, dispatch uses exec_submit. Needs hardware test. |
| **nvidia-drm/UVM** (RTX 3090) | **Fix deployed** | Re-test: `alloc_device()` with `Nv0080AllocParams` — should resolve `0x1F` |

---

## Part 2: Deep Debt Resolution (Iter 31 Summary)

### Compiler Fixes

| Fix | Impact |
|-----|--------|
| `repair_ssa` unreachable block elimination | Forward reachability analysis; `torsion_angles_f64` + complex CFG shaders compile |
| `repair_ssa` critical edge phi handling | Multi-successor phi source insertion; SPIR-V roundtrip tests unblocked |
| f64 `log2` widening from `pow` lowering | `hill_dose_response_f64` and other pow-dependent shaders fixed |
| AMD `FRnd` encoding | `V_TRUNC/FLOOR/CEIL/RNDNE` for F32 (VOP1) and F64 (VOP3) on RDNA2 |
| `vec3<f64>` SM70 scalarization | Componentwise ops for 3-element f64 vectors |
| `emit_f64_cmp` widening | Defensive 1→2 component widening for mixed-precision comparisons |
| SPIR-V `Relational` expressions | `IsNan`, `IsInf`, `All`, `Any` implemented |
| SPIR-V non-literal const init | `Compose`, `Splat`, recursive `Constant` in global expressions |

### Preamble System

| Preamble | Functions | Auto-detect |
|----------|-----------|-------------|
| `complex_f64_preamble.wgsl` | Complex64 struct + 15 ops | `Complex64` or `c64_` |
| `prng_preamble.wgsl` | `xorshift32`, `wang_hash` | `xorshift32` or `wang_hash` |
| `su3_f64_preamble.wgsl` (NEW) | 10 SU(3) matrix ops | `su3_` prefix |
| Dependency chain | Complex64 → PRNG → SU3 → df64 → f32 transcendental | Automatic |

### Driver Fixes

| Fix | Impact |
|-----|--------|
| Nouveau new UAPI structs | `NouveauVmInit`, `NouveauVmBind`, `NouveauExec` + entry structs |
| Nouveau new UAPI ioctls | `vm_init()`, `vm_bind_map()`, `vm_bind_unmap()`, `exec_submit()` |
| UVM `Nv0080AllocParams` | `alloc_device()` passes `device_id` for GPU targeting |
| UVM `Nv2080AllocParams` | `alloc_subdevice()` passes `sub_device_id` |
| RM status constants | `NV_ERR_INVALID_ARGUMENT`, `NV_ERR_OPERATING_SYSTEM`, `NV_ERR_INVALID_OBJECT_HANDLE` |
| Multi-GPU test generalization | Handles any 2+ GPU topology (AMD+NV, 2×NV, etc.) |
| NvDevice new UAPI auto-detect | `open_from_drm` tries `vm_init()` first, falls back to legacy; `alloc` uses `vm_bind_map` with VA bump allocator; `dispatch` uses `exec_submit`; `free` uses `vm_bind_unmap` |
| SM70 encoder `unwrap()→expect()` | 8 production `unwrap()` in `sm70_encode/{control,encoder}.rs` replaced |
| `gem_info` error propagation | `NvDevice::alloc` no longer swallows errors with `unwrap_or((0,0))` |
| `ioctl.rs` smart refactor | 1039 LOC → `ioctl/{mod.rs(692), new_uapi.rs(210), diag.rs(159)}` |
| Device path constants | `NV_CTL_PATH`, `NV_UVM_PATH`, `NV_GPU_PATH_PREFIX`, `DRI_RENDER_PREFIX` |

---

## Part 3: What hotSpring Should Re-Test

### Priority 1: UVM Device Alloc (RTX 3090)

```bash
cd coralReef
git pull
cargo test uvm -p coral-driver -- --ignored --nocapture 2>&1 | tee uvm_retest.log
```

**Expected**: `rm_client_alloc_device` should now PASS (was `0x1F`).
If still failing, capture the new status code — we have named constants for diagnosis.

### Priority 2: Nouveau New UAPI Probe (Titan V)

The new UAPI is now fully wired into `NvDevice::open_from_drm` — it auto-detects
kernel 6.6+ support via `vm_init()` and uses the new path if available.

```bash
cargo test --test hw_nv_probe -p coral-driver -- --ignored --nocapture 2>&1 | tee nv_probe_iter31.log
cargo test --test hw_nv_nouveau -p coral-driver -- --ignored --nocapture 2>&1 | tee nouveau_iter31.log
```

### Priority 3: Multi-GPU Enumeration

```bash
cargo test --test hw_nv_probe -p coral-driver -- --ignored multi_gpu --nocapture 2>&1 | tee multi_gpu_iter31.log
```

**Expected**: `multi_gpu_enumerates_multiple` should now PASS (was `multi_gpu_enumerates_both` expecting AMD).

### Priority 4: Full Parity

```bash
cargo test --test parity_compilation -p coral-reef 2>&1 | tee parity_iter31.log
```

---

## Part 4: Remaining Pipeline to Go Live

| Item | Owner | Status | Unblocks |
|------|-------|--------|----------|
| ~~Wire new UAPI into `NvDevice::open_from_drm`~~ | coralReef | **DONE** | Titan V E2E sovereign dispatch |
| ~~ioctl.rs refactor (>1000 LOC)~~ | coralReef | **DONE** | Smart split: mod.rs + new_uapi.rs + diag.rs |
| ~~SM70 encoder `unwrap()` elimination~~ | coralReef | **DONE** | All replaced with `expect()` |
| ~~Device path hardcoding~~ | coralReef | **DONE** | Constants in uvm.rs + drm.rs |
| ~~biomeOS references~~ | coralReef | **DONE** | All evolved to ecoPrimals |
| ~~COMPILATION_DEBT_REPORT stale entries~~ | coralReef | **DONE** | Section 5 updated, 9/9 resolved |
| UVM re-test with `Nv0080AllocParams` | hotSpring | Next | RTX 3090 UVM pipeline |
| Coverage 63% → 90% | coralReef | Ongoing | Production readiness |
| Pred→GPR coercion chain | coralReef | P2 | Edge cases in encoding |

---

## Test Counts

| Metric | Iter 30 | Iter 31 | Delta |
|--------|---------|---------|-------|
| Passing | 1487 | 1509 | +22 |
| Failed | 0 | 0 | 0 |
| Ignored | 76 | 54 | -22 |
| Clippy warnings | 0 | 0 | 0 |
| Line coverage | 63% | 63% | — |

---

## Addendum: Doc Cleanup (Iteration 31 Final)

- README.md updated to Iter 31, nouveau description updated with new UAPI + rustix
- EVOLUTION.md dependency landscape corrected: coral-driver uses rustix, not libc
- COMPILATION_DEBT_REPORT.md: Section 5 updated (9/9 shaders resolved), unwrap audit complete
- WHATS_NEXT.md, ABSORPTION.md, HARDWARE_TESTING.md headers updated to Iteration 31
- `discovery.rs` doc comment: biomeOS → ecoPrimals
- All root docs now consistent with Iteration 31 state
