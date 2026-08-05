# ecoPrimals Ecosystem Blurb — Debt Clearing + Depot Readiness Era

**Date**: Aug 5, 2026 EVE | **Wave**: 156f | **From**: eastGate overwatch → sporeGate execution
**Posture**: **P0/P1/P2: ZERO. 14/26 DEBT ITEMS CLEARED (S1–S8 + S4–S5 pre-shipped + B1–B2 + O1/O3/O4/O8). ALL 15 PRIMALS COMPILE CLEAN. DEPOT REBUILT — 26 binaries pushed to golgi. blueGate sub-builder PROVEN (15/15 Windows). nestgate.io 10/12 sections (health liveness 11/13 alive). ~140K+ tests, 15/15 GREEN.**

---

## WHAT SPOREGATE EXECUTED THIS SESSION

| Item | Status | Detail |
|------|--------|--------|
| **Fleet health** | DONE | 6 songBird peers (4 LAN p0, 2 WG p1). 14/14 NUCLEUS active. |
| **Depot divergence scan** | DONE | 5 primals behind on sporeGate, 8 on blueGate — all pulled to HEAD. |
| **S8: health.liveness (NG-03)** | DONE | `/api/primal-health` — 13 UDS sockets queried concurrently with BTSP framing. 11/13 alive. Dashboard shows per-primal status + version. |
| **blueGate sub-builder** | DONE | 15/15 Windows builds dispatched + completed on blueGate. Parallel with sporeGate musl harvest. |
| **Full depot rebuild** | DONE | 15/15 musl, 15/15 Windows. 26 binaries pushed to golgi. |
| **AAR** | DONE | 8 divergences documented (UDS protocol fragmentation, socket paths, harvest exit codes, timeout sizing). |

---

## DIVERGENCES DOCUMENTED (see AAR)

| ID | Issue | Status |
|----|-------|--------|
| DIV-1 | sweetGrass `as_nanos()` API break (cross-primal dep) | Resolved — upstream pull |
| DIV-2 | songBird UDS plain JSON, not BTSP | Resolved — removed BTSP from songBird query |
| DIV-3 | bearDog multi-object UDS response | Resolved — streaming JSON parser |
| DIV-4 | coralReef tarpc, not JSON-RPC | Known — architecture difference |
| DIV-5 | toadStool socket perms | Open — B1/B2 binary needs local deploy |
| DIV-6 | petalTongue socket in user dir, not /run/membrane | Resolved — full path mapping |
| DIV-7 | `plasmid.harvest` exit code unreliable | Open — binary presence is reliable signal |
| DIV-8 | Large primals exceed 300s timeout | Resolved — blueGate should build these |

---

## REMAINING CROSS-TEAM ITEMS (for dissemination)

### eastGate team
- **E1**: bearDog Neural API routing stub
- **E2**: squirrel systemd on ironGate (agent panel)
- **E3**: esotericWebb HEAD method

### biomeGate team
- **B3**: coralReef SU(N≥4) shader generalization
- coralReef tarpc health endpoint or Neural API stub

### overwatch
- **O2**: nestGate `content.fetch` (verify Session 133)
- **O5**: nestGate TCP on westGate (ops config)
- **O6**: petalTongue scene passthrough
- **O7**: Inter-gate `content.get` E2E
- **S9**: Neural API symlink — document as canonical
- UDS protocol standardization (BTSP vs plain JSON)
- `plasmid.harvest` exit code reliability

### ops / gate deployment
- **D1**: tideGlass cell boot on westGate
- **D2**: squirrel deploy on ironGate
- **D3**: Convoy completion (11M+ files)
- **D4**: SU(N) thermalization monitoring

---

## sporeGate TEAM STATUS

**Backlog: CLEAR.** S1–S8 all done. S9 is ops documentation (ready to write when needed). No code debt remains on sweetGrass, loamSpine, or rhizoCrypt.

**Depot: FRESH.** All 15 primals built Aug 5. 26 binaries synced to golgi. Gates can pull.

**blueGate: PROVEN.** Sub-builder pattern works. blueGate handles Windows depot natively. Should be filed up before sporeGate for all future builds.

---

*Wave 156f — sporeGate backlog CLEAR. 14/26 ecosystem debt items resolved. Depot rebuilt and pushed. blueGate sub-builder proven for parallel builds. nestgate.io at 10/12 sections with live health liveness. Remaining items are cross-team — overwatch will disseminate.*

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

**ZFS**: 3.21 TB used / 50.7 TB pool (6.3%). CAS pool: **452 GB** (convoy at 145/s).

**Key**: 0 datasets at CONVERGED. Convoy ACTIVE (145/s, ~15h ETA for 7.9M remaining files). Priority: batch the 89 PARTIAL first (smallest datasets), then CAS-ingest 32 PRIMORDIAL.

---

## PRIMAL HEALTH DASHBOARD

