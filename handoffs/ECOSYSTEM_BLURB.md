# ecoPrimals Ecosystem Blurb — Wave 155m

**Date**: Jul 30, 2026 13:00 EDT | **Wave**: 155m | **From**: eastGate overwatch
**Posture**: **ALL P2 DIVERGENCES CLOSED. biomeOS v4.50 ships socket evaporation fix + binary path retention (BOTH P2s FIXED). sporeGate Sovereign CI cascaded all 5 team shipments — depot rebuilt: 34 binaries (16 musl + 3 gnu + 15 windows), all BLAKE3 verified. membrane.exe depot-deployed (15/15 Windows). cellMembrane deep debt + self-knowledge. sporeGate gate health 10/11 (rootpulse.ledger not implemented). ZERO P0s. ZERO P1s. ZERO blocking P2s. 8 operational P2/P3s from sporeGate AAR.**

---

## NUCLEUS — ACHIEVED

Three gates now running full NUCLEUS. Provenance 7/7 validated on two platforms.

```
westGate NUCLEUS (Jul 30 — PROVENANCE 7/7 COMPLETE):
  Tower:  bearDog ✓  songBird ✓  skunkBat ✓
  Nest:   nestGate ✓  loamSpine ✓  sweetGrass ✓  rhizoCrypt ✓
  Node:   toadStool ✓  barraCuda ✓  coralReef ✓
  Viz:    petalTongue ✓  squirrel ✓
  Orch:   biomeOS ✓ (v4.47 COORDINATED, 654 caps)
  Score:  13/13 | 29 sockets | Provenance 7/7 LIVE
  ZFS:    25.4TB ONLINE, 3,252 CAS objects, 1.56× compression

blueGate NUCLEUS (Jul 30 — Windows, Provenance 7/7 VALIDATED):
  13/13 primals, 131.1 MB (down from 147.5 MB), TCP-only
  bearDog crypto.sign LIVE, Provenance 7/7 E2E on Windows
  DID key: did:key:z6Mkryaa7n6hfpSbGaZwbqPMD6MzXukgdQK3XRKzwFSgce8o

strandGate NUCLEUS (Jul 29 — first gate, manual startup):
  8/9 healthy | 1,742 caps | 674 IPC methods | RTX 3090 sub-ms GPU

sporeGate SOVEREIGN CI LIVE:
  Push to Forgejo → auto build → sandbox validate → depot push → HTTPS serve
  J9+J10+J11 KILLED. Zero human intervention for musl builds.
```

**What NUCLEUS + Provenance proved**: full 7-step provenance chain (CAS → DAG → Merkle →
Spine → Ed25519 signature → Attribution braid) works on live hardware with ZFS backend.
Portable across Linux and Windows. Boot order discipline (Tower → Nest → Node → biomeOS)
is the deployment standard. Sovereign CI automates the pipeline end-to-end.

---

## COMPLETED — All Code Chains CLOSED (Wave 155k)

All blocking code work is done. 50 handoffs fossilized to `fossilRecord/wave155k_all_chains_closed/`.

| Chain | What Shipped | Key Commits |
|-------|-------------|-------------|
| biomeOS lifecycle | NUCLEUS orchestrator v4.47: riboCipher, sockets, persistence, composition.start, bind flags, boot_order | `bd202674`, `076d4743` |
| bearDog crypto | crypto.sign_ed25519 + Windows platform gating | `3739e7078`, `d6b1003bb` |
| Windows depot | 14/14 rebuilt by sporeGate, BLAKE3 verified | Jul 30 08:50 EDT |

---

## NEXT PHASES — Deployment + Expansion

### Phase A: Gate Deployment — MOSTLY COMPLETE

