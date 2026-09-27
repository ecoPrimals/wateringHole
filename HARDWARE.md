# ecoPrimals Hardware Profile — Running Inventory

**Last Updated**: Sep 27, 2026 (Wave 158+)
**Location**: House 1 (Lansing MI area) + House 2 + Cloud + Remote
**Architecture Families**: 8 (x86_64-linux, x86_64-windows, aarch64-linux, aarch64-darwin, aarch64-ios, armv7-android, riscv64gc-linux, wasm32)
**Total Investment**: ~$17,000

---

## Architecture Landscape

### What We Compile For

| # | Target Triple | ISA | Status | Builder | Depot |
|---|---------------|-----|--------|---------|-------|
| 1 | `x86_64-unknown-linux-musl` | x86-64 | **PRIMARY** | sporeGate (foreman) | 18/18 |
| 2 | `x86_64-unknown-linux-gnu` | x86-64 | Production | ironGate + sporeGate | 14/14 |
| 3 | `x86_64-pc-windows-gnu` | x86-64 | Production | blueGate (cross) | 14/17 |
| 4 | `aarch64-unknown-linux-musl` | ARMv8.2-A | Production | ironGate (cross) | 15/15 |
| 5 | `aarch64-apple-darwin` | ARMv8.5-A (Apple Silicon) | Production | graftGate (native) | 16/16 |
| 6 | `aarch64-apple-ios` | ARMv8.3-A (A12+) | Staged | graftGate (cross) | Pending |
| 7 | `armv7-linux-androideabi` | ARMv7-A (Tensor G3) | Deployed | eastGate (cross) | — |
| 8 | `riscv64gc-unknown-linux-gnu` | RV64GC (RVA23) | **NEW** | Jupiter 2 (native) / eastGate (cross) | Pending |
| 9 | `wasm32-unknown-unknown` | WebAssembly | Experimental | any | — |

### Industry Standards: Where the ISAs Stand (Sep 2026)

#### x86-64 — The Incumbent
Our primary. Intel and AMD, DDR3 through DDR5, 2012 i7-4771 through 2025 i9-14900K. Mature toolchains, universal library support. The workhorse ISA — will remain primary for years. AVX-512 available on EPYC (strandGate) and newer Intel. Nothing new to acquire here; we have broad coverage.

#### ARMv8/v9 — The Mobile and Efficiency King
Two sub-families in our fleet:
- **Cortex-A76/A78 (ARMv8.2-A)**: Raspberry Pi 5/500 (BCM2712), our Pi cluster. Mature Linux support, 8 GB sufficient for Tower Atomic.
- **Apple Silicon (ARMv8.5-A + Apple AMX)**: M4 Mac Mini on graftGate. Custom microarchitecture, unified memory, Metal GPU. Sole Darwin builder authority. Apple's AMX (matrix coprocessor) is undocumented but real — macOS/iOS acceleration for ML workloads.
- **Tensor G3 (ARMv9)**: Pixel 8a on grapheneGate. Android + StrongBox HSM. Mobile mesh node.

The ARM world is fragmenting into application profiles much like RISC-V. ARMv9 adds SVE2 (scalable vector extensions), MTE (memory tagging), and BTI (branch target identification). Our Pi 500s are v8.2 (no SVE2), graftGate's M4 is v8.5 with Apple's custom extensions, Tensor G3 is v9. For our purposes this doesn't matter — `aarch64-unknown-linux-musl` covers all Linux ARM64 targets.

#### RISC-V RV64GC (RVA23) — The Open Frontier
**This is the genuinely new one.** The Jupiter 2 with SpacemiT K3 is the first RVA23-compliant board we own. What changed from RVA22:

- **V (Vector Extension)**: Optional → **MANDATORY**. 1024-bit vectors on A100 cores. Wider than any x86 AVX-512 (512-bit).
- **Zvfhmin/Zvbb/Zvkt**: Mandatory vector half-precision, bit-manipulation, constant-time crypto.
- **Hypervisor**: Mandatory. Full hardware virtualization.
- **Scalar crypto removed**: Use vector crypto instead — faster.

