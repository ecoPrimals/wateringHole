# ecoPrimals Ecosystem Blurb — Wave 157g ENMESH

**Date**: Aug 10, 2026 3:24PM | **Wave**: 157g | **From**: overwatch (gate-agnostic)
**Posture**: **OVERWATCH RETOOLED. FRONTLOADING PIPELINE WORK.** Overwatch is now a gate-agnostic position (not tied to eastGate). `overwatch-temporal.sh` sweeps all 43 repos across 4 Forgejo orgs via HTTPS API — runs from any gate. primalSpring is the eastGate-resident code + deployment team (separated from overwatch). **Previous wave achievements absorbed**: P1 braid.verify SHIPPED, P2 process leak CLOSED, content.stat CLOSED, NUCLEUS biome.yaml manifest SHIPPED, gossip injection 3/16 LIVE, cellMembrane 13-commit evolution, WASM 38/48. **Now frontloading**: pipeline enmeshment work — sourDough CI, cross-gate gossip, songBird MeshRelay, manifest convergence. Then spring teams activate.

---

## COMPOSITION GRAPH FOUNDATION — Frontloaded Before Springs

### Critical Findings — Status After Team Response

| Finding | Status | Detail |
|---------|--------|--------|
| **swarmVine socket discovery** | **OPEN** — gate ops fix pending | biomeOS connects `.tarpc.sock` instead of JSON-RPC `.sock`. Config issue. |
| **`sourdough validate` not in golgi CI** | **OPEN** — sporeGate + sourDough | 12 validators exist, none wired into post-receive hook |
| **Cross-gate gossip peers unreachable** | **OPEN** — TCP 7800 reachability | `SWARMVINE_PEERS` set but peers not reachable |
| **~~No primal injects gossip~~** | **RESOLVED** — 3 primals LIVE | rhizoCrypt (3 DAG events), loamSpine (4 spine events), lithoSpore (4 validation events). barraCuda spec'd (20 keys, hooks pending). Ant colony has scouts. |
| **~~`braid.verify` missing~~** | **RESOLVED** — sweetGrass `6357f0f` | Method #48. Content integrity + Ed25519 (bearDog) + ledger (loamSpine). Capability-registered. Needs behavioral tests. |
| **~~`content.stat` routing gap~~** | **RESOLVED** — nestGate `60ee88d8` | HTTP transport parity: content.stat/ingest/query/fetch + dataset.convergence all wired |
| **~~Process leak ~36/hr~~** | **RESOLVED** — coralReef `18b9a68` | RAII ChildGuard + AsyncChildGuard on all test spawn sites. Production spawns zero children. |
| **NUCLEUS manifest** | **SHIPPED** — toadStool S375 | `biome.yaml` v1: Tower/Nest/Node sub-graphs, dependency ordering, readiness gates, gossip events, federation. **Execution stubbed** — 4 divergent BiomeManifest structs need convergence. |
| **songBird MeshRelay** | **OPEN** — not yet shipped | Cross-gate gossip relay through `:7700` mesh |

### Subwave Plan — Status After Team Response

