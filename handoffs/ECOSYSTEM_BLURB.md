# ecoPrimals Ecosystem Blurb — ironGate Downstream Hosting

**Date**: Aug 3, 2026 7PM | **Wave**: 155s/156b | **From**: eastGate overwatch
**Posture**: **P0/P1/P2: ZERO. G19 PROVEN. ironGate Session 5: footPrint UNBLOCKED (526 TS tests PASS), Phase 1 structurally ready (cell graph dry-run OK). esotericWebb V26 (471 tests, 8/9 zero-config). neuralSpring V183 deep debt CLEAN (1,518 tests, 87% coverage). BTSP transport signal SPEC shipped. 14 docs fossilized. ~123K+ tests, 12/13 GREEN.**

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
└── footPrint (GIS protist) — Nest Atomic + drawbridge, 526 TS tests (protoKarya/footPrint, cloned on ironGate)
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
- **STATUS**: Structurally ready. Dry-run OK. esotericwebb.sock LIVE. Cell attachment (`--mode attach`) is the remaining ops gap.

### Phase 2: footPrint on ironGate
- Deploy footPrint frontend (TypeScript/Vite/Leaflet) via petalTongue on `:8080`
- Wire nestGate CAS for project persistence (replacing Express CRUD)
- Wire songBird drawbridge for external GIS sources (USGS, FEMA, OSM, Esri)
- Update Caddy / DNS to route `footprint.primals.eco` to ironGate
- **STATUS**: UNBLOCKED. Cloned, 526 tests PASS. Express 5 wildcard fix applied locally (needs upstream). Node.js 22 installed. Remaining: Caddy routing.

### Phase 3: squirrel + petalTongue integration
- Test squirrel `signal.dispatch` → biomeOS `graph.execute` on ironGate
- esotericWebb + footPrint as live dispatch targets
- Validate the 4-strategy dispatch cascade with real providers
- Mature petalTongue G19 live render with actual game/GIS consumers

### Phase 4: westGate science springs (no mesh needed)
- Boot tideGlass on westGate (519 GB data local, **UniBin COMPLETE — 9 crates, 147 tests, 92.71% coverage**)
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
| **footPrint** | **ironGate** | Protist | **No** | Caddy routing (**526 TS tests PASS**, cloned). Express 5 wildcard fix needed upstream | Phase 2 — UNBLOCKED |

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

## RECENT EVOLUTION (Wave 155p → 155s/156b)

| Event | Component | Impact |
|-------|-----------|--------|
| **ironGate Session 5** | ironGate | footPrint UNBLOCKED + cloned (**526 TS tests PASS**). Phase 1 cell graph dry-run OK. esotericwebb.sock LIVE. Cell attachment (`--mode attach`) only remaining gap. Express 5 wildcard fix applied. |
| **neuralSpring V183 deep debt** | neuralSpring | 3 monolithic files split (>1100L→focused submodules). 5 prod stubs→real implementations. Capability discovery replaces hardcoded routing. **1,518 tests, 87.25% coverage.** Phase 5 dependent (needs mesh). |
| **BTSP transport signal SPEC** | cellMembrane | `0xEC 0x01` prefix documented. 7 protocol bytes defined. Per-primal transport requirements table. Discovery+fallback sequence codified. |
| **G19 MILESTONE: scene push PROVEN** | ironGate | petalTongue receiving game scenes via `visualization.render.scene`. exp006 **22/22 PASS**. First GPU render pipeline on downstream host. |
| **esotericWebb V22→V26** | esotericWebb | Deep debt CLEAN. **471 tests, 0 clippy, 0 unsafe.** 8/9 primals compose zero-config. |
| **airSpring deep debt CLEAN** | airSpring | Workspace consolidated. Pure-Rust curve fitting. **1,157 tests, 84.3% coverage.** |
| **groundSpring deep debt** | groundSpring | Pipeline types evolved. westGate deployment ready. |
| **blueGate sub-builder** | blueGate | Divergences 8/10 resolved. |
| **CI-DIV-06 resolved** | sporeGate | Webhook pipeline live. |
| **squirrel 156b** | squirrel | Test perf 400s→16s. **4,613 tests, 34→1 binaries.** |
| **projectNUCLEUS debt** | projectNUCLEUS | Workspace unified. **265 tests.** 9 ext systems. |
| **barraCuda P0** | barraCuda | Subgroup+PRNG FIXED. **5,037 tests.** YELLOW. |
| **songBird mesh** | songBird | Probes shipped. **14,840+ tests.** |
| **biomeOS dispatch** | biomeOS | Executor shipped. **8,570+ tests.** |
| **sweetGrass G31** | sweetGrass | Batch pipeline. **1,644 tests.** |
| **westGate data** | westGate | **519 GB / 130 datasets.** |
| **coralReef dedup** | coralReef | -770 LOC. **3,553 tests.** |
| **bearDog purge** | bearDog | 94 orphans deleted. **14,019 tests.** |
| **14 docs fossilized** | overwatch | ironGate S2/S3, biomeGate wave155n cluster, squirrel 155p, 5 AARs → `wave155r_absorbed/` |

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
| **tideGlass** | **147** | GREEN | biomeOS cell boot, CAS wiring | **Full Rust rebuild: 9 crates, UniBin, 92.71% coverage** |
| **cellMembrane** | 1,281+ | GREEN | Portability | — |