| # | Target | What | Status |
|---|--------|------|--------|
| A1 | **westGate** | biomeOS v4.47 + Compute Trio → NUCLEUS | **DONE** — 13/13, 654 caps, 29 sockets |
| A2 | **Provenance 7/7** | Live E2E validation | **DONE** — westGate (Linux) + blueGate (Windows) |
| A3 | **blueGate** | Fresh depot → NUCLEUS on Windows | **DONE** — 131.1 MB, 14/14 depot, crypto.sign LIVE |
| A4 | **strandGate** | Redeploy with biomeOS v4.47 | NEXT — lowest urgency, already NUCLEUS |

### Phase B: Pipeline Automation — 3/5 KILLED

| Jelly String | What | Status |
|-------------|------|--------|
| ~~J9~~ | Forgejo webhook → auto cascade | **KILLED** — golgi post-receive hook → SSH → sporeGate |
| ~~J10~~ | Drift detection → auto harvest | **KILLED** — `sovereign.ci.trigger` on push |
| ~~J11~~ | Multi-target manifest build | **KILLED** — integrated into sovereign.ci |
| J12 | blueGate sub-builder dispatch | **UNBLOCKED** — membrane.exe FIXED (`4ccbab1`). Needs sporeGate → blueGate IPC wire. |
| J13 | Depot freshness probe | ~20 LOC — `mesh.build_pending` wire needed |

All 3 items from `CELLMEMBRANE_WAVE155k_SOVEREIGN_CI_POLISH.md` SHIPPED → fossilized.

### Divergences — Wave 155m Resolution

| Issue | Fix | Commit | Status |
|-------|-----|--------|--------|
| bearDog dual-socket footgun | Default socket now aliases family-scoped | `a875d463` | **FIXED** |
| bearDog `FAMILY_SEED` required | Precedence: env → file → auto-generate | `a875d463` | **FIXED** |
| `PRIMAL_BIND_MODE` `tcp_only` fallback | petalTongue accepts `tcp` semantics | `551e781` | **FIXED** |
| biomeOS capability wipe cycle | 3-strike prune threshold (v4.49) | `f2d4c4b3` | **FIXED** |
| toadStool tarpc-only | Legacy symlink → JSON-RPC `compute.sock` | `5053e0bc` | **FIXED** |
| petalTongue rejects `--family-id` | `--family-id` propagation added | `551e781` | **FIXED** |
| membrane.exe `UnixStream` P1 | `#[cfg(unix)]` gates + Windows stubs | `4ccbab1` | **FIXED** |
| cellMembrane steamGate user-space | Deploy path readiness for `~/.local/bin/` | `4a7391d` | **FIXED** |
| cellMembrane reqwest dep | Purged → sovereign HTTP/1.1 client (pure-Rust TLS) | `4e77ffd` | **FIXED** |
| biomeOS socket evaporation (health ping format) | v4.50 sporeGate fix + `999044e7` user-space discovery: probes plasmidBin, ~/.local/bin, ~/.cargo/bin, $PATH | `999044e7` | **FIXED** |
| biomeOS binary path retention | Unified binary_search_dirs() SSOT: 5-tier probe (explicit → depot → XDG → cargo → PATH) | `999044e7` | **FIXED** |
| Socket ownership for multi-user IPC | biomeOS socket bind now `0666` | `0e45262f` | **FIXED** |
| checksums.toml partial update on harvest | `finalize_depot()` full disk scan | `0cfcce5` | **FIXED** |
| /run/membrane tmpfiles.d rule | `deploy/systemd/tmpfiles.d/membrane.conf` shipped | `0cfcce5` | **FIXED** |
| rootpulse.ledger degraded probe | Returns ok=true advisory when no session | `0cfcce5` | **FIXED** |
| sandbox false positive for broker primals | `ServerContract` resolution for biomeOS | `0cfcce5` | **FIXED** |
| cellMembrane not in sources.toml | Blocks sovereign CI self-rebuild | — | **P3 OPEN** |
| golgi post-receive hook not auto-firing | biomeOS push didn't trigger CI | — | **P3 OPEN** |

---

## CROSS-PLATFORM EXPANSION — genomeBin Mesh

**Principle**: anything with a chip and a drive is a mesh gate. The genomeBin
standard + Tower Atomic abstraction means one codebase → any platform.

