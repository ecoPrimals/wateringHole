# ecoPrimals Ecosystem Blurb — Wave 147e

**Date**: Jul 17, 2026 11:30 EDT | **Wave**: 147e | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. GARDENS EVOLVING.**

---

## Upstream Primal Demand Signal

Accumulated needs from all downstream consumers. Each primal team: address
your rows. This section grows as gardens evolve — that's the point.

### songBird

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| `PROXY_PATH` drawbridge route | **footPrint** | **P0** | Route `:7780/footprint/ext/*` → footPrint server `:8090/ext` for USGS/FEMA/ArcGIS proxy. **Blocks footPrint going live.** |
| Confirm `discovery.topology` schema | **esotericWebb** | P1 | Webb calls `discovery.topology`, `discovery.health`, `discovery.query`, `discovery.bonds`. Confirm response shapes. |
| BTSP → cellMembrane `gate.enroll` | enrollment pipeline | P1 | `mesh.enroll` method is shipped — wire to cellMembrane's `gate.enroll` for trustless enrollment. |

### nestGate

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| `PROJECTS_PATH` CAS wiring | **footPrint** | P1 | footPrint project CRUD (`/api/projects`) currently uses filesystem. Wire to nestGate CAS for content-addressed persistence + provenance. |

### petalTongue

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| `WS_PATH` agent bridge | **footPrint** | P1 | WebSocket command protocol at `/ws` — petalTongue bridges agent commands to footPrint ECS store. |

### bearDog

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| Confirm crypto JSON-RPC sigs | **esotericWebb** | P1 | Webb calls `crypto.sign`, `crypto.verify`, `crypto.hash`. Confirm method signatures match bearDog's surface. |
| HSM → Android Keystore backend | grapheneGate | P2 | Mobile hardware-backed key storage. |

### sweetGrass

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| Confirm `braid.create/query` | **esotericWebb** | P1 | Webb calls `braid.create` and `braid.query` for attribution tracking. Confirm availability + response format. |

### biomeOS

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| GAP-017: neural-api ZOMBIE | **esotericWebb** | P2 | Neural API needs resurrection for orchestrated composition. |
| GAP-018: executors not exposed | **esotericWebb** | P2 | Executor capabilities not reachable via JSON-RPC. |

### cellMembrane

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| footPrint composition deploy | **footPrint** (ops) | **P0** | Wire `footprint_composition.toml` on sporeGate. Caddy blocks are SHIPPED — need NUCLEUS service unit + deploy. |

### primalSpring

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| `protokarya-wan-deploy` scenario | footPrint + ecosystem | P2 | 1 gap remaining — validate live WAN HTTP 200 + security headers. Blocked on footPrint deploy. |

---

## Path to Live — Downstream Projects

### footPrint → `primals.eco/footprint/` (PARTIALLY LIVE)

Static client is served. Server composition is not deployed.

| Step | Status | Owner |
|------|--------|-------|
| 1. Static client on petalTongue | **LIVE** | — |
| 2. Server binary compiled + in depot | **DONE** (243 tests, security hardened) | footPrint |
| 3. Caddy path-based routing config | **SHIPPED** (`/api/*`→8090, `/ws`→8080, static→8080) | cellMembrane |
| 4. **NUCLEUS service unit on sporeGate** | **NOT DEPLOYED** | cellMembrane + sporeGate ops |
| 5. **songBird drawbridge route for `/ext`** | **NOT STARTED** | songBird |
| 6. nestGate CAS for project persistence | Not started (filesystem works as fallback) | nestGate |
| 7. petalTongue WS bridge for agent commands | Not started (non-blocking for basic use) | petalTongue |
| 8. `protokarya-wan-deploy` validation | Blocked on steps 4+5 | primalSpring |

**Critical path**: Steps 4 + 5. Deploy the server, wire the drawbridge.
Steps 6-7 are enhancements — footPrint is usable without CAS or agent bridge.

### esotericWebb → `primals.eco/webb/` (NOT DEPLOYED)

V15 is shipping code. Needs deployment pipeline.

