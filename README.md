# The Watering Hole - ecoPrimals Ecosystem Guidance

**Purpose**: Authoritative project guidance for every primal in the ecoPrimals ecosystem  
**Audience**: Any primal, at any point in its evolution — and four external audiences (PIs, students, builders, compliance)  
**Last Updated**: April 28, 2026

---

## What is the Watering Hole?

The Watering Hole is the shared knowledge layer of the ecoPrimals project. Every primal - whether newly conceived or production-hardened - comes here to understand the ecosystem it belongs to: what other primals exist, what standards govern interoperability, how coordination works, and what principles guide evolution.

This is not documentation about a subdirectory. This is the living reference for the entire project.

---

## The Three Layers

The ecoPrimals ecosystem is organized into three layers with distinct roles:

| Layer | Role | Examples |
|-------|------|----------|
| **Primals** (gen2) | Self-contained Rust binaries providing domain capabilities via IPC | BearDog, Songbird, barraCuda, biomeOS |
| **Springs** (gen3) | Validation environments: compose primals, validate science, surface gaps | ludoSpring, hotSpring, wetSpring, primalSpring |
| **Gardens** (gen4) | User-facing products: compose primals into tools people use | esotericWebb, helixVision |

Primals provide. Springs validate. Gardens compose for users. Gaps flow back
through wateringHole handoffs, driving co-evolution. See
**`PRIMAL_SPRING_GARDEN_TAXONOMY.md`** for the full taxonomy and interaction
contracts, and **`ECOSYSTEM_EVOLUTION_CYCLE.md`** for the water-cycle model
that governs how capabilities flow between layers and what "season" the
ecosystem is in.

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
| **BarraCuda** | Pure Math | 826 WGSL f64 shaders (the mathematics), naga-IR optimisation (FMA fusion, DCE), precision strategy (f64/DF64/f32). Writes the math; coralReef compiles it; toadStool runs it. Budded from ToadStool (S93). v0.3.12, 4,393+ tests, 32 IPC methods, BTSP Phase 2 | Production (A+) |
| **coralReef** | Shader Compilation | Sovereign WGSL/SPIR-V/GLSL→native shader compiler. 11 GPU architectures (NVIDIA SM35–SM120 + AMD GCN5/RDNA2–RDNA4). Wire contract documented. CompilationInfo in IPC. f64 transcendental lowering (Newton-Raphson, Horner). BTSP Phase 2. ecoBin v3 deny.toml enforced. coral-gpu unified compute abstraction. VFIO dispatch + DRM nvidia-drm UVM. **coral-glowplug** boot-persistent PCIe device lifecycle broker. **coral-ember** ring-keeper with VFIO fd persistence. 4,504 tests, zero warnings | Production (Phase 10, Iter 80) |
| **Squirrel** | AI Coordination | Sovereign AI model context protocol, multi-MCP coordination, vendor-agnostic inference | Production (A++) |
| **biomeOS** | Orchestration | Composition primal: Neural API (320+ translations, 27 domains), 5 coordination patterns (Sequential, Parallel, ConditionalDag, Pipeline streaming, Continuous 60Hz), capability routing, NUCLEUS composition, PathwayLearner optimization, NDJSON streaming, bonding model, Dark Forest coordination, provenance trio wiring, BTSP security posture, cellular deploy via neural-api, tick loop event relay, graph signing (BLAKE3+Ed25519), coordination key caching | Production (v3.29, 7,814+ tests, zero C deps, Security A++ LEGENDARY) |

### Post-NUCLEUS Primals

These primals build emergent behaviors on the NUCLEUS foundation. They compose into higher-order patterns (RootPulse, Memory & Attribution Stack) coordinated by biomeOS via the Neural API. Each is functional and tested, representing the next evolutionary phase.

