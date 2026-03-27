# Gate Deployment Standard — Operational Substrate

**Purpose**: Defines the standard hardware, OS, and tooling configuration for an
ecoPrimals gate. Any machine matching this spec can run the full ecosystem.

**Last Updated**: March 27, 2026

---

## What Is a Gate?

A gate is any device that runs the ecoPrimals stack. The name comes from the
project's naming convention: **Eastgate** (primary), **biomeGate** (HPC),
**flockGate** (family tower), **pixelGate** (mobile). A gate is sovereign — you
own it, you control it, no cloud dependency. Gates span architectures (x86_64,
aarch64), substrates (desktop Linux, Android/GrapheneOS, headless server), and
network topologies (LAN, hotspot, WAN behind NAT).

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

### flockGate (Family Tower — Remote)

| Component | Spec |
|-----------|------|
| **CPU** | Intel i9-13900K |
| **GPU** | NVIDIA RTX 3070 Ti |
| **RAM** | 32 GB |
| **Storage** | NVMe SSD |
| **OS** | Ubuntu 24.04.3 LTS |
| **Role** | Family compute tower, idle compute utilization, remote cross-deployment |
| **Access** | RustDesk remote, SSH (when port-forwarded), behind residential NAT |

flockGate demonstrates the "gamer friend" deployment pattern: a capable machine
owned by a trusted family member, provisioned via bootstrap script over remote
desktop, contributing idle compute to the family mesh.

### pixelGate (Mobile — aarch64)

| Component | Spec |
|-----------|------|
| **CPU** | ARM (Pixel SoC, aarch64) |
| **GPU** | Adreno (Vulkan-capable) |
| **RAM** | 8+ GB |
| **Storage** | UFS |
| **OS** | GrapheneOS (Android-based, privacy-focused) |
| **Role** | Mobile gate, cross-architecture validation, hotspot mesh node |
| **Access** | ADB over USB, iPhone hotspot for networking |

pixelGate demonstrates mobile substrate deployment: aarch64 musl-static binaries
pushed via ADB, abstract Unix sockets for IPC (SELinux-safe), TCP for cross-gate
communication. No systemd, no root, no package manager — pure binary deployment.

### Gate Type Summary

| Gate | Architecture | OS | Network | Deploy Method | Composition |
|------|-------------|-----|---------|---------------|-------------|
| **Eastgate** | x86_64 | Pop!_OS | LAN | Source build | Full NUCLEUS |
| **biomeGate** | x86_64 | Pop!_OS | LAN | Source build | Full NUCLEUS + multi-GPU |
| **flockGate** | x86_64 | Ubuntu | WAN (NAT) | Bootstrap script | Tower + compute |
| **pixelGate** | aarch64 | GrapheneOS | Hotspot/mobile | ADB push | Tower (minimal) |
| **friendGate** | x86_64 | Any Linux | WAN (NAT) | Bootstrap script | Tower + compute |

"friendGate" is the generic pattern for any remote machine bootstrapped via
`bootstrap_gate.sh`.

---

## Operating System

### Desktop/Server Gates (x86_64)

| Requirement | Standard |
|-------------|----------|
| **Distribution** | Pop!\_OS (System76) — preferred. Ubuntu LTS acceptable. |
| **Kernel** | Linux 6.x+ |
| **Display server** | X11 or Wayland (Pop!\_OS defaults) |
| **Init system** | systemd |
| **Package manager** | apt + flatpak (system), cargo (Rust) |

### Mobile Gates (aarch64)

| Requirement | Standard |
|-------------|----------|
| **OS** | GrapheneOS (preferred), stock Android with developer mode |
| **Kernel** | Linux (Android kernel) |
| **Shell** | `/system/bin/sh` via ADB |
| **Init system** | None (primals run as foreground processes via ADB shell) |
| **Package manager** | None (musl-static binaries pushed via ADB) |
| **IPC** | Abstract Unix sockets (SELinux-safe) + TCP |
| **Deploy tool** | ADB over USB |

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

