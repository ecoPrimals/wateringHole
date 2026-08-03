# ecoPrimals Ecosystem Blurb — ironGate Downstream Hosting

**Date**: Aug 3, 2026 5PM | **Wave**: 155q/156b | **From**: eastGate overwatch
**Posture**: **P0/P1/P2: ZERO. G19 MILESTONE: petalTongue scene push PROVEN on ironGate. esotericWebb V26 (V22→V26 in one day): 471 tests, 22/22 exp006 PASS, enrichment FIRING. 8/9 primals compose zero-config. NUCLEUS 26/27 HEALTHY. airSpring deep debt CLEAN (1,157 tests, workspace consolidated). footPrint blocked on Forgejo repo creation. ~121K+ tests, 12/13 GREEN.**

---

## GATE ROLE TAXONOMY

| Gate | Role | What Runs | Why |
|------|------|-----------|-----|
| **ironGate** | **Downstream host** | esotericWebb + footPrint + squirrel + petalTongue live render | NUCLEUS 13/13 LIVE. i9-14900K, RTX 5070, 94GB. Pure compositions — no mesh needed. First live consumer environment. Matures squirrel (G18) + petalTongue (G19). |
| **westGate** | **Data NAS** | tideGlass + wetSpring + groundSpring + airSpring | 519 GB / 130 datasets on ZFS. All data local. Science springs boot here without mesh. |
| **strandGate** | **Compute dev** | hotSpring + neuralSpring | Dual EPYC, RTX 3090, RX 6950 XT. GPU compute + experiment queue. Data from westGate via mesh. |
| **biomeGate** | **GPU lab** | G32 silicon deism. 3 VFIO GPUs. | Threadripper 3970X. coralReef diesel engine. Cross-vendor validation. |
| **blueGate** | **Windows dev** | ludoSpring. Windows NUCLEUS. | G29 H2 DNS. Windows sub-builder. |
| **sporeGate** | **CI / membrane** | Sovereign CI. G34/G35. | Build authority. Depot. DNS. |
| **southGate** | **Validation** | NUCLEUS 22/22 reference gate. | G17+G8 PROVEN. |
| **eastGate** | **Overwatch** | squirrel (local dev). | 156b: test perf 400s→16s, 34→1 binaries. |
| **northGate** | **Windows dev** | RTX 5090. Daily driver. | AlphaFold data source. |
| **grapheneGate** | **Mobile** | Tower (TCP). Pixel 8a. | Beacon seed. |
| **golgi** | **VPS relay** | Forgejo + depot + sporePrint. | Thin-relay composition. |

---

## ironGate DOWNSTREAM STACK

ironGate creates a vertical slice through the entire primal-to-product stack:

```
squirrel (agent dispatch) → signal.plan + signal.dispatch
    │
biomeOS (composition) → graph.execute + cell graph deploy
    │
petalTongue (rendering) → WebGL/WASM live render on RTX 5070
    │
├── esotericWebb (CRPG game garden) — V26, 471 tests, G19 scene push PROVEN
└── footPrint (GIS protist) — Nest Atomic + drawbridge, 478 TS tests (blocked: Forgejo repo)
```

This tests and matures:
- **squirrel**: G18 signal dispatch with real consumers, not mocks
- **petalTongue**: G19 live render pipeline with actual GPU output on RTX 5070
- **biomeOS**: First real multi-composition deployment on a single gate
- **nestGate**: CAS project persistence for footPrint (local, no mesh needed)

**Why no mesh needed**: Both esotericWebb and footPrint are pure primal compositions with no external data gate dependency. All primals run on ironGate's NUCLEUS. External GIS data (USGS, FEMA, OSM) comes via songBird drawbridge (internet, not mesh).

---

## 5-PHASE EXECUTION SEQUENCE

### Phase 1: First live cell boot — esotericWebb on ironGate
- Run biomeOS deploy executor with `esotericwebb_cell.toml` on ironGate
- Validate all 13 primals + esotericWebb garden compose correctly
- Wire petalTongue live render for game shaders (RTX 5070)
- **This is the first-ever live cell composition boot in the ecosystem**
- Blockers: biomeOS live deploy (executor shipped, needs ops)

### Phase 2: footPrint on ironGate
- Deploy footPrint frontend (TypeScript/Vite/Leaflet) via petalTongue on `:8080`
- Wire nestGate CAS for project persistence (replacing Express CRUD)
- Wire songBird drawbridge for external GIS sources (USGS, FEMA, OSM, Esri)
- Update Caddy / DNS to route `footprint.primals.eco` to ironGate
- Blockers: Express API deployment, Caddy routing

