# ecoPrimals Ecosystem Blurb — Wave 136b (cascade update)

**Date**: Jul 11, 2026 18:30 EDT | **Wave**: 136b | **From**: eastGate overwatch
**Posture**: **HARDENED + CONVERGED. ALL 8 STADIAL CRITERIA CLEAR. DNSSEC LIVE.** 4 cascades today, 14 repos evolved. DUAL-CHECKOUT resolved. SIGN-01 blockers identified and handed off. darkforest 26/26 clean sweep. footPrint deep debt pass complete (46 tests, AGPL licensed, solver decomposed). flockGate WAN mesh gap surfaced. Every orthogonal dimension converging.

---

## Active Sprint — 136b

### Cascade Results (Jul 11 — four cascades)

14 repos evolved this wave. 0 conflicts. All repos clean and converged.

| Repo | SHA | Key Evolution |
|------|-----|---------------|
| **bearDog** | `cb80ed2` | Hierarchy refactor, monitoring tests, deep debt |
| **songBird** | `4300d89` | Drawbridge proxy + CLI stubs → real TCP probes (-672L) |
| **nestGate** | `9a46433` | Coord backend wired to all RPC + deep debt |
| **skunkBat** | `d9837a9` | skunky-ingest + RuntimeVerifier + config hydration |
| **cellMembrane** | `bfb1558` | **DUAL-CHECKOUT fixed** + type-safe manifest + harvest split |
| **primalSpring** | `fb03030` | **v0.9.35** — 1,104 tests, 132 scenarios, checksums parser fix |
| **petalTongue** | `225e30f` | TOPO-VIS coord_handlers + K-Derm topology viz |
| **projectNUCLEUS** | `5e59790` | **26/26 clean sweep** — DNSSEC, K-Derm reaffirmed |
| **footPrint** | `f258d42` | **Deep debt pass** — 46 tests, AGPL, solver decomposed, ESLint/Vitest |
| **wateringHole** | `d64d8a9` | EXP-06 + flockGate divergence AAR + SIGN-01 discovery |

### New AARs from Upstream

**SPOREPRINT_DUAL_CHECKOUT (P1)**: golgi had TWO sporePrint checkouts — Caddy served one, rebuild hook updated the other. Site was **30 commits stale**. Fixed immediately. Requires permanent fix: consolidate to single checkout. guideStone Merkle root recommended as deployment health check. See `SPOREPRINT_DUAL_CHECKOUT_AAR_136b.md`.

**LIVE THREAT DATA**: 122 unique attacker IPs, 317 SSH brute-force attempts in 7 days on golgi. Standard IoT botnet dictionary (admin, ubuntu, postgres, AdminGPON). HTTP scanning detected (wp-login, env probes, phpMyAdmin). fail2ban catching it. This is **real adversarial data** for skunkBat — replaces synthetic seed patterns. See `LIVE_THREAT_DATA_ACTIVATION_AAR_136b.md`.

