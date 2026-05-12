<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 99: Token Federation, Bonding Aliases & Scope Compat

**Date**: May 9, 2026
**Primal**: bearDog v0.9.0
**Audit Source**: primalSpring Later-Term Evolution — Upstream Primal Capability Targets (May 2026)
**Registry**: 123 methods (118 concrete + 5 bonding aliases)
**Tests**: 14,889+ passing, 0 failures
**Quality Gates**: `cargo fmt`, `cargo clippy -D warnings`, `RUSTDOCFLAGS="-D warnings" cargo doc`, `cargo test --workspace` — all clean

---

## Resolved Audit Items

### 1. JH-11: Token Key Distribution — `auth.public_key`

**Audit**: "primals need a way to verify BearDog-issued ionic tokens without calling back to the issuing BearDog. Ship either a shared-key distribution mechanism or a token-introspection endpoint."

**Resolution**: New `auth.public_key` JSON-RPC method (gate-handled, public, cleartext-allowed).

**Request**: `{ "jsonrpc": "2.0", "method": "auth.public_key", "id": 1 }`

**Response**:
```json
{
  "public_key": "<base64 Ed25519 verifying key>",
  "public_key_hex": "<hex Ed25519 verifying key>",
  "did": "did:key:z6Mk...",
  "algorithm": "Ed25519",
  "usage": "Verify ionic tokens signed by this primal..."
}
```

**Cross-primal workflow**:
1. Remote primal calls `auth.public_key` once at startup → caches key
2. On each inbound request with bearer token, uses cached `VerifyingKey` for local Ed25519 verification
3. No further calls to BearDog needed for token validation

**primalSpring validation**: exp108 (`exp108_token_federation`) can now complete — call `auth.public_key`, cache key, issue/attach/verify/reject-wrong-scope cycle runs locally.

### 2. `bonding.propose` Runtime Signing

**Audit**: "primalSpring guidestone Layer 5 now attempts a live ionic bond via `bonding.propose`. Currently skips with 'method not found.'"

**Resolution**: Five bonding aliases wired in `HandlerRegistry::route()`:

| Alias | Routes to |
|-------|-----------|
| `bonding.propose` | `crypto.ionic_bond.propose` |
| `bonding.accept` | `crypto.ionic_bond.accept` |
| `bonding.status` | `crypto.ionic_bond.list` |
| `bonding.terminate` | `crypto.ionic_bond.revoke` |
| `bonding.modify_scope` | `crypto.ionic_bond.seal` |

These match the primalSpring `capability_registry.toml` and graph node capabilities. `bonding.propose` triggers the full Ed25519-signed bond proposal flow (hash terms → sign with primal identity → return `bond_id`).

**primalSpring validation**: Guidestone Layer 5 `bonding.propose` call will now resolve to `crypto.ionic_bond.propose` and execute bond proposal with runtime Ed25519 signing.

### 3. Scope Pattern in `auth.issue_ionic` Response

**Audit**: "Ensure `auth.issue_ionic` returns `scopes` as an array of these patterns so the verifier can enforce them."

**Resolution**: All three token response paths now return both field names:
- `"scope"`: original field (array of `*`, `domain.*`, exact patterns)
- `"scopes"`: alias field (same array, same content)

Affected methods: `auth.issue_ionic`, `auth.issue_session`, `auth.verify_ionic` (in `claims`).

**primalSpring validation**: `scope_permits_method()` can read either `scope` or `scopes` from the response and get the array of patterns.

---

## Remaining BearDog Debt

| ID | Item | Status | Notes |
|----|------|--------|-------|
| BD-IONIC-PERSIST | Ionic bond durable persistence | Open | In-memory only; needs NestGate/ledger delegation |
| HSM-P3 | HSM signing path | Open (low) | Comments reference HSM; mocks correctly `#[cfg(test)]`-gated (Wave 98) |

---

## Files Modified

- `crates/beardog-tunnel/src/ionic_token_handlers.rs` — `handle_auth_public_key`, `scopes` alias in responses
- `crates/beardog-tunnel/src/method_gate.rs` — `auth.public_key` in gate dispatch, public methods, `is_gate_handled_method`
- `crates/beardog-tunnel/src/method_gate_tests.rs` — 3 updated tests + 1 new dispatch test
- `crates/beardog-tunnel/src/unix_socket_ipc/handlers/mod.rs` — 5 bonding aliases in `route()`
- `crates/beardog-tunnel/src/unix_socket_ipc/handlers/capabilities.rs` — auth v3.0, `auth.public_key` cost/cleartext, bonding aliases in discovery
- `STATUS.md`, `CHANGELOG.md` — updated metrics and wave entry
