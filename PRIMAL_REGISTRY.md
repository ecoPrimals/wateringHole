# Primal Registry - ecoPrimals Ecosystem

**Purpose**: Authoritative catalog of every primal, its primitives, its domain, and its role in the ecosystem  
**Audience**: Any primal seeking to understand what capabilities exist  
**Last Updated**: April 13, 2026 (Phase 41 — Pre-Downstream Gap Resolution, 12/12 ALIVE, 19/19 exp094 PASS)

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

**IPC Methods**: 185 JSON-RPC methods including beacon, crypto, BTSP, health, capabilities, identity  
**Dependencies**: Zero C dependencies. 100% RustCrypto suite.

**Participates In**: Tower Atomic (with Songbird), NUCLEUS, RootPulse, BirdSong encryption, Dark Forest Federation

---

### Songbird - Network Primal

**Domain**: Network orchestration, discovery, and federation  
**Phase**: Foundation  
**Status**: Production Ready (S+, 79 wire methods, 100% security provider delegation + Pure Rust Tor, 7,265+ lib tests / ~13K total, ~72% coverage, 30 crates, ecoBin v3.0, BTSP Phase 2 complete, Wire Standard L3, `ipc.resolve` returns `native_endpoint`/`virtual_endpoint`, Phase 5 registry seeding for all 9 NUCLEUS primals)

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
| **Storage** | `storage.store`, `storage.retrieve`, `storage.delete`, `storage.list`, `storage.exists`, `storage.stats`, `storage.store_blob`, `storage.retrieve_blob`, `storage.fetch_external` |
| **Model** | `model.register`, `model.exists`, `model.locate`, `model.metadata` |
| **Templates** | `templates.store`, `templates.retrieve`, `templates.list`, `templates.community_top` |
| **Beacon** | `beacon.store`, `beacon.retrieve`, `beacon.list`, `beacon.delete` |
| **Health** | `health.check`, `health.liveness`, `health.readiness`, `health` |

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
**Status**: Production Ready (A++ GOLD STANDARD) — 163 JSON-RPC methods, BTSP auto-detect on all transports (LD-04 resolved), `health.liveness` fully operational, 20,843+ workspace tests, clippy pedantic clean, ~83% line coverage (182K lines instrumented), BearDog crypto delegation enforced (Node Atomic), capability-based discovery, all files < 1000 lines, hw-learn pipeline, PrecisionBrain routing, NvkZeroGuard, VRAM-aware workload routing

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
| **Provenance** | `toadstool.provenance` — cross-spring flow matrix (19+ flows across 6 springs, 19 domains) |
| **Hardware Learning** | `compute.hardware.*` (observe/distill/apply/share_recipe/status), hw-learn pipeline, `RecipeStore`, `RegisterAccess` trait |
| **Firmware Inventory** | `FirmwareInventory` (probe/compute_viable/compute_blockers/needs_software_pmu) via nvpmu |
| **SPIR-V Codegen Safety** | `spirv_codegen_safety` module (`PrecisionBrain`, `NvkZeroGuard`, `HardwareCalibration`), root-cause rename from `nvvm_safety` |
| **IPC** | 96+ JSON-RPC 2.0 methods (semantic naming), tarpc typed RPC, Unix socket standard |

**Key principles**: Capability-based discovery (self-knowledge only), ecoBin compliant (pure Rust core), zero hardcoded primal names/ports, all unsafe blocks documented with `// SAFETY:`. Rust 1.82+ MSRV.

**Participates In**: Node Atomic (with Tower Atomic), NUCLEUS, serves hardware capabilities to BarraCuda

---

### BarraCuda - Math Primal

**Domain**: Pure mathematics — WGSL shaders, precision strategy, naga IR optimisation  
**Phase**: Foundation  
**Status**: Production Ready (A+) — v0.3.12 — 4,368+ tests, 826 WGSL shaders, 1,116+ Rust source files, 32 JSON-RPC methods, zero unsafe (`#![forbid(unsafe_code)]`), zero clippy warnings (pedantic+nursery), zero `Result<T,String>` in production, zero `.expect()` in IPC handlers, AGPL-3.0-or-later, tensor.batch.submit fused pipeline IPC, standardized tensor.* response schemas, LD-05 resolved (TCP sidecar graceful degradation), 3-tier device fallback (wgpu GPU → wgpu CPU → SovereignDevice IPC), BTSP Phase 2 authenticated connections, Wire Standard L2 compliant, 15-tier precision continuum, PrecisionBrain domain→tier routing, NagaExecutor CPU shader interpreter, capability-based discovery (zero hardcoded primal names), `with_device(Arc)` constructors on 8 core types, `bytes::Bytes` zero-copy I/O, `deny.toml` supply chain audit, `cpu-shader` feature default-on (ecoBin), all deps pure Rust (blake3=pure), all production files under 600 lines; budded from ToadStool (S93), separate primal at `ecoPrimals/barraCuda/`

