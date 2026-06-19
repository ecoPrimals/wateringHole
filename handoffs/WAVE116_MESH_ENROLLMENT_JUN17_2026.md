# Wave 116 — Mesh Enrollment & Gate Parity

**Status**: ACTIVE | **From**: eastGate overwatch | **Date**: 2026-06-17
**Last review**: Jun 18 20:09 EDT (STABLE: 660 tests, primal work assigned to live gates, topology.* LIVE, all VCS at parity)

---

## Objective

Gates are on sovereign relay. Now: full enrollment — SSH, NUCLEUS, mesh parity.
Raise every online gate to the same operational standard as sporeGate (13/13 primals,
systemd persisted, SSH accessible, WireGuard overlay, cascade connected).

---

## Sovereign Relay Status (5/9 migrated, 3 remaining, 1 offline)

| Gate | Relay | Zone | OS | SSH | NUCLEUS | WireGuard | Next Action |
|------|-------|------|----|-----|---------|-----------|-------------|
| **sporeGate** | ✅ Sovereign | backbone | Pop!_OS | ✅ | 13/13 | ✅ (10.13.37.2) | Reference gate — fully enrolled |
| **eastGate** | ✅ Sovereign | backbone | Pop!_OS 22.04 | ✅ | 11/13 | ✅ (10.13.37.5) | **NUCLEUS LIVE** — 11/13 primals, 25 sockets, user systemd. biomeos+nestgate need fixes. |
| **northGate** | ✅ Sovereign | backbone | Windows | — | — | — | P3: hobby, SSH + NUCLEUS after Linux proven |
| **ironGate** | ✅ Sovereign | TBD | TBD | — | — | — | SSH enable, identify hardware, assign team |
| **flockGate** | ✅ Sovereign | WAN | Ubuntu 24.04 | ✅ | — | ✅ (10.13.37.6) | **LIVE on mesh** — 32ms to golgi, 72ms to sporeGate. NUCLEUS deploy next. |
| **strandGate** | ❌ Public | house2 (Omada) | TBD | — | — | — | Operator: push sovereign config |
| **southGate** | ❌ Public | house2 (Omada) | TBD | — | — | — | Operator: push sovereign config |
| **swiftGate** | ❌ Public | house2 (WiFi) | TBD | — | — | — | After Flint 2 live: push sovereign config |
| **fieldGate** | ⬛ Offline | house2 (Omada) | Pop!_OS | — | — | — | Dead CMOS, hardware repair |

---

## Teams & Ownership (3 gates, 4 subteams)

### eastGate — primalSpring Evolution + NUCLEUS (this IDE)

*The science and validation engine. Evolve primalSpring, prove NUCLEUS locally.*

| Focus | Detail |
|-------|--------|
| **primalSpring** | Validation scenarios, evolution modules, genetics compliance, Spring→NUCLEUS integration |
| **NUCLEUS on eastGate** | Deploy 13/13 primals locally, systemd persist, prove the compute gate pattern |
| **Overwatch** | Cascade review, cross-team blurbs, gate parity tracking, impulse management |
| **Ecosystem validation** | Run tests (660 cellMembrane, 75 primalSpring scenarios), catch drift, confirm convergence |

**Immediate work:**
1. NUCLEUS deploy on eastGate (13/13 primals + systemd — script staged, needs sudo)
2. primalSpring scenario expansion (mesh topology validation, gate enrollment posture)
3. Cascade review + blurb coordination across teams

### sporeGate — Two Subteams (both on NUC)

#### sporeGate Overwatch — Hardware, Topology, Integration

*Dedicated subteam (like biomeGate). Owns the physical mesh and gate enrollment.*

| Focus | Detail |
|-------|--------|
| **Gate enrollment** | SSH enable → preflight → NUCLEUS deploy → WG peer on remaining gates |
| **LAN topology** | Omada (standalone L2), CRS310, Flint 2 swap, three-hub triangle backbone |
| **Mesh expansion** | WireGuard overlay admin, peer adds, routing, subnet carving |
| **Hardware integration** | Physical ports, cable runs, AP config, NUC onboarding |
| **Relay migration** | Push sovereign config to strandGate, southGate, swiftGate |

