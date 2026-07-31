# ecoPrimals Ecosystem Blurb — Wave 155m

**Date**: Jul 31, 2026 09:15 EDT | **Wave**: 155n | **From**: eastGate overwatch
**Posture**: **ZERO P0/P1/P2. COEVOLUTION SHIPPED. biomeOS v4.55 (`composition.test_swap`) + cellMembrane (`validate_with_deps`) = broker primals validated via live composition. J19 sandbox KILLED. J16 self-CI KILLED. J13 freshness KILLED. 9/11 jelly strings dead. Golgi hook FIXED. biomeOS v4.55 on Forgejo — pending depot rebuild to validate full pipeline E2E.**

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
| **Respawn storm** — riboCipher-only health pings caused DEGRADED cycling → unbounded process accumulation | strandGate: 175 procs / 14 min, 538 resurrections. | **biomeOS** | **FIXED in v4.54** (`88785daf`) — dual-protocol ping: plain JSON-RPC first, BTSP fallback |
| **Socket file deletion** — biomeOS unlinked sockets for primals that failed health ping | westGate: 31→16 sockets in 3 min (50% survival). | **biomeOS** | **FIXED in v4.54** (`88785daf`) — PID ownership + confirmed kill before unlink. Never removes sockets it didn't create. |

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
| ~~biomeOS sandbox false positive~~ | ~~cellMembrane + biomeOS~~ | **FIXED** — cellMembrane `00c6800` wires `composition.test_swap` delegation. biomeOS `5e540221` implements the endpoint. J19 KILLED. |
| ~~cellMembrane not in sources.toml~~ | ~~cellMembrane~~ | **FIXED** — `0d39075` garden self-enrollment in `provision_sources_from_manifest()`. J16 KILLED. |
| /run/membrane permission reset at runtime | biomeOS | Resets dir to 0770 on connection |
| GNU depot incomplete | sporeGate | 4/16 musl targets have gnu builds |
| ~~Zombie process reaping~~ | ~~biomeOS~~ | **FIXED in v4.54** (`88785daf`) — background child.wait() |
| ~~Virtual service DEGRADED churn~~ | ~~biomeOS~~ | **FIXED in v4.54** — skip resurrection for external primals |
| ~~graphs_dir default path~~ | ~~biomeOS~~ | **FIXED in v4.54** — XDG fallback + BIOMEOS_GRAPHS_DIR env |
| ~~riboCipher rejection at ERROR level~~ | ~~biomeOS~~ | **FIXED in v4.54** — demoted to debug |
| ~~biomeOS `--version` reports 0.1.0~~ | ~~biomeOS~~ | **FIXED in v4.54** — workspace version 4.54.0 |

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
| **biomeOS** | 8,570 | **v4.55** (`5e540221`): `composition.test_swap` shipped — running biomeOS validates its own replacement binary. Both P1s + 5 P3s FIXED. On Forgejo. | Depot rebuild (J19 should be unblocked). |
| **cellMembrane** | 1,281 | **J19 FIXED**: `validate_with_deps()` delegates broker primals to running biomeOS via `composition.test_swap`. **J16 FIXED**: `sources.toml` garden self-enrollment. **J13**: `plasmid.staleness --publish` mesh broadcast. Sandbox commit-suffix fix. Socket-base init-scope migration. | Depot rebuild validation. |
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
| NUCLEUS gates | **4** (westGate + blueGate + strandGate + sporeGate 11/11 HEALTHY) |
| Provenance 7/7 | **COMPLETE** — validated on Linux (westGate, 4 consecutive passes) + Windows (blueGate) |
| Primal tests | **~101K+** (squirrel 7,138 was undercounted previously) |
| Signal graphs | **27** |
| BTSP | **13/13** |
| Depot | **35** binaries: 16 musl + 4 gnu + 15 windows, BLAKE3 verified |
| Gates online | **9** (flockGate DOWN) |
| biomeOS | **v4.54** on Forgejo — both P1s FIXED + 5 P3s. **v4.51 in depot** (sandbox P2 blocks). |
| squirrel | **7,138 tests**, 90.1% cov, 0 unsafe, 0 clippy, all IPC wired |
| cellMembrane | **1,273 tests**, MEMBRANE_* standardization, crypto dedup, init-scope sockets |
| sporeGate | **11/11 HEALTHY**, golgi hook FIXED (3 bugs), Sovereign CI E2E verified |
| P0s | **ZERO** |
| P1s | **ZERO** — both FIXED in biomeOS v4.54 (`88785daf`) |
| P2s | **ZERO** — sandbox P2 FIXED (composition.test_swap coevolution shipped) |
| P3s | **2 OPEN** — /run/membrane perm reset, GNU depot incomplete |
| Jelly strings | **9/11 KILLED** (J13, J16, J19 killed this session). 2 remaining: J12 sub-builder, J18 gate coupling |
| Glacial goals | **21** tracked (G3-G4 COMPLETE, G21 NEW: coevolution contract) |

