# Songbird v0.2.1 — Wave 128: Socket Gap Resolved — L2 on songbird.sock

**Date**: April 8, 2026  
**Primal**: Songbird  
**Wave**: 128  
**Status**: Complete — Socket Gap (Medium) resolved  
**Commit**: `67c260b7`  
**Audit Item**: primalSpring — Songbird Socket Gap (Medium)

---

## Problem

biomeOS discovers Songbird via `songbird.sock` and probes Wire Standard L2 methods (`capabilities.list`, `identity.get`, `health.liveness`). The orchestrator's primary Unix socket handler (`UnixSocketServer::handle_jsonrpc_request` in `pure_rust_server/server/handlers.rs`) only had explicit dispatch arms for:
- `health.liveness`, `health.readiness`, `health.check`
- `ipc.register`
- `discover_capabilities`
- `http.request`, `http.get`, `http.post`

All other parsed `JsonRpcMethod` variants — including `capabilities.list`, `capabilities.methods`, `identity`, `identity.get` — hit the catch-all: `Ok(_) => Err(method_not_found)`.

The HTTP gateway (`server/jsonrpc_api/mod.rs`) correctly handled all L2 methods, creating an asymmetry: HTTP worked, socket didn't.

## Fix

Added 4 dispatch arms to `pure_rust_server/server/handlers.rs`, calling the same `songbird_universal_ipc::introspection::*` helpers used by the HTTP gateway:

```rust
Ok(JsonRpcMethod::Capabilities(CapabilitiesMethod::List)) => {
    Ok(songbird_universal_ipc::introspection::capabilities_list())
}
Ok(JsonRpcMethod::Capabilities(CapabilitiesMethod::Methods)) => {
    Ok(songbird_universal_ipc::introspection::capabilities_methods())
}
Ok(JsonRpcMethod::Identity) => {
    Ok(songbird_universal_ipc::introspection::identity(&crate::env_config::family_id()))
}
Ok(JsonRpcMethod::IdentityGet(_)) => {
    Ok(songbird_universal_ipc::introspection::identity_get())
}
```

## Tests Added

7 new tests in `pure_rust_server/server/mod.rs`:
- `wire_standard_l2_capabilities_list_on_socket` — verifies `{primal, version, methods}` envelope
- `wire_standard_l2_capabilities_methods_on_socket` — verifies token→method map
- `wire_standard_l2_identity_get_on_socket` — verifies `{primal, version, domain, license}`
- `wire_standard_l2_identity_on_socket` — verifies legacy identity response
- `wire_standard_l2_health_triad_on_socket` — liveness, readiness, check
- `socket_unknown_method_returns_error` — negative case

## Verification

biomeOS can now probe `songbird.sock` with any L2 method and receive correct responses:
- `capabilities.list` → `{"primal": "songbird", "version": "0.2.1", "methods": [...]}`
- `identity.get` → `{"primal": "songbird", "version": "0.2.1", "domain": "network", "license": "AGPL-3.0-or-later"}`
- `health.liveness` → `{"status": "alive"}`

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 12,922 passed, 0 failed, 252 ignored |
| Clippy | Clean |
| Format | Clean |