**Role**: BarraCuda is pure math. All math originates as WGSL shaders authored in f64 as the canonical precision. BarraCuda does not care about hardware — it writes the mathematics, coralReef compiles it, toadStool discovers and dispatches it. The precision tier (`Fp64Strategy`: f32 / f64 / df64) is the interface between barraCuda and coralReef. naga-IR optimisation (FMA fusion, DCE) operates on the math, not the hardware. Currently uses wgpu as a transitional dispatch substrate until coralReef's sovereign dispatch pipeline is integrated.

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **Core** | 826 WGSL f64 shaders: matmul, relu, softmax, gelu, layer_norm, transpose, elementwise, reduce (incl. DF64 variants), broadcast |
| **Linear Algebra** | solve, cholesky, QR, SVD, LU, sparse eigensolve (Lanczos), GEMM f64, matrix inverse |
| **Scientific Computing** | Crank-Nicolson PDE, Richards equation, MD forces (Coulomb, Morse, Born-Mayer, Yukawa), PPPM electrostatics, HFB nuclear physics |
| **Lattice QCD** | 14 GPU shaders + host: Wilson action, HMC leapfrog, Dirac, CG solver, pseudofermion, polyakov loop |
| **Special Functions** | Bessel, Laguerre, Hermite, Legendre, spherical harmonics, digamma, beta, gamma, erf |
| **ML** | Attention (7 variants), Training losses (10 types), Optimizers (5 types), CNN ops |
| **Bioinformatics** | 31 GPU bio ops: kmer histogram, taxonomy FC, UniFrac, ANI, random forest inference, HMM, Dada2, Gillespie, Wright-Fisher |
| **Kinetics** | Hill activation/repression, Monod saturation, regulatory network primitives |
| **Precision Strategy** | `Fp64Strategy` (Native / Hybrid / Sovereign / Concurrent), `PrecisionRoutingAdvice` (F64Native / F64NativeNoSharedMem / Df64Only / F32Only) |
| **Math-level Optimisation** | naga-IR FMA fusion (~1.3x), dead expression elimination — operates on the algebra, not the ISA |

**Boundary**: barraCuda writes the math. coralReef compiles the math. toadStool runs the math. The shaders are the mathematics; the driver is plumbing.

**Five-Spring ingestion**: hotSpring (lattice QCD, HFB, spectral), neuralSpring (bio ML, Hill kinetics), wetSpring (ODE), airSpring (Richards PDE), groundSpring (sensor noise, Ada Lovelace reclassification). All f32→f64 (S49).

**Participates In**: Node Atomic (via ToadStool), NUCLEUS compute layer

---

### coralReef - Shader Compiler Primal

**Domain**: GPU shader compilation — WGSL/SPIR-V/GLSL to native GPU binary  
**Phase**: Foundation  
**Status**: Phase 10 Iteration 80 (A+) — 4,467 tests passed, 0 failed, ~65% line coverage (~82% non-hardware), 11 GPU architectures (NVIDIA SM35-SM120 + AMD GCN5/RDNA2-4), wire contract documented (`SHADER_COMPILE_WIRE_CONTRACT.md`), `CompilationInfo` in IPC responses, BTSP Phase 2 complete, ecoBin v3 `deny.toml` enforced (ring/openssl/C-sys banned), zero `Result<_, String>` in production, zero `.unwrap()` in library code, zero TODO/FIXME/HACK, `#[forbid(unsafe_code)]` on 10/11 crate roots, zero clippy warnings (pedantic+nursery), zero doc warnings, all files <1000 lines, AGPL-3.0-or-later, hardware: 2× Titan V (VFIO) + RTX 4070 (nvidia-drm)

**Role**: coralReef is the sovereign Rust GPU shader compiler. It compiles WGSL, SPIR-V, and GLSL compute shaders to native GPU binaries with full f64 transcendental support. NVIDIA backend complete (SM35–SM120: Kepler through Blackwell). AMD backend operational (GCN5/GFX906, RDNA2/GFX1030 — MI50 and RX 6950 XT E2E verified). coralDriver provides userspace GPU dispatch via DRM ioctl (AMD amdgpu, NVIDIA nouveau, nvidia-drm/UVM) and VFIO direct BAR0/DMA dispatch (maximum sovereignty). coralGpu unifies compilation and dispatch into a single API with sovereign driver preference (vfio > nouveau > amdgpu > nvidia-drm). Zero C dependencies, zero vendor lock-in, zero FFI. Part of the sovereign compute pipeline: barraCuda generates WGSL shaders, toadStool proxies `shader.compile.*` requests, coralReef compiles to native binary, coralDriver dispatches on hardware.

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **IPC** | `shader.compile.wgsl`, `shader.compile.spirv`, `shader.compile.wgsl.multi`, `shader.compile.status`, `shader.compile.capabilities`, `health.check`, `health.liveness`, `health.readiness`, `identity.get`, `capability.list`, `capability.register`, `ipc.heartbeat` — JSON-RPC 2.0 + tarpc (TCP/Unix socket), zero-copy `bytes::Bytes` payloads, differentiated error codes, `CompilationInfoResponse` (GPR count, instruction count, shared mem, barriers, workgroup size), FMA policy control |
| **NVIDIA Backend** | SM35–SM120 (Kepler through Blackwell), SASS binary output, f64 transcendentals via Newton-Raphson (sqrt, rcp, exp2, log2, sin, cos, exp, log, pow, tan, atan, asin, acos, sinh, cosh, tanh) |
| **AMD Backend** | GCN5 (MI50) + RDNA2–RDNA4, native `v_fma_f64`/`v_sqrt_f64`/`v_rcp_f64`, 1,446 ISA opcodes (Rust-generated from AMD XML) |
| **Compiler Core** | naga frontend, SSA IR, copy propagation, DCE, instruction scheduling, register allocation, vendor-specific legalization and encoding |
| **coralDriver** | AMD DRM ioctl (GEM, PM4, BO list, CS submit, fence sync) — **E2E verified on RX 6950 XT + MI50**, NVIDIA nouveau (sovereign + new UAPI), nvidia-drm/UVM (RM alloc, GPFIFO, USERD), VFIO (BAR0 + DMA + GPFIFO + sync, staged sovereign init) — pure Rust, zero libc |
| **coralGpu** | Unified compile + dispatch API — vendor-agnostic `GpuContext`, multi-GPU auto-detect |
| **f64 Lowering** | Full f64 transcendental suite: sqrt, rcp, exp2, log2, sin, cos, exp, log, pow, tan, atan, asin, acos, sinh, cosh, tanh, Complex64 — NVIDIA (DFMA software) + AMD (native hardware) |
| **Wire Contract** | `docs/SHADER_COMPILE_WIRE_CONTRACT.md` — authoritative JSON-RPC/tarpc schemas, error codes, multi-stage ML pipeline composition patterns |
| **Security** | BTSP Phase 2 (BearDog delegation), `deny.toml` C/FFI bans, `#[forbid(unsafe_code)]` on all non-driver crates, env-configurable socket/heartbeat/namespace, zero hardcoded primal names |