**Immediate work:**
1. NUCLEUS deploy on eastGate (via SSH, once sudo unblocked)
2. NUCLEUS deploy on flockGate (WG live, SSH live — ready now)
3. ironGate OS identification + SSH enable
4. Flint 2 physical swap + config (this weekend)
5. Add flockGate golgi peer (if not done)

#### cellMembrane Team — Code + VPS

*Subteam owns the codebase and VPS infrastructure. Evolves the tooling that overwatch deploys.*

| Focus | Detail |
|-------|--------|
| **cellMembrane code** | Cytoplasm zones, topology.resolve, firewall evolution, gate.* commands, S1-S4 sovereignty |
| **VPS management** | golgi (Forgejo, relay, WG hub), pepti (builds, depot). Fix pepti SSH→forgejo. |
| **Multi-gate support** | Ensure NUCLEUS deploy works identically on all Linux gates |
| **Cascade pipeline** | webhook.rs → GitHub, bidirectional event-driven VCS parity |
| **Fresh binary** | Build from HEAD on pepti, deploy to all gates via overwatch |

**Immediate work:**
1. Fix pepti SSH→forgejo (unblocks fresh binary from HEAD)
2. Cytoplasm zone types in envelope.rs
3. topology.resolve command implementation
4. webhook.rs → GitHub cascade wiring

### flockGate — sporePrint + K-Derm Periplasm Validator (WAN, offsite)

*The WAN proving ground and public face. Owns the website, validates the outer layers.*

| Focus | Detail |
|-------|--------|
| **sporePrint** | Modernize primals.eco (222 pages, many stale). P0: metrics refresh. P1: K-Derm glossary + deployment docs. |
| **K-Derm periplasm** | Only gate testing WG through real WAN, RustDesk relay from offsite, cascade without LAN. |
| **WAN NUCLEUS** | First non-LAN NUCLEUS gate (after sporeGate deploys it). Proves deployment over internet. |
| **Cascade validation** | Every push to Forgejo/GitHub from flockGate proves the outer membrane works. |

**Immediate work:**
1. Await NUCLEUS deploy from sporeGate team (WG + SSH are ready)
2. Begin sporePrint P0: `spore-validate refresh`, fix sitemap count, check links
3. sporePrint P1: glossary refresh (K-Derm terms), SOVEREIGN_DEPLOYMENT.md rewrite
4. Validate cascade: pull all repos via WG overlay, push updates to both remotes

---

## Enrollment Pipeline (sporeGate overwatch executes)

For each gate that's on sovereign relay:

```
1. SSH enable (apt install openssh-server + add sporeGate key)
2. gate.preflight (interface detect, DNS, NM, IP conflict check)
3. membrane binary install (fetch from pepti depot)
4. NUCLEUS deploy (13/13 primals + systemd persist)
5. WireGuard peer (add to golgi hub, assign 10.13.37.X)
6. Cascade connect (git remotes, push/pull verification)
7. Mark ENROLLED in blurb
```

### Immediate Targets (sovereign, need enrollment)

| Gate | Step 1 (SSH) | Step 2 (preflight) | Step 3-7 | Blocker |
|------|-------------|-------------------|----------|---------|
| **eastGate** | ✅ Key authorized | ✅ Probed (i9-12900K, 32GB, 10G) | `enroll.sh` staged at `~/enrollment/` | sudo password (operator) |
| **ironGate** | Pending | — | After SSH | OS identification via RustDesk |
| **flockGate** | ✅ Done | ✅ WG live (32ms golgi, 62ms sporeGate) | NUCLEUS deploy next | — |

---

## Hub 2 WiFi Swap: Eero → GL.iNet Flint 2 (this weekend)

