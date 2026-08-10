# ecoPrimals Ecosystem Blurb — Wave 157g CROSS-GATE GOSSIP LIVE

**Date**: Aug 10, 2026 5:17PM | **Wave**: 157g | **From**: overwatch (gate-agnostic)
**Posture**: **4-GATE GOSSIP MESH LIVE.** Cross-gate epidemic propagation confirmed: westGate → sporeGate, eastGate, strandGate within one 30s cycle. ironGate listening + reachable, not yet peered. blueGate blocked (Windows), southGate not enmeshable (upstream). **sourDough CI SHIPPED** (4 static validators in golgi post-receive, advisory). **Manifest convergence DONE** (toadStool S377: 5→2 BiomeManifest structs). **Tokio vestigial segmentation** (toadStool S378: ~35k LOC feature-gated behind `legacy-*`, 118→~85 tokio files — primordial pre-biomeOS scaffolding excised). **primalSpring biome.yaml consumption DONE** (composition module, exp122 37/37 PASS). **`spine.list` routing gap CLOSED.** Socket discovery FIXED on ironGate + sporeGate. **Remaining**: depot rebuild for gossip binaries, songBird MeshRelay for blueGate/southGate, full bidirectional peering, Tokio long-tail in toadStool (~85 files of real async remain).

---

## COMPOSITION GRAPH FOUNDATION — Frontloaded Before Springs

### Critical Findings — Status After Enmeshment Wave

| Finding | Status | Detail |
|---------|--------|--------|
| **~~swarmVine socket discovery~~** | **FIXED** — ironGate + sporeGate | ironGate: songbird-register.sh expanded to 11 primals, restart ordering fixed. sporeGate: `BIOMEOS_RUNTIME_DIR` path mismatch corrected. |
| **~~sourDough validate not in CI~~** | **SHIPPED** (partial) — cellMembrane `2430a0b` | 4 static validators (transport, ribocipher, platform-substrate, neural-api) in golgi post-receive hook across 15 primal repos. Advisory only. `convergence` + `rpc-surface` (live checks) NOT yet wired. |
| **~~Cross-gate gossip unreachable~~** | **4-GATE MESH LIVE** | westGate → sporeGate, eastGate, strandGate: epidemic propagation confirmed. ironGate listening + reachable, not yet peered. blueGate CLOSED (Windows). southGate not enmeshable. |
| **~~Manifest convergence~~** | **DONE** — toadStool S377 | 5→2 BiomeManifest structs. Canonical in `toadstool-core`, CLI bridge via `From`. All consumers converged. |
| **~~primalSpring biome.yaml~~** | **DONE** — composition module shipped | `config/biome-eastgate.yaml`: 14 primals, 3 compositions. `nucleus_launcher --biome` + reconcile wired. exp122 37/37 PASS. |
| **~~`spine.list` routing gap~~** | **CLOSED** | primalSpring handoff confirms gap closed. |
| **songBird MeshRelay** | **OPEN** — not yet shipped | Needed for blueGate (Windows, no swarmVine) + southGate (different subnet, WG OFF) |
| **Depot rebuild needed** | **OPEN** — sporeGate | Current depot predates gossip injection + MeshRelay binaries. Gates need fresh depot. |
| **Tokio vestigial excision** | **IN PROGRESS** — toadStool S378 | ~35k LOC feature-gated behind `legacy-*`. 118→~85 tokio files. ~85 remain (real async deployment layer). |

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
| **cellMembrane** | sourDough CI wiring | **DONE** — `2430a0b`: 4 static validators in golgi post-receive (15 repos, advisory). `convergence`+`rpc-surface` live checks still needed. |
| **toadStool** | Manifest convergence | **DONE** — S377: 5→2 BiomeManifest structs. All consumers use canonical. |
| **toadStool** | Tokio vestigial segmentation | **DONE** — S378: ~35k LOC feature-gated behind `legacy-*`. 118→~85 tokio files. 9.6+13.1 GiB reclaimed. |
| **ironGate** | Socket fix + enmesh | **DONE** — songbird-register.sh 11 primals, restart ordering fixed, 170 caps. TCP 7800 listening. |
| **sporeGate** | Pipeline enmeshment | **DONE** — Socket discovery fix (`BIOMEOS_RUNTIME_DIR`), sourDough CI shipped. 3-gate mesh confirmed. |
| **blueGate** | Enmeshment | **BLOCKED** — NUCLEUS alive, 13/13 services, but TCP 7800 closed (no swarmVine on Windows). Needs MeshRelay. |
| **southGate** | Enmeshment | **BLOCKED** — 4 upstream blockers (stale depot, no MeshRelay, WG OFF, no socket fix). Local NUCLEUS 13/13 healthy. |
| **primalSpring** | biome.yaml consumption | **DONE** — composition module, `biome-eastgate.yaml` (14 primals, 3 compositions), `nucleus_launcher --biome`, exp122 37/37 PASS. |
| **songBird** | MeshRelay for gossip | **OPEN** — not yet shipped |

