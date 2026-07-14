# ecoPrimals Ecosystem Blurb — Wave 139a

**Date**: Jul 14, 2026 14:30 EDT | **Wave**: 139a | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN.** All Wave 138 items resolved. Zero remaining debt.
Cascade pipeline converged (cyclic graph → DAG). Opening new wave scope.

---

## Wave 138 Summary (fossilized)

All items resolved: HIDRAW-REPORT-ID, FORGEJO-PERMS-RECUR, BIOMEOS-TEMPLATE,
FIDO2-MONOLITH (8 modules, 13,883 tests), AD-HOC-CASCADE (membrane pipeline),
FRESHNESS-CYCLE (tree hashes → DAG), NAPI-LIFECYCLE, SOCKET-DIR-UNIFY, SOCKET-UMASK.

First FIDO2 credential minted on primals.eco. Tap-sequence entropy ceremony built.
38/38 repos at parity. Cascade runs via `membrane temporal.cascade`.

---

## New Wave Scope — 139a

### 1. northGate Mesh Enrollment
**Owner**: overwatch (eastGate) + songBird team
**Target**: northGate (Windows, house1 MikroTik, 9950X3D / RTX 5090)

northGate is the primary remote access hub for all gates. Mesh enrollment via
songBird Windows target. This proves cross-platform mesh (Linux ↔ Windows)
and brings the 5090 into the compute fabric.

| Step | What | Status |
|------|------|--------|
| songBird Windows build | Cross-compile or native build | TODO |
| Mesh peer discovery | northGate ↔ eastGate on CRS310 backbone | TODO |
| Capability registration | GPU compute, remote access relay | TODO |

### 2. AlphaFold Data Migration + Provenance
**Owner**: overwatch + nestGate team
**Target**: northGate → westGate (when online)

~1 TB AlphaFold data currently on northGate needs:
- Move to westGate ZFS cold storage (76 TB capacity)
- Reverse provenance trace via loamSpine (data lineage)
- Content-address registration in nestGate blob store
- drawbridge capability registration for ABG/NF access

| Step | What | Status |
|------|------|--------|
| westGate online | Power on, ZFS health check | BLOCKED (hardware) |
| Data inventory | Catalog AlphaFold datasets on northGate | TODO |
| Transfer plan | rsync/zfs send over 10G backbone | TODO |
| Provenance trace | loamSpine reverse lineage from download source | TODO |
| nestGate registration | Content-addressed blob store | TODO |

### 3. SoloKey Ceremony Completion
**Owner**: bearDog team
**Target**: sporeGate (SoloKey plugged) + eastGate

| Step | What | Status |
|------|------|--------|
| Authenticate | GetAssertion → verify credential | TODO (needs replug) |
| Tap-sequence test | Live 3-5 tap entropy harvest | TODO |
| Loam cert seeding | Tier 1+2+3 → BLAKE3 → Loam cert seed | TODO |
| Pixel StrongBox | ADB ceremony on grapheneGate | TODO |

### 4. Live Compositions + RustScript Architecture
**Owner**: sporePrint team + protoKarya + petalTongue team

footPrint is **LIVE** at https://primals.eco/footprint/ — the first NUCLEUS
composition target. It intakes inner and outer membrane data via 10 drawbridge
weak bond GIS proxies. This is the experiment substrate for routine outer
membrane connections (NCBI, PubChem, etc. via drawbridge registration).

**Architecture**: Pure Rust for everything backend and agentic (primals).
UI aims for Rust via petalTongue. RustScript (footPrint's TypeScript library
encoding Rust's safety constraints) is a portable frontend bridge — petalTongue
may leverage it for rendering in time. RustScript itself is absorbable from
footPrint for any composition needing frontend safety primitives.

```
Backend + Agentic:  Pure Rust (primals, nestGate, bearDog, biomeOS)
UI/Rendering:       Rust via petalTongue (aim) / RustScript (bridge)
Live compositions:  RustScript + drawbridge weak bonds (footPrint, tideGlass)
Data pipelines:     Pure Rust (loamSpine provenance, nestGate blob store)
```

footPrint server-side (Express: project save/load, agent bridge) targets
sporeGate NUCLEUS. Long-term: petalTongue/nestGate replaces Express with
pure Rust. Client static is on golgi (thin relay, Caddy SPA + GIS proxy).

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
eastGate     — PRIMARY. Zero debt. Cascade pipeline converged.
northGate    — Remote access hub. Windows mesh target. ~1TB AlphaFold data.
sporeGate    — NUCLEUS. SoloKey plugged. Depot authority. Build authority.
golgiBody    — Outer membrane. Wildcard DNS. Thin relay.
westGate     — OFFLINE. 76TB ZFS cold storage. Pending power-on.
ironGate     — ABG/NF compute. JupyterHub. 13/13 active.
flockGate    — bearDog FIDO2 + primalSpring scenarios.
grapheneGate — StrongBox target. Android compile unblocked.
```

---

*Wave 139a: zero debt. Opening scope: northGate mesh enrollment (Windows cross-platform),
AlphaFold data migration + provenance, SoloKey ceremony completion, live composition
advancement. Cascade pipeline converged — tree hashes break the cycle.*
