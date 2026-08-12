# ecoPrimals Ecosystem Blurb — Wave 157j

**Date**: Aug 11, 2026 | **Wave**: 157j | **From**: overwatch (gate-agnostic)
**Posture**: **LAN GOSSIP VALIDATED.** southGate confirms Tower Atomic mesh works on LAN without WireGuard. Stale peer registry is the actual blocker. Remaining work: registry cleanup, blueGate/sporeGate depot, 2 code bugs.

---

## REMAINING WORK — PRIORITIZED

### Critical Path (blocks enmeshment)

| Item | Owner | Detail | Blocker For |
|------|-------|--------|-------------|
| ~~songBird MeshRelay~~ | songBird | **SHIPPED.** relay/inject/spread/subscribe. | ~~blueGate + southGate~~ **UNBLOCKED** |
| ~~graftGate depot push~~ | graftGate | **DONE.** 15 darwin binaries pushed (104M, BLAKE3). 5th OS family in depot. iOS cross-compile live. | **RESOLVED** |
| ~~southGate MeshRelay~~ | southGate | **LIVE + LAN GOSSIP VALIDATED.** 5 songBird mesh peers, 4 swarmVine gossip peers on 192.168.4.x/22. Previous "topology blocked" was **wrong** — stale WG-era peer addresses, not network isolation. | **RESOLVED** |
| **Peer registry cleanup** | sporeGate topology | Stale `192.168.1.x` / `10.0.0.x` addresses in songBird discovery registry and wateringHole head files. Must update to actual LAN IPs (`192.168.4.x`). Also: node_id mismatch (southGate reports `pop-os`). | All gates' mesh auto-connect |
| **blueGate depot rebuild** | blueGate | Still on pre-G72 binaries. Needs depot pull (MeshRelay songBird + G72-trimmed now available). | blueGate G72 + gossip parity |
| **sporeGate depot re-rebuild** | sporeGate ops | Depot needs songBird with MeshRelay. Last rebuild was pre-MeshRelay. | blueGate + fleet parity |

### Active Bugs

| Item | Owner | Detail |
|------|-------|--------|
| **biomeOS category shadow** | biomeOS (eastGate) | Category registration shadows TOML translations — braid.verify/braid.list not routable via Neural API. Direct socket calls work (0.4ms). |
| **swarmVine Windows port** | swarmVine | 5 UDS call sites need TCP fallback for Windows. Source fix pattern in CONVENTIONS.md. |
| ~~**nestGate content.exists**~~ | nestGate (westGate) | **FIXED** — S149: `StorageState` reads `NESTGATE_FAMILY_ID` from env. Dispatch errors classified (Validation→-32602, Security→-32604). http_provider abstraction added. |
| ~~**bearDog binary growth**~~ | bearDog (southGate confirms) | **-25%** in Tier 2 binary (bloat fixed). southGate canary validates. |

### Evolution (code teams, next waves)

| Item | Owner | Status |
|------|-------|--------|
| **G72 Tier 2: HTTP consolidation** | ~~nestGate~~, loamSpine | nestGate S149 http_provider **SHIPPED** (capability-discovery + ureq fallback). loamSpine remaining. |
| **G72 Tier 2: YAML unification** | fleet-wide | Remaining Tier 2 item. |
| **sourDough systemd template** | sourDough (graftGate) | No service template. |
| **Atomic compositions** | primalSpring, biomeOS | Multi-composition orchestration, biome.yaml graph executor, deploy→gossip→verify lifecycle. |
| **NUCLEUS inner membrane** | all NUCLEUS gates | Full inner membrane testing — all IPC via Tower Atomic mesh. Validate capability.call fleet-wide. |
| **NanoWire cleanup** | fleet-wide (gradual) | Purge SSH-based patterns. Tower Atomic replaces SSH. Enables LAN/WAN/mobile deployment configs. |

### Hardware (glacial)