---

## THREE-PILLAR ARCHITECTURE

### Pillar 1: Neural API as Composition Graph Executor — The Brain

**Goal (G70)**: NUCLEUS is a **graph of sub-graphs**. Each atomic composition (Tower, Nest, Node) is a sub-graph with internal dependency ordering. biomeOS graph executor starts compositions, routes through them, and orchestrates multi-step workflows.

**Key insight**: A primal can appear in multiple compositions. songBird is Tower Atomic today, may be in a future "Federation Atomic." Compositions are graphs — primals are nodes — same node, multiple graphs. `biome.yaml` = composition manifest (BYOB per gate). toadStool's CLI change to require `biome.yaml` is the right direction.

**primalSpring** is the experimental ground for these compositions. It needs heavy modernization to: (1) prototype the NUCLEUS `biome.yaml` manifest, (2) validate composition start/stop lifecycle, (3) lead future spring composition patterns.

| Item | Status | Next |
|------|--------|------|
| `capability.call` routing | **OPERATIONAL** (1.3ms / 4ms) | Route through composition context, not flat primals |
| `biome.yaml` manifest | **CONVERGED** (toadStool S377: 5→2 structs) | primalSpring consuming: `biome-eastgate.yaml`, `nucleus_launcher --biome`, exp122 37/37 PASS |
| swarmVine socket discovery | **FIXED** — ironGate + sporeGate | sourDough CI wired (4 static validators, advisory). `convergence`+`rpc-surface` pending. |
| Routing gaps | **0 known** — `spine.list` CLOSED, `content.stat` CLOSED | |
| `braid.verify` | **SHIPPED** (sweetGrass `6357f0f`) | P2: needs behavioral tests |
| Gossip injection | **3/16 primals LIVE** + cross-gate propagation confirmed | westGate → sporeGate/eastGate/strandGate within 30s. ironGate reachable. |
| Cross-gate routing | **4-GATE MESH LIVE** — songBird MeshRelay still needed | blueGate + southGate need MeshRelay (can't do direct TCP 7800) |
| Composition lifecycle | **CONSUMED** — primalSpring modules shipped | `nucleus.start` with dep ordering in exp122. Next: multi-composition workflows. |

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
| **HIGH** | **songBird MeshRelay for gossip** | songBird | Days — relay gossip through `:7700` when direct TCP fails. Needed for blueGate + southGate. |
| **HIGH** | **Depot rebuild with gossip binaries** | sporeGate | Hours — current depot predates gossip injection + MeshRelay. Gates need fresh rebuild. |
| **HIGH** | **Full bidirectional peering** | All gates | Hours — westGate inbound not wired (peers need `192.168.4.149:7800`). ironGate 0 gossip peers. |
| **HIGH** | **sourDough `convergence` + `rpc-surface` in CI** | cellMembrane + sourDough | Days — static validators shipped, live checks still missing from post-receive hook |
| **HIGH** | **Dependency Pandemic Tier 1 (G72)** | All primals | Sprint — pollster in GPU springs (~350 files), trim tokio `["full"]` (3 projects), dead dep removal, version alignment. Stadial shift: shed vestigial deps as compositions close gaps. |
| **MED** | **Remaining gossip injection** | barraCuda + others | Days — barraCuda 20 keys spec'd, hooks pending. Other primals need injection points. |
| **MED** | **`braid.verify` behavioral tests** | sweetGrass | Days — P2: content-integrity format-check only, crypto-down permissive |
| **MED** | **Multi-composition graph workflows** | biomeOS | Days — primalSpring has lifecycle, next: multi-step composition orchestration |
| **LOW** | **lithoSpore registry sync** | lithoSpore | Hours — capability_registry.toml stale ("not wired" but code IS live) |

### primalSpring Team (eastGate — code + deployment)

| Priority | Goal | Effort |
|----------|------|--------|
| ~~**HIGH**~~ | ~~Consume `biome.yaml` manifest~~ | **DONE** — composition module, exp122 37/37 PASS |
| **HIGH** | **Multi-composition orchestration** — extend beyond single-composition start/stop | Sprint |
| **HIGH** | **Dep pandemic assist (G72)** — profile archaic patterns across ecosystem primals, coordinate Tier 1 excision, validate compile-time improvements | Sprint |
| **MED** | Lead future spring composition patterns for downstream springs | Ongoing |

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
| **Dep Pandemic Tier 2 (G72)** | Fleet-wide | HTTP→songBird/capability.call (6+ projects), axum→0.8, wgpu→28, YAML unify, tokio::sync→std::sync audit |
| **Science pipeline E2E (G71)** | strandGate + ironGate + sporePrint | NFT registration, pseudoSpore bundles, QCD page |
| **Graph executor workflows** | biomeOS | Multi-step compositions. Eliminate remaining jelly strings (last major: `native_braid.py` 1,259 LOC). |
| **shader.compile.wgsl** | barraCuda → coralReef | General shader compilation via IPC |
| **WASM push (38→48)** | toadStool | 38/48 (79%). Remaining 10 irreducibly native — dep pandemic may unlock more WASM targets. |
| **WebGL pipeline** | petalTongue + esotericWebb | G19 browser surfaces |
| **ludoSpring extraction** | petalTongue | `doom-core` → new spring |

## GLACIAL

| Goal | Status |
|------|--------|
| **Dependency Pandemic (G72)** | **ACTIVE — STADIAL SHIFT.** Primals shed vestigial deps as compositions close gaps. 664 Cargo.toml audited. Tier 1: pollster in GPU springs, trim tokio `["full"]`, dead deps, version alignment. Tier 2: HTTP→songBird/capability.call, axum→0.8, wgpu→28. Tier 3: sourDough dep validator, archaic pattern excision. See `specs/DEPENDENCY_PANDEMIC_SPEC.md`. |
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

## GATE STATUS — 6/6 NUCLEUS — 4-GATE GOSSIP MESH

| Gate | Services | Gossip | Key capability |
|------|----------|--------|---------------|
| **sporeGate** | **15/15** | **MESH** (3-gate) | Depot authority. sourDough CI. Socket fix. Pipeline enmeshed. |
| **strandGate** | **7/7** | **MESH** (3-gate) | Silicon Fold. Production campaign IN PROGRESS. 2 GPUs active. |
| **westGate** | **14/14** | **MESH** (outbound) | Data NAS. First cross-gate gossip propagation confirmed. Inbound pending peering. |
| **ironGate** | **13/13** | **LISTENING** (0 peers) | Socket fix done. 170 caps. TCP 7800 reachable. Peer config pending. |
| **blueGate** | **13/13** | **BLOCKED** | NUCLEUS alive. TCP 7800 closed. No swarmVine on Windows. Needs MeshRelay. |
| **southGate** | **13/13** | **BLOCKED** | NUCLEUS healthy (canary PASS). 4 upstream blockers. WG OFF. Needs depot rebuild. |
| **eastGate** | overwatch + primalSpring | **MESH** (3-gate) | Overwatch (gate-agnostic). primalSpring: biome.yaml consumption DONE, exp122 37/37. |

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
| P0 / P1 / P2 | **0 / 0 / 2** (P2: petalTongue port, braid.verify behavioral tests). |
| Deploy | **COMPLETE** — pepti layer + sub-builders + auto-prune + CAS archival + G69 Phase 1+2+3 |
| Braid pen test | **86/87 PASS** — `braid.verify` atomic exists (sweetGrass method #48) |
| Cross-gate gossip | **4-GATE MESH LIVE** (sporeGate, eastGate, strandGate, westGate). ironGate reachable. blueGate + southGate blocked. |
| Gossip injection | **3/16 primals LIVE** (rhizoCrypt, loamSpine, lithoSpore). 1 spec'd (barraCuda). Cross-gate propagation confirmed. |
| Jelly strings | **9+ eliminated** (cellMembrane excised 6 this wave). Remaining: `native_braid.py` (1,259 LOC). |
| WASM | **38/48** (79%) — compute kernel ceiling. Remaining 10 irreducibly native. |
| NUCLEUS manifest | **CONVERGED** — `biome.yaml` v1 (toadStool S375+S377: 5→2 structs). primalSpring consuming (exp122 37/37 PASS). |
| Tokio segmentation | **~35k LOC feature-gated** (toadStool S378). 118→~85 tokio files. Primordial pre-biomeOS scaffolding excised. |
| sourDough CI | **SHIPPED** (partial) — 4 static validators in golgi post-receive (15 repos, advisory). Live checks pending. |
| Performance | **17,595 conn/s, 0.057ms** — no regression from 157a |
| Production campaign | **IN PROGRESS** — hotSpring 18 commits, 105 configs cached, AMD 18.5x all production sizes |
| cellMembrane | **13-commit evolution** — HealthCheckMethod, G69 complete, mesh builder Tower Atomic, 0 clippy |
| coralReef | **3,963 tests** (+147). GEMM Phase 2 IPC. SM20 encoder. BTSP recovery. |
| Tests | **~150K+** across 16 primals + gardens + springs |

---

*Wave 157g — CROSS-GATE GOSSIP LIVE + DEPENDENCY PANDEMIC (G72). 4-gate mesh with epidemic propagation. Stadial shift: 664 Cargo.toml audited, dep fragmentation mapped, 3-tier excision plan. Primals shed vestigial deps as compositions close gaps — young primals (swarmVine: 11 tokio files) are already lean; old primals converge toward that pattern. Spec at `specs/DEPENDENCY_PANDEMIC_SPEC.md`. 0 P0. 0 P1. 2 P2. 6/6 gates. ~150K+ tests.*
