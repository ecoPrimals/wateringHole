# ecoPrimals Ecosystem Blurb — Wave 147h

**Date**: Jul 17, 2026 18:10 EDT | **Wave**: 147h | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. FOOTPRINT LIVE.**

**This cascade**: sporeGate deployed footPrint server — **LIVE on sporeGate:8090**
with Caddy TLS proxy on golgiBody. API returning HTTP 200, 4h+ uptime confirmed.
`gateway_status = FOOTPRINT_LIVE_PHASE2_COMPLETE`. footPrint path-to-live is
DONE — all 6 steps complete. sporeGate reporting issues (details incoming).

---

## Upstream Primal Demand Signal

### songBird — **3 ITEMS CLOSED THIS WAVE**

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| ~~`PROXY_PATH` drawbridge route~~ | footPrint | ~~P0~~ | **CLOSED** (147f) — `/footprint/*` → `:8090` |
| ~~Raw JSON-RPC endpoint~~ | esotericWebb | ~~P1~~ | **CLOSED** (147f) — `POST /jsonrpc` on drawbridge |
| ~~Confirm discovery schemas~~ | esotericWebb | ~~P1~~ | **CLOSED** (147f) — topology/health/query/bonds implemented |
| BTSP → cellMembrane `gate.enroll` | enrollment | P1 | `mesh.enroll` shipped — integration pending |

### squirrel

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| Accept `null` params on health methods | esotericWebb | P1 | Open (Webb works around with `{}`) |

### nestGate

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| `PROJECTS_PATH` CAS wiring | footPrint | P1 | Open (filesystem fallback works) |

### petalTongue

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| `WS_PATH` agent bridge | footPrint | P1 | Open (non-blocking for basic use) |

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

| Step | Status | Owner |
|------|--------|-------|
| 1. Static client on petalTongue | **LIVE** | — |
| 2. Server binary (266 tests, 0 debt) | **DONE** | footPrint |
| 3. Caddy path-based routing | **DEPLOYED** | cellMembrane |
| 4. NUCLEUS systemd service unit | **DEPLOYED** | cellMembrane |
| 5. songBird drawbridge route | **DEPLOYED** | songBird |
| 6. Deploy on sporeGate | **LIVE** — 4h+ uptime, API 200 | sporeGate |
| 7. nestGate CAS for projects | Enhancement (filesystem works) | nestGate |
| 8. petalTongue WS bridge | Enhancement (non-blocking) | petalTongue |

**footPrint is LIVE.** Server on sporeGate:8090, Caddy TLS on golgiBody.
Remaining items (7-8) are enhancements, not blockers.

### esotericWebb → `primals.eco/webb/` — **COMPOSING, DEPLOY READY**

V17 shipping. 6/9 primals connected. songBird now reachable via `/jsonrpc`.

| Step | Status | Owner |
|------|--------|-------|
| 1. Binary compiled (471+ tests) | **DONE** | esotericWebb |
| 2. Caddy block for `/webb/` | **SHIPPED** | cellMembrane |
| 3. NUCLEUS systemd service unit | **SHIPPED** | cellMembrane |
| 4. songBird discovery schemas | **SHIPPED** | songBird |
| 5. songBird `/jsonrpc` endpoint | **SHIPPED** | songBird |
| 6. Live primal composition | **6/9 CONNECTED** | esotericWebb |
| 7. **Deploy on sporeGate** | **NOT DEPLOYED** | sporeGate ops |
| 8. bearDog crypto sig confirmation | Waiting | bearDog |
| 9. sweetGrass braid confirmation | Waiting | sweetGrass |

**One action remains**: Deploy on sporeGate. songBird P0/P1 blockers
cleared. Confirmation requests are non-blocking.

### lithoSpore → CLI tool — **PIPELINE PROVEN, DEEP DEBT CLEAR**

| Step | Status | Owner |
|------|--------|-------|
| 1. Silicon Atheism Platform trait | **COMPLETE** | lithoSpore |
| 2. `pseudospore pack` command | **SHIPPED** | lithoSpore |
| 3. `pseudospore unpack` command | **SHIPPED** | lithoSpore |
| 4. initioChem first consumer | **SHIPPED** | initioChem |
| 5. Deep debt evolution | **DONE** (222 tests, ring-free ecoBin, tracing) | lithoSpore |
| 6. USB round-trip validation | NOT STARTED | lithoSpore + primalSpring |

### projectFOUNDATION → TBD (NOT STARTED)

Blocked on design decisions. No primal team has received requests yet.

---

## Ecosystem Test Health

| Project | Tests | Clippy | Unsafe | Debt |
|---------|-------|--------|--------|------|
| cellMembrane | 1,100 | 0 | forbidden | 0 |
| esotericWebb | 471+ | 0 | forbidden | 0 |
| songBird | full pass | 0 | forbidden | 0 |
| footPrint | 266 | clean | N/A (TS) | 0 |
| lithoSpore | 222 | 0 | forbidden | 0 |
| sporePrint | 289 | 0 | forbidden | 0 |
| primalSpring | 1,203 | 0 | — | 1 |

---

## Completed Milestones

| Milestone | Status |
|-----------|--------|
| Silicon Atheism Phase 2 (14/14 + lithoSpore) | **COMPLETE** |
| Content-Addressed Convergence (6/6) | **COMPLETE** |
| Glacial Shift (8/8) | **ALL CLEAR** |
| `gate.enroll` fully automated (7 phases) | **SHIPPED** |
| lithoSpore pack/unpack + initioChem | **SHIPPED** + deep debt clear |
| esotericWebb live composition (6/9) | **VALIDATED** |
| **footPrint LIVE on sporeGate** | **LIVE** — 4h+ uptime |
| esotericWebb Caddy + NUCLEUS unit | **SHIPPED** |
| songBird PROXY_PATH + /jsonrpc + discovery | **SHIPPED** |
| Depot (59 binaries, 4 arch) | **OPERATIONAL** |

---

## 6-Gate Mesh (LIVE)

```
golgiBody (10.13.37.1) — hub, VPS, relay
  ├─ sporeGate (10.13.37.2) — builder, [DEPLOY TARGET: footPrint + Webb]
  ├─ eastGate  (10.13.37.5) — orchestrator, overwatch
  ├─ flockGate (10.13.37.6) — esotericWebb V17 [6/9 live]
  ├─ ironGate  (10.13.37.7) — compute, lithoSpore [pipeline proven]
  └─ northGate (10.13.37.8) — Windows, RTX 5090
```

---

*Wave 147g: songBird closed all 3 P0/P1 demand-signal items (PROXY_PATH
drawbridge, /jsonrpc endpoint, discovery schemas). esotericWebb V17 deep
debt. lithoSpore deep debt (222 tests, ring-free ecoBin). footPrint and
esotericWebb both ONE STEP from live — sporeGate deploy is the sole remaining
action. 13 deliveries absorbed today across 7 sub-waves.*
