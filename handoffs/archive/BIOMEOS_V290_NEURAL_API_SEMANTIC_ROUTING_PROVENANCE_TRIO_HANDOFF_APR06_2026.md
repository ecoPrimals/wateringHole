<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->

# biomeOS v2.90 — Neural API Semantic Routing + Provenance Trio + Composition Health

**Date**: April 6, 2026
**From**: biomeOS → primalSpring, wetSpring, all spring teams
**Status**: NUCLEUS UNBLOCKED — Live deployment path open

## Summary
Three HIGH-priority gaps identified by primalSpring/wetSpring resolved in one release.

## Version History
| Version | Change |
|---------|--------|
| v2.90 | Neural API semantic fallback, 32 provenance trio translations, composition health canonical namespace |

## Gap 1: Neural API Semantic Method Fallback (was: BLOCKS LIVE NUCLEUS)
- **Problem**: Springs calling `provenance.begin`, `birdsong.decrypt` as top-level JSON-RPC → MethodNotFound (-32601)
- **Solution**: Universal semantic routing fallback — any `domain.operation` method not in ROUTE_TABLE automatically routes through `capability.call` via CapabilityTranslationRegistry
- **How it works**: `lookup_route()` miss → `split_once('.')` → `capability.call({ capability: domain, operation: op, args: params })`
- **Precedence**: Explicit ROUTE_TABLE entries (graph.*, topology.*, health.*, etc.) always win
- **Renamed**: `MeshCapabilityCall` → `SemanticCapabilityCall` (same mechanic, broader scope)
- **Tests**: 5 new tests (provenance.begin, birdsong.decrypt, dag.dehydrate, composition.tower_health, multipart methods)

## Gap 2: RootPulse Graph Execution
- **Problem**: rootpulse TOML workflows use `capability_call` nodes with domains like `dag.dehydrate`, `commit.session`, `provenance.create_braid` — no translations existed
- **Solution**: 32 new translations across 3 provenance trio domains:
  - **dag** (rhizoCrypt): create_session, dehydrate, rehydrate, get_session, list_sessions, add_vertex, slice + aliases
  - **commit** (LoamSpine): session, append, get, list + spine/permanent_storage aliases
  - **attribution** (sweetGrass): create_braid, get_braid, verify + braid/attribution aliases
  - **birdsong** legacy aliases → BearDog beacon (decrypt/encrypt)
- **Environment providers**: `BIOMEOS_DAG_PROVIDER`, `BIOMEOS_HISTORY_PROVIDER`, `BIOMEOS_ATTRIBUTION_PROVIDER`
- **Result**: `rootpulse_commit.toml` and all 5 rootpulse graphs now resolve all capability_call nodes

## Gap 3: Composition Health Canonical Namespace
- **Problem**: gen3 uses `composition.tower_health`, gen4 uses `composition.webb_*_health`, springs use `composition.science_health` — no canonical registry
- **Solution**: `composition` domain added to CAPABILITY_DOMAINS (biomeOS-local provider). 9 translations:
  - `composition.health` (canonical)
  - `composition.tower_health` (gen3)
  - `composition.service_health`
  - `composition.science_health` (springs)
  - `composition.webb_health`, `composition.webb_compute_health`, `composition.webb_storage_health`, `composition.webb_network_health` (gen4)
  - `composition.nucleus_health`
  - All normalize to `composition.health` on biomeOS-local

## For Downstream Primals
- Springs deploying NUCLEUS: the Neural API now accepts ANY `domain.operation` method and routes through capability layer
- No spring-side code changes required — existing `provenance.begin`, `birdsong.decrypt` calls will work
- Provenance trio (rhizoCrypt/LoamSpine/sweetGrass): register capabilities as usual; translations resolve automatically
- Composition health callers: use any of the 9 aliases; they all normalize to `composition.health`

## Quality Gates
- All workspace tests pass (0 failures, 0 ignored)
- clippy PASS, fmt PASS
- Zero unsafe, zero deprecated APIs

## Verification
```bash
cargo test --workspace --all-features -q
cargo clippy --workspace --all-targets --all-features -- -D warnings
```

---

*© 2025–2026 ecoPrimals — AGPL-3.0-or-later / CC-BY-SA-4.0 / ORC*
