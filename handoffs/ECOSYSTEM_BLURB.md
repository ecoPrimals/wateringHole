# ecoPrimals Ecosystem Blurb — Cephalization Era

**Date**: Aug 6, 2026 5:10PM | **Wave**: 156q | **From**: eastGate overwatch
**Posture**: **CEPHALIZATION PUNCH LIST.** C2 15/15 COMPLETE. G65 9/15. ZERO P0/P1/P2. 15/15 GREEN. skunkBat G65 shipped. This blurb is the remaining work list to fully cephalize all primals + cellMembrane. Once clear, we pivot to deploy + downstream. strandGate + westGate subprojects continue in background.

---

## REMAINING WORK — BY PRIMAL

Every primal and cellMembrane listed with what they need to do to be fully cephalized. Read sourDough (`d3d125f`) as the G65 reference implementation. Read `specs/PROTOCOL_NEGOTIATION_SPEC.md` for the standard.

### G65 DONE (9/15) — no remaining cephalization work

| Primal | HEAD | G65 | Owner | Notes |
|--------|------|-----|-------|-------|
| **squirrel** | `b701c12` | ORIGIN | eastGate | G65 origin (432 lines). **C8 remaining**: ~35K upstream absorption excision (see below). |
| **sourDough** | `d3d125f` | REFERENCE | eastGate | C7 G65 reference implementation DONE. Standards holder. |
| **bearDog** | `754b1a9` | SHIPPED | eastGate | G65 + tarpc 30 methods. grapheneGate. |
| **biomeOS** | `52f7f9e` | SHIPPED | overwatch | G65 + Arc\<str\> hot paths. |
| **petalTongue** | `507541d` | SHIPPED | overwatch | G65 + tarpc server module. 6,615 tests. |
| **nestGate** | `262406c` | SHIPPED | overwatch | G65 Session 139. +758 lines. Multi-tier CAS. |
| **rhizoCrypt** | `a269b2c` | SHIPPED | sporeGate | G65 + tarpc UDS. +789 lines. |
| **sweetGrass** | `f1efb27` | SHIPPED | sporeGate | G65 + `convergence.pressure` backpressure. +495 lines. |
| **skunkBat** | G65 | SHIPPED | eastGate | G65 protocol negotiation. 643 tests. |

### G65 REMAINING (6/15) — each primal implements protocol negotiation independently

| Primal | HEAD | Owner | What's needed | Complexity |
|--------|------|-------|---------------|------------|
| **songBird** | `ab8d174` | overwatch | G65 protocol negotiation on primary UDS. songBird already has tarpc 0.37 + dual-socket (C1a). Add negotiation to JSON-RPC listener. **Also**: songBird gains protocol-transparent cross-gate routing as G65 bonus. | Medium — songBird's routing layer benefits most from G65 |
| **coralReef** | `dcb092a` | biomeGate | **G65 SHIPPED.** Protocol negotiation on UDS. JSON-RPC health shim via G65 backward compat (C3 resolved). 3,686 tests. | **DONE** |
| **barraCuda** | `7e82341` | biomeGate | G65 protocol negotiation. G65 readiness docs already shipped. Has C2 dual-socket + tarpc default. | Low — readiness docs done, just implement |
| **toadStool** | `8fdc98c` | biomeGate | G65 protocol negotiation. **Also C4**: sporeGate ops restart (`sudo systemctl restart membrane-toadstool`) to pick up socket perms fix for nestgate.io 13/13. | Low (code) + ops (restart) |
| **loamSpine** | `96ea990` | sporeGate | G65 protocol negotiation. Already tarpc-CONVERGED (37 methods, full domain parity). tarpc test coverage + UDS E2E just shipped. | Low — most tarpc-mature primal |
| **bingoCube** | `5885d88` | eastGate | G65 protocol negotiation. Just shipped C2 (v0.2.0). | Low — smallest primal |

### cellMembrane — discovery evolution for G65

| Item | HEAD | Owner | What's needed |
|------|------|-------|---------------|
| **cellMembrane** | `6b525d0` | overwatch | Evolve discovery from C2 socket-path tracking to G65 protocol negotiation. `MembraneService.has_tarpc: bool` → `supported_protocols`. Health sweep connects once, negotiates, reports capabilities. systemd units return to single `ExecStart`. Already has tarpc-aware registry (`d533eb2`). |

### C8 — squirrel upstream absorption excision

squirrel's only remaining cephalization work. ~35K lines of songBird/bearDog/toadStool scaffolding not called from production startup path.