**Problem**: Eero bridge mode collapsed overnight — lost internet for hub 2 WiFi clients.
**Interim**: CAT6 from CRS310 restores wired connectivity now.
**Fix**: Replace Eero with GL.iNet Flint 2 (GL-MT6000). OpenWrt-based, fully controllable.

| Task | Owner | Status |
|------|-------|--------|
| Physical Eero removal + Flint 2 install | operator | This weekend |
| Flint 2 initial config: AP mode, same SSID, bridge to 192.168.4.x | sporeGate overwatch | After install |
| swiftGate connectivity (was on Eero WiFi) → connect to Flint 2 | operator | After AP live |
| Push sovereign relay config to swiftGate | operator + sporeGate | After WiFi restored |
| Omada SDN: update port map for Flint 2 | sporeGate overwatch | After install |

**Flint 2 advantages over Eero**:
- OpenWrt: SSH, full CLI, `nftables`, `dnsmasq`, package manager
- Can run as dumb AP (bridge) without stability issues
- Future: WireGuard client directly on AP, VLAN-tagged WiFi, guest isolation
- Meshable with other GL.iNet devices (Goodcloud or manual WG)

---

## Remaining Relay Migration (operator from northGate)

strandGate, southGate, and swiftGate still on public relay. Operator connects
via public RustDesk, pushes sovereign config:

```
pkexec rustdesk --config "=0nI9E1NWJHc2UnbBlGSU9kbRRnRwUFS1ElcIp3MHZWarE1KWRGRVdVQP5Eb0VnI6ISeltmIsIiI6ISawFmIsIyM4EjLz4CMzIjL3UTMiojI5FGblJnIsIyM4EjLz4CMzIjL3UTMiojI0N3boJye"
```

If pkexec fails, use `sudo` or write config file directly (see RUSTDESK_CONFIG.md).

---

## Infrastructure

| System | Owner | Status |
|--------|-------|--------|
| **golgi** (10.13.37.1) | cellMembrane team | HEALTHY — Forgejo, relay, WG hub, 13/13 |
| **pepti** (10.13.37.4) | cellMembrane team | HEALTHY — build, depot, WG peer |
| **Omada SX3008F** | sporeGate overwatch | **STANDALONE L2** — controller STOPPED (broke port 8). Switch runs unmanaged. |
| **Eero 6** | retiring | **WORKAROUND** — CAT6 direct from CRS310, NAT mode. Replaced by Flint 2 this weekend. |
| **GL.iNet Flint 2** | sporeGate overwatch | **ORDERED** — OpenWrt WiFi 6, AP bridge on hub 2. SSH/root, sovereign. |
| **CRS310** | sporeGate overwatch | L2 backbone (hub 1), pure switching |
| **ATT BGW320** | pending passthrough | Double-NAT still active (P2) |
| **Garage (hub 3)** | planned | Future compute + outdoor WiFi. Wiring/insulation upgrade needed. |

### Topology Evolution: Three-Hub Triangle

```
         House 1 (hub 1)             Target: triangle backbone
        CRS310 + sporeGate           with redundant paths.
       ATT + WiFi (evaluate)         Any single leg failure
          /           \              routes through other two.
    leg A/             \leg B (LIVE, 80m AOC 10G)
        /               \
   Garage (hub 3)----House 2 (hub 2)
   planned          leg C    Omada SX3008F (standalone L2)
                    planned  + GL.iNet Flint 2 (OpenWrt WiFi)
```

**Hardware philosophy**: heterogeneous open. MikroTik (RouterOS), TP-Link (standalone L2), GL.iNet (OpenWrt), ATT (proprietary WAN). No single vendor, no cloud management planes. Diversity forces the primal abstraction to be robust.

---

## Primal Work Assignments (live gates)

Each primal has a role. With gates live, we assign work per primal per gate:

### eastGate — Node + Nest (11/13 active, i9-12900K, 32GB, 10G SFP+)

