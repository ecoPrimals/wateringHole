# coralReef — Phase 10 Iteration 15 Handoff

**Date**: March 8, 2026
**From**: coralReef
**To**: barraCuda, toadStool, groundSpring, all springs

---

## What Changed

### AMD MappedRegion Safe Slices
- `crates/coral-driver/src/amd/gem.rs`: `ptr::copy_nonoverlapping` replaced with
  `copy_from_slice` / `to_vec()` via `as_slice()` / `as_mut_slice()` on `MappedRegion`
- Mirrors the NV `NvMappedRegion` RAII pattern from iteration 14
- Both AMD and NV drivers now have zero raw pointer ops at buffer write/read call sites

### Typed DRM Wrappers
- `crates/coral-driver/src/drm.rs`: `gem_close()` and `drm_version()` typed wrappers
- Eliminates `unsafe` from 3 call sites:
  - `GemBuffer::close` (AMD)
  - `NvDevice::free` (NVIDIA)
  - `DrmDevice::driver_name` (common)
- Core `drm_ioctl_typed` remains `unsafe` for low-level vendor-specific ioctls

### Inline Variable Pre-allocation Fix
- `crates/coral-reef/src/codegen/naga_translate/func_ops.rs`: `pre_allocate_local_vars()`
  now called during `inline_call` for callee functions
- Previously, inlined function bodies had no pre-allocated `var_storage` slots for their
  local variables, causing "index out of bounds" panics
- This fix unblocks shaders that use function calls within switch cases or complex control flow

### abs_f64 Inlined
- `crates/coral-reef/tests/fixtures/wgsl/bcs_bisection_f64.wgsl`: `abs_f64` function
  inlined directly (was previously a preamble dependency from hotSpring ShaderTemplate)
- BCS shader now compiles past parsing (blocked on Pred→GPR coercion, not preamble)

### TODO/XXX Cleanup
- Bare `TODO:` comments documented with descriptions
- `XXX:` markers converted to proper comments
- Doc-comment `TODO` → `Note` for performance optimization documentation

---

## Test Results

| Metric | Value |
|--------|-------|
| Total tests | 991 |
| Passing | 960 |
| Ignored | 31 |
| Failed | 0 |
| Clippy warnings | 0 |

No regressions from iteration 14.

---

## Current Blockers (for springs to know)

| Blocker | Shaders Affected | Priority |
|---------|-----------------|----------|
| Pred→GPR encoder coercion | bcs_bisection, batched_hfb | P2 |
| RA SSA tracking | su3_gauge_force | P2 |
| Scheduler loop-carried phi | wilson_plaquette, sigmoid | P2 |
| Math::Acos (trig inverse) | local_elementwise | P2 |
| Complex64 preamble | dielectric_mermin | P2 |

---

## What Springs Should Know

### barraCuda
- AMD + NV driver write/read paths are now fully safe Rust (RAII slices)
- `gem_close()` wrapper available — no more raw ioctl calls needed for buffer cleanup
- `Fp64Strategy` wired since iteration 13; df64 preamble auto-prepended

### toadStool
- `shader.compile.*` IPC contract unchanged
- Inline function variable pre-allocation fix may allow more complex shaders to compile
  that previously hit slot overflow during inlining

### groundSpring / all springs
- If your shaders use function calls inside switch cases, they should now compile
  where they previously panicked with "index out of bounds" in var_storage
- `abs_f64` no longer needs external preamble injection for BCS-type shaders

---

## Unsafe Surface Summary (Iteration 15)

| Location | Blocks | Pattern |
|----------|--------|---------|
| `drm.rs` | 2 | `drm_ioctl_typed` + `drm_ioctl_named` (core syscall wrapper) |
| `amd/gem.rs` | 1 | RAII `MappedRegion` (mmap/munmap), safe slice access |
| `amd/ioctl.rs` | 3 | `amd_ioctl` / `amd_ioctl_read` safe wrappers + `clock_monotonic_ns` |
| `nv/ioctl.rs` | 1 | RAII `NvMappedRegion` (mmap/munmap), safe slice access |
| `nak-ir-proc` | 2 | Proc-macro `from_raw_parts` (justified, layout-checked) |

All unsafe is in coral-driver (kernel ABI boundary) and nak-ir-proc (proc-macro).
6/8 crates enforce `#[deny(unsafe_code)]` at compile time.

---

*991 tests, 960 passing, 0 warnings. AMD E2E verified. Driver unsafe fully consolidated
into RAII MappedRegion pattern. Typed DRM wrappers eliminate call-site unsafe.
The compiler evolves — pure Rust, sovereign compute.*
