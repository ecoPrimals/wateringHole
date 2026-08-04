# ecoPrimals Ecosystem Blurb — ironGate Downstream Hosting

**Date**: Aug 4, 2026 AM | **Wave**: 155u/156b | **From**: eastGate overwatch
**Posture**: **P0/P1/P2: ZERO. PROVENANCE × ACQUISITION DIVERGENCE: 12× throughput gap discovered (74 files/s download vs 6 files/s with inline provenance). Trailer pattern + batch RPC proposal. Massive overnight upstream: esotericWebb V29 (8 commits), hotSpring 13 commits (arXiv production), barraCuda PRNG GREEN (9 commits), nestGate content.fetch, coralReef 156b, biomeOS signal graphs. Mixed provenance states (primordial/CAS-only/braided) — convergence path defined. ~130K+ tests, 13/13 GREEN.**

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
└── footPrint (GIS protist) — 563 tests, nestGate CAS + petalTongue RPC wired, 10/10 constraints
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
| **footPrint** | **ironGate** | Protist | **No** | Caddy routing (**563 tests**, CAS+petalTongue wired). Express absorb into Neural API routing. | Phase 2 — READY |

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

## RECENT EVOLUTION (Wave 155t → 155u/156b)

| Event | Component | Impact |
|-------|-----------|--------|
| **PROVENANCE × ACQUISITION DIVERGENCE** | westGate | **12× throughput collapse** with inline provenance (74/s → 6/s). Sequential UDS RPC serialization. **Trailer pattern** decouples download from braiding. **Batch RPC proposal**: `dag.event.batch` + `spine.entry.batch`. |
| **Mixed provenance states** | westGate | 3 states: **primordial** (no CAS), **CAS-only** (hash but no DAG/spine), **fully braided**. Convergence path defined. `is_dataset_converged()` gate for springs. |
| **esotericWebb V23→V29** | esotericWebb | 8 upstream commits. V27: G18 signal.dispatch inbound. V28: petalTongue live site + grammar + WebGL + animation. V29: deep debt refactor. |
| **hotSpring 13 commits** | hotSpring | arXiv production runs. Volume scan + preprint validation binaries. Provenance trio wired (NFT pattern). biomeGate revalidation. |
| **barraCuda YELLOW → GREEN** | barraCuda | 9 upstream commits. **PRNG half-range bugs FIXED** + statistical validation harness. RK4 zero-alloc. Shader static evolution -182 LOC. |
| **nestGate content.fetch** | nestGate | 4 upstream commits. `content.fetch`: HTTP GET → BLAKE3 → CAS in one atomic step. CAS federation streaming + size guard. |
| **coralReef 156b** | coralReef | 4 upstream commits. ShaderInfo dedup. **3,512 tests.** |
| **biomeOS signal graphs** | biomeOS | 2 upstream commits. 5+3 signal graphs. `content.fetch` wired into `nest.acquire_file`. |
| **toadStool S351** | toadStool | 48 dead deps eliminated (47→39 external). |
| **sweetGrass deep evolution** | sweetGrass | Zero-copy `Arc<str>`, primal_names constants, `#[non_exhaustive]`. |
| **rhizoCrypt G31 batch** | rhizoCrypt | Batch provenance pipeline. 4 upstream commits. Method count 39. |

### Previous wave highlights (155p → 155t)
tideGlass full Rust rebuild (161 tests, CAS wiring, 6 divergences). footPrint deep debt (563 tests). wetSpring V211c (2,210 tests). strandGate silicon deism VALIDATION COMPLETE. G19 PROVEN. neuralSpring V183. petalTongue 156b. 14 docs fossilized. Full history in ortho review.

---

## PRIMAL HEALTH DASHBOARD

