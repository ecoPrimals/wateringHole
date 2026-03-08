# Primal Registry - ecoPrimals Ecosystem

**Purpose**: Authoritative catalog of every primal, its primitives, its domain, and its role in the ecosystem  
**Audience**: Any primal seeking to understand what capabilities exist  
**Last Updated**: March 8, 2026

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

### ToadStool - Hardware Infrastructure Primal

**Domain**: Hardware discovery, capability probing, and compute orchestration  
**Phase**: Foundation  
**Status**: Production Ready (A++ GOLD STANDARD) — 19,140+ workspace tests, 0 clippy warnings, 0 failures, 65+ JSON-RPC methods (dynamically built), capability-based discovery, coralReef shader proxy, cross-spring provenance tracking, all files < 1000 lines

**Role**: ToadStool is the hardware infrastructure primal. It discovers GPUs, NPUs, CPUs at runtime via sysfs/PCIe. It exposes compute substrates to the ecosystem via JSON-RPC 2.0 + tarpc IPC over Unix sockets. GPU job queue with cross-gate routing. Ollama model lifecycle management. Distributed workload dispatch across machines. Cloud cost estimation, compliance validation, and federation. Shader compilation proxy to coralReef with capability-based discovery and naga fallback. Cross-spring provenance tracking via `toadstool.provenance` method. BarraCuda (math dispatch) is a separate primal that consumes ToadStool's hardware capabilities via IPC.

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **GPU Discovery** | Multi-adapter selection (`TOADSTOOL_GPU_ADAPTER`), `GpuAdapterInfo` (driver, f64, workgroups, buffer limits), cross-vendor (NVIDIA/AMD/Intel via WGPU/Vulkan) |
| **NPU Discovery** | Generic `NpuDispatch` trait, `AkidaNpuDispatch` adapter (VFIO/kernel/mmap), `NpuParameterController` trait |
| **CPU Discovery** | `/proc/cpuinfo` parsing, cache hierarchy (L2/L3/Infinity Cache), SIMD capability probing |
| **Hardware Transport** | Display (DRM/KMS), Capture (V4L2), Serial (USB) — frame protocol + `TransportRouter` |
| **GPU Job Queue** | Submit/status/result/cancel/list, cross-gate routing across machines |
| **Precision Routing** | `PrecisionRoutingAdvice` (F64Native, F64NativeNoSharedMem, Df64Only, F32Only), `precision_routing()` |
| **Sovereign Pipeline** | `HardwareFingerprint`, `is_sovereign_capable()`, `safe_allocation_limit` (NVK PTE guard), 12-variant `SubstrateCapabilityKind` |
| **Distributed** | Cross-gate GPU routing, cloud cost estimation, compliance validation, federation |
| **Ollama Integration** | Model lifecycle (list/load/inference/unload) via JSON-RPC |
| **Runtimes** | Native, WASM (wasmi), Python, Container (BYOB), GPU, NPU, Edge (Linux, RPi, ESP32, Arduino) |
| **Shader Proxy** | `shader.compile.*` proxy to coralReef with capability-based discovery, naga fallback |
| **Provenance** | `toadstool.provenance` — cross-spring flow matrix (17+ flows across 5 springs, 9 domains) |
| **IPC** | 65+ JSON-RPC 2.0 methods (semantic naming), tarpc typed RPC, Unix socket standard |

**Key principles**: Capability-based discovery (self-knowledge only), ecoBin compliant (pure Rust core), zero hardcoded primal names/ports, all unsafe blocks documented with `// SAFETY:`. Rust 1.82+ MSRV.

**Participates In**: Node Atomic (with Tower Atomic), NUCLEUS, serves hardware capabilities to BarraCuda

---

### BarraCuda - Math Primal

**Domain**: GPU math dispatch, shaders, and precision strategy  
**Phase**: Foundation  
**Status**: Production Ready (A+) — 3,100+ tests, 786 WGSL shaders, 1,055 Rust source files, zero unsafe, zero clippy warnings, 27-shader cross-spring provenance registry, PrecisionRoutingAdvice, BatchedOdeRK45F64, DF64 reduce shaders for Hybrid devices, `fused_ops_healthy()` canary, `service` subcommand (genomeBin), `bytes::Bytes` zero-copy I/O, thread-local GPU test throttling; budded from ToadStool (S93), separate primal at `ecoPrimals/barraCuda/`

