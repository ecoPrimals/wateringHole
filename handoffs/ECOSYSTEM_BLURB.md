# ecoPrimals Ecosystem Blurb — Wave 157e NEURAL API ESCALATION

**Date**: Aug 10, 2026 12:10PM | **Wave**: 157e | **From**: overwatch (eastGate)
**Posture**: **MESH CONVERGED. PRIMAL EVOLUTION SUBWAVE NEXT.** westGate overwatch validation: 14/14 alive, Ed25519 roundtrip PASS, 990K files braided. **Critical finding: swarmVine UDS uses tarpc (not JSON-RPC) — Neural API cannot route to it.** Cross-gate gossip peers unreachable. Ant colony pattern documented. 8 spring workloads arrived. **Next**: frontload primal evolution subwave (swarmVine→Tower Atomic integration, Neural API routing gaps, gossip mesh enmeshment), then spin up spring teams and downstream protokarya as gates stabilize.

---

## PRIMAL EVOLUTION SUBWAVE — Frontloaded Before Springs

### Critical Findings from westGate Overwatch Validation

| Finding | Impact | Fix Owner |
|---------|--------|-----------|
| **swarmVine socket discovery wrong** | westGate biomeOS connects to `.tarpc.sock` instead of JSON-RPC `.sock`. swarmVine HAS JSON-RPC (server.rs, G65 negotiate). **Deployment config issue, not code issue.** | Gate ops — fix socket discovery to point at JSON-RPC socket. `sourdough validate convergence` would have caught this. |
| **`sourdough validate` not in golgi CI** | sourDough has 12 validators (tarpc, transport, rpc-surface, convergence, neural-api, platform-substrate, etc.) but none are wired into golgi post-receive hook. Manual-only. | sporeGate + sourDough — wire `sourdough validate convergence` + `sourdough validate rpc-surface` into sovereign CI pipeline |
| **Cross-gate gossip peers unreachable** | `SWARMVINE_PEERS` configured but peers not reachable on TCP 7800. Gossip mesh is local-only. | All gates — deploy swarmVine + verify TCP 7800 reachability |
| **swarmVine not in Tower Atomic composition** | Primal #16 but not formally Tower Atomic. Needs songBird mesh relay for gossip transport. | songBird — `MeshRelay` transport variant for gossip |
| **songBird registration service stale** | Failed 1d 3h ago on westGate. | cellMembrane — registration watchdog or self-heal |
| **No primal currently injects gossip** | Ant colony has no scouts. | All primal teams — identify gossip injection points |

### Subwave Plan — Primal Teams

| Team | Evolution | Blocks |
|------|-----------|--------|
| **sporeGate + sourDough** | Wire `sourdough validate convergence` + `sourdough validate rpc-surface` into golgi post-receive hook (sovereign CI). **Catches deployment config issues before they reach gates.** | Fleet-wide conformance assurance |
| **swarmVine** | (1) Verify JSON-RPC socket is discoverable by biomeOS (socket naming convention). (2) Integrate with Tower Atomic — gossip through songBird `:7700` mesh relay when TCP fails. (3) Verify gossip peers across gates. | Springs cannot discover cross-gate capabilities without gossip |
| **songBird** | `MeshRelay` transport variant — relay swarmVine gossip through existing `:7700` mesh. | Cross-gate gossip |
| **biomeOS** | (1) Fix socket discovery for swarmVine (JSON-RPC socket, not tarpc). (2) Fix `capability.call` routing gaps (content.stat, spine.list). (3) `/health` structured response. | Neural API as standard interface |
| **sweetGrass** | `braid.verify` atomic method — single call for Merkle + Ed25519 verification. | Provenance verification automation |
| **toadStool** | `biome.yaml` template or `toadstool run` adaptation. Fix CLI divergence. | ironGate toadStool disabled |
| **coralReef + skunkBat** | Process leak fix — child process reaping (~36 orphans/hr on southGate). | Gate stability |
| **All primals** | Identify gossip injection points (what events should your primal announce to the mesh via swarmVine?). | Ant colony activation |

---

## THREE-PILLAR ARCHITECTURE

### Pillar 1: Neural API (biomeOS) — The Brain

**Goal (G70)**: biomeOS `capability.call` becomes THE routing mechanism. Neural API registry = single source of truth.

| Item | Status | Next |
|------|--------|------|
| `capability.call` standard routing | **OPERATIONAL** (1.3ms westGate, 4ms ironGate) | Wire springs/gardens through Neural API |
| swarmVine routing | **BLOCKED** — UDS is tarpc, not JSON-RPC | swarmVine JSON-RPC adapter |
| Routing gaps | 2 known (content.stat, spine.list) | Fix translation registry |
| `braid.verify` | **P1** (pen test discovered) | sweetGrass atomic method |
| Cross-gate routing | **BLOCKED** — gossip peers unreachable | Gossip mesh enmeshment |
| `/health` response | **GAP** (empty on blueGate) | Structured JSON |

