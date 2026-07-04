# ecoPrimals Ecosystem Blurb — Wave 132

**Date**: Jul 4, 2026 10:00 EDT | **Wave**: 132 | **From**: eastGate overwatch
**Cascade**: All repos at parity. Per-gate heads eliminate divergence (wave.toml + heads/*.toml).
**Posture**: All gates ONLINE. songBird LAN bypass SHIPPED. Deploy → validate → ABG live.

---

## You Are Here

You are an agent on a gate in the ecoPrimals ecosystem. This is the single source of truth for all teams. The ecosystem is a **sovereign, self-hosted mesh of compute gates** running 13 Rust primals (NUCLEUS) coordinated via WireGuard overlay + Forgejo.

**Wave 132 milestone**: Async freshness evolution SHIPPED — per-gate head publishing eliminates all cascade divergence conflicts. songBird LAN direct-connect bypass and bearDog BTSP trust exchange are SHIPPED in code. The only remaining step is deploy + validate + activate the ABG compute pipeline.

---

## ABG Compute Hosting — The System

**Architecture**: sporeGate is the **public entry point** (`lab.primals.eco`). All HPC compute lives behind it on the LAN (ironGate, strandGate, future NUCs) or on WAN via songBird relay (flockGate, future remote nodes).

```
┌─────────────────────────────────────────────────────────────────┐
│                        INTERNET (WAN)                            │
│    lab.primals.eco → Cloudflare → Flint H1 (plasma membrane)    │
└───────────────────────────────┬─────────────────────────────────┘
                                │ :443 DNAT
                                ▼
┌───────────────────────────────────────────────────────────────────┐
│  sporeGate (.3) — PUBLIC ENTRY POINT                              │
│    Caddy: lab.primals.eco reverse proxy                           │
│    songBird mesh hub: routes capability.call to compute backends  │
│    Sovereign CI: builds all primals (musl + gnu targets)          │
│    Forgejo: git.primals.eco                                       │
└──────────────┬──────────────────────────┬─────────────────────────┘
               │ LAN (0.2ms)              │ songBird relay (WAN)
               ▼                          ▼
┌──────────────────────────┐   ┌──────────────────────────────────┐
│  LAN HPC CLUSTER         │   │  WAN COMPUTE (relay via golgi)   │
│                          │   │                                  │
│  ironGate (.237)         │   │  flockGate (WAN, .6 WG)         │
│    RTX 5070 (16GB)       │   │    Tower atomic: songBird dev    │
│    JupyterHub :8000      │   │    bearDog, skunkBat evolution   │
│    GROMACS, CUDA          │   │                                  │
│    ABG: bake3011,        │   │  (future remote GPU nodes)       │
│          alistaire       │   │                                  │
│                          │   └──────────────────────────────────┘
│  strandGate (joining)    │
│    64-core EPYC, 256GB   │
│    STAR alignment        │
│    Heavy CPU workloads   │
│                          │
│  (future NUCs: plug in,  │
│   mesh absorbs)          │
└──────────────────────────┘
```

**Routing flow** (once mesh validated):
1. Student browser → `lab.primals.eco` → Caddy on sporeGate
2. Caddy → songBird `capability.call` → routes to best compute node
3. songBird on sporeGate → LAN direct-connect → ironGate/strandGate
4. songBird on sporeGate → relay via golgi → flockGate (WAN nodes)
5. Compute result flows back through mesh → student browser

**Key principle**: songBird IS the port solver. Services bind to localhost. No ports exposed externally. Mesh handles all routing.

---

## Physical Topology

```
INTERNET → ATT BGW320 (passthrough, no NAT)
    → Flint 2 H1 (EDGE ROUTER — plasma membrane)
        WAN: 162.226.225.148 (public)
        LAN: 192.168.4.1/22
        Services: NAT, DHCP, DNS (91k blocklist), firewall, WiFi
        Port forwards → sporeGate .3 (WG, SSH, Forgejo, HTTP/S, TURN, NestGate)
            │
            ▼
        CRS310 (L2 backbone, 10G/2.5G)
            ├── sporeGate .3 (compute entry, WG hub, Sovereign CI, Nest)
            ├── eastGate .5 (10G, overwatch, primalSpring)
            ├── northGate (Win/5090, hobby)
            └── Omada → House 2 → Flint H2 (bridge, WiFi)
                            └── ironGate .237 (GPU compute)

WireGuard overlay (10.13.37.0/24) via golgi VPS (.1)
    ├── sporeGate .2
    ├── eastGate .5
    ├── flockGate .6 (WAN, via golgi relay)
    └── ironGate .7
```

**Key invariant**: unplugging sporeGate does NOT kill the network. Flint is the membrane. sporeGate is ephemeral compute entry.

---

## Gate Map

| Gate | LAN IP | WG IP | Role |
|------|--------|-------|------|
| **golgi** | VPS | .1 | WG hub, Forgejo, depot, cascade timer, unify_freshness |
| **sporeGate** | .3 | .2 | **Public entry** (Caddy, Sovereign CI, mesh hub) |
| **eastGate** | .5 (.244) | .5 | Overwatch, cellMembrane, primalSpring |
| **flockGate** | WAN | .6 | Tower atomic home (songBird, bearDog, skunkBat) |
| **ironGate** | .237 (H2) | .7 | **GPU compute** (RTX 5070, JupyterHub, ABG) |
| **strandGate** | (joining) | — | **CPU compute** (64-core EPYC, STAR alignment) |

---

## Wave 131 Shipped (fossilized)

- **Async freshness**: wave.toml + heads/<gate>.toml — zero cascade conflicts
- **songBird LAN bypass**: `try_lan_direct_connect`, `/proc/net/fib_trie` subnet detect, typed exhaustive dispatch (62+ methods), hot-path allocation elimination, security fail-closed, health honesty
- **bearDog BTSP exchange**: `mesh_join.rs`, bidirectional registry, E2E test, trusted_issuer_registry refactored (826L → 6 modules), dynamic announce
- **primalSpring**: 110 scenarios, 1060 tests, KNOWN_DEBT=0, 9 orphaned scenarios wired
- **cellMembrane**: 848 tests, KNOWN_MESH_GATES, manifest-first SSH, async systemctl

---

## Forward Work — Deploy + Activate ABG Compute

### Phase 1: Mesh Deploy + Validate (NEXT)

| Task | Gate | Status |
|------|------|--------|
| Build songBird v0.2.1-wave131b (Sovereign CI) | sporeGate | CI triggered |
| Deploy new songBird to sporeGate, eastGate, ironGate | all LAN | Pending CI |
| Test LAN `peer.connect` (sporeGate ↔ eastGate) | eastGate | After deploy |
| Test LAN `peer.connect` (eastGate ↔ ironGate) | eastGate | After deploy |
| Test WAN peering (flockGate → golgi relay → LAN) | flockGate | After LAN works |
| Test `capability.call` cross-gate dispatch | eastGate | After peering |

### Phase 2: Lab Activation

| Task | Gate | Notes |
|------|------|-------|
| Activate Caddy → songBird → JupyterHub route | sporeGate | After capability.call works |
| Install bioinformatics stack (salmon, STAR, R) | ironGate | Via mesh (no SSH) |
| Stage pilot dataset (GSE166686 salmon RNA-seq) | ironGate | Via mesh |
| strandGate enrollment (mesh auto-absorb) | strandGate | When hardware arrives |

### Phase 3: ABG Student Onboarding

| Task | Notes |
|------|-------|
| bake3011: Salmon RNA-seq pipeline validated | STAR + DESeq2 + WGCNA on ironGate → strandGate |
| alistaire: CAZyme FEL pipeline validated | GROMACS metadynamics on ironGate (RTX 5070) |
| KinderLab WiFi for student access | Already deployed (guest-isolated, parenting-filtered) |
| lab.primals.eco: landing page + JupyterHub access | Static dashboard live, interactive pending mesh |

---

## Cascade Interaction Model (Wave 131+ — async evolution)

```
WRITE MODEL (zero conflicts):
  wave.toml         ← overwatch sole writer (wave ID, posture, gates online/offline)
  heads/<gate>.toml ← each gate writes ONLY its own file after cascade
  freshness.toml    ← DEPRECATED (golgi generates from wave.toml + heads/*.toml for compat)

FLOW:
  Gate pushes code → Forgejo → golgi quorum timer (15min)
    → golgi pulls all repos
    → golgi writes heads/golgi.toml (its own HEADs)
    → golgi runs unify_freshness() → regenerates freshness.toml
    → golgi pushes wateringHole to GitHub (mirror)

  Each gate after cascade:
    → writes heads/<gate>.toml with its local repo HEADs
    → pushes wateringHole (FF-only pull first, no conflict)
```

---

## Outer Membrane — Cloudflare (K-Derm Layer)

```
Internet → Cloudflare (outer membrane, DDoS, TLS edge)
    → Origin: Flint H1 (162.226.225.148) for lab.primals.eco
    → Origin: golgi (157.230.3.183) for membrane.primals.eco, git.primals.eco
```

**cellMembrane `cloudflare.*` module** (operational): `dns.list`, `dns.update`, `cache.purge`, `ssl.settings`
**Blocker**: `CF_API_TOKEN` needs provisioning on golgi tower.env (one-time operator action).

---

## Operator Tasks (one-time, then fully agentic)

| Action | Priority | Status |
|--------|----------|--------|
| Provision CF_API_TOKEN on golgi tower.env | P1 | Unlocks agentic DNS |
| ironGate: re-authorize SSH key OR restart WG | P1 | Unlocks compute node access |
| MikroTik CRS310 credential recovery | P3 | When convenient |

---

## Code Metrics

| Repo | Tests | Status |
|------|-------|--------|
| cellMembrane | 848 | Stable |
| primalSpring | 1,060 | Stable (KNOWN_DEBT=0) |
| barraCuda | 4,619 | Stable |
| coralReef | 3,631 | Stable |
| songBird | 8,929+ | Evolved (LAN bypass shipped) |
| toadStool | 9,171 | Stable |
| biomeOS | 8,351 | Stable |
| bearDog | — | Evolved (BTSP exchange shipped) |

---

*sporeGate is the entry. LAN and WAN HPC behind it. songBird routes everything. The mesh absorbs.*
