# Songbird v0.2.1 Handoff — Fully Concurrent Architecture: Injectable Env Readers

**Primal**: Songbird (Network Orchestration & Discovery)  
**Date**: March 21, 2026  
**Version**: v0.2.1 (Cargo.toml aligned)  
**Previous**: v0.3.4 handoff (archived — version was misaligned with Cargo.toml)  
**License**: AGPL-3.0-only (scyBorg provenance trio)

---

## Session Summary

Deep architectural evolution eliminating all global mutable state from tests. Every `from_env()` / `detect()` / `discover()` function evolved to injectable `_with` variants, enabling fully concurrent testing at 16 threads with zero race conditions. Eliminated all 30+ `#[serial_test::serial]` usages. First successful `cargo llvm-cov` run producing clean coverage metrics.

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| `#[serial_test::serial]` | 30+ | 0 |
| Test threads | 1 (serialized) | 16 (fully concurrent) |
| Tests | 9,734 passed | 9,730 passed, 0 failed, 271 ignored |
| Line coverage | ~65% (llvm-cov failing) | 64.14% (llvm-cov clean) |
| Branch coverage | unknown | 63.11% |
| Test suite time | ~513s | ~421s |
| Build warnings | 0 | 0 |
| Total Rust lines | 382,889 | 380,555 |

---

## What Changed

### Injectable Environment Readers (Wave 27)

**Problem**: Tests mutated global process environment (`std::env::set_var`) requiring `#[serial_test::serial]` — a band-aid over fundamentally non-concurrent code.

**Solution**: Every env-reading function now has an injectable `_with` variant:

```rust
// Production API unchanged
pub fn from_env() -> Result<Self> {
    Self::from_env_reader(|k| std::env::var(k))
}

// Tests inject closures — zero global mutation, fully concurrent
pub fn from_env_reader(env: impl Fn(&str) -> Result<String, VarError>) -> Result<Self> {
    let bind = env("SONGBIRD_BIND_ADDRESS").unwrap_or_else(|_| "0.0.0.0".to_string());
    ...
}
```

### Evolved APIs by Crate

- **songbird-config**: `detect_with`, `from_env_reader` (Network, ZeroTouch, Port/Host/Endpoint configs), `try_env_resolution_with`, `discover_from_environment_with`, `get_bind_address_with`, `get_canonical_endpoint_with`, `find_primals_with_capability_in_env`, `get_log_level_with`
- **songbird-discovery**: `discover_self_with`, `introspect_name_with`, `introspect_capabilities_with`
- **songbird-universal**: `DiscoveryConfig::provider_endpoints` (HashMap injection), adapter `with_resolver` constructors, `CapabilityEndpointResolver::with_endpoint_overrides`
- **songbird-universal-ipc**: `EnvironmentStrategy::discover_with`, `IpcServiceHandler::with_family_id_env`
- **songbird-orchestrator**: `ComputeApiState::new_with_capability_endpoint_overrides`, `SecurityFetchMode` enum

---

## Verification

| Check | Status |
|-------|--------|
| `cargo check --workspace --all-features` | PASS (0 warnings) |
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --all-features` | PASS (0 warnings) |
| `cargo test --workspace --all-features -- --test-threads=16` | 9,730 passed, 0 failed |
| `cargo llvm-cov --workspace --all-features` | 64.14% line, 63.11% branch, 63.23% region |
| `grep serial_test::serial crates/` | 0 matches |

---

## Remaining Work

1. **Coverage 64% → 90%** — continued test expansion, now unblocked by concurrent testing
2. **BearDog crypto wiring** — blocked on BearDog availability
3. **Ring-free workspace** — rcgen replacement + quinn feature reconfiguration
4. **Deep documentation** — fill scoped `#[allow(missing_docs)]` internal modules
5. **Hardware tests** — Tower + Pixel 8a validation
6. **Platform backends** — NFC, iOS XPC, WASM
7. **Dependency version alignment** — base64, socket2, rand duplicates
8. **Script/config refresh** — align env var names in config/*.env and scripts/*.sh

---

## For Other Primals

- **BearDog**: Songbird discovers crypto via `capability.call("crypto", ...)` at runtime; stubs return `CryptoUnavailable`
- **biomeOS**: Songbird registers capabilities via `lifecycle.register` when biomeOS is present
- **Squirrel/Toadstool**: JSON-RPC gateway at `/jsonrpc` accepts `{domain}.{operation}` semantic methods; tarpc for native performance
- **All Primals**: Injectable `_with` pattern is recommended for all env-dependent config (concurrent testing standard)
