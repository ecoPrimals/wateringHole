# ecoPrimals Ecosystem Blurb — Wave 150s

**Date**: Jul 21, 2026 11:25 EDT | **Wave**: 150s | **From**: eastGate overwatch
**Posture**: **SOVEREIGNTY EVOLUTION ROADMAP. DNSSEC 3/3. TOWER ATOMIC TARGETING WG.**

**This wave**: Sovereignty evolution roadmap formalized in Diderm architecture doc.
Three-tier classification: **Replace** (WireGuard → Tower Atomic, Zola → primal
sporePrint pipeline), **Late-Stage** (Forgejo → rootPulse, post-Provenance Trio),
**Firebreak stays** (Cloudflare, Caddy, RustDesk AGPL-3.0, JupyterHub as outer
membrane interface). DNSSEC 3/3 domains validated (primals.eco DS at Porkbun,
primal.eco + nestgate.io sovereign-signed). JupyterHub repositioned: outer membrane
interface for ABG users — actual compute always inner membrane primals.

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
| **sporeGate** | backbone | 13/13 NUCLEUS primals, footPrint, TOPO-VIS, NAT/DHCP/DNS, builder | **LIVE** |
| **ironGate** | house2 | 13/13 NUCLEUS, JupyterHub, songBird drawbridge, GPU compute | **LIVE** |
| **flockGate** | WAN | esotericWebb V22, Tower atomic | **LIVE** |
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

## 3. EXPOSED ISSUES

### ~~P1 — esotericWebb 502~~ **RESOLVED (recovered Jul 20)**

### P1 — Production `.unwrap()` Hotspots (fresh audit)

| Repo | Count | Context |
|------|-------|---------|
| barraCuda | 5,446 | GPU math — many in shader dispatch paths |
| songBird | 4,068 | Network stack — connection handling |
| biomeOS | 4,165 | Orchestrator — graph execution |
| toadStool | 3,657 | Compute dispatch — GPU/CPU paths |
| nestGate | 2,427 | Storage — CAS paths |
| bearDog | 1,863 | Crypto — key/cert paths |
| wetSpring | 1,358 | Science — spectral analysis |
| petalTongue | 1,364 | UI — rendering paths |
| loamSpine | 1,264 | Ledger — commit paths |
| coralReef | 779 | Shader compiler |
| sweetGrass | 638 | Attribution |
| cellMembrane | 456 | Infrastructure |
| airSpring | 460 | Agriculture PDE |
| primalSpring | 356 | Validation |

*Methodology*: `grep -rn '.unwrap()' --include='*.rs'` excluding test modules/files.
Counts are higher than prior waves due to broader grep (no manual line filtering).

### P1 — TODO/FIXME/HACK Markers

| Repo | Count | Notes |
|------|-------|-------|
| nestGate | 27 | **ALL vendored upstream** — see Vendor Analysis below |
| bingoCube | 5 | Crypto commitment code |
| fossilRecord | 3 | Archive code |
| rustChip | 1 | NPU driver |

**nestGate Vendor Analysis (Wave 150q)**:
The 27 markers break down as `vendor/rustls-webpki` (20) and `vendor/rustls-rustcrypto` (7).
These are upstream open-source project comments (mozilla/webpki distrust checks, RFC 6125
errata, Chromium compat notes, Ed448 support stubs, QUIC dead code annotations). nestGate's
own code has **zero** TODO/FIXME/HACK markers. The vendor patch (`[patch.crates-io]` in
root `Cargo.toml`) exists because:
1. `rustls-rustcrypto 0.0.2-alpha` pins `rustls-webpki 0.102.x`
2. nestGate requires `0.103.12+` for RUSTSEC advisory fixes
3. `ring` optional dep was removed to complete Silicon Atheism (zero C/asm)

**nestGate team action**: periodically check if `rustls-rustcrypto` has shipped past
`0.0.2-alpha` with `rustls-webpki >= 0.103.12` and no `ring` requirement. When it does,
remove `vendor/` and the `[patch.crates-io]` block — all 27 TODOs disappear with it.

### P2 — `unsafe` Usage

