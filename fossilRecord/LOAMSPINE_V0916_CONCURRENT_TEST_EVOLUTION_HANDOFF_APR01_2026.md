<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# loamSpine — v0.9.16 Concurrent Test Evolution Handoff

**Date**: April 1, 2026
**Version**: 0.9.15 → 0.9.16
**Priority**: Informational — no blockers
**Cross-reference**: `concurrent_test_evolution` plan (7 phases)

---

## Summary

Complete elimination of test serialization across the entire loamSpine codebase.
121 `#[serial]` attributes removed, `serial_test` and `temp-env` crates removed from
workspace, all 1,270 tests run fully concurrent in ~3 seconds. Production code evolved
with inner/outer function pattern for dependency injection.

## Architecture: Inner/Outer Function Pattern

All environment-dependent functions were split into:
- **Inner (pure)**: `resolve_*`, `_from`, `_with` variants accepting explicit parameters
- **Outer (wrapper)**: Reads `std::env::var()` and delegates to inner function

Tests call inner functions directly — no env mutation needed, no serialization required.

## 7-Phase Execution

### Phase 1: Storage tests (26 `#[serial]` removed)
- Sled and redb tests already used unique `tempfile::tempdir()` paths
- Block scoping (`{ ... }`) for deterministic database file lock release

### Phase 2: `constants/network.rs` (25 `#[serial]` removed)
- `resolve_jsonrpc_port`, `resolve_tarpc_port`, `resolve_bind_address`,
  `resolve_use_os_assigned_ports`, `resolve_socket_base_dir_with`,
  `resolve_primal_socket_from`, `negotiate_protocol_from`
- All 25 tests rewritten to call pure functions directly

### Phase 3: `neural_api.rs` (17 `#[serial]` removed)
- `resolve_socket_path_with`, `resolve_neural_api_socket_with`
- `register_at_socket`, `deregister_at_socket` (accept `&Path`)
- Mock-server tests use `tempfile` Unix sockets

### Phase 4: Discovery & manifest (31 `#[serial]` removed)
- `manifest_dir_from`, `discover_manifests_from`, `find_by_capability_from`
- `DiscoveryConfig::env_overrides: HashMap<String, String>` for test config injection
- `DiscoveryConfig::from_explicit(registry_url, cache_ttl)` constructor
- `InfantDiscovery::env_lookup()` checks overrides before process env
- `try_environment_discovery_with`, `discover_discovery_service_with_env`

### Phase 5: CLI signer & lifecycle (8 `#[serial]` removed)
- `CliSigner::discover_binary_from(signer_path, bins_dir)` pure function
- Lifecycle tests inject config via `DiscoveryConfig::env_overrides`

### Phase 6: Integration tests (5 `#[serial]` removed)
- `portpicker::pick_unused_port()` replaces fixed port numbers
- `Command::env()` replaces `temp_env::with_vars` for child process env
- TCP connect polling replaces `thread::sleep(1500ms)` startup wait

### Phase 7: Sleep elimination (8 test sites)
- `#[tokio::test(start_paused = true)]` + `tokio::time::advance()` replaces
  `tokio::time::sleep()` in lifecycle heartbeat, expiry sweeper, and health tests
- Lifecycle tests: 5.0s → 0.00s
- Expiry sweeper tests: 2.0s → 0.00s
- Health tests: 0.1s → 0.00s

## Dependencies

### Removed
- `serial_test` — no longer used anywhere
- `temp-env` — no longer used anywhere

### Added
- `portpicker = "0.1"` (workspace dev-dependency) — dynamic port allocation for
  integration tests

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Version | 0.9.15 | 0.9.16 |
| Tests | 1,397 | 1,270 |
| `#[serial]` tests | 121 | 0 |
| Test suite time | ~15s | ~3s |
| `temp_env` usage | 40+ sites | 0 |
| Test sleep sites | 8 | 0 (deterministic time) |
| Source files | 129 | 129 |
| Max file size | 899 | 899 |
| Clippy warnings | 0 | 0 |
| Doc warnings | 0 | 0 |
| Unsafe blocks | 0 | 0 |

Test count decreased because trivial env-reading tests were consolidated into focused
pure-function tests during the inner/outer refactoring.

## Verification

```bash
cargo test --workspace                   # 1,270 passing, ~3s
cargo clippy --workspace --all-targets -- -D warnings  # 0 warnings
cargo fmt --all -- --check               # clean
```

Three consecutive full-suite runs: all green.

## Remaining `thread::sleep` (acceptable)

- `expiry_sweeper.rs` (2 sites): 50µs wall-clock polling — `Timestamp::now()` uses
  system time, not tokio clock. Cannot use `tokio::time::advance()`.
- `transport/http.rs` (4 sites): 50ms mock HTTP server readiness — blocking server,
  not tokio-based.
- `main_integration.rs` (2 sites): 20ms/50ms process polling — spawned binary process,
  not tokio context.

## Pattern for Other Primals

The inner/outer function pattern applied here is reusable across the ecosystem:

```rust
// Pure inner function (testable, no env dependency)
pub fn resolve_port(env_override: Option<&str>, default: u16) -> u16 {
    env_override
        .and_then(|s| s.parse().ok())
        .unwrap_or(default)
}

// Thin outer wrapper (reads env, delegates)
pub fn port() -> u16 {
    resolve_port(std::env::var("PORT").ok().as_deref(), 8080)
}

// Test (no #[serial], no temp_env, fully concurrent)
#[test]
fn port_from_env() {
    assert_eq!(resolve_port(Some("9090"), 8080), 9090);
}
```
