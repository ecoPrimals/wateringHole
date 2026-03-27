<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.25 Handoff — Ecosystem Absorption & Modern Idiomatic Rust Evolution

**Date**: 2026-03-24
**Primal**: Squirrel (AI Coordination)
**Phase**: Foundation
**From**: alpha.24 → alpha.25

---

## Summary

Absorbed ecosystem patterns from springs and primals (BearDog health tiering,
SweetGrass env-configurable retry, rhizoCrypt Arc<dyn>, LoamSpine JSON-RPC 2.0
strictness, barraCuda/BearDog normalize_method). Added `identity.get` handler
per CAPABILITY_BASED_DISCOVERY_STANDARD v1.0. Tightened cast safety lints.
Cleaned MCP resilience module for modern idiomatic Rust.

## Before / After

| Metric | alpha.24 | alpha.25 |
|--------|----------|----------|
| Tests | 7,035 | 7,065 |
| Exposed capabilities | 24 | 25 |
| `Arc<Box<dyn>>` in production | 2 files | 0 |
| Cast safety lints | none | 3 warns (truncation, sign, precision) |
| Health response | flat status | 3-tier (alive/ready/healthy) |
| JSON-RPC validation | version only | method + params + notifications |
| Retry policy | hardcoded | env-configurable (primal→IPC→default) |
| Method prefix normalization | none | squirrel.*/mcp.* stripped |
| Build | GREEN | GREEN |
| Clippy | CLEAN | CLEAN |
| Format | CLEAN | CLEAN |

## What Was Done

### Phase A: Compliance & New Handlers

1. **`identity.get` handler** (`handlers_identity.rs`)
   - Returns primal self-knowledge: id, domain, version, transport, protocol, license, JWT claims
   - Registered in dispatch match, `capability_registry.toml`, `niche.rs`
   - Per CAPABILITY_BASED_DISCOVERY_STANDARD v1.0

2. **`normalize_method()`** (`jsonrpc_server.rs`)
   - Strips `squirrel.` and `mcp.` prefixes before dispatch
   - Enables `squirrel.system.health` → `system.health` for ecosystem backward compatibility
   - Per BearDog v0.9.0, barraCuda v0.3.7 pattern

3. **JSON-RPC 2.0 strictness** (`jsonrpc_server.rs`)
   - Validates `method` field: must be present, non-empty string
   - Validates `params`: must be object or array when present
   - Single-request notifications: no response body (was only handled in batches)
   - Standard error codes: `SERVER_ERROR_MIN`/`SERVER_ERROR_MAX` (-32099 to -32000)

### Phase B: Modern Idiomatic Rust

4. **Cast safety lints** (`Cargo.toml`)
   - `cast_possible_truncation = "warn"`, `cast_sign_loss = "warn"`, `cast_precision_loss = "warn"`
   - Zero violations found across entire workspace

5. **`Arc<Box<dyn>>` → `Arc<dyn>`** (MCP crate)
   - `circuit_breaker/breaker.rs`: `Arc<dyn CircuitBreakerState + Send + Sync>`
   - `plugins/registry.rs`: `Arc<dyn Plugin>` with `Arc::from(plugin)`
   - Eliminates double indirection per rhizoCrypt pattern

### Phase C: Health Tiering & Retry

6. **Health tiering** (`handlers_system.rs`, `types.rs`)
   - `HealthTier` enum: `Alive`, `Ready`, `Healthy`
   - `HealthCheckResponse` extended with `tier`, `alive`, `ready`, `healthy` booleans
   - Alive = process running; Ready = providers initialized; Healthy = fully operational
   - tarpc service types updated (`TarpcRpcServer`, `HealthCheckResult`)

7. **Env-configurable retry** (`retry_policy.rs`)
   - `StandardRetryPolicy::from_env()` with primal→ecosystem→default chain
   - `SQUIRREL_RETRY_MAX_ATTEMPTS` → `IPC_RETRY_MAX_ATTEMPTS` → 3
   - `SQUIRREL_RETRY_BASE_DELAY_MS` → `IPC_RETRY_BASE_DELAY_MS` → 100
   - `SQUIRREL_RETRY_MAX_DELAY_MS` → `IPC_RETRY_MAX_DELAY_MS` → 5000
   - MCP resilience module exposed in `lib.rs`

