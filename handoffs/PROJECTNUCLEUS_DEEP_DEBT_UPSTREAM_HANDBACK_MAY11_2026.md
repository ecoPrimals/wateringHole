# projectNUCLEUS: Deep Debt Upstream Handback (May 11, 2026)

**Date**: 2026-05-11
**From**: projectNUCLEUS (sporeGarden)
**For**: toadStool team, squirrel team, barraCuda team
**Priority**: Low (all items are localhost-only mitigations, no external exposure)

---

## Context

projectNUCLEUS's deep debt evolution sweep identified three upstream items
that can only be resolved by the owning primal teams. These are not blocking
any projectNUCLEUS work — they are evolution targets for the primal stack.

---

## 1. MethodGate for toadStool

### Problem

toadStool dispatches JSON-RPC requests without a pre-dispatch auth gate.
All methods are callable without authentication or capability verification.
projectNUCLEUS corrected its MethodGate claim from 13/13 to 11/13 (toadStool
+ squirrel are the missing two).

### Risk

Low: toadStool binds `127.0.0.1` and is protected by UFW deny-by-default.
However, any local user (including JupyterHub notebook users) can call any
toadStool method. When Tier 4 IPC-first rewiring lands, toadStool will
receive cross-primal calls that should be scope-checked.

### Recommended Pattern (from bearDog exemplar)

**bearDog implementation**: `beardog-tunnel/src/method_gate.rs`

```
parse request → MethodGate::check(method, caller) → handle_method dispatch
```

Key components:
- `MethodAccessLevel` enum: `Public` (health, status) vs `Protected` (everything else)
- `CallerContext`: bearer token, connection origin (Unix/Loopback/Remote)
- `MethodGate::check()`: public → Ok, protected → verify ionic token or reject
- `EnforcementMode`: `BEARDOG_AUTH_MODE` env var controls permissive/enforced

### Insertion Point in toadStool

**File**: `crates/server/src/pure_jsonrpc/handler/mod.rs`
**Function**: `JsonRpcHandler::handle_request`

Insert gate check after JSON-RPC envelope validation, before `handle_method`:

```rust
// After validating jsonrpc version and id, before handle_method:
let caller = CallerContext::from_connection(&conn_info);
self.method_gate.check(&request.method, &caller)?;
// Then proceed to handle_method dispatch
```

**Secondary path**: `crates/cli/src/daemon/jsonrpc_server.rs` has a separate
`daemon.*` JSON-RPC stack. Gate this path only if biomeOS/clients call it.

### Public Methods (no gate needed)

```
health.liveness, health.readiness, composition.status
```

### Environment Variable

`TOADSTOOL_AUTH_MODE=enforced|permissive` (default: `permissive` for backwards compatibility)

---

## 2. MethodGate for squirrel

### Problem

Same as toadStool — squirrel dispatches JSON-RPC without a pre-dispatch gate.

### Insertion Point in squirrel

**File**: `crates/main/src/rpc/jsonrpc_request_processing.rs`
**Function**: `handle_single_request_object`

Insert gate check after extracting `method_str` and `params`, before
`dispatch_jsonrpc_method`:

```rust
// After extracting method_str, before dispatch:
let caller = CallerContext::from_connection(&conn_info);
self.method_gate.check(method_str, &caller)?;
// Then proceed to dispatch_jsonrpc_method
```

**Method table**: `crates/main/src/rpc/jsonrpc_server.rs` — `dispatch_jsonrpc_method`
is the big match block (`ai.query`, `health.check`, `tool.execute`, etc.)

### Public Methods (no gate needed)

```
health.check, health.liveness, composition.status
```

### Environment Variable

`SQUIRREL_AUTH_MODE=enforced|permissive`

---

## 3. squirrel `LocalProcessProvider` → toadStool IPC

### Problem

`ComputeBackend::Local(LocalProcessProvider)` in squirrel is a dev stub.
`execute_workload` always returns an error with guidance text. `get_capabilities`
returns synthetic values (8 GB, num_cpus cores).

