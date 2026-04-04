# Unified Artifact Evolution — ecoBin Alignment for Validation Artifacts

**Status**: Evolution Record v1.1
**Date**: April 3, 2026 (updated: Universal Substrate Deployment layer)
**Spring**: hotSpring (first adopter)
**Standard**: EXTERNAL_VALIDATION_ARTIFACT_STANDARD.md
**License**: AGPL-3.0-or-later

---

## Context

The hotSpring guideStone artifact was the first full ColdSpore deployment in
ecoPrimals. Through iterative deployment (USB, Docker, VM), several friction
points emerged that violated ecoBin principles. This document records the
evolution from a multi-entry-point, capability-first layout to a unified
ecoBin-aligned artifact.

---

## Evolution: 5 Entry Points to 1

### Before (v0.7.0, March 2026)

```
validation/
├── run                     # validate (shell script, 189 lines)
├── benchmark               # hardware profiling (shell, 215 lines)
├── chuna-engine            # QCD data engine with subcommands (shell, 177 lines)
├── deploy-nucleus          # NUCLEUS deployment (shell, 321 lines)
├── run-overnight           # extended validation (shell, 224 lines)
├── run-matrix              # matrix orchestration (shell, 62 lines)
└── bin/
    ├── static/<name>-x86_64   # musl binaries
    └── gpu/<name>-x86_64      # glibc binaries
```

Problems:
- 5+ entry points violates UniBin "one binary, subcommands" pattern
- GPU detection logic duplicated across run, benchmark, chuna-engine
- Integrity check duplicated across run, chuna-engine, deploy-nucleus
- Architecture detection duplicated everywhere
- Capability-first layout (`bin/static/`, `bin/gpu/`) doesn't match
  plasmidBin/benchScale `BinaryResolver` convention (`<arch>/<name>`)
- x86_64 only; no aarch64 cross-compile

### After (v0.7.1, April 2026)

```
validation/
├── hotspring               # SINGLE ENTRY POINT (genomeBin-style wrapper)
├── _lib.sh                 # shared functions (sourced, not executed)
├── run                     # backward compat → ./hotspring validate
├── benchmark               # backward compat → ./hotspring benchmark
├── chuna-engine            # backward compat → ./hotspring <cmd>
├── deploy-nucleus          # backward compat → ./hotspring deploy
└── bin/
    ├── x86_64/
    │   ├── static/<name>   # musl binaries (CPU-only)
    │   └── gpu/<name>      # glibc binaries (GPU-capable)
    ├── aarch64/
    │   └── static/<name>   # musl binaries (CPU-only, cross-compiled)
    ├── static/<name>-x86_64   # legacy symlinks → ../x86_64/static/<name>
    ├── gpu/<name>-x86_64      # legacy symlinks → ../x86_64/gpu/<name>
    └── <name>-x86_64          # flat symlinks → x86_64/static/<name>
```

---

## Key Decisions

### 1. Shell wrapper, not Rust mega-binary

The `./hotspring` entry point is a shell script that dispatches to per-binary
Rust executables. We did not merge 19 Rust binaries into one because:

- Binary size: each GPU binary is ~8MB; a merged binary would be 50+ MB
- Build time: separate binaries compile in parallel; one would be serial
- Feature isolation: GPU dependencies (wgpu) don't pollute CPU-only builds
- Incremental rebuilds: changing one binary doesn't invalidate others

The shell wrapper achieves the same UX as a single binary (one name,
subcommands) without the binary-level cost.

### 2. Arch-first, not capability-first

Old: `bin/static/validate-x86_64` (capability → arch)
New: `bin/x86_64/static/validate` (arch → capability)

Rationale:
- benchScale's `BinaryResolver` resolves `<base>/<arch>/<name>`
- plasmidBin stores `primals/<arch>/<name>`
- The arch is selected first (by `uname -m`), then capability (by GPU probe)
- This matches the physical decision tree: "what machine am I on?" then
  "what can this machine do?"

### 3. Shared library, not duplication

The `_lib.sh` file provides four functions sourced by `./hotspring`:

