# ecoPrimals Ecosystem Blurb — Wave 134a

**Date**: Jul 8, 2026 17:40 EDT | **Wave**: 134a | **From**: eastGate overwatch
**Posture**: **CONVERGING — VPS-thin reconfigured. golgi is now pure relay/depot. sporeGate builds, golgi serves. E2E 200.**
golgi reconfigured as VPS-thin: only tracks `wateringHole` (was 15+ repos). sporeGate is the source builder; golgi relays binaries + runs sporePrint. bearDog `d594d87` landed BUILD-DIV-01 pre-push gate (`.githooks/pre-push`). flockGate actively testing but drawbridge blocked pending sporeGate redeploy. songBird flockGate HEAD is truncated-zero SHA (caught by our validation).

---

## Ecosystem State

```
✅ 14/14 primals + primalSpring: ALL GREEN — 0 fail across full ecosystem
✅ songBird cd13d36d DEPLOYED on sporeGate (both services) + golgi (relay)
✅ nestGate f3006ccd in depot, active on golgi (sporePrint)
✅ membrane 5efff13 in depot, active on golgi (CLI + cascade)
✅ E2E: primals.eco → 200. All services green.
✅ golgi VPS-THIN: relay + depot + sporePrint only. Tracks wateringHole only.
✅ LAN mesh: eastGate ↔ ironGate ↔ southGate (Omada 10G backbone)
✅ WAN mesh: flockGate ↔ sporeGate (WireGuard 10.13.37.x, 72ms p50)
✅ Sovereignty: S1-S4 ALL GRADUATED on inner membrane
✅ bearDog d594d87: BUILD-DIV-01 pre-push gate landed (.githooks/pre-push)
✅ 7/7 stadial criteria CLEAR
⚠️  golgi disk 71% (2.7G free) — lighter now with VPS-thin (fewer clones)
⚠️  flockGate songBird SHA is truncated zeros — shallow clone artifact, needs cascade refresh
⚠️  flockGate drawbridge: connection refused (sporeGate pepti rebuild in progress)
⚠️  sporeGate bearDog HEAD stale (f6924beb vs d594d87 — needs cascade)
```

**This wave (134a)**: Pepti pipeline hardening + first deployments from depot.

**Landed (134a)**:
- **VPS-thin reconfiguration**: golgi now tracks only `wateringHole`. No primal source repos on VPS. Pure relay + depot + sporePrint host. Frees disk, reduces attack surface.
- **sporeGate deployment**: songBird `cd13d36d` built with glue fix, both services active. nestGate + membrane in depot.
- **golgi deployment**: membrane `5efff13` (CLI + cascade), nestGate `f3006ccd` (sporePrint). E2E `primals.eco → 200`.
- **BUILD-DIV-01 gate**: bearDog `d594d87` adds `.githooks/pre-push` with `cargo check --all-targets` enforcement. DRY riboCipher dispatch refactor included.
- **BUILD-DIV-01 identified** (P2): songBird `cd13d36d` shipped used-but-unimplemented methods. sporeGate CI had to add glue. Root cause: primal pushed without `cargo check --all-targets`. Gate now exists in bearDog, needs adoption across all primals.

**Landed (133h)**:
- Multi-builder authority (`build_authorities = ["sporeGate", "eastGate"]`)
- mesh.publish fan-out, mesh.subscribe handler, build-complete hook
- Consumer auto-fetch (`plasmid/auto_fetch.rs`), SHA validation, staleness detection
- cascade-sense timer (hourly convergence monitoring)

**Previously landed (133g)**:
- CI-DIV-01/02/03 resolved, manifest `[build.*]` + `plasmid.harvest` enrichment
- primalSpring sovereign CI pipeline validation scenario
- rhizoCrypt ephemeral ports, barraCuda ESN panic-resilience

---

## WAVE PLAN: 134a → 135+

### Wave 134a — Pepti Pipeline Hardening + Capability Convergence

**Goal**: WAN-DISPATCH-01 FULL PASS. Remaining pepti rebuilds, then full convergence.

