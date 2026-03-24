# coralReef Handoff: WPR Construction Fix (W1-W7)

**From:** hotSpring (Exp 087 analysis)
**Date:** 2026-03-24
**Priority:** ~~CRITICAL~~ **APPLIED AND VALIDATED**
**Files modified:** `crates/coral-driver/src/nv/vfio_compute/acr_boot/firmware.rs`, `wpr.rs`

> **STATUS: APPLIED (2026-03-24)**
> All W1-W7 fixes implemented in `firmware.rs` + `wpr.rs`. Hardware validated on
> Titan #1 (0000:03:00.0) post-nouveau. ACR processes WPR, BOOTSTRAP_FALCON
> commands acknowledged (mb0=1, mb1=falcon_id). FECS/GPCCS reach cpuctl=0x12
> (HALTED+ALIAS_EN). **Layer 8 SOLVED.** New frontier: Layer 9 (falcon halt release).
> Changes are in coralReef working tree (`git status` shows 2 modified files).

## Summary

Exp 087 performed a byte-level comparison of `build_wpr()` against nouveau's
`gp102_acr_wpr_build` and found 7 bugs in WPR image construction. Two are
critical and together explain why ACR COPY (status=1) never completes.

## Root Cause

The `gr/fecs_bl.bin` and `gr/gpccs_bl.bin` files are NOT raw bootloader code.
They are packaged firmware with headers:

```
[0x000..0x018]  nvfw_bin_hdr       (magic, offsets)
[0x018..0x020]  padding
[0x020..0x03C]  nvfw_hs_bl_desc    (start_tag, code_off/size)
[0x03C..0x040]  padding
[0x040..0x240]  BL CODE SECTION    (512 bytes — THIS is what goes in WPR)
```

Currently `fw.fecs_bl` = full 576-byte file (loaded raw via `read("gr/fecs_bl.bin")`).
The WPR image includes the 64-byte header, shifting all offsets.

Additionally, `bl_imem_off` is hardcoded to 0, but FECS BL expects IMEM address
0x7E00 (start_tag=0x7E << 8) and GPCCS BL expects 0x3400 (start_tag=0x34 << 8).

## Required Changes

### 1. Parse BL File Headers (firmware.rs)

The `HsBlDesc` struct and parser already exist for `acr/bl.bin`. Reuse the same
pattern for `gr/fecs_bl.bin` and `gr/gpccs_bl.bin`:

```rust
pub struct GrBlFirmware {
    pub code: Vec<u8>,       // data section only (512 bytes)
    pub start_tag: u32,      // from nvfw_hs_bl_desc (0x7E for FECS, 0x34 for GPCCS)
    pub bl_code_size: u32,   // from nvfw_hs_bl_desc.code_size (256)
    pub bl_data_size: u32,   // data_size from nvfw_hs_bl_desc
}
```

Parse in `AcrFirmwareSet::load()`:
```rust
fn parse_gr_bl(raw: &[u8]) -> DriverResult<GrBlFirmware> {
    let bin_hdr = NvFwBinHeader::parse(raw)?;  // reuse existing parser
    let bl_desc = HsBlDesc::parse(&raw[bin_hdr.header_offset as usize..])?;
    let data_off = bin_hdr.data_offset as usize;
    let data_size = bin_hdr.data_size as usize;
    Ok(GrBlFirmware {
        code: raw[data_off..data_off + data_size].to_vec(),
        start_tag: bl_desc.bl_start_tag,
        bl_code_size: bl_desc.bl_code_size,
        bl_data_size: bl_desc.bl_data_size,
    })
}
```

### 2. Fix build_wpr (wpr.rs)

Replace raw BL bytes with parsed code sections:

```rust
// BEFORE (WRONG):
let fecs_img = [fw.fecs_bl.as_slice(), fw.fecs_inst.as_slice(), fw.fecs_data.as_slice()].concat();

// AFTER (CORRECT):
let fecs_img = [fw.fecs_bl.code.as_slice(), fw.fecs_inst.as_slice(), fw.fecs_data.as_slice()].concat();
```

Fix `write_lsb` parameters:

```rust
// bl_size: use parsed code section size, NOT full file length
// bl_imem_off: start_tag << 8, NOT 0
write_lsb(
    &mut buf,
    fecs_lsb_off,
    fecs_img_off,
    fecs_bld_off,
    &fw.fecs_sig,
    fw.fecs_bl.code.len(),      // was: fw.fecs_bl.len() [576 → 512]
    fw.fecs_inst.len(),
    fw.fecs_data.len(),
    falcon_id::FECS,
    fw.fecs_bl.start_tag,       // NEW parameter for bl_imem_off
);
```

Fix `write_lsb` internals:

```rust
// bl_imem_off — CRITICAL: use start_tag << 8
buf[t + 16..t + 20].copy_from_slice(&((start_tag << 8) as u32).to_le_bytes());

// bl_data_size — should be 84 (sizeof flcn_bl_dmem_desc_v2), not 256
buf[t + 24..t + 28].copy_from_slice(&84u32.to_le_bytes());
```

Fix BLD DMA addresses:

```rust
let fecs_data_dma = wpr_vram_base + fecs_img_off as u64
    + fw.fecs_bl.code.len() as u64    // was: fw.fecs_bl.len()
    + fw.fecs_inst.len() as u64;
```

Fix WPR header bin_version:

```rust
// Read version from sig file at offset 0x50
let fecs_version = u32::from_le_bytes([fw.fecs_sig[0x50], fw.fecs_sig[0x51],
                                        fw.fecs_sig[0x52], fw.fecs_sig[0x53]]);
w32(&mut buf, 16, fecs_version);  // was: 0
```

Remove depmap writes (lines 254-257 in write_lsb) — those offsets are inside
`lsf_signature_v1.depmap[]`, not firmware metadata fields.

### 3. Firmware File Reference

Verified from `/lib/firmware/nvidia/gv100/`:

| File | Size | data_off | data_size | start_tag | bl_imem_off |
|------|------|----------|-----------|-----------|-------------|
| gr/fecs_bl.bin | 576 | 64 | 512 | 0x7E | 0x7E00 |
| gr/gpccs_bl.bin | 576 | 64 | 512 | 0x34 | 0x3400 |
| acr/bl.bin | 1280 | 512 | 768 | 0xFD | 0xFD00 |
| gr/fecs_inst.bin | 25632 | — | — | — | — |
| gr/fecs_data.bin | 4788 | — | — | — | — |
| gr/gpccs_inst.bin | 12643 | — | — | — | — |
| gr/gpccs_data.bin | 2128 | — | — | — | — |
| gr/fecs_sig.bin | 192 | — | — | — | version=2 |
| gr/gpccs_sig.bin | 192 | — | — | — | version=2 |

## Validation

After applying fixes, run ACR boot test on Titan (either card) in post-nouveau
state (swap to nouveau first, let it init, swap back to vfio). The WPR COPY
status should transition from 1 to 0xFF (complete), and FECS/GPCCS should
show activity in their falcon registers.

## Full Analysis

See `hotSpring/experiments/087_WPR_FORMAT_ANALYSIS.md` for detailed byte-level
comparison, firmware parsing results, and all 7 bug descriptions.
