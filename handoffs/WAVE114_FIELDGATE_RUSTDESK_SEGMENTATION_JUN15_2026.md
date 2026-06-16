# Wave 114 — ABG Sovereign Compute by Friday

**Status**: ACTIVE | Deadline: Friday June 20 | **From**: eastGate overwatch
**Last review**: Jun 16 11:22Z

---

## Objective

Depot deploys to all form factors + primals health-validate via riboCipher.

| Target | Arch | Transport | Status |
|--------|------|-----------|--------|
| **fieldGate** (NUC) | x86_64-musl | LAN via MikroTik | **✅ 13/13 ALIVE** |
| **grapheneGate** (Pixel) | aarch64-musl | LAN/relay | DEPOT READY (device needed) |
| **flockGate** (WAN) | x86_64-musl | relay via golgiBody | PATH PROVEN (target needed) |

---

## Ecosystem Snapshot (Jun 16 11:22Z)

| Metric | Value |
|--------|-------|
| VCS parity | **18/18 ✓** (zero drift) |
| Depot x86_64 | **13/13 BUILT** from HEAD (pepti Jun 16 02:27Z) |
| Depot aarch64 | **13/13 BUILT** on pepti (Jun 15) |
| fieldGate primals | **13/13 ALIVE**, mesh enrolled |
| eastGate live NUCLEUS | **11/11 spawn** from depot (4/11 health-reachable) |
| golgiBody | **FULL GREEN HEALTHY** (all 9 probes OK) |
| RustDesk relay | **EXTERNALLY REACHABLE** (:21115-21117) |
| WAN depot | **HTTPS 200 OK** (membrane.primals.eco) |
| Bidirectional cascade | **WORKING** (confirmed live Jun 16) |

---

## NEW: riboCipher Server-Side Acceptance (P1 — SOFT BLOCKER)

**Discovery**: Jun 16 live NUCLEUS on eastGate — 11/11 primals spawn but 7/11 reject the
`[0xEC, 0x01]` riboCipher prefix, breaking health probes. Fix is mechanical (2 lines at
connection accept per primal).

| Primal | Status | Priority |
|--------|--------|----------|
| beardog | BTSP frame misparse | **P1** (blocks auth) |
| songbird | TLS config + prefix reject | **P1** (blocks federation) |
| rhizocrypt | Rejects prefix | **P1** |
| barracuda | Rejects prefix | P2 |
| loamspine | Rejects prefix | P2 |
| toadstool | Rejects prefix | P2 |
| squirrel | Invalid UTF-8 | P2 |
| sweetgrass | Rejects prefix | P2 |
| coralreef | Passes | ✅ |
| nestgate | Passes | ✅ |
| petaltongue | Passes (UDS) | ✅ |

**Workaround**: `--skip-preflight --no-rollback` + manual `ps` for alive validation.
**AAR**: `handoffs/primalSpring/AAR_WAVE114_EASTGATE_LIVE_NUCLEUS_EXECUTION_JUN16_2026.md`

---

## Remaining Work

### 1. riboCipher Acceptance (all primal teams) — P1

Each primal needs 2-byte prefix consumer at connection accept. Fix pattern in AAR.

### 2. grapheneGate Deployment (ops + cellMembrane)

Depot aarch64 is ready. Needs physical device access to deploy.

### 3. flockGate WAN Validation (cellMembrane)

WAN path proven (2.2 MB/s, HTTPS 200). Needs target gate provisioned.

### 4. ABG Member End-to-End (cellMembrane)

RustDesk relay is live and externally reachable. Needs:
- fieldGate RustDesk client installed
- ABG member connects via relay

---

## cellMembrane Shipped (since last review)

| Commit | What |
|--------|------|
| `fed3335` | Robust bootstrap: systemd units, install phase, secrets, permissions (ALL 7 hurdles) |
| `c032abf` | Mesh retry loop (5x2s), removed --dark-forest, updated docs |

All 7 fieldGate deployment hurdles are now **resolved in code**.

---

## primalSpring Shipped (this session)

| Commit | What |
|--------|------|
| `6190d8e` | `nucleus_launcher validate` subcommand + `s_bootstrap_readiness` scenario (62nd) |
| — | Live NUCLEUS execution: confirmed 11/11 spawn from depot on eastGate |
| — | riboCipher incompatibility diagnosis + AAR filed |

---

## Exit Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | fieldGate (NUC): 13/13 alive + mesh | **✅ DONE** |
| 2 | grapheneGate (Pixel): aarch64 depot + 13/13 | DEPOT READY |
| 3 | flockGate (WAN): relay depot + 13/13 | PATH PROVEN |
| 4 | RustDesk relay operational | **✅ DONE** |
| 5 | ABG member end-to-end | TODO |
| 6 | pepti fresh harvest (both arches) | **✅ DONE** |
| 7 | riboCipher acceptance (≥10/11 primals) | **3/11** — SOFT BLOCKER |

**3/7 cleared. Hard blockers: 0. Soft blocker: riboCipher (mechanical fix per primal).**

---

## Carry (not blocking Wave 114)

| Debt | Owner | Priority |
|------|-------|----------|
| Songbird TLS federation config | songbird | P2 |
| Network segmentation enforcement | cellMembrane | P2 |
| neuralAPI hollow (0 registrations) | biomeOS | P2 |
| Socket naming (family-suffixed) | primalSpring | P2 |
| Webhooks (push-triggered cascade) | cellMembrane | P3/Wave 115 |