| Item | Status |
|------|--------|
| **piGate** (Raspberry Pi 500/500+) | PLANNED. `aarch64-unknown-linux-gnu`. $180-190. Classroom/conference NUCLEUS. |
| **riscGate** (Milk-V Jupiter 2) | ON ORDER. `riscv64gc-unknown-linux-gnu`. Third ISA. 60 TOPS NPU. 10GbE SFP+. |
| iosGate (iPhone XS) | After graftGate + Apple Dev Program |
| steamGate (Steam Deck) | Future platform gate |
| cloudGate (Oracle Ampere) | WAN enrollment proof |
| arXiv 41/42 campaign | IN PROGRESS. pseudoSpore pipeline shipped. 32⁴ validated. |
| `native_braid.py` → Rust | Last major jelly string (1,259 LOC) |
| PrecisionBrain routing | barraCuda Fp64→F16 silicon-aware dispatch |
| PTX SM120 / Blackwell | coralReef next-gen NVIDIA target |

---

## COMPLETED THIS WAVE (157i)

### G72 Dependency Pandemic — TIER 1: 11/11 DONE (~155+ crates shed)

All 11 teams swept. southGate canary: **+12.2%** (19.7K conn/s). Process leak **FIXED** (RAII ChildGuard, 0 orphans/hr). See `fossilRecord/wave157i_g72_pandemic/` for per-gate AARs.

### G72 Tier 2 — PARTIALLY DONE

- ~~axum 0.7→0.8~~: petalTongue `4d46f3e3` (+ hardcoding elimination)
- ~~wgpu 22→28~~: toadStool `e172eb0c3` (S380, + akida fail-safe tests, 8,446/0)
- ~~darwin fixes~~: ALL 4 MERGED — bearDog `24dd74d`, toadStool `e172eb0c3`, squirrel config.toml, petalTongue `4d46f3e3`

### barraCuda HMC Correctness — LANDED

Multi-pass reduction bug: ΔH 73000 → **0.97**, 82% acceptance. WG128 shaders for 32⁴. Omelyan 2MN symplectic correctness. precision_eval module.

### graftGate — G12 COMPLETE, FULLY ENMESHED

M4 Mac Mini. WireGuard LIVE at `10.13.37.13`, 6 mesh peers, 38ms RTT. 15/15 primals compiled (~98.1M Mach-O arm64). All 4 darwin fixes merged upstream. **sporeGate Phase 1 COMPLETE**: Forgejo user created + SSH key registered + org access granted + golgiBody SSH authorized + darwin depot dir created + sporePrint access granted. Depot push of darwin binaries remaining (graftGate action).

### sporeGate Ops — Phase 1 COMPLETE

- Depot rebuilt: **37 binaries across 4 architectures** synced to golgiBody (BLAKE3 verified)
- graftGate fully enmeshed (all 10 tasks done — see AAR)
- Sub-mesh topology evolved: foreman/workhorse/dev/CAS/platform-builders
- sporeGate demoted from `build_authority` to `foreman` — orchestrates, doesn't build
- ironGate promoted to primary workhorse (Linux musl+gnu, GPU, HPC)
- Jelly string excision: 5 repos cleaned (cellMembrane, plasmidBin, wateringHole, primalSpring, petalTongue)
- piGate mobility fix (`"portable"` → manifest parse error fixed)

### Gossip — 9/16 PRIMALS LIVE, 5-gate mesh

| Primal | Events | Primal | Events |
|--------|--------|--------|--------|
| rhizoCrypt | 3 DAG lifecycle | barraCuda | **22/22 full spec** |
| loamSpine | 4 spine events | esotericWebb | 2 session lifecycle |
| lithoSpore | 4 validation events | songBird | 1 capability advertise |
| wetSpring | **4/4** | nestGate | 6 event types, 11 CAS sites |
| **hotSpring** | **10/10 COMPLETE** | | |