**Role**: BarraCuda (Barrier-free Rust-Abstracted Computationally Unified Dimensionalized Algebra) is the math engine. All math originates as WGSL shaders at f64 precision. BarraCuda does not care about hardware — ToadStool provides hardware capabilities via IPC. f64 transcendentals fully covered by `compile_shader_f64()` polyfill pipeline. Sovereign naga-IR compiler (FMA fusion, DCE).

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **Core** | 786 WGSL f64 shaders: matmul, relu, softmax, gelu, layer_norm, transpose, elementwise, reduce (incl. DF64 variants), broadcast |
| **Linear Algebra** | solve, cholesky, QR, SVD, LU, sparse eigensolve (Lanczos), GEMM f64, matrix inverse |
| **Scientific Computing** | Crank-Nicolson PDE, Richards equation, MD forces (Coulomb, Morse, Born-Mayer, Yukawa), PPPM electrostatics, HFB nuclear physics |
| **Lattice QCD** | 14 GPU shaders + host: Wilson action, HMC leapfrog, Dirac, CG solver, pseudofermion, polyakov loop |
| **Special Functions** | Bessel, Laguerre, Hermite, Legendre, spherical harmonics, digamma, beta, gamma, erf |
| **ML** | Attention (7 variants), Training losses (10 types), Optimizers (5 types), CNN ops |
| **Bioinformatics** | 31 GPU bio ops: kmer histogram, taxonomy FC, UniFrac, ANI, random forest inference, HMM, Dada2, Gillespie, Wright-Fisher |
| **f64 Polyfill** | `compile_shader_f64()`: auto-injects software transcendentals on drivers without native f64 |
| **Sovereign Compiler** | naga-IR optimizer: FMA fusion (~1.3x), dead expression elimination, SPIR-V passthrough |
| **Hybrid FP64** | `Fp64Strategy` auto-selects native f64 vs DF64 double-float (~14 digits on FP32 cores) |

**Five-Spring ingestion**: hotSpring (lattice QCD, HFB, spectral), neuralSpring (bio ML), wetSpring (ODE), airSpring (Richards PDE), groundSpring (sensor noise). All f32→f64 (S49).

**Participates In**: Node Atomic (via ToadStool), NUCLEUS compute layer

---

### coralReef - Shader Compiler Primal

**Domain**: GPU shader compilation — WGSL/SPIR-V to native GPU binary  
**Phase**: Foundation  
**Status**: Phase 10 Iteration 14 (A+) — 991 tests (960 passing, 31 ignored), Statement::Switch lowering (chain-of-comparisons), NV `NvMappedRegion` RAII (unsafe reduction: `ptr::copy_nonoverlapping` → safe `copy_from_slice`), `clock_monotonic_ns` consolidation, 14 lower_copy_swap diagnostic panics with src/dst context, `Fp64Strategy` enum, built-in df64 preamble, AMD E2E verified on RX 6950 XT, NVIDIA E2E fully wired (awaiting Titan V / RTX 3090 validation), zero clippy warnings, zero production `unwrap()`/`todo!()`, `#[deny(unsafe_code)]` on 6/8 crates, AGPL-3.0-only

**Role**: coralReef is the sovereign Rust GPU shader compiler. It compiles WGSL and SPIR-V compute shaders to native GPU binaries with full f64 transcendental support. NVIDIA backend complete (SM70-SM89). AMD backend operational (RDNA2/GFX1030) with E2E dispatch verified — WGSL compile, PM4 dispatch, GPU execution, host readback. coralDriver provides userspace GPU dispatch via DRM ioctl. coralGpu unifies compilation and dispatch into a single API. Zero C dependencies, zero vendor lock-in, zero FFI. Part of the sovereign compute pipeline: barraCuda generates WGSL shaders, toadStool proxies `shader.compile.*` requests, coralReef compiles to native binary, coralDriver dispatches on hardware.

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **IPC** | `shader.compile.spirv`, `shader.compile.wgsl`, `shader.compile.status`, `shader.compile.capabilities` — JSON-RPC 2.0 + tarpc (TCP/Unix socket), zero-copy `bytes::Bytes` payloads, differentiated error codes |
| **NVIDIA Backend** | SM70-SM89 (Volta through Ada), SASS binary output, f64 transcendentals via Newton-Raphson (sqrt, rcp, exp2, log2, sin, cos) |
| **AMD Backend** | RDNA2 GFX1030, native `v_fma_f64`/`v_sqrt_f64`/`v_rcp_f64`, 1446 ISA opcodes (Rust-generated from AMD XML) |
| **Compiler Core** | naga frontend, SSA IR, copy propagation, DCE, register allocation, vendor-specific legalization and encoding |
| **coralDriver** | AMD DRM ioctl (GEM, PM4, BO list, CS submit, fence sync) — **E2E verified on RX 6950 XT**, NVIDIA nouveau (channel, GEM, pushbuf, QMD) — pure Rust via libc |
| **coralGpu** | Unified compile + dispatch API — vendor-agnostic `GpuContext` |
| **f64 Lowering** | Full f64 transcendental suite: sqrt, rcp, exp2, log2, sin, cos, exp, log, pow — NVIDIA (DFMA software) + AMD (native hardware) |
| **14/27 Cross-Spring Shaders** | Compiles shaders from hotSpring, groundSpring, neuralSpring, wetSpring, airSpring to native SM70 SASS |
| **AMD E2E Pipeline** | WGSL → compile → PM4 dispatch → GPU execution → host readback — verified on RX 6950 XT (RDNA2 GFX1030) |