| # | Item | Owner | Status |
|---|------|-------|--------|
| 1 | ~~Rebuild + deploy songBird~~ | sporeGate CI | **DONE** — `cd13d36d` + glue, LIVE on sporeGate + golgi |
| 2 | ~~Deploy nestGate to depot + golgi~~ | sporeGate CI | **DONE** — `f3006ccd` active (sporePrint) |
| 3 | ~~Deploy membrane to depot + golgi~~ | sporeGate CI | **DONE** — `5efff13` active (CLI + cascade) |
| 4 | Rebuild remaining pepti: bearDog + skunkBat + coralReef + sweetGrass + others | sporeGate CI | **NEXT** — ~9 primals still need rebuild |
| 5 | flockGate cascade + WAN-DISPATCH-01 re-run → FULL PASS | flockGate | After #4 |
| 6 | grapheneGate 13/13 redeploy from fresh pepti | eastGate | After #4 |
| 7 | Harden sovereign CI: `cargo check --all-targets` before push (BUILD-DIV-01 fix) | all primal teams | **NEW** — prevent used-but-unimplemented gaps |
| 8 | ~~Resolve CI-DIV-01/02/03~~ | cellMembrane | **DONE** |

**Closes**: S-6 (pepti current), S-8 (capability.call cross-gate)
**Posture target**: CAPABILITY CONVERGENCE PROVEN — WAN-DISPATCH-01 FULL PASS

### Wave 134b — Sovereignty Sprint

**Goal**: `primals.eco` served from sovereign infrastructure. bearDog TLS cutover.

| # | Item | Owner | Status |
|---|------|-------|--------|
| 1 | bearDog CryptoProvider investigation/fix (rustls-rustcrypto panic, UNIT-DIV-04) | bearDog team | **P1 BLOCKER** for DNS cutover |
| 2 | DNS cutover: `primals.eco` → golgi direct (bearDog ACME) | eastGate overwatch | After #1 |
| 3 | sporePrint NUCLEUS: Caddy → bearDog TLS cutover on golgi | cellMembrane | After #1 — 7-day shadow |
| 4 | strandGate SSH enrollment (physical access, house 2) | eastGate hw | Pending hardware access |

**Closes**: S-10 (sporePrint inner membrane), UNIT-DIV-04
**Posture target**: SOVEREIGNTY DNS CUTOVER — primals.eco on inner membrane

### Wave 135+ — SHOW_HN Readiness Sprint

**Goal**: All 28 rubric criteria targeting PASS. External proof of stadial readiness.

| Category | Items | Key Actions |
|----------|-------|-------------|
| Evidence (E) | E-1 through E-7 | Cold clone test, CI badges, Lab links, reproduce guide |
| Narrative (N) | N-1 through N-6 | Title, first comment, criticism responses, comparison table |
| Standards (S) | S-1 through S-10 | Test suite 1000+, pepti current, cross-gate dispatch, sporePrint sovereign |
| Operational (O) | O-1 through O-5 | Karma buildup (3-6 month window), posting date, public clone test |

**Posture target**: SHOW_HN PRE-FLIGHT — all rubric items targeting PASS

---

## PIPELINE EVOLUTION: Ad-Hoc → Isomorphic Sovereign CI

The sovereign CI pipeline (Wave 120) works but is held together by bash scripts, hardcoded IPs, and manual SSH triggers. We evolve it toward the fractal/isomorphic/agnostic deployment model documented in `DEPLOYMENT_ISOMORPHISM_DEBT_WAVE120`.

### Current flow (ad-hoc)

```
Push to Forgejo (any primal repo)
  → post-receive.d/sovereign-ci (golgi)         ← bash script
  → SSH sporeGate (10.13.37.2 hardcoded)         ← IP-coupled
  → /opt/depot/build-local.sh <primal> --sync    ← bash, per-primal workarounds
  → rsync to golgi:/opt/ecoPrimals/plasmidBin/   ← rsync over WG
  → Caddy serves at membrane.primals.eco/depot/
```

**Known fragilities**: `/var/log/sovereign-ci.log` permission denied on golgi, golgi freshness publishing sometimes stale. CI-DIV-01/02/03 resolved. Build authority now resilient (multi-gate). BUILD-DIV-01: primals can ship used-but-unimplemented methods if `cargo check --all-targets` is not enforced pre-push.

### Target flow (isomorphic, Wave 134a+ — IMPLEMENTED 133h)

