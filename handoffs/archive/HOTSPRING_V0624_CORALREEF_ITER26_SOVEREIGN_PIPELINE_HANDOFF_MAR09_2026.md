# hotSpring v0.6.24 — coralReef Iter 26 Sovereign Pipeline Handoff

**Date**: March 9, 2026
**From**: hotSpring (v0.6.24, 769 lib tests, 101+ binaries)
**To**: barraCuda team, toadStool team, coralReef team
**Synced**: barraCuda v0.3.3, toadStool S138, coralReef Phase 10 Iter 26

---

## Executive Summary

hotSpring has completed end-to-end integration of the sovereign pipeline:
WGSL → coralReef → native SASS/GFX → coral-driver → GPU. The compilation
stage works for 44/46 standalone physics shaders. The `GpuBackend` trait
implementation is complete (`Send+Sync` resolved in Iter 26). DRM dispatch
needs deeper kernel integration for NVIDIA (nouveau EINVAL on GV100,
nvidia-drm pending UVM). AMD amdgpu path is E2E ready.

This handoff documents: (1) local evolutions in barraCuda that should be
absorbed upstream, (2) lessons learned for the sovereign pipeline, and
(3) remaining gaps for the primal teams.

---

## Local barraCuda Evolutions for Upstream Absorption

### 1. Discovery Manifest Phase 10 Compatibility

**Files**: `crates/barracuda/src/device/coral_compiler/discovery.rs`

coralReef Phase 10 changed the manifest format:
- `"capabilities"` → `"provides"` array
- `transports.jsonrpc` string → object `{"tcp": "...", "path": "..."}`

**Fix**: `read_capability_transport()` checks both `"provides"` and
`"capabilities"`. `read_jsonrpc_from_value()` handles string or object
(extracting `"tcp"` field).

**Status**: Ready for absorption. Backward-compatible with pre-Phase 10.

### 2. CoralReefDevice — Full GpuBackend Implementation

**Files**: `crates/barracuda/src/device/coral_reef_device.rs`

Evolved from scaffold to full `GpuBackend` implementation:

```rust
pub struct CoralReefDevice {
    name: String,
    ctx: Mutex<coral_gpu::GpuContext>,
    has_device: bool,
}
```

**Constructors**:
- `new(target)` — compile-only (no hardware device needed)
- `with_auto_device()` — auto-detect DRM render node
- `from_descriptor(vendor, arch, driver)` — toadStool discovery integration

**GpuBackend trait**: `alloc_buffer`, `alloc_buffer_init`, `alloc_uniform`,
`upload`, `download`, `dispatch_compute` — all implemented with `Mutex<GpuContext>`.
Compile-only mode returns clear "no hardware device" errors for dispatch.

Standalone `compile_wgsl(wgsl, target)` also available for compilation-only
workflows (validates shaders without dispatch).

**Status**: Ready for absorption. `Send+Sync` resolved upstream in Iter 26.

### 3. coral-gpu Re-export

**Files**: `crates/barracuda/src/device/mod.rs`

Added `#[cfg(feature = "sovereign-dispatch")] pub use coral_gpu;` to make
`GpuTarget`, `NvArch`, `AmdArch`, `CompiledKernel` etc. accessible to
downstream crates without direct coral-gpu dependency.

### 4. sovereign-dispatch Feature Gate

**Files**: `crates/barracuda/Cargo.toml`

```toml
[dependencies]
coral-gpu = { version = "0.1", optional = true }

[features]
sovereign-dispatch = ["gpu", "dep:coral-gpu"]
```

Path patches in `.cargo/config.toml` point to local coralReef checkout for
development. Upstream should wire to registry or git dependency.

---

## Compilation Coverage (validate_sovereign_compile)

**Binary**: `hotSpring/barracuda/src/bin/validate_sovereign_compile.rs`

Compiles 46 standalone hotSpring WGSL shaders to native SM70/SM86 SASS via
coral-gpu in-process. Results (Iter 26):

| Result | Count | Details |
|--------|-------|---------|
| OK | 44 | Native binary produced, GPR/instr counts extracted |
| PANIC | 1 | `deformed_potentials_f64` — SSARef truncation in `emit_f64_min_max` |
| FAIL | 1 | `complex_f64` — utility include, not standalone entry point |

**Total native output**: ~213 KB per target architecture.