**Participates In**: Sovereign Compute Pipeline (barraCuda → toadStool → coralReef → native binary → coralDriver → hardware)

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
**Status**: v0.7.0 — 827 lib + 186 forge tests (27 GPU fail: upstream wgpu 28 NVK driver issue), 86 binaries, 78 experiments, 381/381 validation, 146/146 evolution, 20.6× CPU speedup (24/24 parity), 0 clippy warnings (pedantic+nursery), zero unsafe code, zero mocks in production, AGPL-3.0-or-later, standalone barraCuda 0.3.3 (wgpu 28, DF64 precision tier, 3/6 local ops absorbed upstream, fused Welford + fused Pearson wired)

**Role**: airSpring validates agricultural computational methods — FAO-56 ET₀ (8 methods), soil sensor calibration, IoT irrigation, water balance, dual crop coefficient, Richards equation, yield response, ecological diversity, immunological Anderson coupling, and SCS-CN/Green-Ampt hydrology — proving the full ecoPrimals pipeline from paper reproduction to GPU-accelerated sovereign computation on consumer hardware.

**Capabilities**:

| Category | Details |
|----------|---------|
| **Experiments** | 78 complete: FAO-56, soil, IoT, WB, dual Kc, Richards, biochar, yield, CW2D, 8 ET₀ methods, GDD, pedotransfer, ensemble, bias correction, parity, dispatch, Anderson coupling, SCS-CN, Green-Ampt, VG inverse, seasonal WB, immunological Anderson (tissue/cytokine/barrier/cross-species), f64-canonical GPU, cross-spring evolution |
| **ET₀ Methods** | Penman-Monteith, Priestley-Taylor, Hargreaves-Samani, Makkink, Turc, Hamon, Blaney-Criddle, Thornthwaite |
| **Python Baselines** | 1,237/1,237 PASS against digitized paper benchmarks (57 papers) |
| **Rust Validation** | 827 lib + 186 forge tests (27 GPU fail: upstream wgpu 28), 381/381 validation checks, 146/146 evolution |
| **Real Data** | 15,300 station-days Open-Meteo ERA5 (100 Michigan stations), 1498/1498 atlas checks |
| **GPU Orchestrators** | 25 Tier A + 6 GPU-universal (ops 0-13 + jackknife/bootstrap/diversity + 6 f64-canonical local ops), seasonal pipeline, atlas stream, MC ET₀ |
| **Seasonal Pipeline** | ET₀→Kc→WB→Yield chained, GPU stages 1-3, multi-field streaming (57/57), pure GPU end-to-end (46/46) |
| **Local GPU Compute** | 6 f64-canonical ops via `compile_shader_universal()` — SCS-CN, Stewart, Makkink, Turc, Hamon, Blaney-Criddle (3 absorbed upstream: Makkink→Op14, Turc→Op15, Hamon→Op16; 3 local-only) |
| **metalForge** | 27 workloads, 66/66 cross-system routing (GPU+NPU+CPU), 7-stage GPU→NPU PCIe bypass |
| **NPU** | AKD1000 live (3 experiments, 95/95 checks, ~48µs inference) |
| **CPU Benchmark** | 20.6× geometric mean speedup vs Python (24/24 parity), 13,000× atlas-scale |
| **GPU Live** | Titan V 24/24 PASS (0.04% seasonal parity), RTX 4070 validated |
| **NUCLEUS** | biomeOS primal (30 science capabilities), JSON-RPC, deployment graphs, cross-primal forwarding |
| **Nautilus** | bingoCube/nautilus evolutionary reservoir computing (AirSpringBrain, drift detection, NPU export) |