**File**: `crates/main/src/compute_client/provider_trait.rs` (~lines 336-408)

### Evolution Target

Replace `LocalProcessProvider` with an IPC-first dispatch to toadStool:

```rust
// Instead of error stub:
pub async fn execute_workload(&self, workload: Workload) -> Result<WorkloadResult> {
    // Route to toadStool via capability discovery
    let toadstool = composition_context.resolve("compute.dispatch")?;
    toadstool.call("workload.execute", &workload).await
}
```

This aligns with the Tier 4 IPC-first rewiring target. When `barracuda` is
optional and IPC is the default dispatch, squirrel should route compute
through toadStool rather than stubbing it.

### Priority

Low — squirrel currently uses this only as a fallback when no compute
backend is configured. The stub is honest (returns error + guidance).

---

## 4. barraCuda Crypto Delegation to bearDog IPC

### Problem

`barracuda-core` embeds its own crypto crates for BTSP:

**File**: `Cargo.toml` (workspace `[workspace.dependencies]`) and
`crates/barracuda-core/Cargo.toml`

Embedded crates:
- `chacha20poly1305` 0.10
- `hkdf` 0.12
- `hmac` 0.12
- `sha2` 0.10
- `base64ct` 1.6

### Evolution Target

These crypto operations could be delegated to bearDog via IPC (Tower Atomic
pattern). bearDog already provides:
- `crypto.sign` — ed25519 signatures
- `crypto.hash` — BLAKE3 content hashing

When barraCuda's BTSP crypto calls route through bearDog IPC:
1. The embedded crypto crates can be dropped from `barracuda-core`
2. Key material stays in bearDog (single source of truth)
3. HSM gating (H2-10) applies automatically via bearDog

### IPC Pattern

```rust
// Instead of direct chacha20poly1305:
let encrypted = beardog_rpc("crypto.encrypt", &CryptoRequest {
    algorithm: "chacha20-poly1305",
    key_id: "btsp-session",
    plaintext: data,
}).await?;
```

### Priority

Medium — this is a Tier 4 rewiring target. The embedded crates are not
a security risk (they're well-audited RustCrypto crates), but centralizing
crypto in bearDog reduces attack surface and enables HSM gating.

### Caveat

barraCuda's GPU compute paths may need low-latency crypto that IPC overhead
makes impractical. In that case, keep the embedded crates for hot paths and
delegate only key management and signing to bearDog.

---

## Summary

| Team | Item | File | Priority |
|------|------|------|----------|
| toadStool | MethodGate pre-dispatch | `crates/server/src/pure_jsonrpc/handler/mod.rs` | Low |
| squirrel | MethodGate pre-dispatch | `crates/main/src/rpc/jsonrpc_request_processing.rs` | Low |
| squirrel | `LocalProcessProvider` → toadStool IPC | `crates/main/src/compute_client/provider_trait.rs` | Low |
| barraCuda | Crypto delegation to bearDog IPC | `crates/barracuda-core/Cargo.toml` | Medium |

None of these are blocking projectNUCLEUS. All primals bind `127.0.0.1`,
UFW deny-by-default is active, and MethodGate is enforced on the other 11
primals. These items improve the primal stack's sovereignty posture for
when Tier 4 IPC-first rewiring opens up cross-primal trust boundaries.

---

## References

- bearDog MethodGate exemplar: `beardog-tunnel/src/method_gate.rs`
- bearDog MethodGate tests: `beardog-tunnel/src/method_gate_tests.rs`
- projectNUCLEUS cross-ecosystem audit: `infra/wateringHole/handoffs/PROJECTNUCLEUS_CROSS_ECOSYSTEM_AUDIT_MAY11_2026.md`
- projectNUCLEUS EVOLUTION_GAPS.md: canonical absorption target tracker
- COMPLETE_DEPENDENCY_INVENTORY.md Cluster 7: JH-0 status (11/13 enforced)
