# ecoPrimals Ecosystem Blurb — Wave 155m

**Date**: Jul 31, 2026 09:15 EDT | **Wave**: 155n | **From**: eastGate overwatch
**Posture**: **P1 OPEN: biomeOS respawn storm — riboCipher health pings fail on plain JSON-RPC primals → DEGRADED → unbounded process accumulation (175 procs/14 min on strandGate). Socket evaporation confirmed on westGate (50% survival). Root cause: riboCipher and plain JSON-RPC are facets of the same protocol layer, not competing systems — biomeOS health monitor must speak both. Golgi hook P2 FIXED (3 bugs). Depot rebuilt with 999044e7 + 301e236. Sovereign CI E2E verified. cellMembrane shipped MEMBRANE_* env standardization + crypto dedup. 6 P3s tracked.**

---

## NUCLEUS — ACHIEVED

Three gates now running full NUCLEUS. Provenance 7/7 validated on two platforms.

```
westGate NUCLEUS (Jul 31 — v4.51 deployed, PROVENANCE 7/7 COMPLETE):
  13/13 alive | 835 peak caps | Provenance 7/7 (4 consecutive passes)
  ZFS: 25.4TB ONLINE, 3,256 CAS objects, 1.56× compression
  ⚠ Socket evaporation P1: 31→16 sockets in 3 min (50% survival)
  ⚠ membrane/ vs biomeos/ socket dir mismatch (symlink workaround)

blueGate NUCLEUS (Jul 30 — Windows, Provenance 7/7 VALIDATED):
  13/13 primals, 131.1 MB, TCP-only, crypto.sign LIVE

strandGate NUCLEUS (Jul 31 — v4.51 depot deploy, 999044e7 confirmed):
  11/12 healthy | 912 methods | 27 sockets
  ⚠ RESPAWN STORM P1: 175 procs / 14 min, 538 resurrections
  ⚠ riboCipher health ping → plain JSON-RPC primals = DEGRADED → respawn loop

sporeGate SOVEREIGN CI LIVE (Jul 31 — golgi hook FIXED):
  11/11 HEALTHY | 35 depot bins | Golgi hook E2E verified
  Push to Forgejo → auto build → sandbox → depot push → HTTPS serve
  J9+J10+J11 KILLED. Zero human intervention for non-broker primals.
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

### Divergences — Wave 155n

#### P1 — MUST FIX

| Issue | Evidence | Owner | Status |
|-------|----------|-------|--------|
| **Respawn storm** — biomeOS health pings use riboCipher framing, most primals speak plain JSON-RPC → every primal cycles DEGRADED every ~90s → unbounded process accumulation | strandGate: 175 procs / 14 min, 538 resurrections. Kill-before-spawn doesn't reliably reap old instances. | **biomeOS** | **P1 OPEN** |
| **Socket file deletion** — biomeOS unlinks socket files for primals that fail health ping, even though processes are alive | westGate: 31→16 sockets in 3 min (50% survival). All procs alive, sockets deleted. 3 versions, same result. | **biomeOS** | **P1 OPEN** |

**Root cause for both P1s**: riboCipher and plain JSON-RPC are **facets of the same protocol layer** (riboCipher is the intra-functional framing of mitoBeacon genetics). biomeOS health monitor must speak both — ping with riboCipher first, fall back to plain JSON-RPC, or primals declare their protocol at registration. biomeOS must NEVER unlink a socket it didn't create.

#### Previously FIXED (confirmed on gates)

| Issue | Fix | Commit | Gate Validation |
|-------|-----|--------|-----------------|
| bearDog `FAMILY_SEED` precedence | env → file → auto-generate | `a875d463` | westGate CONFIRMED |
| `PRIMAL_BIND_MODE` `tcp_only` fallback | petalTongue accepts `tcp` semantics | `551e781` | westGate CONFIRMED |
| petalTongue `--family-id` propagation | Global flag (before subcommand) | `551e781` | westGate CONFIRMED (caveat: global not subcommand) |
| biomeOS capability wipe cycle | 3-strike prune threshold | `f2d4c4b3` | westGate: retention 30s→165s (+450%). Still cycles. |
| toadStool JSON-RPC | compute.sock responds | `5053e0bc` | westGate: works via riboCipher prefix |
| membrane.exe `UnixStream` P1 | `#[cfg(unix)]` gates + Windows stubs | `4ccbab1` | blueGate CONFIRMED |
| cellMembrane reqwest purge | Sovereign HTTP/1.1 client | `4e77ffd` | westGate: binary -2MB CONFIRMED |
| biomeOS binary path retention | 5-tier probe | `999044e7` | strandGate: all primals found in ~/.local/bin/ |
| golgi post-receive hook | 3 bugs fixed (dispatcher, case, category) | sporeGate 155n | E2E verified (squirrel auto-built) |
| GATE_NAME vs MEMBRANE_GATE_NAME | MEMBRANE_* env standardization + fallback | `4a2b39c` | cellMembrane shipped |

