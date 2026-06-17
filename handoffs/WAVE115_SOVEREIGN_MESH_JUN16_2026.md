# Wave 115 — Sovereign Mesh & Gate Hardening

**Status**: ACTIVE | **From**: eastGate overwatch | **Date**: 2026-06-16
**Last review**: Jun 16 22:51 EDT

---

## Objective

Harden what Wave 114 proved. Every gate persists across reboot, every gate
can remote to every other, teams are autonomous and pushing their own evolution.

---

## Team Assignments (TWO-TEAM SPLIT)

| Team | IDE Location | Focus |
|------|-------------|-------|
| **sporeGate** (NUC) | Cursor on sporeGate | LAN hardware: routing, NAT, DHCP, Omada/Eero, RustDesk mesh push, northGate NUCLEUS deploy |
| **cellMembrane** (code+VPS) | Cursor in `gardens/cellMembrane` | cellMembrane code evolution, VPS management (golgi+pepti), cascade pipeline, depot, Forgejo, bootstrap fixes |
| **ironGate** | projectNUCLEUS | ABG compute access, tiers, JupyterHub/toadStool |
| **eastGate** | primalSpring | Overwatch: validate, coordinate, primalSpring evolution |
| **fieldGate** | Autonomous | Currently offline — check power |
| **northGate** | (pending) | Gaming/remote + final NUCLEUS gate |

**Key split**: sporeGate handles the physical LAN layer. cellMembrane IDE handles all code + VPS.
Both co-evolve. sporeGate deploys what cellMembrane builds.

---

## Ecosystem Snapshot (Jun 16 22:51 EDT)

| Metric | Value |
|--------|-------|
| Genetics | **11/11 ✅** all primals accept mito-beacon |
| Depot x86_64 | **13/13** from HEAD (pepti Jun 16) |
| Depot aarch64 | **13/13** (pepti Jun 15) |
| VCS parity | **17/17** zero drift |
| golgi | **HEALTHY** — 13/13, relay ACTIVE, depot serving |
| sporeGate | **13/13 ALIVE** — systemd persisted, 9h uptime, cascade verified |
| fieldGate | **OFFLINE** — was 13/13, unreachable |
| northGate | RustDesk only — NUCLEUS pending |
| RustDesk relay | **MikroTik LAN gates CONNECTED** — Omada towers + flockGate TODO |
| sporeGate autonomy | golgi SSH ✅, pepti SSH ✅, cascade ✅, Forgejo ✅ |

---

## Remaining Work

### sporeGate Team (LAN Hardware)

#### P1: RustDesk Mesh — Push to Remaining Gates

SSH-push relay config. Do NOT manually type on each machine.

- [ ] SSH-push config to Omada-wired towers (192.168.4.x)
- [ ] Verify Omada is pure L2 switch (operator supplies controller password AM)
- [ ] flockGate WAN: apply config via SSH from golgi or current public RustDesk session
- [ ] fieldGate: deploy config when back online

#### P1: northGate NUCLEUS Deploy

Last LAN gate to fully deploy:

- [ ] Verify SSH access from sporeGate
- [ ] Install membrane binary + fetch depot (13/13 x86_64)
- [ ] Start all primals + mesh.init + RustDesk config

#### P2: Eero WiFi Integration

Eeros likely NAT WiFi clients to separate subnet.

- [ ] Determine Eero subnet (bridge mode or separate NAT?)
- [ ] If bridge: switch Eeros to AP-only mode (sporeGate DHCP serves WiFi)
- [ ] If NAT: add routing + hairpin rules on sporeGate for Eero subnet

#### P2: Network Hardening

- [ ] ATT IP passthrough (eliminate double-NAT)
- [ ] CRS310 formalize as pure L2

---

### cellMembrane Team (Code + VPS)

*IDE: Cursor opened in `gardens/cellMembrane`*

#### P1: VPS Management

- [x] SSH access to golgi (157.230.3.183) — VERIFIED
- [x] SSH access to pepti (157.230.209.218) — VERIFIED
- [ ] Consolidate golgi's 3 depot paths → single canonical
- [ ] Replace `deploy_membrane.sh` bash → Rust `plasmid.refresh`
- [ ] Pepti: deploy Tower Atomic for self-validation