| Primal | Tests | Health | Gap | Recent |
|--------|-------|--------|-----|--------|
| **songBird** | 14,840+ | GREEN | E2E live test | mesh probes shipped |
| **bearDog** | **14,019** | GREEN | — | 94 orphan files purged (155m) |
| **nestGate** | 13,095+ | GREEN | CAS at 519 GB | — |
| **toadStool** | 9,193+ | GREEN | VFIO ember | 48 dead deps removed |
| **biomeOS** | 8,570+ | GREEN | **Live deploy on ironGate** | spring dispatch, deep debt CLEAN |
| **petalTongue** | 6,755 | GREEN | **G19 PROVEN on ironGate** | Wave 156b doc hygiene, 0 doc warnings |
| **barraCuda** | 5,037+ | **GREEN** | — | **PRNG FIXED** (YELLOW→GREEN). Shader -182 LOC. RK4 zero-alloc. |
| **squirrel** | **4,613** | GREEN | **G18 integration on ironGate** | 156b: 400s→16s, 34→1 binaries |
| **coralReef** | 3,512 | GREEN | G32 VFIO | 156b: ShaderInfo dedup, alloc fix |
| **rhizoCrypt** | 1,900 | GREEN | G31 batch | zero-warn 4-target cross-compile |
| **loamSpine** | 1,740 | GREEN | G31 batch | certificate.history RPC |
| **sweetGrass** | 1,644 | GREEN | G31 cross-primal | batch pipeline shipped |
| **tideGlass** | **147** | GREEN | biomeOS cell boot, CAS wiring | **Full Rust rebuild: 9 crates, UniBin, 92.71% coverage** |
| **cellMembrane** | 1,281+ | GREEN | Portability | — |

**Total**: **~130,000+ tests**. **13/13 GREEN** (barraCuda PRNG FIXED → GREEN). esotericWebb V29. hotSpring arXiv production. nestGate content.fetch. biomeOS signal graphs.

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| Gates online | **11** |
| Downstream host | **ironGate** (esotericWebb + footPrint) |
| Data NAS | **westGate** (519 GB / 130 datasets / 17+ domains) |
| Primal tests | **~130,000+** |
| Springs/products bootable NOW (no mesh) | **6** (esotericWebb, footPrint, tideGlass, groundSpring, airSpring, ludoSpring) |
| Springs needing mesh | **5** (healthSpring, lithoSpore, neuralSpring, hotSpring, wetSpring dispatch) |
| First boot target | **esotericWebb on ironGate** |
| G18 integration target | **squirrel → biomeOS on ironGate** |
| G19 render target | **petalTongue on ironGate (RTX 5070) — PROVEN** |
| Glacial goals | **54 tracked** (26 ACTIVE, inc. G55-G58 data pipeline evolution) |
| arXiv | UNBLOCKED (paper relabel pending) |

---

## DUAL-SCIENCE INCREMENTAL STATUS

### Track A: NF Drug Repurposing (Gonzales / Bin Chen)

| Component | Status | Next |
|-----------|--------|------|
| **tideGlass** (protist) | **FULL RUST REBUILD.** 9 crates, 7 science modules, 11 IPC methods. **161 tests, 93% cov.** CAS wiring LIVE with graceful degradation. 6 divergences documented (DIV-1→6). | Convert GPS NumPy/pickle → JSON. Chen 2017 benchmark (r >= 0.52). nestGate canonical client crate. |
| **westGate data** | 519 GB / 130 datasets. GPS platform data in CAS (8 files, 1.4 GB, NumPy/pickle). | Python converter → JSON → CAS re-ingest with derivation lineage. |
| **footPrint** (GPS viz) | **563 tests.** 10/10 constraints. nestGate CAS + petalTongue RPC wired. JSON-RPC 2.0 agent bridge. Runtime SourceManifest. | Route CAS via **Neural API** (capability-based, not direct nestGate). Caddy routing. |
| **petalTongue** (viz) | G19 PROVEN. Wave 156b pushed (**6,755 tests, 0 doc warnings**). | footPrint + tideGlass consume via Neural API. G53 maturation. |
| **nestGate** (CAS) | 13K+ tests. CAS on ZFS. DIV-2: no query-by-tag API. Stale client patterns in other primals. | `content.query` method. Canonical Rust client crate for ecosystem. |
| **Provenance trio** | 7/7 COMPLETE. sweetGrass batch pipeline. | Provenance per tideGlass RGES execution. |

### Track B: Lattice QCD on Consumer GPUs (Murillo / Chuna)

