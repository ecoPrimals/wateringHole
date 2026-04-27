# Songbird v0.2.1 — Wave 174: Deep Debt (Hardcoding, Stability, Dependencies, Coverage)

**Date**: April 27, 2026
**Primal**: Songbird
**Version**: v0.2.1-wave174
**Status**: Complete

---

## Summary

Comprehensive deep debt pass targeting hardcoded IP/port elimination, flaky test stabilization, dependency hygiene, and coverage expansion.

## Changes

### 1. Hardcoded IP/Port Elimination (~12 literals → constants)

Replaced bare `"0.0.0.0:0"`, `"127.0.0.1"`, `"localhost"` string literals across 7 production files with centralized `songbird_types::constants` references:

- `EPHEMERAL_BIND_ADDR` for all UDP/TCP ephemeral socket binds (cli/discovery, onion-relay/stun, discovery/network)
- `LOCALHOST` / `LOCALHOST_HOSTNAME` for loopback address construction (cli/discovery, orchestrator/self_knowledge)
- `DEFAULT_HTTP_PORT` for `CanonicalNetworkConfig` and `CanonicalBindConfig` defaults (replacing magic `8080`)

### 2. Flaky Test Stabilization

`scan_address_simulation_builds_discovered_node` and `scan_subnet_invalid_format_errors_when_not_simulated` in `songbird-cli` used bare `songbird_process_env::set_var` / `reset_overlay`, causing race conditions in parallel test runs. Replaced with `songbird_test_utils::ScopedEnv` (async-safe `tokio::sync::Mutex`-backed RAII guard).

### 3. Dependency Hygiene

- **Removed `mdns` 3.0.0**: declared as optional dep in `songbird-universal` but never imported. Removal drops `net2` 0.2 and `async-std` from the transitive graph. The `mdns` *feature flag* remains functional — it gates the existing pure-Rust mDNS implementation (raw UDP sockets, no external crate).
- **Removed `once_cell` 1.19**: pinned in `songbird-test-utils/Cargo.toml` but unused in source. All code uses `std::sync::OnceLock` / `std::sync::LazyLock`.
- **Unified `tempfile`**: added `tempfile = "3.8"` to `[workspace.dependencies]` and converted all 10 crate references to `tempfile = { workspace = true }`. Eliminated version drift (some crates had `3.0`, others `3.8`).

### 4. Coverage Expansion (+18 tests)

- **`information_layers.rs`** (+12): all `TaskStatus` variants for `build_public`; learning_notes content, capability thresholds, CPU-only path for `build_educational`; no-tower/CPU-only/GPU-hours/queue-time branches for `build_administrative`; CPU-only temperature, completed uptime, empty nodes for `build_infrastructure`; non-failure statuses for `build_operational`
- **`security.rs`** (+2): direct `parse_masking_level` tests for all 6 known values + unknown/None/empty fallback
- **`service.rs`** (+4): endpoint/metadata overwrite, capability/dependency duplicate accumulation, `Custom::as_str`

## Validation

- `cargo fmt --all` — clean
- `cargo clippy --workspace -- -D warnings` — 0 warnings
- `cargo test --workspace --lib` — 7,683 passed, 0 failed
- `cargo check --workspace` — 0 errors

## Known Pre-existing Issues (NOT addressed)

- Integration tests in `songbird-universal/tests/` reference `futures` crate (not `futures-util`) — pre-existing compilation errors in test-only integration test files
- Test count is 7,683 across all crate lib test binaries (`cargo test --workspace --lib`)

## Files Modified

### Production
- `crates/songbird-cli/src/cli/commands/quick.rs`
- `crates/songbird-cli/src/cli/commands/quick/discovery.rs`
- `crates/songbird-cli/src/cli/discovery.rs`
- `crates/songbird-onion-relay/src/coordinator/stun.rs`
- `crates/songbird-discovery/src/discovery/network/mod.rs`
- `crates/songbird-orchestrator/src/self_knowledge.rs`
- `crates/songbird-types/src/config/consolidated_canonical/network.rs`
- `crates/songbird-lineage-relay/src/security.rs` (test accessor only)

### Tests
- `crates/songbird-orchestrator/src/access_control/information_layers.rs`
- `crates/songbird-lineage-relay/src/security_tests.rs`
- `crates/songbird-types/src/service.rs`

### Cargo.toml (dependency changes)
- Root `Cargo.toml` (workspace deps)
- `songbird-universal/Cargo.toml` (mdns removal)
- `songbird-test-utils/Cargo.toml` (once_cell removal)
- 10 crates (tempfile → workspace)
- `songbird-cli/Cargo.toml` (added songbird-test-utils dev-dep)
