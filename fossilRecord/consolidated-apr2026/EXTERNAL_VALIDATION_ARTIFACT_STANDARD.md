# External Validation Artifact Standard

**Status**: Ecosystem Standard v1.1
**Adopted**: March 31, 2026 (updated April 3, 2026: container deployment, cross-OS, cross-arch)
**Authority**: WateringHole Consensus
**Compliance**: Required for all springs, recommended for primals
**License**: AGPL-3.0-or-later

---

## One Artifact. Anywhere.

A collaborator receives a single directory. They copy it to a USB stick, scp
it to an HPC login node, carry it to CERN on a thumb drive, hand it to a
colleague at LANL who puts it on a cluster. Every person runs the same thing.
It works. The math validates. No setup, no dependencies, no conversations
about what they need to install first.

If the artifact requires ANY discussion about the target environment, it has
failed.

---

## The Artifact

### Unified Layout (v2 — arch-first)

```
validation/
├── hotspring               # Single entry point. Subcommands. (genomeBin-style)
├── _lib.sh                 # Shared functions (integrity, arch, GPU probe)
├── run                     # Backward compat → ./hotspring validate
├── benchmark               # Backward compat → ./hotspring benchmark
├── README                  # Plain text, 80 columns, no markdown renderer needed
├── bin/
│   ├── x86_64/
│   │   ├── static/         # Static musl ELFs — CPU-only, works everywhere
│   │   │   ├── validate
│   │   │   └── ...
│   │   └── gpu/            # Glibc ELFs — GPU-capable via Vulkan dlopen
│   │       ├── validate
│   │       └── ...
│   └── aarch64/
│       └── static/         # Static musl ELFs — CPU-only (no GPU cross-compile)
│           ├── validate
│           └── ...
├── shaders/                # WGSL source (human-auditable, the actual math)
│   └── *.wgsl
├── expected/               # Reference results from known-good hardware
│   └── *.json
├── results/                # Created at runtime — output goes here
├── CHECKSUMS               # SHA-256 of everything in bin/ and expected/
└── LICENSE                 # AGPL-3.0-or-later
```

Total size: under 100 MB with dual-binary, under 50 MB static-only.

The `./hotspring` entry point detects architecture via `uname -m`, probes for
glibc + Vulkan to decide GPU vs static binary, and dispatches. The user runs
`./hotspring validate` and the right binary is selected automatically.

### Legacy Layout (v1 — still supported)

```
validation/
├── run                     # Entry point. One command.
├── bin/
│   ├── validate-x86_64     # Static musl ELF, x86_64
│   └── validate-aarch64    # Static musl ELF, aarch64
└── ...
```

The v1 layout with flat `bin/<name>-<arch>` is still generated as backward-
compatible symlinks. Existing scripts and benchScale consumers work unchanged.

---

## `hotspring` (unified entry point)

```bash
./hotspring validate          # physics validation suite
./hotspring benchmark         # hardware profiling
./hotspring generate          # ILDG config generation
./hotspring deploy            # NUCLEUS deployment
./hotspring help              # all commands
```

The entry point sources `_lib.sh` which provides:

- `integrity_check()` — SHA-256 via sha256sum or shasum
- `detect_arch()` — `uname -m` → `ARCH_TAG` (x86_64 or aarch64)
- `detect_gpu()` — probes glibc linker + Vulkan loader → `GPU_MODE`
- `resolve_binary(name)` — finds `bin/<arch>/gpu/<name>` or `bin/<arch>/static/<name>`

Override environment: `HOTSPRING_NO_GPU=1` forces CPU-only,
`HOTSPRING_FORCE_GPU=1` forces GPU binary selection.

Backward compatibility: `./run` → `./hotspring validate`, `./benchmark` →
`./hotspring benchmark`, etc. These are thin 2-line forwarding scripts.

That's it. `./hotspring validate` on a laptop. `./hotspring validate` on ICER.
`./hotspring validate` at CERN. Same command. Same output. The binary detects
what's available and uses it.

