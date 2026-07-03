# ecoPrimals Ecosystem Blurb — Wave 130

**Date**: Jul 3, 2026 07:30 EDT | **Wave**: 130 | **From**: eastGate overwatch
**Cascade**: All repos at parity. golgi auto-relays every 15min.
**Posture**: Infrastructure hardened. Compute hosting platform ready. ABG integration next.

---

## You Are Here

You are an agent on a gate in the ecoPrimals ecosystem. This is the single source of truth for all teams. The ecosystem is a **sovereign, self-hosted mesh of compute gates** running 13 Rust primals (NUCLEUS) coordinated via WireGuard overlay + Forgejo.

**Major topology shift (Wave 127): sporeGate is no longer the edge router. Flint 2 H1 is the plasma membrane. sporeGate is now a hot-pluggable compute node.**

**Wave 130**: KinderLab WiFi deployed (parenting-filtered, guest-isolated at both sites). Sportsbook DNS blocking live on all networks. Boot persistence hardened. Infrastructure is a platform — any NUC plugs in and gets compute-ready.

---

## Physical Topology (NEW — Wave 127)

```
INTERNET → ATT BGW320 (passthrough, no NAT)
    → Flint 2 H1 (EDGE ROUTER — plasma membrane)
        WAN: 162.226.225.148 (public)
        LAN: 192.168.4.1/22
        Services: NAT, DHCP, DNS (91k blocklist), firewall, WiFi (BlackMesa 5G + ApertureScience 2.4G)
        Port forwards → sporeGate .3 (WG, SSH, Forgejo, HTTP/S, RustDesk, TURN, NestGate)
            │
            ▼
        CRS310 (L2 backbone, 10G/2.5G)
            ├── sporeGate .3 (compute, WG hub, Sovereign CI, Nest)
            ├── eastGate .5 (10G, overwatch, primalSpring)
            ├── northGate (Win/5090, hobby)
            └── Omada → House 2 → Flint H2 (bridge, ApertureScience WiFi)
                            └── ironGate .7 (GPU compute)

WireGuard overlay (10.13.37.0/24) via golgi VPS (.1)
    ├── sporeGate .2
    ├── eastGate .5
    ├── flockGate .6 (WAN, via golgi relay)
    └── ironGate .7
```

**Key invariant**: unplugging sporeGate does NOT kill the network. Flint is the membrane. sporeGate is ephemeral compute.

### WiFi Map (Wave 130)

| SSID | Band | Zone | DNS Policy | Sites |
|------|------|------|-----------|-------|
| BlackMesa | 5GHz | LAN /22 | Security + sportsbook (91k) | House 1 |
| Aperture Science | 2.4GHz | LAN /22 | Security + sportsbook (91k) | House 1 (IoT) |
| ApertureScience | 2.4+5GHz | LAN /22 | Security + sportsbook (91k) | House 2 |
| **KinderLab** | 2.4+5GHz | **Guest isolated** (192.168.9.0/24 H1, 192.168.10.0/24 H2) | **Full parenting** (167k rules) | Both |

### Compute Hosting Ready

Any NUC plugs into CRS310 or Omada → gets DHCP from Flint → DNS + internet + mesh access. The platform is modular:
- **sporeGate (.3)**: public face (Caddy, Forgejo, WG hub), port-forwarded from Flint
- **ironGate (.169)**: GPU compute (RTX 5070), 0.2ms from sporeGate
- **New NUCs**: just plug in, mesh absorbs them — open 2.5G ports on CRS310 + Omada
- **KinderLab**: safe demo/classroom network for student devices (filtered, isolated from LAN)

---

## Gate Map

| Gate | LAN IP | WG IP | NUCLEUS | Role |
|------|--------|-------|---------|------|
| **golgi** | VPS | .1 | 18 svc | WG hub, Forgejo, depot, cascade timer |
| **sporeGate** | .3 | .2 | 13/13 | **Compute node** (was router), Sovereign CI, Nest |
| **eastGate** | .5 | .5 | 13/13 | Overwatch, primalSpring (1038), Meta |
| **flockGate** | WAN | .6 | 13/13 | Tower, sporePrint — **DOWN** (pending physical power-on) |
| **ironGate** | H2 | .7 | 12/12 | Node compute, GPU (RTX 5070) |
| **Flint H1** | .1 | — | — | **Edge router** (plasma membrane) |
| **Flint H2** | .250 | — | — | Bridge WiFi AP (House 2) |

---

## Primal → Gate Assignment

