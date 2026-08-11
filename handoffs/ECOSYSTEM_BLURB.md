# ecoPrimals Ecosystem Blurb — Wave 157i POST-PANDEMIC CASCADE

**Date**: Aug 11, 2026 | **Wave**: 157i | **From**: overwatch (gate-agnostic)
**Posture**: **G72 POST-PANDEMIC CASCADE COMPLETE. ALL GATES REPORTED.** G72 Tier 1 (11/11, ~155+ crates) absorbed fleet-wide. **graftGate 15/15 primals compiled** on `aarch64-apple-darwin` (was 12/15 — 4 darwin fixes applied). **WireGuard LIVE** at 10.13.37.13, 6 mesh peers. **southGate canary +12.2%** (19.7K conn/s) — G72 dep trimming = faster IPC. **Process leak FIXED** fleet-wide (RAII ChildGuard). **ironGate 2ms dispatch** (8x faster, was 16ms), 2 gossip peers converged. **westGate braid.verify 99/100 deployed** (0.3ms), E2E provenance 8/8 in 12ms. **Gossip mesh: 5 gates active** (eastGate, sporeGate, strandGate, westGate, ironGate). blueGate G72 source absorbed, awaiting depot rebuild. southGate swarmVine operational (TCP 7800), 0 cross-gate peers (topology blocker). piGate PLANNED, riscGate ON ORDER. Hardware deployment profile: 5 tiers, 4 ISAs.

---

## G72 DEPENDENCY PANDEMIC — TIER 1 COMPLETE (11/11)

| Team | Deps shed | Impact | Status |
|------|-----------|--------|--------|
| **toadStool** | 7 dead deps removed, 6 promoted to workspace, tokio 118→65 files, plugin-loading/vulkano/core-wgpu excised | ~73 GiB reclaimed (S377-S379). `tokio::fs` eliminated (28 files → `std::fs`). | **G72 EXEMPLAR** |
| **nestGate** | jsonrpsee removed (1,864 LOC), crossbeam umbrella→channel, dead bincode. **S147/S148**: nestgate-nas crate dropped, steam feature removed, shared state consolidation | -10 crates. 1,666 tests. Deep debt S146-S148. | **TIER 1 DONE** |
| **rhizoCrypt** | wiremock removed (0 usage), hashbrown dedup | **-46 crates (14.6%)**. Also: deep debt sweep, vertex builder extraction. | **TIER 1 DONE** |
| **coralReef** | futures/tokio-util gated behind `tarpc-transport`, tokio/process→dev-deps | Feature-surface trim. Also: `#[allow]→#[expect]` Rust 2024 idiom. | **TIER 1 DONE** |
| **sweetGrass** | tokio `["full"]`→7 features, dead bincode/chrono removed | **P2 braid.verify CLOSED** (5 behavioral tests). Also: batch+verify submodule extraction. | **TIER 1 DONE** |
| **loamSpine** | url+ICU chain excised, chacha20poly1305 0.10→0.11 | -7 crates. RustCrypto unified. Also: deep debt + test refactoring. | **TIER 1 DONE** |
| **cellMembrane** | tokio rt-multi-thread→dev-deps, time/macros removed | Socket name dedup (3→1 canonical). Also: NUCLEUS install lifecycle extraction. | **TIER 1 DONE** |
| **tideGlass** | tokio rt-multi-thread→rt (current-thread) | Lean gen5 primal. Already 21 transitive deps. | **TIER 1 DONE** |
| **wetSpring** | Verified clean (pollster removed V211) | Primary work: gossip injection. | **TIER 1 VERIFIED** |
| **bearDog** | **41 dead dependencies removed**, `tokio["full"]` eliminated | Massive dep tree trim. Pure trust primal. | **TIER 1 DONE** |
| **petalTongue** | Telemetry crate removed, runtime discovery replaces 13 hardcoded peers, dep/version cleanup | Convergent — discovers peers at runtime, no hardcoding. | **TIER 1 DONE** |

