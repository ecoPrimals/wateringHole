# ecoPrimals Ecosystem Blurb — Wave 150m

**Date**: Jul 19, 2026 08:40 EDT | **Wave**: 150m | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. 4-ORG FORGEJO. STABILIZED.**

**This wave**: Workspace reorganization finalized — bingoCube moved to primals/
(agnostic crypto tool, not infra), rustChip moved to springs/ (syntheticChemistry
experiment). Broken path deps fixed (airSpring, groundSpring). Org mapping,
scorecard, and manifest updated. Gate standardization instructions added below.
Next focus: **bingoCube on primals.eco via petalTongue** — validates the scene
graph rendering pipeline with an interactive cryptographic commitment widget.

---

## 1. DEPLOYMENT CHAIN

```
User → Cloudflare DNS (*.primals.eco wildcard → golgiBody 157.230.3.183)
  → Caddy on golgiBody (TLS, Host-header routing)
    → WireGuard mesh → target gate → service
```

**Cloudflare status**: All records are **DNS-only** (grey cloud, not proxied).
Wildcard `*.primals.eco` covers all new subdomains automatically — no DNS
changes needed for new services. DNSSEC not yet enabled (P2).
New subdomain routing is owned by **sporeGate hardware team** (Caddy config
via cellMembrane shadow generation).

**URL Standard**: `prefix.primals.eco` subdomain. Root → `sporeprint.primals.eco`.

**Three-Domain Model**: `primals.eco` (intra-membrane) | `primal.eco` (inner) | `nestgate.io` (data service)

**Git Relay**: Forgejo (inner membrane, `git.primals.eco`) → push mirror → GitHub (outer membrane).
Gates push to Forgejo only. golgiBody relays to GitHub on every commit. 43/43 repos mirrored.

### Canonical Workspace Layout (ALL GATES MUST MATCH)

| Forgejo/GitHub Org | Local Dir | Role | Count |
|--------------------|-----------|------|-------|
| ecoPrimals | `primals/` | Core primals (IPC daemons + agnostic tools) | 15 |
| sporeGarden | `gardens/` | Compositions, infrastructure products | 9 |
| syntheticChemistry | `springs/` | Springs, validation, chemistry, experiments | 10 |
| protoKarya | `protists/` | Sovereign products (user-facing apps) | 2 |
| ecoPrimals + synChem | `infra/` | Shared infrastructure (non-primal, non-product) | 7 |

**Gate bootstrap** — to replicate this layout on any new gate:

```bash
mkdir -p ~/Development/ecoPrimals/{primals,gardens,springs,protists,infra}
# Clone all repos from Forgejo (origin) — example for primals:
for repo in barraCuda bearDog biomeOS bingoCube coralReef loamSpine \
  nestGate petalTongue rhizoCrypt skunkBat songBird sourDough \
  squirrel sweetGrass toadStool; do
  git clone ssh://git@git.primals.eco:2222/ecoPrimals/$repo.git primals/$repo
done
# Repeat for gardens/ (sporeGarden org), springs/ (syntheticChemistry),
# protists/ (protoKarya), infra/ (mixed orgs — see ecosystem_manifest.toml)
# Then add github read-only remote:
# git remote add github git@github.com:<org>/<repo>.git
```

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

### esotericWebb — **V22, SCENE BINDING FIXED**

453 tests. 6/9 primals connected. V22 fixes P1 scene binding:
Forward-compatible with petalTongue v1.7+ — scene graph pipeline
auto-activates when the new binary deploys.

### Other surfaces: sporePrint (302 pages), TOPO-VIS, Forgejo, JupyterHub — all LIVE.

---

## 3. EXPOSED ISSUES — ACCUMULATING

### ~~P0 — Forgejo-First Remote Swap~~ **RESOLVED (Wave 150k)**

All **43/43** repos now have `origin=Forgejo`, `github=GitHub`.

### ~~P1 — Format Drift~~ **RESOLVED (Wave 150k)**

`cargo fmt` applied and pushed: biomeOS, petalTongue, squirrel — all clean.

