<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.11 — Deep Lint & Evolution Sprint

**Date**: 2026-03-17
**Primal**: Squirrel
**Version**: 0.1.0-alpha.11
**Sprint**: Deep Lint Evolution — Idiomatic Rust, C Dependency Removal, Stub Completion
**Previous**: SQUIRREL_V010A10_DEEP_AUDIT_EVOLUTION_HANDOFF_MAR17_2026

---

## Summary

Comprehensive lint tightening and idiomatic Rust evolution across all 22 crates.
Reduced `#[allow]` blocks from ~50 to ~18 lints per crate, exposing and fixing
170+ Clippy violations. Replaced the `sysinfo` C dependency with pure Rust `/proc`
parsing. Completed the `UnifiedPluginManager` stub. Added human dignity evaluation
to AI routing. Evolved hardcoded credentials and IPs to env-var and capability-based
discovery. Added `rust-toolchain.toml` and `justfile` for reproducible builds.

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all --check` | PASS |
| `cargo clippy --all-features --all-targets -- -D warnings` | PASS (zero warnings) |
| `cargo test --workspace --all-features` | 2,059 pass / 0 stable failures |
| `cargo doc --workspace --no-deps` | PASS |
| Files > 1000 lines | 0 (max: 991) |
| Coverage | 69% (target: 90%) |
| TODO/FIXME in source | 0 |
| Hardcoded credentials | 0 |
| Unsafe code | 0 (`#![forbid(unsafe_code)]` all crates) |

## Changes

### Lint Gate Tightening (P0)

Reduced crate-level `#[allow]` blocks in `squirrel` and `squirrel-mcp`:

- `clippy::unwrap_used` / `clippy::expect_used` → `#[cfg_attr(test, allow(...))]`
- Fixed 42 Clippy errors in `squirrel-mcp` (17 `unwrap()` in production → `map_err()`)
- Fixed 103 Clippy errors in `squirrel` main crate
- Remaining architectural allows documented: `unused_async`, `unused_self`,
  `needless_pass_by_ref_mut`, `return_self_not_must_use` (require API redesign)

### Pure Rust `sys_info` (P0 — ecoBin v3.0)

Replaced `sysinfo` crate (C dependency) with `universal-constants::sys_info`:

- `memory_info()` — `/proc/meminfo` parsing
- `process_rss_mb()` — `/proc/self/status` VmRSS
- `cpu_count()` — `std::thread::available_parallelism()`
- `uptime_seconds()` — `/proc/uptime`
- `hostname()` — `rustix::system::uname()`
- `system_cpu_usage_percent()` — `/proc/stat` delta sampling
- Graceful fallbacks for non-Linux platforms
- `sysinfo` removed from all `Cargo.toml` files; `system-metrics` feature gate removed

### tarpc Client Protocol Negotiation (P0)

`SquirrelClient::connect()` now performs the `PROTOCOLS: ...` handshake using
`negotiate_client` on `UniversalTransport`. Bails with error if server doesn't
select `tarpc`. New `from_negotiated_transport` method; old `from_transport` deprecated.

### UnifiedPluginManager Completion (P1)

Replaced Phase 2 stub with full implementation:

- `UnifiedPluginManager` — load, unload, list, get, shutdown lifecycle
- `PluginEventBus` — topic-based pub/sub for plugin events
- `PluginSecurityManager` — capability-based permission checks
- `ManagerMetrics` — load/unload/error counters
- Comprehensive test suite

### Human Dignity Evaluation (P1)

New `crates/main/src/api/ai/dignity.rs`:

- `DignityEvaluator` — keyword-based checks for discrimination, human oversight,
  manipulation prevention, and explainability
- `DignityGuard` — configurable enforcement wrapper (block vs warn)
- Integrated into `api::ai` module
- Full test coverage for all check categories

### Hardcoding Evolution (P1)

- Dev credentials: `SQUIRREL_DEV_JWT_SECRET`, `SQUIRREL_DEV_API_KEY` from env vars
  (no more hardcoded secrets in `security.rs`)
- TLS paths: `SQUIRREL_TLS_CERT_PATH`, `SQUIRREL_TLS_KEY_PATH` from env vars
- IP address: `ip_address: None` for runtime discovery (was hardcoded `127.0.0.1`)
- Port docs: all constants documented as fallbacks; env vars take precedence

### Tracing Migration (P2)

All `println!`/`eprintln!` in `main.rs` server mode replaced with `tracing::info!`
and `tracing::error!`. `print_version` simplified to avoid `branches_sharing_code`.

### Error Context (P2)

- `From<anyhow::Error>` for `PrimalError` — seamless `.context()` chains
- `.context()` on IPC JSON-RPC serialization and deserialization calls

### Infrastructure (P2)

- `rust-toolchain.toml` — pinned stable with clippy, rustfmt, llvm-tools-preview
- `justfile` — 17 recipes: `ci`, `check`, `fmt`, `clippy`, `test`, `coverage`,
  `build-release`, `build-ecobin`, `audit`, `line-check`, `clean`, `doctor`,
  `future-compat`, `run-server`
- `CapabilityIdentifier` type with well-known constants replaces deprecated
  `EcosystemPrimalType` enum

## Remaining Stubs (Intentional)

| Module | Status | Note |
|--------|--------|------|
| `performance_optimizer/batch_processor` | Phase 2 | Simulated batch loading |
| `performance_optimizer/optimizer` | Phase 2 | Simplified plugin loading |
| `model_splitting/` | Redirect | Functionality in ToadStool |
| `InMemoryMonitoringClient` | Intentional | Fallback when no external monitoring |

## Known Issues

1. `chaos_07_memory_pressure` flaky under parallel test load (environment-sensitive)
2. `test_load_from_json_file` flaky (env var pollution) — needs `#[serial]`
3. Coverage at 69% — gap to 90% target
4. `redis` v0.23 behind optional `persistence` feature — upgrade when ecosystem stabilizes
5. `router.rs` (991L) at file size limit — pending dead-code investigation
6. Architectural `#[allow]` for `unused_async` / `unused_self` — requires API redesign

## Ecosystem Impact

- No API changes — wire-compatible with all ecosystem primals
- `sysinfo` removal is transparent (same function signatures, different implementation)
- tarpc negotiation makes client connections robust against misconfigured servers
- Human dignity checks are additive — no existing flows broken
