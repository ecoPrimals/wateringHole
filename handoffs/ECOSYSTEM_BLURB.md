# ecoPrimals Ecosystem Blurb — Wave 150j

**Date**: Jul 19, 2026 07:35 EDT | **Wave**: 150j | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. FORGEJO-FIRST RELAY ACTIVE.**

**This wave**: Forgejo push mirrors activated on **all 39 repos** — Forgejo is
now the sovereign primary, GitHub is the subordinate outer membrane mirror.
`sync_on_commit: true` on all repos: every Forgejo push auto-propagates to
GitHub via HTTPS token auth on golgiBody. GitHub SSH surface consolidated
from 12 per-gate keys to 2 (`golgiBody-ext@vps` + `forgejo-relay@golgiBody`).
Sync divergence that flockGate reported is now structurally impossible.
petalTongue v1.7.0 binary deployed to golgiBody depot (28MB).

---

## 1. DEPLOYMENT CHAIN

```
User → Cloudflare (*.primals.eco wildcard → golgiBody)
  → Caddy on golgiBody (TLS, Host-header routing)
    → WireGuard mesh → target gate → service
```

**URL Standard**: `prefix.primals.eco` subdomain. Root → `sporeprint.primals.eco`.

**Three-Domain Model**: `primals.eco` (intra-membrane) | `primal.eco` (inner) | `nestgate.io` (data service)

**Git Relay**: Forgejo (inner membrane, `git.primals.eco`) → push mirror → GitHub (outer membrane).
Gates push to Forgejo only. golgiBody relays to GitHub on every commit. 39/39 repos mirrored.

---

## 2. LIVE SYSTEMS — WAN-Validated

| Surface | URL | Status | Gate |
|---------|-----|--------|------|
| footPrint | `footprint.primals.eco` | **LIVE — FULL NUCLEUS** | sporeGate |
| esotericWebb | `webb.primals.eco` | **V22 LIVE — SCENE BINDING FIXED** | flockGate |
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

### esotericWebb — **V22, SCENE BINDING FIXED**

453 tests. 6/9 primals connected. V22 fixes P1 scene binding:
`push_scene_to_ui()` now attempts `visualization.render.scene` with a
`game_scene` SceneGraph (Transform3D at z=0) first, falls back to `ui.render`
on rejection. Forward-compatible with petalTongue v1.7+ — scene graph pipeline
auto-activates when the new binary deploys. Zero code changes needed on Webb
side.

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
| ~~esotericWebb V22 sync~~ | eastGate | **PUSHED** to both Forgejo and GitHub |
| ~~primalSpring CAC sync~~ | eastGate | **PUSHED** `8a456bf` to both remotes |
| `loginctl enable-linger` | flockGate ops | **DONE** — confirmed 10h+ uptime |
| `primals.eco` DNSSEC | ops / Cloudflare | Enable via API |
| ~~petalTongue scene unification~~ | petalTongue | **ALL 4 PHASES COMPLETE** — universal rendering engine, 569 scene tests, zero stubs |
| ~~esotericWebb `ui.render` → `visualization.render`~~ | esotericWebb | **V22 FIXED** — `game_scene` SceneGraph + `ui.render` fallback |
| Deploy petalTongue v1.7+ | sporeGate ops | Activates full scene graph pipeline for Webb (auto, no code changes) |
| `footprint_composition.toml` URL | cellMembrane | Update to subdomain URL |
| cellMembrane `gate.enroll` → `mesh.enroll` | cellMembrane | Integration with songBird |
| HSM → Android Keystore | bearDog | grapheneGate backend |
| Credential store trait | bearDog + squirrel | Silicon Atheism Phase 2 |
| Health monitoring trait | ecosystem | nestGate consolidated procfs (Session 122) |
| `primal-transport` crate | ecosystem | Extract transport abstractions |
| primalSpring CAC scenario | primalSpring | **IMPLEMENTED** (171 scenarios, 15 known-debt, 8a456bf) |

### P2 — pseudoSpore Pipeline

| Need | Owner | Detail |
|------|-------|--------|
| `validation.json` per spore | 6 spring teams | Module validation results |
| Fix groundSpring `bingoCube/nautilus` dep | groundSpring | `cargo test` fails |
| Bash → Rust orchestration | spring teams | 114+ shell scripts |

---

## 4. STRATEGIC GOALS

### NOW

- **Deploy petalTongue v1.7+** to flockGate — activates Webb's scene graph pipeline
- **flockGate rebuild** — esotericWebb V22 source now on Forgejo, flockGate rebuilds from source
- **Enable Cloudflare DNSSEC** for `primals.eco`
- **Visual verification** — confirm footPrint tiles + CAS at `footprint.primals.eco`

### NEAR TERM (next 2-4 weeks)

- **pseudoSpore validation**: promote 6 pending spores
- **projectFOUNDATION design**: thread lineage store, nestGate CAS integration
- **strandGate enrollment**: dual EPYC 7452, 256GB RAM, RTX 3090
- **`primal.eco` inner membrane separation**
- **petalTongue Phase 3-4 renderer integration**: SVG viewport from camera (done), 3D geometry in live renderers

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
| **Forgejo push mirrors — 39/39 repos, sync_on_commit** | **150j** |
| **GitHub SSH surface: 12 keys → 2 (relay consolidation)** | **150j** |
| **petalTongue v1.7.0 binary to golgiBody depot** | **150j** |
| **petalTongue scene unification — ALL 4 PHASES COMPLETE** | **150i** |
| **esotericWebb V22 — scene binding fixed (game_scene + fallback)** | **150i** |
| **cellMembrane depot URL subdomain standard** | **150i** |
| **FULL NUCLEUS COMPOSITION WIRED (footPrint CAS + WS consumer)** | **150h** |
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
  ├─ flockGate (10.13.37.6) — esotericWebb [V22 LIVE]
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
| 4 | Sovereignty | **GREEN** | Forgejo-first relay active, DNSSEC remaining (P2) |
| 5 | Depot | GREEN | 16 primals in depot, compositions build from source |
| 6 | Public Surface | **GREEN** | 5+ surfaces LIVE |
| 7 | Glacial Shift | GREEN | SHOW_HN rubric |
| 8 | Compositions | **GREEN** | Both products fully wired |
| 9 | Documentation | GREEN | — |
| 10 | Cascade | GREEN | — |
| 11 | CAC | GREEN | primalSpring scenario (P2) |
| 12 | Silicon Atheism | GREEN | Credential trait (P2) |

---

*Wave 150j: FORGEJO-FIRST RELAY ACTIVE. 39/39 repos have push mirrors with
sync_on_commit — every Forgejo push auto-propagates to GitHub. GitHub SSH
surface consolidated from 12 per-gate keys to 2 (relay + operator). Gates
push to Forgejo only (inner membrane). Sync divergence structurally eliminated.
petalTongue v1.7.0 binary deployed to golgiBody depot. flockGate sync
divergence resolved (V22 + CAC scenario pushed to Forgejo). 6 surfaces LIVE.
11 GREEN / 1 AMBER dimensions. 23,300+ tests.*