### Phase D: MCP Resilience Cleanup

8. **30+ clippy fixes** in `retry.rs` and `retry_policy.rs`
   - `RetryFuture<T>` type alias (eliminates `type_complexity`)
   - Proper `Default` impls (replaced `pub fn default()`)
   - `const fn` on constructors
   - Integer jitter (no `cast_sign_loss`)
   - `std::io::Error::other()` instead of `Error::new(ErrorKind::Other, ...)`

### Phase E: Documentation Sync

9. **SQUIRREL_LEVERAGE_GUIDE.md** — alpha.11 → alpha.25
   - Added `identity.get`, `graph.parse`, `graph.validate` to IPC table
   - Marked `capabilities.list` as canonical
   - Added normalize_method, health tiering, JSON-RPC strictness sections
   - Updated license to AGPL-3.0-or-later

10. **CURRENT_STATUS.md** — alpha.24 → alpha.25
    - Identity domain in method table
    - 25 exposed capabilities
    - alpha.25 sprint changelog

11. **CONTEXT.md** — version alpha.25

12. **README.md** — updated test count, crate count, license
13. **CHANGELOG.md** — added alpha.24 and alpha.25 entries
14. **ORIGIN.md** — updated test count, license

## Files Changed

### New
- `crates/main/src/rpc/handlers_identity.rs`

### Modified (squirrel)
- `Cargo.toml` (cast lints)
- `capability_registry.toml` (identity.get)
- `crates/adapter-pattern-tests/Cargo.toml` (cast lints)
- `crates/core/mcp/src/lib.rs` (pub mod resilience)
- `crates/core/mcp/src/plugins/registry.rs` (Arc<dyn>)
- `crates/core/mcp/src/resilience/circuit_breaker/breaker.rs` (Arc<dyn>)
- `crates/core/mcp/src/resilience/mod.rs` (re-exports)
- `crates/core/mcp/src/resilience/resilience_error.rs` (trimmed)
- `crates/core/mcp/src/resilience/retry.rs` (30+ clippy fixes)
- `crates/core/mcp/src/resilience/retry_policy.rs` (from_env, Default, clippy)
- `crates/main/src/niche.rs` (identity.get)
- `crates/main/src/rpc/handlers_system.rs` (health tiering)
- `crates/main/src/rpc/jsonrpc_handlers.rs` (module doc)
- `crates/main/src/rpc/jsonrpc_handlers_tests.rs` (identity test)
- `crates/main/src/rpc/jsonrpc_server.rs` (normalize_method, identity dispatch, validation)
- `crates/main/src/rpc/jsonrpc_server_tests.rs` (normalize, health tier tests)
- `crates/main/src/rpc/mod.rs` (handlers_identity)
- `crates/main/src/rpc/tarpc_*.rs` (health tier fields)
- `crates/main/src/rpc/types.rs` (HealthTier, HealthCheckResponse)
- `crates/main/tests/proptest_roundtrip.rs` (health tier)
- `CHANGELOG.md`, `CONTEXT.md`, `CURRENT_STATUS.md`, `ORIGIN.md`, `README.md`

### Modified (wateringHole)
- `SQUIRREL_LEVERAGE_GUIDE.md`

## Known Issues

1. Coverage at 85.4% — remaining ~4.6% gap to 90% is demo binaries, IPC/network code, binary entry points
2. Performance optimizer `batch_processor`/`optimizer` stubs remain deferred to Phase 2
3. `ring` present as transitive via `rustls`/`sqlx`/`jsonwebtoken` — tracked in `docs/CRYPTO_MIGRATION.md`

## Recommended Next Steps

1. Coverage push toward 90% target (IPC integration tests, binary entry points)
2. `rand 0.8 → 0.9` upgrade (23 files, moderate effort)
3. `rustls-rustcrypto` evaluation when it reaches stable (pure Rust TLS)
4. Additional `identity.*` methods as ecosystem standardizes (e.g. `identity.capabilities`)
5. MCP `tools.list`/`tools.call` with JSON Schema alignment (biomeOS V251)
