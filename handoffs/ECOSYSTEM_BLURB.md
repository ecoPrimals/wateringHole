# ecoPrimals Ecosystem Blurb — Wave 147f

**Date**: Jul 17, 2026 14:50 EDT | **Wave**: 147f | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. GARDENS LIVE ON GATES.**

**This cascade**: Massive evolution wave. lithoSpore shipped pack/unpack +
initioChem first consumer (pipeline proven end-to-end). esotericWebb V16:
6/9 primals connected on flockGate in real-time — first live composition
validated. cellMembrane shipped systemd units for footPrint + esotericWebb,
esotericWebb Caddy block, zone House1 fix (1,100 tests). footPrint at 266
tests, 0 internal debt — critical path entirely upstream. 5 handoffs
fossilized. New ecosystem GAPs surfaced from live composition testing.

---

## Upstream Primal Demand Signal

Accumulated needs from all downstream consumers. Each primal team: address
your rows. This section grows as gardens evolve — that's the point.

### songBird (3 consumers, highest demand)

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| `PROXY_PATH` drawbridge route | **footPrint** | **P0** | Route `:7780/footprint/ext/*` → footPrint `:8090/ext`. **Blocks footPrint going live.** |
| Raw JSON-RPC endpoint | **esotericWebb** | **P1** | GAP-037: TCP 7780 speaks HTTP, not NDJSON JSON-RPC. Webb (and sourDough-pattern consumers) can't health-check or call songBird. Expose NDJSON endpoint alongside HTTP. |
| Confirm discovery response schemas | **esotericWebb** | P1 | `discovery.topology`, `discovery.health`, `discovery.query`, `discovery.bonds` — confirm shapes. |
| BTSP → cellMembrane `gate.enroll` | enrollment | P1 | `mesh.enroll` method shipped — wire to cellMembrane. |

### squirrel

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| Accept `null` params on health methods | **esotericWebb** | P1 | GAP: `health.liveness` with `null` params returns `-32602`. JSON-RPC 2.0 allows `null`. Webb works around by sending `{}`. |

### nestGate

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| `PROJECTS_PATH` CAS wiring | **footPrint** | P1 | Project CRUD → nestGate CAS for content-addressed persistence. Filesystem works as fallback. |

### petalTongue

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| `WS_PATH` agent bridge | **footPrint** | P1 | WebSocket command protocol at `/ws`. |

### bearDog

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| Confirm crypto JSON-RPC sigs | **esotericWebb** | P1 | `crypto.sign`, `crypto.verify`, `crypto.hash` — confirm signatures match. |
| HSM → Android Keystore | grapheneGate | P2 | Mobile hardware-backed key storage. |

### sweetGrass

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| Confirm `braid.create/query` | **esotericWebb** | P1 | Attribution tracking — confirm availability + response format. |

### biomeOS

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| GAP-017: neural-api resurrection | **esotericWebb** | P2 | Neural API for orchestrated composition. |
| GAP-018: executors not exposed | **esotericWebb** | P2 | Executor capabilities not reachable via JSON-RPC. |

### ALL primals (ecosystem convention)

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| GAP-036: Socket naming convention | **esotericWebb** | P2 | Some primals register domain-named sockets (`ai.sock`), others primal-named (`rhizocrypt.sock`). Converge on one convention or create symlinks. |
| GAP-038: Stale UDS socket cleanup | **esotericWebb** | P2 | rhizoCrypt and toadStool leave sockets on disk after exit. Trap SIGTERM/SIGINT and unlink, or have biomeOS gc. |

---

## Path to Live — Downstream Projects

### footPrint → `primals.eco/footprint/` (PARTIALLY LIVE)

Static client served. Server not deployed. **0 internal debt remaining.**

| Step | Status | Owner |
|------|--------|-------|
| 1. Static client on petalTongue | **LIVE** | — |
| 2. Server binary (266 tests, 0 debt) | **DONE** | footPrint |
| 3. Caddy path-based routing | **SHIPPED** | cellMembrane |
| 4. NUCLEUS systemd service unit | **SHIPPED** | cellMembrane |
| 5. **Deploy unit on sporeGate** | **NOT DEPLOYED** | sporeGate ops |
| 6. **songBird drawbridge route** | **NOT STARTED** | songBird |
| 7. nestGate CAS for projects | Not started (filesystem fallback works) | nestGate |
| 8. petalTongue WS bridge | Not started (non-blocking) | petalTongue |

