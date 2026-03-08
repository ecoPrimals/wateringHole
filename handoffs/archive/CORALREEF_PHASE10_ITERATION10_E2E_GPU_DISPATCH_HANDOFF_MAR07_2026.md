# coralReef — Phase 10 Iteration 10: E2E GPU Dispatch Verified on AMD

**Date**: March 7, 2026
**From**: coralReef
**To**: hotSpring, groundSpring, neuralSpring, wetSpring, airSpring, barraCuda, toadStool

---

## Summary

coralReef Phase 10 — Iteration 10 achieves the first successful end-to-end
sovereign GPU dispatch: WGSL source code compiled by `coral-reef`, dispatched
by `coral-driver` via PM4 command submission, executed on the AMD RX 6950 XT
(RDNA2/GFX1030), and verified by host readback. The shader `out[0] = 42u`
writes 42 to a GPU buffer and the host reads it back correctly. Three critical
bugs were fixed in the compiler and driver to reach this milestone.

## Metrics

| Metric | Iteration 9 | Iteration 10 | Delta |
|--------|-------------|--------------|-------|
| Total tests | 974 | 990 | **+16** |
| Passing | 952 | 953 | **+1** |
| Ignored | 22 | 37 | **+15** (hw tests require device) |
| Corpus passing SM70 | 14 | 14 | — |
| Clippy warnings | 0 | 0 | — |
| AMD E2E dispatch | ❌ FenceTimeout | **✅ Verified** | **Milestone** |

## E2E Pipeline Verified

```
WGSL source (@compute @workgroup_size(64) fn main(...) { out[0] = 42u; })
       │
       ▼
coral-reef compiler (naga → SSA IR → optimize → legalize → RA → RDNA2 encode)
       │
       ▼
coral-driver PM4 dispatch (GEM alloc → VA map → PM4 SET_SH_REG → DISPATCH_DIRECT)
       │
       ▼
RX 6950 XT GPU execution (wave32, FLAT_STORE_DWORD, 64-bit VA)
       │
       ▼
Host readback via mmap → 0x0000002A (42) ✅
```

Every layer is pure Rust. Zero FFI, zero `*-sys`, zero `extern "C"`.

## Critical Bugs Fixed

### 1. Wave Size: CS_W32_EN in DISPATCH_INITIATOR

**Symptom**: VGPRs v4+ contained 0 — stores executed but wrote wrong data.

**Root cause**: `DISPATCH_INITIATOR` in PM4 did not set bit 15 (`CS_W32_EN`),
causing the GPU to run in wave64 mode. With `vgpr_encoded=0`, wave64 allocates
only 4 VGPRs `((0+1)*4)` instead of the 8 expected for wave32 `((0+1)*8)`.
Any VGPR index >= 4 mapped to unmapped register space and read as zero.

**Fix**: Set `CS_W32_EN` (bit 15) in the `DISPATCH_INITIATOR` word in `pm4.rs`.

**Files**: `crates/coral-driver/src/amd/pm4.rs`

### 2. Literal Constant Emission: SrcEncoding

**Symptom**: Compiled shader's `FLAT_STORE_DWORD` was consumed as the "literal"
DWORD of the preceding `V_MOV_B32`, destroying the instruction stream.

**Root cause**: `src_to_encoding` returned `SRC0=255` (literal indicator) for
`SrcRef::Imm32` values but never appended the actual literal DWORD to the
instruction output. The next instruction was silently consumed as the literal.

**Fix**: Introduced `SrcEncoding` struct bundling `src0: u16` and
`literal: Option<u32>`. Full RDNA2 inline constant map: 128=0, 129–192=1..64,
193–208=-1..-16. All callers updated to call `extend_with_literal()`. VOP3
ops reject literals with `CompileError`.

**Files**: `crates/coral-reef/src/codegen/ops/mod.rs`, `memory.rs`, `system.rs`,
`convert.rs`, `alu_int.rs`, `alu_float.rs`

