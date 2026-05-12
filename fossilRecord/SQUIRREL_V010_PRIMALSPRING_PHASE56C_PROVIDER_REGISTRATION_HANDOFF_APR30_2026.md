# Squirrel v0.1.0 — primalSpring Phase 56c: Provider Registration Protocol

**Date**: April 30, 2026
**Session**: AR
**Audit Source**: primalSpring v0.9.24 Phase 56c — Stadial Convergence
**Status**: RESOLVED

## Gap Addressed

**Squirrel** — Provider registration protocol: springs adding Squirrel to
compositions can't register as providers yet.

## Resolution

Implemented `provider.register`, `provider.list`, `provider.deregister` as
first-class JSON-RPC methods and tarpc binary RPC methods.

### Wire Format (`provider.register`)

```json
{
  "jsonrpc": "2.0",
  "method": "provider.register",
  "params": {
    "provider_id": "neuralspring-01",
    "socket": "/run/user/1000/biomeos/neuralspring-desktop-nucleus.sock",
    "capabilities": ["neural.validate", "neural.simulate"],
    "version": "0.9.24",
    "domain": "neural"
  },
  "id": 1
}
```

Optional: `endpoint` (HTTP URL), `priority` (0–255), `metadata` (JSON object).

### Key Design Decisions

- **Deterministic UUIDs**: Service IDs are derived from `provider_id` via hashing,
  giving upsert semantics. Re-registering the same provider overwrites rather than
  duplicates.
- **Validation**: `provider_id` required (1–256 chars), `capabilities` must be
  non-empty, at least one of `socket` or `endpoint` must be provided.
- **Uses existing `InMemoryServiceRegistry`**: No new infrastructure — leverages
  the `UniversalServiceRegistry` trait and `InMemoryServiceRegistry` that already
  existed but was not wired to any RPC handler.
- **Wire Standard L3**: Methods appear in `capabilities.list`, `cost_estimates`,
  `operation_dependencies`, and `semantic_mappings` from day one.

### Files Changed

| File | Change |
|------|--------|
| `crates/main/src/rpc/handlers_provider.rs` | **NEW** — handlers + 7 tests |
| `crates/main/src/rpc/mod.rs` | Module declaration |
| `crates/main/src/rpc/jsonrpc_dispatch.rs` | Dispatch entries |
| `crates/main/src/rpc/jsonrpc_server.rs` | `provider_registry` field |
| `crates/main/src/rpc/tarpc_service.rs` | Types + trait methods |
| `crates/main/src/rpc/tarpc_server.rs` | Implementation |
| `crates/main/src/niche.rs` | Costs, deps, semantic mappings, group descriptions |
| `crates/universal-constants/src/capabilities.rs` | 3 new entries |
| `capability_registry.toml` | Full schema entries |

### Metrics

- **Tests**: 7,189 passing (was 7,182)
- **Exposed capabilities**: 34 (was 31)
- **Quality gates**: `fmt` ✓, `clippy 0 warnings` ✓, `test` ✓, `deny` ✓

## Impact on Springs

Springs wishing to register as providers with Squirrel at composition startup
should call `provider.register` over their UDS connection to Squirrel, passing
their `provider_id`, socket/endpoint, and capability list. Squirrel will route
future capability-based requests to them.

This complements `inference.register_provider` (AI-specific) with a
general-purpose registration mechanism for any capability domain.
