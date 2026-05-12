<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 83: Bond Persistence Default Upgraded to Capability Discovery

**Date**: May 4, 2026
**Primal**: BearDog (Tower — Security/Crypto)
**Wave**: 83
**Type**: Feature evolution (bond lifecycle)
**Audit**: Phase 58 primalSpring debt handoff

---

## Summary

Wave 83 upgrades the default bond persistence backend from ephemeral in-memory storage to runtime capability discovery. When a `bonding.ledger` provider (NestGate or loamSpine) is discovered via Songbird, sealed ionic bonds are automatically persisted via JSON-RPC. Falls back to in-memory when no provider is available — zero breakage for standalone or composition deployments.

## Phase 58 Audit Resolution

| Gap | Severity | Status | Notes |
|-----|----------|--------|-------|
| Phase 3 transport encryption | HIGH | **RESOLVED (Wave 81)** | `Phase3Session` + `try_phase3_upgrade` + `handle_jsonrpc_phase3` — full encrypted frame I/O after `btsp.negotiate` |
| `crypto.sign_contract` IPC | MEDIUM | **RESOLVED (pre-existing)** | Ed25519 contract signing in `IonicBondHandler` — `crypto.sign_contract` and `crypto.verify_contract` methods |
| `btsp.negotiate` vs `btsp.session.negotiate` | LOW | **INTENTIONAL** | `btsp.negotiate` = Phase 3 encrypted channel. `btsp.session.negotiate` = legacy alias for `btsp.server.negotiate` (session renegotiation). Different methods by design. |
| Bond persistence to NestGate/loamSpine | LOW | **RESOLVED (this wave)** | Default backend now `CapabilityDiscoveryBondPersistence` |

## Technical Change

### Before (Wave 82)
```rust
HandlerRegistry::new() → InMemoryBondPersistence (bonds lost on restart)
```

### After (Wave 83)
```rust
HandlerRegistry::new() → CapabilityDiscoveryBondPersistence
  ├─ discovers "bonding.ledger" via OrchestratorRegistryClient
  ├─ persists via JSON-RPC: bonding.ledger.store/retrieve/list/remove
  └─ falls back to InMemoryBondPersistence when no provider found
```

The `CapabilityDiscoveryBondPersistence` implementation:
- Caches discovered endpoints (lazy, first-call)
- Maintains in-memory fallback for every operation
- Writes to both remote and local on `store` (write-through)
- Merges remote + local on `list` (union)
- Logs warnings on remote failures without propagating errors
- 10-second timeout on ledger RPC calls

## Files Changed

| File | Change |
|------|--------|
| `crates/beardog-tunnel/src/unix_socket_ipc/handlers/mod.rs` | `new()` now creates `CapabilityDiscoveryBondPersistence` instead of `InMemoryBondPersistence` |

## Downstream Impact

- **NestGate/loamSpine teams**: If you expose `bonding.ledger.store`, `bonding.ledger.retrieve`, `bonding.ledger.list`, `bonding.ledger.remove` as JSON-RPC methods and register the `bonding.ledger` capability with Songbird, BearDog will auto-discover and use your service for durable bond storage.
- **primalSpring**: Phase 3 transport encryption was already fixed in Wave 81 — plasmidBin should auto-harvest the current binary. The `crypto.sign_contract` method is available for ionic bond seal phase.
- **No API changes** — same IPC surface, same wire format.

## CI Results

- **cargo fmt**: clean
- **cargo clippy --workspace**: 0 warnings
- **cargo test --workspace --lib**: 12,610 passed, 0 failed
