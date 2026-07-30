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
| biomeOS socket evaporation (health ping format) | Any successful `call_btsp()` = alive (v4.50) | `06ed323f` | **FIXED** |
| biomeOS binary path retention | Discovery probes plasmidBin dirs, stores resolved path | `06ed323f` | **FIXED** |
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

### ALL TEAMS STANDBY (12 teams — all P1s shipped)

| Team | Tests | Key Delivery | Resume When |
|------|-------|-------------|-------------|
| **biomeOS** | 8,564 | **NUCLEUS orchestrator v4.47**: riboCipher fix, socket unification, capability persistence, composition lifecycle, bind flag standard | NUCLEUS E2E validation on gates |
| **bearDog** | 14,019 | **crypto.sign_ed25519** + Windows platform gating. ACME Phase 2 crypto delegation. | Provenance 7/7 live validation |
| **cellMembrane** | 1,247 | boot_order + `dns.configure`/`dns.apply` | Composition lifecycle gate deployment |
| **toadStool** | 9,193 | S347 Windows cross-compile fix | sporeGate depot rebuild |
| **coralReef** | 3,527 | Windows fix + `--bind` alias | sporeGate depot rebuild |
| **songBird** | 14,835 | P0 Windows fix + deep debt | biomeOS TCP registration |
| **sweetGrass** | 1,639 | G3 E2E + UUID fix | Provenance 7/7 live validation |
| **rhizoCrypt** | 1,900 | Cross-compile clean + `--bind` | NUCLEUS lifecycle testing |
| **loamSpine** | 1,739 | Registry fixed + `--bind` | Provenance 7/7 live validation |
| **nestGate** | 13,095+ | CAS on ZFS verified | AlphaFold ingestion |
| **petalTongue** | 6,605 | Stable v1.7.0 | WASM validation |
| **squirrel** | 763 | Stable | Capability testing |

### GATE STANDBY

| Gate | Status | Resume When |
|------|--------|-------------|
| **strandGate** | **NUCLEUS** (v4.47 depot deploy, `nucleus start`). Socket evaporation P2. | biomeOS v4.49 ping tolerance fix. |
| **blueGate** | **NUCLEUS** (14/14 fresh, Provenance 7/7 validated). | Sub-builder (needs membrane.exe P1). |
| **westGate** | **NUCLEUS** (Provenance 7/7 COMPLETE, ZFS 25.4TB). | AlphaFold ~1TB ingestion. |
| **swiftGate** | HW ready. Windows. | After blueGate sub-builder stable. |
| **ironGate** | Online. 14TB+1TB+1TB+2TB. | Tower + HDD enclave. |
| **southGate** | HW ready. | Enrollment. |
| **grapheneGate** | Tower LIVE (Pixel 8a). | ADB mesh expansion. |

### GATE ACTIVE

| Gate | Status | Next |
|------|--------|------|
| **eastGate** | Overwatch. | Cross-platform expansion. Disseminate P2 divergences. |
| **sporeGate** | **Sovereign CI LIVE.** Push-to-deploy automated. | J12 (blueGate sub-builder, blocked on membrane.exe). J13 polish. |

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
| biomeOS | **v4.50** — socket evap + binary path FIXED (`06ed323f`). Deployed on sporeGate. |
| bearDog | **14,019 tests**, crypto.sign + Windows gate shipped |
| cellMembrane boot_order | **SHIPPED** (b7707ee) |
| cellMembrane dns.configure | **SHIPPED** (2b82722, 1,247 tests) |
| Active dimensions | **9** (D10 Jelly Strings REOPENED for J9–J13) |
| Fossilized dimensions | **13** (F13 covers J1–J8 only) |
| P0s | **ZERO** |
| P1s | **ZERO** — membrane.exe FIXED (`4ccbab1`) |
| P2s | **ZERO** |
| P3s | **2 OPEN** — cellMembrane self-CI, golgi hook auto-fire |
| Depot | **35** binaries: 16 musl + **4** gnu + 15 windows (biomeOS gnu NEW, all BLAKE3 verified) |

---

## WHAT'S NEXT

```
gen4: COMPLETE. gen5: INFRASTRUCTURE READY. Science pipeline is sole bottleneck.

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

GEN5 CRITICAL PATH (infrastructure DONE — science pipeline is sole bottleneck):
  Step 3: tideGlass Phase 0 — GPS archaeology, Zenodo download, deps. NEXT.
  Step 5: NF Data Portal ingestion through Nest Atomic (can start data download now)
  Step 7: One NF pseudoSpore — the gen5 artifact
  Step 8: JOSS paper + CTF NDU prelim data
  Timeline: pseudoSpore late Sep (optimistic) / Dec 2026 (realistic)

DEPLOYMENT + EXPANSION:
  1. Gate redeployments: westGate, strandGate, blueGate — fresh v4.50 + cellMembrane fixes
  2. J12: blueGate sub-builder enrollment under sporeGate
  3. steamGate: Steam Deck Tower Atomic (cellMembrane user-space deploy ready)
  4. AlphaFold ~1TB ingestion through westGate Nest Atomic (G7)

LIVE SCIENCE (sporePrint = subGen presented to the world):
  G14: sporePrint content refresh to Wave 155m reality (Phase 1 — NOW)
  G16: pseudoSpore grab pattern on web (Phase 3 — after NF data)
  Surfaces: hotSpring QCD viz, footPrint GIS, wetSpring genomics, esotericWebb

GLACIAL:
  G6:  bearDog public (crates.io)
  G8:  Plasmodium (multi-gate bonding)
  G11: Any chip + drive = mesh gate (steamGate NEXT)
  G12: darwinGate — Mac Mini acquisition
  G13: iosGate — iPhone (after darwin)
  G17: Portability — reconstitute from cold (cellMembrane site-profile + pseudoSpore)
```

---

*Wave 155m — gen4 COMPLETE. gen5 infrastructure READY. ZERO P0/P1/P2. 11/11 divergences
FIXED. 6/10 jelly strings killed. Depot 35 binaries. biomeOS v4.50. Provenance 7/7. 3
NUCLEUS gates. Sovereign CI LIVE. sporePrint live science strategy shipped. gen5 critical
path: tideGlass Phase 0 is sole bottleneck (Steps 1-2 DONE, 6 remaining). pseudoSpore
target: late Sep (optimistic) / Dec 2026 (realistic). 2 P3s remaining. ~63K+ tests.*