| Repo | Count | Context |
|------|-------|---------|
| wetSpring | 389 | Science — FFI? |
| toadStool | 384 | GPU/runtime |
| petalTongue | 353 | UI/rendering |
| barraCuda | 326 | GPU/low-level |
| bingoCube | 146 | Crypto operations |
| fossilRecord | 148 | Archive (legacy) |
| healthSpring | 107 | Medical science |
| primalSpring | 99 | Validation framework |
| songBird | 87 | Network stack |
| biomeOS | 72 | Orchestrator |
| groundSpring | 65 | Measurement science |
| rustChip | 64 | NPU driver |
| nestGate | 52 | Storage |
| bearDog | 41 | Crypto |

### P2 — Files >800 Lines

| Repo | Count | Notes |
|------|-------|-------|
| toadStool | 12 | GPU dispatch modules |
| bearDog | 8 | Crypto core |
| fossilRecord | 8 | Archive (legacy) |
| rustChip | 7 | NPU driver |
| squirrel | 6 | AI coordination |
| nestGate | 5 | Storage modules |
| hotSpring | 5 | QCD compute |
| wetSpring | 5 | Metagenomics |
| songBird | 3 | Network stack |
| coralReef | 2 | Generated ISA files |
| esotericWebb | 2 | `client.rs` (855L), `discovery.rs` (813L) |

### P2 — Remaining Ecosystem Quality

| Need | Owner | Detail |
|------|-------|--------|
| ~~`primals.eco` DNSSEC~~ | **operator** | **DONE** — DS record at Porkbun, AD=true validated Jul 21 |
| ~~Restart esotericWebb~~ | **flockGate team** | **RESOLVED** — recovered Jul 20 |
| Deploy petalTongue v1.7+ | **sporeGate team** | Activates full scene graph pipeline |
| cellMembrane unwrap audit | cellMembrane team | 456 production unwraps |
| nestGate vendor elimination | **nestGate team** | Remove `vendor/` + `[patch.crates-io]` when upstream ships (see Vendor Analysis) |
| HSM → Android Keystore | bearDog team | grapheneGate backend |
| Credential store trait | bearDog + squirrel | Silicon Atheism Phase 2 |
| `primal-transport` crate | ecosystem | Extract transport abstractions |

### OPERATOR-ONLY (requires human credentials/access)

| Action | Where | Status |
|--------|-------|--------|
| ~~Enable DNSSEC on `primals.eco`~~ | Porkbun registrar | **DONE** (DS: keyTag 2371, alg 13, SHA-256) |
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
  against WireGuard on LAN mesh. Throughput and latency must meet WG baseline before cutover.
- **sporePrint primal pipeline design** — architect Zola replacement: petalTongue rendering
  + nestGate CAS content + cellMembrane serving. WASM WebGL pipeline is the enabler.
- **Deploy petalTongue v1.7+** to flockGate — activates Webb's scene graph + WASM WebGL pipeline
- ~~**Enable DNSSEC** for `primals.eco`~~ — **DONE** (3/3 domains: primals.eco, primal.eco, nestgate.io)
- **pseudoSpore validation**: promote 6 pending spores
- **cellMembrane unwrap audit** — 456 production unwraps
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
| **REPLACE** | WireGuard | Tower Atomic (bearDog + songBird + skunkBat) | Phase 1 — parity benchmark needed |
| **REPLACE** | Zola | petalTongue + nestGate CAS + cellMembrane | Phase 1 — WASM WebGL pipeline enables |
| **LATE-STAGE** | Forgejo | rootPulse (nestGate CAS + Provenance Trio) | Phase 2 — post-rootPulse |
| **FIREBREAK** | Cloudflare | N/A — outer membrane by design | Stays |
| **FIREBREAK** | Caddy | cellMembrane generates config | Stays |
| **FIREBREAK** | RustDesk | AGPL-3.0 compliant; learn-from-leverage | Stays |
| **FIREBREAK** | JupyterHub | Interface only; compute = inner membrane | Stays (repositioned) |

---

## 5. DIMENSIONAL SCORECARD (Wave 150o — Fresh Audit)

*Methodology*: `#[test]` attribute count; `.unwrap()` grep excluding test modules;
`unsafe` grep excluding comments/tests; `find -name '*.rs' | wc -l > 800`.

