# Songbird v0.2.1 Wave 70+71 — Deep Debt, JSON-RPC Enum Dispatch, Coverage Expansion, Stub Evolution

**Date**: March 24, 2026
**Sessions**: 17–18
**Status**: All quality gates passing

---

## Summary

Two sessions of deep debt evolution, architectural improvement, and coverage expansion:

1. **JSON-RPC Enum Dispatch** — Replaced stringly-typed method routing with typed `JsonRpcMethod` enum in `songbird-types` (50+ methods, 12 domain sub-enums); migrated 3 dispatch sites
2. **Smart File Refactoring** — 8 large files refactored into domain-aligned submodules while preserving API surface
3. **Coverage Expansion** — +204 new tests across 25+ modules (CLI, config, bluetooth, types, orchestrator)
4. **Stub Evolution** — Not-yet-implemented stubs return `SongbirdError::not_implemented_with_detail` instead of silent no-ops
5. **Mock/Placeholder Isolation** — XOR encryption test-only, HMAC-SHA256 fingerprint fallback, SHA-256 beacon ID
6. **Hardcoding Evolution** — Primal identifiers centralized via `primal_names` constants in IPC handlers

---

## Metrics

| Metric | Wave 69 (Before) | Wave 71 (After) |
|--------|-------------------|------------------|
| Tests | 10,235 | 10,687 (0 failed, 271 ignored) |
| Coverage | ~66.59% | ~67% |
| Files >1000 lines | 0 | 0 (max 948 test; 915 production) |
| JSON-RPC dispatch | String matching | `JsonRpcMethod` enum (50+ methods) |
| Method normalization | `songbird-universal-ipc` | `songbird-types` (reusable) |
| Production mocks | XOR encryption, placeholder fingerprints | `CryptoUnavailable` errors, HMAC-SHA256 fallback |
| Not-implemented stubs | Silent `Ok(())` / empty lists | `SongbirdError::not_implemented_with_detail` |
| Clippy | Clean | Clean (`-D warnings`) |
| Format | Clean | Clean |
| Docs | Clean | Clean |

---

## Key Architectural Changes

### JSON-RPC Enum Dispatch (`songbird-types::json_rpc_method`)

New typed routing replaces string matching across all dispatch handlers:

```rust
pub enum JsonRpcMethod {
    Primal(PrimalMethod),
    Health(HealthMethod),
    Discovery(DiscoveryMethod),
    Stun(StunMethod),
    Igd(IgdMethod),
    Relay(RelayMethod),
    Federation(FederationMethod),
    Network(NetworkMethod),
    Tor(TorMethod),
    // ... 12 domains total
}
```

- `FromStr`/`Display`/`Serialize`/`Deserialize` for wire compatibility
- `from_wire_str()` parses canonical and alias names
- `parse_ipc()` normalizes then parses
- Migrated: `IpcServiceHandler::handle`, HTTP gateway, Unix IPC server

### Smart Refactoring (8 files)

| Original File | Lines Before | Lines After | Extracted To |
|--------------|-------------|-------------|--------------|
| `tests_discovery_bridge.rs` | 959 | 400 | `tests_discovery_bridge_e2e.rs` |
| `security.rs` | 868 | 699 | `security_types.rs` |
| `host.rs` | 833 | 560 | `host/scan.rs` |
| `config/mod.rs` | 824 | 647 | `config/security.rs` |
| `canonical.rs` | 888 | 342 | `canonical_types.rs` |
| `capability_based_runtime_discovery.rs` | 822 | 478 | Tests extracted |
| `sovereignty/adapter.rs` | 816 | 355 | `adapter_tests.rs` |
| `tower_atomic.rs` | 810 | 501 | `tower_atomic_tests.rs` |

---

## Files Changed (Session 17 — Wave 70)

- `crates/songbird-universal/src/adapters/security.rs` → extracted `security_types.rs`
- `crates/songbird-bluetooth/src/host.rs` → split into `host/mod.rs` + `host/scan.rs`
- `crates/songbird-config/src/config/mod.rs` → extracted `config/security.rs`
- `crates/songbird-types/src/traits/canonical.rs` → extracted `canonical_types.rs`
- `crates/songbird-orchestrator/src/app/tests_discovery_bridge.rs` → extracted E2E tests
- `crates/songbird-universal/src/sovereignty/adapter.rs` → extracted tests
- `crates/songbird-universal-ipc/src/tower_atomic.rs` → extracted tests
- `crates/songbird-config/src/capability_based_runtime_discovery.rs` → extracted tests
- `crates/songbird-network-federation/src/rendezvous/client.rs` — HMAC-SHA256 fingerprint
- `crates/songbird-network-federation/src/beardog/birdsong.rs` — XOR mock isolated
- `crates/songbird-discovery/src/anonymous/broadcaster.rs` — SHA-256 beacon ID
- `crates/songbird-universal-ipc/src/introspection.rs` — `primal_names` constants
- `crates/songbird-universal-ipc/src/handlers/birdsong_handler.rs` — `primal_names` constants
- `crates/songbird-universal-ipc/src/handlers/onion_handler.rs` — `primal_names` constants

## Files Changed (Session 18 — Wave 71)

- `crates/songbird-types/src/json_rpc_method.rs` — NEW: `JsonRpcMethod` enum module
- `crates/songbird-types/src/lib.rs` — Re-exports `JsonRpcMethod`, `normalize_json_rpc_method_name`
- `crates/songbird-universal-ipc/src/service.rs` — Migrated to enum dispatch
- `crates/songbird-orchestrator/src/server/jsonrpc_api/mod.rs` — Migrated to enum dispatch
- `crates/songbird-orchestrator/src/ipc/unix/server.rs` — Migrated to enum dispatch
- `crates/songbird-cli/src/cli/commands/{status,tower,quick,network,federation}.rs` — New tests
- `crates/songbird-config/src/{discoverable_endpoint,discovery/runtime_engine,defaults/hosts_evolved,config/paths,zero_touch/infant_config}.rs` — New tests
- `crates/songbird-bluetooth/src/gatt/{services,descriptors}.rs`, `transport/mod.rs` — New tests
- `crates/songbird-types/src/{errors,traits/canonical_types}.rs` — New tests
- `crates/songbird-orchestrator/src/connections/{limited,full_trust,federated}_btsp.rs` — New tests + clippy fix
- `crates/songbird-orchestrator/src/{network/mod,core/api}.rs` — New tests
- `crates/songbird-config/src/discovery/runtime_engine.rs` — Stubs → typed errors
- `crates/songbird-discovery/src/abstraction/delegation.rs` — Stubs → typed errors

---

## Remaining Work (Prioritized)

1. **Coverage to 90%** — Currently ~67%; largest gaps in CLI commands, bluetooth transport, federation
2. **BearDog crypto wiring** — All placeholders return `CryptoUnavailable`; real crypto needs BearDog running
3. **genomeBin evolution** — Not yet implemented
4. **songbird-discovery abstraction module** — Pre-existing compilation issues in `modernized_factory.rs` and related files (API drift from canonical trait evolution)
5. **BTSP bidirectional communication** — Phase 2 feature, returns `NotImplemented`

---

## Ecosystem Notes

- `normalize_json_rpc_method_name` moved to `songbird-types` — other primals can now reuse it
- `JsonRpcMethod` enum is in `songbird-types` — available for any primal's IPC dispatch
- All BearDog delegations return `CryptoUnavailable` when BearDog is not running — clean degradation
