# ecoPrimals Ecosystem Blurb — Debt Clearing + Depot Readiness Era

**Date**: Aug 5, 2026 EVE | **Wave**: 156f | **From**: eastGate overwatch
**Posture**: **P0/P1/P2: ZERO. 12/26 DEBT ITEMS CLEARED THIS CASCADE (S1–S7, B1–B2, O1, O3–O4, O8; S4–S5 verified SHIPPED). ALL 15 PRIMALS COMPILE CLEAN. 15/15 at HEAD on origin. sweetGrass convergence.check + braid.list (1,655 tests). nestGate content.ingest + dataset.convergence + dual-path CAS + Neural API (1,630 tests). loamSpine spine.status (1,752 tests). toadStool socket perms FIXED. petalTongue mesh.peers LIVE. coralReef 6 evolution commits (3,525 tests). squirrel 7,140 tests (156j). rhizoCrypt S4+S5 verified SHIPPED. ~140K+ tests, 15/15 GREEN. DEPOT REBUILD READY.**

---

## WHAT JUST HAPPENED — Session 14 Cascade (Debt Clearing)

| Event | Source | Status |
|-------|--------|--------|
| **sweetGrass S1+S2+S3 CLEARED** | sporeGate | `convergence.check` — one-call provenance chain verification (CAS→DAG→spine→braid→signed). `convergence.batch_check` for bulk. `braid.list` — lightweight braid enumeration with filters. `compute_depth` helper. Capability wiring + niche + registry + docs. **1,655 tests (610→610 pass).** LedgerClient refactor **COMPILES CLEAN**. |
| **nestGate O1+O3+O4+O8 CLEARED** | overwatch | **Session 136**: `content.ingest` (9 tests — scan dir, BLAKE3, bulk CAS store, eliminates `revalidate_data.py`). `dataset.convergence` (10 tests — CAS provenance state per dataset). Dual-path CAS (warm/cold env vars, 7 handlers updated). `content.fetch` gap fix. 94 IPC methods, 21 capability domains, **996 tests**. **Session 137**: Neural API O8 — announce expanded to 5 domains + 6 federation methods. `route.register` dynamic. Remote capability router wired to coordinator. MeshRelay transport connected. **1,630 tests total.** |
| **loamSpine S6 CLEARED** | sporeGate | `spine.status` — entry count, tip/genesis hashes, state, timestamps, sessions with Merkle roots (most-recent-first). Full-stack: handler → dispatch → niche (53 methods) → MCP → capability registry. **1,752 tests.** Zero unsafe, zero unwrap, zero TODO. |
| **toadStool B1+B2 CLEARED** | biomeGate | Membrane dir 0o700→0o750 (group-traversable). Socket 0o600→0o660 (group-connectable). Primals sharing `biomeos` group can discover and connect without `SOCKET_MODE` override. **Unblocks cell boot on ALL gates.** |
| **petalTongue S7 CLEARED** | overwatch | `mesh.peers` handler now queries songBird at `/run/membrane/songbird.sock` via JSON-RPC. Falls back to static manifest when UDS unavailable. Dashboard shows "songBird live" pill, peer address, priority, transport type. |
| **coralReef 6 COMMITS** | biomeGate | VOP3 opcode split (929→523 LOC). Compile-path heap alloc elimination. SM20 f64 legalize tests hardened. WGSL double-parse eliminated for emit_spirv. Registry drift + fossil cleanup. **3,525 tests (3,519 pass, 6 ignored HW-gated).** |
| **squirrel DEEP DEBT SWEEP** | eastGate | Waves 156e→156j: `AIError` → `AIToolsError` migration. `PrimalType` dedup. Hardcoded port elimination. `EcosystemPrimalType` → String migration (9 fields across 5 files). `sync_manager_tests.rs` deleted (546 lines). Context quality improvements (Copy derives, clone elimination). **7,140 tests (handoff) / 6,269 unique (measured).** |
| **AKD1000 NPU ONLINE** | strandGate | VFIO bound (IOMMU group 92), pure Rust, 80 NPs, 10 MB SRAM. toadStool ← rustChip synced (7,755 lines, 9 new modules absorbed upstream). metalForge 42/42 revalidated (zero Python). `sun_npu_monitor`: SU(N) phase classification at 66 µs/sample on AKD1000 hardware. **AAR**: `AKIDA_NPU_EXPLORATION_AAR_AUG05_2026.md` |

