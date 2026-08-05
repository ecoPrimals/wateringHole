# ecoPrimals Ecosystem Blurb — LAN HPC Enmeshment Era

**Date**: Aug 5, 2026 PM | **Wave**: 156e | **From**: eastGate overwatch
**Posture**: **P0/P1/P2: ZERO. ALL 6 NUCLEUS GATES v4.57+. nestgate.io LIVE (20 primals, Neural API bridge, 8/12 sections). footPrint petal-bridge WIRED (dual-socket WS↔UDS: agent.*→squirrel, viz→petalTongue). tideGlass PetalTongueClient ACTIVATED (viz forwarding live). hotSpring SU(N) GENERALIZED (N=2→8, 87-config grid, 652 tests). westGate 4-tier storage (NVMe convoy 217/s, inline 265/s). ~136K+ tests, 13/13 GREEN.**

---

## WHAT JUST HAPPENED — Session 13 Cascade (LAN HPC Enmeshment)

| Event | Gate | Status |
|-------|------|--------|
| **nestgate.io NEURAL API BRIDGE** | sporeGate | Root cause: petalTongue `NeuralApiProvider::discover()` couldn't find socket (wrong dir). Fix: symlink + env vars. Now discovers **20 primals**, **8/12 dashboard sections functional**. Tower Atomic architecture view, Neural API routing table, namespace distribution, data braids section all LIVE. |
| **footPrint PETAL-BRIDGE WIRED** | ironGate | `petal-bridge.ts`: dual-socket WS↔UDS relay. `agent.*`/`bridge.*` → squirrel UDS (translates `agent.query` → `ai.query`). All else → petalTongue UDS. NDJSON framing. `autoLoadDefaultProject()` → map no longer empty. CSP dedup via `SKIP_CSP=1`. 708 tests. |
| **tideGlass PetalTongueClient LIVE** | westGate | `dead_code` removed. Instantiated at startup via `discover_petaltongue_socket()`. `ServerContext` carries `Arc<PetalTongueClient>`. Viz scene forwarding fire-and-forget after dispatch. `is_viz_method()` gates forwarding. **220 tests.** |
| **hotSpring SU(N) GENERALIZED** | strandGate | `GaugeGroup` trait: SU(N) for N=2,3,4,5,6,8. `GenericLattice<G>` — HMC + full observable battery. `Su2Matrix` (64 B/link stack), `SuNMatrix` (heap N≥4). Cayley exp + Creutz ratios + Polyakov + Wilson loops + flow + Q_top. **87-config thermalization grid RUNNING** (SU(2) first, ~2wk total on 64 EPYC threads). **652 lib tests.** Paper reframed: "Vendor-Agnostic SU(N) Lattice Gauge Theory on Consumer GPUs." |
| **westGate 4-TIER STORAGE** | westGate | NVMe hot CAS tier activated → convoy **217/s** (2.7x over spinner). Inline braiding **265/s** (warm). T0: RAM ARC (98% hit). T1: NVMe (1.7 GB/s write). T2: SSD L2ARC (65.9% hit). T3: HDD raidz1 (cold archive). Storage was the bottleneck, never primals (~5ms/file). |
| **Caddy CLEANUP** | golgi | `basicauth` → `basic_auth`. 10 redundant `header_up` removed. Clean reload. |
| **webb.primals.eco DIAGNOSIS** | sporeGate | GET returns 200 (11,768 B HTML). HEAD returns 502. Root cause: esotericWebb HTTP handler missing HEAD method. Not a Caddy issue. |

---

## GATE FLEET STATUS — POST-SYNC