| Primal | Domain | Role | Status |
|--------|--------|------|--------|
| **petalTongue** | Representation | Universal UI: visual, audio, terminal, web, headless. Accessibility-first multi-modal rendering | Production (A++) |
| **rhizoCrypt** | Ephemeral Memory | Content-addressed DAG engine for working memory. Sessions, Merkle trees, real-time streaming | Production (A+) |
| **sweetGrass** | Attribution | Semantic provenance (v0.7.27). W3C PROV-O braids, fair attribution, 32 JSON-RPC methods + tarpc 0.37 + REST + UDS, UniBin, ecoBin, 1,446 tests + 56 Docker CI, 91.7% coverage, Edition 2024, BTSP crypto relay aligned with `beardog_types`, `BraidSignature` removed (Witness-only), env vars fully centralized, BraidBackend enum dispatch (zero async-trait/dyn), sled eliminated, `detect_protocol` three-way multiplexer, pedantic+nursery clean | Production |
| **LoamSpine** | Permanence | Immutable linear ledger for selective permanence. Loam Certificates for ownership and transfer | Production (A+) |
| **skunkBat** | Defense | Defensive network security: threat detection (5 types), graduated response, baseline profiling. JSON-RPC IPC server (TCP + UDS), BTSP Phase 1, Wire Standard L2/L3, capability-based discovery. 124+ tests, Edition 2024 | Production |

### Supporting Tools

| Tool | Purpose |
|------|---------|
| **sourDough** | Starter culture — the nascent primal. Absorbs converged patterns (BTSP relay, auto-detect, JSON-RPC, ecoBin) so future primals get them correct on first compile. Not dictated — extracted from what evolved primals converge on |

---

## Composed Systems

Primals achieve their greatest power through composition. These are not separate projects - they are coordination patterns that emerge when primals work together.

### Tower Atomic

**What**: BearDog (crypto) + Songbird (TLS/HTTP) = Pure Rust HTTPS

**How**: Songbird implements TLS 1.3 protocol logic. BearDog provides all cryptographic operations via JSON-RPC. Neither embeds the other. The result is a fully Pure Rust HTTPS stack with zero C dependencies.

**Used by**: Any primal that needs external network access routes through Tower Atomic.

### NUCLEUS

**What**: Exactly **12 primals** orchestrated by biomeOS (the coordinator primal). All deploy from plasmidBin as musl-static binaries.

**Layers** (atomics):
- **Tower Atomic** (electron) = BearDog + Songbird — trust boundary, mediates all inter-atomic bonding
- **Node Atomic** (proton) = Tower + ToadStool (dispatch) + barraCuda (math) + coralReef (compile)
- **Nest Atomic** (neutron) = Tower + NestGate (storage) + rhizoCrypt (DAG) + loamSpine (ledger) + sweetGrass (attribution)
- **Meta Tier** (cross-atomic) = biomeOS (coordinator) + Squirrel (AI) + petalTongue (visualization/UI)

**Desktop NUCLEUS** = Full NUCLEUS with petalTongue in `live` mode (native egui desktop window). Deploy via `tools/desktop_nucleus.sh`. See `DESKTOP_NUCLEUS_DEPLOYMENT.md`.

**What is NOT a primal**: `primalspring_primal` and `primalspring_guidestone` are dev validation artifacts. Spring binaries are Rust science validation. None are NUCLEUS composition nodes. A spring IS a composition of the 12 primals, defined by a cell graph.

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

**Specification**: `fossilRecord/UNIBIN_ARCHITECTURE_STANDARD.md` (ecoBin supersedes for new primals)
**Technical paper**: `whitePaper/technical/UNIBIN_TECHNICAL_SPECIFICATION.md`

### ecoBin - Universal Portability Standard

ecoBin = UniBin + Pure Rust + Cross-Platform. Zero C dependencies in application code, cross-compiles to any Rust target with a single `cargo build` command, platform-agnostic IPC with runtime transport discovery.

**Specification**: `ECOBIN_ARCHITECTURE_STANDARD.md`  
**Technical paper**: `whitePaper/technical/ECOBIN_TECHNICAL_SPECIFICATION.md`

### genomeBin - Autonomous Deployment Standard

genomeBin = ecoBin + deployment wrapper. Self-extracting archive that auto-detects the system, installs the correct binary, configures services, and validates health. One command installs on any system with zero manual configuration.

