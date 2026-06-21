# ecoPrimals Ecosystem — Wave 121 Blurb

**Date**: Jun 21, 2026 18:35 EDT | **From**: eastGate overwatch
**Cascade**: All repos at parity | **Mesh**: 5-node LIVE (golgi 41ms, sporeGate 75ms, ironGate 79ms from eastGate)

---

## Gate Status — ALL ENROLLED

| Gate | NUCLEUS | WG | Role | Hardware | Status |
|------|---------|-----|------|----------|--------|
| **sporeGate** | 13/13 | .2 | Build authority + Nest + Overwatch | Ryzen 5 6600H 27GB | ✅ Sovereign CI |
| **eastGate** | 13/13 | .5 | Meta atomic + primalSpring + Overwatch | i7 64GB | ✅ 998 tests |
| **flockGate** | 13/13 | .6 | Tower atomic + sporePrint | i9-13900K 62GB (WAN) | ✅ Tower ready |
| **ironGate** | 12/12 | .7 | Node atomic + **GPU compute** | i9-12900K + **RTX 5070** | ✅ GPU live |
| **golgi** | 18 svc | .1 | Sole VPS: Forgejo, WG hub, relay, depot | DO droplet | ✅ 0 failed |

**Infrastructure**: Flint 2 (GL-MT6000) bridge AP at Hub 2 — WiFi 6, WPA2/3, zero cloud.

**Deferred**: strandGate, southGate (relay push pending), northGate (Win/5090, P3), fieldGate (dead CMOS).

---

## Active Work by Team

### sporeGate Overwatch — Nest + Build Authority + Infra

| Task | Priority | Notes |
|------|----------|-------|
| **Dual-target depot** (gnu for GPU primals) | P1 | Impulse filed by ironGate. Build barracuda+coralReef as glibc for GPU gates |
| Nest provenance depth | P1 | Ledger height 3, periodic commits |
| HPC VLAN 10 implementation | P2 | Designed, blocked on MikroTik credentials |
| Omada VLAN config (192.168.4.111) | P2 | Access confirmed |
| strandGate/southGate relay push | P2 | Via RustDesk |

### flockGate Tower — BearDog, Songbird, SkunkBat

| Task | Priority | Notes |
|------|----------|-------|
| BearDog: BTSP trust bootstrap over WAN | P1 | Auth evolution S1→S2 |
| Songbird: mesh.init topology-aware routing | P1 | Identity-based discovery available |
| SkunkBat: threat detection + defense attestation | P1 | K-Derm outer membrane defense |
| sporePrint content evolution | P2 | 183+ tests, taxonomy audited |

### ironGate Node — ToadStool, BarraCuda, CoralReef + GPU

| Task | Priority | Notes |
|------|----------|-------|
| BarraCuda GPU compute (RTX 5070 operational) | P1 | LSTM zero-copy, Vulkan shaders, f64 native |
| CoralReef shader pipelines | P1 | GPU dispatch via sovereign-dispatch IPC |
| ToadStool fleet management (S323, 9,074 tests) | P1 | submit split, test extraction |
| Dual-target depot integration (fetch gnu binaries) | P1 | Coordinate with sporeGate |

### eastGate Meta — BiomeOS, Squirrel, PetalTongue + Overwatch

| Task | Priority | Notes |
|------|----------|-------|
| primalSpring scenario expansion | P1 | 998 lib tests, growing |
| Overwatch: cascade, review, blurb | P1 | Continuous |
| Squirrel AI pipeline + provenance | P2 | Wired |
| PetalTongue visualization | P2 | Dashboard for ecosystem state |

### cellMembrane — Code Evolution

| Task | Priority | Notes |
|------|----------|-------|
| Dual-target depot support (arch enum, fetch logic) | P1 | Per ironGate impulse |
| Tier 3 isomorphism (gate.migrate, absorb) | P2 | Self-healing mesh |
| Auth evolution: bearDog BTSP → composition auth | P2 | S1→S2→S3 path |

---

## Code Metrics