| Gate | NUCLEUS | Depot | Status |
|------|---------|-------|--------|
| **sporeGate** | **14/14 v4.57+** | **BUILD AUTHORITY — FRESH** | Sovereign CI. 52/52 harvest complete. LAN-first Tower (4 local, 1ms). |
| **ironGate** | **10/10 v4.57+** | **CURRENT** | **G18 DISPATCH LIVE (9 providers). NUCLEUS storage 12.7 TB CAS. songBird federation to westGate.** 708 tests. |
| **westGate** | **14/14 v4.57** | **SOURCE-BUILT** | GPS data converted. Convergence sweep complete. `nucleus attach` ready. |
| **strandGate** | **v4.57+ (restart deferred)** | **CURRENT** | GPU at 100% QCD production. Config cache COMPLETE (9/10, 325 MB). Dual-GPU scan LAUNCHED. |
| **blueGate** | **14/14 v4.57+** | **CURRENT** | Depot sync done. UniBin CLI migration documented. |
| **southGate** | **13/13 v4.57+** | **CURRENT** | Re-validated after 97h uptime. Tower 0.15ms avg, 19 Gbps. RTX 4060 Vulkan healthy. |
| **biomeGate** | Source-built compute | — | GPU lab. Not full NUCLEUS. |
| **golgi** | Thin relay | **footprint.primals.eco LIVE** | Caddy routing → ironGate :3002. UFW 3002/tcp. |
| **northGate** | — | — | Daily driver. Skip. |
| **grapheneGate** | Tower | — | Mobile. Skip. |
| **eastGate** | — | — | Overwatch. Skip. |

### Remaining Sync Work

```
DONE: sporeGate harvest (52/52)      ✓  14/14 HEALTHY
DONE: ironGate redeploy              ✓  10/10, cell boot, footPrint LIVE
DONE: westGate source-built v4.57    ✓  14/14 HEALTHY, GPS converted
DONE: strandGate binaries staged     ✓  restart deferred (GPU 100%)
DONE: blueGate depot sync            ✓  14/14 HEALTHY, UniBin CLI
DONE: southGate depot sync           ✓  13/13 HEALTHY, re-validated
DONE: golgi Caddy routing            ✓  footprint.primals.eco LIVE

ALL 6 NUCLEUS GATES SYNCED TO v4.57+.
```

---

## GATE ROLE TAXONOMY

| Gate | Role | What Runs | Key Specs |
|------|------|-----------|-----------|
| **ironGate** | **Downstream host** | esotericWebb (cell boot) + footPrint (Phase 2 LIVE) + squirrel + petalTongue | i9-14900K, RTX 5070, 94GB. |
| **westGate** | **Data NAS** | tideGlass + wetSpring + groundSpring + airSpring | 3.21 TB / 153 datasets on ZFS raidz1 50.7TB. v4.57 LIVE. GPS data converted. |
| **strandGate** | **Compute** | hotSpring + neuralSpring | Dual EPYC, RTX 3090, RX 6950 XT. QCD production. |
| **biomeGate** | **GPU lab** | G32 silicon deism. 3 VFIO GPUs. | Threadripper 3970X, 128GB. |
| **blueGate** | **Windows dev** | ludoSpring. Windows NUCLEUS. | Sub-builder. |
| **sporeGate** | **CI / membrane** | Sovereign CI. Build authority. nestgate.io. | Depot. Knot DNS. |
| **southGate** | **Validation** | NUCLEUS reference gate. | G17+G8 PROVEN. |
| **eastGate** | **Overwatch** | squirrel (156d). | Code hub. |
| **northGate** | **Windows dev** | RTX 5090. Daily driver. | AlphaFold data source. |
| **grapheneGate** | **Mobile** | Tower (TCP). Pixel 8a. | Beacon seed. |
| **golgi** | **VPS relay** | Forgejo + depot + sporePrint. | Thin-relay. |

---

## CODE OWNERSHIP — WHO PUBLISHES WHAT

Each primal has a **primary team** responsible for committing working code and pushing to Forgejo. sporeGate + blueGate rebuild the depot from Forgejo. Other gates can read, review, and push fixes, but the primary team owns compilation health and publish responsibility.

**Rule**: Only the primary team should have uncommitted changes for their primal. If you're not the owner, don't leave dirty working directories — commit and push, or discard.

| Primary Gate | Primals | Basis |
|-------------|---------|-------|
| **sporeGate** | sweetGrass, loamSpine, rhizoCrypt | Provenance trio. Active refactoring (LedgerClient, batch pipeline). |
| **biomeGate** | toadStool, barraCuda, coralReef | Node Atomics + GPU compute. 2,100+ toadStool commits. |
| **eastGate** | bearDog, skunkBat, squirrel, sourDough, bingoCube | Tower security + agent + tools. |
| **overwatch** | biomeOS, songBird, nestGate, petalTongue, cellMembrane | Orchestration + discovery + storage + render + CI. Multiple gates contribute; overwatch merges. |

