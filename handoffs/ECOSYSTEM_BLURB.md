# ecoPrimals Ecosystem Blurb — Wave 130

**Date**: Jul 3, 2026 07:30 EDT | **Wave**: 130 | **From**: eastGate overwatch
**Cascade**: All repos at parity. golgi auto-relays every 15min.
**Posture**: Infrastructure hardened. Compute hosting platform ready. ABG integration next.

---

## You Are Here

You are an agent on a gate in the ecoPrimals ecosystem. This is the single source of truth for all teams. The ecosystem is a **sovereign, self-hosted mesh of compute gates** running 13 Rust primals (NUCLEUS) coordinated via WireGuard overlay + Forgejo.

**Major topology shift (Wave 127): sporeGate is no longer the edge router. Flint 2 H1 is the plasma membrane. sporeGate is now a hot-pluggable compute node.**

**Wave 130**: KinderLab WiFi deployed (parenting-filtered, guest-isolated at both sites). Sportsbook DNS blocking live on all networks. Boot persistence hardened. Infrastructure is a platform — any NUC plugs in and gets compute-ready.

**Wave 130b**: ABG compute hosting architecture deployed. sporeGate is the `lab.primals.eco` gateway (Caddy reverse proxy). ironGate is first compute node. strandGate joining this weekend for heavy CPU alignment.

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

### Compute Hosting — lab.primals.eco

```
Internet → lab.primals.eco (DNS: 162.226.225.148)
    → Flint H1 (:443 DNAT) → sporeGate (.3, Caddy reverse proxy)
        → ironGate (.169, 0.2ms): GPU compute, JupyterHub, RTX 5070
        → strandGate (joining): 64-core EPYC, 256GB, STAR alignment
        → future NUCs: plug in, mesh absorbs
```

**Architecture**: sporeGate is the gateway. Compute towers behind it are interchangeable. Caddy routes:
- `/hub/*`, `/user/*`, `/api/*` → ironGate JupyterHub (:8000)
- `/` → static lab dashboard (sporeGate local)
- KinderLab provides safe student WiFi (filtered, isolated from LAN)

**ABG Projects hosted:**
| Project | Workload | Gate | Status |
|---------|----------|------|--------|
| Salmon RNA-seq (bake3011) | STAR alignment, DESeq2, WGCNA | ironGate → strandGate | Pipeline setup |
| CAZyme FEL (Alistaire) | GROMACS metadynamics, GPU FES | ironGate (RTX 5070) | pseudoSpore v1.7.0 ready |

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

## Outer Membrane — Cloudflare (K-Derm Layer)

Cloudflare is the **outer membrane** for all public-facing services (`primals.eco`, `lab.primals.eco`, `git.primals.eco`). DNS management is agentic via `membrane cloudflare.dns.update` — no operator login to dashboard required.

**Architecture**:
```
Internet → Cloudflare (outer membrane, DDoS, TLS edge)
    → Origin: Flint H1 (162.226.225.148) for lab.primals.eco
    → Origin: golgi (157.230.3.183) for membrane.primals.eco, git.primals.eco, primals.eco
```

**cellMembrane `cloudflare.*` module** (shipped Wave 77, operational):
- `membrane cloudflare.dns.list --zone primals.eco`
- `membrane cloudflare.dns.update --zone primals.eco --id <id> --type A --name lab --content 162.226.225.148`
- `membrane cloudflare.cache.purge --zone primals.eco --all`
- `membrane cloudflare.ssl.settings --zone primals.eco`

**Blocker**: `CF_API_TOKEN` needs provisioning on golgi tower.env (operator, one-time). Once deployed, all DNS changes are agentic.

**Long-term**: Cloudflare is transitional outer membrane. Internal transport fully replaces it via BTSP/BirdSong relay (songBird + bearDog = sovereign TLS + sovereign routing). Phase:
1. ✅ Cloudflare manages public DNS (now)
2. ✅ cellMembrane has full Cloudflare API client (shipped)
3. 🔜 CF_API_TOKEN provisioned → DNS becomes agentic
4. 🔜 songBird mesh.init → inter-gate relay operational
5. 🔮 bearDog BTSP + songBird Dark Forest → Cloudflare becomes optional outer cache only

---

## Transport Layer — Replacing SSH with Primal Mesh

Gates communicate via **cellMembrane transport**, NOT SSH:

```
LOCAL:    primal → UDS socket (/run/membrane/<primal>.sock) → JSON-RPC
MESH:     gate → WireGuard overlay (10.13.37.x) → TCP → peer primal
RELAY:    gate → songBird relay.forward → encrypted multi-hop → peer gate
```

**Resolution order** (cellMembrane `resolve.rs`):
1. Local UDS — if capability is on this gate
2. Mesh TCP — via WireGuard overlay
3. Mesh relay — via songBird (for NAT-ed or unreachable peers)

**sporeGate status**: 13/13 primals running, all UDS sockets live in `/run/membrane/`. songBird responds to JSON-RPC. Mesh not yet initialized (`mesh.init` pending on flockGate team).

**ironGate status**: WireGuard overlay not responding (handshake expired or interface down). LAN reachable at .169 (0.2ms). SSH key auth broken (key not in authorized_keys). Needs either:
- RustDesk push: re-authorize sporeGate's ed25519 key, OR
- WireGuard restart + mesh transport activation

**Once mesh is live**: `capability.call` routes computation requests transparently. SSH becomes irrelevant for primal operations. Human operators still use SSH/RustDesk for system administration, but all primal-to-primal traffic flows through sovereign channels.

---

## Coordination

- **Cascade**: push to Forgejo → golgi relays → GitHub. Agentic divergence handles races.
- **Posture**: ABG hosting active. sporeGate Caddy live (:443/:80). Cloudflare outer membrane mapped.
- **Operator actions (one-time, then fully agentic)**:
  1. Provision `CF_API_TOKEN` in golgi `/etc/membrane/tower.env` → unlocks agentic DNS
  2. Via RustDesk: re-authorize sporeGate key on ironGate (`~/.ssh/authorized_keys`) OR restart WG
  3. ironGate: start JupyterHub, create ABG accounts
- **Strategic**: Cloudflare = outer membrane. BirdSong/BTSP = inner transport. SSH → primal mesh migration.
- **Blocked**: ironGate transport (WG down + SSH key broken), strandGate power-on (weekend).

---

## Operator Tasks (resumable)

| Action | Status |
|--------|--------|
| ~~ATT IP Passthrough~~ | ✅ DONE (to Flint) |
| ~~Flint H1 edge router~~ | ✅ DONE (Wave 127) |
| ~~Flint H2 bridge WiFi~~ | ✅ DONE (Wave 121) |
| Provision CF_API_TOKEN on golgi tower.env | P1 — unlocks agentic DNS |
| ironGate: re-authorize SSH key OR restart WG | P1 — unlocks compute node |
| Cloudflare: update lab.primals.eco A → 162.226.225.148 | P1 (agentic once token deployed) |
| MikroTik CRS310 credential recovery | When convenient |
| Flint blocklist persistence (rc.local) | Quick fix when on-site |

---

*Cloudflare is the outer membrane. Primals are the inner transport. SSH is transitional. The mesh absorbs.*
