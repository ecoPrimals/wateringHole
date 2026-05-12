# Songbird v0.2.1 — Wave 93 Deep Debt: Ring Elimination, Sled Feature-Gate, Concurrency Fix

**Date**: April 2, 2026  
**Version**: v0.2.1  
**Sessions**: 34–35 (Waves 92–93)  
**Previous**: `SONGBIRD_V021_WAVE91_CONCURRENT_TEST_DEEP_DEBT_HANDOFF_APR01_2026.md`

---

## Summary

Deep debt execution focused on: eliminating the `rcgen`/`ring` dependency with pure Rust cert generation, feature-gating `sled` with in-memory fallbacks, refactoring three large files into directory modules, expanding test coverage, and fixing a critical `yield_now()` infinite-loop concurrency bug in test poll helpers.

---

## What Changed

### Ring Dependency Elimination (SB-02 Progress)

- **`rcgen` removed** from `songbird-tls` dev-dependencies
- Replaced with `ed25519-dalek` + manual ASN.1 DER construction (same pattern as `songbird-quic/cert_gen.rs`)
- `cargo tree -p songbird-tls -e dev --all-features | grep "ring v"` — **no output**
- `ring` remains in lockfile only via `rustls/ring` (CLI opt-in `ring-crypto` feature) and transitive paths — tracked, not urgent

### Sled Feature-Gating (SB-03 Progress)

- `sled` now optional behind `sled-storage` feature (default enabled) in `songbird-orchestrator` and `songbird-sovereign-onion`
- `InMemoryStorage` fallbacks implement `ConsentStorageBackend`, `TaskStorageBackend`, `OnionStorageBackend`
- `cargo check --no-default-features` compiles clean for both crates
- Path to NestGate IPC migration: swap `sled-storage` default → `nestgate-storage` when NG-01 ships

### Large File Refactoring

- `birdsong_handler.rs` (855 lines) → `birdsong_handler/` 7-file module
- `production_analytics.rs` (812 lines) → `production_analytics/` 6-file module
- `service.rs` (797 lines) → `service/` 7-file module
- All production modules now under 800 lines; largest file in workspace is a test file at 950 lines

### Critical Concurrency Bug Fix

**Root cause**: `tokio::task::yield_now()` in poll-until loops under `#[tokio::test(start_paused = true)]` causes infinite loops. Virtual time only advances on `tokio::time::sleep`, not on `yield_now()`. The polling loop yields forever without the spawned tasks' sleeps completing.

**Fix**: Replaced `yield_now()` with `tokio::time::sleep(Duration::from_millis(1))` in all poll helpers:
- `tests/common/sync_helpers.rs` — `poll_until`, `poll_until_some`, `poll_until_ok`, `wait_for_condition`
- `tests/common/event_helpers.rs` — `wait_for`, `wait_for_async`, `wait_for_some`
- `tests/capability_integration_tests.rs` — `wait_for_provider_state`
- `tests/discovery_e2e_test.rs`, `integration_relay_forwarding.rs`, `runtime_engine_tests.rs`

**Impact**: Orchestrator test suite went from hanging indefinitely to completing in ~84s.

**Lesson for ecosystem**: Any `yield_now()` loop + `start_paused` is a hang. The correct pattern is `tokio::time::sleep(small)` which cooperates with both real and virtual time.

### Discovery Fast-Fail

- `RuntimeDiscoveryEngine` skips mDNS daemon startup and multicast listener for sub-50ms timeouts
- Network discovery skips DNS-SD resolver queries for sub-100ms mDNS listen windows
- Test-path discovery dropped from ~10s to ~0.01s

### Coverage Expansion

- 60+ new test functions across songbird-http-client, songbird-universal-ipc, songbird-stun, songbird-lineage-relay
- Focus on pure logic modules: connection pool, crypto discovery, capability strategy/registry, punch handler, STUN message parsing, relay forwarding

---

## Current Metrics

| Metric | Value |
|--------|-------|
| Tests | 11,917 passing, 0 failed |
| Full suite | ~84s (workspace, all features) |
| Coverage | ~69% (target 90%) |
| Total Rust | ~412,555 lines |
| Clippy | Clean (`--all-targets --all-features -D warnings`) |
| Formatting | Clean |
| Docs | Clean (`-D warnings`) |
| Files >1000 LOC | 0 |
| `#[serial_test]` | 0 |
| Production panics | 0 |

---

## Remaining Deep Debt

### Coverage Gap (69% → 90%)
Priority modules by missed lines: `songbird-orchestrator` (~56%), `songbird-config` (~68%), `songbird-universal` (~72%), `songbird-http-client` (~65%), `songbird-universal-ipc` (~67%).

### BearDog Crypto Integration
All stubs return `CryptoUnavailable`; wiring requires BearDog running. Tor protocol, TLS/Sovereign Onion, and ring-free workspace items pending.

### Platform & Infrastructure
NFC backends, real hardware IGD test, genesis physical channels, iOS XPC, WASM support — all pending platform availability.

---

## For Other Primals

### Pattern: `yield_now()` vs `sleep()` in Test Polls
If your primal has poll-until helpers that use `yield_now()`, they will hang under `start_paused = true`. Replace with `tokio::time::sleep(Duration::from_millis(1))`. This is a correctness fix, not a style preference.

### Pattern: Feature-Gated Storage
Songbird now feature-gates `sled` with in-memory fallback. Other primals using sled directly should consider the same pattern for minimal builds and eventual NestGate migration.
