# NestGate v4.7.0-dev Session 54 Handoff

**Date**: May 5, 2026
**Session**: 54
**Trigger**: primalSpring downstream audit — protocol standardization + discovery hierarchy

---

## Summary

All `capabilities.list` surfaces upgraded to Wire Standard L3 with machine-readable
`protocol` and `transport` fields. Transport array expanded to include TCP.
Consumed capability naming aligned. Discovery tier support documented.

---

## What Changed

### Wire Standard L3 on All Surfaces

Previously only the UDS legacy dispatch returned `protocol` and `transport` in
`capabilities.list`. Now all four active surfaces return L3:

- **UDS legacy** (`model_cache_handlers.rs`)
- **HTTP JSON-RPC** (`jsonrpsee capability_methods.rs`)
- **Semantic router** (`semantic_router/capabilities.rs`)
- **Isomorphic IPC adapter** (`unix_adapter_handlers.rs`)

Response shape on all surfaces:
```json
{
  "primal": "nestgate",
  "version": "...",
  "methods": [...],
  "protocol": "jsonrpc-2.0",
  "transport": ["uds", "tcp", "http"]
}
```

### Transport Expanded

`["uds", "http"]` → `["uds", "tcp", "http"]` to reflect `TcpFallbackServer`
(newline-delimited JSON-RPC 2.0 over TCP, activated via `--port`/`--listen`/
`NESTGATE_JSONRPC_TCP`).

Updated in: code (all 4 surfaces), `capability_registry.toml`, cross-check
test `transport_includes_uds_tcp_http`.

### Consumed Capabilities Aligned

`"type": "discovery"` → `"type": "discovery_mesh"` in `capabilities_list()`
to match `capability_registry.toml` TOML key. `CAPABILITY_MAPPINGS.md` corrected:
stale `"network"` consumed capability replaced with actual entries.

### `discover_capabilities` Upgraded

Now includes `protocol` and `transport` fields alongside the existing
`capabilities`/`backend` response.

### Discovery Tiers Documented

STATUS.md now explicitly documents:
- **Tier 3**: UDS filesystem convention (`storage-{fid}.sock` symlink)
- **Tier 4**: Socket registry / manifest (`capability_registry.toml`)
- **Tier 5**: TCP probing (when `--port` active)
- **Tiers 1-2**: Songbird `ipc.resolve` / biomeOS `capability.discover`
  handled by orchestration layer

---

## Verification

```
cargo fmt --all --check          PASS
cargo clippy --workspace         PASS (zero own-code warnings)
  --all-targets -- -D warnings
cargo test --workspace --lib     8,872 passing / 0 failures / 60 ignored
```

---

## Downstream Impact

- **All consumers** of `capabilities.list` on any surface now receive `protocol`
  and `transport` fields — machine-readable protocol discovery as requested by
  primalSpring audit
- **biomeOS routing**: `transport` array enables programmatic detection of NestGate's
  TCP availability without port probing
- **`consumed_capabilities`** naming change (`discovery` → `discovery_mesh`) may
  affect consumers that parse the type field literally