### ~~P1 — Broken Path Deps~~ **RESOLVED (Wave 150l)**

bingoCube path deps fixed in airSpring (`infra/`→`primals/`) and groundSpring
(`primalTools/`→`primals/`). wetSpring was already correct.

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
| `primals.eco` DNSSEC | **operator** | Cloudflare dashboard → DNS → Enable DNSSEC |
| Cloudflare proxy toggle | **operator** | Records are DNS-only; enable proxying for firebreak? |
| Deploy petalTongue v1.7+ | **sporeGate team** | Activates full scene graph pipeline for Webb |
| `footprint_composition.toml` URL | cellMembrane team | Update to subdomain URL |
| cellMembrane `gate.enroll` → `mesh.enroll` | cellMembrane team | Integration with songBird |
| HSM → Android Keystore | bearDog team | grapheneGate backend |
| Credential store trait | bearDog + squirrel teams | Silicon Atheism Phase 2 |
| Health monitoring trait | ecosystem | nestGate consolidated procfs (Session 122) |
| `primal-transport` crate | ecosystem | Extract transport abstractions |

### P2 — pseudoSpore Pipeline

| Need | Owner | Detail |
|------|-------|--------|
| `validation.json` per spore | 6 spring teams | Module validation results |
| Bash → Rust orchestration | spring teams | 114+ shell scripts |

### OPERATOR-ONLY (requires human credentials/access)

| Action | Where | Status |
|--------|-------|--------|
| ~~`sudo rm -rf wetSpring/`~~ | eastGate | **DONE** |
| ~~Add northGate SSH key to Forgejo~~ | git.primals.eco | **DONE** (sporeGate) |
| ~~Verify wildcard DNS for new subdomains~~ | Cloudflare | **CONFIRMED** — `*.primals.eco → 157.230.3.183` |
| Enable DNSSEC on `primals.eco` | Cloudflare dashboard | **PENDING** |
| Consider enabling Cloudflare proxy (orange cloud) | Cloudflare dashboard | **PENDING** — enables DDoS/WAF firebreak |
| Verify push mirrors working | Spot-check GitHub repos | **PENDING** |

---

## 4. TEAM BLURB STATUS

| Team/Project | Gate | State | Needs Blurb? | Priority Task |
|--------------|------|-------|-------------|---------------|
| **petalTongue** | sporeGate | Active, v1.7.0 | **YES** | bingoCube widget + deploy v1.7+ |
| **bingoCube** | (unassigned) | Active, primals/ | **YES** | Interactive widget via petalTongue |
| **cellMembrane** | sporeGate | Active, 1,100 tests | **YES** | Unwrap audit (551) + mesh.enroll |
| **esotericWebb** | flockGate | V22 LIVE | **YES** | Rebuild from Forgejo, petalTongue v1.7+ |
| **footPrint** | flockGate | LIVE, NUCLEUS | **YES** | E2E tutorial, visual verification |
| **projectFOUNDATION** | (unassigned) | 9.5k LOC | **WHEN SPINNING UP** | Thread lineage design |
| **projectNUCLEUS** | (unassigned) | 15k LOC | **WHEN SPINNING UP** | — |
| **metalForge** | (unassigned) | 2.2k LOC | **WHEN SPINNING UP** | Compute node provisioning |
| **initioChem** | (unassigned) | Early | **WHEN SPINNING UP** | pseudospore-core integration |
| blueFish | — | Seed | NO | — |
| helixVision | — | Seed | NO | — |
| tideGlass | flockGate | Empty scaffold | NO | Phase 0 not started |
| coralForge | — | Empty | NO | — |

**Blurb template**: `handoffs/TEAM_STARTUP_BLURB_TEMPLATE.md`

---

## 5. STRATEGIC GOALS

### NOW

- **bingoCube on primals.eco** — interactive crypto commitment widget via petalTongue
  scene graph. Validates petalTongue rendering pipeline (SceneGraph → SVG/WebGL)
  with real data before broader bingoCube deployment. Target: `bingo.primals.eco`
  or sporePrint embed.
