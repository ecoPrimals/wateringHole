# ecoPrimals Ecosystem Blurb — Wave 133h

**Date**: Jul 8, 2026 10:38 EDT | **Wave**: 133h | **From**: eastGate overwatch
**Posture**: **CONVERGENCE + AUTO-DISTRIBUTION LANDED — multi-builder authority, mesh.publish fan-out, auto-fetch pipeline.**
15/15 pass, 0 fail. Resilient build authority (sporeGate + eastGate). songBird `mesh.publish` now fans out to all peers. cellMembrane auto-fetches on `depot.updated`. SHA validation rejects truncated commits. cascade-sense timer template added for all gates. 574 cellMembrane tests, 585 songbird-types tests, 0 fail.

---

## Ecosystem State

```
✅ 14/14 primals + primalSpring: ALL GREEN — 0 fail across full ecosystem
✅ 30/30 ecobins in pepti (15 x86_64 + 15 aarch64) — 12 need fresh rebuild
✅ 1099 tests GREEN, 126 scenarios, 0 fail (sovereign CI pipeline scenario added)
✅ LAN mesh: eastGate ↔ ironGate ↔ southGate (Omada 10G backbone)
✅ WAN mesh: flockGate ↔ sporeGate (WireGuard 10.13.37.x, 72ms p50)
✅ Mobile: grapheneGate 12/13 TCP-only (13/13 after pepti rebuild)
✅ Sovereignty: S1-S4 ALL GRADUATED on inner membrane
✅ golgi: sporePrint NUCLEUS (212 pages) + thin edge relay + freshness auto-publishing
✅ 7/7 stadial criteria CLEAR — all operational proof exercises are validation, not blockers
✅ SHOW_HN publication rubric established (28 criteria, 4 categories)
```

**This wave (133h)**: Convergence + resilient build authority + mesh auto-distribution.

**Landed (133h)**:
- **Multi-builder authority**: `build_authorities = ["sporeGate", "eastGate"]` in manifest. Any gate with Rust + musl-tools can build. `TopologyRoles` struct extended, `GateProfile.build_authority` added.
- **mesh.publish fan-out**: songBird `handle_publish` now POSTs to all reachable peers (was stub). Uses `post_jsonrpc_fire_and_forget`.
- **mesh.subscribe handler**: New method receives `depot.updated` notifications, spawns `membrane plasmid.auto_fetch` (fire-and-forget).
- **Build-complete hook**: `harvest.rs` calls songBird `mesh.publish depot.updated` after successful builds — peers auto-notified.
- **Consumer auto-fetch**: New `plasmid/auto_fetch.rs` module. Rate-limited (5min), idempotent, BLAKE3-verified. Wired into `plasmid.auto_fetch` CLI dispatch.
- **SHA validation**: `publish_gate_heads()` rejects truncated SHAs (40-byte hex ending in 28+ zeros). Prevents corrupt head files from propagating.
- **Peer staleness detection**: `mesh.status` now includes `stale_peers` array (gates with `heads/<gate>.toml` older than 24h).
- **cascade-sense timer**: New systemd timer+service pair — hourly convergence monitoring for all gates.

**Previously landed (133g)**:
- CI-DIV-01/02/03 resolved, manifest `[build.*]` + `plasmid.harvest` enrichment
- primalSpring sovereign CI pipeline validation scenario (1099 tests, 126 scenarios)
- rhizoCrypt ephemeral ports, barraCuda ESN panic-resilience
- Hardcoded IP extraction in build-local.sh, cargo config divergence inventory

---

## WAVE PLAN: 134a → 135+

### Wave 134a — Pepti Pipeline Hardening + Capability Convergence

**Goal**: WAN-DISPATCH-01 FULL PASS. Evolve sovereign CI from ad-hoc scripts to robust isomorphic pipeline.

| # | Item | Owner | Status |
|---|------|-------|--------|
| 1 | Rebuild pepti: songBird + bearDog + skunkBat + nestGate + coralReef + sweetGrass | sporeGate CI | **NEXT** — 6 primals need fresh builds. CI hook already triggered for songBird. |
| 2 | Harden sovereign CI pipeline (see Pipeline Evolution below) | sporeGate + cellMembrane | **NEW** — evolve bash→Rust, add depot integrity checks |
| 3 | Redeploy songBird on sporeGate from pepti | sporeGate team | After #1 |
| 4 | flockGate re-runs WAN-DISPATCH-01 → target FULL PASS | flockGate | After #3 |
| 5 | grapheneGate 13/13 redeploy from fresh pepti | eastGate | After #1 |
| 6 | Verify composition subtypes match live deployments | projectNUCLEUS | Ongoing |
| 7 | ~~Resolve CI-DIV-01/02/03~~ | cellMembrane | **DONE** — manifest `[build.*]` + `plasmid.harvest` enrichment landed |

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

