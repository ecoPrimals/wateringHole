# External Validation Artifact Standard

**Status**: Ecosystem Standard v1.0
**Adopted**: March 31, 2026
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

```
validation/
├── run                     # Entry point. One command. (shell script, executable)
├── README                  # Plain text, 80 columns, no markdown renderer needed
├── bin/
│   ├── validate-x86_64     # Static musl ELF, x86_64
│   └── validate-aarch64    # Static musl ELF, aarch64
├── shaders/                # WGSL source (human-auditable, the actual math)
│   └── *.wgsl
├── expected/               # Reference results from known-good hardware
│   └── *.json
├── results/                # Created at runtime — output goes here
├── CHECKSUMS               # SHA-256 of everything in bin/ and expected/
└── LICENSE                 # AGPL-3.0-or-later
```

Total size: under 50 MB. Fits on any USB stick ever made.

---

## `run`

```bash
#!/bin/sh
set -eu

cd "$(dirname "$0")"

# Integrity
sha256sum -c CHECKSUMS --quiet 2>/dev/null || shasum -a 256 -c CHECKSUMS --quiet || {
    echo "INTEGRITY FAILED — files may be corrupted or tampered with"
    exit 1
}

# Architecture
ARCH=$(uname -m)
case "$ARCH" in
    x86_64|amd64)   BIN=bin/validate-x86_64 ;;
    aarch64|arm64)   BIN=bin/validate-aarch64 ;;
    *)               echo "Unsupported architecture: $ARCH"; exit 1 ;;
esac

if [ ! -x "$BIN" ]; then
    chmod +x "$BIN" 2>/dev/null || true
fi

# Run. The binary auto-detects GPU. No flags needed.
exec "$BIN" --expected expected/ --output results/
```

That's it. `./run` on a laptop. `./run` on ICER. `./run` at CERN. Same
command. Same output. The binary detects what's available and uses it.

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
| **Two architectures, one layout** | x86_64 and aarch64 binaries side by side. `run` picks the right one. |
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

## Compliance Checklist

```
## Validation Artifact — <Spring/Primal> <Version>

- [ ] ./run works on a fresh x86_64 Linux with no GPU, no sudo, no internet
- [ ] ./run works on a fresh aarch64 Linux with no GPU, no sudo, no internet
- [ ] Binary has zero dynamic library dependencies (ldd reports "not a dynamic executable")
- [ ] CPU-only validation covers the full check suite (not a subset)
- [ ] Every check has: name, paper reference, measured value, threshold, justification
- [ ] JSON output written to results/ with substrate and engine metadata
- [ ] Reference data in expected/ with provenance
- [ ] CHECKSUMS verified before execution
- [ ] README is plain ASCII, 80 columns, readable with cat
- [ ] Total artifact size < 50 MB
- [ ] LICENSE file present (AGPL-3.0-or-later)
```

---

## Relationship to Other Standards

| Standard | Relationship |
|----------|-------------|
| ecoBin | The validation binary IS an ecoBin (pure Rust, static musl, cross-arch) |
| Spring Presentation | The 5-Minute Test now has a binary-only path: `./run` |
| plasmidBin | Artifact binaries are harvested to plasmidBin; artifact tarballs to GitHub Releases |
| scyBorg licensing | The artifact is AGPL-3.0 — anyone who receives it can use, modify, redistribute |
