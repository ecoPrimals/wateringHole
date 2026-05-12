# NestGate v4.7.0-dev Session 59 Handoff — JH-0 MethodGate

**Date**: May 8, 2026
**Session**: 59
**Trigger**: primalSpring v0.9.25 JH-0 audit — every primal must adopt the MethodGate pre-dispatch authorization pattern

---

## Summary

Session 59 implements the ecosystem-standard MethodGate pre-dispatch
authorization gate (JH-0, per `wateringHole/METHOD_GATE_STANDARD.md`) in
NestGate. The gate classifies every incoming JSON-RPC method as Public or
Protected before it reaches the dispatch table. Starts in permissive mode
(backward-compatible); `NESTGATE_AUTH_MODE=enforced` activates rejection.

---

## Implementation

### New module: `nestgate-rpc/src/rpc/method_gate.rs`

- `MethodAccessLevel` — `Public` / `Protected` enum.
- `classify_method()` — Public whitelist: `health.*`, `auth.*`,
  `identity.get`, `capabilities.list`, `capability.list`,
  `discover_capabilities`, `discover.capabilities`,
  `discovery.capability.register`, `lifecycle.status`.
  Everything else is Protected.
- `CallerContext` — bearer token + connection origin (`Unix`).
- `EnforcementMode` — `Permissive` (default) / `Enforced`, resolved from
  `NESTGATE_AUTH_MODE` env var.
- `MethodGate` — `check(method, caller)` returns `Ok(())` or
  `MethodGateRejection` with code `-32001` (`PERMISSION_DENIED`).
- `auth_introspection()` — handles `auth.check`, `auth.mode`,
  `auth.peer_info` directly (these methods need gate context).

### Dispatch wiring

Gate check runs at the top of `dispatch::handle_request()` after JSON-RPC
2.0 validation and before the method dispatch table:

1. Auth introspection intercept — `auth.*` methods return directly.
2. Gate check — Protected + no token + enforced = `-32001`.
3. Otherwise proceed to dispatch table.

Composes with the existing BTSP transport-level gate: BTSP-rejected calls
never reach MethodGate.

### Differences from primalSpring reference implementation

- Uses `NESTGATE_AUTH_MODE` (not `PRIMALSPRING_AUTH_MODE`).
- Public whitelist includes NestGate's legacy discovery aliases
  (`discover_capabilities`, `discover.capabilities`,
  `discovery.capability.register`).
- Self-contained in `nestgate-rpc` — no cross-crate imports from
  primalSpring.
- `ConnectionOrigin::Loopback` deferred (TCP gate wiring incremental).
- `-32000 UNAUTHORIZED` constant deferred until BearDog ships
  `auth.verify_ionic` (token verification is presence-only for now).

### Capabilities

- `auth.check`, `auth.mode`, `auth.peer_info` registered in
  `UNIX_SOCKET_SUPPORTED_METHODS` (66 total, up from 63).
- `auth` capability group added to L3 `provided_capabilities` envelope
  and `capability_registry.toml`.

---

## False positives from the audit

Two "open items" carried forward in the primalSpring audit were already
resolved:

1. **`storage.retrieve` for large/streaming tensors** — RESOLVED
   (Session 43p). `storage.store_stream`, `storage.store_stream_chunk`,
   `storage.retrieve_stream`, `storage.retrieve_stream_chunk`,
   `storage.object.size` are implemented and registered.

2. **Cross-spring persistent storage IPC** — RESOLVED (Session 55+).
   `family_id` parameter on all storage calls enables cross-family
   scoping. Namespace isolation is complete.

---

## Verification

| Check | Result |
|-------|--------|
| `cargo check --workspace` | PASS |
| `cargo clippy --workspace -- -D warnings` | PASS (zero warnings) |
| `cargo fmt --all --check` | PASS |
| `cargo test --workspace --lib` | 8,915 passed, 0 failed, 60 ignored |

---

## What remains deferred

- **Peer credentials** (`SO_PEERCRED`) — API unstable,
  `#![forbid(unsafe_code)]`.
- **Token verification** — deferred until BearDog ships
  `auth.verify_ionic`; gate currently checks token presence only.
- **TCP/HTTP gate wiring** — UDS is primary; other surfaces incremental.
- **Enforced mode activation** — requires downstream coordination (all
  springs must send tokens before flipping the switch).
