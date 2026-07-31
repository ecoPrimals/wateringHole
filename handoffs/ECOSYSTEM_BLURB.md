# ecoPrimals Ecosystem Blurb — Wave 155n

**Date**: Jul 31, 2026 13:10 EDT | **Wave**: 155n | **From**: eastGate overwatch
**Posture**: **ZERO P0/P1. 1 P2 (membrane.exe platform detection, blocks J12). ALL 4 NUCLEUS gates on v4.55. southGate ENROLLED. NODE ATOMIC LANDMARK: strandGate 2,130 matmul/sec, cross-atomic provenance E2E. Coevolution COMPLETE (G21). G22 NEW: whitePaper API convergence. gen5 thesis VALIDATED.**

---

## NUCLEUS — ACHIEVED

Four gates running full NUCLEUS. Both P1s gate-validated. Provenance 7/7 on two platforms.

```
westGate NUCLEUS v4.55 — P1 GATE VALIDATED (Jul 31):
  31/31 sockets stable 225s (was 31→16 in 3 min on v4.51). 0% socket loss.
  835 peak caps | Provenance 7/7 (5th consecutive pass)
  ZFS: 25.4TB ONLINE, 3,256 CAS objects, 1.56× compression
  Mode gap fix verified: Neural API Coordinated, 13 primals ACTIVE.

strandGate NUCLEUS v4.55 — NODE ATOMIC LANDMARK (Jul 31):
  12/12 HEALTHY | 1,017 methods | 30 sockets | 13 processes (1 per primal)
  RTX 3090: 2,130 matmul/sec, SVD 128×128 in 48.7ms, FFT 4096 in 11.6ms
  Concurrent 4-primal: 5,268 ops/sec, 0 errors. 56+ min stable.
  Cross-atomic IPC E2E: GPU→sign→verify→DAG→attribution→Merkle. W3C PROV-O.
  AlphaFold: 20-30 structures/day capacity, reduced DB fits (1.3TB free).
  "This is no longer a whitePaper. This is a working system."

blueGate NUCLEUS v4.55 (Jul 31 — Windows, biomeOS v4.55.0 deployed):
  13/13 primals, 173.6 MB warm. Prov 7/7 E2E. crypto.sign LIVE.
  membrane.exe first Windows run: networking OK, local probes P2 (linux-musl target).
  ⚠ P2: membrane.exe embeds linux-musl target triple — blocks J12 sub-builder.

sporeGate SOVEREIGN CI LIVE (Jul 31 — golgi hook FIXED):
  11/11 HEALTHY | 35 depot bins | Golgi hook E2E verified
  Push → build → sandbox → composition.test_swap → depot push → HTTPS serve
  9/11 jelly strings KILLED. Fully automated for ALL 13 primals.
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
| A3 | **blueGate** | biomeOS v4.55 + membrane.exe on Windows | **DONE** — v4.55.0 deployed, membrane first run. P2: platform detection. |
| A4 | **strandGate** | Redeploy with biomeOS v4.55 | **DONE** — P1 GATE VALIDATED: 12/12, 1,017 methods, 1 proc/primal |

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
| **Respawn storm** — riboCipher-only health pings caused DEGRADED cycling → unbounded process accumulation | strandGate: 175→**13** procs (1 per primal). **GATE VALIDATED.** | **biomeOS** | **FIXED + VALIDATED** v4.55 — dual-protocol ping. Kill-before-spawn. |
| **Socket file deletion** — biomeOS unlinked sockets for primals that failed health ping | westGate: **31/31 sockets held 225+ sec** (was 31→16 in 3 min). **GATE VALIDATED.** | **biomeOS** | **FIXED + VALIDATED** v4.55 — PID ownership guard. 0% socket loss. |

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

#### CONVERGENCE — legacy items resolved or P3

| Issue | Status | Detail |
|-------|--------|--------|
| bearDog dual-socket | **P3** | Default socket still separate listener returning stubs. Family socket works. Workaround: set `BEARDOG_SOCKET`. Non-blocking. |
| ~~Socket evaporation~~ | **FIXED + VALIDATED** | PID ownership guard (`88785daf`): 0% socket loss on westGate (225s test). |
| membrane/ vs biomeos/ socket dir | **P3** | Symlink bridge works. Will converge when biomeOS owns socket namespace (G22 API convergence). |

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
| **biomeOS** | 8,570 | **v4.55+** (`652cf8a7`): mode gap FIXED — Neural API `btsp_optional=true`, accepts plain JSON-RPC. `composition.test_swap` E2E path OPEN. Depot rebuilt 11:11 EDT. | Convergence: merge api + neural-api into single process. |
| **cellMembrane** | 1,281+ | Registry API hardened (`require_capability`/`require_binary`). `validate_via_composition` test hardened. J19+J16+J13 shipped. | STANDBY — coevolution complete from cellMembrane side. |
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
| **westGate** | **NUCLEUS v4.55.** 31/31 sockets stable 225s. Prov 7/7 (5th pass). 835 caps. **Both P1s VALIDATED FIXED.** | AlphaFold ingestion. |
| **strandGate** | **NUCLEUS v4.55.** 12/12 HEALTHY. 1,017 methods. 13 procs (1 each). RTX 3090 p50=0.33ms. **P1 VALIDATED FIXED.** | Node Atomic profiling. |
| **blueGate** | **NUCLEUS v4.55** (13/13). Prov 7/7. membrane.exe first Windows run. **P2: platform detection** (linux-musl embedded in Windows binary). | cellMembrane platform fix → J12 sub-builder. |
| **flockGate** | **DOWN** — rebooted, RustDesk locked out. May be on mesh. | **esotericWebb → ironGate** (LAN). |
| **ironGate** | Online. 14TB+1TB+1TB+2TB. **Takes esotericWebb from flockGate.** | Tower + esotericWebb + HDD enclave. |
| **swiftGate** | HW ready. Windows. | After blueGate sub-builder stable. |
| **southGate** | **ENROLLED** — 32/33 repos at 155n HEAD. 16 musl binaries deployed (biomeOS v4.55). 5800X3D + RTX 4060 + 128GB + 5TB NVMe. WG peer add pending (sudo). | NUCLEUS launch + gate validation. |
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
| NUCLEUS gates | **4 — ALL v4.55** (westGate, strandGate, blueGate, sporeGate) + **southGate ENROLLED** |
| Provenance 7/7 | **COMPLETE** — westGate (5th consecutive pass) + blueGate (Windows) |
| Primal tests | **~101K+** |
| Signal graphs | **27** |
| BTSP | **13/13** |
| Depot | **35** binaries: 16 musl + 4 gnu + 15 windows. biomeOS v4.55 rebuilt 11:11 EDT. BLAKE3 verified. |
| Gates online | **9** (flockGate DOWN) |
| biomeOS | **v4.55** in depot — both P1s GATE VALIDATED + coevolution + mode gap fix. |
| squirrel | **7,138 tests**, 90.1% cov, 0 unsafe, 0 clippy, all IPC wired |
| cellMembrane | **1,281+ tests**, `validate_with_deps`, registry API hardened, J19+J16+J13 killed |
| sporeGate | **11/11 HEALTHY**, golgi hook FIXED, Sovereign CI E2E verified for ALL 13 primals |
| P0s | **ZERO** |
| P1s | **ZERO** — both GATE VALIDATED (westGate: 0% socket loss, strandGate: 1 proc/primal) |
| P2s | **1 NEW** — membrane.exe platform detection (linux-musl on Windows, blocks J12) |
| P3s | **6 P3** — /run/membrane perms, bearDog dual-socket, songBird PID, rhizoCrypt double-port, coralReef --version log, petalTongue TCP close |
| Jelly strings | **9/11 KILLED.** 2 remaining: J12 (sub-builder), J18 (gate coupling/portability) |
| Glacial goals | **22** tracked (G3+G4+G21 COMPLETE, **G22 NEW: whitePaper API convergence**) |

---

## WHAT'S NEXT

```
whitePaper CONVERGENCE (G22 — NEW CONCEPTUAL GOAL):
  biomeOS API + neuralAPI merge into single process.
  Long-term whitePaper goal now suddenly achievable: coevolution (G21) proved
  that biomeOS can speak both riboCipher and plain JSON-RPC natively via
  btsp_optional=true. The dual-service architecture was transitional scaffold.
  One biomeOS process = one socket namespace = full composition authority.

  CONVERGENCE STEPS:
    - Merge api + neural-api into single biomeOS process
    - biomeOS owns /run/membrane socket namespace
    - Sovereign CI trigger: git pull before build (source tree divergence fix)
    - P3 cleanup: /run/membrane perms, bearDog dual-socket, socket dir mismatch