### Depot Targets — Current vs Needed

| Target Triple | Status | Depot | Gates |
|---------------|--------|-------|-------|
| `x86_64-unknown-linux-musl` | **LIVE** | 16 bins | eastGate, sporeGate, westGate, strandGate, ironGate, flockGate |
| `x86_64-unknown-linux-gnu` | **LIVE** | 3 bins (GPU trio) | strandGate (GPU) |
| `x86_64-pc-windows-gnu` | **LIVE** | 14 bins | blueGate, swiftGate, northGate |
| `aarch64-unknown-linux-musl` | **TIER 1** | directory only | grapheneGate (pepti warehouse) |
| `aarch64-linux-android` | **TIER 1** | directory only | grapheneGate (via ADB) |
| `x86_64-unknown-linux-gnu` (SteamOS) | **TIER 2 — NEXT** | depot exists (3 bins) | steamGate (Steam Deck) |
| `aarch64-apple-darwin` | **TIER 2 — GLACIAL** | needs Mac host to build | darwinGate (Mac Mini, acquisition needed) |
| `aarch64-apple-ios` | **TIER 2 — GLACIAL** | needs darwinGate + signing | iosGate (iPhone, walled garden) |

### New Gates

| Gate | Platform | Target | Status | Notes |
|------|----------|--------|--------|-------|
| **steamGate** | SteamOS (Arch Linux) | `x86_64-unknown-linux-gnu` | **NEXT** | Steam Deck. Portable compute. User-space deploy. Depot bins may work as-is. |
| **darwinGate** | macOS (Mac Mini) | `aarch64-apple-darwin` | **GLACIAL** | Needs HW acquisition (~$500 M1). Self-builds darwin genomeBins. Prerequisite for iosGate. |
| **iosGate** | iOS (iPhone) | `aarch64-apple-ios` | **GLACIAL** | Walled garden. Needs darwinGate + Apple Dev Program. Silicon deism obligation. |

**Silicon deism sequence**: steamGate (have HW) → darwinGate (acquire Mac Mini) → iosGate (after darwin lessons)
**Learning path**: Linux↔Windows cross taught us platform abstraction. Darwin is the next frontier — launchd, Mach-O, Keychain, XPC. iOS pushes further into sandboxed/hostile environments.

### Platform Abstraction Status

| Platform Concern | Linux | Windows | SteamOS | macOS | iOS | Android |
|------------------|-------|---------|---------|-------|-----|---------|
| IPC transport | UDS | TCP | UDS | UDS | sandboxed | TCP (ADB) |
| Service manager | systemd | Win Service | systemd (user) | launchd | none (app lifecycle) | init/pepti |
| Binary format | ELF | PE (.exe) | ELF | Mach-O | Mach-O (signed) | ELF (Bionic) |
| Build target | musl/gnu | windows-gnu | gnu | apple-darwin | apple-ios | android |
| Background services | yes | yes | yes | yes | **NO** (killed ~30s) | yes |
| Port listening | yes | yes | yes | yes | **NO** (foreground only) | yes |
| Cross-compile from Linux | N/A | yes (mingw) | **NO** (need Mac) | **NO** (need Mac) | **NO** | yes (NDK) |
| songBird universal-ipc | SHIPPED | SHIPPED | validate | validate | **research** | SHIPPED |
| Depot binaries | 16+3 | 14 | reuse gnu | **NEEDED** (glacial) | **NEEDED** (glacial) | warehouse |
| Silicon deism status | **PROVEN** | **PROVEN** | **NEXT** | **LEARNING** | **LEARNING** | **PROVEN** |

### Blockers for New Targets

### Blockers for New Targets

