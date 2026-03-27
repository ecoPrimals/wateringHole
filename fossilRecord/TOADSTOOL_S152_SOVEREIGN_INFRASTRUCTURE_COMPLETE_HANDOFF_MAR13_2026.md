# toadStool S152 — Sovereign Infrastructure Complete Handoff

**Date**: March 13, 2026
**Session**: S152
**Pins**: hotSpring v0.6.31, coralReef Iter 42, barraCuda v0.35

---

## Summary

Resolved all toadStool-owned sovereign compute gaps (1, 5, 7, 8, 9, 12).
Sovereign dispatch pipeline fully wired. OS keyring integration, cross-gate
GPU pooling, and mock hardware layers for headless CI all implemented.
Infrastructure phase complete — only VFIO hardware validation (Gap 2) remains.

---

## Changes

### 1. Sovereign Dispatch Pipeline (Gap 1)

`compute.dispatch.submit` accepts compiled GPU binaries from coralReef, resolves
BDF (prefers VFIO), performs thermal safety check, and forwards to coralReef's
`compute.dispatch.execute`. Also: `status`, `result`, `capabilities` methods.
`SOVEREIGN_BINARY_PIPELINE = true`.

**File**: `crates/server/src/pure_jsonrpc/handler/dispatch.rs`

### 2. Multi-Architecture Register Classification (Gap 5)

`GpuGen` enum (Maxwell→Ampere) with `from_chip()`. `classify_register_for_gen()`
provides per-generation register tables from envytools/NVIDIA docs. `classify_events`
accepts an optional chip hint for architecture context.

**File**: `crates/core/hw-learn/src/distiller/classify.rs`

### 3. Multi-GPU Parallel Init (Gap 12)

`compute.hardware.auto_init_all` discovers all GPUs, finds best recipes, and applies
them in parallel via `tokio::task::spawn_blocking`. Per-GPU thermal checks, rollback
on failure, succeeded/failed/skipped reporting.

**File**: `crates/server/src/pure_jsonrpc/handler/hw_learn.rs`

### 4. Huge Page DMA (Infrastructure)

`DmaAllocator::allocate_huge()` with `HugePageSize::Huge2M` and `Huge1G` via
`mmap_anonymous` + `MAP_HUGETLB`. `supports_huge_pages()` checks sysfs for
kernel huge page availability.

**File**: `crates/core/nvpmu/src/dma.rs`

### 5. MSI-X / eventfd Completion (Infrastructure)

`VfioMsixInterrupt::configure()` creates an eventfd and wires it to the MSI-X
vector via `VFIO_DEVICE_SET_IRQS` ioctl. `wait()` and `wait_timeout()` for
interrupt-driven GPU completion notification.

**File**: `crates/core/nvpmu/src/vfio.rs`

### 6. GPU Reset and Power Management (Infrastructure)

`GpuPowerController` for PCI-level control: `power_state()` (D0/D3hot), `reset()`
(Function-Level Reset), `power_on()`/`power_suspend()`, `available_reset_methods()`,
`power_limit_uw()`. All via sysfs — no kernel module dependency.

**File**: `crates/core/nvpmu/src/power.rs`

### 7. `extern "C"` Elimination (Deep Debt)

Last `extern "C"` block in workspace (raw `ioctl` in `nouveau_drm.rs`) replaced
with `rustix`-based `DrmIoctl` implementing `rustix::ioctl::Ioctl`. Dynamic opcode
construction. Zero `extern "C"` remaining in workspace.

**File**: `crates/core/hw-learn/src/applicator/nouveau_drm.rs`

### 8. OS Keyring Integration (Gap 8)

`os_keyring` module — `secret-tool` (D-Bus SecretService) on Linux, `security`
(macOS Keychain) on macOS. Wired as step 2.5 in `resolve_credential` chain between
file-based credentials and security provider. No new crate dependencies.

**File**: `crates/core/common/src/os_keyring.rs`

### 9. Cross-Gate GPU Pooling (Gap 9)

`RemoteDispatcher` forwards compute jobs to remote toadStool instances via Unix
socket or TCP. `GateGpuInfo.endpoint` for remote gates. `compute_submit` auto-forwards
when router selects remote gate, falls back to local on transport failure.
`compute.dispatch.forward` JSON-RPC method for explicit relay.

**Files**: `crates/server/src/cross_gate.rs`, `crates/server/src/pure_jsonrpc/handler/job.rs`

### 10. Mock Hardware Layers (Gap 7)

`MockV4l2Device` — synthetic frame generation (Solid, Gradient, Counter, Random
patterns), error injection, capture lifecycle, format switching. `MockVfioDevice` —
BAR0 register simulation, access logging, `RegisterAccess` trait implementation,
error injection. Headless CI can now test V4L2 and VFIO code paths.

**Files**: `crates/testing/src/mocks/v4l2.rs`, `crates/testing/src/mocks/vfio.rs`

### 11. Unsafe Audit (Deep Debt)

All `unified_memory/` and `display/` unsafe blocks audited — all justified for
FFI/hardware. `MmapBuffer::as_slice()` centralizes V4L2 mmap unsafe. `read_frame`
no longer has inline unsafe. `// SAFETY:` comments on all remaining blocks.

---

## Impact on Other Primals

| Primal | Impact |
|--------|--------|
| coralReef | Can now dispatch compiled binaries to toadStool via `compute.dispatch.submit`. MSI-X available for completion notification. Huge page DMA improves channel bandwidth. |
| barraCuda | No direct impact — math dispatch unchanged. Multi-arch classifier means future hardware recipes are more accurate. |
| hotSpring | Cross-gate pooling means hotSpring jobs can be routed to any toadStool in the mesh. GPU power management available for thermal-aware scheduling. |
| songBird | Remote dispatch relay uses songBird mesh endpoints. `GateGpuInfo.endpoint` carries relay address. |

---

## Gap Status After S152

| Gap | Status |
|-----|--------|
| 1 — Dispatch client | ✅ Resolved |
| 2 — VFIO hardware validation | **Open** — needs physical test rig |
| 3 — Error recovery | ✅ Resolved (S151) |
| 4 — DMA buffers | ✅ Resolved (S151) |
| 5 — Multi-arch classifier | ✅ Resolved |
| 6 — Unified PCI discovery | ✅ Resolved (S151) |
| 7 — Test coverage / mock layers | ✅ Resolved |
| 8 — OS keyring | ✅ Resolved |
| 9 — Cross-gate pooling | ✅ Resolved |
| 10 — Thermal safety | ✅ Resolved (S151) |
| 11 — VFIO bind/unbind | ✅ Resolved (S151) |
| 12 — Multi-GPU init | ✅ Resolved |
| 13 — Conv2D/Pool shaders | barraCuda-owned |
| 14 — E2E integration tests | Blocked on Gap 2 |
| 15 — Streaming bio I/O | Deferred |

**All toadStool-owned software gaps (1–12) are now resolved.**

---

## Test Status

20,262 tests passing, 0 failures. ~150K production lines.
