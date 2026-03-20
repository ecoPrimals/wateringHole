# Songbird v0.3.2 Handoff — Deep Audit Evolution & Capability Purity

**Primal**: Songbird (Network Orchestration & Discovery)  
**Date**: March 20, 2026  
**Version**: v0.3.2  
**Previous**: v0.3.1 (Full Compliance, Edition 2024, UniBin Consolidation)  
**License**: AGPL-3.0-only (scyBorg provenance trio)

---

## Session Summary

Multi-session deep audit and evolution pass. Resolved all compilation blockers, evolved production stubs to real implementations, purified discovery to capability-only (zero primal names), wired JSON-RPC handlers to live registries, fixed test deadlocks, established coverage baseline at 62.04%, and cleaned debris.

---

## What Changed

### 1. Production Code Evolution (Stubs → Real Implementations)

| Area | Before | After |
|------|--------|-------|
| `ProductionServiceDiscovery` | All methods returned `Ok(vec![])` or `Ok(())` | Real filtering, registration, health updates, live watch stream |
| JSON-RPC `services.list/get/register` | Returned `"not_implemented"` | Wired to `FederatedServiceRegistry` CRUD |
| JSON-RPC `federation.peers/join` | Returned `"not_implemented"` | Wired to `FederationState` node management |
| iOS XPC `create_endpoint` | `warn!()` stub | Returns `InProcess` fallback with clear error on XPC variants |
| `production_storage.rs` | Syntax-corrupted, uncompilable | Full rewrite, correct struct definitions, filesystem persistence |

### 2. Capability-Only Discovery (Zero Primal Names)

All discovery paths purged of hardcoded primal names (`beardog`, `squirrel`, `nestgate`, `toadstool`):

- `primal_discovery.rs`: socket patterns, TCP discovery, socket scanning — all capability terms only
- `auth/capability_discovery.rs`: search terms (`security`, `auth`, `encryption`) and socket paths
- `crypto/discovery.rs`: search terms and common socket paths
- `btsp/provider.rs`: UPA endpoint configurable via `SONGBIRD_UPA_ENDPOINT`
- `connection_manager.rs`, `capability_query.rs`, `container.rs`, `network.rs`: capability-based inference
- `primal_self_knowledge.rs`: capability-term inference from process name
- All e2e and unit tests updated to use capability-named sockets (`crypto.sock`, `http.sock`, etc.)

### 3. Hardcoding Elimination

- SSH deploy user: `default_value = "eastgate"` → `$USER` with `"root"` fallback
- Tower CLI: port/bind now respect `SONGBIRD_HTTP_PORT` / `SONGBIRD_BIND_ADDRESS` env vars
- BTSP provider URL: hardcoded `localhost:8080` → `SONGBIRD_UPA_ENDPOINT` env var

### 4. Test Infrastructure Fixes

- **Deadlock fix**: `env_isolation.rs` tests were double-acquiring `ENV_LOCK` (manual + `ScopedEnv` internal), causing workspace test hangs. Removed redundant manual locks.
- **E2e test evolution**: All XDG socket discovery e2e tests updated for capability-named sockets

### 5. Debris Cleanup

- Archived orphaned `network/scan.rs` (dead code, syntax-corrupted, never compiled)
- Archived superseded local handoffs to fossil record
- Moved v0.3.0/v0.3.1 wateringHole handoffs to `handoffs/archive/`

---

## Current Metrics

| Metric | Value |
|--------|-------|
| Tests | ~6,100+ passed, 0 failed |
| Line Coverage | 62.04% (148,723 instrumented lines, cargo llvm-cov) |
| Clippy | 29/29 crates clean (pedantic + nursery, `-D warnings`) |
| Production `todo!()` | 0 |
| Production `FIXME`/`HACK` | 0 |
| Production `unimplemented!()` | 0 |
| JSON-RPC handlers | All wired to live registries |
| Capability discovery | Pure (zero primal name strings in discovery logic) |
| Files >1000 lines | 0 |

---

## Known Remaining

1. **Coverage gap** (62% → 90% target): lowest coverage in `tarpc_client.rs` (31%), `tower_atomic.rs` (38%), iOS platform stub (15%), container/network discovery backends (~47-52%)
2. **`ring` C dependency**: structural via `quinn` + `rcgen`; requires quinn feature reconfiguration or upstream pure-Rust QUIC
3. **Database persistence backend**: `production_storage.rs` DB methods fall back to filesystem with `warn!()`
4. **Streaming upload**: `http_deploy.rs` streaming method falls back to single upload with `warn!()`
5. **Template transformation**: `universal_proxy.rs` template engine not yet integrated

---

## Files Modified (Key)

- `crates/songbird-orchestrator/src/server/jsonrpc_api.rs`
- `crates/songbird-orchestrator/src/primal_discovery.rs`
- `crates/songbird-orchestrator/src/auth/capability_discovery.rs`
- `crates/songbird-orchestrator/src/crypto/discovery.rs`
- `crates/songbird-discovery/src/production/real_service_discovery.rs`
- `crates/songbird-universal/src/discovery/backends/{network,container}.rs`
- `crates/songbird-universal/src/capabilities/adapter/{connection_manager,capability_query}.rs`
- `crates/songbird-discovery/src/primal_self_knowledge.rs`
- `crates/songbird-network-federation/src/btsp/provider.rs`
- `crates/songbird-universal-ipc/src/platform/ios.rs`
- `crates/songbird-registry/src/persistence/production_storage.rs`
- `crates/songbird-remote-deploy/src/deploy.rs`
- `crates/songbird-test-utils/src/env_isolation.rs`
- `crates/songbird-cli/src/cli/commands/tower.rs`
- `crates/songbird-orchestrator/tests/xdg_socket_discovery_e2e.rs`

---

## Handoff Notes

- All changes pass `cargo clippy --workspace --all-features -- -D warnings` with zero warnings
- All changes pass `cargo fmt --all --check`
- All orchestrator tests pass (653 lib + 8 e2e, 0 failed)
- Coverage baseline established; next session can target specific low-coverage modules
- The `examples/legacy/` and `examples/future/` directories are retained as documentation but are not wired as Cargo examples
