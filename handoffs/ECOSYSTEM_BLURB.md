# ecoPrimals Ecosystem Blurb — Wave 136b

**Date**: Jul 11, 2026 15:30 EDT | **Wave**: 136b | **From**: eastGate overwatch
**Posture**: **HARDENED. ALL 8 STADIAL CRITERIA CLEAR. Outer membrane sprint complete (9/14 closed). darkforest v3.0 live scan 25/26 PASS. footPrint protist spinning up — petalTongue visual parity target established. Cooling sprint continues.**

---

## Overnight Evolution (since 136b bump)

| Repo | Commit | What |
|------|--------|------|
| nestGate | `510d66f` | Deep debt sweep: typed errors, thiserror derives, modern idioms across 12 files |
| primalSpring | `b10aad7` | darkforest v3.0 AAR (Wave 136c): TLS evolution + outer membrane live results, cross-spring parity scorecard updated |

Both pulled clean (fast-forward). bearDog stale local revert discarded. **All 20+ repos at HEAD, zero dirty.**

---

## Wave 136a Sprint — DELIVERED (Jul 10)

### Exposure Matrix — 9/14 Closed

| ID | What | Status |
|----|------|--------|
| EXP-01 | Security headers (HSTS, X-Frame, nosniff, Permissions-Policy) | CLOSED |
| EXP-02 | 404 catch-all → proper `handle_errors` | CLOSED |
| EXP-03 | Cert lifecycle (Caddy ACME, all 5 domains) | CLOSED |
| EXP-04 | Forgejo SSH fail2ban (port 2222, 3-try ban) | CLOSED |
| EXP-05 | Depot rate-limiting (iptables 50 conn/10s) | CLOSED |
| CSP-01 | Content-Security-Policy (static + proxy policies) | CLOSED |
| AUDIT-01 | JSON access logs (50MiB roll, 30d) | CLOSED |
| EXP-07a | WireGuard key audit + 90d rotation policy | CLOSED |
| RF-01 | Cert renewal drill validated | CLOSED |

### Primal Evolution Absorbed

| Primal | Commit | What |
|--------|--------|------|
| skunkBat | `f9154a8` | HTTP anomaly detection: `HttpObservation`, `advisory_check_http()`. 553 tests. |
| songBird | `eb4d0be` | EXP-06 drawbridge auth-gate hardening (code) |
| cellMembrane | `c1fa85a` | SIGN-01 signing pipeline + security sprint |
| nestGate | `510d66f` | Coord handlers + deep debt sweep (thiserror, typed errors) |
| projectNUCLEUS | `d35df65` | darkforest v3.0 — TLS outer membrane pen-test (25/26 PASS live) |
| primalSpring | `b10aad7` | `s_outer_membrane_posture` scenario (129 scenarios, 1102 tests) + darkforest AAR |

### darkforest v3.0 Live Results (primals.eco)

25/26 checks PASS. One DARK_FOREST (ODN-02: DNSSEC not enabled on `primals.eco` — infrastructure gap, registrar-level). 6 outer modules: tls, http, depot, forge, dns, mesh. 149 Rust tests.

---

## Remaining Work — 136b Sprint

### HIGH Priority

| ID | Task | Owner | Status |
|----|------|-------|--------|
| SIGN-01 | Cascade signing activation (deploy ed25519 key + verify in pipeline) | cellMembrane + sporeGate | Code landed, activation pending |
| EXP-06 | Lab auth-gate at Caddy layer (`lab.primals.eco` basic_auth or mTLS) | sporeGate | songBird code landed, Caddy wiring pending |
| SITE-REBUILD | Deploy `content.rebuild` fix to golgi (Zola auto-build after cascade) | sporeGate | Code landed, membrane binary needs redeploy |
| ODN-02 | DNSSEC on `primals.eco` (registrar-level) | operator | darkforest flagged |

### MEDIUM Priority

| ID | Task | Owner | Status |
|----|------|-------|--------|
| SKUNY-INGEST | Wire Caddy JSON logs → skunkBat `baseline.observe` | skunkBat team | Logs flowing, ingestion pipeline not wired |
| DF-REPORT | darkforest v3.0 outer membrane execution report | projectNUCLEUS | 25/26 PASS, report pending |
| NESTGATE-DEBT | Continue nestGate deep debt sweep (thiserror landed, more modules to follow) | nestGate team | In progress |

### footPrint Protist — Spinning Up (flockGate)

**New ecosystem layer**: `protists/` — protoKarya org repos, proto-organisms evolving toward primals.

