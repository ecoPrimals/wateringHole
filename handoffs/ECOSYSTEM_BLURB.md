# ecoPrimals Ecosystem Blurb — G66 Depot Rebuild

**Date**: Aug 6, 2026 NIGHT | **Wave**: 156u | **From**: eastGate overwatch → sporeGate G66 depot
**Posture**: **G66 DEPOT REBUILT. GOLGI UPDATED.** Musl: 16/16 on golgi. Windows: 10/15 fresh G66. sporeGate: 12/13 ALIVE. Three convergence waves deployed in one day.

---

## sporeGate EXECUTION — G66 DEPOT REBUILD

| Step | Status |
|------|--------|
| Pull all 15 + cellMembrane to G66 HEADs | **DONE** |
| Musl harvest (15) + cellMembrane | **DONE** — 16/16 |
| Deploy to sporeGate NUCLEUS | **DONE** |
| petalTongue G66 socket evolution | **DONE** — `ceb92e2` pushed |
| Push musl depot to golgi | **DONE** — 16/16 |
| blueGate Windows builds | **DONE** — 10/15 (5 code errors) |
| Push Windows depot to golgi | **DONE** — 10/10 fresh |

---

## G66 DIVERGENCES

1. **coralReef G66 musl compile**: `crate::ipc` module behind `#[cfg(any(test, feature = "e2e"))]` but `connect_local()` references it unconditionally. **biomeGate action**: export `ipc::transport` types outside test cfg. Running G65 binary.

2. **skunkBat G66 socket path**: Now creates at `/run/membrane/skunkbat.sock` directly (not family-qualified). petalTongue health updated (`ceb92e2`).

3. **Windows compile failures** (5 primals): coralReef, petalTongue, skunkBat, squirrel, toadStool. Unix-only IPC code without `#[cfg(unix)]` guards.

4. **blueGate toolchain**: `RUSTUP_TOOLCHAIN=stable-x86_64-pc-windows-gnu` override required. GNU channels (1.93.0, 1.94.0, 1.94.1) installed.

---

## HEALTH — 12/13

12 ALIVE. toadStool blocked on B1/B2 socket permissions.

---

## GATE DEPLOYMENT — READY

golgi depot updated. Gate teams: pull and deploy.

---

*Wave 156u — G66 DEPOT REBUILT. Musl 16/16. Windows 10/15. 12/13 alive. G64+G65+G66 ALL COMPLETE. Gate teams: deploy.*
