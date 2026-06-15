# Wave 114 — ABG Sovereign Compute by Friday

**Status**: ACTIVE | ALL THREADS P1 | Deadline: Friday June 20
**Date**: June 15, 2026
**From**: eastGate overwatch

---

## Driving Objective

Evolve the proven compute path into robust, sovereign, multi-target infrastructure.

**Exit gate**: cellMembrane + plasmidBin depots live and deploying on all form factors:
- **NUC** (fieldGate) — x86_64, LAN 2.5G, canary-fieldmouse profile
- **Pixel** (grapheneGate) — aarch64, mobile/LAN
- **WAN** (flockGate) — x86_64, relay-only via golgiBody

Full validation: depot pull → bootstrap/update → 13/13 alive → health sweep GREEN.

---

## Compliance Snapshot (post-cascade Jun 15 10:00)

| Metric | Score | Notes |
|--------|-------|-------|
| riboCipher accept | ~14/15 | bearDog + toadStool SHIPPED (code) |
| riboCipher signal | 9-10/15 | squirrel full bidirectional, bearDog likely signals |
| health method | ~13/15 | bearDog + toadStool SHIPPED |
| depot (x86_64) | **13/13 BUILT** | plasmidBin rebuilt today (2026-06-15T14:05Z) |
| VCS parity (origin↔forgejo) | **ALL SYNCED** | 14/14 repos pushed Jun 15 |
| toadStool S319 | dead protocol purge | gRPC + OpenCL deleted (−458 lines, 60 files) |
| cellMembrane bf0c7c3 | VCS parity probe + RustDesk health | gate.status now detects drift + relay TCP |

**Critical path resolved**: Depot is **13/13 current from HEAD** (all x86_64 musl).
The blocker was depot builds — **pepti** (build-authority VPS) is now actively
rebuilding a fresh set (redundant validation). Next: aarch64 cross-compile for Pixel.

---

## Remaining Work — Closing Checklist

### 1. Diderm Sync + Depot Rebuild (P1 — THE CRITICAL PATH)

**Owner**: cellMembrane/ironGate
**AAR**: [AAR_DIDERM_CASCADE_STALE_FORGEJO_WAVE114_JUN15_2026.md](AAR_DIDERM_CASCADE_STALE_FORGEJO_WAVE114_JUN15_2026.md)

Forgejo was 49 commits stale — now synced. Depot rebuilt from HEAD.

**First ant through** (unblock this week):

| Task | Status |
|------|--------|
| Sync all 14 repos to forgejo (`git push forgejo main`) | **DONE** (Jun 15) |
| Depot x86_64 rebuilt from HEAD (plasmidBin 13/13) | **DONE** (Jun 15 14:05Z) |
| pepti rebuild (redundant build-authority validation) | IN PROGRESS (building) |
| `plasmid.harvest --targets aarch64` (cross-compile for Pixel) | TODO |
| Verify BLAKE3 checksums match rebuilt binaries | DONE (checksums.toml updated) |

**Evolve and abstract** (cellMembrane self-healing — Wave 115):

| Evolution | Status |
|-----------|--------|
| Bidirectional cascade: detect drift on either remote, push ahead→behind | TODO |
| Event-driven: Forgejo webhook on push-receive triggers cascade | TODO |
| VCS parity in health sweep (drift > 0 = WARN) | **SHIPPED** (bf0c7c3) |
| RustDesk relay TCP health in gate.status | **SHIPPED** (bf0c7c3) |
| No workflow change for gate teams — peptid layer self-heals | TODO |

**Then validate deployment on all three targets:**

| Target | Arch | Transport | Validation |
|--------|------|-----------|------------|
| fieldGate (NUC) | x86_64-musl | LAN 2.5G direct | gate.bootstrap → 13/13 alive |
| grapheneGate (Pixel) | aarch64-musl | LAN/relay | gate.fetch + gate.update → 13/13 alive |
| flockGate (WAN) | x86_64-musl | relay via golgiBody | gate.fetch + gate.update → 13/13 alive |

### 2. fieldGate NUC Onboarding (P1 — ops + cellMembrane/ironGate)

| Task | Owner | Status |
|------|-------|--------|
| NUC physical: rack, power, Cat6e (2.5G) to 10G switch | ops | TODO |
| Base OS (Pop!_OS minimal), SSH from eastGate | ops | TODO |
| `gate.bootstrap --gate fieldGate --profile canary-fieldmouse` | cellMembrane | TODO |
| 13/13 health-alive + songBird mesh enrolled | cellMembrane | TODO |

### 3. RustDesk Relay (P1 — cellMembrane/ironGate)

| Task | Status |
|------|--------|
| Verify hbbs-membrane + hbbr-membrane alive on golgiBody-ext (:21115-21117) | TODO |
| Add relay to cellMembrane health sweep | **SHIPPED** (bf0c7c3 — S2 TCP probe) |
| fieldGate RustDesk client → golgiBody relay | TODO |
| flockGate → relay-only via golgiBody | TODO |
| grapheneGate → LAN P2P when home, relay when away | TODO |

