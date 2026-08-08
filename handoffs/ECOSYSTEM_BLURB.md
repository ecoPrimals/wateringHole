# ecoPrimals Ecosystem Blurb — Wave 157a DEPLOY READY + Pipeline Audit

**Date**: Aug 7, 2026 9:55PM | **Wave**: 157a | **From**: eastGate overwatch → sporeGate depot ops
**Posture**: **DEPLOY READY. 14/15 PROD-CLEAN. 15/15 CROSS-ARCH.** Depot current on golgi (Musl 17/17, Windows 14/15). **cellMembrane bootstrap gap found and fixed** — cascade timer was running stale `f7d2ac5` (G66), now upgraded to `60b0f8b` (G68 + DIV-7). Pipeline audit: cascade auto-harvests + auto-stages, but doesn't push to golgi.

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

## REMAINING SEQUENCE

1. ~~Phase A: cascade timer~~ — **DONE** (proven, now with G68 membrane)
2. ~~Depot refresh (4 passes)~~ — **DONE** (including cellMembrane bootstrap fix)
3. ~~G68 prod convergence~~ — **14/15 prod-clean**
4. **Phase C: sync graph materialization** — primalSpring team
5. **N2-N5 verification** — primalSpring team (DIV-4 unblocks this)
6. **Deploy across all 6 NUCLEUS gates** — gate teams pull from golgi
7. **toadStool musl VFIO type fix** — toadStool team (S363 regression)
8. **Cascade golgi push automation** — add rsync post-harvest to cascade
9. **Activate springs** — hotSpring, tideGlass, esotericWebb

---

*Wave 157a — DEPLOY READY. 14/15 prod-clean, 15/15 cross-arch. cellMembrane bootstrap gap found and fixed: cascade timer was running stale G66 membrane, now G68+DIV-7. Pipeline audit: cascade auto-harvests + stages locally, but golgi push is manual. toadStool S363 introduced musl VFIO type regression (non-blocking). Depot: musl 17/17, Windows 14/15. Next: gate deployment, then springs.*