| Component | Status | Next |
|-----------|--------|------|
| **strandGate VALIDATION** | **ALL high-priority validation COMPLETE.** Action-force (6 sig figs). Creutz equality (5 sig figs). **Dual-GPU parity: RTX 3090 + RX 6950 XT, |ΔP| < 10⁻³.** β-scan matches SU(3) published data. **PAPER SUBMISSION-READY.** | Resolve plaquette ×4 normalization. Then Rung 1 production campaign. |
| **hotSpring** (spring) | arXiv beta scan binary. riboCipher transport enforced. | Rung 1 BLOCKED on plaquette normalization. SU(2)→SU(3) relabel. |
| **barraCuda** (GPU math) | 5,037+ tests. **GREEN** (PRNG FIXED). Shader -182 LOC. RK4 zero-alloc. | Statistical validation harness in place. |
| **coralReef** (shaders) | 3,553 tests. Windows cross-compile. | WGSL compilation for QCD kernels. |
| **toadStool** (compute) | 9,193+ tests. S349 deep debt. | compute.dispatch for GPU lattice. |
| **esotericWebb** (viz) | V26, 471 tests. Scene push FIRING. | QCD visualization via petalTongue. |
| **wetSpring** (spring) | **2,210 tests.** V211c deep debt. 186 casts migrated. Capability discovery. | westGate deployment. |
| **strandGate** (gate) | Dual EPYC + RTX 3090 + RX 6950 XT. | Experiment queue. Needs mesh for 293 GB streaming. |

### Support → Science Convergence (G53 / G54)

**footPrint + esotericWebb on ironGate → mature petalTongue G19 → reusable viz for both tracks.**

- footPrint matures petalTongue's GIS/spatial rendering → GPS platform for NF drug screen
- esotericWebb matures petalTongue's scene graph + interaction → lattice visualization for QCD
- Both exercise squirrel G18 dispatch, biomeOS composition, nestGate CAS — the full stack
- petalTongue becomes a **live science exploration tool**, not just a presentation layer

**Neural API routing pattern**: footPrint and tideGlass CAS data should flow through the **biomeOS Neural API** (`neural-api-default.sock`) for capability-based routing rather than connecting directly to `nestgate.sock`. This means:
- No hardcoded primal socket paths in consumer code
- biomeOS routes `content.get`/`content.put` to nestGate automatically via capability discovery
- When nestGate evolves (e.g., `content.query` method), consumers get it without rewiring
- Same pattern applies to all primal interactions — consumers talk to Neural API, not individual primals

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

*Wave 155u/156b cascade. The provenance × acquisition divergence is the headline: inline provenance during bulk AlphaFold download caused a 12× throughput collapse (74 files/s → 6 files/s) due to sequential UDS RPC serialization. The trailer pattern (download fast, braid later) is the bridge; batch RPCs (`dag.event.batch` + `spine.entry.batch`) are the permanent fix. westGate now has data in three provenance states (primordial, CAS-only, fully braided) — the convergence path is defined and revalidation is running. This is a foundational scaling challenge that affects all high-throughput data federation. Meanwhile, massive upstream evolution overnight: esotericWebb evolved from V22 to V29 (8 commits — G18 signal dispatch, petalTongue live site, deep debt), hotSpring shipped 13 commits of arXiv production work (volume scan, preprint validation, provenance trio NFT pattern), and barraCuda went from YELLOW to GREEN (PRNG half-range bugs fixed, statistical validation harness). nestGate added `content.fetch` (HTTP→BLAKE3→CAS atomic), biomeOS wired 8 signal graphs for data federation, coralReef hit 156b debt pass (3,512 tests), toadStool eliminated 48 dead deps, sweetGrass evolved to zero-copy Arc\<str\>, and rhizoCrypt shipped G31 batch provenance. The ecosystem is now at **13/13 GREEN** for the first time — barraCuda's PRNG fix was the last holdout. ~130K+ tests. The data ingress and braiding pipeline is the critical evolution path: batch RPCs close the throughput gap, Neural API routing eliminates hardcoded socket paths, and the convergence check pattern (`is_dataset_converged()`) gives springs a trust gate before computation.*
