# ecoPrimals Ecosystem Blurb — Wave 150k

**Date**: Jul 19, 2026 08:05 EDT | **Wave**: 150k | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. FULL DIMENSIONAL REVIEW.**

**This wave**: Full dimensional review across all 30+ projects. 7 stale AARs
(Waves 139b–148c) and 1 stale handoff (PETALTONGUE_SCENE_UNIFICATION) fossilized.
**P0 finding**: 28 of 30 repos still have `origin=GitHub` — only petalTongue and
wateringHole are Forgejo-first. All 28 have the `forgejo` remote configured;
swap is a rename operation. **P1 finding**: 3 repos have format drift (biomeOS
2,236 diff lines, petalTongue 1,811, squirrel 41). Scorecard expanded from 10
to 30 projects with actual data.

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

## 3. EXPOSED ISSUES — ACCUMULATING

### P0 — Forgejo-First Remote Swap (28 repos)

Only **petalTongue** and **wateringHole** have `origin=Forgejo`. All other repos
still push to GitHub as origin. Pattern: `git remote rename origin github &&
git remote rename forgejo origin`.

| Category | Repos needing swap | Count |
|----------|-------------------|-------|
| primals/ | barraCuda, bearDog, biomeOS, coralReef, loamSpine, nestGate, rhizoCrypt, skunkBat, songBird, sourDough, squirrel, sweetGrass, toadStool | 13 |
| gardens/ | cellMembrane, esotericWebb, blueFish, helixVision, initioChem, lithoSpore, projectFOUNDATION, projectNUCLEUS | 8 |
| infra/ | sporePrint, plasmidBin, agentReagents, benchScale, bingoCube, fossilRecord, whitePaper | 7 |

### P1 — Format Drift

| Repo | `cargo fmt --check` diff lines |
|------|-------------------------------|
| biomeOS | 2,236 |
| petalTongue | 1,811 |
| squirrel | 41 |

### P1 — Production `.unwrap()` Hotspots

| Repo | Count | Notes |
|------|-------|-------|
| cellMembrane | 551 | Highest — needs audit |
| sporePrint | 349 | Zola templates (likely build-time) |
| petalTongue | 287 | ~286 in tests; 1 in `server_mode.rs` |
| projectFOUNDATION | 219 | foundation-core paths |
| benchScale | 203 | libvirt/VM paths |
| lithoSpore | 147 | |
| bearDog | 57 | All in test modules |
| songBird | 32 | All in `#[cfg(test)]` |

### P2 — `unsafe` Usage

| Repo | Count | Context |
|------|-------|---------|
| barraCuda | 323 | GPU/low-level (`#![forbid(unsafe_code)]` on libs) |
| toadStool | 279 | GPU/runtime |
| projectFOUNDATION | 18 | foundation-core |
| squirrel | 17 | |
| benchScale | 14 | libvirt |
| coralReef | 5 | |
| sourDough | 1 | |

### P2 — Files >800 Lines

| Repo | Files | Notes |
|------|-------|-------|
| esotericWebb | 2 | `client.rs` (855L), `discovery.rs` (813L) |
| coralReef | 2 | Generated ISA files (929L, 801L) |

### P2 — Ecosystem Quality (remaining)

| Need | Owner | Detail |
|------|-------|--------|
| `primals.eco` DNSSEC | ops / Cloudflare | Enable via API |
| Deploy petalTongue v1.7+ | sporeGate ops | Activates full scene graph pipeline for Webb |
| `footprint_composition.toml` URL | cellMembrane | Update to subdomain URL |
| cellMembrane `gate.enroll` → `mesh.enroll` | cellMembrane | Integration with songBird |
| HSM → Android Keystore | bearDog | grapheneGate backend |
| Credential store trait | bearDog + squirrel | Silicon Atheism Phase 2 |
| Health monitoring trait | ecosystem | nestGate consolidated procfs (Session 122) |
| `primal-transport` crate | ecosystem | Extract transport abstractions |

### P2 — pseudoSpore Pipeline

| Need | Owner | Detail |
|------|-------|--------|
| `validation.json` per spore | 6 spring teams | Module validation results |
| Fix groundSpring `bingoCube/nautilus` dep | groundSpring | `cargo test` fails |
| Bash → Rust orchestration | spring teams | 114+ shell scripts |

---

## 4. STRATEGIC GOALS

### NOW

- **Forgejo-first remote swap** — batch rename `origin`→`github`, `forgejo`→`origin` on 28 repos
- **Deploy petalTongue v1.7+** to flockGate — activates Webb's scene graph pipeline
- **flockGate rebuild** — esotericWebb V22 source now on Forgejo, flockGate rebuilds from source
- **`cargo fmt`** on biomeOS, petalTongue, squirrel

### NEAR TERM (next 2-4 weeks)

- **Enable Cloudflare DNSSEC** for `primals.eco`
- **cellMembrane unwrap audit** — 551 production unwraps, highest in ecosystem
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

## 5. DIMENSIONAL SCORECARD (Wave 150k — Full Ecosystem)

### Primals (14)

