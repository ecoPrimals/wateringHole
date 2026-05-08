<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 91 Handoff

**Date**: May 7, 2026
**Primal**: BearDog (P3)
**Wave**: 91
**Scope**: Typed errors — BondPersistence & SslKeylog

---

## Summary

Last remaining `Result<_, String>` in the BearDog persistence layer and TLS keylog utility migrated to typed error enums. Resolves the final P3 item from the primalSpring Phase 60 deep-debt audit.

---

## Changes

### `BondPersistenceError` enum (new)

- **File**: `crates/beardog-tunnel/src/unix_socket_ipc/handlers/ionic_bond/persistence.rs`
- **Variants**: `Serialization { context, source }`, `Io { context, source }`, `RpcTimeout`, `RpcError(String)`, `InvalidResponse(&'static str)`
- **`BondPersistenceResult<T>`** type alias added
- **Trait**: `BondPersistence` — all 4 methods migrated from `Result<_, String>` to `BondPersistenceResult<_>`
- **Implementations updated**: `InMemoryBondPersistence`, `BondPersistenceBackend`, `CapabilityDiscoveryBondPersistence`
- **Handler boundary**: `lifecycle.rs` call sites convert via `.map_err(|e| e.to_string())` — no change to JSON-RPC `MethodHandler` contract
- **Re-export**: `BondPersistenceError` and `BondPersistenceResult` added to `ionic_bond/mod.rs` public API

### `SslKeylogError` enum (new)

- **File**: `crates/beardog-tunnel/src/unix_socket_ipc/handlers/crypto/sslkeylog.rs`
- **Variants**: `InvalidClientRandom(usize)`, `Io { context, source }`
- **Function**: `export_to_sslkeylogfile` return type changed from `Result<(), String>` to `Result<(), SslKeylogError>`
- **Caller**: `derive_handshake.rs` unchanged — uses `Display` via `warn!("{}", e)`
- **Re-export**: `SslKeylogError` added to `crypto/mod.rs` public API

### Tests

- 2 persistence tests pass (in-memory roundtrip, capability-discovery fallback)
- 3 sslkeylog tests pass (no-env-var, invalid-length, handshake-export)
- 19 ionic_bond handler tests pass (lifecycle, contract signing, verification)
- Test `test_invalid_client_random_length` updated to use `matches!` on `SslKeylogError::InvalidClientRandom(16)` instead of string contains

---

## CI Gates

| Gate | Status |
|------|--------|
| `cargo check` | Clean |
| `cargo clippy --workspace -- -D warnings` | 0 warnings |
| `cargo fmt --check` | Clean |
| Unit tests (24 targeted) | All pass |

---

## Audit Resolution

| Audit Item | Status |
|------------|--------|
| `BondPersistence` trait `Result<_, String>` | **RESOLVED** — `BondPersistenceError` |
| `InMemoryBondPersistence` `Result<_, String>` | **RESOLVED** — same enum |
| `CapabilityDiscoveryBondPersistence` `Result<_, String>` | **RESOLVED** — same enum |
| `export_to_sslkeylogfile` `Result<(), String>` | **RESOLVED** — `SslKeylogError` |

**primalSpring Phase 60 BearDog P3 — 0 items remaining.**

---

## Files Changed (7)

1. `crates/beardog-tunnel/src/unix_socket_ipc/handlers/ionic_bond/persistence.rs` — error enum + trait + 3 impls
2. `crates/beardog-tunnel/src/unix_socket_ipc/handlers/ionic_bond/lifecycle.rs` — `.map_err(|e| e.to_string())` at 3 call sites
3. `crates/beardog-tunnel/src/unix_socket_ipc/handlers/ionic_bond/mod.rs` — re-exports
4. `crates/beardog-tunnel/src/unix_socket_ipc/handlers/crypto/sslkeylog.rs` — error enum + function signature + tests
5. `crates/beardog-tunnel/src/unix_socket_ipc/handlers/crypto/mod.rs` — re-export
6. `CHANGELOG.md` — Wave 91 entry
7. `STATUS.md` — Wave 91 entry + architecture compliance update
