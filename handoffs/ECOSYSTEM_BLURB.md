# ecoPrimals Ecosystem Blurb — Wave 150v

**Date**: Jul 22, 2026 07:20 EDT | **Wave**: 150v | **From**: eastGate overwatch
**Posture**: **TOWER ATOMIC LIVE. STRUCTURAL 21/21 GREEN. WAN-FIRST BENCHMARK SPINNING UP.**

**This wave**: **sporeGate + flockGate AARs received** — both gates Tower Atomic 3/3 LIVE,
structural 21/21 GREEN, convergence rule followed (zero code changes). WG baselines measured:
sporeGate→golgiBody 38ms, flockGate→golgiBody 31ms, end-to-end ~66-68ms. **esotericWebb V22
confirmed healthy** on flockGate (was 502 in 150o — recovered). **Two blockers identified**:
golgiBody TURN relay not deployed (code complete, needs systemd unit), benchmark harness not
built (`songbird benchmark` CLI). primalSpring doc warning fixed (registry.rs:55). `cargo fmt`
clean. cellMembrane unwrap RESOLVED (false positive). 43/43 repos converged.

---

## 1. DEPLOYMENT CHAIN

```
User → Cloudflare DNS (*.primals.eco wildcard → golgiBody 157.230.3.183)
  → Caddy on golgiBody (TLS, Host-header routing)
    → WireGuard mesh → target gate → service
```

**Cloudflare status**: All records are **DNS-only** (grey cloud, not proxied).
Wildcard `*.primals.eco` covers all new subdomains automatically — no DNS
changes needed for new services. **DNSSEC enabled** (3/3 domains validated — Jul 21).

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

### Gate Bootstrap

**USB enrollment** (new gates — offline bootstrap):

```bash
# 1. Stage USB on eastGate (or any builder gate)
cd infra/plasmidBin
./stage_usb.sh --dest /mnt/usb/ecoprimals --composition full --enroll --verify

# 2. Edit enroll/gate-template.toml on USB with gate name + IP
# 3. Plug USB into target, run:
sudo ./gate-usb-bootstrap.sh

# Script installs WireGuard, configures mesh, deploys primal binaries,
# installs + configures RustDesk pointing at relay (remote.primals.eco),
# prints RustDesk ID + WG pubkey for operator.
#
# 4. Add WG peer on golgiBody (printed by script)
# 5. RustDesk in, Cursor agent runs: membrane gate.enroll <name>
# If automation fails: see enroll/RELAY_MANUAL.md
```

**Manual clone** (for gates already on the mesh):

```bash
mkdir -p ~/Development/ecoPrimals/{primals,gardens,springs,protists,infra}
for repo in barraCuda bearDog biomeOS bingoCube coralReef loamSpine \
  nestGate petalTongue rhizoCrypt skunkBat songBird sourDough \
  squirrel sweetGrass toadStool; do
  git clone ssh://git@git.primals.eco:2222/ecoPrimals/$repo.git primals/$repo
done
# Repeat for gardens/ (sporeGarden org), springs/ (syntheticChemistry),
# protists/ (protoKarya), infra/ (mixed orgs — see ecosystem_manifest.toml)
```

---

## 2. RUNTIME — What's Actually Running Where

Dev (repos cloned) ≠ Runtime (services live). This section tracks **runtime**.

| Gate | Zone | Running Services | Status |
|------|------|-----------------|--------|
| **golgiBody** | VPS | Forgejo, Caddy TLS, RustDesk relay, sporePrint, depot, push mirrors | **LIVE** |
| **sporeGate** | backbone | 13/13 NUCLEUS, footPrint, TOPO-VIS, NAT/DHCP/DNS, Tower 3/3, primalSpring | **LIVE** |
| **ironGate** | house2 | 13/13 NUCLEUS, JupyterHub, songBird drawbridge, GPU compute | **DOWN** (hw) |
| **flockGate** | WAN | esotericWebb V22, Tower 3/3 (since Jul 16), primalSpring | **LIVE** |
| **grapheneGate** | mobile | Tower (bearDog + songBird + skunkBat) | **LIVE** |
| **eastGate** | backbone | Dev workstation — primals run ad-hoc for testing | **DEV** |
| **northGate** | house1 | RustDesk running. WireGuard active (.8). No primals deployed yet | **ENROLLED** |

### Live Surfaces (WAN-validated Jul 21, 2026)

