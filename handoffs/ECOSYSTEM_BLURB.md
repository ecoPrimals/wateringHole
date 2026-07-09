# ecoPrimals Ecosystem Blurb — Wave 135

**Date**: Jul 9, 2026 13:30 EDT | **Wave**: 135 | **From**: eastGate overwatch
**Posture**: **SOVEREIGN — Wave 134 closed. primals.eco live on bearDog TLS. All gates converged. Beginning: live site evolution, coordination backend, SHOW_HN readiness.**

---

## Wave 134 Summary (CLOSED)

Wave 134 ran Jul 7–9 across 8 sub-waves (134a–134h). All objectives met:

| Objective | Result |
|-----------|--------|
| Pepti depot 100% current | 34/34 builds, 0 failures |
| WAN-DISPATCH-01 transport | PASS (10/10, 142ms p50) |
| DNS cutover: primals.eco sovereign | bearDog ACME TLS on golgi, LE cert |
| BUILD-DIV-01/02 resolved | Code fixed + pre-push gates |
| UNIT-DIV-04 resolved | CryptoProvider idempotent since 132f |
| SHALLOW-DIV-01/02 absorbed | cellMembrane classified diagnostics |
| Composition profiles formalized | 5 profiles in manifest + code |
| All operational fixes | Forgejo, CI log, ironGate cascade |

---

## Production Architecture

```
primals.eco (LIVE — sovereign)
  :443 → bearDog ACME TLS → Caddy :8091 → sporePrint static (Zola)
  :80  → bearDog HTTP-01 + redirect

Subdomains (:8443 Caddy)
  membrane.primals.eco → nestGate depot
  git.primals.eco      → Forgejo
  lab.primals.eco      → sporeGate songBird drawbridge

Mesh
  sporeGate ↔ flockGate (WireGuard, 142ms)
  eastGate ↔ golgi ↔ ironGate + southGate (covalent, <1ms)
```

---

## Wave 135 Goals

### 1. live.primals.eco — petalTongue NUCLEUS Hosting

**Static site is the sovereign baseline. Dynamic site proves the NUCLEUS.**

```
primals.eco      → golgi (static Zola — always available)
live.primals.eco → golgi bearDog → WireGuard → sporeGate petalTongue (NUCLEUS)
```

petalTongue evolves from dashboard-only to full sporePrint host with backend
capabilities. The live site validates that NUCLEUS composition can render,
serve, and exceed a static site — then grows with backend capability:

| Capability | Status | Wave |
|------------|--------|------|
| Zola static parity (serve existing content) | Dashboard only | 135 |
| `/api/gates` — live gate topology | Exists in dashboard | 135 |
| `/api/health` — composition health | Not exposed | 135 |
| `/api/primals` — primal registry | Not exposed | 135 |
| `/api/metrics` — ecosystem metrics | Not exposed | 135+ |
| pseudoSpore gallery (live artifacts) | Static today | 136 |
| squirrel AI chat integration | Not started | 136+ |

**Validation gate**: 6 checks before production traffic (200 on `/`, CSS, RSS, JSON API, content match, p99 ≤ 100ms).

### 2. nestGate Coordination Backend

**The ecosystem's public-facing coordination surface — like wateringHole, but live.**

nestGate on golgi already serves the depot (`membrane.primals.eco`). Extend it
to serve the coordination layer — blurbs, FRAGOs, AARs, wave state, gate heads —
as a structured API and dashboard. Public-facing but intended for ecosystem
evolution: overwatch uses it to direct the eco, teams use it to read state.

```
nestGate coordination backend:
  /coord/blurbs      — current + archived blurbs (from wateringHole/handoffs/)
  /coord/fragos      — FRAGOs and AARs
  /coord/waves       — wave state (from wave.toml)
  /coord/heads       — gate HEADs (from heads/*.toml)
  /coord/topology    — live mesh topology
  /coord/depot       — depot status, staleness, checksums
```

This replaces the current pattern of reading `.md` files from git with a live
queryable surface. As the project grows, overwatch agents and teams can query
`nestGate` instead of cascading git pulls to read state. wateringHole remains
the git-native source of truth; nestGate reads and serves it.

### 3. bearDog Cert Consolidation

bearDog owns :80/:443 but Caddy still handles subdomain certs on :8443.
Before Aug 13 (cert expiry), consolidate:

| Option | Complexity | Result |
|--------|------------|--------|
| **bearDog Host-header routing** | Medium | All domains on :443. Eliminates :8443. |
| DNS-01 in bearDog ACME | Medium | Caddy renews independently on :8443. |
| Temporary bearDog stop for renewal | Low | Manual, but works. |

### 4. capability.call FULL PASS

sporeGate drawbridge configured. flockGate retests `capability.call("jupyter")`.
Should be a formality — transport already proven.

### 5. strandGate Enrollment

Pending physical access (house 2). Hardware team.

---

## Team Dispatches

| Team | Wave 135 Work |
|------|---------------|
| **petalTongue** | Evolve to sporePrint host: serve Zola content + expose `/api/gates`, `/api/health`, `/api/primals`. Validation parity with static site. |
| **nestGate** | Coordination backend: serve blurbs, FRAGOs, wave state, gate heads from wateringHole as structured API. Public-facing dashboard. |
| **sporeGate/golgi** | Cert consolidation strategy. DNS for `live.primals.eco`. petalTongue NUCLEUS composition on sporeGate. |
| **bearDog** | Host-header routing for cert consolidation. CSR SAN fix already landed. |
| **flockGate** | capability.call retest for FULL PASS. |
| **cellMembrane** | Composition lifecycle LIVE. Monitor auto-fetch across topology. |
| **sporePrint** | Content evolution — 249+ pages, thesis. Target: feed live.primals.eco with structured data. |
| **primalSpring** | SHOW_HN readiness (E-category: cold clone, CI badges, test naming). |

---

## Gate Convergence (Wave 135)

```
✅ eastGate   — All repos current. Overwatch directing Wave 135.
✅ sporeGate  — Depot 100%. Drawbridge configured. petalTongue NUCLEUS host target.
✅ golgiBody  — primals.eco LIVE (bearDog TLS). Thin relay. 39% disk.
✅ flockGate  — WAN PASS. capability.call retest pending.
✅ ironGate   — 20 repos current.
🔧 strandGate — Enrollment pending (house 2).
```

---

## SHOW_HN Readiness (tracking)

| Category | Status |
|----------|--------|
| S-6 (pepti current) | ✅ |
| S-8 (cross-gate dispatch) | ⏳ (retest pending) |
| S-10 (sporePrint sovereign) | ✅ |
| E-1 through E-7 (evidence) | In progress (primalSpring) |
| N-1 through N-6 (narrative) | Not started |
| O-1 (karma buildup) | 3-6 month window active |

*primals.eco: sovereign. Pipeline: push → harvest → mesh.publish → auto_fetch → deploy. Next: live.primals.eco proves the NUCLEUS.*
