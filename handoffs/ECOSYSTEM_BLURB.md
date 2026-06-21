# ecoPrimals Ecosystem — Wave 122+ Evolution Blurb

**Date**: Jun 21, 2026 19:30 EDT | **From**: eastGate overwatch
**State**: STABLE PLATFORM — all gates enrolled, all P1s shipped. Planning next evolution.

---

## Strategic Position

Wave 121 proved the **infrastructure layer is complete**:
- 5-node WG mesh, all gates pushing to Forgejo
- Sovereign CI: 14/14 primals built on sporeGate, dual-target (musl + gnu)
- 744 cellMembrane tests, 998 primalSpring tests
- All 4 compute gates at full NUCLEUS, GPU live on ironGate

The ecosystem is now at the **gen4 → gen5 boundary** (see whitePaper/gen5/):
- gen4 proved primals compose into products (esotericWebb, lithoSpore, helixVision)
- gen5 asks: "does someone else's science come out the other end?"
- The infrastructure we just proved (sovereign CI, mesh, GPU) enables gen5 delivery

**What remains is evolution, not repair.**

---

## The Four Goals (from whitePaper analysis)

### 1. Sovereignty Completion (L3 → L4)

From `PRIMAL_VS_SOVEREIGNTY_GOALS.md`: Layer 3 is ~60% complete. The proven platform accelerates the remaining sovereignty targets:

| Target | Current | Next Step | Owner |
|--------|---------|-----------|-------|
| TLS sovereign | Caddy + LE live | BearDog ACME on :8443 (shadow) | sporeGate cellMembrane |
| NAT sovereign | Songbird TURN live | Formal 7-day gate | sporeGate overwatch |
| DNS sovereign | knot-dns live (ns1+ns2) | Registrar NS cutover | Operator (registrar action) |
| Auth sovereign | S1 complete (ed25519) | BearDog BTSP (S2) | flockGate Tower |
| Content sovereign | sporePrint via Caddy | petalTongue backend wiring | flockGate team |
| Git sovereign | Forgejo primary (38+ repos) | ✅ Complete | — |
| CI sovereign | sporeGate builds | Forgejo Actions (stretch) | sporeGate cellMembrane |
| GPU sovereign | RTX 5070 + dual depot | barraCuda WGSL maturity | ironGate Node |

### 2. Covalent Mesh Trust (from gen5/COVALENT_MESH_TRUST_VALIDATION.md)

The 5-gate mesh is connected but trust is at Phase 1 (discovery). Next phases:

| Phase | What | Status | Wave Target |
|-------|------|--------|-------------|
| 1: Discovery | Gates see each other | ✅ Proven (5 nodes) | — |
| 2: Dispatch | Cross-gate capability.call | Ready (Songbird push model) | 123-124 |
| 3: Security | BTSP cross-gate token validation | bearDog w135 delivered | 123-124 |
| 4: Content | NestGate federation (BLAKE3 end-to-end) | Ready | 125-126 |
| 5: Dark Forest | Invariants enforced across mesh | Implemented | 125-126 |

### 3. Transport Evolution (from gen5/TRANSPORT_EVOLUTION.md)

Currently at **Nanowire** (SSH-triggered). Next:

| Phase | Transport | What Changes |
|-------|-----------|--------------|
| Current | Nanowire | SSH push/pull, manual cascade |
| Next | Quorum Phase 1 | Timer-based `potential.sense` on nodes — autonomous |
| Future | Quorum Phase 2 | Songbird `mesh.publish` carries impulses (sub-second) |
| Horizon | Quorum Phase 3 | Capability-routed, self-integrating |

**Immediate value**: Quorum Phase 1 makes the cascade autonomous — nodes pull without being told.

### 4. Primal Code Evolution (per-team)

| Team | Gate | Focus | Goal |
|------|------|-------|------|
| **Tower** (flockGate) | bearDog, songBird, skunkBat | BTSP trust bootstrap, mesh routing, defense | S2 auth, cross-gate trust |
| **Node** (ironGate) | toadStool, barraCuda, coralReef | GPU compute, fleet dispatch, shaders | LSTM zero-copy, Vulkan, fleet |
| **Nest** (sporeGate) | nestGate, rhizoCrypt, loamSpine, sweetGrass | Provenance depth, federation, content | Ledger depth, BLAKE3 federation |
| **Meta** (eastGate) | biomeOS, squirrel, petalTongue | Orchestration, AI, visualization | primalSpring 1000+, perceptron |

---

## Wave 123-126 Roadmap

### Wave 123: Covalent Trust + Quorum Sensing

| Task | Team | Deliverable |
|------|------|-------------|
| Cross-gate `capability.call` validation | primalSpring (eastGate) | Live test: eastGate → sporeGate → ironGate chain |
| BTSP cross-gate token exchange | flockGate Tower (bearDog) | TrustedIssuerRegistry across 5 nodes |
| `potential.sense` timer on golgi | sporeGate cellMembrane | Autonomous cascade (Quorum Phase 1) |
| primalSpring → 1000 tests | eastGate Meta | Cross-gate scenarios |