- **Deploy petalTongue v1.7+** to flockGate — activates Webb's scene graph pipeline
- **flockGate rebuild** — esotericWebb V22 from Forgejo source
- **cellMembrane unwrap audit** — 551 production unwraps, highest in ecosystem

### NEAR TERM (next 2-4 weeks)

- **Enable Cloudflare DNSSEC** for `primals.eco`
- **pseudoSpore validation**: promote 6 pending spores
- **projectFOUNDATION design**: thread lineage store, nestGate CAS integration
- **strandGate enrollment**: dual EPYC 7452, 256GB RAM, RTX 3090
- **`primal.eco` inner membrane separation**
- **petalTongue live renderer integration**: 3D geometry in WebGL/canvas renderers

### FUTURE (quarter horizon)

- **tideGlass composition**: computational chemistry product
- **primal-transport crate**: publish shared transport abstraction
- **SHOW_HN readiness**: rubric, narrative, demo path
- **fieldGate/biomeGate recovery**

---

## 6. DIMENSIONAL SCORECARD (Wave 150m — Full Ecosystem)

### Primals (15)

| Project | Tests | Clippy | Fmt | TODO/FIXME | Unsafe | >800L | `.unwrap()` |
|---------|-------|--------|-----|-----------|--------|-------|-------------|
| barraCuda | 5,153 | 0 | 0 | 0 | 323 (GPU) | 0 | 0 |
| bearDog | 13,884 | 0 | 0 | 0 | 0 | 0 | 57 (test) |
| **bingoCube** | **73** | 0 | 0 | 0 | 0 | 0 | 0 |
| biomeOS | 8,446 | 0 | 0 | 0 | 0 | 0 | 0 |
| coralReef | 3,650 | 0 | 0 | 0 | 5 | 2 (gen) | 0 |
| loamSpine | 1,702 | 0 | 0 | 0 | 0 | 0 | 0 |
| nestGate | 1,710 | 0 | 0 | 0 | 0 | 0 | 0 |
| petalTongue | 6,500 | 0 | 0 | 0 | 0 | 0 | 287 (test) |
| rhizoCrypt | 1,878 | 0 | 0 | 0 | 0 | 0 | 0 |
| skunkBat | 567 | 0 | 0 | 0 | 0 | 0 | 0 |
| songBird | 8,929 | 0 | 0 | 0 | 0 | 0 | 32 (test) |
| sourDough | 502 | 0 | 0 | 0 | 1 | 0 | 0 |
| squirrel | 7,171 | 0 | 0 | 0 | 17 | 0 | 0 |
| sweetGrass | 1,608 | 0 | 0 | 0 | 0 | 0 | 0 |
| toadStool | 23,000 | 0 | 0 | 0 | 279 (GPU) | 0 | 0 |

**Primals total**: ~84,773 tests. 0 clippy. 0 TODO/FIXME/HACK. 0 `forbid(unsafe)` violations.

### Gardens (9)

| Project | Tests | Clippy | Fmt | TODO/FIXME | Unsafe | >800L | `.unwrap()` |
|---------|-------|--------|-----|-----------|--------|-------|-------------|
| cellMembrane | 1,100 | 0 | 0 | 0 | 0 | 0 | 551 |
| esotericWebb | 453 | 0 | 0 | 0 | 0 | 2 | 0 |
| blueFish | — | — | — | 0 | 0 | 0 | 0 |
| helixVision | — | — | — | 0 | 0 | 0 | 0 |
| initioChem | — | — | — | 0 | 0 | 0 | 0 |
| lithoSpore | 227 | 0 | 0 | 0 | 0 | 0 | 147 |
| **metalForge** | — | — | — | 0 | 0 | 0 | 0 |
| projectFOUNDATION | — | 0 | 0 | 0 | 18 | 0 | 219 |
| projectNUCLEUS | — | 0 | 0 | 0 | 0 | 0 | 0 |

### Springs (10) + Infra (7)

