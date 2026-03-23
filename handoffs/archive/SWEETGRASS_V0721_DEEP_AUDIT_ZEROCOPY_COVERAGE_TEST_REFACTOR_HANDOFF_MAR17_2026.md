# SweetGrass v0.7.21 — Deep Audit: Zero-Copy, Handler Coverage, Test Refactor

**Primal**: sweetGrass (phase2/sweetGrass)
**Version**: v0.7.21
**Date**: 2026-03-17
**Previous**: v0.7.20 (archived)

---

## Summary

Comprehensive audit execution: zero-copy `Arc<str>` for `Braid.mime_type` across
all 7 crates, hardcoded primal name eliminated, 28 new JSON-RPC handler tests
expanding coverage across all domains, and smart refactor of oversized test file
(1,448 lines → 5 domain-organized submodules, all under 1,000 lines).

## Changes

### P1: Zero-Copy Evolution

| Change | Detail |
|--------|--------|
| `Braid.mime_type: String` → `Arc<str>` | Cross-crate migration: core (braid, builder), store (memory indexes), store-sled, store-redb, store-postgres (bind), query (engine, `AgentContributions.by_mime_type`). MIME type indexes share `Arc<str>`, eliminating per-query allocations on hot paths. |
| Wire types evaluated | `ContributionRecord`, `PrimalInfo`, `SessionContributions` fields left as `String` — single-use deserialization types, not hot-path. |

### P2: Hardcoding Eliminated

| Change | Detail |
|--------|--------|
| `"sweetgrass".to_string()` → `PRIMAL_NAME` | `jsonrpc/contribution.rs` now uses canonical `sweet_grass_core::identity::PRIMAL_NAME` constant. Primal code only has self-knowledge. |

### P3: Test Coverage Expansion

| Change | Detail |
|--------|--------|
| +28 JSON-RPC handler tests | Coverage for `anchoring.anchor`, `anchoring.verify`, `attribution.chain`, `attribution.calculate_rewards`, `attribution.top_contributors`, `braid.commit`, `compression.compress_session`, `compression.create_meta_braid`, `provenance.graph`, `provenance.export_provo`, `provenance.export_graph_provo`, `contribution.record_dehydration`, `pipeline.attribute`. |
| Tests include | Success paths, not-found errors, invalid params, custom spine IDs, zero-value rewards, empty summaries, no-agents fallback, depth parameters, hash validation. |

### P4: Smart Test Refactor

| Change | Detail |
|--------|--------|
| `jsonrpc/tests.rs` (1,448 → 480 lines) | Split into 5 domain test modules matching the handler structure. |
| `tests_anchoring.rs` | All `anchoring.*` tests (~220 lines) |
| `tests_attribution.rs` | All `attribution.*` tests (~200 lines) |
| `tests_compression.rs` | All `compression.*` tests (~120 lines) |
| `tests_contribution.rs` | All `contribution.*` + `pipeline.*` tests (~220 lines) |
| `tests_provenance.rs` | All `provenance.*` tests (~170 lines) |

### P5: Clippy Pedantic Fixes

| Change | Detail |
|--------|--------|
| `#[must_use]` on test allocators | `allocate_test_port()` and `allocate_test_ports()` annotated per clippy pedantic. |
| `float_cmp` fix | `assert_eq!` on `f64` replaced with epsilon-based `assert!`. |
| `clone_on_ref_ptr` | `Arc::clone(&x)` used instead of `x.clone()` for `Arc<str>`. |

### Codebase Scan Results (Clean)

| Item | Status |
|------|--------|
| Mocks in production | **None** — all gated to `#[cfg(test)]` or `feature = "test"` |
| `unsafe` blocks | **None** — all crates use `#![forbid(unsafe_code)]` |
| C/C++ dependencies | **None** — deny.toml blocks openssl, ring, etc. |
| `unwrap()` / `expect()` in production | **None** — only `unwrap_or()` with defaults |
| TODO/FIXME in source | **None** |
| Files over 1,000 lines | **None** (max: 808) |
| `#[allow]` remaining | **2** — both `dead_code` on conditionally-compiled mock impls (correct pattern) |