### Cross-Compilation (for multi-arch gates)

| Tool | Purpose | Notes |
|------|---------|-------|
| **aarch64-linux-gnu-gcc** | aarch64 linker for musl targets | `apt install gcc-aarch64-linux-gnu` |
| **aarch64-linux-gnu-strip** | Strip aarch64 binaries on x86_64 host | Included with cross-gcc |
| **musl-tools** | x86_64 musl-static compilation | `apt install musl-tools` |
| **adb** | Android Debug Bridge for mobile gates | `apt install android-tools-adb` |

Rust targets for cross-compilation:
```bash
rustup target add x86_64-unknown-linux-musl
rustup target add aarch64-unknown-linux-musl
```

The `aarch64-linux-gnu-gcc` linker works for musl targets in pure Rust contexts
(no C code linked). Configure via:
```bash
export CARGO_TARGET_AARCH64_UNKNOWN_LINUX_MUSL_LINKER="aarch64-linux-gnu-gcc"
```

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

---

## plasmidBin Integration

Gates fetch primal binaries from `plasmidBin` (the ecosystem binary repository)
rather than building from source. This enables rapid deployment to machines
without a Rust toolchain.

### Binary Layout

```
plasmidBin/
├── primals/              # x86_64 musl-static primal binaries
│   ├── beardog
│   ├── songbird
│   ├── squirrel
│   ├── toadstool
│   ├── nestgate
│   └── aarch64/          # aarch64 musl-static primal binaries
│       ├── beardog
│       ├── songbird
│       └── ...
├── springs/              # Spring binaries (primalSpring only)
│   └── aarch64/
├── products/             # sporeGarden products (gitignored)
├── manifest.toml         # Version, arch, capability metadata
├── checksums.toml        # BLAKE3 checksums for all binaries
├── sources.toml          # GitHub repo + release asset patterns
├── fetch.sh              # Download from GitHub Releases
├── harvest.sh            # Publish local builds into plasmidBin
├── update.sh             # Fetch + verify workflow
├── deploy_gate.sh        # Deploy to remote gate via SSH
├── deploy_pixel.sh       # Deploy to Pixel/Android via ADB
├── bootstrap_gate.sh     # Self-contained bootstrap for fresh machines
├── start_primal.sh       # Unified primal startup wrapper
├── seed_workflow.sh       # Dark Forest seed lifecycle management
├── validate_gate.sh      # Single-gate health validation
├── validate_mesh.sh      # Multi-gate mesh validation
└── stop_gate.sh          # Graceful primal shutdown
```

### Fetching Binaries

On a gate with internet access:
```bash
cd ~/Development/ecoPrimals/plasmidBin
./fetch.sh --all                    # Fetch all primals for local arch
./update.sh --verify-only           # Verify checksums without fetching
```

Architecture is auto-detected. On aarch64 machines, binaries are fetched to
`primals/aarch64/`.

### Harvesting Local Builds

After building from source (development gates):
```bash
./harvest.sh --source /tmp/primalspring-deploy/primals
./harvest.sh --source /tmp/primalspring-deploy/primals/aarch64 --arch aarch64
```

Harvest strips, checksums, and copies binaries into the correct plasmidBin
directory.

---

## Deployment Patterns

### Pattern 1: Development Gate (Source Build)

The primary development machine builds from source and harvests into plasmidBin.

```bash
# Build musl-static binaries for both architectures
./scripts/build_ecosystem_musl.sh --harvest

# Validate
./plasmidBin/update.sh --verify-only
```

### Pattern 2: Bootstrap Gate (Remote Friend/Family)

For a fresh machine accessible via remote desktop (RustDesk) or SSH:

```bash
# On the development gate, generate bootstrap instructions:
./plasmidBin/deploy_gate.sh --mode bootstrap \
    --family-id <id> --dark-forest

# Remote user pastes in their terminal:
curl -sL https://raw.githubusercontent.com/ecoPrimals/plasmidBin/main/bootstrap_gate.sh | \
    bash -s -- --family-id <id> --dark-forest

# Remote user opens firewall:
sudo ufw allow 9100/tcp    # BearDog
sudo ufw allow 9200/tcp    # Songbird
```

