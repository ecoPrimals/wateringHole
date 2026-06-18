# Wave 116 — Mesh Enrollment & Gate Parity

**Status**: ACTIVE | **From**: eastGate overwatch | **Date**: 2026-06-17
**Last review**: Jun 18 10:22 EDT (flockGate LIVE on mesh at 72ms, fresh binary built, eastGate preflight complete)

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
| **eastGate** | ✅ Sovereign | backbone | Pop!_OS 22.04 | ✅ | — | ⏳ (10.13.37.5) | SSH key added, enroll.sh staged, needs sudo |
| **northGate** | ✅ Sovereign | backbone | Windows | — | — | — | P3: hobby, SSH + NUCLEUS after Linux proven |
| **ironGate** | ✅ Sovereign | TBD | TBD | — | — | — | SSH enable, identify hardware, assign team |
| **flockGate** | ✅ Sovereign | WAN | Ubuntu 24.04 | ✅ | — | ✅ (10.13.37.6) | **LIVE on mesh** — 72ms RTT, golgi peer active. NUCLEUS deploy next. |
| **strandGate** | ❌ Public | house2 (Omada) | TBD | — | — | — | Operator: push sovereign config |
| **southGate** | ❌ Public | house2 (Omada) | TBD | — | — | — | Operator: push sovereign config |
| **swiftGate** | ❌ Public | house2 (WiFi) | TBD | — | — | — | After Flint 2 live: push sovereign config |
| **fieldGate** | ⬛ Offline | house2 (Omada) | Pop!_OS | — | — | — | Dead CMOS, hardware repair |

---

## Teams & Ownership

### eastGate — primalSpring Evolution + NUCLEUS + Overwatch (this IDE)

| Focus | Detail |
|-------|--------|
| **primalSpring** | Validation scenarios, evolution modules, genetics compliance |
| **NUCLEUS** | Local primals, atomic model tests, gate readiness, NUCLEUS ON EASTGATE |
| **Overwatch** | Cascade review, cross-team coordination, FRAGO/blurb, gate parity tracking |

### sporeGate Overwatch — Topology Exploration + Gate Enrollment (Cursor on NUC)

*Dedicated subteam: LAN/WAN sovereignty exploration ground.*

| Focus | Detail |
|-------|--------|
| **Gate enrollment** | SSH enable on each sovereign gate → preflight → NUCLEUS deploy → WG peer |
| **Mesh expansion** | WireGuard overlay: add eastGate, ironGate, flockGate as peers |
| **Omada management** | SDN controller, VLAN segmentation, port labeling |
| **Remaining migration** | Investigate strandGate, southGate, swiftGate (still on public) |
| **Fresh binary** | Harvest membrane from pepti with latest (gate.preflight, firewall.generate) |

### cellMembrane Team — Code + VPS (Cursor on sporeGate, separate IDE)

| Focus | Detail |
|-------|--------|
| **cellMembrane code** | Cytoplasm zones types, topology.resolve, Omada API client |
| **VPS management** | golgi (Forgejo, relay), pepti (builds, depot) |
| **Cascade pipeline** | Webhook.rs → GitHub, bidirectional event-driven cascade |
| **Sovereignty shadows** | Evolve S1-S4 tracks |
| **Multi-gate support** | Ensure NUCLEUS deploy works identically on all Linux gates |

### flockGate Team — sporePrint + WAN NUCLEUS + K-Derm Periplasm (WAN, offsite)

*The WAN proving ground. Only gate that validates ALL K-Derm layers end-to-end.*

| Focus | Detail |
|-------|--------|
| **sporePrint** | Modernize 222-page site (stale since March). P0: refresh metrics. P1: K-Derm + glossary. |
| **WAN NUCLEUS** | First non-LAN NUCLEUS gate. 13/13 primals across real internet latency. |
| **K-Derm periplasm** | WG direct to golgi (bypasses plasma membrane). Tests outer membrane + periplasm. |
| **Cascade validation** | Push to Forgejo/GitHub from WAN. Proves cascade works without LAN. |

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
| **flockGate** | ✅ Done | — | WG configured, awaiting golgi peer add | golgi peer add (sporeGate) |

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

## Code Evolution Targets (cellMembrane team)

| Item | Priority | Unblocks |
|------|----------|----------|
| Fresh binary harvest (pepti) | P1 | gate.preflight + firewall.generate on all gates |
| Cytoplasm zone types (envelope.rs) | P2 | Zone-aware preflight + topology.resolve |
| Omada API client | P3 | Programmatic switch management from membrane |
| Windows NUCLEUS port | P3 | northGate idle compute |
| webhook.rs → GitHub cascade | P2 | Bidirectional event-driven VCS parity |

---

## Ecosystem Metrics

| Metric | Value |
|--------|-------|
| Gates on sovereign relay | **5/9** (+ 3 pending, 1 offline) |
| Gates fully enrolled | **1/9** (sporeGate) |
| Gates in enrollment | **2** (eastGate: enroll.sh staged, flockGate: WG configured) |
| WireGuard mesh nodes | **3 live** + 2 pending (golgi, sporeGate, pepti live; eastGate .5 + flockGate .6 pending connect) |
| cellMembrane tests | **539**, zero warnings, zero clippy |
| membrane tooling | gate.preflight, gate.bootstrap, firewall.generate, gate.status, gate.health — ALL WORKING |
| Depot x86_64 | 13/13 (pepti behind HEAD — SSH→forgejo fix needed) |
| VCS parity | 17/17 repos synced |
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