| Repo | Tests | Latest Evolution |
|------|-------|-----------------|
| **cellMembrane** | 731 | Manifest config gen, gate.validate trust barrier, leak fix, BLAKE3 sentinel |
| **primalSpring** | 998 | toadStool S323, deep debt sweep, scenario expansion |
| **sporePrint** | 183+ | Taxonomy audit, depot tests, tower metrics |
| **biomeOS** | 8,351 | v4.31 structural refactor, 88% coverage |
| **songBird** | 8,929 | Wave 121 idiom sweep, clippy --all-targets zero |
| **toadStool** | 9,074 | S323 submit split, test extraction, composition graduation |
| **barraCuda** | — | LSTM zero-copy, mul_add, GPU depot evolution |

---

## Sovereign CI + Depot

```
Forgejo push → golgi hook → SSH sporeGate → cargo build (musl) → rsync to golgi → WAN depot
```
Full build: ~14 min | Incremental: ~2–5 min | Cost: $0 | Depot: BLAKE3 verified 14/14

**Proposed evolution**: Dual-target (musl + gnu) for GPU primals on compute gates.

---

## Topology & Hardware

```
Internet → ATT BGW320 → sporeGate (NAT/FW/BUILD/DHCP)
                              │ eno1 (LAN 192.168.4.0/22)
                              │ wg0 (10.13.37.2)
                              │
                         CRS310 (10G L2 trunk) → Omada SX3008F (Hub 2)
                              │                       │
                         eastGate (.5)           ironGate (.7) [RTX 5070]
                                                Flint 2 (.250) [WiFi 6 AP]
                                                     └── "ApertureScience" 2.4G+5G

                    WireGuard overlay → golgi VPS (.1) ← sole VPS
                                          ├── Forgejo (git.primals.eco:2222)
                                          ├── WG Hub (5 peers, forwarding)
                                          ├── Sovereign Relay (hbbs/hbbr)
                                          ├── Caddy TLS (membrane.primals.eco)
                                          └── WAN Depot (fed by sporeGate rsync)

                                        flockGate (.6) ← WAN via golgi relay
```

**HPC VLAN 10** (192.168.10.0/24) designed — gate-to-gate compute over 10G SFP+ trunk. Blocked on MikroTik credentials.

---

## Sovereignty & Auth

| Stage | Model | Status |
|-------|-------|--------|
| S1 | Manual ed25519 keys + Forgejo user | ✅ Current (all gates enrolled) |
| S2 | bearDog BTSP trust bootstrap | P1 — flockGate Tower team owns |
| S3 | Composition-deterministic auth | Tier 3 target |
| S4 | Self-healing mesh (gate.migrate/absorb) | Tier 3 target |

---

## Deployment Isomorphism

| Tier | Status | Capabilities |
|------|--------|--------------|
| **1** | ✅ | `topology.service`, `topology.roles` — identity-based discovery |
| **2** | ✅ | `wireguard.generate`, `caddy.generate`, `firewall.generate` — manifest-driven |
| **3** | Next | `gate.migrate`, `gate.bootstrap --absorb`, credential portability, DNS gen |

---

## Glacial State (deep infrastructure)

- **pepti**: Decommissioned Wave 120. $24/mo saved.
- **Eero mesh**: Retired Wave 120. Replaced by Flint 2 (zero cloud).
- **Sovereign CI**: Migrated from pepti VPS to sporeGate hardware Wave 120.
- **WG mesh**: Evolved from 3-node (Wave 116) → 4-node (Wave 119) → 5-node (Wave 121).
- **NUCLEUS pattern**: Proven across 4 gates (sporeGate system, eastGate/flockGate/ironGate user systemd).
- **GPU compute**: ironGate RTX 5070 confirmed. Dual-target depot proposal active.

---

## Operator-Only

| Action | Unblocks | When |
|--------|----------|------|
| MikroTik CRS310 credential recovery (5s reset) | HPC VLAN implementation | When convenient |
| ATT BGW320 IP Passthrough (MAC: 84:47:09:38:97:54) | Eliminate double NAT | When convenient |
| fieldGate CMOS repair | fieldGate enrollment | Low priority |
