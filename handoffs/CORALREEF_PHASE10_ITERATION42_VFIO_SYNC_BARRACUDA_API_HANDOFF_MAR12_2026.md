# coralReef — Iteration 42: VFIO Sync + barraCuda API

**Date**: March 12, 2026
**Primal**: coralReef
**Phase**: 10 — Iteration 42

---

## Summary

Two critical gaps closed for the sovereign compute pipeline:

1. **VFIO `sync()` — proper GPU completion polling** via USERD DMA page GP_GET
2. **`GpuContext::from_vfio()` — public convenience API** unblocking barraCuda integration

## What Changed

### 1. VFIO GPFIFO Completion Polling

`NvVfioComputeDevice::sync()` was previously a no-op that only freed inflight
buffers without waiting for GPU completion. This made `readback()` after
`dispatch()` potentially return stale data.

**Fix**: `poll_gpfifo_completion()` now reads GP_GET from the USERD DMA page
via volatile pointer read, matching the UVM path's pattern exactly:

- GPU writes GP_GET to USERD page offset 0x04 as it consumes GPFIFO entries
- Host polls with `std::ptr::read_volatile` in a spin-loop (10µs sleep)
- 5-second timeout returns `DriverError::FenceTimeout`
- `submit_pushbuf()` now also writes GP_PUT to USERD page offset 0x00

**Files changed**:
- `crates/coral-driver/src/nv/vfio_compute.rs` — `userd` module, `poll_gpfifo_completion()`, `submit_pushbuf()` GP_PUT write, `sync()` calls polling

### 2. GpuContext::from_vfio() Convenience API

barraCuda's `CoralReefDevice::from_vfio_device()` was a stub returning
`Err("blocked on coral-gpu VFIO support")`. The existing `from_descriptor_with_path`
path worked but required callers to know the full descriptor format.

**Added**:
- `GpuContext::from_vfio(bdf: &str)` — auto-detects SM from sysfs, opens device
- `GpuContext::from_vfio_with_sm(bdf: &str, sm: u32)` — explicit SM override

Both are `#[cfg(all(target_os = "linux", feature = "vfio"))]` gated.

**Files changed**:
- `crates/coral-gpu/src/lib.rs` — two new public methods on `GpuContext`

## barraCuda Integration Path

barraCuda can now replace its stub:

```rust
// Before (stub in barraCuda):
pub fn from_vfio_device(pci_address: &str, ...) -> Result<Self> {
    Err(BarracudaError::Device("blocked on coral-gpu VFIO support"))
}

// After (using coral-gpu):
pub fn from_vfio_device(pci_address: &str, ...) -> Result<Self> {
    let ctx = coral_gpu::GpuContext::from_vfio(pci_address)?;
    Ok(Self::new(ctx))
}
```

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1669 default + 35 VFIO, 0 failed, 64+5 ignored |
| Clippy | 0 warnings |
| Formatting | Clean |
| New unsafe blocks | 1 (volatile read in poll_gpfifo_completion, with SAFETY comment) |

## Dependencies

- **barraCuda**: Can now wire `CoralReefDevice::from_vfio_device()` using `GpuContext::from_vfio()`
- **toadStool**: No changes needed — VFIO hardware contract from Iteration 41 unchanged
- **hotSpring**: No changes needed

---

*coralReef Iteration 42 — VFIO dispatch is now functionally complete:
open → alloc → upload → dispatch → sync (with proper GPU completion) → readback.
barraCuda has a clean public API to wire against.*
