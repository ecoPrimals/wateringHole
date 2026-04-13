# Primal Responsibility Matrix — Cross-Primal Concern Ownership

**Version:** 3.0.0
**Date:** April 3, 2026
**Authority:** wateringHole (ecoPrimals Core Standards)
**Purpose:** Define each primal's role, capability domain, and interaction boundaries.
This matrix governs what each primal OWNS, how primals interact, and where
OVERSTEP has been identified. It is the primary reference for humans and AI
agents working in the ecoPrimals ecosystem.

---

## Primal Directory

Each primal has exactly one core domain. All inter-primal communication flows
through JSON-RPC 2.0 over Unix Domain Sockets (UDS) or TCP, routed by biomeOS
Neural API capability discovery — never by hardcoded primal names.

### NUCLEUS Atomics (foundation layer)

| Primal | Domain | Capability Namespace | Role |
|--------|--------|---------------------|------|
| **BearDog** | Crypto / Signing | `crypto.*` | Signs, verifies, hashes, generates keypairs. Every primal delegates cryptographic operations to BearDog. The identity and trust root of the ecosystem. |
| **Songbird** | Network / Transport | `net.*` | Peer discovery, mesh networking, encrypted transport (QUIC/TLS). The only primal that should own network stack dependencies. |
| **NestGate** | Storage / Permanence | `storage.*` | Persistent key-value and object storage. Primals delegate data persistence here rather than embedding their own storage engines. |
| **toadStool** | Compute / GPU Dispatch | `compute.*`, `ember.*` | Hardware inventory, GPU job dispatch, ember (execution unit) management. Owns the interface between software and accelerator hardware. |

### Extended Computation

| Primal | Domain | Capability Namespace | Role |
|--------|--------|---------------------|------|
| **barraCuda** | Math / Numerical | `math.*` | Tensor operations, activation functions, statistics, noise generation, Fitts/Hick laws, special functions. Pure numerical computation with no hardware dispatch. |
| **coralReef** | Shader Compilation | `shader.*` | Compiles WGSL/SPIR-V shaders. Deferred boundary with toadStool — coralReef compiles, toadStool dispatches. GPU driver stack under active development. |

### Meta-Tier (orchestration + intelligence + presentation)

| Primal | Domain | Capability Namespace | Role |
|--------|--------|---------------------|------|
| **biomeOS** | Orchestration | `capability.*`, `graph.*`, `topology.*`, `lifecycle.*` | The nervous system. Routes capability discovery, deploys composition graphs, manages primal lifecycle. All primals register capabilities with biomeOS on startup. |
| **Squirrel** | AI / Inference | `ai.*`, `context.*` | Model inference routing (Ollama, local LLMs). Context window management, summarization, AI-driven analysis. |
| **petalTongue** | Visualization | `visualization.*`, `interaction.*` | Scene rendering, dashboard construction, SVG/HTML export, user interaction events. The eyes and hands of the ecosystem. |

### Provenance Trio

| Primal | Domain | Capability Namespace | Role |
|--------|--------|---------------------|------|
| **rhizoCrypt** | DAG / Provenance | `dag.*` | Ephemeral session-scoped directed acyclic graphs, Merkle proofs. Tracks causal relationships between events. |
| **loamSpine** | Ledger / History | `entry.*`, `ledger.*` | Append-only immutable ledger. Linear history with inclusion proofs and certificates. |
| **sweetGrass** | Attribution | `attribution.*` | Semantic attribution — content braids, contribution tracking, convergence scoring. |

### Tooling

Ecosystem tools (gen2.5) — standalone crates or CLIs consumed by primals, springs, or
infrastructure. Not long-running IPC services. See `PRIMAL_SPRING_GARDEN_TAXONOMY.md`
for the full taxonomy.

