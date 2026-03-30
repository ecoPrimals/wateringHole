# The Watering Hole - ecoPrimals Ecosystem Guidance

**Purpose**: Authoritative project guidance for the ecoPrimals ecosystem — primals, springs, and gen4 products  
**Audience**: Any primal, spring, or gen4 product at any point in its evolution — plus external audiences (PIs, students, builders, creatives, compliance)  
**Last Updated**: March 29, 2026

---

## What is the Watering Hole?

The Watering Hole is the shared knowledge layer of the ecoPrimals project. Every primal - whether newly conceived or production-hardened - comes here to understand the ecosystem it belongs to: what other primals exist, what standards govern interoperability, how coordination works, and what principles guide evolution.

This is not documentation about a subdirectory. This is the living reference for the entire project.

---

## Core Concepts

### What is a Primal?

A **primal** is a collection of **primitives** - small, focused capabilities that solve one domain well. Primals are autonomous: each is a self-contained Rust binary that knows only itself. Complexity is never solved by making a primal larger. It is solved through **coordination** - primals composing their primitives together at runtime, orchestrated by biomeOS.

**Key properties of every primal:**

- **Self-knowledge only**: A primal knows what it can do, never what others can do
- **Capability-based discovery**: Primals find each other at runtime by advertising capabilities
- **Zero compile-time coupling**: No primal imports another primal's code
- **Pure Rust**: 100% Rust application code, zero C dependencies
- **UniBin architecture**: One binary per primal, multiple operational modes

### What are Primitives?

Primitives are the atomic operations a primal provides. BearDog's primitives include Ed25519 signing, BLAKE3 hashing, and X25519 key exchange. Songbird's primitives include TLS 1.3 handshakes, mDNS discovery, and UDP multicast. A primitive is the smallest unit of capability in the ecosystem.

### How do Primals Coordinate?

Primals communicate via **JSON-RPC 2.0** over platform-agnostic transports (Unix sockets, abstract sockets, TCP, named pipes). They never share memory or embed each other's code. biomeOS discovers primals by their capabilities at runtime and coordinates them into higher-order behaviors.

The result: complex systems **emerge** from simple composition, rather than being engineered monolithically.

---

## The Primals

### Foundation Primals

These primals form the NUCLEUS deployment architecture. They are the bedrock of the ecosystem - production-ready, extensively tested, and required for core ecosystem function.

| Primal | Domain | Role | Status |
|--------|--------|------|--------|
| **BearDog** | Cryptography | All cryptographic operations: signing, encryption, key exchange, hashing, certificates, genetic lineage | Production (A+ LEGENDARY) |
| **Songbird** | Networking | Network orchestration: TLS 1.3, service discovery, NAT traversal, federation, BirdSong protocol, Pure Rust Tor | Production (S+) |
| **NestGate** | Data Storage | Content-addressed storage, dataset management, capability-based service discovery | Production (A++ TOP 1%) |
| **ToadStool** | Hardware Infrastructure | Hardware discovery, capability probing, compute orchestration: CPU, GPU, NPU, WASM, containers, edge. 20,843 tests, 96+ JSON-RPC methods. Node Atomic for sovereign compute. `toadstool-sysmon` (pure Rust /proc, zero C). ecoBin v3.0 certified. Cross-compile verified (aarch64, armv7 in CI) | Production (A++ GOLD) |
| **BarraCuda** | Pure Math | FMA-evolved math, 816 WGSL f64 shaders (the mathematics), naga-IR optimisation (FMA fusion, DCE), precision strategy (f64/DF64/f32). Writes the math; coralReef compiles it; toadStool runs it. Budded from ToadStool (S93). v0.3.11, 4,162+ tests | Production (A+) |
| **coralReef** | Shader Compilation | Sovereign WGSL→native shader compiler. naga parser + lowering passes (f64, FMA fusion, dead expression elimination). JSON-RPC IPC via XDG discovery. AMD E2E proven, NVIDIA SM70-SM89. coral-gpu unified compute abstraction. VFIO dispatch with PFIFO channel + V2 MMU + USERD_TARGET fix. **coral-glowplug** production-grade boot-persistent PCIe device lifecycle broker (systemd daemon, personality hot-swap, health monitor, VFIO-first boot, graceful shutdown, IOMMU group handling). **coral-ember** immortal VFIO fd holder: `SCM_RIGHTS` fd passing, atomic `swap_device` RPC, DRM isolation preflight, external fd holder deadlock detection. **DRM isolation**: Xorg `AutoAddGPU=false` + udev 61-prefix seat tag removal — compute GPU driver swaps invisible to display manager. **FECS firmware direct execution proven** (LS bypass on clean falcon). SEC2 EMEM breakthrough (Exp 066-070). D3hot→D0 sovereign VRAM recovery. GP_PUT cache flush experiment (Iter 57). Reproducibility checklist for adding new GPUs | Production (Phase 10, Iter 57) |
| **Squirrel** | AI Coordination | Sovereign AI model context protocol, multi-MCP coordination, vendor-agnostic inference | Production (A++) |
| **biomeOS** | Orchestration | Composition primal: Neural API (290+ translations, 26 domains), 5 coordination patterns (Sequential, Parallel, ConditionalDag, Pipeline streaming, Continuous 60Hz), 5-tier capability discovery, NUCLEUS composition, PathwayLearner optimization, NDJSON streaming, bonding model, Dark Forest coordination, provenance trio wiring, niche self-knowledge, caller-agnostic lineage. Cross-gate federation (GateRegistry, route.register, forward_to_remote_gate), inference scheduling (VRAM-aware GPU routing). 7,202 tests, 90%+ coverage (llvm-cov, all above 90%), zero C deps, ecoBin v3.0, primalSpring-aligned. 0 TODO/FIXME/HACK, 0 unsafe prod, 0 clippy warnings | Production (v2.76, Security A++ LEGENDARY) |