---

## The Binary

Static musl-linked ELF. Zero dynamic library dependencies. PIE enabled.
Runs on any Linux from CentOS 7 (2014) to whatever ships in 2030.

### Runtime Detection (inside the binary, not the script)

The binary probes the substrate at startup:

1. **Vulkan available + GPU with SHADER_F64?** → GPU + CPU dual-path validation.
   Run the math on GPU, run it on CPU interpreter, compare. Report both.
2. **Vulkan available but no f64?** → GPU (f32/DF64) + CPU (f64 reference).
   Still dual-path. CPU is the precision oracle.
3. **No Vulkan, no GPU?** → CPU-only. NagaExecutor interprets the WGSL shaders
   natively. Same math, same tolerances, same PASS/FAIL. Slower, equally correct.
4. **coralReef binary alongside?** → Also run Cranelift JIT path. Triple
   validation: interpreter, JIT, GPU (if present). Report all paths.

The user never chooses. The binary tells them what it found and what it did.

### Output

Terminal (immediate feedback):
```
substrate: x86_64 linux (login03.icer.msu.edu)
gpu:       none detected — running CPU validation
engine:    NagaExecutor (naga IR tree-walk interpreter)

[PASS] gradient_flow_w7_8x8x8x8    order=2.08  (>1.5)       12.4s
[PASS] gradient_flow_w7_convergence  ε=0.02→0.001 monotonic   8.1s
[PASS] dielectric_debye_screening    err=1.2e-12 (<1e-6)      0.3s
[PASS] dielectric_fsum_rule          converging to -πωₚ²/2    0.8s
[PASS] bgk_mass_conservation         Δm=0.0 (exact)           0.1s
[PASS] bgk_momentum_conservation     Δp=2.1e-15 (<1e-12)      0.1s
[PASS] euler_sod_shock               front resolved            0.4s
[PASS] coupled_interface_density     err=0.12 (<0.15)          1.2s
...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
41/41 passed    cpu-only    total: 1m 47s

results written to: results/validation_2026-04-01T0800.json
compare against your own data: diff your_results.json results/validation_2026-04-01T0800.json
```

JSON (machine-readable, in `results/`):
```json
{
  "version": "1.0",
  "timestamp": "2026-04-01T08:00:00Z",
  "substrate": {
    "arch": "x86_64",
    "os": "linux",
    "hostname": "login03.icer.msu.edu",
    "kernel": "5.14.0-362.el9.x86_64"
  },
  "engine": {
    "primary": "naga-executor",
    "gpu": null,
    "jit": null
  },
  "checks": [
    {
      "name": "gradient_flow_w7_8x8x8x8",
      "domain": "lattice_qcd",
      "paper": "Bazavov & Chuna, arXiv:2101.05320",
      "passed": true,
      "measured": 2.08,
      "threshold": 1.5,
      "comparison": "greater_than",
      "unit": "convergence_order",
      "tolerance_justification": "finite-size suppressed from nominal 3; >1.5 confirms correct order",
      "duration_ms": 12400
    }
  ],
  "summary": { "total": 41, "passed": 41, "failed": 0 }
}
```

Every check traces to a paper. Every tolerance has a physics justification.
The JSON is the peer review artifact — not the binary, not the code, the
**output**.

---

## What Makes It One Artifact

| Property | How |
|----------|-----|
| **One directory** | Copy the whole thing. Don't pick files. |
| **Two architectures, one layout** | x86_64 and aarch64 in `bin/<arch>/`. Entry point picks the right one. |
| **Dual binary** | Static musl (CPU, universal) + dynamic glibc (GPU via Vulkan). Auto-detected. |
| **No network** | Everything needed is in the directory. No downloads, no package managers. |
| **No sudo** | Runs in user space. Writes only to its own `results/` directory. |
| **No GPU required** | CPU-only is the default when no GPU is detected. Same math. |
| **No Rust required** | Pre-built static binary. No `cargo`, no toolchain, no compiler. |
| **No configuration** | `./run`. That's the interface. |
| **Self-verifying** | Checksums validated before execution. Tampered files are caught. |
| **Self-documenting** | README is plain text. Output explains what engine was used and why. |
| **Portable across time** | Static musl binary runs on kernels from 2014 onward. No glibc version issues. |