| Surface | URL | HTTP | Gate |
|---------|-----|------|------|
| sporePrint | `sporeprint.primals.eco` | **200** (340ms) | golgiBody |
| footPrint | `footprint.primals.eco` | **200** (368ms) | sporeGate |
| TOPO-VIS | `live.primals.eco` | **200** (442ms) | sporeGate |
| Forgejo | `git.primals.eco` | **200** (332ms) | golgiBody |
| JupyterHub | `lab.primals.eco` | **401** (275ms) — auth expected | ironGate |
| esotericWebb | `webb.primals.eco` | **200** (338ms) | flockGate |

---

## 3. OPEN ISSUES + TEAM ACTIONS

### Code Quality (Wave 150o audit — details in ORTHOGONAL_DIMENSIONS_REVIEW.md)

- **`.unwrap()` methodology corrected**: grep over-counts `#[cfg(test)]` module bodies.
  Canonical: `cargo clippy -- -W clippy::unwrap_used`. Confirmed **0 prod unwraps**:
  nestGate, loamSpine, toadStool, esotericWebb, cellMembrane. Remaining primals need audit.
- **TODO markers**: 9 project TODOs (bingoCube 5, fossilRecord 3, rustChip 1).
  nestGate's 27 are vendored upstream — un-vendor when `rustls-rustcrypto` ships past alpha.
- **`unsafe`**: Concentrated in GPU primals, science FFI, crypto. See scorecard for counts.

### Team Actions (Wave 150u — full blurbs in `WAVE150U_TEAM_EVOLUTION_BLURBS.md`)

| # | Need | Owner | Pri | Status |
|---|------|-------|-----|--------|
| 1 | Android Keystore backend + grapheneGate test | bearDog (southGate) | **P1** | NEW |
| 2 | CredentialStore integration via `secrets.*` | squirrel (eastGate) | **P1** | Handoff issued |
| 3a | Tower parity structural scenario | primalSpring (eastGate) | **P1** | **DONE** — 21/21 checks, AAR filed |
| 3b | WAN benchmark — flockGate peer | flockGate team | **P1** | **READY** — Tower 3/3 LIVE, WG baseline 31ms, AAR filed |
| 3c | WAN benchmark — sporeGate peer | sporeGate team | **P1** | **READY** — Tower 3/3 LIVE, WG baseline 38ms, AAR filed |
| 3d | **TURN relay deploy on golgiBody** | golgiBody ops / songBird | **P0** | **BLOCKER** — code complete, needs systemd unit |
| 3e | **Benchmark harness** (`songbird benchmark`) | songBird (eastGate) | **P1** | **BLOCKER** — CLI not yet built |
| 3f | LAN benchmark (sporeGate↔eastGate) | sporeGate + eastGate | **P1** | READY — same backbone LAN |
| 3g | WAN latency target recalibration | primalSpring (eastGate) | **P3** | WG=68ms 2-hop, spec says <50ms |
| 4 | Deploy petalTongue v1.7+ to flockGate | sporeGate ops | **P1** | Binary in depot |
| 5 | Lansing Scuffle pages + primal pipeline | sporePrint (flockGate) | **P1** | Blurb issued |
| 6 | ~~cellMembrane unwrap audit~~ | **RESOLVED** | — | 0 prod unwraps (false positive) |
| 7 | Promote 6 pending pseudoSpores | lithoSpore (strandGate) | **P2** | Stream std v1.0 |
| 8 | bingoCube WASM WebGL widget | bingoCube (eastGate) | **P2** | Unblocked (150r) |
| 9 | footPrint declarative source registry | footPrint (flockGate) | **P2** | Spec committed |
| 10 | pseudoSpore Explorer prototype | esotericWebb (ironGate) | **P3** | Concept |
| — | ~~nestGate vendor elimination~~ | **DONE** | — | vendor/ removed (150u) |
| — | ~~Credential store trait~~ | **SHIPPED** | — | FileVault + secrets.* (150u) |

### Operator Actions

| Action | Where | Status |
|--------|-------|--------|
| southGate USB enrollment | eastGate → house2 | **P1** — USB staged, .9 allocated |
| strandGate enrollment | eastGate → strandGate | **P1** — dual EPYC, 256GB, pending |
| Consider Cloudflare proxy (orange cloud) | Cloudflare dashboard | **PENDING** |
| Verify push mirrors working | Spot-check GitHub repos | **PENDING** |

---

## 4. STRATEGIC GOALS

### NOW

- **bingoCube on primals.eco** — **UNBLOCKED** by petalTongue WASM WebGL (Wave 150r).
  `render_color_grid_webgl` export ready. Needs bingoCube team to consume it.
