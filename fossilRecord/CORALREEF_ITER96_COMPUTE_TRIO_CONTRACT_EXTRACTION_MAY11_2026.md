# coralReef Iter 96 — Compute Trio Wire Contract + Extraction Boundary

**Date**: May 11, 2026
**Primal**: coralReef v0.1.0
**Tests**: 4,754 passing (0 failures, 181 ignored HW-gated)

## Wire Contract Alignment (Compute Trio Gate 1)

coralReef's `shader.compile.*` IPC surface now matches the Compute Trio
specification. All field renames use `#[serde(rename)]` — Rust field names
are unchanged, only the JSON wire format changed.

### `shader.compile.wgsl` response (before → after)

| Rust field       | Old wire name      | New wire name     | Notes                        |
|------------------|--------------------|-------------------|------------------------------|
| `binary`         | `binary`           | `binary_b64`      | base64-encoded via Bytes     |
| `arch`           | `arch`             | `target`          | architecture compiled for    |
| `info`           | `info`             | `shader_info`     | dispatch metadata block      |
| `gpr_count`      | `gpr_count`        | `gprs`            |                              |
| `shared_mem_bytes`| `shared_mem_bytes` | `shared_memory`   |                              |
| `barrier_count`  | `barrier_count`    | `barriers`        |                              |
| `workgroup_size` | `workgroup_size`   | `workgroup`       |                              |
| `wave_size`      | (new)              | `wave_size`       | 32 NVIDIA, 32/64 AMD         |
| `local_memory`   | (new)              | `local_memory`    | per-thread scratch bytes     |
| `compile_time_ms`| (new)              | `compile_time_ms` | wall-clock compilation time  |

### `shader.compile.capabilities` (Gate 1)

| Rust field       | Old wire name      | New wire name | Notes                     |
|------------------|--------------------|---------------|---------------------------|
| `supported_archs`| `supported_archs`  | `targets`     | Gate 1 contract field     |

### Upstream changes (coral-reef compiler library)

- `CompilationInfo` gained `local_mem_bytes: u32` field
- Populated from `ShaderInfo::shared_local_mem_size` in NVIDIA and AMD backends
- PTX emit path defaults to 0 (PTX driver manages local memory)

## Extraction Boundary — What Moves to toadStool

coralReef's hardware-domain crates are cleanly decoupled from the compiler
domain. Neither `coralreef-core` nor `coral-gpu` imports from `coral-ember`
or `coral-glowplug`. The extraction is a copy+adapt operation on toadStool's
side, followed by vestigial removal from coralReef.

### Moves to toadStool (WHERE domain)

| Crate/module           | LOC     | Tests | Role                                    |
|------------------------|---------|-------|-----------------------------------------|
| `coral-ember`          | ~11,200 | 216   | VFIO fd holder, device lifecycle, swap journal |
| `coral-glowplug`       | ~20,800 | 484   | Fleet orchestration, personality detection, sovereign boot |
| `coral-driver` hardware| ~60k+   | —     | BAR0/MMIO, VFIO channels, DRM ioctls, UVM compute, GSP, Falcon/SEC2 |

**coral-driver hardware modules** (all `#[cfg(target_os = "linux")]`):
- `src/mmio.rs`, `src/mmio_region.rs` — MMIO primitives
- `src/drm.rs` — generic DRM ioctl + mmap
- `src/amd/` (except `shader_binary.rs`) — amdgpu GEM, ioctl, PM4
- `src/nv/bar0.rs` — BAR0 register access
- `src/nv/ioctl/` — nouveau DRM ioctls
- `src/nv/pushbuf.rs` — hardware method stream
- `src/nv/probe.rs` — BAR0 GR init, sysfs identity
- `src/nv/nvidia_drm.rs` — proprietary DRM EXEC
- `src/nv/uvm/` — RM-style alloc/structs/constants
- `src/nv/uvm_compute/` — GPFIFO, channel setup, open paths
- `src/nv/vfio_compute/` (92 files) — ACR boot, Falcon/SEC2, Kepler, submission
- `src/nv/kepler_falcon.rs` — Kepler Falcon
- `src/nv/coral_kmod.rs` — kernel module interface
- `src/vfio/` (109 files) — VFIO device/channel/DMA/PCI discovery
- `src/gsp/` — GSP firmware, GR init, BAR0 applicator
- `src/intel/` — i915/xe skeleton
- `src/cuda/mod.rs` — cudarc device path
- `src/linux_paths.rs` — sysfs/procfs roots
- `src/bin/coral_probe.rs` — GPU diagnostic CLI

### Stays in coralReef (HOW domain)

| Crate/module           | Role                                    |
|------------------------|-----------------------------------------|
| `coralreef-core`       | IPC dispatch, service layer, UniBin CLI |
| `coral-reef`           | Compiler library: naga IR → PTX/SASS/AMD |
| `coral-gpu`            | GPU context wrapper (uses coral-reef)   |
| `coral-driver` QMD     | `src/nv/qmd/` — dispatch descriptor construction |
| `coral-driver` cubin   | `src/cuda/cubin.rs` — ELF packaging     |
| `coral-driver` generation | `src/nv/generation.rs` — SM/profile → capabilities |
| `coral-driver` AMD ELF | `src/amd/shader_binary.rs` — AMDGPU ELF metadata |
| `coral-driver` shared  | `src/lib.rs` (`ComputeDevice` trait, `ShaderInfo`), `src/error.rs`, `src/hardware.rs` |

### Shared Boundary

`coral-driver::ShaderInfo` is consumed by both domains:
- coralReef populates it from compilation metadata
- toadStool needs it for QMD/PM4 dispatch descriptor construction

Options:
1. **Thin shared types crate** — extract `ShaderInfo` + `HardwareCapabilities` into a `compute-trio-types` crate
2. **Full duplication** — toadStool defines its own `ShaderInfo` matching the wire contract
3. **Wire-only** — toadStool deserializes `shader_info` from JSON directly (no shared Rust type)

Recommendation: option 3 (wire-only) matches the primal isolation principle.

### Interface Contract

toadStool's `compute.dispatch.submit` consumes coralReef's `shader.compile.wgsl`
response via JSON-RPC IPC:

```
coralReef → { "binary_b64": "...", "shader_info": { "gprs": 32, ... } }
         → toadStool.compute.dispatch.submit
```

No crate-level dependency. Wire contract is the only interface.

## Files Changed (Iter 96)

- `crates/coral-reef/src/backend.rs` — `CompilationInfo` + `local_mem_bytes`
- `crates/coral-reef/src/codegen/nv/ptx_emit/mod.rs` — populate `local_mem_bytes`
- `crates/coralreef-core/src/service/types.rs` — serde renames + new fields
- `crates/coralreef-core/src/service/compile.rs` — timing, wave_size, local_memory
- `crates/coralreef-core/src/service/tests.rs` — contract shape assertions
- `crates/coralreef-core/src/ipc/tests_unix.rs` — `targets` wire field
- `crates/coralreef-core/src/ipc/tests_unix_dispatch.rs` — `targets` wire field