| Step | Status | Owner |
|------|--------|-------|
| 1. Binary compiled + in depot | **DONE** (373 tests) | esotericWebb |
| 2. Caddy block for `primals.eco/webb/` | NOT CREATED | cellMembrane |
| 3. NUCLEUS service unit on flockGate | NOT CREATED | cellMembrane + sporeGate ops |
| 4. songBird discovery schema confirmation | **WAITING** — Webb calls 4 methods | songBird |
| 5. bearDog crypto signature confirmation | **WAITING** | bearDog |
| 6. sweetGrass braid method confirmation | **WAITING** | sweetGrass |
| 7. Content bundles (rulesets, voices) | Partial (voice engine + RulesetCert done, YAML authoring pending) | esotericWebb |

**Critical path**: Steps 2 + 3 (Caddy + NUCLEUS), then step 4 (songBird
schemas) for the first milestone: static topology rendering from live mesh.

### lithoSpore → CLI tool (NOT PACKAGED)

Not a web service — "live" means pseudoSpore files work.

| Step | Status | Owner |
|------|--------|-------|
| 1. Silicon Atheism Platform trait | **COMPLETE** (216 tests) | lithoSpore |
| 2. `pseudospore pack` command | NOT STARTED | lithoSpore |
| 3. `pseudospore unpack` command | NOT STARTED | lithoSpore |
| 4. initioChem as first consumer | NOT STARTED | initioChem |
| 5. USB round-trip validation | NOT STARTED | lithoSpore + primalSpring |

**Critical path**: Steps 2 + 3 (pack/unpack), then step 4 (prove it with initioChem).

### projectFOUNDATION → TBD (NOT STARTED)

| Step | Status | Owner |
|------|--------|-------|
| 1. Thread lineage store design | NOT STARTED | projectFOUNDATION |
| 2. nestGate CAS integration | NOT STARTED | nestGate + FOUNDATION |
| 3. Provenance trio wiring | NOT STARTED | rhizoCrypt + loamSpine + sweetGrass |

---

## Completed Milestones

| Milestone | Status |
|-----------|--------|
| Silicon Atheism Phase 2 (14/14 + lithoSpore) | **COMPLETE** |
| Content-Addressed Convergence (6/6) | **COMPLETE** |
| Glacial Shift (8/8) | **ALL CLEAR** |
| `gate.enroll` fully automated (7 phases) | **SHIPPED** |
| footPrint Caddy blocks | **SHIPPED** |
| Depot (59 binaries, 4 arch) | **OPERATIONAL** |

---

## 6-Gate Mesh (LIVE)

```
golgiBody (10.13.37.1) — hub, VPS, relay
  ├─ sporeGate (10.13.37.2) — builder, site router
  ├─ eastGate  (10.13.37.5) — orchestrator, overwatch
  ├─ flockGate (10.13.37.6) — WAN gate, esotericWebb [target]
  ├─ ironGate  (10.13.37.7) — compute, ABG, lithoSpore [target]
  └─ northGate (10.13.37.8) — Windows, RTX 5090
```

---

## Ecosystem Test Health

| Project | Tests | Clippy | Unsafe | Debt |
|---------|-------|--------|--------|------|
| cellMembrane | 1,096 | 0 | forbidden | 0 |
| songBird | full pass | 0 | forbidden | 0 |
| esotericWebb | 373 | 0 | forbidden | 0 |
| lithoSpore | 216 | 0 | forbidden | 0 |
| footPrint | 243 | clean | N/A (TS) | 0 |
| sporePrint | 289 | 0 | forbidden | 0 |
| primalSpring | 1,203 | 0 | — | 1 |

---

*Wave 147e: Blurb restructured to demand-signal view. Upstream primal needs
at top — 8 primals have accumulated requests from 3 downstream consumers
(footPrint, esotericWebb, enrollment). Path-to-live roadmaps for all 4
gardens. footPrint critical path: sporeGate NUCLEUS deploy + songBird
drawbridge. esotericWebb critical path: Caddy block + NUCLEUS + songBird
schema confirmation.*
