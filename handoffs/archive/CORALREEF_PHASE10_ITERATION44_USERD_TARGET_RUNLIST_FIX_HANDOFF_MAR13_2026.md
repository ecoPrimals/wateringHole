# coralReef — Iteration 44: USERD_TARGET + INST_TARGET Runlist Fix

**Date**: March 13, 2026
**Primal**: coralReef
**Phase**: 10 — Iteration 44

---

## Summary

Root cause fix for the VFIO dispatch `FenceTimeout` (7th test failure on
biomeGate Titan V). hotSpring's hardware debugging identified that the
PBDMA never reads the USERD page because the runlist channel entry had
incorrect memory aperture targets.

## Root Cause

The Volta PBDMA reads the USERD pointer from the **runlist channel entry**
(not just from RAMFC). The runlist DW0 has `USERD_TARGET[3:2]` which
tells the PBDMA where the USERD page is located:

- `0` = VRAM (wrong — USERD is in host system memory via IOMMU DMA)
- `2` = SYS_MEM_COHERENT (correct for VFIO DMA buffers)

Similarly, DW2 has `INST_TARGET[5:4]` for the instance block location.

Without the correct targets, the PBDMA reads from VRAM at the IOVA
address (finding nothing), never sees `GP_PUT`, and never fetches
GPFIFO entries.

## What Changed

### `crates/coral-driver/src/vfio/channel.rs`

**Runlist DW0** — added `USERD_TARGET(SYS_MEM_COH=2)` in bits [3:2]:

```rust
(userd_iova as u32 & 0xFFFF_FE00) | (TARGET_SYS_MEM_COHERENT << 2) | (runq << 1)
```

**Runlist DW2** — added `INST_TARGET(SYS_MEM_NCOH=3)` in bits [5:4]:

```rust
(INSTANCE_IOVA as u32 & 0xFFFF_F000) | (TARGET_SYS_MEM_NCOH << 4) | self.channel_id
```

### Target Encoding Reference

| Encoding scheme | 0 | 1 | 2 | 3 |
|-----------------|---|---|---|---|
| PCCSR / RAMIN / Runlist | VRAM | — | SYS_MEM_COH | SYS_MEM_NCOH |
| PBDMA / RAMFC | VRAM | SYS_MEM_COH | SYS_MEM_NCOH | — |

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1669 default + 48 VFIO, 0 failed, 66+8 ignored |
| Clippy | 0 warnings |
| Formatting | Clean |
| New tests | 2 (DW0 USERD_TARGET encoding, DW2 INST_TARGET encoding) |

## Expected Hardware Result

After this fix, on Titan V:
- PBDMA USERD register should show the USERD IOVA (~0x2000), not 0
- PBDMA GP_PUT should read 1 after host writes to USERD
- `vfio_dispatch_nop_shader` should pass (7/7)

## Dependencies

- **hotSpring**: Provided the root cause analysis via CUDA-as-oracle BAR0 comparison
- **toadStool**: No changes needed — VFIO hardware contract unchanged
- **barraCuda**: No changes needed — `GpuContext::from_vfio()` API unchanged

---

*coralReef Iteration 44 — The USERD_TARGET fix addresses the final known
blocker for VFIO compute dispatch. Hardware revalidation on Titan V will
confirm 7/7 test pass rate.*