| Team | Assigned | Result |
|------|----------|--------|
| **sweetGrass** | `braid.verify` atomic | **DONE** — method #48, capability-registered. P1→P2 (needs behavioral tests). |
| **coralReef** | Process leak fix | **DONE** — RAII guards on all spawn sites. P2 CLOSED. Also: GEMM Phase 2 IPC wired (`tiling` param), SM20 coverage, 3,963 tests (+147). |
| **nestGate** | Routing gaps | **DONE** — HTTP transport parity. `content.stat` gap CLOSED. `dataset.convergence` endpoint shipped. |
| **toadStool** | `biome.yaml` manifest | **DONE** — S375: v1 schema with compositions, dependency ordering, readiness gates. S376: WASM 38/48, Tokio blast radius. 9.1 GiB reclaimed. |
| **rhizoCrypt** | Gossip injection | **DONE** — 3 DAG lifecycle events via `gossip.spread`. Conditional, zero-cost when absent. |
| **loamSpine** | Gossip injection | **DONE** — 4 spine events (`cas.have`, `braid.head`, `spine.sealed`, `anchor.published`) via `gossip.inject` UDS. |
| **barraCuda** | Gossip injection + GEMM | **SPEC** — 20 gossip keys documented in registry, hooks pending. Sovereign GEMM executor bridge shipped. |
| **lithoSpore** | Gossip injection | **DONE** — 4 validation events via `gossip.spread`. Registry says "not wired" but code IS live (needs registry sync). |
| **cellMembrane** | Evolution wave | **DONE** — 13 commits: HealthCheckMethod wired, G69 Phase 1+2+3 complete, mesh builder Tower Atomic, 6 jelly strings excised, chrono→time, 0 clippy, 1353 tests. |
| **hotSpring** | QCD campaign | **DONE** — 18 commits: arxiv analysis Rust pipeline, production campaign, AMD 18.5x, 105 configs, SU(3) measurement battery. |
| **whitePaper** | Paper integration | **DONE** — 13 commits: ant colony pattern, atomic compositions, measurement battery, silicon exploration, novelty sections. |
| **esotericWebb** | Vertebrate self-audit | **DONE** — V32b: crypto.sign base64 fix (P0-A real Ed25519 active), biomeOS FD bypass, 28 capabilities verified, LimitNOFILE=65536. |
| **5 springs** | toadStool workload dispatch | **DONE** — health/ground/ludo/neural/airSpring all received workload dispatch TOML specs from projectNUCLEUS. |
| **sporeGate + sourDough** | sourDough CI wiring | **OPEN** — not yet pushed |
| **songBird** | MeshRelay for gossip | **OPEN** — not yet pushed |
| **biomeOS** | Socket discovery fix | **OPEN** — not yet pushed |
| **primalSpring** | Modernization | **OPEN** — next priority |

---

## THREE-PILLAR ARCHITECTURE

### Pillar 1: Neural API as Composition Graph Executor — The Brain

**Goal (G70)**: NUCLEUS is a **graph of sub-graphs**. Each atomic composition (Tower, Nest, Node) is a sub-graph with internal dependency ordering. biomeOS graph executor starts compositions, routes through them, and orchestrates multi-step workflows.

**Key insight**: A primal can appear in multiple compositions. songBird is Tower Atomic today, may be in a future "Federation Atomic." Compositions are graphs — primals are nodes — same node, multiple graphs. `biome.yaml` = composition manifest (BYOB per gate). toadStool's CLI change to require `biome.yaml` is the right direction.

**primalSpring** is the experimental ground for these compositions. It needs heavy modernization to: (1) prototype the NUCLEUS `biome.yaml` manifest, (2) validate composition start/stop lifecycle, (3) lead future spring composition patterns.

| Item | Status | Next |
|------|--------|------|
| `capability.call` routing | **OPERATIONAL** (1.3ms / 4ms) | Route through composition context, not flat primals |
| `biome.yaml` manifest | **SHIPPED** (toadStool S375 — v1 schema) | Converge 4 divergent BiomeManifest structs → 1 canonical in `toadstool-core`. primalSpring consumes. |
| swarmVine socket discovery | **CONFIG FIX** — pending biomeOS + gate ops | Wire sourDough CI to prevent recurrence |
| Routing gaps | **1 remaining** (`spine.list`). `content.stat` **CLOSED** (nestGate `60ee88d8`). | biomeOS translation registry for spine.list |
| `braid.verify` | **SHIPPED** (sweetGrass `6357f0f`) | P2: needs behavioral tests (content-integrity is format-check only, crypto-down case permissive) |
| Gossip injection | **3/16 primals LIVE** (rhizoCrypt, loamSpine, lithoSpore). 1 spec'd (barraCuda). | Remaining primals identify injection points. Cross-gate reachability. |
| Cross-gate routing | **BLOCKED** — gossip peers unreachable, songBird MeshRelay pending | TCP 7800 reachability + MeshRelay |
| Composition lifecycle | **SCHEMA SHIPPED** — execution stubbed | primalSpring prototypes `nucleus.start` with dependency ordering |

### Pillar 2: Data Federation — The Nervous System

**Goal**: Data flows across gates via CAS federation, provenance braiding, and gossip. Every object has lineage, every computation has proof.

