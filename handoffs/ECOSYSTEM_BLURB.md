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
| ODN-02 | DNSSEC on `primals.eco` | operator (registrar UI) | **REALWORLD** — registrar web portal, no API |

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

### External Review: Post-Cloudflare Resilience → MacGuffin Test

External reviewer flagged DDoS/traffic-spike risk post-Cloudflare. Corrections: golgi is a DO VPS (NYC1), not residential. lab.primals.eco HTTP was timing, now CSP/HSTS deployed. DDoS gap is real but bounded by DO upstream mitigation.

**Our response: defense in depth and mathematics, not obscurity.** If we can't show how the system works and remain secure, we have a MacGuffin, not security. The architecture is built on ChaCha20-Poly1305, BLAKE3, ed25519, diderm membranes, WireGuard overlay, CSP, rate limiting, skunkBat detection — independent layers, each sufficient without the others. 301 pages of published architecture already prove this.

**The evolution target**: sporePrint becomes a **live topology visualization** — gate status, mesh connectivity, membrane layers, security posture, wave state — rendered by petalTongue from nestGate coordination data and songBird mesh heartbeats. This IS the security argument. Showing how it works is the proof. footPrint GIS visualization tech informs the approach.

CDN mirror (SURGE-01) repositioned: availability during spikes, not a hiding place. Full analysis: `handoffs/EXTERNAL_REVIEW_RESPONSE_136b.md`

### Backlog

| ID | Task | Owner | Priority |
|----|------|-------|----------|
| TOPO-VIS | sporePrint live topology visualization (petalTongue + nestGate + songBird) | sporePrint + petalTongue | HIGH |
| SKUNY-INGEST | Caddy JSON logs → skunkBat `baseline.observe` | skunkBat | MEDIUM |
| DF-REPORT | darkforest v3.0 outer membrane execution report | projectNUCLEUS | MEDIUM |
| NESTGATE-DEBT | Deep debt sweep continuation (thiserror landed) | nestGate | MEDIUM |
| FP-PARITY | petalTongue visual parity with footPrint (12 VT areas) | petalTongue | MEDIUM |
| COORD-ACTIVATE | nestGate coordination backend activation | nestGate + petalTongue | MEDIUM |
| LIVE-ACTIVATE | `live.primals.eco` petalTongue NUCLEUS hosting | sporeGate | MEDIUM |
| SURGE-01 | GitHub Pages as availability mirror (cached sporePrint, not a hiding place) | sporePrint + sporeGate | LOW |

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
strandGate   — Enrollment pending. REALWORLD: physical access (house 2, cable + power).
grapheneGate — Pending pepti pull. REALWORLD: USB ADB cable + physical device.
```

## Operator Task Audit — Agentic vs Realworld

Every task currently tagged "operator" or requiring manual intervention, classified:

### REALWORLD — Physical/Hardware Required (cannot be agentic)

| Task | Why Realworld | Gate |
|------|--------------|------|
| strandGate enrollment | Physical: cable ethernet, power on, OS install at house 2 | strandGate |
| grapheneGate pepti deploy | Physical: USB ADB cable to Pixel 8a, `adb push` ecobins | grapheneGate |
| ODN-02 DNSSEC | Registrar web portal (no API) — human clicks in Porkbun/Namecheap UI | golgiBody |
| WireGuard key rotation (EXP-07a) | Key ceremony: generate on gate, exchange out-of-band, verify | mesh team |
| Network failover drill (RF-02) | Physical cable moves, router config at physical hardware | LAN |
| northGate/swiftGate/kinGate enrollment | Hardware ready but not deployed — physical setup | various |

### AGENTIC NOW — Already Evolved (no operator needed)

| Task | How It Became Agentic |
|------|----------------------|
| DNS NS cutover | Done (Wave 134h). Was manual registrar action, now complete. |
| Temporal cascade sync | `membrane temporal.cascade` — was manual git loops, now agentic (Wave 84) |
| Cert management | Caddy ACME auto-renewal — was manual certbot, now self-resolving |
| sporePrint rebuild | `membrane content.rebuild` — was manual Zola build, now agentic (Wave 135b) |
| Depot distribution | `membrane plasmid.harvest` + mesh auto-fetch — was manual scp, now agentic |
| fail2ban monitoring | Systemd service, auto-banning — no operator intervention |
| Security headers | Caddy snippets, auto-applied — no operator intervention |
| Access log rotation | Caddy JSON logs, 50MiB roll, 30d retention — automatic |

### EVOLVE TO AGENTIC — Can and should be automated

| Task | Current State | Agentic Path | Owner |
|------|--------------|-------------|-------|
| SIGN-01 activation | Code landed, needs key deploy + verify on sporeGate | `membrane sign.activate` — generate keypair, distribute pubkey via mesh, verify round-trip | cellMembrane |
| EXP-06 lab auth-gate | songBird code landed, Caddy config manual | `membrane caddy.configure` or template in provision script — Caddy API supports hot-reload | sporeGate |
| SITE-REBUILD deploy | membrane binary on golgi needs update | `membrane plasmid.fetch` on golgi pulls new binary, systemd restart — fully agentic path exists | sporeGate |
| Caddy config changes | Currently SSH + edit Caddyfile | Caddy has a REST API (`/config/`). cellMembrane could manage Caddy config via API calls | cellMembrane |
| SURGE-01 static mirror | Manual GitHub Pages setup | GitHub Actions workflow: on sporePrint push, build Zola, deploy to gh-pages branch — fully automatable | sporePrint |
| RustDesk client config | Manual per-gate change to point at `remote.primals.eco` | cellMembrane `gate.configure` could template RustDesk config at enrollment time | cellMembrane |

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

*Wave 136b: Hardened and stable. Defense in depth and mathematics, not obscurity. Operator tasks audited — 6 realworld (physical), 8 already agentic, 6 targeted for agentic evolution. sporePrint evolves to live topology visualization. footPrint introduced as first composition target. flockGate: clone and spin up.*
