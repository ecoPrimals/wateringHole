# biomeOS v2.41 — Deep Audit Handoff

**Date**: March 15, 2026
**Version**: 2.41
**Previous**: v2.40 (Spring Absorption Deep Debt)
**Status**: Production Ready

---

## Summary

Comprehensive 9-phase audit and evolution: CI hardening, sovereignty guardian integration with human dignity evaluation, tarpc forwarding implementation, zero-copy Arc<str> migration in socket discovery, incubation module refactoring, production code quality fixes, and foundation standardization (edition 2024, forbid(unsafe_code) on all binaries, SPDX completeness).

---

## Changes

### Phase 1: Foundation Fixes
- `rustfmt.toml` edition `2021` → `2024` (per wateringHole standards)
- `#![warn(missing_docs)]` added to `neural-api-client-sync` + all 5 doc warnings resolved
- `#![deny(unsafe_code)]` → `#![forbid(unsafe_code)]` in `biomeos-genome-extract`
- `#![forbid(unsafe_code)]` added to 4 binary crates: `federation`, `biomeos`, `biomeos-api`, `platypus`
- SPDX `AGPL-3.0-only` headers added to 5 `bin/chimeras/` files (now 100% SPDX coverage)

### Phase 2: CI Pipeline Hardening
- Clippy: `--lib` → `--all-targets` (tests, bins, benches now linted)
- Removed `continue-on-error` from: security audit, dependency check, integration tests
- Standards checks (TODO/FIXME, panic!) now fail CI (`exit 1`)
- File size check now enforced at 1000 lines
- Added coverage threshold enforcement (75% minimum via `--fail-under-lines`)
- Added `--all-features` to all `cargo test` commands

### Phase 3: Production Code Quality
- 4 `eprintln!` calls in library code → `tracing::warn!()` with structured fields
  - `biomeos-system/lib.rs`, `biomeos-graph/validation.rs`, `biomeos-graph/loader.rs`, `biomeos-core/observability/mod.rs`
- Added `tracing` dependency to `biomeos-system`
- Verified all `unwrap()`/`expect()`/`panic!` correctly confined to test code

### Phase 4: Hardcoded Values → Capability-Based
- STUN fallback `"127.0.0.1:3478"` → named `DEFAULT_STUN_FALLBACK` constant
- Added `BIOMEOS_STUN_FALLBACK_ADDRESS` env var override
- 4-tier discovery: config → runtime discovery → env var → named constant

### Phase 5: Sovereignty Guardian Integration
- Fixed 3 operator precedence bugs in data/privacy evaluation (`&&`/`||` without parens)
- Implemented `evaluate_human_dignity()`: discrimination detection, human oversight enforcement, manipulation prevention, right to explanation
- Integrated `pub mod sovereignty_guardian` into `biomeos-core/src/lib.rs` (was dead code)
- 5 new test cases covering full human dignity evaluation

### Phase 6: tarpc Implementation
- Implemented `forward_via_tarpc()` in NeuralRouter
- Replaces commented-out block with real tarpc-first-then-JSON-RPC fallback
- Derives tarpc socket path via `biomeos_primal_sdk::tarpc_transport::tarpc_socket_path()`
- 5-second connect timeout, 10-second response timeout, graceful fallback

### Phase 7: Zero-Copy Evolution (String → Arc<str>)
- `SocketDiscovery.family_id` → `FamilyId` (Arc<str>)
- `DiscoveredSocket.primal_name` → `Option<Arc<str>>`
- `TransportEndpoint` variants: `name`, `host` fields → `Arc<str>`
- `DiscoveryMethod::EnvironmentHint` → `Arc<str>`
- `DiscoveryStrategy.tcp_fallback_host` → `Arc<str>`
- `AtomicClient` constructors → `impl AsRef<str>`, store `Arc<str>`

### Phase 8: Smart Refactoring
- `incubation.rs` (934 lines) → 4-module structure (330+180+115+60)
  - `mod.rs`: Coordinator, `SporeIncubator`, public API
  - `local_entropy.rs`: System entropy gathering
  - `node_config.rs`: Config/result types
  - `tower_metadata.rs`: tower.toml extraction
- Full API compatibility preserved via re-exports

