# ecoPrimals Ecosystem — Wave 120 Blurb

**Date**: Jun 21, 2026 07:35 EDT | **From**: eastGate overwatch
**Cascade**: All repos at parity | **Mesh**: 4-node (golgi ↔ sporeGate ↔ eastGate ↔ flockGate)

---

## Gate Status

| Gate | NUCLEUS | WG | Role | Status |
|------|---------|-----|------|--------|
| **sporeGate** | 13/13 | .2 | Build authority + Nest provenance + Overwatch | ✅ Sovereign CI live |
| **eastGate** | 13/13 | .5 | Meta atomic + primalSpring evolution | ✅ Overwatch |
| **flockGate** | 13/13 | .6 | Tower atomic + sporePrint | ✅ Tower work unblocked |
| **ironGate** | — | — | Node atomic (compute trio) | ⏳ SSH enrollment (sporeGate RustDesk) |
| **golgi** | 18 svc | .1 | Sole VPS: Forgejo, WG hub, relay, depot | ✅ 0 failed |

**Deferred**: strandGate, southGate (Omada-side, relay push pending), swiftGate (Flint 2), northGate (Windows P3), fieldGate (dead CMOS).

---

## Active Work by Team

### sporeGate Overwatch — Nest + Infra

| Task | Priority | Notes |
|------|----------|-------|
| ironGate SSH enrollment | P0 | RustDesk → add key → deploy NUCLEUS |
| cellMembrane evolution (deployment isomorphism) | P1 | 731 tests, Tier 1+2 shipped, driving Tier 3 |
| Nest provenance depth (ledger commits per wave) | P1 | Height 3, SweetGrass 4 braids |
| Flint 2 config (after operator installs) | P2 | SSH in, AP bridge, sovereign config |
| Omada VLAN config (192.168.4.111, admin/admin) | P2 | Access confirmed |
| strandGate/southGate relay push | P2 | Via RustDesk |

### flockGate Tower — BearDog, Songbird, SkunkBat

| Task | Priority | Notes |
|------|----------|-------|
| BearDog: BTSP trust bootstrap over WAN | P1 | WG mesh live, WAN periplasm validator |
| Songbird: mesh.init topology-aware routing | P1 | Identity-based discovery now available |
| SkunkBat: threat detection + defense attestation | P1 | Defense layer for K-Derm outer membrane |
| sporePrint content + taxonomy coverage | P2 | 183+ tests, 222 pages |

### eastGate Meta — BiomeOS, Squirrel, PetalTongue + Overwatch

| Task | Priority | Notes |
|------|----------|-------|
| primalSpring scenario expansion (87 → grow) | P1 | 963 lib tests, interaction testing hub |
| Overwatch: cascade, review, blurb | P1 | Continuous |
| Squirrel AI pipeline + provenance tracking | P2 | Wired, ready for depth |
| PetalTongue visualization | P2 | Dashboard for ecosystem state |
| BiomeOS neural-api (8,351 tests) | P3 | Deep debt complete, stable |

### ironGate Node — ToadStool, BarraCuda, CoralReef (after enrollment)

| Task | Priority | Notes |
|------|----------|-------|
| ToadStool fleet management | P1 | S321, 112 methods, 9,069 lib tests |
| BarraCuda tensor dispatch | P1 | Compute pipeline |
| CoralReef shader pipelines | P1 | GPU/compute shaders |

---

## Code Metrics

| Repo | Tests | Latest Evolution |
|------|-------|-----------------|
| **cellMembrane** | 731 | Manifest-driven config gen, gate.validate trust barrier, nftables refactor |
| **primalSpring** | 963 (87 scenarios) | toadStool S321, typed errors, deep debt clean |
| **sporePrint** | 183+ | Taxonomy audit, depot tests, tower metrics, zero expect() |
| **biomeOS** | 8,351 | v4.31 structural refactor, 88% coverage |
| **songBird** | 8,929 | WG mesh overlay, zero hardcoded names |

---

## Deployment Isomorphism

| Tier | Status | Capabilities |
|------|--------|--------------|
| **1** | ✅ Shipped | `topology.service <role>`, `topology.roles` — identity-based discovery |
| **2** | ✅ Shipped | `wireguard.generate`, `caddy.generate` — declarative config from manifest |
| **3** | Next | `gate.migrate`, `gate.bootstrap --absorb`, credential portability, DNS gen |

Manifest `roles` + `wg_ip` populated for: golgi, sporeGate, eastGate, flockGate, ironGate.

---

## Sovereign CI

```
Forgejo push → golgi hook → SSH sporeGate → cargo build (musl) → rsync to golgi → WAN depot
```
Full build: ~24 min | Incremental: ~2–5 min | Cost: $0 | Depot: BLAKE3 verified 13/13

---

## Architecture

```
Internet → ATT → sporeGate (NAT/FW/BUILD) → CRS310 (L2) → eastGate, ironGate
                      ↕ WireGuard                              ↕ Omada (Hub 2)
               golgi VPS (sole)                          strandGate, southGate, Flint 2
               ├── Forgejo + WG Hub
               ├── Sovereign Relay
               ├── Caddy TLS + WAN Depot        flockGate (WAN, via golgi relay)
               └── Fed by sporeGate rsync
```

---

## Operator-Only

| Action | Unblocks | When |
|--------|----------|------|
| Flint 2 physical install at Hub 2 | swiftGate + Omada-side WiFi | This weekend |
| fieldGate CMOS repair | fieldGate enrollment | Low priority |