| Target | Blocker | Owner | Sequencing |
|--------|---------|-------|------------|
| SteamOS | Read-only rootfs — user-space deploy only (`~/.local/bin/`) | cellMembrane | **NOW** — have the hardware |
| SteamOS | Vulkan GPU — Steam runtime, not system packages | toadStool/coralReef | After Tower stable |
| `*-apple-darwin` | Needs Mac host (can't cross-compile from Linux) | darwinGate | **GLACIAL** — acquire Mac Mini |
| `*-apple-ios` | Needs darwinGate + Apple Dev Program ($99/yr) + signing | iosGate | After darwinGate |
| `*-apple-ios` | iOS kills background processes, sandboxes IPC, no port listening | Architecture | Silicon deism learning |
| All new | `--bind` flag standard | biomeOS | **DONE** (`PRIMAL_BIND_FLAGS_STANDARD.md`) |

---

## TEAMS — ACTIVE vs STANDBY

### ACTIVE CODE TEAMS

| Team | Tests | Wave 155m/n Delivery | Next |
|------|-------|---------------------|------|
| **biomeOS** | 8,570 | v4.51+ P2 socket evap **FIXED all paths** (`999044e7`): 5-tier binary discovery (plasmidBin, ~/.local/bin, ~/.cargo/bin, $PATH). 14 deps removed, registry perf. | G18: neuralAPI agent orchestration |
| **cellMembrane** | 1,263 | 4 AAR fixes (checksums, sandbox, rootpulse, tmpfiles), socket unification, dispatch split | Socket discovery for non-plasmidBin deploy paths |
| **squirrel** | 7,138 | Deep debt: 150+ clippy, universal-constants, Cargo.lock purge. 90.1% coverage. 0 unsafe. | G18: biomeOS neuralAPI agent integration |
| **petalTongue** | 6,605 | Modern idiom pass, debris audit | G19: Node Atomic live rendering pipeline |

### STANDBY CODE TEAMS (all P1s shipped)

| Team | Tests | Resume When |
|------|-------|-------------|
| **bearDog** | 14,019 | STANDBY — all P1s shipped |
| **songBird** | 14,835 | STANDBY |
| **toadStool** | 9,193 | G19/G20 rendering + game pipeline |
| **coralReef** | 3,527 | G20 shader pipeline |
| **barraCuda** | 4,957 | G19 tensor computation |
| **sweetGrass** | 1,639 | STANDBY |
| **rhizoCrypt** | 1,900 | STANDBY |
| **loamSpine** | 1,739 | STANDBY |
| **nestGate** | 13,095+ | AlphaFold ingestion |
| **skunkBat** | — | STANDBY |

### GATE STATUS

| Gate | Status | Next |
|------|--------|------|
| **eastGate** | Overwatch. biomeOS + squirrel + petalTongue local. | Platform wiring (G18-G20). |
| **sporeGate** | **11/11 HEALTHY.** Sovereign CI LIVE. biomeOS v4.51 deployed. | J12 sub-builder. Depot rebuilt. |
| **westGate** | **NUCLEUS.** Prov 7/7. v4.50 deployed. Needs `999044e7` redeploy. | Redeploy biomeOS + AlphaFold ingestion. |
| **strandGate** | **NUCLEUS.** v4.50 deployed (source). Needs `999044e7` redeploy. | Redeploy biomeOS. |
| **blueGate** | **NUCLEUS** (15/15 fresh, Prov 7/7). Sub-builder UNBLOCKED. | J12 enrollment under sporeGate. |
| **flockGate** | **DOWN** — rebooted, RustDesk locked out. May be on mesh. | **esotericWebb → ironGate** (LAN). |
| **ironGate** | Online. 14TB+1TB+1TB+2TB. **Takes esotericWebb from flockGate.** | Tower + esotericWebb + HDD enclave. |
| **swiftGate** | HW ready. Windows. | After blueGate sub-builder stable. |
| **southGate** | HW ready. | Enrollment. |
| **grapheneGate** | Tower LIVE (Pixel 8a). | ADB mesh expansion. |

### GATE NEW (cross-platform expansion)

| Gate | Platform | Target | Status |
|------|----------|--------|--------|
| **steamGate** | SteamOS (Steam Deck) | `x86_64-unknown-linux-gnu` | **NEXT** — have HW, gnu bins in depot |
| **darwinGate** | macOS (Mac Mini) | `aarch64-apple-darwin` | **GLACIAL** — needs HW acquisition |
| **iosGate** | iOS (iPhone) | `aarch64-apple-ios` | **GLACIAL** — needs darwinGate + Dev Program |

---

## METRICS

| Metric | Value |
|--------|-------|
| NUCLEUS gates | **3** (westGate + blueGate + strandGate) + sporeGate (CI) |
| Provenance 7/7 | **COMPLETE** — validated on Linux (westGate) + Windows (blueGate) |
| Primal tests | **~63K+** |
| Signal graphs | **27** |
| BTSP | **13/13** |
| Linux depot | **19/19** (16 musl + 3 glibc) |
| Windows depot | **14/14 CURRENT** (rebuilt Jul 30 — zero blocked) |
| Depot targets | **5** (musl, gnu, windows-gnu, aarch64-musl, aarch64-android) |
| Gates online | **10** |
| strandGate NUCLEUS caps | **1,742** |
| strandGate IPC methods | **674** |
| GPU | RTX 3090 matmul p50 **0.30ms**, pipeline **~2,000 ops/sec** |
| CAS objects (westGate) | **3,216** on ZFS 25.3TB |
| Provenance Trio | **7/7 COMPLETE** — live E2E signed chain on westGate (ZFS) + blueGate (Windows) |
| Sovereign CI | **LIVE** — push-to-deploy, J9+J10+J11 killed |
| sweetGrass P2 UUID | **FIXED** (`4b5167b`) |
| biomeOS | **v4.51** — 14 unused deps removed, registry perf fix. Socket evap P2 REOPENED (non-sporeGate deploys). |
| squirrel | **7,138 tests** (Wave 155n). 90.1% coverage. 0 unsafe. 0 clippy. All IPC adapters wired. |
| sporeGate | **11/11 HEALTHY** — first clean gate health. biomeOS v4.51 deployed. |
| bearDog | **14,019 tests**, crypto.sign + Windows gate shipped |
| cellMembrane boot_order | **SHIPPED** (b7707ee) |
| cellMembrane dns.configure | **SHIPPED** (2b82722, 1,247 tests) |
| Active dimensions | **9** (D10 Jelly Strings REOPENED for J9–J13) |
| Fossilized dimensions | **13** (F13 covers J1–J8 only) |
| P0s | **ZERO** |
| P1s | **ZERO** — membrane.exe FIXED (`4ccbab1`) |
| P2s | **ZERO** — socket evaporation FIXED for all deploy paths (`999044e7`) |
| P3s | **2 OPEN** — cellMembrane self-CI, golgi hook auto-fire |
| Depot | **35** binaries: 16 musl + **4** gnu + 15 windows (biomeOS gnu NEW, all BLAKE3 verified) |

---

## WHAT'S NEXT

```
gen4: COMPLETE. gen5: NUCLEUS IS THE PLATFORM. squirrel + biomeOS + petalTongue + Node Atomics.

Done this wave:
  ✓ ALL P0/P1/P2 divergences RESOLVED (11/11 fixed by 5 code teams + biomeOS + cellMembrane)
  ✓ 3 NUCLEUS gates (westGate, blueGate, strandGate) — Provenance 7/7 on 2 platforms
  ✓ Sovereign CI LIVE — push-to-deploy automated (J9+J10+J11 killed)
  ✓ Depot 35 binaries (16 musl + 4 gnu + 15 windows) — biomeOS gnu NEW, BLAKE3 verified
  ✓ biomeOS v4.50 socket ownership + evaporation + binary path + capability wipe ALL FIXED
  ✓ cellMembrane: membrane.exe P1, checksums, sandbox, rootpulse, tmpfiles, reqwest purge
  ✓ toadStool S349, petalTongue --family-id, bearDog dual-socket + FAMILY_SEED + 94 files
  ✓ whitePaper gen4 COMPLETE checkpoint, sporePrint live science strategy
  ✓ 6/10 jelly strings killed (J9–J11, J14–J15, J17)

NUCLEUS AS LIVE PLATFORM (gen4 DONE — gen5 is the platform serving real workloads):
  squirrel (AI agent) → biomeOS (backend) → petalTongue + Node Atomics (rendering + GPU)
  = science visualization, game engines, AI agents, provenance-tracked artifacts

  PLATFORM WIRING:
    G18: squirrel → biomeOS neuralAPI agent orchestration (natural language → dispatch)
    G19: petalTongue + Node Atomics live rendering pipeline (GPU → WebGL/WASM output)
    G20: esotericWebb game engine on NUCLEUS (shaders, scene composition, creative surface)

  SCIENCE PIPELINE (one track through the platform):
    Step 3: tideGlass Phase 0 — GPS archaeology, Zenodo download. NEXT.
    Steps 4-7: Reproduce → NF ingestion → reversal screen → NF pseudoSpore
    Step 8: JOSS paper + CTF NDU
    Timeline: pseudoSpore late Sep (optimistic) / Dec 2026 (realistic)

  DATA INGESTION:
    G7:  AlphaFold ~1TB through westGate Nest Atomic (pipeline READY)

DEPLOYMENT + EXPANSION:
  1. Gate redeployments: v4.50 + cellMembrane fixes to westGate, strandGate, blueGate
  2. J12: blueGate sub-builder enrollment
  3. steamGate: Steam Deck Tower Atomic (cellMembrane user-space deploy ready)

LIVE SCIENCE (sporePrint = subGen presented to the world):
  G14: sporePrint content refresh (Phase 1 NOW)
  G16: pseudoSpore grab pattern on web (Phase 3, after NF data)
  Surfaces: QCD viz, game engine, GIS, genomics — all powered by NUCLEUS

GLACIAL:
  G6:  bearDog public (crates.io)
  G8:  Plasmodium (multi-gate bonding)
  G11: Any chip + drive = mesh gate (steamGate NEXT)
  G12: darwinGate — Mac Mini acquisition
  G13: iosGate — iPhone (after darwin)
  G17: Portability — reconstitute from cold (pseudoSpore pack/unpack)
```

---

### SPOREPRINT (Wave 155m — Jul 30, 2026)

**NUCLEUS transplant + root doc cleanup:**
- NUCLEUS ACHIEVED on 3 gates, Provenance 7/7, gen4 COMPLETE
- NUCLEUS promoted to Deploy Now shelf, architecture index leads with it
- 94,927 tests, ZERO P0/P1/P2. bearDog 14,019, rhizoCrypt 1,900
- README: canonical URL fixed, NUCLEUS/Provenance/SovCI milestones marked done
- CITATION.cff date updated, EVOLUTION_QUEUE refreshed to 155m state
- cargo clean: removed 1.3G build artifacts
- No stale scripts, orphan pages, or debris found. All TODOs in content are
  legitimate (documenting "zero TODO in primals", not actual action items)

**Upstream gaps for primal teams:**
- barraCuda/wetSpring: JOSS-ready? Need published release (crates.io or Zenodo)
- All springs: "Reproduce It" sections still needed in READMEs (per SEO standard)
- wateringHole PRIMAL_EMOJI_STANDARD: sporePrint entity registry needs cross-check

---

*Wave 155m — gen4 COMPLETE. NUCLEUS IS THE PLATFORM: squirrel (AI agent) → biomeOS (backend)
→ petalTongue + Node Atomics (rendering + GPU) = science to videogames. ZERO P0/P1/P2.
11/11 divergences FIXED. 6/10 jelly strings killed. Depot 35 binaries. biomeOS v4.50.
Provenance 7/7. 3 NUCLEUS gates. Sovereign CI LIVE. 20 glacial goals (G3-G4 COMPLETE,
G18-G20 NEW: agent orchestration, live rendering, game engine). Science pipeline: tideGlass
Phase 0 NEXT. pseudoSpore target: late Sep / Dec 2026. ~63K+ tests.*
