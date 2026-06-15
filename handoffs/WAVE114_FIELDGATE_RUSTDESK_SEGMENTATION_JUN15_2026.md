# Wave 114 — ABG Sovereign Compute by Friday

**Status**: ACTIVE | Deadline: Friday June 20 | **From**: eastGate overwatch
**Last review**: Jun 15 22:17Z (full temporal/sovereignty/glacial)

---

## Objective

Depot deploys to all form factors. Three targets must pass:

| Target | Arch | Transport | Status |
|--------|------|-----------|--------|
| **fieldGate** (NUC) | x86_64-musl | LAN via MikroTik | **✅ 13/13 ALIVE** |
| **grapheneGate** (Pixel) | aarch64-musl | LAN/relay | BLOCKED (cross-compile) |
| **flockGate** (WAN) | x86_64-musl | relay via golgiBody | READY (path proven) |

---

## Ecosystem Snapshot (Jun 15 22:17Z)

| Metric | Value |
|--------|-------|
| VCS parity | **18/18 ✓** (zero drift anywhere) |
| Depot x86_64 | **13/13 BUILT** from HEAD |
| fieldGate primals | **13/13 ALIVE**, mesh enrolled |
| pepti state | OPERATIONAL — repos at HEAD, harvest running |
| Bidirectional cascade | **SHIPPED** (push_target=all) |
| Sovereignty (golgi) | S1-S4 all GREEN |
| Sovereignty (fieldGate) | S4 GREEN, S1-S3 intermittent (LAN routing) |

---

## Remaining Work (4 threads)

### 1. aarch64 Cross-Compile for Pixel (cellMembrane/ironGate)

Toolchain ready on pepti. Just needs harvest run.

| Task | Status |
|------|--------|
| `plasmid.harvest --targets aarch64` on pepti | TODO |
| grapheneGate gate.update with aarch64 binaries | TODO |
| grapheneGate 13/13 alive validation | TODO |

### 2. flockGate WAN Validation (cellMembrane)

WAN path proven (2.2 MB/s). Needs execution.

| Task | Status |
|------|--------|
| gate.fetch via relay (x86_64 depot) | TODO |
| gate.update + 13/13 alive | TODO |

### 3. RustDesk Relay + ABG Access (cellMembrane/ironGate)

| Task | Status |
|------|--------|
| Verify hbbs/hbbr alive on golgiBody-ext (:21115-21117) | TODO |
| fieldGate RustDesk client → relay | TODO |
| ABG member end-to-end via relay | TODO |

### 4. pepti Full Harvest (cellMembrane/ironGate)

| Task | Status |
|------|--------|
| Complete x86_64 harvest (in progress) | IN PROGRESS |
| Run aarch64 harvest | TODO |

---

## fieldGate Deployment Hurdles (cellMembrane evolution debt)

8 issues discovered during first-ant-through. All are bootstrap automation gaps:

| Hurdle | Priority |
|--------|----------|
| Port 8080 collision (songbird + nestgate) | P1 |
| biomeos binary path discovery failure | P1 |
| No systemd units installed by bootstrap | P1 |
| Missing NESTGATE_JWT_SECRET generation | P2 |
| checksums.toml not in depot (phase fails) | P2 |
| /opt/membrane permissions (needs chmod) | P2 |
| mesh.init not called after songbird starts | P2 |
| cellMembrane Forgejo org mismatch | FIXED |

---

## Exit Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | fieldGate (NUC): 13/13 alive + mesh | **✅ DONE** |
| 2 | grapheneGate (Pixel): aarch64 depot + 13/13 | BLOCKED |
| 3 | flockGate (WAN): relay depot + 13/13 | TODO |
| 4 | RustDesk relay + ABG member connects | TODO |
| 5 | pepti fresh harvest (x86 + aarch64) | IN PROGRESS |

**1/5 cleared. Remaining work is execution — no design blockers.**

---

## Carry (not blocking Wave 114)

| Debt | Owner | Priority |
|------|-------|----------|
| Network segmentation enforcement | cellMembrane | P2 |
| neuralAPI hollow (0 registrations) | biomeOS | P2 |
| riboCipher outbound (~5 primals) | per-team | P2 |
| Webhooks (push-triggered cascade) | cellMembrane | P3/Wave 115 |
| Tiered access architecture | long-term | P3 |
| freshness.mesh (songBird distribution) | long-term | P3 |