**Depot flow**: Primary team commits → pushes to Forgejo → sporeGate sovereign CI rebuilds → depot updates → gates deploy via `plasmid.harvest`.

**What broke**: sweetGrass had uncommitted WIP on eastGate (LedgerClient refactor removing `handle_braid_batch_create`/`handle_braid_batch_commit` from `braid.rs` but not `registry.rs`). This is sporeGate's responsibility — eastGate discarded the WIP. sporeGate team should complete and push when ready.

---

## PHASE STATUS

### Phase 1: Cell Boot — SUCCEEDED
`biomeos nucleus attach esotericwebb_cell.toml` on ironGate. First-ever cell attachment. exp006 21/22 PASS (1 skip from `biomeos/` → `membrane/` socket path migration, 0 fail). Scene push to petalTongue firing post-attach.

### Phase 2: footPrint — DEPLOYED + LIVE + BRIDGE WIRED
systemd active on ironGate. CAS E2E verified (TCP local-trust). 708 tests. golgi Caddy routing DONE. **petal-bridge.ts** dual-socket relay: `agent.*` → squirrel, viz → petalTongue. `autoLoadDefaultProject()` → map auto-loads on visit. `SKIP_CSP=1` deduplicates CSP headers. **Remaining**: squirrel UDS socket needs to exist at `/run/user/1000/biomeos/squirrel.sock` for agent panel to connect.

### Phase 3: squirrel + petalTongue — G18 LIVE
- squirrel G18 signal dispatch **LIVE** on ironGate — 9 primal providers, cross-primal routing validated
- petalTongue G19 live render on RTX 5070 — NEXT

### Phase 4: westGate science springs — UNBLOCKED
- westGate v4.57 DEPLOYED (14/14 HEALTHY), `nucleus attach` available
- tideGlass GPS data CONVERTED (11 JSON, 103 MB CAS-ingested)
- Cell TOMLs exist for all 4 springs
- **Next**: `biomeos nucleus attach --cell tideglass_cell.toml` on westGate
- groundSpring, airSpring also ready. ludoSpring on blueGate waiting.

### Phase 5: Inter-gate mesh — FUTURE
- songBird probes ready, nestGate content.fetch ready
- Blocks healthSpring, lithoSpore, neuralSpring, hotSpring, wetSpring

---

## westGate CONVERGENCE SWEEP — Aug 4, 2026

| State | Count | Size | Description |
|-------|-------|------|-------------|
| **CONVERGED** | 0 | — | Full provenance chain |
| **CAS-ONLY** | 5 | ~15 GB | BLAKE3 in CAS, no DAG/spine |
| **PARTIAL** | 89 | ~205 GB | Some files CAS'd |
| **PRIMORDIAL** | 32 | ~636 GB | No CAS at all |
| **EMPTY** | 21 | 0 | Placeholders |
| **Not scanned** | 6 | ~70 GB | Sweep timeout |

**ZFS**: 3.21 TB used / 50.7 TB pool (6.3%). CAS pool on **NVMe hot tier** (convoy at **217/s**, inline at **265/s**).

**Key**: 0 datasets at CONVERGED. Convoy ACTIVE on NVMe (**217/s**, ~14h ETA for 11M+ files). **4-tier storage**: T0 RAM ARC (98% hit) → T1 NVMe (1.7 GB/s write) → T2 SSD L2ARC (65.9% hit) → T3 HDD raidz1 (cold archive). Post-convoy: rsync hot→cold, evaluate nestGate dual-path as upstream feature.

---

## PRIMAL HEALTH DASHBOARD

