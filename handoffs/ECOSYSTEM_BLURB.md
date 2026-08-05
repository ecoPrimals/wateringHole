# ecoPrimals Ecosystem Blurb — Signal Dispatch + Federation Era

**Date**: Aug 5, 2026 AM | **Wave**: 156d | **From**: eastGate overwatch
**Posture**: **P0/P1/P2: ZERO. ALL 6 NUCLEUS GATES v4.57+. G18 SIGNAL DISPATCH LIVE (ironGate, 9 providers). ironGate NUCLEUS storage LIVE (12.7 TB CAS, songBird federation to westGate configured). Convoy provenance at 145/s (460x total improvement). 16⁴ DUAL-GPU DATA COMPLETE (cross-vendor parity: 6 ppm at β=6.2, +0.01% vs published at β=6.0). tideGlass 214 tests, 17 IPC methods. Reviewer rubric shipped (42 items). ~135K+ tests, 13/13 GREEN.**

---

## WHAT JUST HAPPENED — Session 10-12 Cascade

| Event | Gate | Status |
|-------|------|--------|
| **G18 SIGNAL DISPATCH LIVE** | ironGate | squirrel rebuilt from source, `signal.dispatch` operational. 7→9 primal providers. Cross-primal routing validated: squirrel → rhizoCrypt (1ms), squirrel → bearDog (crypto hash). |
| **ironGate NUCLEUS STORAGE LIVE** | ironGate | 12.7 TB ext4 disk (`/dev/sdc1`) mounted at `/mnt/nestgate`. nestGate v0.5.0 with BLAKE3 CAS. TCP local-trust + UDS BTSP. CAS roundtrips through footPrint and esotericWebb validated. |
| **songBird FEDERATION to westGate** | ironGate → westGate | songBird configured with `SONGBIRD_PEERS=westgate@192.168.4.149:7700`. LAN mesh connected. Blocked: westGate needs to expose nestGate TCP + register content capability. |
| **CONVOY PROVENANCE 145/s** | westGate | 4-worker native socket convoy replaces socat subprocess. 460x total improvement (0.3/s → 145/s). CAS pool now 452 GB. Disk I/O is sole bottleneck (15.4% iowait on spinning raidz1). |
| **16⁴ DUAL-GPU DATA COMPLETE** | strandGate | RTX 3090 + RX 6950 XT from same cached configs. β=6.0: +0.01% vs published. β=6.2: -0.04%. Cross-vendor: 6 ppm at β=6.2. AMD 9.4x faster at 16⁴. |
| **tideGlass 214 TESTS** | westGate | content.query wired, 17 IPC methods, 5 petalTongue viz scenes. GPS data converted. |
| **footPrint 708 TESTS** | ironGate | Deep-debt: manifest-driven sources, riboCipher UDS, CAS TCP transport, neural-api client. |
| **REVIEWER RUBRIC SHIPPED** | eastGate | 42-item quality gate for arXiv Rung 1 (Bazavov 12, Chuna 10, Murillo 10, cross 10). 12 MUST-fix items. |

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

## PHASE STATUS

### Phase 1: Cell Boot — SUCCEEDED
`biomeos nucleus attach esotericwebb_cell.toml` on ironGate. First-ever cell attachment. exp006 21/22 PASS (1 skip from `biomeos/` → `membrane/` socket path migration, 0 fail). Scene push to petalTongue firing post-attach.

### Phase 2: footPrint — DEPLOYED + LIVE
systemd active on ironGate. CAS E2E verified (TCP local-trust). 708 tests. Agent bridge live. **golgi Caddy routing DONE** (`footprint.primals.eco` → ironGate :3002). **Remaining refinement**: auto-load default project, connect squirrel, deduplicate CSP (Express + Caddy both emit headers).

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

**ZFS**: 3.21 TB used / 50.7 TB pool (6.3%). CAS pool: 135 GB.

**Key**: 0 datasets at CONVERGED. Canonical pipeline proven (43/s) but not run at bulk. Priority: batch the 89 PARTIAL first (smallest datasets), then CAS-ingest 32 PRIMORDIAL.

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
| Data NAS | **westGate** (3.21 TB / 153 datasets / 17+ domains / **452 GB CAS**) |
| ironGate storage | **12.7 TB CAS LIVE** — `/mnt/nestgate`, nestGate v0.5.0, 9 squirrel providers |
| Primal tests | **~135,000+** |
| Signal dispatch | **G18 LIVE** — ironGate, 9 providers, cross-primal routing validated |
| Convoy provenance | **145/s** (460x total improvement). Disk I/O sole bottleneck. |
| arXiv Rung 1 | **16⁴ DATA COMPLETE** — +0.01% at β=6.0, 6 ppm cross-vendor. 42-item reviewer rubric. |
| Convergence | **convoy running** — 7.9M files, ETA ~15h at 145/s |
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

*59 glacial goals (9 COMPLETE, 30 ACTIVE). 139 docs fossilized. ~135K+ tests, 13/13 GREEN.*
