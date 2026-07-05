# ecoPrimals Ecosystem Blurb — Wave 132f

**Date**: Jul 5, 2026 08:10 EDT | **Wave**: 132f | **From**: eastGate overwatch
**Cascade**: All repos cascaded (Jul 5 AM). cellMembrane bidirectional relay landed. primalSpring 114 scenarios. sporeGate deployed songBird http.proxy LIVE but bearDog ACME panics.
**Posture**: **DEBT RESOLUTION** — Tower HTTP integration exposed 2 critical blockers in bearDog startup path + BindMode. cellMembrane evolved bidirectional relay. Divergence gap solved at code level, needs deploy on golgi.

---

## You Are Here

You are an agent on a gate in the ecoPrimals ecosystem. This is the single source of truth for all teams. The ecosystem is a **sovereign, self-hosted mesh of compute gates** running 13 Rust primals (NUCLEUS) coordinated via WireGuard overlay + Forgejo.

**Wave 132f milestone**: sporeGate deployed evolved songBird (906fe886) — `http.proxy` routes LIVE, SONGBIRD_PROXY_ROUTES env configured. bearDog deployed (ff18b17f5) but **ACME gateway panics at startup** — `rustls_rustcrypto::provider().install_default()` never called in `beardog-cli` `main()`. cellMembrane evolved (926 tests): bidirectional relay (`relay.absorb()` + `relay.parity()`) merged on Forgejo, pending deploy to golgi. primalSpring now 114 scenarios / 1078 tests with `s_tower_http_gateway` structural validation.

**DEBT FOUND (P1)**:
1. **bearDog `CryptoProvider` missing** — `beardog-cli/src/main.rs` startup path never calls `rustls_rustcrypto::provider().install_default()`. The ACME gateway (`serve_https_gateway`) and ACME client (`build_http_client`) panic via `rustls_provider::assert_installed()`. **Fix**: single line at top of `main()`. Needs flockGate.
2. **bearDog `BindMode::Auto` not merged** — local fix on eastGate (detects Android/abstract sockets) never pushed upstream. Blocks grapheneGate. **Fix**: commit + push from eastGate or flockGate absorb.

**DEBT FOUND (P2)**:
3. **Bidirectional relay not deployed to golgi** — code landed in cellMembrane (fce96e2) but needs deploy to golgi so `relay.absorb()` actually runs on the 15min timer. Needs sporeGate/golgi.
4. **ironGate JupyterHub still NOT STARTED** — backend not deployed, capability not registered. Still the E2E blocker.

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
| **grapheneGate** | ADB (USB) | — | **Portable trust anchor** (Pixel 8a, Tower, cellular relay) |
| **strandGate** | (joining) | — | **CPU compute** (64-core EPYC, STAR alignment) |

---

## Wave 131 Shipped (fossilized)

- **Async freshness**: wave.toml + heads/<gate>.toml — zero cascade conflicts
- **songBird LAN bypass**: `try_lan_direct_connect`, `/proc/net/fib_trie` subnet detect, typed exhaustive dispatch (62+ methods), hot-path allocation elimination, security fail-closed, health honesty
- **bearDog BTSP exchange**: `mesh_join.rs`, bidirectional registry, E2E test, trusted_issuer_registry refactored (826L → 6 modules), dynamic announce
- **primalSpring**: 110 scenarios, 1060 tests, KNOWN_DEBT=0, 9 orphaned scenarios wired
- **cellMembrane**: 913 tests, gateway deployment tooling, KNOWN_MESH_GATES, manifest-first SSH

---

## Forward Work — Deploy + Activate ABG Compute

### Phase 1: Mesh Deploy + Validate — COMPLETE

| Task | Gate | Status |
|------|------|--------|
| ~~Build songBird v0.2.1 with LAN bypass~~ | eastGate | ✅ Built + installed in depot |
| ~~Deploy + restart songBird on eastGate~~ | eastGate | ✅ Running (v0.2.1, mesh initialized) |
| ~~Test LAN `peer.connect` (eastGate → sporeGate)~~ | eastGate | ✅ **CONNECTED** (direct TCP, 0ms) |
| ~~Deploy songBird v0.2.1 to sporeGate~~ | sporeGate | ✅ Built, deployed, running |
| ~~Deploy songBird v0.2.1 to ironGate~~ | ironGate | ✅ Cascade + build + running on :7700 |
| ~~Test LAN `peer.connect` (eastGate ↔ ironGate)~~ | eastGate | ✅ **CONNECTED** (direct TCP, 0ms) |
| ~~Validate `capability.call` cross-gate~~ | eastGate | ✅ eastGate→ironGate, sporeGate→ironGate |
| ~~Wire Caddy → ironGate JupyterHub~~ | sporeGate | ✅ Caddyfile updated + reloaded |
| flockGate WAN peering (golgi relay) | flockGate | **ASSIGNED** to flockGate team |

