# ecoPrimals Ecosystem Blurb — Wave 157i PANDEMIC RESPONDS

**Date**: Aug 10, 2026 9:59PM | **Wave**: 157i | **From**: overwatch (gate-agnostic)
**Posture**: **G72 PANDEMIC: 9/9 PHASE 1 TEAMS RESPONDED. ALL TIER 1 COMPLETE.** The stadial shift landed. 9 teams pushed G72 Tier 1 dep excision — ~114 crates shed fleet-wide, tokio trimmed/gated across 8 primals, jsonrpsee excised (nestGate), wiremock excised (rhizoCrypt -46 crates), url+ICU chain removed (loamSpine -7), dead features excised (toadStool: plugin-loading, vulkano, core wgpu). **P2 braid.verify CLOSED** (sweetGrass behavioral tests). **Gossip injection 3→6/16 primals LIVE** (barraCuda 19 events fully wired, esotericWebb 2, lithoSpore synced). **hotSpring pseudoSpore E2E pipeline shipped** (compute → manifest → bundle → sign → register — pure Rust, no Python). **toadStool tokio 118→65 files (45% reduction).** **darwinGate hardware arrived** (M4 Mac Mini) — iPhone XS tethering for network, first `aarch64-apple-darwin` target.

---

## G72 DEPENDENCY PANDEMIC — TIER 1 COMPLETE

| Team | Deps shed | Impact | Status |
|------|-----------|--------|--------|
| **toadStool** | 7 dead deps removed, 6 promoted to workspace, tokio 118→65 files, plugin-loading/vulkano/core-wgpu excised | ~73 GiB reclaimed (S377-S379). `tokio::fs` eliminated (28 files → `std::fs`). | **G72 EXEMPLAR** |
| **nestGate** | jsonrpsee removed (1,864 LOC), crossbeam umbrella→channel, dead bincode | -10 crates. Also: deep debt S146 (fake success paths eliminated). | **TIER 1 DONE** |
| **rhizoCrypt** | wiremock removed (0 usage), hashbrown dedup | **-46 crates (14.6%)**. Also: deep debt sweep, vertex builder extraction. | **TIER 1 DONE** |
| **coralReef** | futures/tokio-util gated behind `tarpc-transport`, tokio/process→dev-deps | Feature-surface trim. Also: `#[allow]→#[expect]` Rust 2024 idiom. | **TIER 1 DONE** |
| **sweetGrass** | tokio `["full"]`→7 features, dead bincode/chrono removed | **P2 braid.verify CLOSED** (5 behavioral tests). Also: batch+verify submodule extraction. | **TIER 1 DONE** |
| **loamSpine** | url+ICU chain excised, chacha20poly1305 0.10→0.11 | -7 crates. RustCrypto unified. Also: deep debt + test refactoring. | **TIER 1 DONE** |
| **cellMembrane** | tokio rt-multi-thread→dev-deps, time/macros removed | Socket name dedup (3→1 canonical). Also: NUCLEUS install lifecycle extraction. | **TIER 1 DONE** |
| **tideGlass** | tokio rt-multi-thread→rt (current-thread) | Lean gen5 primal. Already 21 transitive deps. | **TIER 1 DONE** |
| **wetSpring** | Verified clean (pollster removed V211) | Primary work: gossip injection. | **TIER 1 VERIFIED** |

**Tier 2 queued**: HTTP client consolidation (nestGate ureq→songBird, loamSpine ureq→capability.call), axum 0.7→0.8 (5 projects), wgpu 22→28 (toadStool), YAML unification.

---

## GOSSIP INJECTION — 6/16 PRIMALS LIVE (was 3/16)

| Entity | Events | Status |
|--------|--------|--------|
| **rhizoCrypt** | 3 DAG lifecycle | LIVE |
| **loamSpine** | 4 spine events | LIVE |
| **lithoSpore** | 4 validation events | LIVE (registry synced) |
| **barraCuda** | **19 runtime events** (compute, tower, shader, dispatch) | **LIVE** — was "20 spec'd, hooks pending" |
| **esotericWebb** | 2 session lifecycle | **LIVE** (V33) |
| **songBird** | 1 capability advertise | LIVE |
| **wetSpring** | 2/4 (PipelineComplete, ProvenanceWitness) | PARTIAL |
| **hotSpring** | 0/10 (scaffold, not hooked) | SCAFFOLD |

**Cross-gate**: 4-gate mesh (sporeGate, eastGate, strandGate, westGate). ironGate listening, not yet peered. blueGate + southGate blocked (need MeshRelay + depot rebuild).

---

## SCIENCE PIPELINE

**hotSpring pseudoSpore E2E** — pure Rust pipeline shipped:
- `arxiv_production_campaign` → `arxiv_analysis` → `pseudospore_manifest` → `pseudospore_bundle` → `pseudospore_sign` (bearDog Ed25519) → `pseudospore_register` (westGate CAS + ironGate NFT)
- 32⁴ thermalization fix (dt 0.01→0.005, warmup 500→1500)
- 10 gossip events defined (scaffold — not yet hooked)