| Primal | Tests | Health | Recent |
|--------|-------|--------|--------|
| **songBird** | 14,840+ | GREEN | 22 drawbridge bonds. LAN-first Tower (1ms). |
| **bearDog** | 14,019 | GREEN | 94 orphans purged |
| **nestGate** | 13,095+ | GREEN | **`content.query` SHIPPED.** ZFS REST. tarpc 0.37. nestgate.io wired. |
| **toadStool** | 9,193+ | GREEN | S351: -48 dead deps. Symlink fix. |
| **biomeOS** | 8,570+ | GREEN | **v4.57: `nucleus attach` — CELL BOOT SUCCEEDED.** westGate DEPLOYED. |
| **petalTongue** | 6,755 | GREEN | **nestgate.io 20 primals, 8/12 sections.** Neural API bridge. Tower Atomic dashboard. |
| **barraCuda** | 4,959 | GREEN | **MultiDevicePool.** `device.pool` IPC. |
| **squirrel** | 4,613 | GREEN | 156d sovereignty. 27 deprecated aliases removed. |
| **coralReef** | 3,512 | GREEN | ShaderInfo dedup, alloc fix, identity tests. |
| **rhizoCrypt** | 1,791 | GREEN | **G63 SO_PEERCRED SHIPPED.** CAS local-trust. |
| **loamSpine** | 1,740 | GREEN | OnceLock UID cache. Tower/custodian BTSP. |
| **sweetGrass** | 1,636 | GREEN | **LedgerClient v0.8.0** → loamSpine. |
| **cellMembrane** | 1,281+ | GREEN | **Harvest scheduler.** CI-DIV fixes. Phase 2a manifest registry. |

**Total**: **~135,000+ tests**. **13/13 GREEN**.

---

## DUAL-SCIENCE STATUS

### Track A: NF Drug Repurposing (Gonzales / Bin Chen)

| Component | Status | Next |
|-----------|--------|------|
| **tideGlass** | **220 tests.** 9 crates. **PetalTongueClient ACTIVATED** (viz forwarding live, `is_viz_method()` gate). `ServerContext` carries CAS + petal clients. GPS data CONVERTED (11 JSON, 103 MB). `content.query` WIRED. | `nucleus attach` on westGate. Chen 2017 benchmark. |
| **footPrint** | **PHASE 2 DEPLOYED on ironGate.** 708 tests. CAS E2E. Agent bridge. | golgi Caddy routing. GPS viz integration. |
| **westGate data** | 3.21 TB / 153 datasets. 452 GB CAS pool. **4-tier storage active** (NVMe hot at 217/s, inline at 265/s). | Convoy completion → bulk convergence. |
| **nestGate** | **`content.query` SHIPPED.** nestgate.io content backend wired. **Neural API bridge LIVE** (20 primals on sporeGate). | Federation: TCP + songBird capability registration. |
| **Provenance trio** | 7/7. Loop CLOSED. **460x improvement** (0.3/s → 145/s → 217/s on NVMe). | Convoy running. Post-convoy: rsync hot→cold. |

### Track B: Lattice QCD on Consumer GPUs (Murillo / Chuna)

| Component | Status | Next |
|-----------|--------|------|
| **strandGate** | 12⁴ paper-ready. **16⁴ DUAL-GPU DATA COMPLETE** (6 ppm, +0.01%). **SU(N) GENERALIZED** — GaugeGroup trait covers N=2,3,4,5,6,8. 87-config thermalization grid RUNNING. Paper reframed: "Vendor-Agnostic SU(N) Lattice Gauge Theory on Consumer GPUs." | Populate SU(N) data tables. 32⁴ minimal publishable target. |
| **hotSpring** | 8 arxiv binaries inc. `arxiv_thermalize_sun` + `arxiv_measure_battery`. GaugeGroup trait + GenericLattice\<G\>. **652 lib tests.** Config cache LIVE. | SU(2) thermalizing. SU(3)→SU(8) queued. |
| **barraCuda** | MultiDevicePool. 4,959 tests. GREEN. | Cross-vendor GPU dispatch. |
| **esotericWebb** | V31b. CELL BOOT SUCCEEDED. Scene builder. 484 tests. | QCD viz via petalTongue. |

---

## CONJUGATION ARCHITECTURE — PRIMAL ↔ BROWSER

Primals are Rust. Browser surfaces need TypeScript. The boundary between them is a **conjugation layer**, not a primal layer.

| Layer | Language | Owns | Examples |
|-------|----------|------|----------|
| **Primal** | Rust | Capabilities, data, compute, provenance | nestGate CAS, petalTongue render, squirrel dispatch |
| **Conjugation** | TypeScript (RustScript) | Safety-pattern translation for non-Rust targets | `Result<T,E>`, `Option<T>`, `Owned<T>`, `RefCell<T>`, `Iter<T>`, `Brand<T,B>` |
| **Browser surface** | HTML/WebGL/WebGPU | User interaction, scene display | Leaflet maps (footPrint), WebGL scenes (esotericWebb), dashboards (nestgate.io) |