| Item | Owner | Status | Next |
|------|-------|--------|------|
| Provenance chain | Provenance Trio | **VERIFIED** (86/87 pen test) | Wire `braid.verify` for atomic verification |
| CAS federation | nestGate + petalTongue | **LIVE** (`content.replicate` cross-gate) | L1 cache on golgi for hot objects |
| Jelly string elimination | fleet-wide | **9+ ELIMINATED** (cellMembrane excised 6 more this wave) | Remaining: `native_braid.py` (1,259 LOC) + biomeOS graph executor targets |
| `native_braid.py` → Rust | cellMembrane + westGate | **LAST MAJOR JELLY** | `membrane content.braid` (1,259 LOC Python → Rust) |
| Signed spine commits | bearDog + loamSpine | **LIVE on westGate** | Fleet-wide deployment |
| Depot lineage | cellMembrane + sporeGate | **G69 Phase 1+2+3 WIRED** | CAS archival operational in harvest pipeline |

### Pillar 3: Pepti Layer — The Skeleton

**Goal**: Deployment is solved. golgiBody is the thin relay. Sub-builders compile. Gates pull. Auto-prune keeps it clean.

| Item | Owner | Status |
|------|-------|--------|
| Depot unified | sporeGate | **DONE** — canonical path, Caddy-direct, no symlinks |
| Auto-prune | cellMembrane | **DONE** — non-registry binaries removed on every harvest |
| Disk health guard | sporeGate | **DONE** — warns 80%, blocks 90% |
| CAS archival (G69 Phase 3) | sporeGate | **WIRED** — sign→spine→braid→CAS before overwrite |
| Sub-builder fleet | blueGate (primary), sporeGate, eastGate, darwinGate (enrolling) | **LIVE** |
| Process management | All gates | ~~P2 process leak~~ **RESOLVED** — coralReef RAII guards (`18b9a68`). Test-only; production spawns zero children. |

---

## IMMEDIATE WORK — Pipeline Enmeshment

### Primal Pipeline (code teams — frontloaded)

| Priority | Goal | Owner | Effort |
|----------|------|-------|--------|
| **HIGH** | **Wire sourDough validate into golgi CI** | sporeGate + sourDough | Days — `convergence` + `rpc-surface` in post-receive hook |
| **HIGH** | **Fix swarmVine socket discovery** | biomeOS + gate ops | Hours — biomeOS connects wrong socket (JSON-RPC exists) |
| **HIGH** | **Gossip mesh enmeshment** | All gates | Hours — TCP 7800 cross-gate reachability verification |
| **HIGH** | **songBird MeshRelay for gossip** | songBird | Days — relay gossip through `:7700` when TCP fails |
| **HIGH** | **Manifest convergence** | toadStool + biomeOS | Days — 4 divergent BiomeManifest structs → 1 canonical `toadstool-core` |
| **MED** | **`nucleus.start` sub-graph executor** | biomeOS | Days — consume toadStool manifest, start sub-graphs with dep ordering |
| **MED** | **Remaining gossip injection** | barraCuda + others | Days — barraCuda 20 keys spec'd, hooks pending |
| **MED** | **`spine.list` routing gap** | biomeOS | Hours — last known routing gap |
| **MED** | **`braid.verify` behavioral tests** | sweetGrass | Days — P2: content-integrity format-check only, crypto-down permissive |
| **LOW** | **lithoSpore registry sync** | lithoSpore | Hours — capability_registry.toml stale ("not wired" but code IS live) |

### primalSpring Team (eastGate — code + deployment)

| Priority | Goal | Effort |
|----------|------|--------|
| **HIGH** | **Modernization**: consume `biome.yaml` manifest, prototype composition start/stop lifecycle | Sprint |
| **MED** | Lead future spring composition patterns for downstream springs | Ongoing |
| **MED** | eastGate depot validation — confirm 157e deploy is healthy | Hours |

### Overwatch (gate-agnostic — coordination)

| Priority | Goal | Effort |
|----------|------|--------|
| **DONE** | `overwatch-temporal.sh` — Forgejo API sweep, 43 repos, 4 orgs | Shipped |
| **DONE** | Role split: overwatch (floats) vs primalSpring (eastGate code+deploy) | Documented |
| **NEXT** | Adopt Phase B impulse-driven workflow (read impulses, not manual fetch) | Days |
| **NEXT** | As gates enmesh, test overwatch from other gates (ironGate via browser?) | Weeks |