### Phase 3: squirrel + petalTongue integration
- Test squirrel `signal.dispatch` → biomeOS `graph.execute` on ironGate
- esotericWebb + footPrint as live dispatch targets
- Validate the 4-strategy dispatch cascade with real providers
- Mature petalTongue G19 live render with actual game/GIS consumers

### Phase 4: westGate science springs (no mesh needed)
- Boot tideGlass on westGate (519 GB data local, Cargo workspace ready)
- Boot groundSpring + airSpring on westGate (NOAA/USGS/USDA local)
- First science spring compositions with real data
- ludoSpring on blueGate (pure composition, no deps)

### Phase 5: Inter-gate mesh validation
- Run songBird `mesh.connectivity_check` + `mesh.throughput` between ironGate ↔ westGate
- Validate content.get roundtrip with provenance chain across gate boundary
- Unblock healthSpring + lithoSpore on ironGate (data from westGate)
- Unblock neuralSpring on strandGate (293 GB streaming from westGate)
- Unblock wetSpring compute dispatch (westGate → strandGate)

---

## SPRING STARTUP READINESS

### Immediate — No Mesh Needed (Phase 1-2)

| Workload | Gate | Type | Mesh? | Blocker | Status |
|----------|------|------|-------|---------|--------|
| **esotericWebb** | **ironGate** | Garden | **No** | biomeOS live deploy (**V26, 471 tests, G19 scene push PROVEN**) | **FIRST BOOT TARGET** |
| **footPrint** | **ironGate** | Protist | **No** | **Forgejo repo creation** + Caddy routing (478 TS tests) | Phase 2 — BLOCKED |

### Next — Local Data, Same Gate (Phase 4)

| Workload | Gate | Type | Mesh? | Blocker |
|----------|------|------|-------|---------|
| **tideGlass** | westGate | Protist | **No** | biomeOS live deploy |
| **groundSpring** | westGate | Spring | **No** | biomeOS live deploy |
| **airSpring** | westGate | Spring | **No** | biomeOS live deploy |
| **ludoSpring** | blueGate | Spring | **No** | biomeOS live deploy |

### Later — Need Mesh Validation (Phase 5)

| Workload | Gate | Data From | Mesh? | Blocker |
|----------|------|-----------|-------|---------|
| **healthSpring** | ironGate | westGate | **Yes** | content.get E2E |
| **lithoSpore** | ironGate | westGate | **Yes** | content.get E2E + G31 batch |
| **neuralSpring** | strandGate | westGate | **Yes** | content.get E2E (293 GB streaming) |
| **hotSpring** | strandGate | westGate | **Yes** | experiment queue + content.get |
| **wetSpring** | westGate→strandGate | westGate | **Partial** | compute dispatch test |

---

## RECENT EVOLUTION (Wave 155p → 155q/156b)

| Event | Component | Impact |
|-------|-----------|--------|
| **G19 MILESTONE: scene push PROVEN** | ironGate | **petalTongue receiving game scenes from esotericWebb via `visualization.render.scene` on ironGate.** exp006 22/22 PASS, 0 skip. First proven GPU render pipeline on a downstream host. |
| **esotericWebb V22→V26** | esotericWebb | 4-version deep debt pass in one day. V23: pure Rust deps. V24: BTSP transport + membrane discovery + cell graph. V25–V26: deep debt CLEAN. **471 tests, 0 clippy, 0 unsafe, 0 C deps.** 8/9 primals compose zero-config. |
| **ironGate Session 4 AAR** | ironGate | NUCLEUS **26/27 HEALTHY**. RTX 5070 idle 42°C. 7 repos synced. V24 cell graph support ready for Phase 1 live boot. footPrint still blocked on Forgejo repo. |
| **airSpring deep debt CLEAN** | airSpring | Workspace consolidated (5-member root Cargo.toml). Pure-Rust curve fitting (5 functions). `gpu_or_skip!` macro (52/60 GPU tests). **1,157 tests, 84.3% coverage, 0 stubs, 0 hardcoded.** |
| **blueGate sub-builder coevolution** | blueGate | Divergence status: 8/10 resolved. Windows sub-builder + G29 H2 DNS progress. |
| **CI-DIV-06 resolved** | sporeGate | Golgi post-receive hooks + Caddy webhook + scheduler ingest wired. Webhook E2E verified. |
| **squirrel Wave 156b** | squirrel | **Test perf 400s→16s** — `without_discovery()` factories. **4,613 tests, 34→1 binaries.** |
| **squirrel Wave 156a** | squirrel | PrimalType eliminated → `CapabilityIdentifier`. Build artifacts **9.5→4.1 GiB.** |
| **projectNUCLEUS deep debt** | projectNUCLEUS | Workspace unified. Tier 2 pure Rust. **265 tests.** 9 ext systems mapped. |
| **barraCuda P0 fixes** | barraCuda | Subgroup + PRNG compose FIXED. **5,037 tests.** YELLOW (PRNG validation). |
| **songBird mesh probes** | songBird | `mesh.connectivity_check` + `mesh.throughput` SHIPPED. **14,840+ tests.** |
| **biomeOS spring dispatch** | biomeOS | Deploy graph executor SHIPPED. Deep debt CLEAN. **8,570+ tests.** |
| **sweetGrass G31 batch** | sweetGrass | `braid.batch_create` + `braid.batch_commit`. **1,644 tests.** |
| **westGate data campaign** | westGate | **519 GB / 130 datasets.** 9 domains. 50+ sources. |
| **coralReef deep debt** | coralReef | Wave 156a+156b dedup. **-770 LOC.** **3,553 tests.** |
| **bearDog 155m orphan purge** | bearDog | **94 orphan files** purged. **14,019 tests, 236 methods.** |