RVA23 is the inflection where software can finally *assume* vectors exist and optimize accordingly. Ubuntu 26.04 adopted RVA23 as baseline — won't run on older RISC-V. This is why the Jupiter 2 matters: it's not another science project board, it's the first board where the ecosystem is serious.

**What to watch**: The `riscv64a23-unknown-linux-gnu` Rust target (RVA23-specific) is in development. Currently we use `riscv64gc-unknown-linux-gnu` which targets the baseline RV64GC without assuming RVA23 extensions. When the a23 target lands, we'll get auto-vectorization for free.

---

## Gate Inventory — Full Fleet

### House 1 (Online / Bring-up This Week)

#### sporeGate — Foreman + Depot + Cascade Hub
| Component | Specification |
|-----------|---------------|
| **CPU** | AMD Ryzen 5 6600H (6C/12T) |
| **RAM** | 27 GB DDR5 |
| **Storage** | NVMe |
| **Network** | CRS310 ether8 at 2.5G |
| **OS** | Linux |
| **Role** | Build foreman, depot authority, cascade, inner membrane |
| **Status** | ✅ ONLINE |

#### northGate — Personal Gaming + Remote Compute
| Component | Specification |
|-----------|---------------|
| **CPU** | AMD Ryzen 9 9950X3D (16C/32T, 3D V-Cache) |
| **GPU** | NVIDIA RTX 5090 (32 GB GDDR7, Blackwell SM120) |
| **RAM** | 96 GB DDR5 |
| **Storage** | 5 TB NVMe |
| **Network** | 10G NIC (pending cable), 1G active |
| **OS** | Windows 11 |
| **Role** | Strongest single GPU in mesh. Gaming primary, compute secondary. |
| **Status** | 🔄 ENROLLING |

#### biomeGate — Semi-Mobile HPC / HBM2 Test Bench
| Component | Specification |
|-----------|---------------|
| **CPU** | AMD Threadripper 3970X (32C/64T) |
| **Display GPU** | NVIDIA RTX 5060 (8 GB GDDR7) |
| **Work GPUs** | 2× Titan V (12 GB HBM2 ea), 2× MI50 (16 GB HBM2 ea) |
| **NPU** | BrainChip Akida AKD1000 (from strandGate) |
| **RAM** | 256 GB DDR4 |
| **Storage** | 5 TB NVMe |
| **OS** | Pop!_OS |
| **Role** | HBM2 sovereign compiler dev (coralReef sm_70 + gfx906). hotSpring team home. |
| **Status** | ⏸️ OFFLINE — power on needed |

#### graftGate — Darwin Builder (Apple Silicon)
| Component | Specification |
|-----------|---------------|
| **SoC** | Apple M4 (10C: 4P+6E, 10-core GPU, 16-core Neural Engine) |
| **RAM** | 16–24 GB unified LPDDR5 |
| **Storage** | NVMe (internal) |
| **Network** | 1G Ethernet + Wi-Fi 6E. WG overlay via iPhone XS USB tethering. |
| **OS** | macOS (Sequoia) |
| **Role** | Sole Darwin compilation authority. 16/16 aarch64-apple-darwin. iOS builder (pending Apple Dev Program). |
| **Status** | ⏸️ OFFLINE — power on needed |
| **Arch** | `aarch64-apple-darwin` |

**Apple Silicon notes**: The M4 is ARMv8.5-A with Apple's custom extensions: AMX (matrix coprocessor for ML), ProRes encoder/decoder, 16-core Neural Engine. The Neural Engine is locked to CoreML — no direct access from Rust. The AMX is used transparently by Accelerate.framework and BLAS. For our Rust builds, it's just a fast aarch64 CPU. What matters is that it's the *only* machine that can produce signed Darwin and iOS binaries.