### Production Campaign (science pipeline)

| Priority | Goal | Owner | Status |
|----------|------|-------|--------|
| **MED** | QCD campaign | strandGate + hotSpring | **IN PROGRESS** — 105 configs, AMD 18.5x |
| **MED** | Science pipeline E2E (G71) | strandGate + ironGate + sporePrint | NFT endpoint, pseudoSpore, QCD page |

## AFTER ENMESHMENT — Springs + Protokarya Spin-Up

**Sequence**: Pipeline enmeshment (sourDough CI, gossip mesh, MeshRelay, manifest convergence) → primalSpring validates composition patterns on eastGate → gates enmesh → overwatch floats to wherever needed → spring teams activate → downstream protokarya teams activate.

**Overwatch can now coordinate from any gate.** As gates enmesh, overwatch may move to ironGate (via nestgate.io browser surface), or run from multiple gates simultaneously. primalSpring drives code + deployment from eastGate. These roles are independent.

### Gate Enmeshment Targets (for science surface)

| Gate | Mesh Role | Science Surface |
|------|-----------|-----------------|
| **westGate** | Data NAS + provenance | AlphaFold, braided datasets, CAS federation |
| **ironGate** | Downstream host + NFT | esotericWebb, footPrint, pseudoSpore bundles |
| **southGate** | Validation + compute | Performance canary, GPU available for QCD |
| **strandGate** | GPU estate + science | Production campaign, cross-vendor GPU, Silicon Fold |

### Spring Teams (activate after gossip mesh works)

| Spring | Gate | Workload | Dependency |
|--------|------|----------|------------|
| **hotSpring** | strandGate | QCD campaign → arXiv pseudoSpore | Production campaign must complete |
| **tideGlass** | westGate | Cell 2026 rebuild → NF drug screen | CAS federation, Neural API routing |
| **esotericWebb** | ironGate | CRPG browser surface | petalTongue WebGL pipeline (G19) |
| **footPrint** | ironGate | GIS agent panel | squirrel + petalTongue wiring |
| **sporePrint** | golgi | QCD page, download routes, LaTeX→web | strandGate campaign data |
| **wetSpring** | westGate | 16S rRNA sovereign pipeline | toadStool dispatch, CAS |

### Downstream Protokarya (activate after springs prove surface)

8 spring workloads already arrived (toadStool dispatch TOML pattern). Science surface provides the substrate for:
- **SunMemo paper** — needs strandGate GPU surface + westGate data braids + sporePrint publishing
- **NF drug screen** (Gonzales/Bin) — tideGlass on westGate CAS federation
- **CTF NDU grant** — pseudoSpore artifact from NF screen

## NEAR-TERM — Next Wave Focus

| Goal | Owner | Description |
|------|-------|-------------|
| **Science pipeline E2E (G71)** | strandGate + ironGate + sporePrint | NFT registration, pseudoSpore bundles, QCD page |
| **Graph executor workflows** | biomeOS | Multi-step compositions. Eliminate remaining jelly strings (last major: `native_braid.py` 1,259 LOC). |
| **shader.compile.wgsl** | barraCuda → coralReef | General shader compilation via IPC |
| **WASM push (38→48)** | toadStool | 38/48 (79%). Remaining 10 irreducibly native (daemon, container, display, sandbox, tests). Compute kernel ceiling reached. |
| **WebGL pipeline** | petalTongue + esotericWebb | G19 browser surfaces |
| **ludoSpring extraction** | petalTongue | `doom-core` → new spring |

## GLACIAL

| Goal | Status |
|------|--------|
| arXiv 41/42 | Campaign IN PROGRESS (hotSpring 18 commits, 105 configs, AMD 18.5x). `validate.sh` → Rust. Reviewer send. |
| `native_braid.py` → Rust | Last major jelly string (1,259 LOC) |
| Inner Membrane Phase 4 | Pure primal communication — WG deprecation |
| aarch64-musl depot | 13/19, no ARM64 gates active |
| darwinGate (M4 Mac Mini) | Manifest registered, pending `gate.bootstrap` |
| southGate mesh enrollment | LAN discovery pending |
| steamGate | Future platform gate |
| PrecisionBrain routing | barraCuda Fp64→F16 silicon-aware dispatch |
| PTX SM120 / Blackwell | coralReef next-gen NVIDIA target |
| Vertex/Fragment shaders | coralReef 8-12 week graphics pipeline |