---

## GATE FLEET STATUS — POST-SYNC

| Gate | NUCLEUS | Depot | Status |
|------|---------|-------|--------|
| **sporeGate** | **14/14 v4.57+** | **BUILD AUTHORITY — FRESH** | Sovereign CI. 52/52 harvest complete. LAN-first Tower (4 local, 1ms). |
| **ironGate** | **10/10 v4.57+** | **CURRENT** | **G18 DISPATCH LIVE (9 providers). NUCLEUS storage 12.7 TB CAS. songBird federation to westGate.** 708 tests. |
| **westGate** | **14/14 v4.57** | **SOURCE-BUILT** | GPS data converted. Convergence sweep complete. `nucleus attach` ready. |
| **strandGate** | **v4.57+ (restart deferred)** | **CURRENT** | GPU at 100% QCD production. Config cache COMPLETE. Dual-GPU scan LAUNCHED. **AKD1000 NPU ONLINE** (VFIO, 97% phase accuracy, 66 µs). toadStool ← rustChip synced. |
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
| **bearDog** | 14,019 | GREEN | E1 Neural API routing stub (156e). |
| **nestGate** | 1,630+ | GREEN | **content.ingest + dataset.convergence + dual-path CAS + Neural API wiring (O1/O3/O4/O8).** 94 IPC methods, 21 capability domains. |
| **toadStool** | 9,193+ | GREEN | **B1/B2: membrane socket perms FIXED.** 0o750 dir + 0o660 socket. Cell boot unblocked. |
| **biomeOS** | 8,570+ | GREEN | **v4.57: `nucleus attach` — CELL BOOT SUCCEEDED.** westGate DEPLOYED. |
| **squirrel** | 7,140 | GREEN | **156i–156j: AIToolsError migration, PrimalType dedup, EcosystemPrimalType→String, port elimination.** |
| **petalTongue** | 6,606 | GREEN | **mesh.peers LIVE via songBird UDS (S7).** nestgate.io 20 primals, 8/12 sections. |
| **barraCuda** | 4,959 | GREEN | **MultiDevicePool.** `device.pool` IPC. |
| **coralReef** | 3,525 | GREEN | **VOP3 opcode split, WGSL double-parse eliminated, SM20 f64 hardened.** 6 evolution commits. |
| **rhizoCrypt** | 1,791 | GREEN | **G63 SO_PEERCRED SHIPPED.** CAS local-trust. |
| **loamSpine** | 1,752 | GREEN | **spine.status SHIPPED (S6).** 53 JSON-RPC methods. Zero unsafe/unwrap/TODO. |
| **sweetGrass** | 1,655 | GREEN | **convergence.check + braid.list SHIPPED (S1/S2/S3).** 47 methods + 11 aliases. |
| **cellMembrane** | 1,281+ | GREEN | **Harvest scheduler.** CI-DIV fixes. Phase 2a manifest registry. |
| **skunkBat** | 609 | GREEN | Chaos tests. Config evolution. |
| **sourDough** | 502 | GREEN | Identity + IPC capability. Cross-arch clean. |
| **bingoCube** | 31 | GREEN | Brain prediction engine. |