**~155+ crates shed fleet-wide** (up from ~114 with 9/9). **Tier 2 queued**: HTTP client consolidation (nestGate ureq→songBird, loamSpine ureq→capability.call), axum 0.7→0.8 (5 projects), wgpu 22→28 (toadStool), YAML unification.

---

## GOSSIP INJECTION — 7/16 PRIMALS LIVE (was 6/16)

| Entity | Events | Status |
|--------|--------|--------|
| **rhizoCrypt** | 3 DAG lifecycle | LIVE |
| **loamSpine** | 4 spine events | LIVE |
| **lithoSpore** | 4 validation events | LIVE (registry synced) |
| **barraCuda** | **22/22 runtime events** (compute, tower, shader, dispatch, quota, OOM, precision — recovered, precision-degraded, systemic-error final 3 wired) | **LIVE — FULL SPEC COVERAGE** |
| **esotericWebb** | 2 session lifecycle | **LIVE** (V33) |
| **songBird** | 1 capability advertise | LIVE |
| **wetSpring** | **4/4** (PipelineComplete, ProvenanceWitness + 2 remaining wired) | **LIVE** |
| **nestGate** | Gossip hooks at 11 CAS sites, 6 event types | **WIRED** (S147/S148) |
| **hotSpring** | 0/10 (scaffold, not hooked) | SCAFFOLD |

**Cross-gate gossip mesh — 5 gates active**:

| Gate | Gossip Peers | Status | Notes |
|------|-------------|--------|-------|
| eastGate | 3 peers, 662 ingested | **ACTIVE** | Hub node |
| sporeGate | 2 peers, 660+ ingested | **ACTIVE** | Hub node |
| westGate | 4 peers | **ACTIVE** | braid.verify 99/100 deployed, E2E 8/8 12ms |
| ironGate | 2 peers (westGate + eastGate) | **ACTIVE** | 2ms dispatch (8x faster). Vine-bat operational. |
| strandGate | 1 peer | **ACTIVE** | |
| southGate | 0 cross-gate peers | **OPERATIONAL locally** | swarmVine TCP 7800 listening, topology blocker. Canary +12.2%. Process leak FIXED. |
| blueGate | 0 cross-gate peers | **TCP 7800 2/7 open** | G72 source absorbed, depot pre-rebuild. MeshRelay needed. |
| graftGate | — | **WG LIVE, 6 peers** | 15/15 compiled. Gossip not yet started. |

---

## SCIENCE PIPELINE

**hotSpring pseudoSpore E2E** — pure Rust pipeline shipped:
- `arxiv_production_campaign` → `arxiv_analysis` → `pseudospore_manifest` → `pseudospore_bundle` → `pseudospore_sign` (bearDog Ed25519) → `pseudospore_register` (westGate CAS + ironGate NFT)
- 32⁴ thermalization fix (dt 0.01→0.005, warmup 500→1500)
- 10 gossip events defined (scaffold — not yet hooked)

---

## graftGate — 15/15 COMPILED, WireGuard LIVE

**Hardware**: M4 Mac Mini (Apple Silicon, `aarch64-apple-darwin`)
**Network**: WireGuard **LIVE** at `10.13.37.13`, 6 mesh peers reachable (golgiBody + 5 gates). 38ms RTT to golgiBody.
**Status**: **15/15 primals compiled** (100%). 41/42 repos cloned. WG operational.

**All `aarch64-apple-darwin` binaries** (total ~98.1M Mach-O arm64):

| Primal | Size | Fix? | Primal | Size | Fix? |
|--------|------|------|--------|------|------|
| bearDog | 6.3M | Yes (ios.rs import) | sweetGrass | 10M | Clean |
| songBird | 17M | Clean | barraCuda | 2.2M | Clean |
| skunkBat | 2.6M | Clean | coralReef | 6.6M | Clean |
| nestGate | 6.7M | Clean | biomeOS | 16M | Clean |
| rhizoCrypt | 5.8M | Clean | swarmVine | 2.0M | Clean |
| loamSpine | 3.8M | Clean | sourDough | 2.8M | Clean |
| toadStool | 6.3M | Yes (cfg gate) | squirrel | 2.8M | Yes (`--target`) |
| petalTongue | 13M | Yes (rustix API) | | | |

