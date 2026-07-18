# ecoPrimals Ecosystem Blurb — Wave 150h

**Date**: Jul 18, 2026 18:30 EDT | **Wave**: 150h | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. FULL NUCLEUS COMPOSITION WIRED.**

**This wave**: footPrint wired both consumer-side connections (petalTongue `/ws`
JSON-RPC bridge + nestGate CAS client). esotericWebb shipped V21 — browser-
navigable HTML frontend + live visual rendering via petalTongue `ui.render`.
NUCLEUS composition is now end-to-end wired through live products. All P1
items resolved on both provider AND consumer sides.

---

## 1. DEPLOYMENT CHAIN

```
User → Cloudflare (*.primals.eco wildcard → golgiBody)
  → Caddy on golgiBody (TLS, Host-header routing)
    → WireGuard mesh → target gate → service
```

**URL Standard**: `prefix.primals.eco` subdomain. Root → `sporeprint.primals.eco`.

**Three-Domain Model**: `primals.eco` (intra-membrane) | `primal.eco` (inner) | `nestgate.io` (data service)

---

## 2. LIVE SYSTEMS — WAN-Validated

| Surface | URL | Status | Gate |
|---------|-----|--------|------|
| footPrint | `footprint.primals.eco` | **LIVE — FULL NUCLEUS** | sporeGate |
| esotericWebb | `webb.primals.eco` | **V21 LIVE — BROWSER-NAVIGABLE** | flockGate |
| sporePrint | `sporeprint.primals.eco` | **LIVE** | golgiBody |
| TOPO-VIS | `live.primals.eco` | **LIVE** | sporeGate |
| Forgejo | `git.primals.eco` | **LIVE** | golgiBody |
| JupyterHub | `lab.primals.eco` | **LIVE** | ironGate |

### footPrint — **FULL NUCLEUS COMPOSITION WIRED**

466 tests. All composition layers connected:

| Layer | Primal | Wiring | Status |
|-------|--------|--------|--------|
| Data proxy | songBird | `/ext` drawbridge + weak bonds | LIVE |
| Project storage | nestGate | CAS client (`/api/cas/`) — BLAKE3 content-addressed | **WIRED (Wave 150h)** |
| Agent bridge | petalTongue | `/ws` WebSocket JSON-RPC (7 methods) | **WIRED (Wave 150h)** |
| Static + API | footPrint Express | CSP + security headers + SPA fallback | LIVE |

Consumer modules shipped: `petal-tongue.ts` (231L, auto-reconnecting WS client)
and `nestgate-cas.ts` (84L, BLAKE3 content-addressed project persistence).

### esotericWebb — **V21, BROWSER-NAVIGABLE + LIVE VISUALS**

453 tests. 6/9 primals connected. GET handler shipped — `webb.primals.eco/`
now serves a self-contained HTML frontend (zero external JS/CSS dependencies).
Live visual rendering via petalTongue `ui.render` confirmed working
(`scene_pushed: true`). `session.poll_input` method for interaction loop.

### Other surfaces: sporePrint (302 pages), TOPO-VIS, Forgejo, JupyterHub — all LIVE.

---

## 3. PRIMAL DEMAND SIGNAL — P2 ONLY

### Inter-Primal Wiring — ALL COMPLETE

| Item | Provider | Consumer | Status |
|------|----------|----------|--------|
| `PROJECTS_PATH` CAS | nestGate | footPrint | **COMPLETE** (both sides) |
| `null` params on health | squirrel | esotericWebb | **FIXED** |
| BTSP `mesh.enroll` | songBird | cellMembrane | **ACTIVE** |
| `WS_PATH` agent bridge | petalTongue | footPrint | **COMPLETE** (both sides) |

### P2 — Ecosystem Quality

| Need | Owner | Detail |
|------|-------|--------|
| esotericWebb V21 depot binary | sporeGate ops | Local build, not in depot |
| `loginctl enable-linger` | flockGate ops | systemd user unit persistence |
| `primals.eco` DNSSEC | ops / Cloudflare | Enable via API |
| petalTongue SceneGraph vs `ui.render` | petalTongue | Narrative composition format decision |
| `footprint_composition.toml` URL | cellMembrane | Update to subdomain URL |
| cellMembrane `gate.enroll` → `mesh.enroll` | cellMembrane | Integration with songBird |
| HSM → Android Keystore | bearDog | grapheneGate backend |
| Credential store trait | bearDog + squirrel | Silicon Atheism Phase 2 |
| Health monitoring trait | ecosystem | nestGate consolidated procfs (Session 122) |
| `primal-transport` crate | ecosystem | Extract transport abstractions |
| primalSpring CAC scenario | primalSpring | FRAGO issued |

### P2 — pseudoSpore Pipeline

| Need | Owner | Detail |
|------|-------|--------|
| `validation.json` per spore | 6 spring teams | Module validation results |
| Fix groundSpring `bingoCube/nautilus` dep | groundSpring | `cargo test` fails |
| Bash → Rust orchestration | spring teams | 114+ shell scripts |

---

## 4. STRATEGIC GOALS

### NOW

- **Visual verification** — confirm footPrint tiles + CAS at `footprint.primals.eco`
- **Visual verification** — confirm esotericWebb HTML frontend at `webb.primals.eco`
- **Enable Cloudflare DNSSEC** for `primals.eco`
- **Push V21 to depot**

