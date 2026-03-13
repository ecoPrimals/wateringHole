# coralReef Phase 10 — Iteration 41: VFIO Sovereign GPU Dispatch

**Date**: March 12, 2026
**Primal**: coralReef
**Iteration**: 41

---

## Summary

coralReef now has a complete VFIO-based GPU dispatch backend. This is the
maximum sovereignty path: no kernel GPU driver (nouveau/nvidia) needed,
only VFIO-IOMMU plumbing. The GPU is accessed via direct BAR0 MMIO
register writes and IOMMU-mapped DMA buffers.

## What Changed

### 1. VFIO Core Module (`coral-driver/src/vfio/`)

New module with 4 files implementing the Linux VFIO API in pure Rust:

- **`types.rs`** — `repr(C)` kernel ABI structs (VfioDeviceInfo, VfioRegionInfo,
  VfioGroupStatus, VfioDmaMap, VfioDmaUnmap, PollConfig) and ioctl opcode
  constants matching `<linux/vfio.h>`
- **`ioctl.rs`** — Safe wrappers over VFIO ioctls using rustix: container
  API version/extension/IOMMU, group status/container/device_fd, device
  info/region_info/reset, DMA map/unmap
- **`dma.rs`** — `DmaBuffer`: page-aligned, mlock'd, IOMMU-mapped host
  memory with auto-cleanup on drop (munlock → DMA unmap → dealloc)
- **`device.rs`** — `VfioDevice`: full lifecycle (container → group → device fd),
  `MappedBar` for MMIO, IOMMU group discovery from sysfs

### 2. NvVfioComputeDevice (`nv/vfio_compute.rs`)

Implements `ComputeDevice` trait via VFIO:

- Opens GPU via `VfioDevice::open(bdf)`, maps BAR0, reads BOOT0 chip ID
- DMA-backed GPFIFO ring (128 entries) + USERD doorbell page
- User buffers are DMA-allocated with monotonically increasing IOVAs
- `dispatch()` builds QMD + pushbuf (reusing existing builders), writes
  GPFIFO entry, rings USERD doorbell via BAR0 write
- `sync()` frees inflight temporaries (full BAR0 polling pending)

### 3. Feature Gate and Discovery

- `--features vfio` on both `coral-driver` and `coral-gpu`
- `DriverPreference` sovereign order: `vfio` > `nouveau` > `amdgpu` > `nvidia-drm`
- `discover_vfio_nvidia_bdf()`: scans `/sys/bus/pci/drivers/vfio-pci/`
  for NVIDIA vendor ID devices
- `vfio_detect_sm()`: maps PCI device ID to SM architecture
- `from_descriptor("nvidia", _, Some("vfio"))`: explicit VFIO creation

### 4. Tests

- 27 unit tests in VFIO core (type defaults, struct layout, ABI sizes,
  page alignment math, ioctl adapter behavior)
- 8 unit tests in NvVfioComputeDevice (GPFIFO encoding, IOVA layout,
  constants, error paths)
- 5 ignored hardware integration tests (require `CORALREEF_VFIO_BDF` env var)

## Metrics

| Metric | Value |
|--------|-------|
| Default workspace tests | 1669 passing, 0 failed |
| VFIO feature tests | +35 passing (total 201 in coral-driver) |
| HW integration tests | 5 (ignored, needs VFIO hardware) |
| Clippy warnings | 0 |
| Fmt check | Clean |
| New files | 6 (4 vfio core + 1 vfio_compute + 1 integration test) |

---

## toadStool Hardware Contract

**This section defines what toadStool must provide for coralReef's VFIO
dispatch to function.** This is the "fractal interface" — coralReef owns
the dispatch, toadStool owns the hardware setup.

### Prerequisites toadStool Must Satisfy

1. **GPU bound to `vfio-pci` driver**
   ```bash
   # Unbind from current driver
   echo "0000:01:00.0" > /sys/bus/pci/devices/0000:01:00.0/driver/unbind
   # Bind to vfio-pci
   echo "10de XXXX" > /sys/bus/pci/drivers/vfio-pci/new_id
   ```

2. **IOMMU enabled in kernel**
   - Intel: `intel_iommu=on` kernel parameter
   - AMD: `amd_iommu=on` kernel parameter
   - Verify: `/sys/bus/pci/devices/{bdf}/iommu_group` symlink exists

3. **VFIO group permissions**
   - udev rule or group membership for `/dev/vfio/*`
   - Example udev rule:
     ```
     SUBSYSTEM=="vfio", OWNER="root", GROUP="vfio", MODE="0660"
     ```

4. **All devices in IOMMU group bound to vfio-pci**
   - VFIO requires ALL devices in the same IOMMU group to be bound
   - Common issue: audio device on same GPU PCIe function

### What coralReef Does (toadStool Does NOT Need To Do)

- Opens `/dev/vfio/vfio` container
- Opens `/dev/vfio/{group}` and attaches to container
- Gets device fd via `VFIO_GROUP_GET_DEVICE_FD`
- Maps BAR0 via `mmap(device_fd, region_offset)`
- Allocates DMA buffers (page-aligned, mlock'd, IOMMU-mapped)
- Writes GPFIFO entries and rings USERD doorbell
- Builds QMD and push buffers from coral-reef compiler output

### Future Contract Extensions

- **eventfd for IRQ**: toadStool may need to configure MSI-X interrupts
  for completion notification (currently coralReef uses polling)
- **GPU reset recovery**: toadStool handles PCI-level reset if GPU hangs
- **Power management**: toadStool manages GPU power state transitions

### Discovery Interface

coralReef discovers VFIO-bound GPUs by scanning:
```
/sys/bus/pci/drivers/vfio-pci/{bdf}/vendor  # must be 0x10de (NVIDIA)
/sys/bus/pci/devices/{bdf}/iommu_group      # symlink to group number
/sys/bus/pci/devices/{bdf}/device           # PCI device ID for SM detection
```

toadStool should ensure these sysfs paths are readable by the coralReef
process user.

---

## Architecture Diagram

```text
┌─────────────────────────────────────────────────────────┐
│                    coralReef                              │
│  ┌──────────────┐  ┌──────────────────────────────────┐ │
│  │  coral-reef   │  │        coral-driver               │ │
│  │  (compiler)   │  │  ┌────────────┐ ┌─────────────┐  │ │
│  │  WGSL→binary  │  │  │ vfio/      │ │ nv/         │  │ │
│  │               │  │  │ types.rs   │ │ vfio_       │  │ │
│  │               │  │  │ ioctl.rs   │ │ compute.rs  │  │ │
│  │               │  │  │ dma.rs     │ │ (Compute    │  │ │
│  │               │  │  │ device.rs  │ │  Device)    │  │ │
│  │               │  │  └────────────┘ └─────────────┘  │ │
│  └──────────────┘  └──────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
         │                       │
         │              ┌────────┴────────┐
         │              │   VFIO/IOMMU    │
         │              │  /dev/vfio/*    │
         │              └────────┬────────┘
         │                       │
┌────────┴───────────────────────┴────────────────────────┐
│                     toadStool                            │
│  - Bind GPU to vfio-pci                                  │
│  - Enable IOMMU                                          │
│  - Set /dev/vfio/* permissions                           │
│  - Handle PCIe-level reset/power                         │
└─────────────────────────────────────────────────────────┘
```
