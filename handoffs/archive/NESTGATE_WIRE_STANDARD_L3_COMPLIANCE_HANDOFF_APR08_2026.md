# NestGate Wire Standard L3 Compliance — Handoff

**Date:** April 8, 2026
**Primal:** NestGate
**Session:** 37
**Resolves:** GAP-MATRIX-04 (Wire Standard catch-up sprint)

---

## Summary

NestGate is now fully compliant with Capability Wire Standard Level 3 (Composable).
Previously, NestGate had a working JSON-RPC/UDS handler (Session 35) but lacked the
structured envelope format and capability grouping required by the Wire Standard.

## Changes

### identity.get — Wire Standard L2

- Added `domain: "storage"` (SHOULD per spec)
- Added `license: "AGPL-3.0-or-later"` (MAY per spec)
- Existing fields preserved: `primal`, `version`, `family_id`

### capabilities.list — Wire Standard L3

- Response now returns full envelope: `{primal, version, methods, provided_capabilities, consumed_capabilities, protocol, transport}`
- `provided_capabilities`: 9 groups — storage, model, templates, session, audit, nat, beacon, data, zfs
- `consumed_capabilities`: `[]` (NestGate is a leaf primal — no cross-primal dependencies)
- `protocol`: `"jsonrpc-2.0"`
- `transport`: `["uds", "http"]`

### UNIX_SOCKET_SUPPORTED_METHODS — Method Advertisement

Expanded from 37 → 57 methods. Previously unadvertised but callable methods now listed:
- `identity.get`
- `session.save`, `session.load`
- `data.ncbi_search`, `data.ncbi_fetch`, `data.noaa_ghcnd`, `data.iris_stations`, `data.iris_events`
- `discovery.capability.register`

Wire Standard rule: "The methods array MUST contain every method the primal will accept."

### Test Coverage

- 3 new tests: Wire Standard L2 envelope validation, L3 composable validation, protocol+transport
- 410 existing nestgate-rpc tests still passing

## Files Changed

| File | Change |
|------|--------|
| `nestgate-rpc/src/rpc/model_cache_handlers.rs` | `capabilities.list` L3 envelope, expanded methods array, 3 new tests |
| `nestgate-rpc/src/rpc/unix_socket_server/mod.rs` | `identity.get` domain + license fields |
| `nestgate-observe/src/observability/metrics.rs` | Fix pre-existing clippy (`u64::MAX` comparison) |
| `README.md` | JSON-RPC compliance note updated to L3 |
| `STATUS.md` | Wire Standard level + 57 advertised methods |
| `CHANGELOG.md` | Session 37 entry |
| `wateringHole/CAPABILITY_WIRE_STANDARD.md` | NestGate added to compliance table |

## Compliance Level

| Level | Status | Details |
|-------|--------|---------|
| L1 (Routable) | ✓ | `capabilities.list` responds, `health.liveness` alive |
| L2 (Standard) | ✓ | `{primal, version, methods}` envelope, `identity.get` with domain, all 57 methods callable |
| L3 (Composable) | ✓ | `provided_capabilities` (9 groups), `consumed_capabilities` declared, `protocol` + `transport` |

## Verification

```bash
echo '{"jsonrpc":"2.0","method":"capabilities.list","id":1}' | nc -U /run/user/1000/biomeos/storage.sock
echo '{"jsonrpc":"2.0","method":"identity.get","id":2}' | nc -U /run/user/1000/biomeos/storage.sock
cd code && cargo test -p nestgate-rpc -- wire_standard
```
