<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- ScyBorg Provenance: crafted by human intent, assisted by AI -->

# LoamSpine V0.9.2 — Structured IPC & Ecosystem Absorption Handoff

**Primal**: LoamSpine  
**Version**: 0.9.2  
**Date**: March 16, 2026  
**Phase**: Deep IPC Evolution + Cross-Spring Absorption

---

## Summary

Following the V0.9.2 deep debt resolution session, this handoff covers the ecosystem absorption phase: structured IPC errors, tarpc alignment, generic primal discovery, and the `#[allow]` → `#[expect]` migration.

---

## Changes Made

### 1. Structured IPC Errors (rhizoCrypt Alignment)

**Pattern absorbed from**: rhizoCrypt `IpcErrorPhase`, healthSpring `SendError`

Added `IpcPhase` enum to `loam-spine-core::error`:

```
IpcPhase::Connect | Write | Read | InvalidJson | HttpStatus(u16) | NoResult | JsonRpcError(i64) | Serialization
```

New `LoamSpineError::Ipc { phase: IpcPhase, message: String }` variant replaces all unstructured `Network(format!(...))` in transport and discovery code.

**Files migrated**:
- `crates/loam-spine-core/src/error.rs` — new types + `ipc()` helper + `is_recoverable()` method
- `crates/loam-spine-core/src/transport/mod.rs` — `TransportResponse::json()` uses `IpcPhase::InvalidJson`
- `crates/loam-spine-core/src/transport/http.rs` — all ureq errors → `IpcPhase::Connect`/`IpcPhase::Read`
- `crates/loam-spine-core/src/transport/neural_api.rs` — full phase coverage (Connect, Write, Read, InvalidJson, NoResult, JsonRpcError, Serialization)
- `crates/loam-spine-core/src/discovery_client/mod.rs` — discovery, advertise, heartbeat, deregister
- `crates/loam-spine-api/src/error.rs` — `Ipc` maps to `ApiError::Transport` with phase context

**`is_recoverable()` semantics**:
- Recoverable: Connect, Write, Read, HttpStatus(5xx), CapabilityUnavailable, Network
- Not recoverable: InvalidJson, NoResult, JsonRpcError, HttpStatus(4xx), Serialization

### 2. tarpc 0.34 → 0.35

Bumped in `crates/loam-spine-api/Cargo.toml`. No API breakage.

### 3. Generic Primal Discovery Helpers (sweetGrass Pattern)

Added to `crates/loam-spine-core/src/constants/network.rs`:
- `socket_env_var(primal)` → `"{PRIMAL}_SOCKET"` (e.g., `"RHIZOCRYPT_SOCKET"`)
- `address_env_var(primal)` → `"{PRIMAL}_ADDRESS"`
- `resolve_primal_socket_with_env(primal, family_id)` → checks env override, falls back to standard biomeos socket dir

### 4. `#[allow]` → `#[expect(reason)]` Migration

16 `#[allow(clippy::...)]` annotations in test modules migrated to `#[expect(clippy::..., reason = "...")]` with verified lint trigger. Remaining ~25 annotations stayed as `#[allow]` because their lints are not always triggered (would cause unfulfilled-expectation errors).

### 5. `IpcPhase` Re-exported

`loam_spine_core` now re-exports `IpcPhase` alongside `LoamSpineError` and `LoamSpineResult`.

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 1,180 | 1,190 |
| Coverage (function) | 85.25% | 91.01% |
| Coverage (line) | 91.72% | 88.84% |
| Clippy warnings | 0 | 0 |
| Doc warnings | 0 | 0 |
| Unsafe in production | 0 | 0 |
| `#[expect]` annotations | 0 | 16 |
| tarpc version | 0.34 | 0.35 |
| Source files | 121 | 121 |

---

## Ecosystem Alignment

| Pattern | Source | LoamSpine Status |
|---------|--------|------------------|
| `IpcErrorPhase` typed errors | rhizoCrypt | ABSORBED as `IpcPhase` |
| `SendError` variants | healthSpring | ABSORBED (same phase structure) |
| `socket_env_var()` / `address_env_var()` | sweetGrass V0.7.17 | ABSORBED |
| `provenance-trio-types` v0.1.1 | ecosystem | Already aligned (path dep) |
| `capabilities` key in `capability.list` | neuralSpring S156 | Already emitting |
| tarpc 0.35 | ecosystem drift | ABSORBED |
| `#[expect(reason)]` over `#[allow]` | ecosystem standard | 16 migrated, remaining kept as `#[allow]` |

---

## What Remains for V0.9.3

1. **Storage backend error-path coverage** — redb/sled/sqlite error branches need additional fault-injection tests
2. **PostgreSQL/RocksDB backends** — optional feature-gated implementations
3. **Remaining `#[allow]` → `#[expect]`** — need clippy changes or test restructuring to trigger lints
4. **Line coverage lift** — 88.84% → 90%+ line target (function coverage already at 91%)
5. **Cross-primal e2e tests** — rhizoCrypt ↔ loamSpine ↔ sweetGrass trio integration