---

## GATE STATUS — 6/6 NUCLEUS — ALL 157e DEPLOYED

| Gate | Services | Key capability |
|------|----------|---------------|
| **sporeGate** | **15/15** | Depot authority. Pepti layer. CAS archival. 7 jelly strings excised. |
| **strandGate** | **7/7** | Silicon Fold. Production campaign IN PROGRESS (hotSpring 105 configs cached). 2 GPUs active. |
| **westGate** | **14/14** | Data NAS. Signed spine commits. Braid pen test 86/87. Pipeline Rust-native. |
| **blueGate** | **13/13** | Primary builder. `:9800` validated. golgi SSH. Windows native. |
| **southGate** | **13/13** | Canary PASS. 17,595 conn/s. 0.057ms. No regression. |
| **ironGate** | **13/13** | Downstream host. 166 caps. Vine-bat. 12.7 TB CAS. |
| **eastGate** | overwatch + primalSpring | Overwatch (gate-agnostic, can float). primalSpring (code + deploy, eastGate-resident). |

---

## PEPTI-LAYER DOCTRINE

**golgiBody** = peptidoglycan relay. HEAD-only depot. All-arch. Never compiles. Sub-builders push; gates pull.

| Target | Sub-builder | Status |
|--------|-------------|--------|
| `x86_64-unknown-linux-musl` | sporeGate | **LIVE** |
| `x86_64-unknown-linux-gnu` | sporeGate | **LIVE** |
| `x86_64-pc-windows-gnu` | blueGate | **LIVE** |
| `aarch64-unknown-linux-musl` | eastGate (cross) | **PARTIAL** |
| `aarch64-apple-darwin` | darwinGate (M4) | **ENROLLING** |

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| Primals | **16** |
| NUCLEUS gates | **6/6** — all 157e deployed |
| P0 / P1 / P2 | **0 / 0 / 2** (P2: petalTongue port, braid.verify behavioral tests). P1 `braid.verify` SHIPPED → P2. P2 process leak CLOSED. |
| Deploy | **COMPLETE** — pepti layer + sub-builders + auto-prune + CAS archival + G69 Phase 1+2+3 |
| Braid pen test | **86/87 PASS** — `braid.verify` atomic now exists (sweetGrass method #48) |
| Gossip injection | **3/16 primals LIVE** (rhizoCrypt, loamSpine, lithoSpore). 1 spec'd (barraCuda). Ant colony has scouts. |
| Jelly strings | **9+ eliminated** (cellMembrane excised 6 more this wave). Remaining: `native_braid.py` (1,259 LOC), biomeOS graph executor targets. |
| WASM | **38/48** (79%) — compute kernel ceiling. Remaining 10 irreducibly native. |
| NUCLEUS manifest | **SHIPPED** — `biome.yaml` v1 (toadStool S375). Schema exists; execution pending. |
| Performance | **17,595 conn/s, 0.057ms** — no regression from 157a |
| Production campaign | **IN PROGRESS** — hotSpring 18 commits, 105 configs cached, AMD 18.5x all production sizes |
| cellMembrane | **13-commit evolution** — HealthCheckMethod, G69 complete, mesh builder Tower Atomic, 0 clippy |
| coralReef | **3,963 tests** (+147). GEMM Phase 2 IPC. SM20 encoder. BTSP recovery. |
| Tests | **~150K+** across 16 primals + gardens + springs |

---

*Wave 157g — OVERWATCH RETOOLED + ENMESH. Overwatch is gate-agnostic (overwatch-temporal.sh sweeps 43 repos via Forgejo API). primalSpring = eastGate code+deploy team (separated). All previous closures absorbed: braid.verify, process leak, content.stat, biome.yaml manifest, gossip 3/16. Frontloading pipeline enmeshment: sourDough CI, gossip mesh, songBird MeshRelay, manifest convergence. Then springs activate. 0 P0. 0 P1. 2 P2. 6/6 gates. ~150K+ tests.*
