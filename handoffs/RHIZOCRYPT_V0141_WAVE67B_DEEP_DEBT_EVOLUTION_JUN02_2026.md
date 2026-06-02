# rhizoCrypt v0.14.1 — Wave 67B Deep Debt Evolution Sprint

**Date**: 2026-06-02
**Primal**: rhizoCrypt
**Version**: 0.14.1
**Gate**: strandGate

## Summary

Continued evolution sprint for provenance trio readiness and structural debt reduction. All changes build, test (1,655 passing), and clippy-clean (0 warnings).

## Changes

### Discovery Wiring (Critical Path for Trio)

- **Eager peer population**: `register_with_discovery` now returns the connected `DiscoveryClient`. `serve_with_tcp` calls `populate_registry()` at startup so the engine's `DiscoveryRegistry` is seeded with peer endpoints immediately — capability clients (signing, permanent storage, provenance) no longer wait for their first lazy query. Lazy fallback via `set_discovery_source` remains active.

### Structural Extraction

- **Neural API announce extracted**: `announce_to_biomeos`, `discover_neural_api_socket`, and `send_jsonrpc_uds` moved from `lib.rs` (712→589 lines) into `neural_api.rs` (141 lines). Keeps all production files under the 700-line limit.
- **Clippy doc-markdown fix**: Backticked `dag.partial_dehydrate` in test module doc comment.

### Docs Reconciliation

- README, CONTEXT, DEPLOYMENT_CHECKLIST, and sporeprint/validation-summary metrics aligned to 180 `.rs` files, 1,655 tests, max 686L production file.

## Stadial Gate

| Metric | Value |
|--------|-------|
| Tests | 1,655 passing (all features) |
| Clippy | 0 warnings |
| Source files | 180 `.rs` |
| Max production file | 686 lines (`service.rs`) |
| unsafe blocks | 0 |

## Ecosystem Blockers (Unchanged)

- Songbird `ipc.watch` — awaiting Phase 1 mesh validation
- `live-clients` tarpc feature — awaiting gate deployment
- `provenance.create_braid` — awaiting sweetGrass v0.8.0
- Cross-gate compute dispatch — awaiting biomeOS `compute.dispatch`

## Next Local Targets

- `Session` encapsulation (private fields + accessors/snapshot views)
- `PresenceVerifier` → real BTSP auth when bearDog S4 lands
- `IntegrationStatus` → true health checks