#### Jupiter 2 — RISC-V Pioneer (NEW)
| Component | Specification |
|-----------|---------------|
| **SoC** | SpacemiT K3 (RVA23) |
| **CPU** | 8× X100 @ 2.4 GHz (general, VLEN=256) + 8× A100 @ 2.0 GHz (AI, VLEN=1024) |
| **GPU** | IMG PowerVR BXM-4-64-MC1 (Vulkan 1.3, OpenCL 3.0) |
| **AI** | Up to 60 TOPS (A100 cores + IME2 matrix engine) |
| **RAM** | 32 GB LPDDR5 (6400 MT/s) |
| **Storage** | 128 GB onboard UFS (3.4 GB/s read) + M.2 NVMe slot |
| **Network** | 10GbE SFP+ + 1GbE RJ45 + Wi-Fi 6 |
| **OS** | Bianbu 4.0 (Debian-based, kernel 6.18) / Ubuntu 26.04 available |
| **Role** | 7th architecture family. RISC-V native builder. Mesh node. Vector compute playground. |
| **Status** | 🆕 ARRIVED — bring-up pending |
| **Arch** | `riscv64gc-unknown-linux-gnu` |
| **Power** | 11W idle, 22W load |

**K3 architecture notes**: big.LITTLE RISC-V. The A100 cores are kernel-fenced — standard userspace only runs on 8 X100 cores. A100 cores require `/proc/set_ai_thread` registration before scheduling. 3 MB TCM on-chip SRAM at 5.4 GB/s from A100 cores. Memory bandwidth is ~3 GB/s (1/5th of comparable ARM — main bottleneck). The 10GbE SFP+ is the fastest NIC in House 1.

#### 3× Raspberry Pi 500 — ARM64 Cluster (NEW)
| Component | Specification |
|-----------|---------------|
| **SoC** | BCM2712 (Cortex-A76 4C @ 2.4 GHz, ARMv8.2-A) |
| **RAM** | 8 GB LPDDR4X (each) |
| **Storage** | microSD (+ optional M.2 2230 via HAT) |
| **Network** | 1GbE + Wi-Fi 5 + BT 5.0 |
| **Form** | Keyboard-integrated — self-contained workstation |
| **OS** | Raspberry Pi OS (64-bit) / Ubuntu Server |
| **Role** | Mesh gossip peers, site hosts, aarch64 validation fleet |
| **Status** | 🆕 ACQUIRED — bring-up pending |
| **Arch** | `aarch64-unknown-linux-musl` |
| **Power** | ~5W idle, ~12W load (each) |

**Pi 500 notes**: All 15 aarch64 primal binaries already exist in the depot. Zero compilation needed — just deploy. At ~5W idle per unit, three can run 24/7 as always-on mesh infrastructure for ~15W total.

#### DDR3 NUC Bench — x86 Sub-Builders
| Component | Specification |
|-----------|---------------|
| **CPU** | Intel Celeron J3455 (quad-core) |
| **RAM** | 4–8 GB DDR3 (each) |
| **Storage** | Various |
| **Network** | 1GbE |
| **Role** | Sub-builders, site hosts, mesh expansion |
| **Status** | 🆕 Available — compose pending |
| **Arch** | `x86_64-unknown-linux-musl` |

### House 2 (Offline — Power Rebalance Next Week)

#### eastGate — Overwatch + Primary Development
| Component | Specification |
|-----------|---------------|
| **CPU** | AMD Ryzen 9 7950X (16C/32T) |
| **Display GPU** | NVIDIA RTX 4070 (12 GB, Ada Lovelace) |
| **NPU** | BrainChip Akida AKD1000 |
| **RAM** | 128 GB DDR5 |
| **Storage** | NVMe |
| **Network** | 10G SFP+ |
| **OS** | Pop!_OS |
| **Role** | Overwatch orchestration, primary dev, primalSpring, code teams |
| **Status** | ✅ ONLINE |

