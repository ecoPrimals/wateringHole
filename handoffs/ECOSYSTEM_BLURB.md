# ecoPrimals Ecosystem Blurb — Wave 157a DEPLOYED

**Date**: Aug 8, 2026 6:26AM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **DEPLOYED. 13/13 ALIVE. 14/15 PROD-CLEAN. 15/15 CROSS-ARCH.** sporeGate deployed all primals overnight — 13/13 ALIVE, toadStool socket fixed. toadStool shipped S364+S365 (L3 trait surface) — 24→7 prod violations, all in `hw-safe` containment zone. Cascade timer clean, zero drift. Wave cadence shifts to targeted primal waves.

---

## G68 SCANNER V2 RESULTS — FROM SPOREGATE

Scanner v2 (`1cbac92`) correctly separates production violations from test assertions. Two primals promoted:

| Primal | Scanner v1 | Scanner v2 | Change |
|--------|-----------|-----------|--------|
| sweetGrass | 1 violation | **0 prod** (2 test-only) | `enforcement_mode()` was false positive |
| coralReef | 1 violation | **0 prod** (1 test-only) | `PermissionsExt` in test-only `method_gate.rs` |

**G68 prod compliance: 14/15.** toadStool shipped S364 (6 new cross-platform traits) + S365 (G68 complete claim). Scanner shows **7 remaining prod violations** (was 24): 6 `rustix` in `hw-safe` + 1 `mode()` in `akida-driver/hybrid/selector.rs`. Down from 205 at wave start.

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

All primal .exe files pass cross-arch. toadStool S363 fixed Windows, S365 confirmed.

---

## HEALTH — 13/13 ALIVE

All primals running on sporeGate NUCLEUS. toadStool socket permissions fixed. biomeOS upgraded to 4.57.0 (Stage 2). 7 stale impulses cleared. Cascade timer: synced=15, zero drift.

---

## CASCADE PIPELINE AUDIT

The cascade timer (`membrane temporal.cascade`) is more capable than initially documented:

```
Forgejo → cascade fetch → detect drift → auto-harvest → stage to local depot
   ✓           ✓              ✓              ✓                 ✓
```

**Working**: fetch, drift detection, auto-build, local depot staging
**Gap 1**: Sandbox validation fails with `Permission denied` (`composition.test_swap` socket timeout)
**Gap 2**: No golgi push — local depot is updated but golgi must be synced manually
**Gap 3**: `mesh.publish` on songBird times out — status broadcasting broken
**Gap 4 (FIXED)**: cellMembrane bootstrap — cascade ran stale `f7d2ac5` (G66), now `60b0f8b` (G68 + DIV-7)

### cellMembrane Bootstrap Problem

The cascade timer auto-harvests primals but **didn't rebuild itself**. The `membrane` binary in the depot was from Aug 6 (`f7d2ac5`, G66 transport), missing:
- `75953fb` — DIV-7 harvest exit code reliability (3 bugs fixed)
- `60b0f8b` — G68 platform substrate (fully isomorphic cross-arch)

**Fixed**: rebuilt membrane `60b0f8b`, staged to depot, pushed to golgi. Next cascade cycle uses the G68 binary.

### toadStool musl compile divergence

`akida-driver/src/mmio.rs:191` — `VFIO_DEVICE_GET_REGION_INFO` is `u64` on musl but `libc::ioctl` expects `i32`. This is a genuine L3 platform issue in the VFIO device backend. The cascade's auto-harvested binary (from a pre-S363 commit) is deployed; the S363 commit introduced this regression for musl specifically.

---

## WAVE CADENCE — SHIFT

Wave 157a was an ecosystem-wide convergence day (71+ commits, 16 repos, 4 depot passes, full deployment). That mode is **done**. From here, waves are **targeted**: a couple primals push, one rebuild, one deploy.

### Completed (157a)
1. ~~Phase A: cascade timer~~ — **LIVE**, G68 membrane, zero drift
2. ~~Depot refresh (4 passes)~~ — all at Forgejo HEAD on golgi
3. ~~G68 prod convergence~~ — 14/15 prod-clean, 15/15 cross-arch
4. ~~sporeGate deployment~~ — **13/13 ALIVE**
5. ~~cellMembrane bootstrap fix~~ — cascade now runs G68+DIV-7 membrane

### Active (long-tail, targeted waves)
6. **toadStool `hw-safe` G68 convergence** — 7 violations (6 L3 rustix + 1 L2 mode), team actively working. Push when ready, sporeGate rebuilds that one primal.
7. **Phase C: sync graph materialization** — primalSpring team
8. **N2-N5 verification** — primalSpring team
9. **Deploy across remaining NUCLEUS gates** — gate teams pull from golgi
10. **Cascade golgi push automation** — rsync post-harvest
11. **Activate springs** — hotSpring, tideGlass, esotericWebb

---

*Wave 157a — DEPLOYED. 13/13 ALIVE on sporeGate. 14/15 prod-clean, 15/15 cross-arch. toadStool shipped S364+S365 overnight: 24→7 prod violations (all in hw-safe containment). Depot: Musl 17/17, Windows 15/15. Cascade timer clean, zero drift. Wave cadence shifts to targeted primal waves — no more ecosystem-wide convergence days. toadStool converges hw-safe, then sporeGate rebuilds that one primal. Gate teams deploy from golgi. Springs activate when ready.*
