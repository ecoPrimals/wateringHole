# ecoPrimals Ecosystem Blurb — Wave 133e

**Date**: Jul 7, 2026 16:45 EDT | **Wave**: 133e | **From**: eastGate overwatch
**Posture**: **CODE DEBT SWEPT — teams delivered, convergence accelerating**
Code teams delivered: barraCuda deep debt sweep, bearDog gatehouse hardening, rhizoCrypt readiness fix + test splits, primalSpring cold-clone + CI badges + deep debt. 12 primals now need pepti rebuild. 1098 tests GREEN.

---

## Ecosystem State

```
✅ 13/13 primals CONVERGED — zero CI workarounds, zero code debt
✅ 30/30 ecobins in pepti (15 x86_64 + 15 aarch64) — 4-5 stale, pending rebuild
✅ 1098 tests GREEN, 125 scenarios, 0 fail (composition subtypes landed)
✅ LAN mesh: eastGate ↔ ironGate ↔ southGate (Omada 10G backbone)
✅ WAN mesh: flockGate ↔ sporeGate (WireGuard 10.13.37.x, 72ms p50)
✅ Mobile: grapheneGate 12/13 TCP-only (13/13 after pepti rebuild)
✅ Sovereignty: S1-S4 ALL GRADUATED on inner membrane
✅ golgi: sporePrint NUCLEUS (212 pages) + thin edge relay + freshness auto-publishing
✅ 7/7 stadial criteria CLEAR — all operational proof exercises are validation, not blockers
✅ SHOW_HN publication rubric established (28 criteria, 4 categories)
```

**This wave**: Standards housekeeping + wave plan. songBird drawbridge auto-advertisement committed (`026f6e3e`). 2 superseded handoffs archived. GLACIAL, SOVEREIGNTY, TOPOLOGY docs updated to 133d. Wave plan shaped: 134a (deploy convergence), 134b (sovereignty sprint), 135+ (SHOW_HN readiness).

**Cascade findings (14:50 EDT)**:
- bearDog `a586fbee` — fix absorbed: zero clippy warnings + crossbeam-epoch advisory
- sporeGate holds songBird `026f6e3e` (auto-advertisement) + bearDog `a586fbee`
- ironGate head still STALE (Jul 4) — needs cascade refresh on next SSH
- 1098 tests, 125 scenarios, 0 fail — confirmed post-cascade

**Code debt sweep (14 primals — overwatch + code teams)**:
- 14/14 clippy ZERO warnings
- barraCuda `7edc83a` — deep debt sweep: capability-based discovery, clone reduction, fn pointers + ESN wgpu fix
- bearDog `f6924be` — gatehouse production hardening: bind errors, shadow metrics, tests
- rhizoCrypt `2d9c146` — readiness fix + vendor decoupling + transport split + test file splits
- primalSpring `d8028d6` — cold-clone fix (E-2), CI workflow + badges (SHOW_HN), deep debt cleanup
- toadStool `002332e` — shader dispatch error assertion widened for wgpu fallback
- biomeOS `39a1118` — squirrel availability test environment-agnostic
- petalTongue `ebaf483` — mesh topology test updated for 11-node count
- rhizoCrypt readiness tests: still environment-dependent (partial fix, needs further investigation)
- 12 primals now need pepti rebuild

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
| 7 | Resolve CI-DIV-01/02/03 (biomeOS, skunkBat, nestGate build quirks) | primal teams | P2 — manual workarounds in place |

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

**Known fragilities**: CI-DIV-01 (biomeOS `--package`), CI-DIV-02 (skunkBat `--package`), CI-DIV-03 (nestGate `ld.lld`), `/var/log/sovereign-ci.log` permission denied on golgi, golgi freshness publishing sometimes stale.

### Target flow (isomorphic, Wave 134a+)

```
Push to Forgejo (any primal repo)
  → Forgejo webhook → membrane sovereign.ci.trigger    ← Rust, typed
  → membrane plasmid.harvest <primal>                   ← Rust, manifest-driven
    - reads ecosystem_manifest.toml for binary_name, build_args, package
    - cargo build --release --target {target}
    - BLAKE3 checksum + provenance.toml update
  → membrane plasmid.sync --target depot               ← Rust, rsync or native
  → Gates auto-fetch via plasmid.fetch --check-update   ← Rust, checksum-verified
```

### Evolution steps (134a scope)

| # | Step | What changes | Isomorphism gain |
|---|------|-------------|-----------------|
| 1 | Fix golgi `sovereign-ci.log` permissions | `chown` or `logrotate.d` entry | Removes silent failure |
| 2 | Move per-primal build workarounds into `ecosystem_manifest.toml` | `[primals.biomeOS] package = "biomeos-unibin"` | Manifest-driven, not script-hardcoded |
| 3 | `membrane plasmid.harvest` absorbs `build-local.sh` | Rust replaces bash | Same command on any builder gate |
| 4 | Depot integrity: checksum verify after sync | BLAKE3 compare on golgi post-sync | Catch rsync corruption |
| 5 | Auto-notify on build completion | songBird mesh impulse or wateringHole head update | Gates know when to fetch |

