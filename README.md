# The Watering Hole - ecoPrimals Ecosystem Guidance

**Purpose**: Authoritative project guidance for every primal in the ecoPrimals ecosystem  
**Audience**: Any primal, at any point in its evolution  
**Last Updated**: May 11, 2026 (Phase 60+ POST-INTERSTADIAL — zero upstream gaps, 413 canonical methods, 8/8 springs evolved, post-interstadial targets all green, evolution cycle ownership model, LTEE Targeted GuideStone subsystem)

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
| **ToadStool** | Compute | Universal compute orchestration: CPU, GPU, neuromorphic, WASM, containers. BarraCuda — 643+ WGSL f64 shaders (shader-first: all math is WGSL, zero CPU-only production math). f64 transcendental polyfills, lattice QCD (14 shaders + HMC/CG), HFB physics, linalg GPU-dispatched, PPPM GPU FFT, RBF surrogate GPU pipeline. Runtime f64 probe + probe-informed Fp64Strategy. AlphaFold2 Evoformer primitives (6 attention + 2 structure). HMM forward/backward/Viterbi. Anderson coupling. Grid search ops via ComputeDispatch builder. ESN 11-head multi-target. ODE universal precision (Scalar/op_*). All Springs absorbed at f64. | Production (A++ GOLD) |
| **Squirrel** | AI Coordination | Sovereign AI model context protocol, multi-MCP coordination, vendor-agnostic inference | Production (A++) |
| **biomeOS** | Orchestration | Ecosystem substrate: Neural API, capability routing, NUCLEUS composition, bonding model, Dark Forest coordination | Production (A, Security A++ LEGENDARY) |

### Post-NUCLEUS Primals

These primals build emergent behaviors on the NUCLEUS foundation. They compose into higher-order patterns (RootPulse, Memory & Attribution Stack) coordinated by biomeOS via the Neural API. Each is functional and tested, representing the next evolutionary phase.

| Primal | Domain | Role | Status |
|--------|--------|------|--------|
| **petalTongue** | Representation | Universal UI: visual, audio, terminal, web, headless. Accessibility-first multi-modal rendering | Production (A++) |
| **rhizoCrypt** | Ephemeral Memory | Content-addressed DAG engine for working memory. Sessions, Merkle trees, real-time streaming | Production (A+) |
| **sweetGrass** | Attribution | Semantic provenance tracking. W3C PROV-O compliant braids, fair attribution calculation | Production (A+) |
| **LoamSpine** | Permanence | Immutable linear ledger for selective permanence. Loam Certificates for ownership and transfer | Production (A+) |
| **skunkBat** | Defense | Defensive network security: threat detection, graduated response, baseline profiling | Production |

### Supporting Tools

| Tool | Purpose |
|------|---------|
| **sourDough** | Starter culture - scaffolding, genomeBin tooling, ecosystem bootstrapping |

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
- **Node Atomic** = Tower + ToadStool (+ compute)
- **Nest Atomic** = Tower + NestGate (+ storage)
- **Full NUCLEUS** = All primals + Squirrel (+ AI)

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
- Layer 1: Primals (capabilities)
- Layer 2: biomeOS (orchestration, learning)
- Layer 3: Niche APIs (domain patterns like RootPulse)

The system learns from usage patterns over time, optimizing coordination automatically.

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

### Operational (May 2026)

- **rhizoCrypt + LoamSpine**: Dehydration (temporal collapse from DAG to linear) — validated via projectNUCLEUS
- **NestGate + LoamSpine**: Content-addressed storage backing immutable history — validated
- **sweetGrass + LoamSpine**: Attribution braids anchored to permanent timeline — validated
- **Provenance trio (rhizoCrypt + LoamSpine + sweetGrass)**: Full pipeline exercised on ironGate (Nest Atomic, 9 primals)

### Under Development

- **Songbird + Songbird**: Cross-tower federation, multi-family routing
- **Spring library-to-binary rewiring**: Springs replacing local barraCuda imports with ecobin IPC
- **petalTongue DataBinding per spring**: Science outputs as live presentations
- **sweetGrass braids per spring**: Experiment attribution as structural artifacts

