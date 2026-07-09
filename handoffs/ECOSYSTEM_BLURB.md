# ecoPrimals Ecosystem Blurb — Wave 134e

**Date**: Jul 9, 2026 11:10 EDT | **Wave**: 134e | **From**: eastGate overwatch
**Posture**: **CONVERGING — UNIT-DIV-04 RESOLVED (bearDog team confirmed). DNS cutover unblocked. Composition-scoped lifecycle in cellMembrane. Pepti rebuilds remain.**

---

## Current State

```
✅ 14/14 primals pass cargo check --all-targets (zero BUILD-DIV)
✅ E2E: primals.eco → 200 (golgi VPS-thin)
✅ Composition profiles: full, thin-relay, tower, compute, nest (manifest + code)
✅ Composition-scoped lifecycle: health, fetch, bootstrap, refresh, restart (cellMembrane 1be2b7f)
✅ Sovereign CI pipeline: plasmid.harvest → mesh.publish → auto_fetch (LIVE)
✅ Multi-builder authority: sporeGate + eastGate
✅ Pre-push gates: songBird + bearDog (.githooks/pre-push)
✅ UNIT-DIV-04 RESOLVED (bearDog team: CryptoProvider idempotent since 132f)
✅ bearDog gateway bind regression fixed (80c322d — error surfacing restored)
✅ 7/7 stadial criteria CLEAR
✅ WAN mesh: sporeGate ↔ flockGate (WireGuard, 72ms p50)
✅ LAN mesh: eastGate ↔ ironGate ↔ southGate (10G backbone)
⚠️  Pepti depot: ~9 primals still need rebuild on sporeGate
⚠️  ironGate: 5+ days stale (needs SSH)
⚠️  cellMembrane Forgejo bare repo: unpacker error (shallow broke on rebase)
```

---

## Remaining Work — Focused

### 1. Pepti Rebuilds (sporeGate CI)

~9 primals need rebuild from current HEADs. songBird, nestGate, membrane already deployed.

```
DONE:    songBird · nestGate · membrane · bearDog (pushed)
NEXT:    skunkBat · coralReef · sweetGrass · biomeOS · toadStool
         squirrel · petalTongue · loamSpine · rhizoCrypt · barraCuda
```

**Command**: `membrane plasmid.harvest --all` on sporeGate
**Unblocks**: flockGate WAN-DISPATCH-01, grapheneGate 13/13 redeploy

### 2. DNS Cutover — primals.eco → bearDog ACME TLS

UNIT-DIV-04 **RESOLVED** (bearDog team confirmed: idempotent `install_default()` since Wave 132f, self-healing fallback in `assert_installed()`). DNS cutover is unblocked once pepti delivers a current bearDog ecobin to golgi.
**Path**: pepti rebuild bearDog → deploy to golgi → 7-day Caddy shadow → DNS flip
**Unblocks**: sporePrint sovereignty (S-10)

### 3. cellMembrane Forgejo Bare Repo (golgi operator)

Push rejected with `unresolved deltas` — shallow depth=1 bare repo broke after rebase.
**Fix**: On golgi, delete and recreate with `git clone --mirror` from origin.
**Origin (GitHub)** is current at `1be2b7f` (composition-scoped lifecycle).

### 4. ironGate Cascade (SSH operator)

5+ days stale (since Jul 4). Needs SSH access for cascade refresh. Also: strandGate enrollment prep (physical access, house 2).

### 5. flockGate WAN Validation (after pepti)

Drawbridge connection refused (waiting for sporeGate pepti redeploy). songBird HEAD shows truncated-zero SHA (shallow clone, needs deep fetch). WAN-DISPATCH-01 re-run once pepti is complete.

### 6. golgi Sovereign-CI Log Fix

`/var/log/sovereign-ci.log` permission denied. Quick `chown` or `logrotate.d` entry.

---

## Wave Plan

### 134a — Pepti + Capability Convergence (current)

