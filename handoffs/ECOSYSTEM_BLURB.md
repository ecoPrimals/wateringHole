# ecoPrimals Ecosystem Blurb — Wave 157a DEPLOY READY

**Date**: Aug 7, 2026 9:44PM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **DEPLOY READY. 14/15 PROD-CLEAN. 15/15 CROSS-ARCH.** Depot current on golgi (Musl 17/17, Windows 15/15). toadStool's 24 L3 device violations are acknowledged long-tail — team is actively abstracting into backend traits. No blockers remain. **Wave cadence shifts: targeted primal waves from here, not ecosystem-wide rebuild days.**

---

## G68 SCANNER V2 RESULTS — FROM SPOREGATE

Scanner v2 (`1cbac92`) correctly separates production violations from test assertions. Two primals promoted:

| Primal | Scanner v1 | Scanner v2 | Change |
|--------|-----------|-----------|--------|
| sweetGrass | 1 violation | **0 prod** (2 test-only) | `enforcement_mode()` was false positive |
| coralReef | 1 violation | **0 prod** (1 test-only) | `PermissionsExt` in test-only `method_gate.rs` |

**Updated G68 prod compliance: 14/15** (was 12/15). Only toadStool (24 prod violations — 23 L3 rustix + 1 L2 mode()) has real production violations. biomeOS shipped `64419f6b` clearing all 4 prod violations (platform_boot, boot_logger migrated to query_access/platform_link). toadStool shipped S363 (`cb056fc0e`) fixing Windows cross-arch — 15/15 cross-arch pass.

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

### Windows — 15/15

All 15 primal .exe files pass cross-arch. toadStool S363 fixed `select_backend` gating + `akida device open` migration.

---

## HEALTH — 12/13

12 ALIVE on sporeGate NUCLEUS.

| Issue | Owner | Severity |
|-------|-------|----------|
| toadStool `Permission denied` (B1/B2 socket) | biomeGate | P2 |
| biomeOS local `4.56.0` (depot has `4.57.0` + DIV-4) | sporeGate ops | P2 — restart |

---

## WAVE CADENCE — SHIFT

Wave 157a was an ecosystem-wide convergence day (71+ commits, 16 repos, 3 depot passes). That mode is **done**. From here, waves are **targeted**: a couple primals push, rebuild, deploy. No more constant single-day ecosystem rebuilds.

### Completed (157a)
1. ~~Phase A: cascade timer~~ — **LIVE** on sporeGate
2. ~~Depot refresh (3 passes)~~ — all at Forgejo HEAD on golgi
3. ~~G68 prod convergence~~ — 14/15 prod-clean, 15/15 cross-arch
4. ~~biomeOS G68 clearance~~ — all 4 prod violations resolved
5. ~~toadStool cross-arch~~ — S363 fixed Windows

### Active (long-tail, targeted waves)
6. **toadStool L3 device backend traits** — 24 violations, team actively working. Will push when ready; sporeGate rebuilds + deploys that one primal.
7. **Phase C: sync graph materialization** — primalSpring team
8. **N2-N5 verification** — primalSpring team (DIV-4 unblocks this)
9. **Deploy across all 6 NUCLEUS gates** — gate teams pull from golgi
10. **Activate springs** — hotSpring, tideGlass, esotericWebb

---

*Wave 157a complete — deploy ready. 14/15 prod-clean, 15/15 cross-arch, depot current on golgi (Musl 17/17, Windows 15/15). toadStool's 24 L3 device violations are long-tail — team actively abstracting. No blockers. Wave cadence shifts to targeted primal waves: a couple primals push, one rebuild, one deploy. The ecosystem-wide convergence day is done. Gate teams deploy from golgi. Springs activate when ready.*
