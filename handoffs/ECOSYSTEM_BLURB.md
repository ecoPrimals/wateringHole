# ecoPrimals Ecosystem Blurb — Deployment Wave

**Date**: Aug 6, 2026 5:46PM | **Wave**: 156r | **From**: eastGate overwatch
**Posture**: **PRIMALS CLEAR. DEPLOY.** G65 15/15 COMPLETE. C2 15/15 COMPLETE. C8 DONE (-67K). C3 VERIFIED. cellMembrane G65 discovery SHIPPED. **All cephalization work items closed.** This blurb is the deployment handoff. sporeGate golgi: validate depot rebuild. Gate teams: deploy after rebuild confirms.

---

## STATUS — ALL CLEAR

| Milestone | Status |
|-----------|--------|
| Phase 1 (JSON-RPC) | **15/15 COMPLETE** |
| Phase 2 (C2 dual-socket) | **15/15 COMPLETE** |
| Phase 3 (G65 protocol negotiation) | **15/15 COMPLETE** |
| C3 (coralReef health shim) | **VERIFIED** — 3 E2E health tests |
| C8 (squirrel excision) | **DONE** — -67,090 lines, 16→12 crates |
| cellMembrane G65 discovery | **SHIPPED** — `supported_protocols` replaces `has_tarpc` |

---

## DEPOT REBUILD — GOLGI ACTION REQUIRED

**All 15 primals have advanced significantly.** Every primal now ships G65 protocol negotiation on a single UDS socket. The deployed binaries on all gates are pre-cephalization. A full depot rebuild is required before any gate deployment.

### Primal HEADs for rebuild

| Primal | HEAD | G65 | Key changes since last depot |
|--------|------|-----|------------------------------|
| squirrel | `f6667a6` | ORIGIN | C8: -67K lines, 16→12 crates, 4,090 tests |
| sourDough | `d3d125f` | REFERENCE (C7) | G65 reference implementation |
| bearDog | `754b1a9` | SHIPPED | G65 + tarpc 30 methods |
| skunkBat | `c840975` | SHIPPED | G65 + 643 tests |
| bingoCube | `ce4c0ac` | SHIPPED | G65 (v0.3.0) |
| biomeOS | `52f7f9e` | SHIPPED | G65 + Arc\<str\> hot paths |
| songBird | `ec734a7` | SHIPPED | G65 + protocol-transparent routing |
| petalTongue | `507541d` | SHIPPED | G65 + tarpc server module, 6,615 tests |
| nestGate | `262406c` | SHIPPED | G65 Session 139, multi-tier CAS |
| rhizoCrypt | `a269b2c` | SHIPPED | G65 + tarpc UDS, +789 lines |
| sweetGrass | `f1efb27` | SHIPPED | G65 + convergence.pressure backpressure |
| loamSpine | `3361d68` | SHIPPED | G65, tarpc 37 methods (full domain parity) |
| barraCuda | `525674f` | SHIPPED | G65 + libc→rustix (#![forbid(unsafe_code)]) |
| coralReef | `3442282` | SHIPPED | G65 + C3 health verified, 3,689 tests |
| toadStool | `e310f27` | SHIPPED | G65 protocol negotiation |

cellMembrane: `f6f1e62` — G65 discovery evolution.

---

## GATE DEPLOYMENT — AFTER DEPOT REBUILD

| Gate | Action | Priority |
|------|--------|----------|
| **sporeGate** | Deploy + restart all primal services. Verify nestgate.io 13/13 health. | **FIRST** |
| **ironGate** | Deploy. Activate downstream springs. | HIGH |
| **westGate** | Deploy. Enable nestGate TCP (O5). | HIGH |
| **blueGate** | Deploy latest bins. | NORMAL |
| **southGate** | Re-deploy cephalization baseline. | LOW |
| **strandGate** | Deploy when thermalization batch completes. | DEFERRED |

---

## AFTER DEPLOY — SPRINGS + SCIENCE

| # | Item | Gate | Unblocks |
|---|------|------|----------|
| E2 | squirrel systemd on ironGate | ironGate | Agent panel LIVE |
| D1 | tideGlass cell boot | westGate | NF GPS science |
| O5 | nestGate TCP on westGate | westGate | Inter-gate CAS federation |
| O7 | Inter-gate `content.get` E2E | mesh | All data-remote springs |
| O6 | petalTongue scene passthrough | petalTongue | GPS + QCD viz |

### Science (ironGate downstream surface)

| Project | Status | Next |
|---------|--------|------|
| **NF Drug Repurposing** | GPS data on westGate CAS. tideGlass 220 tests. | D1 cell boot → Chen 2017 benchmark |
| **MILC Engine (QCD)** | arXiv 40/42 (95%). Observable battery **69/69 COMPLETE**. | SU(N) data → ironGate viz |
| **esotericWebb** | V31c. 484 tests. Cell boot succeeded. | G19 WebGL pipeline |
| **footPrint** | Phase 2 LIVE. 708 tests. | E2 squirrel → agent panel |

---

## BACKGROUND — CONTINUING INDEPENDENTLY

| Gate | Project | Status |
|------|---------|--------|
| **westGate** | ChunkedBraid 71/153. AlphaFold 1.3 TB. Multi-tier CAS drain. | Running |
| **strandGate** | SU(N) 87-config grid + NPU. arXiv 40/42. Observable battery 69/69. | Running |

---

## CODE OWNERSHIP

| Primary Gate | Primals | G65 |
|-------------|---------|-----|
| **sporeGate** | sweetGrass, loamSpine, rhizoCrypt | 3/3 ✅ |
| **biomeGate** | toadStool, barraCuda, coralReef | 3/3 ✅ |
| **eastGate** | bearDog, squirrel, sourDough, skunkBat, bingoCube | 5/5 ✅ |
| **overwatch** | biomeOS, songBird, nestGate, petalTongue, cellMembrane | 5/5 ✅ |

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| Cephalization | **G65 15/15. C2 15/15. C8 DONE. C3 VERIFIED. COMPLETE.** |
| Gates online | **11** |
| Depot | **REBUILD REQUIRED** |
| squirrel | 190K lines, 12 crates, 4,090 tests |
| Primal tests | ~140,000+ |
| arXiv | 40/42 (95%) |
| Observable battery | 69/69 COMPLETE |
| K-derm | 3/3 FULLY OPERATIONAL |
| Convergence | ChunkedBraid 71/153 |

---

*Wave 156r — **PRIMALS CLEAR. DEPLOY.** G65 15/15. C2 15/15. C8 done (-67K). C3 verified. cellMembrane G65 shipped. All cephalization closed. golgi: rebuild depot with all 15 HEADs above. Gate teams: deploy after rebuild confirms. Then springs + science. Observable battery 69/69. 12 COMPLETE / 26 ACTIVE / 23 GLACIAL. 61 goals. ~140K+ tests, 15/15 GREEN.*