### Phase 2: Lab Activation (NEXT — gate team work)

| Task | Gate | Assigned To |
|------|------|-------------|
| Deploy JupyterHub on ironGate (localhost:8000) | ironGate | **ironGate team** |
| Register `compute` capability with songBird | ironGate | **ironGate team** (`primal.announce` from barraCuda) |
| Install bioinformatics stack (salmon, STAR, R) | ironGate | **ironGate team** |
| Stage pilot dataset (GSE166686 salmon RNA-seq) | ironGate | **eastGate overwatch** (via mesh transfer) |
| strandGate enrollment (mesh auto-absorb) | strandGate | When hardware arrives |

### Phase 3: ABG Student Onboarding

| Task | Notes |
|------|-------|
| bake3011: Salmon RNA-seq pipeline validated | STAR + DESeq2 + WGCNA on ironGate → strandGate |
| alistaire: CAZyme FEL pipeline validated | GROMACS metadynamics on ironGate (RTX 5070) |
| KinderLab WiFi for student access | Already deployed (guest-isolated, parenting-filtered) |
| lab.primals.eco: landing page + JupyterHub access | Static dashboard live, interactive routes WIRED |

---

## Team Assignments — Wave 132c (Tower HTTP + Living Topology)

| Team | Gate | Handoff | Active Work |
|------|------|---------|-------------|
| **flockGate: songBird IDE** | flockGate | `FLOCKGATE_WAVE132_TOWER_HTTP_GATEWAY` | `http.proxy` method, `http_gateway/` wiring, `ReverseProxyConfig` routes |
| **flockGate: bearDog IDE** | flockGate | `FLOCKGATE_WAVE132_TOWER_HTTP_GATEWAY` | ACME front :443, `HotReloadAcceptor` wire, HTTP-01 solver spawn |
| **flockGate: skunkBat IDE** | flockGate | `FLOCKGATE_WAVE132_TOWER_HTTP_GATEWAY` | `security.scan` advisory on inbound requests |
| **eastGate: petalTongue IDE** | eastGate | `EASTGATE_WAVE132_SPOREPRINT_LIVING_TOPOLOGY` | Wire DataService → songBird `mesh.peers`, live viz, sporePrint page |
| **sporeGate: cellMembrane** | sporeGate | `SPOREGATE_WAVE132_GATEWAY_WIRING` | Deploy evolved binaries, systemd units, shadow validate, retire Caddy |
| **ironGate: compute team** | ironGate | `IRONGATE_WAVE132_COMPUTE_REGISTRATION` | JupyterHub deploy, `jupyter` capability registration, E2E validation |
| **eastGate overwatch** | eastGate | — | Coordinate, monitor divergence, stage pilot data, cascade sync |
| **golgi** | golgi VPS | — | Quorum timer, `unify_freshness()`, relay — no dev work |

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
| ~~ironGate: re-authorize SSH key OR restart WG~~ | ~~P1~~ | ✅ SSH via `irongate` user, mesh peered |
| MikroTik CRS310 credential recovery | P3 | When convenient |
| ironGate: deploy JupyterHub (Docker or systemd) | P2 | Gate team task |

---

## Code Metrics

| Repo | Tests | Status |
|------|-------|--------|
| cellMembrane | 926 | Evolved (bidirectional relay absorb + parity, deploy tooling) |
| primalSpring | 1,078 | Evolved (114 scenarios, s_tower_http_gateway, KNOWN_DEBT=0) |
| barraCuda | 4,619 | Stable |
| coralReef | 3,631 | Stable |
| songBird | 8,929+ | Evolved (http.proxy LIVE on sporeGate) |
| toadStool | 9,171+ | Stable |
| biomeOS | 8,351 | Stable |
| bearDog | 13,866+ | **DEBT**: CryptoProvider panic + BindMode::Auto local |
| skunkBat | 539 | Evolved (security.advisory + dispatch split) |
| sweetGrass | 1,658 | Stable (cargo-deny clean) |
| sporePrint | 220 | Evolved (IPC consolidation, v0.3.1 living topology) |
| petalTongue | 363 | Evolved (mesh.peers wired, /api/mesh-peers) |

