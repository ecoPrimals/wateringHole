# ecoPrimals Ecosystem Blurb — Wave 157j

**Date**: Aug 11, 2026 | **Wave**: 157j | **From**: overwatch (gate-agnostic)
**Posture**: **PEER REGISTRY FIXED + DEPOT CURRENT.** sporeGate closed the stale-IP root cause (cellMembrane + topology). Depot 13/13. biomeOS shadow FIXED. Remaining: blueGate depot pull, eastGate NUCLEUS restart, hostname fix, swarmVine Windows.

---

## REMAINING WORK — PRIORITIZED

### Critical Path (blocks enmeshment)

| Item | Owner | Detail | Blocker For |
|------|-------|--------|-------------|
| ~~songBird MeshRelay~~ | songBird | **SHIPPED.** relay/inject/spread/subscribe. | ~~blueGate + southGate~~ **UNBLOCKED** |
| ~~graftGate depot push~~ | graftGate | **DONE.** 15 darwin binaries pushed (104M, BLAKE3). 5th OS family in depot. iOS cross-compile live. | **RESOLVED** |
| ~~southGate MeshRelay~~ | southGate | **LIVE + LAN GOSSIP VALIDATED.** 5 songBird mesh peers, 4 swarmVine gossip peers on 192.168.4.x/22. Previous "topology blocked" was **wrong** — stale WG-era peer addresses, not network isolation. | **RESOLVED** |
| ~~**Peer registry cleanup**~~ | sporeGate topology | **DONE.** cellMembrane `b84bed6` adds LAN IPs to `MESH_REGISTRY` (6 gates verified via ip addr/ARP/ping). wateringHole `42834e5e1` adds `lan_ip` to `TOPOLOGY_MAP.toml` songbird_covalent peers. 264 tests pass. | **RESOLVED** |
| ~~**sporeGate depot re-rebuild**~~ | sporeGate ops | **DONE.** 13/13 current, 0 stale. songBird depot binary confirmed to contain MeshRelay. biomeOS rebuilt to `650ac475`. 57 total binaries, 4 architectures. Sandbox perm fix applied. | **RESOLVED** |
| **blueGate depot pull** | blueGate | Depot now fully current (MeshRelay songBird + G72 + biomeOS fix). blueGate needs to pull and redeploy. | blueGate G72 + gossip parity |
| **eastGate runtime health** | eastGate | bearDog `trust.evaluate_peer` rejections + swarmVine socket refused + 8 stuck test procs (killed). **Not an API gap** — bearDog implements the method; songBird routes via capability discovery (`SecurityAdapter::from_discovery`). Runtime degradation needs NUCLEUS restart. | eastGate enmeshment |
| **hostname mismatch** | eastGate, southGate | Both report `pop-os` as node_id. Fix: set hostname or songBird `--node-id` flag. | Mesh identity |

### Active Bugs

| Item | Owner | Detail |
|------|-------|--------|
| ~~**biomeOS category shadow**~~ | biomeOS (eastGate) | **FIXED** — `08942cc6`: translation socket fallback for capability.call. dispatch_with_translation constructs endpoint from translation's own socket path when category discovery fails. +2 regression tests (1,602 total). Wave 157j AAR: **0/0/0**. |
| **swarmVine Windows port** | swarmVine | 5 UDS call sites need TCP fallback for Windows. Source fix pattern in CONVENTIONS.md. |
| ~~**nestGate content.exists**~~ | nestGate (westGate) | **FIXED** — S149: `StorageState` reads `NESTGATE_FAMILY_ID` from env. Dispatch errors classified (Validation→-32602, Security→-32604). http_provider abstraction added. |
| ~~**bearDog binary growth**~~ | bearDog (southGate confirms) | **-25%** in Tier 2 binary (bloat fixed). southGate canary validates. |
| **eastGate runtime health** | eastGate | bearDog `trust.evaluate_peer` rejections, swarmVine socket not accepting, 8 stuck test procs killed. Not an API gap — bearDog implements the method and songBird routes via capability discovery. Likely socket/process degradation. Needs NUCLEUS restart + hostname fix (`pop-os` → `eastGate`). |
| **southGate hostname** | southGate | Also reports `pop-os`. Node_id mismatch in songBird mesh. |

### Evolution (code teams, next waves)

