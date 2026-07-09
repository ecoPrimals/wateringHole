# ecoPrimals Ecosystem Blurb — Wave 134g

**Date**: Jul 9, 2026 11:40 EDT | **Wave**: 134g | **From**: eastGate overwatch
**Posture**: **NEAR-CONVERGED — Pepti 100%. WAN transport PASS. songBird P2 fix landed. ironGate cascade resolved. DNS cutover is the last gate.**

---

## Current State

```
✅ 14/14 primals pass cargo check --all-targets
✅ Pepti depot: 34/34 builds, 0 failures (sporeGate AAR). 16 binaries × 2 triples.
✅ WAN-DISPATCH-01 transport: PASS (10/10, 142ms p50)
✅ songBird P2 fix landed (82fb474): http.request origin-form for HTTP/1.1
✅ E2E: primals.eco → 200 (golgi VPS-thin, 39% disk, 5.7G free)
✅ UNIT-DIV-04 RESOLVED
✅ cellMembrane Forgejo bare repo: FIXED (re-shallowed to 1be2b7f)
✅ golgi sovereign-ci.log: FIXED (0666 + logrotate)
✅ ironGate cascade: RESOLVED (20 repos current)
✅ Composition-scoped lifecycle LIVE (cellMembrane 1be2b7f)
✅ Multi-builder authority: sporeGate + eastGate
✅ Pre-push gates: songBird + bearDog
✅ 7/7 stadial criteria CLEAR
✅ Forgejo shallow relay: 40/40 repos, 410M (from 3.8G), reshallow timer deployed
⚠️  capability.call("jupyter"): needs sporeGate drawbridge env config
⚠️  DNS cutover: primals.eco → bearDog ACME TLS (unblocked, pending 7-day shadow)
```

---

## Remaining Work

### 1. sporeGate Drawbridge Config (unblocks capability.call FULL PASS)

```bash
sudo systemctl edit songbird
# [Service]
# Environment=SONGBIRD_DRAWBRIDGE_ROUTES=/hub=jupyter
sudo systemctl restart songbird
```

Quick env config — no code change. Triggers `provided_capabilities()` → mesh announce.

### 2. DNS Cutover — primals.eco → bearDog ACME TLS

All blockers cleared: UNIT-DIV-04 resolved, pepti current, bearDog deployed.
**Path**: Enable bearDog ACME on golgi → 7-day Caddy shadow → DNS flip
**Closes**: S-10 (sporePrint sovereignty)

### 3. Operational

| Item | Owner | Status |
|------|-------|--------|
| strandGate enrollment | hardware team | Pending physical access (house 2) |

---

## Upstream Divergences (from sporeGate AAR)

| ID | Issue | Impact |
|----|-------|--------|
| SHALLOW-DIV-01 | Merge commits can't push to shallow Forgejo (unresolved deltas) | Workaround: re-shallow from mirror. Linear pushes work fine. |
| SHALLOW-DIV-02 | UFW rules can exist in config but not in iptables | Add `ufw reload` to provisioning + health checks. |
| SHALLOW-DIV-03 | Blurb state lag — items listed as pending when already done | sporeGate should push heads more frequently. |

**Recommendation**: cellMembrane `temporal.cascade` should detect shallow push failures and auto-reshallow from the sovereign mirror.

---

## Wave Plan

### 134 — Capability Convergence (nearly complete)

| Item | Status |
|------|--------|
| ~~Pepti rebuilds~~ | **DONE** — 34/34 builds, 0 failures |
| ~~WAN-DISPATCH-01 transport~~ | **PASS** — 10/10, 142ms p50 |
| ~~songBird P2 fix~~ | **DONE** — `82fb474` origin-form |
| ~~ironGate cascade~~ | **DONE** — 20 repos current |
| ~~cellMembrane Forgejo~~ | **DONE** — re-shallowed |
| ~~golgi CI log~~ | **DONE** — permissions fixed |
| sporeGate drawbridge env config | Quick fix |
| capability.call FULL PASS | After env config |

### 135 — Sovereignty Sprint

| Item | Status |
|------|--------|
| DNS cutover: primals.eco → bearDog ACME TLS | **UNBLOCKED** |
| sporePrint: Caddy → bearDog TLS (7-day shadow) | After DNS cutover |
| strandGate SSH enrollment | Pending hardware |

### 136+ — SHOW_HN Readiness

S-6 (pepti) ✅ | S-8 (cross-gate dispatch) → after env config | S-10 (sporePrint sovereign) → 135 | O-1 (karma buildup) → 3-6 month window

---

## Team Dispatches

| Team | Status |
|------|--------|
| **sporeGate** | **CONVERGED.** 34/34 builds. Set drawbridge env config for full capability.call pass. |
| **songBird** | P2 fix landed (`82fb474`). Ready for pepti redeploy with origin-form fix. |
| **flockGate** | WAN transport PASS. Awaiting capability.call after sporeGate env config. |
| **bearDog** | Ready. 13,884+ tests. Deploy to golgi for DNS cutover. |
| **cellMembrane** | Composition lifecycle LIVE. Forgejo synced. |
| **sporePrint** | 249+ pages. Evolving thin-relay → NUCLEUS. |
| **primalSpring** | Composition lifecycle scenario evolved (`9117d1b`). 1101+ tests. |
| **ironGate** | Cascade RESOLVED — 20 repos current. |

---

## Gate Convergence (134g — 11:40 EDT)

```
CONVERGED:
  ✅ eastGate   — All 16 repos cascaded. Heads current.
  ✅ sporeGate  — 34/34 builds, depot 100% current. Drawbridge live.
  ✅ golgiBody  — Thin relay. 39% disk. Forgejo fixed. sporePrint serving.
  ✅ flockGate  — songBird 0.2.1. WAN transport PASS. 2 mesh peers.
  ✅ ironGate   — 20 repos current. Cascade resolved.

PENDING:
  🔧 strandGate — Enrollment pending (physical access, house 2).
```

*Pipeline: push → harvest → checksum → mesh.publish → auto_fetch → verify → deploy*
