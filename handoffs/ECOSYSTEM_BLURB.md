# ecoPrimals Ecosystem Blurb — Wave 139c

**Date**: Jul 15, 2026 07:15 EDT | **Wave**: 139c | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. DEPOT FULLY HARVESTED.**
sporeGate team completed full multi-arch harvest: 36 fresh binaries across 4
architectures. Signed, verified, live on VPS depot. songBird NCBI/PubChem
drawbridge bonds shipped. cellMembrane error taxonomy refactored.
All code divergences resolved. Zero P1/P2/P3.

---

## Incoming Evolution (this cascade)

| Repo | Commit | What |
|------|--------|------|
| **bearDog** | 5db229b | BTreeMap batch 2 + orphan/deprecated cleanup (Wave 139b) |
| **songBird** | 64393c2 | **NCBI/PubChem drawbridge bonds** + northGate capability registration |
| **nestGate** | 2a6b215 | Deep debt sweep round 3 — `String::from`, enum `#[default]`, clone (2 commits) |
| **cellMembrane** | 060b645 | Error taxonomy + `reconcile_and_push` refactor (Wave 139b) |
| **primalSpring** | 2e8a629 | +1 northgate-mesh-enrollment scenario + scenario count fix (158 total) |
| **wateringHole** | 488f7c0 | **DEPOT HARVEST AAR** — 36 fresh binaries, Windows target added |

### Key Items

- **DEPOT-COVERAGE RESOLVED**: sporeGate completed full multi-architecture harvest:
  - x86_64-unknown-linux-musl: **16/16** (all 14 primals + membrane + nucleus_launcher)
  - aarch64-unknown-linux-musl: **16/16**
  - x86_64-pc-windows-gnu: **1** (songbird.exe — first Windows ecobin)
  - aarch64-linux-android: **3** (stale Jul 13 — re-harvest when NDK ready)
  - Total: **36 fresh** + 3 stale Android = **39 depot binaries**
  - BLAKE3 checksums + Ed25519 signatures generated
  - rsync pushed to golgi VPS, live at `membrane.primals.eco/depot/`
- **NCBI/PubChem drawbridge bonds**: songBird now has science API bond definitions + Caddy proxy config for external data ingestion
- **northGate mesh scenario**: primalSpring now has Windows mesh readiness validation (158 scenarios total)
- **cellMembrane error taxonomy**: Refactored error types + push reconciliation logic

---

## Active Divergences

**ZERO.** All previous divergences resolved:

| ID | Resolution |
|----|-----------|
| ~~DEPOT-COVERAGE~~ | **RESOLVED** — 36 fresh binaries, 4 architectures, signed + verified |
| ~~CASCADE-HANG~~ | **RESOLVED** — cellMembrane skip non-bare repos (580a7e8) |
| ~~SPOREGATE-PUSH~~ | **RESOLVED** — non-bare detection (580a7e8) |
| ~~SPOREPRINT-REBUILD~~ | **RESOLVED** — 304 pages deployed |

---

## Depot State — Universal Deployment System

sporeGate is the builder node (rustc 1.96.1). It builds, signs, and pushes
ecobins to the VPS depot. All gates fetch from `membrane.primals.eco/depot/`.

```
Architecture              Binaries  Status
x86_64-unknown-linux-musl    16     FRESH (Jul 15) — all Linux gates
aarch64-unknown-linux-musl   16     FRESH (Jul 15) — Pixel, ARM gates
x86_64-pc-windows-gnu         1     NEW — songbird.exe for northGate
aarch64-linux-android          3     STALE (Jul 13) — needs NDK re-harvest
```

**Remaining depot evolution**:

| Step | What | Status |
|------|------|--------|
| Windows full harvest | All 14 primals as .exe for northGate | TODO — only songbird.exe so far |
| Android re-harvest | 14/14 with NDK toolchain | TODO — needs NDK setup |
| `membrane plasmid.harvest --local` | Skip clone, build from local checkout (~10x faster) | cellMembrane TODO |
| `membrane plasmid.depot_sync` | SSH config for golgi VPS (currently uses rsync workaround) | cellMembrane TODO |
| `sources.toml` auto-provision | Self-healing depot prerequisites | cellMembrane TODO |
| Auto-harvest timer | Periodic rebuild on sporeGate | TODO |

---

## Wave 139c Remaining Scope

### 1. northGate Mesh Enrollment — **UNBLOCKED**
**Owner**: overwatch + songBird team

songbird.exe is in the VPS depot. NCBI/PubChem bonds shipped. Mesh readiness
scenario added to primalSpring.