| Item | Owner | Status |
|------|-------|--------|
| **G72 Tier 2: HTTP consolidation** | ~~nestGate~~, loamSpine | nestGate S149 http_provider **SHIPPED** (capability-discovery + ureq fallback). loamSpine remaining. |
| **G72 Tier 2: YAML unification** | fleet-wide | Remaining Tier 2 item. |
| **sourDough systemd template** | sourDough (graftGate) | No service template. |
| **Atomic compositions** | primalSpring, biomeOS | biomeOS deploy→gossip→verify **WIRED** (`ce812818`). Multi-composition orchestration + biome.yaml graph executor remaining. |
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

Multi-pass reduction bug: ΔH 73000 → **0.97**, 82% acceptance. WG128 shaders for 32⁴. Omelyan 2MN symplectic correctness. precision_eval module. **+ InitParams struct alignment** (`49fe5abb`): Rust `#[repr(C)]` padding misaligned epsilon at byte 16 vs WGSL offset 8 — shader was reading zeros, hot_start produced identity links.

### graftGate — G12 COMPLETE, FULLY ENMESHED

M4 Mac Mini. WireGuard LIVE at `10.13.37.13`, 6 mesh peers, 38ms RTT. 15/15 primals compiled (~98.1M Mach-O arm64). All 4 darwin fixes merged upstream. **sporeGate Phase 1 COMPLETE**: Forgejo user created + SSH key registered + org access granted + golgiBody SSH authorized + darwin depot dir created + sporePrint access granted. Depot push of darwin binaries remaining (graftGate action).

### sporeGate Ops — Phase 1 + Phase 2 COMPLETE

- Phase 1: 37 binaries across 4 architectures synced. graftGate fully enmeshed. Topology evolved.
- **Phase 2 (Wave 157j):** Peer registry root cause CLOSED — LAN IPs added to cellMembrane `MESH_REGISTRY` (`b84bed6`) and wateringHole `TOPOLOGY_MAP.toml` (`42834e5e1`). 6 gates verified via ip addr/ARP/ping. Depot rebuilt to **13/13 current** (57 total, 4 arch). songBird depot confirmed MeshRelay-enabled. Sandbox perm fix. eastGate triaged (8 stuck procs killed).
- Jelly string excision: 5 repos cleaned
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

### cellMembrane — Sovereign Defense Wired

fail2ban incident (sporeGate banned during cascade push) → new `sovereign_defense` module in cellmembrane-types. Mesh-aware whitelist derivation, `SystemdActive` health checks, `SovereignDefense` + `SourceForge` service capabilities. golgiBody jail.local deployed (mesh whitelist 10.13.37.0/24 + WAN NAT, maxretry 3→5). 1,328 tests. (`5c628f6`)

### biomeOS — Composition Lifecycle Wired

deploy→gossip→verify pipeline wired into `composition.orchestrate` (`ce812818`). Category shadow **FIXED** (`08942cc6`). Wave 157j AAR: **0/0/0** — no remaining biomeOS bugs.

### Hardware Deployment Profile — FILED

5-tier model (Systems/Mobile/Accelerators/Edge/Exotic). 4 ISAs. piGate + riscGate entries in `ecosystem_manifest.toml`. Full matrix in `ORTHOGONAL_DIMENSIONS_REVIEW.md`.

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| Primals | **16** |
| NUCLEUS gates | **6/6** (5/6 G72-deployed, blueGate awaiting local rebuild or depot pull) |
| P0 / P1 / P2 | **0 / 0 / 1** (P2: swarmVine Windows port) |
| Gossip injection | **9/16 primals LIVE** (hotSpring 10/10 joined). barraCuda 22/22. |
| Cross-gate gossip | **5-gate mesh + southGate LAN VALIDATED** (4 gossip peers, 39 entries). Peer registry **FIXED** (LAN IPs in cytoplasm + topology). blueGate awaiting depot pull. |
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

*Wave 157j — PEER REGISTRY FIXED (cellMembrane b84bed6 + topology 42834e5e1). Depot 13/13 current, MeshRelay confirmed. southGate LAN VALIDATED. biomeOS shadow FIXED (0/0/0). barraCuda struct alignment FIXED. cellMembrane sovereign defense wired. eastGate runtime degraded (trust.evaluate_peer rejections are socket/process issue, not API gap — bearDog implements method, songBird routes via capability discovery). Remaining: blueGate depot pull, eastGate NUCLEUS restart, hostname fix (2 gates), swarmVine Windows. 0/0/1. 6/6 NUCLEUS. ~150K+ tests.*