| Primal | Gate | Connect |
|--------|------|---------|
| **BearDog** | flockGate | RustDesk (WAN relay) |
| **Songbird** | flockGate | RustDesk (WAN relay) |
| **SkunkBat** | flockGate | RustDesk (WAN relay) |
| **ToadStool** | ironGate | SSH 192.168.4.x (via Omada/H2) |
| **BarraCuda** | ironGate | SSH 192.168.4.x (via Omada/H2) |
| **CoralReef** | ironGate | SSH 192.168.4.x (via Omada/H2) |
| **NestGate** | sporeGate | SSH 192.168.4.3 |
| **RhizoCrypt** | sporeGate | SSH 192.168.4.3 |
| **LoamSpine** | sporeGate | SSH 192.168.4.3 |
| **SweetGrass** | sporeGate | SSH 192.168.4.3 |
| **cellMembrane** | sporeGate | SSH 192.168.4.3 |
| **BiomeOS** | eastGate | (this gate) |
| **Squirrel** | eastGate | (this gate) |
| **PetalTongue** | eastGate | (this gate) |
| **primalSpring** | eastGate | (this gate) |
| **sporePrint** | flockGate | RustDesk (WAN relay) |

---

## What Wave 128-130 Proved

- **ironGate**: GNU depot VERIFIED (BLAKE3 match, RTX 5070 functional), clippy pedantic ZERO warnings, 12-axis debt audit CLEAN (zero actionable debt across all axes)
- **primalSpring**: 110 scenarios, 1060 lib tests, KNOWN_DEBT=0, PORT_REGISTRY deprecated, 9 orphaned scenarios wired
- **cellMembrane**: 848 tests, manifest-first SSH resolution, async systemctl, KNOWN_MESH_GATES constant, dispatch/data.rs test coverage
- **NestGate**: dead dep purge, Arc clones, content_handlers split, fabricated metrics eliminated
- **Squirrel**: mock evolution, timeout threading, dead module purge
- **biomeOS**: mega-test split + topology sync
- **RhizoCrypt**: deep debt sweep (2 rounds)

---

## Remaining Work by Team

### sporeGate

| Task | Priority | Notes |
|------|----------|-------|
| systemd-networkd hardening (eno1 → .3, gw .1) | P1 | Prevent DHCP fallback |
| Nest provenance depth (ledger → 5+) | P1 | Convergence |
| Flint config backup to git | P2 | Disaster recovery |
| Blocklist persistence (rc.local on Flint) | P2 | Lost on reboot currently |

### flockGate

| Task | Priority | Notes |
|------|----------|-------|
| songBird mesh.init validation | P1 | WG auto-init shipped, validate it works |
| bearDog BTSP: auth.trust_issuer exchange | P1 | One key pair as proof |
| skunkBat: document method gaps | P1 | Debt: know what's missing |
| sporePrint stale content cleanup | P2 | Content debt |

### ironGate

| Task | Priority | Notes |
|------|----------|-------|
| ~~GNU depot validation~~ | — | ✅ DONE (BLAKE3 verified, RTX 5070 functional) |
| ~~barraCuda clippy pedantic~~ | — | ✅ DONE (zero warnings, 12-axis audit clean) |
| toadStool enrollment (12/12 → 13/13) | P1 | Blocked on biomeOS composition update |
| coralReef SM120 edge cases | P2 | Debt |

### eastGate

| Task | Priority | Notes |
|------|----------|-------|
| ~~primalSpring KNOWN_DEBT sweep~~ | — | ✅ DONE (KNOWN_DEBT=0, 1060 tests) |
| Cross-gate scenario (relay.forward validation) | P1 | Validate E2E |
| BiomeOS composition test (local) | P2 | Deploy graph validation |

---

## Code Metrics

| Repo | Tests | Trend |
|------|-------|-------|
| cellMembrane | 848 | ↑ (SSH abstraction, KNOWN_MESH_GATES, data.rs coverage) |
| primalSpring | 1,060 | ↑ (110 scenarios, 9 orphaned wired, KNOWN_DEBT=0) |
| barraCuda | 4,619 | ↑ (clippy pedantic zero, 12-axis audit clean) |
| coralReef | 3,631 | Stable |
| songBird | 8,929+ | Stable |
| toadStool | 9,171 | Stable |
| biomeOS | 8,351 | Stable (mega-test split done) |
| NestGate | — | Evolved (dead deps purged, Arc clones, handlers split) |
| Squirrel | — | Evolved (mock evolution, timeout threading) |
| RhizoCrypt | — | Evolved (2-round deep debt sweep) |

---

## Coordination

- **Cascade**: push to Forgejo → golgi relays → GitHub. Agentic divergence handles races.
- **Posture**: platform ready. Compute hosting modular. ABG integration next.
- **Operator**: available. flockGate pending physical power-on (offsite).
- **Strategic**: gen5/THERMAL_SOVEREIGNTY + SOVEREIGN_PALLET whitepapers shipped. KinderLab deployed.
- **ABG Compute**: infrastructure supports NUC-as-gateway. Student sessions land on any gate.

---

## Operator Tasks (resumable)

| Action | Status |
|--------|--------|
| ~~ATT IP Passthrough~~ | ✅ DONE (to Flint) |
| ~~Flint H1 edge router~~ | ✅ DONE (Wave 127) |
| ~~Flint H2 bridge WiFi~~ | ✅ DONE (Wave 121) |
| MikroTik CRS310 credential recovery | When convenient |
| Flint blocklist persistence (rc.local) | Quick fix when on-site |

---

*Topology is sovereign. Compute is ephemeral. Debt is converging to zero. The rooms are being prepared.*