**Total**: **~123,150+ tests**. 12/13 GREEN. tideGlass adds 147 (full rebuild). neuralSpring adds 1,518 (V183 deep debt). airSpring 1,157. footPrint 526. bearDog top 3 at 14,019.

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| Gates online | **11** |
| Downstream host | **ironGate** (esotericWebb + footPrint) |
| Data NAS | **westGate** (519 GB / 130 datasets / 17+ domains) |
| Primal tests | **~123,000+** |
| Springs/products bootable NOW (no mesh) | **6** (esotericWebb, footPrint, tideGlass, groundSpring, airSpring, ludoSpring) |
| Springs needing mesh | **5** (healthSpring, lithoSpore, neuralSpring, hotSpring, wetSpring dispatch) |
| First boot target | **esotericWebb on ironGate** |
| G18 integration target | **squirrel → biomeOS on ironGate** |
| G19 render target | **petalTongue on ironGate (RTX 5070) — PROVEN** |
| Glacial goals | **50 tracked** (22 ACTIVE, inc. G53/G54 dual-science) |
| arXiv | UNBLOCKED (paper relabel pending) |

---

## DUAL-SCIENCE INCREMENTAL STATUS

### Track A: NF Drug Repurposing (Gonzales / Bin Chen)

| Component | Status | Next |
|-----------|--------|------|
| **tideGlass** (protist) | **Full Rust rebuild COMPLETE.** 9 crates, UniBin, 11 IPC methods, 147 tests, 92.71% coverage. Phase 4 — Package. | biomeOS cell boot on westGate. nestGate CAS wiring for LINCS/ChEMBL. Chen 2017 benchmark (r >= 0.52). |
| **westGate data** | 519 GB / 130 datasets. NF-relevant datasets identified. | Ingest NF expression profiles |
| **footPrint** (GPS viz) | 526 tests PASS on ironGate. Cloned. Express 5 fix applied. | Caddy routing → `footprint.primals.eco`. Experiment with petalTongue scene push for GIS overlays. |
| **petalTongue** (viz) | G19 PROVEN. `visualization.render.scene` live. WebGL compiler. | Wire footPrint → petalTongue for GPS visualization (volcano plots, heatmaps, enrichment curves). G53 maturation. |
| **nestGate** (CAS) | 13K+ tests. CAS on ZFS verified. | CAS project persistence for tideGlass provenance chain |
| **Provenance trio** | 7/7 COMPLETE. sweetGrass batch pipeline. | Provenance per RGES execution |

### Track B: Lattice QCD on Consumer GPUs (Murillo / Chuna)

| Component | Status | Next |
|-----------|--------|------|
| **hotSpring** (spring) | arXiv beta scan binary. riboCipher transport enforced. | Rung 1: reproduce plaquette normalization. SU(2)→SU(3) relabel. |
| **barraCuda** (GPU math) | 5,037 tests. P0 fixes landed. MultiDevicePool wired. YELLOW (PRNG). | PRNG validation. WGSL shader source for lattice ops. |
| **coralReef** (shaders) | 3,553 tests. -770 LOC dedup. Windows cross-compile. | WGSL compilation for QCD kernels. G32 VFIO diesel. |
| **toadStool** (compute) | 9,193+ tests. S349 deep debt. | compute.dispatch for GPU lattice execution |
| **esotericWebb** (viz) | V26, 471 tests. Scene push FIRING on ironGate. | Experiment with petalTongue for QCD visualization (lattice configs, Wilson loops, β-scan plots). |
| **strandGate** (gate) | Dual EPYC + RTX 3090 + RX 6950 XT. | Experiment queue for hotSpring. Needs mesh for 293 GB streaming. |

### Support → Science Convergence (G53 / G54)

**footPrint + esotericWebb on ironGate → mature petalTongue G19 → reusable viz for both tracks.**

- footPrint matures petalTongue's GIS/spatial rendering → GPS platform for NF drug screen
- esotericWebb matures petalTongue's scene graph + interaction → lattice visualization for QCD
- Both exercise squirrel G18 dispatch, biomeOS composition, nestGate CAS — the full stack
- petalTongue becomes a **live science exploration tool**, not just a presentation layer

---

## petalTongue GAME ENGINE EVOLUTION — STRATEGIC DIRECTION

