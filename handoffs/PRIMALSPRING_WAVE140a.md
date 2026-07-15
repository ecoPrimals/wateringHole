# primalSpring Wave 140a — Tangibles Pivot Validation

**Date**: 2026-07-15 | **From**: primalSpring overwatch (eastGate)
**Version**: v0.9.38 → 166 scenarios, 1,198 tests, 0 failures

---

## Sprint Summary

Absorbed Wave 140a cascade. Fixed protist category recognition, delivered 4 new
composition scenarios closing the "MISSING" gap identified in the blurb.
primalSpring now validates the full protoKarya tangibles pipeline structurally.

## Changes

### Fixes

| Fix | What |
|-----|------|
| `VALID_CATEGORIES` | Added `"protist"` — footPrint/tideGlass now pass schema validation |
| `forgejo_repo` optionality | Protists and `composition_status = "planned"` repos don't require forgejo_repo |
| `KNOWN_DEBT` alignment | Removed `sporeprint-pure-primal-parity` (now passes), corrected `graphenegate-readiness` to 1 |

### New Scenarios (4)

| Scenario | Track | What it proves |
|----------|-------|----------------|
| `footprint-drawbridge-live` | Lifecycle | E2E: USGS/FEMA GIS bonds → songBird http.proxy → nestGate CAS |
| `tideglass-composition-routing` | Lifecycle | Deploy graph: barraCuda compute + petalTongue viz + science bonds + manifest |
| `protokarya-cross-feed` | Lifecycle | Protist mesh: footPrint data → CAS → tideGlass via capability.call + ipc.discover |
| `drawbridge-consumer-parity` | Security | Bond inventory integrity: all bonds have hosts, consumers, tiers; no orphans |

### Metrics Delta

| Metric | Before (140a cascade) | After |
|--------|----------------------|-------|
| Scenarios | 162 | 166 |
| Tests | 1,194 | 1,198 |
| Failures | 0 | 0 |
| Known debt | 1 (graphenegate-readiness) | 1 |

---

## What These Scenarios Prove

### footprint-drawbridge-live
- 5 GIS bonds (USGS, FEMA, NRCS, OSM×2) declared with footPrint as consumer
- songBird owns http.proxy (drawbridge transport layer)
- nestGate CAS pipeline (storage.store) routable for response caching
- Composition wiring: bonds → consumers → cache policy → CAS
- Live surface: composition URL in manifest, upstream hosts declared

### tideglass-composition-routing
- Compute pipeline: tensor.matmul, math.matvec, math.stats → barraCuda
- Visualization: petalTongue renders charts/graphs
- Science bonds: PubChem, Entrez, UniProt declared with protoKarya consumer
- Deploy graph: all 5 required primals in registry
- Manifest: tideGlass registered as protist with composition URL

### protokarya-cross-feed
- Production: nestGate storage.store* for CAS output
- Consumption: storage.fetch* + ipc.discover for sibling data
- Routing: capability.call and capability.discover registered
- Shared domains: storage, discovery, tensor all non-empty
- Cross-feed bridge: storage + http + compute sections present

### drawbridge-consumer-parity
- Bond inventory: ≥10 bonds, all with hosts, all with consumers
- Consumer consistency: unique consumers tracked, all bonds tiered
- songBird ownership: discovery domain, http.proxy registered
- Trust tiers: scientific, community, commercial, municipal all present
- Fragility: municipal bonds marked fragile

---

## Remaining MISSING (from blurb)

| Scenario | Status | Notes |
|----------|--------|-------|
| `protokarya-wan-deploy` | NOT YET | Requires live Caddy route config + composition manifest — blocked on footPrint server deploy |

This scenario validates actual WAN deployment (`*.primals.eco` routes), which depends
on upstream teams completing the footPrint server composition and Caddy block configuration.
primalSpring can create the structural validation once `footprint_composition.toml` exists.

---

## Upstream Gaps Surfaced

| Gap | Owner | Priority |
|-----|-------|----------|
| `footprint_composition.toml` doesn't exist yet | overwatch | P1 |
| tideGlass not yet cloned into workspace | overwatch | P2 |
| No `storage.query` method (protist data discovery) | nestGate team | P2 |
| `capability.call` / `capability.discover` not yet routable | NUCLEUS | P1 |
| Caddy blocks for protist composition URLs | cellMembrane team | P1 |

---

*Wave 140a: protoKarya tangibles validated structurally. 4 new scenarios.
166 scenarios, 1,198 tests, 0 failures. Newton-Leibniz convergence holds.*
