<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 Wave 93 — JH-0 MethodGate Pre-Dispatch Authorization

**Date**: May 8, 2026
**Scope**: JH-0 adoption from `primalSpring/wateringHole/METHOD_GATE_STANDARD.md`
**Status**: Complete — 2,163 tests pass, clippy clean, fmt clean

---

## Summary

BearDog now runs every incoming JSON-RPC call through a `MethodGate` pre-dispatch
authorization layer before reaching `HandlerRegistry::route()`. Methods are classified
as `Public` (always allowed) or `Protected` (require a capability token when enforcement
is active). Default mode is `Permissive` (logs violations but allows all), switchable
to `Enforced` via `BEARDOG_AUTH_MODE=enforced`.

Three new auth introspection methods (`auth.check`, `auth.mode`, `auth.peer_info`) are
handled inline at the dispatch layer, not through the `HandlerRegistry`, because they
need access to `CallerContext` and `MethodGate` state.

---

## Files Created

| File | LOC | Purpose |
|------|-----|---------|
| `crates/beardog-tunnel/src/method_gate.rs` | ~300 | `MethodGate`, `CallerContext`, `classify_method`, auth handlers, 26 tests |

## Files Modified

| File | Change |
|------|--------|
| `crates/beardog-ipc/src/protocol.rs` | Added `UNAUTHORIZED`, `PERMISSION_DENIED`, `NOT_READY` error codes |
| `crates/beardog-tunnel/src/lib.rs` | Added `pub mod method_gate;`, `#![recursion_limit = "256"]` |
| `crates/beardog-tunnel/src/unix_socket_ipc/types.rs` | Added error constants + `permission_denied()`, `unauthorized()` constructors |
| `crates/beardog-tunnel/src/unix_socket_ipc/server.rs` | `MethodGate` field, `CallerContext` parameter threading, auth intercept, gate check |
| `crates/beardog-tunnel/src/unix_socket_ipc/connection_handlers.rs` | `CallerContext::from_unix()` at connection entry, passed through all 5 call sites |
| `crates/beardog-tunnel/src/tcp_ipc/server.rs` | `Arc<MethodGate>` field, loopback/remote detection, auth intercept + gate in both NDJSON and BTSP paths |
| `crates/beardog-tunnel/src/unix_socket_ipc/handlers/capabilities.rs` | `auth.*` in `provided_capabilities`, `discover_capabilities`, cleartext methods, cost estimates |
| `docs/PRIMAL_CONTRACTS.md` | Auth introspection section, method count 111→114 |
| `STATUS.md` | Wave 93 entry, method count updated |
| `CHANGELOG.md` | Wave 93 entry |

## Error Codes Added

| Code | Name | When |
|------|------|------|
| -32000 | `UNAUTHORIZED` | Caller identity not established |
| -32001 | `PERMISSION_DENIED` | Protected method, no token, enforced mode |
| -32002 | `NOT_READY` | Primal still initializing (reserved) |

## Public Method Whitelist

Methods always allowed regardless of enforcement mode:

- `health.*` (prefix match)
- `identity.get`
- `capabilities.list`, `capability.list`
- `lifecycle.status`
- `auth.check`, `auth.mode`, `auth.peer_info`

## What This Does NOT Include (deferred to JH-1)

- `identity.create` — create a new primal identity keypair
- `auth.issue_ionic` — issue a capability/ionic token
- `auth.verify_ionic` — verify a capability token
- Real token verification logic (currently `bearer_token.is_some()` suffices)
- `SO_PEERCRED` extraction (blocked on Rust API stabilization)

## Test Coverage

- **26 new tests** in `method_gate::tests` — classification, gate enforcement, auth handlers, dispatch routing
- **2,163 total** beardog-tunnel lib tests pass
- **4 TCP server tests** updated for new `handle_connection` signature
- **7 capabilities tests** pass (including updated minimum count)

## Verification

```bash
cargo fmt --all -- --check       # Clean
cargo clippy -p beardog-tunnel -p beardog-ipc -- -D warnings  # Clean
cargo test -p beardog-tunnel --lib  # 2,163 pass, 0 fail
```

---

## Action Items for primalSpring

1. Mark JH-0 as resolved for BearDog in `PRIMAL_GAPS.md`
2. Verify `METHOD_GATE_STANDARD.md` public whitelist matches BearDog's implementation
3. Plan JH-1 wave (ionic token issuance/verification)
