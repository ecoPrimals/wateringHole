# ecoPrimals Ecosystem Blurb — Wave 157a G68 Refined + Depot Pass 3

**Date**: Aug 7, 2026 9:30PM | **Wave**: 157a | **From**: eastGate overwatch → sporeGate depot ops
**Posture**: **G68: 14/15 PROD-CLEAN. DEPOT CURRENT.** sourDough scanner v2 refined (prod/test split) — sweetGrass + coralReef promoted to G68-prod. sourDough v2 + bingoCube rebuilt on golgi. Phase A cascade timer LIVE.

---

## G68 SCANNER V2 RESULTS — FROM SPOREGATE

Scanner v2 (`1cbac92`) correctly separates production violations from test assertions. Two primals promoted:

| Primal | Scanner v1 | Scanner v2 | Change |
|--------|-----------|-----------|--------|
| sweetGrass | 1 violation | **0 prod** (2 test-only) | `enforcement_mode()` was false positive |
| coralReef | 1 violation | **0 prod** (1 test-only) | `PermissionsExt` in test-only `method_gate.rs` |

**Updated G68 prod compliance: 14/15** (was 12/15). Only toadStool (27 L3 device backends) has real production violations.

---

## DEPOT REFRESH — 3RD PASS

| Primal | Commit | Change | Musl | Windows |
|--------|--------|--------|------|---------|
| **sourDough** | `1cbac92` | Scanner v2 (prod/test split, false positive exclusion) | 3.3MB | 3.0MB |
| **bingoCube** | `87d236d` | Standard crate layout restructure | 11.0MB | 5.4MB |

All fresh on golgi. Previous passes (biomeOS `b3dadf0`, barraCuda `9bb8709`) still current.

---

## DEPOT STATUS ON GOLGI — ALL CURRENT

### Musl — 17/17

All binaries on golgi fresh (Aug 7). All primals at latest Forgejo HEAD.

### Windows — 14/15

14 core primal .exe files on golgi. squirrel sole failure (cross-arch).

---

## HEALTH — 12/13

12 ALIVE on sporeGate NUCLEUS.

| Issue | Owner | Severity |
|-------|-------|----------|
| toadStool `Permission denied` (B1/B2 socket) | biomeGate | P2 |
| biomeOS local `4.56.0` (depot has `4.57.0` + DIV-4) | sporeGate ops | P2 — restart |

---

## REMAINING SEQUENCE

1. ~~Phase A: cascade timer~~ — **DONE** (proven)
2. ~~Depot refresh (3 passes)~~ — **DONE** (barraCuda P0, biomeOS DIV-4, sourDough v2, bingoCube)
3. ~~sweetGrass + coralReef G68 prod fix~~ — **NOT NEEDED** (scanner v2 promoted to G68-prod)
4. **Phase C: sync graph materialization** — primalSpring team
5. **N2-N5 verification** — primalSpring team (DIV-4 unblocks this)
6. **Deploy across all 6 NUCLEUS gates** — gate teams pull from golgi
7. **toadStool L3 device backend traits** — toadStool team (non-blocking)
8. **Activate springs** — hotSpring, tideGlass, esotericWebb

---

*Wave 157a — G68 refined: 14/15 prod-clean (scanner v2 promoted sweetGrass + coralReef). Depot: 3 passes complete, all at Forgejo HEAD. Musl 17/17, Windows 14/15. Phase A cascade timer LIVE. 12/13 ALIVE. Only toadStool has real prod violations (27 L3 device backends). Next: N2-N5 verification, gate deployment, springs.*