| Priority | Target | Lines | Action |
|----------|--------|------:|--------|
| **P1** | `ecosystem/` | 6,497 | EXCISE — `EcosystemManager` immediately discarded in main.rs |
| **P1** | `biomeos_integration/` | 6,365 | EXCISE — only tests reference it |
| **P1** | `compute_client/` + `storage_client/` + `security_client/` | 8,832 | EXCISE — toadStool/bearDog/nestGate client SDKs, zero handler refs |
| **P1** | `primal_provider/` | 4,044 | EXCISE — never instantiated in prod |
| **P1** | `universal/` + `universal_primal_ecosystem/` + `universal_adapter_v2.rs` | 4,582 | EXCISE — duplicates of ecosystem-api traits |
| **P2** | `ecosystem-api` crate | 4,715 | Inline 2 used types, drop crate |
| **P2** | `universal-patterns` (partial) | ~7K | Keep transport/IPC, excise federation/registry/security |
| **P2** | `error_handling/` | 67 | EXCISE — empty module, replaced by `error/` |
| **P3** | `monitoring/` + `observability/` + `metrics/` | 7,850 | Consolidate to one observability module |

squirrel's true domain: AI coordination, tool routing, signal dispatch, G65 RPC, agent panel. Target: ~257K → ~212K.

---

## CEPHALIZATION SCORECARD

| Phase | Status |
|-------|--------|
| ~~Phase 1~~ | JSON-RPC only — **15/15 COMPLETE** |
| ~~Phase 2 (C2)~~ | Dual-socket — **15/15 COMPLETE** |
| **Phase 3 (G65)** | Protocol negotiation — **9/15 shipped, 6 remaining** |
| **C8** | squirrel excision — **~35K lines identified, guidance issued** |
| **cellMembrane** | Discovery evolution — **tarpc-aware registry done, G65-aware pending** |
| **C3** | coralReef JSON-RPC health shim — **RESOLVED** (G65 backward-compat JSON-RPC fallback) |
| **C4** | toadStool deploy restart — **pending (ops)** |
| **Depot rebuild** | All primals advanced — **rebuild needed after G65 closes** |

**When all items above clear: primals are fully cephalized. Pivot to deploy + downstream.**

---

## BACKGROUND — CONTINUING INDEPENDENTLY

| Gate | Project | Status |
|------|---------|--------|
| **westGate** | ChunkedBraid 71/153 braided. AlphaFold 1.3 TB in progress. Multi-tier CAS drain. | Running |
| **strandGate** | SU(N) 87-config grid + NPU. arXiv 40/42 (95%). hotSpring measurement battery. | Running |

---

## DOWNSTREAM (AFTER CEPHALIZATION)

Depot rebuild → gate deployment → springs activation → science.

| Priority | Item | Gate |
|----------|------|------|
| Deploy | Depot rebuild (all primals advanced) | golgi → all gates |
| Deploy | toadStool restart C4 | sporeGate |
| Springs | squirrel systemd E2 | ironGate |
| Springs | tideGlass cell boot D1 | westGate |
| Springs | nestGate TCP O5 | westGate |
| Springs | Inter-gate content.get E2E O7 | mesh |
| Science | NF GPS (tideGlass → petalTongue) | ironGate |
| Science | QCD viz (hotSpring → petalTongue) | ironGate |

---

## CODE OWNERSHIP

| Primary Gate | Primals | G65 Status |
|-------------|---------|------------|
| **sporeGate** | sweetGrass ✅, rhizoCrypt ✅, loamSpine ❌ | 2/3 |
| **biomeGate** | toadStool ❌, barraCuda ❌, coralReef ✅ | 1/3 |
| **eastGate** | bearDog ✅, squirrel ✅, sourDough ✅, skunkBat ✅, bingoCube ❌ | 4/5 |
| **overwatch** | biomeOS ✅, petalTongue ✅, nestGate ✅, songBird ❌, cellMembrane ❌ | 3/5 |

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| Cephalization | **C2 15/15 COMPLETE. G65 9/15. C8 guidance issued. cellMembrane pending.** |
| Gates online | **11** |
| Depot | **REBUILD NEEDED** (all primals advanced — C2 + G65 wave) |
| Primal tests | **~140,000+** |
| arXiv | **40/42 (95%)** — 2 external items remain |
| K-derm | **3/3 FULLY OPERATIONAL** |
| Convergence | **ChunkedBraid 71/153** — AlphaFold in progress |

---

## GLACIAL GOALS — SCORECARD

| Category | Count | IDs |
|----------|-------|-----|
| **COMPLETE** | 12 | G3, G4, G8, G10, G17, G21, G22, G29, G31, G55, G59 |
| **ACTIVE** | 26 | G7, G9, G11, G14, G15, G18, G19, G20, G30, G32, G34, G35, G36–39, G43–45, G53–54, G56–58, G60–62, G64, **G65** |
| **GLACIAL** | 23 | Future phases |
| **Total** | 61 | |

---

*Wave 156q — **Cephalization Punch List.** C2 15/15 COMPLETE. G65 10/15 (squirrel, sourDough, bearDog, biomeOS, petalTongue, nestGate, rhizoCrypt, sweetGrass, skunkBat, coralReef). 5 primals remaining for G65 (songBird, barraCuda, toadStool, loamSpine, bingoCube). cellMembrane G65-aware discovery pending. C8 squirrel ~35K excision guidance issued. C3 RESOLVED. C4 toadStool restart pending. Once clear: deploy rebuild → downstream → science. 12 COMPLETE / 26 ACTIVE / 23 GLACIAL. 61 goals. ~140K+ tests, 15/15 GREEN.*