---

## Transfer

The artifact doesn't care how it gets there:

```bash
# USB stick
cp -r validation/ /media/usb/

# SCP to HPC
scp -r validation/ user@login.hpc.edu:~/

# Shared filesystem
cp -r validation/ /scratch/user/

# GitHub release
tar czf validation.tar.gz validation/
# attach to release

# Email (if small enough)
zip -r validation.zip validation/
```

On the other end:
```bash
cd validation/
./run
```

---

## Per-Spring / Per-Primal Requirements

Every spring that makes scientific claims must produce this artifact.

1. **Static musl binaries** for x86_64 and aarch64. Both in `bin/`.
2. **CPU-only mode works.** If the binary can't execute its full validation
   suite without a GPU, it is not compliant.
3. **Every numeric check has**: a name, a paper reference (if applicable),
   a measured value, a threshold or tolerance, a comparison type, a physics
   justification for the tolerance, and a duration.
4. **Reference results** in `expected/` from a known-good run. Provenance
   documented (hardware, date, binary version, engine used).
5. **CHECKSUMS** for integrity. SHA-256. No GPG, no external keys — just
   hashes that a reviewer can verify with standard tools.
6. **README** in plain text. Not markdown, not HTML, not PDF. A terminal
   user reads it with `cat` or `less`. 80 columns.
7. **AGPL-3.0-or-later LICENSE** included. The reviewer can fork, modify,
   redistribute. No ambiguity.

### For barraCuda specifically

barraCuda is the math engine. Its artifact validates the shader math corpus:
- Every `assert_shader_math!` / `assert_shader_math_f64!` check runs via
  NagaExecutor on CPU
- Precision tiers (f32/DF64/f64) are explicit in the output
- Cross-vendor results (if GPU available) are reported alongside CPU reference
- The WGSL shaders in `shaders/` are the auditable source — a physicist reads
  them to verify the algorithm matches the paper

### For hotSpring specifically

hotSpring is the science validation biome. Its artifact validates published
physics:
- Each of Chuna's three papers has named checks with paper citations
- Convergence data, conservation laws, and spectral properties are measured
- The `expected/` directory contains reference data traced to ICER/MILC runs
- A physicist compares JSON output against their own production data

---

## Why One Artifact

TC Chuna is in Germany. He SSHs to a login node. He has no GPU. He runs
`./run` and sees 41/41 pass in under 2 minutes. He copies the `results/`
JSON and compares it against his MILC data from 2021.

His advisor at MSU gets the same USB stick. Plugs it into a workstation with
an RTX A6000. Runs `./run`. The binary detects the GPU, runs dual-path
validation, reports GPU and CPU results side by side. Same 41/41.

A student at CERN gets the tarball. Untars it on lxplus. No GPU on the login
node. `./run`. Same 41/41. They show their supervisor. The supervisor runs it
on a GPU batch node. Dual-path. Same results.

One artifact. Three continents. Five substrates. Same math.

---

## Container Deployment (v1.1)

For non-Linux hosts or environments where native binaries cannot execute
(restricted HPC, macOS, Windows without WSL2), the artifact includes an
OCI container image.

### Container Layout

```
validation/
├── container/
│   └── hotspring-guidestone.tar   # OCI image (Docker/Podman)
├── hotspring.bat                  # Windows launcher
└── Dockerfile                     # (at project root, for rebuilding)
```

### Container Image

- **Base**: Ubuntu 22.04
- **Deps**: `libvulkan1`, `mesa-vulkan-drivers`
- **Contents**: Full `validation/` artifact mounted at `/opt/validation`
- **Entry**: `./hotspring` (same unified entry point)
- **Size**: ~150 MB compressed tarball

### Container Usage

