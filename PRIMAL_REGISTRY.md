# Primal Registry - ecoPrimals Ecosystem

**Purpose**: Authoritative catalog of every primal, its primitives, its domain, and its role in the ecosystem  
**Audience**: Any primal seeking to understand what capabilities exist  
**Last Updated**: February 25, 2026

---

## How to Read This Document

Each primal entry below includes:

- **Domain**: What problem space this primal owns
- **Role**: What this primal does for the ecosystem
- **Primitives**: The atomic capabilities this primal provides
- **Phase**: Foundation (forms the NUCLEUS deployment architecture) or Post-NUCLEUS (builds emergent behaviors on the foundation)
- **Status**: Current production readiness
- **Participates In**: What composed systems this primal contributes to

---

## Foundation Primals

These primals form the NUCLEUS deployment architecture. They are production-ready, extensively tested, and required for core ecosystem function. This tier includes all original Phase 1 primals plus biomeOS, which has matured to foundation status through its role as the ecosystem orchestrator.

### BearDog - Cryptography Primal

**Domain**: Cryptographic operations and genetic lineage  
**Phase**: Foundation  
**Status**: Production Ready (A+ LEGENDARY, 99/100)

**Role**: BearDog is the cryptographic foundation of the ecosystem. Every signing operation, every encryption, every hash, every key exchange in the ecosystem flows through BearDog's primitives. It also manages genetic lineage - the family seed system that enables auto-trust between primals.

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **Signatures** | Ed25519, ECDSA (P-256, P-384), RSA (PKCS#1 v1.5, PSS) |
| **Key Exchange** | X25519, ECDHE (P-256, P-384) |
| **AEAD Encryption** | ChaCha20-Poly1305, AES-128-GCM, AES-256-GCM |
| **Hashing** | BLAKE3, SHA-256, SHA-384, SHA-512, HMAC |
| **Key Derivation** | HKDF (TLS 1.3), TLS 1.2 PRF, PBKDF2, Argon2id |
| **Certificates** | X.509 generation, parsing, validation |
| **Genetic Crypto** | Lineage-based key derivation, beacon seeds, family seed management |
| **Dark Forest** | Challenge-response federation protocol |

**IPC Methods**: 72 JSON-RPC methods (69 crypto + 3 introspection)  
**Dependencies**: Zero C dependencies. 100% RustCrypto suite.

**Participates In**: Tower Atomic (with Songbird), NUCLEUS, RootPulse, BirdSong encryption, Dark Forest Federation

---

### Songbird - Network Primal

**Domain**: Network orchestration, discovery, and federation  
**Phase**: Foundation  
**Status**: Production Ready (S+, 100% BearDog delegation + Pure Rust Tor)

**Role**: Songbird is the nervous system of the ecosystem. It handles all network communication - TLS, discovery, NAT traversal, and federation. It is the only primal that speaks to the external network directly; all others route through Songbird when external connectivity is needed.

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **TLS** | TLS 1.3 (RFC 8446), TLS 1.2 fallback, Pure Rust via BearDog crypto delegation |
| **Discovery** | BirdSong encrypted UDP multicast, mDNS/DNS-SD, capability-based 6-layer strategy |
| **NAT Traversal** | Pure Rust STUN server (RFC 5389), relay server with lineage-based auth |
| **Federation** | Zero-trust progressive escalation, cross-tower routing |
| **Dark Forest** | Zero metadata leakage discovery, encrypted beacons |
| **Transport** | Multi-transport IPC (Unix sockets, abstract sockets, TCP) |

**Participates In**: Tower Atomic (with BearDog), NUCLEUS, RootPulse (discovery/federation), BirdSong protocol

---

### NestGate - Data Primal

**Domain**: Storage and content-addressed data management  
**Phase**: Foundation  
**Status**: Production Ready (A++ TOP 1%, 99%)

**Role**: NestGate provides all data persistence for the ecosystem. Content-addressed storage means data is identified by its hash, not its location. NestGate handles blob storage, tree structures, metadata, and quota management. It also provides capability-based service discovery.

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **Storage** | `storage.put`, `storage.get`, `storage.delete`, `storage.list`, `storage.exists`, `storage.metadata`, `storage.copy`, `storage.move`, `storage.quota` |
| **Discovery** | `discovery.announce`, `discovery.query`, `discovery.list`, `discovery.metadata`, `discovery.capabilities` |
| **Metadata** | `metadata.store`, `metadata.retrieve`, `metadata.update`, `metadata.search` |
| **Health** | `health.check`, `health.metrics`, `health.ready`, `health.alive` |

**Storage Backends**: Filesystem, ZFS, object storage  
**Content Addressing**: BLAKE3 hashes  
**Optimization**: Entropy-based compression routing, zero-copy I/O with SIMD

**Participates In**: NUCLEUS, RootPulse (content storage), Nest Atomic (with Tower Atomic)

---

### Squirrel - AI Primal

**Domain**: AI model coordination and inference  
**Phase**: Foundation  
**Status**: Production Hardened (A++, 98/100)

**Role**: Squirrel provides sovereign AI capabilities through the Model Context Protocol (MCP). It routes AI tasks to appropriate models (local or remote), manages context windows, and coordinates multi-model workflows - all without compile-time coupling to any AI vendor.

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **Inference** | Model inference routing, multi-provider support (OpenAI, Anthropic, Ollama, local) |
| **Context** | Advanced context window management, memory optimization |
| **Task Routing** | Intelligent routing based on task requirements and model capabilities |
| **MCP** | Multi-MCP coordination, sovereign operation |
| **Integration** | Vendor-agnostic AI, zero compile-time coupling |

**Architecture**: TRUE PRIMAL - runtime discovery, isomorphic IPC, multi-protocol (JSON-RPC + tarpc)

**Participates In**: Full NUCLEUS (all atomics + AI), RootPulse (intelligent merge resolution)

---

### ToadStool - Compute Primal

**Domain**: Universal compute orchestration  
**Phase**: Foundation  
**Status**: Production Ready (A++ GOLD STANDARD) — 2,440+ barracuda tests, 21,599+ workspace tests, 0 clippy warnings, sovereign compiler operational

**Role**: ToadStool enables isomorphic workload execution across any compute substrate - CPU, GPU, neuromorphic hardware, WebAssembly, containers, and edge devices. Its BarraCuda library (Barrier-free Rust-Abstracted Computationally Unified Dimensionalized Algebra) provides 687 WGSL f64 shaders (zero orphans) as the **primary math implementation**. All math originates as WGSL shaders at f64 precision -- barracuda does not care about hardware. ToadStool routes to the best substrate at runtime. CPU reference implementations exist only for `#[cfg(test)]` validation. f64 transcendentals (exp, log, pow, sin, cos, gamma, erf) are fully covered by `compile_shader_f64()` polyfill pipeline on every GPU.

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **BarraCuda Core** | 687 WGSL f64 shaders (shader-first, zero CPU-only math): matmul, relu, softmax, gelu, layer_norm, transpose, elementwise, reduce, broadcast |
| **Linear Algebra** | GPU-dispatched: solve, cholesky, QR, SVD, LU, sparse eigensolve (Lanczos), GEMM f64, matrix inverse |
| **Scientific Computing** | Crank-Nicolson PDE, Richards equation, all MD forces GPU (Coulomb, Morse, Born-Mayer, Yukawa), PPPM electrostatics (GPU FFT), HFB nuclear physics (11 shaders) |
| **Lattice QCD** | 14 GPU shaders + host orchestration: Wilson action, HMC leapfrog, Dirac, CG solver, pseudofermion, polyakov loop, kinetic energy |
| **Special Functions** | GPU: Bessel (J0/J1/Y0/Y1), Laguerre, Hermite, Legendre, spherical harmonics, digamma, beta, gamma, erf |
| **Statistics** | GPU: variance, covariance, correlation, kinetic energy, fused map-reduce, weighted dot, cosine similarity |
| **MD Observables** | GPU: RDF (atomic histogram), MSD, VACF, stress virial, velocity-Verlet integrator, Berendsen thermostat |
| **Surrogates** | RBF surrogate (GPU cdist + GPU solve), adaptive sampling, sparsity sampling |
| **Bioinformatics** | 25 GPU bio ops: kmer histogram, taxonomy FC, UniFrac, pairwise L2, multi-objective fitness, swarm NN, hill gate, batch fitness, ANI, random forest inference |
| **CNN** | conv2d, batch_norm, max_pool2d, avg_pool2d, elementwise (CPU + WGSL) |
| **Attention** | Scaled Dot-Product, Multi-Head, Causal, Sparse, Rotary, Cross, ALiBi |
| **Training** | Focal Loss, Contrastive Loss, Huber Loss, BCE, Hinge, KL Divergence, Lovasz, MAE, Smooth L1 |
| **Optimizers** | SGD, Adam, AdaGrad, RMSprop, AdaDelta |
| **IoT/Streaming** | Moving window statistics (mean/var/min/max), batched ODE RK4 |
| **Neuromorphic** | Pure Rust Akida driver (160 NPUs detected), ESN export/import weights |
| **f64 Polyfill** | `compile_shader_f64()`: auto-injects software transcendentals (exp, log, pow, sin, cos, tan, gamma, erf) on drivers without native f64 support (NVK, RADV, Ada) |
| **Sovereign Compiler** | naga-IR optimizer: FMA fusion (~1.3x), dead expression elimination, SPIR-V passthrough — end-to-end Rust GPU compilation |
| **Hybrid FP64** | `Fp64Strategy` auto-selects native f64 (compute GPUs) vs DF64 double-float f32-pair (~14 digits on FP32 cores). 12 DF64 WGSL files. |
| **Runtimes** | Native, WASM, Python, Container, GPU, NPU, Edge (Linux, RPi, ESP32, Arduino) |

**Four-Spring ingestion**: hotSpring (11 HFB physics + heat current), neuralSpring (4 bio ML + PRNG, all f64), wetSpring (5 ODE f64), airSpring (Richards PDE + moving window). All 13 f32 shaders evolved to f64 (S49). **Deep debt resolved**: S62-63 systematically eliminated dead code, refactored large files (coulomb_f64 -39%, morse_f64 -16%), wired unused implementations.

**Participates In**: Node Atomic (with Tower Atomic), NUCLEUS, BarraCuda compute layer

---

### biomeOS - Ecosystem Orchestrator

**Domain**: Primal orchestration and ecosystem coordination  
**Phase**: Foundation  
**Status**: Production Ready (A, Security A++ LEGENDARY)

**Role**: biomeOS is the orchestration substrate. It discovers primals by their capabilities at runtime, routes requests semantically via the Neural API, composes primals into atomics (Tower, Node, Nest, NUCLEUS), and coordinates higher-order patterns like RootPulse. It is the composer - primals are the instruments.

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **Neural API** | Semantic routing (`capability.call`), pathway learning, bidirectional feedback |
| **Atomics** | Tower Atomic, Node Atomic, Nest Atomic, Full NUCLEUS composition |
| **Discovery** | Runtime capability matching, primal health monitoring |
| **Deployment** | genomeBin management, graph-based deployment, cross-device federation |
| **Security** | Dark Forest integration (A++ LEGENDARY), genetic model coordination |
| **IPC** | Universal IPC v3.0, multi-transport support |

**Participates In**: Coordinates all composed systems (RootPulse, Tower Atomic, NUCLEUS, federation). biomeOS is to the ecosystem what the nervous system is to an organism.

---

## Post-NUCLEUS Primals

These primals build emergent behaviors on the NUCLEUS foundation. They compose into higher-order patterns (RootPulse, Memory & Attribution Stack) coordinated by biomeOS via the Neural API. Each is functional, tested, and has its own showcase demonstrations. They represent the next evolutionary phase - building emergent capabilities on the foundation that the primals above provide.

### petalTongue - Representation Primal

**Domain**: Universal multi-modal user interface  
**Phase**: Post-NUCLEUS  
**Status**: Production Ready (A++, 99/100)

**Role**: petalTongue renders ecosystem state across every sensory modality. Sighted users see graph visualizations. Blind users hear sonified health data. Terminal users get rich TUI. Web users get a dashboard. The same primal adapts to whatever representation capability is available.

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **Visual Modes** | Desktop GUI (egui/wayland), Terminal UI (ratatui), Web server (axum), Headless rendering (SVG/PNG) |
| **Audio** | Sonification engine: 5 instruments, health-to-pitch mapping, position-to-stereo panning |
| **Layout** | 4 graph layout algorithms, pan/zoom/select |
| **Integration** | Live primal discovery via Songbird, biomeOS SSE event subscription |
| **Configuration** | Environment-driven (ENV > File > Defaults), TCP fallback IPC |

**UniBin Modes**: `ui`, `tui`, `web`, `headless`, `status`

**Participates In**: biomeOS ecosystem visualization, real-time health monitoring display

---

### rhizoCrypt - Ephemeral Memory Primal

**Domain**: Content-addressed DAG engine for working memory  
**Phase**: Post-NUCLEUS  
**Status**: Production Ready (A+, 96/100, 509/509 tests, 87%+ coverage)

**Role**: rhizoCrypt provides the ephemeral workspace layer - a git-like DAG of content-addressed events that serves as working memory. Sessions are scoped, lock-free, and real-time. Data lives here temporarily until it is either discarded or "dehydrated" (committed) to LoamSpine for permanence.

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **Vertex Operations** | Content-addressed events with BLAKE3 hashing, multi-parent DAG links, nanosecond timestamps |
| **Session Management** | Scoped workspaces with full lifecycle (active, committed, discarded) |
| **Merkle Trees** | Content verification, inclusion proofs, root computation |
| **Dehydration** | Temporal collapse: commit session state to LoamSpine |
| **Slice Semantics** | 6 query modes for traversing the DAG |
| **Attribution** | Embedded sweetGrass metadata, BearDog DID agent identity |

**Participates In**: RootPulse (ephemeral workspace layer), Memory & Attribution stack

---

### sweetGrass - Attribution Primal

**Domain**: Semantic provenance and attribution  
**Phase**: Post-NUCLEUS  
**Status**: Production Ready (A+, 98/100, 381/381 tests, 86% coverage)

**Role**: sweetGrass tracks who created what, when, and how. It creates "braids" - content-addressable provenance records compliant with W3C PROV-O - and calculates fair attribution shares across contributors. Privacy controls are built in (GDPR-inspired, 5 levels).

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **Braids** | Content-addressable provenance records, W3C PROV-O / JSON-LD compliant |
| **Attribution Engine** | 12 role types (Creator, Contributor, Reviewer...), derivation chain analysis, time decay, recursive propagation |
| **Provenance Graph** | Complete data lineage tracking, DAG queries, "where did this come from?" |
| **Privacy** | 5 privacy levels, GDPR-inspired data subject rights |
| **Storage** | Memory, Sled, PostgreSQL backends |
| **Export** | W3C PROV-O JSON-LD standard, ~88% compression with session dedup + zstd |

**Participates In**: RootPulse (attribution layer), Memory & Attribution stack, Loam Certificate provenance

---

### LoamSpine - Permanence Primal

**Domain**: Immutable linear ledger for selective permanence  
**Phase**: Post-NUCLEUS  
**Status**: Production Ready (A+, 98/100, 416/416 tests, 77.68% coverage)

**Role**: LoamSpine is the fossil record. Where rhizoCrypt is ephemeral and fast, LoamSpine is permanent and provable. Important events are deliberately committed ("dehydrated") from rhizoCrypt into LoamSpine's append-only ledger. Most data should be temporary; only what matters should be permanent.

**Primitives (Specified)**:

| Category | Primitives |
|----------|-----------|
| **LoamEntry** | Append-only entries with sequential index, previous hash chain, cryptographic signatures |
| **Spine Structure** | Sovereign ledgers (personal, professional, community, public) |
| **Loam Certificates** | Memory-bound objects: digital game keys, credentials, property deeds, ownership transfer, lending |
| **Replication** | Federated sync (peers, federation, archive) |
| **Proofs** | Inclusion proofs, certificate proofs, recursive spine stacking |

**Participates In**: RootPulse (permanence layer), Memory & Attribution stack, Loam Certificate Layer

---

### skunkBat - Defense Primal

**Domain**: Defensive network security  
**Phase**: Post-NUCLEUS  
**Status**: Production Ready (87.37% coverage, core modules 90-100%)

**Role**: skunkBat protects sovereign computing environments through threat detection and graduated response. It is strictly defensive - reconnaissance, not surveillance. It learns your network's normal baseline and detects deviations. It never inspects content, only metadata.

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **Threat Detection** | Genetic (unknown lineage), Topology (layer-hopping), Behavioral (statistical anomalies), Intrusion (attack signatures), Resource (DoS, exhaustion) |
| **Defense Actions** | Monitor + Alert (low), Quarantine (isolate), Block (deny, operator decision) |
| **Baseline** | Statistical profiling of normal network patterns |
| **Reconnaissance** | Network intelligence (metadata-only, no content) |
| **Integration** | Trait-based ecosystem integration (BearDog, ToadStool, Songbird, NestGate) |

**Principles**: Defensive only, user authority required, privacy by architecture

**Participates In**: Ecosystem security layer, Dark Forest defense coordination

---

## The Memory & Attribution Stack

rhizoCrypt, LoamSpine, and sweetGrass form a unified stack with three semantic layers over one DAG engine:

```
Application Layer (Gaming, Scientific, Collaboration)
        |
  sweetGrass (Attribution) - Query & export layer
        |
   LoamSpine (Permanence) - Selective immutable history
        |
  rhizoCrypt (Core DAG) - Content-addressed working memory
```

**rhizoCrypt** is the engine. **LoamSpine** adds permanence semantics. **sweetGrass** adds attribution semantics. biomeOS coordinates them via the Neural API into RootPulse.

---

## Primal Coordination Summary

### Who Coordinates Whom

```
biomeOS (orchestrator)
  |
  +-- Neural API routes capability.call requests
  |
  +-- Composes atomics:
  |     Tower Atomic  = BearDog + Songbird
  |     Node Atomic   = Tower + ToadStool
  |     Nest Atomic   = Tower + NestGate
  |     Full NUCLEUS  = All + Squirrel
  |
  +-- Coordinates RootPulse:
  |     rhizoCrypt (ephemeral) + LoamSpine (permanent)
  |     + NestGate (storage) + BearDog (signing)
  |     + sweetGrass (attribution) + Songbird (discovery)
  |
  +-- Feeds petalTongue:
        Real-time SSE events for ecosystem visualization
```

### No Primal Knows About Another

BearDog doesn't know Songbird exists. rhizoCrypt doesn't know about LoamSpine. sweetGrass doesn't know about RootPulse. Each primal advertises its capabilities, and biomeOS discovers and coordinates them at runtime. This is fundamental - complexity through coordination, not through coupling.

---

## Domain Validation Primals (Springs)

These primals validate the ecoPrimals compute pipeline end-to-end by reproducing published science in specific domains. Each Spring follows Paper → Python → Rust (BarraCuda CPU) → GPU (ToadStool shaders) → metalForge (mixed hardware) → biomeOS (NUCLEUS deployment). Springs consume ToadStool/BarraCuda compute and contribute domain-specific fixes, shaders, and absorption candidates back upstream.

### airSpring - Ecological & Agricultural Sciences

**Domain**: Precision agriculture, irrigation science, environmental systems
**Phase**: Domain Validation
**Status**: v0.5.2 — 584 lib + 31 forge tests, 55 binaries, 0 clippy warnings

**Role**: airSpring validates agricultural computational methods — FAO-56 ET₀, soil sensor calibration, IoT irrigation, water balance, dual crop coefficient, Richards equation, yield response, and ecological diversity — proving the full ecoPrimals pipeline from paper reproduction to GPU-accelerated sovereign computation on consumer hardware.

**Capabilities**:

| Category | Details |
|----------|---------|
| **Experiments** | 45 complete: FAO-56, soil, IoT, WB, dual Kc, Richards, biochar, yield, CW2D, 7 ET₀ methods, GDD, pedotransfer, ensemble, bias correction, parity, dispatch, Anderson coupling |
| **ET₀ Methods** | Penman-Monteith, Priestley-Taylor, Hargreaves-Samani, Makkink, Turc, Hamon, Thornthwaite |
| **Python Baselines** | 1109/1109 PASS against digitized paper benchmarks |
| **Rust Validation** | 584 lib + 31 forge tests, 55 binaries, 75/75 cross-validation (tol=1e-5) |
| **Real Data** | 15,300 station-days Open-Meteo ERA5 (100 Michigan stations), 80yr download active |
| **GPU Orchestrators** | 11 Tier A + 4 Tier B wired (ops 0-8), seasonal pipeline, atlas stream, MC ET₀ |
| **Seasonal Pipeline** | ET₀→Kc→WB→Yield chained, 73/73 PASS (12 stations, 4800 crop-year results) |
| **metalForge** | 18 workloads, 29/29 cross-system routing (GPU+NPU+CPU) |
| **NPU** | AKD1000 live (3 experiments, 95/95 checks, ~48µs inference) |
| **CPU Benchmark** | 25.9× faster than Python (8/8 parity, geometric mean) |
| **GPU Live** | Titan V 24/24 PASS (0.04% seasonal parity), RTX 4070 validated |

**ToadStool Contributions**:
- TS-001: `pow_f64` fractional exponent fix (discovered during ET₀ atmospheric pressure calc)
- TS-003: `acos` precision boundary fix
- TS-004: reduce buffer N≥1024 fix
- Richards PDE solver absorbed upstream (S40)
- Stats metrics absorbed upstream (S64)

**Participates In**: Node Atomic (via ToadStool compute), Nest Atomic (via NestGate data), NUCLEUS (via biomeOS deployment graphs), metalForge cross-system dispatch

---

## Registering a New Primal

To add a new primal to this registry:

1. Define your domain (what problem space you own)
2. Catalog your primitives (every atomic capability you provide)
3. Identify your IPC methods
4. Declare what composed systems you could participate in
5. Add your entry to this document following the format above
6. Ensure you follow UniBin and ecoBin standards

---

**This registry is the source of truth for what exists in the ecoPrimals ecosystem.**
