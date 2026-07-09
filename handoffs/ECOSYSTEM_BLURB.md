# ecoPrimals Ecosystem Blurb — Wave 134f

**Date**: Jul 9, 2026 11:25 EDT | **Wave**: 134f | **From**: eastGate overwatch
**Posture**: **CONVERGING — WAN-DISPATCH-01 transport PASS (10/10, 142ms). UNIT-DIV-04 resolved. Two protocol gaps found. Pepti + DNS cutover remain.**

---

## Current State

```
✅ 14/14 primals pass cargo check --all-targets
✅ WAN-DISPATCH-01 transport: PASS (10/10, 142ms p50, flockGate → sporeGate → ironGate)
✅ E2E: primals.eco → 200 (golgi VPS-thin)
✅ UNIT-DIV-04 RESOLVED (bearDog CryptoProvider idempotent since 132f)
✅ Composition profiles + composition-scoped lifecycle (cellMembrane 1be2b7f)
✅ Sovereign CI: plasmid.harvest → mesh.publish → auto_fetch (LIVE)
✅ Multi-builder authority: sporeGate + eastGate
✅ Pre-push gates: songBird + bearDog
✅ 7/7 stadial criteria CLEAR
✅ flockGate: songBird 0.2.1 redeployed from pepti depot, 2 mesh peers
⚠️  capability.call("jupyter"): FAIL — sporeGate env config needed (P1)
⚠️  songBird http.request: 404 path-handling bug at drawbridge (P2)
⚠️  Pepti depot: ~9 primals still need rebuild
⚠️  cellMembrane Forgejo bare repo: unpacker error
⚠️  ironGate: 5+ days stale
```

---

## Remaining Work

### 1. sporeGate Drawbridge Config (P1 — unblocks capability.call)

flockGate proved the HTTP transport works (curl to drawbridge → 200). But `capability.call("jupyter")` fails because sporeGate's songBird doesn't advertise the route.

```bash
# On sporeGate:
sudo systemctl edit songbird
# Add:
# [Service]
# Environment=SONGBIRD_DRAWBRIDGE_ROUTES=/hub=jupyter
sudo systemctl restart songbird
```

This triggers `provided_capabilities()` → `announce_drawbridge_capabilities()` → mesh peers discover the route. Quick fix, no code change.

### 2. songBird http.request Path Bug (P2 — code team)

curl to `http://10.13.37.2:7780/hub/api` returns 200. songBird's `http.request` to the same URL returns 404. Both reach JupyterHub (verified by response headers). The divergence is below HTTP headers — likely path normalization or HTTP/2 upgrade difference in songBird's reqwest client vs drawbridge proxy.

**Reproduce**: `tcpdump` on sporeGate port 7780, compare curl vs songBird payloads.
**Impact**: Low — transport proven, this is a client interop issue.

### 3. Pepti Rebuilds (~9 primals)

```
DONE:    songBird · nestGate · membrane · bearDog (pushed)
NEXT:    skunkBat · coralReef · sweetGrass · biomeOS · toadStool
         squirrel · petalTongue · loamSpine · rhizoCrypt · barraCuda
```

**Command**: `membrane plasmid.harvest --all` on sporeGate

### 4. DNS Cutover (unblocked)

UNIT-DIV-04 resolved. Path: pepti rebuild bearDog → deploy to golgi → 7-day Caddy shadow → DNS flip → sporePrint sovereignty (S-10).

### 5. Operational

| Item | Owner | Status |
|------|-------|--------|
| cellMembrane Forgejo bare repo | golgi operator | `git clone --mirror` recreate |
| ironGate cascade refresh | SSH operator | 5+ days stale |
| golgi sovereign-ci.log permissions | golgi operator | Quick `chown` fix |
| strandGate enrollment | hardware team | Pending physical access |

---

## Wave Plan

### 134a — Pepti + Capability Convergence (current)

| Item | Status |
|------|--------|
| sporeGate drawbridge env config | **P1 — quick fix** |
| Rebuild remaining ~9 pepti primals | NEXT |
| flockGate WAN-DISPATCH-01 FULL PASS (capability.call) | After env config |
| grapheneGate 13/13 from fresh pepti | After pepti |

### 134b — Sovereignty Sprint (unblocked)

| Item | Status |
|------|--------|
| ~~UNIT-DIV-04~~ | **RESOLVED** |
| DNS cutover: primals.eco → bearDog ACME TLS | After pepti |
| sporePrint: Caddy → bearDog TLS (7-day shadow) | After DNS cutover |
| strandGate SSH enrollment | Pending hardware |

### 135+ — SHOW_HN Readiness

S-6 (pepti current) → 134a | S-8 (cross-gate dispatch) → 134a | S-10 (sporePrint sovereign) → 134b | O-1 (karma buildup) → 3-6 month window

---

## Team Dispatches

| Team | Work | Priority |
|------|------|----------|
| **sporeGate** | Set `SONGBIRD_DRAWBRIDGE_ROUTES=/hub=jupyter` (P1). Pepti rebuilds (~9). cellMembrane Forgejo recreate. | **NOW** |
| **songBird** | `http.request` path-handling bug (P2): 404 where curl gets 200. Investigate reqwest vs drawbridge. | P2 |
| **flockGate** | WAN-DISPATCH-01 transport PASS. songBird 0.2.1 redeployed. Awaiting sporeGate env config for full pass. | Waiting |
| **bearDog** | Ready. 13,884+ tests. Gateway bind regression fixed. UNIT-DIV-04 resolved. | Ready |
| **cellMembrane** | Composition-scoped lifecycle LIVE. Forgejo needs golgi operator. | Active |
| **sporePrint** | 249+ pages. SEO bridging landed. Evolving thin-relay → NUCLEUS. | Active |
| **primalSpring** | 128 scenarios, 1101 tests, 0 fail. Deep debt cleanup landed. | Active |
| **ironGate** | 5+ days stale. Needs SSH for cascade + strandGate enrollment. | Next SSH |

---

## Topology

```
HARDWARE:
  House 1 (CRS310):  sporeGate · eastGate · northGate
  House 2 (SX3008F): ironGate · southGate · strandGate(pending)
  Link: 80m 10G AOC trunk

MESH (validated):
  songBird covalent:  eastGate ↔ golgi ↔ ironGate + southGate + grapheneGate
  WireGuard WAN:      sporeGate ↔ flockGate (69ms ICMP, 142ms HTTP p50)

VPS:
  golgiBody (thin-relay): relay + depot + sporePrint
  golgiBody-ext:          sporePrint mirror, TURN relay
```

---

## Gate Convergence (134f — 11:25 EDT)

```
CONVERGED:
  ✅ eastGate   — All 16 repos cascaded. Heads current.
  ✅ golgiBody  — VPS-thin. sporePrint serving. E2E 200.
  ✅ sporeGate  — Pepti in progress. Needs drawbridge env config.
  ✅ flockGate  — songBird 0.2.1 redeployed. WAN transport PASS. 2 mesh peers.

STALE:
  ⚠️  ironGate   — Jul 4, 5+ days. Needs SSH.
```

*Pipeline: push → harvest → checksum → mesh.publish → auto_fetch → verify → deploy*