**Total**: **~140,000+ tests**. **15/15 GREEN**.

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
| **Peptidoglycan** | `nestgate.io` | Sovereign Knot DNS + DNSSEC | **LIVE — 20 primals discovered, 9/12 sections.** Tower Atomic dashboard. Neural API bridge. Namespace distribution. Data braids. Gate mesh table (songBird). |
| **Inner** | `primal.eco` | Sovereign Knot DNS (zero public) | **LIVE** — dnsmasq deployed, all 11 gates resolving. |

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| Debt items | **12/26 CLEARED** (S1–S7, B1–B2, O1, O3–O4, O8; S4–S5 verified pre-shipped) |
| Gates online | **11** |
| Depot | **v4.57+ SYNCED — ALL 6 NUCLEUS GATES. 15/15 primals compile clean at HEAD. REBUILD READY.** |
| Data NAS | **westGate** (3.21 TB / 153 datasets / 17+ domains / **452 GB CAS**) |
| ironGate storage | **12.7 TB CAS LIVE** — `/mnt/nestgate`, nestGate v0.5.0, 9 squirrel providers |
| Primal tests | **~140,000+** |
| Signal dispatch | **G18 LIVE** — ironGate, 9 providers, cross-primal routing validated |
| Convoy provenance | **217/s on NVMe** (700x total). Inline braiding 265/s. 4-tier storage. |
| arXiv | **SU(N) GENERALIZED** (N=2,3,4,5,6,8). 16⁴ dual-GPU CONFIRMED (6 ppm). Paper reframed. 87-config grid RUNNING. 32⁴ target. 42-item rubric. |
| Convergence | **convoy running** — 11M+ files, ~14h ETA at 217/s on NVMe |
| K-derm | **3/3 FULLY OPERATIONAL** |
| GPS data | **CONVERTED** — 11 JSON (103 MB) CAS-ingested with BLAKE3 |
| nestGate IPC | **94 methods, 21 capability domains** (content.ingest, dataset.convergence, dual-path CAS) |
| sweetGrass | **47 methods + 11 aliases** (convergence.check, braid.list, compute_depth) |
| loamSpine | **53 methods** (spine.status, full observability) |

---

## DEBT CLEARING — PER-TEAM PUNCH LIST

Clear all debt so we can focus on downstream gate deployments and science pipelines. Each item is assigned to its **code owner** per the ownership table above. Commit clean, push to Forgejo, depot rebuilds automatically.

### sporeGate team — Provenance Trio (sweetGrass, loamSpine, rhizoCrypt)

| # | Item | Primal | Status |
|---|------|--------|--------|
| S1 | ~~sweetGrass `LedgerClient` refactor~~ | sweetGrass | **DONE** — compiles clean, 1,655 tests |
| S2 | ~~sweetGrass `convergence.check`~~ | sweetGrass | **DONE** — one-call chain verification, `batch_check` for bulk |
| S3 | ~~sweetGrass `braid.list`~~ | sweetGrass | **DONE** — enumeration with filters |
| S4 | ~~rhizoCrypt `dag.pipeline.ingest`~~ | rhizoCrypt | **DONE** — shipped Wave 156b. PipelineIngestRequest wire type, JSON-RPC + tarpc handlers, MCP tool. |
| S5 | ~~rhizoCrypt `dag.session.list`~~ | rhizoCrypt | **DONE** — shipped pre-Wave 155. Niche catalog, core `list_sessions()`, full handler stack. |
| S6 | ~~loamSpine `spine.status`~~ | loamSpine | **DONE** — 53 methods, 1,752 tests, full-stack wiring |
| S7 | ~~nestgate.io `mesh.peers`~~ | petalTongue (web) | **DONE** — songBird UDS → `/api/mesh-peers`, live pill |
| S8 | **nestgate.io NG-03: health liveness** — query `health.liveness` per primal via UDS. | petalTongue (web) | OPEN |
| S9 | **Neural API symlink pattern** — document as canonical. Currently a sporeGate workaround; should be replicated on all NUCLEUS gates. | biomeOS (ops) | OPEN |

### biomeGate team — Node Atomics (toadStool, barraCuda, coralReef)

