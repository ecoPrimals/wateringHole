# ecoPrimals Ecosystem Blurb — Wave 126

**Date**: Jun 23, 2026 09:00 EDT | **Wave**: 126 | **From**: eastGate overwatch
**Cascade**: All repos at parity via Forgejo (git.primals.eco:2222) + golgi 15-min auto-relay

---

## You Are Here

You are an agent on a gate in the ecoPrimals ecosystem. This is the single source of truth for all teams. Read it fully — it tells you who you are, what the ecosystem is, and what to do next.

The ecosystem is a **sovereign, self-hosted mesh of compute gates** running 13 Rust primals (called NUCLEUS). Gates communicate via WireGuard overlay, build via Sovereign CI on sporeGate, and coordinate via this wateringHole repository.

**The infrastructure is proven. GPU is validated. Transport is intelligent. What remains is composition maturity.**

---

## Gate Map

| Gate | WG IP | Hardware | NUCLEUS | Role | K-Derm Layer |
|------|-------|----------|---------|------|--------------|
| **golgi** | .1 | DO droplet | 18 svc | WG hub, Forgejo, relay, depot, cascade timer | Periplasm |
| **sporeGate** | .2 | Ryzen 5 6600H 27GB | 13/13 | Build authority, Nest, firewall, public IP | Peptidoglycan |
| **eastGate** | .5 | i7 64GB | 13/13 | Overwatch, primalSpring (1038), Meta | Cytoplasm |
| **flockGate** | .6 | i9-13900K 62GB (WAN) | 13/13 | Tower, sporePrint (petalTongue wired) | Outer membrane |
| **ironGate** | .7 | i9-12900K + RTX 5070 | 12/12 | Node compute, GPU validated (4619 tests) | Cytoplasm |

**Deferred**: strandGate, southGate (relay push pending), northGate (Win/5090), fieldGate (CMOS dead).

---

## NUCLEUS — 13 Primals, 4 Atomics