### Post-NUCLEUS Primals

These primals build emergent behaviors on the NUCLEUS foundation. They compose into higher-order patterns (RootPulse, Memory & Attribution Stack) coordinated by biomeOS via the Neural API. Each is functional and tested, representing the next evolutionary phase.

| Primal | Domain | Role | Status |
|--------|--------|------|--------|
| **petalTongue** | Representation | Universal UI: visual, audio, terminal, web, headless. Accessibility-first multi-modal rendering | Production (A++) |
| **rhizoCrypt** | Ephemeral Memory | Content-addressed DAG engine for working memory. Sessions, Merkle trees, real-time streaming | Production (A+) |
| **sweetGrass** | Attribution | Semantic provenance (v0.7.22). W3C PROV-O braids, fair attribution, 24 JSON-RPC methods + tarpc 0.37 + REST + UDS, UniBin, ecoBin, 1,077 tests, Edition 2024, zero unsafe, sovereign types (no shared crates), Arc<str> zero-copy identifiers, IpcErrorPhase w/ Timeout, DispatchOutcome, OrExit, proptest, parking_lot locks, Provenance Trio coordination via JSON-RPC, Tower Atomic enforced, provenance-trio-types banned in deny.toml | Production |
| **LoamSpine** | Permanence | Immutable linear ledger for selective permanence. Loam Certificates for ownership and transfer | Production (A+) |
| **skunkBat** | Defense | Defensive network security: threat detection, graduated response, baseline profiling | Production |

### Supporting Tools

| Tool | Purpose |
|------|---------|
| **sourDough** | Starter culture - scaffolding, genomeBin tooling, ecosystem bootstrapping |

### Infrastructure Tools (`ecoPrimals/infra/`)

These tools validate and deploy primal compositions. They don't implement primal behavior — they test that compositions work before reaching real gates. Originally from the syntheticChemistry org, now integrated into ecoPrimals.

| Tool | Domain | Role | Status |
|------|--------|------|--------|
| **plasmidBin** | Binary deployment | Harvested primal binaries (x86_64 + aarch64), deploy/fetch/validate scripts, multi-arch gate deployment | Production |
| **benchScale** | Lab substrate | Pure Rust crate (v3.0.0) + shell lab creation. clap CLI, yaml_serde, capability-based config (env-overridable paths/IPs/OS). Docker/LXD/QEMU backends, YAML topologies, 5 network presets, plasmidBin deploy + health pipeline. 212 tests | Production — v3.0.0 modernized, live-tested Docker labs |
| **agentReagents** | Artifact supply chain | Cloud-init configs, VM images, ISOs, debs for gate provisioning. Hardened scripts (`set -euo pipefail`), `defaults.env`, SHA256 verification, lint.sh quality gate. 9 active + 9 legacy scripts | Active — hardened, ecoPrimals-branded |
| **fossilRecord** | Ecosystem archaeology | Historical record of ecosystem evolution, archived handoffs and decisions | Archive |
| **sporePrint** | Deployment templates | Gate deployment blueprints and patterns | Templates |