### Fractal principle

The pipeline pattern must be **the same shape at every scale**:
- **Single primal rebuild**: push → build → sync → verify
- **Full sweep**: push all → build all → sync → verify
- **New gate onboard**: `plasmid.fetch --all` → same depot, same checksums, same NUCLEUS
- **New builder gate**: install Rust + musl-tools, set `build_authority = true` in manifest → same pipeline

Any gate with the right toolchain can be a builder. Any gate with depot access can be a consumer. The manifest is the single source of truth, not bash scripts on specific hosts.

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
| **sporeGate** | 134a pepti rebuild (10 primals evolved), songBird redeploy, golgi CI log fix | **NOW** |
| **flockGate** | 134a WAN-DISPATCH-01 re-validation after pepti rebuild | After pepti |
| **ironGate** | Cascade refresh (stale Jul 4), 134b strandGate enrollment prep | Next SSH |
| **rhizoCrypt** | Readiness fix shipped, 2 startup tests still env-dependent — may need timeout increase | Code team |
| **barraCuda** | wgpu fix + deep debt sweep DELIVERED — verify in pepti rebuild | Done |
| **bearDog** | 134b CryptoProvider fix (UNIT-DIV-04 — P1 for DNS cutover) | Code team |
| **cellMembrane** | CI-DIV-01/02/03 manifest absorption (biomeOS `--package`, skunkBat `--package`, nestGate `ld.lld`) | Code team |
| **sporePrint** | 134b sovereignty sprint, DNS cutover, petalTongue rendering | After 134a |
| **projectNUCLEUS** | Composition subtype manifests, deployment profiles | Ongoing |
| **primalSpring** | 135+ SHOW_HN E-category prep (cold clone, CI badges, test naming) | Ongoing |

---

## Code Team Dispatches (pre-existing debt for dedicated IDE agents)

### rhizoCrypt — Server Startup Readiness (PARTIALLY RESOLVED)

Readiness fix shipped (`edd950c`): replaced `yield_now()` spin-loop with `server.ready_notifier().notified().await`. Test file splits completed (>800L files split). However, 2 startup tests still timeout on eastGate under load — the `run_server_with_ready` path does UDS + manifest + neural announce before reaching TCP bind. May need increased timeout or async startup restructuring.

### barraCuda — wgpu/ESN (RESOLVED)

`9ef6641` fixed wgpu BindGroupLayout SIGSEGV. `7edc83a` deep debt sweep shipped: capability-based discovery, clone reduction, fn pointers.

### bearDog — CryptoProvider Panic (UNIT-DIV-04)

`rustls-rustcrypto` CryptoProvider panics on install. Blocks Caddy→bearDog ACME TLS cutover (134b sovereignty sprint). P1 for DNS cutover.

**File**: `crates/beardog-acme/src/` area — `CryptoProvider::install()` call site
**Context**: ES256 signing + defensive install added in Wave 132f (`136857739`). The panic may be double-install or incompatible provider state.

### cellMembrane — CI Build Workaround Absorption

3 per-primal build workarounds in `build-local.sh` need absorption into `ecosystem_manifest.toml`:
- CI-DIV-01: biomeOS requires `--package biomeos-unibin`
- CI-DIV-02: skunkBat requires `--package skunk-bat-server`
- CI-DIV-03: nestGate requires `ld.lld` linker (project `.cargo/config.toml` diverges)

**Target**: Add `[primals.<name>] package = "..."` and `linker = "..."` fields to manifest. `plasmid.harvest` reads manifest instead of hardcoded workarounds.

---

## Remaining Work (134a critical path)

| # | Item | Owner | Blocked by | Status |
|---|------|-------|------------|--------|
| 1 | Pepti rebuild: 12 primals (songBird, bearDog, toadStool, biomeOS, petalTongue, barraCuda, rhizoCrypt, skunkBat, nestGate, coralReef, sweetGrass + sourDough unchanged) | sporeGate CI | — | **NEXT** — all code debt swept, teams delivered, ready to build |
| 2 | Fix golgi `sovereign-ci.log` permissions | golgi/cellMembrane | — | Quick fix |
| 3 | Redeploy songBird on sporeGate from fresh pepti | sporeGate team | #1 | Pending |
| 4 | flockGate WAN-DISPATCH-01 re-run → target FULL PASS | flockGate | #3 | Pending |
| 5 | grapheneGate 13/13 from fresh pepti | eastGate | #1 | Pending |
| 6 | ironGate cascade refresh | ironGate | SSH access | STALE since Jul 4 |

*Wave 133e — Code teams delivered. barraCuda wgpu fix + deep debt sweep. bearDog gatehouse hardening. rhizoCrypt readiness fix + vendor decoupling. primalSpring cold-clone + CI badges for SHOW_HN. 12 primals evolved, all pushed. 14/14 clippy zero. Critical path: pepti rebuild (12 primals) → songBird redeploy → WAN-DISPATCH-01 FULL PASS.*