**4 darwin fixes applied locally** (need upstream merge):
1. **bearDog**: ios.rs missing `use beardog_config::env_keys` import
2. **toadStool**: `#[cfg(unix)]` → `#[cfg(target_os = "linux")]` alignment for `silicon_registry_status`
3. **squirrel**: `.cargo/config.toml` hardcodes musl target — build with explicit `--target aarch64-apple-darwin`
4. **petalTongue**: rustix Signal API → `test_kill_process(pid)` (purpose-built process probe)

**Remaining blockers**: SSH key registration in Forgejo (push access), golgiBody SSH for depot push of 15 darwin binaries.

**graftGate: G12 COMPLETE. G11 — 4th platform, 5th OS family. 15/15 on apple-darwin.**

---

## CASCADE STATUS — Gate Reports

All gates have cascaded and reported via AARs. Phase 2 (pull + redeploy) is **COMPLETE** for 5/6 NUCLEUS gates.

### Gate Cascade Results

| Gate | Cascade | Binaries | Key Result |
|------|---------|----------|------------|
| **westGate** | 42/42 repos | 16 G72-trimmed pulled | braid.verify 99/100 (0.3ms). E2E 8/8 (12ms). content.stat operational. tideGlass absorbed. |
| **southGate** | full | 12/13 updated | Canary **+12.2%** (19.7K conn/s). Process leak **FIXED** (RAII ChildGuard). swarmVine operational (0 peers). Readiness 8/11. |
| **ironGate** | 26 repos | 15 G72-trimmed deployed | **2ms dispatch** (8x faster). 2 gossip peers (westGate + eastGate). 166 capabilities. Vine-bat operational. |
| **blueGate** | 19/20 repos (source) | **0/15** (depot pre-rebuild) | NUCLEUS 13/13 alive. TCP 7800 2/7 open (from 0). WG 7/7 peers incl. graftGate .13. MeshRelay needed. |
| **graftGate** | 41/42 repos | **15/15 compiled locally** | WG LIVE at .13, 6 mesh peers. 4 darwin fixes applied. ~98.1M darwin payload ready. |

### Remaining Phase 1: sporeGate — Topology + graftGate Enmeshment

sporeGate owns the peptidoglycan layer (LAN↔golgiBody) and mesh topology.

| Task | Detail | Status |
|------|--------|--------|
| **Register graftGate SSH key** in Forgejo | Enable push access (currently HTTPS read-only) | PENDING |
| **Add graftGate WG peer** on golgiBody | Pubkey: `ekHFlu0N6gdAFkk5lNLhgmWqGOptiTzmso8qWGx/yB4=`, AllowedIPs: `10.13.37.13/32` | **WG LIVE** (peer added) |
| **G72 Depot rebuild** | Rebuild with G72-trimmed binaries. blueGate still on pre-G72 depot. | PENDING |
| **sporePrint clone** for graftGate | sporePrint is private — graftGate needs SSH auth before it can clone (41/42 currently) | PENDING |
| **Darwin depot target** | 15 darwin binaries ready for new depot target dir once SSH access granted | PENDING |

### Phase 3: Next Waves — Code Evolution + Enmeshment

Code teams (Tier 2 agents) pick up primal-specific work. Overwatch does NOT fix code — code teams own their primals.

