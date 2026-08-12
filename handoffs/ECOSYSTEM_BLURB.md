# ecoPrimals Ecosystem Blurb — Wave 157k

**Date**: Aug 12, 2026 | **Wave**: 157k | **From**: overwatch (gate-agnostic)
**Posture**: **INNER MEMBRANE LIVE.** Three-domain topology operational. Nest Atomic 6/6 domains. riboCipher P0 FIXED. nestgate.io Phase 2 LIVE. 6-gate gossip mesh. 12 gates ONLINE. 182 AARs/handoffs fossilized. **0/0/0.**

---

## REMAINING WORK — PRIORITIZED

### Operational (blocks next wave)

| Item | Owner | Detail | Blocker For |
|------|-------|--------|-------------|
| **blueGate depot pull** | blueGate | Depot 13/13 current (MeshRelay songBird + G72 + biomeOS + Nest Atomic). blueGate needs to pull and redeploy. `.210:7700` timed out from southGate — may not be running. | blueGate G72 + gossip parity |
| **eastGate runtime health** | eastGate | bearDog `trust.evaluate_peer` rejections + swarmVine socket refused + stuck procs killed. Runtime degradation needs NUCLEUS restart + hostname fix (`pop-os` → `eastGate`). | eastGate enmeshment |
| **songBird --node-id flag** | songBird | songBird reports binary name (`songbird`) as node_id, not gate hostname. swarmVine has `--gate-id`, songBird needs equivalent. | Mesh identity |
| **southGate LAN IP discrepancy** | sporeGate topology | TOPOLOGY_MAP says `.149` but actual DHCP is `.148`. Minor — `.149` is a different device per ARP. | Topology accuracy |

### Evolution (code teams, next waves)

| Item | Owner | Status |
|------|-------|--------|
| **NanoWire retirement** | sporeGate ops | **AUDIT COMPLETE** — 18 files, 19 items, 7 tiers. Central choke: `ssh.rs` (9 functions). Tier 2 (gate.pull/check/info, service.*, plasmid.trigger) blocks cascade autonomy. Shadow validation via `--mesh` flag. See `NANOWIRE_RETIREMENT_CHECKLIST.md`. |
| **nestgate.io Phase 3** | westGate-CAS | Phase 2 LIVE (`/depot/`, `/provenance/`). Next: `/cas/{hash}` content retrieval, cross-gate CAS federation via songBird `content.locate`. |
| **native_braid.py → Rust** | westGate-CAS | Last Python in production (1,308 LOC). Target: `membrane content.braid` wrapping biomeOS graph composition. Unblocks 145/s → 16K/s throughput. |
| **G72 Tier 2 remaining** | loamSpine, fleet | HTTP consolidation (loamSpine). YAML unification. |
| **Glue deprecation** | westGate | 9 scripts marked — 4 fossilRecord (archived), 5 active (documented replacement paths). |
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
| PrecisionBrain routing | barraCuda Fp64→F16 silicon-aware dispatch |
| PTX SM120 / Blackwell | coralReef next-gen NVIDIA target |

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| Primals | **16** |
| NUCLEUS gates | **6/6** (5/6 G72-deployed, blueGate awaiting depot pull) |
| Gates ONLINE | **12** (6 NUCLEUS + graftGate enmeshed + 1 crankshaft + 4 other) |
| P0 / P1 / P2 | **0 / 0 / 0** |
| Gossip injection | **9/16 primals LIVE** (hotSpring 10/10, barraCuda 22/22, wetSpring 4/4, nestGate 11 CAS sites) |
| Cross-gate gossip | **6-gate mesh** (southGate: 342 ingested, bidirectional federation). cascade.notify gossip types wired. blueGate awaiting depot. |
| Provenance | braid.verify 99/100 (0.3ms). E2E 8/8 (12ms). |
| Performance | ironGate 2ms dispatch. southGate 18.3K conn/s. Process leak 0/hr. |
| Nest Atomic | **6/6 domains, 139 translations, 14 primals alive.** riboCipher FIXED. nestgate.io Phase 2 LIVE. |
| Inner membrane | **THREE-DOMAIN LIVE.** primals.eco (pull), primal.eco (mesh), nestgate.io (PETI). dnsmasq LAN entries deployed. |
| graftGate | 15/15 compiled. WG LIVE. Fully enmeshed. Depot pushed (104M, BLAKE3). iOS cross-compile live. |
| Silicon | toadStool silicon ledger + idle-aware routing. barraCuda concurrent routing upstreamed. hotSpring gpu_hmc fossilized. |
| WASM | 38/48 (79%) |
| Tests | ~157K+ |
| Fossilized | **333+ files** across 22 checkpoints (1,750+ records). 182 fossilized this wave. |