| Tool | Domain | Location | Role |
|------|--------|----------|------|
| **sourDough** | Scaffolding / Meta | `primals/` | The starter culture. Scaffolds new primals with inlined DNA (traits, workspace, standards). Validates primal structure. Packages genomeBin artifacts. Reference implementation for UniBin, ecoBin, JSON-RPC IPC. Generated primals have no runtime dependency on sourDough. |
| **bingoCube** | Crypto Commitment | `primals/` | Human-verifiable cryptographic commitment system. BLAKE3 two-board cross-binding with progressive reveal. Nautilus evolutionary reservoir computing. Consumed by BearDog (identity), Songbird (peer trust), NestGate (content fingerprinting), ToadStool (computation proofs). |
| **benchScale** | Lab Substrate | `infra/` | Pure Rust laboratory substrate for distributed system testing. VM provisioning, topology management, network simulation. v3.0.0 production. 22K lines. |
| **agentReagents** | VM Image Builder | `infra/` | Template-driven VM image builder for gate provisioning. Depends on benchScale for the underlying substrate. Cloud-init, PCI passthrough, COSMIC desktop templates. |
| **rustChip** | NPU Characterization | `sort-after/` | BrainChip Akida NPU register-level driver, model format parser, benchmarks. Extracted from toadStool metalForge, evolves via hotSpring. Pure Rust, no C++ SDK. Symbiotic exception with BrainChip. |

### Defense

| Primal | Domain | Capability Namespace | Role |
|--------|--------|---------------------|------|
| **skunkBat** | Thymus / Immune | `security` | Defensive network security primal. Reconnaissance, threat detection (5 types), graduated defense, security observability. JSON-RPC IPC server with BTSP Phase 1, Wire Standard L2/L3. Metadata-only, no content inspection. |

---

## Atomic Compositions

Primals compose into standard deployment units:

| Composition | Members | Purpose |
|-------------|---------|---------|
| **Tower Atomic** | BearDog + Songbird | Security + Network foundation. Minimum viable base for any deployment. |
| **Node Atomic** | Tower + toadStool (+ barraCuda, coralReef) | Adds compute/hardware dispatch to Tower. |
| **Nest Atomic** | Tower + NestGate | Adds storage/permanence to Tower. |
| **NUCLEUS Complete** | Tower + Node + Nest + Squirrel + petalTongue | Full deployment with all atomics + AI + visualization. |
| **Provenance Overlay** | rhizoCrypt + loamSpine + sweetGrass | Data integrity layer. Composes on top of any atomic. |

---

## Interaction Rules

### How primals discover each other

