# ecoPrimals Ecosystem Blurb — Wave 124

**Date**: Jun 22, 2026 12:00 EDT | **Wave**: 124 | **From**: eastGate overwatch
**Cascade**: All repos at parity via Forgejo (git.primals.eco:2222)

---

## You Are Here

You are an agent on a gate in the ecoPrimals ecosystem. This is the single source of truth for all teams. Read it fully — it tells you who you are, what the ecosystem is, and what to do next.

The ecosystem is a **sovereign, self-hosted mesh of compute gates** running 13 Rust primals (called NUCLEUS). Gates communicate via WireGuard overlay, build via Sovereign CI on sporeGate, and coordinate via this wateringHole repository.

**Wave 123 delivered massive evolution. The mesh is now intelligent, not just connected.**

---

## What Wave 123 Proved

| Achievement | Evidence |
|-------------|----------|
| **ATT IP Passthrough live** | Public IP on sporeGate (162.226.225.148), double NAT eliminated |
| **IPC audit clean** | No plaintext primal APIs exposed to network. WG overlay is opaque. |
| **BLAKE3 depot verified** | 14/14 musl + 2/2 gnu binaries validated |
| **Quorum Phase 1 live** | golgi cascade-sense.timer: 15-min auto-pull + relay to GitHub |
| **relay.forward shipped** | cellMembrane → songBird mesh relay wired end-to-end |
| **GPU pipeline validated** | BarraCuda LSTM on RTX 5070: f64 native, XOR MLP MSE 1.11e-30 |
| **primalSpring 1017 tests** | 98 scenarios, toadStool S325 (9,127 tests) |
| **cellMembrane 779 tests** | Transport resolver, TCP consolidation, typed RPC errors |
| **sporePrint petalTongue wired** | IPC client operational, render format gap identified |
| **Tower probed** | bearDog auth.public_key live, songBird needs mesh.init, skunkBat methods missing |

---

## Gate Map

| Gate | WG IP | Hardware | NUCLEUS | Role | K-Derm Layer |
|------|-------|----------|---------|------|--------------|
| **golgi** | .1 | DO droplet | 18 svc | WG hub, Forgejo, relay, depot, **cascade timer** | Periplasm |
| **sporeGate** | .2 | Ryzen 5 6600H 27GB | 13/13 | Build authority, Nest, firewall, **public IP** | Peptidoglycan |
| **eastGate** | .5 | i7 64GB | 13/13 | Overwatch, primalSpring (1017), Meta | Cytoplasm |
| **flockGate** | .6 | i9-13900K 62GB (WAN) | 13/13 | Tower, sporePrint (petalTongue wired) | Outer membrane |
| **ironGate** | .7 | i9-12900K + RTX 5070 | 12/12 | Node compute, **GPU validated** | Cytoplasm |

**Deferred**: strandGate, southGate (relay push pending), northGate (Win/5090, hobby), fieldGate (CMOS dead).

---

## NUCLEUS — 13 Primals, 4 Atomics

```
Tower Atomic (trust + transport + defense):
  BearDog     — crypto identity, BTSP auth, TLS, ionic tokens
  Songbird    — mesh routing, STUN/TURN, relay, relay.forward
  SkunkBat    — threat detection, MethodGate enforcement, audit

Node Atomic (compute + fleet + shaders):
  ToadStool   — workload dispatch, fleet management (9,127 tests)
  BarraCuda   — GPU compute, LSTM zero-copy, f64, Vulkan/WGSL (4,624 tests)
  CoralReef   — shader compilation, SPIR-V, WGSL→PTX (27ms)

Nest Atomic (storage + provenance):
  NestGate    — content-addressed storage, federation, BLAKE3
  RhizoCrypt  — DAG sessions, Merkle roots, dehydration
  LoamSpine   — ledger commits, spine management
  SweetGrass  — provenance braids, attribution, anchoring

Meta (orchestration + AI + viz):
  BiomeOS     — composition orchestrator, deploy graphs, Neural API
  Squirrel    — AI dispatch, Ollama backend
  PetalTongue — visualization, web mode, dashboards
```

---

## Sovereign Infrastructure (proven, stable)

| System | Status |
|--------|--------|
| WireGuard mesh (5-node via golgi) | ✅ |
| Sovereign CI (14/14, dual-target musl+gnu) | ✅ |
| ATT IP Passthrough (no more double NAT) | ✅ NEW |
| Quorum Phase 1 (golgi auto-cascade every 15min) | ✅ NEW |
| relay.forward (cellMembrane → songBird mesh relay) | ✅ NEW |
| IPC audit (no plaintext on network) | ✅ NEW |
| BLAKE3 depot (14 musl + 2 gnu verified) | ✅ |
| Network hardening (167k DNS blocklist, DoT, nftables) | ✅ |
| SSH-only auth (PATs revoked) | ✅ |
| Flint 2 WiFi (Hub 2, bridge, ApertureScience) | ✅ |
| Deployment isomorphism Tier 1+2 | ✅ |
| metalForge (hardware topology probes, WiFi drift auto-remediation) | ✅ NEW |

