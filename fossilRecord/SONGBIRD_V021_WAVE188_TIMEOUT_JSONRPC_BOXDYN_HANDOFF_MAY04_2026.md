# Songbird v0.2.1 — Wave 188 Handoff

**Date**: May 4, 2026  
**Wave**: 188 — Timeout centralization (wave 2), JSONRPC_VERSION consolidation, Box<dyn Error> elimination  
**Status**: Complete  
**Tier**: S+ (deep debt pass)

---

## Changes

### Timeout Centralization (Wave 2)

15 new constants added to `songbird-types/src/defaults/timeouts.rs`:

- `DEFAULT_TLS_HANDSHAKE_TIMEOUT` (10s)
- `DEFAULT_TLS_RECORD_READ_TIMEOUT` (5s)
- `DEFAULT_POST_HANDSHAKE_READ_WINDOW` (200ms)
- `DEFAULT_IPC_JSON_READ_TIMEOUT` (30s)
- `DEFAULT_POOL_MAX_IDLE_TIME` (300s)
- `DEFAULT_POOL_ACQUIRE_TIMEOUT` (5s)
- `DEFAULT_SECURITY_RPC_TIMEOUT` (10s)
- `DEFAULT_NEURAL_API_TIMEOUT` (5s)
- `DEFAULT_MDNS_TIMEOUT` (3s)
- `DEFAULT_DNSSD_TIMEOUT` (5s)
- `DEFAULT_HOLE_PUNCH_ATTEMPT_TIMEOUT` (200ms)
- `DEFAULT_HOLE_PUNCH_ATTEMPT_DELAY` (50ms)
- `DEFAULT_RELAY_WAIT_CYCLE` (300s)
- `DEFAULT_CONTAINER_API_TIMEOUT` (10s)

Replaced 10+ scattered `Duration` literals across TLS handshake, IPC client, security RPC, discovery, relay, and execution modules.

### JSONRPC_VERSION Consolidation

20 `"2.0".to_string()` heap allocations replaced with `JSONRPC_VERSION.into()` using local `&str` constants:
- `unix_listener.rs` (14 sites)
- `security_rpc_client/rpc.rs` (2 sites)
- `crypto-provider/rpc.rs` (4 sites)

### Box<dyn Error> Elimination

Fully eliminated from `songbird-test-utils`:
- `concurrent_helpers.rs` type alias → `anyhow::Result`
- 4 mock providers evolved (security, compute, AI, storage)
- `capability_mocks.rs` tests evolved
- `chaos_activation_test.rs` evolved

### Primal-Name Evolution

Final "BearDog" comment in `security_rpc_client/rpc.rs` evolved to "security provider".

### Dependency Update

- `serde_with` 3.18 → 3.19
- `tokio` 1.52.1 → 1.52.2

---

## Verification

- 0 clippy warnings (`-D warnings`)
- All 506 lib tests pass
- All songbird-test-utils tests pass
- `cargo fmt --check` clean
- 37 files changed across 8 crates

---

## Remaining Debt Surface

| Category | Status |
|----------|--------|
| Scattered Duration literals | ~5 remaining (discovery constructors with `with_timeout` builder pattern, protocol_api UNIX_EPOCH fallback) |
| Legacy primal env vars | Intentional deprecation shims with `tracing::warn!` — backward compat, not debt |
| Duplicate deps (thiserror 1/2, syn 1/2, base64 0.21/0.22) | Upstream-blocked (kube-client, tarpc, derivative) |
| Coverage 73.41% → 90% | I/O-heavy paths need E2E infrastructure |