**Participates In**: Sovereign Compute Pipeline (barraCuda → toadStool → coralReef → native binary → coralDriver → hardware)

---

### biomeOS - Ecosystem Orchestrator

**Domain**: Primal orchestration and ecosystem coordination  
**Phase**: Foundation  
**Version**: v2.99  
**Status**: Production Ready (A++, Security A++ LEGENDARY) — 7,695 tests (0 failures), 90%+ region / function / line coverage (llvm-cov), 26 workspace crates, 40 deploy graphs, 20 niche templates, 290+ capability translations, 26 capability domains, zero-copy `bytes::Bytes` + `Arc<str>`, Rust 2024 edition, clippy pedantic+nursery (0 warnings), `#[expect(reason)]` lint policy, ecoBin v3.0 compliant, `#[forbid(unsafe_code)]` all crate roots + all 20+ binaries, BTSP security posture wired

**Role**: biomeOS is the orchestration substrate. It discovers primals by their capabilities at runtime, routes requests semantically via the Neural API, composes primals into atomics (Tower, Node, Nest, NUCLEUS), and coordinates higher-order patterns like RootPulse. It is the composer - primals are the instruments.

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **Neural API** | Semantic routing (`capability.call`), 290+ translations, 26 domains, pathway learning |
| **Atomics** | Tower Atomic, Node Atomic, Nest Atomic, Full NUCLEUS composition |
| **Provenance** | `rootpulse_commit` graph, `provenance_pipeline` graph, rhizoCrypt/LoamSpine/sweetGrass domains |
| **Discovery** | Runtime capability matching, primal health monitoring, prefix resolution |
| **Deployment** | genomeBin management, graph-based deployment, cross-device federation |
| **Security** | Dark Forest integration (A++ LEGENDARY), genetic model coordination |
| **IPC** | Universal IPC v3.0, multi-transport support |

**Participates In**: Coordinates all composed systems (RootPulse, Tower Atomic, NUCLEUS, federation). Provenance trio (rhizoCrypt + LoamSpine + sweetGrass) wired into Neural API for `dag.*`, `commit.*`, `provenance.*` routing.

---

## Post-NUCLEUS Primals

These primals build emergent behaviors on the NUCLEUS foundation. They compose into higher-order patterns (RootPulse, Memory & Attribution Stack) coordinated by biomeOS via the Neural API. Each is functional, tested, and has its own showcase demonstrations. They represent the next evolutionary phase - building emergent capabilities on the foundation that the primals above provide.

### petalTongue - Universal User Interface Primal

**Domain**: Universal User Interface — any computational universe → any modality → any user type  
**Phase**: Post-NUCLEUS  
**Status**: Production Ready (A+) — v1.6.6, 16 crates, 5,244 tests, ~86% / ~87% coverage, edition 2024, `#![forbid(unsafe_code)]` + `deny(unwrap/expect)`, zero C deps, AGPL-3.0-or-later, 11 DataBinding variants, UUI glossary module, SAME DAVE model, `#[expect]` migration. See [PETALTONGUE_NEEDS_FROM_ECOSYSTEM.md](petaltongue/PETALTONGUE_NEEDS_FROM_ECOSYSTEM.md) for integration gaps

