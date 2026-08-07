# ecoPrimals Ecosystem Blurb — Deployment Wave

**Date**: Aug 6, 2026 NIGHT | **Wave**: 156r | **From**: eastGate overwatch → sporeGate depot rebuild
**Posture**: **DEPOT REBUILT. GOLGI UPDATED. DEPLOY.** Musl: 17/17 (15 primals + membrane + launcher). Windows: 8/15 fresh G65 + 7 stale (code errors). sporeGate local: 12/13 ALIVE.

---

## sporeGate EXECUTION COMPLETE

| Step | Status |
|------|--------|
| Pull all 15 primals to G65 HEADs | **DONE** — all verified |
| cellMembrane `f6f1e62` built + pushed | **DONE** (16.1MB) |
| sporeGate musl harvest (15) | **DONE** — 15/15 |
| Deploy to sporeGate NUCLEUS | **DONE** — 14/14 system + petalTongue user |
| petalTongue G65 health evolution | **DONE** — 12/13 alive |
| Push musl depot to golgi | **DONE** — 17/17 fresh Aug 6 |
| blueGate Windows builds | **8/15 fresh** — 7 have code errors |
| Push Windows depot to golgi | **DONE** — 8 fresh G65 pushed |

---

## GOLGI DEPOT — MUSL: COMPLETE, WINDOWS: PARTIAL

### Musl (x86_64-unknown-linux-musl) — 17/17 ALL CURRENT

All 15 primals + membrane + nucleus_launcher on golgi, all Aug 6 timestamps.

### Windows (x86_64-pc-windows-gnu) — 8/15 G65 FRESH

| Built Today | Failed (code errors) |
|-------------|---------------------|
| barraCuda, bearDog, biomeOS, coralReef, songBird, sourDough, sweetGrass, toadStool | bingoCube, loamSpine, nestGate, petalTongue, rhizoCrypt, skunkBat, squirrel |

**Root cause**: `rust-toolchain.toml` files were resolving to MSVC toolchains on blueGate. Fixed with `RUSTUP_TOOLCHAIN=stable-x86_64-pc-windows-gnu` + installing GNU versions of pinned channels (1.93.0, 1.94.0, 1.94.1). The 7 remaining failures are **actual code compilation errors** on Windows (IPC/tarpc modules with unix-only code paths).

**Action**: Code teams should add `#[cfg(unix)]` guards or Windows equivalents for the affected IPC modules.

---

## HEALTH — 12/13 ALIVE

| Primal | Status | Notes |
|--------|--------|-------|
| barracuda | ALIVE | |
| beardog | ALIVE | beardog-default.sock |
| biomeos | ALIVE (v4.56.0) | BTSP signal |
| coralreef | ALIVE | G65 plain JSON-RPC |
| loamspine | ALIVE | |
| nestgate | ALIVE | |
| petaltongue | ALIVE | |
| rhizocrypt | ALIVE (v0.14.17) | |
| skunkbat | ALIVE | Family socket |
| songbird | ALIVE | |
| squirrel | ALIVE (v0.1.0) | |
| sweetgrass | ALIVE | BTSP enforced |
| toadstool | ERROR | B1/B2 socket perms |

---

## DIVERGENCES RESOLVED THIS SESSION

1. **blueGate GNU toolchain**: `rust-toolchain.toml` → MSVC resolution. Fixed with `RUSTUP_TOOLCHAIN` override + GNU channel installs.
2. **G65 transport signal**: BTSP 0xEC 0x01 required by some primals. petalTongue health module updated with BTSP+plain fallback.
3. **cellMembrane stale**: Was Aug 3 on golgi. Rebuilt at `f6f1e62` and pushed.
4. **skunkBat socket volatility**: Family socket at `/run/user/0/biomeos/` disappears on root session expiry. Restart recreates it.

---

## GATE DEPLOYMENT — READY (MUSL)

Gate teams: pull musl binaries from golgi and deploy.

| Gate | Action |
|------|--------|
| **ironGate** | Deploy. Activate downstream springs. |
| **westGate** | Deploy. Enable nestGate TCP (O5). |
| **blueGate** | Deploy 8 fresh Windows + continue fixing 7 compile errors. |
| **southGate** | Re-deploy cephalization baseline. |
| **strandGate** | Deploy when thermalization batch completes. |

---

*Wave 156r — DEPOT REBUILT. Musl 17/17 on golgi. Windows 8/15 fresh (7 code errors for code teams). 12/13 alive on sporeGate. Gate teams: deploy musl.*