**Critical path**: Steps 5 + 6. Service unit is written — deploy it. Wire drawbridge.

### esotericWebb → `primals.eco/webb/` (COMPOSING ON GATE)

V16 live on flockGate. 6/9 primals connected. First milestone nearly reached.

| Step | Status | Owner |
|------|--------|-------|
| 1. Binary compiled (471 tests) | **DONE** | esotericWebb |
| 2. Caddy block for `/webb/` | **SHIPPED** | cellMembrane |
| 3. NUCLEUS systemd service unit | **SHIPPED** | cellMembrane |
| 4. Live primal composition | **6/9 CONNECTED** | esotericWebb |
| 5. songBird raw JSON-RPC endpoint | **BLOCKED** (GAP-037) | songBird |
| 6. Deploy on sporeGate (WAN) | NOT DEPLOYED | sporeGate ops |
| 7. Content bundles (YAML authoring) | Partial | esotericWebb |

**Connected**: squirrel, petalTongue, nestGate, loamSpine, sweetGrass, bearDog
**Stale socket**: rhizoCrypt, toadStool (GAP-038)
**Transport mismatch**: songBird (GAP-037)

### lithoSpore → CLI tool (PIPELINE PROVEN)

Pack/unpack shipped. initioChem is first consumer. Pipeline proven end-to-end.

| Step | Status | Owner |
|------|--------|-------|
| 1. Silicon Atheism Platform trait | **COMPLETE** (219 tests) | lithoSpore |
| 2. `pseudospore pack` command | **SHIPPED** | lithoSpore |
| 3. `pseudospore unpack` command | **SHIPPED** | lithoSpore |
| 4. initioChem as first consumer | **SHIPPED** (2 tests) | initioChem |
| 5. USB round-trip validation | NOT STARTED | lithoSpore + primalSpring |

**Critical path**: Step 5 — primalSpring scenario for USB round-trip.

### projectFOUNDATION → TBD (NOT STARTED)

| Step | Status | Owner |
|------|--------|-------|
| 1. Thread lineage store design | NOT STARTED | projectFOUNDATION |
| 2. nestGate CAS integration | NOT STARTED | nestGate + FOUNDATION |
| 3. Provenance trio wiring | NOT STARTED | rhizoCrypt + loamSpine + sweetGrass |

---

## Ecosystem Test Health

| Project | Tests | Clippy | Unsafe | Debt |
|---------|-------|--------|--------|------|
| cellMembrane | 1,100 | 0 | forbidden | 0 |
| esotericWebb | 471 | 0 | forbidden | 0 |
| songBird | full pass | 0 | forbidden | 0 |
| footPrint | 266 | clean | N/A (TS) | 0 |
| lithoSpore | 219 | 0 | forbidden | 0 |
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
| lithoSpore pack/unpack + initioChem consumer | **SHIPPED** |
| esotericWebb live composition (6/9 primals) | **VALIDATED** |
| footPrint Caddy + NUCLEUS unit | **SHIPPED** |
| esotericWebb Caddy + NUCLEUS unit | **SHIPPED** |
| Depot (59 binaries, 4 arch) | **OPERATIONAL** |

---

## 6-Gate Mesh (LIVE)

```
golgiBody (10.13.37.1) — hub, VPS, relay
  ├─ sporeGate (10.13.37.2) — builder, site router, [deploy target]
  ├─ eastGate  (10.13.37.5) — orchestrator, overwatch
  ├─ flockGate (10.13.37.6) — WAN gate, esotericWebb V16 [6/9 live]
  ├─ ironGate  (10.13.37.7) — compute, ABG, lithoSpore [pipeline proven]
  └─ northGate (10.13.37.8) — Windows, RTX 5090, zone House1
```

---

*Wave 147f: lithoSpore pack/unpack + initioChem consumer SHIPPED (pipeline
proven). esotericWebb V16: 6/9 primals connected on flockGate (first live
composition). cellMembrane: systemd units + Caddy for both footPrint and
esotericWebb + zone House1 fix (1,100 tests). footPrint 266 tests, 0 internal
debt — critical path entirely upstream. 3 new ecosystem GAPs from live
composition (socket naming, songBird HTTP transport, stale UDS sockets).
5 handoffs fossilized. Next: sporeGate deploy + songBird drawbridge route.*