```bash
docker load < container/hotspring-guidestone.tar
docker run --rm hotspring-guidestone:v0.7.0 validate
docker run --rm --device /dev/dri hotspring-guidestone:v0.7.0 validate
```

### Cross-OS Entry Points

| OS | Entry Point | How It Works |
|----|-------------|-------------|
| Linux | `./hotspring` | Native binary dispatch (arch + GPU auto-detect) |
| macOS | `sh ./hotspring` | Auto-detects non-Linux, dispatches to Docker/Podman |
| Windows | `hotspring.bat` | Checks WSL2 first, then Docker Desktop |

### Filesystem Compatibility

The `_lib.sh` `resolve_binary()` function handles non-executable filesystems:

1. Attempt `chmod +x` on the resolved binary
2. If that fails (exFAT, NTFS, NFS noexec), copy to `$TMPDIR` and chmod there
3. Execution proceeds transparently from the tmpdir copy

This makes the artifact deployable on exFAT-formatted USB drives (readable
on all OSes) without requiring ext4.

---

## Compliance Checklist

```
## Validation Artifact — <Spring/Primal> <Version>

Entry Point:
- [ ] ./hotspring validate works (or ./run as backward compat)
- [ ] Single entry point with subcommands (ecoBin UniBin pattern)

Cross-Platform:
- [ ] Works on a fresh x86_64 Linux with no GPU, no sudo, no internet
- [ ] Works on a fresh aarch64 Linux with no GPU, no sudo, no internet (if --cross built)
- [ ] Static musl binary has zero dynamic library dependencies
- [ ] GPU binary only requires libc + libvulkan (no other runtime deps)
- [ ] GPU detection is automatic (glibc + Vulkan probe), no user flags needed

Cross-OS (v1.1):
- [ ] OCI container image included in container/ (optional but recommended)
- [ ] Windows launcher (hotspring.bat) delegates to WSL2 or Docker (optional)
- [ ] macOS auto-dispatch to Docker/Podman in entry point (optional)
- [ ] exFAT tmpdir fallback in resolve_binary() (required if USB deployment)
- [ ] OS detection (detect_os()) for non-Linux dispatch (required if container shipped)

Validation:
- [ ] CPU-only validation covers the full check suite (not a subset)
- [ ] Every check has: name, paper reference, measured value, threshold, justification
- [ ] JSON output written to results/ with substrate and engine metadata
- [ ] Reference data in expected/ with provenance

Layout:
- [ ] Arch-first bin layout: bin/<arch>/{static,gpu}/<name>
- [ ] Legacy symlinks: bin/{static,gpu}/<name>-<arch> (backward compat)
- [ ] CHECKSUMS covers all binaries, scripts, and reference data
- [ ] README is plain ASCII, 80 columns, readable with cat
- [ ] Total artifact size < 100 MB (dual binary), < 50 MB (static only)
- [ ] LICENSE file present (AGPL-3.0-or-later)

benchScale Validation:
- [ ] Passes 4-substrate Docker test (CPU Ubuntu, NVIDIA, AMD, Alpine)
- [ ] aarch64 via qemu-user substrate: ✅ validated (40/40 bit-identical)
- [ ] Optional: agentReagents VM template passes verification
```

---

## Relationship to Other Standards

| Standard | Relationship |
|----------|-------------|
| ecoBin | The validation binary IS an ecoBin (pure Rust, static musl, cross-arch) |
| Spring Presentation | The 5-Minute Test now has a binary-only path: `./run` |
| plasmidBin | Artifact binaries are harvested to plasmidBin; artifact tarballs to GitHub Releases |
| scyBorg licensing | The artifact is AGPL-3.0 — anyone who receives it can use, modify, redistribute |
| liveSpore ColdSpore | USB deployments use ext4 or exFAT + dual binaries (static + GPU); see `LIVESPORE_DEPLOYMENT_REVIEW.md` |
| OCI container | Universal fallback for non-Linux or restricted environments; see `UNIFIED_ARTIFACT_EVOLUTION.md` |