---

## darwinGate — M4 Mac Mini ARRIVED

**Hardware**: M4 Mac Mini (Apple Silicon, aarch64-apple-darwin)
**Network**: iPhone XS tethering via USB (ecoPrimal user)
**Role**: First apple-darwin gate. Self-builds `aarch64-apple-darwin` binaries for depot.

**Setup plan**:
1. **Bootstrap**: Install Rust toolchain (rustup), clone ecoPrimals from Forgejo
2. **Network**: USB tethering to iPhone XS → internet access for initial setup. Then LAN via ethernet/WiFi to mesh
3. **Build**: Self-compile Tower Atomic (bearDog + songBird + skunkBat) as proof of `aarch64-apple-darwin`
4. **Enroll**: `gate-enroll.sh` → golgiBody drawbridge → mesh enrollment
5. **Depot**: Push `aarch64-apple-darwin` binaries to golgi (new depot target directory)
6. **Validate**: NUCLEUS lifecycle on macOS — launchd vs systemd (cellMembrane `InitSystem::Launchd` path)
7. **Future**: iosGate (iPhone) depends on this gate + Apple Dev Program

**darwinGate moves from GLACIAL → ACTIVE (G12).**

---

## IMMEDIATE WORK — Post-Pandemic

| Priority | Goal | Owner | Effort |
|----------|------|-------|--------|
| **HIGH** | **songBird MeshRelay** | songBird | Days — blueGate + southGate blocked |
| **HIGH** | **Depot rebuild** with gossip + MeshRelay binaries | sporeGate | Hours |
| **HIGH** | **darwinGate bootstrap** | overwatch + primalSpring | Days — M4 setup + tower compile + enrollment |
| **HIGH** | **sourDough `convergence` + `rpc-surface` live CI** | cellMembrane + sourDough | Days |
| **MED** | **G72 Tier 2**: HTTP→songBird, axum→0.8, wgpu→28 | Fleet-wide | Sprint |
| **MED** | **Remaining gossip hooks** | hotSpring (10 events), wetSpring (2 remaining), barraCuda (3 edge) | Days |
| **MED** | **pseudoSpore E2E validation** | hotSpring + ironGate + westGate | Days |
| **LOW** | **Full bidirectional gossip peering** | All gates | Hours |

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| Primals | **16** |
| NUCLEUS gates | **6/6** — all 157e deployed |
| P0 / P1 / P2 | **0 / 0 / 1** (P2: petalTongue port). ~~braid.verify behavioral~~ **CLOSED** (sweetGrass). |
| G72 Tier 1 | **9/9 teams DONE**. ~114 crates shed fleet-wide. toadStool tokio 118→65. |
| Cross-gate gossip | **4-gate mesh LIVE**. ironGate reachable. blueGate + southGate blocked. |
| Gossip injection | **6/16 primals LIVE** (was 3). barraCuda 19 events. esotericWebb 2. 9 entities total. |
| WASM | **38/48** (79%). toadStool wiring improved (S379 last-mile), count flat. |
| Science pipeline | **hotSpring pseudoSpore E2E shipped** (pure Rust: compute → sign → register). |
| darwinGate | **M4 ARRIVED**. First `aarch64-apple-darwin`. iPhone XS tethering. GLACIAL → ACTIVE. |
| Tests | **~150K+** across 16 primals + gardens + springs |

---

## GLACIAL

| Goal | Status |
|------|--------|
| **G72 Dependency Pandemic** | **Tier 1 COMPLETE (9/9 teams).** Tier 2: HTTP→songBird, axum→0.8, wgpu→28. Tier 3: sourDough dep validator. |
| **darwinGate (G12)** | **ACTIVE** — M4 arrived. iPhone XS tethering. Setup imminent. |
| arXiv 41/42 | Campaign IN PROGRESS. pseudoSpore pipeline shipped. 32⁴ fix landed. |
| `native_braid.py` → Rust | Last major jelly string (1,259 LOC) |
| Inner Membrane Phase 4 | Pure primal communication — WG deprecation |
| iosGate | After darwinGate + Apple Dev Program |
| steamGate | Future platform gate |
| PrecisionBrain routing | barraCuda Fp64→F16 silicon-aware dispatch |
| PTX SM120 / Blackwell | coralReef next-gen NVIDIA target |

---

*Wave 157i — PANDEMIC RESPONDS. G72 Tier 1: 9/9 teams complete, ~114 crates shed, toadStool tokio 118→65. P2 braid.verify CLOSED (0/0/1). Gossip 6/16 LIVE (barraCuda 19 events). hotSpring pseudoSpore E2E pipeline shipped. darwinGate M4 arrived — GLACIAL→ACTIVE. The interstadial selects for lean primals. 6/6 gates. ~150K+ tests.*
