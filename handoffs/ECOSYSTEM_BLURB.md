# ecoPrimals Ecosystem Blurb — Wave 150p

**Date**: Jul 20, 2026 10:30 EDT | **Wave**: 150p | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 5-GATE ACTIVE MESH. LANSING SCUFFLE LANDED.**

**This wave**: Full cascade — all repos pushed to Forgejo. Dimensional review (150o)
plus incoming evolutions: nestGate deep unwrap audit (0 prod unwrap, procfs
consolidation), lithoSpore pseudoSpore pipeline matured (spore-status +
populate-validation + promote-spore), initioChem wired pseudospore-core.
**Lansing Scuffle** — 10-document campus vision landed in whitePaper, sporePrint
team blurb issued, footPrint GeoJSON location added. southGate IP corrected
to .9 (northGate is .8). webb.primals.eco 502 (flockGate needs restart).

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
| **flockGate** | WAN | esotericWebb (process down — 502), Tower atomic | **DEGRADED** |
| **grapheneGate** | mobile | Tower (bearDog + songBird + skunkBat) | **LIVE** |
| **eastGate** | backbone | Dev workstation — primals run ad-hoc for testing | **DEV** |
| **northGate** | house1 | RustDesk running. WireGuard active (.8). No primals deployed yet | **ENROLLED** |

### Live Surfaces (WAN-validated Jul 20, 2026)

| Surface | URL | HTTP | Gate |
|---------|-----|------|------|
| sporePrint | `sporeprint.primals.eco` | **200** (266ms) | golgiBody |
| footPrint | `footprint.primals.eco` | **200** (332ms) | sporeGate |
| TOPO-VIS | `live.primals.eco` | **200** (463ms) | sporeGate |
| Forgejo | `git.primals.eco` | **200** (291ms) | golgiBody |
| JupyterHub | `lab.primals.eco` | **401** (257ms) — auth expected | ironGate |
| esotericWebb | `webb.primals.eco` | **502** — process down | flockGate |

---

## 3. EXPOSED ISSUES

### P1 — esotericWebb 502

`webb.primals.eco` returning 502. Caddy TLS terminates fine but the backend
(esotericWebb on flockGate) is not responding. Needs process restart on flockGate.

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
| nestGate | 27 | Storage paths — needs triage |
| bingoCube | 5 | Crypto commitment code |
| fossilRecord | 3 | Archive code |
| rustChip | 1 | NPU driver |

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
| `primals.eco` DNSSEC | **operator** | Cloudflare dashboard → Enable DNSSEC |
| Restart esotericWebb | **flockGate team** | Process down, 502 on webb.primals.eco |
| Deploy petalTongue v1.7+ | **sporeGate team** | Activates full scene graph pipeline |
| cellMembrane unwrap audit | cellMembrane team | 456 production unwraps |
| nestGate TODO triage | nestGate team | 27 markers — team audit in progress (Session 120-122) |
| HSM → Android Keystore | bearDog team | grapheneGate backend |
| Credential store trait | bearDog + squirrel | Silicon Atheism Phase 2 |
| `primal-transport` crate | ecosystem | Extract transport abstractions |

### OPERATOR-ONLY (requires human credentials/access)

| Action | Where | Status |
|--------|-------|--------|
| Enable DNSSEC on `primals.eco` | Cloudflare dashboard | **PENDING** |
| Consider Cloudflare proxy (orange cloud) | Cloudflare dashboard | **PENDING** |
| Verify push mirrors working | Spot-check GitHub repos | **PENDING** |

---

## 4. STRATEGIC GOALS

### NOW

- **Lansing Scuffle → sporePrint** — transplant campus vision into public pages
  (consulting.md, companies.md, scuffle.md, thermal.md — see `SPOREPRINT_LANSING_SCUFFLE_BLURB.md`)
- **Restart esotericWebb on flockGate** — 502, process down
- **southGate USB enrollment** — USB staged, IP allocated (.9), plug and bootstrap
- **bingoCube on primals.eco** — interactive crypto commitment widget via petalTongue

### NEAR TERM (next 2-4 weeks)

- **Deploy petalTongue v1.7+** to flockGate — activates Webb's scene graph pipeline
- **Enable Cloudflare DNSSEC** for `primals.eco`
- **pseudoSpore validation**: promote 6 pending spores
- **cellMembrane unwrap audit** — 456 production unwraps
- **strandGate enrollment**: dual EPYC 7452, 256GB RAM, RTX 3090

### FUTURE (quarter horizon)