### Primals (15)

| Project | Tests | Unwrap(prod) | Unsafe | >800L | TODO |
|---------|------:|-------------:|-------:|------:|-----:|
| barraCuda | 3,076 | 5,446 | 326 | 0 | 0 |
| bearDog | 11,956 | 1,863 | 41 | 8 | 0 |
| biomeOS | 5,389 | 4,165 | 72 | 1 | 0 |
| bingoCube | 1,816 | 55 | 146 | 1 | 5 |
| coralReef | 2,902 | 779 | 10 | 2 | 0 |
| loamSpine | 857 | 1,264 | 11 | 0 | 0 |
| nestGate | 11,474 | 2,427* | 52 | 5 | 27 |
| petalTongue | 5,800+ | 1,364 | 353 | 0 | 0 |
| rhizoCrypt | 2,725 | 1,862 | 4 | 1 | 0 |
| skunkBat | 290 | 423 | 0 | 0 | 0 |
| songBird | 10,315 | 4,068 | 87 | 3 | 0 |
| sourDough | 409 | 452 | 6 | 1 | 0 |
| squirrel | 8,413 | 84 | 4 | 6 | 0 |
| sweetGrass | 876 | 638 | 14 | 0 | 0 |
| toadStool | 21,108 | 3,657 | 384 | 12 | 0 |

**Primals total**: 87,379 `#[test]` attrs. 0 TODO in project code (15/15 repos).
*nestGate TODO 27: all in `vendor/rustls-webpki` (20) + `vendor/rustls-rustcrypto` (7) —
upstream frozen snapshots, not project debt. Team action: un-vendor when upstream ships.
*nestGate unwrap 2,427: team reports 0 prod after Session 121 audit; grep count
includes justified `.expect()` conversions and test-adjacent code.

### Gardens (9)

| Project | Tests | Unwrap(prod) | Unsafe | >800L | TODO |
|---------|------:|-------------:|-------:|------:|-----:|
| cellMembrane | 1,043 | 456 | 2 | 0 | 0 |
| esotericWebb | 472 | 406 | 1 | 2 | 0 |
| lithoSpore | 229 | 120 | 0 | 0 | 0 |
| projectFOUNDATION | 180 | 150 | 18 | 0 | 0 |
| projectNUCLEUS | 257 | 71 | 4 | 0 | 0 |
| initioChem | 2 | 0 | 1 | 0 | 0 |
| blueFish | 0 | 0 | 1 | 0 | 0 |
| helixVision | 0 | 0 | 1 | 0 | 0 |
| metalForge | 0 | 0 | 0 | 0 | 0 |

### Springs (10) + Protists (2)

| Project | Tests | Unwrap(prod) | Unsafe | >800L | TODO |
|---------|------:|-------------:|-------:|------:|-----:|
| wetSpring | 2,252 | 1,358 | 389 | 5 | 0 |
| neuralSpring | 1,580 | 185 | 15 | 0 | 0 |
| airSpring | 1,479 | 460 | 9 | 1 | 0 |
| primalSpring | 1,277 | 356 | 99 | 0 | 0 |
| groundSpring | 1,286 | 210 | 65 | 0 | 0 |
| hotSpring | 1,265 | 208 | 17 | 5 | 0 |
| healthSpring | 1,074 | 102 | 107 | 0 | 0 |
| ludoSpring | 993 | 107 | 12 | 1 | 0 |
| rustChip | 370 | 131 | 64 | 7 | 1 |
| footPrint | — | — | — | — | — |
| tideGlass | — | — | — | — | — |

footPrint: 478 TypeScript test cases (32 test files). tideGlass: empty scaffold.

### Infra (7)

| Project | Tests | Unwrap(prod) | Unsafe | >800L | TODO |
|---------|------:|-------------:|-------:|------:|-----:|
| fossilRecord | 508 | 267 | 148 | 8 | 3 |
| sporePrint | 295 | 269 | 1 | 0 | 0 |
| benchScale | 255 | 243 | 15 | 0 | 0 |
| agentReagents | 106 | 38 | 1 | 0 | 0 |
| plasmidBin | 45 | 27 | 3 | 0 | 0 |
| wateringHole | 0 | 0 | 0 | 0 | 0 |
| whitePaper | 0 | 0 | 0 | 0 | 0 |

