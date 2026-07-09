# ecoPrimals Ecosystem Blurb — Wave 135a

**Date**: Jul 9, 2026 13:25 EDT | **Wave**: 135a | **From**: eastGate overwatch
**Posture**: **CONVERGED — DNS cutover COMPLETE. primals.eco sovereign on bearDog TLS (golgi). S-10 CLOSED. petalTongue forward architecture for live.primals.eco defined.**

---

## Current State

```
✅ primals.eco: SOVEREIGN — bearDog ACME TLS on golgi (:443/:80), LE cert
✅ DNS cutover: GitHub Pages → golgi VPS (157.230.3.183), DNS-only Cloudflare
✅ 14/14 primals pass cargo check --all-targets
✅ Pepti depot: 34/34 builds, 0 failures
✅ WAN-DISPATCH-01 transport: PASS (10/10, 142ms p50)
✅ Drawbridge: CONFIGURED on sporeGate
✅ All 5 gates converged
✅ 7/7 stadial criteria CLEAR
✅ S-10 (sporePrint sovereign): CLOSED
✅ bearDog CSR SAN bug fixed (multi-domain ACME)
⚠️  Caddy cert renewal blocked (bearDog owns :80) — existing certs valid until Aug 13
⚠️  www.primals.eco serves 200 (same content) — no Host-header routing in bearDog yet
⚠️  live.primals.eco: not yet configured — petalTongue NUCLEUS hosting is forward work
```

---

## Architecture (golgi — production)

```
Internet
  │
  ├─ :443 → bearDog (ACME TLS, LE cert for primals.eco + www)
  │           └─ upstream → Caddy :8091
  │                          └─ file_server /opt/ecoPrimals/sporePrint/public
  │
  ├─ :80  → bearDog (HTTP-01 challenges + HTTPS redirect)
  │
  └─ :8443 → Caddy (LE certs for subdomains)
              ├─ membrane.primals.eco → nestGate cache + depot
              ├─ git.primals.eco → Forgejo :3000
              └─ lab.primals.eco → sporeGate :7780 (songBird drawbridge)
```

## Forward Architecture: live.primals.eco

**Option B (recommended from sporeGate postmortem):**

```
primals.eco      → golgi Caddy :8091 (static Zola — always available)
live.primals.eco → golgi bearDog → WireGuard → sporeGate petalTongue (dynamic, NUCLEUS)
```

Static site is always up. Dynamic version with live gate data, primal registry,
and capability-backed APIs available when sporeGate is online.

**petalTongue needs to become:**

| Capability | Status |
|------------|--------|
| Serve Zola static content as baseline | Dashboard only today |
| Gate topology API (`/api/gates`) | Exists in dashboard |
| Composition health (`/api/health`) | Not exposed |
| Ecosystem metrics (`/api/metrics`) | Not exposed |
| Primal registry (`/api/primals`) | Not exposed |
| pseudoSpore gallery (live) | Static today |
| Validation parity with Zola site | Not tested |

**Validation gate**: petalTongue on sporeGate must pass 6 checks (200 on `/`, CSS, RSS, API, content match, p99 ≤ 100ms) before serving production traffic.

---

## Remaining Work

### 1. Caddy Cert Renewal Strategy (before Aug 13)

bearDog owns :80, blocking Caddy HTTP-01 renewal for subdomains. Options:
- Add DNS-01 support to bearDog ACME
- Temporarily stop bearDog for Caddy renewal
- bearDog Host-header routing (all domains on :443, eliminate :8443)

### 2. live.primals.eco (petalTongue NUCLEUS)

Forward work for petalTongue team — evolve from dashboard-only to full sporePrint host with backend capabilities. Validate against static site, then deploy via bearDog → WireGuard → sporeGate.

### 3. capability.call Retest

sporeGate drawbridge configured. flockGate needs to retest for WAN-DISPATCH-01 FULL PASS.

### 4. strandGate Enrollment

Pending physical access (house 2).

---

## Wave Plan

| Wave | Goal | Status |
|------|------|--------|
| **134** | Pepti + capability convergence + DNS cutover | **COMPLETE** |
| **135** | petalTongue NUCLEUS hosting + cert renewal strategy | Starting |
| **136+** | SHOW_HN readiness (28 rubric criteria) | S-6 ✅, S-8 retest pending, S-10 ✅ |

---

## Team Status

| Team | State |
|------|-------|
| **sporeGate/golgi** | DNS cutover DONE. bearDog TLS live. Owns cert renewal strategy. |
| **petalTongue** | Forward: evolve from dashboard to sporePrint NUCLEUS host for live.primals.eco. |
| **flockGate** | Retest capability.call for FULL PASS. |
| **bearDog** | CSR SAN bug fixed. Host-header routing needed for cert consolidation. |
| **songBird** | P2 fix deployed. Ready. |
| **cellMembrane** | SHALLOW-DIV absorbed. Composition lifecycle LIVE. |
| **sporePrint** | 249+ pages. Static site live on primals.eco. NUCLEUS evolution → live.primals.eco. |
| **primalSpring** | 1101+ tests. 128 scenarios. |
| **ironGate** | 20 repos current. |

---

## Gate Convergence (135a)

```
✅ eastGate   — All repos current.
✅ sporeGate  — Depot 100%. Drawbridge configured.
✅ golgiBody  — DNS cutover LIVE. bearDog TLS. sporePrint serving. E2E 200.
✅ flockGate  — WAN PASS. Retest capability.call.
✅ ironGate   — 20 repos current.
🔧 strandGate — Enrollment pending (house 2).
```

*primals.eco: bearDog TLS → Caddy static → sovereign. Pipeline: push → harvest → checksum → mesh.publish → auto_fetch → verify → deploy.*
