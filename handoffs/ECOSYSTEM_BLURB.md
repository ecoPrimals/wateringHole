# ecoPrimals Ecosystem Blurb — Wave 147i

**Date**: Jul 17, 2026 18:30 EDT | **Wave**: 147i | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. FOOTPRINT LIVE.**

**This cascade**: sporeGate AAR absorbed. footPrint **confirmed LIVE** — full
path `primals.eco/footprint/` → client → API → drawbridge wired and serving.
esotericWebb deploy **BLOCKED** — binary not in depot, repo not on sporeGate,
flockGate:8080 not responding. sporePrint brief Cloudflare 404 during
cascade-sense rebuild — resolved naturally, try_files fix holds. primalSpring
green, KNOWN_DEBT stable at 2.

---

## Upstream Primal Demand Signal

### esotericWebb team (DEPLOY BLOCKER)

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| **Binary in depot** | sporeGate ops | **P0** | esotericWebb binary not in depot. sporeGate can't deploy what it can't fetch. Either add to depot via plasmidBin or provide build instructions. |
| **Repo access on sporeGate** | sporeGate ops | **P0** | Repo not cloned on sporeGate or eastGate. sporeGate needs source or binary access. |
| **flockGate:8080 health** | sporeGate ops | P1 | flockGate:8080 (where Webb is reportedly composing) not responding. Investigate — process may have exited. |

### songBird (3 CLOSED, 1 open)

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| ~~`PROXY_PATH` drawbridge route~~ | footPrint | ~~P0~~ | **CLOSED** (147f) |
| ~~Raw JSON-RPC endpoint~~ | esotericWebb | ~~P1~~ | **CLOSED** (147f) |
| ~~Discovery schemas~~ | esotericWebb | ~~P1~~ | **CLOSED** (147f) |
| BTSP → cellMembrane `gate.enroll` | enrollment | P1 | Pending integration |

### squirrel

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| Accept `null` params on health | esotericWebb | P1 | Open (Webb sends `{}`) |

### nestGate

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| `PROJECTS_PATH` CAS wiring | footPrint | P1 | Open (filesystem works) |

### petalTongue

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| `WS_PATH` agent bridge | footPrint | P1 | Open (non-blocking) |

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

| Step | Status |
|------|--------|
| 1. Static client on petalTongue | **LIVE** |
| 2. Server binary (266 tests, 0 debt) | **DEPLOYED** |
| 3. Caddy path-based routing | **DEPLOYED** |
| 4. NUCLEUS systemd service unit | **DEPLOYED** |
| 5. songBird drawbridge route | **DEPLOYED** |
| 6. sporeGate deploy | **LIVE** — 4h+ uptime, API 200 |
| 7. nestGate CAS for projects | Enhancement |
| 8. petalTongue WS bridge | Enhancement |

**Full path live**: `internet → golgi (Caddy TLS) → WG → sporeGate (footPrint:8090) → drawbridge`

### esotericWebb → `primals.eco/webb/` — **DEPLOY BLOCKED**

V17 code is ready. 6/9 primals were connected on flockGate. Deploy blocked
on logistics — not code.

| Step | Status | Owner |
|------|--------|-------|
| 1. Binary compiled (471+ tests) | **DONE** (on flockGate only) | esotericWebb |
| 2. Caddy block for `/webb/` | **SHIPPED** | cellMembrane |
| 3. NUCLEUS systemd service unit | **SHIPPED** | cellMembrane |
| 4. songBird discovery schemas | **SHIPPED** | songBird |
| 5. songBird `/jsonrpc` endpoint | **SHIPPED** | songBird |
| 6. **Binary in depot** | **MISSING** — not in plasmidBin | esotericWebb |
| 7. **Repo on sporeGate/eastGate** | **MISSING** — not cloned | esotericWebb |
| 8. **flockGate:8080 health** | **NOT RESPONDING** | esotericWebb |
| 9. Deploy on sporeGate | BLOCKED on 6+7 | sporeGate ops |

**esotericWebb team**: Either push the binary to depot via `plasmidBin push`,
or ensure the repo is cloneable from Forgejo so sporeGate can build it.
Also investigate flockGate:8080 — the composition that was running may have
exited.

### lithoSpore → CLI tool — **PIPELINE PROVEN, DEEP DEBT CLEAR**

| Step | Status |
|------|--------|
| 1. Silicon Atheism Platform trait | **COMPLETE** |
| 2-3. pseudospore pack/unpack | **SHIPPED** |
| 4. initioChem first consumer | **SHIPPED** |
| 5. Deep debt (222 tests, ring-free ecoBin) | **DONE** |
| 6. USB round-trip validation | NOT STARTED |

### projectFOUNDATION → TBD (NOT STARTED)

---

## Ecosystem Test Health

| Project | Tests | Clippy | Debt |
|---------|-------|--------|------|
| cellMembrane | 1,100 | 0 | 0 |
| esotericWebb | 471+ | 0 | 0 |
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
| **footPrint LIVE** | **LIVE** — first composition product on sovereign mesh |
| songBird PROXY_PATH + /jsonrpc + discovery | **SHIPPED** |
| Depot (59 binaries, 4 arch) | **OPERATIONAL** |

---

## 6-Gate Mesh (LIVE)

```
golgiBody (10.13.37.1) — hub, VPS, Caddy TLS
  ├─ sporeGate (10.13.37.2) — builder, footPrint:8090 [LIVE]
  ├─ eastGate  (10.13.37.5) — orchestrator, overwatch
  ├─ flockGate (10.13.37.6) — esotericWebb [NOT RESPONDING]
  ├─ ironGate  (10.13.37.7) — compute, lithoSpore [pipeline proven]
  └─ northGate (10.13.37.8) — Windows, RTX 5090
```

---

*Wave 147i: sporeGate AAR absorbed. footPrint confirmed LIVE (full path
wired and serving). esotericWebb deploy BLOCKED — binary not in depot,
repo not on sporeGate, flockGate:8080 not responding. esotericWebb team
needs to push binary to depot or provide repo access. sporePrint 404
resolved. primalSpring green (KNOWN_DEBT 2). 14 deliveries + 1 AAR
absorbed today across 8 sub-waves.*