*Heavy compute gate. Ideal for tensor/shader work, provenance, AI inference.*

| Primal | Atomic | Role | Work Assignment |
|--------|--------|------|-----------------|
| **BearDog** | Tower | Trust & crypto | BTSP key generation, cross-gate bond authentication, family seed management |
| **Songbird** | Tower | Discovery & NAT | Mesh relay for WG overlay, peer discovery across 5-node mesh |
| **SkunkBat** | Tower | Defense & audit | Threat assessment, cascade integrity checks, anomaly detection |
| **ToadStool** | Node | Compute dispatch | Route primalSpring workloads, experiment dispatch, scenario orchestration |
| **BarraCuda** | Node | Tensor & GPU | GPU compute jobs (future: 5090 offload via covalent bond to northGate) |
| **CoralReef** | Node | Shader compilation | Shader pipeline, visualization backend for petalTongue |
| **NestGate** | Nest | Content storage | Local content-addressed blob store, experiment artifacts, scenario results |
| **RhizoCrypt** | Nest | DAG provenance | Commit provenance tracking, rootpulse ledger, cascade verification |
| **LoamSpine** | Nest | Merkle ledger | Sovereign ledger commits, wave state persistence |
| **SweetGrass** | Nest | Attribution | Commit braids, contribution attribution across gates |
| **Squirrel** | Meta | AI inference | primalSpring scenario intelligence, evolution guidance, pattern matching |
| ~~BiomeOS~~ | Meta | Orchestration | BLOCKED — CLI path issue (cellMembrane team P1) |
| ~~NestGate~~ | Nest | Content gates | BLOCKED — `NESTGATE_JWT_SECRET` needed (cellMembrane team P1) |

**Compute focus**: primalSpring evolution, experiment orchestration, provenance trio (rhizoCrypt → BearDog → LoamSpine → sweetGrass).

### sporeGate — Full NUCLEUS (13/13, NUC, site router, plasma membrane)

*Reference gate. Runs the plasma membrane (nftables), DHCP, mesh hub relay.*

| Primal | Work Assignment |
|--------|-----------------|
| **BearDog** | Gate enrollment authentication, BTSP for all inbound bonds |
| **Songbird** | Mesh federation hub, RustDesk relay management |
| **SkunkBat** | Firewall rule validation, intrusion detection, K-Derm membrane integrity |
| **ToadStool** | Dispatch membrane commands to enrolled gates via SSH/WG |
| **BarraCuda** | Binary builds (membrane from HEAD), cross-compile for gate architectures |
| **CoralReef** | Gate health visualization, topology diagram generation |
| **NestGate** | Depot serving (13/13 binaries), content distribution to gates |
| **RhizoCrypt** | Cascade provenance, dehydrate state for rootpulse commits |
| **LoamSpine** | Sovereign ledger authority, wave state commits |
| **SweetGrass** | Attribution for multi-gate code changes, commit braids |
| **BiomeOS** | NUCLEUS orchestration, primal lifecycle, gate.status coordination |
| **Squirrel** | Topology intelligence, zone-aware routing decisions |
| **PetalTongue** | Dashboard visualization, gate.health rendering |

**Infra focus**: membrane generation, gate enrollment, firewall, depot authority, cascade hub.

### flockGate — NUCLEUS pending (WG live, WAN, periplasm prover)

*WAN gate. Proves NUCLEUS works over internet, validates K-Derm outer layers.*

Once NUCLEUS is deployed (sporeGate team, blocked on SSH key):

| Primal | Work Assignment |
|--------|-----------------|
| **Tower trio** | Validate BTSP over WAN (latency-tolerant crypto handshakes) |
| **NestGate** | sporePrint content serving, WAN depot mirror |
| **RhizoCrypt** | WAN cascade provenance (proves outer membrane integrity) |
| **LoamSpine** | Ledger replication over periplasm (golgi → flockGate) |
| **SweetGrass** | Attribution for sporePrint commits (K-Derm layer 2 proof) |
| **Squirrel** | sporePrint content intelligence, stale page detection |
| **BiomeOS** | WAN NUCLEUS lifecycle (first non-LAN orchestration test) |