**Local validation pipeline** (benchScale + plasmidBin + primalSpring):
```
validate_local_lab.sh → create Docker lab → deploy binaries → health check → run experiments → teardown
```
One command, ~30 seconds, repeatable on any machine with Docker. Pre-gates remote SSH deploys via `deploy_gate.sh --local-validate`.

---

## Composed Systems

Primals achieve their greatest power through composition. These are not separate projects - they are coordination patterns that emerge when primals work together.

### Tower Atomic

**What**: BearDog (crypto) + Songbird (TLS/HTTP) = Pure Rust HTTPS

**How**: Songbird implements TLS 1.3 protocol logic. BearDog provides all cryptographic operations via JSON-RPC. Neither embeds the other. The result is a fully Pure Rust HTTPS stack with zero C dependencies.

**Used by**: Any primal that needs external network access routes through Tower Atomic.

### NUCLEUS

**What**: The full primal composition orchestrated by biomeOS.

**Layers**:
- **Tower Atomic** = BearDog + Songbird (crypto + network)
- **Node Atomic** = Tower + ToadStool (hardware) + BarraCuda (math)
- **Nest Atomic** = Tower + NestGate (+ storage)
- **Full NUCLEUS** = All primals + Squirrel (+ AI)

*Note*: BarraCuda budded from ToadStool into a standalone primal (S93).
BarraCuda is pure math — WGSL shaders and precision strategy. coralReef
compiles the math to native GPU binaries. ToadStool discovers and dispatches
hardware. Springs depend on BarraCuda directly for math without pulling
ToadStool's runtime or coralReef's compiler.

biomeOS composes these atomics based on what capabilities are available at runtime.

### RootPulse

**What**: Distributed version control that emerges from primal coordination - not a monolithic VCS.

**Composition**:
- **rhizoCrypt** provides the ephemeral DAG workspace (fast, lock-free, present/future)
- **LoamSpine** provides the immutable linear history (permanent, cryptographically provable, past)
- **NestGate** provides content-addressed blob storage
- **BearDog** provides cryptographic signing and verification
- **sweetGrass** provides semantic attribution tracking
- **Songbird** provides discovery and federation

**Coordinator**: biomeOS orchestrates these primals via the Neural API. No primal knows about "version control" - biomeOS composes their primitives into temporal coordination patterns, and version control emerges.

**Core insight**: "RootPulse is what primals DO together, not what they ARE."

### Plasmodium (Over-NUCLEUS Collective)

**What**: The emergent coordination layer formed when 2+ NUCLEUS instances bond covalently.

**Analogy**: Named after the slime mold *Physarum polycephalum* -- no central brain, collective intelligence, pulsing coordination, graceful degradation.

**How**: biomeOS on any gate queries the local Songbird mesh for bonded peers, connects to their NUCLEUS instances, and aggregates capabilities, models, and load into a unified collective view. Workloads route to the best gate based on capability match, resource availability, and model affinity.

**Key properties**:
- No master node -- any gate can query the collective
- Gates join and leave dynamically (like slime mold pseudopods)
- Uses only existing primal primitives (Songbird mesh, BearDog trust, AtomicClient IPC)
- Security: genetic lineage trust via shared family seed, BearDog Dark Forest verification

**Specification**: `phase2/biomeOS/specs/PLASMODIUM_OVER_NUCLEUS_SPEC.md`  
**CLI**: `biomeos plasmodium status|gates|models`

### Neural API

**What**: biomeOS's adaptive orchestration layer that routes semantic requests to capable primals.

**How**: A caller requests `capability.call("crypto", "sha256")` and the Neural API discovers which primal provides that capability, routes the request, and returns the result. The caller never needs to know about BearDog specifically.

**Architecture**:
- Layer 1: Primals (capabilities via JSON-RPC)
- Layer 2: biomeOS (orchestration, routing, learning)
- Layer 3: Niche APIs (domain patterns like RootPulse, RPGPT)

**Five Coordination Patterns** (all driven by TOML graphs):

| Pattern | Method | Description |
|---------|--------|-------------|
| Sequential | `graph.execute` | Nodes in dependency order |
| Parallel | `graph.execute` | Independent nodes concurrently |
| ConditionalDag | `graph.execute` | DAG with `condition`/`skip_if` branching |
| Pipeline | `graph.execute_pipeline` | Streaming via bounded mpsc channels — items flow through nodes immediately |
| Continuous | `graph.start_continuous` | Fixed-timestep tick loop (e.g., 60Hz for game engines) |