### Phase 9: Coverage Expansion
- 17 new tests across binary entry points and sovereignty guardian
- `src/bin/biome.rs`: 6 template content tests
- `src/bin/launch_primal.rs`: 3 path resolution tests
- `src/bin/nucleus.rs`: 3 argument parsing tests
- `sovereignty_guardian.rs`: 5 human dignity evaluation tests

### Cleanup
- Deleted `.project-status` (outdated since Feb 2026)
- Removed commented-out legacy code from `biomeos-core`: migration notes, `SongbirdClient` import, `ClientRegistry` import, `adapters` module declarations
- Updated all root docs (README, START_HERE, DOCUMENTATION, QUICK_START, CURRENT_STATUS) with accurate metrics
- Fixed redundant closure in `genome_dist/discovery.rs`
- Fixed unnecessary `to_string()` in `translation_loader.rs`
- Added docs to `RefreshReport` fields in `spore.rs`

---

## Dependencies Added
- `biomeos-system`: `tracing = "0.1"`
- `biomeos-atomic-deploy`: `biomeos-primal-sdk` (path dependency)

---

## Metrics

| Metric | v2.40 | v2.41 |
|--------|-------|-------|
| Tests | 4,946 | 5,017 (+71) |
| Ignored | 131 | 0 (-131) |
| Line Coverage | 76.15% | 77.61% (+1.46pp) |
| Function Coverage | 79.23% | 80.32% (+1.09pp) |
| Clippy | PASS (lib) | PASS (all-targets) |
| Format | PASS | PASS |
| Docs | PASS | PASS (-D warnings) |
| Unsafe | 0 | 0 |
| C deps | 0 | 0 |
| Files >1000 LOC | 0 (max 925) | 0 (max 920) |

---

## Files Modified

| Area | Files |
|------|-------|
| Foundation | `rustfmt.toml`, 5× `bin/chimeras/*.rs`, `genome-extract/main.rs`, `neural-api-client-sync/lib.rs`, `federation/main.rs`, `biomeos/main.rs`, `biomeos-api/main.rs`, `platypus/main.rs` |
| CI | `.github/workflows/ci.yml` |
| Code quality | `biomeos-system/lib.rs`, `biomeos-graph/validation.rs`, `biomeos-graph/loader.rs`, `biomeos-core/observability/mod.rs` |
| Hardcoding | `biomeos-core/stun_extension.rs` |
| Sovereignty | `biomeos-core/sovereignty_guardian.rs`, `biomeos-core/lib.rs` |
| tarpc | `biomeos-atomic-deploy/neural_router.rs`, `biomeos-atomic-deploy/Cargo.toml` |
| Zero-copy | `biomeos-core/socket_discovery/{engine,result,transport,strategy}.rs`, `biomeos-core/atomic_client.rs`, `biomeos-atomic-deploy/translation_loader.rs` |
| Refactoring | `biomeos-spore/incubation/{mod,local_entropy,node_config,tower_metadata}.rs` |
| Coverage | `src/bin/{biome,launch_primal,nucleus}.rs` |
| Docs | `README.md`, `START_HERE.md`, `DOCUMENTATION.md`, `QUICK_START.md`, `CURRENT_STATUS.md` |
| Cleanup | `.project-status` (deleted), `biomeos-core/{lib,p2p_coordination,universal_biomeos_manager}` |

---

## Next Evolution

1. **Coverage 77.61% → 90%**: Primary targets are `main.rs` (43%), `model_cache.rs` (67%), `nucleus` mode (65%), `api` mode (38%)
2. **tarpc primal servers**: Primals need to implement tarpc endpoints for the NeuralRouter to use the new `forward_via_tarpc()` path
3. **Shell scripts → Rust**: 18 .sh scripts remain as deployment tooling; evolution path per EVOLUTION_PATH spec
4. **Python STUN server**: `scripts/mini_stun_server.py` awaiting Songbird pure Rust STUN
5. **String → Arc<str>**: Remaining handler struct fields outside socket discovery
6. **Duplicate templates**: `niches/templates/` vs `templates/niches/` deduplication
7. **plasmidBin/tower/tower**: Mock shell script → real binary or documentation