**RustScript** (`@protokarya/rustscript`) is the conjugation structure — 11 zero-dep TypeScript modules encoding Rust safety primitives (ownership, borrowing, exhaustive match, RAII, channels). It is not a primal, and it is not scaffolding. It is the acceptable frontend for cases where Rust can't work (browser, TS-native systems). petalTongue owns the render pipeline; RustScript conjugates the safety patterns across the language boundary.

**footPrint** originated as a TypeScript exploration project, became a useful tool and evolution target, and is now evolving toward pure primals. The Express server disappears into nestGate + songBird. The Leaflet/Turf GIS layer evolves toward petalTongue WebGPU rendering. RustScript remains as the conjugation layer between petalTongue's Rust render pipeline and the browser DOM.

---

## K-DERM THREE-DOMAIN TOPOLOGY — FULLY OPERATIONAL

| Layer | Domain | DNS | Status |
|-------|--------|-----|--------|
| **Outer** | `primals.eco` | Cloudflare (wildcard) | **LIVE** — 14 Caddy routes. |
| **Peptidoglycan** | `nestgate.io` | Sovereign Knot DNS + DNSSEC | **LIVE — 20 primals discovered, 8/12 sections.** Tower Atomic dashboard. Neural API bridge. Namespace distribution. Data braids. |
| **Inner** | `primal.eco` | Sovereign Knot DNS (zero public) | **LIVE** — dnsmasq deployed, all 11 gates resolving. |

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| Gates online | **11** |
| Depot | **v4.57+ SYNCED — ALL 6 NUCLEUS GATES DEPLOYED.** 52 builds. |
| Data NAS | **westGate** (3.21 TB / 153 datasets / 17+ domains / **452 GB CAS**) |
| ironGate storage | **12.7 TB CAS LIVE** — `/mnt/nestgate`, nestGate v0.5.0, 9 squirrel providers |
| Primal tests | **~135,000+** |
| Signal dispatch | **G18 LIVE** — ironGate, 9 providers, cross-primal routing validated |
| Convoy provenance | **217/s on NVMe** (700x total). Inline braiding 265/s. 4-tier storage. |
| arXiv | **SU(N) GENERALIZED** (N=2,3,4,5,6,8). 16⁴ dual-GPU CONFIRMED (6 ppm). Paper reframed. 87-config grid RUNNING. 32⁴ target. 42-item rubric. |
| Convergence | **convoy running** — 11M+ files, ~14h ETA at 217/s on NVMe |
| K-derm | **3/3 FULLY OPERATIONAL** |
| GPS data | **CONVERTED** — 11 JSON (103 MB) CAS-ingested with BLAKE3 |

---

## DEBT CLEARING — PER-TEAM PUNCH LIST

Clear all debt so we can focus on downstream gate deployments and science pipelines. Each item is assigned to its **code owner** per the ownership table above. Commit clean, push to Forgejo, depot rebuilds automatically.

### sporeGate team — Provenance Trio (sweetGrass, loamSpine, rhizoCrypt)

| # | Item | Primal | Blocks |
|---|------|--------|--------|
| S1 | **sweetGrass `LedgerClient` refactor** — complete the WIP: `handle_braid_batch_create` + `handle_braid_batch_commit` removed from `braid.rs` but `registry.rs` still references them. Either restore or remove dispatch entries. **Must compile before push.** | sweetGrass | Depot rebuild |
| S2 | **sweetGrass `convergence.check`** — one-call provenance chain verification (CAS → DAG → spine → braid → signed?). Eliminates `convergence_check.py` (183 lines). This is the trust gate for spring data consumption. | sweetGrass | Spring boots |
| S3 | **sweetGrass `braid.list`** — enumerate braids by dataset, time range, committer. No way to audit braids currently. | sweetGrass | Observability |
| S4 | **rhizoCrypt `dag.pipeline.ingest`** — full pipeline in one RPC: file list → session → batch events → dehydrate → Merkle root. Eliminates multi-step Python glue. | rhizoCrypt | westGate scripts |
| S5 | **rhizoCrypt `dag.session.list`** — enumerate active/completed sessions with stats. | rhizoCrypt | Observability |
| S6 | **loamSpine `spine.status`** — report entry count, last commit, Merkle root, associated sessions. | loamSpine | Observability |
| S7 | **nestgate.io NG-01: `mesh.peers`** — wire songBird query into `/api/gate-mesh`. songBird at `/run/membrane/songbird.sock`. | petalTongue (web) | Dashboard |
| S8 | **nestgate.io NG-03: health liveness** — query `health.liveness` per primal via UDS. | petalTongue (web) | Dashboard |
| S9 | **Neural API symlink pattern** — document as canonical. Currently a sporeGate workaround; should be replicated on all NUCLEUS gates. | biomeOS (ops) | Gate deploys |

