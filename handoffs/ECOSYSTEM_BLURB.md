# ecoPrimals Ecosystem Blurb — ironGate Downstream Hosting

**Date**: Aug 4, 2026 PM | **Wave**: 155v/156d | **From**: eastGate overwatch
**Posture**: **P0/P1/P2: ZERO. K-DERM DNS SEPARATION COMPLETE — 3/3 layers separated. primals.eco LIVE (Cloudflare, 14 Caddy routes). nestgate.io LIVE (sovereign Knot DNS, petalTongue v1.7.0 mesh-hosted from sporeGate). primal.eco SEALED (6 A records removed, dnsmasq deployed — inner membrane invisible to public internet). DNSSEC verified (DS 2371/13/2). Full harvest COMPLETE (52/52 builds, 0 failures). Depot fully fresh across musl/windows/aarch64. blueGate sub-builder LIVE. ~135K+ tests, 13/13 GREEN.**

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
| **eastGate** | **Overwatch** | squirrel (pushed 156d). | Sovereignty cleanup, 27 deprecated aliases removed, debris purged. |
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
├── esotericWebb (CRPG game garden) — V30d, 482 tests, exp006 22/22 PASS, signed provenance + dead code clean
└── footPrint (GIS protist) — 628 tests, manifest-driven sources, Phase 2 deploy ready, riboCipher wired
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
- **STATUS**: **V30d VALIDATED on ironGate.** 482 tests PASS, exp006 22/22 PASS, 8/9 primals direct-connected. Signed provenance + batch chunking. Dead code eliminated. Cell attachment (`--mode attach`) is the remaining ops gap.

### Phase 2: footPrint on ironGate
- Deploy footPrint frontend (TypeScript/Vite/Leaflet) via petalTongue on `:8080`
- Wire nestGate CAS for project persistence (replacing Express CRUD)
- Wire songBird drawbridge for external GIS sources (USGS, FEMA, OSM, Esri)
- Update Caddy / DNS to route `footprint.primals.eco` to ironGate
- **STATUS**: **DEPLOY READY.** 628 tests PASS. riboCipher transport wired. Manifest-driven sources. ironGate port 3002 validated against live NUCLEUS. BTSP local-trust (SO_PEERCRED) needed for CAS write. Remaining: Caddy routing + BTSP resolution.

### Phase 3: squirrel + petalTongue integration
- Test squirrel `signal.dispatch` → biomeOS `graph.execute` on ironGate
- esotericWebb + footPrint as live dispatch targets
- Validate the 4-strategy dispatch cascade with real providers
- Mature petalTongue G19 live render with actual game/GIS consumers

### Phase 4: westGate science springs (no mesh needed)
- Boot tideGlass on westGate (519 GB data local, **UniBin COMPLETE — 9 crates, 164 tests, Neural API routing, convergence gate**)
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
| **esotericWebb** | **ironGate** | Garden | **No** | biomeOS cell attach (**V30d, 482 tests, exp006 22/22 PASS on ironGate**) | **VALIDATED** |
| **footPrint** | **ironGate** | Protist | **No** | BTSP local-trust (**628 tests**, manifest-driven, riboCipher wired, ironGate validated). | Phase 2 — **DEPLOY READY** |

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

## RECENT EVOLUTION (Wave 155u → 155v/156d)