5-gate mesh active: eastGate (662 ingested), sporeGate (660+), westGate (4 peers), ironGate (2 peers, 2ms dispatch), strandGate (1 peer). **southGate LAN-validated** (9 mesh peers, 4 gossip peers, 39 entries). blueGate awaiting depot pull.

### Provenance

braid.verify **99/100 deployed** (0.3ms). E2E chain **8/8** (12ms). content.stat operational. P2 braid.verify **CLOSED**.

### Gate Cascade — ALL REPORTED

| Gate | Key Result |
|------|------------|
| westGate | 42/42 repos. braid.verify 99/100. E2E 8/8. tideGlass absorbed. |
| southGate | **LAN GOSSIP VALIDATED** (Wave 157j). 5 mesh + 4 gossip peers. Enmeshment **11/11**. Previous "topology blocked" corrected — stale WG addresses. |
| ironGate | 2ms dispatch (8x). 2 gossip peers. 166 capabilities. Vine-bat operational. |
| blueGate | G72 source absorbed. Depot pre-rebuild. TCP 7800 2/7 open. |
| graftGate | 15/15 compiled. WG LIVE. 4 darwin fixes. ~98.1M ready for depot. |

### Hardware Deployment Profile — FILED

5-tier model (Systems/Mobile/Accelerators/Edge/Exotic). 4 ISAs. piGate + riscGate entries in `ecosystem_manifest.toml`. Full matrix in `ORTHOGONAL_DIMENSIONS_REVIEW.md`.

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| Primals | **16** |
| NUCLEUS gates | **6/6** (5/6 G72-deployed, blueGate awaiting local rebuild or depot pull) |
| P0 / P1 / P2 | **0 / 0 / 1** (P2: petalTongue port) |
| Gossip injection | **9/16 primals LIVE** (hotSpring 10/10 joined). barraCuda 22/22. |
| Cross-gate gossip | **5-gate mesh + southGate LAN VALIDATED** (4 gossip peers, 39 entries). blueGate awaiting depot. Stale peer registry is the real blocker, not topology. |
| Provenance | braid.verify 99/100 (0.3ms). E2E 8/8 (12ms). |
| Performance | ironGate 2ms dispatch. southGate 19.7K conn/s. Process leak 0/hr. |
| graftGate | 15/15 compiled. WG LIVE. Fully enmeshed. **Depot pushed** (104M, BLAKE3). iOS cross-compile live. |
| WASM | 38/48 (79%) |
| Tests | ~150K+ |

---

## GATE × TEAM MATRIX

| Gate | Code Teams |
|------|------------|
| eastGate | primalSpring, biomeOS, squirrel, songBird, overwatch |
| ironGate | toadStool, barraCuda, coralReef, petalTongue, esotericWebb, footPrint |
| westGate | rhizoCrypt, loamSpine, sweetGrass, nestGate, tideGlass, wetSpring |
| strandGate | hotSpring batch only |
| sporeGate | cellMembrane ops only |
| biomeGate | Node Atomic cross-vendor GPU |
| graftGate | Apple/darwin builds, iosGate prep, sourDough |

## CONVERGENCE RULE

> **Forgejo is canonical. Gates pull, validate, report.**
> 1. Gate teams pull and redeploy.
> 2. Code teams fix their own primals (K-NOME Blurb 1 + 2).
> 3. Overwatch coordinates via this ecosystem blurb (Tier 3).

---

*Wave 157j — southGate LAN GOSSIP VALIDATED. Previous "topology blocked" was wrong — stale WG-era peer addresses, not network isolation. 5 mesh + 4 gossip peers on 192.168.4.x/22. graftGate depot pushed (5th OS, 104M), iOS live. songBird MeshRelay SHIPPED. nestGate S149 FIXED. bearDog -25%. hotSpring 10/10. Remaining: peer registry cleanup (stale IPs + node_id), blueGate depot, sporeGate re-rebuild, biomeOS shadow, swarmVine Windows. 0/0/1. 6/6 NUCLEUS. ~150K+ tests.*