**Specification**: `fossilRecord/consolidated-apr2026/GENOMEBIN_ARCHITECTURE_STANDARD.md`
**See also**: `ARTIFACT_AND_PACKAGING.md` (consolidated)
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

### Universal IPC Standard (v3.1 — consolidated)

Behavioral specification for multi-transport IPC. Each primal discovers the best transport at runtime: Unix sockets on Linux/macOS, abstract sockets on Android, named pipes on Windows, TCP as universal fallback. No shared IPC crate - each primal owns its communication code.

**Specification**: `PRIMAL_IPC_PROTOCOL.md` (v3.1, consolidates prior Universal IPC v3)
**Archived**: `archive/standards_v2/UNIVERSAL_IPC_STANDARD_V3.md`

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

### primalSpring Coordination (ecosystem self-validation)

- **primalSpring + All NUCLEUS Primals**: Atomic composition testing (Tower, Node, Nest, Full NUCLEUS)
- **primalSpring + biomeOS**: Graph execution validation — all 5 coordination patterns with real primals
- **primalSpring + Provenance Trio**: RootPulse emergent system validation (commit, branch, merge, diff, federate)
- **primalSpring + Songbird Mesh**: Plasmodium formation, gate failure, capability aggregation
- **primalSpring + neuralSpring + wetSpring + hotSpring + ToadStool + NestGate**: coralForge neural object pipeline
- **primalSpring + airSpring + wetSpring + neuralSpring**: Cross-spring ecology data flow
- **primalSpring + fieldMouse + NestGate + sweetGrass**: Edge data ingestion pipeline
- **primalSpring + petalTongue**: SSE visualization pipeline
- **primalSpring + Squirrel**: AI coordination via biomeOS capability graph

### Under Development

- **Songbird + Songbird**: Cross-tower federation, multi-family routing

**Detail**: `fossilRecord/consolidated-apr2026/INTER_PRIMAL_INTERACTIONS.md`

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
- **`STANDARDS_AND_EXPECTATIONS.md`** — **Start here.** Single-document reference for all ecoPrimals standards, expectations, and conventions.
- **`GLOSSARY.md`** — Definitive terminology for the ecoPrimals ecosystem.
- **`PRIMAL_SPRING_GARDEN_TAXONOMY.md`** — **The three layers.** Primals (gen2), springs (gen3), gardens (gen4): roles, boundaries, interaction contracts.
- **`PRIMAL_REGISTRY.md`** — Complete primal definitions and primitive catalogs.

### Architecture & Binary Standards
- `ECOBIN_ARCHITECTURE_STANDARD.md` — Universal portability (Pure Rust, cross-compile)
- `ARTIFACT_AND_PACKAGING.md` — genomeBin, guideStone, validation artifacts, domain infrastructure
- `fossilRecord/UNIBIN_ARCHITECTURE_STANDARD.md` — UniBin binary structure (archived — ecoBin supersedes)

### Communication & Discovery Standards
- `PRIMAL_IPC_PROTOCOL.md` — JSON-RPC 2.0 inter-primal communication (v3.1, consolidates Universal IPC v3)
- `SEMANTIC_METHOD_NAMING_STANDARD.md` — `domain.verb` API naming conventions
- `CAPABILITY_BASED_DISCOVERY_STANDARD.md` — Discover by capability domain, not primal name
- `CAPABILITY_WIRE_STANDARD.md` — Wire format for `capabilities.list` / `identity.get` responses
- `PRIMAL_SELF_KNOWLEDGE_STANDARD.md` — Self-knowledge boundaries, socket/env conventions
- `PRIMAL_RESPONSIBILITY_MATRIX.md` — Ownership, domains, overstep boundaries
- `ECOSYSTEM_COMPLIANCE_MATRIX.md` — Per-primal compliance across 9 tiers (A–F grades)