- `integrity_check()` — SHA-256 verification
- `detect_arch()` — architecture normalization
- `detect_gpu()` — glibc + Vulkan probing
- `resolve_binary(name)` — arch-first path resolution with legacy fallback

These were previously duplicated across 5+ scripts. The shared library
eliminates ~150 lines of duplicated logic.

### 4. aarch64 via cross-compile, not qemu build

The build script uses `cargo build --target aarch64-unknown-linux-musl` for
static ARM binaries. GPU binaries are NOT cross-compiled (Vulkan dlopen
requires host-arch GPU drivers). This means:

- aarch64 gets static/CPU-only binaries (universal, works on any ARM Linux)
- GPU validation on aarch64 requires native compilation on ARM hardware
- benchScale can test aarch64 via qemu-user Docker containers

---

## benchScale Integration

`validate-hotspring-multi.sh` now supports:

| Substrate | Layout | GPU | Status |
|-----------|--------|-----|--------|
| CPU-only Ubuntu | arch-first or legacy | HOTSPRING_NO_GPU=1 | Required |
| NVIDIA GPU | arch-first or legacy | auto-detect | Required |
| AMD GPU | arch-first or legacy | auto-detect | Required |
| Alpine musl | arch-first or legacy | HOTSPRING_NO_GPU=1 | Required |
| aarch64 qemu-user | arch-first | CPU-only | Optional (--with-aarch64) |

The script auto-detects the `./hotspring` entry point. If not found, it
falls back to `./run` for legacy artifacts.

---

## agentReagents Integration

A new template `templates/springs/gate-hotspring-validation.yaml` provides
VM-level validation:

- Ubuntu 24.04 cloud image
- Vulkan ICD + mesa drivers pre-installed
- Copies artifact, runs `./hotspring validate` and `./hotspring benchmark`
- Verification checks: results JSON exists, all checks passed
- Optional PCI passthrough for GPU-specific VM validation

This complements benchScale's container-level testing with full VM isolation.

---

## Backward Compatibility

All old entry points continue to work:

```sh
./run                     # → ./hotspring validate
./benchmark               # → ./hotspring benchmark
./chuna-engine generate   # → ./hotspring generate
./deploy-nucleus          # → ./hotspring deploy
./run-overnight           # → ./hotspring overnight
./run-matrix              # → ./hotspring matrix
```

The legacy bin layout (`bin/static/<name>-<arch>`, `bin/gpu/<name>-<arch>`,
`bin/<name>-<arch>`) is preserved as symlinks pointing into the arch-first
tree. benchScale scripts that check for `bin/validate-x86_64` still find it.

---

## What Other Springs Should Adopt

1. **Single entry point**: one script/binary named after the spring, subcommands
2. **`_lib.sh` pattern**: source shared detection functions, don't duplicate
3. **Arch-first layout**: `bin/<arch>/{static,gpu}/<name>`
4. **GPU detection via probe**: check glibc linker + Vulkan at runtime
5. **Backward-compat forwarders**: thin scripts that `exec` the unified entry
6. **benchScale multi-substrate test**: validate across Docker substrates
7. **agentReagents VM template**: validate in full VM isolation

---

## Files Changed

| File | Change |
|------|--------|
| `validation/hotspring` | NEW — unified entry point |
| `validation/_lib.sh` | NEW — shared functions |
| `validation/run` | Rewritten as thin forwarder |
| `validation/benchmark` | Rewritten as thin forwarder |
| `validation/chuna-engine` | Rewritten as thin forwarder |
| `validation/deploy-nucleus` | Rewritten as thin forwarder |
| `validation/run-overnight` | Rewritten as thin forwarder |
| `validation/run-matrix` | Rewritten as thin forwarder |
| `scripts/build-guidestone.sh` | Rewritten for arch-first layout + aarch64 cross |
| `benchScale/scripts/validate-hotspring-multi.sh` | Updated for new layout + aarch64 |
| `agentReagents/templates/springs/gate-hotspring-validation.yaml` | NEW — VM template |
| `wateringHole/EXTERNAL_VALIDATION_ARTIFACT_STANDARD.md` | Updated layout + checklist |
| `wateringHole/UNIFIED_ARTIFACT_EVOLUTION.md` | This document |

---