**Validation focus**: sporePrint content, K-Derm periplasm proof, WAN cascade integrity.

---

## Code Evolution Targets (sporeGate team)

| Item | Priority | Status |
|------|----------|--------|
| Fix pepti SSH→forgejo | **P0** | Still needed — blocks fresh builds from reconciled HEAD |
| eastGate 13/13 (biomeos + nestgate) | **P1** | 11/13 done. biomeos CLI path + nestgate JWT needed |
| flockGate NUCLEUS deploy | **P1** | ✅ UNBLOCKED: SSH key authorized (irongate@pop-os). Deploy via `ssh flockgate@10.13.37.6` |
| ~~Cytoplasm zone types~~ | ~~P2~~ | ✅ SHIPPED — CytoplasmZone enum + struct, topology.resolve |
| ~~Sovereignty ledger~~ | ~~P2~~ | ✅ SHIPPED — rootpulse_commit/verify round-trip |
| webhook.rs → GitHub cascade | P2 | Provider abstraction shipped, wiring pending |
| Omada API client | P3 | Controller STOPPED but switch readable |
| Windows NUCLEUS port | P3 | northGate idle compute — after Linux proven |

---

## Ecosystem Metrics

| Metric | Value |
|--------|-------|
| Gates on sovereign relay | **5/9** (+ 3 pending, 1 offline) |
| Gates fully enrolled | **1/9** (sporeGate: 13/13 + WG + cascade) |
| Gates NUCLEUS-active | **2** — sporeGate (13/13), eastGate (11/13 user systemd) |
| Gates WG-enrolled (NUCLEUS pending) | **1** — flockGate (.6, ready for deploy) |
| WireGuard mesh nodes | **5 live** — golgi(.1), sporeGate(.2), pepti(.4), eastGate(.5), flockGate(.6) |
| cellMembrane tests | **660**, zero warnings, zero clippy |
| VCS parity | **ALL REPOS AT PARITY** — zero drift across origin + forgejo (fixed cellMembrane diverge) |
| membrane tooling | gate.preflight, gate.bootstrap, firewall.generate, gate.status, gate.health, **topology.resolve/zones/mesh** — ALL WORKING |
| Depot x86_64 | 13/13 (pepti behind HEAD — SSH→forgejo fix needed) |
| Fresh binary | Deployed sporeGate + eastGate (f7ecefe → 9c14725). topology.* commands LIVE. |
| Omada controller | **STOPPED** — switch runs standalone L2 (controller broke port 8) |
| Eero status | **RETIRING** — CAT6 workaround from CRS310, NAT mode |
| Flint 2 | **ORDERED** — OpenWrt WiFi 6, replaces Eero this weekend |
| Topology model | **v5.0.0** — three-hub triangle, heterogeneous open hardware |
| Cytoplasm zones | 3 defined (backbone, house2, garage planned) |

---

## Carry (Wave 117+)

| Debt | Owner | Priority |
|------|-------|----------|
| Flint 2 deploy + Eero retire | sporeGate overwatch | **P1** |
| ATT IP passthrough | operator + sporeGate | P2 |
| Hub 1 WiFi evaluation (replace ATT WiFi with OpenWrt AP) | sporeGate overwatch | P2 |
| Garage (hub 3) wiring + insulation | operator | P3 |
| Triangle leg A (house1↔garage) + leg C (garage↔house2) | operator + sporeGate | P3 |
| VLAN segmentation (compute/wifi/guest) | sporeGate overwatch | P3 |
| Version tag hygiene | cellMembrane team | P3 |
| IPv6 with NAT66/PD | sporeGate overwatch | P3 |
| LAN-local hbbs relay | sporeGate overwatch | P3 |
| LLDP auto-zone detection | cellMembrane team | P3 |
