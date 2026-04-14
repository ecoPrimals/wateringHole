# NestGate v4.7.0-dev — storage.fetch_external: TLS Boundary Implementation

**Date**: April 7, 2026
**Commit**: `bd28bbac` — `feat: implement storage.fetch_external — NestGate owns the TLS boundary`
**Branch**: `main`
**Resolves**: primalSpring BLOCKER — wetSpring V138 Exp310, Exp311

---

## Summary

Implemented the `storage.fetch_external` JSON-RPC capability. NestGate now owns the TLS boundary for the ecosystem — springs never open network connections. External data flows through primal composition only.

## Wire Format

### Request
```json
{
  "jsonrpc": "2.0",
  "method": "storage.fetch_external",
  "params": {
    "url": "https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id=CHEMBL4296",
    "cache_key": "chembl/oclacitinib_ic50_panel",
    "family_id": "wetspring",
    "timeout_secs": 120,
    "allow_insecure_http": false
  },
  "id": 1
}
```

### Response (cache miss — fresh fetch)
```json
{
  "result": {
    "value": { "...parsed JSON payload..." },
    "data": { "...same as value..." },
    "key": "chembl/oclacitinib_ic50_panel",
    "blake3": "a1b2c3d4e5f6...",
    "url": "https://www.ebi.ac.uk/chembl/api/data/activity.json?...",
    "size": 45231,
    "content_type": "application/json",
    "cached": false,
    "family_id": "wetspring"
  }
}
```

### Response (cache hit)
```json
{
  "result": {
    "value": { "...cached JSON payload..." },
    "data": { "...same..." },
    "key": "chembl/oclacitinib_ic50_panel",
    "blake3": "a1b2c3d4e5f6...",
    "cached": true,
    "family_id": "wetspring"
  }
}
```

## Capability Registration

- Listed in `capabilities.list` / `discover_capabilities`
- `backend.features.fetch_external: true` in discovery metadata
- Available on Unix socket server and isomorphic IPC transports

## Architecture

```
wetSpring → capability.call("storage", "fetch_external", { url, cache_key })
  → biomeOS routes to NestGate (domain="storage")
    → NestGate: check cache → fetch HTTPS → BLAKE3 hash → store → return
      → Provenance sidecar: { url, blake3, size, content_type, fetched_at }
```

### Security
- **HTTPS-only** by default — HTTP requires explicit `allow_insecure_http: true`
- URL scheme validation (rejects ftp://, file://, etc.)
- User-Agent: `NestGate/{version}`
- Configurable timeout (default 60s)
- Pure Rust TLS via `rustls` (no OpenSSL dependency)

### Caching
- Payload stored at: `{storage_base}/datasets/{family_id}/_external/{cache_key}`
- Metadata sidecar at: `{storage_base}/datasets/{family_id}/_external/{cache_key}.meta.json`
- Cache-first: returns immediately if both files exist
- BLAKE3 hash enables provenance chain verification

## Dependencies Added

| Crate | Version | Features | Purpose |
|-------|---------|----------|---------|
| `reqwest` | 0.12 | `rustls-tls`, `gzip`, `brotli` | HTTPS client (pure Rust TLS) |
| `blake3` | 1.5 | — | Content-addressing for provenance |

## Tests

8 unit tests covering:
- Parameter validation (url, cache_key required)
- URL scheme enforcement (ftp rejected, http rejected by default)
- HTTP opt-in with `allow_insecure_http`
- URL format validation
- Cache hit path (pre-populated cache returns without network)

## Impact on wetSpring

The Gonzales pipeline (Exp310 D02, Exp311 D05) should now produce data instead of gap reports when:
1. NestGate process is running
2. biomeOS has `storage` domain routed to NestGate
3. wetSpring calls `capability.call("storage", "fetch_external", { url, cache_key })`

### Data sources unblocked
- ChEMBL activity data
- PubChem compound data
- SRA sequence data
- Zenodo datasets
- EPA environmental data
- PDB structure data

## Files Changed

| File | Changes |
|------|---------|
| `Cargo.toml` | Added `reqwest`, `blake3` workspace deps |
| `nestgate-rpc/Cargo.toml` | Added `reqwest`, `blake3`, `url` deps |
| `storage_handlers.rs` | +295 lines: handler + helpers + 8 tests |
| `unix_socket_server/mod.rs` | Dispatch arm for `storage.fetch_external` |
| `model_cache_handlers.rs` | Added to method list + features |
| `unix_adapter_handlers.rs` | Added to capabilities list |
