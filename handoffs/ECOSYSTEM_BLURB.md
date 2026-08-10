# ecoPrimals Ecosystem Blurb — Wave 157e NEURAL API ESCALATION

**Date**: Aug 10, 2026 11:50AM | **Wave**: 157e | **From**: overwatch (eastGate)
**Posture**: **MESH CONVERGED. NEURAL API BECOMES THE INTERFACE.** All 6 gates deployed on 157e depot. Performance canary PASS (no regression). Deploy infrastructure COMPLETE (pepti layer + sub-builder fleet + CAS archival). Provenance chain verified E2E (86/87 pen test). **Phase shift: biomeOS Neural API escalates from infrastructure to primary composition interface.** All consumers route through `capability.call`. Graph executor orchestrates multi-step workflows. Pepti layer + data federation + Neural API = three-pillar architecture.

---

## THREE-PILLAR ARCHITECTURE — What's Next

### Pillar 1: Neural API (biomeOS) — The Brain

**Goal (G70)**: biomeOS `capability.call` becomes THE routing mechanism for ALL consumers. No more direct socket paths. Neural API registry = single source of truth for what's available where across the mesh.

| Item | Owner | Status | Next |
|------|-------|--------|------|
| `capability.call` standard routing | biomeOS | **OPERATIONAL** (1.3ms westGate, 4ms ironGate) | Wire all springs/gardens to route through Neural API |
| Graph executor for workflows | biomeOS | **FOUNDATION SHIPPED** (`graph_foreach`, depot lineage templates) | Multi-step compositions: ingest→hash→braid→sign→commit |
| Routing gaps | biomeOS | 2 known (content.stat, spine.list on westGate) | Fix translation registry entries |
| `braid.verify` atomic | sweetGrass | **P1** (pen test discovered) | Verification must be one call, not manual Merkle + Ed25519 |
| Cross-gate `capability.call` | biomeOS + swarmVine | **FOUNDATION** (gossip table in `capability.resolve`) | Targeted cross-gate dispatch via gossip hints |
| toadStool biome.yaml | toadStool + biomeOS | **DIVERGENCE** (ironGate disabled) | `biome.yaml` template or `toadstool run` adaptation |
| `/health` structured response | biomeOS | **GAP** (blueGate returns empty string) | Return JSON schema from `/health` endpoint |

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

## IMMEDIATE WORK — This Wave

| Goal | Owner | Description | Effort |
|------|-------|-------------|--------|
| **Neural API routing gaps** | biomeOS | Fix `content.stat`, `spine.list` translation registry entries. `/health` structured response. | Days |
| **`braid.verify`** | sweetGrass | Atomic verification composition (P1 from pen test) | Days |
| **toadStool biome.yaml** | toadStool | CLI divergence — `up` requires manifest. ironGate disabled. | Days |
| **Production campaign** | strandGate | 22/45 → 45/45 (~6h remaining). Physics quality excellent. | Hours |
| **Process leak** | coralReef + skunkBat | Fork-based orphans ~36/hr. Child process reaping needed. | Days |
| **toadStool S374 depot binary** | sporeGate | Rebuild to include silicon registry (non-blocking) | Hours |

## NEAR-TERM — Next Wave

| Goal | Owner | Description |
|------|-------|-------------|
| **Science pipeline E2E (G71)** | strandGate + ironGate + sporePrint | NFT registration, pseudoSpore bundles, QCD page, `validate.sh` → Rust |
| **Spring cell boots** | tideGlass, hotSpring, esotericWebb | Route through Neural API. First consumers of `capability.call` as standard interface. |
| **Graph executor workflows** | biomeOS | Multi-step compositions: ingest→hash→braid→sign→commit. Eliminate remaining 4/7 jelly strings. |
| **shader.compile.wgsl** | barraCuda → coralReef | General shader compilation via IPC (beyond GEMM) |
| **WASM push (26→48)** | toadStool | Tokio deep debt cleared path |
| **WebGL pipeline** | petalTongue + esotericWebb | G19 browser surfaces. `/ws/scene` foundation ready. |
| **ludoSpring extraction** | petalTongue | `doom-core` → new spring for game/visualization engine |

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

*Wave 157e — MESH CONVERGED. DEPLOY COMPLETE. NEURAL API ESCALATION BEGINS. biomeOS `capability.call` becomes the primary composition interface. Three-pillar architecture: Neural API (brain) + data federation (nervous system) + pepti layer (skeleton). 6/6 gates deployed. 86/87 braid pen test. 3/7 jelly strings eliminated. Production campaign 22/45. 16 primals. 0 P0. 1 P1. ~148K+ tests.*