---

## WAVE 157k COMPLETED WORK

### Inner Membrane Enrollment — sporeGate

- live.primals.eco 502 FIXED (Caddy port mismatch).
- cascade.notify gossip domain types in swarmVine (`cb58d32`).
- nestgate.io Phase 2 deployed (`947183a7`, `7ffb7a21`): /depot/ (4 arch, 54 binaries, 594MB) + /provenance/ (BLAKE3 prefix-match).
- NanoWire retirement audit: 18 files, 19 items, 7 priority tiers.
- dnsmasq LAN entries for inner membrane (6 gates at 192.168.4.x).
- Service unit drift fixed (stale binary, wrong port, missing env).

### Nest Atomic + riboCipher P0 Fix — biomeOS / westGate

- deploy→gossip→verify pipeline wired (`ce812818`). Category shadow FIXED (`08942cc6`).
- **Nest Atomic Neural API** (`1473737d`): 6-domain health probes, 139 translations, `nest.health` + `nest.capabilities` endpoints.
- **riboCipher P0 FIX**: 3 independent paths (`load_from_config`, `primal.announce`, graph loader) overwrote TOML `ribocipher=true` → `false`. +2 regression tests.
- westGate: 9 glue scripts deprecated with Rust/Neural API replacement paths. CAS Data Plan filed.

### graftGate — G12 COMPLETE, FULLY ENMESHED

M4 Mac Mini. WireGuard LIVE at `10.13.37.13`, 6 mesh peers, 38ms RTT. 15/15 primals compiled (~98.1M Mach-O arm64). All 4 darwin fixes merged upstream. Depot push of darwin binaries DONE (104M, BLAKE3). iOS cross-compile live. 5th OS family in depot.

### southGate — Hostname Fixed + LAN Gossip Validated

`pop-os` → `southGate` via hostnamectl. 342 gossip entries ingested, 1,216 sent, 4 LAN peers, bidirectional federation. songBird reports binary name (needs `--node-id` flag).

### swarmVine — Windows Port DONE + Cascade Types

Windows UDS→TCP done (`1759b2a`, `e5cfacd`, `b2bbb21`). + cascade domain types (`cb58d32`): `CascadeNotification`, `CascadeResult`, `DepotFreshness`. 141 tests.

### Silicon — Node-Atomic Concurrent Routing

- toadStool `7f42eeb22`: silicon ledger + idle-aware routing
- barraCuda `e4a02b29`: concurrent routing upstreamed from hotSpring
- hotSpring `807c5392`: fossilize gpu_hmc/ — production compute moves upstream

### cellMembrane — Sovereign Defense Wired

fail2ban mesh-aware whitelist derivation, `SystemdActive` health checks, `SovereignDefense` + `SourceForge` service capabilities. golgiBody jail.local deployed. 1,328 tests. (`5c628f6`)

### sporeGate Ops — Depot Rebuilt + Peer Registry FIXED

Peer registry root cause CLOSED — LAN IPs added to cellMembrane `MESH_REGISTRY` (`b84bed6`) and wateringHole `TOPOLOGY_MAP.toml` (`42834e5e1`). Depot rebuilt to 13/13 current (57 total, 4 arch). songBird depot confirmed MeshRelay-enabled.

### G72 Dependency Pandemic — Tier 1: 11/11 DONE

All 11 teams swept (~155+ crates shed). Tier 2 partially done (axum 0.8, wgpu 28, 4 darwin fixes). See `fossilRecord/wave157i_g72_pandemic/`.

### Fossilization — 182 Files Archived

AARs and handoffs from waves 155n–157i archived to 8 fossilRecord directories. Active surface: 3 AARs + 15 handoffs (157j–157k only).

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

*Wave 157k — INNER MEMBRANE LIVE. Three-domain topology operational. Nest Atomic 6/6 domains, 139 translations, riboCipher P0 FIXED. nestgate.io Phase 2 LIVE. NanoWire retirement audit: 19 items, 7 tiers. graftGate FULLY ENMESHED (15/15, depot pushed). southGate LAN gossip VALIDATED (342/1,216, bidirectional). swarmVine Windows DONE + cascade.notify. Silicon: toadStool ledger + barraCuda concurrent + hotSpring fossilize. cellMembrane sovereign defense. 6-gate gossip mesh. 9/16 primals. 182 files fossilized. Remaining: blueGate depot pull, eastGate NUCLEUS restart, songBird --node-id. 0/0/0. 12 gates. ~157K+ tests.*
