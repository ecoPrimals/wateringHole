# Wave 115 — Sovereign Mesh & Gate Hardening

**Status**: ACTIVE | **From**: eastGate overwatch | **Date**: 2026-06-16
**Last review**: Jun 17 09:30 EDT (cellMembrane deep-debt evolution complete)

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

- [~] Forgejo webhook handler exists (webhook.rs, 440 lines) — push events → local ops. Needs: trigger cascade to GitHub.
- [ ] GitHub → Forgejo sync path (GitHub Actions or webhook endpoint on golgi)
- [ ] Wire bidirectional: any push to either remote cascades to the other
- [ ] Eliminate all manual VCS convergence

#### P1: Bootstrap & Depot Fixes

- [x] Fix `gate.bootstrap` hang — per-phase `tokio::time::timeout(120s)` wrapping ALL phases (permissions, identity, install, nucleus, mobility, mesh, deployment)
- [x] `depot.integrity`: `membrane depot.integrity` command SHIPPED — generates/verifies checksums.toml (BLAKE3) for all depot binaries. IntegrityReport + IntegrityMismatch types. 4 new tests.
- [ ] `plasmid.harvest` multi-arch: flag for cross-compile or multi-builder coordination (pepti=x86_64, need aarch64 path)
- [ ] Consolidate golgi's 3 depot paths → single canonical (prerequisite for checksums)

#### P2: Git Credential Seeding (AAR from sporeGate onboarding)

- [x] `gate.bootstrap` `identity.git` phase: detects missing `git config user.name`/`user.email` + `~/.ssh/id_ed25519`, emits WARNING with actionable message
- [ ] pepti as credential depot: gates fetch identity config on enrollment
- [ ] USB kit include gitconfig fragment for operator manual application

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
- [x] VPS SSH: golgi confirmed, pepti confirmed (IP provided)
- [x] RustDesk sovereign relay configured + hairpin fixed
- [x] FAMILY_SEED + secrets installed
- [x] Mesh connected (1 peer reachable: golgiBody)
- [x] HPC characterization document filed

### Shipped (cellMembrane IDE Jun 17 07:39)

- [x] Deep debt evolution (86e9435): 412 tests passing, 60 net new
- [x] Zero clippy pedantic+nursery, zero fmt, zero doc warnings
- [x] ~70 eprintln! → tracing structured logging
- [x] SPDX headers on all specs + scripts + systemd units
- [x] `ring` banned in deny.toml, cargo-deny CI gate added
- [x] Hardcoded ports/paths → capability-based registry lookups
- [x] ribocipher constants public with ALL arrays
- [x] gate/bootstrap.rs refactored (split extra_exec_args + generate_unit_content)
- [x] All files under 800 LOC, all `as` casts → try_from/millis_u64
- [x] Zero-copy temporal layer (bf54650): Arc manifest, Cow defaults, pre-computed refs
- [x] sporeGate Forgejo remote fixed (HTTPS → SSH, host key added)

---

## cellMembrane Code Evolution SHIPPED (Wave 113–115)

| What | Detail |
|------|--------|
| bootstrap refactor | `gate/bootstrap.rs` 861L → 555L: `nucleus.rs` (228L), `mesh.rs` (138L) extracted |
| spawn_blocking | All sync fs phases (permissions, identity, install, nucleus, mobility, deploy) moved to `spawn_blocking` via `blocking_phase` helper |
| per-phase timeouts | 120s `tokio::time::timeout` on every bootstrap phase |
| identity detection | `identity.git` phase detects missing git config + SSH key |
| depot.integrity | `membrane depot.integrity` command: BLAKE3 checksums generate/verify |
| safe casts | All `as` casts → `usize::try_from()` / `usize::from()` / `.to_le_bytes()[0]` |
| zero .expect() | All production `.expect()` → proper error handling |
| env-driven config | SSH user (`MEMBRANE_PROVISION_SSH_USER`), Caddy admin (`CADDY_ADMIN_ENDPOINT`), config/socket/install paths |
| lint tightening | `option_if_let_else` promoted from allow → warn, all instances resolved |
| zero-copy | `Arc<EcosystemManifest>` in cascade, `Cow<'static, str>` relay defaults, pre-computed remote refs |
| SPDX headers | All .rs, .sh, .md, .service, .timer, .target files carry SPDX license identifier |
| cargo-deny CI | `deny.toml` with ring ban + Forgejo CI job |
| test expansion | 416 → 471 tests (nucleus, mesh, verify, service, types, resolve modules) |
| dependency audit | All pure Rust except ring (via reqwest→rustls), feature-gated, tracked |

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