The bootstrap script clones plasmidBin, fetches binaries, starts a Tower
(BearDog + Songbird), and prints the public IP for mesh registration.

### Pattern 3: Mobile Gate (ADB Push)

For Android/GrapheneOS devices connected via USB:

```bash
# Build aarch64 binaries (on development gate)
./scripts/build_ecosystem_musl.sh --aarch64-only --harvest

# Deploy to Pixel
./plasmidBin/deploy_pixel.sh \
    --dark-forest \
    --beacon-seed ~/.config/biomeos/family/.beacon.seed \
    --local-port-offset 10000

# Validate via ADB-forwarded ports
./plasmidBin/validate_gate.sh localhost:19100
```

Key mobile substrate considerations:
- Binaries go to `/data/local/tmp/plasmidBin/primals/`
- `HOME` and `TMPDIR` must point to writable directory (e.g., `/data/local/tmp/biomeos`)
- BearDog uses `--abstract` for SELinux-safe IPC sockets
- Songbird uses TCP `--port` (no filesystem UDS)
- ADB port forwarding bridges device ports to localhost

### Pattern 4: SSH Push Gate

For machines with SSH access:

```bash
./plasmidBin/deploy_gate.sh \
    --host user@remote-ip \
    --mode push \
    --family-id <id> \
    --dark-forest \
    --beacon-seed ~/.config/biomeos/family/.beacon.seed
```

---

## Dark Forest Seed Distribution

New gates require cryptographic seeds to join a family mesh. The two-seed genetic
architecture (defined in `birdsong/DARK_FOREST_BEACON_GENETICS_STANDARD.md`)
separates discovery from authorization:

| Seed | Analog | Shared? | Purpose |
|------|--------|---------|---------|
| **Beacon Seed** | Mitochondrial DNA | Yes (all family) | Encrypted discovery — who can *find* family |
| **Lineage Seed** | Nuclear DNA | No (unique per device) | Authorization — what a node can *do* |

### Seed Lifecycle

```bash
# Initialize family (once, on primary gate)
./plasmidBin/seed_workflow.sh init --family-name "eastgate-family"

# Add nodes
./plasmidBin/seed_workflow.sh add-node --node-id devgate
./plasmidBin/seed_workflow.sh add-node --node-id pixel
./plasmidBin/seed_workflow.sh add-node --node-id flockgate

# Export for remote distribution
./plasmidBin/seed_workflow.sh export --format base64

# Generate deploy bundle for a specific node
./plasmidBin/seed_workflow.sh distribute --node-id flockgate
```

### Distribution Methods

| Method | Use Case | Security |
|--------|----------|----------|
| **ADB push** | Mobile gate (USB connected) | Physical access required |
| **RustDesk paste** | Remote gate (bootstrap) | Shared screen, manual paste |
| **SSH scp** | Remote gate (SSH access) | Encrypted channel |
| **Out-of-band** | Any | Phone call, Signal message, etc. |

The beacon seed is shared with all family members. Lineage seeds are unique per
node and should only be distributed to the specific device.

---

## Network Topology Patterns

### LAN (Local Network)

```
Eastgate ──── LAN ──── biomeGate
```

Direct connectivity, no NAT. Primals discover via BirdSong multicast.
This is the simplest deployment and the default for `mesh.auto_discover`.

### Hotspot LAN (Mobile Tethering)

```
Eastgate ──── iPhone Hotspot LAN ──── pixelGate
```

The iPhone creates a local network. Eastgate and pixelGate can reach each other
directly over this LAN. ADB port forwarding provides an alternative path.
BirdSong multicast works within the hotspot subnet.

### WAN with NAT (Remote Gate)

```
Eastgate ──── Internet ──── NAT ──── flockGate
```

flockGate is behind residential NAT. Options for connectivity:

1. **Port forwarding**: Remote user opens ports 9100, 9200 on their router
2. **STUN/punch**: Songbird's built-in NAT traversal (requires STUN server)
3. **Relay**: Songbird relay server with lineage-based authentication

For bootstrapped gates, port forwarding is the recommended initial approach.
`bootstrap_gate.sh` prints firewall hints.

### Mixed Topology (Three-Node Mesh)

```
devGate (x86_64, LAN)
    ├── hotspot LAN ──── pixelGate (aarch64)
    └── WAN/NAT ──────── flockGate (x86_64)
```

This is the tested topology. All three gates share a beacon seed (mitobeacon)
for encrypted discovery. Each has a unique lineage seed for authorization.
Mesh validation:

```bash
./plasmidBin/validate_mesh.sh \
    --gates "devGate=localhost,pixelGate=<ip>,flockGate=<ip>" \
    --birdsong-exchange
```

---

## Minimum Gate Spec (Updated)

### Desktop/Server Gate

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 8 cores, x86_64 | 16+ cores (Ryzen 7 / Threadripper) |
| **GPU** | Any Vulkan-capable GPU | NVIDIA RTX 3060+ (f64 capable) |
| **RAM** | 16 GB | 32+ GB |
| **Storage** | 256 GB SSD | 1 TB+ NVMe |
| **OS** | Any Linux with Vulkan | Pop!\_OS 22.04 LTS |

### Mobile Gate

| Component | Minimum | Notes |
|-----------|---------|-------|
| **CPU** | aarch64 (ARMv8+) | Any modern ARM SoC |
| **RAM** | 4 GB | 8+ GB recommended |
| **OS** | Android 10+ with developer mode | GrapheneOS preferred |
| **Access** | ADB over USB | `adb devices` must list device |

### Bootstrap Gate (Remote)

| Component | Minimum | Notes |
|-----------|---------|-------|
| **CPU** | 4 cores, x86_64 | Any modern desktop/laptop |
| **RAM** | 8 GB | 16+ GB recommended for compute |
| **OS** | Any Linux with bash, curl, git | Ubuntu LTS, Fedora, Arch all work |
| **Network** | Internet access + at least 2 open TCP ports | 9100, 9200 for Tower |

Springs can run without a GPU (CPU fallback via barraCuda), but GPU acceleration
is where the performance story lives. coralReef's sovereign path requires NVIDIA
(SM70+) with VFIO support.

---

## Post-Install Checklists

### Desktop Gate

- [ ] Linux installed with NVIDIA drivers (if applicable)
- [ ] Rust toolchain installed via rustup (stable + nightly)
- [ ] aarch64 cross-compilation target installed (`rustup target add aarch64-unknown-linux-musl`)
- [ ] Cross-compilation toolchain installed (`gcc-aarch64-linux-gnu`, `musl-tools`)
- [ ] Cursor installed with rust-analyzer
- [ ] SSH key generated and added to GitHub
- [ ] `~/Development/ecoPrimals/` directory created
- [ ] All repos cloned via SSH
- [ ] plasmidBin binaries fetched and checksums verified
- [ ] `cargo test --all-features` passes on at least one spring
- [ ] `vulkaninfo` shows GPU capabilities (if GPU present)
- [ ] Python 3.10+ with numpy/scipy available for cross-validation
- [ ] Dark Forest seeds initialized (`seed_workflow.sh init`)

### Bootstrap Gate

- [ ] `bootstrap_gate.sh` run successfully
- [ ] plasmidBin cloned and binaries fetched
- [ ] Beacon seed distributed and loaded
- [ ] Firewall ports opened (9100, 9200)
- [ ] Tower validated (`validate_gate.sh <ip>`)

### Mobile Gate

- [ ] Developer mode enabled, ADB authorized
- [ ] aarch64 musl-static binaries pushed via `deploy_pixel.sh`
- [ ] Beacon seed pushed
- [ ] ADB port forwarding configured
- [ ] Gate validated (`validate_gate.sh localhost:<forwarded-port>`)