### Pillar 2: Data Federation — The Nervous System

**Goal**: Data flows across gates via CAS federation, provenance braiding, and gossip. Every object has lineage, every computation has proof.

| Item | Owner | Status | Next |
|------|-------|--------|------|
| Provenance chain | Provenance Trio | **VERIFIED** (86/87 pen test) | Wire `braid.verify` for atomic verification |
| CAS federation | nestGate + petalTongue | **LIVE** (`content.replicate` cross-gate) | L1 cache on golgi for hot objects |
| Jelly string elimination | westGate pipeline | **3/7 DONE** | Remaining 4 need biomeOS graph executor or nestGate tier awareness |
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
| Process management | All gates | **P2** — coralReef/skunkBat process leak ~36/hr on southGate |

---

## IMMEDIATE WORK — Primal Evolution Subwave

| Priority | Goal | Owner | Effort |
|----------|------|-------|--------|
| **HIGH** | **Wire sourDough validate into golgi CI** | sporeGate + sourDough | Days — `convergence` + `rpc-surface` in post-receive hook |
| **HIGH** | **Fix swarmVine socket discovery** | biomeOS + gate ops | Hours — biomeOS connects to tarpc socket, should use JSON-RPC socket |
| **HIGH** | **Gossip mesh enmeshment** | All gates | Hours — verify swarmVine TCP 7800 cross-gate reachability |
| **HIGH** | **songBird MeshRelay for gossip** | songBird | Days — relay gossip through `:7700` when TCP fails |
| **HIGH** | **biomeOS routing gaps** | biomeOS | Days — content.stat, spine.list, /health |
| **HIGH** | **`braid.verify` atomic** | sweetGrass | Days — P1 from pen test |
| **MED** | **toadStool biome.yaml** | toadStool | Days — ironGate disabled |
| **MED** | **Process leak** | coralReef + skunkBat | Days — ~36 orphans/hr |
| **MED** | **Production campaign** | strandGate | Hours — 22/45 → 45/45 |

## AFTER SUBWAVE — Springs + Protokarya Spin-Up

**Sequence**: Primal evolution subwave (swarmVine integration, gossip mesh, Neural API gaps) → gates stabilize + enmesh → spring teams activate → downstream protokarya teams activate.

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
| **Graph executor workflows** | biomeOS | Multi-step compositions. Eliminate remaining 4/7 jelly strings. |
| **shader.compile.wgsl** | barraCuda → coralReef | General shader compilation via IPC |
| **WASM push (26→48)** | toadStool | Tokio deep debt cleared path |
| **WebGL pipeline** | petalTongue + esotericWebb | G19 browser surfaces |
| **ludoSpring extraction** | petalTongue | `doom-core` → new spring |

## GLACIAL

| Goal | Status |
|------|--------|
| arXiv 41/42 | Campaign 22/45. `validate.sh` → Rust. Reviewer send. |
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
| **strandGate** | **7/7** | Silicon Fold. Production campaign 22/45. 2 GPUs active. |
| **westGate** | **14/14** | Data NAS. Signed spine commits. Braid pen test 86/87. Pipeline Rust-native. |
| **blueGate** | **13/13** | Primary builder. `:9800` validated. golgi SSH. Windows native. |
| **southGate** | **13/13** | Canary PASS. 17,595 conn/s. 0.057ms. No regression. |
| **ironGate** | **13/13** | Downstream host. 166 caps. Vine-bat. 12.7 TB CAS. |
| **eastGate** | overwatch | primalSpring validation pending. |

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
| P0 / P1 / P2 | **0 / 1 / 2** (P1: `braid.verify`. P2: petalTongue port, process leak) |
| Deploy | **COMPLETE** — pepti layer + sub-builders + auto-prune + CAS archival |
| Braid pen test | **86/87 PASS** — provenance chain E2E verified |
| Jelly strings | **3/7 eliminated** (remaining 4 need biomeOS graph) |
| Performance | **17,595 conn/s, 0.057ms** — no regression from 157a |
| Production campaign | **22/45** (strandGate QCD Rung 1) |
| Tests | **~148K+** across 16 primals |

---

*Wave 157e — MESH CONVERGED. PRIMAL EVOLUTION SUBWAVE NEXT. Critical: swarmVine UDS is tarpc (Neural API can't route), cross-gate gossip peers unreachable. Subwave: swarmVine JSON-RPC adapter + songBird MeshRelay + gossip enmeshment + Neural API gaps. Then: spring teams activate, downstream protokarya spin up. Ant colony pattern documented. 8 spring workloads arrived. 6/6 gates deployed. 86/87 braid pen test. 16 primals. 0 P0. 1 P1. ~148K+ tests.*