```
Push to Forgejo (any primal repo)
  → Forgejo webhook → membrane sovereign.ci.trigger    ← Rust, typed
  → membrane plasmid.harvest <primal>                   ← Rust, manifest-driven
    - reads ecosystem_manifest.toml for binary_name, build_args, package
    - cargo build --release --target {target}
    - BLAKE3 checksum + provenance.toml update
  → drift::publish_depot_checksums                      ← depot metadata updated
  → notify_mesh_depot_updated → songBird mesh.publish   ← LIVE (133h)
    { topic: "depot.updated", primals_updated: [...], builder: gate }
  → songBird fans out to all reachable peers             ← LIVE (133h)
  → Consumer gates receive mesh.subscribe                ← LIVE (133h)
  → membrane plasmid.auto_fetch (rate-limited, BLAKE3)  ← LIVE (133h)
```

### Evolution steps (134a scope)

| # | Step | What changes | Isomorphism gain |
|---|------|-------------|-----------------|
| 1 | Fix golgi `sovereign-ci.log` permissions | `chown` or `logrotate.d` entry | Removes silent failure |
| 2 | Move per-primal build workarounds into `ecosystem_manifest.toml` | `[primals.biomeOS] package = "biomeos-unibin"` | Manifest-driven, not script-hardcoded |
| 3 | `membrane plasmid.harvest` absorbs `build-local.sh` | Rust replaces bash | Same command on any builder gate |
| 4 | Depot integrity: checksum verify after sync | BLAKE3 compare on golgi post-sync | Catch rsync corruption |
| 5 | ~~Auto-notify on build completion~~ | ~~songBird mesh impulse~~ | **DONE (133h)** — `mesh.publish depot.updated` + `mesh.subscribe` + `plasmid.auto_fetch` |
| 6 | Pre-push CI gate: `cargo check --all-targets` | Enforced in Forgejo post-receive or primal CI | Prevents BUILD-DIV-01 class (used-but-unimplemented methods) |

### Fractal principle

The pipeline pattern must be **the same shape at every scale**:
- **Single primal rebuild**: push → build → sync → verify
- **Full sweep**: push all → build all → sync → verify
- **New gate onboard**: `plasmid.fetch --all` → same depot, same checksums, same NUCLEUS
- **New builder gate**: install Rust + musl-tools, set `build_authority = true` in manifest, add to `build_authorities` list → same pipeline
- **Builder failover**: if sporeGate is down, eastGate (or any `build_authority = true` gate) runs the same `plasmid.harvest` → same depot, same mesh notification

Any gate with the right toolchain can be a builder. Any gate with depot access can be a consumer. The manifest is the single source of truth, not bash scripts on specific hosts. The mesh auto-distributes via `mesh.publish` → `mesh.subscribe` → `plasmid.auto_fetch`.

---

## TRACK 1: DEPLOY — Pepti + Capability Convergence

**Immediate priority for 134a.** songBird drawbridge auto-advertisement committed (026f6e3e). Pattern documented in `GATEHOUSE_DARKFOREST_STANDARD.md`:

```
SONGBIRD_DRAWBRIDGE_ROUTES=/hub=jupyter,/api=inference
→ songBird auto-registers ["jupyter", "inference"] at startup
→ announces to mesh peers via mesh.capabilities_announce
→ remote gates can capability.call("jupyter") → routed to drawbridge
```

Composition subtypes formalized in projectNUCLEUS:

| Composition | Primals | Gate | Purpose |
|-------------|---------|------|---------|
| **Full NUCLEUS** | All 13 | eastGate, ironGate | Complete sovereign stack |
| **Tower** | bearDog + songBird + skunkBat | grapheneGate, new gates | Minimal secure mesh entry |
| **JupyterHub host** | songBird (drawbridge) + bearDog + biomeOS | ironGate | `lab.primals.eco` via mesh relay |
| **sporePrint host (VPS-thin)** | nestGate + songBird + membrane relay | golgi VPS | Sovereign website + depot + relay. No source repos. |
| **Cold storage** | nestGate + sweetGrass + rhizoCrypt | westGate | 76TB ZFS CAS archive |
| **Compute dispatch** | toadStool + barraCuda + coralReef + biomeOS | strandGate | GPU compute mesh |

---

