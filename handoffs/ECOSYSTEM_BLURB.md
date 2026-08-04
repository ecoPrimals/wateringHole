# ecoPrimals Ecosystem Blurb — Cell Boot + Depot Sync Era

**Date**: Aug 4, 2026 PM | **Wave**: 156d | **From**: eastGate overwatch
**Posture**: **P0/P1/P2: ZERO. ALL GATES v4.57+ SYNCED (6/6 NUCLEUS gates deployed). Cell boot SUCCEEDED (21/22 PASS). footprint.primals.eco LIVE. nestgate.io LIVE (branded). K-derm FULLY OPERATIONAL. southGate 13/13 re-validated (97h → restart, Tower 0.15ms). strandGate config cache COMPLETE (9/10, 325 MB), dual-GPU scan LAUNCHED. ~135K+ tests, 13/13 GREEN.**

---

## WHAT JUST HAPPENED — Session 8 Cascade

| Event | Gate | Status |
|-------|------|--------|
| **Depot v4.57+ SYNCED** | sporeGate | 52 builds (13 primals × 4 targets). golgi depot pushed (45 new, 10 current). |
| **sporeGate NUCLEUS restarted** | sporeGate | 14/14 HEALTHY on new binaries. |
| **ironGate NUCLEUS restarted** | ironGate | 10/10 HEALTHY on new binaries. |
| **strandGate binaries staged** | strandGate | Binaries ready, restart pending. |
| **FIRST CELL BOOT SUCCEEDED** | ironGate | `biomeos nucleus attach esotericwebb_cell.toml` — first-ever cell attachment. exp006 21/22 PASS (1 skip, 0 fail). Scene push to petalTongue firing. |
| **footPrint Phase 2 DEPLOYED** | ironGate | systemd active, CAS E2E verified (TCP local-trust), 708 tests, agent bridge live. Remaining: golgi Caddy routing. |
| **nestgate.io DIVs RESOLVED** | sporeGate | DIV-1: nestGate UDS socket wired. DIV-2: content-provider → nestGate. DIV-4: Branded "ecoPrimals Data Surface". |
| **K-derm FULLY OPERATIONAL** | all | dnsmasq `primal-eco.conf` deployed, all 11 gates resolving. LAN-first Tower active. |
| **GPS data CONVERTED** | westGate | pickle→JSON converter: 2198 genes, MLP weights, RCL ensembles, compound matrices. 11 JSON outputs (103.4 MB) CAS-ingested with BLAKE3. |
| **westGate v4.57 DEPLOYED** | westGate | Built from source (commit 96083386). `nucleus attach` available. NUCLEUS restarted: 14/14 HEALTHY. |
| **westGate convergence sweep** | westGate | 153 datasets scanned. 0 CONVERGED, 5 CAS-ONLY, 89 PARTIAL, 32 PRIMORDIAL, 21 EMPTY. Bulk provenance campaign needed. |

---

## GATE FLEET STATUS — POST-SYNC

| Gate | NUCLEUS | Depot | Status |
|------|---------|-------|--------|
| **sporeGate** | **14/14 v4.57+** | **BUILD AUTHORITY — FRESH** | Sovereign CI. 52/52 harvest complete. LAN-first Tower (4 local, 1ms). |
| **ironGate** | **10/10 v4.57+** | **CURRENT** | **FIRST CELL BOOT + footPrint Phase 2 LIVE.** 708 tests. |
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

