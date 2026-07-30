# ecoPrimals Ecosystem Blurb — Wave 155k

**Date**: Jul 30, 2026 10:10 EDT | **Wave**: 155k | **From**: eastGate overwatch
**Posture**: **PROVENANCE 7/7 COMPLETE. westGate NUCLEUS (second gate, 13/13, 654 caps, Provenance 7/7 first-ever full signed chain on live hardware). blueGate NUCLEUS refreshed (14/14 depot, 131 MB, Provenance 7/7 validated on Windows). SOVEREIGN CI LIVE on sporeGate (J9+J10+J11 killed — push-to-deploy automated). ZERO P0s. 1 P1 (membrane.exe Windows cross-compile). 12 teams STANDBY.**

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
| J12 | blueGate sub-builder dispatch | **BLOCKED** — membrane.exe won't cross-compile (P1) |
| J13 | Depot freshness probe | ~20 LOC — `mesh.build_pending` wire needed |

Handoff: `CELLMEMBRANE_WAVE155k_SOVEREIGN_CI_POLISH.md` (3 items: build_pending 20 LOC, webhook listener 200 LOC, membrane.exe P1)

### Divergences Found (P2 — upstream teams)

| Issue | Gate | Owner | Priority |
|-------|------|-------|----------|
| bearDog dual-socket footgun (`default` vs `family-scoped` have different capabilities) | westGate | bearDog | P2 |
| bearDog `FAMILY_SEED` now required (breaking change from 155i) | blueGate | bearDog (docs) | P2 |
| `PRIMAL_BIND_MODE` — `tcp_only` silently falls back to `auto` (should be `tcp`) | blueGate | All primals | P2 |
| biomeOS capability wipe cycle (654→0→187→654 over ~60s on rescan) | westGate | biomeOS | P2 |
| biomeOS Neural API socket still hardcoded to `membrane/` (not unified) | westGate | biomeOS | P2 |
| toadStool tarpc-only (no JSON-RPC health endpoint) | westGate | toadStool | P2 |
| petalTongue rejects `--family-id` flag | westGate | petalTongue | P2 |
| biomeOS API 403 on all non-/health endpoints (BTSP auth enforced) | blueGate | biomeOS (docs) | P2 |
| membrane.exe `UnixStream` not `#[cfg(unix)]` gated | sporeGate | cellMembrane | **P1** |

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
| **strandGate** | **NUCLEUS** (manual startup). | biomeOS v4.47 redeploy. |
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
| biomeOS | **v4.47 NUCLEUS orchestrator** (`bd202674`) |
| bearDog | **14,019 tests**, crypto.sign + Windows gate shipped |
| cellMembrane boot_order | **SHIPPED** (b7707ee) |
| cellMembrane dns.configure | **SHIPPED** (2b82722, 1,247 tests) |
| Active dimensions | **9** (D10 Jelly Strings REOPENED for J9–J13) |
| Fossilized dimensions | **13** (F13 covers J1–J8 only) |
| P0s | **ZERO** |
| P1s | **1** — membrane.exe Windows cross-compile (blocks blueGate sub-builder) |

---

## WHAT'S NEXT

```
NUCLEUS: 3 gates. Provenance 7/7: COMPLETE. Sovereign CI: LIVE. 1 P1 remaining.

Done this wave:
  ✓ westGate NUCLEUS (13/13, 654 caps, 29 sockets, Provenance 7/7)
  ✓ blueGate NUCLEUS refreshed (131 MB, Provenance 7/7 on Windows)
  ✓ Sovereign CI on sporeGate (J9+J10+J11 killed, push-to-deploy live)
  ✓ Depot 14/14 rebuilt + BLAKE3 verified

Active:
  1. P1: membrane.exe Windows cross-compile (blocks blueGate sub-builder J12)
  2. P2 divergences: bearDog dual-socket, FAMILY_SEED, capability wipe cycle (9 items)
  3. strandGate: redeploy with biomeOS v4.47
  4. AlphaFold ~1TB ingestion through westGate Nest Atomic
  5. steamGate: Steam Deck user-space Tower (have HW, gnu bins in depot)

Glacial:
  G6:  bearDog public (crates.io)
  G9:  JOSS publication — live multi-platform NUCLEUS with Provenance 7/7
  G8:  Plasmodium (multi-gate bonding)
  G11: Any chip + drive = mesh gate
  G12: darwinGate — Mac Mini acquisition
  G13: iosGate — iPhone (after darwin)
```

---

*Wave 155k — PROVENANCE 7/7 COMPLETE. 3 NUCLEUS gates (westGate, blueGate, strandGate).
Sovereign CI LIVE (push-to-deploy). westGate: first full signed provenance chain on live
ZFS hardware. blueGate: Provenance 7/7 on Windows. J9+J10+J11 killed. 1 P1 (membrane.exe).
9 P2 divergences cataloged. 33+ binaries, 5 targets. ~63K+ tests. 10+ gates.*