**ToadStool/BarraCuda Contributions**:
- TS-001: `pow_f64` fractional exponent fix (discovered during ET₀ atmospheric pressure calc)
- TS-003: `acos` precision boundary fix
- TS-004: reduce buffer N≥1024 fix
- Richards PDE solver absorbed upstream (S40)
- Stats metrics absorbed upstream (S64)
- 6 f64-canonical WGSL shader ops (3 absorbed: Makkink→Op14, Turc→Op15, Hamon→Op16)
- Fused Welford `mean_variance_f64.wgsl` wired into SeasonalReducer (hotSpring S58 provenance)
- Fused Pearson `correlation_full_f64.wgsl` wired into gpu/stats (neuralSpring S69 provenance)
- NVK/Mesa f64 reliability finding → GPU fallback to CPU Welford documented

**Participates In**: Node Atomic (via ToadStool compute), Nest Atomic (via NestGate data), NUCLEUS (via biomeOS deployment graphs), metalForge cross-system dispatch

### hotSpring - Computational Physics

**Domain**: Plasma physics, nuclear structure, lattice QCD, transport, spectral theory
**Phase**: Domain Validation
**Status**: v0.6.15 — ~700 tests, 84 binaries, 62 WGSL shaders, 39/39 validation suites

**Role**: hotSpring validates the ecoPrimals compute pipeline against published computational physics — Yukawa OCP, nuclear EOS (HFB), lattice QCD (SU(3) pure gauge + dynamical fermion HMC), Stanton-Murillo transport, Anderson localization, and Hofstadter butterfly. First consumer-GPU dynamical fermion QCD. First neuromorphic silicon (AKD1000) in a lattice QCD production pipeline.

**Capabilities**:

| Category | Details |
|----------|---------|
| **Experiments** | 30 complete/active: MD, GPU scaling, parity, lattice QCD, NPU characterization, brain architecture, adaptive steering |
| **Physics Domains** | Yukawa OCP MD, nuclear EOS (SEMF→HFB→deformed), SU(3) gauge + dynamical fermion HMC, Green-Kubo transport, Anderson 1D/2D/3D, Hofstadter butterfly, Abelian Higgs |
| **GPU Validation** | 62 WGSL shaders, DF64 core streaming (3.24 TFLOPS, 14-digit precision on FP32), GPU-resident CG (15,360× readback reduction) |
| **NPU Integration** | Live AKD1000 via PCIe, 15-head ESN (11 production + 4 proxy), cross-run learning, concept edge detection |
| **Brain Architecture** | 4-layer concurrent: RTX 3090 motor + Titan V pre-motor + CPU cortex + NPU cerebellum |
| **Nautilus Shell** | Evolutionary reservoir computing (bingoCube/nautilus): 5.3% LOO, 2.6% blind Exp 029, 540× quenched→dynamical cost reduction, self-regulating drift + edge seeding, AKD1000 int4 export |
| **Production Results** | Deconfinement χ=40.1 at β=5.69 (32⁴, 13.6h, $0.58). Dynamical crossover confirmed (8⁴, 17 β points) |

**ToadStool Contributions**:
- 62 WGSL shaders evolved via cross-spring absorption (lattice QCD, HFB, transport, spectral)
- GPU-resident CG solver pattern absorbed upstream
- DF64 core streaming validated and expanded (S60)
- NVK dual-GPU deadlock fix (serialize device creation)
- ESN cross-substrate patterns (GPU WGSL dispatch, NPU int4 quantization)

**primalTools Contributions**:
- bingoCube/nautilus: evolutionary reservoir computing crate (31 tests, 5 examples)
- NautilusBrain API for NPU integration, self-regulating drift monitor, integrated edge seeder
- AKD1000 int4 weight export with quantization validation (MSE=0.004)
- Full brain rehearsal: save/restore/transfer/merge/AKD1000 end-to-end validated
- Exp 030: adaptive steering fix (--max-adaptive=12), bootstrapped from 29 data points

**Participates In**: Node Atomic (via ToadStool compute), metalForge (NPU + multi-GPU), NUCLEUS (via biomeOS deployment)

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