PRIORITY 2 — FLEET EXPANSION:
  1. southGate: WG peer add (sudo) → NUCLEUS launch → gate validation (5800X3D + RTX 4060)
  2. cellMembrane: P2 membrane.exe platform detection fix (blocks J12)
  3. ironGate: takes esotericWebb from flockGate (LAN)
  4. steamGate: Steam Deck Tower Atomic (gnu bins in depot, user-space deploy)
  5. J12: blueGate sub-builder after membrane.exe platform fix
  6. J18: /etc/environment abstraction (last portability jelly string)

PRIORITY 3 — PLATFORM WIRING (gen5):
  G18: squirrel → biomeOS neuralAPI agent orchestration
  G19: petalTongue + Node Atomics live rendering pipeline
  G20: esotericWebb game engine on NUCLEUS (ironGate)

SCIENCE PIPELINE:
  Step 3: tideGlass Phase 0 — archaeology. NEXT.
  Steps 4-8: Reproduce → NF → pseudoSpore → JOSS. Target: late Sep / Dec 2026.
  G7: AlphaFold ~1TB through westGate Nest Atomic (pipeline READY)

GLACIAL:
  G6: bearDog public | G8: Plasmodium | G11: steamGate
  G12: darwinGate | G13: iosGate | G17: Portability
```

---

*Wave 155n — ZERO P0/P1. 1 P2 (membrane.exe platform). ALL 4 NUCLEUS gates on v4.55.
southGate ENROLLED (5th NUCLEUS gate pending launch). NODE ATOMIC LANDMARK: strandGate
RTX 3090 — 2,130 matmul/sec, cross-atomic provenance chain E2E, W3C PROV-O, AlphaFold
20-30/day capacity. gen5 thesis VALIDATED: "this is no longer a whitePaper." Coevolution
COMPLETE (G21). G22 NEW: whitePaper API convergence. 9/11 jelly strings KILLED. ~101K+ tests.*