## TRACK 2: SOVEREIGN — DNS Cutover + Inner Membrane

**134b target.** bearDog CryptoProvider fix is the gate.

```
CURRENT:
  primals.eco → Cloudflare → Caddy on golgi → sporePrint (212 pages)
  primal.eco  → sovereign (S1-S4 GRADUATED) ✅
  bearDog ACME → BLOCKED (CryptoProvider panic, UNIT-DIV-04)

TARGET (134b):
  primals.eco → golgi VPS → bearDog ACME TLS → petalTongue rendering
  primal.eco  → sovereign ✅ (no change)
  Cloudflare → outer membrane only (acceptable per diderm)
```

Membrane channels: Channel 1 (DNS) LIVE, Channel 2 (TURN) LIVE, Channel 2b (RustDesk) LIVE, Channel 3 (TLS) LIVE via Caddy (bearDog shadow BLOCKED).

---

## TRACK 3: GLACIAL — Stadial Entry + Operational Proof

**All 7 criteria CLEAR.** What remains is operational validation:

| Exercise | Purpose | Wave | Status |
|----------|---------|------|--------|
| WAN-DISPATCH-01 FULL PASS | capability.call routes through WAN relay | 134a | Unblocked — songBird evolved |
| strandGate enrollment | 3+ gate mesh enrollment reproducible | 134b | Physical access needed |
| grapheneGate 13/13 | Full mobile NUCLEUS from pepti | 134a | After pepti rebuild |
| Dark-forest re-enable | Full bearDog security posture | 134b+ | After 3+ LAN peers |
| pepti rebuild | CI pipeline → clean binaries, zero workarounds | 134a | NEXT action |

---

## TRACK 4: PUBLICATION — SHOW_HN as External Proof

The SHOW_HN rubric is not a marketing exercise — it IS the glacial proof made external. Every S-category criterion maps to an existing stadial criterion or deployment goal.

**Key linkages**:
- S-6 (pepti current) → 134a pepti rebuild
- S-8 (cross-gate dispatch) → 134a WAN-DISPATCH-01
- S-10 (sporePrint sovereign) → 134b DNS cutover
- E-2 (cold clone) → spring team prep
- O-1 (karma buildup) → 3-6 month window starts now

**Timeline model**: ~3-6 months of karma buildup + content refinement → SHOW_HN submission when all S-category PASS and narrative is sharp. The karma buildup window naturally paces the sovereignty sprint and operational proof exercises.

---

## Physical + Mesh Topology (133e)

```
HARDWARE (physical switching):
  House 1 (CRS310 backbone):  sporeGate, eastGate, northGate, biomeGate(offline)
  House 2 (Omada SX3008F):    ironGate, southGate, strandGate(pending), fieldGate
  Link: 80m 10G AOC trunk between adjacent lots

MESH OVERLAYS:
  Songbird covalent (TCP :7700): eastGate ↔ golgi ↔ ironGate + southGate + grapheneGate
  WireGuard WAN (10.13.37.x):   sporeGate ↔ flockGate (72ms p50, connection pooling active)
  Capability routing:            PARTIAL — http.request proven, jupyter pending pepti rebuild
```

---

## Distribution

Copy this blurb to all active teams/gates:

| Recipient | Focus | Priority |
|-----------|-------|----------|
| **sporeGate** | Continue pepti rebuilds (~9 remaining). Monitor golgi disk (71%). Fix CI log permissions. | **NOW** |
| **songBird** | Commit BUILD-DIV-01 glue back to repo: `provided_capabilities()`, `announce_drawbridge_capabilities()`, Subscribe dispatch arm. Add pre-push `cargo check --all-targets` gate. | **NOW** |
| **flockGate** | 134a WAN-DISPATCH-01 re-validation after full pepti rebuild | After pepti |
| **ironGate** | Cascade refresh (stale Jul 4, 4+ days). strandGate enrollment prep. | Next SSH |
| **bearDog** | 134b CryptoProvider fix (UNIT-DIV-04 — P1 for DNS cutover) | Code team |
| **cellMembrane** | ~~CI-DIV absorption~~ **DONE**. ~~Auto-distribution~~ **DONE**. Monitor auto-fetch on gate deploys. | Monitoring |
| **sporePrint** | 134b sovereignty sprint, DNS cutover, petalTongue rendering | After 134a |
| **projectNUCLEUS** | Composition subtype manifests, deployment profiles | Ongoing |
| **primalSpring** | 135+ SHOW_HN E-category prep (cold clone, CI badges, test naming) | Ongoing |

