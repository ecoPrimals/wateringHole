# ecoPrimals Ecosystem Blurb — Cephalization Era

**Date**: Aug 6, 2026 AM | **Wave**: 156i | **From**: eastGate overwatch
**Posture**: **CEPHALIZATION ERA — CONVOY COMPLETE.** ZERO P0/P1/P2. 15/15 GREEN. ~140K+ tests. **D3 convoy 100% — 10.99M provenance events braided.** Multi-tier CAS LIVE on westGate (ENOSPC→fix in one session). loamSpine tarpc-CONVERGED (37 methods). toadStool C5 RESOLVED (neuromorphic excluded from workspace). hotSpring +4,361 lines SU(N) science. esotericWebb V31c (bridge reconnect). Priority: primal mountain → sporeGate deploy → NUCLEUS springs → ironGate surface.

---

## LATEST ARRIVALS (since 156h)

| Event | Source | Impact |
|-------|--------|--------|
| **D3 CONVOY 100% COMPLETE** | westGate | **10,994,802 provenance events braided** across 11,119,514 queue lines. All 4 workers finished. Queue fully processed. D3 CLOSED. |
| **ENOSPC → Multi-tier CAS LIVE** | westGate | NVMe hot tier hit 100% at 313/s. Same-session fix: `SubstrateTiers` wired into `content.put`. Cross-tier dedup + 10 GB backpressure guard DEPLOYED. |
| **loamSpine tarpc-CONVERGED** | sporeGate | G64 first convergence: 24→37 tarpc methods. All domain ops have tarpc parity. loamSpine moves from "tarpc-wired" to "tarpc-converged". |
| **toadStool C5 RESOLVED** | biomeGate | Neuromorphic crates excluded from default workspace (-1,265 lines). Cross-gate builds unblocked without rustChip. |
| **hotSpring +4,361 lines** | strandGate | SU(N) GaugeGroup trait + GenericLattice. `tile_from()` dynamic programming (bootstrap larger from cached). NPU phase classifier + thermalization monitor. |
| **esotericWebb V31c** | ironGate | Bridge reconnection for stale primal connections. Documents `/run/membrane` socket permissions P1. |
| **coralReef compiler evolution** | biomeGate | CFG block-id verify helper + `Src::without_modifier`. |
| **rhizoCrypt** | sporeGate | blake3 1.8.5→1.8.6 dep update. |
| **Compute Memoization doc** | whitePaper | NFT pattern formalized. Dynamic programming: tile 16⁴→32⁴ from cached configs. |
| **Ephemeral tier AAR** | wateringHole | Full incident writeup. Lessons: backpressure > monitoring, nest atomic owns its pools. |

---

## PRIORITY 1 — PRIMAL MOUNTAIN

Get all primals solid as a foundation for everything that follows.

### G64: Cephalization — tarpc Convergent Evolution

All 15 primals converge to dual-protocol (JSON-RPC + tarpc) composition. JSON-RPC bootstraps discovery; tarpc carries performance. Each primal evolves independently — convergent evolution, not directed.

| Layer | Protocol | Scope | Speed | Status |
|-------|----------|-------|-------|--------|
| **Intra-gate** | tarpc UDS (binary) | Same NUCLEUS | sub-ms | Phase 1 — 5 primals ready |
| **Cross-gate bootstrap** | JSON-RPC on songBird mesh | Gate-to-gate | ~1-5ms | LIVE |
| **Cross-gate elevated** | tarpc on songBird relay | Gate-to-gate composition | sub-ms binary | Phase 2 (after version convergence) |
| **Browser/diagnostic** | JSON-RPC / REST | Conjugation layer | ~10ms | Permanent |

| tarpc State | Primals | Count |
|-------------|---------|-------|
| **tarpc-CONVERGED** (full domain parity) | **loamSpine** (37 tarpc / 53 JSON-RPC) | 1 |
| **tarpc-default** (server + client, default feature) | coralReef, barraCuda, toadStool, nestGate, squirrel | 5 |
| **tarpc-wired** (service definitions, optional) | songBird, sweetGrass, rhizoCrypt, petalTongue, biomeOS | 5 |
| **tarpc dep only** (not yet serving) | bearDog, skunkBat, bingoCube | 3 |
| **NEXT to CONVERGE** (C6 — reference impl) | **sourDough** (standards holder, nascent spawning primal) | 1 |

**Convergence blockers**:
1. **tarpc 0.34 → 0.37**: songBird + petalTongue stuck on 0.34 (bincode 1.3→2.x).
2. **UDS protocol fragmentation**: 6 divergences documented (DIV-1→6). BTSP vs plain JSON vs tarpc.
3. **Port-agnostic routing**: songBird moves from port assignments to capability routing.

