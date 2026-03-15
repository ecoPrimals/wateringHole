# Gate Deployment Standard — Operational Substrate

**Purpose**: Defines the standard hardware, OS, and tooling configuration for an
ecoPrimals gate. Any machine matching this spec can run the full ecosystem.

**Last Updated**: March 15, 2026

---

## What Is a Gate?

A gate is a physical computer that runs the ecoPrimals stack. The name comes from
the project's naming convention: **Eastgate** (primary), **biomeGate** (HPC).
A gate is sovereign — you own it, you control it, no cloud dependency.

---

## Current Gates

### Eastgate (Primary Development)

| Component | Spec |
|-----------|------|
| **CPU** | AMD (desktop-class) |
| **GPU** | NVIDIA RTX 4070 (Ada Lovelace, SM89) |
| **RAM** | 32+ GB |
| **Storage** | NVMe SSD |
| **OS** | Pop!\_OS 22.04 LTS (System76, Ubuntu-based) |
| **Role** | Daily driver, development, single-GPU validation |

### biomeGate (Multi-GPU HPC)

| Component | Spec |
|-----------|------|
| **CPU** | AMD Threadripper 3970X (32C/64T) |
| **GPU 1** | NVIDIA RTX 3090 (Ampere, SM86) — proprietary driver |
| **GPU 2** | NVIDIA Titan V (Volta, SM70) — NVK open-source driver |
| **RAM** | 128 GB |
| **Storage** | NVMe SSD |
| **OS** | Pop!\_OS 22.04 LTS |
| **Role** | Lattice QCD, WDM transport, multi-GPU validation, Kokkos parity benchmarks |
| **Cost** | ~$4,000 (assembled from used parts) |

biomeGate was built specifically to extend hotSpring beyond what Eastgate's
single RTX 4070 could do — lattice QCD at 8⁴ and above, dual-GPU cooperative
dispatch, VFIO sovereign compute.

---

## Operating System

| Requirement | Standard |
|-------------|----------|
| **Distribution** | Pop!\_OS (System76) — preferred. Ubuntu LTS acceptable. |
| **Kernel** | Linux 6.x+ |
| **Display server** | X11 or Wayland (Pop!\_OS defaults) |
| **Init system** | systemd |
| **Package manager** | apt + flatpak (system), cargo (Rust) |

### Why Pop!\_OS?

- System76 hardware support (if using System76 machines)
- NVIDIA driver integration out of the box (hybrid graphics, PRIME)
- Ubuntu package ecosystem without Snap enforcement
- Stable LTS base with a usable desktop
- COSMIC desktop (Rust-native, aligns with ecosystem philosophy)

### Kernel Configuration for Sovereign Compute

For VFIO GPU passthrough (coralReef sovereign path):

- `intel_iommu=on` or `amd_iommu=on` in kernel command line
- VFIO modules loaded: `vfio`, `vfio_pci`, `vfio_iommu_type1`
- GPU isolated from host driver for sovereign dispatch

---

## Toolchain

### Rust

| Tool | Version | Notes |
|------|---------|-------|
| **rustc** | stable (latest) | Primary compilation target |
| **rustc nightly** | latest | Used for `cargo doc`, some unstable features |
| **cargo** | bundled with rustc | Build, test, publish |
| **clippy** | bundled | `pedantic` + `nursery`, zero warnings mandatory |
| **rustfmt** | bundled | Standard formatting |
| **cargo-criterion** | latest | Benchmarking (healthSpring, neuralSpring) |
| **wasm-pack** | latest | WebAssembly targets (if needed) |

