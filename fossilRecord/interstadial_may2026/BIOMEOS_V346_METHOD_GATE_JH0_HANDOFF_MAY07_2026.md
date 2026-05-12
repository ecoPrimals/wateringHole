# biomeOS v3.46 — MethodGate Pre-Dispatch Authorization (JH-0)

**Date**: May 7, 2026
**Audit Item**: JH-0 (ALL primals — ecosystem-standard pre-dispatch capability gate)
**Status**: RESOLVED for biomeOS
**primalSpring Reference**: v0.9.25 `wateringHole/METHOD_GATE_STANDARD.md`

---

## What Changed

biomeOS now implements the ecosystem-standard `MethodGate` pre-dispatch
authorization pattern, matching the reference implementation in
`primalSpring/ecoPrimal/src/ipc/method_gate.rs`.

### New Module: `biomeos-core::method_gate`

- `MethodGate` — pre-dispatch check, `Permissive` (default) or `Enforced`.
- `CallerContext` — bearer token, `PeerCredentials` (pid/uid), `ConnectionOrigin`.
- `classify_method()` — Public/Protected classification.
- `EnforcementMode` — reads `BIOMEOS_AUTH_MODE` env var.
- Error codes: `-32001 PERMISSION_DENIED`, `-32000 UNAUTHORIZED`.
- 26 unit tests.

### Public Methods (always allowed without token)

| Method | Purpose |
|--------|---------|
| `health.*` | Liveness and readiness probes |
| `identity.get` | Primal self-identification |
| `capabilities.list` | Capability advertisement |
| `capability.list` | Alias for above |
| `lifecycle.status` | Running/stopped status |
| `auth.check` | Is the caller authenticated? |
| `auth.mode` | Current enforcement mode |
| `auth.peer_info` | Peer credential introspection |

Everything else is **Protected**.

### Wiring in Neural API Server

- `NeuralApiServer` gains a `method_gate: MethodGate` field.
- `handle_request()` in `routing.rs` calls `method_gate.check()` after
  request parsing, before the route dispatch table.
- Bearer tokens extracted from `_bearer_token` field in request params.
- Three new `auth.*` routes registered in `ROUTE_TABLE` and dispatched
  directly by the gate (no handler delegation needed).

### Error Code Constructors in `biomeos-types`

- `JsonRpcError::permission_denied(method)` → code `-32001`.
- `JsonRpcError::unauthorized(reason)` → code `-32000`.

---

## Enforcement Modes

| Mode | Behavior | Env Var |
|------|----------|---------|
| `Permissive` | Log violations but allow (default) | `BIOMEOS_AUTH_MODE=permissive` or unset |
| `Enforced` | Reject with `-32001` | `BIOMEOS_AUTH_MODE=enforced` |

---

## Remaining JH Items for biomeOS

| Item | Severity | Status | Description |
|------|----------|--------|-------------|
| JH-0 | Critical | **RESOLVED** | MethodGate wired, permissive default |
| JH-2 | High | Open | Resource envelope enforcement (needs BearDog JH-1 ionic tokens) |
| JH-3 | Medium | Open | `composition.reload` hot-reload for per-primal swap |

---

## Test Results

- 7,897 tests (0 failures, fully concurrent).
- `cargo clippy --all-targets`: 0 warnings.
- `cargo fmt --check`: clean.
