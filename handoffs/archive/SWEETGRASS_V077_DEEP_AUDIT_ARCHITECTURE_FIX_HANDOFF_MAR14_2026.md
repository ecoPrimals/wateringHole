# SweetGrass v0.7.7 — Deep Audit + Architecture Fix + UniBin Compliance

**Date**: March 14, 2026
**From**: v0.7.6 → v0.7.7
**Status**: Complete — all checks pass

---

## Summary

Comprehensive audit of sweetGrass against wateringHole standards with execution on all findings. Critical architecture bug fixed, full clippy compliance restored, UniBin binary naming corrected, typed errors throughout, stale specs updated.

---

## Critical: tarpc Shared State

The tarpc server was constructing its own `MemoryStore`, `BraidFactory`, `QueryEngine`, etc. — completely isolated from the HTTP/JSON-RPC stack which used the bootstrapped `AppState` (potentially postgres, redb, or sled).

**Data created via REST/JSON-RPC was invisible to tarpc and vice versa.**

### Fix

- `SweetGrassServer.store` evolved from `Arc<MemoryStore>` to `Arc<dyn BraidStore>`
- New `SweetGrassServer::from_app_state(&AppState)` constructor shares all state
- `spawn_tarpc_server()` in binary now takes `&AppState` instead of constructing its own
- `store_type` in status response reports actual backend (was hardcoded `"memory"`)

**Inter-primal impact**: Any primal connecting to sweetGrass via tarpc now sees the same data as JSON-RPC/REST callers. Previously they would have seen an empty store.

---

## Changes

### Architecture

| Change | Before | After |
|--------|--------|-------|
| tarpc store | Separate `MemoryStore` | Shared `Arc<dyn BraidStore>` from `AppState` |
| Binary name | `sweet-grass-service` | `sweetgrass` (UniBin compliant) |
| `start_tarpc_server` return | `Box<dyn Error>` | `Result<(), ServiceError>` |
| UDS listener return | `Box<dyn Error>` | `Result<(), ServiceError>` |
| `http_health_check` return | `Box<dyn Error>` | `Result<String, String>` |
| `ServiceError` variants | 8 | 9 (added `Io`) |

### Specs

- `specs/ARCHITECTURE.md` crate layout rewritten — removed stale gRPC/proto/GraphQL/SPARQL/listener references, aligned with actual 10-crate structure

### Quality

| Metric | v0.7.6 | v0.7.7 |
|--------|--------|--------|
| Tests | 843 | 849 |
| Clippy `--all-targets` | FAIL (8 errors) | PASS |
| `Box<dyn Error>` in prod | 4 functions | 0 |
| Binary name | `sweet-grass-service` | `sweetgrass` |
| Sled corruption test | Flaky | Fixed |

---

## Test Results

```
849 passed, 0 failed, 34 ignored
cargo fmt --check: PASS
cargo clippy --all-targets --all-features -D warnings: PASS
cargo doc --no-deps -D warnings: PASS
0 unsafe blocks (all crates #![forbid(unsafe_code)])
All files under 1000 lines (max: 828)
108/108 .rs files have SPDX headers
```

---

## Compliance Audit Results

| Standard | Status |
|----------|--------|
| UniBin | PASS (binary = `sweetgrass`, subcommands, exit codes) |
| ecoBin | PASS (pure Rust, cross-compilation, platform-agnostic IPC) |
| JSON-RPC 2.0 | PASS (semantic `{domain}.{operation}` naming) |
| tarpc first | PASS (shared state, primary RPC) |
| Capability-based discovery | PASS (no hardcoded primal names) |
| AGPL-3.0-only | PASS (LICENSE, Cargo.toml, SPDX headers, deny.toml) |
| No gRPC/protobuf | PASS (deny.toml bans, 0 in dep tree) |
| No outbound HTTP | PASS (reqwest/ureq banned) |
| Sovereignty | PASS (no telemetry, pure Rust crypto, zero C deps) |
| Human dignity | PASS (privacy module, consent, zero vendor lock-in) |

---

## Files Modified

```
crates/sweet-grass-service/src/server/mod.rs      — SweetGrassServer generic, from_app_state
crates/sweet-grass-service/src/server/tests.rs     — Updated for Arc<dyn BraidStore>
crates/sweet-grass-service/src/bin/service.rs      — spawn_tarpc_server uses AppState
crates/sweet-grass-service/src/error.rs            — ServiceError::Io variant
crates/sweet-grass-service/src/uds.rs              — Typed errors
crates/sweet-grass-service/src/state.rs            — Removed unfulfilled lint expect
crates/sweet-grass-service/src/lib.rs              — Re-exports
crates/sweet-grass-service/Cargo.toml              — Binary name = "sweetgrass"
crates/sweet-grass-core/src/scyborg.rs             — Test allow attribute
crates/sweet-grass-integration/src/discovery/tests.rs — String::new() lint fix
crates/sweet-grass-store-sled/src/store/tests.rs   — Flaky test fix + similar_names
specs/ARCHITECTURE.md                              — Full crate layout rewrite
Cargo.toml                                         — Version 0.7.7
README.md, DEVELOPMENT.md, CHANGELOG.md, ROADMAP.md, QUICK_COMMANDS.md — Updated
deploy.sh                                          — Binary name fix
```

---

## Next Steps (v0.8.0)

- Connect to deployed signing service (Capability::Signing)
- Connect to deployed anchoring service (Capability::Anchoring)
- End-to-end multi-primal integration testing
- Chemistry entity types for wetSpring
