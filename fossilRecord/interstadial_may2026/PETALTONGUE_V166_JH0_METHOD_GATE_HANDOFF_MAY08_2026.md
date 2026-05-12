<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# petalTongue v1.6.6 — JH-0 MethodGate Pre-Dispatch Authorization

**Date**: May 8, 2026
**Scope**: JH-0 adoption from ecosystem `METHOD_GATE_STANDARD`
**Status**: Complete — 200 tests pass, 8 e2e pass, clippy clean, fmt clean

---

## Summary

petalTongue now runs every incoming JSON-RPC call through a `MethodGate`
pre-dispatch authorization layer before reaching the handler dispatch table.
Methods are classified as `Public` (always allowed) or `Protected` (require a
capability token when enforcement is active). Default mode is `Permissive`
(logs violations but allows all), switchable to `Enforced` via
`PETALTONGUE_AUTH_MODE=enforced`.

Three new auth introspection methods (`auth.check`, `auth.mode`,
`auth.peer_info`) are intercepted inline at the dispatch layer before the
handler match table.

---

## Files Created

| File | LOC | Purpose |
|------|-----|---------|
| `crates/petal-tongue-ipc/src/method_gate.rs` | 494 | `MethodGate`, `CallerContext`, `classify_method`, auth handlers, 26 tests |

## Files Modified

| File | Change |
|------|--------|
| `crates/petal-tongue-ipc/src/lib.rs` | Added `pub mod method_gate;` + re-exports |
| `crates/petal-tongue-ipc/src/json_rpc.rs` | Added `UNAUTHORIZED (-32000)`, `PERMISSION_DENIED (-32001)` error codes |
| `crates/petal-tongue-ipc/src/unix_socket_rpc_handlers/mod.rs` | `method_gate: MethodGate` field on `RpcHandlers` |
| `crates/petal-tongue-ipc/src/unix_socket_rpc_handlers/dispatch.rs` | `handle_request` accepts `&CallerContext`, auth intercept + gate check |
| `crates/petal-tongue-ipc/src/unix_socket_connection.rs` | `handle_connection` + `handle_connection_split` accept `&CallerContext` |
| `crates/petal-tongue-ipc/src/btsp/phase3.rs` | `handle_encrypted_stream` + `try_phase3_negotiate` accept `&CallerContext` |
| `crates/petal-tongue-ipc/src/unix_socket_server.rs` | `CallerContext` threading through UDS/TCP/BTSP paths, `peer_addr` on TCP |
| `crates/petal-tongue-ipc/src/unix_socket_rpc_handlers/system/capabilities.rs` | `auth.check`, `auth.mode`, `auth.peer_info` in methods list |
| `crates/petal-tongue-ipc/src/unix_socket_rpc_handlers/tests.rs` | All 32 dispatch tests updated for `CallerContext` |
| `crates/petal-tongue-ipc/tests/pipeline_tests.rs` | All pipeline tests updated for `CallerContext` |
| `CHANGELOG.md` | JH-0 entry |
| `CONTEXT.md` | MethodGate description |
| `START_HERE.md` | `PETALTONGUE_AUTH_MODE` env var documented |

## Error Codes Added

| Code | Name | When |
|------|------|------|
| -32000 | `UNAUTHORIZED` | Caller identity not established |
| -32001 | `PERMISSION_DENIED` | Protected method, no token, enforced mode |

## Public Method Whitelist

Methods always allowed regardless of enforcement mode:

- `health.*` (prefix match), `health`, `ping`, `status`, `check`
- `identity.get`
- `capabilities.list`, `capability.list`, `primal.capabilities`
- `lifecycle.status`
- `auth.check`, `auth.mode`, `auth.peer_info`

## CallerContext

Connection origin tracked per-connection:
- **Unix** — local UDS (trusted)
- **Loopback** — TCP 127.0.0.1/::1
- **Remote** — TCP from non-loopback address

Bearer tokens extracted from `_bearer_token` field in request params per-request.

## What This Does NOT Include (deferred to JH-1+)

- `identity.create` — create a new primal identity keypair
- `auth.issue_ionic` — issue a capability/ionic token
- `auth.verify_ionic` — verify a capability token
- Real token verification logic (currently `bearer_token.is_some()` suffices)
- `SO_PEERCRED` extraction (blocked on Rust API stabilization)

## Test Coverage

- **26 new tests** in `method_gate::tests` — classification, gate enforcement, auth handlers, CallerContext construction
- **200 total** lib + integration tests pass (all updated for `CallerContext`)
- **8 e2e** tests pass

## Verification

```bash
cargo fmt --check                    # Clean
cargo clippy --all-targets --all-features -- -D warnings  # Clean
cargo test --all-features            # 200 pass + 8 e2e
cargo doc --no-deps                  # Clean
```

---

## Action Items for primalSpring

1. Mark JH-0 as RESOLVED for petalTongue in `PRIMAL_GAPS.md`
2. petalTongue is now 8/13 on JH-0 adoption wave
3. Plan JH-1 wave (ionic token issuance/verification from BearDog)