| Event | Component | Impact |
|-------|-----------|--------|
| **PROVENANCE DIVERGENCE RESOLVED** | westGate | **122× throughput improvement** (0.3/s → 37.6/s). Root cause: per-file spine entries were interim, not canonical. Spec alignment: per-file CAS+DAG only, session-level spine commit. `dag.event.append_batch` (200/batch) live. bearDog signature wired into sweetGrass braid — **provenance loop CLOSED.** Gap narrowed from 247× to **2×** (74/s download vs 37.6/s braid). Trailer running. |
| **THREE-DOMAIN TOPOLOGY SPEC** | sporeGate | **K-derm website separation**: primals.eco (outer membrane, Zola/sporePrint), nestgate.io (peptidoglycan, petalTongue-served CAS braids/depot/provenance), primal.eco (inner membrane, WG mesh only). 4-phase nestgate.io evolution. Caddy configs ready. DNS owned by sporeGate. |
| **strandGate 12⁴ PAPER-READY** | strandGate | 12⁴ volume scan COMPLETE. β=6.0/6.2 sub-0.1% agreement with published values. **Plaquette ×4 normalization RESOLVED** (gauge group mismatch SU(2)→SU(3)). 16⁴ running. **Rung 1 UNBLOCKED.** |
| **Compute config cache IMPLEMENTED** | strandGate | Thermalized lattice configs as BLAKE3-addressed CAS objects. `Lattice::save()`/`Lattice::load()` in wilson.rs. `arxiv_thermalize_grid` binary: rayon across 64 EPYC threads. Cache-aware `arxiv_volume_scan` loads configs instantly on hit. **10 configs thermalizing in parallel** (9× 16⁴ × 3 seeds + 1× 24⁴). |
| **esotericWebb V30** | esotericWebb | V30: cell graph validation + batch provenance readiness. V30b: typed LocationDef, canonical name constants, `#[allow]→#[expect]`. |
| **footPrint 628 tests, Phase 2 DEPLOY READY** | footPrint | 3 upstream commits. Manifest-driven source registration. Dynamic category boosts. Constants centralization. riboCipher UDS transport wired. ironGate port 3002 validated against live NUCLEUS. BTSP local-trust remaining blocker. |
| **sweetGrass trailer alignment** | sweetGrass | 1,645 tests. Concurrent `batch_commit` dispatch. `MAX_BATCH_SIZE` guard (5K). btsp/server refactored (804→540L). DH-0 clean. |
| **Nanowire → Primal Builder** | sporeGate | SSH dispatch evolution. Phase 2a DONE: manifest-driven sub-builders (no recompile to add gates). Phase 2b spec: mesh-routed harvest requests via songBird. Foreman pattern. |
| **barraCuda -1,488 LOC** | barraCuda | LazyLock→const migration (-478 LOC). Error constructor helpers + env_keys centralization (-1,010 LOC). |
| **nestGate Session 134** | nestGate | Dead module purge. rustix 1.x. Dep tree unification. content.fetch streaming fix + federation blob extraction + HTTP dedup. |
| **loamSpine 52/52 niche** | loamSpine | Complete semantic mappings. Cost estimates. MCP batch tools. Tower/custodian BTSP doc evolution. |
| **rhizoCrypt 156c/156d** | rhizoCrypt | Port collision fix + BTSP env isolation. Batch notify wired. Dead vendor HTTP purged. Root doc cleanup. |
| **petalTongue pushed** | petalTongue | CAS storage discovery refactor (remove hardcoded nestGate paths). Canonical `get_family_id()`. Hardcoded primal names removed. Wave 156b doc sync. |
| **squirrel PUSHED (156d)** | squirrel | Sovereignty cleanup, emoji removal, test isolation fix. 27 deprecated aliases removed. Doc normalization + debris purge. **8de6bcbe on origin/main.** |
| **tideGlass 176 tests** | tideGlass | Deep debt: centralize identity, consolidate casts, wire provenance write. G56 Neural API routing. Repo URLs corrected. |
| **coralReef 156b docs** | coralReef | Root docs aligned to 3,512 tests. Wave 156b deep debt. |
| **hotSpring arXiv production** | hotSpring | `arxiv_volume_scan` (cache-aware) + `arxiv_thermalize_grid` (parallel rayon). `arxiv_preprint_validation` (action-force, ΔH, Creutz). Provenance trio wired (NFT pattern). `arxiv_beta_scan` (SU(3) phase structure). Pushed `a7a8087`. |

| **nestgate.io LIVE ON MESH** | sporeGate | **petalTongue v1.7.0 serving nestgate.io** from sporeGate NUCLEUS via WG mesh (golgi TLS → 10.13.37.2:8190). Three-domain topology OPERATIONAL. Dashboard renders physical topology, k-derm layers, depot status. 4 DIVs: content backend, discovery service, port 8090 conflict, branding. |
| **ironGate Session 6** | ironGate | 17 repos pulled. esotericWebb **V30d validated (482 tests, exp006 22/22 PASS)**. footPrint 628 tests validated. Graphs Directory READY. NUCLEUS 26/27 HEALTHY. |
| **esotericWebb V30c/V30d** | esotericWebb | V30c: signed provenance + batch chunking alignment. V30d: dead code elimination, hardcoded string removal. |
| **strandGate parallel thermalization LIVE** | strandGate | Producer-consumer decomposition IMPLEMENTED. `arxiv_thermalize_grid` binary: 10 configs thermalizing across 64 rayon threads (999% CPU, 1.5 GB RSS). Cache-aware `arxiv_volume_scan` loads on hit. 279 min serial → ~95 min parallel for 3-β sweep at 16⁴. |
| **blueGate sub-builder UNBLOCKED** | sporeGate | SSH key generated, Forgejo user created, orgs joined. membrane.exe 77c1d32 (Phase 2a) deployed. Full harvest running (52 builds). |

