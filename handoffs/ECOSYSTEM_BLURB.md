# ecoPrimals Ecosystem Blurb — Wave 139d

**Date**: Jul 15, 2026 08:35 EDT | **Wave**: 139d | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. PIPELINE CONNECTED. DEPOT OPERATIONAL.**

Divergence trace completed: all 39 repos converged. sporeGate membrane
binary rebuilt to 13543be (was 70+ commits behind at Wave ~132). SSH from
sporeGate to golgi configured. Depot symlinks aligned on both nodes.
`depot_sync` now functional end-to-end. `resolve_depot` fallthrough fix
shipped. Pipeline topology issues documented for parallel team work.

---

## This Cascade (139c → 139d)

| Fix | What |
|-----|------|
| **MEMBRANE-BINARY-STALE** | sporeGate membrane rebuilt: f7ecefe (Wave ~132) → 13543be (Wave 139d). Gains: tree hashes, CASCADE-HANG, SIGN-VERIFY, error taxonomy, harvest --local, depot_sync, sources.toml |
| **DEPOT-PATH-DIVERGENCE** | golgi had TWO depot dirs: `/opt/ecoPrimals/depot/` (real, Caddy serves) and `/opt/ecoPrimals/plasmidBin/` (stale). Symlinked both nodes: `plasmidBin → depot`, `infra/plasmidBin → depot` |
| **SSH-SPOREGATE-TO-GOLGI** | Added `golgi` and `golgi-ext` SSH host entries on sporeGate. `depot_sync` now connects |
| **RESOLVE-DEPOT-FALLTHROUGH** | `depot.rs resolve_depot()` hardcoded `infra/plasmidBin` only. Now falls through to flat `plasmidBin/` matching `local.rs` priority (13543be) |
| **NUCLEUS-SYNC** | projectNUCLEUS absorbed Wave 139a identity sync commit |
| **WATERINGHOLE-GOLGI-HEADS** | Merged golgiBody auto-publish from forgejo, rebased, pushed all remotes |

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

**Pipeline Status**:

| Component | Status |
|-----------|--------|
| `membrane` on sporeGate | **CURRENT** (13543be) — was 70+ commits behind |
| SSH sporeGate → golgi | **CONNECTED** |
| `plasmid.depot_sync` | **FUNCTIONAL** — 4 synced, 9 missing (thin relay has few installed) |
| Depot symlinks (both nodes) | **ALIGNED** — `plasmidBin → depot`, `infra/plasmidBin → depot` |
| `harvest --local` | SHIPPED in code, needs rebuild + test on sporeGate |
| rsync push (harvest → VPS) | WORKING (manual rsync, needs `depot_sync` evolution) |

---

## Parallel Team Assignments

### sporeGate Hardware Team
**Focus**: Complete remaining harvests and depot interactions

| Task | Priority | Notes |
|------|----------|-------|
| Windows full harvest (14/14 .exe) | P1 | Only songbird.exe exists. Need `--target x86_64-pc-windows-gnu` for all primals |
| Android re-harvest (NDK) | P2 | 3 stale bins from Jul 13. Needs NDK toolchain setup |
| Test `harvest --local` end-to-end | P1 | Code shipped (7018df6), membrane rebuilt (13543be). Test: `membrane plasmid.harvest --local --all` |
| Auto-harvest timer | P3 | Periodic rebuild cron/systemd on sporeGate |
| SoloKey ceremony completion | P2 | GetAssertion → verify → tap-sequence → Loam cert |

### cellMembrane Code Team
**Focus**: Close remaining depot_sync topology gaps

| Task | Priority | Notes |
|------|----------|-------|
| `depot_sync` topology awareness | P1 | Currently SSHes to golgi and syncs install→depot. Builder workflow needs LOCAL depot → REMOTE depot (rsync). Add `--push` mode or detect builder role |
| `depot_sync` checksums propagation | P2 | checksums.toml copy fails when src=dst (symlink). Need to detect and skip self-copy |
| `resolve_depot` unification | P3 | Three resolution paths (depot.rs, local.rs, dispatch). Unify to single canonical resolver |
| `depot_sync vps_root` SSH config | P2 | Add golgi SSH host to ShadowConfig or `membrane.toml` so it auto-configures (currently manual ~/.ssh/config) |
| PLASMIDBIN→GENOMEBIN rename | P3 | Rename constants and paths from `plasmidBin` to `genomeBin` (depot evolution) |

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

### 3. Live Compositions + Drawbridge
**Owner**: sporePrint + protoKarya + petalTongue teams

| Step | Status |
|------|--------|
| footPrint client (primals.eco/footprint/) | **LIVE** |
| NCBI/PubChem drawbridge bonds | **SHIPPED** |
| footPrint server on sporeGate | TODO |
| RustScript absorption | TODO |
| tideGlass Phase 0 | TODO |

### 4. Infrastructure Hygiene
**Owner**: overwatch

| Step | Status |
|------|--------|
| Re-publish freshness (Wave 137 → 139d) | TODO |
| ironGate/sporeGate head re-publish | TODO |
| DNSSEC on primals.eco | TODO |
| primal.eco inner membrane separation | TODO |

---

## Three Tracks → Glacial Goals

### Track 1: Hardware Trust → NUCLEUS USB Kit
```
DONE    First credential + FIDO2 refactor + CTAP2 hardening
DONE    Depot: 36 fresh binaries, 4 architectures, signed
DONE    cellMembrane pipeline shipped + membrane rebuilt on sporeGate
NOW     northGate mesh enrollment (songbird.exe ready)
NOW     SoloKey authenticate + tap-sequence + Loam cert
NOW     Windows full harvest (14/14 .exe)
GOAL    User is their own key. USB kit deploys NUCLEUS identity.
```

### Track 2: K-Derm → Sovereign Membrane Parity
```
DONE    CASCADE-HANG + SPOREGATE-PUSH + DEPOT-COVERAGE
DONE    Identity web (ORCID, Keyoxide, JSON-LD, DISCOVERED_BY)
DONE    harvest --local + depot_sync SSH + resolve_depot fallthrough
DONE    Depot symlinks aligned (both nodes), SSH connected
NOW     depot_sync topology: builder push mode (LOCAL→REMOTE)
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
eastGate     — PRIMARY. Zero divergences. Cascade authority. 39/39 repos converged.
northGate    — Windows mesh target. songbird.exe in depot. RTX 5090. ~1TB AlphaFold.
sporeGate    — NUCLEUS. Build authority. membrane CURRENT (13543be). SSH to golgi CONNECTED.
                SoloKey plugged. rustc 1.96.1, 6 targets. depot_sync functional.
golgiBody    — Outer membrane. 3 live surfaces (all 200). Depot serving. Symlinks aligned.
westGate     — OFFLINE. ZFS cold storage. Pending power-on.
ironGate     — ABG/NF compute. JupyterHub. Head stale (Jul 4).
flockGate    — WAN covalent. 16 bonds. 143 scenarios green.
grapheneGate — StrongBox target. Android ecobins stale (NDK pending).
```

---

*Wave 139d: Pipeline connected. sporeGate membrane rebuilt (70+ commits absorbed).
SSH sporeGate↔golgi live. Depot symlinks aligned. resolve_depot fallthrough fix shipped.
depot_sync functional. Two parallel tracks: sporeGate hardware team (Windows harvest,
SoloKey, harvest --local test) + cellMembrane code team (depot_sync topology, checksums
propagation, genomeBin rename).*