| Project | Tests | Clippy | Fmt | TODO/FIXME | Unsafe | >800L | `.unwrap()` |
|---------|-------|--------|-----|-----------|--------|-------|-------------|
| barraCuda | 5,153 | 0 | 0 | 0 | 323 (GPU) | 0 | 0 |
| bearDog | 13,884 | 0 | 0 | 0 | 0 | 0 | 57 (test) |
| biomeOS | 8,446 | 0 | **2,236** | 0 | 0 | 0 | 0 |
| coralReef | 3,650 | 0 | 0 | 0 | 5 | 2 (gen) | 0 |
| loamSpine | 1,702 | 0 | 0 | 0 | 0 | 0 | 0 |
| nestGate | 1,710 | 0 | 0 | 0 | 0 | 0 | 0 |
| petalTongue | 6,500 | 0 | **1,811** | 0 | 0 | 0 | 287 (test) |
| rhizoCrypt | 1,878 | 0 | 0 | 0 | 0 | 0 | 0 |
| skunkBat | 567 | 0 | 0 | 0 | 0 | 0 | 0 |
| songBird | 8,929 | 0 | 0 | 0 | 0 | 0 | 32 (test) |
| sourDough | 502 | 0 | 0 | 0 | 1 | 0 | 0 |
| squirrel | 7,171 | 0 | **41** | 0 | 17 | 0 | 0 |
| sweetGrass | 1,608 | 0 | 0 | 0 | 0 | 0 | 0 |
| toadStool | 23,000 | 0 | 0 | 0 | 279 (GPU) | 0 | 0 |

**Primals total**: ~84,700 tests. 0 clippy warnings. 0 TODO/FIXME/HACK.

### Gardens (8)

| Project | Tests | Clippy | Fmt | TODO/FIXME | Unsafe | >800L | `.unwrap()` |
|---------|-------|--------|-----|-----------|--------|-------|-------------|
| cellMembrane | 1,100 | 0 | 0 | 0 | 0 | 0 | 551 |
| esotericWebb | 453 | 0 | 0 | 0 | 0 | 2 | 0 |
| blueFish | — | — | — | 0 | 0 | 0 | 0 |
| helixVision | — | — | — | 0 | 0 | 0 | 0 |
| initioChem | — | — | — | 0 | 0 | 0 | 0 |
| lithoSpore | 227 | 0 | 0 | 0 | 0 | 0 | 147 |
| projectFOUNDATION | — | 0 | 0 | 0 | 18 | 0 | 219 |
| projectNUCLEUS | — | 0 | 0 | 0 | 0 | 0 | 0 |

### Infra (8)

| Project | Tests | Clippy | Fmt | TODO/FIXME | Unsafe | >800L | `.unwrap()` |
|---------|-------|--------|-----|-----------|--------|-------|-------------|
| sporePrint | 289 | — | — | 0 | 0 | 0 | 349 |
| wateringHole | — | — | — | 0 | 0 | 0 | 0 |
| plasmidBin | — | — | — | 0 | 0 | 0 | 16 |
| agentReagents | — | — | — | 0 | 0 | 0 | 33 |
| benchScale | — | — | — | 0 | 14 | 0 | 203 |
| bingoCube | — | — | — | 0 | 0 | 0 | 0 |
| fossilRecord | — | — | — | 0 | 0 | 8 (archive) | 0 |
| whitePaper | — | — | — | 0 | 0 | 0 | 0 |

**Ecosystem totals**: **~62,000+ tests** (tracked). 0 clippy warnings.
0 TODO/FIXME/HACK. 0 mocks. `unsafe` concentrated in GPU primals
(barraCuda 323, toadStool 279) and libvirt tooling (benchScale 14).

---

## 6. COMPLETED MILESTONES

| Milestone | Wave |
|-----------|------|
| **Full dimensional review — 30 projects scored** | **150k** |
| **7 AARs + 1 handoff fossilized (139b–150h)** | **150k** |
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
| 2 | Ecological | **AMBER** | 3 repos need `cargo fmt`; 28 repos wrong remote layout |
| 3 | Hardware | AMBER | 4 gates offline |
| 4 | Sovereignty | **AMBER** | 28/30 repos still origin=GitHub; DNSSEC remaining |
| 5 | Depot | GREEN | 16 primals in depot, compositions build from source |
| 6 | Public Surface | GREEN | 6 surfaces LIVE |
| 7 | Glacial Shift | GREEN | SHOW_HN rubric |
| 8 | Compositions | GREEN | Both products fully wired |
| 9 | Documentation | GREEN | 4 active handoffs, 14 fossilized, 7 AARs fossilized |
| 10 | Cascade | **AMBER** | 28 repos push to wrong origin — cascades hit GitHub not Forgejo |
| 11 | CAC | GREEN | primalSpring scenario (P2) |
| 12 | Silicon Atheism | GREEN | Credential trait (P2) |

**Summary**: 9 GREEN / 3 AMBER. The remote layout gap is the primary blocker —
until all repos have `origin=Forgejo`, the Forgejo-first relay architecture is
incomplete and cascades diverge through GitHub.

---

*Wave 150k: FULL DIMENSIONAL REVIEW. 30 projects scored. 62,000+ tests tracked
ecosystem-wide. 0 clippy warnings. 0 TODO/FIXME/HACK. P0: 28/30 repos need
Forgejo-first remote swap (origin=GitHub → origin=Forgejo). P1: 3 repos need
cargo fmt. 7 stale AARs + 1 handoff fossilized. 9/12 GREEN, 3 AMBER.*
