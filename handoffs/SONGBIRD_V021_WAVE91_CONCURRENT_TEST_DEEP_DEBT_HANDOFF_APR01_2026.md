# Songbird v0.2.1 — Wave 91 Deep Debt: Concurrent Test Evolution Handoff

**Date**: April 1, 2026  
**Version**: v0.2.1  
**Sessions**: 32–33 (Waves 90–91)  
**Previous**: `SONGBIRD_V021_WAVE89_90_DEEP_DEBT_CRYPTO_DELEGATION_FRAME_REFACTOR_HANDOFF_MAR31_2026.md`

---

## Summary

Deep debt execution focused on eliminating all serial test patterns, migrating to fully concurrent test architecture, replacing production sleeps with event-driven readiness signals, and evolving circuit breaker tests to deterministic timing. Also completed primalSpring audit items SB-02 (ring-crypto documentation) and SB-03 (sled storage abstraction layer).

---

## What Changed

### Zero Serial Tests — Full Concurrency

- **14 `#[serial_test::serial]` annotations removed** across 8 files in `songbird-config` (10), `songbird-universal-ipc` (2), `songbird-config` capability tests (1), e2e (1)
- **`serial_test` dev-dependency removed** from 3 crates (`songbird-config`, `songbird-universal-ipc`, `songbird-types`)
- **Injectable `_with()` pattern**: `detect_public_ip_with()` and `check_cloud_metadata_with()` in `songbird-config::defaults::network_detection` accept environment reader closures — tests inject mocks, zero global state mutation
- **Unique per-test env keys**: All env-touching tests use unique prefixed keys (`E2ERTCOMP_`, `E2ESOV*_`, `E2EPSK_`, `sbserialrtcap`, etc.) — parallel execution cannot conflict

### E2E `std::env` Migration

- All `tests/e2e/test_runtime_discovery.rs`, `test_service_discovery_sovereign.rs`, `test_primal_self_knowledge.rs` migrated from `std::env::set_var`/`remove_var` (Rust 2024 unsafe) to `songbird_process_env` overlay
- Each test uses unique env key prefixes for full concurrency

### Event-Driven Broker Startup

- `TowerAtomicServer::serve_with_ready()` — accepts `tokio::sync::oneshot::Sender<()>`, signals after socket bind
- `UniversalIpcBroker::start_with_ready()` — uses oneshot channel readiness signal
- `start_broker_with_discovery` — replaced 100ms `tokio::time::sleep` with explicit readiness await
- Zero production `sleep` calls in IPC startup path

### Deterministic Circuit Breaker Tests

- Both `songbird-universal` and `songbird-orchestrator` circuit breakers: `std::time::Instant` → `tokio::time::Instant`
- Tests use `#[tokio::test(start_paused = true)]` + `tokio::time::advance()` — complete in 0.00s, no real waits
- Immune to CI timing variability

### primalSpring Audit: SB-02 + SB-03

- **SB-02**: `ring-crypto` feature clearly documented as opt-in-only, ecoBin-violating, standalone testing without BearDog. `deny.toml` comments clarified wrapper paths (`rcgen` via dev-deps, `rustls` via CLI feature gate)
- **SB-03**: Storage backend traits created (`ConsentStorageBackend`, `TaskStorageBackend`, `OnionStorageBackend`) with sled as default. `storage.*` JSON-RPC methods added to `JsonRpcMethod` dispatch (5 methods). Migration to nestGate IPC is mechanical when NG-01 ships

### Rustdoc Fixes

- 4 redundant explicit link targets simplified to intra-doc links in `songbird-quic` (`flow_control.rs`, `varint.rs`)

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| `#[serial_test::serial]` | 14 | **0** |
| `serial_test` dev-dep crates | 3 | **0** |
| `std::env::set_var` in test code | 20+ | **0** (all `songbird_process_env`) |
| Production `sleep` in IPC startup | 1 (100ms) | **0** (oneshot readiness) |
| Circuit breaker test wall time | ~2.5s (real sleeps) | **0.00s** (paused clock) |
| Storage backend abstractions | 0 | 3 traits + sled impls |
| `storage.*` JSON-RPC methods | 0 | 5 (get/put/delete/list/flush) |
| Rustdoc warnings | 4 | **0** |