---

## Wave 132 Shipped

- **3-gate LAN mesh LIVE**: eastGate ↔ sporeGate ↔ ironGate, bilateral direct TCP, 0ms latency
- **capability.call cross-gate VALIDATED**: eastGate→ironGate, sporeGate→ironGate via mesh HTTP
- **Caddy → ironGate route WIRED**: `lab.primals.eco` paths proxy to ironGate:8000 (pending deploy)
- **guideStone convergence COMPLETE**: All 13 primals 0 ACTIVE / 13 STANDBY (Wave 109 items resolved)
- **bearDog STARTUP-BD-01 RESOLVED**: `BindMode::Auto` now auto-detects Android/abstract platforms
- **songBird deployed to 3 gates**: eastGate, sporeGate, ironGate all running v0.2.1
- **ironGate mesh**: cascade (22/22 synced), build (release), songBird running, firewall opened (7700/tcp + 8000/tcp LAN)

---

## Wave 132c-e Actioned

- **songBird Tower HTTP**: `http.proxy` IPC method + `CapabilityProxyRouter` (env + TOML routes) + `ReverseProxyConfig` with `ProxyRouteEntry` + `capability_router()` getter + MockRemoteGate HTTP test evolution
- **bearDog ACME gateway**: `serve_https_gateway()` (TLS → songBird:7700), `HotReloadAcceptor`, const_oid fix, zero clippy
- **skunkBat security**: `security.advisory` composable IPC + `dispatch_security.rs` split + config hydration + test consolidation
- **petalTongue living topology**: `DataService → mesh.peers` wired, `/api/mesh-peers` endpoint (PeerStatus, transport, latency, caps), `/api/sporeprint` endpoint, dashboard mesh panel + routing flow diagram, 363 tests
- **sporePrint**: v0.3.1 living topology page + v3.1.0 IPC consolidation + toml 1.x upgrade, 220 tests
- **cellMembrane**: 926 tests, bidirectional relay (absorb + parity), gateway deployment tooling
- **grapheneGate LIVE**: Pixel 8a, Tower running via ADB, 14/14 binaries, dual-role tether

---

## Remaining Work — Debt + Integration

### P1 Critical (blocks Tower activation)

| Task | Gate | Status | Fix |
|------|------|--------|-----|
| **bearDog `CryptoProvider` init** | flockGate | **DEBT** | Add `rustls_rustcrypto::provider().install_default()` to `beardog-cli main()` |
| **bearDog `BindMode::Auto` merge** | flockGate | **DEBT** | Absorb eastGate local fix (Android/abstract detect) |
| Deploy JupyterHub on ironGate | ironGate | **NOT STARTED** | FRAGO dispatched to projectNUCLEUS |
| Register `jupyter` capability | ironGate | Pending | JupyterHub deploy |

### P2 Deploy (code exists, needs deploy)

| Task | Gate | Status | Notes |
|------|------|--------|-------|
| Deploy bidirectional relay to golgi | sporeGate/golgi | **NOT DEPLOYED** | cellMembrane fce96e2 has code, needs membrane binary push |
| bearDog :443 ACME cert issuance | sporeGate | Blocked | Needs P1 CryptoProvider fix first |
| Caddy retirement (7-day shadow) | sporeGate | Pending | Shadow starts after ACME works |
| CF_API_TOKEN provision on golgi | golgi | Operator action | One-time, unlocks agentic DNS |

### P3 Validation (can proceed in parallel)

| Task | Gate | Status |
|------|------|--------|
| E2E: browser → bearDog → songBird → ironGate → JupyterHub | All | After P1 + JupyterHub |
| Stage pilot dataset (GSE166686 RNA-seq) | eastGate → ironGate | After JupyterHub |
| grapheneGate songBird mesh.init | grapheneGate | Pending BindMode::Auto |
| flockGate WAN peering via golgi relay | flockGate | Assigned |

---

*Critical path: bearDog CryptoProvider fix → ACME gateway → shadow → Caddy retirement. ironGate JupyterHub is parallel blocker for E2E.*
