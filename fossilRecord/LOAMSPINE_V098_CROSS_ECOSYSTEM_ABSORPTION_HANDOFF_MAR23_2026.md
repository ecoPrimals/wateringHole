<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# LoamSpine v0.9.8 — Cross-Ecosystem Absorption Handoff

**Date:** March 23, 2026
**From:** loamSpine v0.9.8
**To:** primalSpring, biomeOS, rhizoCrypt, sweetGrass, all springs
**License:** AGPL-3.0-or-later

---

## Executive Summary

LoamSpine v0.9.8 absorbs patterns from 9 ecoSprings, 5 phase1 primals,
4 phase2 primals, and root-level ecosystem primals. All changes are
backward-compatible — no wire format or API changes. Ecosystem partners
need **zero changes** for compatibility.

---

## What Changed

### Ecosystem Pattern Absorption

| Pattern | Source | What LoamSpine Absorbed |
|---------|--------|------------------------|
| `normalize_method()` | barraCuda v0.3.7 | Centralized backward-compat alias resolution before dispatch. Legacy `permanent-storage.*`, `commit.session`, `primal.capabilities` etc. now normalized in a single function rather than duplicated match arms. |
| `IpcErrorPhase` | primalSpring, rhizoCrypt, biomeOS | Renamed `IpcPhase` → `IpcErrorPhase` with `pub type IpcPhase = IpcErrorPhase` alias for backward compat. Aligns with ecosystem vocabulary. |
| `extract_rpc_result` | neuralSpring S168b, healthSpring V33 | New utility to extract typed results from JSON-RPC responses. Companion to existing `extract_rpc_error`. Includes `extract_rpc_result_typed<T>` for deserialize-in-one-step. |
| Cast lint deny | airSpring, neuralSpring, groundSpring | `cast_possible_truncation`, `cast_sign_loss`, `cast_precision_loss`, `cast_possible_wrap` = deny at workspace level. Zero violations found (codebase was already clean). |
| Structured IPC in SyncEngine | ecosystem `IpcErrorPhase` pattern | SyncEngine's `rpc_call` evolved from flat `Network` errors to structured `IpcErrorPhase` errors (Connect, Write, Read, InvalidJson, JsonRpcError). Now uses `extract_rpc_result` for response handling. Phase-aware retry and observability. |

### Proptest Expansion

- **9 new proptests** for Entry and Spine core types
  - Entry hash determinism, index sensitivity, genesis invariants
  - Spine height monotonicity, sealed spine rejection, name preservation
- Total proptests: now covers `error`, `types`, `entry`, `spine` modules

### Metrics

| Metric | v0.9.7 | v0.9.8 |
|--------|--------|--------|
| Tests | 1,232 | 1,247 |
| Clippy | pedantic+nursery clean | + cast deny clean |
| Cast lints | warn | deny (0 violations) |
| `IpcPhase` name | internal only | `IpcErrorPhase` (ecosystem-aligned) |
| SyncEngine errors | flat `Network` | structured `IpcErrorPhase` |

---

## Provenance Trio Blocker — RESOLVED

The primalSpring PROVENANCE_TRIO_HANDOFF_MAR22_2026 identifies a blocker:
`phase2/provenance-trio-types/` does not exist on disk.

**This blocker is resolved for all three trio primals:**

| Primal | Resolution | When |
|--------|------------|------|
| **loamSpine** | Types inlined in `trio_types.rs` | v0.9.5+ |
| **rhizoCrypt** | Types inlined in `dehydration_wire.rs` | v0.13.0-dev (Mar 2026) |
| **sweetGrass** | Types inlined, `provenance-trio-types` banned in `deny.toml` | v0.7.22 (Mar 2026) |

JSON remains the contract. No shared compile-time crate needed.

**Remaining integration step:** Binary placement. Each team needs to:
1. Build release binary
2. Copy to `plasmidBin/primals/{primalname}`
3. Verify Unix socket JSON-RPC works

### loamSpine Required Methods (all implemented)

All methods listed in the primalSpring handoff are implemented:
- `health.liveness` ✓
- `capability.list` / `capabilities.list` ✓ (via `normalize_method`)
- `spine.create`, `spine.get`, `spine.seal` ✓
- `entry.append`, `entry.get` ✓
- `certificate.mint`, `certificate.transfer` ✓
- `session.commit` / `commit.session` ✓ (via `normalize_method`)

---

## What Partners Should Know

### No Breaking Changes

- `IpcPhase` type alias preserved for backward compat
- All JSON-RPC methods still work (normalization is transparent)
- Wire format unchanged

### New Public API

```rust
// Extract typed result from JSON-RPC response
use loam_spine_core::extract_rpc_result;
use loam_spine_core::extract_rpc_result_typed;
use loam_spine_core::IpcErrorPhase; // canonical name
use loam_spine_core::IpcPhase;      // backward-compat alias

// In loam-spine-api
use loam_spine_api::jsonrpc::normalize_method;
```

### For Springs Using LoamSpine IPC

The `extract_rpc_result` / `extract_rpc_result_typed` utilities are
available for any spring making outbound JSON-RPC calls to LoamSpine.
They handle error extraction, NoResult detection, and typed
deserialization in a single call.

---

## Ecosystem Patterns NOT Yet Absorbed (Tracked for Future)

| Pattern | Source | Status |
|---------|--------|--------|
| MCP `tools/list` + `tools/call` | airSpring v0.10 | Tracked — needed for Squirrel visibility |
| Circuit breaker in SyncEngine | primalSpring, healthSpring | Tracked — `ResilientAdapter` exists in discovery_client |
| `ValidationHarness` / `ValidationSink` | rhizoCrypt, springs | Tracked — useful if validation binaries are added |

---

**License**: AGPL-3.0-or-later