| Item | Status |
|------|--------|
| Rebuild remaining ~9 pepti primals | **NEXT** |
| flockGate WAN-DISPATCH-01 FULL PASS | After pepti |
| grapheneGate 13/13 from fresh pepti | After pepti |
| golgi sovereign-ci.log permissions | Quick fix |

### 134b — Sovereignty Sprint

| Item | Status |
|------|--------|
| ~~bearDog CryptoProvider fix (UNIT-DIV-04)~~ | **RESOLVED** (132f) |
| DNS cutover: primals.eco → bearDog ACME TLS | **UNBLOCKED** — after pepti |
| sporePrint: Caddy → bearDog TLS (7-day shadow) | After DNS cutover |
| strandGate SSH enrollment | Pending hardware access |

### 135+ — SHOW_HN Readiness

All 28 rubric criteria targeting PASS. Key linkages:
- S-6 (pepti current) → 134a
- S-8 (cross-gate dispatch) → 134a WAN-DISPATCH-01
- S-10 (sporePrint sovereign) → 134b DNS cutover
- O-1 (karma buildup) → 3-6 month window active

---

## Team Dispatches

| Team | Work | Priority |
|------|------|----------|
| **sporeGate** | Pepti rebuilds (~9 remaining). cellMembrane Forgejo bare repo recreate. | **NOW** |
| **bearDog** | ~~UNIT-DIV-04~~ **RESOLVED**. 13,884+ tests. Gateway bind regression fixed (`80c322d`). Ready for pepti + DNS cutover. | Ready |
| **sporePrint** | 249+ pages, thesis scaffolded, SEO bridging landed. Evolving thin-relay → NUCLEUS. | Active |
| **cellMembrane** | Composition-scoped lifecycle (`1be2b7f`): health, fetch, bootstrap, refresh, restart all composition-aware. Forgejo needs golgi operator. | Active |
| **primalSpring** | Deep debt cleanup (`aa4f627`): `as` cast elimination across 15 files. 128 scenarios. | Active |
| **ironGate** | Cascade refresh (5+ days stale). strandGate enrollment. | Next SSH |
| **flockGate** | WAN-DISPATCH-01 re-validation after pepti. | After pepti |

---

## Topology

```
HARDWARE:
  House 1 (CRS310):  sporeGate · eastGate · northGate
  House 2 (SX3008F): ironGate · southGate · strandGate(pending)
  Link: 80m 10G AOC trunk

MESH:
  songBird covalent:  eastGate ↔ golgi ↔ ironGate + southGate + grapheneGate
  WireGuard WAN:      sporeGate ↔ flockGate (72ms p50)

VPS:
  golgiBody (thin-relay): relay + depot + sporePrint. Tracks wateringHole only.
  golgiBody-ext:          sporePrint mirror, TURN relay
```

---

## Composition Profiles

Defined in `ecosystem_manifest.toml [compositions]`. Query: `membrane plasmid.composition`

| Profile | Primals | Use |
|---------|---------|-----|
| **full** | All 13+ | Sovereign NUCLEUS gate |
| **thin-relay** | songBird, nestGate, membrane | Deployable anywhere — VPS, HPC, edge |
| **tower** | bearDog, songBird, skunkBat | Minimal mesh entry |
| **compute** | toadStool, barraCuda, coralReef, biomeOS | GPU/HPC |
| **nest** | nestGate, sweetGrass, rhizoCrypt | Cold storage |

sporePrint evolution: thin-relay → +squirrel → +petalTongue → +barraCuda → full NUCLEUS

---

## Gate Convergence (134e — 11:10 EDT)

```
CONVERGED:
  ✅ eastGate   — All 16 repos cascaded. cellMembrane 1be2b7f, bearDog ddabf6a, primalSpring aa4f627.
  ✅ golgiBody  — VPS-thin. sporePrint serving. E2E 200.
  ✅ sporeGate  — Pepti rebuilds in progress.

BLOCKED:
  🔄 flockGate  — WG UP. Drawbridge pending pepti redeploy.

STALE:
  ⚠️  ironGate   — Jul 4, 5+ days. Needs SSH.
```

*Pipeline: push → harvest → checksum → mesh.publish → auto_fetch → verify → deploy*
