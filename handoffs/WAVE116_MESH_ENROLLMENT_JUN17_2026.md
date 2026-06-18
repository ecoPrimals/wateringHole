# Wave 116 — Mesh Enrollment & Gate Parity

**Status**: ACTIVE | **From**: eastGate overwatch | **Date**: 2026-06-17
**Last review**: Jun 17 19:30 EDT

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
| **eastGate** | ✅ Sovereign | backbone | Pop!_OS | ✅ | — | — | NUCLEUS deploy, WG peer |
| **northGate** | ✅ Sovereign | backbone | Windows | — | — | — | P3: hobby, SSH + NUCLEUS after Linux proven |
| **ironGate** | ✅ Sovereign | TBD | TBD | — | — | — | SSH enable, identify hardware, assign team |
| **flockGate** | ✅ Sovereign | WAN | TBD | — | — | — | SSH enable, WG peer (site-to-site via golgi) |
| **strandGate** | ❌ Public | house2 (Omada) | TBD | — | — | — | Operator: push sovereign config |
| **southGate** | ❌ Public | house2 (Omada) | TBD | — | — | — | Operator: push sovereign config |
| **swiftGate** | ❌ Public | Eero WiFi | TBD | — | — | — | Operator: push sovereign config |
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

| Gate | Step 1 (SSH) | Step 2-7 | Notes |
|------|-------------|----------|-------|
| **eastGate** | ✅ Done | sporeGate executes | 10G compute, primalSpring host |
| **ironGate** | Pending | After SSH | projectNUCLEUS/ABG, reassign when identified |
| **flockGate** | Pending | After SSH | WAN site-to-site, WG through golgi |

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
| **Omada SDN** | sporeGate overwatch | LIVE — 18 clients, 8 SFP+ mapped, VLAN-ready |
| **Eero 6** | bridged (operator) | Flat 192.168.4.x, transparent AP |
| **CRS310** | sporeGate overwatch | L2 backbone, pure switching |
| **ATT BGW320** | pending passthrough | Double-NAT still active (P2) |

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
| WireGuard mesh nodes | **3** (golgi, sporeGate, pepti) |
| cellMembrane tests | **527**, zero warnings |
| Depot x86_64 | 13/13 from HEAD |
| VCS parity | 17/17 repos synced |
| Omada clients visible | 18 |
| Cytoplasm zones | 2 (backbone, house2) + Eero bridged |

---

## Carry (Wave 117+)

| Debt | Owner | Priority |
|------|-------|----------|
| ATT IP passthrough | operator + sporeGate | P2 |
| VLAN segmentation (compute/wifi/guest) | sporeGate overwatch | P3 |
| Version tag hygiene | cellMembrane team | P3 |
| IPv6 with NAT66/PD | sporeGate overwatch | P3 |
| LAN-local hbbs relay | sporeGate overwatch | P3 |
| LLDP auto-zone detection | cellMembrane team | P3 |