**Performance thesis**: convoy at 217/s is ~5ms/file JSON-RPC IPC. tarpc binary framing eliminates serde roundtrip — composition goes exponential for high-frequency patterns (provenance braiding, CAS ops, GPU dispatch).

### Primal Mountain Work Items

| # | Item | Primal | Owner | Impact |
|---|------|--------|-------|--------|
| **C1a** | **tarpc 0.34→0.37** + bincode 2.x migration | songBird | overwatch | Cephalization version alignment |
| **C1b** | **tarpc 0.34→0.37** + bincode 2.x migration | petalTongue | overwatch | Cephalization version alignment |
| **C2** | **UDS dual-socket pattern** — JSON-RPC on `.sock`, tarpc on `.tarpc.sock` | sourDough (reference impl), then: bearDog, songBird, skunkBat, nestGate, rhizoCrypt, loamSpine, sweetGrass, toadStool, barraCuda, coralReef, petalTongue, biomeOS, squirrel, bingoCube | per-primal owner | Port-agnostic routing |
| **C3** | **JSON-RPC health shim** alongside tarpc primary | coralReef | biomeGate | nestgate.io 13/13 alive |
| **C4** | **Deploy restart** — running binary predates B1/B2 fix. `sudo systemctl restart membrane-toadstool`. | toadStool | sporeGate (ops) | nestgate.io 13/13 alive |
| ~~**C5**~~ | ~~rustChip → Forgejo~~ — **RESOLVED.** Neuromorphic excluded from workspace. | toadStool | biomeGate | **DONE** |
| **C6** | **sourDough cephalization** — reference primal gets dual-protocol first. tarpc service definitions for all standard methods. sourDough sets the pattern, others follow. | sourDough | eastGate | **Reference implementation** for G64 |

---

## PRIORITY 2 — SPOREGATE REBUILD & DEPLOYMENT

Depot is rebuilt (26 binaries, golgi). Now deploy to all NUCLEUS gates.

| Gate | Current | Action | Status |
|------|---------|--------|--------|
| **sporeGate** | v4.57+ (depot authority) | **Restart toadStool** (C4). Verify 13/13 health. | NEXT |
| **ironGate** | v4.57+ (10/10) | Deploy updated depot binaries. Verify downstream services. | QUEUED |
| **westGate** | v4.57 | Deploy latest depot. Enable nestGate TCP (O5). | QUEUED |
| **blueGate** | v4.57+ (14/14) | Sub-builder already proven. Verify latest bins. | QUEUED |
| **southGate** | v4.57+ (13/13) | Re-deploy for cephalization baseline. | LOW |
| **strandGate** | v4.57+ (deferred) | GPU at 100% — deploy when thermalization batch completes. | DEFERRED |

---

## PRIORITY 3 — NUCLEUS SPRINGS & CROSS-GATE SYSTEMS

Once primals are solid and deployed, activate the spring projects.

| # | Item | Owner | Gate | Unblocks |
|---|------|-------|------|----------|
| **E2** | **squirrel systemd on ironGate** — `squirrel.service`, petal-bridge routes `agent.*`. | eastGate | ironGate | Agent panel LIVE |
| **D1** | **tideGlass cell boot on westGate** — `biomeos nucleus attach`. GPS data ready. | overwatch | westGate | Track A science |
| **O5** | **nestGate TCP on westGate** — `NESTGATE_JSONRPC_TCP=1`. Register `content` with songBird. | overwatch | westGate | Inter-gate CAS federation |
| **O7** | **Inter-gate `content.get` E2E** — ironGate pulls CAS object from westGate via songBird. | overwatch | mesh | All data-remote springs |
| **O6** | **petalTongue scene passthrough** — accept tideGlass declarative viz format. | overwatch | petalTongue | GPS + QCD viz pipeline |
| **E3** | **esotericWebb HEAD method** — GET=200, HEAD=502 (NG-06). | eastGate | esotericWebb | Health checks |
| **E1** | **bearDog Neural API routing stub** — register with Neural API for nestgate.io. | eastGate | bearDog | nestgate.io 11/12 |

---

## BACKGROUND — CONTINUING WORK

These teams continue their own project work independently.

| Gate | Project | Status | ETA |
|------|---------|--------|-----|
| ~~**westGate**~~ | ~~Convoy~~ — **100% COMPLETE. 10.99M events braided.** | **DONE** | — |
| **westGate** | Multi-tier CAS drain: warm→cold rsync + `content.archive` wiring | NEXT | Post-drain |
| **westGate** | Data braids convergence — promote primordial → fully braided | NEXT | After drain |
| **strandGate** | SU(N) thermalization — 87-config grid + NPU phase classification | Running | ~2wk |
| **strandGate** | hotSpring SU(N) measurement battery + `tile_from()` bootstrapping | After thermalization | After grid |

