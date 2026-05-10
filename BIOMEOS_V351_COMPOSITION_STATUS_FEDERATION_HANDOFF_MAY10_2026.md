# biomeOS v3.51 — Composition Status + Method Registration + Token Federation

**Date**: May 10, 2026
**Commit**: `26e8e90d`
**Tests**: 7,934 pass / 0 fail / 113 ignored
**Audit source**: primalSpring interstadial + sovereignty goals (May 9, 2026)

---

## Changes

### 1. `composition.status` Method (HIGH — pappusCast)

New JSON-RPC method for projectNUCLEUS adaptive daemons (pappusCast):

```json
{
  "active_users": 11,
  "primal_health": [
    { "name": "bearDog", "state": "active", "latency_ms": 2, "failures": 0, "resurrection_count": 0 },
    { "name": "toadStool", "state": "degraded", "latency_ms": 45, "failures": 3, "resurrection_count": 1 }
  ],
  "resource_pressure": {
    "cpu": 0.42,
    "memory": 0.67,
    "disk": 0.31
  },
  "total_primals": 13,
  "topology_version": 7
}
```

- `active_users` — count of primals in Active state (proxy for load)
- `primal_health` — per-primal state, latency, failure count, resurrection count
- `resource_pressure` — host CPU/memory/disk from `/proc` via `biomeos-system`
- `topology_version` — monotonic counter from `LifecycleHandler`

Route: `composition.status` → `LifecycleHandler::composition_status()`

### 2. `method.register` Endpoint (GAP-09 — Spring Method Registration)

New JSON-RPC method for springs to register their IPC methods into the
semantic routing layer:

```json
// Request
{
  "method": "method.register",
  "params": {
    "primal": "ludoSpring",
    "transport": "/run/user/1000/biomeos/ludoSpring.sock",
    "methods": ["game.start", "game.join", "game.end", "score.get", "score.leaderboard"]
  }
}

// Response
{
  "registered": 5,
  "domains": ["game", "score"],
  "primal": "ludoSpring",
  "endpoint": "/run/user/1000/biomeos/ludoSpring.sock"
}
```

Domain prefixes are extracted from method names. Each domain is registered
as a capability, and each method as a semantic mapping. After registration,
`game.start` routes via the semantic fallback → `capability.call`.

### 3. `composition.deploy` Route Alias (GAP-03)

`composition.deploy` is now a registered route alias for `graph.execute`,
matching the primalSpring contract name. Both names dispatch to the same
`GraphHandler::execute()` handler.

### 4. BearDogVerifier — Cross-Primal Token Federation (JH-11)

New `BearDogVerifier` in `biomeos-core::method_gate`:

- Calls `auth.verify_ionic` on BearDog via IPC to cryptographically verify
  bearer tokens before forwarding to downstream primals
- Falls back to `LocalClaimsVerifier` (parse-only) when BearDog is unreachable
- Socket resolved from `BEARDOG_SOCKET` env or XDG defaults
- Integrated into `NeuralApiServer`; created automatically via `from_env()`

Forwarding paths (`CapabilityCall`, semantic fallback, `SemanticCapabilityCall`)
now inject `_token_verified: true|false` alongside `_bearer_token`, so
downstream primals know whether biomeOS verified the token.

**What this IS**: Step 1 of federation — verify-then-forward. Downstream
primals receive a verified token with attestation from the composition layer.

**What this is NOT**: Full offline verification (requires BearDog to ship
shared-key distribution so primals can verify without IPC callbacks).

### Files Changed

| File | Change |
|------|--------|
| `crates/biomeos-core/src/method_gate.rs` | +`BearDogVerifier` struct, `verify_async()`, `from_env()`, 5 tests |
| `crates/biomeos-core/src/lib.rs` | Re-export `BearDogVerifier` |
| `crates/biomeos-atomic-deploy/Cargo.toml` | +`biomeos-system` dependency |
| `crates/biomeos-atomic-deploy/src/handlers/lifecycle.rs` | +`composition_status()` method |
| `crates/biomeos-atomic-deploy/src/handlers/capability.rs` | +`register_methods()` method |
| `crates/biomeos-atomic-deploy/src/neural_api_server/mod.rs` | +`beardog_verifier` field |
| `crates/biomeos-atomic-deploy/src/neural_api_server/routing.rs` | +3 routes, async `enrich_for_forwarding`, `_token_verified` |
| `crates/biomeos-atomic-deploy/src/neural_api_server/routing_tests.rs` | +5 tests |

---

## Remaining JH-11 Roadmap

| Step | Status | Owner |
|------|--------|-------|
| `_bearer_token` forwarding through composition | DONE (v3.50) | biomeOS |
| `BearDogVerifier` IPC verification | DONE (v3.51) | biomeOS |
| `_token_verified` attestation field | DONE (v3.51) | biomeOS |
| Shared-key distribution for offline verification | PENDING | BearDog |
| Token introspection endpoint | PENDING | BearDog |

## primalSpring Experiment Status

| Experiment | Status |
|-----------|--------|
| exp109 (`composition.reload` contract) | RESOLVED (v3.50) |
| exp111 (`gate_routing` forwarding) | RESOLVED (v3.50 + v3.51) |
| exp108 (`token_federation`) | PARTIAL — verify-then-forward works; offline verification blocked on BearDog |
