# coralReef VFIO Hardware Validation Results — March 13, 2026

**Source**: hotSpring validation on biomeGate (Titan V, GV100, SM70)
**Test rig**: Titan V bound to `vfio-pci`, IOMMU group 36, kernel 6.17.9
**coralReef**: Phase 10 Iteration 42

---

## Hardware Setup

| Component | Value |
|-----------|-------|
| GPU | NVIDIA Titan V (GV100, SM70) |
| PCI BDF | `0000:4b:00.0` |
| IOMMU group | 36 (GPU + audio, clean isolation) |
| Driver | `vfio-pci` (via `driver_override` + `drivers_probe`) |
| Host GPU | RTX 3090 on `nvidia` proprietary (boot_vga=1, undisturbed) |
| CPU | Threadripper 3970X |
| Kernel | 6.17.9-76061709-generic (Pop!_OS) |
| IOMMU | AMD-Vi, 73 groups |

**Dual-use confirmed**: RTX 3090 stays on nvidia proprietary for display,
Titan V on VFIO for sovereign compute. No reboot needed.

---

## Test Results: 6/7 PASS

```
CORALREEF_VFIO_BDF=0000:4b:00.0 CORALREEF_VFIO_SM=70
cargo test --test hw_nv_vfio --features vfio -- --ignored --test-threads=1
```

| Test | Result | What It Validates |
|------|--------|-------------------|
| `vfio_open_and_bar0_read` | **PASS** | VFIO device open, BAR0 mmap, BOOT0 chip ID read |
| `vfio_alloc_and_free` | **PASS** | DMA buffer allocation via IOMMU, page alignment, mlock |
| `vfio_upload_and_readback` | **PASS** | DMA write + read data round-trip (256 bytes verified byte-by-byte) |
| `vfio_multiple_buffers` | **PASS** | 4 concurrent DMA allocations, sequential free |
| `vfio_free_invalid_handle` | **PASS** | Error path for invalid buffer handle |
| `vfio_readback_invalid_handle` | **PASS** | Error path for invalid buffer handle |
| `vfio_dispatch_nop_shader` | **FAIL** | `FenceTimeout { ms: 5000 }` — GPU never signals completion |

---

## What Works (Validated on Real Hardware)

1. **VFIO container + group**: Open VFIO container, attach group 36, set IOMMU type
2. **BAR0 MMIO via VFIO**: `map_bar(0)` works, `read_u32(BOOT0)` returns valid chip ID
3. **DMA allocation**: `mmap` + `mlock` + `VFIO_IOMMU_MAP_DMA` — IOMMU maps host
   memory into GPU-visible IOVA space
4. **DMA data path**: Upload 256 bytes → readback matches byte-for-byte. The IOMMU
   DMA mapping is functional — host ↔ GPU memory path works.
5. **Multiple buffers**: Concurrent DMA allocations with different IOVAs work correctly
6. **Error handling**: Invalid handle operations return proper errors

**This validates the entire VFIO infrastructure stack.** The plumbing from
userspace → VFIO container → IOMMU group → device fd → BAR0 mmap → DMA mapping
is production-ready.

---

## What Fails: Dispatch (Channel Init Gap)

### Root Cause

`NvVfioComputeDevice::open()` maps BAR0 and allocates DMA buffers but never
creates a **GPU hardware channel**. The NVIDIA GPU's command processor (Host/PFIFO)
does not know about the GPFIFO ring or USERD page.

### What's Missing

The dispatch path does:
```
alloc DMA → upload shader → build QMD → build push buffer → write GPFIFO entry
→ write GP_PUT to USERD → ring doorbell at BAR0+0x0090 → poll GP_GET from USERD
```

But step 0 is never performed:
```
Program PFIFO channel RAM → set GPFIFO base IOVA → set USERD base IOVA
→ enable channel → bind compute engine to channel → submit GR context init
```

Without a channel, the doorbell write is meaningless — the GPU doesn't know
our GPFIFO exists, and GP_GET is never updated (stays 0).

### What Needs to Be Implemented

