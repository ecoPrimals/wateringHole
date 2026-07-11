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

### footPrint — Primal Composition Target (flockGate)

**New ecosystem layer**: `protists/` — protoKarya org repos. Not proto-primals — proto-compositions. Projects that will be *served by* primals, not *become* primals.

| Item | Detail |
|------|--------|
| `protists/footPrint` | GIS home improvement planner (TypeScript/Leaflet/Vite). Built in isolation as a practical tool, now introduced to the ecosystem. **Dev server verified** on eastGate. Build passes (347 modules, 819KB). Zero TS errors. |
| Architecture | Full ECS, command pipeline with undo/redo, Gauss-Newton constraint solver, reactive graph, 8 data sources (OSM, FEMA, parcels, zoning, USGS, soils, Michigan GIS, infrastructure), intelligence layer, snap/grid/dimensions/terrain. |
| RustScript | 12-module zero-dep TypeScript library encoding Rust safety primitives. **Not a bridge to Rust — evidence for pure Rust.** Shows that Rust constraints improve any language, but only native compile-time enforcement gives full safety. 3 constraints can't be expressed in TS at all (lifetimes, Send/Sync, zero-cost). 9 require runtime wrappers. This validates why primals are pure Rust. Section added to `CONSTRAINED_EVOLUTION_FORMAL.md` (§5.5). |
| Gate owner | **flockGate** — WAN-accessible, LAN HPC reach. Registered in `ecosystem_manifest.toml` (repo 40/40). |
| Composition target | footPrint is NOT a primal. It is a **primal composition**: petalTongue serves the frontend, nestGate provides CAS persistence, songBird proxies data sources. The Express server disappears — primals absorb its backend responsibilities. The browser frontend is the product. |

**Evolution**: Express goes away → primals take over backend → footPrint becomes first interactive tool on `live.primals.eco`. Static (sporePrint) and interactive (petalTongue/footPrint) are the twin public faces of the ecosystem. RustScript stays as a blueprint for anyone who wants safer TypeScript — for ecoPrimals, it's the control experiment that proved pure Rust is right.

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