---

## Design Principles

1. **Single Responsibility**: Each primal does one thing. BearDog only does cryptography. Songbird only does networking. Complexity emerges from coordination, not from expanding scope.

2. **Interface Segregation**: Primals expose narrow, focused interfaces. LoamSpine doesn't know about "commits" - it provides append-only storage. biomeOS composes that into version control.

3. **Dependency Inversion**: Primals depend on abstract capabilities, not concrete implementations. Any storage provider works, not just NestGate.

4. **Message Passing**: Communication via messages over IPC, never shared state. No locks, no race conditions, inherently concurrent.

5. **Emergence Over Engineering**: Don't build a monolithic VCS - coordinate existing primals and let version control emerge. Don't build a monolithic security stack - let BearDog and Songbird compose into Tower Atomic.

---

## Document Index

### Living Documents (updated regularly)
- `ECOSYSTEM_EVOLUTION_CYCLE.md` — The water cycle model; current season assessment, convergence trajectory (v1.4.0)
- `NUCLEUS_SPRING_ALIGNMENT.md` — Canonical spring × atomic alignment matrix (Phase 58)
- `SPRING_NUCLEUS_AUDIT_MAY2026.md` — 7-dimension audit of all 8 springs, per-spring evolution blurbs
- `DOWNSTREAM_EVOLUTION_MAY2026.md` — Team communication blurb for spring teams
- `PRIMAL_REGISTRY.md` — Complete primal definitions and primitive catalogs

### Active Standards
- `BTSP_PROTOCOL_STANDARD.md` — BearDog Transport Security Protocol (Phase 3 complete, 13/13 AEAD)
- `CAPABILITY_BASED_DISCOVERY_STANDARD.md` — Runtime capability discovery
- `CAPABILITY_WIRE_STANDARD.md` — Wire format for capability calls
- `CAPABILITY_DOMAIN_REGISTRY.md` — Domain namespace registry
- `COMPOSITION_HEALTH_STANDARD.md` — Health check patterns for compositions
- `COMPOSITION_TICK_MODEL_STANDARD.md` — Tick budget model for real-time compositions
- `CROSS_SPRING_COORDINATION_STANDARD.md` — Cross-spring validation patterns
- `DEPLOYMENT_VALIDATION_STANDARD.md` — Deployment validation procedures
- `DESKTOP_NUCLEUS_DEPLOYMENT.md` — Desktop NUCLEUS deployment guide
- `ECOBIN_ARCHITECTURE_STANDARD.md` — Universal portability standard
- `GARDEN_COMPOSITION_ONRAMP.md` — Garden product composition onramp
- `NUCLEUS_TWO_TIER_CRYPTO_MODEL.md` — Two-tier crypto architecture
- `PURE_RUST_SOVEREIGN_STACK_GUIDANCE.md` — Pure Rust sovereignty guidance
- `SECRETS_AND_SEEDS_STANDARD.md` — Seed management and secret handling
- `SEMANTIC_METHOD_NAMING_STANDARD.md` — API naming conventions
- `TARGETED_GUIDESTONE_STANDARD.md` — How composed subsystems bud into portable, deployable artifacts (scope graph, data manifest, binary bundle, validation harness, provenance chain, liveSpore tracking)
- `WORKSPACE_DEPENDENCY_STANDARD.md` — Cargo workspace dependency rules
- `STANDARDS_AND_EXPECTATIONS.md` — Meta-standard: what standards are and how they evolve

### Foundation and Sediment
- `FOUNDATION_INTEGRATION_GUIDE.md` — How springs, primals, and gardens integrate with `sporeGarden/foundation`
- `SEDIMENT_LAYER_MODEL.md` — The geological model: how validated results accumulate as load-bearing layers

