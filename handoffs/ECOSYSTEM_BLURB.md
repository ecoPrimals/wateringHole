# ecoPrimals Ecosystem Blurb — Wave 157k

**Date**: Aug 12, 2026 | **Wave**: 157k | **From**: overwatch (gate-agnostic)
**Posture**: **INNER MEMBRANE LIVE.** Nest Atomic 6/6 domains, 139 translations, riboCipher P0 FIXED. nestgate.io Phase 2 LIVE. NanoWire retirement audit: 19 items, 7 tiers. southGate hostname FIXED, gossip 342 entries. swarmVine Windows DONE. Silicon ledger + concurrent routing upstreamed. Remaining: blueGate depot pull, eastGate NUCLEUS restart, songBird --node-id flag.

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
| **blueGate depot pull** | blueGate | Depot 13/13 current (MeshRelay songBird + G72 + biomeOS + Nest Atomic). blueGate needs to pull and redeploy. `.210:7700` timed out from southGate — may not be running. | blueGate G72 + gossip parity |
| **eastGate runtime health** | eastGate | bearDog `trust.evaluate_peer` rejections + swarmVine socket refused + stuck procs killed. Runtime degradation needs NUCLEUS restart + hostname fix (`pop-os` → `eastGate`). | eastGate enmeshment |
| **songBird --node-id flag** | songBird | songBird reports binary name (`songbird`) as node_id, not gate hostname. swarmVine has `--gate-id`, songBird needs equivalent. | Mesh identity |

### Active Bugs

| Item | Owner | Detail |
|------|-------|--------|
| ~~**biomeOS category shadow**~~ | biomeOS (eastGate) | **FIXED** — `08942cc6`: translation socket fallback. Wave 157j AAR: **0/0/0**. |
| ~~**biomeOS riboCipher overwrite**~~ | biomeOS (westGate) | **P0 FIXED** — `1473737d`: 3 paths overwrote TOML `ribocipher=true` with `false`. All sweetGrass attribution methods now route correctly. +2 regression tests. |
| ~~**swarmVine Windows port**~~ | swarmVine | **DONE** — `1759b2a`: 4 UDS call sites → transport abstraction. `e5cfacd`: Unix-only guards. `b2bbb21`: confirmed done. |
| ~~**nestGate content.exists**~~ | nestGate (westGate) | **FIXED** — S149. |
| ~~**bearDog binary growth**~~ | bearDog (southGate confirms) | **-25%** in Tier 2 binary. |
| ~~**southGate hostname**~~ | southGate | **FIXED** — `hostnamectl set-hostname southGate`. swarmVine reports `southGate`. songBird still reports binary name (needs --node-id). |
| **southGate LAN IP discrepancy** | sporeGate topology | TOPOLOGY_MAP says `.149` but actual DHCP is `.148`. Minor — `.149` is a different device per ARP. |

### Evolution (code teams, next waves)

| Item | Owner | Status |
|------|-------|--------|
| **NanoWire retirement** | sporeGate ops | **AUDIT COMPLETE** — 18 files, 19 items, 7 tiers. Central choke: `ssh.rs` (9 functions). Tier 2 (gate.pull/check/info, service.*, plasmid.trigger) blocks cascade autonomy. Shadow validation via `--mesh` flag. See `NANOWIRE_RETIREMENT_CHECKLIST.md`. |
| **Inner membrane enrollment** | sporeGate | **PHASE 2 LIVE.** primal.eco = sealed mesh (songBird dispatch), primals.eco = pull surface, nestgate.io = PETI bridge. dnsmasq LAN entries deployed. cascade.notify gossip wired in swarmVine (`cb58d32`). live.primals.eco 502 **FIXED**. |
| **nestgate.io Phase 3** | westGate-CAS | Phase 2 LIVE (`/depot/`, `/provenance/`). Next: `/cas/{hash}` content retrieval, cross-gate CAS federation via songBird `content.locate`. |
| **Nest Atomic** | westGate-CAS, biomeOS | **6/6 domains LIVE**, 14 primals alive, 139 translations. `nest.health` + `nest.capabilities` endpoints. hotSpring thin-layer pattern absorbed. |
| **native_braid.py → Rust** | westGate-CAS | Last Python in production (1,308 LOC). Target: `membrane content.braid` wrapping biomeOS graph composition. Unblocks 145/s → 16K/s throughput. |
| **Glue deprecation** | westGate | 9 scripts marked — 4 fossilRecord (archived), 5 active (documented replacement paths). |
| **Silicon ledger** | toadStool, barraCuda | toadStool `7f42eeb22`: silicon ledger + idle-aware routing. barraCuda `e4a02b29`: concurrent routing from hotSpring Node-Atomic. |
| **G72 Tier 2 remaining** | loamSpine, fleet | HTTP consolidation (loamSpine). YAML unification. |
| **wetSpring + projectFOUNDATION** | westGate-CAS | Colocated on westGate tower. Local UDS to Nest Atomic. 50.7 TB ZFS, 452 GB CAS, 5,800 objects. 89 PARTIAL datasets need braid pipeline. |

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

## COMPLETED THIS WAVE (157i–157k)

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

5-gate mesh active: eastGate (662 ingested), sporeGate (660+), westGate (4 peers), ironGate (2 peers, 2ms dispatch), strandGate (1 peer). **southGate** (342 ingested, 1,216 sent, 4 gossip peers, bidirectional federation). blueGate awaiting depot pull.

### Provenance

braid.verify **99/100 deployed** (0.3ms). E2E chain **8/8** (12ms). content.stat operational. P2 braid.verify **CLOSED**.

### Gate Cascade — ALL REPORTED

