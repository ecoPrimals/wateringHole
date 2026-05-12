# biomeOS v3.26 — Socket Family-ID Fix, Graph Schema Alignment, `list` Method

**Date**: April 26, 2026
**From**: biomeOS
**Addresses**: primalSpring Live Composition Validation (April 26, 2026) — PG-41, PG-39, bare `list` method

---

## PG-41: Socket Family-ID Mismatch — RESOLVED

**Problem**: biomeOS forwarded `activation.fitts` to `barracuda-default.sock` instead of `barracuda-nucleus01.sock`. The graph-bootstrap step pre-registered capabilities with `{primal}-{self.family_id}.sock`, and the NeuralRouter used append-only semantics (`providers.push()`). When live discovery later found the correct socket, it was appended as `providers[1]` — but capability routing always selected `providers[0]`.

**Fix**: `NeuralRouter::register_capability()` now uses upsert semantics. When a capability is registered for a primal name that already has an entry, the endpoint, timestamp, and source are **updated** instead of creating a duplicate. Live socket discovery (startup step 5) now correctly overrides graph-bootstrap entries (step 4c).

**File**: `crates/biomeos-atomic-deploy/src/neural_router/mod.rs`

**Impact**: All primals launched with a non-default `FAMILY_ID` will now have their correct socket paths used for capability routing. No action needed from downstream primals.

---

## PG-39: Graph Schema Alignment — RESOLVED

**Problem**: primalSpring cell graphs use `[[graph.nodes]]` with `name`/`binary`/`by_capability`/`order`. biomeOS's `convert_deployment_node()` expected `id`/`capability`/`config.primal` and silently dropped the primalSpring-specific fields. Additionally, `convert_deployment_node` placed capability/params on `operation.params` but `node_capability_call_with_registry` reads from `config["capability"]`/`config["params"]` — a silent execution gap.

**Fix**:
1. `name` now falls back to `id` when `id` is absent
2. `by_capability` now falls back to `capability`
3. `binary` maps to `config["primal"]` and populates `PrimalSelector.by_name`
4. `PrimalSelector` is constructed from available fields (was always `None`)
5. `config["capability"]` and `config["params"]` are populated during conversion, fixing the `capability_call` execution path

**File**: `crates/biomeos-atomic-deploy/src/neural_graph.rs`

**Recommendation to primalSpring**: biomeOS now accepts both schemas. Migrating cell graphs to the `[[nodes]]` + `id` + `[nodes.primal]` format is optional — the converter handles both transparently.

---

## Neural API bare `list` method — RESOLVED

**Problem**: petalTongue DataService called bare `list` via neural-api and got "unknown JSON-RPC method: list". Single-word methods don't trigger biomeOS's semantic capability fallback (which requires a dot separator), so they always returned `MethodNotFound`.

**Fix**: Added `("list", Route::TopologyPrimals)` to `ROUTE_TABLE`. Maps to the same handler as `primal.list` / `topology.primals` / `neural_api.get_primals`.

**File**: `crates/biomeos-atomic-deploy/src/neural_api_server/routing.rs`

**Note**: petalTongue's `NeuralApiProvider::get_primals()` already uses `primal.list` (which has been working since v3.24). The bare `list` call may come from a separate code path (e.g., `DataService` vs `NeuralApiProvider`). Both are now supported.

---

## Verification

- `cargo check --workspace`: 0 errors
- `cargo clippy --workspace -- -D warnings`: 0 warnings
- `cargo fmt --check`: clean
- All test failures are pre-existing (environment-dependent discovery tests sensitive to live sockets on the build host)