---

## PRIMAL HEALTH DASHBOARD

| Primal | Tests | Health | Gap | Recent |
|--------|-------|--------|-----|--------|
| **songBird** | 14,840+ | GREEN | E2E live test | mesh probes shipped |
| **bearDog** | **14,019** | GREEN | — | 94 orphan files purged (155m) |
| **nestGate** | 13,095+ | GREEN | CAS at 519 GB | — |
| **toadStool** | 9,193+ | GREEN | VFIO ember | 48 dead deps removed |
| **biomeOS** | 8,570+ | GREEN | **Live deploy on ironGate** | spring dispatch, deep debt CLEAN |
| **petalTongue** | 6,755 | GREEN | **G19 PROVEN on ironGate** | scene push FIRING (exp006) |
| **barraCuda** | 5,037 | **YELLOW** | PRNG validation | P0 shader fixes landed |
| **squirrel** | **4,613** | GREEN | **G18 integration on ironGate** | 156b: 400s→16s, 34→1 binaries |
| **coralReef** | 3,553 | GREEN | G32 VFIO | -770 LOC dedup |
| **rhizoCrypt** | 1,900 | GREEN | G31 batch | zero-warn 4-target cross-compile |
| **loamSpine** | 1,740 | GREEN | G31 batch | certificate.history RPC |
| **sweetGrass** | 1,644 | GREEN | G31 cross-primal | batch pipeline shipped |
| **cellMembrane** | 1,281+ | GREEN | Portability | — |

**Total**: **~121,000+ tests**. 12/13 GREEN. airSpring adds 1,157 tests (deep debt CLEAN). esotericWebb now 471 (V26). bearDog top 3 at 14,019.

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| Gates online | **11** |
| Downstream host | **ironGate** (esotericWebb + footPrint) |
| Data NAS | **westGate** (519 GB / 130 datasets / 17+ domains) |
| Primal tests | **~121,000+** |
| Springs/products bootable NOW (no mesh) | **6** (esotericWebb, footPrint, tideGlass, groundSpring, airSpring, ludoSpring) |
| Springs needing mesh | **5** (healthSpring, lithoSpore, neuralSpring, hotSpring, wetSpring dispatch) |
| First boot target | **esotericWebb on ironGate** |
| G18 integration target | **squirrel → biomeOS on ironGate** |
| G19 render target | **petalTongue on ironGate (RTX 5070) — PROVEN** |
| Glacial goals | **50 tracked** (22 ACTIVE, inc. G53/G54 dual-science) |
| arXiv | UNBLOCKED (paper relabel pending) |

---

*G19 MILESTONE HIT. petalTongue scene push is firing on ironGate — esotericWebb exp006 went from 21/22 PASS (1 skip) to 22/22 PASS (0 skip) in Session 4. Game scenes are being pushed via `visualization.render.scene` through the NUCLEUS IPC layer to the RTX 5070. This is the first proven GPU render pipeline on a downstream host. esotericWebb completed a V22→V26 evolution in one day (BTSP transport, membrane discovery, cell graph support, deep debt CLEAN — 471 tests, 0 clippy, 8/9 primals zero-config). airSpring finished deep debt on westGate (workspace consolidated, pure-Rust curve fitting, 1,157 tests, 84% coverage). blueGate sub-builder divergences at 8/10 resolved. CI-DIV-06 resolved (golgi webhook pipeline live). The ecosystem is at ~121K+ tests across 12/13 GREEN primals. Upstream action items: (1) toadStool systemd ExecStart fix for 9/9 membrane composition, (2) membrane socket permissions for non-root UDS access, (3) BTSP `0xEC 0x01` transport signal documentation. footPrint still blocked on Forgejo repo creation. Critical path: biomeOS live cell boot on ironGate (infrastructure ready, code team has V24+ cell graph), then footPrint Forgejo unblock, then squirrel G18 integration with real consumers.*