#### P1: Cascade Pipeline Evolution

- [ ] Event-driven: Forgejo webhook → sync GitHub
- [ ] Event-driven: GitHub webhook → sync Forgejo (bidirectional)
- [ ] `membrane remote.configure --relay golgi` command (SSH-push automation)
- [ ] Eliminate all manual VCS convergence

#### P1: Bootstrap & Depot Fixes

- [ ] Fix `gate.bootstrap` hang (timeout on missing binary, skip logic)
- [ ] `depot.integrity`: generate checksums.toml for all depot binaries
- [ ] Evolve `plasmid.harvest` for automated multi-arch depot refresh

#### P2: Code Evolution

- [ ] `membrane gate.discover` — scan LAN for SSH-reachable gates
- [ ] `membrane remote.configure` — push any config to discovered gates
- [ ] Improve `gate.status` probe reporting (reduce JSON noise)

---

### ironGate Team (projectNUCLEUS)

#### P2: ABG First Member

- [ ] External user → sovereign relay → NUC → workload (end-to-end)
- [ ] Access tiers enforced (Observer → Operator)
- [ ] Cursor IDE pairing via relay

---

### Shipped (sporeGate confirmed Jun 16 22:48)

- [x] 13/13 primals alive + systemd persisted (membrane-nucleus.target)
- [x] Cascade verified: push/pull both remotes clean
- [x] VPS SSH: golgi confirmed, pepti now confirmed (IP provided)
- [x] RustDesk sovereign relay configured + hairpin fixed
- [x] FAMILY_SEED + secrets installed
- [x] Mesh connected (1 peer reachable: golgiBody)

---

## Shipped This Wave (so far)

| What | Detail |
|------|--------|
| sporeGate FULL ONBOARD | 13/13 systemd persisted, cascade verified, VPS SSH, mesh, secrets |
| RustDesk relay | golgi hbbs/hbbr ACTIVE, hairpin NAT fixed, one-command config |
| MikroTik gates connected | eastGate, northGate, sporeGate all on sovereign relay |
| Team split | sporeGate=LAN hardware, cellMembrane IDE=code+VPS, ironGate=ABG |
| VPS access | sporeGate SSH to golgi + pepti confirmed |
| Dual-channel handoff | USB kit + Git push active |
| Full documentation | AAR, topology, onboarding blurb, FRAGO response from sporeGate |

---

## Carry (Wave 116+)

| Debt | Owner | Priority |
|------|-------|----------|
| ATT passthrough (double NAT) | sporeGate (hardware) | P2 |
| aarch64 fresh harvest | cellMembrane team (pepti) | P2 |
| IPv6 with proper NAT66/PD | sporeGate (hardware) | P3 |
| VLAN segmentation | sporeGate (hardware) | P3 |
| Version tag hygiene | cellMembrane team | P3 |
| Nuclear lineage per-user | bearDog/overwatch | P3 |
| LAN-local hbbs relay | sporeGate (hardware) | P3 |

---

## Architecture

```
Internet → ATT → sporeGate (NAT/FW) → CRS310 (L2) → LAN gates
                  ↕ WiFi (OOB mgmt)              ↕
              golgi VPS (relay/forge)    eastGate, northGate, fieldGate
              pepti VPS (builds)        Omada (L2 switch) → Eeros (WiFi/NAT)
                                        └─ wired towers (192.168.4.x)
                                        └─ WiFi clients (Eero subnet?)
```

**sporeGate team**: LAN hardware, routing, NAT, DHCP, Omada/Eero, gate deploys
**cellMembrane team**: Code evolution, VPS (golgi+pepti), cascade pipeline, depot, Forgejo
**Co-evolution**: sporeGate deploys what cellMembrane builds. Both push to same repos.

RustDesk relay: `157.230.3.183` | One-command config:
```
pkexec rustdesk --config "=0nI9E1NWJHc2UnbBlGSU9kbRRnRwUFS1ElcIp3MHZWarE1KWRGRVdVQP5Eb0VnI6ISeltmIsIiI6ISawFmIsIyM4EjLz4CMzIjL3UTMiojI5FGblJnIsIyM4EjLz4CMzIjL3UTMiojI0N3boJye"
```