### Visualization and Attribution
- `SWEETGRASS_SPRING_BRAID_PATTERNS.md` — Per-spring attribution braid patterns
- `PROVENANCE_TRIO_INTEGRATION_GUIDE.md` — Provenance trio integration for springs
- `petaltongue/VISUALIZATION_INTEGRATION_GUIDE.md` — petalTongue DataBinding spec
- `petaltongue/PETALTONGUE_SPRING_SCIENCE_MAP.md` — Per-spring visualization channel mapping

### Reference
- `GLOSSARY.md` — Ecosystem terminology
- `LICENSING_AND_COPYLEFT.md` — AGPL-3.0 licensing guidance
- `PRIMAL_SPRING_GARDEN_TAXONOMY.md` — Primal/spring/garden layer taxonomy
- `UPSTREAM_CONTRIBUTIONS.md` — Contributions to upstream Rust ecosystem
- `EXTERNAL_VALIDATION_AND_UPSTREAM_STRATEGY.md` — External validation strategy

### Sovereign Hosting & Cell Membrane
- `handoffs/PROJECTNUCLEUS_SOVEREIGN_HOSTING_DNS_HANDOFF_MAY09_2026.md` — Hosting evolution, DNS metadata closure, cell membrane addendum
- `handoffs/PROJECTNUCLEUS_CELL_MEMBRANE_COMPOSITION_HANDOFF_MAY10_2026.md` — Cell membrane architecture, NUCLEUS composition patterns, neuralAPI deployment, per-team absorption targets

### Post-Interstadial
- `handoffs/PROJECTNUCLEUS_POST_INTERSTADIAL_FINDINGS_UNIBIN_HANDOFF_MAY10_2026.md` — NUCLEUS findings, spring UniBin → plasmidBin readiness, static observer, darkforest v0.2.1

### Targeted GuideStone (LTEE)
- `TARGETED_GUIDESTONE_STANDARD.md` — Standard for how composed subsystems bud into portable artifacts (budding model, 5 components, cross-platform via ecoBin/genomeBin, liveSpore tracking, data freshness protocol)
- `handoffs/LTEE_GUIDESTONE_SUBSYSTEM_HANDOFF_MAY11_2026.md` — LTEE guideStone subsystem: first Targeted GuideStone artifact (Barrick Lab), 7 science modules, 36 paper-spring assignments across 6 springs, three-tier architecture, projectNUCLEUS deployment subsystem

### Deep Debt & Upstream Handbacks
- `handoffs/PROJECTNUCLEUS_CROSS_ECOSYSTEM_AUDIT_MAY11_2026.md` — Cross-ecosystem audit findings, MethodGate parity, spring skunkBat wiring, barraCuda version skew
- `handoffs/PROJECTNUCLEUS_DEEP_DEBT_UPSTREAM_HANDBACK_MAY11_2026.md` — Upstream handback: toadStool/squirrel MethodGate, barraCuda crypto delegation, squirrel LocalProcessProvider
- `handoffs/PROJECTNUCLEUS_DEEP_DEBT_EVOLUTION_SWEEP_HANDOFF_MAY11_2026.md` — Full sweep handoff: composition patterns, NestGate priority, lessons for all teams, what's next for data/compute chains

### Subdirectories
- `handoffs/` — Cross-primal evolution handoff documents (active + 900+ archived including 19 post-interstadial closures)
- `petaltongue/` — petalTongue integration documentation
- `compute-sharing/` — Sovereign compute sharing validation
- `healthspring/` — healthSpring-specific guidance
- `airspring/` — airSpring-specific guidance
- `birdsong/` — BirdSong protocol specification
- `btsp/` — BTSP protocol details
- `genomeBin/` — genomeBin tooling
- `fossilRecord/` — Archived documents from previous consolidation waves
- `scripts/` — Utility scripts
- `templates/` — Templates for new primals/springs

### Fossil Record
Documents superseded by newer standards or absorbed into living documents are
preserved in `fossilRecord/`. Two consolidation waves:

- `fossilRecord/consolidated-apr2026/` — 56 documents from March-April 2026
- `fossilRecord/consolidated-may2026/` — 24 documents superseded by Phase 58 audit

---

## For New Primals