- **Lansing Scuffle → sporePrint** — transplant campus vision into public pages
  (consulting.md, companies.md, scuffle.md, thermal.md — see `SPOREPRINT_LANSING_SCUFFLE_BLURB.md`)
- **southGate USB enrollment** — USB staged, IP allocated (.9), plug and bootstrap

### NEAR TERM (next 2-4 weeks)

- **Tower Atomic parity assessment** — benchmark Tower (bearDog + songBird + skunkBat)
  against WireGuard. Initial goal: **parity** (any tractable first solution). WireGuard has
  years of dev time on us — we aim to match, then evolve past. Parity is the floor, not the
  ceiling. **Blockers**: golgiBody TURN relay deploy (P0), benchmark harness build (P1).
- **sporePrint primal pipeline design** — architect Zola replacement: petalTongue rendering
  + nestGate CAS content + cellMembrane serving. WASM WebGL pipeline is the enabler.
- **Deploy petalTongue v1.7+** to flockGate — activates Webb's scene graph + WASM WebGL pipeline
- **pseudoSpore validation**: promote 6 pending spores
- ~~cellMembrane unwrap audit~~ — **RESOLVED** (0 prod unwraps, false positive)
- **strandGate enrollment**: dual EPYC 7452, 256GB RAM, RTX 3090

### FUTURE (quarter horizon)

- **rootPulse design**: sovereign version control over nestGate CAS + Provenance Trio
  (rhizoCrypt lineage, loamSpine ledger, sweetGrass attribution) — Forgejo replacement path
- **projectFOUNDATION design**: thread lineage store, nestGate CAS integration
- **tideGlass composition**: computational chemistry product (shelved)
- **primal-transport crate**: publish shared transport abstraction
- **SHOW_HN readiness**: rubric, narrative, demo path
- **`primal.eco` inner membrane separation**

### SOVEREIGNTY EVOLUTION (Diderm Roadmap — Wave 150s)

| Tier | Tool | Primal Path | Status |
|------|------|-------------|--------|
| **REPLACE** | WireGuard | Tower Atomic (bearDog + songBird + skunkBat) | Phase 1 — parity first, then exceed. Gates READY, blockers: TURN + harness |
| **REPLACE** | Zola | petalTongue + nestGate CAS + cellMembrane | Phase 1 — WASM WebGL pipeline enables |
| **LATE-STAGE** | Forgejo | rootPulse (nestGate CAS + Provenance Trio) | Phase 2 — post-rootPulse |
| **FIREBREAK** | Cloudflare | N/A — outer membrane by design | Stays |
| **FIREBREAK** | Caddy | cellMembrane generates config | Stays |
| **FIREBREAK** | RustDesk | AGPL-3.0 compliant; learn-from-leverage | Stays |
| **FIREBREAK** | JupyterHub | Interface only; compute = inner membrane | Stays (repositioned) |

---

## 5. ECOSYSTEM HEALTH SUMMARY (Wave 150o audit)

| Category | Primals (15) | Gardens (9) | Springs+Protists (12) | Infra (7) | Total |
|----------|-------------|------------|----------------------|-----------|-------|
| `#[test]` attrs | 87,379 | 2,183 | 14,405 | 1,209 | **~105K** |
| Project TODOs | 5 (bingoCube) | 0 | 1 (rustChip) | 3 (fossilRecord) | **9** |

nestGate's 27 TODO markers are vendored upstream (`rustls-webpki`/`rustls-rustcrypto`) —
0 project debt. Team action: un-vendor when `rustls-rustcrypto` ships past alpha.

*Full per-repo scorecard (tests, unwraps, unsafe, >800L files) in `ORTHOGONAL_DIMENSIONS_REVIEW.md`.*

---

## 6. MESH TOPOLOGY

```
golgiBody (10.13.37.1) — hub, VPS, Caddy TLS, Cloudflare firebreak [TURN relay needed]
  ├─ sporeGate (10.13.37.2) — builder, footPrint, Tower 3/3 [FULL NUCLEUS + BENCHMARK]
  ├─ eastGate  (10.13.37.5) — orchestrator, overwatch, dev [FULL]
  ├─ flockGate (10.13.37.6) — esotericWebb V22, Tower 3/3 [WAN PEER READY]
  ├─ ironGate  (10.13.37.7) — compute, JupyterHub, GPU [DOWN — hw offline]
  └─ northGate (10.13.37.8) — Windows, RTX 5090 [enrolled, no primals yet]

Pending USB enrollment:
  └─ southGate (10.13.37.9) — house2, full NUCLEUS [USB READY]

Offline: westGate, fieldGate (dead CMOS), biomeGate (kernel), strandGate (pending)
```

