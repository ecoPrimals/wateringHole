# biomeOS v2.44 — Deep Audit Evolution: Modern Idiomatic Rust

**Date**: March 16, 2026
**Version**: 2.44
**Status**: PRODUCTION READY
**Focus**: Comprehensive audit + systematic evolution against wateringHole standards

---

## Summary

Full codebase audit against ecoPrimals wateringHole standards followed by systematic execution of all findings. Upgraded to Rust Edition 2024, implemented real tarpc binary protocol, evolved to capability-based discovery, and hardened lint configuration.

---

## Changes

### Critical Fixes

| Fix | Detail |
|-----|--------|
| **Sovereignty bug** | Operator precedence in `enforce_economic_sovereignty()` — `(a && b) \|\| c` corrected to `a && (b \|\| c)` |
| **Failing test** | `test_socket_dir_default` replaced with env-race-free `SystemPaths` comparison |
| **Lint hardening** | `unwrap_used`/`expect_used` promoted from `warn` to `deny` workspace-wide |

### Edition 2024 Migration

- Upgraded `Cargo.toml` from `edition = "2021"` to `edition = "2024"`
- Created `biomeos-test-utils::env_helpers` with safe `set_test_env()`, `remove_test_env()`, `TestEnvGuard`
- Migrated ~130 `set_var`/`remove_var` calls across ~20 files to safe wrappers
- Refactored 2 production `set_var` calls:
  - `config/mod.rs` → stores env vars in config metadata for `Command::env()` propagation
  - `seed.rs` → returns `(key, value)` tuples instead of mutating global state
- Fixed all edition 2024 pattern-matching changes and collapsible-if lint suggestions
- `biomeos-test-utils` changed from `forbid(unsafe_code)` to `deny(unsafe_code)` (only crate with this exception)

### Capability-Based Discovery

- Added `capability` constants module in `biomeos-types/src/constants.rs`:
  - `CRYPTO`, `MESH_NETWORKING`, `TLS`, `STORAGE`, `GATEWAY`, `NAT_TRAVERSAL`, `CACHING`, `VISUALIZATION`, `GRAPH_DATABASE`, `PERSISTENCE`, `GPU_COMPUTE`, `SIGNING`, `ENCRYPTION`
- Renamed `BeardogSecurityAdapter` → `CryptoSecurityAdapter`, `SongbirdDiscoveryAdapter` → `MeshDiscoveryAdapter`
- Added `discover_by_capability()` and `discover_endpoint_by_capability()` functions
- Evolved `configure_beardog_env()` → agnostic `crypto_provider_env()`

### Port / IP / Path Constants

- Added `ports` module: `STUN` (3478), `MDNS` (5353), `SSDP` (1900), `API_DEFAULT` (3000), etc.
- Fixed Google DNS sovereignty violation: `2001:4860:4860::8888` → RFC 3849 `FALLBACK_RESOLVER_IPV6`
- Centralized metrics DB path through `SystemPaths`

### Zero-Copy (Arc<str>)

- `JsonRpcRequest.method` → `Arc<str>` (cloned on every JSON-RPC request)
- Neural router types: `DiscoveredPrimal.name`, `RoutingMetrics`, `RegisteredCapability` → `Arc<str>`

### tarpc Binary Protocol

- Created `tarpc_client.rs` with `connect_tarpc_health()`, `connect_tarpc_discovery()`, `connect_tarpc_security()`
- `forward_via_tarpc()` now uses actual tarpc binary protocol (Bincode over Unix sockets) for health/discovery/security methods
- Added `serve_tarpc_health()` server helper in `biomeos-primal-sdk`
- Connected protocol escalation engine to verify tarpc connections
- Falls back to JSON-RPC for unrecognized methods

### Production Panic Removal

- Only production `panic!()` in `pipeline.rs` replaced with `GraphError::NodeNotFound` + `?` propagation
- All other panics confirmed to be test-only

### Code Quality

- Reviewed 77 `#[allow(clippy::*)]` directives; `too_many_arguments` refactored to `PrimalCommandConfig` struct
- `neural_router.rs` split into 4 domain modules (types/discovery/forwarding/mod)
- Tests extracted from `neural_graph.rs`, `discovery.rs`, `capability.rs`
- +60 new tests across graph handlers, neural executor, atomic client, beacon genetics, connection strategy, vm federation

### Cleanup

- Removed backup debris (`livespore-usb/.family.seed.backup-usb-original`, `primals.bak.*`)
- Removed duplicate template (`test-deployment.yaml` = `test-biome.yaml`)
- Removed biomeOS-local `wateringHole/` duplicate (canonical lives in `ecoPrimals/wateringHole/`)
- Archived stale `docs/handoffs/` (Feb 2026) to wateringHole archive

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Edition | 2021 | **2024** |
| Tests | 5,108 | **5,168** |
| Coverage | 77.47% | **77.92%** |
| Clippy | PASS | PASS |
| Fmt | PASS | PASS |
| Docs | PASS | PASS |
| Unsafe | 0 | 0 |
| Production panics | 1 | **0** |
| `unwrap_used`/`expect_used` | warn | **deny** |
| Hardcoded primal names in logic | ~100 | ~30 (tests only) |
| tarpc binary protocol | scaffolding | **implemented** |

---

## Remaining Gaps (for future sessions)

### Coverage (77.92% → 90% target)
- Binary entry points at 0% (899 lines in `tower.rs` alone) — need integration/E2E harness
- Network-dependent code needs mock infrastructure
- Deep async paths need full pipeline test scenarios
- E2E/chaos/fault test infrastructure not yet built

### Hardcoded Primal Names
- ~30 remaining instances in test code (acceptable for fixtures)
- Adapter type aliases kept for backward compatibility

### Files Approaching 1000 Lines
- `socket_discovery/engine.rs` (894), `atomic_client.rs` (929), `networking.rs` (904) — tightly coupled, further splitting needs broader restructure

---

## Standards Compliance

| Standard | Status |
|----------|--------|
| Rust Edition 2024 | Compliant |
| ecoBin v3.0 | Compliant (Pure Rust) |
| AGPL-3.0-only | Compliant |
| `forbid(unsafe_code)` | All crates except `biomeos-test-utils` (uses `deny`) |
| No hardcoded primal names | Compliant in production logic |
| Capability-based discovery | Implemented |
| JSON-RPC 2.0 + tarpc | Both implemented |
| Zero-copy | `Arc<str>` on hot paths, `Bytes` for binary payloads |
| Semantic method naming | Compliant |
| XDG paths | Compliant |
| Max 1000 lines/file | Compliant |
| Sovereignty / Human Dignity | Implemented and tested |