### Security & Networking (birdsong/)
- `birdsong/BIRDSONG_PROTOCOL.md` — Encrypted UDP discovery (BirdSong)
- `birdsong/DARK_FOREST_BEACON_GENETICS_STANDARD.md` — Two-seed genetic lineage architecture
- `birdsong/SONGBIRD_TLS_TOWER_ATOMIC_INTEGRATION_GUIDE.md` — Tower Atomic TLS guide
- `btsp/BEARDOG_TECHNICAL_STACK.md` — BearDog cryptographic foundation
- `BTSP_PROTOCOL_STANDARD.md` — BTSP handshake specification (v1.0)
- `SOURDOUGH_BTSP_RELAY_PATTERN.md` — **Converged BTSP relay pattern** extracted from working primals. The standard sourDough will absorb for future primals

### Deployment & Composition (consolidated)
- **`DESKTOP_NUCLEUS_DEPLOYMENT.md`** — **Start here for desktop deployment.** 12-primal NUCLEUS from plasmidBin, petalTongue live UI, spring overlay pattern, capability reference
- `DEPLOYMENT_AND_COMPOSITION.md` — Composition patterns, BYOB schema, niche deployment, gate/fieldMouse/sporeGarden classes, gen4 bridge, workspace layout

### GPU & Compute (consolidated)
- `GPU_AND_COMPUTE_EVOLUTION.md` — Sovereign compute vision, GPU bring-up, numerical stability, fixed-function science
- `PURE_RUST_SOVEREIGN_STACK_GUIDANCE.md` — Cross-primal sovereign compute guidance

### Strategy & Licensing (consolidated)
- `LICENSING_AND_COPYLEFT.md` — Lysogeny protocol, scyBorg framework (AGPL + ORC + CC-BY-SA), symbiotic exceptions
- `UPSTREAM_CONTRIBUTIONS.md` — Standalone crates for crates.io from ecoPrimals
- `fossilRecord/NOVEL_FERMENT_TRANSCRIPT_GUIDANCE.md` — NFT architecture (archived — see `whitePaper/gen4/economics/`)
- `fossilRecord/consolidated-apr2026/SCYBORG_PROVENANCE_TRIO_GUIDANCE.md` — scyBorg licensing via trio (archived — see `PROVENANCE_TRIO_INTEGRATION_GUIDE.md`)

### Spring Patterns (consolidated)
- `SPRING_INTERACTION_PATTERNS.md` — Cross-evolution, interop, data flow, shader evolution, compute trio
- `SPRING_COORDINATION_AND_VALIDATION.md` — Handoffs, provenance trio, validation assignments
- `CROSS_SPRING_COORDINATION_STANDARD.md` — **Cross-spring RPC patterns**: shared baselines, five-way bridge, precision routing, attribution flow, inter-primal interactions

### Leverage Guides (consolidated)
- `LEVERAGE_GUIDES.md` — All 13 per-entity leverage patterns in one document

### Presentation & External Review
- **`SPRING_PRIMAL_PRESENTATION_STANDARD.md`** — Checklist for making a spring/primal independently reviewable.
- `PUBLIC_SURFACE_STANDARD.md` — GitHub metadata, PII hygiene, AI discoverability

### Secrets & Publication Hygiene
- `SECRETS_AND_SEEDS_STANDARD.md` — No static secrets in repos, seed generation patterns, build cleanliness, publication identity standard

### Deployment Validation
- `DEPLOYMENT_VALIDATION_STANDARD.md` — Runtime deployment contract: health triad, transport requirements, CLI convergence, per-primal fix paths. Driven by plasmidBin live validation.

### Temporal & Interaction Models
- `COMPOSITION_TICK_MODEL_STANDARD.md` — **Heterogeneous temporal requirements**: continuous (60Hz), convergence, event, batch, seasonal — how domains declare tick needs and biomeOS schedules them
- `INTERACTION_EVENT_TAXONOMY.md` — **Unified interaction event taxonomy**: sensor → interaction → intent layers, modality-agnostic intents, accessibility-first design
- `TOADSTOOL_SENSOR_CONTRACT.md` — `SensorEvent` IPC for petalTongue input (Layer 1 of interaction taxonomy)

### Provenance & Attribution
- `PROVENANCE_TRIO_INTEGRATION_GUIDE.md` — **Operational guide**: wiring rhizoCrypt + loamSpine + sweetGrass, commit flow, graceful degradation, known issues (PG-52), cross-spring provenance

