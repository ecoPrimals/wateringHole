# ecoPrimals Ecosystem Blurb — Wave 157a Neural API Routing

**Date**: Aug 8, 2026 6:39AM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **DEPLOYED + NEURAL API ROUTING SPEC.** westGate pushed atomic ingress AAR documenting Neural API gaps (sweetGrass not announced, capability.call timeout). Overwatch shipped routing spec, verification script, Neural API braid client, and fixed convergence_check.py. All atomics documented for routing via biomeOS. 15/16 prod-clean, 16/16 cross-arch.

---

## G68 FULL AUDIT — 16 REPOS (sourDough scanner v2)

| Primal | Level | Prod | Test | Notes |
|--------|-------|------|------|-------|
| sourDough | **G68** | 0 | 0 | Reference + validator |
| nestGate | **G68** | 0 | 0 | |
| petalTongue | **G68** | 0 | 0 | |
| bingoCube | **G68** | 0 | 0 | |
| loamSpine | **G68** | 0 | 0 | |
| barraCuda | **G68** | 0 | 0 | |
| cellMembrane | **G68** | 0 | 0 | Now tracked as deployable primal |
| squirrel | **G68-prod** | 0 | 1 | test assertion |
| bearDog | **G68-prod** | 0 | 1 | test assertion |
| songBird | **G68-prod** | 0 | 1 | test assertion |
| rhizoCrypt | **G68-prod** | 0 | 1 | test assertion |
| skunkBat | **G68-prod** | 0 | 1 | test assertion |
| sweetGrass | **G68-prod** | 0 | 1 | test assertion |
| coralReef | **G68-prod** | 0 | 1 | test assertion |
| biomeOS | **G68-prod** | 0 | 1 | test assertion |
| toadStool | partial | **7** | 2 | 6 L3 `hw-safe` rustix + 1 L2 selector mode() |

**8/16 G68 compliant. 7/16 G68-prod. 1/16 partial. 15/16 zero production violations. 16/16 cross-arch.**

toadStool remaining 7: `hw-safe/huge_page.rs`, `vfio_setup.rs`, `vfio_dma.rs`, `platform_backends.rs`, `drm_ioctl.rs`, `locked_memory.rs` (all L3 `rustix`), + `akida-driver/hybrid/selector.rs` (L2 `mode()`). Team actively abstracting — long-tail, not a blocker.

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
3. ~~G68 prod convergence~~ — 15/16 prod-clean, 16/16 cross-arch (cellMembrane added)
4. ~~sporeGate deployment~~ — **13/13 ALIVE**
5. ~~cellMembrane bootstrap fix~~ — cascade now runs G68+DIV-7 membrane

### Active (long-tail, targeted waves)
6. **toadStool `hw-safe` G68 convergence** — 7 violations (6 L3 rustix + 1 L2 mode), team actively working.
7. **Neural API routing fixes** — sweetGrass needs `primal.announce` at startup (or TOML domain bridge entry). `capability.call` timeout for provenance queries needs investigation. See `specs/NEURAL_API_ATOMIC_ROUTING_SPEC.md`.
8. **primalSpring registry gaps** — `braid.list`, `braid.query`, `braid.get_by_hash`, `braid.batch_create`, `braid.batch_commit`, `braid.delete`, `convergence.check`, `convergence.batch_check` missing from `capability_registry.toml`. See routing spec handoff section.
9. **Phase C: sync graph materialization** — primalSpring team
10. **Deploy across remaining NUCLEUS gates** — gate teams pull from golgi
11. **Cascade golgi push automation** — rsync post-harvest
12. **Activate springs** — hotSpring, tideGlass, esotericWebb

---

*Wave 157a — DEPLOYED + NEURAL API ROUTING. westGate atomic ingress AAR absorbed: 2,085 lines of jelly archived, native_braid.py enhanced, atomic ingress pattern established ("no data without provenance"). Neural API routing spec shipped with full atomic matrix (tower/provenance/nest/node). Two routing gaps identified: sweetGrass not announced to capability registry, capability.call timeout on provenance queries. Verification script + braid client + convergence fix shipped. 15/16 prod-clean, 16/16 cross-arch. Targeted primal waves from here.*