| Step | What | Status |
|------|------|--------|
| songbird.exe available | In VPS depot (x86_64-pc-windows-gnu) | **DONE** |
| Deploy to northGate | Download + run songbird.exe | TODO |
| Mesh peer discovery | northGate ↔ eastGate on CRS310 backbone | TODO |
| Capability registration | GPU compute (RTX 5090), remote access relay | TODO |

### 2. AlphaFold Data Migration + Provenance
**Owner**: overwatch + nestGate team

| Step | What | Status |
|------|------|--------|
| westGate online | Power on, ZFS health check | BLOCKED (hardware) |
| Data inventory | Catalog AlphaFold datasets on northGate | TODO |

### 3. SoloKey Ceremony Completion
**Owner**: bearDog team

| Step | What | Status |
|------|------|--------|
| Authenticate | GetAssertion → verify credential | TODO |
| Tap-sequence test | Live entropy harvest | TODO |
| Loam cert seeding | Tier 1+2+3 → BLAKE3 → Loam cert seed | TODO |

### 4. Live Compositions + Drawbridge
**Owner**: sporePrint + protoKarya + petalTongue teams

| Step | What | Status |
|------|------|--------|
| footPrint client | primals.eco/footprint/ | **LIVE** |
| NCBI/PubChem bonds | songBird bond defs + Caddy proxy config | **SHIPPED** |
| footPrint server | Express on sporeGate | TODO |
| RustScript absorption | Extract lib for petalTongue | TODO |
| tideGlass Phase 0 | Sovereign GPS platform | TODO |

### 5. cellMembrane Pipeline Improvements (from depot AAR)
**Owner**: cellMembrane team

| Step | What | Status |
|------|------|--------|
| `--local` harvest mode | Build from local checkout, skip clone | TODO |
| `depot_sync` SSH config | Add golgi host entry to ShadowConfig | TODO |
| `sources.toml` auto-provision | Self-healing depot prereqs | TODO |
| Error taxonomy | Refactored (060b645) | **DONE** |
| Push reconciliation | Non-bare skip + timeout (580a7e8 + 060b645) | **DONE** |

---

## Three Tracks → Glacial Goals

### Track 1: Hardware Trust → NUCLEUS USB Kit
```
DONE    First credential + FIDO2 refactor + CTAP2 hardening
DONE    Depot: 36 fresh binaries, 4 architectures, signed
NOW     northGate mesh enrollment (songbird.exe in depot)
NOW     SoloKey authenticate + tap-sequence + Loam cert
NEXT    Pixel StrongBox ceremony
GOAL    User is their own key. USB kit deploys NUCLEUS identity.
```

### Track 2: K-Derm → Sovereign Membrane Parity
```
DONE    CASCADE-HANG + SPOREGATE-PUSH + DEPOT-COVERAGE
DONE    Identity web (ORCID, Keyoxide, JSON-LD, DISCOVERED_BY)
DONE    cellMembrane error taxonomy + push reconciliation
NOW     Windows full harvest (14/14 .exe for northGate)
NOW     cellMembrane --local harvest + depot_sync SSH
NOW     primal.eco separation (inner membrane)
GOAL    Universal depot — same system for every gate and architecture
```

### Track 3: Live Compositions → External Science Production
```
DONE    footPrint LIVE + sporePrint (304 pages)
DONE    NCBI/PubChem drawbridge bonds (songBird 64393c2)
DONE    DISCOVERED_BY standard (26 repos, 4 orgs)
NOW     footPrint server on sporeGate
NOW     Live drawbridge ingestion (NCBI, PubChem via Caddy proxy)
NEXT    tideGlass Phase 0, ABG accounts
GOAL    Pure Rust backend + sovereign compositions
```

---

## Gate Status
```
eastGate     — PRIMARY. Zero debt. Zero divergences. Cascade authority.
northGate    — Windows mesh target. songbird.exe in depot. RTX 5090. ~1TB AlphaFold.
sporeGate    — NUCLEUS. SoloKey. Build authority. 36 fresh bins harvested.
                rustc 1.96.1, 6 targets (x86_64-musl/gnu, aarch64-musl/gnu/android, windows-gnu).
golgiBody    — Outer membrane. 3 live surfaces (all 200). Depot serving at membrane.primals.eco.
westGate     — OFFLINE. ZFS cold storage. Pending power-on.
ironGate     — ABG/NF compute. JupyterHub.
flockGate    — WAN covalent. 16 bonds. 143 scenarios green.
grapheneGate — StrongBox target. Android ecobins stale (NDK pending).
```

---

*Wave 139c: ZERO divergences. Depot fully harvested (36 fresh binaries, 4 architectures,
Ed25519 signed, live on VPS). NCBI/PubChem drawbridge bonds shipped. cellMembrane
error taxonomy refactored. Remaining: Windows full harvest, cellMembrane --local mode,
northGate mesh deployment, SoloKey ceremony, live compositions.*
