# sweetGrass v0.7.27 — NestGate Store, Composition Health, Deploy Graph Evolution

**Date**: April 12, 2026
**Primal**: sweetGrass v0.7.27
**Trigger**: wetSpring validation and ecosystem alignment

---

## Summary

Ecosystem evolution sprint informed by wetSpring pattern analysis. Three
deliverables: (1) NestGate JSON-RPC store backend as Postgres evolution path,
(2) composition health handlers per COMPOSITION_HEALTH_STANDARD, (3) canonical
deploy graph migration to `[[graph.nodes]]` schema.

---

## 1. NestGate Store Backend (`sweet-grass-store-nestgate`)

### Problem
sweetGrass had Postgres as its only networked storage backend. Ecosystem
direction is NestGate for delegated persistence, redb for embedded.

### Solution
New crate `sweet-grass-store-nestgate` implementing `BraidStore` via
NestGate `storage.*` JSON-RPC over UDS:

- **Methods**: `storage.store`, `storage.retrieve`, `storage.delete`,
  `storage.list`, `storage.exists` (aliases `storage.put`/`storage.get`)
- **Key schema**: `{prefix}:braid:{id}`, `{prefix}:activity:{id}`,
  `{prefix}:idx:agent:{did}`, `{prefix}:idx:derived:{hash}`
- **Socket discovery**: `NESTGATE_SOCKET` → `STORAGE_PROVIDER_SOCKET` →
  `{BIOMEOS_SOCKET_DIR}/nestgate.sock` → XDG → `/tmp/biomeos/nestgate.sock`
- **Family ID**: scoped via `FAMILY_ID` env or family-scoped sockets
- **Query**: client-side filtering with NestGate prefix listing
- **Feature-gated**: `STORAGE_BACKEND=nestgate` + `--features nestgate`

### Architecture
```
sweetGrass ──JSON-RPC over UDS──▶ NestGate (filesystem/ZFS)
    │                                  │
    ├─ storage.store (put braid)      ├─ key-value JSON storage
    ├─ storage.retrieve (get braid)   ├─ family-scoped namespaces
    ├─ storage.list (query indices)   └─ BLAKE3 content addressing
    └─ storage.exists (check)
```

### Backend Landscape After This Sprint

| Backend | Type | Status | Use Case |
|---------|------|--------|----------|
| redb | Embedded (pure Rust) | **Primary** | Standalone / development |
| NestGate | Delegated (JSON-RPC) | **New** | Composed deployments |
| Postgres | External (sqlx) | **Legacy** | Relational/ops workloads |
| sled | Embedded (deprecated) | Feature-gated | Backward compat |
| Memory | In-process | Testing | Unit tests / benchmarks |

---

## 2. Composition Health Handlers

Per `wateringHole/COMPOSITION_HEALTH_STANDARD.md` v1.0.0:

| Method | Subsystems Probed |
|--------|-------------------|
| `composition.tower_health` | security, discovery |
| `composition.node_health` | security, discovery, compute |
| `composition.nest_health` | security, discovery, storage |
| `composition.nucleus_health` | security, discovery, compute, storage, provenance, ledger, attribution (self) |

Each handler:
- Discovers capability sockets via `{BIOMEOS_SOCKET_DIR}/{domain}.sock`
- Sends `health.liveness` with 3-second timeout
- Returns `{ healthy, deploy_graph, subsystems: { domain: ok|degraded|unavailable } }`

---

## 3. Deploy Graph Schema Migration

Migrated `graphs/sweetgrass_deploy.toml` from flat `[graph]` + `[[dependencies]]`
to canonical `[[graph.nodes]]` schema with:
- `[graph.metadata]`: domain, wire_standard, btsp_phase, binary, subcommand
- `[graph.bonding_policy]`: security, discovery, storage requirements
- `[[graph.nodes]]`: capabilities_provided (32), capabilities_consumed (8),
  per-node dependency declarations
- `[scheduling]` + `[environment]` preserved

---

## Gap Analysis: wetSpring Validation Results

| Pattern | sweetGrass Before | After |
|---------|------------------|-------|
| Wire L2/L3 (identity.get, consumed_capabilities) | HAS | HAS |
| Composition health RPCs | MISSING | **DONE** |
| Deploy graph `[[graph.nodes]]` | OUTDATED | **DONE** |
| NestGate store backend | MISSING | **DONE** |
| WireWitnessRef type name | Aligned vocabulary | Low priority |
| upstream_contract guards | MISSING | Deferred |

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 1,416 | 1,427 |
| .rs files | 168 | 174 |
| LOC | 48,719 | 49,837 |
| Crates | 10 | 11 |
| Capabilities | 28 | 32 |
| Store backends | 4 | 5 |
| Clippy | 0 warnings | 0 warnings |
| `cargo deny` | All clear | All clear |

---

## Ecosystem Impact

### For Trio Partners
- NestGate store pattern is reusable for rhizoCrypt/loamSpine delegated storage
- Composition health pattern is ecosystem-standard (copy for adoption)

### For Composition
- sweetGrass now participates in all composition tiers (tower through nucleus)
- Deploy graph is parseable by biomeOS deploy-graph tooling (canonical schema)
- NestGate backend enables true Nest Atomic deployments

### Remaining Known Gaps

| Gap | Priority | Notes |
|-----|----------|-------|
| Postgres CI coverage | Low | Needs Docker in CI; error paths covered |
| upstream_contract guards | Low | wetSpring pattern; consider for critical deps |
| NestGate backend integration tests | Medium | Needs running NestGate; unit tests cover logic |
| BTSP Phase 3 | Deferred | Ecosystem-wide |
| async-trait for 6 dyn traits | Deferred | Needs trait_variant |