### 4. ABG Compute Access (P1 — cellMembrane/ironGate)

| Task | Status |
|------|--------|
| SSH tunnel: external → golgiBody → fieldGate → workload gate | TODO |
| RustDesk: ABG connects via relay to workload gate | TODO |
| First ABG member validates end-to-end | TODO |

### 5. Network Segmentation (P1 — cellMembrane/ironGate)

| Zone | Routing | Validate |
|------|---------|----------|
| LAN (east, iron, field, north, strand) | Direct mesh, 10G backbone | Depot pull direct |
| WAN (flockGate) | Relay-only via golgiBody | Cannot reach LAN direct |
| Mobile (grapheneGate) | P2P home, relay away | Both paths work |
| Bridge (golgiBody, pepti) | Relay + depot | WAN→LAN forwarding |

---

## Multi-Droplet VPS Architecture

| Droplet | Host | CPU | RAM | Disk | Role |
|---------|------|-----|-----|------|------|
| **golgi** | golgiBody | 1 | 2GB | 10GB | Forgejo, relay, periplasm (lightweight) |
| **golgi-ext** | golgiBody-ext | — | — | — | RustDesk relay (hbbs/hbbr :21115-21117) |
| **pepti** | peptidoglycan | 2 | 4GB | 80GB | **Build authority**, depot host, sync hub |

**pepti** has cargo (1.96.0), full workspace at `/opt/ecoPrimals/`, and 65GB free.
It simulates what a dedicated WAN gate with more power would look like — hosting
depot builds and serving plasmidBin over HTTPS. golgi stays lightweight (services only).

---

## Per-Gate Assignment

| Gate | Role This Week |
|------|----------------|
| **fieldGate** | ONBOARDING — zero to 13/13, depot pull, ABG intake |
| **grapheneGate** | aarch64 depot validation target (Pixel) |
| **flockGate** | WAN depot validation target (relay-only) |
| **ironGate** | cellMembrane: bootstrap, depot rebuild, relay, segmentation |
| **eastGate** | Overwatch: validate, test, coordinate |
| **golgi** | Forgejo, relay bridge, mesh hub (lightweight services) |
| **pepti** | **BUILD AUTHORITY** — depot builds, plasmidBin WAN host |
| **golgi-ext** | RustDesk relay host (hbbs/hbbr :21115-21117) |
| **strandGate/northGate** | Workload targets (ABG science, GPU) |
| **ops** | Physical: fieldGate rack, power, cable, OS |

---

## Resolved This Wave

| Item | Resolution |
|------|-----------|
| 10G backbone | INSTALLED — SFP+ AOC, towers upgrading, NUCs on 2.5G |
| bearDog compliance | 3/3 SHIPPED (riboCipher + health + prefix) — needs depot rebuild |
| toadStool silent socket | FIXED (d1faa877) — health + riboCipher accept shipped |
| toadStool S319 dead protocol purge | gRPC + OpenCL **DELETED** (60 files, −458 LOC) |
| cellMembrane probe_policy | FIXED (047ad49) — probes tolerate transitional primals |
| cellMembrane VCS parity probe | SHIPPED (bf0c7c3) — gate.status detects origin↔forgejo drift |
| cellMembrane RustDesk health | SHIPPED (bf0c7c3) — hbbs/hbbr TCP reachability in S2 probe |
| sync_converge refactor | SHIPPED (443fc6a) — try_pull_converge graduated strategy |
| cellMembrane ext processes | ELIMINATED (94c4261) — pure Rust, capability-driven |
| Forgejo sync (14 repos) | ALL SYNCED (Jun 15) — origin = forgejo parity |
| Depot x86_64 rebuild | **13/13 BUILT** (Jun 15 14:05Z) — all primals from HEAD |
| pepti as build authority | VALIDATED — cargo 1.96.0, 4GB RAM, 80GB disk, building |

---

## Carry (parallel, not blocking close)

| Debt | Owner | Priority |
|------|-------|----------|
| riboCipher outbound signal (remaining ~5 primals) | per-team | P2 |
| neuralAPI capability registration | biomeOS team | P2 |
| Diderm self-healing cascade (P1 evolution, see AAR) | cellMembrane | P1 |
| freshness.mesh via songBird (long-term) | songBird + cellMembrane | P3 |

---

## Exit Criteria

| # | Criterion | How |
|---|-----------|-----|
| 1 | Depot rebuilt from HEAD (x86_64 + aarch64) | plasmid.harvest --all |
| 2 | fieldGate (NUC): depot pull + 13/13 alive | gate.bootstrap + gate.status |
| 3 | grapheneGate (Pixel): depot pull + 13/13 alive | gate.fetch + gate.status |
| 4 | flockGate (WAN): depot pull via relay + 13/13 alive | gate.fetch + gate.status |
| 5 | RustDesk relay operational + health-probed | cellMembrane sweep |
| 6 | ABG member connects via sovereign path | RustDesk or SSH validated |

**Wave 114 closes when depot deploys validated across NUC + Pixel + WAN.**
