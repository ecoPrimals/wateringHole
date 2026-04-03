# liveSpore Deployment Review — hotSpring guideStone ColdSpore

**Status**: Field Report v1.0
**Date**: April 3, 2026
**Spring**: hotSpring (Lattice QCD / Condensed Matter Physics)
**Artifact**: hotSpring-guideStone-v0.7.0
**Medium**: USB flash drive (ext4), 15 GB
**Reviewer**: Automated via ecoPrimals development pipeline

---

## Context

This is the first full ColdSpore deployment artifact produced in the ecoPrimals
ecosystem. The goal was to create a USB drive that validates lattice QCD physics
(Papers 43-45: gradient flow, BGK dielectric, kinetic-fluid coupling) on any
Linux machine — plug in, run, get verified results.

The artifact went through several iterations over 48 hours, each revealing gaps
in the deployment pipeline that required fixes. This document captures what
worked, what broke, and what the ecosystem should evolve.

---

## What Worked

### 1. Static musl binaries (CPU baseline)

The `x86_64-unknown-linux-musl` target with `+crt-static` and
`link-self-contained=yes` produced binaries with zero dynamic dependencies.
These ran on the first attempt on the target machine. No glibc version
mismatch, no missing .so files, no LD_LIBRARY_PATH. The External Validation
Artifact Standard's core promise held: **one binary, any x86_64 Linux**.

Verified: 59/59 CPU checks pass on the static binary from USB.

### 2. CHECKSUMS integrity pipeline

The SHA-256 integrity check (`sha256sum -c CHECKSUMS`) caught every binary
update correctly. When we modified `validate_chuna_overnight.rs` to add GPU
streaming HMC and rebuilt, the checksums failed until we regenerated. The
self-verifying property is genuine.

### 3. Cross-GPU determinism

Running the GPU binary on all three substrates (NVIDIA RTX 3090, AMD RX 6950 XT,
llvmpipe software rasterizer) produced cross-GPU plaquette agreement at ~10^-11
relative precision. The wgpu abstraction + barracuda's f64 shader pipeline
delivers substrate-independent physics.

### 4. ext4 filesystem choice

After the FAT32 failure (see below), switching to ext4 solved all permission
issues permanently. Binaries execute directly from the drive. Results write
back to the drive. The USB is both the deployment medium and the results store.

### 5. Self-knowledge (liveSpore.json)

The auto-updating manifest tracks every system the USB visits: hostname, date,
GPU/CPU mode, checks passed, duration. When you hand the drive to someone and
they hand it back, you can see exactly what happened on their hardware.

---

## What Broke and How We Fixed It

### 1. FAT32 permission failure (critical)

**Problem**: The USB was initially formatted as FAT32 (VFAT) for cross-platform
compatibility. Linux mounted it with `fmask=0022` and `showexec`, which means:

- No file has execute permission unless it ends in .exe, .com, or .bat
- `chmod +x` is silently ignored (writes to inode succeed but have no effect)
- Even `sh ./setup.sh` worked, but `./bin/validate-x86_64` returned EPERM

**Fix**: Reformatted to ext4. This is Linux-only, but the target audience
(physics HPC users) is 100% Linux. FAT32 was a false optimization.

**Lesson for ecosystem**: The EXTERNAL_VALIDATION_ARTIFACT_STANDARD should
document that ext4 is the required USB filesystem for Linux-target deployments.
FAT32 is only appropriate when macOS/Windows compatibility is required, and
in that case, the `setup.sh` copy-to-local pattern is mandatory.

**Gap**: biomeOS `create_livespore.sh` creates a bootable Alpine+EFI layout
with GPT partitions — it doesn't have this problem because it controls the
filesystem. But for data-only ColdSpore artifacts (validation, not a boot OS),
the filesystem choice needs to be documented as a decision point.

### 2. Static musl cannot dlopen Vulkan (critical)

**Problem**: The static-pie musl binary cannot call `dlopen("libvulkan.so.1")`
because musl's static builds do not include a dynamic linker. wgpu uses dlopen
to load Vulkan at runtime. Result: `GpuF64::enumerate_adapters()` returns 0
adapters from the static binary, even on a machine with working Vulkan.

The validation suite completed 59/59 CPU-only checks but silently skipped all
GPU validation — no error, no warning, just "No f64-capable GPU found."

**Fix**: Ship dual binaries:

```
bin/static/  — musl, CPU-only, works on any Linux
bin/gpu/     — glibc, GPU-capable (only needs libc/libm/libgcc_s)
```

The `run` script auto-detects glibc + Vulkan availability and selects the
appropriate binary. With the GPU binary: 71/71 checks (CPU + 3 GPUs).