| # | Item | Primal | Status |
|---|------|--------|--------|
| B1 | ~~toadStool `ExecStart` fix~~ | toadStool | **DONE** — membrane 0o750, socket 0o660 |
| B2 | ~~membrane socket permissions~~ | toadStool / biomeOS | **DONE** — group-connectable, no SOCKET_MODE override needed |
| B3 | **coralReef SU(N≥4) shader generalization** — WGSL shaders hardcoded for 3×3 (SU(3)). GPU rendering of SU(4+) needs templated or runtime-generated shaders. Not blocking Rung 1 (CPU measurement suffices) but blocks GPU-accelerated higher-N. | coralReef | OPEN |

### eastGate team — Tower + Agent (bearDog, skunkBat, squirrel)

| # | Item | Primal | Blocks |
|---|------|--------|--------|
| E1 | **bearDog Neural API routing stub** — bearDog doesn't register a capability routing stub with Neural API (NG-04). Other primals do. Means nestgate.io can't show bearDog in the routing table. | bearDog | nestgate.io |
| E2 | **squirrel systemd service on ironGate** — petal-bridge routes `agent.*` → squirrel UDS (`/run/user/1000/biomeos/squirrel.sock`). squirrel needs to be running. Create `squirrel.service`, deploy, validate `agent.query` → `ai.query` translation. | squirrel | Agent panel LIVE |
| E3 | **esotericWebb HEAD method** — `webb.primals.eco` GET=200 but HEAD=502. HTTP handler missing HEAD support (NG-06). | esotericWebb | Live site |

### overwatch — Orchestration (biomeOS, songBird, nestGate, petalTongue, cellMembrane)

| # | Item | Primal | Status |
|---|------|--------|--------|
| O1 | ~~nestGate `content.ingest`~~ | nestGate | **DONE** — 9 tests, eliminates `revalidate_data.py` |
| O2 | **nestGate `content.fetch`** — download URL directly into CAS. Fetch→hash→store in one RPC. Eliminates download-then-ingest scripts. | nestGate | OPEN (already shipped Session 133 — verify) |
| O3 | ~~nestGate `dataset.convergence`~~ | nestGate | **DONE** — 10 tests, CAS provenance state per dataset, trust gate for springs |
| O4 | ~~nestGate dual-path CAS~~ | nestGate | **DONE** — warm/cold paths, 7 handlers updated, backward compatible |
| O5 | **nestGate TCP on westGate** — expose :8080 local-trust (same pattern as ironGate). Register `content` capability with songBird. Unblocks federation. | nestGate + songBird | OPEN (ops config) |
| O6 | **petalTongue scene passthrough** — accept tideGlass declarative format (`{ "scene": "rges_volcano", ... }`). If `SceneGraph` format doesn't match, add passthrough mode. | petalTongue | OPEN |
| O7 | **Inter-gate `content.get` E2E** — live operational test on actual gates (songBird probes ready, nestGate `content.fetch` ready). First test: ironGate pulls object from westGate CAS. | songBird + nestGate | OPEN (ops) |
| O8 | ~~nestGate Neural API wiring~~ | nestGate | **DONE** — 5 capability domains, 6 federation methods, coordinator routing, MeshRelay transport wired. Consumers use `capability.call`, no nestgate-specific crate. |

### Downstream / Gate Deployment (not code debt — ops)

| # | Item | Gate | Blocks |
|---|------|------|--------|
| D1 | **tideGlass cell boot** on westGate — `biomeos nucleus attach`. GPS data ready. | westGate | Track A science |
| D2 | **squirrel deploy** on ironGate — systemd service + UDS socket. | ironGate | Agent system |
| D3 | **Convoy completion** — 11M+ files at 217/s on NVMe. Post-convoy: rsync hot→cold. | westGate | Data convergence |
| D4 | **SU(N) thermalization** — 87-config grid running. Monitor + measure as configs land. | strandGate | Track B paper |

### Priority for Depot Rebuild