#### PARTIAL — needs convergence

| Issue | Status | Detail |
|-------|--------|--------|
| bearDog dual-socket | **PARTIAL** | Default socket still separate listener returning stubs. Family socket works. Workaround: set `BEARDOG_SOCKET`. |
| Socket evaporation (binary discovery) | **PARTIAL** | Binary discovery FIXED (999044e7). But socket file deletion is a separate code path — biomeOS unlinks sockets regardless. |
| membrane/ vs biomeos/ socket dir | **OPEN** | Primals create in `/run/user/1000/biomeos/`, Neural API scans `/run/user/1000/membrane/`. Workaround: symlink bridge. |

#### P3 — Tracked

| Issue | Owner | Status |
|-------|-------|--------|
| cellMembrane not in sources.toml | cellMembrane | Blocks self-CI |
| biomeOS sandbox false positive for broker primals | biomeOS + cellMembrane | Needs composition.test_swap |
| /run/membrane permission reset at runtime | biomeOS | Resets dir to 0770 on connection |
| Zombie process reaping | biomeOS | waitpid() / SIGCHLD handler needed |
| Virtual service DEGRADED churn | biomeOS | Exclude aggregate capability sockets from health monitor |
| graphs_dir default path | biomeOS | Falls back to $CWD/graphs, missing on non-sporeGate |
| riboCipher rejection at ERROR level | biomeOS | Should be WARN/DEBUG for protocol negotiation |
| biomeOS `--version` reports 0.1.0 | biomeOS | Version not set during CI build |
| GNU depot incomplete | sporeGate | 4/16 musl targets have gnu builds |

---

## CROSS-PLATFORM EXPANSION — genomeBin Mesh

**Principle**: anything with a chip and a drive is a mesh gate. The genomeBin
standard + Tower Atomic abstraction means one codebase → any platform.

### Depot Targets — Current vs Needed

| Target Triple | Status | Depot | Gates |
|---------------|--------|-------|-------|
| `x86_64-unknown-linux-musl` | **LIVE** | 16 bins | eastGate, sporeGate, westGate, strandGate, ironGate, flockGate |
| `x86_64-unknown-linux-gnu` | **LIVE** | 4 bins (biomeOS + cellMembrane + petalTongue + squirrel) | strandGate (GPU) |
| `x86_64-pc-windows-gnu` | **LIVE** | 15 bins | blueGate, swiftGate, northGate |
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
| **biomeOS** | 8,570 | v4.51+ binary discovery FIXED (`999044e7`). 14 deps removed. **TWO P1s OPEN**: (1) respawn storm — kill-before-spawn + protocol negotiation; (2) socket file deletion — never unlink a socket biomeOS didn't create. riboCipher health pings must fall back to plain JSON-RPC. | **P1 FIX** |
| **cellMembrane** | 1,273 | MEMBRANE_* env standardization (GATE_NAME P3 FIXED), crypto dedup (HKDF/HMAC consolidated), bootstrap 738→291L + phases split, plasmid smart split (-310L). | sources.toml self-enrollment. |
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
| **sporeGate** | **11/11 HEALTHY** (perm drift to 8/11). Golgi hook FIXED (3 bugs). Depot rebuilt: 35 bins, all current. | biomeOS composition authority evolution. |
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
| P1s | **2 OPEN** — biomeOS respawn storm + socket file deletion (riboCipher health ping mismatch) |
| P2s | **ZERO** — golgi hook FIXED (3 bugs), depot rebuilt with `999044e7` + `301e236` |
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