### Garden Onramp (gen4 Products)
- `GARDEN_COMPOSITION_ONRAMP.md` — **Start here for gardens.** Binary fetch, deploy graphs, PrimalBridge, niche YAML, degradation, gap filing

### Other Standards
- `LINK_INTEGRITY_STANDARD.md` — No dead links on public surfaces
- `PRIMAL_EMOJI_STANDARD.md` — Canonical 2-emoji identities
- `WORKSPACE_DEPENDENCY_STANDARD.md` — Workspace-root dependency pins
- `fossilRecord/CONTENT_CONVERGENCE_EXPERIMENT_GUIDE.md` — sweetGrass content convergence experiment (archived)
- `fossilRecord/CONTENT_SIMILARITY_EXPERIMENT_GUIDE.md` — sweetGrass content similarity experiment (archived)

### Ecosystem Evolution
- `ECOSYSTEM_EVOLUTION_CYCLE.md` — **The water cycle**: how capabilities flow from primals → primalSpring → springs → gardens, seasonal phases, acceleration effect, current composition elevation priorities

### Spring Composition & Evolution
- `SPRING_COMPOSITION_PATTERNS.md` — **Standardized patterns** extracted from all 7 springs: method normalization, capability registration, tiered discovery, graph validation, niche identity
- `NUCLEUS_SPRING_ALIGNMENT.md` — **Spring × Atomic alignment matrix**, composition readiness status, neuralSpring AI provider role, cross-pollination network
- `SPRING_AUDIT_PROMPT.md` — **Canonical audit prompt** for spinning up spring sessions (includes primal composition validation layer)
- `airspring/AIRSPRING_COMPOSITION_GUIDANCE.md` — How airSpring composes
- `healthspring/HEALTHSPRING_COMPOSITION_GUIDANCE.md` — How healthSpring composes

### BTSP Convergence
- `SOURDOUGH_BTSP_RELAY_PATTERN.md` — **Start here for BTSP.** The relay pattern extracted from 9 converged primals
- `BTSP_PROTOCOL_STANDARD.md` — Full protocol specification (v1.0)
- `fossilRecord/UPSTREAM_GAP_STATUS_APR20_2026.md` — Upstream gap tracker (biomeOS v3.29 absorbed, April 28)
- `handoffs/archive/BTSP_WIRE_CONVERGENCE_APR24_2026.md` — Per-primal convergence status and scoreboard

### Interactive Composition
- `LIVE_GUI_COMPOSITION_PATTERN.md` — petalTongue live mode interaction loop (scene → render → input → loop)
- `primalSpring/tools/nucleus_composition_lib.sh` — 41-function reusable NUCLEUS wiring library (+ biomeOS integration helpers)
- `primalSpring/tools/desktop_nucleus.sh` — Desktop NUCLEUS launcher (12-primal deployment)
- `primalSpring/tools/composition_nucleus.sh` — Parameterized NUCLEUS launcher (shell-managed)
- `primalSpring/tools/composition_template.sh` — Minimal starter skeleton for spring compositions
- `primalSpring/graphs/cells/nucleus_desktop_cell.toml` — Canonical 12-primal desktop cell graph
- `primalSpring/graphs/cells/nucleus_desktop_overlay_template.toml` — Template for spring domain overlays
- `primalSpring/wateringHole/DOWNSTREAM_COMPOSITION_EXPLORER_GUIDE.md` — Per-spring exploration lanes

### Handoffs
- `handoffs/*.md` — 27 active session handoffs (April 26–28, 2026)
- `handoffs/archive/` — Fossil record (663 archived handoffs)

### Fossil Record
- `fossilRecord/consolidated-apr2026/` — 49 original documents consolidated April 4, 2026
- `fossilRecord/petaltongue-jan2026/` — Historical petaltongue docs from January 2026

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

The `publicRelease/` documents in `whitePaper/attsi/non-anon/contact/publicRelease/`
make ecosystem-wide claims. Each spring and primal must ensure its own presentation
supports those claims.

---

**The Watering Hole is maintained by all primals. Every primal's evolution strengthens the whole ecosystem.**
