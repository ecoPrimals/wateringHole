# ecoPrimals Ecosystem Blurb — Cell Boot + Depot Sync Era

**Date**: Aug 4, 2026 PM | **Wave**: 156d | **From**: eastGate overwatch
**Posture**: **P0/P1/P2: ZERO. DEPOT v4.57+ SYNCED (52 builds). FIRST CELL BOOT SUCCEEDED (ironGate Session 8 — `biomeos nucleus attach`, 21/22 PASS). footPrint Phase 2 DEPLOYED (systemd, CAS E2E, 708 tests). nestgate.io FULLY OPERATIONAL (content backend wired, branded). K-derm FULLY OPERATIONAL (dnsmasq deployed, 11 gates resolving). GPS data CONVERTED (11 JSON, 103 MB CAS-ingested). ~135K+ tests, 13/13 GREEN.**

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
| **strandGate** | v4.56 → **binaries staged** | **READY TO RESTART** | Active GPU production. Schedule restart. |
| **blueGate** | v4.56 | **NEEDS DEPOT PULL** | Windows — membrane.exe rebuild needed. |
| **southGate** | v4.56 | **NEEDS DEPOT PULL** | Validation re-check after sync. |
| **biomeGate** | Source-built compute | — | GPU lab. Not full NUCLEUS. |
| **golgi** | Thin relay | — | Needs Caddy update for `footprint.primals.eco`. |
| **northGate** | — | — | Daily driver. Skip. |
| **grapheneGate** | Tower | — | Mobile. Skip. |
| **eastGate** | — | — | Overwatch. Skip. |

### Remaining Sync Work

```
DONE: sporeGate harvest (52/52)     ✓
DONE: ironGate redeploy (10/10)     ✓
DONE: strandGate binaries staged    ✓
DONE: westGate source-built v4.57   ✓  (14/14 HEALTHY)

NEXT: strandGate NUCLEUS restart    — schedule during therm pause
NEXT: blueGate + southGate          — Windows + validation
NEXT: golgi Caddy routing           — footprint.primals.eco
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

### Phase 2: footPrint — DEPLOYED
systemd active on ironGate. CAS E2E verified (TCP local-trust). 708 tests. Agent bridge live. **Remaining: golgi Caddy routing.**

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
| **tideGlass** | **214 tests.** 9 crates. 17 IPC methods. Live NUCLEUS on westGate. **GPS data CONVERTED** (11 JSON, 103 MB). `content.query` WIRED. 5 P0 viz scenes. | `nucleus attach` on westGate. Chen 2017 benchmark. |
| **footPrint** | **PHASE 2 DEPLOYED on ironGate.** 708 tests. CAS E2E. Agent bridge. | golgi Caddy routing. GPS viz integration. |
| **westGate data** | 3.21 TB / 153 datasets. GPS JSON in CAS. 135 GB CAS pool. **Convergence**: 0 CONVERGED, 89 PARTIAL, 32 PRIMORDIAL. | Batch provenance campaign. |
| **nestGate** | **`content.query` SHIPPED.** nestgate.io content backend wired. | tideGlass `content.query` **WIRED** — metadata search operational. |
| **Provenance trio** | 7/7. Loop CLOSED. 122× improvement. | Bulk convergence campaign across 153 datasets. |

### Track B: Lattice QCD on Consumer GPUs (Murillo / Chuna)

| Component | Status | Next |
|-----------|--------|------|
| **strandGate** | 12⁴ paper-ready. 16⁴ dual-GPU validated. **Binaries staged.** | Restart NUCLEUS → Rung 1 paper draft. |
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
| Depot | **v4.57+ SYNCED** (52 builds). sporeGate + ironGate + **westGate** DEPLOYED. strandGate STAGED. |
| Data NAS | **westGate** (3.21 TB / 153 datasets / 17+ domains / 135 GB CAS) |
| Primal tests | **~135,000+** |
| Cell boot | **SUCCEEDED** — ironGate Session 8, 21/22 PASS |
| westGate Phase 4 | **UNBLOCKED** — v4.57 DEPLOYED, GPS converted, `nucleus attach` ready |
| Convergence | **0/153 CONVERGED** — bulk provenance campaign needed |
| K-derm | **3/3 FULLY OPERATIONAL** |
| GPS data | **CONVERTED** — 11 JSON (103 MB) CAS-ingested with BLAKE3 |

---

## REMAINING WORK — ORDERED (westGate perspective)

1. **tideGlass cell boot** — `biomeos nucleus attach --cell tideglass_cell.toml` on westGate (UNBLOCKED)
2. **Bulk convergence campaign** — batch provenance across 89 PARTIAL + 32 PRIMORDIAL datasets
3. **strandGate NUCLEUS restart** — binaries staged, schedule during therm pause
4. **golgi Caddy routing** — `footprint.primals.eco` → ironGate
5. **blueGate + southGate depot pull** — Windows rebuild + validation re-check
6. **Depot CDN fix** — golgi still serves v4.56 binary despite fresh provenance.toml
7. **Inter-gate content.get E2E** — songBird probes ready, Tower Atomic on LAN

---

*Wave 156d — **Cell Boot + Depot Sync Era.** westGate now on v4.57 (source-built, 14/14 HEALTHY). GPS data converted (11 JSON, 103 MB CAS). Convergence sweep complete: 0/153 datasets at full provenance — bulk campaign needed. Phase 4 science springs UNBLOCKED on westGate. tideGlass cell boot next. ~135K+ tests, 13/13 GREEN.*
