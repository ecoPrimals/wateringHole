# ecoPrimals Ecosystem Blurb — Wave 148a

**Date**: Jul 18, 2026 07:15 EDT | **Wave**: 148a | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. FOOTPRINT LIVE. WEBB READY.**

**This cascade**: esotericWebb AAR resolved all 3 deploy blockers: binary in
depot (3.3M stripped, plasmidBin manifest V17), Forgejo synced, **LIVE on
flockGate:8090** (6/9 primals, 472 tests, mesh-accessible). Port confusion
clarified (8080 = nestGate, not Webb). Deploy command and persistence
requirements handed off to cellMembrane/sporeGate ops. plasmidBin manifest
updated.

---

## Upstream Primal Demand Signal

### cellMembrane / sporeGate ops (DEPLOY)

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| esotericWebb persistent deploy | **esotericWebb** | **P0** | Binary in depot, Caddy block SHIPPED, systemd unit SHIPPED. Deploy: `esotericwebb serve --content content/ --listen 0.0.0.0:8090`. Needs `Restart=on-failure`. Route `/webb/` → `flockGate:8090`. |

### songBird (3 CLOSED, 1 open)

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| ~~`PROXY_PATH` drawbridge~~ | footPrint | — | **CLOSED** |
| ~~`/jsonrpc` endpoint~~ | esotericWebb | — | **CLOSED** |
| ~~Discovery schemas~~ | esotericWebb | — | **CLOSED** |
| BTSP → cellMembrane `gate.enroll` | enrollment | P1 | Pending |

### squirrel

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| Accept `null` params on health | esotericWebb | P1 | Open |

### nestGate

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| `PROJECTS_PATH` CAS wiring | footPrint | P1 | Open |

### petalTongue

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| `WS_PATH` agent bridge | footPrint | P1 | Open |

### bearDog

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| Confirm crypto JSON-RPC sigs | esotericWebb | P1 | Open |
| HSM → Android Keystore | grapheneGate | P2 | Open |

### sweetGrass

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| Confirm `braid.create/query` | esotericWebb | P1 | Open |

### biomeOS

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| GAP-017: neural-api resurrection | esotericWebb | P2 | Open |
| GAP-018: executors not exposed | esotericWebb | P2 | Open |

### ALL primals (ecosystem convention)

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| GAP-036: Socket naming convention | esotericWebb | P2 | Open |
| GAP-038: Stale UDS socket cleanup | esotericWebb | P2 | Open |

---

## Path to Live — Downstream Projects

### footPrint → `primals.eco/footprint/` — **LIVE**

Full path wired: `internet → golgi (Caddy TLS) → WG → sporeGate:8090 → drawbridge`

All 6 core steps complete. Enhancements (nestGate CAS, petalTongue WS) open.

### esotericWebb → `primals.eco/webb/` — **LIVE ON GATE, PERSISTENCE PENDING**

Running on flockGate:8090, mesh-accessible, 6/9 primals connected.
Needs cellMembrane/sporeGate to make it persistent (systemd + Caddy).

| Step | Status | Owner |
|------|--------|-------|
| 1. Binary (472 tests, 3.3M stripped) | **IN DEPOT** | esotericWebb |
| 2. Caddy block for `/webb/` | **SHIPPED** | cellMembrane |
| 3. NUCLEUS systemd service unit | **SHIPPED** | cellMembrane |
| 4. songBird discovery + /jsonrpc | **SHIPPED** | songBird |
| 5. Live primal composition | **6/9 CONNECTED** on flockGate | esotericWebb |
| 6. Forgejo repo synced | **DONE** | esotericWebb |
| 7. **Persistent deploy (systemd)** | **PENDING** | cellMembrane/sporeGate ops |
| 8. **Caddy route live** | **PENDING** | cellMembrane/golgiBody ops |

**Deploy command**: `esotericwebb serve --content content/ --listen 0.0.0.0:8090`
**Service unit**: `deploy/systemd/esotericwebb-server.service` (already in cellMembrane)
**Binary source**: `plasmidBin/primals/esotericwebb` or `cargo build --release`

### lithoSpore → CLI tool — **PIPELINE PROVEN, DEEP DEBT CLEAR**

| Step | Status |
|------|--------|
| 1-5. Platform trait, pack/unpack, initioChem, deep debt | **ALL DONE** (222 tests) |
| 6. USB round-trip validation | NOT STARTED |

### projectFOUNDATION → TBD (NOT STARTED)

---

## Ecosystem Test Health

| Project | Tests | Clippy | Debt |
|---------|-------|--------|------|
| cellMembrane | 1,100 | 0 | 0 |
| esotericWebb | 472 | 0 | 0 |
| songBird | full pass | 0 | 0 |
| footPrint | 266 | clean | 0 |
| lithoSpore | 222 | 0 | 0 |
| sporePrint | 289 | 0 | 0 |
| primalSpring | 1,203 | 0 | 2 |

---

## Completed Milestones

| Milestone | Status |
|-----------|--------|
| Silicon Atheism Phase 2 (14/14 + lithoSpore) | **COMPLETE** |
| Content-Addressed Convergence (6/6) | **COMPLETE** |
| Glacial Shift (8/8) | **ALL CLEAR** |
| `gate.enroll` fully automated (7 phases) | **SHIPPED** |
| lithoSpore pack/unpack + initioChem | **SHIPPED** |
| **footPrint LIVE** | **LIVE** — sovereign mesh serving |
| **esotericWebb LIVE on flockGate** | **LIVE** — 6/9 primals, persistence pending |
| songBird drawbridge + /jsonrpc + discovery | **SHIPPED** |
| Depot (59+ binaries, 4 arch) | **OPERATIONAL** |

---

## 6-Gate Mesh (LIVE)

```
golgiBody (10.13.37.1) — hub, VPS, Caddy TLS
  ├─ sporeGate (10.13.37.2) — builder, footPrint:8090 [LIVE]
  ├─ eastGate  (10.13.37.5) — orchestrator, overwatch
  ├─ flockGate (10.13.37.6) — esotericWebb:8090 [LIVE, persistence pending]
  ├─ ironGate  (10.13.37.7) — compute, lithoSpore [pipeline proven]
  └─ northGate (10.13.37.8) — Windows, RTX 5090
```

---

*Wave 148a: esotericWebb deploy blockers resolved — binary in depot (3.3M,
plasmidBin V17), Forgejo synced, LIVE on flockGate:8090 (6/9 primals, 472
tests, mesh-accessible). Port 8080 confusion clarified (nestGate, not Webb).
cellMembrane/sporeGate ops: make it persistent (systemd unit + Caddy route).
Two composition products now serving on sovereign mesh: footPrint (sporeGate)
and esotericWebb (flockGate).*
