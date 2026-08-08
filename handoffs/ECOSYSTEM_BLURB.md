# ecoPrimals Ecosystem Blurb — Wave 157a DEPLOYED + S366 Convergence

**Date**: Aug 8, 2026 6:50AM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **DEPLOYED. 13/13 ALIVE. 15/16 PROD-CLEAN. 16/16 CROSS-ARCH.** toadStool S366: musl ioctl regression fixed (`as _` cast, aligns with S363 pattern). Socket permissions now permanent (ExecStartPost). Depot: Musl 17/17, Windows **15/15** (squirrel.exe added). Cascade timer: synced=15, zero drift.

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
| toadStool | partial | **7** | 2 | 6 L3 `hw-safe` rustix + 1 L2 selector mode() |

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
9. **toadStool `hw-safe` G68 convergence** — 7 violations (6 L3 rustix + 1 L2 mode), team actively working
10. **Phase C: sync graph materialization** — primalSpring team
11. **Deploy across remaining NUCLEUS gates** — gate teams pull from golgi
12. **Cascade golgi push automation** — rsync/plasmid.push post-harvest
13. **Activate springs** — hotSpring, tideGlass, esotericWebb

---

*Wave 157a — DEPLOYED + S366 CONVERGENCE. 13/13 ALIVE on sporeGate. toadStool musl ioctl regression fixed (S366), socket permissions permanent (ExecStartPost). Depot: Musl 17/17, Windows 15/15 (squirrel.exe added). 15/16 prod-clean, 16/16 cross-arch. Cascade timer: synced=15, zero drift. Wave cadence: targeted primal waves. toadStool hw-safe convergence is the long-tail.*
