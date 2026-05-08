# biomeOS v3.43 — Discovery Schema Alignment

**Date**: May 5, 2026
**Version**: 3.43
**From**: biomeOS
**Status**: PRODUCTION READY — 7,867 tests (0 failures), clippy PASS, fmt PASS

---

## Changes

### capability.discover response schema alignment

`biomeos-core`'s `SocketDiscovery` client was parsing a stale response schema
from `capability.discover`. The live Neural API handler returns:

```json
{
  "primary_endpoint": "/run/user/1000/biomeos/beardog.sock",
  "primals": [{"name": "beardog", "endpoint": "...", "healthy": true}]
}
```

But `registry_queries.rs` expected the old format:

```json
{
  "primary_socket": "/path/to.sock",
  "provider": "beardog"
}
```

This meant any primal using `discover_via_registry_by_capability()` against the
live Neural API would silently fail (return `None`).

**Fix**: `registry_queries.rs` now reads:
- `primary_endpoint` first, falling back to `primary_socket` (backward compat)
- `primals[0].name` first, falling back to `provider` (backward compat)
- Endpoint strings parsed via `TransportEndpoint::parse()` for full transport
  support (Unix socket paths, TCP addresses, HTTP URLs)

1 new test: `discover_via_registry_by_capability_live_format`

### primalSpring Phase 59 audit — status

- **biomeOS rated LOW** — v3.42 evolution clean
- **Discovery Escalation Hierarchy**: biomeOS Neural API is tier 2
  (`capability.discover`); `ipc.resolve` already wired as alias for
  `capability.resolve` (tier 1 compatible)
- **Cross-gate dispatch**: functional via `GateRegistry` + `capability.call`
  with `gate` param; not yet exercised in live ironGate composition
- **Provenance trio**: all `dag.*`, `commit.*`/`spine.*`, `braid.*` capabilities
  fully registered in `capability_registry.toml`

---

## Codebase Health

| Metric | Value |
|--------|-------|
| Tests | 7,867 (0 failures, fully concurrent) |
| Files >800 LOC | 0 (largest: 798) |
| Unsafe | 0 |
| TODO/FIXME | 0 |
| Production mocks | 0 |
| Hardcoded primal names/env vars | 0 |
| External C deps | 0 |
| Clippy | PASS (pedantic+nursery, -D warnings) |
| Format | PASS |