**WG mesh health** (Jul 21, 2026): All 5 active peers healthy. 6/6 surfaces 200.

**WG IP allocation**:
.1=golgiBody, .2=sporeGate, .5=eastGate, .6=flockGate, .7=ironGate,
.8=northGate, .9=southGate (pending). Available: .3, .4, .10+

---

## 7. RECENT MILESTONES

| Milestone | Wave |
|-----------|------|
| Tower Atomic structural GREEN (21/21), cellMembrane unwrap resolved, WAN benchmark spin-up | **150v** |
| Cascade convergence — vendor eliminated, credential store, Tower parity spec | **150u** |
| Standards reorganized — 37 → 4 dirs, root 4 docs, full dimensional review | **150t** |
| Sovereignty Evolution Roadmap — 3-tier classification, DNSSEC 3/3 | **150s** |
| petalTongue WASM WebGL — browser-side 3D, bingoCube unblocked | **150r** |
| nestGate vendor analysis — 27 TODOs = vendored upstream, 0 debt | **150q** |
| Lansing Scuffle + nestGate unwrap audit + lithoSpore pipeline | **150p** |
| Full dimensional review — 43 repos audited, scorecard refreshed | **150o** |
| USB gate enrollment + southGate allocated | **150n** |
| Workspace reorg + 4-org Forgejo (43/43 mirrored) | **150l-m** |
| Forgejo-first (43/43) + push mirrors (sync_on_commit) | **150j-k** |

*Earlier milestones (fossilized): scene unification (150i), NUCLEUS wired (150h),
Silicon Atheism P2 14/14 (145a), CAC 6/6 (143b), Depot (142a), Glacial Shift 8/8 (137b).*

---

## 8. ORTHOGONAL DIMENSIONS

### Active Dimensions

| Dim | Area | Status | Open items |
|-----|------|--------|------------|
| 1 | Temporal | GREEN | wave.toml current, 0 impulses, 5 handoffs |
| 2 | Ecological | GREEN | 0 project TODOs (15/15 primals); nestGate vendor cleanup is team action |
| 3 | Hardware | AMBER | 4 gates offline, southGate pending USB enrollment |
| 4 | Sovereignty | GREEN | DNSSEC 3/3; evolution roadmap: WG→Tower (P1), Zola→primal (P1), Forgejo→rootPulse (P2) |
| 5 | Public Surface | GREEN | 6/6 surfaces healthy (webb recovered) |
| 6 | Compositions | GREEN | pseudoSpore pipeline maturing, 6 validation.json pending |
| 7 | Documentation | GREEN | Standards reorganized (4 dirs), 5 handoffs, Scuffle blurb |
| 8 | Campus/Physical | GREEN | Vision documented; sporePrint pages pending |

### Fossilized Dimensions (complete, not re-checked)

| Dim | Area | Fossilized | Completed |
|-----|------|-----------|-----------|
| F1 | Glacial Shift | 150p | 137b — 8/8 ALL CLEAR |
| F2 | CAC | 150p | 143b — 6/6 layers complete |
| F3 | Silicon Atheism | 150p | 145a — Phase 1+2 complete (14/14) |
| F4 | Depot / Build | 150p | 150n — fully operational |
| F5 | Cascade Pipeline | 150p | 150k — 43/43 converged |

**Summary**: 8 active (7 GREEN / 1 AMBER hardware) + 5 fossilized (all GREEN).

---

*Wave 150v: sporeGate + flockGate AARs received — both gates Tower Atomic 3/3 LIVE,
structural 21/21 GREEN, convergence rule followed (zero code changes). WG baselines:
sporeGate→golgiBody 38ms, flockGate→golgiBody 31ms, end-to-end 66-68ms. esotericWebb V22
healthy (recovered from 502). Two blockers: golgiBody TURN relay needs deploy (P0),
benchmark harness needs build (P1). primalSpring doc warning fixed, cargo fmt clean.
Flaky s_depot_architecture_coverage test noted (P2). WAN latency target may need
recalibration (WG=68ms on 2-hop exceeds <50ms spec). Next: deploy TURN relay on golgiBody,
build songbird benchmark CLI, execute WAN parity, sporePrint pipeline, southGate enrollment.*
