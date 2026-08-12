# ECOSYSTEM BLURB — Wave 157k Post-Pandemic Evolution

**Date**: Aug 12, 2026 | **Wave**: 157k | **From**: overwatch (eastGate)
**To**: ALL GATES + PRIMAL TEAMS
**Posture**: INNER MEMBRANE LIVE. 11 gates ONLINE (biomeGate DOWN). **0/0/0.** iosGate FIRST DEPLOY. graftGate FULL NUCLEUS via biomeOS Neural API. All canary bugs RESOLVED. Ownership rationalized.

---

## CODE TEAM OWNERSHIP — RATIONALIZED

| Gate | Code Teams | Role |
|------|-----------|------|
| eastGate | biomeOS, squirrel, projectNUCLEUS, primalSpring, blueFish + overwatch infra | Orchestration + sovereignty |
| ironGate | bearDog, songBird, skunkBat, swarmVine, bingoCube, petalTongue, esotericWebb, footPrint, tideGlass + 4 parked springs | Primal workhorse, 14TB NFT braid, primary Linux builder |
| strandGate | toadStool, barraCuda, coralReef, hotSpring, rustChip, helixVision, initioChem | Compute trio + batch HPC + science |
| westGate | rhizoCrypt, loamSpine, sweetGrass, nestGate, wetSpring, projectFOUNDATION | Provenance trio + data CAS (50.7TB ZFS) |
| sporeGate | cellMembrane, lithoSpore, plasmidBin ops | Topology + depot + cascade + pseudoSpore |
| graftGate | sourDough | Darwin builder (15/15, enmeshed) |
| southGate | neuralSpring | Validation canary |
| blueGate | (builds all 13, no code teams) | Windows builder |
| biomeGate | — | DOWN — SSH recovery pending |

---

## BUG STATUS — SOUTHGATE CANARY FINDINGS (ALL RESOLVED)

| # | Sev | Bug | Owner | Status |
|---|-----|-----|-------|--------|
| 1 | ~~P1~~ | ~~toadstool wgpu 28 backend panic~~ | strandGate (toadStool) | **RESOLVED.** Workspace `Cargo.toml` already has `vulkan-portability` feature (`e172eb0c3`). Depot binary needs rebuild from HEAD — source is correct. |
| 2 | ~~P2~~ | ~~riboCipher framing mismatch~~ | ironGate (swarmVine) | **RESOLVED.** swarmVine now accepts any ASCII-printable first byte as legacy JSON-RPC. Bidirectional gossip restored during rolling deploys. |
| 3 | ~~P2~~ | ~~swarmVine→songBird relay method~~ | ironGate (swarmVine + songBird) | **RESOLVED.** swarmVine calls `gossip.relay`. songBird added `mesh.*` → `gossip.*` aliases. Both sides fixed. |
| 4 | ~~P2~~ | ~~biomeOS skunkBat spawn leak~~ | eastGate (biomeOS) | **RESOLVED** (`6df4220e`). Root cause: `monitoring.rs` reset `resurrection_attempts` to 0 on Degraded transition → infinite spawn loops. Rapid-restart detection added. |

---

## OPERATIONAL BLOCKERS (5)

| # | Item | Owner | Update |
|---|------|-------|--------|
| 1 | blueGate depot pull — `.210:7700` timed out | blueGate | No response yet |
| 2 | eastGate NUCLEUS restart + hostname fix (`pop-os` → `eastgate`) | eastGate | primalSpring documented fix path — no reboot needed |
| 3 | ~~songBird `--node-id` flag~~ | ironGate (songBird) | **RESOLVED** in `5bc2d3988`. `--node-id` / `--gate-id` CLI flag added with env overlay. |
| 4 | southGate LAN IP `.149` vs `.148` | sporeGate topology | Minor |
| 5 | biomeGate SSH recovery | biomeGate | Gate down, eventual |

---

## GATE RESPONSES — POST-RATIONALIZATION REDEPLOY

