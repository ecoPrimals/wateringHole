# ecoPrimals Ecosystem Blurb — Wave 139c

**Date**: Jul 15, 2026 07:42 EDT | **Wave**: 139c | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. ZERO DIVERGENCES. DEPOT OPERATIONAL.**

All code converged. 3 live surfaces (all 200). 36 fresh ecobins across 4
architectures, Ed25519 signed, live at `membrane.primals.eco/depot/`.
wateringHole cleaned and fossilized (Wave 138 handoffs, stale impulses,
old genomeBin/systemd/snapshots/compute-sharing archived).

---

## Orthogonal Review Findings (Jul 15)

| Dimension | Status | Notes |
|-----------|--------|-------|
| 1. Temporal | **CLEAN** | wave.toml 139c, 0 active impulses. ironGate/sporeGate heads stale (Jul 4-5) — need cascade from those gates |
| 2. Ecological | **GREEN** | 39 repos converged, 0 ahead/behind on all locals |
| 3. Hardware | **OK** | 7 online, 2 offline (strandGate, westGate). SoloKey on sporeGate |
| 4. Sovereignty | **STRONG** | K-Derm intact, Forgejo 200, all security headers deployed. DNSSEC still TODO |
| 5. Depot | **OPERATIONAL** | 16+16+1 bins live. Windows/Android coverage incomplete |
| 6. Website | **LIVE** | primals.eco 200, /footprint/ 200, live.primals.eco 200. Full header suite |
| 7. Glacial | **ALL 8 CLEAR** | Updated to 139c |
| 8. Compositions | **PARTIAL** | footPrint client LIVE, drawbridge bonds SHIPPED. Server + tideGlass pending |
| 9. Documentation | **CLEAN** | Fossilized 9 handoffs, 7 impulses, 4 stale dirs. 49 root standards remain |
| 10. Cascade | **HEALTHY** | CASCADE-HANG fixed, tree hashes, Forgejo live |

### Issues Identified

- **HEAD-STALE**: ironGate (Jul 4) and sporeGate (Jul 5) haven't published head files in 10+ days. Next cascade from those gates should re-publish.
- **FRESHNESS-WAVE**: `freshness.toml` shows Wave 137. Needs re-publish via `membrane temporal.cascade --publish-freshness`.
- **DNSSEC**: ODN-02 (DNSSEC on `primals.eco`) remains TODO.

---

## Depot State — Universal Deployment System

sporeGate builds, signs, and pushes ecobins to VPS depot.
All gates fetch from `membrane.primals.eco/depot/`.

```
Architecture              Binaries  Status
x86_64-unknown-linux-musl    16     FRESH (Jul 15) — all Linux gates
aarch64-unknown-linux-musl   16     FRESH (Jul 15) — Pixel, ARM gates
x86_64-pc-windows-gnu         1     songbird.exe for northGate
aarch64-linux-android          3     STALE (Jul 13) — needs NDK re-harvest
```

**Remaining depot evolution**:

| Step | What | Status |
|------|------|--------|
| Windows full harvest | All 14 primals as .exe for northGate | TODO |
| Android re-harvest | 14/14 with NDK toolchain | TODO — needs NDK setup |
| `harvest --local` | Build from local checkout, skip clone | **SHIPPED** (7018df6) |
| `depot_sync vps_root` | SSH config for golgi VPS | **SHIPPED** (7018df6) |
| `sources.toml` auto-provision | Self-healing depot prerequisites | **SHIPPED** (7018df6) |
| Auto-harvest timer | Periodic rebuild on sporeGate | TODO |

---

## Remaining Scope

### 1. northGate Mesh Enrollment
**Owner**: overwatch + songBird team

| Step | Status |
|------|--------|
| songbird.exe in VPS depot | **DONE** |
| Deploy songbird.exe to northGate | TODO |
| Mesh peer discovery (northGate ↔ eastGate via CRS310) | TODO |
| Capability registration (RTX 5090, remote access relay) | TODO |

### 2. AlphaFold Data Migration + Provenance
**Owner**: overwatch + nestGate team

| Step | Status |
|------|--------|
| westGate online (power on, ZFS check) | BLOCKED (hardware) |
| Catalog AlphaFold datasets on northGate | TODO |
| Provenance trace back to source | TODO — after westGate |

### 3. SoloKey Ceremony Completion
**Owner**: bearDog team

| Step | Status |
|------|--------|
| GetAssertion → verify credential | TODO |
| Tap-sequence live entropy harvest | TODO |
| Loam cert seeding (Tier 1+2+3 → BLAKE3) | TODO |

### 4. Live Compositions + Drawbridge
**Owner**: sporePrint + protoKarya + petalTongue teams

| Step | Status |
|------|--------|
| footPrint client (primals.eco/footprint/) | **LIVE** |
| NCBI/PubChem drawbridge bonds | **SHIPPED** |
| footPrint server (Express on sporeGate) | TODO |
| RustScript absorption (extract lib for petalTongue) | TODO |
| tideGlass Phase 0 (sovereign GPS) | TODO |

### 5. Infrastructure Hygiene
**Owner**: overwatch

| Step | Status |
|------|--------|
| Re-publish freshness (Wave 137 → 139c) | TODO |
| ironGate head re-publish | TODO — needs cascade from ironGate |
| sporeGate head re-publish | TODO — needs cascade from sporeGate |
| DNSSEC on primals.eco (ODN-02) | TODO |
| primal.eco inner membrane separation | TODO |

---

## Three Tracks → Glacial Goals

### Track 1: Hardware Trust → NUCLEUS USB Kit
```
DONE    First credential + FIDO2 refactor + CTAP2 hardening
DONE    Depot: 36 fresh binaries, 4 architectures, signed
DONE    cellMembrane pipeline (--local, depot_sync, auto-provision)
NOW     northGate mesh enrollment (songbird.exe ready)
NOW     SoloKey authenticate + tap-sequence + Loam cert
NEXT    Pixel StrongBox ceremony
GOAL    User is their own key. USB kit deploys NUCLEUS identity.
```

### Track 2: K-Derm → Sovereign Membrane Parity
```
DONE    CASCADE-HANG + SPOREGATE-PUSH + DEPOT-COVERAGE
DONE    Identity web (ORCID, Keyoxide, JSON-LD, DISCOVERED_BY)
DONE    cellMembrane error taxonomy + push reconciliation
DONE    harvest --local + depot_sync SSH + sources.toml auto-provision
NOW     Windows full harvest (14/14 .exe for northGate)
NOW     DNSSEC + primal.eco separation
NOW     Auto-harvest timer on sporeGate
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
sporeGate    — NUCLEUS. SoloKey. Build authority. rustc 1.96.1, 6 targets.
                Head stale (Jul 5) — needs re-publish.
golgiBody    — Outer membrane. 3 live surfaces (all 200). Depot serving.
westGate     — OFFLINE. ZFS cold storage. Pending power-on.
ironGate     — ABG/NF compute. JupyterHub. Head stale (Jul 4) — needs re-publish.
flockGate    — WAN covalent. 16 bonds. 143 scenarios green.
grapheneGate — StrongBox target. Android ecobins stale (NDK pending).
```

---

*Wave 139c: ZERO divergences. Depot operational (36 fresh binaries, 4 architectures,
Ed25519 signed). Pipeline closed (harvest --local, depot_sync, auto-provision all shipped).
wateringHole cleaned. Remaining: Windows/Android harvest expansion, northGate mesh
deployment, SoloKey ceremony, footPrint server, DNSSEC, head re-publishes.*
