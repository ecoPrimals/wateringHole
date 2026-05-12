# Songbird v0.2.1 — Wave 159 — Deep Debt: Port Centralization & Constant Cleanup

**Date**: April 15, 2026
**Crate**: Songbird (primals/songBird)
**Wave**: 159
**Trigger**: Comprehensive deep debt audit — deprecated constants, scattered port defaults, stale features

---

## Problem

Comprehensive audit revealed:
- 12 deprecated port constants in `songbird-types::constants` with zero external consumers
- 4 crates defining their own local port constants duplicating `defaults::ports`
- 3 stale feature flags declared but never referenced in source
- 1 dead legacy constant (`NESTGATE_AUTHENTICATION_PURPOSE`) with zero callers
- `DEFAULT_ORCHESTRATOR_PORT` value mismatch (8000 in types vs 8080 actual HTTP API)
- `songbird-config::config::constants::network` maintaining local copies of constants already defined in `songbird-types`

## Changes

### Removed (zero-consumer deprecated items)
- `DEFAULT_HTTP_PORT`, `DEFAULT_HTTPS_PORT`, `DEFAULT_DISCOVERY_PORT`, `DEFAULT_FEDERATION_PORT`, `DEFAULT_HEALTH_PORT`, `DEFAULT_DASHBOARD_PORT`, `DEFAULT_METRICS_PORT`, `DEFAULT_ORCHESTRATOR_PORT`, `DEFAULT_CRYPTO_TRANSPORT_PORT`, `DEFAULT_SECURITY_VAULT_PORT`, `DEFAULT_FEDERATION_BIND_PORT` from `songbird-types::constants`
- `NESTGATE_AUTHENTICATION_PURPOSE` from `songbird-orchestrator::auth::security_jwt_client`
- `gaming`, `federation` feature flags from `songbird-network-federation`
- `test-mocks` feature flag from `songbird-bluetooth`

### Centralized (scattered → defaults::ports)
- `DEFAULT_BIRDSONG_PORT` (42424): added to `defaults::ports`, `songbird-lineage-relay` now imports
- `DEFAULT_QUIC_PORT` (4433): added to `defaults::ports`, `songbird-quic` now re-exports
- `DEFAULT_STUN_PORT` (3478): `songbird-universal-ipc` and `songbird-onion-relay` now import from `defaults::ports`

### Aligned
- `DEFAULT_ORCHESTRATOR_PORT`: 8000 → 8080 (matching actual HTTP API port)
- `songbird-config::constants::network`: local definitions replaced with re-exports from `songbird-types`

## Verification

- `cargo check`: 0 errors, 0 warnings
- `cargo clippy --workspace`: 0 warnings
- `cargo fmt --check`: clean
- `cargo test --workspace --lib`: all pass (7,387+), 0 failures

## Retained (migration aids, correct pattern)

Legacy primal-name env vars (`BEARDOG_ENDPOINT`, `NESTGATE_ENDPOINT`, `SQUIRREL_ENDPOINT`, `TOADSTOOL_ENDPOINT`) and their `SONGBIRD_ENABLE_*` counterparts are properly implemented as fallback discovery paths with `tracing::warn!()` deprecation messages. This is the correct pattern for gradual migration — removal would break deployments that haven't updated their environment configuration. `serde(alias = "...")` wire-compat aliases follow the same principle.

Legacy socket filenames (`LEGACY_SECURITY_SOCKET_FILENAME`, etc.) serve as on-disk migration constants with documented fallback paths and deprecation warnings in consuming code.

## What Remains

Per `REMAINING_WORK.md`:
1. **BTSP Phase 3**: E2E integration test, `btsp.server.export_keys`, encrypted framing
2. **Coverage**: 72.29% → 90% target
3. **Dependency evolution**: `serde_yaml` removal, `bincode` advisory, transitive duplicates
4. **Platform**: NFC backends, hardware IGD, Genesis physical channels
