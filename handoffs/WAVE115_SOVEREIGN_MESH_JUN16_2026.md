# Wave 115 — Sovereign Mesh & Gate Hardening

**Status**: ACTIVE | **From**: eastGate overwatch | **Date**: 2026-06-16
**Last review**: Jun 16 21:53 EDT

---

## Objective

Harden what Wave 114 proved. Every gate persists across reboot, every gate
can remote to every other, teams are autonomous and pushing their own evolution.

---

## Team Assignments

| Gate | Team | Focus |
|------|------|-------|
| **sporeGate** | cellMembrane owner | LAN routing, cascade, depot, bootstrap, RustDesk mesh |
| **ironGate** | projectNUCLEUS | ABG compute access, tiers, JupyterHub/toadStool |
| **eastGate** | Overwatch | Validate, coordinate, primalSpring evolution |
| **northGate** | (pending onboard) | Gaming/remote + final NUCLEUS gate |
| **fieldGate** | Autonomous | Currently offline — check power |

---

## Ecosystem Snapshot (Jun 16 21:53 EDT)

| Metric | Value |
|--------|-------|
| Genetics | **11/11 ✅** all primals accept mito-beacon |
| Depot x86_64 | **13/13** from HEAD (pepti Jun 16) |
| Depot aarch64 | **13/13** (pepti Jun 15) |
| VCS parity | **17/17** zero drift |
| golgi | **HEALTHY** — 13/13, relay ACTIVE, depot serving |
| sporeGate | **13/13 ALIVE** — routing 11GB+, hairpin NAT fixed |
| fieldGate | **OFFLINE** — was 13/13, unreachable |
| northGate | RustDesk only — NUCLEUS pending |
| RustDesk relay | **ALL LAN GATES CONNECTED** (golgi key deployed) |
| Temporal | Active primals 11-14h old, springs 11h, infra 39min |

---

## Remaining Work

### P1: Gate Persistence (cellMembrane/sporeGate)

Primals on sporeGate/fieldGate run as `nohup` — reboot kills them.

- [ ] Generate systemd units for 13 primals on sporeGate
- [ ] Fix `gate.bootstrap` hang (timeout on missing binary, skip logic)
- [ ] Fill FAMILY_SEED on sporeGate (`/opt/membrane/env`)
- [ ] Deploy fieldGate units when it's back online

### P1: northGate NUCLEUS (cellMembrane/sporeGate)

Last LAN gate to fully deploy:

- [ ] Verify SSH access from sporeGate
- [ ] Install membrane binary
- [ ] Fetch depot (13/13 x86_64)
- [ ] Start all primals + mesh.init
- [ ] Deploy RustDesk systemd persistence

### P2: ABG First Member (ironGate/projectNUCLEUS)

- [ ] External user → sovereign relay → NUC → workload (end-to-end)
- [ ] Access tiers enforced (Observer → Operator)
- [ ] Cursor IDE pairing via relay

### P2: VPS Convergence (cellMembrane/sporeGate)

- [ ] Consolidate golgi's 3 depot paths → single canonical
- [ ] Replace `deploy_membrane.sh` bash → Rust `plasmid.refresh`
- [ ] Pepti: deploy Tower Atomic for self-validation

### P2: Event-Driven Cascade

- [ ] Forgejo webhook → sync GitHub (eliminate manual convergence)
- [ ] GitHub webhook → sync Forgejo (bidirectional)

---

## Shipped This Wave (so far)

| What | Detail |
|------|--------|
| sporeGate live | 13/13, NAT/DHCP/DNS, LAN periplasm operational |
| RustDesk relay fixed | golgi WorkingDir created, key generated |
| Hairpin NAT | eno1→eno1 accept + LAN masquerade (same-NAT relay) |
| eastGate relay | Config fixed (GUI-authoritative pattern learned) |
| northGate relay | Configured, can reach all LAN gates |
| Team restructure | sporeGate owns cellMembrane, ironGate → projectNUCLEUS |
| sporeGate SSH keys | Forgejo + GitHub — can push bidirectionally |
| sporeGate AAR | 8 deployment interventions documented |
| Topology map | TOPOLOGY_LIVE.md + INFRA_LAYERS.toml |
| Network sovereignty | Full architecture documented |

---

## Carry (Wave 116+)

| Debt | Owner | Priority |
|------|-------|----------|
| ATT passthrough (double NAT) | ops + sporeGate | P2 |
| CRS310 → pure L2 | ops + sporeGate | P2 |
| aarch64 fresh harvest | cellMembrane/pepti | P2 |
| IPv6 with proper NAT66/PD | sporeGate | P3 |
| VLAN segmentation | sporeGate | P3 |
| Version tag hygiene | all | P3 |
| Nuclear lineage per-user | bearDog | P3 |
| LAN-local hbbs relay | sporeGate | P3 |

---

## Architecture

```
Internet → ATT → sporeGate (NAT/FW) → CRS310 (L2) → LAN gates
                  ↕ WiFi (OOB mgmt)              ↕
              golgi VPS (relay/forge)    eastGate, northGate, fieldGate
              pepti VPS (builds)        Omada → mesh WiFi clients
```

RustDesk relay: `157.230.3.183` | One-command config:
```
pkexec rustdesk --config "=0nI9E1NWJHc2UnbBlGSU9kbRRnRwUFS1ElcIp3MHZWarE1KWRGRVdVQP5Eb0VnI6ISeltmIsIiI6ISawFmIsIyM4EjLz4CMzIjL3UTMiojI5FGblJnIsIyM4EjLz4CMzIjL3UTMiojI0N3boJye"
```
