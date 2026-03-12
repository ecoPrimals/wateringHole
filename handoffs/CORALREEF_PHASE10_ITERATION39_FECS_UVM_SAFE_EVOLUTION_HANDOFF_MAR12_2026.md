# coralReef — Phase 10 Iteration 39 Handoff

**Date**: March 12, 2026
**Phase**: 10 — Iteration 39 (FECS GR Context + UVM Alignment + Safe Evolution)
**Tests**: 1667 passing (+10), 64 ignored

---

## Summary

Iteration 39 closes the critical GPU dispatch gaps identified by hotSpring's
investigation, evolves unsafe code to safe Rust patterns, and aligns the UVM
dispatch model with the nouveau path for compiler consistency.

---

## Changes

### 1. FECS GR Context Init (Gap 3 — Critical Blocker)

The single biggest blocker for NVIDIA GPU execution was CTXNOTVALID — the
PBDMA tried to load the channel's GR context and found it invalid.

**What was done:**

- **`firmware_parser.rs`**: `sw_ctx.bin` content is now stored as raw bytes
  in `GrFirmwareBlobs.ctx_data` (previously parsed for size, content dropped).
  `sw_nonctx.bin` content also retained. Added `ctx_size()`, `nonctx_size()`,
  `has_ctx_template()` accessor methods.

- **`pushbuf.rs`**: New `PushBuf::gr_context_init()` builds a push buffer
  from FECS method entries — binds the compute class on subchannel 0, then
  submits each method entry as a class method write.

- **`nv/mod.rs`**: `NvDevice::open_from_drm()` now calls `try_gr_context_init()`
  after channel creation. This loads `sw_method_init.bin` entries for the GPU's
  chip, builds the FECS init pushbuf, and submits it via the channel (new UAPI
  or legacy). Non-fatal — logs and continues if firmware is absent.

- **New helper**: `sm_to_chip()` maps SM architecture to chip codename for
  firmware lookup (SM70→gv100, SM75→tu102, SM86→ga102, etc.).

### 2. UVM CBUF Descriptor Alignment (Gap 2)

The UVM dispatch path bound user buffers directly to individual CBUF slots
(CBUF 0 = buffer 0, CBUF 1 = buffer 1). However, the compiler generates
`c[0][binding * 8]` for buffer address lookups — an indirection model where
CBUF 0 contains a descriptor table. This mismatch meant compiled shaders
wouldn't work on the UVM path.

**Fix**: UVM dispatch now builds the same descriptor-table-in-CBUF-0 model
as the nouveau path:
- Allocates a descriptor buffer with `[addr_lo, addr_hi, size]` entries
- Binds it as the sole CBUF 0 in the QMD
- Uses `build_qmd_for_sm()` instead of manual version selection

### 3. hotSpring Dispatch Fixes Absorbed

Verified commit `a691023` (QMD field layout, CBUF descriptors, syncobj sync,
dispatch diagnostics) is on `main`. Added `NvUvmComputeDevice` re-export
from `nv::mod.rs` (was missing — caused `E0433` in `coral-gpu`).

### 4. Unsafe Evolution

| Before | After |
|--------|-------|
| 4 ioctl wrappers without `// SAFETY:` | All annotated (syncobj_create/destroy/wait, exec_submit_with_signal) |
| `unsafe impl Send/Sync` without docs | `// SAFETY:` comment explaining FD and mmap safety |
| `ptr::copy_nonoverlapping` in UVM upload/readback | Safe `slice::from_raw_parts_mut` + `copy_from_slice` |

Every `unsafe` block in production code now has a `// SAFETY:` comment.
41 unsafe blocks total in coral-driver (all at FFI/mmap boundary); 0 in
other crates (`#[deny(unsafe_code)]`).

### 5. Hardcoding Evolution

- AMD `gpu_va` calculation extracted to named constants:
  `AMD_USER_VA_BASE = 0x0000_8000_0000`, `AMD_VA_STRIDE = 0x0100_0000`
- Zero cross-primal references in production code (verified by grep)
- Zero hardcoded port numbers outside test code
- Firmware path `/lib/firmware/nvidia/` retained (kernel convention, not deployment assumption)

### 6. Test Coverage (+10 tests)

| Test | Module | What it validates |
|------|--------|-------------------|
| `legacy_parse_retains_ctx_data` | firmware_parser | sw_ctx.bin content stored, not just size |
| `missing_ctx_produces_empty` | firmware_parser | Missing files produce empty Vec, not error |
| `gr_context_init_structure` | pushbuf | FECS init pushbuf has correct SET_OBJECT + method entries |
| `gr_context_init_empty_methods` | pushbuf | Empty method list produces SET_OBJECT-only pushbuf |
| `sm_to_chip_mapping` | nv/mod | SM→chip codename mapping (50→gm200, 70→gv100, etc.) |
| `compute_class_selection` | nv/mod | SM→compute class (70→Volta, 75→Turing, 86→Ampere) |
| `gpfifo_entry_encoding` | uvm_compute | GPFIFO entry VA/length field encoding roundtrip |
| `gpfifo_entry_zero_length` | uvm_compute | Zero-length entry preserves VA, zeroes length field |
| `gpu_gen_sm_roundtrip` | uvm_compute | GpuGen enum SM version identity |

---

## Quality Gates

| Check | Status |
|-------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --workspace --all-targets -- -D warnings` | PASS (0 warnings) |
| `cargo doc --workspace --no-deps` | PASS |
| `cargo test --workspace` | PASS (1667 passing, 0 failed, 64 ignored) |
| Files over 1000 LOC | 0 |

## Files Modified

| File | Change |
|------|--------|
| `crates/coral-driver/src/gsp/firmware_parser.rs` | Store ctx_data/nonctx_data content, add accessors, add 2 tests |
| `crates/coral-driver/src/gsp/mod.rs` | Export BundleEntry, MethodEntry |
| `crates/coral-driver/src/nv/mod.rs` | FECS init integration, sm_to_chip, NvUvmComputeDevice re-export, 2 tests |
| `crates/coral-driver/src/nv/pushbuf.rs` | gr_context_init() builder, 2 tests |
| `crates/coral-driver/src/nv/uvm_compute.rs` | Descriptor CBUF model, safe copy, SAFETY docs, 3 tests |
| `crates/coral-driver/src/nv/ioctl/new_uapi.rs` | 4 SAFETY comments added |
| `crates/coral-driver/src/amd/gem.rs` | VA base/stride named constants |
| `crates/coral-driver/tests/hw_nv_nouveau.rs` | dead_code expect annotation |

## Remaining for GPU Execution

The FECS GR context init is now submitted, but the critical question is whether
the kernel's nouveau driver has already initialized the FECS falcon. If FECS
isn't running (no PMU firmware for desktop Volta), the method submission will
fail silently. This needs on-site hardware validation:

1. **Titan V (GV100)**: Test if FECS method submission resolves CTXNOTVALID
2. **RTX 3090**: Test UVM dispatch with aligned CBUF descriptor model
3. If FECS submission insufficient: toadStool BAR0 pre-init path needed

---

*coralReef is a sovereign Rust GPU compiler — zero FFI, zero libc, zero vendor lock-in*
