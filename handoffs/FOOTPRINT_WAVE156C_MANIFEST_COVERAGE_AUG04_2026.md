# footPrint — Wave 156c: Manifest-Driven Sources + Coverage Expansion

**Date**: 2026-08-04 | **Gate**: ironGate | **From**: footPrint deep-debt session
**Commit**: `01e1adc` on `protoKarya/footPrint`

---

## Summary

Deep-debt elimination pass focused on three pillars:
1. **Manifest-driven source registration** — sources only activate when endpoints exist
2. **Constants centralization** — single source of truth, no scattered magic values
3. **Test coverage expansion** — 572 → 628 tests (+56), 7 new test files

---

## Changes Made

### Manifest-Driven Source Registration (P1 complete for runtime)

- New `src/client/source-registry.ts`: wraps 8 registrars, gates each on endpoint availability
- `app.ts` reduced from 8 imperative calls to single `registerAllSources()`
- Sources that cannot be satisfied (missing endpoints in registry) are silently skipped
- Michigan/Lansing data only registers when Michigan endpoints are bootstrapped

### Dynamic Category Boosts

- Removed hardcoded `Lansing: 0.6` / `Michigan: 0.4` from `src/types/spatial.ts`
- `deriveCategoryBoosts()` computes regional boosts from manifest coverage areas
- Universal categories (OSM, FEMA, USGS) retain intrinsic boosts
- Regional categories derive boost proportional to inverse coverage area

### Constants Centralization

| Constant | Source | Consumers |
|----------|--------|-----------|
| `CAS_PATH` | constants.ts | nestgate-cas.ts, server.ts, primals.ts |
| `CAS_FAMILY` | constants.ts | nestgate-cas.ts |
| `RPC_TIMEOUT_MS` | constants.ts | petal-tongue.ts |
| `NEURAL_API_TIMEOUT_MS` | constants.ts | neural-api.ts |
| `CACHE_KEY_HASH_LENGTH` | constants.ts | server.ts |

### Membrane Socket Default Unified

- `server.ts` no longer hardcodes fallback socket path
- `createNeuralApiClient()` resolution: `MEMBRANE_SOCKET` env → `/run/membrane/nestgate.sock`
- No more `biomeos.sock` vs `nestgate.sock` confusion

### Dead Code Removed

- `sendUserMessage()` — exported but zero call sites → removed
- `agentMessages[]` queue — written at line 239, never consumed → removed

### Michigan GIS Host → Manifest

- `gisp.mcgi.state.mi.us` removed from hardcoded `ALLOWED_HOSTS`
- Registered as `mi-gisp` endpoint in `manifest-defaults.ts`
- `endpointHosts()` now includes it automatically

### Test Coverage (+56 tests, 7 new files)

| File | Coverage Target |
|------|----------------|
| `nestgate-cas.test.ts` | CAS client CRUD + error handling |
| `storage.test.ts` | Dual-write persistence, graceful CAS failure |
| `discover.test.ts` | Capability scoring, auto-enable logic |
| `petal-tongue.test.ts` | JSON-RPC framing, timeout, reconnection |
| `server-bridge.test.ts` | WebSocket bridge, project.command flow |
| `source-registry.test.ts` | Manifest-gated registration |
| `spatial.test.ts` | Dynamic boost derivation |

---

## Current Metrics

| Metric | Value |
|--------|-------|
| Tests | 628 (43 files) |
| Statement coverage | 48.3% |
| TypeScript errors | 0 |
| ESLint errors | 0 |
| Format violations | 0 |
| Largest file | 604L (server.ts) |

---

## Remaining Evolutionary Targets (glacial priority)

### For footPrint

| Priority | Item | Effort |
|----------|------|--------|
| P2 | Declarative JSON source manifests (CAS-stored) | Medium |
| P2 | Municipality discovery (reverse geocode → source lookup) | Medium |
| P2 | Client E2E tests via Playwright (28 DOM modules at 0%) | High |
| P3 | CSP img-src derived from registered endpoint hostnames | Low |
| P3 | Protocol handlers (shared Overpass/ArcGIS fetch layer) | Medium |

### Upstream Dependencies

| Primal | Need | Status |
|--------|------|--------|
| nestGate | BTSP local-trust (SO_PEERCRED for same-gate UDS callers) | Blocks CAS write |
| songBird | Drawbridge route absorption (proxy → songBird) | Blocks Express removal |
| coralReef | GPU terrain batch (DEM raster → slope/contour) | Blocks terrain offload |

---

## Self-Knowledge Compliance

After this pass, footPrint's production code:
- Does NOT hardcode primal socket paths (env-configured via `MEMBRANE_SOCKET`)
- Does NOT hardcode data source URLs (manifest-driven via `getEndpoint()`)
- Does NOT assume which sources exist (manifest-gated registration)
- Does NOT hardcode category scoring (derived from coverage areas)
- DOES reference `nestGate` by name in comments/docs (acceptable for operator context)
- DOES assume `/ws` routes to petalTongue (deployment knowledge in Caddy config, not code)

---

*Sources are discovered, not hardcoded. Registration is conditional, not imperative.*