**Lesson for ecosystem**: The External Validation Artifact Standard currently
specifies "Static musl ELF" only. This is insufficient for GPU workloads.
The standard should define a **dual binary layout** for artifacts that include
GPU validation, with auto-detection as the default dispatch strategy.

**Gap**: No primal currently handles this detection. toadStool discovers GPU
hardware at runtime but assumes the calling binary can already use GPUs. The
detection of "can this binary even dlopen Vulkan?" is in a shell script (`run`)
rather than in a primal. Eventually this should live in toadStool's substrate
detection: "calling binary is static-pie, Vulkan dlopen will fail, suggest
GPU binary alternative."

### 3. Overnight validation used CPU HMC (performance)

**Problem**: `validate_chuna_overnight.rs` was calling CPU-only `hmc_trajectory`
for all HMC calculations, including the 16^4 x 500 sweep that takes ~6 hours.
The GPU streaming pipeline (`gpu_hmc_trajectory_streaming`) was fully
implemented and used by `chuna_generate`, but the validation binary didn't
use it.

**Fix**: Replaced `hmc_trajectory` with `gpu_hmc_trajectory_streaming` in
the convergence sweep, production beta scan, and dynamical fermion sections.
Expected 16^4 speedup: 6 hours -> 15-30 minutes.

**Lesson**: When adding new GPU pipelines, update ALL consumer binaries.
The "works in chuna_generate but not validate_chuna_overnight" gap persisted
undetected because overnight runs are long and infrequent.

### 4. Symmetric-only lattice geometry (physics)

**Problem**: All validation lattices were N^4 (e.g., [8,8,8,8], [16,16,16,16]).
For finite-temperature QCD — which is the target physics (freeze-out, HVP,
crossover) — the temporal extent must differ from spatial: Ns^3 x Nt.

**Fix**: Added asymmetric lattice points:

```
[8, 8, 8, 16]   — T ~ 125 MeV (near QCD crossover)
[16, 16, 16, 32] — T ~ 62 MeV (low temperature, large volume)
```

**Gap**: The lattice dimension parsing (`parse_dims_from_args`, `--ns`/`--nt`)
was already implemented in `chuna_generate` but not wired into the validation
binary. This is the same "production uses it, validation doesn't" pattern.

### 5. No GPU benchmarking capability

**Problem**: The artifact could validate physics but not profile hardware. When
you hand a USB to a collaborator with unknown hardware, the first question is
"what can this machine do?" — not "are the physics right?"

**Fix**: Added `./benchmark` entry point that runs `bench_gpu_fp64`,
`bench_gpu_hmc`, `bench_precision_tiers` and writes structured results to
`results/benchmarks/<hostname>_<date>/`. Results persist on the USB.

**Gap**: The benchmarks are individual binaries with their own output formats.
There is no unified benchmark schema that toadStool or biomeOS can consume
for capacity planning. This should evolve in the toadStool hardware
characterization pipeline.

---

## Friction Points (Not Yet Resolved)

### 1. No toadStool socket on ColdSpore

The GPU binary tries to report measurements to toadStool at
`/run/user/1000/biomeos/toadstool-default.sock`. On a ColdSpore USB plugged
into a machine without biomeOS installed, this socket does not exist. The
binary logs "report failed: No such file or directory" for every GPU
measurement.

This is not an error — the binary gracefully falls back — but it is noise
in the output. The binary should detect ColdSpore mode (via
`BIOMEOS_DEPLOYMENT_MODE=cold`) and skip toadStool reporting unless a socket
is explicitly provided.

### 2. ~~No cross-architecture support~~ — RESOLVED (April 3, 2026)

**Resolved.** aarch64 static musl binaries now cross-compile and ship in the
artifact under `bin/aarch64/static/`. Validated on benchScale via qemu-user
Docker emulation: 40/40 cross-substrate observable comparisons are
bit-identical between x86_64 and aarch64. An agentReagents VM template
(`gate-hotspring-aarch64.yaml`) is also available for full ARM64 VM
validation.

### 3. No ILDG config output from USB

The USB validates physics but does not generate production configurations in
ILDG/LIME format. `chuna_generate` (in `bin/gpu/`) can do this, and the
`chuna-engine` wrapper exposes it, but there is no guided workflow for a
physicist who just wants to generate a 16^3 x 32 ensemble.

The `deploy-nucleus` script includes a reference ensemble step but uses
hardcoded parameters. A "guided generation" mode (`./hotspring generate
--ns=16 --nt=32 --beta=6.0 --configs=100`) would make the USB a complete
physics tool, not just a validator.

### 4. genomeBin manifest not generated