#### ironGate — Primal Workhorse
| Component | Specification |
|-----------|---------------|
| **CPU** | Intel i9-14900K (24C/32T, P+E cores) |
| **GPU** | NVIDIA RTX 5070 (12 GB, Blackwell SM120) |
| **RAM** | 96 GB DDR5 |
| **Storage** | 3.6 TB NVMe |
| **Network** | 1G |
| **OS** | Pop!_OS 22.04 |
| **Role** | Agentic dev, composition validation, aarch64-linux builder, JupyterHub |
| **Status** | ⏸️ OFFLINE — power rebalance |

#### strandGate — Bioinformatics Powerhouse
| Component | Specification |
|-----------|---------------|
| **CPU** | Dual AMD EPYC 7452 (64C/128T total) |
| **GPU** | NVIDIA RTX 3090 (24 GB) + AMD RX 6950 XT (16 GB) |
| **NPU** | BrainChip Akida AKD1000 |
| **RAM** | 256 GB DDR4 ECC |
| **Storage** | 18 TB NVMe (2×2TB + 4×4TB Hyper M.2) |
| **OS** | Pop!_OS |
| **Role** | HPC, dual-vendor GPU validation, lattice QCD production, toadStool team |
| **Status** | ⏸️ OFFLINE — power rebalance. 45 QCD configs banked. |

#### westGate — Sovereign Data NAS
| Component | Specification |
|-----------|---------------|
| **CPU** | AMD Ryzen 7 5700X (8C/16T) |
| **GPU** | NVIDIA RTX 3070 (8 GB, Ampere) |
| **RAM** | 64 GB DDR4 |
| **Storage** | 50.7 TB ZFS raidz1 (5×14TB) + 2TB SSD cache + 1.8TB NVMe boot |
| **OS** | Pop!_OS 22.04 |
| **Role** | Cold storage archive, provenance data root, 153 datasets |
| **Status** | ⏸️ OFFLINE — power rebalance |

#### southGate — Full NUCLEUS + Canary
| Component | Specification |
|-----------|---------------|
| **CPU** | AMD Ryzen 7 5800X3D (8C/16T, 3D V-Cache) |
| **GPU** | NVIDIA RTX 4060 (8 GB, Ada Lovelace) |
| **RAM** | 128 GB DDR4 |
| **Storage** | 4.5 TB NVMe |
| **OS** | Pop!_OS 22.04 |
| **Role** | Full NUCLEUS deployment, validation canary |
| **Status** | ⏸️ OFFLINE — power rebalance |

#### blueGate — Windows Expansion
| Component | Specification |
|-----------|---------------|
| **RAM** | 128 GB DDR4 |
| **Storage** | 2 TB NVMe |
| **OS** | Windows |
| **Role** | Windows builder, cross-platform validation |
| **Status** | ⏸️ OFFLINE — rack move incomplete |

### Cloud

#### golgiBody — VPS Relay + Forgejo + Depot
| Component | Specification |
|-----------|---------------|
| **Provider** | DigitalOcean NYC |
| **Role** | Caddy reverse proxy, Forgejo (git.primals.eco), Zola site builder, depot server, WireGuard relay |
| **Sites** | sporeprint.primals.eco, detroit.primals.eco, gorilla.primals.eco |
| **Status** | ✅ ONLINE — cascade autonomous |

### Remote

#### flockGate — Brother's Node
| Component | Specification |
|-----------|---------------|
| **CPU** | Intel i9-13900K (24C/32T) |
| **GPU** | NVIDIA RTX 3070 Ti (8 GB) |
| **RAM** | 64 GB DDR5 |
| **OS** | Ubuntu 24.04.3 |
| **Role** | Remote covalent mesh node, latency-tolerant batch compute |
| **Status** | ⏸️ OFFLINE |

### Mobile

#### grapheneGate — Portable Mesh Anchor
| Component | Specification |
|-----------|---------------|
| **SoC** | Google Tensor G3 (ARMv9) |
| **Device** | Pixel 8a, GrapheneOS |
| **Role** | Mobile bearDog, HSM seed carrier, mesh beacon |
| **Arch** | `armv7-linux-androideabi` (Android) |
| **Status** | ✅ CARRIED |

