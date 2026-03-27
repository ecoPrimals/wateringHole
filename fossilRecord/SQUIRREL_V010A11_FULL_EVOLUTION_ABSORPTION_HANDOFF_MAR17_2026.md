<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.11 — Full Evolution & Cross-Ecosystem Absorption

**Date**: 2026-03-17
**Primal**: Squirrel
**Version**: 0.1.0-alpha.11
**Sprint**: Deep Lint Evolution + Cross-Ecosystem Absorption
**Previous**: SQUIRREL_V010A10_DEEP_AUDIT_EVOLUTION_HANDOFF_MAR17_2026

---

## Summary

Two-phase sprint: (1) comprehensive lint tightening and idiomatic Rust evolution
across all 22 crates, and (2) cross-ecosystem absorption from 8 springs and 12
primals. Reduced `#[allow]` blocks from ~50 to ~18, fixed 170+ Clippy violations,
replaced `sysinfo` C dependency with pure Rust, completed `UnifiedPluginManager`
stub, added human dignity evaluation, and absorbed manifest writer, safe_cast,
total_cmp, health probes, and expanded consumed capabilities from the latest
spring and primal releases.

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all --check` | PASS |
| `cargo clippy --all-features --all-targets -- -D warnings` | PASS (zero warnings) |
| `cargo test --workspace` | 4,979 pass / 0 failures |
| `cargo doc --workspace --no-deps` | PASS |
| Files > 1000 lines | 0 (max: 991) |
| Coverage | 69% (target: 90%) |
| TODO/FIXME in source | 0 |
| Hardcoded credentials | 0 |
| Unsafe code | 0 (`#![forbid(unsafe_code)]` all crates) |
| Debris/orphans | 0 |

## Phase 1: Lint Evolution

### Clippy Full Compliance (P0)

- Reduced crate-level `#[allow]` from ~50 to ~18 in `squirrel` and `squirrel-mcp`
- `unwrap_used` / `expect_used` → `#[cfg_attr(test, allow(...))]`
- Fixed 42 errors in `squirrel-mcp` (17 `unwrap()` in production → `map_err()`)
- Fixed 103 errors in `squirrel` main crate
- Architectural allows documented: `unused_async`, `unused_self`, `needless_pass_by_ref_mut`

### Pure Rust `sys_info` (P0 — ecoBin v3.0)

Replaced `sysinfo` crate (C dependency) with `universal-constants::sys_info`:
`memory_info()`, `process_rss_mb()`, `cpu_count()`, `uptime_seconds()`,
`hostname()`, `system_cpu_usage_percent()` — all via `/proc` parsing on Linux
with graceful fallbacks.

### tarpc Client Negotiation (P0)

`SquirrelClient::connect()` now performs `PROTOCOLS: ...` handshake via
`negotiate_client`. Bails on non-tarpc selection. `from_negotiated_transport`
replaces deprecated `from_transport`.

### Plugin Manager Completion (P1)

`UnifiedPluginManager` with load/unload lifecycle, `PluginEventBus` (pub/sub),
`PluginSecurityManager` (capability-based), `ManagerMetrics` counters.

### Human Dignity Evaluation (P1)

`DignityEvaluator` + `DignityGuard` in AI routing: discrimination risk,
human oversight, manipulation prevention, explainability checks.

### Hardcoding Evolution (P1)

- Dev credentials → env vars (`SQUIRREL_DEV_JWT_SECRET`, `SQUIRREL_DEV_API_KEY`)
- TLS paths → env vars (`SQUIRREL_TLS_CERT_PATH`, `SQUIRREL_TLS_KEY_PATH`)
- IP address → `None` for runtime discovery
- Tracing migration: all `println!`/`eprintln!` in server code → `tracing`

### Infrastructure (P2)

- `rust-toolchain.toml` — pinned stable + clippy + rustfmt + llvm-tools-preview
- `justfile` — 17 recipes for CI, build, lint, test, coverage
- `CapabilityIdentifier` type replacing deprecated `EcosystemPrimalType`
- `From<anyhow::Error>` for `PrimalError`; `.context()` on IPC paths

## Phase 2: Cross-Ecosystem Absorption

### Manifest Writer (P0 — biomeOS v2.49 / rhizoCrypt v0.13)

Squirrel writes `$XDG_RUNTIME_DIR/ecoPrimals/squirrel.json` at startup with
primal ID, version, socket, capabilities, PID, timestamp, FAMILY_ID. Cleaned
up on graceful shutdown. Enables biomeOS manifest-based bootstrap discovery.

### Consumed Capabilities Expanded (P1)

| Source | Capabilities Added |
|--------|-------------------|
| ToadStool S158 | `compute.dispatch.submit/status/result`, `compute.hardware.observe` |
| NestGate 4.1 | `model.register`, `model.locate`, `model.metadata` |
| rhizoCrypt v0.13 | `dag.session.create` |
| sweetGrass v0.7.21 | `anchoring.anchor`, `attribution.calculate_rewards` |

### Health Probes (P1 — PRIMAL_IPC_PROTOCOL v3.0)

`health.liveness` and `health.readiness` added to:
- `niche.rs` CAPABILITIES, SEMANTIC_MAPPINGS, COST_ESTIMATES
- `capability_registry.toml` with input schemas
- `cost_estimates_json()` and `operation_dependencies()`
- Also added `capability.list` to the TOML registry (was in niche but missing)

### `safe_cast` Module (P2 — groundSpring V114 / airSpring V0.8.9)

`universal-constants::safe_cast` with `usize_to_u32`, `usize_to_u32_saturating`,
`f64_to_f32`, `u64_to_usize`, `i64_to_usize`, `f64_to_u64_clamped`. 11 tests.

### `total_cmp()` Sweep (P2 — neuralSpring V115)

Replaced all 5 `partial_cmp().unwrap()` with `f64::total_cmp` in constraints,
selector, rule_viz (2x), and load_testing.

### Platform-Agnostic Tests (P3 — neuralSpring)

`/tmp` hardcoding replaced with `std::env::temp_dir()` in `policy_tests.rs`.

### Leverage Guide Updated (P3)

`SQUIRREL_LEVERAGE_GUIDE.md` bumped to alpha.11 with health probes, manifest
discovery, human dignity, primalSpring Track 6 exp044, RPGPT composition.

## Remaining Stubs (Intentional)

| Module | Status | Note |
|--------|--------|------|
| `performance_optimizer/batch_processor` | Phase 2 | Simulated batch loading |
| `performance_optimizer/optimizer` | Phase 2 | Simplified plugin loading |
| `model_splitting/` | Redirect | Functionality in ToadStool |
| `InMemoryMonitoringClient` | Intentional | Fallback when no external monitoring |

## Known Issues

1. `chaos_07_memory_pressure` flaky under parallel test load
2. `test_load_from_json_file` flaky (env var pollution) — needs `#[serial]`
3. Coverage at 69% — gap to 90% target
4. `redis` v0.23 behind optional `persistence` feature
5. `router.rs` (991L) at file size limit — pending dead-code investigation
6. Architectural `#[allow]` for `unused_async` / `unused_self`

## Ecosystem Impact

- No API changes — wire-compatible with all ecosystem primals
- Manifest writer enables biomeOS bootstrap discovery of Squirrel
- Health probes make Squirrel discoverable via PRIMAL_IPC_PROTOCOL v3.0
- Expanded consumed capabilities declare intent for ToadStool, NestGate,
  rhizoCrypt, and sweetGrass integration
- `safe_cast` and `total_cmp()` align with cross-ecosystem numeric patterns