---

## Team Assignments — Wave 124

### sporeGate — Overwatch + cellMembrane

| Task | Priority | Notes |
|------|----------|-------|
| Build gnu depot binaries (`build-local.sh --target all`) | P1 | ironGate needs gnu dir on golgi |
| rsync gnu directory to golgi depot | P1 | Unblocks ironGate dual-target fetch |
| Dark Forest beacon deployment (Phase 4) | P2 | Encrypted discovery on LAN |
| Nest provenance depth (ledger → 5+) | P2 | Continuing |
| strandGate/southGate relay push | P2 | Opportunistic |

### flockGate — Tower Primals

| Task | Priority | Notes |
|------|----------|-------|
| songBird `mesh.init` — initialize mesh with node_id | P1 | Probed as "not initialized" |
| bearDog BTSP cross-gate: exchange keys with other gates | P1 | auth.public_key is live, trust_issuer next |
| skunkBat method wiring (method_gate.status, threat.report) | P1 | Methods don't exist yet in binary |
| sporePrint petalTongue render format alignment | P2 | Entity graph schema mismatch |

### ironGate — Node Primals

| Task | Priority | Notes |
|------|----------|-------|
| toadStool enrollment (enable in NUCLEUS composition) | P1 | Currently excluded, 12/12 |
| coralReef shader.compile.multi (batch compilation) | P1 | Method missing upstream |
| Validate gnu fetch from depot (once sporeGate builds) | P1 | Dir doesn't exist yet |
| sm_120 Blackwell codegen (currently falls back to sm_70) | P2 | |

### eastGate — Meta + Overwatch

| Task | Priority | Notes |
|------|----------|-------|
| GPU compute primalSpring scenarios | P1 | Pipeline validated, scenarios next |
| Update ecosystem_manifest.toml (ironGate gpu_target) | P1 | Per ironGate impulse |
| BiomeOS composition on multi-gate topology | P2 | Deploy graph across WG mesh |
| PetalTongue visualization dashboard | P2 | |

---

## Active Impulses

| Impulse | From | Status |
|---------|------|--------|
| `wave123-flockgate-tower.toml` | eastGate | PARTIALLY COMPLETE (sporePrint done, Tower P1 ongoing) |
| `wave123-irongate-node.toml` | eastGate | PARTIALLY COMPLETE (GPU validated, depot+toadStool pending) |
| `wave123-gpu-pipeline-validation.toml` | ironGate | RESPONSE — validated, upstream actions listed |
| `wave124-divergence-resolution.toml` | eastGate | ACTIVE — multi-writer sync policy |

---

## Strategic Goals

1. **Sovereignty**: ATT passthrough done. DNS registrar cutover next. Then Layer 4 full composition.
2. **Covalent trust**: relay.forward shipped. mesh.init + BTSP key exchange = Phase 2-3.
3. **Transport**: Quorum Phase 1 live. Phase 2 (Songbird mesh.publish) next. Phase 4 (Dark Forest) designed.
4. **GPU**: Pipeline proven. Depot gnu build + toadStool enrollment = full Node atomic.
5. **Hardware**: Flint 2 #2 incoming. MikroTik creds for VLAN 10. Operator-paced.
6. **metalForge**: Hardware topology testing live. 7 probes (WiFi drift, WG mesh, DNS/DHCP, topology sweep). Auto-remediation proven.

---

## Coordination Rules

- **Cascade**: push to Forgejo, golgi auto-relays every 15min (Quorum Phase 1 live!)
- **Impulses**: propose evolutions or report results. File in `impulses/active/`.
- **Handoffs**: long-term AARs. Archived when fossilized.
- **This blurb**: the ONE document. Paste to any IDE, any gate. Complete context.

---

## Operator-Only

| Action | Status |
|--------|--------|
| ~~ATT IP Passthrough~~ | ✅ DONE (Wave 123) |
| Flint 2 #2 install (ordered) | Pending delivery |
| MikroTik CRS310 credential recovery | When convenient |

---

## Code Metrics

| Repo | Tests | Latest |
|------|-------|--------|
| cellMembrane | 788 | pepti decommissioned, typed plasmid errors (11 sigs), hardcode sweep |
| primalSpring | 1,017 | 98 scenarios, toadStool S325, debt sweep |
| biomeOS | 8,351 | v4.31, 88% coverage |
| songBird | 8,929+ | relay.forward handler, mesh capabilities |
| toadStool | 9,127 | S325 sentinel coverage, discovery gate |
| barraCuda | 4,624 | LSTM zero-copy, f64 native, GPU validated |
| sporePrint | 183+ | petalTongue IPC wired |
| metalForge | 7 probes | WiFi drift, topology sweep, WG mesh, DNS/DHCP audit |

---

*Single source of truth. Paste anywhere. Every agent knows the whole ecosystem and their role in it.*