### graftGate — CLEAN (15/15, Tower Atomic LIVE)
- 15/15 rebuilt from latest source (~10 min), depot pushed to golgiBody (104M, Aug 12 13:21 UTC)
- Tower Atomic: bearDog + songBird + skunkBat + swarmVine running, 6 LAN peers discovered
- sourDough: service template shipped (`028f0cc`), v0.4.0, all tests passing
- Xcode 26.6 installed, iOS SDK `iPhoneOS26.5.sdk` available, bearDog iOS cross-compile tested
- **0/0/0**

### ironGate — CLEAN (13/13, 594 gossip entries, MeshRelay ENABLED)
- 15-repo cascade absorbed, 7 targeted depot binaries replaced
- 13/13 services active, 166 capabilities (skunkBat registration expanded 5→31)
- 2 gossip peers (westGate + eastGate), 594 entries ingested (up from 1)
- MeshRelay ENABLED, southGate TCP newly reachable
- songBird `--node-id`: mesh.status already reports correct node_id from GATE_ID env var
- TCP 7800 unreachable: sporeGate, strandGate, graftGate
- **0/0/0**

### southGate (canary) — 4 BUGS FOUND (13/14, toadstool crashed)
- 14/14 depot pull fresh, 13/14 running after redeploy
- **toadstool CRASHED** — wgpu 28 backend panic on musl (P1)
- Process leak FIXED (256 skunkBat forks → 0)
- songBird `node_id: southGate` correct (hostname fix persists)
- Gossip: 3 peers outbound, **inbound BLOCKED** by riboCipher framing (P2)
- swarmVine→songBird relay method mismatch (P2)
- bearDog throughput -19% (cold start, not regression), multi-socket latency improved -9%

### westGate — CLEAN (14/14, Nest 6/6, 1170 gossip)
- 14/14 services active, Nest Atomic 6/6 domains healthy
- 5 gossip peers, 1170 ingested, provenance pipeline confirmed
- CAS federation designed, awaiting songBird `content.locate`
- native_braid.py → Rust replacement path documented

### primalSpring — CLEAN (config updated, 1,282 tests)
- Ownership rationalization absorbed into biome config + deployment matrix
- Lifecycle: 8 verified, 2 gossip registered, 3 deployed, 1 not deployed (songbird socket)
- Hostname fix documented — `sudo hostnamectl set-hostname eastgate` + NUCLEUS restart

### graftGate — FULL NUCLEUS via biomeOS Neural API (21 ACTIVE domains)
- `biomeos nucleus start --mode full` bootstrapped 12 primals in <60s
- **1830 capabilities**, 21 ACTIVE domains, 36 UDS sockets in `/tmp/eco/membrane/`
- 7 LAN peers, WireGuard live at `10.13.37.13`
- **10 divergences documented** (D1-D10): macOS SUN_LEN socket limit, barracuda binary name mismatch, codesign keychain, WWDR certs, songBird↔bearDog security provider, biomeOS security resurrection loop, PATH in screen sessions, Apple Dev enrollment delay, iOS Developer Mode, songBird toolchain target
- Depot refreshed: 15 darwin binaries on golgiBody (104M)
- sourDough v0.4.0, service template shipped, 0/0/0

### iosGate — FIRST DEPLOY (BearDogApp on iPhone XS)
- **6th OS family proven** (Linux + Windows + Android + macOS + iOS + SteamOS-planned)
- BearDogApp (PID 557) + iosGate mesh discovery (PID 603) running on iPhone XS
- WiFi LAN peer discovery: probes 7 gate IPs, no USB tether required
- 4 iOS Rust binaries built: beardog 6.3M, songbird 17M, skunkbat 2.6M, swarmvine 2.1M
- Signed: `Apple Development: eco.primal@pm.me (4DMC3GXQ65)`, free provisioning (7-day expiry)