**Largest shaders** (most complex physics):
- `su3_link_update_f64`: 26,400B, 62 GPR, 1,642 instructions
- `su3_gauge_force_f64`: 20,512B, 54 GPR, 1,274 instructions
- `dirac_staggered_f64`: 18,800B, 46 GPR, 1,167 instructions
- `yukawa_force_celllist_v2_f64`: 14,496B, 78 GPR, 898 instructions

---

## Lessons Learned

### 1. f64 in Sovereign Compilers Is Hard

The f64 lowering pipeline is the most fragile part of the sovereign path.
Every math function needs explicit 2-component handling for f64 register
pairs. The Iter 26 fix for `Min/Max/Abs/Clamp` resolved the majority of
panics, but `deformed_potentials_f64` reveals that some f64 values still
flow through paths that produce 1-component SSARefs.

**Recommendation**: Audit all `func_math.rs` branches for f64 handling.
Any function that reads `a[0]` without checking component count is a
potential truncation point.

### 2. Mutex<GpuContext> Works for Thread-Safe Dispatch

The `Mutex<GpuContext>` pattern for implementing `GpuBackend: Send + Sync`
is clean and correct. Performance cost is minimal — lock contention only
matters for concurrent dispatch, which is already serialized at the GPU
level.

### 3. DRM Dispatch Is Vendor-Dependent

- **amdgpu**: Works E2E. PM4 command streams, GEM buffers, CS submit, fence.
- **nouveau**: Compute subchannel binding (Iter 26) is necessary but not
  sufficient for GV100. The kernel's NVIF object model requires deeper
  setup for compute engine instantiation. Mesa NVK's approach (NVIF objects
  for channel setup) should be studied.
- **nvidia-drm**: UVM integration is the blocker. Without it, buffer
  allocation is not possible. This is a kernel/driver interface issue.

### 4. Path Patches Enable Write-Absorb-Lean

The `.cargo/config.toml` patch pattern works well for local development:

```toml
[patch.crates-io]
coral-gpu = { path = "../coralReef/crates/coral-gpu" }
coral-reef = { path = "../coralReef/crates/coral-reef" }
coral-driver = { path = "../coralReef/crates/coral-driver" }
```

Springs evolve locally with path patches, upstream absorbs, then springs
lean back to released versions.

---

## Remaining Gaps

### For coralReef Team

1. **`deformed_potentials_f64` panic** — `func_math_helpers.rs:143`, SSARef
   index out of bounds (len 1, index 1). An f64 value flows through a math
   function that hasn't been updated with the Iter 26 2-component handling.
2. **nouveau DRM dispatch** — `create_channel` with compute subchannel still
   returns EINVAL on GV100. Needs NVIF compute object setup (study Mesa NVK).
3. **nvidia-drm UVM** — buffer allocation requires UVM integration.

### For barraCuda Team

1. **Absorb discovery.rs fix** — Phase 10 manifest compatibility
2. **Absorb CoralReefDevice** — full `GpuBackend` implementation
3. **Absorb sovereign-dispatch feature** — coral-gpu optional dep + re-export
4. **Consider dispatch routing** — when DRM dispatch matures, add a strategy
   that routes to `CoralReefDevice` instead of `WgpuDevice` based on
   `Fp64Strategy::Sovereign`

### For toadStool Team

1. **coralReef discovery integration** — toadStool should discover coralReef
   daemon via XDG manifest and expose `shader.compile` capability
2. **`from_descriptor` routing** — toadStool's GPU discovery can pass
   vendor/arch/driver to `CoralReefDevice::from_descriptor()` for sovereign
   path selection
3. **Precision routing** — `PrecisionRoutingAdvice` should consider sovereign
   path when coralReef is available

---

## hotSpring Test Results

| Metric | Value |
|--------|-------|
| lib tests | 769 (0 failed, 6 ignored) |
| binaries | 101+ |
| WGSL shaders | 84 |
| clippy warnings | 0 (lib + all bins) |
| unsafe blocks | 0 |
| Chuna overnight | 44/44 |
| sovereign compile | 44/46 |
| coralReef sync | Phase 10, Iter 26 |
| toadStool sync | S138 |
| barraCuda sync | v0.3.3 |

---

*hotSpring v0.6.24 — sovereign pipeline integration complete. Compilation
stage operational (44/46 shaders). GpuBackend implemented. DRM dispatch
awaiting coral-driver maturation. The compilation gap is one shader
(deformed_potentials_f64). The dispatch gap is kernel-side NVIF for
NVIDIA. AMD is E2E ready.*