| Wave | Scope | Teams |
|------|-------|-------|
| **Darwin upstream merge** | 4 local fixes need upstream: bearDog ios.rs import, toadStool cfg gate, squirrel `--target`, petalTongue rustix API. | bearDog, toadStool, squirrel, petalTongue |
| **biomeOS category shadow** | Category registration shadows explicit TOML translations — braid.verify/braid.list not routable via Neural API. Direct socket calls work (0.4ms). | biomeOS code team |
| **bearDog binary growth** | +2.9MB despite 41-dep removal. Possible debug symbols or static linking change. | bearDog code team |
| **songBird MeshRelay** | Critical cross-gate blocker for blueGate + southGate gossip. mesh.init works, relay/inject/spread not shipped. | songBird code team |
| **swarmVine Windows port** | 5 UDS call sites need `#[cfg(unix)]` + TCP fallback. Source fix exists, not in depot. | swarmVine code team |
| **G72 Tier 2** | HTTP client → songBird/capability.call, axum 0.7→0.8, wgpu 22→28, YAML unification | Fleet-wide |
| **Gossip completion** | hotSpring 0/10 events (scaffold only). Cross-gate peering expansion. | hotSpring, songBird |
| **Atomic compositions** | Multi-composition orchestration, biome.yaml graph executor, deploy register→gossip→verify-in-mesh lifecycle | primalSpring, biomeOS |
| **NUCLEUS inner membrane** | Full inner membrane testing — all IPC via Tower Atomic mesh. Validate capability.call fleet-wide. | All NUCLEUS gates |
| **NanoWire cleanup** (late stage) | Purge SSH-based patterns. Tower Atomic replaces SSH. Enables LAN/WAN/mobile deployment configs. | Fleet-wide, gradual |

### Convergence Rule

> **Forgejo is canonical. Gates pull, validate, report.**
> 1. Gate teams pull from Forgejo and redeploy.
> 2. Code teams fix their own primals in fresh IDE sessions (K-NOME Blurb 1 + 2).
> 3. Overwatch coordinates via this ecosystem blurb (Tier 3).
> 4. Darwin/platform findings are documented as handoffs — code teams merge upstream.
> 5. NanoWire/SSH cleanup is evolutionary, not a hard cutover — Tower Atomic replaces SSH patterns as primals go live on each gate.

---

## GATE × TEAM MATRIX — Rationalized Placement

See `ORTHOGONAL_DIMENSIONS_REVIEW.md` § "Gate × Team × Deployment Matrix" for the full table.

| Gate | Code Teams |
|------|------------|
| eastGate | primalSpring, biomeOS, squirrel, songBird, overwatch |
| ironGate | toadStool, barraCuda, coralReef, petalTongue, esotericWebb, footPrint |
| westGate | rhizoCrypt, loamSpine, sweetGrass, nestGate, tideGlass, wetSpring |
| strandGate | hotSpring batch only — no interactive code teams |
| sporeGate | cellMembrane ops only — lean |
| biomeGate | Node Atomic cross-vendor GPU experiments |
| graftGate | Apple/darwin builds, iosGate prep, sourDough cross-arch |

## THREE-TIER BLURB SYSTEM

| Tier | Audience | Document | Lifecycle |
|------|----------|----------|-----------|
| **1 (Gate)** | Hardware overwatch agent | `GATE_SPINUP_BLURB.md` (universal, platform-adaptive) | Long-lived, rare restart |
| **2 (Code Team)** | Fresh per-team agent | User's K-NOME Blurb 1 (audit) + Blurb 2 (execute) from northGate prompt bank | Frequent restart, disposable |
| **3 (Ecosystem)** | Overwatch coordination | `ECOSYSTEM_BLURB.md` (this document) | As needed for cascade context |

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| Primals | **16** (15 + sourDough) |
| NUCLEUS gates | **6/6** — 5/6 G72-deployed, blueGate awaiting depot rebuild |
| P0 / P1 / P2 | **0 / 0 / 1** (P2: petalTongue port). ~~braid.verify~~ **CLOSED**. ~~process leak~~ **FIXED** (RAII ChildGuard). |
| G72 Tier 1 | **11/11 teams DONE**. **~155+ crates shed.** Fleet-wide cascade complete. southGate canary: **+12.2%** (19.7K conn/s). |
| Cross-gate gossip | **5-gate mesh ACTIVE** (eastGate, sporeGate, strandGate, westGate, ironGate). southGate operational locally. blueGate TCP 7800 2/7 open. |
| Gossip injection | **7/16 primals LIVE**. barraCuda **22/22**. wetSpring **4/4**. nestGate 11 CAS sites. |
| Provenance | **braid.verify 99/100 deployed** (0.3ms). **E2E chain 8/8** (12ms). content.stat operational. |
| Performance | ironGate **2ms dispatch** (8x faster). southGate **19.7K conn/s** (+12.2%). Process leak **0/hr** fleet-wide. |
| graftGate | **15/15 compiled** (was 12/15). WG LIVE at .13, 6 peers. 4 darwin fixes applied, need upstream merge. |
| WASM | **38/48** (79%). toadStool wiring improved (S379 last-mile). |
| Science pipeline | **hotSpring pseudoSpore E2E shipped** (pure Rust). |
| Hardware profile | piGate (Pi 500) PLANNED. riscGate (Jupiter 2) ON ORDER. 5-tier deployment matrix. |
| Tests | **~150K+** across 16 primals + gardens + springs |