**biomeOS as Composition Primal**: biomeOS is functionally the super-service — the
primal that composes all other primals into systems. While it sits at the same level
as other primals (sovereign, self-contained, JSON-RPC first), its unique role is
orchestrating emergent systems: RootPulse (version control), RPGPT (game engines),
AlphaFold-class (protein folding), and any other system that emerges as a function
of primal coordination.

**Streaming (v2.43)**: Pipeline graphs use NDJSON streaming — primals write multiple
response lines per request. The `AtomicClient::call_stream()` reads them as they
arrive. No new protocol needed. All primals already have streaming transport.

The PathwayLearner analyzes execution metrics and suggests optimizations (parallelization,
prewarming, batching, caching) that improve over time.

---

## Architecture Standards

These standards define how every primal is built, packaged, and deployed.

### UniBin - Binary Structure Standard

One binary per primal, multiple operational modes via subcommands. Professional CLI with `--help`, `--version`, and structured error messages. Every primal is a single executable named after itself.

**Specification**: `UNIBIN_ARCHITECTURE_STANDARD.md`  
**Technical paper**: `whitePaper/technical/UNIBIN_TECHNICAL_SPECIFICATION.md`

### ecoBin - Universal Portability Standard

ecoBin = UniBin + Pure Rust + Cross-Platform. Zero C dependencies in application code, cross-compiles to any Rust target with a single `cargo build` command, platform-agnostic IPC with runtime transport discovery.

**Specification**: `ECOBIN_ARCHITECTURE_STANDARD.md`  
**Technical paper**: `whitePaper/technical/ECOBIN_TECHNICAL_SPECIFICATION.md`

### genomeBin - Autonomous Deployment Standard

genomeBin = ecoBin + deployment wrapper. Self-extracting archive that auto-detects the system, installs the correct binary, configures services, and validates health. One command installs on any system with zero manual configuration.

**Specification**: `GENOMEBIN_ARCHITECTURE_STANDARD.md`  
**Technical paper**: `whitePaper/technical/GENOMEBIN_TECHNICAL_SPECIFICATION.md`

### The Evolutionary Ladder

```
UniBin   (structure)    → One binary, multiple modes
  ↓
ecoBin   (portability)  → + Pure Rust, cross-compilation, platform-agnostic IPC
  ↓
genomeBin (deployment)  → + Auto-detection, service integration, health monitoring
```

All ecoBins are UniBins. All genomeBins are ecoBins. Each stage adds capability without replacing the previous.

---

## Communication Standards

### Primal IPC Protocol

JSON-RPC 2.0 over platform-agnostic transports. Capability-based discovery with zero cross-embedding. Every primal implements its own IPC independently - standards define WHAT, primals implement HOW.

**Specification**: `PRIMAL_IPC_PROTOCOL.md`

### Universal IPC Standard (v3.0)

Behavioral specification for multi-transport IPC. Each primal discovers the best transport at runtime: Unix sockets on Linux/macOS, abstract sockets on Android, named pipes on Windows, TCP as universal fallback. No shared IPC crate - each primal owns its communication code.

**Specification**: `UNIVERSAL_IPC_STANDARD_V3.md`

### BirdSong Protocol

Encrypted UDP discovery protocol for auto-trust within genetic lineages. Songbird broadcasts encrypted beacons; only primals sharing the same family seed can decrypt them. Zero metadata leakage.

**Specification**: `birdsong/BIRDSONG_PROTOCOL.md`

### Semantic Method Naming

Method names describe intent, not implementation: `crypto.sign`, `tls.handshake`, `storage.put`. Domain namespaces enable Neural API translation and isomorphic evolution across primals.

**Specification**: `SEMANTIC_METHOD_NAMING_STANDARD.md`

---

## Security Model

### Genetic Lineage

A group of primals sharing a common `family_seed` - enabling cryptographic auto-trust. BearDog manages lineage seeds (nuclear DNA, for identity/permissions) and beacon seeds (mitochondrial DNA, for Dark Forest discovery).

### Auto-Trust Within Family

Primals of the same genetic lineage trust each other automatically. Decryption of a BirdSong beacon proves family membership. No manual configuration, no certificate authorities.

### Zero Trust Outside Family

No trust without family membership. Encrypted payloads are unreadable to outsiders. Continuous validation. Dark Forest protocol ensures zero metadata leakage - observers cannot even tell that communication is occurring.

### Pure Rust Security