## Metrics

| Metric | Value |
|--------|-------|
| Version | v0.7.21 |
| Tests | 1,077 (+28 from v0.7.20) |
| .rs files | 133 (+5 domain test modules) |
| JSON-RPC methods | 24 |
| Clippy warnings | 0 (pedantic + nursery) |
| Unsafe blocks | 0 |
| `#[allow]` attrs | 2 (both justified) |
| Max file size | 808 lines (was 1,448) |
| tarpc | 0.37 |
| Edition | 2024 |
| MSRV | 1.87 |

## Files Changed

### New
- `crates/sweet-grass-service/src/handlers/jsonrpc/tests_anchoring.rs`
- `crates/sweet-grass-service/src/handlers/jsonrpc/tests_attribution.rs`
- `crates/sweet-grass-service/src/handlers/jsonrpc/tests_compression.rs`
- `crates/sweet-grass-service/src/handlers/jsonrpc/tests_contribution.rs`
- `crates/sweet-grass-service/src/handlers/jsonrpc/tests_provenance.rs`

### Significantly Modified
- `crates/sweet-grass-core/src/braid/mod.rs` — `mime_type: Arc<str>`
- `crates/sweet-grass-core/src/braid/builder.rs` — `Arc<str>` conversion
- `crates/sweet-grass-store/src/memory/indexes.rs` — `HashMap<Arc<str>, _>`
- `crates/sweet-grass-query/src/engine/mod.rs` — `AgentContributions.by_mime_type: HashMap<Arc<str>, usize>`
- `crates/sweet-grass-service/src/handlers/jsonrpc/contribution.rs` — `PRIMAL_NAME` constant
- `crates/sweet-grass-service/src/handlers/jsonrpc/tests.rs` — trimmed to core/braid/health/helpers
- `crates/sweet-grass-service/src/handlers/jsonrpc/mod.rs` — registered 5 new test modules

### Updated (Arc<str> compatibility)
- `crates/sweet-grass-store-sled/src/store/mod.rs` — `&*braid.mime_type` comparison
- `crates/sweet-grass-store-redb/src/store/mod.rs` — `&*braid.mime_type` comparison
- `crates/sweet-grass-store-postgres/src/store/mod.rs` — `.bind(&*braid.mime_type)`
- Test files across 8 crates — `&*braid.mime_type` assertions
- Root docs: README, CHANGELOG, ROADMAP, DEVELOPMENT, QUICK_COMMANDS, specs
- Config: capability_registry.toml, sweetgrass_deploy.toml, deploy.sh
- Showcase: 00_START_HERE, README

## Ecosystem Alignment

| Pattern | sweetGrass | rhizoCrypt | loamSpine | airSpring | neuralSpring |
|---------|------------|------------|-----------|-----------|--------------|
| `Arc<str>` identifiers | v0.7.0+ | v2.0+ | v0.90+ | v0.8+ | S150+ |
| `Arc<str>` mime_type | v0.7.21 | N/A | N/A | N/A | N/A |
| `PRIMAL_NAME` constant | v0.7.21 | `PRIMAL_NAME` | `PRIMAL_NAME` | `PRIMAL_NAME` | `PRIMAL_NAME` |
| Zero production unwrap | v0.7.0+ | v2.0+ | v0.90+ | v0.8+ | S150+ |
| 1,000-line file limit | v0.7.21 | v2.3+ | v0.94+ | v0.8.7 | S160 |
| tarpc 0.37 | v0.7.18 | v2.3+ | v0.94+ | v0.8.7 | S160 |
| Edition 2024 | v0.7.17 | v2.3+ | v0.94+ | v0.8.7 | S160 |

## Next Steps

- P3: 90% llvm-cov target, E2E tests against running server, chaos/fault expansion
- Manifest-based discovery, FAMILY_ID socket paths, temp-env crate for testing
- Production IPC wiring: `extract_rpc_error` in tarpc clients, `extract_capabilities` in discovery
- Content Convergence experiment (ISSUE-013)
- sunCloud integration for reward distribution