**Role**: petalTongue is the Universal User Interface — translating any computational universe into any modality for any user type. It implements a composable **Grammar of Graphics** pipeline: any primal sends a declarative grammar expression (data + variable bindings + scales + geometry + coordinates), and petalTongue compiles it to the best available representation (desktop display, terminal, audio sonification, SVG, PNG, JSON API, haptic, braille). Tufte constraints (data-ink ratio, lie factor, accessibility) are machine-checked on every render. The **SAME DAVE** cognitive model (Sensory Afferent / Motor Efferent) provides bidirectional feedback loops. Heavy computation (statistics, 3D tessellation, physics) is offloaded to barraCuda via capability-based discovery. The grammar is domain-agnostic: the same pipeline renders ecosystem topology, clinical vitals, molecular structures, game worlds, and universe simulations. Accessibility is not a feature — it is the architecture: every modality is a first-class compilation target, serving sighted humans, blind hikers, paraplegic developers, AI agents, and beyond. Live ecosystem wiring enables 60 Hz sensor streaming, interaction broadcast, and Neural API self-registration with biomeOS.

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **Display Modes** | Desktop display (egui/wayland), Terminal display (ratatui), Web interface (axum), Headless rendering (SVG/PNG) |
| **Audio** | Sonification engine: 5 instruments, health-to-pitch mapping, position-to-stereo panning |
| **UUI** | Canonical glossary (`uui_glossary`), modality names, user types, SAME DAVE model constants |
| **Layout** | 4 graph layout algorithms, pan/zoom/select |
| **Grammar of Graphics** | Declarative grammar expressions (Scale, Geometry, Coordinate, Statistic, Aesthetic, Facet traits), grammar compiler → RenderPlan, modality compilers (egui, ratatui, audio, SVG, PNG, JSON) |
| **Tufte Constraints** | Data-ink ratio, lie factor, chartjunk detection, small multiples preference, color accessibility, data density, smallest effective difference — auto-correctable |
| **Interaction** | Inverse scale pipeline (display coords → data values), brush selection, linked views, cross-primal interaction events via `visualization.interact` |
| **Integration** | Live primal discovery via Songbird, biomeOS SSE event subscription, barraCuda GPU compute offload (`math.stat.*`, `math.tessellate.*`, `math.project.*`) |
| **IPC** | `visualization.render`, `visualization.render.stream`, `visualization.export`, `visualization.validate`, `visualization.capabilities`, `visualization.interact` — JSON-RPC 2.0 + tarpc, `bytes::Bytes` zero-copy for binary payloads |
| **Configuration** | Environment-driven (ENV > File > Defaults), TCP fallback IPC |

**UniBin Modes**: `ui`, `tui`, `web`, `headless`, `server`, `status`

**Key principle**: One Engine, Infinite Representations. Data defines structure. Grammar defines mapping. Modality defines rendering. The user defines interaction. Other primals send grammar expressions or raw data; petalTongue handles the rest. See `wateringHole/petaltongue/VISUALIZATION_INTEGRATION_GUIDE.md`.

**Participates In**: biomeOS ecosystem visualization, real-time health monitoring display, barraCuda compute pipeline (grammar → GPU statistics/tessellation → render), cross-primal interaction events

---

### rhizoCrypt - Ephemeral Memory Primal

**Domain**: Content-addressed DAG engine for working memory  
**Phase**: Post-NUCLEUS  
**Version**: 0.14.0-dev  
**Status**: Production Ready (1,441 tests, 94.34% llvm-cov, clippy pedantic+nursery enforced (`doc_markdown`, `must_use_candidate`, etc.), Edition 2024, `unsafe_code = "deny"` / `unwrap_used`+`expect_used = "deny"` workspace-wide, zero `unsafe` blocks, AGPL-3.0-or-later, UniBin compliant, musl-static x86_64 shipped in plasmidBin (5.4M), cargo-deny enforced (18-crate ecoBin ban list incl. reqwest + ring), `--fail-under-lines 90` CI gate, cross-compile CI (musl x86_64/aarch64 + RISC-V), `niche.rs` self-knowledge with MCP tools, `niche.rs` runtime: 28 methods (5 domains) — 24 in `capability_registry.toml` + 4 implicit (`health.readiness`, `identity.get`, `tools.list`, `tools.call`) + deploy graph with `fallback = "skip"`, `DagBackend` enum dispatch (redb default), GC sweeper, zero cross-primal compile deps — sovereign wire types, `dag.dehydrate` alias, `identity.get` implemented, biomeOS Format E wire compatibility, GAP-MATRIX-05 live-validated, reqwest eliminated — hyper/tower pure Rust, **BTSP Phase 1** — FAMILY_ID socket scoping + BIOMEOS_INSECURE guard)

