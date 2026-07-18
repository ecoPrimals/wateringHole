# ecoPrimals Ecosystem Blurb — Wave 148b

**Date**: Jul 18, 2026 07:55 EDT | **Wave**: 148b | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. 2 PRODUCTS LIVE.**

**This cascade**: cellMembrane shipped esotericWebb deploy fix (correct port
8090, ExecStart, WorkingDirectory, Caddy routing). Live Frontend E2E Tutorial
Standard issued — all live frontends must have known locations / demo scenarios
that double as E2E verification suites. footPrint: 5 known locations specified
(MSU Campus, Downtown EL, Red Cedar flood, Meridian Twp, Haslett Ag).
esotericWebb: guided demo scenario pattern specified.

---

## Upstream Primal Demand Signal

### footPrint team (E2E TUTORIAL — SHIPPED)

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| ~~Known locations + picker UI~~ | users + operators | — | **SHIPPED** (`5f449df`). 5 locations, `<select>` picker, URL hash deep-linking (#msu-campus), 9 new tests. |

### esotericWebb team (E2E TUTORIAL + OPS — NEW)

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| Guided demo scenario | users + operators | **P1** | `content/demos/` YAML walkthrough exercising all connected primals. See standard. |
| systemd persistence on flockGate | sporeGate ops | P1 | cellMembrane unit FIXED (`33aa33a`). Deploy: `systemctl enable --now esotericwebb-server`. |
| Caddy route `/webb/` on golgiBody | sporeGate ops | P1 | Caddy config FIXED. Route `/webb/` → `flockGate:8090`. |

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

Full path wired. All 6 core steps complete.
**Next**: E2E test runner (Playwright or primalSpring scenario `footprint-known-locations-e2e`).

### esotericWebb → `primals.eco/webb/` — **LIVE ON GATE**

472 tests, 6/9 primals connected, flockGate:8090. Deploy artifacts FIXED.

| Step | Status | Owner |
|------|--------|-------|
| 1-6. Binary, Caddy, unit, songBird, composition, Forgejo | **ALL DONE** | — |
| 7. systemd enable on flockGate | **PENDING** | sporeGate ops |
| 8. Caddy route on golgiBody | **PENDING** | sporeGate ops |
| 9. E2E demo scenario | **NOT STARTED** | esotericWebb |

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
| footPrint | 275 | clean | 0 |
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