### Current Architecture (v1.7.0)

petalTongue is a **Universal User Interface** — 19 crates, 6,755 tests, 56 JSON-RPC methods, 7 modality compilers (SVG, WebGL, terminal, audio, braille, haptic, description). It renders ecosystem state but delegates heavy compute to toadStool/barraCuda/coralReef.

**Already present (game-adjacent):**
- egui/eframe desktop GUI + glow (OpenGL)
- Declarative scene graph with 3D primitives (Sphere, Cylinder, Mesh3D, Camera, Projection)
- Manim-style animation system
- Bidirectional interaction engine (SAME DAVE cognitive model)
- Physics bridge → toadStool compute dispatch (CPU fallback)
- Texture attach for external framebuffers (`memfd://godot-fb-0` URIs)
- WebGL compiler (browser GPU path without wgpu)
- Platform embedding: WASM, Android/iOS cdylib, cross-arch

### Evolution Paths

| Path | What | Leverage |
|------|------|---------|
| **WebGPU via wgpu** | Native GPU render loop in-process. Replaces glow/OpenGL with modern GPU API. | toadStool already has wgpu. Wire `GpuCompiler` → coralReef shader compilation → toadStool display backend. |
| **egui + wgpu** | egui already supports wgpu backend. Switch from eframe/glow to egui-wgpu for native WGSL shader execution. | Minimal — egui_wgpu is a drop-in backend. Enables custom render passes for science viz. |
| **Godot interop** | Godot as external game runtime. petalTongue feeds scene data via texture attach + IPC. Godot handles physics, animation, multiplayer. | `visualization.texture.attach` already accepts Godot memfd URIs. GDScript ↔ JSON-RPC bridge is straightforward. |
| **VR/AR (OpenXR)** | New modality compiler + display backend. Stereo rendering via dual Camera/Projection. Head/hand tracking as sensory input adapters. | Scene graph with 3D + Camera/Projection already exists. Sensory Capability Matrix can extend to XR device profiles. Multi-perspective interaction is an architectural precursor. |
| **Live science exploration** | petalTongue as the entry point for exploring NF drug data (GPS maps, volcano plots, enrichment curves) and QCD lattice configurations (Wilson loops, β-scan, plaquette distributions) in real-time. | Grammar of Graphics Phase 4–5. barraCuda offload. coralReef shader compilation. All IPC contracts exist. |

### Recommended Strategy

**petalTongue renders; other primals provide capabilities.** The path is not "replace Godot/Unity inside petalTongue" but:

1. **Wire `GpuCompiler` → coralReef → toadStool** for native WGSL shader execution (today: WebGL draw commands only)
2. **Add egui-wgpu backend** alongside glow — enables custom render passes for science visualization
3. **Godot as an optional game runtime** — petalTongue feeds scene data, Godot handles physics/animation/multiplayer. Texture attach mechanism exists.
4. **XR as a new modality** — extend scene graph Camera/Projection for stereo, add OpenXR display backend, sensory input adapters for controllers/hand tracking
5. **Keep game/science logic in springs** — esotericWebb, hotSpring, tideGlass own domain logic. petalTongue stays the universal renderer.

This makes petalTongue a **live science exploration platform** (VR/AR/desktop/browser/mobile) that can visualize lattice QCD configurations and NF drug repurposing results in real-time, with the GPU compute stack (barraCuda → coralReef → toadStool) providing the actual shader execution.

---

*Wave 155s/156b cascade. ironGate Session 5 confirmed footPrint UNBLOCKED (526 TS tests PASS, Express 5 wildcard fixed locally, Node.js 22 installed). Phase 1 cell graph dry-run OK — biomeOS deploy executor parses the graph, esotericwebb.sock is LIVE, cell attachment CLI is the single remaining gap. neuralSpring V183 completed deep debt (1,518 tests, 87% coverage, 3 monolithic files split, 5 stubs→real implementations, capability discovery replaces hardcoding). BTSP transport signal spec shipped — `0xEC 0x01` prefix, 7 protocol bytes, per-primal requirements table. 14 docs fossilized to `wave155r_absorbed/`. Both science tracks advancing: Track A (NF/GPS) has tideGlass specs + 519 GB data + footPrint on ironGate for GPS viz maturation; Track B (QCD) has hotSpring arXiv ready + barraCuda GPU math + esotericWebb on ironGate for lattice viz. petalTongue's evolution toward a full science exploration platform (WebGPU/egui-wgpu, Godot interop, VR/AR via OpenXR) is strategically mapped — the path is capability delegation through the GPU stack (barraCuda→coralReef→toadStool), not engine replacement. ~123K+ tests across 12/13 GREEN primals. Critical path: biomeOS cell attachment CLI for Phase 1 live boot, then footPrint Caddy routing, then squirrel G18 integration with both consumers driving petalTongue G53 maturation.*
