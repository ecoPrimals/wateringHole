# ecoPrimals Ecosystem Blurb — Wave 134d

**Date**: Jul 9, 2026 09:45 EDT | **Wave**: 134d | **From**: eastGate overwatch
**Posture**: **CONVERGING — 14/14 primals clean. Composition profiles formalized. Pepti rebuilds and sovereignty sprint are the remaining gates.**

---

## Current State

```
✅ 14/14 primals pass cargo check --all-targets (zero BUILD-DIV)
✅ E2E: primals.eco → 200 (golgi VPS-thin)
✅ Composition profiles: full, thin-relay, tower, compute, nest (manifest + code)
✅ Sovereign CI pipeline: plasmid.harvest → mesh.publish → auto_fetch (LIVE)
✅ Multi-builder authority: sporeGate + eastGate
✅ Pre-push gates: songBird + bearDog (.githooks/pre-push)
✅ 7/7 stadial criteria CLEAR
✅ WAN mesh: sporeGate ↔ flockGate (WireGuard, 72ms p50)
✅ LAN mesh: eastGate ↔ ironGate ↔ southGate (10G backbone)
⚠️  Pepti depot: ~9 primals still need rebuild on sporeGate
⚠️  bearDog CryptoProvider panic (UNIT-DIV-04) — blocks DNS cutover
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

### 2. bearDog CryptoProvider (UNIT-DIV-04) — P1

`rustls-rustcrypto` CryptoProvider panics on install. Blocks Caddy → bearDog ACME TLS cutover.
**File**: `crates/beardog-acme/src/` — `CryptoProvider::install()` call site
**Likely cause**: Double-install or incompatible provider state (ES256 signing added Wave 132f)
**Unblocks**: DNS cutover (`primals.eco` → bearDog TLS), sporePrint sovereignty

### 3. cellMembrane Forgejo Bare Repo (golgi operator)

Push rejected with `unresolved deltas` — shallow depth=1 bare repo broke after rebase.
**Fix**: On golgi, delete and recreate with `git clone --mirror` from origin.
**Origin (GitHub)** is current at `ad4e532` (604 tests, composition profiles).

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
| bearDog CryptoProvider fix (UNIT-DIV-04) | **P1 BLOCKER** |
| DNS cutover: primals.eco → bearDog ACME TLS | After CryptoProvider |
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
| **bearDog** | CryptoProvider fix (UNIT-DIV-04). P1 for DNS cutover. | **P1** |
| **sporePrint** | 249 pages, thesis scaffolded. Evolving thin-relay → NUCLEUS for hosting (nestGate → +squirrel → +petalTongue → +barraCuda). | Active |
| **cellMembrane** | 604 tests. Composition profiles LIVE. Forgejo needs golgi operator. | Active |
| **primalSpring** | 128 validation scenarios. SHOW_HN prep ongoing. | Active |
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

## Gate Convergence (134d — 09:45 EDT)

```
CONVERGED:
  ✅ eastGate   — All repos cascaded. 604 membrane tests, 128 scenarios, 249 pages.
  ✅ golgiBody  — VPS-thin. sporePrint serving. E2E 200.
  ✅ sporeGate  — Pepti rebuilds in progress.

BLOCKED:
  🔄 flockGate  — WG UP. Drawbridge pending pepti redeploy.

STALE:
  ⚠️  ironGate   — Jul 4, 5+ days. Needs SSH.
```

*Pipeline: push → harvest → checksum → mesh.publish → auto_fetch → verify → deploy*