| Step | Description | Registers/Mechanism |
|------|-------------|---------------------|
| 1 | **PFIFO channel create** | Program channel slot in BAR0 PFIFO range (~0x002000–0x003FFF on Volta). Set channel GPFIFO base, USERD base, engine binding. |
| 2 | **Channel enable** | Set the channel enable bit so PFIFO starts polling GPFIFO. |
| 3 | **Compute engine bind** | Bind `VOLTA_COMPUTE_A` (0xC3C0) to the channel's subchannel 0. |
| 4 | **GR context init** | Submit `PushBuf::gr_context_init()` via the now-functional GPFIFO to initialize the PGRAPH context. Uses `gsp::applicator` firmware entries. |
| 5 | **Doorbell** | Write to the correct per-channel doorbell offset (may differ from 0x0090 on Volta). |

### Approaches

**Path A — hw-learn observation**: Use toadStool's hw-learn observer to trace
nouveau's channel creation on the RTX 3090 (which is on nouveau after a
re-bind), then distill the register sequence into a recipe that can be applied
via BAR0 on the VFIO-bound Titan V.

**Path B — GSP firmware**: GV100 has GSP firmware blobs that contain PFIFO
init sequences. Parse these (similar to `gsp::firmware_parser`) and apply via
BAR0.

**Path C — nouveau source study**: Reverse-engineer the channel create
sequence from `drivers/gpu/drm/nouveau/nvkm/engine/fifo/` (specifically
`gv100.c` for Volta). Translate the register writes into a Rust init sequence.

**Path D — Minimal RUNLIST approach**: On Volta+, PFIFO uses RUNLIST-based
scheduling. Create a minimal channel entry in the runlist, point it at our
GPFIFO/USERD, and trigger a runlist update via BAR0.

### Recommendation

Path C (nouveau source study) is most reliable for Volta. The register
sequences are well-documented in the open-source driver. Path A (hw-learn)
is the long-term sovereign approach and should be pursued in parallel.

---

## Gap 2 Update

**Gap 2 (VFIO hardware validation)** is now **partially resolved**:

- [x] VFIO device open on real hardware
- [x] BAR0 MMIO via VFIO
- [x] DMA allocation and IOMMU mapping
- [x] DMA data round-trip (upload + readback)
- [ ] GPU channel creation via BAR0 MMIO
- [ ] Compute dispatch via VFIO GPFIFO
- [ ] Dispatch sync (GP_GET polling)
- [ ] End-to-end: WGSL → compile → VFIO dispatch → readback

**New sub-gap**: "PFIFO channel init via BAR0" — this is the last code gap
in the sovereign VFIO pipeline. Everything else is validated.

---

## Test Rig Setup (Reproducible)

```bash
# On biomeGate (or any machine with 2+ NVIDIA GPUs):

# 1. Load VFIO modules + bind secondary GPU
sudo bash -c '
modprobe vfio-pci
echo vfio-pci > /sys/bus/pci/devices/0000:4b:00.0/driver_override
echo 0000:4b:00.0 > /sys/bus/pci/drivers_probe
echo vfio-pci > /sys/bus/pci/devices/0000:4b:00.1/driver_override
echo 0000:4b:00.1 > /sys/bus/pci/drivers_probe
chmod 0666 /dev/vfio/36
'

# 2. Run tests
cd coralReef
CORALREEF_VFIO_BDF=0000:4b:00.0 CORALREEF_VFIO_SM=70 \
  cargo test --test hw_nv_vfio --features vfio -- --ignored --test-threads=1

# 3. Restore GPU to nouveau (optional)
sudo bash -c '
echo > /sys/bus/pci/devices/0000:4b:00.0/driver_override
echo 0000:4b:00.0 > /sys/bus/pci/devices/0000:4b:00.0/driver/unbind 2>/dev/null
echo 0000:4b:00.0 > /sys/bus/pci/drivers_probe
'
```

---

## Impact

This is the **first time coralReef has run on real VFIO-bound GPU hardware**.
The 6/7 pass rate validates the entire VFIO infrastructure layer. The remaining
gap (channel init) is a well-defined driver task, not an architectural problem.

The dual-use setup works: RTX 3090 on nvidia for gaming, Titan V on VFIO for
sovereign compute, same machine, no reboot.

---

*Validated by hotSpring on biomeGate, March 13, 2026.*
