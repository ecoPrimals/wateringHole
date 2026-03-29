# ToadStool S166 — Deep Debt Evolution Handoff

**Date**: March 29, 2026
**Session**: S166
**Primal**: toadStool
**License**: AGPL-3.0-only

---

## Summary

Deep debt execution session completing capability-based evolution, production stub completion, smart file refactoring, dependency evolution, and workspace-wide lint cleanup. Net -7200 lines across 123 files.

## Changes

### Capability-Based Discovery (Breaking Pattern Change)
- All hardcoded primal names (`beardog`, `songbird`, `nestgate`, `squirrel`) deprecated in favor of capability IDs (`crypto`, `coordination`, `storage`, `routing`)
- New `resolve_capability_socket_fallback(capability, env)` with precedence: `BIOMEOS_{CAP}_SOCKET` → legacy env → `{capability}.sock`
- `ecosystem::capabilities` module with `COORDINATION`, `CRYPTO`, `STORAGE`, `ROUTING` constants
- Affects: `primal_sockets/`, `constants/ecosystem.rs`, `interned_strings.rs`, `cli/capability_helpers.rs`, `glowplug_client.rs`

### Workspace Lint Cleanup
- 29 lib.rs files cleaned of redundant `#![allow(clippy::...)]` that duplicated workspace `[lints]`
- Blanket `#![allow(clippy::nursery)]` removed from `server` and `cross-substrate-validation`
- All crates now consistently inherit workspace pedantic+nursery lints

### Production Stub Completion
- `crypto_lock/access_control/manager.rs`: `load_permissions()` reads from JSON file, `validate_delegation_request()` enforces holder match, delegation depth, time bounds, feature/geography subsets, resource limits
- `config/builder/substrate.rs`: `SubstrateConfig::validate()` checks power budget, fallback order, capability lists; `build()` returns `Result`

### Smart Refactoring (7 production files → module directories)
| File | Lines | New Modules |
|------|-------|-------------|
| `server/resource_validator.rs` | 986 | types, error, system_query, analysis, tests/ |
| `auto_config/ecosystem.rs` | 851 | constants, helpers, discoverer, tests/ |
| `gpu/engine/mod.rs` | 744 | types, init, devices, execution, meta, runtime_engine, defaults, tests/ |
| `display/capabilities.rs` | 735 | types, paths, operations, tests |
| `distributed/types/resources.rs` | 725 | requirements, core_conversions, retry, constraints, allocation, host_config, tests |
| `infant_discovery/engine.rs` | 715 | conversions, core, capability_discovery, tests |
| `universal/substrate.rs` | 717 | substrate_kind, capabilities, buffer, compute_substrate, adapter, tests |

All new files under 400 lines. Public API surfaces unchanged (re-exports from mod.rs).

### Dependency Evolution
- `md5` crate → `md-5` (RustCrypto family, consistent with existing `sha2` usage)
- `bollard` aligned to 0.18 workspace-wide (was 0.15 in workspace, 0.16 in container crate)

### Bug Fix
- `UniversalCloudOrchestrator::analyze_deployment_requirements`: Provider selection now intersects with compliance-allowed providers and sorts deterministically (was HashMap iteration order dependent)

## Quality Gates
- `cargo check --workspace --all-targets`: Clean
- `cargo fmt --all`: Clean
- `cargo test`: 3,947+ tests verified across modified crates, 0 failures
- Net: 123 files changed, +1,145/-8,334 lines

## Impact on Other Primals
- **Capability socket names changed**: Other primals discovering toadStool sockets should use `BIOMEOS_*_SOCKET` env vars or capability-based filenames (`crypto.sock`, `coordination.sock`, etc.) instead of primal-named sockets (`beardog.sock`, `songbird.sock`)
- Legacy env vars (`BEARDOG_SOCKET`, `SONGBIRD_SOCKET`) still work as fallback
- `bollard` version bump to 0.18 may affect container-using primals sharing the workspace

---

Part of [ecoPrimals](https://github.com/ecoPrimals) — sovereign compute for science and human dignity.
