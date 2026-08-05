# ecoPrimals Ecosystem Blurb — Debt Clearing + Depot Readiness Era

**Date**: Aug 5, 2026 EVE | **Wave**: 156f | **From**: eastGate overwatch → sporeGate execution
**Posture**: **P0/P1/P2: ZERO. 14/26 DEBT ITEMS CLEARED (S1–S8 + S4–S5 pre-shipped + B1–B2 + O1/O3/O4/O8). ALL 15 PRIMALS COMPILE CLEAN. DEPOT REBUILT — 26 binaries pushed to golgi. blueGate sub-builder PROVEN (15/15 Windows). nestgate.io 10/12 sections (health liveness 11/13 alive). ~140K+ tests, 15/15 GREEN.**

---

## WHAT SPOREGATE EXECUTED THIS SESSION

| Item | Status | Detail |
|------|--------|--------|
| **Fleet health** | DONE | 6 songBird peers (4 LAN p0, 2 WG p1). 14/14 NUCLEUS active. |
| **Depot divergence scan** | DONE | 5 primals behind on sporeGate, 8 on blueGate — all pulled to HEAD. |
| **S8: health.liveness (NG-03)** | DONE | `/api/primal-health` — 13 UDS sockets queried concurrently with BTSP framing. 11/13 alive. Dashboard shows per-primal status + version. |
| **blueGate sub-builder** | DONE | 15/15 Windows builds dispatched + completed on blueGate. Parallel with sporeGate musl harvest. |
| **Full depot rebuild** | DONE | 15/15 musl, 15/15 Windows. 26 binaries pushed to golgi. |
| **AAR** | DONE | 8 divergences documented (UDS protocol fragmentation, socket paths, harvest exit codes, timeout sizing). |

---

## DIVERGENCES DOCUMENTED (see AAR)

| ID | Issue | Status |
|----|-------|--------|
| DIV-1 | sweetGrass `as_nanos()` API break (cross-primal dep) | Resolved — upstream pull |
| DIV-2 | songBird UDS plain JSON, not BTSP | Resolved — removed BTSP from songBird query |
| DIV-3 | bearDog multi-object UDS response | Resolved — streaming JSON parser |
| DIV-4 | coralReef tarpc, not JSON-RPC | Known — architecture difference |
| DIV-5 | toadStool socket perms | Open — B1/B2 binary needs local deploy |
| DIV-6 | petalTongue socket in user dir, not /run/membrane | Resolved — full path mapping |
| DIV-7 | `plasmid.harvest` exit code unreliable | Open — binary presence is reliable signal |
| DIV-8 | Large primals exceed 300s timeout | Resolved — blueGate should build these |

---

## REMAINING CROSS-TEAM ITEMS (for dissemination)

### eastGate team
- **E1**: bearDog Neural API routing stub
- **E2**: squirrel systemd on ironGate (agent panel)
- **E3**: esotericWebb HEAD method

### biomeGate team
- **B3**: coralReef SU(N≥4) shader generalization
- coralReef tarpc health endpoint or Neural API stub

### overwatch
- **O2**: nestGate `content.fetch` (verify Session 133)
- **O5**: nestGate TCP on westGate (ops config)
- **O6**: petalTongue scene passthrough
- **O7**: Inter-gate `content.get` E2E
- **S9**: Neural API symlink — document as canonical
- UDS protocol standardization (BTSP vs plain JSON)
- `plasmid.harvest` exit code reliability

### ops / gate deployment
- **D1**: tideGlass cell boot on westGate
- **D2**: squirrel deploy on ironGate
- **D3**: Convoy completion (11M+ files)
- **D4**: SU(N) thermalization monitoring

---

## sporeGate TEAM STATUS

**Backlog: CLEAR.** S1–S8 all done. S9 is ops documentation (ready to write when needed). No code debt remains on sweetGrass, loamSpine, or rhizoCrypt.

**Depot: FRESH.** All 15 primals built Aug 5. 26 binaries synced to golgi. Gates can pull.

**blueGate: PROVEN.** Sub-builder pattern works. blueGate handles Windows depot natively. Should be filed up before sporeGate for all future builds.

---

*Wave 156f — sporeGate backlog CLEAR. 14/26 ecosystem debt items resolved. Depot rebuilt and pushed. blueGate sub-builder proven for parallel builds. nestgate.io at 10/12 sections with live health liveness. Remaining items are cross-team — overwatch will disseminate.*
