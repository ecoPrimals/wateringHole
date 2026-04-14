<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 48: Transport Security Advertisement (TS-01) Handoff

**Date**: April 14, 2026
**Author**: bearDog team (automated)
**Trigger**: primalSpring benchScale audit — composition gap where biomeOS
forwards plaintext to BTSP-required sockets

---

## Problem

biomeOS's `capability.call` forwarding connects directly to BearDog's
family-scoped UDS socket and sends plaintext JSON-RPC. BearDog rejects the
connection (no BTSP handshake) with a **silent drop** — no error message. This
causes opaque "Failed to forward health.liveness" errors in biomeOS and all
composition experiments (exp001, exp060, exp061–068, exp095).

The root fix belongs in biomeOS (route through Tower Atomic) and primalSpring
(AtomicHarness needs FAMILY_ID + BTSP pre-auth). But BearDog can help by:
1. Advertising transport requirements so consumers know BTSP is needed
2. Sending actionable errors instead of silent drops

## Solution

### 1. `transport_security` in Capability Responses

Both `capabilities.list` and `discover_capabilities` now include:

```json
{
  "transport_security": {
    "btsp_required": true,
    "btsp_version": "2.0",
    "btsp_server_available": true,
    "cleartext_available": false,
    "note": "Family-scoped socket: BTSP handshake required before JSON-RPC."
  }
}
```

`btsp_required` is dynamically determined: `true` when `FAMILY_ID` is set to a
non-standalone/non-default value, `false` otherwise.

### 2. JSON-RPC Rejection on BTSP-Required Sockets

When a non-BTSP connection arrives on a family-scoped socket, the server now
sends a `-32600` error with guidance before closing:

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32600,
    "message": "BTSP handshake required",
    "data": {
      "reason": "This socket is family-scoped and requires a BTSP handshake...",
      "btsp_version": "2.0"
    }
  },
  "id": null
}
```

### 3. Wire Standard TS-01

New "Transport Security Advertisement" section in `CAPABILITY_WIRE_STANDARD.md`
documenting the field format and rejection behavior.

## Modified Files

| File | Change |
|------|--------|
| `crates/beardog-tunnel/src/unix_socket_ipc/handlers/capabilities.rs` | Added `transport_security` to both response types, `is_btsp_required()` helper |
| `crates/beardog-tunnel/src/unix_socket_ipc/server.rs` | BTSP rejection sends JSON-RPC error before drop |
| `CHANGELOG.md` | Wave 48 entry |
| `STATUS.md` | Wave 48 entry |

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt` | Clean |
| `cargo clippy --workspace -- -D warnings` | 0 warnings |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | Clean |
| `cargo test --workspace` | 14,784 passed, 0 failed |

## Upstream Impact

**biomeOS**: Can now check `transport_security.btsp_required` in capability
responses to determine routing strategy (Tower Atomic BTSP vs direct JSON-RPC).

**primalSpring**: AtomicHarness can read the `-32600` rejection to auto-detect
that BTSP wiring is needed.

**No breaking changes** — the `transport_security` field is additive.