| Primal | Tests | Health | Recent |
|--------|-------|--------|--------|
| **songBird** | 14,840+ | GREEN | 22 drawbridge bonds. LAN-first Tower (1ms). |
| **bearDog** | 14,019 | GREEN | 94 orphans purged |
| **nestGate** | 13,095+ | GREEN | **`content.query` SHIPPED.** ZFS REST. tarpc 0.37. nestgate.io wired. |
| **toadStool** | 9,193+ | GREEN | S351: -48 dead deps. Symlink fix. |
| **biomeOS** | 8,570+ | GREEN | **v4.57: `nucleus attach` — CELL BOOT SUCCEEDED.** westGate DEPLOYED. |
| **petalTongue** | 6,755 | GREEN | nestgate.io branded. TCP hardened. FAMILY_ID unified. |
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
| **tideGlass** | 177 tests. 9 crates. Live NUCLEUS on westGate. **GPS data CONVERTED** (11 JSON, 103 MB). | `nucleus attach` on westGate (v4.57 DEPLOYED). Chen 2017 benchmark. |
| **footPrint** | **PHASE 2 DEPLOYED on ironGate.** 708 tests. CAS E2E. Agent bridge. | golgi Caddy routing. GPS viz integration. |
| **westGate data** | 3.21 TB / 153 datasets. GPS JSON in CAS. 135 GB CAS pool. **Convergence**: 0 CONVERGED, 89 PARTIAL, 32 PRIMORDIAL. | Batch provenance campaign. |
| **nestGate** | **`content.query` SHIPPED.** nestgate.io content backend wired. | Wire into tideGlass for GPS metadata search. |
| **Provenance trio** | 7/7. Loop CLOSED. 122× improvement. | Bulk convergence campaign across 153 datasets. |

### Track B: Lattice QCD on Consumer GPUs (Murillo / Chuna)

| Component | Status | Next |
|-----------|--------|------|
| **strandGate** | 12⁴ paper-ready. **16⁴ DUAL-GPU DATA COMPLETE** — β=6.0 +0.01%, β=6.2 -0.04% vs published. Cross-vendor 6 ppm. AMD 9.4x faster. | Rubric items → LaTeX → reviewer send → arXiv submit. |
| **hotSpring** | 5 arxiv binaries. Parallel therm 279→95 min. Config cache LIVE. | Rung 1 production campaign. |
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
| **Peptidoglycan** | `nestgate.io` | Sovereign Knot DNS + DNSSEC | **LIVE** — branded "ecoPrimals Data Surface". Content backend wired. |
| **Inner** | `primal.eco` | Sovereign Knot DNS (zero public) | **LIVE** — dnsmasq deployed, all 11 gates resolving. |

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| Gates online | **11** |
| Depot | **v4.57+ SYNCED — ALL 6 NUCLEUS GATES DEPLOYED.** 52 builds. |
| Data NAS | **westGate** (3.21 TB / 153 datasets / 17+ domains / **866 GB ZFS CAS + 303 GB NVMe hot**) |
| ironGate storage | **12.7 TB CAS LIVE** — `/mnt/nestgate`, nestGate v0.5.0, 9 squirrel providers |
| Primal tests | **~135,000+** |
| Signal dispatch | **G18 LIVE** — ironGate, 9 providers, cross-primal routing validated |
| Convoy provenance | **313/s instantaneous** (NVMe hot tier, 2.4× over spinner). Rust primals at ~5ms/file — never the bottleneck. |
| arXiv Rung 1 | **16⁴ DATA COMPLETE** — +0.01% at β=6.0, 6 ppm cross-vendor. 42-item reviewer rubric. |
| Convergence | **convoy running** — 4.8M braided / 11M total (44%), ETA ~midnight tonight |
| K-derm | **3/3 FULLY OPERATIONAL** |
| GPS data | **CONVERTED** — 11 JSON (103 MB) CAS-ingested with BLAKE3 |

---

## NEXT PHASE: DATA FLOW ACTIVATION + PETAL VIS

The infrastructure is deployed. Data flows need to be turned on. petalTongue needs to become the visualization layer. RustScript is the conjugation structure for the browser boundary.

### Gate Team Assignments

**westGate team** (Data NAS):

1. **tideGlass cell boot** — `biomeos nucleus attach --cell ~/graphs/tideglass_cell.toml`. GPS data is converted (11 JSON, 103 MB in CAS). Verify tideGlass discovers nestGate socket via Neural API scan. Test `content.query` against 452 GB CAS pool. Run one end-to-end: `science.rges_screen` → `viz.rges_volcano` → scene JSON.
2. **Federation unblock** — expose nestGate on TCP (same pattern as ironGate :8080 local-trust). Register `content` capability with songBird. This unblocks ironGate's `content.replicate.pull`.
3. **Convoy convergence** — 7.9M files at 145/s (~15h ETA). CAS pool at 452 GB. Monitor and report completion.

**ironGate team** (Downstream host):