---

## Build Verification

- `cargo check --workspace --all-features` — Clean
- `cargo fmt --all -- --check` — Clean
- `cargo clippy -p songbird-config -p songbird-universal-ipc -p songbird-universal -p songbird-orchestrator -p songbird-quic -- -D warnings` — Clean
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` — Clean
- `cargo deny check` — Clean (advisories, bans, licenses, sources)
- `cargo test -p songbird-config` — 727 passed
- `cargo test -p songbird-universal` — 674 passed
- `cargo test -p songbird-universal-ipc` — 320 passed
- `cargo test -p songbird-quic` — 178 passed
- `cargo test -p songbird-orchestrator -- circuit_breaker` — 33 passed

---

## Files Changed (33 files, +680 -503 lines)

### Production Code
- `crates/songbird-config/src/defaults/network_detection.rs` — injectable `_with()` pattern
- `crates/songbird-orchestrator/src/ipc/universal_broker.rs` — oneshot readiness signal
- `crates/songbird-universal-ipc/src/tower_atomic.rs` — `serve_with_ready()`
- `crates/songbird-universal/src/circuit_breaker.rs` — `tokio::time::Instant`
- `crates/songbird-orchestrator/src/error_recovery/circuit_breaker.rs` — `tokio::time::Instant`
- `crates/songbird-types/src/json_rpc_method.rs` — `StorageMethod` enum
- `crates/songbird-orchestrator/src/consent_management/mod.rs` — `ConsentStorageBackend` trait
- `crates/songbird-orchestrator/src/task_lifecycle/mod.rs` — `TaskStorageBackend` trait
- `crates/songbird-sovereign-onion/src/storage.rs` — `OnionStorageBackend` trait

### Test Code
- `crates/songbird-config/src/runtime_discovery.rs` — removed `#[serial]`
- `crates/songbird-config/src/capability_based_runtime_discovery_tests.rs` — removed `#[serial]`
- `crates/songbird-config/src/config/hardcoded_elimination.rs` — removed `#[serial]`
- `crates/songbird-config/src/config/paths_tests.rs` — removed `#[serial]`
- `crates/songbird-config/src/defaults/service_locator_tests.rs` — removed `#[serial]`
- `crates/songbird-config/src/defaults/network_detection_tests.rs` — injectable env mocks
- `crates/songbird-universal-ipc/src/capability/discovery.rs` — removed `#[serial]`
- `tests/e2e/test_runtime_discovery.rs` — `songbird_process_env` + unique keys
- `tests/e2e/test_service_discovery_sovereign.rs` — `songbird_process_env` + unique keys
- `tests/e2e/test_primal_self_knowledge.rs` — `songbird_process_env` + unique keys

### Config
- `Cargo.toml` (root) — added `songbird-process-env` dev-dep
- `crates/songbird-config/Cargo.toml` — removed `serial_test`
- `crates/songbird-universal-ipc/Cargo.toml` — removed `serial_test`
- `crates/songbird-types/Cargo.toml` — removed `serial_test`
- `deny.toml` — clarified `ring` wrapper comments

---

## Remaining (songbird-specific)

1. **sled → nestGate `storage.*` IPC**: Abstraction layer complete; blocked on NG-01 real persistence
2. **Coverage**: ~69.14% → 90% target; primary gaps in integration/e2e paths
3. **`ring-crypto` feature gate**: Remains opt-in on CLI for standalone HTTPS testing without BearDog
4. **`async_trait` → native async**: ~8 traits with no `dyn` dispatch are candidates for native async fn in trait (Rust 2024)
5. **Man pages**: `man/songbird.1` and `man/songbird-config.1` from mid-2025 — may need refresh

---

## Ecosystem Context

- **Songbird rating**: S+ (lowest-debt primal, 14 capabilities, stable)
- **primalSpring audit**: SB-02 resolved, SB-03 abstraction complete (blocked on nestGate)
- **Concurrent test architecture**: Pattern (`_with()` injectable env, unique per-test keys, `songbird_process_env` overlay) available for adoption by other primals
- **Event-driven readiness**: `serve_with_ready()` pattern available for any primal using Tower Atomic IPC
