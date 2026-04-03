# Songbird v0.2.1-wave97: Capability-Based Discovery Compliance

**Date**: 2026-04-02
**Commit**: `c4d7f3af0`
**Status**: COMPLIANT (was NON-COMPLIANT)
**Priority**: 2 (from primalSpring downstream audit)

## Summary

Replaced all `discover_beardog*` calls with capability-based `discover_security_provider_socket`
across 13 crates (53 files). Songbird now discovers crypto/security by **capability domain**
(`"security"`), not by primal identity (`"beardog"`), per wateringHole v1.2 standard.

## What Changed

### Discovery Priority Chain (new standard)

```
1. $SECURITY_PROVIDER_SOCKET   (capability-standard env var)
2. $CRYPTO_PROVIDER_SOCKET     (alternate capability name)
3. $XDG_RUNTIME_DIR/biomeos/security.sock  (capability symlink)
4. $XDG_RUNTIME_DIR/biomeos/crypto.sock    (domain socket)
5. $BEARDOG_SOCKET             (legacy — logged as deprecated)
6. /tmp/biomeos/security.sock  (fallback)
```

### Crate-by-Crate

| Crate | Changes |
|-------|---------|
| `songbird-crypto-provider` | Canonical `discover_security_provider_socket()` with full priority chain; `routing_mode_from_env()` checks `SECURITY_PROVIDER_MODE` before `BEARDOG_MODE`; new `security_socket_path_in_biomeos_runtime()` |
| `songbird-http-client` | `discover_security_provider_socket()` with capability-first chain; re-exports updated |
| `songbird-tls` | Internal `discover_security_provider_socket_with_env()` (was already capability-first, now renamed); Windows/other platform fallbacks add `SECURITY_PROVIDER_SOCKET` |
| `songbird-orchestrator` | 15 callers migrated: `app/core.rs`, `security_client/client.rs`, `http_gateway/mod.rs`, `ipc/handlers/http.rs`, `ipc/unix/handlers/{encryption,health}.rs`, `btsp_client.rs`, `primal_discovery.rs`, config templates |
| `songbird-universal-ipc` | birdsong handler, tor handler, unix platform, http handler all use capability-first discovery |
| `songbird-nfc` | Config discovery renamed, genesis comments updated |
| `songbird-execution-agent` | `discover_security_provider()` with deprecated `discover_beardog()` alias |
| `songbird-sovereign-onion` | Module docs updated for `SECURITY_PROVIDER_MODE` |
| `songbird-network-federation` | beardog module and rendezvous client check `SECURITY_PROVIDER_SOCKET` first |
| `songbird-lineage-relay` | Socket discovery docs aligned |
| `songbird-types` | Added `SECURITY_SOCKET_DEFAULT`, `SECURITY_SOCKET_TMP_FALLBACK` constants |
| `songbird-test-utils` | Fixture docs updated |

### Backward Compatibility

All deprecated `discover_beardog_socket()` functions are preserved as thin wrappers with
`#[deprecated(note = "Use discover_security_provider_socket")]` annotations.
Legacy `BEARDOG_SOCKET` env var still works as a fallback in the discovery chain.

## Metrics

- **53 files changed**, 610 insertions, 386 deletions
- **0 clippy warnings** (workspace-wide)
- **All tests pass** (workspace-wide)
- **16 remaining `discover_beardog` refs** — all deprecated aliases or `#[allow(deprecated)]` re-exports
- **Bootstrap exception**: `SECURITY_PROVIDER_MODE=direct` documented for pre-Neural-API crypto bootstrap

## Known Exceptions

- **Bootstrap case**: When Songbird needs crypto before Neural API is available, it uses
  `SECURITY_PROVIDER_MODE=direct` (or legacy `BEARDOG_MODE=direct`) to bypass capability.call
  routing. Documented in `songbird-crypto-provider` module docs.
- **BearDog module/struct names** (`BearDogProvider`, `beardog_crypto`, `BearDogClient`): These are
  internal abstraction names, not discovery violations. They wrap the security capability interface
  and will be renamed in a future wave if desired.

## Cross-Primal Impact

- BearDog: No changes needed — it already publishes `security.sock` capability symlink
- Neural API: Routing via `capability.call("security", ...)` unchanged
- All primals: Can now set `SECURITY_PROVIDER_SOCKET` instead of primal-specific env vars