1. **footPrint → squirrel** — G18 signal dispatch is LIVE with 9 providers. footPrint's `petal-tongue.ts` WebSocket client points at petalTongue `:3001/ws`. Wire the agent panel: `agentConnected` should become `true` when squirrel registers as a provider. The WebSocket bridge exists — it needs the connection to succeed.
2. **tideGlass PetalTongueClient activation** — in `tideglass-bin/src/petaltongue.rs`, the client is `#[allow(dead_code)]`. Remove `dead_code`, instantiate in the dispatch loop (`dispatch.rs`). When a petalTongue socket is discovered, the 5 viz handlers (`viz.rges_volcano`, `viz.enrichment_curve`, `viz.gps4drug_scatter`, `viz.mcts_trace`, `viz.nf_dashboard`) should forward their scene JSON to `PetalTongueClient::render_scene()` in addition to returning it.
3. **petalTongue scene passthrough** — `visualization.render.scene` handler already accepts `SceneGraph` JSON via UDS. Verify it can accept tideGlass's declarative format (`{ "scene": "rges_volcano", "data": {...}, "format": "webgl", "interactive": true }`). If the format doesn't match `SceneGraph`, add a passthrough mode for declarative scene JSON.

**strandGate team** (Compute):

1. **arXiv Rung 1 rubric** — 16⁴ data COMPLETE. Address 12 MUST-fix items from `whitePaper/subGen/ARXIV_REVIEWER_RUBRIC.md` (figures, jackknife errors, 1-paragraph abstract, 25-30 references, genericize ecosystem jargon, remove gauge group audit appendix, fix pseudoSpore URL to `su3`). LaTeX regen via tectonic. Target: send PDF to Murillo/Chuna/Bazavov.

**eastGate overwatch** (You):

1. **RustScript extraction** — `protists/footPrint/src/rustscript/` already has `package.json` for `@protokarya/rustscript`. Publish as standalone npm package. This is the conjugation layer for all TypeScript consumers of primals.
2. **petalTongue TypeScript SDK** — create `@protokarya/petaltongue-client` wrapping `petal-tongue.ts` with RustScript types. Scene handles become `Result<SceneHandle, RpcError>`. This becomes the standard browser ↔ primal bridge for any TS project (footPrint, nestgate.io, future mobile).

### Data Flow Map — Target State

| Consumer | Data Source | Transport | Viz Layer | Status |
|----------|-----------|-----------|-----------|--------|
| **tideGlass** | westGate CAS (452 GB, GPS) | UDS `CasClient` → nestGate | 5 petalTongue scenes (volcano, enrichment, scatter, MCTS, NF) | **READY — needs cell boot** |
| **footPrint** | ironGate CAS (12.7 TB) | TCP :8080 `NeuralApiClient` | petalTongue WebSocket → map overlays (conjugated via RustScript) | **CAS E2E works — needs squirrel + petal wiring** |
| **esotericWebb** | ironGate CAS via squirrel | UDS signal dispatch | petalTongue `visualization.render.scene` via cell graph | **IPC works — needs petalTongue WebGL pipeline (G19)** |
| **nestgate.io** | sporeGate mesh | HTTP (public) | petalTongue SSR or WebSocket bridge | **Dashboard loads — needs mesh bridge** |

### LIVE SITE ASSESSMENT

| Site | URL | Status | Issue |
|------|-----|--------|-------|
| **sporePrint** | `sporeprint.primals.eco` | **LIVE, renders well** | Zola static site. Science content. Claims verifiable. |
| **footPrint** | `footprint.primals.eco` | **LIVE, serves 200** | CAS works (3 objects, 1 real project). Map empty — no auto-load, `agentConnected:false`. Wire squirrel → petal WebSocket. |
| **nestgate.io** | `nestgate.io` | **LIVE, serves 200** | Dashboard "Loading..." — needs petalTongue mesh bridge or SSR pre-render. |
| **esotericWebb** | `webb.primals.eco` | **502** | IPC-only CRPG engine. Needs petalTongue WebGL pipeline (G19) for browser surface. |

---

*Wave 156d — **Data Flow Activation Era.** Infrastructure deployed across all 6 NUCLEUS gates. G18 signal dispatch LIVE (9 providers). ironGate 12.7 TB CAS + westGate 452 GB CAS. Convoy at 145/s (460x). 16⁴ dual-GPU data COMPLETE (6 ppm, +0.01%). Reviewer rubric 42 items. **Next phase**: activate data flows (tideGlass cell boot, footPrint→squirrel, federation unblock), wire petalTongue as visualization layer (5 tideGlass scenes, footPrint map overlays), establish RustScript as the conjugation layer (`@protokarya/rustscript` → `@protokarya/petaltongue-client`). footPrint evolved from TS exploration to primal evolution target; RustScript is the acceptable frontend for the browser boundary, not scaffolding.*

*59 glacial goals (9 COMPLETE, 30 ACTIVE). 145 docs fossilized (1,462 total records, 10 checkpoints). ~135K+ tests, 13/13 GREEN.*
