# biomeOS v3.31 — Phase 56 Gap Resolution Handoff

**Date**: April 29, 2026
**From**: biomeOS team
**To**: Ecosystem (primalSpring, ludoSpring, petalTongue, all downstream consumers)
**Previous**: v3.30 (deep debt cleanup)
**Audit source**: primalSpring v0.9.24 Phase 56 — Desktop NUCLEUS live deployment (12 primals)

---

## Summary

v3.31 resolves all 4 biomeOS gaps identified during primalSpring's Phase 56 live Desktop NUCLEUS deployment, plus absorbs the bash symlink workarounds into native Neural API behavior.

## Changes

### GAP-13 (P1): Fix storage capability routing

`capability_call.rs`: when a translation exists (e.g., `storage.store` → NestGate), the handler now **prefers the provider declared in the translation registry** over `providers[0]` (discovery insertion order). Previously, if ToadStool also advertised storage capabilities and was discovered first, `capability.call` with `capability="storage"` would route to ToadStool instead of NestGate.

**Impact**: `capability.call { capability: "storage", operation: "store" }` now correctly routes to NestGate.

### GAP-14 (P1): Unified graph parser

Three separate graph parsers (neural-api, deploy CLI, continuous CLI) previously required different TOML schemas. Now:

1. **`graph.save`** wraps serialized TOML under `[graph]` so saved files round-trip through both `Graph::from_toml_str` and `DeploymentGraph` parsing
2. **`load_as_deployment_graph()`** dual-parser: tries native `DeploymentGraph` first, falls back to `Graph::from_toml_str` + `neural_to_deployment()` converter
3. **`graph.start_continuous`** and **`graph.execute_pipeline`** now use this unified loader

**Impact**: A single graph TOML file now works across all three execution paths. Springs no longer need dual `id`+`name` workarounds.

### GAP-15 (P1): Fix graph.start_continuous for runtime-injected graphs

Runtime graphs saved via `graph.save` can now be started as continuous sessions. The `[graph]`-wrapped save format + dual-parse loader eliminates the schema mismatch that caused `Failed to parse DeploymentGraph` errors.

**Impact**: `graph.save` → `graph.start_continuous` flow now works for game loop graphs.

### GAP-16 (P2): Fix graph.execute node dispatch

- Added `register_only` as an alias for `register_capabilities` in the executor (used in 10+ deployment graphs)
- Nodes with a capability selector (`by_capability` or non-empty `capabilities`) now dispatch as `capability_call` even if the operation name is unrecognized, instead of being silently skipped

**Impact**: Desktop graphs with `by_capability` nodes execute correctly instead of skipping all nodes as "unknown type".

### Symlink absorption

`capability.resolve` RPC already existed in the Neural API route table. With GAP-13's routing fix, the resolution chain now correctly prefers the translation registry's provider. Springs can call `capability.resolve { capability: "storage" }` to get the correct socket path instead of creating filesystem symlinks.

**Target pattern**: Primals register capabilities → Neural API resolves them → springs discover by capability name. No bash, no symlinks, no hardcoded socket paths.

## Verification

- `cargo check`: PASS
- `cargo clippy -D warnings`: PASS (0 warnings, pedantic+nursery)
- `cargo fmt --check`: PASS
- `cargo test --workspace`: 7,814+ passing (1 pre-existing env-dependent skip)

## Impact on Downstream

- **primalSpring**: `desktop_nucleus.sh` symlinks can be replaced with `capability.resolve` calls
- **ludoSpring**: Game loop graphs can use `graph.save` → `graph.start_continuous` flow
- **All springs**: Single graph TOML format works for all execution paths

## Gaps NOT addressed (other primal teams)

| Gap | Owner | Description |
|-----|-------|-------------|
| GAP-01 | petalTongue | Hardcodes heartbeat to `discovery-service.sock` |
| GAP-03 | Squirrel | HTTP inference provider URLs treated as UDS paths |
| GAP-17 | petalTongue | Not discoverable via `visualization` capability |
| GAP-19 | ludoSpring | Not discoverable via `game_science` capability |
| GAP-22 | rhizoCrypt | `dag.session.create` errors on capability socket |
| GAP-23 | BearDog | `crypto.blake3_hash` errors on capability socket |

---

**Status**: Production Ready (v3.31)
**Tests**: 7,814+ passing | **Clippy**: 0 warnings | **C deps**: 0 | **Unsafe**: 0 | **Blocking debt**: 0