The wateringHole `genomeBin/manifest.toml` defines a standard format for
binary distribution including versions, architectures, capabilities, and
checksums. The hotSpring artifact does not generate a genomeBin-compatible
manifest — it uses its own `liveSpore.json` format.

These should converge. The liveSpore manifest should include or embed a
genomeBin-compatible section so that biomeOS and primalSpring can consume it
through their existing manifest parsing.

### 5. No primalSpring composition validation

primalSpring's `prepare_spore_payload.sh` assembles multi-primal spore
payloads with tower configs, deployment graphs, and beacon genetics. The
hotSpring USB includes biomeOS tower.toml and a validation graph, but these
are hand-written, not generated by primalSpring's composition pipeline.

When primalSpring evolves its composition validation, the hotSpring artifact
should be producible via `primalSpring` graph execution — not by shell
scripts.

---

## Post-Deployment Evolution (April 3, 2026)

The initial ColdSpore deployment (v1.0 of this review) identified 5 gaps
and 5 friction points. The Universal Substrate Deployment work resolved
several of these and introduced new capabilities.

### Resolved Gaps

**Cross-architecture (Gap #2)**: aarch64 static musl binaries now ship in
`bin/aarch64/static/`. benchScale validates them via qemu-user Docker
emulation (`docker run --platform linux/arm64`). The 5-substrate validation
suite (CPU-only Ubuntu, NVIDIA GPU, AMD GPU, Alpine musl, aarch64 qemu-user)
confirms bit-identical physics across architectures: 40/40 observable
comparisons PASS.

**exFAT filesystem support (evolution of Gap #1 — FAT32)**: The original
FAT32 failure is now addressed by a tmpdir fallback in `_lib.sh`. When
`chmod +x` fails on non-executable filesystems (exFAT, NTFS, NFS noexec),
the binary is automatically copied to `$TMPDIR` and made executable there.
This makes the artifact deployable on USB drives formatted as exFAT
(universal readability across Windows/macOS/Linux) without requiring ext4.

### New Capabilities

**OCI container image**: `container/hotspring-guidestone.tar` is a
Docker/Podman image (Ubuntu 22.04 base + libvulkan1 + mesa-vulkan-drivers)
containing the full artifact. Enables deployment on any OS with a container
runtime. Built by `scripts/build-container.sh`, loaded via
`docker load < container/hotspring-guidestone.tar`.

**Cross-OS launchers**: `hotspring.bat` launches on Windows via WSL2 or
Docker Desktop. On macOS, `./hotspring` auto-detects the non-Linux OS and
dispatches to the container runtime (Docker or Podman). Platform-specific
setup instructions are printed if no container runtime is found.

**OS detection (`detect_os()`)**: `_lib.sh` now identifies Linux, Darwin,
and Windows-shell (MINGW/MSYS/CYGWIN) environments. Non-Linux hosts are
redirected to container execution or given setup instructions.

**Container dispatch helpers**: `container_available()`, `container_cmd()`,
`container_ensure_loaded()`, `container_exec()` in `_lib.sh` provide a
complete pattern for transparent container delegation. GPU passthrough flags
are automatically added when running on Linux.

**`prepare-usb.sh` dual-mode**: Supports both ext4 (Linux-native, preserves
permissions) and exFAT (universal, requires tmpdir fallback) USB preparation.
Writes `liveSpore.json` manifest with dual-architecture metadata, cross-platform
deployment strategies, and validated substrate list.

### Updated Deployment Matrix

| Platform | Method | GPU | Status |
|----------|--------|-----|--------|
| Linux x86_64 (ext4 USB) | Direct `./hotspring` | Auto-detect | ✅ Validated |
| Linux x86_64 (exFAT USB) | tmpdir fallback | Auto-detect | ✅ Validated |
| Linux aarch64 | Direct `./hotspring` (static) | CPU-only | ✅ Validated (qemu-user) |
| Linux (any, Docker) | `docker load + run` | GPU passthrough | ✅ Validated |
| Windows (WSL2) | `hotspring.bat` → WSL2 | Host GPU via WSL2 | ✅ Launcher tested |
| Windows (Docker Desktop) | `hotspring.bat` → Docker | GPU passthrough | ✅ Launcher tested |
| macOS (Docker/Podman) | `./hotspring` auto-dispatch | CPU-only | ✅ Launcher tested |
| Alpine musl | Direct `./hotspring` (static) | CPU-only | ✅ Validated |

### Remaining Evolution Targets

1. **toadStool socket on ColdSpore** — still unresolved (friction #1)
2. **ILDG guided generation** — still unresolved (friction #3)
3. **genomeBin manifest convergence** — still unresolved (friction #4)
4. **primalSpring composition pipeline** — still unresolved (friction #5)
5. **Container graph awareness** — `biomeOS/graphs/hotspring_deploy.toml`
   does not yet model the container dispatch path
6. **ARM GPU binaries** — aarch64/gpu/ not yet possible (Vulkan cross-compile
   requires native ARM GPU hardware)

---

## Performance Comparison

| Metric | CPU-only (musl) | GPU (glibc) |
|--------|----------------|-------------|
| Checks passed | 59/59 | 71/71 |
| GPUs discovered | 0 | 3 |
| Wall time | 602.9s | 89.8s |
| Cross-GPU parity | N/A | ~10^-11 |
| Speedup | 1x | 6.7x |

The 6.7x speedup comes from two sources:
1. GPU gradient flow parity checks (12 additional checks at ~4s total)
2. CPU-side code path is slightly different in the glibc build (compiler opts)

The overnight validation with GPU streaming HMC (16^4 x 500 sweeps) is
expected to show 10-20x speedup over the CPU path, pending benchmark.

---

## Recommendations for Ecosystem Evolution

### For EXTERNAL_VALIDATION_ARTIFACT_STANDARD

1. Document the dual binary layout (static/ + gpu/) as a sanctioned pattern
2. Specify ext4 as the default USB filesystem for Linux deployments
3. Add auto-detection logic requirements for GPU/CPU dispatch
4. Define a benchmark entry point as a recommended (not required) feature

### For biomeOS

1. The ColdSpore detection in `deployment_mode.rs` should handle the case
   where `.biomeos-spore` is present but no biomeOS primals are running
2. Socket fallback: when `BIOMEOS_DEPLOYMENT_MODE=cold`, primals should not
   attempt IPC to sockets that cannot exist
3. The `create_livespore.sh` script should offer a "data ColdSpore" mode
   (ext4, no Alpine, no bootloader) alongside the current "boot LiveSpore"

### For toadStool

1. Add substrate detection for static-pie binaries ("can this binary dlopen?")
2. Expose a benchmark schema that ColdSpore artifacts can write and toadStool
   can later consume for capacity planning
3. The hardware calibration (`PrecisionBrain`) should be serializable to a
   portable JSON format that travels with the USB

### For primalSpring

1. Add a hotSpring composition test: produce a ColdSpore artifact via graph
   execution and validate it runs correctly
2. The `prepare_spore_payload.sh` pattern should be generalized beyond
   primalSpring's own primals to include spring-specific payloads (hotSpring
   validation binaries, wetSpring data artifacts, etc.)
3. Cross-spring ColdSpore: a single USB with validation artifacts from
   multiple springs, selected at runtime via `spore.sh <spring>`

### For barracuda

1. When `GpuF64::enumerate_adapters()` returns empty in a glibc build with
   Vulkan available, log a diagnostic (driver issue vs missing ICD vs other)
2. The GPU streaming pipeline types should be exported at the crate root
   for easier consumption by validation binaries
3. Consider a `--benchmark` flag on `validate_chuna` that includes GPU
   throughput metrics alongside physics validation

---

## File Manifest

Files created or modified during this deployment cycle:

| File | Action | Purpose |
|------|--------|---------|
| `barracuda/src/bin/validate_chuna_overnight.rs` | Modified | GPU streaming HMC, asymmetric lattices |
| `scripts/build-guidestone.sh` | Modified | Dual binary build (static + GPU) |
| `validation/run` | Modified | Auto GPU/CPU detection and dispatch |
| `validation/benchmark` | Created | Hardware benchmarking entry point |
| USB `.biomeos-spore` | Created | ColdSpore marker for biomeOS detection |
| USB `biomeOS/tower.toml` | Created | Tower config for ColdSpore |
| USB `biomeOS/graphs/hotspring_validation.toml` | Created | Validation flow graph |
| USB `biomeOS/.family.seed` | Created | Genetics lineage for this spore |
| USB `spore.sh` | Created | biomeOS ColdSpore entry point |
| USB `liveSpore.json` | Modified | v2.0: dual binary, self-knowledge, ColdSpore |
| USB `README.txt` | Modified | ColdSpore deployment documentation |

---

## Summary

The first ecoPrimals ColdSpore deployment works. A USB drive can be plugged
into a Linux machine, auto-detect GPU capability, validate lattice QCD physics
across multiple GPU vendors, benchmark the hardware, and carry the results with
it. The dual binary strategy (static musl for universal CPU + dynamic glibc for
GPU) solves the fundamental tension between portability and GPU access.

The gaps are real: no toadStool integration on ColdSpore, no genomeBin manifest
convergence, no primalSpring composition pipeline, no cross-architecture builds,
no guided generation workflow. These are evolution targets, not blockers. The
artifact validates physics. The infrastructure validates the deployment model.
The rest is optimization.
