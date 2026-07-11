# ecoPrimals Ecosystem Blurb — Wave 136b

**Date**: Jul 11, 2026 | **Wave**: 136b | **From**: eastGate overwatch
**Posture**: **HARDENED. ALL 8 STADIAL CRITERIA CLEAR.** Outer membrane sprint complete (9/14 exposures closed). darkforest v3.0 live: 25/26 PASS. footPrint composition target introduced. Cooling sprint continues.

---

## Active Sprint — 136b

### Hardening (carry from 136a)

| ID | Task | Owner | Status |
|----|------|-------|--------|
| SIGN-01 | Cascade signing activation (ed25519 key deploy + verify) | cellMembrane + sporeGate | Code landed, activation pending |
| EXP-06 | Lab auth-gate at Caddy layer (`lab.primals.eco`) | sporeGate | songBird code landed, Caddy wiring pending |
| SITE-REBUILD | Deploy `content.rebuild` to golgi (Zola auto-build) | sporeGate | Code landed, membrane redeploy needed |
| ODN-02 | DNSSEC on `primals.eco` | operator | darkforest flagged (registrar-level) |

### New: footPrint Composition (flockGate)

footPrint is a GIS home improvement planner built in isolation, now introduced to the ecosystem as the first **primal composition target**. It is NOT a primal — it is a product that primals compose into.

**flockGate overwatch**: clone `protoKarya/footPrint` to `protists/footPrint`, `npm install`, verify dev server runs. You own this composition. Manifest entry is live (repo 40/40, `evolution_target = "composition"`).

| Team | Action |
|------|--------|
| **flockGate** | Clone repo, spin up dev server, own the composition going forward |
| **petalTongue** | Serve footPrint frontend from Axum — 12 visual target areas define parity (`specs/PETALTONGUE_VISUAL_TARGETS.md`) |
| **nestGate** | Replace Express project CRUD with CAS persistence (content-addressed, rootPulse-traced) |
| **songBird** | Replace Express `/api/proxy` with drawbridge routing (same allowlist: OSM, FEMA, USGS, ArcGIS) |
| **projectNUCLEUS** | Package as deployable composition (petalTongue + nestGate + songBird serving footPrint) |

The Express server disappears — primals absorb backend. Browser frontend (Leaflet/Turf.js) is the product. Static (sporePrint, 301 pages) and interactive (petalTongue/footPrint) become the twin public faces of the ecosystem.

**RustScript** (12 Rust safety modules in TypeScript) is evidence FOR pure Rust, not a bridge to it. Added to gen3 thesis as §5.5. Blueprint available for anyone who wants safer TypeScript.

### External Review: Post-Cloudflare Resilience

External reviewer flagged DDoS/traffic-spike risk now that Cloudflare is removed. Key corrections and actions:

- **Not residential**: golgi is a DigitalOcean VPS (NYC1), not a home box. DO provides upstream DDoS mitigation.
- **lab.primals.eco HTTP**: was EXP-06 timing — Caddy terminates TLS, internal hop is WireGuard-encrypted. CSP + headers now deployed. Auth-gate (EXP-06) still pending.
- **Real gap**: no CDN edge caching or enterprise DDoS absorption for HN-scale traffic spikes.
- **Suggestion adopted**: evaluate GitHub Pages as static CDN mirror for sporePrint content (SURGE-01). Outer membrane absorbs spike, sovereign golgi serves live content. Compatible with diderm model.

Full analysis: `handoffs/EXTERNAL_REVIEW_RESPONSE_136b.md`

### Backlog

| ID | Task | Owner |
|----|------|-------|
| SURGE-01 | GitHub Pages as static CDN mirror for HN traffic spike | sporePrint + sporeGate |
| SKUNY-INGEST | Caddy JSON logs → skunkBat `baseline.observe` | skunkBat |
| DF-REPORT | darkforest v3.0 outer membrane execution report | projectNUCLEUS |
| NESTGATE-DEBT | Deep debt sweep continuation (thiserror landed) | nestGate |
| FP-PARITY | petalTongue visual parity with footPrint (12 VT areas) | petalTongue |
| COORD-ACTIVATE | nestGate coordination backend activation | nestGate + petalTongue |
| LIVE-ACTIVATE | `live.primals.eco` petalTongue NUCLEUS hosting | sporeGate |

---

## 136a Delivery (Complete)

9/14 exposures closed: security headers (HSTS, CSP, X-Frame, nosniff), 404 fix, fail2ban, depot rate-limiting, JSON access logs, WireGuard key audit, cert renewal drill. All validated live on primals.eco. Full AAR: `handoffs/OUTER_MEMBRANE_HARDENING_AAR_136a.md`.

Primal evolution absorbed: skunkBat HTTP anomaly detection (`f9154a8`, 553 tests), songBird auth-gate hardening (`eb4d0be`), cellMembrane SIGN-01 pipeline (`c1fa85a`), nestGate deep debt sweep (`510d66f`), darkforest v3.0 (`d35df65`, 149 tests, 25/26 PASS live), primalSpring outer membrane scenario (`b10aad7`, 1102 tests, 129 scenarios).

---

## Gate Convergence

```
eastGate     — Overwatch. All repos at HEAD. 136b coordinated.
sporeGate    — Hardened (9/14 closed). Depot 100%. Site live.
golgiBody    — Caddy hardened, fail2ban active, rate-limited.
flockGate    — WAN PASS. footPrint gate owner. Clone + spin up.
ironGate     — darkforest v3.0 active. 25/26 PASS live.
strandGate   — Enrollment pending (house 2).
grapheneGate — Pending pepti pull + ADB deploy.
```

## Tests

| Suite | Tests | Scenarios | Status |
|-------|-------|-----------|--------|
| primalSpring | 1,102 | 129 | GREEN |
| groundSpring | 1,047+ | — | GREEN |
| skunkBat | 553 | — | GREEN |
| projectNUCLEUS | 149 | — | GREEN |

## Glacial

**ALL 8 CRITERIA CLEAR.** Criterion 8 (outer membrane) 5/5 met. SIGN-01 + EXP-06 are defense-in-depth, not blockers.

---

## Handoffs This Wave

| Document | What |
|----------|------|
| `FOOTPRINT_COMPOSITION_WAVE136b.md` | Team actions for footPrint composition |
| `FRAGO_PROTISTS_CATEGORY_136b.md` | Taxonomy: `protists/` = composition targets |
| `OUTER_MEMBRANE_HARDENING_AAR_136a.md` | Full 136a security sprint AAR |
| `SKUNKBAT_OUTER_MEMBRANE_136a.md` | skunkBat HTTP detection spec |
| `EXTERNAL_REVIEW_RESPONSE_136b.md` | Post-Cloudflare resilience analysis + CDN mirror recommendation |

*Wave 136b: Hardened and stable. footPrint introduced — first composition target. flockGate: clone and spin up. Teams: see your action items above.*
