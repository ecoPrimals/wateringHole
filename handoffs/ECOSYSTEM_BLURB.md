# ecoPrimals Ecosystem Blurb — Wave 139a

**Date**: Jul 14, 2026 18:30 EDT | **Wave**: 139a | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN.** All Wave 138 items resolved. Zero remaining debt.
Cascade pipeline converged (cyclic graph → DAG). 16/16 repos at parity across all remotes.
3 live public surfaces. Opening new wave scope.

---

## Full Dimensions Review — Wave 139a

### 1. Temporal
- `wave.toml` bumped to 139a. 6 gate heads published (eastGate, sporeGate, golgi, golgiBody, ironGate, flockGate).
- 7 active impulses — all wateringHole/plasmidBin divergence from today's cascade. Root cause: sporeGate-direct is a non-bare repo (push to checked-out branch rejected). Content is synced via origin (GitHub). **Not a data divergence — topology issue.**
- `freshness.toml` uses tree hashes (DAG fix from Wave 138). No cyclic divergence.

### 2. Ecological (Primal Health)
- 16/16 repos fully converged (zero ahead/behind on all remotes).
- Zero P1 blockers. Transport 11/11 adopted. Neural API 12/12 shipped.
- Test counts stable. FIDO2 refactor added 13,883 new tests.
- Key heads: bearDog f3ca8a0, biomeOS 6d88426, songBird 624b092, cellMembrane d11a407.

### 3. Hardware / Topology
- **sporeGate**: ONLINE. Build authority + NUCLEUS + SoloKey plugged. LAN 192.168.4.1/3.
- **eastGate**: ONLINE. Primary orchestrator. Zero debt.
- **golgi**: ONLINE. VPS thin relay. Wildcard DNS. 3 live surfaces (200/200/200).
- **ironGate**: ONLINE. ABG/NF compute. JupyterHub. 13/13.
- **flockGate**: ONLINE. WAN covalent. sporePrint.
- **grapheneGate**: ONLINE. StrongBox target. Android NUCLEUS.
- **northGate**: NEW. Windows. Remote access hub. ~1TB AlphaFold. Mesh target.
- **westGate**: OFFLINE. 76TB ZFS cold storage. Pending power-on.
- SoloKeys: 1 on sporeGate, 1 on eastGate. First FIDO2 credential minted.
- Network: CRS310 backbone (house1), Omada (house2), WireGuard overlay.

### 4. Sovereignty / Membranes
- K-Derm three-layer intact: Cloudflare (outer) → Caddy/bearDog (sovereign) → primals (inner).
- S1-S4 ALL GRADUATED. DNSSEC enabled on primal.eco + nestgate.io.
- Wildcard `*.primals.eco` deployed in Cloudflare.
- Domain separation: primals.eco (ecosystem), primal.eco (personal sovereign), nestgate.io (federated data gateway).
- Zero commercial services in inner membrane data path.

### 5. Depot / Build Pipeline
- **DIVERGENCE FOUND**: sporeGate genomeBin depot has only 6/14 primals (songbird, beardog, biomeos, nestgate, squirrel, toadstool). Missing: barraCuda, coralReef, loamSpine, petalTongue, rhizoCrypt, skunkBat, sourDough, sweetGrass.
- **DIVERGENCE FOUND**: genomeBin binaries are dynamically linked (gnu), not musl-static as post-primordial standard requires. This is the older depot layout — needs reconciliation with plasmidBin pipeline.
- `checksums.toml` / `signatures.toml` not found on sporeGate genomeBin.
- eastGate local has no plasmidBin directory (fetches from depot authority).
- SIGN-VERIFY-ON-FETCH operational in cellMembrane.

### 6. Website / Public Surface / Security
- `primals.eco` → 200 (sporePrint static site via Caddy)
- `primals.eco/footprint/` → 200 (GIS composition, 10 weak bond proxies)
- `live.primals.eco` → 200 (petalTongue TOPO-VIS dashboard)
- Security headers deployed. fail2ban active. Rate limiting configured.
- TLS auto-renewing via ACME/LE.
- No new CRITICAL exposures.

### 7. Glacial Shift
- **ALL 8 CRITERIA CLEAR** for stadial entry (unchanged since Wave 111 for 1-7, Wave 136 for 8).
- Next glacial goal: Universal Substrate Evolution (multi-arch depot parity).
- SHOW_HN readiness rubric established (28 criteria, 4 categories).

### 8. Compositions / RustScript
- footPrint LIVE at primals.eco/footprint/. GIS weak bonds functional.
- RustScript architecture documented in gen5/foundations/RUSTSCRIPT_LAST_MILE.md.
- Composition routing standard published in wateringHole.
- JupyterHub access guide published for ABG collaborators.
- tideGlass Phase 0 planned.

### 9. Documentation / Fossil Record
- wateringHole distilled to ~83 active documents.
- 14 gen5 foundation documents current.
- ORTHOGONAL_DIMENSIONS_REVIEW.md created as reusable reassessment checklist.
- Stale Wave 132-138 artifacts fossilized.

### 10. Cascade Pipeline / Convergence
- `membrane temporal.cascade` ran but hung on sporeGate-direct wateringHole push rejection (non-bare repo).
- All repos converged via origin (GitHub) — sporeGate pulls from origin.
- Forgejo mirrors operational (38 repos).
- Tree hash convergence working — no cyclic divergence.
- **Action needed**: cascade should skip or gracefully handle non-bare direct push targets.

---

## Active Divergences