**Role**: rhizoCrypt provides the ephemeral workspace layer — a git-like DAG of content-addressed events that serves as working memory. Sessions are scoped, lock-free (DashMap), and real-time. Data lives here temporarily until it is either discarded or "dehydrated" (committed) to permanent storage. All inter-primal communication uses capability-based discovery — rhizoCrypt has zero hardcoded vendor references.

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **Vertex Operations** | Content-addressed events with BLAKE3 hashing, multi-parent DAG links, nanosecond timestamps |
| **Session Management** | Scoped workspaces with full lifecycle (active, committed, discarded), lock-free |
| **Merkle Trees** | Content verification, inclusion proofs, root computation |
| **Dehydration** | Temporal collapse: commit session state to permanent storage via JSON-RPC 2.0 |
| **Slice Semantics** | 6 query modes (Copy, Loan, Consignment, Escrow, Mirror, Provenance) |
| **Attribution** | Agent DID identity, per-agent event counting, role assignment |
| **Niche** | `niche.rs` self-knowledge module with `PRIMAL_ID`, `CAPABILITIES`, `CONSUMED_CAPABILITIES`, `COST_ESTIMATES`, `operation_dependencies()` |
| **IPC** | JSON-RPC 2.0 (required) + tarpc/bincode (optional), 28 methods across 5 domains (`dag.*`, `health.*`, `capabilities.*`, `identity.*`, `tools.*`), enhanced `capabilities.list` with per-method cost/deps, `health.liveness` + `health.readiness` probes, `tools.list` + `tools.call` MCP, 4-format capability parsing, `ValidationSink` pluggable output, `normalize_method()` legacy prefix support |

**Participates In**: RootPulse (ephemeral workspace layer), Memory & Attribution stack

---

### sweetGrass - Attribution Primal

**Domain**: Semantic provenance and attribution  
**Phase**: Post-NUCLEUS  
**Status**: Production Ready (v0.7.27, 1,218 tests, 90.90% region coverage, Wire Standard L3 FULL COMPLIANCE, BTSP Phase 1 compliant (GAP-MATRIX-12 RESOLVED), GAP-MATRIX-05 RESOLVED, ecoBin compliant, musl-static ready, redb default, parking_lot locks, Edition 2024, MSRV 1.87, AGPL-3.0-or-later, pedantic+nursery clean, zero unsafe, zero production unwrap, 28 JSON-RPC methods incl. `identity.get`, 7 benchmarks, 17 proptest strategies across 5 crates, `Braid.witness` (WireWitnessRef aligned), sovereign types — no shared crates, UDS live-validated via socat, BIOMEOS_INSECURE guard enforced)

**Role**: sweetGrass tracks who created what, when, and how. It creates "braids" - content-addressable provenance records compliant with W3C PROV-O - and calculates fair attribution shares across contributors. Privacy controls are built in (GDPR-inspired, 5 levels).

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **Braids** | Content-addressable provenance records, W3C PROV-O / JSON-LD compliant, `Arc<str>` zero-copy identifiers |
| **Attribution Engine** | 12 role types (Creator, Contributor, Reviewer...), derivation chain analysis, time decay, recursive propagation |
| **Provenance Graph** | Complete data lineage tracking, DAG queries, "where did this come from?" |
| **Privacy** | 5 privacy levels, GDPR-inspired data subject rights |
| **Storage** | Memory, redb (recommended), Sled (legacy), PostgreSQL backends |
| **Export** | W3C PROV-O JSON-LD standard, ~88% compression with session dedup + zstd |
| **IPC** | JSON-RPC 2.0 + tarpc + REST + UDS, DispatchOutcome, health probes, OrExit |

**Participates In**: RootPulse (attribution layer), Memory & Attribution stack, Loam Certificate provenance

---

### LoamSpine - Permanence Primal

**Domain**: Immutable linear ledger for selective permanence  
**Phase**: Post-NUCLEUS  
**Status**: Production Ready (v0.9.16, 1,507 tests, 92%+ line / 89%+ region coverage, pure Rust, ecoBin compliant, UniBin, Edition 2024, pedantic+nursery clean, cast lint deny, `#[expect(reason)]` bulk migration, CONTEXT.md per PUBLIC_SURFACE_STANDARD, `capabilities.list` + `health.liveness` + `tools.list` + `tools.call` (MCP) per Semantic Method Naming v2.1, tarpc 0.37 (json transport, bincode path eliminated), `ResilientSyncEngine` (circuit-breaker + retry for federation), `DispatchOutcome`/`IpcErrorPhase`/`StreamItem`/`OrExit`/`extract_rpc_result`/`normalize_method` ecosystem patterns, cargo deny 4/4 clean, provenance trio types inlined (no shared crate), `publish = false` on all workspace crates, BTSP Phase 2 handshake (blake3+uuid challenge entropy, 5-submodule architecture), domain-based socket naming (`permanence.sock`), `--socket`/`--port` CLI flags, SignalHandler (SIGTERM/SIGINT graceful shutdown), UDS backpressure semaphore (256 max concurrent), workspace dependency centralization, zero flaky storage tests, registry path constants centralized, BTSP provider socket constant, jsonrpc TCP/UDS transport split, TCP_NODELAY on all TCP sockets, 8×5 concurrent UDS load test)

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
**Status**: Production Ready — v0.1.0, 124+ tests, clippy pedantic+nursery clean

**Role**: skunkBat protects sovereign computing environments through threat detection and graduated response. JSON-RPC 2.0 IPC server on TCP + UDS with BTSP Phase 1 socket naming and Wire Standard L2/L3 compliance. Strictly defensive — reconnaissance, not surveillance. Learns your network's normal baseline and detects deviations. Never inspects content, only metadata.

**Primitives**:

| Category | Primitives |
|----------|-----------|
| **Threat Detection** | Genetic (unknown lineage), Topology (layer-hopping), Behavioral (statistical anomalies), Intrusion (attack signatures), Resource (DoS, exhaustion) |
| **Defense Actions** | Monitor + Alert (low), Quarantine (isolate), Block (deny, operator decision) |
| **Baseline** | Statistical profiling via `VecDeque` rolling window, `/proc/loadavg` system load |
| **Reconnaissance** | Network intelligence (metadata-only, no content) |
| **IPC** | JSON-RPC 2.0 (TCP + UDS), BTSP Phase 1, Wire Standard L2/L3, `security.sock` domain symlink |
| **Integration** | Capability-based runtime discovery (ToadStool, Songbird, BearDog via JSON-RPC) |

**Principles**: Defensive only, user authority required, privacy by architecture

**Participates In**: Ecosystem security layer, Dark Forest defense coordination, NUCLEUS compositions

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

**Spring Versions (as of April 13, 2026)**:

| Spring | Version |
|--------|---------|
| ToadStool | S155b (20,843 tests, hw-learn, nvpmu RegisterAccess, spirv_codegen_safety rename, FirmwareInventory in gpu.info) |
| hotSpring | v0.6.30 (upstream sync v5, naga root-cause rename, BatchedComputeDispatch) |
| groundSpring | V103 |
| neuralSpring | V98/S145 (GPU dispatch evolution, PipelineGraph ready for absorption) |
| wetSpring | V99 |
| airSpring | v0.7.6 |
| barraCuda | v0.3.12 (4,368+ tests, 826 shaders, AGPL-3.0-or-later, 32 IPC methods, LD-05/LD-10 resolved, BTSP Phase 2, all production files <600 lines) |
| coralReef | Phase 10 Iteration 80 (4,467 tests, ~65% line / ~82% non-hw coverage, 11 GPU archs, wire contract documented, CompilationInfo IPC, BTSP Phase 2, ecoBin v3 deny.toml, zero warnings, all files <1000 LOC) |
| primalSpring | v0.9.14 Phase 41 (443 lib tests, 13 FullNucleus capabilities, 19/19 exp094 PASS, NUCLEUS VALIDATED, Phase 5 registry seeding, cross-gate deployment tooling: build_ecosystem_musl.sh, prepare_spore_payload.sh, validate_remote_gate.sh, exp073 LAN mesh, exp074 cross-gate health, LAN deployment guide, zero warnings, zero unsafe) |
| ludoSpring | V30 (82 experiments, 675+19 tests, 42 Python parity, 91.27% coverage, thiserror, MCP tools, tarpc optional, handler architecture split, UniBin 7 subcommands, CI, deploy graph, scyBorg triple license) |

### airSpring - Ecological & Agricultural Sciences

**Domain**: Precision agriculture, irrigation science, environmental systems  
**Phase**: Domain Validation  
**Status**: v0.10.0 — 911 lib + 311 integration + 61 forge + 22 property tests, 97 binaries, 87 experiments, 381/381 validation, 146/146 evolution, 14.3× CPU speedup (24/24 parity, 21/21 CPU-GPU), 0 clippy warnings (pedantic+nursery), zero unsafe code (`#![forbid(unsafe_code)]`), zero mocks in production, zero C deps (14 crates banned in `deny.toml`), AGPL-3.0-or-later, standalone barraCuda 0.3.5 (wgpu 28, DF64 precision tier), Edition 2024. 10 MCP tools wired (Squirrel AI). Platform-agnostic IPC (Transport enum: Unix + TCP). 63 provenance baselines. 63 named tolerances (4 submodules). `#[expect(reason)]` Rust 2024 complete. Full validation pipeline green (2026-03-19)

**Role**: airSpring validates agricultural computational methods — FAO-56 ET₀ (8 methods), soil sensor calibration, IoT irrigation, water balance, dual crop coefficient, Richards equation, yield response, ecological diversity, immunological Anderson coupling, and SCS-CN/Green-Ampt hydrology — proving the full ecoPrimals pipeline from paper reproduction to GPU-accelerated sovereign computation on consumer hardware.

**Capabilities**:

