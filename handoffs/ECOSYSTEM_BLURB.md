# ecoPrimals Ecosystem Blurb — Wave 157a G68 Convergence + Long-Tail Debt

**Date**: Aug 7, 2026 6:52PM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **G68 CONVERGING. 5/15 COMPLIANT. TRIAD LIVE.** sourDough validator running. barraCuda on long-tail debt (P0+P1: −37,144 LOC). toadStool L3 backend traits shipped. Phase A cascade timer LIVE on sporeGate. biomeOS Neural API orchestrates everything.

---

## WHAT SHIPPED SINCE LAST BLURB

| Delivered | Team | Impact |
|-----------|------|--------|
| **barraCuda P1 migration** | barraCuda | 225 non-WGSL ops unified, −26,373 LOC. Long-tail debt continuing. |
| **toadStool G68 L2+L3** | toadStool | L2 PermissionsExt migrated. L3 backend traits + hybrid module refactor (S360). |
| **rhizoCrypt G68** | rhizoCrypt | Zero raw platform APIs. L1 `platform_link()` adopted. |
| **loamSpine G68 L2** | loamSpine | PlatformAccess replaces PermissionsExt. |
| **coralReef PLop3 + G68 false positives** | coralReef | AMD RDNA2 predicate logic. 56 L2 reports are GPU texture fields (scanner false positive). |
| **nestGate deep debt S142** | nestGate | Test suite green, installer L2 migration, stale dep removal. |
| **cellMembrane G68** | cellMembrane | Fully isomorphic cross-arch. |
| **Phase A cascade timer** | sporeGate | `membrane temporal.cascade` on 15m systemd timer. LIVE. |
| **barraCuda P0 depot refresh** | sporeGate | Musl 5.6MB, Windows 5.1MB on golgi. |

---

## G68 AUDIT — sourDough VALIDATOR (fresh scan)

`sourdough validate platform-substrate` run against all 15 primals on eastGate:

| Status | Primals | Violations |
|--------|---------|-----------|
| **COMPLIANT** (5) | sourDough, squirrel, nestGate, petalTongue, bingoCube | 0 |
| **L2 only** (8) | barraCuda (4), sweetGrass (5), loamSpine (5), coralReef (9), skunkBat (14), rhizoCrypt (14), bearDog (18), songBird (23) | 92 L2 |
| **L1 + L2** (1) | biomeOS (1 L1 + 49 L2) | 50 |
| **L2 + L3** (1) | toadStool (36 L2 + 27 L3) | 63 |

**Totals**: 205 violations across 10 primals. **L2 (permissions) is 91% of debt.**

Fix pattern: `PermissionsExt::set_mode()` → `PlatformAccess::apply()`

**Cross-arch**: 14/15 PASS. toadStool fails Windows (consumer crate gating — `select_backend` import).

---

## REMAINING WORK — BY OWNER

### Primal Code Teams — G68 Convergence

Each team runs `sourdough validate platform-substrate /path/to/primal` and fixes violations.

| Priority | Primal | Violations | Effort |
|----------|--------|-----------|--------|
| 1 | barraCuda | 4 L2 | Trivial (on long-tail debt, can absorb) |
| 2 | sweetGrass | 5 L2 | Quick |
| 3 | loamSpine | 5 L2 | Quick |
| 4 | coralReef | 9 L2 | Moderate (56 false positives documented as GPU texture fields) |
| 5 | skunkBat | 14 L2 | Moderate |
| 6 | rhizoCrypt | 14 L2 | Moderate |
| 7 | bearDog | 18 L2 | Moderate-heavy |
| 8 | songBird | 23 L2 | Heavy |
| 9 | biomeOS | 1 L1 + 49 L2 | Heaviest (but platform is always Linux — non-blocking) |
| 10 | toadStool | 36 L2 + 27 L3 | L3 backend traits shipped, consumer crate gating remains |

### barraCuda — Long-Tail Debt

barraCuda is on deep debt: P0 (92 WGSL ops, −10,771 LOC) and P1 (225 non-WGSL ops, −26,373 LOC) ComputeDispatch migrations. Combined: **−37,144 LOC across 400+ files.** This is independent of G68 — the 4 L2 violations are trivial absorb-while-working.

### sporeGate

- Phase A: **DONE** — cascade timer LIVE
- Depot refresh: **DONE** (barraCuda P0)
- Next depot refresh after G68 convergence wave

### primalSpring

- Phase C: sync graph materialization (handoff delivered)
- N2-N5 Neural API verification

### Gate Teams — Deploy after G68 depot refresh

| Gate | Status | Next |
|------|--------|------|
| sporeGate | Timer LIVE, depot current | Refresh after G68 convergence |
| eastGate | Dev gate, validator running | primalSpring N2-N5 |
| westGate | 14/14 HEALTHY | Deploy post-G68 |
| strandGate | GPU at 100% QCD | Deploy post-G68 |
| blueGate | Windows builder | Deploy post-G68 |
| ironGate | NUCLEUS | Springs surface |
| southGate | Validation gate | Validates portability |

---

## ORDERING

```
1. G68 primals: fix L2 violations — trivial first (barraCuda, sweetGrass, loamSpine)
   Run: sourdough validate platform-substrate /path/to/primal
2. sporeGate: depot rebuild (post G68 convergence)
3. primalSpring: Phase C sync graphs + N2-N5
4. Gate teams: deploy from golgi depot
5. Springs: tideGlass, hotSpring viz, esotericWebb, arXiv
```

---

## METRICS

| Metric | Value |
|--------|-------|
| G68 compliant (sourDough scanner) | **5/15** (was 3, +petalTongue +bingoCube) |
| G68 violations remaining | **205** across 10 primals (91% L2 permissions) |
| Cross-arch | **14/15 PASS** (toadStool consumer crate gating) |
| barraCuda debt cleared | **−37,144 LOC** (P0+P1 ComputeDispatch) |
| Phase A cascade timer | **LIVE** on sporeGate |
| Glacial goals | **15 COMPLETE / 26 ACTIVE / 23 GLACIAL — 64 total** |
| Total tests | **~140K+** |
| P0/P1 | **ZERO** |

---

*Wave 157a — G68 converging. 5/15 compliant (sourDough, squirrel, nestGate, petalTongue, bingoCube). 205 violations across 10 primals — 91% are L2 permissions (trivial fix pattern). barraCuda on long-tail debt (−37K LOC). toadStool shipped L3 backend traits. Phase A cascade timer LIVE on sporeGate. biomeOS Neural API orchestrates everything.*