Zero C dependencies eliminates entire classes of memory safety vulnerabilities. RustCrypto suite for all cryptographic operations. No openssl, no ring, no C assembly.

---

## Primal Interaction Map

### Currently Working

- **Songbird + BearDog**: Encrypted BirdSong discovery (Tower Atomic)
- **biomeOS + All Primals**: Health monitoring, capability discovery, Neural API routing
- **biomeOS + petalTongue**: Real-time SSE events for ecosystem visualization

### Wired (biomeOS coordination layer)

- **rhizoCrypt + LoamSpine + sweetGrass**: Provenance trio — `rootpulse_commit` graph orchestrates dehydration → sign → store → commit → attribute
- **Any Spring + Provenance Trio**: `provenance_pipeline` graph — universal experiment provenance
- **NestGate + LoamSpine**: Content-addressed storage backing immutable history

### primalSpring Coordination (ecosystem self-validation + gen4 bridge)

- **primalSpring + All NUCLEUS Primals**: Atomic composition testing (Tower, Node, Nest, Full NUCLEUS)
- **primalSpring + biomeOS**: Graph execution validation — all 5 coordination patterns with real primals
- **primalSpring + Provenance Trio**: RootPulse emergent system validation (commit, branch, merge, diff, federate)
- **primalSpring + Songbird Mesh**: Plasmodium formation, gate failure, capability aggregation
- **primalSpring + neuralSpring + wetSpring + hotSpring + ToadStool + NestGate**: coralForge neural object pipeline
- **primalSpring + airSpring + wetSpring + neuralSpring**: Cross-spring ecology data flow
- **primalSpring + fieldMouse + NestGate + sweetGrass**: Edge data ingestion pipeline
- **primalSpring + petalTongue**: SSE visualization pipeline
- **primalSpring + Squirrel**: AI coordination via biomeOS capability graph
- **primalSpring + esotericWebb**: gen4 composition validation — Webb deploy graphs declare `primalspring_primal` as composition health validator (`composition.webb_*_health` capabilities). primalSpring validates that primal stacks compose correctly for product use.
- **primalSpring + ludoSpring**: Game science composition — ludoSpring validates game models, primalSpring validates the IPC and composition that makes those models available to gen4 products

### Under Development

- **Songbird + Songbird**: Cross-tower federation, multi-family routing

**Detail**: `INTER_PRIMAL_INTERACTIONS.md`

---

## The Generational Model

The ecoPrimals ecosystem evolves through four generations, each building on
the previous:

| Gen | Question | Answer | Artifacts |
|-----|----------|--------|-----------|
| **gen1** | Can we build it? | Yes — $11K cluster, fault-tolerant HPC, AI-assisted dev | NestGate, Squirrel, hardware fleet |
| **gen2** | What should we build? | A sovereign protocol — 8 composable primals, AGPL as trust, BYOAI | biomeOS, BearDog, Songbird, Philosophy of Forgetting |
| **gen3** | Does it work? | Yes — 12,510+ checks, 70+ papers, 7 springs, 14 primals | Springs, constrained evolution, SPRING/PRIMAL catalogs, thesis |
| **gen4** | Who uses it? | Creatives, scientists, sovereign builders | sporeGarden products, standalone plasmidBin, creative surface |

### How the Generations Relate

- **Primals** are gen2 entities — they define capabilities and exist as deployable binaries
- **Springs** are gen3 entities — they validate primals by reproducing published science
- **Products** (sporeGarden) are gen4 entities — they compose primals into tools people use
- **plasmidBin** (standalone repo) is the gen4 deployment surface where validated binaries land

Springs have tighter coupling to primals (e.g. hotSpring cracks sovereign GPU
compiling with coralReef, ludoSpring validates game science models). This is
expected — springs are the validation layer. Products (gen4) have zero coupling
to spring source; they consume only deployed binaries via IPC.

### Three Organizations

```
syntheticChemistry/     — Springs (science validation, gen3) + infra tools (benchScale, agentReagents)
ecoPrimals/             — Primals + infrastructure (gen2–gen3)
sporeGarden/            — Products (creative surface, gen4)
```

### plasmidBin — Primal Deployment Surface