| Category | Details |
|----------|---------|
| **Experiments** | 87 complete: FAO-56, soil, IoT, WB, dual Kc, Richards, biochar, yield, CW2D, 8 ET₀ methods, GDD, pedotransfer, ensemble, bias correction, parity, dispatch, Anderson coupling, SCS-CN, Green-Ampt, VG inverse, seasonal WB, immunological Anderson (tissue/cytokine/barrier/cross-species), f64-canonical GPU, cross-spring evolution, CPU/GPU parity (21/21), toadStool dispatch (19/19), NUCLEUS mesh (17/17), graph coordination (22/22) |
| **ET₀ Methods** | Penman-Monteith, Priestley-Taylor, Hargreaves-Samani, Makkink, Turc, Hamon, Blaney-Criddle, Thornthwaite |
| **Python Baselines** | 1,284/1,284 PASS against digitized paper benchmarks (57 papers), 63 provenance records |
| **Rust Validation** | 911 lib + 311 integration + 61 forge tests, 381/381 validation checks, 146/146 evolution |
| **Real Data** | 15,300 station-days Open-Meteo ERA5 (100 Michigan stations), 1498/1498 atlas checks |
| **GPU Orchestrators** | 25 Tier A + 6 GPU-universal (ops 0-19 all upstream `BatchedElementwiseF64`), seasonal pipeline, atlas stream, MC ET₀ |
| **Seasonal Pipeline** | ET₀→Kc→WB→Yield chained, GPU stages 1-3, multi-field streaming (57/57), pure GPU end-to-end (46/46) |
| **metalForge** | 27 workloads, 66/66 cross-system routing (GPU+NPU+CPU), 7-stage GPU→NPU PCIe bypass |
| **NPU** | AKD1000 live (3 experiments, 95/95 checks, ~48µs inference) |
| **CPU Benchmark** | 14.3× geometric mean speedup vs Python (24/24 parity), 13,000× atlas-scale |
| **GPU Live** | Titan V 24/24 PASS (0.04% seasonal parity), RTX 4070 validated |
| **NUCLEUS** | biomeOS primal (41 capabilities), JSON-RPC 2.0, 4 deploy graphs, cross-primal forwarding |
| **Nautilus** | bingoCube/nautilus evolutionary reservoir computing (AirSpringBrain, drift detection, NPU export) |
| **MCP Tools** | 10 ecology tools (Squirrel AI): et0, hargreaves, water_balance, soil_moisture, dual_kc, richards, yield_response, spi_drought, diversity, pedotransfer |
| **IPC** | Platform-agnostic Transport (Unix + TCP), 3-tier discovery, health probes, circuit breaker |

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
- Transport enum + resolve_transport() pattern (upstream absorption candidate)
- MCP tool dispatch pattern (tools/list + tools/call in primal dispatch)

**Participates In**: Node Atomic (via ToadStool compute), Nest Atomic (via NestGate data), NUCLEUS (via biomeOS deployment graphs), metalForge cross-system dispatch

### hotSpring - Computational Physics

**Domain**: Plasma physics, nuclear structure, lattice QCD, transport, spectral theory
**Phase**: Domain Validation
**Status**: v0.6.23 — ~700 tests, 84 binaries, 62 WGSL shaders, 39/39 validation suites

**Role**: hotSpring validates the ecoPrimals compute pipeline against published computational physics — Yukawa OCP, nuclear EOS (HFB), lattice QCD (SU(3) pure gauge + dynamical fermion HMC), screened Coulomb transport, Anderson localization, and Hofstadter butterfly. First consumer-GPU dynamical fermion QCD. First neuromorphic silicon (AKD1000) in a lattice QCD production pipeline.

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

### primalSpring - Coordination and Composition Validation

**Domain**: Primal coordination, atomic composition, graph execution, emergent systems, bonding  
**Phase**: Phase 41 (Pre-Downstream Gap Resolution — 12/12 ALIVE, 19/19 exp094 PASS)  
**Status**: v0.9.14 Phase 41 — 443 lib tests (all passing), 53+ experiments, 19/19 exp094 composition parity PASS (0 FAIL, 0 SKIP), all LD-01 through LD-10 gaps RESOLVED, `IpcError::is_transport_mismatch()` for graceful transport handling, `CompositionContext::from_live_discovery()`, `validate_parity` with `stats.mean`/`storage.store`/`crypto.hash` wire methods, `nucleus_launcher.sh` Phase 5 registry seeding, 67+ TOML graphs across 9 subdirectories, cross-gate deployment tooling, IPC resilience stack, MCP tools (8 typed), zero clippy warnings, zero unsafe, ecoBin compliant

**Role**: primalSpring is the spring whose domain IS coordination. Where other springs validate domain science via the ecoPrimals infrastructure, primalSpring validates the infrastructure itself — that biomeOS composes primals correctly, that NUCLEUS atomics deploy and degrade gracefully, that all 5 coordination patterns work with real primals, that Layer 3 emergent systems emerge correctly, and that cross-spring data flows maintain provenance. It has proven the full composition lifecycle — binary discovery, socket nucleation, topological startup, capability-based health validation, and multi-primal coordination with real IPC.

**Capabilities**:

| Category | Details |
|----------|---------|
| **Experiments** | 53 across 10 tracks: Atomic Composition (6), Graph Execution (6), Emergent Systems (6), Bonding & Plasmodium (5), Cross-Spring Coordination (5), Showcase-Mined (10), Live Composition (11), Multi-Node Bonding (2), Cross-Gate Deployment (2). All use real `discover_by_capability()` with honest `check_skip` for live-IPC checks. |
| **Deploy Graphs** | 22 (18 single-node + 4 multi-node): all parsed, structurally validated, topologically sorted via `topological_waves()` (Kahn's algorithm). All nodes have `by_capability` (enforced by test). |
| **Niche Self-Knowledge** | 37 capabilities (including ai.query, ai.health, composition.tower_squirrel_health), semantic mappings (7 domains), operation dependencies, cost estimates |
| **RPC Methods** | 17 methods: health.check, health.liveness, health.readiness, capabilities.list, coordination.validate_composition, coordination.validate_composition_by_capability, coordination.discovery_sweep, coordination.probe_primal, coordination.probe_capability, coordination.deploy_atomic, coordination.bonding_test, coordination.neural_api_status, graph.list, graph.validate, graph.waves, graph.capabilities, lifecycle.status, mcp.tools.list |
| **IPC Resilience** | IpcError (8 typed variants + IpcErrorPhase), CircuitBreaker, RetryPolicy, resilient_call(), DispatchOutcome\<T\>, extract_rpc_result/dispatch, 4-format capability parsing |
| **Live Composition** | Tower STABLE (beardog + songbird + biomeOS, 24/24 gates). Squirrel AI composition (Tower + Squirrel + Anthropic Claude). exp060: biomeOS-orchestrated Tower deploy. exp061: 3-primal AI composition. |
| **Emergent Systems Tested** | RootPulse (commit/branch/merge/diff/federate), RPGPT (60Hz tick + provenance), coralForge (neural object Pipeline graph), cross-spring ecology |

**Participates In**: biomeOS (primary test subject), all NUCLEUS primals (deploy + health), Provenance Trio (RootPulse validation), all springs (cross-spring coordination validation), Squirrel (live AI composition)

### ludoSpring - Game Design & Interaction Science

**Domain**: Ludology, HCI, game science, procedural generation, interaction design  
**Phase**: Domain Validation  
**Status**: V30 — 82 experiments, 675 barracuda + 19 forge tests, 42 Python parity, 19 proptest, 11 IPC integration. Zero `#[allow()]`, zero `unsafe`, zero clippy warnings (pedantic+nursery), zero TODO/FIXME. `#![forbid(unsafe_code)]`, AGPL-3.0-or-later (scyBorg triple: AGPL + ORC + CC-BY-SA-4.0), Edition 2024, MSRV 1.87. 91.27% line coverage (85% floor enforced). `thiserror` 2.x on all error types. MCP `tools.list`/`tools.call` (8 science tools). Optional `tarpc-ipc` feature. Handlers split into 5 domain submodules. UniBin 7 subcommands. CI pipeline. Deploy graph fragment. `GpuContext` + `TensorSession` wired behind `gpu` feature. `default-features = false` on barraCuda v0.3.7.

**Role**: ludoSpring validates the ecoPrimals pipeline against 13 foundational HCI/game science models — Fitts's law, Hick's law, Steering law, GOMS, Flow theory, Dynamic Difficulty, Four Keys to Fun, Engagement metrics, Perlin noise, Wave Function Collapse, L-systems, BSP trees, Tufte data-ink — proving faithful port from Python baselines to Rust CPU to GPU WGSL shaders. The validated math builds playable prototypes (Doom terminal, roguelike explorer) and cross-domain applications (field genomics provenance, medical access control, extraction shooter anti-cheat).

**Capabilities**:

| Category | Details |
|----------|---------|
| **Game Science** | `game.evaluate_flow`, `game.evaluate_engagement`, `game.evaluate_fun`, `game.evaluate_dda`, `game.evaluate_tufte`, `game.evaluate_interaction_cost`, `game.evaluate_goms`, `game.classify_genre` |
| **Procedural** | `game.generate_noise`, `game.generate_wfc`, `game.generate_lsystem`, `game.generate_bsp` |
| **GPU Compute** | 5 WGSL shaders (fog_of_war, tile_lighting, pathfind_wavefront, perlin_2d, dda_raycast), `TensorSession` via `GpuContext` |
| **Telemetry** | 13-event portable game telemetry protocol (NDJSON), external adapters (Veloren, Fish Folk, A/B Street) |
| **RPGPT** | Sovereign RPG engine architecture — any open ruleset + any world + AI narration |
| **Cross-Domain** | Provenance trio integration, extraction shooter fraud detection, field sample lifecycle, consent-gated medical access, cross-domain fraud unification |
| **Health** | `health.check`, `health.liveness`, `health.readiness` |
| **Niche** | `capability.list`, `lifecycle.status`, `capability.register`, `capability.deregister` |
| **Experiments** | 82 across 22 tracks: core game systems, interaction models, PCG, metrics, benchmarks, external control groups, cross-spring (NCBI, NUCLEUS), RPGPT, Games@Home, provenance trio, extraction shooters, composable viz, lysogeny (6 open recreations), cross-spring provenance (5), RPGPT dialogue plane (9), game history revalidation (7) |
| **Python Baselines** | 7 scripts, `combined_baselines.json` with `content_sha256`, 42 parity tests |
| **Deployment** | UniBin (server/status/version), deploy graph, niche YAML, Neural API domain registration, 26 capabilities (24 game + 2 health) |

**IPC Methods**: 26 JSON-RPC 2.0 methods (game evaluation, procedural generation, telemetry, health, lifecycle, capability) over Unix sockets  
**Dependencies**: barraCuda (CPU math, `default-features = false`), wgpu (optional `gpu` feature), serde, uuid. Zero C dependencies in application code.

**Participates In**: RPGPT (game science + session quality), Provenance Trio (rhizoCrypt DAG + loamSpine certs + sweetGrass braids), biomeOS (niche citizen), toadStool (GPU dispatch), coralReef (shader compilation), petalTongue (visualization), Squirrel (AI narration), metalForge (cross-substrate routing)

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