### Wave 124: Content Federation + GPU Pipeline

| Task | Team | Deliverable |
|------|------|-------------|
| NestGate federation live test | sporeGate Nest | put on eastGate, pull on sporeGate, BLAKE3 verify |
| BarraCuda LSTM on RTX 5070 | ironGate Node | Zero-copy GPU inference, gnu binary |
| sporePrint petalTongue backend | flockGate team | Content from NestGate, not static files |
| Songbird relay Phase 3.5 | flockGate Tower | Ed25519 signature verification on relay |

### Wave 125: Sovereignty Shadow Graduation

| Task | Team | Deliverable |
|------|------|-------------|
| DNS NS registrar cutover | Operator | Sovereign DNS resolution path |
| S2 auth 7-day gate | sporeGate overwatch + flockGate Tower | BTSP replaces ed25519-only |
| HPC VLAN 10 activation | Operator + sporeGate overwatch | 10G trunk for compute traffic |
| Dark Forest cross-gate validation | primalSpring | Full 5-invariant enforcement |

### Wave 126: Gen5 Readiness

| Task | Team | Deliverable |
|------|------|-------------|
| First external collaborator artifact | helixVision (cross-team) | Gonzales NF data → validated output |
| Quorum Phase 2 (Songbird mesh.publish) | cellMembrane + songBird | Sub-second impulse propagation |
| biomeOS composition orchestration | eastGate Meta | Deploy graph live on multi-gate |
| Layer 4 integration test | All teams | Full request path, zero external deps |

---

## Hardware Expansion (Operator-driven, feeds into above)

| Item | Purpose | Feeds Into |
|------|---------|-----------|
| **Flint 2 #2** (ordered) | Hub 1 or mesh extension | Topology, HPC VLAN |
| MikroTik CRS310 creds | 10G trunk for VLAN 10 | Wave 125 HPC activation |
| ATT BGW320 IP Passthrough | Eliminate double NAT | WG mesh performance |
| Future gates (DDR3 NUCs, etc.) | Expand mesh | Quorum Phase 2+ nodes |

**Enrollment pattern (proven)**: Hardware arrives → operator installs → sporeGate enrolls via SSH/WG → NUCLEUS deploys agentically → gate joins mesh → team assigned.

---

## K-Derm Topology (Current vs Target)

```
CURRENT (Wave 122):
  golgi (.1)         — sole VPS: Forgejo + WG hub + relay + depot
  sporeGate (.2)     — build authority + Nest + overwatch
  eastGate (.5)      — Meta + overwatch + primalSpring
  flockGate (.6)     — Tower + sporePrint (WAN)
  ironGate (.7)      — Node + GPU compute

TARGET (Wave 126+):
  golgi (.1)         — VPS: Forgejo + WG hub + depot + quorum relay
  sporeGate (.2)     — peptidoglycan: builds + Nest + LAN topology + quorum node
  eastGate (.5)      — cytoplasm: Meta + overwatch + coordination
  flockGate (.6)     — outer membrane: Tower (trust boundary) + WAN relay
  ironGate (.7)      — cytoplasm: Node compute (GPU) + HPC VLAN participant
  [new gates]        — cytoplasm: expansion nodes, quorum participants
```

The K-Derm model (from gen5/KDERM_DIDERM_ENVELOPE.md) maps gates to membrane layers:
- **flockGate** = outer membrane (trust boundary, facing WAN)
- **sporeGate** = peptidoglycan (structural, builds, mediates)
- **eastGate/ironGate** = cytoplasm (internal compute, coordination)
- **golgi** = periplasm (VPS relay, content depot)

---

## Debt Register (tracked, not blocking)

| Item | Type | Priority | Notes |
|------|------|----------|-------|
| Registrar NS cutover | Sovereignty | P2 | Manual action when convenient |
| Forgejo Actions CI | Sovereignty | P3 | 74 workflows to port (stretch) |
| grapheneGate aarch64 | Platform | P3 | NDK cross-compile, Pixel 8 |
| fieldGate CMOS | Hardware | P4 | Dead, low priority |
| strandGate/southGate relay | Enrollment | P2 | RustDesk config push |
| Multi-vendor peptidoglycan | Resilience | P4 | Hetzner/Vultr redundancy |

---

## Summary

The ecosystem has crossed from **infrastructure proving** to **capability evolution**. Every wave from here advances the gen4→gen5 arc:

1. **Covalent trust** makes the mesh intelligent (not just connected)
2. **Quorum sensing** makes the cascade autonomous (not just triggered)
3. **Sovereignty graduation** removes remaining external deps
4. **Primal evolution** matures the capabilities that products consume
5. **Hardware expansion** grows the mesh physically (operator-paced)

Teams work autonomously. Operator adds hardware as available. Overwatch coordinates via cascade. The system is self-sustaining.

---

*End of ecosystem blurb. Single source of truth for all teams.*