### biomeGate team — Node Atomics (toadStool, barraCuda, coralReef)

| # | Item | Primal | Blocks |
|---|------|--------|--------|
| B1 | **toadStool `ExecStart` fix** — BLOCKING 9/9 membrane composition. systemd unit doesn't start correctly. | toadStool | Cell boot on all gates |
| B2 | **membrane socket permissions** — `/run/membrane/` sockets are `root:root`. Need group-writable for `biomeos` user. Affects all gates. | toadStool / biomeOS | Cell boot |
| B3 | **coralReef SU(N≥4) shader generalization** — WGSL shaders hardcoded for 3×3 (SU(3)). GPU rendering of SU(4+) needs templated or runtime-generated shaders. Not blocking Rung 1 (CPU measurement suffices) but blocks GPU-accelerated higher-N. | coralReef | G45 Rung 2+ |

### eastGate team — Tower + Agent (bearDog, skunkBat, squirrel)

| # | Item | Primal | Blocks |
|---|------|--------|--------|
| E1 | **bearDog Neural API routing stub** — bearDog doesn't register a capability routing stub with Neural API (NG-04). Other primals do. Means nestgate.io can't show bearDog in the routing table. | bearDog | nestgate.io |
| E2 | **squirrel systemd service on ironGate** — petal-bridge routes `agent.*` → squirrel UDS (`/run/user/1000/biomeos/squirrel.sock`). squirrel needs to be running. Create `squirrel.service`, deploy, validate `agent.query` → `ai.query` translation. | squirrel | Agent panel LIVE |
| E3 | **esotericWebb HEAD method** — `webb.primals.eco` GET=200 but HEAD=502. HTTP handler missing HEAD support (NG-06). | esotericWebb | Live site |

### overwatch — Orchestration (biomeOS, songBird, nestGate, petalTongue, cellMembrane)

| # | Item | Primal | Blocks |
|---|------|--------|--------|
| O1 | **nestGate `content.ingest`** — scan directory, hash all files, bulk store. Eliminates `revalidate_data.py`. **P1 upstream gap.** | nestGate | westGate scripts |
| O2 | **nestGate `content.fetch`** — download URL directly into CAS. Fetch→hash→store in one RPC. Eliminates download-then-ingest scripts. **P2 upstream gap.** | nestGate | Data pipelines |
| O3 | **nestGate `dataset.convergence`** — report provenance state per dataset path in one call. **P1 upstream gap.** | nestGate | Spring trust gate |
| O4 | **nestGate dual-path CAS** — `NESTGATE_HOT_PATH` (NVMe) + `NESTGATE_COLD_PATH` (HDD) for permanent 2-tier. Proposed by westGate convoy AAR. | nestGate | 4-tier storage |
| O5 | **nestGate TCP on westGate** — expose :8080 local-trust (same pattern as ironGate). Register `content` capability with songBird. Unblocks federation. | nestGate + songBird | Inter-gate CAS |
| O6 | **petalTongue scene passthrough** — accept tideGlass declarative format (`{ "scene": "rges_volcano", ... }`). If `SceneGraph` format doesn't match, add passthrough mode. | petalTongue | Viz pipeline |
| O7 | **Inter-gate `content.get` E2E** — live operational test on actual gates (songBird probes ready, nestGate `content.fetch` ready). First test: ironGate pulls object from westGate CAS. | songBird + nestGate | All data-remote springs |
| O8 | **nestGate canonical client crate** — 6 tideGlass CAS divergences (DIV-1→6). groundSpring + airSpring have stale CAS clients. One crate for all consumers. | nestGate | Spring standardization |

