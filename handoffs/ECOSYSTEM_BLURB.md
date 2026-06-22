# ecoPrimals Ecosystem Blurb — Wave 123

**Date**: Jun 22, 2026 08:05 EDT | **Wave**: 123 | **From**: eastGate overwatch
**Cascade**: All repos at parity via Forgejo (git.primals.eco:2222)

---

## You Are Here

You are an agent on a gate in the ecoPrimals ecosystem. This is the single source of truth for all teams. Read it fully — it tells you who you are, what the ecosystem is, and what to do next.

The ecosystem is a **sovereign, self-hosted mesh of compute gates** running 13 Rust primals (called NUCLEUS). Gates communicate via WireGuard overlay, build via Sovereign CI on sporeGate, and coordinate via this wateringHole repository.

**All infrastructure is proven. What remains is evolution, not repair.**

---

## Gate Map

| Gate | WG IP | Hardware | NUCLEUS | Role | K-Derm Layer |
|------|-------|----------|---------|------|--------------|
| **golgi** | .1 | DO droplet | 18 svc | WG hub, Forgejo, relay, depot | Periplasm (VPS relay) |
| **sporeGate** | .2 | Ryzen 5 6600H 27GB | 13/13 | Build authority, Nest provenance, LAN firewall | Peptidoglycan (structural) |
| **eastGate** | .5 | i7 64GB | 13/13 | Overwatch, primalSpring, Meta primals | Cytoplasm (coordination) |
| **flockGate** | .6 | i9-13900K 62GB (WAN) | 13/13 | Tower primals, sporePrint | Outer membrane (trust boundary) |
| **ironGate** | .7 | i9-12900K + RTX 5070 | 12/12 | Node compute, GPU | Cytoplasm (heavy compute) |

**Deferred**: strandGate, southGate (relay push pending), northGate (Win/5090, hobby), fieldGate (CMOS dead), swiftGate (Omada-side).

---

## NUCLEUS — 13 Primals, 4 Atomics

