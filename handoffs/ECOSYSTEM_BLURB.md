# ecoPrimals Ecosystem Blurb — Wave 150u

**Date**: Jul 21, 2026 14:10 EDT | **Wave**: 150u | **From**: eastGate overwatch
**Posture**: **CASCADE CONVERGENCE. VENDOR ELIMINATED. TOWER PARITY SPEC. CREDENTIAL STORE SHIPPED.**

**This wave**: Full cascade across 43 repos — 15 with incoming evolution pulled and
converged. Major threads: **nestGate vendor elimination COMPLETE** (vendor/ dir removed,
BLAKE3 crypto consolidated, 27 upstream TODOs gone). **bearDog CredentialStore trait
shipped** (InMemory + FileVault backends, `secrets.*` JSON-RPC, squirrel handoff issued —
Silicon Atheism evolving edge resolved). **songBird Tower Atomic convergence brief** —
parity benchmark spec defined, `mesh.enroll` LIVE with BTSP-HMAC proof. **toadStool
S337-S339** deep debt — hot-path `Cow<str>`, 3 structural splits, Rust 1.96 clippy sweep
(251 files, 0 warnings). **lithoSpore Validation Data Stream standard v1.0** — contract
for all spring teams. **footPrint** Lansing Scuffle GeoJSON + data layer primal abstraction
spec. **loamSpine** doc trim (757→207L). **esotericWebb** IPC refactor (<800L). Standards
reorganized (37 → 4 dirs). DNSSEC 3/3. 43/43 repos converged.

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

## 3. OPEN ISSUES + TEAM ACTIONS

### Code Quality (Wave 150o audit — details in ORTHOGONAL_DIMENSIONS_REVIEW.md)

- **`.unwrap()` hotspots**: Top 5 — barraCuda (5,446), biomeOS (4,165), songBird (4,068),
  toadStool (3,657), nestGate (2,427*). 14 repos with 100+ production unwraps.
- **TODO markers**: 9 project TODOs (bingoCube 5, fossilRecord 3, rustChip 1).
  nestGate's 27 are vendored upstream — un-vendor when `rustls-rustcrypto` ships past alpha.
- **`unsafe`**: Concentrated in GPU primals, science FFI, crypto. See scorecard for counts.

### Team Actions

| Need | Owner | Detail |
|------|-------|--------|
| Deploy petalTongue v1.7+ | **sporeGate team** | Activates scene graph + WASM WebGL |
| cellMembrane unwrap audit | cellMembrane team | 456 production unwraps |
| ~~nestGate vendor elimination~~ | **DONE** | vendor/ removed, BLAKE3 consolidated (150u) |
| HSM → Android Keystore | bearDog team | grapheneGate backend |
| ~~Credential store trait~~ | **SHIPPED** | bearDog CredentialStore + FileVault, squirrel handoff (150u) |
| `primal-transport` crate | ecosystem | Extract transport abstractions |

### Operator Actions

| Action | Where | Status |
|--------|-------|--------|
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

## 7. RECENT MILESTONES

| Milestone | Wave |
|-----------|------|
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

*Wave 150u: Cascade convergence — 15 repos pulled with incoming evolution. nestGate vendor
elimination DONE (vendor/ removed). bearDog CredentialStore shipped (squirrel handoff).
songBird Tower Atomic parity benchmark specified. toadStool S337-S339 deep debt (hot-path
Cow, structural splits, Rust 1.96 clippy 251 files). lithoSpore Validation Data Stream v1.0.
footPrint Lansing Scuffle GeoJSON + data layer primal abstraction. loamSpine doc trim.
esotericWebb IPC refactor. Standards reorganized (150t). 43/43 repos converged at parity.
Next: Tower parity benchmark execution, sporePrint primal pipeline, pseudoSpore promotions,
southGate enrollment, esotericWebb pseudoSpore explorer.*
