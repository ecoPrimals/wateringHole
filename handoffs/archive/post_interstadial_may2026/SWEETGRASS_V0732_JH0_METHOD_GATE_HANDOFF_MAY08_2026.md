# sweetGrass v0.7.32 — JH-0 Method Gate Adoption

**Date**: May 8, 2026
**From**: sweetGrass team
**Resolves**: JH-0 adoption (primalSpring Phase 59 method gate wave)

---

## Summary

sweetGrass now implements the JH-0 pre-dispatch capability gate per
`wateringHole/METHOD_GATE_STANDARD.md`. This makes sweetGrass the 8th primal
to adopt JH-0 (joining BearDog, Songbird, ToadStool, Squirrel, rhizoCrypt,
loamSpine, coralReef, and primalSpring).

## Implementation

### Module: `method_gate.rs`

Adapted from primalSpring's `ipc/method_gate.rs` reference implementation.

**Types:**
- `MethodGate` — pre-dispatch authorization checker
- `EnforcementMode` — `Permissive` (default) or `Enforced`
- `CallerContext` — bearer token, peer credentials, connection origin
- `MethodAccessLevel` — `Public` or `Protected`

**Env var:** `SWEETGRASS_AUTH_MODE` (`permissive` | `enforced` | `enforce` | `strict`)

### Method Classification

**Public (always allowed):**
- `health.*` (prefix) — health probes
- `auth.*` (prefix) — gate introspection
- `identity.get` — Wire Standard L2
- `capabilities.list`, `capability.list` — self-knowledge
- `lifecycle.status` — lifecycle probes
- `tools.list` — MCP tool discovery

**Protected (require token when enforced):**
- `braid.*` — provenance record CRUD
- `anchoring.*` — LoamSpine anchoring
- `provenance.*` — W3C PROV-O export
- `attribution.*` — credit assignment
- `compression.*` — session compression
- `contribution.*` — contribution tracking
- `pipeline.*` — trio coordination
- `composition.*` — ecosystem health probes
- `tools.call` — MCP tool execution

### New Methods (3)

| Method | Response |
|--------|----------|
| `auth.mode` | `{ "mode": "permissive" \| "enforced" }` |
| `auth.check` | `{ "authenticated": false, "mode": "..." }` |
| `auth.peer_info` | `{ "origin": "Loopback" \| "Unix" \| "Remote", "peer": null \| { "uid": N, "pid": N } }` |

### Error Codes

| Code | Name | Usage |
|------|------|-------|
| `-32001` | `PERMISSION_DENIED` | Protected method called without token (enforced mode) |
| `-32000` | `UNAUTHORIZED` | Reserved for future identity verification |
| `-32004` | `NOT_FOUND` | Resource not found (braid, anchor, etc.) — migrated from `-32001` |

### Wiring

The gate is checked in `dispatch_classified()` before handler lookup. All
transports (HTTP, TCP, UDS, BTSP) pass through this single choke point.
`CallerContext::loopback()` is used as the default context; transport-layer
callers can evolve to pass real peer credentials later.

## Verification

- `auth.mode` responds with `{ "mode": "permissive" }` (default)
- `auth.check` responds with `{ "authenticated": false, "mode": "permissive" }`
- `auth.peer_info` responds with `{ "origin": "Loopback", "peer": null }`
- `health.check` passes through gate without token (public)
- `braid.create` passes through gate in permissive mode (logged warning)

## Metrics

- Tests: 1,522 pass, 0 failures (+21 method gate tests)
- Methods: 35 (32 domain + 3 auth)
- Clippy: 0 warnings (pedantic + nursery)