### Downstream / Gate Deployment (not code debt — ops)

| # | Item | Gate | Blocks |
|---|------|------|--------|
| D1 | **tideGlass cell boot** on westGate — `biomeos nucleus attach`. GPS data ready. | westGate | Track A science |
| D2 | **squirrel deploy** on ironGate — systemd service + UDS socket. | ironGate | Agent system |
| D3 | **Convoy completion** — 11M+ files at 217/s on NVMe. Post-convoy: rsync hot→cold. | westGate | Data convergence |
| D4 | **SU(N) thermalization** — 87-config grid running. Monitor + measure as configs land. | strandGate | Track B paper |

### Priority for Depot Rebuild

The depot is **currently up to date** — no code debt blocks deployments right now. The items above are feature gaps and WIP that should land cleanly:

1. **S1 (sweetGrass compile fix)** — must land first. Broken WIP must not be pushed.
2. **B1+B2 (toadStool ExecStart + socket perms)** — unblocks clean cell boot on all gates.
3. **E2 (squirrel service)** — unblocks agent panel on ironGate.
4. **O5 (nestGate TCP on westGate)** — unblocks inter-gate federation.

Everything else is P2/P3 feature work that can land incrementally without blocking gate deployments.

### Data Flow Map — Target State

| Consumer | Data Source | Transport | Viz Layer | Status |
|----------|-----------|-----------|-----------|--------|
| **tideGlass** | westGate CAS (452 GB, GPS) | UDS `CasClient` → nestGate | 5 petalTongue scenes (`PetalTongueClient` LIVE, `is_viz_method()` gate) | **VIZ FORWARDING LIVE — needs cell boot on westGate** |
| **footPrint** | ironGate CAS (12.7 TB) | TCP :8080 `NeuralApiClient` | **petal-bridge.ts** dual-socket WS↔UDS (agent→squirrel, viz→petal) | **BRIDGE WIRED — needs squirrel UDS socket** |
| **esotericWebb** | ironGate CAS via squirrel | UDS signal dispatch | petalTongue `visualization.render.scene` via cell graph | **IPC works — needs petalTongue WebGL (G19) + HEAD fix** |
| **nestgate.io** | sporeGate Neural API (20 primals) | UDS symlink bridge | Tower Atomic dashboard, routing table, namespace chart | **8/12 SECTIONS LIVE — needs mesh.peers + health liveness** |

### LIVE SITE ASSESSMENT (Aug 5 PM)

| Site | URL | Status | Issue |
|------|-----|--------|-------|
| **sporePrint** | `sporeprint.primals.eco` | **LIVE** | Zola static. Science content. Claims verifiable. |
| **footPrint** | `footprint.primals.eco` | **LIVE, auto-loads** | petal-bridge wired. Auto-load default project. `SKIP_CSP=1`. **Remaining**: squirrel UDS socket for agent panel. |
| **nestgate.io** | `nestgate.io` | **LIVE, 8/12 sections** | Neural API bridge wired. 20 primals discovered. Tower Atomic layers, routing table, namespace chart visible. **Remaining**: `mesh.peers` for gate table (NG-01), health liveness per primal (NG-03). |
| **esotericWebb** | `webb.primals.eco` | **GET 200 / HEAD 502** | HTML served correctly. HEAD method missing in upstream handler (NG-06). Needs petalTongue WebGL for live game surface (G19). |

---

*Wave 156e — **LAN HPC Enmeshment Era.** The mesh is becoming functional: nestgate.io discovers 20 primals and renders a Tower Atomic architecture dashboard. footPrint bridges browser→squirrel+petalTongue via dual-socket relay. tideGlass forwards viz scenes to petalTongue on dispatch. hotSpring generalizes to SU(N) with a 87-config thermalization grid. westGate runs convoy on NVMe at 217/s (700x total improvement). biomeOS Neural API is confirmed as the routing backbone — all consumers discover primals through it, not hardcoded sockets. squirrel agent system is the next unlock: deploy squirrel on ironGate, connect petal-bridge, and the agent panel goes live.*

*59 glacial goals (9 COMPLETE, 30 ACTIVE). 151 docs fossilized (1,472 total records, 10 checkpoints). ~136K+ tests, 13/13 GREEN.*