| Item | Detail |
|------|--------|
| `protists/footPrint` | GIS home improvement planner (TypeScript/Leaflet/Vite). Cloned from `protoKarya/footPrint`. **Dev server verified** on eastGate (Vite `:5173` + Express `:3000`). Build passes (347 modules, 819KB). Zero TS errors. |
| Architecture | Full ECS (entity-component-system), command pipeline with undo/redo, Gauss-Newton parametric constraint solver, reactive computation graph, 8 data source integrations (OSM, FEMA, parcels, zoning, USGS, soils, Michigan GIS, infrastructure), intelligence layer (proximity, conflicts, elevation), snap/grid/dimensions/terrain. |
| RustScript | 12-module zero-dep TypeScript library encoding Rust safety primitives (Result, Option, Owned, RefCell, Iter, Vec, Cow, Channel, Brand, exhaustive). Compile-time + runtime enforcement. AI-translatable to Rust — validates gen3 constrained-evolution thesis. |
| Gate owner | **flockGate** — WAN-accessible, can reach LAN HPC for compute-heavy operations (DEM processing, batch elevation). Registered in `ecosystem_manifest.toml` (repo 40/40). |
| petalTongue target | 12 visual capability areas documented (`specs/PETALTONGUE_VISUAL_TARGETS.md`). petalTongue must achieve visual parity with footPrint, then exceed it with sovereign backend (nestGate CAS, rootPulse provenance, mesh federation). |
| projectNUCLEUS target | footPrint validates the full rendering + data + persistence pipeline. projectNUCLEUS must package this as a deployable composition. The 4-phase evolution: visual parity → backend sovereignty → compute integration → full primal composition. |

**Evolution path**: TypeScript validation layer proves patterns → petalTongue absorbs frontend → server logic becomes Rust primal → RustScript becomes native compile-time enforcement. Just as sporePrint serves static content (301 pages), petalTongue will serve interactive tools — footPrint is the first.

### LOW Priority / Backlog

| ID | Task | Owner |
|----|------|-------|
| FP-PARITY | petalTongue visual parity with footPrint (12 VT areas) | petalTongue + projectNUCLEUS |
| FP-CAS | footPrint project persistence → nestGate CAS migration | nestGate + petalTongue |
| FP-MESH | Data source proxying through songBird drawbridge | songBird + footPrint |
| ALERT-01 | Cert expiry alerting (7d warning via rootPulse) | nestGate |
| SKUNY-HTTP-IDS | HTTP intrusion heuristics (path enumeration, method confusion) | skunkBat |
| COORD-ACTIVATE | nestGate coordination backend activation (ingest pipeline + petalTongue dashboard) | nestGate + petalTongue |
| LIVE-ACTIVATE | `live.primals.eco` petalTongue NUCLEUS hosting | sporeGate |

---

## Test Suite Health

| Spring/Primal | Tests | Scenarios | Status |
|---------------|-------|-----------|--------|
| primalSpring | 1,102 | 129 | **GREEN** |
| groundSpring | 1,047+ | — | **GREEN** |
| skunkBat | 553 | — | **GREEN** |
| projectNUCLEUS | 149 | — | **GREEN** (darkforest v3.0) |

---

## Gate Convergence

```
✅ eastGate     — All 20+ repos at HEAD. Wave 136b coordinated. Zero dirty.
✅ sporeGate    — Security hardened (9/14 closed). Depot 100%. Site live.
✅ golgiBody    — Caddy hardened, certs renewing, fail2ban active, rate-limited.
✅ flockGate    — WAN PASS. Outer membrane validated. footPrint gate owner (protist spinning up).
✅ ironGate     — darkforest v3.0 active. 25/26 PASS live.
🔧 strandGate   — Enrollment pending (house 2).
📱 grapheneGate  — Pending pepti pull + ADB deploy.
```

---

## Glacial Shift

**ALL 8 CRITERIA CLEAR.** Criterion 8 (outer membrane hardening) now 5/5 sub-criteria met. Remaining SIGN-01 + EXP-06 are defense-in-depth, not stadial blockers.

## Team Dispatches

| Team | Status | Next |
|------|--------|------|
| **petalTongue** | Coordination backend code landed | footPrint visual parity (12 VT areas) — first interactive tool for `live.primals.eco` |
| **projectNUCLEUS** | darkforest v3.0 outer membrane 25/26 PASS | footPrint composition packaging, execution report |
| **sporeGate/golgi** | Sprint complete: 9 exposures closed | SIGN-01 activation, EXP-06 Caddy auth, site rebuild deploy |
| **flockGate** | WAN validated, footPrint gate owner | footPrint deployment, WAN accessibility for GIS tool |
| **skunkBat** | HTTP anomaly detection live (553 tests) | Caddy log ingestion pipeline |
| **songBird** | Auth-gate code landed | drawbridge proxy for footPrint data sources |
| **cellMembrane** | SIGN-01 pipeline + content.rebuild | Deploy signing keys, deploy rebuilt membrane to golgi |
| **nestGate** | Coord backend + deep debt sweep | CAS persistence for footPrint projects, cert alerting |
| **sporePrint** | 301 pages live, auto-merge | Content evolution — static counterpart to petalTongue interactive |

*Wave 136b: System stable. footPrint protist spinning up — petalTongue and projectNUCLEUS now have a concrete visual parity target. Cooling sprint continues. No regressions.*