### 3. 64-bit Address Construction

**Symptom**: Shader accessed address `0x0000002A_81000000` (va_lo correct,
va_hi = 42 instead of 0) — GPU page fault, then FenceTimeout.

**Root cause**: `emit_store`, `emit_load`, `emit_load_f64`, and `emit_atomic`
in `func_mem.rs` passed `addr[0].into()` (only the low 32 bits of the 64-bit
address) to `OpSt`/`OpLd`/`OpAtom`. The high 32 bits (`addr[1]`) became dead
code and were eliminated by DCE. The FLAT instruction's `v[addr:addr+1]` pair
then used whatever was in the next VGPR (the constant 42) as `addr_hi`.

**Fix**: Changed all four functions to pass `addr.clone().into()` — the full
2-component `SSARef` — preserving both address components through DCE and
register allocation.

**Files**: `crates/coral-reef/src/codegen/naga_translate/func_mem.rs`

## Additional Fixes

### unwrap_or(0) Audit

Replaced all silent `unwrap_or(0)` fallbacks in the ops encoder with proper
`CompileError` returns:

- **Register indices** (`dst_to_vgpr_index`, `src_to_vgpr_index`, `src_to_encoding`):
  overflow returns `CompileError::InvalidInput`
- **Branch offsets** (`OpBra::encode`): `i16` overflow returns `CompileError`
- **FLAT memory offsets** (`OpLd`, `OpSt`, `OpAtom`): helper `checked_flat_offset`
  returns `CompileError` on `i16` overflow

### PM4 User Data Wiring

Buffer GPU virtual addresses are now passed to shaders via `COMPUTE_USER_DATA`
registers (SGPRs 0+). The PM4 builder collects buffer VAs from `ShaderInfo`
and emits `SET_SH_REG` packets targeting `COMPUTE_USER_DATA_0` (offset 0x2E40).
`cbuf_to_user_sgpr_encoding` maps constant buffer references to the correct
SGPR indices.

## Impact on Other Primals

### barraCuda
The E2E pipeline is now proven for AMD. `ComputeDispatch::CoralReef` can route
through `coral-gpu` for AMD targets with confidence that compiled shaders
execute correctly. NVIDIA E2E remains to be validated.

### groundSpring
The `addr[0].into()` bug affected all 64-bit memory operations — loads, stores,
and atomics. Any WGSL shader accessing storage buffers through the `coral-reef`
compiler was silently corrupted. This is now fixed.

### hotSpring / neuralSpring / airSpring
Cross-spring WGSL shaders that compile for RDNA2 can now be dispatched on
AMD hardware. The inline constant fix ensures values 0–64 encode correctly
as immediates; larger constants emit proper literal DWORDs.

## Hardware Tests

Five AMD hardware tests pass on RX 6950 XT:

| Test | Description | Status |
|------|-------------|--------|
| `storage_write_shader_compiles_for_rdna2` | Compilation check | ✅ |
| `nop_shader_dispatches_and_syncs` | Basic PM4 pipeline | ✅ |
| `handcrafted_store_42_shader` | Hand-assembled SGPR user data | ✅ |
| `hardcoded_va_store_42_shader` | Multi-store regression | ✅ |
| `dispatch_writes_42_and_readback_verifies` | **Full E2E** | ✅ |

## Checks

All pass:

```
cargo check --workspace          # OK
cargo test --workspace           # 990 tests (953 passing, 37 ignored)
cargo clippy -- -D warnings      # 0 warnings
cargo fmt --check                # OK
cargo doc --workspace --no-deps  # 0 warnings
```

---

*The sovereign pipeline is proven. WGSL source compiles to native RDNA2 binary,
dispatches on real hardware, executes correctly, and reads back verified results.
Every layer is pure Rust — from the shader compiler to the DRM ioctl to the
PM4 command buffer to the GPU fence. No vendor SDK, no FFI, no C.*