1. Every primal registers its capabilities with **biomeOS** Neural API on startup.
2. Primals discover services by **capability domain** (e.g., "who provides `crypto.sign`?"), never by primal name.
3. Socket paths follow `$XDG_RUNTIME_DIR/biomeos/<primal>.sock`. Domain symlinks (e.g., `security.sock -> beardog.sock`) are encouraged.
4. See `CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.2 for the full standard.

### How primals communicate

1. **Protocol**: JSON-RPC 2.0, newline-delimited framing.
2. **Transport**: UDS (primary) + TCP (secondary, for remote/mobile). `server --port <PORT>` binds TCP.
3. **Health**: Every primal implements `health.liveness`, `health.readiness`, `health.check`.
4. See `PRIMAL_IPC_PROTOCOL.md` v3.1 for wire format and transport details.

### What a primal must NOT do

1. **Import code from another primal.** Each primal is a sovereign workspace. Share patterns via wateringHole, not crate dependencies.
2. **Hardcode another primal's name in routing code.** Use capability discovery.
3. **Implement functionality outside its domain.** If you need crypto, call BearDog. If you need storage, call NestGate. See the Concern Matrix below.
4. **Depend on C libraries** in the default build (ecoBin compliance). Feature-gate any C deps.

---

## Concern Matrix

Legend:
- **OWNS** — Canonical provider for this concern
- **DELEGATES** — Should call the owner via IPC
- **OVERSTEP** — Currently implements locally but should delegate
- **EXTENDS** — Meta-tier primal that augments this concern
- **N/A** — Not relevant
- **(resolved)** — Was overstep, now cleaned

| Concern | BearDog | Songbird | NestGate | toadStool | coralReef | barraCuda | biomeOS | Squirrel | petalTongue | rhizoCrypt | loamSpine | sweetGrass | sourDough |
|---------|---------|----------|----------|-----------|-----------|-----------|---------|----------|-------------|------------|-----------|------------|-----------|
| **Crypto / Signing** | **OWNS** | (resolved) | OVERSTEP | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| **Network / Transport** | OVERSTEP | **OWNS** | OVERSTEP | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| **Discovery / Registry** | OVERSTEP | DELEGATES | OVERSTEP | (resolved) | N/A | N/A | **OWNS** | N/A | N/A | N/A | N/A | N/A | N/A |
| **Storage / Permanence** | N/A | OVERSTEP | **OWNS** | N/A | N/A | N/A | N/A | OVERSTEP | N/A | N/A | N/A | N/A | N/A |
| **AI / Inference** | OVERSTEP | N/A | OVERSTEP | (resolved) | N/A | N/A | N/A | **OWNS** | N/A | N/A | N/A | N/A | N/A |
| **Compute / GPU** | N/A | N/A | N/A | **OWNS** | (deferred) | DELEGATES | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| **Shader Compile** | N/A | N/A | N/A | DELEGATES | **OWNS** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| **Math / Numerical** | N/A | N/A | N/A | N/A | N/A | **OWNS** | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| **Orchestration** | N/A | N/A | OVERSTEP | (resolved) | N/A | N/A | **OWNS** | N/A | N/A | N/A | N/A | N/A | N/A |
| **Visualization** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | **OWNS** | N/A | N/A | N/A | N/A |
| **Hardware Inventory** | N/A | N/A | N/A | **OWNS** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| **DAG / Provenance** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | **OWNS** | N/A | N/A | N/A |
| **Ledger / History** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | **OWNS** | N/A | N/A |
| **Attribution** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | **OWNS** | N/A |
| **Capability Reg.** | DELEGATES | DELEGATES | DELEGATES | DELEGATES | DELEGATES | DELEGATES | **OWNS** | DELEGATES | DELEGATES | DELEGATES | DELEGATES | DELEGATES | N/A |
| **Scaffolding** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | **OWNS** |

---

## Overstep Detail

### NestGate (most overstep — oldest primal)

| Area | Module | Delegate To | Status |
|------|--------|-------------|--------|
| Crypto | `nestgate-security` | BearDog `crypto.*` | Partially resolved — `CryptoDelegate` wired (NG-05), but crate still exists |
| Discovery | `nestgate-discovery` | biomeOS Neural API | Deprecated modules marked, 7 files remain |
| Network | `nestgate-network` | Songbird `net.*` | Still present |
| AI / MCP | `nestgate-mcp` | Squirrel via biomeOS | Still present |
| Orchestration | `nestgate-automation` | biomeOS graph execution | Still present |

### BearDog

| Area | Module | Delegate To | Status |
|------|--------|-------------|--------|
| HTTP REST | `beardog-integration` | Songbird (network domain) | Still present |
| mDNS discovery | `beardog-discovery` | biomeOS Neural API | Still present |
| AI optimization | `beardog-utils/ai_optimization` | Squirrel | Feature-gated behind `ai` feature (11.9K LOC) |
| Deploy orchestration | `beardog-deploy` | biomeOS deploy graphs | Still present |

### Songbird

Wave 102: major capability-based migration. All `beardog_*` → `security_*`, `squirrel_*` → `coordination_*`, `nestgate` → `storage_provider`, `toadstool` → `compute_provider`.

| Area | Module | Delegate To | Status |
|------|--------|-------------|--------|
| App crypto | JWT, checkpoints | BearDog `crypto.*` | **Resolved** (wave 89) — delegates with fallback |
| TLS record crypto | `songbird-tls` | BearDog `crypto.aead_*` | **Resolved** (wave 89) |
| Embedded persistence | `sled` in orchestrator | NestGate `storage.*` | Pending — blocked on NestGate storage API |
| Discovery naming | primal-named structs/modules | capability-domain names | **In progress** (wave 102) — 42% ref reduction, trajectory strong |

### toadStool

Major overstep resolved in S169 (-10,659 lines). Remaining:

| Area | Module | Delegate To | Status |
|------|--------|-------------|--------|
| coralReef discovery | `capability.discover("shader")` | Songbird ecosystem registration | **RESOLVED** (TS-01, Iter 65+) |
| Security sandbox | `toadstool-security-sandbox` | BearDog or OS sandbox | Open |

### Squirrel

| Area | Module | Delegate To | Status |
|------|--------|-------------|--------|
| Persistence | `sled`/`sqlx` | NestGate `storage.*` | Still present — broader than "cache only" |
| Crypto | `ed25519-dalek`/TLS | BearDog `crypto.*` | Still present |

---

## Capability Routing Guide

When composing primals via biomeOS deploy graphs, route by capability domain:

| Need | Capability Domain | Owner | Never Route To |
|------|-------------------|-------|----------------|
| Sign/verify/hash | `crypto.*` | BearDog | NestGate (overstep) |
| Network transport | `net.*` | Songbird | NestGate, BearDog (overstep) |
| Persist data | `storage.*` | NestGate | Songbird sled, Squirrel sled (overstep) |
| GPU compute | `compute.*`, `ember.*` | toadStool | — |
| Compile shaders | `shader.*` | coralReef | toadStool (delegates) |
| Math/tensors | `math.*` | barraCuda | — |
| AI inference | `ai.*` | Squirrel | BearDog AI tree, NestGate MCP (overstep) |
| Render/visualize | `visualization.*`, `interaction.*` | petalTongue | — |
| Orchestrate | `capability.*`, `graph.*`, `topology.*` | biomeOS | NestGate automation (overstep) |
| DAG provenance | `dag.*` | rhizoCrypt | — |
| Ledger history | `entry.*`, `ledger.*` | loamSpine | — |
| Attribution | `attribution.*` | sweetGrass | — |
| Scaffold new primal | CLI (`sourdough scaffold`) | sourDough | — |

Deploy graphs should **never** route a concern to a primal listed as OVERSTEP. Use
`required = false` for graceful degradation when the owning primal is unavailable.

---

## Compliance Status (April 3, 2026 — primalSpring audit)

| Primal | Clippy | Fmt | Tests | Discovery | Key Debt |
|--------|--------|-----|-------|-----------|----------|
| biomeOS | CLEAN | PASS | PASS | **C** | — |
| BearDog | CLEAN | PASS | PASS (14.4K) | **C** | Overstep: HTTP, mDNS, AI tree (feature-gated) |
| Songbird | CLEAN | PASS | PASS (8.9K) | **P→C** (935 refs) | Wave 109: 63% total discovery reduction (2558→935) |
| NestGate | CLEAN | PASS | PASS (11.3K) | **P→C** | EnvSource injection, automation+network deprecated, -15K lines |
| toadStool | **FAIL** | PASS | PASS (6.5K) | **P** | TS-01 RESOLVED; clippy regression (aes_gcm deprecated) |
| petalTongue | CLEAN | PASS | PASS (6K) | **P→C** | PT-04/06 resolved; discovery renames landed |
| Squirrel | CLEAN | PASS | PASS (6.9K) | **P** | Build FIXED (alpha.36); sled/crypto overstep |
| rhizoCrypt | CLEAN | PASS | PASS | **C** | — |
| loamSpine | CLEAN | PASS | PASS | **C** | `--port` alias shipped (v0.9.15); public chain anchor (v0.9.16) |
| sweetGrass | 1 warn | PASS | PASS | **C** | Missing `--port` alias |
| barraCuda | CLEAN | PASS | PASS (4.4K) | n/a | All quality gates green; 4,366 tests; LD-05/LD-10 resolved |
| sourDough | CLEAN | PASS | PASS (239) | **C** | Missing `deny.toml`; musl/signing |
| coralReef | CLEAN | PASS | PASS (4.5K) | **C** | Iter 80 — 4,477 tests, wire contract documented, CompilationInfo IPC, BTSP Phase 2, deny.toml enforced, zero clippy/doc warnings |
| skunkBat | CLEAN | PASS | PASS (124) | **C** | IPC server, BTSP Phase 1, Wire L2/L3. Zero hardcoded primal names. |

**Discovery legend**: **C** = compliant, **P** = partial, **X** = non-compliant

---

## Related Standards

- **`PRIMAL_SELF_KNOWLEDGE_STANDARD.md` v1.0.0** — Defines the
  self-knowledge boundary, capability domain registry (mirrors this
  matrix's primal directory), and concrete code patterns for how primals
  organize for capability-based interaction. The canonical reference for
  socket naming, env var conventions, and migration phasing.

---

## Version History

- **V1.0** (March 30, 2026): Initial matrix from ludoSpring V35.3 ecosystem review
- **V2.0** (March 31, 2026): Expanded with 32-gap registry, toadStool S169 resolution, tiered actions
- **V2.1** (March 31, 2026): 10 gaps resolved post-pull
- **V2.2** (April 1, 2026): Deep per-primal validation, LS-03/RC-01 resolution
- **V2.3** (April 2, 2026): primalSpring re-audit, overstep scan
- **V3.0** (April 3, 2026): **Major restructure.** Added Primal Directory with clear role definitions and capability namespaces. Added sourDough and skunkBat. Added Interaction Rules section. Restructured Concern Matrix with sourDough column and resolved status markers. Added Capability Routing Guide for deploy graph design. Updated compliance table with measured audit data (primalSpring full scan). Simplified overstep detail. Designed for human and AI agent comprehension.
