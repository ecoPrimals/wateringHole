# ecoPrimals Ecosystem Blurb — Deployment Wave

**Date**: Aug 6, 2026 8:30PM | **Wave**: 156s | **From**: eastGate overwatch
**Posture**: **DEPLOY + G66.** Musl depot 17/17 on golgi — gate teams deploy now. G66 (Transport Abstraction) formalized as next convergence: sourDough reference already complete. 7 primals evolve transport layer independently to eliminate silicon deism. G64+G65 GRADUATED to COMPLETE. 14 COMPLETE / 25 ACTIVE / 23 GLACIAL. 62 goals.

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

### Track 2: G66 TRANSPORT ABSTRACTION (code teams — next convergence)

**The deeper issue**: 7/15 primals failed Windows because they import `UnixStream`/`rustix` unconditionally — **silicon deism**. The fix is NOT `#[cfg(unix)]` guards (that's arch-exclusion). The fix is **transport abstraction**: primals express *what* to connect to, not *how*.

**sourDough already has the reference** (`crates/sourdough-core/src/transport/`):
- `TransportEndpoint` — UDS / TCP / MeshRelay (platform-neutral destination)
- `TransportStream` — `#[cfg(unix)]` confined to transport layer only
- `connect_transport()` — TCP fallback on non-Unix (primals actually work on Windows)
- `platform_default()` — UDS on Linux, TCP localhost on Windows

**Spec**: `specs/TRANSPORT_ABSTRACTION_SPEC.md`

| Primal | Owner | What to evolve |
|--------|-------|----------------|
| **bingoCube** | eastGate | Add transport module, refactor G65 IPC |
| **loamSpine** | sporeGate | Transport-abstract tarpc server + tests |
| **nestGate** | overwatch | Confine `rustix` to transport, abstract protocol negotiation |
| **petalTongue** | overwatch | Transport-abstract `unix_socket_server/`, confine `rustix` |
| **rhizoCrypt** | sporeGate | Transport-abstract tarpc UDS + client |
| **skunkBat** | eastGate | Transport-abstract IPC transport layer (11+ unix refs) |
| **squirrel** | eastGate | Transport-abstract listener/types, confine `rustix` |

**Already clear** (8/15 — can serve as secondary references): barraCuda, bearDog, biomeOS, coralReef, nestGate*, petalTongue*, songBird, sourDough, sweetGrass, toadStool. (*Some need transport confinement even if they build today.)

**This unlocks**: Windows IPC (not just "compiles"), macOS dev, WASM/browser (WebSocket variant for petalTongue), QUIC WAN, port-aesthetic songBird routing.

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
| Cephalization (G64+G65) | **COMPLETE.** G65 15/15. C2 15/15. C8 DONE. |
| G66 Transport Abstraction | **sourDough reference DONE. 7/15 primals need adoption.** |
| Musl depot | **17/17 on golgi** |
| Windows depot | **8/15 fresh** — 7 blocked on G66 |
| sporeGate health | **12/13 alive** (toadStool B1/B2) |
| Gates online | **11** |
| Primal tests | **~140,000+** |
| arXiv | **40/42 (95%)** |
| Observable battery | **69/69 COMPLETE** |

---

*Wave 156s — **DEPLOY + G66.** Musl 17/17 on golgi — gate teams deploy. G66 Transport Abstraction formalized: sourDough reference complete, 7 primals converge independently to eliminate silicon deism. Not `#[cfg(unix)]` guards — transport abstraction (TransportEndpoint/TransportStream/connect_transport). Spec: `specs/TRANSPORT_ABSTRACTION_SPEC.md`. G64+G65 GRADUATED COMPLETE. 14 COMPLETE / 25 ACTIVE / 23 GLACIAL. 62 goals. ~140K+ tests, 15/15 GREEN.*
