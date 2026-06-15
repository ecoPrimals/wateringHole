# Wave 114 — ABG Sovereign Compute by Friday

**Status**: ACTIVE | Deadline: Friday June 20 | **From**: eastGate overwatch

---

## Objective

Depot deploys to all form factors. Three targets must pass:

| Target | Arch | Transport | Status |
|--------|------|-----------|--------|
| **fieldGate** (NUC) | x86_64-musl | LAN via MikroTik | **✅ 13/13 ALIVE** (first ant through) |
| **grapheneGate** (Pixel) | aarch64-musl | LAN/relay | BLOCKED (cross-compile) |
| **flockGate** (WAN) | x86_64-musl | relay via golgiBody | READY (path proven) |

---

## State (Jun 15 11:37)

| Metric | Value |
|--------|-------|
| Depot x86_64 | **13/13 BUILT** from HEAD |
| VCS parity | **18/18 synced** (all repos, both remotes) |
| pepti x86_64 harvest | **IN PROGRESS** (building from HEAD) |
| pepti aarch64 toolchain | **READY** (rustup + gcc + linker auto-set) |
| Bidirectional cascade | **SHIPPED** (9dd0cae7 — push_target=all) |
| Harvest freshness gate | **SHIPPED** (369701c — warns on stale source) |
| Depot age probe | **SHIPPED** (c1d1222 — >7d = DEGRADED) |
| RustDesk health probe | **SHIPPED** (bf0c7c3) |
| VCS parity probe | **SHIPPED** (bf0c7c3) |
| toadStool S319 | gRPC + OpenCL DELETED (−458 LOC) |

---

## Remaining Work

### Thread 1: fieldGate NUC Onboarding — ✅ COMPLETE

**13/13 primals alive. Mesh enrolled (1 peer, 1 reachable). First ant through.**

| Task | Owner | Status |
|------|-------|--------|
| NUC on LAN via MikroTik switch (Cat6) | ops | **DONE** |
| SSH from eastGate (192.168.4.36, user fieldgate) | ops | **DONE** |
| membrane binary + env + family key deployed | overwatch | **DONE** |
| gate.bootstrap (7/9 phases auto, 2 manual fixes) | fieldGate team | **DONE** |
| 13/13 alive (biomeos via `api --socket --unix-only`) | fieldGate team | **DONE** |
| Mesh enrolled (songBird → golgiBody :7700) | fieldGate team | **DONE** |
| Workspace + repos (diderm: Forgejo + GitHub) | fieldGate team | **DONE** |

**Deployment time**: ~4 hours (including hurdle discovery + documentation).
**Hurdles**: 8 documented → cellMembrane evolution debt in FRAGO.

### Thread 2: RustDesk Relay + ABG Access

| Task | Status |
|------|--------|
| Verify hbbs/hbbr alive on golgiBody-ext (:21115-21117) | TODO |
| Health probe in gate.status | **DONE** (bf0c7c3) |
| fieldGate RustDesk client → relay | TODO |
| ABG member end-to-end via relay | TODO |

### Thread 3: Pepti Build Authority (cellMembrane/ironGate — MOSTLY RESOLVED)

pepti = dedicated build VPS. **Unblocked**: pulls from Forgejo (264ms), SSH via golgi proxy (1s), aarch64 toolchain ready.

| Task | Owner | Status |
|------|-------|--------|
| SSH access (eastGate → pepti via golgi proxy) | cellMembrane | **DONE** |
| Forgejo latency (was 28s, now 264ms — transient) | cellMembrane | **RESOLVED** |
| Harvest freshness gate (warn on stale source) | cellMembrane | **SHIPPED** (369701c) |
| Depot age probe in gate.status (>7d = DEGRADED) | cellMembrane | **SHIPPED** (c1d1222) |
| aarch64 toolchain (rustup + gcc + linker auto-set) | cellMembrane | **SHIPPED** (3dd403c) |
| Bidirectional cascade (push_target=all) | cellMembrane | **SHIPPED** (9dd0cae7) |
| pepti x86_64 harvest (repos at HEAD, building) | cellMembrane | **IN PROGRESS** |
| pepti aarch64 harvest (for Pixel) | cellMembrane | TODO |

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
| Diderm self-healing (bidirectional push) | cellMembrane | **SHIPPED** (9dd0cae7) |
| Network segmentation enforcement | cellMembrane | P2 |
| neuralAPI hollow (0 registrations) | biomeOS | P2 |
| riboCipher outbound signal (~5 primals) | per-team | P2 |
| Event-driven webhooks (Forgejo push → cascade) | cellMembrane | P3 (Wave 115) |
| Tiered access architecture | long-term | P3 |
| freshness.mesh (songBird) | long-term | P3 |

---

## Exit Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | fieldGate (NUC): depot pull + bootstrap + 13/13 alive | **✅ DONE** |
| 2 | grapheneGate (Pixel): aarch64 depot pull + 13/13 alive | BLOCKED (cross-compile) |
| 3 | flockGate (WAN): depot pull via relay + 13/13 alive | TODO |
| 4 | RustDesk relay operational + health-probed | TODO |
| 5 | ABG member connects via sovereign path | TODO |
| 6 | pepti builds from fresh source (no stale harvests) | IN PROGRESS |

**1/6 exit criteria CLEARED. Wave 114 closes when depot deploys validated across NUC + Pixel + WAN.**