| ID | What | Severity | Owner |
|----|------|----------|-------|
| DEPOT-LAYOUT | genomeBin on sporeGate has 6/14 primals, dynamically linked | P2 | sporeGate + cellMembrane |
| SPOREGATE-PUSH | Non-bare repo rejects push to checked-out branch | P3 | cellMembrane |
| CASCADE-HANG | membrane cascade hangs after push rejection | P2 | cellMembrane |

---

## Wave 139a Scope

### 1. northGate Mesh Enrollment
**Owner**: overwatch (eastGate) + songBird team

| Step | What | Status |
|------|------|--------|
| songBird Windows build | Cross-compile or native build | TODO |
| Mesh peer discovery | northGate ↔ eastGate on CRS310 backbone | TODO |
| Capability registration | GPU compute, remote access relay | TODO |

### 2. AlphaFold Data Migration + Provenance
**Owner**: overwatch + nestGate team

| Step | What | Status |
|------|------|--------|
| westGate online | Power on, ZFS health check | BLOCKED (hardware) |
| Data inventory | Catalog AlphaFold datasets on northGate | TODO |
| Transfer plan | rsync/zfs send over 10G backbone | TODO |
| Provenance trace | loamSpine reverse lineage from download source | TODO |
| nestGate registration | Content-addressed blob store | TODO |

### 3. SoloKey Ceremony Completion
**Owner**: bearDog team

| Step | What | Status |
|------|------|--------|
| Authenticate | GetAssertion → verify credential | TODO |
| Tap-sequence test | Live 3-5 tap entropy harvest | TODO |
| Loam cert seeding | Tier 1+2+3 → BLAKE3 → Loam cert seed | TODO |
| Pixel StrongBox | ADB ceremony on grapheneGate | TODO |

### 4. Live Compositions + RustScript
**Owner**: sporePrint + protoKarya + petalTongue teams

| Step | What | Status |
|------|------|--------|
| footPrint client live | GIS tool at primals.eco/footprint/ | **LIVE** |
| GIS proxy routes | 10 weak bond hosts via Caddy drawbridge | **LIVE** |
| footPrint server | Express on sporeGate (project save, agent bridge) | TODO |
| NCBI/PubChem bonds | Drawbridge registrations for science APIs | TODO |
| RustScript absorption | Extract lib for petalTongue/other compositions | TODO |
| ABG user accounts | JupyterHub access for collaborators | TODO |
| tideGlass Phase 0 | Sovereign GPS platform clone | TODO |
| primal.eco separation | Inner membrane personal substrate | TODO |

### 5. Depot Reconciliation (from review)
**Owner**: sporeGate + cellMembrane teams

| Step | What | Status |
|------|------|--------|
| Full 14/14 harvest | Build all primals musl-static on sporeGate | TODO |
| Depot layout migration | genomeBin → plasmidBin standard layout | TODO |
| Checksums + signatures | Generate checksums.toml + signatures.toml | TODO |
| Cascade push fix | Handle non-bare repos gracefully | TODO |

---

## Three Tracks → Glacial Goals

### Track 1: Hardware Trust → NUCLEUS USB Kit

```
DONE    First credential minted + tap-sequence ceremony
DONE    FIDO2 IPC refactor (8 modules)
NOW     Authenticate + live tap test → Loam cert seeding
NOW     northGate mesh enrollment (Windows cross-platform)
NEXT    Pixel StrongBox ceremony
NEXT    AlphaFold data provenance
GOAL    User is their own key. USB kit deploys NUCLEUS identity.
```

### Track 2: K-Derm Extrication → Sovereign Membrane Parity

```
DONE    Wildcard DNS, FORGEJO-PERMS, BIOMEOS-TEMPLATE
DONE    NAPI-LIFECYCLE + SOCKET-DIR-UNIFY
DONE    Cyclic graph → DAG (freshness tree hashes)
NOW     Depot reconciliation (genomeBin → plasmidBin standard)
NOW     primal.eco separation (inner membrane)
GOAL    Full sovereign membrane parity
```

### Track 3: Live Compositions → External Science Production

```
DONE    footPrint LIVE at primals.eco/footprint/ (10 GIS weak bonds)
DONE    JupyterHub + composition routing standard
NOW     footPrint server on sporeGate (project persistence, agent bridge)
NOW     NCBI/PubChem drawbridge bonds (routine outer membrane data)
NOW     RustScript absorption for petalTongue UI safety primitives
NEXT    ABG user accounts, tideGlass Phase 0
NEXT    AlphaFold data → westGate → nestGate blob store
GOAL    Pure Rust backend + RustScript UI bridge → sovereign compositions
```

---

## Gate Status

```
eastGate     — PRIMARY. Zero debt. 16/16 repos converged.
northGate    — NEW. Remote access hub. Windows mesh target. ~1TB AlphaFold.
sporeGate    — NUCLEUS. SoloKey plugged. Depot authority. Build authority.
                Depot divergence: genomeBin 6/14, needs full harvest.
golgiBody    — Outer membrane. Wildcard DNS. Thin relay. 3 live surfaces.
westGate     — OFFLINE. 76TB ZFS cold storage. Pending power-on.
ironGate     — ABG/NF compute. JupyterHub. 13/13 active.
flockGate    — WAN covalent. bearDog FIDO2 + primalSpring scenarios.
grapheneGate — StrongBox target. Android compile unblocked.
```

---

*Wave 139a: zero code debt. 3 active divergences (depot layout, cascade push, cascade hang — all P2/P3).
New scope: northGate mesh, AlphaFold provenance, SoloKey ceremony, live compositions, depot reconciliation.
Orthogonal dimensions review checklist added to wateringHole for future reassessment.*
