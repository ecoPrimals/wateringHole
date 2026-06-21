# ecoPrimals Ecosystem — Wave 120 Blurb

**Date**: Jun 21, 2026 12:00 EDT | **From**: sporeGate overwatch + eastGate overwatch
**Cascade**: All repos at parity | **Mesh**: 5-node (golgi ↔ sporeGate ↔ eastGate ↔ flockGate ↔ ironGate)

---

## Gate Status

| Gate | NUCLEUS | WG | Role | Status |
|------|---------|-----|------|--------|
| **sporeGate** | 13/13 | .2 | Build authority + Nest provenance + Overwatch | ✅ Sovereign CI live |
| **eastGate** | 13/13 | .5 | Meta atomic + primalSpring evolution | ✅ Overwatch |
| **flockGate** | 13/13 | .6 | Tower atomic + sporePrint | ✅ Tower work unblocked |
| **ironGate** | — | .7 | Node atomic (compute trio) | ⏳ SSH key exchange needed for NUCLEUS |
| **golgi** | 18 svc | .1 | Sole VPS: Forgejo, WG hub, relay, depot | ✅ 0 failed |

**Deferred**: strandGate, southGate (Omada-side, relay push pending), northGate (Windows P3), fieldGate (dead CMOS).
**Infrastructure**: Flint 2 (GL-MT6000) enrolled as bridge AP at Hub 2 — `ApertureScience` WiFi 6, Eeros retired.

---

## Active Work by Team

### sporeGate Overwatch — Nest + Infra

| Task | Priority | Notes |
|------|----------|-------|
| ironGate SSH enrollment | P0 | Key exchange needed → deploy NUCLEUS |
| **Convergence shipped** | ✅ | firewall/wireguard/caddy generate from manifest, zero flags, proven identical |
| **Flint 2 enrolled** | ✅ | Bridge AP at Hub 2, ApertureScience WiFi 6, Eeros retired |
| cellMembrane evolution (deployment isomorphism) | P1 | 731 tests, Tier 1+2 shipped, Tier 3 next |
| Nest provenance depth (ledger commits per wave) | P1 | Height 3, SweetGrass 4 braids |
| ~~eastGate connectivity~~ | ✅ | RESOLVED — was transient (sleep/hibernate). golgi 32ms, sporeGate 60ms |
| Omada VLAN config (192.168.4.2) | P2 | Access confirmed |
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
| **cellMembrane** | 731 | **Convergence**: firewall/wireguard/caddy generate from manifest (zero flags), wg_pubkey, interface fields |
| **primalSpring** | 963 (87 scenarios) | toadStool S323+, typed errors, deep debt clean |
| **sporePrint** | 183+ | Taxonomy audit, depot tests, tower metrics, zero expect() |
| **biomeOS** | 8,351 | v4.31 structural refactor, 88% coverage |
| **songBird** | 8,929 | WG mesh overlay, zero hardcoded names |

---

## Deployment Isomorphism

| Tier | Status | Capabilities |
|------|--------|--------------|
| **1** | ✅ Shipped | `topology.service <role>`, `topology.roles` — identity-based discovery |
| **2** | ✅ Shipped | `wireguard.generate`, `caddy.generate`, `firewall.generate` — all manifest-aware, zero flags |
| **3** | Next | `gate.migrate`, `gate.bootstrap --absorb`, credential portability (bearDog BTSP), DNS gen |

Manifest `roles` + `wg_ip` + `wg_pubkey` populated for all 4 mesh gates. Interface fields for sporeGate. `wan_endpoint` for golgi.

### Auth Evolution (S1→S3)

| Stage | Model | Status |
|-------|-------|--------|
| **S1** | Manual ed25519 keys + Forgejo user | Current — fragile, host-coupled |
| **S2** | bearDog BTSP trust bootstrap | flockGate Tower team owns |
| **S3** | Composition-deterministic auth (genetics) | Tier 3 isomorphism target |

ironGate Forgejo issue: key IS registered (ID 1, May 28). Problem on ironGate side (likely wrong remote URLs — same pepti pattern). Troubleshooting in FRAGO.

---

## Sovereign CI

```
Forgejo push → golgi hook → SSH sporeGate → cargo build (musl) → rsync to golgi → WAN depot
```
Full build: ~14 min | Incremental: ~2–5 min | Cost: $0 | Depot: BLAKE3 verified 14/14 (includes membrane)

---

## Architecture

```
Internet → ATT → sporeGate (NAT/FW/BUILD) → CRS310 (L2) → eastGate, ironGate
                      ↕ WireGuard                              ↕ Omada (Hub 2)
               golgi VPS (sole)                          strandGate, Flint 2 (bridge AP)
               ├── Forgejo + WG Hub                           └── WiFi "ApertureScience"
               ├── Sovereign Relay                                 2.4G+5G WiFi 6
               ├── Caddy TLS + WAN Depot        flockGate (WAN, via golgi relay)
               └── Fed by sporeGate rsync
```

---

## Operator-Only

| Action | Unblocks | When |
|--------|----------|------|
| ~~Flint 2 physical install at Hub 2~~ | ~~swiftGate + Omada-side WiFi~~ | ✅ Done — bridge AP live |
| ironGate: add sporegate-gate-v1 to authorized_keys | NUCLEUS deploy + full mesh | Waiting on ironGate team |
| ~~eastGate WG check~~ | ~~Mesh integrity~~ | ✅ RESOLVED — transient (was sleeping) |
| fieldGate CMOS repair | fieldGate enrollment | Low priority |
