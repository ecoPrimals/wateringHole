# ecoPrimals Ecosystem Blurb — Wave 128

**Date**: Jun 27, 2026 09:40 EDT | **Wave**: 128 | **From**: eastGate overwatch
**Cascade**: All repos at parity. golgi auto-relays every 15min.
**Posture**: Convergence + debt. Topology cutover complete. sporeGate ephemeral.

---

## You Are Here

You are an agent on a gate in the ecoPrimals ecosystem. This is the single source of truth for all teams. The ecosystem is a **sovereign, self-hosted mesh of compute gates** running 13 Rust primals (NUCLEUS) coordinated via WireGuard overlay + Forgejo.

**Major topology shift (Wave 127): sporeGate is no longer the edge router. Flint 2 H1 is the plasma membrane. sporeGate is now a hot-pluggable compute node.**

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

---

## Gate Map

| Gate | LAN IP | WG IP | NUCLEUS | Role |
|------|--------|-------|---------|------|
| **golgi** | VPS | .1 | 18 svc | WG hub, Forgejo, depot, cascade timer |
| **sporeGate** | .3 | .2 | 13/13 | **Compute node** (was router), Sovereign CI, Nest |
| **eastGate** | .5 | .5 | 13/13 | Overwatch, primalSpring (1038), Meta |
| **flockGate** | WAN | .6 | 13/13 | Tower, sporePrint |
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

## Convergence + Debt Tasks

### sporeGate

| Task | Priority | Notes |
|------|----------|-------|
| ~~GNU depot build~~ | — | ✅ DONE (15/15) |
| ~~Topology cutover~~ | — | ✅ DONE (Flint is edge, sporeGate is compute) |
| systemd-networkd hardening (eno1 → .3, gw .1) | P1 | Debt: prevent DHCP fallback |
| Nest provenance depth (ledger → 5+) | P1 | Convergence |
| ~~cellMembrane SSH abstraction evolution~~ | — | ✅ DONE (ssh_target_for, exec_on_gate, 842 tests) |
| Flint config backup to git | P2 | Disaster recovery |
| Blocklist persistence (rc.local on Flint) | P2 | Lost on reboot currently |

### flockGate

| Task | Priority | Notes |
|------|----------|-------|
| songBird mesh.init (WG auto-init shipped) | P1 | Validate zero-config init works |
| bearDog BTSP: auth.trust_issuer exchange | P1 | One key pair as proof |
| skunkBat: document method gaps | P1 | Debt: know what's missing |
| sporePrint stale content cleanup | P2 | Content debt |

### ironGate

| Task | Priority | Notes |
|------|----------|-------|
| toadStool enrollment (12/12 → 13/13) | P1 | biomeOS composition update |
| Validate gnu fetch from golgi depot | P1 | Depot is live, test fetch |
| barraCuda clippy pedantic sweep | P2 | Debt |
| coralReef SM120 edge cases | P2 | Debt |

### eastGate

| Task | Priority | Notes |
|------|----------|-------|
| primalSpring KNOWN_DEBT sweep | P1 | 1038 tests, clean remaining |
| Cross-gate scenario (relay.forward validation) | P1 | Validate E2E |
| BiomeOS composition test (local) | P2 | Deploy graph validation |

---

## Code Metrics

| Repo | Tests | Trend |
|------|-------|-------|
| cellMembrane | 842 | ↑ (manifest-first SSH, async systemctl, dep update, LAN DNS) |
| primalSpring | 1,038 | Stable |
| barraCuda | 4,619 | Stable |
| coralReef | 3,631 | Stable |
| songBird | 8,929+ | Stable |
| toadStool | 9,171 | Stable |
| biomeOS | 8,351 | Stable |

---

## Coordination

- **Cascade**: push to Forgejo → golgi relays → GitHub. Agentic divergence handles races.
- **Posture**: convergence + debt. No new features unless organic.
- **Operator**: back from temporal lag. Hardware tasks resumable.

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

*Topology is sovereign. Compute is ephemeral. Infrastructure is independent. Converge and stabilize.*