---

## PRIORITY 4 — IRONGATE DOWNSTREAM SURFACE

ironGate becomes the usable surface for science projects. Two depot roles: ironGate holds **novel ferment transcripts** (compute outputs, analysis results, science artifacts); westGate holds **data braids** (raw ingested datasets with provenance).

### ironGate Science Surface

| Project | Stack | Status | Next |
|---------|-------|--------|------|
| **NF Drug Repurposing (GPS)** | tideGlass → petalTongue → nestGate CAS | GPS data on westGate CAS. tideGlass 220 tests, PetalTongueClient wired. | D1 cell boot → Chen 2017 benchmark |
| **ABG (initioChem)** | initioChem → toadStool → barraCuda → nestGate | G50 ACTIVE. Whole-cell expression artifact target. | Cell boot after tideGlass proves pattern |
| **MILC Engine** | hotSpring → coralReef → barraCuda → petalTongue | strandGate primary (compute). ironGate for viz surface. | SU(N) data → ironGate petalTongue renders |
| **esotericWebb** | esotericWebb → petalTongue → coralReef (shaders) | V31b, 484 tests, cell boot SUCCEEDED. | G19 WebGL pipeline |
| **footPrint** | footPrint → petalTongue → nestGate | PHASE 2 LIVE. 708 tests. petal-bridge wired. | E2 squirrel → agent panel |

### Dual CAS Depot Architecture

| Depot | Gate | Content | Role |
|-------|------|---------|------|
| **Data Braids** | westGate | Raw datasets, AlphaFold, NF data portal, GPS, genomics. 3.21 TB / 452 GB CAS. | Ingestion + provenance. Source of truth for raw data. |
| **Novel Ferment Transcripts** | ironGate | Compute results, analysis artifacts, science outputs, tideGlass results. 12.7 TB CAS. | Output depot. Products of primal composition. |

ironGate's CAS grows as springs produce results: tideGlass GPS analyses, hotSpring QCD measurements, esotericWebb game state, footPrint GIS artifacts. westGate feeds raw data; ironGate stores what the mesh computes from it.

---

## DEPOT STATUS

All 15 primals compile clean at HEAD. **Depot REBUILT** — 26 binaries on golgi.

| Primal | HEAD | Key Change |
|--------|------|------------|
| nestGate | `ad3923e` | **Multi-tier CAS** — warm writes, cross-tier dedup, backpressure (ENOSPC fix) |
| loamSpine | `f7213cb` | **G64 tarpc-CONVERGED** — 24→37 tarpc domain methods |
| toadStool | `22116a4` | **C5 RESOLVED** — neuromorphic excluded from workspace (-1,265 lines) |
| coralReef | `15aab6f` | CFG block-id verify + `Src::without_modifier` |
| rhizoCrypt | `061acfa` | blake3 1.8.5→1.8.6 |
| sweetGrass | `4a6ec48` | convergence.check + braid.list (S1–S3) |
| petalTongue | `783aaac` | mesh.peers (S7) + health.liveness (S8) |
| squirrel | `d752462` | deep debt sweep 156e→156j (+local WIP: error refactor -978 lines) |

Remaining 7 primals (songBird, bearDog, biomeOS, barraCuda, cellMembrane, skunkBat, sourDough, bingoCube) — depot-current, no changes this cascade.

**Non-primal evolution**: hotSpring +4,361 lines (SU(N) GaugeGroup, NPU integration, tile_from()), esotericWebb V31c (bridge reconnect), whitePaper (compute memoization + ephemeral tier docs).

---

## GATE FLEET

| Gate | NUCLEUS | Role | Key Status |
|------|---------|------|------------|
| **sporeGate** | 14/14 v4.57+ | CI / membrane | Depot REBUILT. nestgate.io 10/12. **NEXT: toadStool restart (C4)** |
| **ironGate** | 10/10 v4.57+ | **Downstream surface** | NF GPS + ABG + MILC. 12.7 TB CAS. footPrint LIVE. **NEXT: squirrel deploy (E2)** |
| **westGate** | 14/14 v4.57 | **Data braids depot** | 3.21 TB / 452 GB CAS. **CONVOY COMPLETE (10.99M events).** Multi-tier CAS LIVE. **NEXT: drain warm→cold, nestGate TCP (O5), tideGlass boot (D1)** |
| **strandGate** | v4.57+ (deferred) | Compute | SU(N) 87-config grid + NPU phase classifier + tile_from() DP. Background. |
| **blueGate** | 14/14 v4.57+ | Windows dev | Sub-builder PROVEN (15/15). |
| **southGate** | 13/13 v4.57+ | Validation | G17+G8 proven. |
| **biomeGate** | Source-built | GPU lab | Akida. rustChip local. 3 VFIO GPUs. coralReef tarpc vanguard. |
| **golgi** | Thin relay | VPS | Depot + Caddy + Drawbridge. |

