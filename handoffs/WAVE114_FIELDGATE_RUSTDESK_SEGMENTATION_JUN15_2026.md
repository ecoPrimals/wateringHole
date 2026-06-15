# Wave 114 — ABG Sovereign Compute by Friday

**Status**: ACTIVE | Deadline: Friday June 20 | **From**: eastGate overwatch

---

## Objective

Depot deploys to all form factors. Three targets must pass:

| Target | Arch | Transport | Status |
|--------|------|-----------|--------|
| **fieldGate** (NUC) | x86_64-musl | LAN direct (eno1 P2P hardwire) | READY |
| **grapheneGate** (Pixel) | aarch64-musl | LAN/relay | BLOCKED (cross-compile) |
| **flockGate** (WAN) | x86_64-musl | relay via golgiBody | READY (path proven) |

---

## State (Jun 15 10:30)

| Metric | Value |
|--------|-------|
| Depot x86_64 | **13/13 BUILT** from HEAD (14:05Z today) |
| VCS parity | **14/14 synced** (origin = forgejo) |
| pepti rebuild | IN PROGRESS (cargo 1.96.0, building) |
| Depot aarch64 | TODO (cross-compile on pepti) |
| RustDesk health probe | **SHIPPED** (bf0c7c3) |
| VCS parity probe | **SHIPPED** (bf0c7c3) |
| toadStool S319 | gRPC + OpenCL DELETED (−458 LOC) |

---

## Remaining Work

### Thread 1: fieldGate NUC Onboarding

NUC is physically adjacent to eastGate. Hardwire via `eno1` (unused onboard NIC) for
ADB-like point-to-point. Static /30, instant SSH, no switch needed.

| Task | Owner | Status |
|------|-------|--------|
| Cable NUC → eastGate eno1, power on | ops | TODO |
| Configure eno1 static IP (/30) | ops | TODO |
| Base OS + SSH accessible | ops | TODO |
| scp membrane + env to fieldGate | cellMembrane | READY |
| `gate.bootstrap --gate fieldGate --profile canary-fieldmouse` | cellMembrane | TODO |
| 13/13 alive + mesh enrolled | cellMembrane | TODO |

### Thread 2: RustDesk Relay + ABG Access

| Task | Status |
|------|--------|
| Verify hbbs/hbbr alive on golgiBody-ext (:21115-21117) | TODO |
| Health probe in gate.status | **DONE** (bf0c7c3) |
| fieldGate RustDesk client → relay | TODO |
| ABG member end-to-end via relay | TODO |

### Thread 3: Pepti Build Authority (cellMembrane debt)

pepti = dedicated build VPS (2 cores, 4GB, 80GB, cargo). **Cannot self-fetch** (no GitHub SSH key, golgi SSH 28s+).

| Task | Status |
|------|--------|
| Deploy key for GitHub (or reliable Forgejo pull) | TODO |
| Investigate pepti↔golgi 28s SSH latency | TODO |
| harvest freshness gate (refuse stale source) | TODO |
| aarch64 cross-compile target | TODO |

### Thread 4: aarch64 for Pixel

| Task | Status |
|------|--------|
| Install aarch64-unknown-linux-musl target on pepti | TODO |
| `plasmid.harvest --targets aarch64` | TODO |
| grapheneGate gate.update with aarch64 binaries | TODO |

---

## Multi-Droplet Architecture

| Droplet | CPU | RAM | Disk | Role |
|---------|-----|-----|------|------|
| **golgi** | 1 | 2GB | 10GB | Forgejo + relay + services (lightweight) |
| **pepti** | 2 | 4GB | 80GB | **Build authority** + depot WAN host |

---

## Per-Gate This Week

| Gate | Role |
|------|------|
| **fieldGate** | Onboarding target (NUC → 13/13) |
| **grapheneGate** | aarch64 validation (Pixel) |
| **flockGate** | WAN validation (relay-only) |
| **pepti** | Build authority — harvests + serves depot |
| **golgi** | Services — Forgejo, relay, mesh hub |
| **eastGate** | Overwatch + pair-program fieldGate |
| **ops** | Physical: cable + power for NUC |

---

## Carry (not blocking close)

| Debt | Owner | Priority |
|------|-------|----------|
| Diderm self-healing (bidirectional push) | cellMembrane | P1 |
| Network segmentation enforcement | cellMembrane | P2 |
| neuralAPI hollow (0 registrations) | biomeOS | P2 |
| riboCipher outbound signal (~5 primals) | per-team | P2 |
| Tiered access architecture | long-term | P3 |
| freshness.mesh (songBird) | long-term | P3 |

---

## Exit Criteria

1. fieldGate: depot pull + bootstrap + 13/13 alive
2. grapheneGate: aarch64 depot pull + update + 13/13 alive
3. flockGate: WAN depot pull via relay + 13/13 alive
4. RustDesk relay operational + health-probed
5. ABG member connects via sovereign path
6. pepti builds from fresh source (no stale harvests)

**Wave 114 closes when depot deploys validated across NUC + Pixel + WAN.**