| Project | Tests | Clippy | Fmt | TODO/FIXME | Unsafe | >800L | `.unwrap()` |
|---------|-------|--------|-----|-----------|--------|-------|-------------|
| **rustChip** | **370** | 0 | 0 | 0 | 0 | 0 | 0 |
| **coralForge** | — | — | — | 0 | 0 | 0 | 0 |
| sporePrint | 289 | — | — | 0 | 0 | 0 | 349 |
| wateringHole | — | — | — | 0 | 0 | 0 | 0 |
| plasmidBin | — | — | — | 0 | 0 | 0 | 16 |
| agentReagents | — | — | — | 0 | 0 | 0 | 33 |
| benchScale | — | — | — | 0 | 14 | 0 | 203 |
| fossilRecord | — | — | — | 0 | 0 | 8 (archive) | 0 |
| whitePaper | — | — | — | 0 | 0 | 0 | 0 |

**Ecosystem totals**: **~62,500+ tests** (tracked). 0 clippy warnings.
0 TODO/FIXME/HACK. 0 mocks. `unsafe` concentrated in GPU primals
(barraCuda 323, toadStool 279) and libvirt tooling (benchScale 14).

---

## 7. COMPLETED MILESTONES

| Milestone | Wave |
|-----------|------|
| **Workspace reorg: bingoCube→primals, rustChip→springs, path deps fixed** | **150m** |
| **4-org Forgejo: protoKarya created, 43/43 repos mirrored** | **150l** |
| **cellMembrane canonicalized under sporeGarden** | **150l** |
| **metalForge + coralForge cloned + registered on Forgejo** | **150l** |
| **GitHub duplicates archived (ecoPrimals/{benchScale,agentReagents})** | **150l** |
| **Stale root dirs cleaned (fossilRecord/, primalTools/)** | **150l** |
| **Forgejo-first remote swap — 43/43 repos origin=Forgejo** | **150k** |
| **cargo fmt — biomeOS, petalTongue, squirrel (0 drift)** | **150k** |
| **Full dimensional review — 30+ projects scored** | **150k** |
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
| Silicon Atheism Phase 2 (14/14 + lithoSpore) | 145a |
| Content-Addressed Convergence (6/6) | 143b |
| Glacial Shift (8/8) ALL CLEAR | 137b |
| Depot operational (59+ binaries, 4 arch) | 142a |

---

## 8. MESH TOPOLOGY

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

## 9. ORTHOGONAL DIMENSIONS

| Dim | Area | Status | Open items |
|-----|------|--------|------------|
| 1 | Temporal | GREEN | — |
| 2 | Ecological | GREEN | fmt clean, remote swap complete, path deps fixed |
| 3 | Hardware | AMBER | 4 gates offline |
| 4 | Sovereignty | GREEN | 43/43 Forgejo-first; DNSSEC remaining (P2) |
| 5 | Depot | GREEN | 15 primals in depot, compositions build from source |
| 6 | Public Surface | GREEN | 6 surfaces LIVE |
| 7 | Glacial Shift | GREEN | SHOW_HN rubric |
| 8 | Compositions | GREEN | Both products fully wired |
| 9 | Documentation | GREEN | 4 active handoffs, 14 fossilized, 8 AARs fossilized |
| 10 | Cascade | GREEN | All repos push to Forgejo; mirrors relay to GitHub |
| 11 | CAC | GREEN | primalSpring scenario (P2) |
| 12 | Silicon Atheism | GREEN | Credential trait (P2) |

**Summary**: 11 GREEN / 1 AMBER (hardware only — not blocking).

---

*Wave 150m: WORKSPACE FINALIZED. bingoCube→primals/ (agnostic tool, not infra),
rustChip→springs/ (syntheticChemistry experiment). Broken path deps fixed in
airSpring + groundSpring. Gate standardization instructions published — canonical
5-dir layout with bootstrap script. Next: bingoCube on primals.eco as interactive
petalTongue widget — validates scene graph pipeline with real cryptographic data.
43/43 repos across 4 Forgejo orgs. 62,500+ tests. 11/12 GREEN.*