---

## DUAL-SCIENCE STATUS

### Track A: NF Drug Repurposing (Gonzales / Bin Chen)

| Step | Status | Next |
|------|--------|------|
| Provenance 7/7 | **DONE** | — |
| westGate data federation | **3.21 TB / 452 GB CAS. GPS CONVERTED. CONVOY COMPLETE (10.99M events).** Multi-tier CAS LIVE. | Drain warm→cold |
| tideGlass specs | **SHIPPED** (5 spec docs) | — |
| **tideGlass Phase 0** | 220 tests. PetalTongueClient ACTIVATED. | **D1: cell boot on westGate** |
| Phase 1: GPS reproduction | — | After Phase 0 |
| NF reversal screen | — | After Phase 1 |
| CTF NDU grant ($125K) | — | After reversal screen |

### Track B: Lattice QCD (Murillo / Chuna)

| Step | Status | Next |
|------|--------|------|
| barraCuda DF64 | **DONE** (FP64 104T RTX 3090) | — |
| hotSpring SU(N) | **GENERALIZED** (N=2→8, +4,361 lines). GaugeGroup trait, GenericLattice, `tile_from()` DP, NPU phase classifier. | — |
| 16⁴ dual-GPU | **CONFIRMED** (6 ppm cross-vendor) | — |
| **arXiv Rung 1** | 42-item rubric. Murillo/Chuna/Bazavov panel. | **12 MUST-fix → LaTeX → send** |
| SU(N) thermalization | 87-config grid + NPU monitor + metalforge experiment | ~2wk |

---

## LIVE SITES

| Site | URL | Status | Remaining |
|------|-----|--------|-----------|
| **sporePrint** | `sporeprint.primals.eco` | LIVE | — |
| **footPrint** | `footprint.primals.eco` | LIVE (auto-loads) | squirrel UDS (E2) |
| **nestgate.io** | `nestgate.io` | **10/12** sections | bearDog stub (E1), CAS browse |
| **esotericWebb** | `webb.primals.eco` | GET 200 / HEAD 502 | **V31c** (bridge reconnect). HEAD fix (E3), WebGL (G19) |

---

## K-DERM — FULLY OPERATIONAL (G59 GRADUATED)

| Layer | Domain | Status |
|-------|--------|--------|
| Outer | `primals.eco` | LIVE — Cloudflare, 14 Caddy routes |
| Peptidoglycan | `nestgate.io` | LIVE — 20 primals, 10/12, sovereign Knot DNS + DNSSEC |
| Inner | `primal.eco` | LIVE — dnsmasq, zero public records |

---

## CODE OWNERSHIP

| Primary Gate | Primals |
|-------------|---------|
| **sporeGate** | sweetGrass, loamSpine, rhizoCrypt |
| **biomeGate** | toadStool, barraCuda, coralReef |
| **eastGate** | bearDog, skunkBat, squirrel, sourDough, bingoCube |
| **overwatch** | biomeOS, songBird, nestGate, petalTongue, cellMembrane |

---

## GLACIAL GOALS — SCORECARD

| Category | Count | IDs |
|----------|-------|-----|
| **COMPLETE** | 12 | G3, G4, G8, G10, G17, G21, G22, G29, G31, G55, G59 |
| **ACTIVE** | 25 | G7, G9, G11, G14, G15, G18, G19, G20, G30, G32, G34, G35, G36–39, G43–45, G53–54, G56–58, G60–62, G64 |
| **GLACIAL** | 23 | Future phases |
| **Total** | 60 | |

---

*Wave 156i — **Cephalization Era — Convoy Complete.** D3 convoy 100% done (10.99M events). Multi-tier CAS LIVE (ENOSPC→same-session fix). loamSpine first tarpc-CONVERGED primal (37 methods). toadStool C5 resolved (neuromorphic excluded). hotSpring +4,361 lines (SU(N) science push: GaugeGroup, tile_from, NPU). esotericWebb V31c (bridge reconnect). Priority: primal mountain → sporeGate deploy → NUCLEUS springs → ironGate surface. 12 COMPLETE / 25 ACTIVE / 23 GLACIAL. All 15 primals at HEAD, ~140K+ tests, 15/15 GREEN.*
