# biomeOS — Neural API Capability Registration Gap

**Date**: March 31, 2026
**Priority**: P2 — HIGH
**Reporter**: ludoSpring V37.1 + primalSpring Phase 23f investigation
**Cross-reference**: primalSpring `docs/PRIMAL_GAPS.md` BM-04, BM-05
**SPRING_EVOLUTION_ISSUES**: ISSUE-014

---

## Problem

Running primals (barraCuda, BearDog, NestGate, sweetGrass, etc.) are alive on UDS
sockets but the Neural API `capability.list` only shows 5 capabilities:

```
primal.germination, primal.terraria, ecosystem.nucleation,
graph.execution, ecosystem.coordination
```

These are `BIOMEOS_SELF_CAPABILITIES` — biomeOS's own capabilities registered in
`register_self_in_registry()` at startup. No external primal capabilities appear.

Missing domains: `math`, `tensor`, `compute`, `noise`, `stats`, `activation`, `dag`,
`visualization`, `crypto`, `security`, `storage`

## Root Cause

`discover_and_register_primals()` in `server_lifecycle.rs` runs **once** at startup.
It scans `$XDG_RUNTIME_DIR/biomeos/*.sock`, sends `capabilities.list` with **500ms
timeout**, and registers responses in `NeuralRouter.capability_registry`.

**Problem 1 (timing)**: In normal graph startup order, biomeOS starts first, then
primals start after. By the time primals are listening, discovery has already completed.

**Problem 2 (response format)**: `probe_primal_capabilities` expects a specific JSON
shape from `capabilities.list`. Primals returning different formats get empty results
and are silently skipped.

**Problem 3 (no retry)**: There is no periodic re-discovery. If a primal starts late,
it stays invisible to `capability.call` unless it explicitly calls `capability.register`.

## Impact

- **14 checks fail** across ludoSpring exp084, exp087, exp088
- `capability.call` cannot route to ANY primal by domain
- `graph.execute_pipeline` and `graph.start_continuous` cannot resolve graph node capabilities

## Fix Options (in order of complexity)

### Quick: Add `topology.rescan` method
Add a JSON-RPC method that re-runs `discover_and_register_primals()`. Scripts and
composition launchers call it after all primals are started.

```bash
echo '{"jsonrpc":"2.0","method":"topology.rescan","id":1}' | socat - UNIX-CONNECT:/run/user/1000/biomeos/neural-api.sock
```

### Medium: Lazy discovery on miss
In `discover_capability()`, when a category lookup fails and the registry has no
matching entries, re-run `discover_and_register_primals()` once, then retry.

### Full: Primal self-registration
Primals call `capability.register` on startup (requires `biomeos-primal-sdk` to
include registration as part of the startup sequence). This is the design intent
per the `primal_coordinator.rs` comment:
```
// Capability sharing happens via the Neural API when primals register
// with `lifecycle.register` + `capability.register`.
```

## Relevant Code

| File | Role |
|------|------|
| `biomeos-atomic-deploy/src/neural_api_server/server_lifecycle.rs` | `discover_and_register_primals()` + `probe_primal_capabilities()` |
| `biomeos-atomic-deploy/src/neural_router/mod.rs` | `register_capability()`, `list_capabilities()` |
| `biomeos-atomic-deploy/src/neural_router/discovery.rs` | `discover_capability()`, `discover_by_capability_category()` |
| `biomeos-atomic-deploy/src/bootstrap.rs` | `register_self_in_registry()` (the 5 self-capabilities) |
| `biomeos-types/src/primal_names.rs` | `BIOMEOS_SELF_CAPABILITIES` constant |

## Workaround (primalSpring)

primalSpring's thin gateway bypasses `capability.call` and resolves sockets directly
via `capability.discover` + socket directory scanning. This works but isn't the
intended capability routing path.
