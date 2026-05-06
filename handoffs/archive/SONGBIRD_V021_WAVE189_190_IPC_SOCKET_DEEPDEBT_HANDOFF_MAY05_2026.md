# Songbird v0.2.1 — Waves 189–190 Handoff

**Date**: May 5, 2026  
**Primal**: Songbird  
**Version**: v0.2.1  
**Waves**: 189–190  
**Status**: Complete — pushed

---

## Wave 189: `ipc.resolve` Socket Field for primalSpring Tier-1 Discovery

### Problem
primalSpring's `CompositionContext::discover()` expects `ipc.resolve` to return a bare filesystem socket path in a `socket`, `native_endpoint`, or `endpoint` field. Songbird's `native_endpoint` returned `unix:///path` (scheme-prefixed URI) — incompatible with `PathBuf::from()` in primalSpring.

### Solution
- Added `NativeEndpoint::socket_path()` method — extracts bare connect-ready path (Unix → `/path`, Abstract → `@name`, TCP → `addr:port`)
- Added `socket: Option<String>` field to `ResolveResult`, `ProviderInfo`, `CapabilityResolveResult` response structs
- Wired `socket` population into `ipc.resolve`, `ipc.discover`, `capability.resolve` handlers via `entry.native_endpoint.socket_path()`
- Field uses `#[serde(skip_serializing_if = "Option::is_none")]` — backward compatible

### Files Changed
- `songbird-universal-ipc/src/endpoint.rs` — `socket_path()` method
- `songbird-universal-ipc/src/service_types.rs` — `socket` field on 3 structs + tests
- `songbird-universal-ipc/src/service/ipc_registry.rs` — wiring
- `songbird-universal-ipc/src/service/service_tests.rs` — test updates

---

## Wave 190: Hardcoded Literal Cleanup & Robust Parsing

### Changes
1. **IP literals centralized**: `endpoint.rs` TcpLocal display/socket_path use `LOCALHOST` constant; `udp_hole_punch.rs` uses `EPHEMERAL_BIND_ADDR`
2. **Redundant clone eliminated**: `circuit_breaker.rs` `stats()` — computed `current_failures` from `&state`, moved once into struct
3. **Robust endpoint parsing**: New `parse_endpoint()` helper in `tarpc_server.rs` handles IPv6 `[::1]:port`, `tcp://host:port`, and port-less hostnames. Replaces fragile `split(':').nth(1).unwrap_or(0)` in tarpc_server + websocket_api
4. **Test Duration literals**: `concurrent_helpers.rs` extracted `DEFAULT_READINESS_TIMEOUT`, `DEFAULT_COMPLETION_TIMEOUT`, `DEFAULT_BARRIER_TIMEOUT`
5. **Integration test fix**: `load_balancer_comprehensive_tests.rs` evolved from `assert_eq!(anyhow::Error, &str)` to `.to_string().contains()`

### Files Changed
- `songbird-universal-ipc/src/endpoint.rs`
- `songbird-lineage-relay/src/udp_hole_punch.rs`
- `songbird-orchestrator/src/resilience/circuit_breaker.rs`
- `songbird-orchestrator/src/server/tarpc_server.rs`
- `songbird-orchestrator/src/server/websocket_api.rs`
- `songbird-test-utils/src/concurrent_helpers.rs`
- `songbird-orchestrator/tests/load_balancer_comprehensive_tests.rs`

---

## Verification
- 0 clippy warnings (`-D warnings`)
- `cargo fmt --check` clean
- 506 lib tests pass
- 13 load_balancer integration tests pass
- All workspace crates compile clean

---

## Remaining Debt (Post-Wave 190)
- Coverage 73.41% → 90% target (I/O-heavy paths)
- `Result<_, String>` in JSON-RPC handler layer (trait constraint — architectural)
- Transitive duplicate deps blocked on upstream (kube, tarpc, derivative)
- Tor/TLS crypto blocked on live security provider
- `bincode` 1.x (RUSTSEC-2025-0141) — blocked on tarpc upstream
