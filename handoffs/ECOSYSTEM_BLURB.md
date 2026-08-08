# ecoPrimals Ecosystem Blurb — Wave 157a Revalidated

**Date**: Aug 8, 2026 7:01AM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **DEPLOYED + CONVERGING.** toadStool 7→4 prod violations (S366 libc elimination, S367 cross-arch abstraction, mode()→substrate_mode() rename). sweetGrass shipped `capability.call` handler for Neural API routing (gap #2 from AAR). cellMembrane fixed 3 cascade pipeline gaps. Neural API routing spec live. 15/16 prod-clean, 16/16 cross-arch.

---

## EXECUTION SUMMARY — sporeGate/eastGate overwatch

### toadStool S366 — Musl ioctl regression FIXED
- `mmio.rs:191` — `VFIO_DEVICE_GET_REGION_INFO` passed as `c_ulong` to `libc::ioctl` (expects `c_int` on musl)
- The `vfio/ioctls.rs` wrappers already used `as _` casts (S363), but this standalone call in `mmio.rs` was missed
- Fix: single `as _` cast at call site — musl build now clean (1m 21s)
- Committed as S366, pushed to Forgejo (`62643c5`)
- Fresh binary staged to depot (13MB) and pushed to golgi

### toadStool Socket Fix — PERMANENT
- Previous fix: manual `chmod 660 && chgrp sporegate` after each restart — reverted on service restart
- New: `ExecStartPost` in systemd unit applies `chmod 660 + chgrp sporegate` automatically
- Verified: socket now `root:sporegate srw-rw----` after automated restart
- toadStool ALIVE on health check immediately after deploy

### squirrel Windows — 15/15 ACHIEVED
- `squirrel.exe` was missing from golgi Windows depot (14/15 was actual, not 15/15)
- Built on blueGate (`9ef3ca3`, 1m 16s, 3.7MB .exe)
- Pushed to golgi — Windows depot now genuinely **15/15**

### S366 Deployed to NUCLEUS
- Stopped toadStool service, atomic unlink-then-copy from depot to install dir
- Restarted with ExecStartPost socket fix
- Health: **13/13 ALIVE** confirmed

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
| toadStool | partial | **4** | 2 | 4 L3 `hw-safe` rustix (S366+S367 cleared 3) |

**8/16 G68 compliant. 7/16 G68-prod. 1/16 partial. 15/16 zero production violations. 16/16 cross-arch.**

---

## DEPOT STATUS ON GOLGI — ALL CURRENT

### Musl — 17/17
All binaries at Forgejo HEAD including S366 toadStool.

### Windows — 15/15
All 15 primal .exe files on golgi (squirrel.exe added this session).

---

## HEALTH — 13/13 ALIVE

All primals running on sporeGate NUCLEUS. biomeOS 4.57.0 (Stage 2). toadStool S366 deployed, socket fix permanent. Cascade timer: synced=15, zero drift.

---

## CASCADE PIPELINE STATUS

```
Forgejo → cascade fetch → detect drift → auto-harvest → stage to local depot
   ✓           ✓              ✓              ✓                 ✓
```

**Working**: fetch, drift detection, auto-build, local depot staging, G68 membrane
**Gap 1**: Sandbox validation — `composition.test_swap` socket timeout (non-blocking)
**Gap 2**: No golgi push — local depot updated, golgi synced manually
**Gap 3**: `mesh.publish` on songBird — status broadcasting timeout

---

## WAVE CADENCE — TARGETED

Wave 157a ecosystem-wide convergence is **DONE**. Waves are now targeted.

### Completed
1. ~~Phase A: cascade timer~~ — **LIVE**, G68 membrane, zero drift
2. ~~Depot refresh (4 passes + S366)~~ — all at Forgejo HEAD on golgi
3. ~~G68 prod convergence~~ — 15/16 prod-clean, 16/16 cross-arch
4. ~~sporeGate deployment~~ — **13/13 ALIVE**
5. ~~cellMembrane bootstrap fix~~ — cascade runs G68+DIV-7
6. ~~toadStool musl ioctl regression~~ — **S366 FIXED** and deployed
7. ~~toadStool socket permissions~~ — **ExecStartPost permanent**
8. ~~squirrel Windows~~ — **15/15 on golgi**

### Active (long-tail, targeted waves)
9. **toadStool `hw-safe` G68 convergence** — 4 violations remaining (`vfio_setup`, `vfio_dma`, `platform_backends`, `drm_ioctl`), team actively working
10. **Neural API routing fixes** — sweetGrass shipped `capability.call` handler. biomeOS `capability.call` timeout still needs investigation. **Owner: biomeOS.** See `specs/NEURAL_API_ATOMIC_ROUTING_SPEC.md`.
11. **primalSpring registry gaps** — `braid.list`, `braid.query`, `convergence.check`, etc. missing from `capability_registry.toml`. **Owner: primalSpring.**
12. **Evolve native_braid.py → Rust** — last Python in active pipeline. **Owner: cellMembrane or sourDough.**
13. **Phase C: sync graph materialization** — primalSpring team
14. **Deploy across remaining NUCLEUS gates** — gate teams pull from golgi
15. **Activate springs** — hotSpring, tideGlass, esotericWebb

---

*Wave 157a — REVALIDATED. toadStool 7→4 prod violations (S366 libc elimination + S367 cross-arch + mode() rename). sweetGrass shipped capability.call handler. cellMembrane fixed cascade gaps. Neural API routing spec live with wire format reference. 15/16 prod-clean, 16/16 cross-arch. 13/13 ALIVE. toadStool has 4 hw-safe VFIO/DRM violations remaining — converging. westGate absorbs and continues.*