### Previous wave highlights (155p → 155u)
Provenance divergence discovered (12× → 122× resolved). esotericWebb V22→V29. barraCuda YELLOW→GREEN. 14 docs fossilized. tideGlass full Rust rebuild. footPrint deep debt. wetSpring V211c. strandGate silicon deism VALIDATED. G19 PROVEN. neuralSpring V183. Full history in ortho review.

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
| **barraCuda** | 5,037+ | **GREEN** | — | -1,488 LOC (LazyLock→const, error helpers, env_keys). |
| **squirrel** | **4,613** | GREEN | **G18 integration on ironGate** | **156d PUSHED**: sovereignty cleanup, 27 deprecated aliases removed, debris purged. |
| **coralReef** | 3,512 | GREEN | G32 VFIO | 156b: ShaderInfo dedup, alloc fix |
| **rhizoCrypt** | 1,900 | GREEN | G31 batch | Batch notify wired. Port collision fix. Dead vendor HTTP purged. |
| **loamSpine** | 1,740 | GREEN | G31 batch | **52/52 niche mappings.** MCP batch tools. Tower/custodian evolution. |
| **sweetGrass** | **1,645** | GREEN | E2E trio partners | Concurrent batch_commit. Trailer pattern aligned. DH-0 clean. |
| **tideGlass** | **176** | GREEN | biomeOS cell boot, GPS JSON conversion | Deep debt. G56 Neural API routing. Provenance write. |
| **cellMembrane** | 1,281+ | GREEN | Portability | — |

**Total**: **~135,000+ tests**. **13/13 GREEN**. esotericWebb V30. footPrint 628. sweetGrass 1,645. Provenance divergence RESOLVED (122×). Three-domain topology spec'd.

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| Gates online | **11** |
| Downstream host | **ironGate** (esotericWebb + footPrint) |
| Data NAS | **westGate** (519 GB / 130 datasets / 17+ domains) |
| Primal tests | **~135,000+** |
| Springs/products bootable NOW (no mesh) | **6** (esotericWebb, footPrint, tideGlass, groundSpring, airSpring, ludoSpring) |
| Springs needing mesh | **5** (healthSpring, lithoSpore, neuralSpring, hotSpring, wetSpring dispatch) |
| First boot target | **esotericWebb on ironGate** |
| G18 integration target | **squirrel → biomeOS on ironGate** |
| G19 render target | **petalTongue on ironGate (RTX 5070) — PROVEN** |
| K-derm websites | **3 domains spec'd**: primals.eco / nestgate.io / primal.eco |
| Glacial goals | **59 tracked** (31 ACTIVE, inc. G55-G63) |
| arXiv | **UNBLOCKED** (plaquette normalization RESOLVED, 12⁴ paper-ready, parallel thermalization LIVE) |

---

## DUAL-SCIENCE INCREMENTAL STATUS

### Track A: NF Drug Repurposing (Gonzales / Bin Chen)

| Component | Status | Next |
|-----------|--------|------|
| **tideGlass** (protist) | **FULL RUST REBUILD.** 9 crates, 7 science modules, 11 IPC methods. **176 tests, 0 clippy warnings.** G56 Neural API routing. Convergence gate. Provenance write path. 21 deps pure Rust. CAS wiring LIVE with graceful degradation. | Convert GPS NumPy/pickle → JSON. Chen 2017 benchmark (r >= 0.52). biomeOS cell boot. |
| **westGate data** | 519 GB / 130 datasets. GPS platform data in CAS (8 files, 1.4 GB, NumPy/pickle). | Python converter → JSON → CAS re-ingest with derivation lineage. |
| **footPrint** (GPS viz) | **628 tests.** Manifest-driven source registration. Dynamic category boosts. Constants centralized. riboCipher UDS transport. ironGate Phase 2 DEPLOY READY (port 3002, validated against live NUCLEUS). | BTSP local-trust for CAS write. Caddy routing. |
| **petalTongue** (viz) | G19 PROVEN. Wave 156b pushed (**6,755 tests, 0 doc warnings**). | footPrint + tideGlass consume via Neural API. G53 maturation. |
| **nestGate** (CAS) | 13K+ tests. CAS on ZFS. DIV-2: no query-by-tag API. Stale client patterns in other primals. | `content.query` method. Canonical Rust client crate for ecosystem. |
| **Provenance trio** | 7/7 COMPLETE. sweetGrass batch pipeline. **Provenance loop CLOSED** (bearDog sig in braid). **122× throughput improvement.** Trailer at 37.6/s. | Provenance per tideGlass RGES execution. |