```
Tower Atomic (trust + transport + defense):
  BearDog     — crypto identity, BTSP auth, TLS, ionic tokens
  Songbird    — mesh routing, STUN/TURN, relay.forward, WG auto-init
  SkunkBat    — threat detection, MethodGate enforcement, audit

Node Atomic (compute + fleet + shaders):
  ToadStool   — workload dispatch, fleet management (9,127 tests)
  BarraCuda   — GPU compute, LSTM zero-copy, f64, quota-aware OOM (4,619 tests)
  CoralReef   — shader.compile.multi, SM120 Blackwell, SPIR-V (3,631 tests)

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

## Proven Infrastructure (stable, no rework needed)

| System | Wave |
|--------|------|
| WireGuard mesh (5-node via golgi) | 121 |
| Sovereign CI (14/14, dual-target musl+gnu) | 121 |
| ATT IP Passthrough (public IP on sporeGate) | 123 |
| Quorum Phase 1 (golgi 15-min auto-cascade) | 123 |
| relay.forward (cellMembrane → songBird E2E) | 123 |
| IPC audit clean (no plaintext on network) | 123 |
| BLAKE3 depot verified (14 musl + 2 gnu) | 123 |
| Network hardening (167k DNS blocklist, DoT, nftables) | 122 |
| SSH-only auth (PATs revoked) | 121 |
| Flint 2 WiFi (Hub 2, bridge, ApertureScience) | 121 |
| Deployment isomorphism Tier 1+2 | 121 |
| metalForge (7 probes, WiFi drift auto-remediation) | 124 |
| GPU pipeline (LSTM f64, SM120, shader.compile.multi) | 123-125 |
| Agentic divergence resolution (multi-writer safe) | 124 |

---

## Remaining Work by Team

### sporeGate — Overwatch + cellMembrane

| Task | Priority | Status |
|------|----------|--------|
| Build gnu depot (`build-local.sh --target all`) | P1 | Unblocks ironGate |
| rsync gnu to golgi depot | P1 | Unblocks ironGate dual-target fetch |
| golgi timer: force-with-lease for mirror pushes | P2 | Operational refinement |
| Dark Forest beacon deployment (Phase 4) | P2 | Designed, not deployed |
| Nest provenance depth (ledger → 5+) | P2 | Continuing |
| strandGate/southGate relay push | P2 | Opportunistic |
| Tier 3 isomorphism (gate.migrate, absorb) | P3 | Future |

### flockGate — Tower Primals

| Task | Priority | Status |
|------|----------|--------|
| songBird mesh.init (WG auto-init shipped, validate) | P1 | Zero-config WG init registered in capability_registry |
| bearDog BTSP cross-gate key exchange | P1 | auth.public_key live, trust_issuer next |
| skunkBat method wiring (method_gate.status) | P1 | Methods not in binary |
| sporePrint petalTongue render format | P2 | Entity graph schema mismatch |

### ironGate — Node Primals

| Task | Priority | Status |
|------|----------|--------|
| toadStool enrollment (biomeOS composition update) | P1 | 12/12 → 13/13 |
| Validate gnu fetch from depot (once built) | P1 | Blocked on sporeGate |
| ~~coralReef shader.compile.multi~~ | ~~P1~~ | ✅ SHIPPED (3631 tests, SM120 confirmed) |
| ~~quota-aware OOM migration~~ | ~~P1~~ | ✅ SHIPPED (4619 tests) |

### eastGate — Meta + Overwatch

| Task | Priority | Status |
|------|----------|--------|
| primalSpring cross-gate scenarios | P1 | 1038 tests, growing |
| BiomeOS multi-gate composition deploy | P2 | Deploy graph across WG mesh |
| PetalTongue ecosystem dashboard | P2 | Visualization layer |
| Squirrel AI + cross-gate barraCuda | P2 | When GPU depot fetch works |

---

## Active Impulses

None. All Wave 123-125 impulses fossilized (objectives shipped or carried into team tasks).

---

## Strategic Goals

1. **Node atomic completion**: gnu depot build → toadStool enrollment → ironGate 13/13
2. **Covalent trust Phase 2-3**: mesh.init + BTSP key exchange → cross-gate auth
3. **Transport Phase 2**: Songbird mesh.publish for sub-second impulse propagation
4. **Transport Phase 4**: Dark Forest encrypted beacon discovery on LAN
5. **Sovereignty L3→L4**: DNS registrar cutover, content via petalTongue, full composition
6. **Hardware**: Flint 2 #2 incoming. MikroTik creds for VLAN 10. Operator-paced.

---

## Coordination Rules

- **Cascade**: push to Forgejo → golgi auto-relays every 15min → GitHub synced
- **Divergence**: wateringHole uses `agentic` policy (sovereign-first, force-with-lease mirrors)
- **Impulses**: propose evolutions. File in `impulses/active/`. Overwatch reviews + archives.
- **Handoffs**: long-term AARs + cross-team requests. Archived when fossilized.
- **This blurb**: the ONE document. Paste to any IDE, any gate. Complete context.

---

## Operator-Only

| Action | Status |
|--------|--------|
| ~~ATT IP Passthrough~~ | ✅ DONE |
| Flint 2 #2 install (ordered) | Pending delivery |
| MikroTik CRS310 credential recovery | When convenient |

---

## Code Metrics

| Repo | Tests | Latest |
|------|-------|--------|
| cellMembrane | 810 | Consolidation, typed enums, relay.forward graduated, pepti decommission |
| primalSpring | 1,038 | GPU dispatch tolerance, multigate composition, deep debt |
| biomeOS | 8,351 | v4.31, 88% coverage |
| songBird | 8,929+ | relay.forward, WG auto-init, mesh capabilities |
| toadStool | 9,127 | S325 sentinel coverage, discovery gate |
| barraCuda | 4,619 | Quota-aware OOM, LSTM zero-copy, f64, GPU validated |
| coralReef | 3,631 | shader.compile.multi, SM120 Blackwell, 84% coverage |
| sporePrint | 183+ | petalTongue IPC, tower-status probes |
| metalForge | 7 probes | WiFi drift, topology sweep, WG mesh, DNS/DHCP |

---

*Single source of truth. Paste anywhere. Every agent knows the whole ecosystem and their role in it.*