## Universal Substrate Deployment Layer (v1.1, April 2026)

The v0.7.1 unified entry point was Linux-only. The v1.1 evolution adds a
universal substrate layer: any OS, any filesystem, any architecture.

### New Components

```
validation/
├── hotspring               # Updated: detect_os() → container dispatch for non-Linux
├── hotspring.bat            # NEW — Windows launcher (WSL2 → Docker fallback)
├── _lib.sh                 # Updated: detect_os(), container_*, tmpdir fallback
├── container/
│   └── hotspring-guidestone.tar  # NEW — OCI container image (Docker/Podman)
└── bin/
    └── aarch64/
        └── static/         # NOW VALIDATED — qemu-user cross-arch confirmed
```

### Key Additions

| Feature | Implementation | Pattern |
|---------|---------------|---------|
| OS detection | `detect_os()` in `_lib.sh` | Linux / Darwin / windows-shell |
| Container dispatch | `container_exec()` in `_lib.sh` | Docker or Podman, GPU flags |
| OCI image | `Dockerfile` + `build-container.sh` | Ubuntu 22.04 + Vulkan |
| Windows launcher | `hotspring.bat` | WSL2 first, Docker fallback |
| macOS auto-dispatch | `./hotspring` non-Linux path | Container delegation |
| exFAT tmpdir | `resolve_binary()` in `_lib.sh` | Copy to $TMPDIR, chmod +x |
| USB preparation | `scripts/prepare-usb.sh` | ext4 or exFAT dual-mode |
| aarch64 cross-validation | benchScale + qemu-user binfmt | 40/40 bit-identical |

### Cross-Architecture Validation Results

5-substrate benchScale validation (`validate-hotspring-multi.sh --with-aarch64`):

| Substrate | Arch | GPU | Checks | Status |
|-----------|------|-----|--------|--------|
| CPU-only Ubuntu | x86_64 | None | 59/59 | ✅ PASS |
| NVIDIA GPU | x86_64 | RTX 3090 | 59/59 | ✅ PASS |
| AMD GPU | x86_64 | RX 6950 XT | 59/59 | ✅ PASS |
| Alpine musl | x86_64 | None | 59/59 | ✅ PASS |
| aarch64 qemu-user | aarch64 | None | 59/59 | ✅ PASS |

Cross-substrate observable comparison: **40/40 PASS** (bit-identical physics
across all substrates and architectures).

### Deployment Matrix

| Platform | Runtime | Entry Point | GPU |
|----------|---------|-------------|-----|
| Linux x86_64 | Native | `./hotspring` | Auto-detect |
| Linux aarch64 | Native | `./hotspring` | CPU-only (static) |
| Linux (any) | Docker/Podman | `./hotspring container run` | GPU passthrough |
| Windows | WSL2 | `hotspring.bat` | Host GPU via WSL2 |
| Windows | Docker Desktop | `hotspring.bat` | GPU passthrough |
| macOS | Docker/Podman | `sh ./hotspring` | CPU-only |

### Filesystem Compatibility

| Filesystem | Permissions | Strategy |
|------------|-------------|----------|
| ext4 | Native | Direct execution |
| exFAT | No execute bit | tmpdir fallback (transparent) |
| NTFS (WSL2) | Emulated | WSL2 handles permissions |
| NFS noexec | Blocked | tmpdir fallback |

---

## Future Evolution

- **Rust dispatcher**: replace shell `./hotspring` with a Rust binary that
  uses clap subcommands and calls library functions directly. This is the
  true ecoBin (one binary, no shell wrapper). Blocked on merging the Rust
  binary table in Cargo.toml without bloating binary size.

- **genomeBin manifest**: `liveSpore.json` should embed or generate a
  `genomeBin/manifest.toml`-compatible section for ecosystem consumption.

- **primalSpring composition**: the artifact should be producible via
  primalSpring graph execution, not shell scripts.

- **Cross-arch GPU**: when ARM GPU hardware (Jetson, Apple Silicon via Asahi)
  is available in the gate matrix, add `bin/aarch64/gpu/` binaries.

- **Container graph awareness**: `biomeOS/graphs/hotspring_deploy.toml`
  should model the container dispatch path alongside native execution.