#### iosGate — iOS Validation Target
| Component | Specification |
|-----------|---------------|
| **SoC** | Apple A12 Bionic |
| **Device** | iPhone XS |
| **Role** | iOS deploy target (pending Apple Dev Program) |
| **Arch** | `aarch64-apple-ios` |
| **Status** | GLACIAL — awaiting signing cert |

### Utility

#### NUC-Intake — Tunnel Termination
| Component | Specification |
|-----------|---------------|
| **Model** | GMKtec NucBox M6 |
| **RAM** | 32 GB |
| **Role** | External tunnel termination, reverse proxy |
| **Status** | Planned |

---

## Aggregate Hardware

| Resource | Total |
|----------|-------|
| **Gates (towers + SBCs)** | 16+ named gates |
| **Architecture families** | 8 ISAs |
| **CPU cores** | 200+ (across all gates) |
| **GPU VRAM (display tier)** | ~80 GB (RTX 5090 32 + 5070 12 + 5060 8 + 4070 12 + 4060 8 + 3070 8) |
| **GPU VRAM (work pool)** | ~128 GB (3× RTX 3090 72 + 2× Titan V 24 + 2× MI50 32) |
| **GPU VRAM (total)** | ~244 GB |
| **HBM2** | 56 GB (2× Titan V + 2× MI50, on biomeGate) |
| **System RAM** | ~1.4 TB |
| **Storage** | ~110 TB+ (50.7TB ZFS + NVMe across nodes) |
| **GPU vendors** | NVIDIA + AMD + IMG PowerVR |
| **GPU architectures** | Volta → Ampere → Ada → Blackwell (NVIDIA) + RDNA 2 (AMD) + PowerVR B-Series (RISC-V) |
| **CPU vendors** | Intel + AMD + Apple + Google + SpacemiT + Broadcom |
| **Memory types** | DDR3, DDR4, DDR4 ECC, DDR5, LPDDR4X, LPDDR5, HBM2, UFS, TCM SRAM |
| **NPU** | 3× BrainChip Akida AKD1000 + Apple Neural Engine (M4) + SpacemiT IME2 (K3) |
| **HSM** | 4× SoloKey FIDO2 + Android StrongBox + Apple Secure Enclave |
| **10GbE backbone** | House 2 all-10G (MikroTik), eastGate via 10G fiber to House 2, Jupiter 2 SFP+ (pending transceiver) |

---

## Work Card Pool (Swappable GPUs)

Large GPUs that move between gates based on workload:

| Card | Qty | VRAM | Type | Current Home |
|------|-----|------|------|-------------|
| RTX 3090 | 3 | 24 GB GDDR6X each | Compute | strandGate (1) + swappable (2) |
| Titan V | 2 | 12 GB HBM2 each | HBM2 compute | biomeGate |
| MI50 | 2 | 16 GB HBM2 each | HBM2 compute | biomeGate |
| Tesla K80 | 1 | 24 GB GDDR5 (2×12) | Legacy Kepler | biomeGate |

---

## Neuromorphic

| Card | Location | Interface |
|------|----------|-----------|
| BrainChip Akida AKD1000 | eastGate | PCIe (Phase C sovereign — zero vendor SDK) |
| BrainChip Akida AKD1000 | biomeGate | PCIe (moved from strandGate) |
| BrainChip Akida AKD1000 | strandGate | PCIe |
| **Total** | | **3 cards** |

rustChip (pure Rust AKD1000/AKD1500 driver) validated on eastGate: 18.8K Hz inference, 367 tests, 10 undocumented hardware discoveries. First non-Python path to the hardware.

---

## Networking

### Physical Topology

House 1 ←— **10G fiber** —→ House 2

**House 2** is the 10G backbone — all gates connected at 10 Gbps to the MikroTik switch.

**House 1** has eastGate on 10G SFP+ (cross-house fiber link). Other House 1 nodes (sporeGate, Jupiter 2, Pi 500s, NUCs, biomeGate, graftGate) connect via 1G RJ45 to the MikroTik.