### NEAR TERM (next 2-4 weeks)

- **pseudoSpore validation**: promote 6 pending spores
- **projectFOUNDATION design**: thread lineage store, nestGate CAS integration
- **strandGate enrollment**: dual EPYC 7452, 256GB RAM, RTX 3090
- **`primal.eco` inner membrane separation**
- **petalTongue scene format**: SceneGraph narrative variant or `ui.render` canonical

### FUTURE (quarter horizon)

- **tideGlass composition**: computational chemistry product
- **primal-transport crate**: publish shared transport abstraction
- **SHOW_HN readiness**: rubric, narrative, demo path
- **fieldGate/biomeGate recovery**

---

## 5. DIMENSIONAL SCORECARD (Wave 150h)

| Project | Tests | Clippy | Fmt | Debt | Unsafe | >800L | Prod unwrap |
|---------|-------|--------|-----|------|--------|-------|-------------|
| cellMembrane | 1,100 | 0 | 0 | 0 | 0 | 0 | 0 |
| esotericWebb | 453 | 0 | 0 | 0 | 0 | 0 | 0 |
| footPrint | 466 | 0 | — | 0 | — | 0 | — |
| songBird | 14,322 | swept | swept | 0 | 0 | swept | swept |
| lithoSpore | 227+ | 0 | 0 | 0 | 0 | 0 | 0 |
| loamSpine | 1,702 | 0 | 0 | 0 | 0 | 0 | 0 |
| rhizoCrypt | 1,878 | 0 | 0 | 0 | 0 | 0 | 0 |
| nestGate | 1,710 | 0 | 0 | 0 | 0 | 0 | 10 (justified) |
| primalSpring | 1,203 | 0 | 0 | 0 | 0 | 0 | 0 |
| sporePrint | 289 | — | — | 0 | — | 0 | — |

**Ecosystem**: ~23,300+ tests, 0 debt, 0 unsafe, 0 mocks.

---

## 6. COMPLETED MILESTONES

| Milestone | Wave |
|-----------|------|
| **FULL NUCLEUS COMPOSITION WIRED (footPrint CAS + WS consumer)** | **150h** |
| **esotericWebb V21 — browser-navigable + live visuals** | **150h** |
| ALL P1 inter-primal wiring RESOLVED (4/4, both sides) | 150g/h |
| 5 composition surfaces LIVE from WAN | 150f |
| Deployment chain validated end-to-end | 150f |
| cellMembrane subdomain routing overhaul | 150e |
| songBird `mesh.enroll` ACTIVE | 150e |
| nestGate dimensional audit ALL CLEAR (1,710 tests) | 150e |
| Silicon Atheism Phase 2 (14/14 + lithoSpore) | 145a |
| Content-Addressed Convergence (6/6) | 143b |
| Glacial Shift (8/8) ALL CLEAR | 137b |
| lithoSpore ALL CLEAR + 7 pseudoSpores emitted | 150a |
| GAP-036 + GAP-038 closed ecosystem-wide | 150a |
| Depot operational (59+ binaries, 4 arch) | 142a |

---

## 7. MESH TOPOLOGY

```
golgiBody (10.13.37.1) — hub, VPS, Caddy TLS, Cloudflare firebreak
  ├─ sporeGate (10.13.37.2) — builder, footPrint [FULL NUCLEUS]
  ├─ eastGate  (10.13.37.5) — orchestrator, overwatch
  ├─ flockGate (10.13.37.6) — esotericWebb [V21 LIVE]
  ├─ ironGate  (10.13.37.7) — compute, lithoSpore [ALL CLEAR]
  └─ northGate (10.13.37.8) — Windows, RTX 5090 [enrolled]

Offline: westGate, fieldGate, strandGate (pending), biomeGate
```

---

## 8. ORTHOGONAL DIMENSIONS

| Dim | Area | Status | Open items |
|-----|------|--------|------------|
| 1 | Temporal | GREEN | — |
| 2 | Ecological | GREEN | — |
| 3 | Hardware | AMBER | 4 gates offline |
| 4 | Sovereignty | AMBER | `primals.eco` DNSSEC (P2) |
| 5 | Depot | GREEN | esotericWebb V21 not in depot |
| 6 | Public Surface | **GREEN** | 5+ surfaces LIVE |
| 7 | Glacial Shift | GREEN | SHOW_HN rubric |
| 8 | Compositions | **GREEN** | Both products fully wired |
| 9 | Documentation | GREEN | — |
| 10 | Cascade | GREEN | — |
| 11 | CAC | GREEN | primalSpring scenario (P2) |
| 12 | Silicon Atheism | GREEN | Credential trait (P2) |

---

*Wave 150h: NUCLEUS COMPOSITION WIRED. footPrint consumer-side wiring COMPLETE
(petal-tongue.ts: 231L WS client, nestgate-cas.ts: 84L CAS client). esotericWebb
V21: browser-navigable HTML frontend + petalTongue ui.render confirmed. nestGate
Session 122: procfs consolidation. All P1 resolved on BOTH provider and consumer
sides. 5 surfaces LIVE. 10 GREEN / 2 AMBER dimensions. 23,300+ tests. Demand
signal P2-only. Next: visual verification, DNSSEC, pseudoSpore promotion.*