If you are a new primal entering the ecosystem:

1. **Read this document** to understand the ecosystem you are joining
2. **Review PRIMAL_REGISTRY.md** to see what capabilities already exist
3. **Follow UniBin standard** from day one (single binary, subcommands)
4. **Target ecoBin** (Pure Rust, zero C deps, cross-compilation)
5. **Implement IPC** following Universal IPC Standard v3.0
6. **Advertise capabilities** so biomeOS can discover and coordinate you
7. **Register your primal** in PRIMAL_REGISTRY.md with your primitives

You do not need to know about other primals. You need to know what you can do, and how to tell the ecosystem about it.

---

## Current Ecosystem State (May 2026)

- **13 primals** — all BTSP Phase 3 authenticated (full AEAD encrypted framing), zero debt
- **413 registered capability methods** (primalSpring canonical, zero drift)
- **46 cross-architecture binaries** in plasmidBin (6 target triples, Tier 1 39/39)
- **primalSpring v0.9.25** — guideStone Level 8 (absorbed), eukaryotic UniBin, 89 experiments (20 tracks), 680 tests, two-tier validation (Rust + Live), `CompositionContext` throughout, zero debt
- **8 springs** completed primordial extinction — all at eukaryotic UniBin (certification organelle, scenario registry, fossil record, zero debt/clippy)
- **12,900+ tests** across the river delta (wetSpring 1,962 · neuralSpring 1,450 · airSpring 1,327 · groundSpring 1,101 · hotSpring 1,025 · healthSpring 999 · ludoSpring 854 · primalSpring 680 + metalForge/integration/Python suites)
- **1 garden** active (esotericWebb from ludoSpring)
- **projectNUCLEUS** — 13-primal Full NUCLEUS on active gate, cell membrane architecture, deep debt evolution sweep complete (pappusCast modular, zero hardcoded paths, gate-agnostic systemd, specs reconciled). MethodGate 11/13 (toadStool/squirrel upstream handback delivered). **Next priority: NestGate content pipeline for full data/compute chains**
- **sporeGarden/foundation** — Live scientific knowledge layer: 10 domain threads, 100+ public data source anchors (NCBI/UniProt/KEGG/PDB), 36 validation targets
- **LTEE guideStone** — First Targeted GuideStone (projectNUCLEUS subsystem): 7 science modules, 36 paper-spring assignments, three-tier deployment (Python → Rust ecoBin → Primal), USB-deployable to Barrick Lab

### Current Phase: POST-INTERSTADIAL — Evolution Wave Complete

All 8 springs completed eukaryotic evolution + post-interstadial targets (May 11):
- **8/8 UniBin** — single binary per spring with `certify`/`validate`/`status`/`version`
- **8/8 Certification organelle** — guidestone layers absorbed as library modules
- **8/8 Scenario registry** — `validation/scenarios/` with `ScenarioMeta`
- **8/8 CI cross-sync** — all springs validate local methods against canonical 413
- **8/8 skunkBat Rust IPC** — all springs have Rust skunkBat modules or deploy graph nodes
- **8/8 `method.register`** — all springs wired (airSpring added v0.10.0)
- **8/8 `composition.status`** — all springs absorbing biomeOS v3.51
- **8/8 NUCLEUS workload TOMLs** — all springs have projectNUCLEUS validation workloads
- **Zero open upstream gaps** — JH-11, GAP-03/06/09/12, U1-U3, all Tier 3 items resolved

### Upcoming Horizons

**Tier 4 Rewiring** (now unblocked by JH-11):
- IPC-first defaults for all inter-primal communication
- `barracuda` as `optional = true` with feature-gated library imports
- `CompositionContext` for all cross-primal calls

**JH-5 Audit Forwarding** (now unblocked by skunkBat Phase 2):
- Cross-primal audit events → rhizoCrypt DAG + sweetGrass braid
- Springs wire skunkBat into deploy graphs (8/8 have Rust modules or graph nodes)