### Phase 3: squirrel + petalTongue — NEXT
- squirrel G18 signal dispatch with real consumers (esotericWebb + footPrint)
- petalTongue G19 live render on RTX 5070

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
| **strandGate** | 12⁴ paper-ready. 16⁴ dual-GPU validated. **Config cache COMPLETE (9/10, 325 MB).** Dual-GPU scan LAUNCHED. | Restart NUCLEUS when therm done → Rung 1 paper draft. |
| **hotSpring** | 5 arxiv binaries. Parallel therm 279→95 min. Config cache LIVE. | Rung 1 production campaign. |
| **barraCuda** | MultiDevicePool. 4,959 tests. GREEN. | Cross-vendor GPU dispatch. |
| **esotericWebb** | V31b. CELL BOOT SUCCEEDED. Scene builder. 484 tests. | QCD viz via petalTongue. |

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
| Data NAS | **westGate** (3.21 TB / 153 datasets / 17+ domains / 135 GB CAS) |
| Primal tests | **~135,000+** |
| Cell boot | **SUCCEEDED** — ironGate Session 8, 21/22 PASS |
| westGate Phase 4 | **UNBLOCKED** — v4.57 DEPLOYED, GPS converted, `nucleus attach` ready |
| Convergence | **0/153 CONVERGED** — bulk provenance campaign needed |
| K-derm | **3/3 FULLY OPERATIONAL** |
| GPS data | **CONVERTED** — 11 JSON (103 MB) CAS-ingested with BLAKE3 |

---

## REMAINING WORK — ORDERED

1. **tideGlass cell boot on westGate** — `biomeos nucleus attach` (GPS data converted, v4.57 LIVE)
2. **Bulk convergence campaign** — 89 PARTIAL + 32 PRIMORDIAL → fully braided (0/153 converged)
3. **strandGate NUCLEUS restart** — binaries staged, GPU at 100% QCD. Config cache COMPLETE. Restart when therm completes.
4. **Inter-gate content.get E2E** — songBird probes ready, Tower Atomic on LAN
5. **arXiv Rung 1 paper draft** — 12⁴ paper-ready, 16⁴ dual-GPU cross-vendor validated
6. **Socket path migration** — `biomeos/` → `membrane/` (exp006 1 skip)

### LIVE SITE ASSESSMENT

| Site | URL | Status | Issue |
|------|-----|--------|-------|
| **sporePrint** | `sporeprint.primals.eco` | **LIVE, renders well** | Zola static site. Science content. Claims verifiable. |
| **footPrint** | `footprint.primals.eco` | **LIVE, serves 200** | API works (health OK, CAS 3 objects, 1 real project). Map UI loads empty — no auto-load, squirrel disconnected (`agentConnected:false`). Dual CSP headers (Express + Caddy both emit). Refinement: auto-load default project, connect squirrel, deduplicate CSP. |
| **nestgate.io** | `nestgate.io` | **LIVE, serves 200** | Dashboard loads but all sections show "Loading..." — petalTongue on sporeGate cannot reach live mesh data from public internet path. Needs either SSR pre-render or WebSocket bridge to mesh. |
| **esotericWebb** | `webb.primals.eco` | **502 Bad Gateway** | Cell boot succeeded (IPC level) but no web-facing surface. esotericWebb is a Rust CRPG engine with IPC/session logic — it has no HTTP server or browser client. A live game requires petalTongue WebGL rendering pipeline. |

---

*Wave 156d — **All Gates Synced.** All 6 NUCLEUS gates deployed on v4.57+. Cell boot succeeded (ironGate 21/22 PASS). footprint.primals.eco LIVE (golgi Caddy → ironGate :3002). southGate re-validated after 97h (13/13, Tower 0.15ms, 19 Gbps). strandGate config cache COMPLETE (9/10 configs, 325 MB 16⁴), dual-GPU scan launched. GPS data converted (11 JSON, 103 MB). Live site assessment: sporePrint renders well; footPrint serves but needs CAS data flow; nestgate.io loads but dashboards show "Loading..." (mesh unreachable from public); esotericWebb has no web surface (502 — CRPG engine is IPC-only, needs petalTongue WebGL pipeline for browser rendering).*

*59 glacial goals (9 COMPLETE, 30 ACTIVE). 129 docs fossilized. ~135K+ tests, 13/13 GREEN.*
