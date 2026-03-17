# SweetGrass v0.7.20 — IPC Timeout, extract_rpc_error, Capability Parsing, Proptest

**Primal**: sweetGrass (phase2/sweetGrass)
**Version**: v0.7.20
**Date**: 2026-03-16
**Previous**: v0.7.19 (archived)

---

## Summary

Deep debt execution: IPC timeout variant, JSON-RPC error extraction helper, dual-format
capability parsing for cross-primal interop, property-based testing, smart refactoring of
duplicated query/braid-lookup patterns. All `#[allow(unused_imports)]` eliminated via cfg alignment.

## Changes

### P1: IPC & Security Hardening

| Change | Detail |
|--------|--------|
| `deny.toml` `yanked = "deny"` | Yanked crates now block builds (was `warn`). Aligned with airSpring v0.8.7, neuralSpring S160. |
| `IpcErrorPhase::Timeout` | New variant for explicit timeout phase. `is_retriable()` = true, `is_timeout_likely()` = true. Aligned with neuralSpring S160 `IpcError::Timeout`. |
| `extract_rpc_error()` | Extracts `(code, message)` from JSON-RPC 2.0 error responses. Handles missing message (defaults to "unknown error"). Aligned with airSpring v0.8.7 + neuralSpring S160 patterns. |

### P2: Ecosystem Interop

| Change | Detail |
|--------|--------|
| `extract_capabilities()` | Dual-format parser for `capability.list` responses. Handles flat array (`{"methods": [...]}`) and structured domains (`{"domains": {"braid": ["create"]}}`). Handles `result` wrapper, `capabilities` alias (neuralSpring S156), deduplication, sorting. |
| Proptest properties (6) | `extract_rpc_error` roundtrip + never-panics, `IpcErrorPhase` display/retriable consistency, `extract_capabilities` flat roundtrip + never-panics. |

### Refactoring

| Change | Detail |
|--------|--------|
| `require_braid_by_hash()` | server/mod.rs: 4 methods (`attribution_chain`, `calculate_rewards`, `top_contributors`, `export_provo`) deduplicated via shared helper. |
| `ValidatedFilter` + `bind_filter!` | store-postgres: eliminated duplicated WHERE clause building and parameter binding between main query and count query. |
| `#[allow(unused_imports)]` removed (2) | `lib.rs` mock re-exports aligned to `#[cfg(any(test, feature = "test"))]`. |
| `discovery` module public | Enables `sweet_grass_integration::discovery::extract_capabilities`. |
| `error` module public | Enables `sweet_grass_integration::error::extract_rpc_error`. |

### Codebase Scan Results (Clean)

| Item | Status |
|------|--------|
| Mocks in production | **None** — all gated to `#[cfg(test)]` or `feature = "test"` |
| `unsafe` blocks | **None** — all crates use `#![forbid(unsafe_code)]` |
| C/C++ dependencies | **None** — deny.toml blocks openssl, ring, etc. |
| `unwrap()` / `expect()` in production | **None** — only `unwrap_or()` with defaults |
| `eprintln!` in production | **None** — only `println!` in CLI output |
| `#[allow]` remaining | **2** — both `dead_code` on conditionally-compiled mock impls (correct pattern) |

## Metrics

| Metric | Value |
|--------|-------|
| Version | v0.7.20 |
| Tests | 1,049 (+19 from v0.7.19) |
| JSON-RPC methods | 24 |
| Clippy warnings | 0 (pedantic + nursery) |
| Unsafe blocks | 0 |
| `#[allow]` attrs | 2 (both justified) |
| tarpc | 0.37 |
| Edition | 2024 |
| MSRV | 1.87 |

## Files Changed

### New / Significantly Modified
- `crates/sweet-grass-integration/src/error.rs` — `IpcErrorPhase::Timeout`, `extract_rpc_error()`, proptest properties
- `crates/sweet-grass-integration/src/discovery/mod.rs` — `extract_capabilities()`, `ConnectionFailed` field docs
- `crates/sweet-grass-integration/src/discovery/tests.rs` — `extract_capabilities` tests + proptest
- `crates/sweet-grass-integration/src/lib.rs` — public `discovery` + `error` modules, re-exports
- `crates/sweet-grass-service/src/server/mod.rs` — `require_braid_by_hash()` helper
- `crates/sweet-grass-store-postgres/src/store/mod.rs` — `ValidatedFilter` + `bind_filter!` macro
- `deny.toml` — `yanked = "deny"`

### Updated
- `crates/sweet-grass-integration/src/listener/mod.rs` — removed `#[allow(unused_imports)]`
- `crates/sweet-grass-integration/src/anchor/mod.rs` — removed `#[allow(unused_imports)]`
- Root docs: README, CHANGELOG, ROADMAP, DEVELOPMENT, QUICK_COMMANDS, specs
- Showcase: 00_START_HERE, README
- Config: capability_registry.toml, sweetgrass_deploy.toml, deploy.sh

## Ecosystem Alignment

| Pattern | sweetGrass | rhizoCrypt | loamSpine | airSpring | neuralSpring |
|---------|------------|------------|-----------|-----------|--------------|
| `IpcErrorPhase::Timeout` | v0.7.20 | v2.3+ | v0.94+ | v0.8.7 | S160 |
| `extract_rpc_error()` | v0.7.20 | - | - | v0.8.7 | S160 |
| `extract_capabilities()` | v0.7.20 | - | - | - | S156 |
| `yanked = "deny"` | v0.7.20 | v2.3+ | v0.94+ | v0.8.7 | S160 |
| `DispatchOutcome` | v0.7.19 | v2.3+ | - | - | - |
| `OrExit` | v0.7.19 | - | - | - | - |
| `health.liveness/readiness` | v0.7.19 | v2.3+ | v0.94+ | v0.8.7 | S160 |
| tarpc 0.37 | v0.7.18 | v2.3+ | v0.94+ | v0.8.7 | S160 |
| Edition 2024 | v0.7.17 | v2.3+ | v0.94+ | v0.8.7 | S160 |

## Next Steps

- P3: Manifest-based discovery, FAMILY_ID socket paths, temp-env crate for testing
- Production IPC wiring: `extract_rpc_error` in tarpc clients, `extract_capabilities` in discovery
- Content Convergence experiment (ISSUE-013)