| Gate | Key Result |
|------|------------|
| westGate | **Nest Atomic 6/6 + riboCipher P0 FIXED.** 139 translations, 14 primals. CAS Data Plan filed. 9 glue scripts deprecated. |
| southGate | **Hostname FIXED + gossip ACTIVE.** 342 ingested, 1,216 sent, bidirectional federation. 11/11. |
| ironGate | 2ms dispatch (8x). 2 gossip peers. 166 capabilities. |
| blueGate | G72 source absorbed. Depot pre-rebuild. `.210:7700` timed out from southGate. |
| graftGate | 15/15 compiled. WG LIVE. Depot pushed (104M, BLAKE3). iOS live. |
| sporeGate | **Inner Membrane (157k).** NanoWire audit. cascade.notify gossip. nestgate.io Phase 2. live.primals.eco FIXED. |

### cellMembrane — Sovereign Defense Wired

fail2ban incident (sporeGate banned during cascade push) → new `sovereign_defense` module in cellmembrane-types. Mesh-aware whitelist derivation, `SystemdActive` health checks, `SovereignDefense` + `SourceForge` service capabilities. golgiBody jail.local deployed (mesh whitelist 10.13.37.0/24 + WAN NAT, maxretry 3→5). 1,328 tests. (`5c628f6`)

### biomeOS — Nest Atomic + riboCipher P0 Fix

- deploy→gossip→verify pipeline wired (`ce812818`). Category shadow FIXED (`08942cc6`).
- **Nest Atomic Neural API** (`1473737d`): 6-domain health probes, 139 translations, `nest.health` + `nest.capabilities` endpoints.
- **riboCipher P0 FIX**: 3 independent paths (`load_from_config`, `primal.announce`, graph loader) overwrote TOML `ribocipher=true` → `false`. All sweetGrass attribution methods now route through `[0xEC, 0x01]` framing. +2 regression tests.

### westGate — Nest Atomic AAR + CAS Data Plan

riboCipher transport fix + Nest Atomic composition. 6/6 domains healthy, 14 primals alive. 9 glue scripts deprecated with Rust/Neural API replacement paths. CAS Data Plan filed for wetSpring + projectFOUNDATION + nestgate.io PETI. 50.7 TB ZFS, 452 GB CAS.

### sporeGate — Inner Membrane Enrollment (Wave 157k)

- live.primals.eco 502 FIXED (Caddy port mismatch).
- cascade.notify gossip domain types in swarmVine (`cb58d32`).
- nestgate.io Phase 2 deployed (`947183a7`, `7ffb7a21`): /depot/ (4 arch, 54 binaries, 594MB) + /provenance/ (BLAKE3 prefix-match).
- NanoWire retirement audit: 18 files, 19 items, 7 priority tiers.
- dnsmasq LAN entries for inner membrane (6 gates at 192.168.4.x).
- Service unit drift fixed (stale binary, wrong port, missing env).

### southGate — Hostname Fixed (Wave 157j-b)

`pop-os` → `southGate` via hostnamectl. Mesh reconnected: 4 LAN peers live, bidirectional federation forming. Gossip: 342 ingested, 1,216 sent. swarmVine correctly reports `southGate`. songBird still reports binary name (needs `--node-id` flag). LAN IP discrepancy: TOPOLOGY_MAP says `.149`, actual DHCP is `.148`.

### swarmVine — Windows Port DONE + Cascade Types

Windows UDS→TCP done (`1759b2a`, `e5cfacd`, `b2bbb21`). + cascade domain types (`cb58d32`): `CascadeNotification`, `CascadeResult`, `DepotFreshness`. 141 tests.

### Silicon — Node-Atomic Concurrent Routing

- toadStool `7f42eeb22`: silicon ledger + idle-aware routing (Node-Atomic AAR)
- barraCuda `e4a02b29`: concurrent routing upstreamed from hotSpring
- hotSpring `807c5392`: fossilize gpu_hmc/ — production concurrent moves to upstream

### Hardware Deployment Profile — FILED

5-tier model (Systems/Mobile/Accelerators/Edge/Exotic). 4 ISAs. piGate + riscGate entries in `ecosystem_manifest.toml`. Full matrix in `ORTHOGONAL_DIMENSIONS_REVIEW.md`.

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| Primals | **16** |
| NUCLEUS gates | **6/6** (5/6 G72-deployed, blueGate awaiting local rebuild or depot pull) |
| P0 / P1 / P2 | **0 / 0 / 0** |
| Gossip injection | **9/16 primals LIVE** (hotSpring 10/10 joined). barraCuda 22/22. |
| Cross-gate gossip | **6-gate mesh** (southGate fully active: 342 ingested, bidirectional federation). Peer registry FIXED. cascade.notify gossip types wired. blueGate awaiting depot. |
| Provenance | braid.verify 99/100 (0.3ms). E2E 8/8 (12ms). |
| Performance | ironGate 2ms dispatch. southGate 18.3K conn/s. Process leak 0/hr. |
| Nest Atomic | **6/6 domains, 139 translations, 14 primals alive.** riboCipher FIXED. nestgate.io Phase 2 LIVE. |
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

*Wave 157k — INNER MEMBRANE LIVE. Nest Atomic 6/6 domains, 139 translations, riboCipher P0 FIXED (1473737d). nestgate.io Phase 2 deployed (/depot/ + /provenance/). NanoWire retirement audit: 19 items, 7 tiers. southGate hostname FIXED, gossip 342/1216 (bidirectional federation forming). swarmVine Windows DONE + cascade.notify gossip types. live.primals.eco 502 FIXED. Silicon: toadStool ledger + barraCuda concurrent routing + hotSpring fossilize. 9 glue scripts deprecated. Remaining: blueGate depot pull, eastGate NUCLEUS restart, songBird --node-id flag. 0/0/0. 6/6 NUCLEUS. ~150K+ tests.*