---

## GLACIAL

| Goal | Status |
|------|--------|
| **G72 Dependency Pandemic** | **Tier 1 COMPLETE (11/11 teams, ~155+ crates).** Tier 2: HTTP→songBird, axum→0.8, wgpu→28. Tier 3: sourDough dep validator. |
| **graftGate (G12)** | **15/15 compiled.** WG LIVE at .13, 6 peers. 4 darwin fixes applied locally — need upstream merge. SSH key registration + depot push remaining. |
| arXiv 41/42 | Campaign IN PROGRESS. pseudoSpore pipeline shipped. 32⁴ fix landed. |
| `native_braid.py` → Rust | Last major jelly string (1,259 LOC) |
| Inner Membrane Phase 4 | Pure primal communication — WG deprecation |
| iosGate | After graftGate + Apple Dev Program |
| steamGate | Future platform gate |
| **piGate (Pi 500)** | **PLANNED.** Raspberry Pi 500/500+ keyboard computer. `aarch64-unknown-linux-gnu`. $180-190. Cortex-A76 2.4GHz quad, 8/16 GB, Vulkan 1.3. Classroom/conference NUCLEUS demo — plug HDMI + USB-C, join mesh. Pi 500+ (16 GB) for full NUCLEUS headroom. |
| **riscGate (Jupiter 2)** | **ON ORDER.** Milk-V Jupiter 2. `riscv64gc-unknown-linux-gnu`. Third ISA, first RISC-V gate. SpacemiT K3 8-core RVA23 2.4GHz, up to 32 GB LPDDR5, **60 TOPS A100 NPU** (INT4-FP16), 10GbE SFP+. Self-build like graftGate. NPU dispatch via rustChip pattern. RVV 1.0 vector codegen validation. |
| PrecisionBrain routing | barraCuda Fp64→F16 silicon-aware dispatch |
| PTX SM120 / Blackwell | coralReef next-gen NVIDIA target |
| **Hardware Deployment Profile** | **Wave 157i.** 5-tier deployment matrix profiled: Systems (A), Mobile (B), Accelerators (C), Edge/IoT (D), Exotic/type-check (E). ISA coverage: x86_64 PROVEN, aarch64 PROVEN+PLANNED, riscv64 ON ORDER, armv7 depot. See `ORTHOGONAL_DIMENSIONS_REVIEW.md` Hardware Deployment Profile section. |

---

*Wave 157i — POST-PANDEMIC CASCADE COMPLETE. G72 Tier 1: 11/11, ~155+ crates. All gates cascaded and reported. graftGate 15/15 on apple-darwin, WG LIVE. southGate canary +12.2%, process leak FIXED. ironGate 2ms dispatch (8x). westGate braid.verify 99/100 (0.3ms), E2E 8/8 (12ms). 5-gate gossip mesh active. piGate PLANNED, riscGate ON ORDER. 0/0/1. 6/6 NUCLEUS. ~150K+ tests.*