- **projectFOUNDATION design**: thread lineage store, nestGate CAS integration
- **tideGlass composition**: computational chemistry product (shelved)
- **primal-transport crate**: publish shared transport abstraction
- **SHOW_HN readiness**: rubric, narrative, demo path
- **`primal.eco` inner membrane separation**

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
| petalTongue | 5,773 | 1,364 | 353 | 0 | 0 |
| rhizoCrypt | 2,725 | 1,862 | 4 | 1 | 0 |
| skunkBat | 290 | 423 | 0 | 0 | 0 |
| songBird | 10,315 | 4,068 | 87 | 3 | 0 |
| sourDough | 409 | 452 | 6 | 1 | 0 |
| squirrel | 8,413 | 84 | 4 | 6 | 0 |
| sweetGrass | 876 | 638 | 14 | 0 | 0 |
| toadStool | 21,108 | 3,657 | 384 | 12 | 0 |

**Primals total**: 87,379 `#[test]` attrs. 0 TODO in 13/15 repos.
*nestGate: team reports 0 prod `.unwrap()` after Session 121 audit; grep count
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

**Ecosystem totals**: ~100,000+ `#[test]` attrs across 43 repos. 36 TODO/FIXME markers
(nestGate 27, bingoCube 5, fossilRecord 3, rustChip 1). `unsafe` concentrated in
GPU primals, science springs (wetSpring FFI), and crypto (bingoCube).

---

## 6. MESH TOPOLOGY

```
golgiBody (10.13.37.1) — hub, VPS, Caddy TLS, Cloudflare firebreak
  ├─ sporeGate (10.13.37.2) — builder, footPrint, NAT/DHCP [FULL NUCLEUS]
  ├─ eastGate  (10.13.37.5) — orchestrator, overwatch, dev [FULL]
  ├─ flockGate (10.13.37.6) — esotericWebb [502 — needs restart]
  ├─ ironGate  (10.13.37.7) — compute, JupyterHub, GPU [FULL NUCLEUS]
  └─ northGate (10.13.37.8) — Windows, RTX 5090 [enrolled, no primals yet]

Pending USB enrollment:
  └─ southGate (10.13.37.9) — house2, full NUCLEUS [USB READY]

Offline: westGate, fieldGate (dead CMOS), biomeGate (kernel), strandGate (pending)
```

**WG mesh health** (Jul 20, 2026): All 5 active peers have handshakes within 2 minutes.

**WG IP allocation**:
.1=golgiBody, .2=sporeGate, .5=eastGate, .6=flockGate, .7=ironGate,
.8=northGate, .9=southGate (pending). Available: .3, .4, .10+

---

## 7. COMPLETED MILESTONES

| Milestone | Wave |
|-----------|------|
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

| Dim | Area | Status | Open items |
|-----|------|--------|------------|
| 1 | Temporal | GREEN | wave.toml current, 0 active impulses |
| 2 | Ecological | AMBER | nestGate 27 TODOs, high unwrap counts across primals |
| 3 | Hardware | AMBER | 4 gates offline, webb 502, southGate pending |
| 4 | Sovereignty | GREEN | 43/43 Forgejo-first; DNSSEC remaining (P2) |
| 5 | Depot | GREEN | 13 primals in depot, USB enrollment ready |
| 6 | Public Surface | AMBER | webb.primals.eco 502 (5/6 surfaces healthy) |
| 7 | Glacial Shift | GREEN | SHOW_HN rubric pending |
| 8 | Compositions | GREEN | Both products wired, footPrint LIVE |
| 9 | Documentation | GREEN | 5 active handoffs (Lansing Scuffle blurb new), 8 fossilized, 14 AARs |
| 10 | Cascade | GREEN | 43/43 Forgejo-first, mirrors operational |
| 11 | CAC | GREEN | primalSpring scenario (P2) |
| 12 | Silicon Atheism | GREEN | Credential trait (P2) |

**Summary**: 9 GREEN / 3 AMBER (ecological debt, hardware gaps, surface 502).

---

*Wave 150p: FULL CASCADE + LANSING SCUFFLE. All repos pushed to Forgejo. nestGate
deep unwrap audit (0 prod unwrap, procfs→linux_proc). lithoSpore pseudoSpore
pipeline matured (3 new CLI commands). initioChem wired pseudospore-core. Lansing
Scuffle — 10-document 464K SF campus vision landed in whitePaper, sporePrint team
blurb issued (4 new pages + 4 updates), footPrint GeoJSON location added. webb 502
(flockGate). southGate .9 allocated. 43/43 repos on Forgejo. 100k+ tests. 9/12
GREEN, 3 AMBER. Next: sporePrint Scuffle pages, restart webb, enroll southGate.*