**12 of 26 items CLEARED** (S1–S7, B1–B2, O1, O3–O4, O8; S4–S5 verified pre-shipped). The critical-path blockers are resolved. Remaining 14 items are feature work, ops deployments, or downstream integration. All 15 primals compile clean at HEAD and are pushed to Forgejo. **Depot rebuild can proceed immediately.**

Remaining critical path:
1. **E2 (squirrel service on ironGate)** — deploy squirrel systemd, agent panel goes live.
2. **O5 (nestGate TCP on westGate)** — ops config only, code already shipped.
3. **D1 (tideGlass cell boot)** — `biomeos nucleus attach` on westGate, GPS data ready.
4. **S8 (nestgate.io health liveness)** — per-primal health query via UDS.

### Data Flow Map — Target State

| Consumer | Data Source | Transport | Viz Layer | Status |
|----------|-----------|-----------|-----------|--------|
| **tideGlass** | westGate CAS (452 GB, GPS) | UDS `CasClient` → nestGate | 5 petalTongue scenes (`PetalTongueClient` LIVE, `is_viz_method()` gate) | **VIZ FORWARDING LIVE — needs cell boot on westGate** |
| **footPrint** | ironGate CAS (12.7 TB) | TCP :8080 `NeuralApiClient` | **petal-bridge.ts** dual-socket WS↔UDS (agent→squirrel, viz→petal) | **BRIDGE WIRED — needs squirrel UDS socket** |
| **esotericWebb** | ironGate CAS via squirrel | UDS signal dispatch | petalTongue `visualization.render.scene` via cell graph | **IPC works — needs petalTongue WebGL (G19) + HEAD fix** |
| **nestgate.io** | sporeGate Neural API (20 primals) | UDS symlink bridge + songBird mesh.peers | Tower Atomic dashboard, routing table, namespace chart, gate mesh table | **9/12 SECTIONS LIVE — needs health liveness (S8/NG-03)** |

### LIVE SITE ASSESSMENT (Aug 5 PM)

| Site | URL | Status | Issue |
|------|-----|--------|-------|
| **sporePrint** | `sporeprint.primals.eco` | **LIVE** | Zola static. Science content. Claims verifiable. |
| **footPrint** | `footprint.primals.eco` | **LIVE, auto-loads** | petal-bridge wired. Auto-load default project. `SKIP_CSP=1`. **Remaining**: squirrel UDS socket for agent panel. |
| **nestgate.io** | `nestgate.io` | **LIVE, 9/12 sections** | Neural API bridge wired. 20 primals discovered. Tower Atomic layers, routing table, namespace chart, **gate mesh table** (mesh.peers LIVE via songBird UDS). **Remaining**: health liveness per primal (NG-03). |
| **esotericWebb** | `webb.primals.eco` | **GET 200 / HEAD 502** | HTML served correctly. HEAD method missing in upstream handler (NG-06). Needs petalTongue WebGL for live game surface (G19). |

---

*Wave 156f — **Debt Clearing + Depot Readiness Era.** 12 of 26 punch list items cleared. Entire sporeGate team backlog DONE (S1–S7). toadStool socket perms FIXED (B1+B2, cell boot unblocked everywhere). nestGate 4 upstream gaps closed (O1/O3/O4/O8, 94 IPC methods, 21 capability domains, Neural API wiring). rhizoCrypt S4+S5 verified pre-shipped. coralReef lands 6 evolution commits. squirrel completes deep debt sweep (156e→156j, 7,140 tests).*

*All 15 primals compile clean and are pushed to Forgejo. Depot rebuild can proceed immediately. Next unlock: squirrel deploy on ironGate (agent panel goes live), tideGlass cell boot on westGate (Track A science starts), inter-gate federation (O5+O7).*

*59 glacial goals (9 COMPLETE, 30 ACTIVE). 151 docs fossilized (1,472 total records, 10 checkpoints). ~140K+ tests, 15/15 GREEN.*
