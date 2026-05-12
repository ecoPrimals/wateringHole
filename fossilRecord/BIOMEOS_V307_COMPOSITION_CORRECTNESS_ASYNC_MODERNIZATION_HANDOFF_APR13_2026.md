# biomeOS v3.07 — Composition Correctness & Async Modernization

**Date**: April 13, 2026
**From**: biomeOS primal team
**To**: primalSpring, downstream springs
**License**: AGPL-3.0-or-later

---

## Summary

biomeOS v3.07 addresses the remaining primalSpring audit gaps:
1. **`graph.execute` cross-gate validation** — silent local fallback eliminated
2. **Songbird mesh state probing** — `composition.health` now queries real mesh state
3. **`async-trait` modernization** — first RPITIT migration + dependency cleanup

## Changes

### 1. graph.execute cross-gate validation (BUG FIX)

`neural_executor.rs`: When a graph node has `gate` set but the gate is not in the
registry, execution now **fails with an explicit error** instead of silently falling
through to local execution. This matches `capability.call` behavior (v3.05).

- `gate = "local"` → explicit local execution (falls through to local handlers)
- `gate = "<registered_name>"` → forwards to remote Neural API
- `gate = "<unknown>"` → **error** with known gates listed

Prevents incorrect compositions where gate2/Pixel nodes silently execute on the
wrong biomeOS instance.

### 2. Songbird mesh state probing (ENRICHMENT)

`lifecycle.rs`: `composition.health` mesh subsystem now probes Songbird's
`mesh.status` via IPC when Songbird is active, returning:

```json
{
  "status": "ok",
  "detail": "mesh_probed",
  "peer_count": 3,
  "mesh_state": { ... }
}
```

Falls back gracefully to `{"status": "ok", "detail": "process_alive_mesh_unprobed"}`
when `mesh.status` is unavailable. The mesh response is now a structured object
instead of a flat string.

### 3. async-trait modernization

- `PrimalOperationExecutor` trait in `biomeos-graph` migrated from `#[async_trait]`
  to native RPITIT (`impl Future<Output = ...> + Send`). Zero-cost async.
- `async-trait` removed from `biomeos-types` Cargo.toml (was unused)
- `async-trait` moved to `[dev-dependencies]` in `biomeos-api` (test-only usage)
- Remaining 71 `#[async_trait]` usages blocked by `dyn Trait` dispatch;
  migration requires converting to enum dispatch (cross-cutting architectural work)

## Quality Gates

| Gate | Result |
|------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --workspace --all-targets -- -D warnings` | PASS (0 warnings) |
| `cargo test --workspace` | **7,784 tests**, 0 failures |
| Production `.unwrap()` | 0 |
| Production `unsafe` | 0 |
| Files >1000 LOC | 0 (all <835) |
| `#[allow(` in production | 0 |

## primalSpring Audit Status

From the primalSpring PRIMAL_GAPS.md biomeOS section:

| Audit Item | Status |
|-----------|--------|
| BM-01 through BM-11 | **ALL RESOLVED** (v2.79–v3.05) |
| `graph.execute` gate fallback | **RESOLVED** (v3.07) |
| Songbird mesh state | **RESOLVED** (v3.07) |
| `async-trait` modernization | **PARTIAL** (1/72 migrated, 2 crates optimized) |
| Docker UDS topology | **ACKNOWLEDGED** — deployment constraint, not code bug |
| gate2/Pixel deploy validation | **RESOLVED** (v3.07 — executor enforces gate registration) |

## Files Changed

| File | Change |
|------|--------|
| `biomeos-atomic-deploy/src/neural_executor.rs` | Gate validation: error on unregistered gate |
| `biomeos-atomic-deploy/src/handlers/lifecycle.rs` | Mesh state probing via Songbird IPC |
| `biomeos-atomic-deploy/src/handlers/lifecycle_tests.rs` | Test assertions updated for structured mesh response |
| `biomeos-graph/src/executor/trait.rs` | RPITIT migration (native async fn) |
| `biomeos-graph/src/executor/tests.rs` | Removed `#[async_trait]` from mock impl |
| `biomeos-types/Cargo.toml` | Removed unused `async-trait` dependency |
| `biomeos-api/Cargo.toml` | Moved `async-trait` to dev-dependencies |
| `CHANGELOG.md` | v3.07 entry |
| `README.md`, `CURRENT_STATUS.md`, etc. | Version bumps |

---

*Fossil record: `ecoPrimals/infra/wateringHole/handoffs/`*