Install via `rustup`:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup default stable
rustup component add clippy rustfmt
rustup install nightly
```

### Editor

| Tool | Version | Notes |
|------|---------|-------|
| **Cursor** | Latest | VS Code fork with AI agent. Primary development environment. |

Cursor extensions:
- rust-analyzer (Rust language server)
- Even Better TOML (Cargo.toml editing)
- GitLens (git history visualization)

### Python (Cross-Validation Only)

| Tool | Version | Notes |
|------|---------|-------|
| **Python** | 3.10+ | Reference implementations for paper parity |
| **numpy** | latest | Numerical baselines |
| **scipy** | latest | Statistical baselines |
| **scikit-bio** | latest | wetSpring diversity cross-validation |
| **pip** | latest | Package management |

Python is never in the production path. It exists solely to generate reference
outputs that Rust implementations are validated against.

### GPU Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| **wgpu** | Portable GPU compute via Vulkan/Metal/DX12 | Primary GPU path for all springs |
| **vulkaninfo** | GPU capability probing | Verify Vulkan support |
| **nvidia-smi** | NVIDIA GPU monitoring | Temperature, memory, utilization |
| **mesa (NVK)** | Open-source NVIDIA Vulkan driver | Titan V on biomeGate |

No CUDA SDK. No cuDNN. No vendor-specific compute frameworks. The portable path
uses wgpu (Vulkan backend). The sovereign path uses coralReef (VFIO + native
shader compilation).

### System Utilities

| Tool | Purpose |
|------|---------|
| **git** | Version control (SSH to GitHub) |
| **gh** | GitHub CLI (PRs, issues) |
| **rg** (ripgrep) | Fast code search |
| **fd** | Fast file finder |
| **htop** | Process monitoring |
| **nvtop** | GPU process monitoring |

---

## Directory Structure

Standard layout on a gate:

```
~/Development/
├── ecoPrimals/           # Main workspace
│   ├── wateringHole/     # Shared knowledge layer (this repo)
│   ├── whitePaper/       # gen3/, baseCamp, attsi/, atlasHugged
│   ├── wetSpring/        # QS, 16S pipeline, Anderson ecology
│   ├── hotSpring/        # MD, nuclear EOS, lattice QCD
│   ├── neuralSpring/     # ML, surrogates, reservoir computing
│   ├── groundSpring/     # Spectral theory, measurement science
│   ├── airSpring/        # Precision agriculture, hydrology
│   ├── healthSpring/     # PK/PD, microbiome, biosignal, NLME
│   ├── ludoSpring/       # Game science, HCI, procedural generation
│   ├── barraCuda/        # Pure math library (standalone)
│   ├── coralReef/        # Sovereign shader compiler
│   ├── phase1/
│   │   ├── squirrel/     # AI coordination
│   │   ├── beardog/      # Cryptography
│   │   ├── songbird/     # Networking
│   │   └── nestgate/     # Data storage
│   └── phase2/
│       ├── biomeOS/      # Orchestration substrate
│       ├── petalTongue/  # Visualization / UI
│       ├── rhizoCrypt/   # Ephemeral memory (DAG)
│       ├── sweetGrass/   # Attribution / provenance
│       └── loamSpine/    # Immutable ledger
├── metalForge/           # Cross-substrate dispatch (if separate)
└── scripts/              # Utility scripts
```

Each spring and primal is its own git repository. No monorepo.

---

## Network Configuration

| Service | Protocol | Notes |
|---------|----------|-------|
| **GitHub** | SSH (git@github.com) | All repos pushed via SSH keys |
| **NCBI E-utilities** | HTTPS | NestGate data provider for live data |
| **crates.io** | HTTPS | Upstream contributions (planned) |

No cloud compute. No CI/CD runners (yet — planned via self-hosted).
All compilation and testing happens on the gate.

---

## Minimum Gate Spec

To run the ecoPrimals stack at a useful level:

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 8 cores, x86_64 | 16+ cores (Ryzen 7 / Threadripper) |
| **GPU** | Any Vulkan-capable GPU | NVIDIA RTX 3060+ (f64 capable) |
| **RAM** | 16 GB | 32+ GB |
| **Storage** | 256 GB SSD | 1 TB+ NVMe |
| **OS** | Any Linux with Vulkan | Pop!\_OS 22.04 LTS |

Springs can run without a GPU (CPU fallback via barraCuda), but GPU acceleration
is where the performance story lives. coralReef's sovereign path requires NVIDIA
(SM70+) with VFIO support.

---

## Post-Install Checklist

After setting up a new gate:

- [ ] Pop!\_OS installed with NVIDIA drivers (if applicable)
- [ ] Rust toolchain installed via rustup (stable + nightly)
- [ ] Cursor installed with rust-analyzer
- [ ] SSH key generated and added to GitHub
- [ ] `~/Development/ecoPrimals/` directory created
- [ ] All repos cloned via SSH
- [ ] `cargo test --all-features` passes on at least one spring
- [ ] `vulkaninfo` shows GPU capabilities (if GPU present)
- [ ] Python 3.10+ with numpy/scipy available for cross-validation