**NUCLEUS Sovereignty Horizons**:
- H2 Step 2b: BTSP auth for JupyterHub (replaces PAM)
- H2 Step 3a: NestGate + petalTongue content pipeline (sovereign extracellular)
- H2 Step 3b: BearDog TLS shadow run on port 8443 (upstream shipped)
- H2 Step 3c: Songbird NAT + VPS relay integration (upstream shipped)
- H2 Step 4: Sovereign DNS (knot-dns authoritative, BTSP direct resolution)
- H3: Primal-only (JupyterHub → petalTongue, GitHub → Forgejo, plasmidBin → NestGate)

**Spring → plasmidBin Deployment**:
- Springs produce UniBin release binaries → plasmidBin GitHub Releases
- projectNUCLEUS workload TOMLs reference fetched binaries for science validation
- 8/8 springs have workload TOMLs (healthSpring biosignal/microbiome/certification added May 11)

**LTEE Targeted GuideStone** (projectNUCLEUS subsystem):
- First artifact that buds from the ecosystem into a portable, self-contained deployment
- USB-deployable: 7 science modules reproducing Barrick/Lenski LTEE papers + new Anderson-QS predictions
- Three-tier: Python (universal) → Rust ecoBin (Linux) → Primal composition (NUCLEUS)
- No containers — ecoBin/genomeBin binaries, primals self-container via genomeBin if needed
- 36 paper-spring assignments seeded across 6 springs (wetSpring, neuralSpring, groundSpring, hotSpring, healthSpring, airSpring)
- liveSpore.json tracks deployment provenance; data freshness protocol for source URI re-fetch
- Standard: `TARGETED_GUIDESTONE_STANDARD.md`; subsystem handoff: `handoffs/LTEE_GUIDESTONE_SUBSYSTEM_HANDOFF_MAY11_2026.md`

### Remaining Spring Gaps (May 11 — post-interstadial push)

Previous 7 gaps resolved (May 10-11):
- ~~ludoSpring skunkBat~~ → V60 Rust IPC module
- ~~groundSpring skunkBat~~ → V130 Rust IPC module
- ~~airSpring method.register~~ → v0.10.0 `ipc/method_register.rs`
- ~~airSpring deny.toml~~ → **FALSE GAP** — workspace-root `deny.toml` exists, bans `aws-lc-sys`
- ~~healthSpring skunkBat~~ → V62 deploy graph node
- ~~hotSpring dead_code~~ → cleaned in post-interstadial push

| Spring | Gap | Severity | Owner Layer |
|--------|-----|----------|-------------|
| wetSpring | 8 open primal gaps (PG-01–PG-22, 14 closed) | Medium | L3 (spring) |
| airSpring | gS Level 2+ (ecosystem median is L4) | Low | L3 (spring) |
| neuralSpring | gS Level 3 (target L4+) | Low | L3 (spring) |
| ludoSpring | No .ipynb paper notebooks (Python baselines only) | Low | L3 (spring) |
| hotSpring | Sovereign GPU barriers (Titan V FECS, K80 PCIe) | Low | L3 (spring + coralReef) |

### Evolution Cycle Ownership

Gaps are owned by exactly one layer:
- **L1 (Primals)**: Zero open — 13/13 clean
- **L2 (primalSpring)**: Canonical registry, CompositionContext, PG-54/PG-63
- **L3 (Springs)**: Domain debt, barraCuda Tier 4, gS levels, foundation seeding
- **L4 (Products)**: NUCLEUS sovereignty horizons, composition absorption, deployment
- **L5 (Foundation)**: Thread coverage, data anchoring, provenance validation

See `primalSpring/docs/PRIMAL_GAPS.md` for the full ownership model.

See `SPRING_NUCLEUS_AUDIT_MAY2026.md` for per-spring 7-dimension audit.
See `ECOSYSTEM_EVOLUTION_CYCLE.md` for the full evolution narrative.
See `handoffs/archive/post_interstadial_may2026/` for 19 archived closure handoffs.

---

**The Watering Hole is maintained by all primals. Every primal's evolution strengthens the whole ecosystem.**
