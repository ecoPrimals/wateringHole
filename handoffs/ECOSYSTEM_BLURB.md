# ecoPrimals Ecosystem Blurb — ironGate Downstream Hosting

**Date**: Aug 3, 2026 | **Wave**: 155p/156a | **From**: eastGate overwatch
**Posture**: **P0/P1/P2: ZERO. ironGate designated PRIMARY DOWNSTREAM HOST (esotericWebb + footPrint). Other gates serve as primal dev environments. westGate is data NAS (519 GB / 130 datasets). ~119K+ tests, 12/13 GREEN. First live cell boot target: esotericWebb on ironGate.**

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
| **eastGate** | **Overwatch** | squirrel (local dev). | PrimalType elimination, signal.dispatch. |
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
├── esotericWebb (CRPG game garden) — pure composition, 472 tests
└── footPrint (GIS protist) — Nest Atomic + drawbridge, 478 TS tests
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
| **esotericWebb** | **ironGate** | Garden | **No** | biomeOS live deploy | **FIRST BOOT TARGET** |
| **footPrint** | **ironGate** | Protist | **No** | Express API + Caddy routing | Phase 2 |

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

## WHAT JUST HAPPENED (overnight evolution)

| Event | Primal | Impact |
|-------|--------|--------|
| **barraCuda P0 shader fixes** | barraCuda | Subgroup entry point FIXED. PRNG compose FIXED. **5,037 tests.** Still YELLOW (PRNG validation Week 3+). |
| **songBird mesh probes** | songBird | `mesh.connectivity_check` + `mesh.throughput` SHIPPED. **20 mesh methods, 14,840+ tests.** |
| **biomeOS spring dispatch** | biomeOS | Deploy graph executor SHIPPED. Deep debt CLEAN. **8,570+ tests, zero debt.** |
| **squirrel signal.dispatch (G18)** | squirrel | 4-strategy dispatch cascade WIRED. **7,243 tests, 90.1% coverage.** |
| **sweetGrass G31 batch** | sweetGrass | `braid.batch_create` + `braid.batch_commit` SHIPPED. **42 methods, 1,644 tests.** |
| **westGate data campaign** | westGate | **519 GB / 130 datasets.** AlphaFold v6 42/46 proteomes. |
| **Gauge group resolved** | hotSpring | SU(3) code, SU(2) paper. arXiv UNBLOCKED. Paper relabel pending. |

---

## PRIMAL HEALTH DASHBOARD

| Primal | Tests | Health | Gap |
|--------|-------|--------|-----|
| **songBird** | 14,840+ | GREEN | E2E live test |
| **nestGate** | 13,095+ | GREEN | CAS at 519 GB |
| **toadStool** | 9,193+ | GREEN | VFIO ember |
| **biomeOS** | 8,570+ | GREEN | **Live deploy on ironGate** |
| **squirrel** | 7,243 | GREEN | **G18 integration on ironGate** |
| **petalTongue** | 6,755 | GREEN | **G19 live render on ironGate** |
| **barraCuda** | 5,037 | **YELLOW** | PRNG validation |
| **coralReef** | 3,553 | GREEN | G32 VFIO |
| **rhizoCrypt** | 1,900 | GREEN | G31 batch |
| **loamSpine** | 1,740 | GREEN | G31 batch |
| **sweetGrass** | 1,644 | GREEN | G31 cross-primal |
| **cellMembrane** | 1,281+ | GREEN | Portability |

**Total**: ~119,000+ tests. 12/13 GREEN. 3 primals have ironGate as their maturation target (biomeOS, squirrel, petalTongue).

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| Gates online | **11** |
| Downstream host | **ironGate** (esotericWebb + footPrint) |
| Data NAS | **westGate** (519 GB / 130 datasets / 17+ domains) |
| Primal tests | **~119,000+** |
| Springs/products bootable NOW (no mesh) | **6** (esotericWebb, footPrint, tideGlass, groundSpring, airSpring, ludoSpring) |
| Springs needing mesh | **5** (healthSpring, lithoSpore, neuralSpring, hotSpring, wetSpring dispatch) |
| First boot target | **esotericWebb on ironGate** |
| G18 integration target | **squirrel → biomeOS on ironGate** |
| G19 render target | **petalTongue on ironGate (RTX 5070)** |
| Glacial goals | 48 tracked |
| arXiv | UNBLOCKED (paper relabel pending) |

---

*ironGate becomes the primary downstream hosting machine — the first gate running live cell compositions for real users. esotericWebb (pure CRPG garden) and footPrint (GIS protist) need no inter-gate mesh, no external data gates, just the 13 primals already running on ironGate's NUCLEUS. This creates the environment to mature squirrel (G18 dispatch with real consumers), petalTongue (G19 live render on RTX 5070), and biomeOS (first multi-composition deployment). Other gates stay as dev: strandGate for compute, biomeGate for GPU experiments, westGate as the 519 GB data NAS. The mesh matures in parallel — when content.get E2E validates, healthSpring and lithoSpore join ironGate with westGate data. The first live cell boot (esotericWebb) proves the entire deploy chain end-to-end.*