```
Tower Atomic (trust + transport + defense):
  BearDog     — crypto identity, BTSP auth, TLS, ionic tokens
  Songbird    — mesh routing, STUN/TURN, relay, NAT traversal
  SkunkBat    — threat detection, MethodGate enforcement, audit

Node Atomic (compute + fleet + shaders):
  ToadStool   — workload dispatch, fleet management (9,127 tests)
  BarraCuda   — GPU compute, LSTM, Vulkan/WGSL shaders
  CoralReef   — shader compilation, SPIR-V, FECS stability

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
| Sovereign CI (Forgejo → golgi hook → sporeGate build → rsync depot) | ✅ 14/14 |
| Dual-target depot (musl all + gnu GPU primals) | ✅ BLAKE3 verified |
| SSH-only auth (PATs revoked) | ✅ |
| Network hardening (167k DNS blocklist, DoT, nftables rate-limit) | ✅ |
| ATT BGW320 IP Passthrough (sporeGate = true edge, public IP) | ✅ `162.226.225.148` |
| Flint 2 WiFi (Hub 2, bridge, ApertureScience) | ✅ |
| Quorum Phase 1 (golgi cascade-sense timer, 15min, Forgejo→GitHub relay) | ✅ |
| IPC audit (UDS dominant, no plaintext primal APIs on network) | ✅ |
| TransportEndpoint.mesh_relay graduation (relay.forward in songBird) | ✅ |
| Deployment isomorphism Tier 1+2 (identity + config gen) | ✅ |

---

## Team Assignments

### sporeGate — Overwatch + cellMembrane

**Overwatch** owns: LAN topology, hardware enrollment, build authority, Nest provenance.
**cellMembrane team** owns: membrane-shadow (791 tests), transport layer, deployment tooling.

| Task | Priority | Stream |
|------|----------|--------|
| ~~Transport Envelope Phase 1: audit inter-gate IPC~~ | ~~P1~~ | **DONE** — UDS dominant, no plaintext APIs |
| ~~Quorum Phase 1: systemd timer on golgi~~ | ~~P1~~ | **DONE** — cascade-sense.timer, 15min, Forgejo→GitHub relay |
| ~~TransportEndpoint.mesh_relay graduation~~ | ~~P1~~ | **DONE** — relay.forward handler in songBird |
| ~~Nest provenance depth (ledger height → 4+)~~ | ~~P1~~ | **DONE** — temporal.cascade 15/17 synced |
| ~~BLAKE3 depot verification post dual-target~~ | ~~P1~~ | **DONE** — 14/14 musl PASS + 2 gnu verified |
| ATT passthrough hardening (DNS, WG port 51821) | P1 | Overwatch |
| strandGate/southGate relay push (opportunistic) | P2 | Overwatch |
| Tier 3 isomorphism (gate.migrate, absorb) | P2 | cellMembrane |
| golgi-as-NUCLEUS evolution | P2 | cellMembrane |

**Context**: All 5 sporeGate Overwatch P1s from Wave 123 are complete. ATT passthrough activated — sporeGate is the true WAN edge (`162.226.225.148`). Discovered and worked around BGW320 UDP port mapping bug (WG moved to 51821). DNS hardened with dhclient hook + immutable resolv.conf. cellMembrane's `relay.forward` graduated — songBird now handles `TransportEndpoint::MeshRelay` dispatch end-to-end. golgi cascade-sense timer running (15min interval, Forgejo→GitHub relay verified). See `impulses/active/2026-06-22T07-40_sporeGate__wave121-sovereign-transport-envelope.toml`.

### flockGate — Tower Primals (bearDog, songBird, skunkBat)

No dedicated overwatch — Tower primal agent evolves code directly.

| Task | Priority | Stream |
|------|----------|--------|
| BTSP cross-gate trust: TrustedIssuerRegistry across 5 gates | P1 | bearDog |
| Ed25519 key exchange between gates (auth.trust_issuer) | P1 | bearDog |
| Songbird mesh routing: capabilities_announce + topology-aware | P1 | songBird |
| SkunkBat MethodGate enforcement validation | P1 | skunkBat |
| Transport Envelope Phase 2: songBird relay on golgi-ext | P2 | songBird |
| sporePrint petalTongue backend wiring | P2 | sporePrint |

**Context**: flockGate is the outer membrane — trust boundary facing WAN. Tower atomic is the immune system + transport. bearDog w135 shipped TrustedIssuerRegistry with multi-issuer verify. Songbird has mesh.capabilities_announce (push model). The code exists; deployment across the mesh is the work.

### ironGate — Node Primals (toadStool, barraCuda, coralReef)

No dedicated overwatch — Node primal agent evolves code directly.

| Task | Priority | Stream |
|------|----------|--------|
| BarraCuda LSTM zero-copy inference on RTX 5070 (gnu binary) | P1 | barraCuda |
| CoralReef shader pipelines via sovereign-dispatch IPC | P1 | coralReef |
| ToadStool fleet dispatch coordinating GPU workloads | P1 | toadStool |
| Validate dual-target depot fetch (gnu for GPU, musl for rest) | P1 | all |
| HPC VLAN participant (when VLAN 10 activates) | P2 | infra |

**Context**: ironGate has the only GPU in the mesh (RTX 5070, CUDA 12.8). Dual-target depot is shipped — `primals/x86_64-unknown-linux-gnu/` exists for GPU primals. All `ml.*` methods are behind BTSP MethodGate. Full ML pipeline (train→save→load→infer) delivered Wave 76.

### eastGate — Meta Primals + Overwatch + primalSpring

**Overwatch** owns: cascade, review, blurb maintenance, ecosystem coordination.
**primalSpring team** owns: scenario expansion, cross-gate validation, coordination testing.

| Task | Priority | Stream |
|------|----------|--------|
| Cross-gate capability.call scenarios (eastGate → sporeGate) | P1 | primalSpring |
| BTSP cross-gate verify scenarios (issued here, verified there) | P1 | primalSpring |
| Mesh capability propagation scenarios | P1 | primalSpring |
| primalSpring → 1000+ tests | P1 | primalSpring |
| BiomeOS composition deploy on multi-gate topology | P2 | biomeOS |
| Squirrel AI pipeline (local Ollama + cross-gate barraCuda) | P2 | squirrel |
| PetalTongue ecosystem visualization dashboard | P2 | petalTongue |

**Context**: eastGate is the coordination hub. primalSpring validates that trust (flockGate), compute (ironGate), and provenance (sporeGate) all compose correctly. Cross-gate scenarios are the growth path to 1000+ tests.

---

## Active Impulses

| Impulse | From | Focus |
|---------|------|-------|
| `wave123-covalent-trust.toml` | eastGate overwatch | Full FRAGO: 6 streams, all teams |
| `wave121-sovereign-transport-envelope.toml` | sporeGate overwatch | Physical/digital topology separation |

---

## Strategic Goals (from whitePaper gen4/gen5)

1. **Sovereignty completion** (L3→L4): TLS, DNS registrar cutover, content, CI
2. **Covalent mesh trust** (Phases 2-5): dispatch → security → content → Dark Forest
3. **Transport evolution**: Nanowire → Quorum Phase 1 → Phase 2 → Phase 4 (envelope)
4. **Primal code evolution**: each team evolves their assigned primals autonomously
5. **Hardware expansion**: operator-paced, gates enroll agentically

---

## Coordination Rules

- **Cascade**: push to Forgejo, all gates pull. wateringHole is the shared state.
- **Impulses**: propose evolutions. File in `impulses/active/`, overwatch reviews.
- **Handoffs**: long-term AARs and tracking. Archived when objectives complete.
- **FRAGOs**: per-wave task orders in impulses/active/ (TOML, machine-readable).
- **This blurb**: the ONE document. Paste to any IDE on any gate. Replaces all per-team blurbs.

---

## Operator-Only (user handles, not agentic)

| Action | Unblocks |
|--------|----------|
| Flint 2 #2 install (ordered) | Hub 1 WiFi |
| MikroTik CRS310 credential recovery (5s reset) | HPC VLAN 10 |
| ~~ATT BGW320 IP Passthrough~~ | **DONE** — `162.226.225.148`, WG port 51821 |

---

## Code Metrics

| Repo | Tests | Latest |
|------|-------|--------|
| cellMembrane | 769 | Wire format fix, sovereignty coverage, Quorum P1, TCP transport |
| primalSpring | 998 | toadStool S323, scenario expansion |
| biomeOS | 8,351 | v4.31, 88% coverage |
| songBird | 8,929 | Relay primitives, mesh.capabilities_announce |
| toadStool | 9,127 | S325 kernel sentinel coverage, path consolidation, clone elimination, discovery gate |
| sporePrint | 183+ | Taxonomy audit |

---

*Single source of truth. Paste anywhere. Every agent knows the whole ecosystem and their role in it.*