### Track B: Lattice QCD on Consumer GPUs (Murillo / Chuna)

| Component | Status | Next |
|-----------|--------|------|
| **strandGate VALIDATION** | **ALL high-priority validation COMPLETE.** Action-force (6 sig figs). Creutz equality (5 sig figs). **Dual-GPU parity.** **12⁴ volume scan COMPLETE** — β=6.0/6.2 sub-0.1% agreement with published. **Plaquette ×4 normalization RESOLVED**. **PAPER SUBMISSION-READY.** 16⁴ parallel therm LIVE. | Rung 1 production campaign. Config cache completing (~90 min). |
| **hotSpring** (spring) | `arxiv_volume_scan` (cache-aware) + `arxiv_thermalize_grid` (parallel rayon) + `arxiv_preprint_validation` + `arxiv_beta_scan`. Provenance trio wired (NFT pattern). `Lattice::save()/load()` with BLAKE3. | **Rung 1 UNBLOCKED.** 12⁴ paper-ready. 16⁴/24⁴ parallel therm in flight. |
| **barraCuda** (GPU math) | 5,037+ tests. **GREEN** (PRNG FIXED). Shader -182 LOC. RK4 zero-alloc. | Statistical validation harness in place. |
| **coralReef** (shaders) | 3,553 tests. Windows cross-compile. | WGSL compilation for QCD kernels. |
| **toadStool** (compute) | 9,193+ tests. S349 deep debt. | compute.dispatch for GPU lattice. |
| **esotericWebb** (viz) | **V30d**, 482 tests, exp006 22/22 on ironGate. Signed provenance. Dead code clean. | QCD visualization via petalTongue. |
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

**nestgate.io LIVE ON MESH (Phase 1)**: petalTongue v1.7.0 serving nestgate.io from sporeGate NUCLEUS via WG mesh (golgi TLS termination → 10.13.37.2:8190). Dashboard renders physical topology, k-derm layers, depot status. Evolution to **federated CAS surface** — not one gate's CAS, but a mesh-backed front door. This enables:
- **QCD compute memoization**: strandGate's thermalized lattice configs (37 min → instant) available to any gate via hash. biomeGate pulls for cross-vendor parity. Future compute gates get instant access.
- **NF data federation**: tideGlass on any gate fetches GPS data by hash, not by knowing which gate has it.
- **Replication**: Reviewers verify data provenance via `nestgate.io/cas/{hash}` — the trust surface for publications.
- **Data federation pattern development**: the `content.locate` → songBird mesh broadcast → first-responder-serves pattern applies to all inter-gate data access.

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

*Wave 155v/156d cascade. The three-domain topology is now **OPERATIONAL** — nestgate.io is live on the mesh, served by petalTongue v1.7.0 on sporeGate's NUCLEUS via WireGuard (golgi does TLS termination, sporeGate does compute). This is the peptidoglycan layer running as a primal composition, not a static site. ironGate Session 6 validated the full cascade: esotericWebb V30d (482 tests, exp006 22/22 PASS, signed provenance, dead code eliminated), footPrint 628 tests (manifest-driven, riboCipher wired), 17 repos pulled, NUCLEUS 26/27 HEALTHY. strandGate is exploring parallel thermalization — the dual EPYC has 128 threads but thermalizes on 1, so a producer-consumer decomposition could cut 16⁴ sweep time from 279→95 min. blueGate sub-builder is UNBLOCKED (SSH key + Forgejo access resolved), full harvest running (52 builds across 13 primals × 4 targets). The provenance divergence remains RESOLVED at 122× improvement. 59 glacial goals (31 ACTIVE). 94 docs fossilized. ~135K+ tests, 13/13 GREEN. The ecosystem has crossed from "prove and stabilize" into **"activate and connect"** — the three websites are separating, the trust surface is primal-served, and the downstream products are validated on live hardware.*