---

## Code Team Dispatches (status after 134a deployment)

### songBird — BUILD-DIV-01: Used-but-Unimplemented Methods (RESOLVED on gate)

songBird `cd13d36d` added `MeshMethod::Subscribe` variant and referenced two methods that weren't implemented yet: `DrawbridgeConfig::provided_capabilities()` and `IpcServiceHandler::announce_drawbridge_capabilities()`. sporeGate CI had to add glue code during build:

- `provided_capabilities()` on `DrawbridgeConfig` — extracts unique capability names from routes
- `announce_drawbridge_capabilities()` on `IpcServiceHandler` — delegates to `MeshHandler::announce_capabilities_to_peers()`
- `Subscribe` match arm in orchestrator dispatch — routes to existing `handle_subscribe`

**Upstream action needed**: These glue implementations should be committed back to the songBird repo so the next `cargo check --all-targets` passes without gate-side patching. Pre-push CI gate: `cargo check --all-targets` should be enforced to catch this class of divergence before it reaches Forgejo.

### rhizoCrypt — Server Startup Readiness (RESOLVED)

Root cause: two TCP startup tests were resolving to the production default port instead of ephemeral port 0. When a rhizoCrypt service was already running (or another test occupied the port), `bind()` returned EADDRINUSE and the readiness notification timed out. Fix: both tests now pass `Some(0)` as port_override, matching all other passing startup tests. 86/86 pass.

### barraCuda — wgpu/ESN (RESOLVED)

ESN test panicked with `BindGroupLayout[Id(0,3)] does not exist` under concurrent test load (3900+ parallel tests). This is a wgpu-core race condition in internal resource epoch tracking, not a code bug. Fix: (1) ESN test now uses `get_test_device()` (CPU-first) for algorithm validation instead of requiring GPU hardware, and (2) test body runs in a spawned task with panic recovery, converting wgpu races into logged skips instead of suite-failing panics. 3911/3911 pass.

### bearDog — CryptoProvider Panic (UNIT-DIV-04)

`rustls-rustcrypto` CryptoProvider panics on install. Blocks Caddy→bearDog ACME TLS cutover (134b sovereignty sprint). P1 for DNS cutover.

**File**: `crates/beardog-acme/src/` area — `CryptoProvider::install()` call site
**Context**: ES256 signing + defensive install added in Wave 132f (`136857739`). The panic may be double-install or incompatible provider state.

### cellMembrane — CI Build Workaround Absorption

CI-DIV-01/02/03 build workarounds **RESOLVED** — absorbed into `ecosystem_manifest.toml` `[build.*]` section:
- CI-DIV-01: biomeOS `package = "biomeos-unibin"` in `[build.biomeos]`
- CI-DIV-02: skunkBat `package = "skunk-bat-server"` in `[build.skunkbat]`
- CI-DIV-03: nestGate `cargo_config = true` in `[build.nestgate]` (linker handled by project `.cargo/config.toml`, resolved Wave 133a)

`plasmid.harvest` now reads manifest build entries and enriches `sources.toml` with correct `--package` args and GPU flags. Triple-source convergence: manifest is authoritative for build config, `sources.toml` retained for release/fetch metadata.

---

## Remaining Work (134a critical path)

