# coralReef Iteration 68 — W1 Header Fix + Firmware Metadata Wiring

**Date:** 2026-03-25
**From:** hotSpring (Exp 093) → coralReef (coral-driver)
**Status:** Code complete, compiles clean, awaiting hardware validation

## What Changed

### Bug Fix: W1 Header Stripping in Direct PIO Boot Path

`fecs_boot.rs` `FecsFirmware::load()` and `GpccsFirmware::load()` previously loaded raw `*_bl.bin` files including `nvfw_bin_hdr` + `nvfw_hs_bl_desc` headers. The falcon attempted to execute header bytes as instructions, causing exception `0x0307` at PC=0 (Exp 091 root cause for direct PIO path).

**Fix:** BL files now parsed through `GrBlFirmware::parse()` — extracts code section only, computes `bl_imem_off` from `start_tag << 8`.

### Architecture: Correct IMEM Layout

Previous layout (wrong):
```
IMEM[0]          = BL (with headers)
IMEM[BL.len()]   = inst
BOOTVEC          = 0
```

Fixed layout:
```
IMEM[0]          = inst (application code)
IMEM[bl_imem_off]= BL (stripped code, position-dependent)
BOOTVEC          = bl_imem_off
```

### Firmware-Derived BOOTVEC (no more hardcoded offsets)

`FalconBootvecOffsets` struct carries firmware-derived BL IMEM offsets. `attempt_acr_mailbox_command()` now accepts these instead of using local `const GPCCS_BL_IMEM_OFF: u32 = 0x3400`. The solver constructs offsets from `fw.gpccs_bl.bl_imem_off()` / `fw.fecs_bl.bl_imem_off()`.

### Named FBIF Register Constants

`FBIF_TRANSCFG` (0x624), `FBIF_TARGET_PHYS_VID` (0x01), `FBIF_PHYSICAL_OVERRIDE` (0x80) added to `registers.rs`. All raw `0x624` literals in `sec2_hal.rs` replaced.

## Files Touched

| Crate | File | Summary |
|-------|------|---------|
| coral-driver | `src/nv/vfio_compute/fecs_boot.rs` | `GrBlFirmware` parsing, `bl_imem_off` fields, `falcon_boot()` + `falcon_boot_probed()` signature |
| coral-driver | `src/nv/vfio_compute/acr_boot/strategy_mailbox.rs` | `FalconBootvecOffsets`, firmware-derived BOOTVEC fix |
| coral-driver | `src/nv/vfio_compute/acr_boot/solver.rs` | Construct + pass `FalconBootvecOffsets` |
| coral-driver | `src/nv/vfio_compute/acr_boot/mod.rs` | Export `GrBlFirmware`, `FalconBootvecOffsets` |
| coral-driver | `src/nv/vfio_compute/acr_boot/sec2_hal.rs` | Named FBIF constants |
| coral-driver | `src/vfio/channel/registers.rs` | `FBIF_TRANSCFG`, target/override constants |
| coral-driver | `tests/hw_nv_vfio/falcon.rs` | Fixed `vfio_sovereign_gr_boot`, `vfio_fecs_acr_boot_and_probe` |

## Build Status

- `cargo check -p coral-driver`: clean (0 new warnings)
- `cargo check -p coral-driver --tests --features vfio`: clean (0 new warnings)
- Full workspace: clean

## Next: Hardware Validation

Priority experiment (post-nouveau warm swap):

```bash
coralctl swap 0000:03:00.0 nouveau && sleep 10
coralctl swap 0000:03:00.0 vfio
cargo test vfio_sovereign_gr_boot --features vfio -p coral-driver -- --nocapture --ignored
```

Success = `gpccs_exci == 0 && gpccs_pc != 0`. If FECS signals ready via CTXSW_MAILBOX, L10+L11 are cracked.
