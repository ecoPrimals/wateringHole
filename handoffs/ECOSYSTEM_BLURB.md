# ecoPrimals Ecosystem Blurb — Wave 157a G68 COMPLETE

**Date**: Aug 8, 2026 7:53AM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **16/16 PROD-CLEAN. 16/16 CROSS-ARCH. G68 CONVERGED.** toadStool S368 cleared final 4 hw-safe violations → G68-prod. Every primal and cellMembrane now has zero production G68 violations. 205→0 production violations across Wave 157a. Neural API routing spec live. cellMembrane debt sweep shipped.

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
| toadStool | **G68-prod** | 0 | 2 | **S368 CLEARED** (was 24 at wave start) |

**8/16 G68 compliant. 8/16 G68-prod. 0 partial. 16/16 zero production violations. 16/16 cross-arch.**

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
9. ~~toadStool hw-safe G68~~ — **DONE** (S368 cleared all 4, G68-prod)
10. **Neural API routing** — sweetGrass shipped `capability.call` handler. biomeOS dispatch timeout needs investigation. **Owner: biomeOS.** primalSpring guides compositional evolution and owns capability registry. See `specs/NEURAL_API_ATOMIC_ROUTING_SPEC.md`.
11. **Evolve native_braid.py → Rust** — last Python. Target: `membrane braid.*` CLI. **Owner: cellMembrane.**
12. **Deploy across remaining NUCLEUS gates** — gate teams pull from golgi
13. **Activate springs** — hotSpring, tideGlass, esotericWebb

---

*Wave 157a — G68 COMPLETE. 16/16 prod-clean, 16/16 cross-arch. 205→0 production violations. toadStool S368 cleared final 4 hw-safe violations (S363→S368 across the wave: 24→0). Every primal + cellMembrane at zero production G68 violations. Neural API routing spec live. Next: biomeOS fixes capability.call dispatch, primalSpring evolves compositional routing, cellMembrane evolves native_braid.py to Rust. Gate teams deploy from golgi. Springs activate when ready.*