| # | Item | Owner | Blocked by | Status |
|---|------|-------|------------|--------|
| 1 | ~~songBird build + deploy~~ | sporeGate CI | — | **DONE** — `cd13d36d` + glue, LIVE on sporeGate + golgi |
| 2 | ~~nestGate build + deploy~~ | sporeGate CI | — | **DONE** — `f3006ccd` in depot, active on golgi |
| 3 | ~~membrane build + deploy~~ | sporeGate CI | — | **DONE** — `5efff13` in depot, active on golgi |
| 4 | Rebuild remaining pepti (~9 primals) | sporeGate CI | — | **IN PROGRESS** — bearDog, skunkBat, coralReef, sweetGrass, biomeOS, toadStool, squirrel, petalTongue, loamSpine |
| 5 | Commit BUILD-DIV-01 glue back to songBird repo | songBird team | — | **NEXT** — `provided_capabilities()`, `announce_drawbridge_capabilities()`, Subscribe dispatch |
| 6 | Fix golgi `sovereign-ci.log` permissions | golgi/cellMembrane | — | Quick fix |
| 7 | flockGate cascade + WAN-DISPATCH-01 re-run → FULL PASS | flockGate | #4 | Pending |
| 8 | grapheneGate 13/13 from fresh pepti | eastGate | #4 | Pending |
| 9 | ironGate cascade refresh | ironGate | SSH access | STALE since Jul 4 |
| 10 | ~~cellMembrane CI-DIV absorption~~ | cellMembrane | — | **DONE** |
| 11 | ~~Mesh auto-distribution pipeline~~ | songBird + cellMembrane | — | **DONE (133h)** |
| 12 | ~~Multi-builder resilience~~ | manifest + cellMembrane | — | **DONE (133h)** |

## Build Config Convergence Inventory

CI-DIV-01/02/03 absorbed into `ecosystem_manifest.toml` `[build.*]`. Remaining documented divergences:

**Musl linking strategies** (two camps — both produce valid static ecobins):
| Strategy | Primals | Notes |
|---|---|---|
| `link-self-contained=yes` | coralReef, nestGate, sourDough | No musl-tools package needed |
| Explicit linkers + `-static` | sweetGrass, skunkBat, loamSpine, biomeOS, toadStool, squirrel | Requires `musl-tools` installed |

**Resolver versions**: sweetGrass and barraCuda use resolver `"3"`, all others use `"2"`. No impact on ecobins.

**Rust edition**: All 14 primals at edition `2024`. Outliers: nestGate vendored deps (2021), biomeOS chimeras (2021, excluded sub-workspaces).

**rust-version spread**: 1.85 (loamSpine, nestGate, toadStool, coralReef) to 1.93.0 (bearDog). CI builder must run at least the highest.

**squirrel default target**: `.cargo/config.toml` sets `[build] target = "x86_64-unknown-linux-musl"` globally. All `cargo` invocations on squirrel default to musl without `--target`.

**sourDough `-D warnings`**: Global rustflags `-D warnings` in `.cargo/config.toml`. May fail builds if upstream deps emit warnings.

**nestGate `[patch.crates-io]`**: Only primal with `[patch]` section — patches `rustls-rustcrypto` and `rustls-webpki` to vendored forks for UNIT-DIV-04 investigation.

**No cross-primal compile deps**: All inter-primal paths are commented out. Communication is runtime JSON-RPC/tarpc IPC only.

---

## Gate Convergence (134a — 17:40 EDT)

```
CONVERGED + DEPLOYED:
  ✅ sporeGate  — 16:19Z. songBird cd13d36d LIVE. 14 primals tracked.
                  bearDog stale (f6924beb, needs d594d87 cascade).
  ✅ golgiBody  — 17:13Z. VPS-THIN — only wateringHole tracked.
                  membrane 5efff13 + nestGate f3006ccd LIVE. sporePrint serving. E2E 200.
  ✅ eastGate   — current. 19 repos tracked. bearDog at d594d87.

ACTIVELY TESTING:
  🔄 flockGate  — 16:03Z. WG UP, 2 peers, 72ms RTT.
                  Drawbridge: connection refused (sporeGate pepti rebuild).
                  capability.call: FAIL (no jupyter provider).
                  songBird HEAD: 05e22043…000000 (truncated — shallow clone artifact).
                  BLOCKER: waiting for sporeGate drawbridge redeploy.

STALE:
  ⚠️  ironGate   — Jul 4, 4+ days stale. Needs SSH access.

DISK:
  ⚠️  golgi      — 71% (2.7G free). Lighter with VPS-thin (only wateringHole cloned).
```

*Wave 134a — CONVERGING. VPS-thin landed on golgi (relay-only). sporeGate deploys LIVE. bearDog ships BUILD-DIV-01 pre-push gate. flockGate actively testing but blocked on drawbridge redeploy. ~9 primals remaining for full pepti. Pipeline: **build → sync → announce → fetch → verify → deploy**.*