[github.com/ecoPrimals/plasmidBin](https://github.com/ecoPrimals/plasmidBin) is
the standalone deployment surface. Primal teams build and harvest binaries →
`harvest.sh` creates GitHub Releases with checksums → consumers run `fetch.sh`
to populate their local plasmidBin. 7 x86_64 + 5 aarch64 ecoBin-compliant binaries as of v2026.03.28. See `IPC_COMPLIANCE_MATRIX.md` for per-primal transport compliance.

The local `ecoPrimals/plasmidBin/` directory is the gen3 embedded version
(manifest + sources). The standalone repo is the gen4 deployment surface
(metadata + binaries via GitHub Releases).

`deploy_gate.sh --local-validate` runs a benchScale Docker lab before SSH-pushing to a real gate.

### benchScale + agentReagents — Validation Substrate

benchScale (`ecoPrimals/infra/benchScale`) creates repeatable multi-node labs from
YAML topology files. Docker containers, network condition simulation (5 presets from
basement LAN to satellite), automated binary deployment from plasmidBin. Originally
a syntheticChemistry project, now wired into primalSpring's `validate_local_lab.sh`.

agentReagents (`ecoPrimals/infra/agentReagents`) is the artifact supply chain for
gate provisioning: cloud-init configs, VM images, ISOs. Used by benchScale's libvirt
backend for Tier 2 (VM) validation.

**Live status (March 28)**: 7/8 primals alive in Docker, 2 experiments pass, per-primal
CLI gaps documented. Both tools modernized: benchScale v3.0.0 (yaml_serde, clap, capability config,
212 tests), agentReagents hardened (strict bash, defaults.env, SHA256, legacy scripts archived).
See `BENCHSCALE_AGENTREAGENTS_LOCAL_VALIDATION_SUBSTRATE_HANDOFF_MAR28_2026.md` and
`BENCHSCALE_AGENTREAGENTS_MODERNIZATION_HANDOFF_MAR28_2026.md`.

### gen4 Products

**esotericWebb** ([sporeGarden/esotericWebb](https://github.com/sporeGarden/esotericWebb))
is the first gen4 product — a CRPG engine that composes primals into a playable
game. It consumes 8 primal domains via `PrimalBridge` (JSON-RPC IPC), with
graceful degradation when primals are absent. 166 tests, 23 bridge methods,
zero spring imports. Its `EVOLUTION_GAPS.md` feeds gap pressure back to primal
teams — driving the ecosystem forward.

**helixVision** (planned — sporeGarden) is the second gen4 product pattern — a
sovereign genomics discovery platform that composes wetSpring (16S pipeline,
microbiome analytics) and neuralSpring/coralForge (structure prediction) into a
deployable tool for field biologists, wastewater engineers, and environmental
scientists. Same PrimalBridge pattern, same deploy graphs, different domain.
coralForge becomes helixVision's structure prediction module; the gen3 science
doesn't rename.

### gen4 Documentation

Full gen4 documentation lives in `whitePaper/gen4/` (21 working papers across
6 sections: thesis, architecture, products, economics, knome, outreach).

---

## Design Principles

1. **Single Responsibility**: Each primal does one thing. BearDog only does cryptography. Songbird only does networking. Complexity emerges from coordination, not from expanding scope.

2. **Interface Segregation**: Primals expose narrow, focused interfaces. LoamSpine doesn't know about "commits" - it provides append-only storage. biomeOS composes that into version control.

3. **Dependency Inversion**: Primals depend on abstract capabilities, not concrete implementations. Any storage provider works, not just NestGate.

4. **Message Passing**: Communication via messages over IPC, never shared state. No locks, no race conditions, inherently concurrent.

5. **Emergence Over Engineering**: Don't build a monolithic VCS - coordinate existing primals and let version control emerge. Don't build a monolithic security stack - let BearDog and Songbird compose into Tower Atomic.

---

## Document Index

### Master Index
- **`GEN4_BRIDGE.md`** — **Start here if you're new to gen4.** How primals become products. The flow from binary harvest to product composition to gap pressure. What every team needs to know.
- **`STANDARDS_AND_EXPECTATIONS.md`** — Single-document reference for all ecoPrimals standards, expectations, and conventions. Links to every standard below.
- **`GLOSSARY.md`** — Definitive terminology for the ecoPrimals ecosystem. Gate, primal, spring, atomic, niche, deploy graph, germination, absorption, delegation, fossil record, and every other term.
- **`GATE_DEPLOYMENT_STANDARD.md`** — Hardware, OS, and tooling spec for ecoPrimals gates. Multi-arch (x86_64/aarch64), multi-substrate (desktop, mobile/Android, remote bootstrap). plasmidBin integration, Dark Forest seed distribution, network topology patterns.

### Architecture Standards
- `UNIBIN_ARCHITECTURE_STANDARD.md` — Binary structure (one binary, subcommands)
- `ECOBIN_ARCHITECTURE_STANDARD.md` — Universal portability (Pure Rust, cross-compile)
- `GENOMEBIN_ARCHITECTURE_STANDARD.md` — Autonomous deployment (self-extracting, auto-detect)
- `SPRING_AS_NICHE_DEPLOYMENT_STANDARD.md` — Springs deploy as biomeOS niches
- `SPRING_NICHE_DEPLOYMENT_GUIDE.md` — How-to guide for niche deployment

### Communication Standards
- `PRIMAL_IPC_PROTOCOL.md` — JSON-RPC 2.0 inter-primal communication (v3.0 — consolidated, includes platform-agnostic transport + dual protocol)
- `SEMANTIC_METHOD_NAMING_STANDARD.md` — `domain.verb` API naming conventions
- `CROSS_SPRING_DATA_FLOW_STANDARD.md` — Time series exchange format

### Security & Networking (birdsong/)
- `birdsong/BIRDSONG_PROTOCOL.md` — Encrypted UDP discovery (BirdSong)
- `birdsong/DARK_FOREST_BEACON_GENETICS_STANDARD.md` — Two-seed genetic lineage architecture
- `birdsong/SONGBIRD_TLS_TOWER_ATOMIC_INTEGRATION_GUIDE.md` — Tower Atomic TLS guide
- `btsp/BEARDOG_TECHNICAL_STACK.md` — BearDog cryptographic foundation

### Domain & Beacon Infrastructure
- `DOMAIN_INFRASTRUCTURE.md` — Domain architecture: nestgate.io (BirdSong beacon via Cloudflare Tunnel), primals.eco (public portal via GitHub Pages), LAN cloud multi-machine resilience, operational procedures

### GPU & Numerical Computing
- `GPU_F64_NUMERICAL_STABILITY.md` — f64 precision lessons from hotSpring
- `NUMERICAL_STABILITY_EVOLUTION_PLAN.md` — Fast AND safe math strategy
- `SOVEREIGN_COMPUTE_EVOLUTION.md` — Pure Rust GPU stack (VFIO, glow plug, power management)
- `PURE_RUST_SOVEREIGN_STACK_GUIDANCE.md` — Cross-primal sovereign compute guidance
- `CROSS_SPRING_SHADER_EVOLUTION.md` — How springs evolve barraCuda collectively
- `SPRING_VALIDATION_ASSIGNMENTS.md` — Each spring validates specific barraCuda primitives

### Strategy & Licensing
- `LYSOGENY_PROTOCOL.md` — Area denial through open prior art
- `SCYBORG_PROVENANCE_TRIO_GUIDANCE.md` — **Ecosystem licensing standard** (AGPL + ORC + CC-BY-SA)
- `NOVEL_FERMENT_TRANSCRIPT_GUIDANCE.md` — NFT architecture (memory-bound digital objects)
- `UPSTREAM_CONTRIBUTIONS.md` — Standalone crates for crates.io from ecoPrimals

### Composition & Deployment
- `COMPOSITION_PATTERNS.md` — **Canonical reference** for deploy graphs (`[[graph.node]]` vs `[[nodes]]`), niche YAML, primal launch profiles, and 8-step socket discovery resolution order
- `SPOREGARDEN_DEPLOYMENT_STANDARD.md` — How gen4 products compose primals: BYOB model, esotericWebb reference implementation, environment contract, quality gates
- `PRIMALSPRING_COMPOSITION_GUIDANCE.md` — primalSpring's composition validation capabilities

### Coordination & Patterns
- `INTER_PRIMAL_INTERACTIONS.md` — Production interaction map and plans
- `PRIMAL_REGISTRY.md` — Complete primal definitions and primitive catalogs
- `IPC_COMPLIANCE_MATRIX.md` — Per-primal IPC compliance tracking (wire framing, sockets, health, port, standalone, substrate)
- `SPRING_AS_PROVIDER_PATTERN.md` — biomeOS capability registration
- `SPRING_PROVENANCE_TRIO_INTEGRATION_PATTERN.md` — Provenance trio integration
- `SPRING_EVOLUTION_ISSUES.md` — Active issues discovered by springs

### Presentation & External Review
- **`SPRING_PRIMAL_PRESENTATION_STANDARD.md`** — **Read before any docs sweep.** Checklist for making a spring/primal independently reviewable by PIs, students, hobbyists, and compliance reviewers. The 5-minute test. Self-assessment template. Common problems and fixes. References `publicRelease/` audience briefs.
- **`PUBLIC_SURFACE_STANDARD.md`** — **Read before any public publish.** GitHub repo descriptions, topic tags, PII review checklist, AI-ingestible `CONTEXT.md` template, and the copy-paste task for public surface passes. Defines the five layers: GitHub metadata, README on-ramp, AI context block, PII hygiene, and the reusable surface-pass blurb.

### Leverage Guides (Per-Primal)
- `BARRACUDA_LEVERAGE_GUIDE.md`, `BIOMEOS_LEVERAGE_GUIDE.md`, `CORALREEF_LEVERAGE_GUIDE.md`
- `LOAMSPINE_LEVERAGE_GUIDE.md`, `PRIMALSPRING_LEVERAGE_GUIDE.md`, `RHIZOCRYPT_LEVERAGE_GUIDE.md`
- `SQUIRREL_LEVERAGE_GUIDE.md`, `SWEETGRASS_LEVERAGE_GUIDE.md`, `TOADSTOOL_LEVERAGE_GUIDE.md`
- `PETALTONGUE_LEVERAGE_GUIDE.md`
- `WETSPRING_LEVERAGE_GUIDE.md`, `NEURALSPRING_LEVERAGE_GUIDE.md`
- `petaltongue/` — petalTongue integration documentation (biomeOS API, quick start, showcase)

### Spring Composition Guidance (Per-Spring)
- `airspring/AIRSPRING_COMPOSITION_GUIDANCE.md` — How airSpring composes with other springs and primals
- `healthspring/HEALTHSPRING_COMPOSITION_GUIDANCE.md` — How healthSpring composes with other springs and primals

### Handoffs
- `handoffs/*.md` — Active handoffs (91 current — latest version per primal/spring, cross-deploy substrate evolution, per-primal team debt handoffs)
- `fossilRecord/` — 691 absorbed handoffs (Feb–Mar 2026) — superseded evolution history, preserved as permanent record

---

## For New Primals

If you are a new primal entering the ecosystem:

1. **Read this document** to understand the ecosystem you are joining
2. **Review PRIMAL_REGISTRY.md** to see what capabilities already exist
3. **Follow UniBin standard** from day one (single binary, subcommands)
4. **Target ecoBin** (Pure Rust, zero C deps, cross-compilation)
5. **Implement IPC** following `PRIMAL_IPC_PROTOCOL.md` v3.0
6. **Advertise capabilities** so biomeOS can discover and coordinate you
7. **Register your primal** in PRIMAL_REGISTRY.md with your primitives
8. **Get your face together** per `SPRING_PRIMAL_PRESENTATION_STANDARD.md` — your repo should be reviewable by any of the four external audiences in 5 minutes

You do not need to know about other primals. You need to know what you can do, and how to tell the ecosystem about it.

---

## Getting Your Face Together

Every spring and primal should be independently reviewable by outsiders.
See **`SPRING_PRIMAL_PRESENTATION_STANDARD.md`** for the full checklist,
but the short version is: a reviewer should be able to do this in 5 minutes:

1. Open `README.md` → understand what this does and what it replaces
2. `cargo test --workspace` → see all tests pass
3. `cargo run --release --bin validate_<something>` → see explicit PASS/FAIL
4. Open `CHANGELOG.md` → understand recent evolution
5. Open `whitePaper/baseCamp/README.md` → see the faculty and science context

Four external audiences will read your repo without context:

| Audience | What They Look For |
|----------|-------------------|
| **Faculty / PIs** | What does this replace? How does it compare to commercial tools? Can I verify claims? |
| **Students / Core Facilities** | How do I build it? How do I run it? Where do I start? |
| **Hardware Builders / Hobbyists** | What hardware does it need? What can my GPU do? How do I contribute compute? |
| **Compliance / Institutional Review** | What standards does it meet? What are the dependencies? Is it safe? What's the license? |
| **Creatives / Game Designers** | What can I make with this? How do I author content? What do I keep? (gen4 audience via sporeGarden) |

The `publicRelease/` documents in `whitePaper/attsi/non-anon/contact/publicRelease/`
make ecosystem-wide claims. Each spring and primal must ensure its own presentation
supports those claims.

---

**The Watering Hole is maintained by all primals, springs, and products. Every evolution — from primal binary to spring validation to product composition — strengthens the whole ecosystem. gen4 is where the primals become invisible. The Watering Hole is where they stay visible to each other.**