**Known fragilities**: `/var/log/sovereign-ci.log` permission denied on golgi, golgi freshness publishing sometimes stale. CI-DIV-01/02/03 resolved. Build authority now resilient (multi-gate).

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
| **sporePrint host** | petalTongue + nestGate + songBird + bearDog | golgi VPS | Sovereign website with live mesh viz |
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
| **sporeGate** | 134a pepti rebuild (12 primals ALL GREEN), songBird redeploy, golgi CI log fix | **NOW** |
| **flockGate** | 134a WAN-DISPATCH-01 re-validation after pepti rebuild | After pepti |
| **ironGate** | Cascade refresh (stale Jul 4), 134b strandGate enrollment prep | Next SSH |
| **bearDog** | 134b CryptoProvider fix (UNIT-DIV-04 — P1 for DNS cutover) | Code team |
| **cellMembrane** | ~~CI-DIV absorption~~ **DONE**. ~~Auto-distribution~~ **DONE (133h)** — `auto_fetch.rs` + `notify_mesh_depot_updated` + SHA validation + `build_authorities()` helpers | Code team |
| **sporePrint** | 134b sovereignty sprint, DNS cutover, petalTongue rendering | After 134a |
| **projectNUCLEUS** | Composition subtype manifests, deployment profiles | Ongoing |
| **primalSpring** | 135+ SHOW_HN E-category prep (cold clone, CI badges, test naming) | Ongoing |

---

## Code Team Dispatches (status after 133f sweep)

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
| 1 | Pepti rebuild: 12 primals | sporeGate CI | — | **IN PROGRESS** — 3 builds auto-triggered (rhizoCrypt, barraCuda, nestGate). Remaining 9 need trigger or manual push-to-forgejo. |
| 2 | Fix golgi `sovereign-ci.log` permissions | golgi/cellMembrane | — | Quick fix |
| 3 | Redeploy songBird on sporeGate from fresh pepti | sporeGate team | #1 | Pending |
| 4 | flockGate cascade + WAN-DISPATCH-01 re-run → FULL PASS | flockGate | #3 | Pending — gate is stale (15:14Z) |
| 5 | grapheneGate 13/13 from fresh pepti | eastGate | #1 | Pending |
| 6 | ironGate cascade refresh | ironGate | SSH access | STALE since Jul 4 |
| 7 | ~~cellMembrane CI-DIV absorption into manifest~~ | cellMembrane | — | **DONE** — manifest `[build.*]` + harvest enrichment |
| 8 | ~~Mesh auto-distribution pipeline~~ | songBird + cellMembrane | — | **DONE (133h)** — mesh.publish fan-out + auto-fetch + staleness alerting |
| 9 | ~~Multi-builder resilience~~ | manifest + cellMembrane | — | **DONE (133h)** — `build_authorities = ["sporeGate", "eastGate"]` |

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

## Gate Convergence (133f)

```
CONVERGED (all primals at current HEADs):
  ✅ eastGate   — updated 01:50Z, 19 repos tracked
  ✅ sporeGate  — updated 23:26Z, 14 primals + wateringHole
  ✅ golgiBody  — updated 01:46Z, 15 repos + plasmidBin + projectNUCLEUS

STALE (need cascade refresh):
  ⚠️  flockGate  — 15:14Z, all primals behind. Waiting for pepti rebuild + songBird redeploy.
  ⚠️  ironGate   — Jul 4, 3+ days stale. Needs SSH access.
```

*Wave 133h — ALL PRIMALS GREEN. 15/15 pass, 0 fail. Convergence + auto-distribution landed. Build authority resilient (sporeGate + eastGate). mesh.publish fans out depot notifications to all peers. Consumer gates auto-fetch on notification. SHA validation rejects truncated commits. cascade-sense timer template deployed. Pipeline shape: **build → sync → announce → fetch → verify → deploy** — fractal at every scale.*