| Component | Location | Speed | Status |
|-----------|----------|-------|--------|
| MikroTik switch | House 2 | 10G backbone | Active — all House 2 gates on 10G |
| 10G fiber link | House 1 ↔ House 2 | 10 Gbps | Active — eastGate endpoint in House 2 |
| 10G SFP+ NIC | eastGate | 10 Gbps | Active (via fiber to House 2 switch) |
| 10G NIC (copper) | northGate | 10 Gbps | Installed, on House 2 switch |
| 10G NIC | ironGate | 10 Gbps | On House 2 switch |
| 10G NIC | strandGate | 10 Gbps | On House 2 switch |
| 10G NIC | westGate | 10 Gbps | On House 2 switch |
| 10G NIC | southGate | 10 Gbps | On House 2 switch |
| 10GbE SFP+ | Jupiter 2 | 10 Gbps | Built-in, House 1 — needs transceiver + fiber/DAC to switch |
| CRS310 2.5G | sporeGate | 2.5 Gbps | Active (House 1 MikroTik uplink) |
| 1G RJ45 | House 1 nodes | 1 Gbps | Pi 500s, NUCs, biomeGate, graftGate |
| WireGuard overlay | golgiBody ↔ mesh | WAN | Live (sporeGate, eastGate, northGate) |

**Note**: Jupiter 2's built-in 10GbE SFP+ could be a House 1 high-speed node if connected to the MikroTik via fiber or DAC, but currently House 1 nodes other than eastGate are on 1G.

---

## What's Still Missing / To Acquire

### High Priority

| Item | Why | Est. Cost |
|------|-----|-----------|
| **SFP+ transceiver/DAC for Jupiter 2** | Connect Jupiter 2's 10GbE SFP+ to House 1 MikroTik or House 2 switch via fiber | $20-50 |
| **Apple Developer Program** | Unlock iOS signing for iosGate (iPhone XS) | $99/yr |
| **NVMe for Pi 500s** (optional) | M.2 2230 HAT for faster storage than microSD | $30-60 ea |

### Medium Priority

| Item | Why | Est. Cost |
|------|-----|-----------|
| **AKD1500 (next-gen Akida)** | rustChip already has AKD1500 register definitions; test on real silicon | ~$100-200 |
| **ECC DDR5 for eastGate** | Currently non-ECC; science pipeline would benefit | $200+ |
| **UPS / power management** | House 1 + House 2 gates need clean shutdown on power loss | $200-400 |

### Exploration / Wishlist

| Item | Why | Est. Cost |
|------|-----|-----------|
| **RISC-V board with RVV 1.0 + IOMMU** | VFIO passthrough testing for rustChip on RISC-V | TBD |
| **Lattice / Intel FPGA** | coralReef sovereign shader compilation to fabric | $100-500 |
| **More HBM2/HBM3 cards** | Expand coralReef validation surface (MI100, MI200?) | Marketplace finds |
| **POWER / s390x board** | Silicon atheism completeness (2 more ISA families) | Rare/expensive |

---

## The Heterogeneity Principle

Every gate is different. DDR3 sits next to DDR5 next to LPDDR5 next to HBM2. A 2012 i7 runs the same primal binaries as a 2025 Ryzen 9. NVIDIA sits next to AMD sits next to PowerVR sits next to BrainChip. A Celeron NUC runs Tower Atomic alongside a 64-core EPYC.

That's silicon atheism — the architecture doesn't care what the metal is. 8 ISA families, 6 CPU vendors, 3 GPU vendors, 3 NPU families, 5 memory technologies, and one unified codebase that compiles for all of them.

The display/work tier split, the work card pool, the sub-builder dispatch — these patterns exist because the hardware demanded them. The topology is fluid; the architecture handles it because heterogeneity is the natural state.

**Built from scratch. Assembled in a basement and a living room. Two houses, one cloud node, one brother. The metal is real.**