---

## WHAT'S NEXT

```
PRIORITY 1 — COEVOLUTION CONTRACT (G21, J19): biomeOS + cellMembrane

  biomeOS = COMPOSITION AUTHORITY:
    - composition.test_swap: hot-swap binary, validate in live composition, rollback on failure
    - Own /run/membrane socket namespace (create dir, set perms, manage lifecycle)
    - Manage cellMembrane as a composition member
    - Self-takeover: running biomeOS orchestrates its own replacement

  cellMembrane = BUILD AUTHORITY:
    - sovereign.ci.trigger: build binary, delegate validation to running biomeOS via neural-api
    - Depot push after biomeOS confirms composition health
    - sources.toml self-enrollment (J16)
    - MEMBRANE_GATE_NAME standardization (DONE in 4a2b39c)

  DELIVERABLES:
    biomeOS:  composition.test_swap capability + cellMembrane in composition graph
    cellMembrane: sovereign.ci.trigger → neural-api delegation (replaces standalone sandbox)

  UNBLOCKS:
    ✓ J19 sandbox false positive → biomeOS v4.54 reaches depot
    ✓ /run/membrane permission fights → biomeOS owns namespace
    ✓ Zero-downtime deploys → hot-swap with rollback
    ✓ biomeOS self-rebuild → full autonomous pipeline

PRIORITY 2 — GATE REDEPLOYMENTS:
  1. westGate + strandGate: redeploy biomeOS v4.54 from depot (after J19 resolved)
  2. ironGate: takes esotericWebb from flockGate (LAN, no RustDesk dependency)
  3. steamGate: Steam Deck Tower Atomic (cellMembrane user-space deploy READY)
  4. J12: blueGate sub-builder enrollment under sporeGate

PRIORITY 3 — PLATFORM WIRING (gen5):
  G18: squirrel → biomeOS neuralAPI agent orchestration
  G19: petalTongue + Node Atomics live rendering pipeline
  G20: esotericWebb game engine on NUCLEUS (ironGate, moved from flockGate)

SCIENCE PIPELINE (one track through the platform):
  Step 3: tideGlass Phase 0 — archaeology. NEXT.
  Steps 4-8: Reproduce → NF → pseudoSpore → JOSS. Target: late Sep / Dec 2026.
  G7: AlphaFold ~1TB through westGate Nest Atomic (pipeline READY)

LIVE SCIENCE:
  G14: sporePrint content refresh
  G16: pseudoSpore grab pattern on web (after NF data)

GLACIAL:
  G6: bearDog public (crates.io) | G8: Plasmodium | G11: steamGate
  G12: darwinGate | G13: iosGate | G17: Portability
```

---

*Wave 155n — ZERO P0/P1/P2. COEVOLUTION SHIPPED: biomeOS v4.55 (composition.test_swap) +
cellMembrane (validate_with_deps + J16 self-CI + J13 freshness). 9/11 jelly strings KILLED.
Both P1s FIXED (dual-protocol health ping + socket ownership guard). 5 P3s FIXED.
4 NUCLEUS gates (sporeGate 11/11 HEALTHY). Sovereign CI E2E verified. Golgi hook FIXED.
Provenance 7/7. 35 depot binaries. 21 glacial goals (G21 coevolution COMPLETE).
~101K+ tests. flockGate DOWN → esotericWebb to ironGate.*