**PRIMALSPRING v0.9.35**: chacha20poly1305 0.11, TOPO-VIS scenario (#132), all deps current, all pure Rust. See `PRIMALSPRING_V0935_EVOLUTION_136b.md`.

### Hardening Status

| ID | Task | Owner | Status |
|----|------|-------|--------|
| ~~ODN-02~~ | ~~DNSSEC on `primals.eco`~~ | operator | **DONE** — CF DNSSEC enabled, DS at Porkbun (keyTag 2371, alg 13) |
| SIGN-01 | Cascade signing activation (ed25519 key deploy + verify) | cellMembrane + sporeGate | Wire contract aligned (`d681466`), activation pending |
| ~~EXP-06~~ | ~~Lab auth-gate at Caddy layer~~ | sporeGate | **DONE** — basicauth on lab.primals.eco (`348df71`). Creds: see sporeGate handoff |
| SITE-REBUILD | Deploy `content.rebuild` to golgi (Zola auto-build) | sporeGate | Code landed, membrane redeploy needed |
| ~~SKUNKY-INGEST~~ | ~~Caddy JSON logs → skunkBat~~ | skunkBat | **DONE** — code complete, golgi deploy pending (`385f66f`). skunky-ingest crate delivered. |
| ~~COORD-ACTIVATE~~ | ~~nestGate coordination backend~~ | nestGate | **DONE** — wired to all RPC surfaces (`b829eb9`) |
| ~~DF-REPORT~~ | ~~darkforest v3.0 outer membrane report~~ | projectNUCLEUS | **DONE** — report + footPrint graph (`5fdc3c9`) |

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

**FP-DEPLOY: footPrint live on primals.eco** — The SPA is already built (`dist/client/` — index.html + Leaflet/Vite assets). Deployment path for sporeGate:

```
1. rsync dist/client/ to golgi:/opt/ecoPrimals/footPrint/
2. Add Caddy block:  handle_path /footprint/* { root * /opt/ecoPrimals/footPrint  file_server }
3. Proxy /api/* to songBird drawbridge on sporeGate (allowlist: OSM, FEMA, USGS, ArcGIS)
4. Verify: https://primals.eco/footprint/
```

This makes footPrint the first live composition target — a real GIS tool served by sovereign infrastructure. The Express server is NOT deployed; API proxy goes through songBird drawbridge (`87b7779` already has the allowlist).

**RustScript** (12 Rust safety modules in TypeScript) is evidence FOR pure Rust, not a bridge to it. Added to gen3 thesis as §5.5. Blueprint available for anyone who wants safer TypeScript.

### K-Derm Topology Reaffirmed — Cloudflare is the Outer Membrane

Porkbun dashboard confirms: `primals.eco` NS remains `alfie/serena.ns.cloudflare.com`. This is correct — it was never removed. The existing K-Derm diderm architecture (`DIDERM_DOMAIN_ARCHITECTURE.md`, `K_DERM_TOPOLOGY_STANDARD.md`) already defines this topology. The three-layer model maps directly to K-Derm layers:

```
K-Derm Layer          │ What                        │ primals.eco Path
──────────────────────┼─────────────────────────────┼──────────────────────────
Extracellular         │ Public internet, crawlers   │ Hostile traffic
Outer membrane (trans)│ Cloudflare proxy + Caddy    │ DDoS/CDN + TLS/CSP/HSTS
Periplasm             │ golgi relay, sporeGate CI   │ WireGuard routing, build
Plasma membrane       │ Gate firewall (Flint/UFW)   │ Boundary enforcement
Cytoplasm             │ NUCLEUS primals, UDS IPC    │ Sovereign compute
```

**Outer membrane data reinforces inner membrane.** Per §Cross-Membrane Validation in `DIDERM_DOMAIN_ARCHITECTURE.md`: inner membrane validates outer membrane integrity (content hash, timing baseline, TLS cert, DNS consistency, route integrity). This is not a transitional state — **the dual membrane is the target architecture** (§Why This Is Stronger Than Eliminating Cloudflare).

**The sovereign Rust outer membrane** (skunkBat HTTP detection, bearDog TLS, Caddy hardening, rate limiting, fail2ban) is the evolution target. As it achieves parity with Cloudflare's capabilities, the Cloudflare layer becomes **optional defense in depth**, not a dependency. Porkbun is the billboard — NS can redirect anywhere.

SURGE-01 (CDN mirror) **dropped** — Cloudflare IS the CDN. New item: **CF-DATA** — Cloudflare analytics → skunkBat `baseline.observe` (outer → inner data flow).

**Defense in depth and mathematics, not obscurity.** If we can't show how all K-Derm layers work and remain secure, it's a MacGuffin. sporePrint evolves to live topology visualization — rendering all layers from nestGate data and songBird heartbeats.

### Remaining Work

| ID | Task | Owner | Priority |
|----|------|-------|----------|
| ~~DUAL-CHECKOUT~~ | ~~Consolidate sporePrint to single checkout~~ | cellMembrane | **DONE** (`4ce165a`) — orphan removed, service fixed, membrane redeployed |
| SIGN-01-ACTIVATE | Deploy signing keys — **3 blockers identified** (see SIGN-01 AAR), handed off to cellMembrane | cellMembrane | HIGH |
| FP-DEPLOY | Deploy footPrint SPA to golgi — serve at `primals.eco/footprint/` | sporeGate | HIGH |
| TOPO-VIS | sporePrint live topology viz — petalTongue coord_handlers landed | petalTongue | HIGH |
| FLOCKGATE-MESH | songBird mesh has **zero peers** from flockGate — port 7700 not reachable on WG overlay | mesh team | HIGH |
| THREAT-ACTIVATE | Feed live threat data (122 IPs, 317 attempts) into skunkBat `baseline.observe` | skunkBat | MEDIUM |
| CF-DATA | Cloudflare analytics → skunkBat (outer → inner data flow) | skunkBat | MEDIUM |
| FP-PARITY | petalTongue visual parity with footPrint (12 VT areas) | petalTongue | MEDIUM |
| LIVE-ACTIVATE | `live.primals.eco` petalTongue NUCLEUS hosting | sporeGate | MEDIUM |

---

## 136a Delivery (Complete)

9/14 exposures closed: security headers (HSTS, CSP, X-Frame, nosniff), 404 fix, fail2ban, depot rate-limiting, JSON access logs, WireGuard key audit, cert renewal drill. All validated live on primals.eco. Full AAR: `handoffs/OUTER_MEMBRANE_HARDENING_AAR_136a.md`.

136b upstream evolution (4 cascades): cellMembrane DUAL-CHECKOUT fix + harvest split (`bfb1558`), projectNUCLEUS 26/26 clean sweep (`5e59790`), primalSpring checksums parser fix (`fb03030`), footPrint deep debt — 46 tests, AGPL, solver decomposed (`f258d42`), flockGate divergence + mesh gap AAR (`d64d8a9`). Earlier: skunkBat skunky-ingest, songBird drawbridge proxy, nestGate coord backend, bearDog hierarchy refactor.

---

## Gate Convergence

```
eastGate     — Overwatch. All 28 repos at HEAD. 4 cascades today. Converged.
sporeGate    — Hardened. DUAL-CHECKOUT resolved. SIGN-01 handed off.
golgiBody    — Caddy hardened, fail2ban active, rate-limited. sporePrint consolidated.
flockGate    — footPrint deep debt complete. WAN mesh gap surfaced (port 7700).
ironGate     — darkforest v3.0 active. projectNUCLEUS 26/26 clean sweep.
strandGate   — Enrollment pending. REALWORLD: physical access.
grapheneGate — Pending pepti pull. REALWORLD: ADB cable.
```

## Operator Task Audit — Agentic vs Realworld

Every task currently tagged "operator" or requiring manual intervention, classified:

### REALWORLD — Physical/Hardware Required (cannot be agentic)

| Task | Why Realworld | Gate |
|------|--------------|------|
| strandGate enrollment | Physical: cable ethernet, power on, OS install at house 2 | strandGate |
| grapheneGate pepti deploy | Physical: USB ADB cable to Pixel 8a, `adb push` ecobins | grapheneGate |
| ~~ODN-02 DNSSEC~~ | ~~Cloudflare + Porkbun~~ — **DONE** (Jul 11) | golgiBody |
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
| ~~SURGE-01~~ | ~~Manual GitHub Pages setup~~ | **DROPPED** — Cloudflare outer membrane already handles this | — |
| RustDesk client config | Manual per-gate change to point at `remote.primals.eco` | cellMembrane `gate.configure` could template RustDesk config at enrollment time | cellMembrane |

## Tests

| Suite | Tests | Scenarios | Status |
|-------|-------|-----------|--------|
| primalSpring | 1,104 | 132 | GREEN (v0.9.35) |
| groundSpring | 1,047+ | — | GREEN |
| skunkBat | 563 | — | GREEN |
| footPrint | 46 | — | GREEN (Vitest, V8 coverage) |
| projectNUCLEUS | 149 | — | GREEN (26/26 clean sweep) |

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
| `EXTERNAL_REVIEW_RESPONSE_136b.md` | Post-Cloudflare resilience analysis (corrected: CF never removed) |
| `KDERM_REAFFIRMATION_WAVE136b.md` | K-Derm topology reaffirmation — team responsibilities + DNSSEC path |
| `SPOREPRINT_DUAL_CHECKOUT_AAR_136b.md` | P1: dual checkout divergence — **RESOLVED** by cellMembrane `4ce165a` |
| `SPOREPRINT_CONSOLIDATION_SIGN01_AAR_136b.md` | DUAL-CHECKOUT resolution + SIGN-01 3-blocker analysis |
| `FLOCKGATE_DIVERGENCE_TOPOLOGY_AAR_136b.md` | Checksums parser fix + WAN mesh gap (port 7700) |
| `FOOTPRINT_COMPOSITION_AUDIT_AAR_WAVE136b.md` | Deep debt: 46 tests, AGPL, solver decomposed, ESLint/Vitest |
| `LIVE_THREAT_DATA_ACTIVATION_AAR_136b.md` | 122 attacker IPs, 317 SSH attempts — real adversarial data for skunkBat |
| `PRIMALSPRING_V0935_EVOLUTION_136b.md` | v0.9.35: 1,104 tests, 132 scenarios, checksums parser fix |
| `SKUNKY_INGEST_136b.md` | skunky-ingest operational spec |
| `NESTGATE_SESSION106_COORD_ACTIVATE_DEEP_DEBT_JUL11_2026.md` | nestGate coord backend + deep debt AAR |

*Wave 136b: 14 repos evolved across 4 cascades. DUAL-CHECKOUT **resolved** (cellMembrane `4ce165a`). SIGN-01 blockers identified and handed off. darkforest 26/26 clean sweep. footPrint deep debt complete (46 tests, AGPL, solver decomposed). flockGate WAN mesh gap surfaced (port 7700). DNSSEC live. K-Derm reaffirmed. Glacial: all 8 clear. 4 HIGH remain (SIGN-01-ACTIVATE, FP-DEPLOY, TOPO-VIS, FLOCKGATE-MESH). Every orthogonal dimension converging.*
