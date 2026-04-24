# Songbird v0.2.1 — Wave 165: Deep Debt Dependency Cleanup

**Date**: April 15, 2026
**Primal**: Songbird
**Version**: v0.2.1
**Wave**: 165
**Supersedes**: Wave 164 handoff (archived)

---

## Summary

Comprehensive deep debt audit and cleanup focused on dependency hygiene,
hardcoded value elimination, lint discipline, and dead code removal.

### Dependency Evolution

| Before | After | Crates affected |
|--------|-------|-----------------|
| `serde_yaml` 0.9 (deprecated) | `serde_yaml_ng` 0.10 (maintained fork) | songbird-config, songbird-discovery |
| `hostname` 0.4 (duplicate) | `gethostname` 0.4 (consolidated) | songbird-discovery, songbird-orchestrator, songbird-cli, songbird-types, songbird-compute-bridge |
| `futures` 0.3 (facade) | `futures-util` (workspace) | songbird-universal |
| `url` 2.0 (old) | `url` 2.5 (aligned) | songbird-universal |

### Hardcoded Elimination

- `"0.0.0.0:0"` in `udp_discovery.rs` → `songbird_types::constants::EPHEMERAL_BIND_ADDR`
- `"0.0.0.0:{port}"` in `stun_handler/server.rs` → `songbird_types::constants::PRODUCTION_BIND_ADDRESS`

### Lint Hygiene

- `songbird-discovery/src/lib.rs` test `cfg_attr` block: added `reason = "..."`
- `tests/integration_task_lifecycle.rs`: consolidated 3 bare `#[allow]` into one with reason
- `examples/ipc_client_simple.rs` and `ipc_client_discovery.rs`: added `reason = "..."`

### Dead Code Removed (7 zero-caller deprecated items)

- `MockSquirrel` type alias
- `MockToadStool` type alias
- `mocks::squirrel`, `mocks::toadstool`, `mocks::nestgate` module aliases
- `discover_beardog_binary()` in songbird-test-utils
- `discover_security_provider_socket_with()` in songbird-crypto-provider

### Test Evolution

13 sync `#[test]` + `futures::executor::block_on()` tests in `sovereignty/adapter_tests.rs`
converted to `#[tokio::test]` + `async fn` + `.await` (idiomatic async test pattern).

### Verification

- `cargo fmt -- --check` — clean
- `cargo clippy --workspace -- -D warnings` — 0 warnings
- `cargo test --workspace --lib` — 497 passed, 0 failed

### Audit Findings (no action needed)

- 0 files >800 lines (largest: 763L `primal_discovery.rs`)
- 0 unsafe code, `forbid(unsafe_code)` on all 30 crates
- 0 `async-trait` annotations
- 0 mocks in production (all gated by `#[cfg(test)]` or `feature = "test-mocks"`)
- 0 `todo!()` / `unimplemented!()` / `panic!()` in production
- 0 `Box<dyn Error>` in production APIs