### songBird — DEEP-DEBT SWEEP (`5bc2d3988`)
- **148 files changed, +6,962 / -5,198 lines** (net -1,236 lines)
- **Blocker #3 RESOLVED**: `--node-id` / `--gate-id` CLI flag with env overlay
- **P2 #3 RESOLVED**: `mesh.*` aliases to `gossip.*` — relay forwarding restored
- `content.locate` **FUNCTIONAL** — CAS federation relay for westGate. Local scope operational.
- `identity.get` L2 complete (primal/version/domain/license/methods envelope)
- 10 legacy snake_case methods → canonical `domain.verb` wire names
- 5 monoliths → 25+ submodules, 14 dead deps removed
- 8,500+ tests, zero clippy warnings

### swarmVine — EVOLUTION AAR (186 tests, 90.8% coverage)
- **P2 #2 RESOLVED**: accepts any ASCII-printable first byte as legacy JSON-RPC. Bidirectional gossip during rolling deploys.
- **P2 #3 RESOLVED**: `relay_via_songbird()` now calls `gossip.relay`
- Zero-copy `Arc<str>` for GossipEntry (key + origin_gate)
- G65 protocol negotiation now DEFAULT (no `--negotiate` flag)
- 143 → 186 tests (+43), 6 integration tests, 3 benchmarks
- Coverage: 80.9% → 90.8% line, 92.1% function
- scyBorg triple license on all 25 source files

---

## DEPLOYMENT EVOLUTION — biomeOS Neural API

**Direction**: Deploy via biomeOS `composition.orchestrate` (deploy→gossip→verify pipeline) instead of manual depot pull.

**PROOF**: graftGate achieved FULL NUCLEUS via `biomeos nucleus start --mode full` — 12 primals orchestrated in <60s, 1830 capabilities, 21 ACTIVE domains. This validates biomeOS Neural API as the composition authority.

Atomic progression:

1. **Tower Atomic** (bearDog + songBird + skunkBat) — trust boundary. LIVE on graftGate, southGate, westGate, ironGate.
2. **Nest Atomic** (Tower + provenance trio + nestGate) — storage/data. LIVE on westGate.
3. **Node Atomic** (Nest + compute trio + biomeOS) — compute substrate. On strandGate + ironGate.
4. **Full NUCLEUS** (all 13+) — complete sovereignty. **PROVEN on graftGate via biomeOS.** eastGate, ironGate, southGate also full.

biomeOS Neural API will evolve to interact with cellMembrane (sovereignty boundary) and sporeGate topology (mesh enrollment/cascade) as the composition graph develops.

**Gossip nervous system**: swarmVine `cascade.notify` + `endpoint.alive` tell biomeOS what's running where. riboCipher backward compat now RESOLVED — gossip is bidirectional during rolling deploys.

**Depot refresh needed**: songBird (`5bc2d3988`) and swarmVine (pending push) have new binaries with P2 fixes. Fleet should pull after depot rebuild.

---

## SOLO ENABLERS

- **sporeGate**: NanoWire Tier 2 retirement → autonomous cascade
- **westGate**: CAS federation — songBird `content.locate` now FUNCTIONAL (local scope). Nest Atomic 139 translations. native_braid.py → Rust (145/s → 16K/s)
- **strandGate**: arXiv Rung 1 campaign (22/45), pseudoSpore pipeline

---

## CONVERGENCE RULE

> **Forgejo is canonical. Gates pull, validate, report.**
> 1. Gate teams pull and redeploy.
> 2. Code teams fix their own primals.
> 3. Overwatch coordinates via this ecosystem blurb.

---

*Wave 157k — POST-PANDEMIC EVOLUTION. iosGate FIRST DEPLOY (BearDogApp on iPhone XS — 6th OS family). graftGate FULL NUCLEUS via biomeOS Neural API (21 ACTIVE domains, 1830 capabilities, <60s). songBird deep-debt: 148 files, -1,236 lines, content.locate FUNCTIONAL, --node-id RESOLVED. swarmVine: P2 riboCipher + relay RESOLVED, 90.8% coverage. biomeOS: P2 spawn leak RESOLVED (6df4220e). toadStool: P1 wgpu28 RESOLVED in source (depot rebuild needed). All 4 canary bugs RESOLVED. 11 gates online (biomeGate DOWN). Depot refresh needed (songBird + swarmVine + toadStool + biomeOS). 0/0/0.*
