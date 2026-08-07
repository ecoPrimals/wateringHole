# ecoPrimals Ecosystem Blurb — Deployment Wave

**Date**: Aug 6, 2026 8:15PM | **Wave**: 156s | **From**: eastGate overwatch
**Posture**: **MUSL DEPOT COMPLETE. DEPLOY GATES.** 17/17 musl on golgi (15 primals + membrane + launcher). sporeGate: 12/13 alive (toadStool B1/B2 perms). Windows: 8/15 fresh — 7 primals need `#[cfg(unix)]` guards for cross-arch. Gate teams: deploy musl now. Code teams: fix Windows after.

---

## DEPOT STATUS

| Target | Binaries | Status |
|--------|----------|--------|
| **x86_64-unknown-linux-musl** | **17/17** | COMPLETE on golgi. All Aug 6. Deploy. |
| **x86_64-pc-windows-gnu** | **8/15** | 7 primals have unix-only IPC code |

---

## sporeGate HEALTH — 12/13 ALIVE

| Primal | Status | Notes |
|--------|--------|-------|
| barracuda | ALIVE | Plain JSON-RPC |
| beardog | ALIVE | beardog-default.sock |
| biomeos | ALIVE (v4.56.0) | BTSP signal |
| coralreef | ALIVE | G65 plain JSON-RPC |
| loamspine | ALIVE | BTSP fallback |
| nestgate | ALIVE | BTSP fallback |
| petaltongue | ALIVE | G65 health fix `6c47ae0` |
| rhizocrypt | ALIVE (v0.14.17) | BTSP fallback |
| skunkbat | ALIVE | Family socket + BTSP |
| songbird | ALIVE | BTSP fallback |
| squirrel | ALIVE (v0.1.0) | BTSP fallback |
| sweetgrass | ALIVE | BTSP enforced |
| **toadstool** | **ERROR** | **B1/B2 socket perms — root-only** |

---

## TWO TRACKS — PARALLEL

### Track 1: GATE DEPLOYMENT (musl — NOW)

Musl depot is complete. Gate teams deploy immediately.

| Gate | Action | Priority |
|------|--------|----------|
| **sporeGate** | DEPLOYED. 12/13. toadStool needs B1/B2 perm fix. | DONE (minus B1/B2) |
| **ironGate** | Pull musl from golgi. Deploy. Activate downstream springs. | **NOW** |
| **westGate** | Pull musl. Deploy. Enable nestGate TCP (O5). | **NOW** |
| **blueGate** | Pull musl. Deploy musl side. Windows continues Track 2. | NORMAL |
| **southGate** | Re-deploy cephalization baseline. | LOW |
| **strandGate** | Deploy when thermalization completes. | DEFERRED |

### Track 2: WINDOWS CROSS-ARCH (code teams)

7 primals have unix-only IPC paths (UDS, `rustix`, `tokio::net::Unix*`) compiled unconditionally. G65 protocol negotiation modules are the primary cause.

| Primal | Owner | Unix deps | Fix |
|--------|-------|-----------|-----|
| **bingoCube** | eastGate | G65 IPC module | `#[cfg(unix)]` guard IPC module |
| **loamSpine** | sporeGate | `tarpc_server.rs`, tokio `UnixStream`, lifecycle tests | Guard tarpc UDS server + tests |
| **nestGate** | overwatch | `rustix` (fs/net/process), protocol negotiation | Guard rustix-using modules |
| **petalTongue** | overwatch | `rustix`, `unix_socket_server/`, audio socket | Guard IPC + rustix modules |
| **rhizoCrypt** | sporeGate | `tarpc_uds.rs`, UDS client, shutdown | Guard tarpc UDS + client |
| **skunkBat** | eastGate | `tarpc_uds.rs`, IPC transport, BTSP (11+ refs) | Guard IPC transport layer |
| **squirrel** | eastGate | `rustix`, transport listener/types, security | Guard transport + auth modules |

**Pattern**: Wrap UDS/IPC modules with `#[cfg(unix)]`. Use `rustix` (not raw `libc`) for any syscall needs — barraCuda's `libc→rustix` migration (`525674f`) is the reference, restoring `#![forbid(unsafe_code)]`. Convergent — each team implements independently. The 8 primals that already build on Windows can serve as references.

---

## DIVERGENCES FROM DEPLOY (for reference)

1. **BTSP signal enforcement**: sweetGrass, biomeOS, bearDog, skunkBat require riboCipher `0xEC 0x01` prefix. petalTongue health module updated with BTSP+plain fallback.
2. **bearDog full BTSP**: Main socket requires `ClientHello`. Use `beardog-default.sock` for plain health.
3. **skunkBat family socket**: Creates at `/run/user/0/biomeos/skunkbat-*.sock`. Volatile on root session expiry.
4. **toadStool B1/B2**: Socket `srw-------` (root only). Needs biomeGate B1/B2 group-connectable fix.
5. **DIV-7 harvest exit codes**: 9/15 false non-zero. `plasmid.harvest --verify` still needed.

---

## AFTER DEPLOY — SPRINGS + SCIENCE

| # | Item | Gate | Unblocks |
|---|------|------|----------|
| E2 | squirrel systemd on ironGate | ironGate | Agent panel LIVE |
| D1 | tideGlass cell boot | westGate | NF GPS science |
| O5 | nestGate TCP on westGate | westGate | Inter-gate CAS |
| O7 | Inter-gate `content.get` E2E | mesh | Data-remote springs |

---

## BACKGROUND

| Gate | Project | Status |
|------|---------|--------|
| **westGate** | ChunkedBraid 71/153. AlphaFold 1.3 TB. Multi-tier CAS. | Running |
| **strandGate** | SU(N) 87-config grid. arXiv 40/42. Observable battery 69/69. | Running |

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| Cephalization | **G65 15/15. C2 15/15. C8 DONE. COMPLETE.** |
| Musl depot | **17/17 on golgi** |
| Windows depot | **8/15 fresh** — 7 need `#[cfg(unix)]` |
| sporeGate health | **12/13 alive** (toadStool B1/B2) |
| Gates online | **11** |
| Primal tests | **~140,000+** |
| arXiv | **40/42 (95%)** |
| Observable battery | **69/69 COMPLETE** |

---

*Wave 156s — **MUSL DEPOT COMPLETE.** 17/17 on golgi. sporeGate deployed, 12/13 alive. Gate teams: deploy musl now. Code teams: 7 primals need `#[cfg(unix)]` for Windows cross-arch (bingoCube, loamSpine, nestGate, petalTongue, rhizoCrypt, skunkBat, squirrel). toadStool needs B1/B2 socket perms. Two parallel tracks: deploy gates (musl) + fix Windows cross-compilation. ~140K+ tests, 15/15 GREEN.*
