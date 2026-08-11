# ecoPrimals Ecosystem Blurb — Wave 157i

**Date**: Aug 11, 2026 | **Wave**: 157i | **From**: overwatch (gate-agnostic)
**Posture**: **POST-PANDEMIC CASCADE COMPLETE.** All gates reported. Code teams delivering. Reshaping to remaining work.

---

## REMAINING WORK — PRIORITIZED

### Critical Path (blocks enmeshment)

| Item | Owner | Detail | Blocker For |
|------|-------|--------|-------------|
| ~~**songBird MeshRelay**~~ | songBird code team | **SHIPPED.** relay + spread (`0dc82bc`) + subscribe (`9351230`) — full surface: relay/inject/spread/subscribe. Topic-based pub-sub with local delivery. | ~~blueGate + southGate~~ **UNBLOCKED** |
| **graftGate depot push** | graftGate | 15 darwin binaries (~98.1M) → `aarch64-apple-darwin/` on golgiBody. Dir created, SSH authorized. | 5th OS family in depot |
| **blueGate local depot rebuild** | blueGate | G72 source absorbed but still running pre-G72 binaries. Needs local `cargo build` or depot pull after sporeGate rebuild. | blueGate G72 parity |

### Active Bugs

| Item | Owner | Detail |
|------|-------|--------|
| **biomeOS category shadow** | biomeOS (eastGate) | Category registration shadows explicit TOML translations — braid.verify/braid.list not routable via Neural API. capability.call tries category match first, fails, never falls through. Direct socket calls work (0.4ms). |
| **bearDog binary growth** | bearDog (westGate) | +2.9MB despite 41-dep removal. Debug symbols or static linking change. Investigate. |
| **swarmVine Windows port** | swarmVine | 5 UDS call sites need `#[cfg(unix)]` + TCP fallback for Windows. Source fix pattern exists (CONVENTIONS.md). |
| **nestGate content.exists** | nestGate (westGate) | Returns "Internal error" via biomeOS Neural API. Direct calls work. |

### Evolution (code teams, next waves)

| Item | Owner | Status |
|------|-------|--------|
| **G72 Tier 2: HTTP consolidation** | nestGate, loamSpine | ureq → songBird/capability.call. Not started. |
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

5-gate mesh active: eastGate (662 ingested), sporeGate (660+), westGate (4 peers), ironGate (2 peers, 2ms dispatch), strandGate (1 peer). southGate + blueGate operational locally, blocked on MeshRelay/depot.

### Provenance

braid.verify **99/100 deployed** (0.3ms). E2E chain **8/8** (12ms). content.stat operational. P2 braid.verify **CLOSED**.

### Gate Cascade — ALL REPORTED

| Gate | Key Result |
|------|------------|
| westGate | 42/42 repos. braid.verify 99/100. E2E 8/8. tideGlass absorbed. |
| southGate | Canary +12.2%. Process leak FIXED. swarmVine operational. Readiness 8/11. |
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
| Cross-gate gossip | **5-gate mesh ACTIVE**. southGate + blueGate local-only. |
| Provenance | braid.verify 99/100 (0.3ms). E2E 8/8 (12ms). |
| Performance | ironGate 2ms dispatch. southGate 19.7K conn/s. Process leak 0/hr. |
| graftGate | 15/15 compiled. WG LIVE. Fully enmeshed (Forgejo + SSH + org). Depot push remaining. |
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

*Wave 157i — POST-PANDEMIC CASCADE COMPLETE. G72 11/11. Gossip 9/16. 5-gate mesh. graftGate 15/15, fully enmeshed. sporeGate ops complete: depot rebuilt (37 binaries, 4 archs), sub-mesh topology evolved. songBird MeshRelay SHIPPED (relay/inject/spread/subscribe) — blueGate + southGate UNBLOCKED. Remaining: graftGate depot push, blueGate rebuild, biomeOS shadow, bearDog growth, swarmVine Windows. 0/0/1. 6/6 NUCLEUS. ~150K+ tests.*