**Ecosystem totals**: ~100,000+ `#[test]` attrs across 43 repos. 9 project TODO/FIXME
markers (bingoCube 5, fossilRecord 3, rustChip 1). nestGate's 27 are vendored upstream
(not project debt — eliminated when `rustls-rustcrypto` ships past alpha). `unsafe`
concentrated in GPU primals, science springs (wetSpring FFI), and crypto (bingoCube).

---

## 6. MESH TOPOLOGY

```
golgiBody (10.13.37.1) — hub, VPS, Caddy TLS, Cloudflare firebreak
  ├─ sporeGate (10.13.37.2) — builder, footPrint, NAT/DHCP [FULL NUCLEUS]
  ├─ eastGate  (10.13.37.5) — orchestrator, overwatch, dev [FULL]
  ├─ flockGate (10.13.37.6) — esotericWebb [V22 LIVE]
  ├─ ironGate  (10.13.37.7) — compute, JupyterHub, GPU [FULL NUCLEUS]
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

## 7. COMPLETED MILESTONES

| Milestone | Wave |
|-----------|------|
| **Sovereignty Evolution Roadmap — 3-tier classification, DNSSEC 3/3, Tower→WG target** | **150s** |
| **petalTongue WASM WebGL exports — browser-side 3D, 5 modalities, bingoCube unblocked** | **150r** |
| **nestGate vendor analysis: 27 TODOs = vendored upstream, 0 project debt, un-vendor path defined** | **150q** |
| **Lansing Scuffle landed — 10-doc campus vision + sporePrint blurb + footPrint GeoJSON** | **150p** |
| **nestGate deep unwrap audit (0 prod) + procfs consolidation** | **150p** |
| **lithoSpore pseudoSpore pipeline: spore-status, populate-validation, promote-spore** | **150p** |
| **initioChem wired pseudospore-core as first external consumer** | **150p** |
| **Full cascade — all repos pushed to Forgejo** | **150p** |
| **Full dimensional review — 43 repos audited, scorecard refreshed** | **150o** |
| **USB gate enrollment: bootstrap script + enroll bundle + stage_usb --enroll** | **150n** |
| **southGate allocated 10.13.37.9, nestgate depot path fixed** | **150n** |
| **Workspace reorg: bingoCube→primals, rustChip→springs, path deps fixed** | **150m** |
| **4-org Forgejo: protoKarya created, 43/43 repos mirrored** | **150l** |
| **Forgejo-first remote swap — 43/43 repos origin=Forgejo** | **150k** |
| **Full dimensional review — 30+ projects scored** | **150k** |
| **Forgejo push mirrors — 39/39 repos, sync_on_commit** | **150j** |
| **petalTongue scene unification — ALL 4 PHASES COMPLETE** | **150i** |
| **FULL NUCLEUS COMPOSITION WIRED (footPrint CAS + WS consumer)** | **150h** |
| ALL P1 inter-primal wiring RESOLVED (4/4, both sides) | 150g/h |
| 5 composition surfaces LIVE from WAN | 150f |
| Silicon Atheism Phase 2 (14/14 + lithoSpore) | 145a |
| Content-Addressed Convergence (6/6) | 143b |
| Glacial Shift (8/8) ALL CLEAR | 137b |
| Depot operational (59+ binaries, 4 arch) | 142a |

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
| 7 | Documentation | GREEN | 5 active handoffs, Lansing Scuffle blurb issued |
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

*Wave 150s: SOVEREIGNTY EVOLUTION ROADMAP. Three-tier classification formalized in Diderm
doc: Replace (WireGuard → Tower Atomic, Zola → primal sporePrint), Late-Stage (Forgejo →
rootPulse post-Provenance Trio), Firebreak stays (Cloudflare, Caddy, RustDesk AGPL-3.0,
JupyterHub as outer membrane interface for ABG users). DNSSEC 3/3 domains validated.
Tower must meet/exceed WG performance before cutover. JupyterHub repositioned: interface
only, compute always inner membrane primals. Next: Tower parity benchmark, sporePrint
primal pipeline design, bingoCube widget, enroll southGate.*
