# biomeOS v3.24 — primal.list, Graph Executor Fix, Bootstrap Tolerance

**Date**: April 22, 2026
**From**: biomeOS v3.24
**Scope**: primalSpring downstream audit resolution — Neural API protocol gaps + graph bootstrapping

---

## What Changed

### 1. `primal.list` Method (Neural API + API Socket)

**Gap addressed**: primalSpring audit identified `primal.list` as unimplemented, causing
petalTongue fatal startup failure (patched locally by petalTongue to tolerate absence).

**Fix**:
- Neural API `ROUTE_TABLE`: added `("primal.list", Route::TopologyPrimals)` — aliases
  to same `TopologyHandler::get_primals()` as `topology.primals` / `neural_api.get_primals`
- `biomeos-api/unix_server.rs`: added `primal.list` + `topology.primals` dispatch arms
  with self-report response (`{"primals":[{"name":"biomeos","role":"orchestrator","status":"alive"}],"count":1}`)
- `capabilities.list` now includes `primal.list` in its advertised methods

**Tests**: 4 new (`test_dispatch_jsonrpc_line_primal_list`, `test_dispatch_jsonrpc_line_topology_primals_alias`,
`test_dispatch_jsonrpc_line_capabilities_list_includes_primal_list`,
`test_handle_request_primal_list_routes_to_topology_primals`)

### 2. Graph Executor `rpc_call` Operation Fallback

**Gap addressed**: `init_sovereign_onion` graph node fails with
"rpc_call requires 'target' config (primal name)" because graph TOMLs define
`target`/`method`/`params` in `[nodes.operation]` and `[nodes.operation.params]`,
but `node_rpc_call` only reads from `node.config` (a separate HashMap).

**Root cause**: The `Operation` struct lacked a `target` field, so
`target = "songbird"` in `[nodes.operation]` was silently dropped by serde.
`node_rpc_call` then failed on the first guard.

**Fix**:
- Added `target: Option<String>` to `Operation` struct (with `Default` derive)
- `node_rpc_call` now falls back to `operation.target`, `operation.params["method"]`,
  and `operation.params["params"]` when `node.config` is empty
- Backward compatible: `node.config` is checked first

### 3. Bootstrap Tolerance

**Gap addressed**: `init_sovereign_onion` calls Songbird's `onion.start` which requires
Tor. On hosts without Tor, this fails and rolls back the entire bootstrap graph.

**Fix**: Added `fallback = "skip"` to `init_sovereign_onion` and `init_beacon_mesh`
nodes in all 4 graph TOMLs:
- `graphs/tower_atomic_bootstrap.toml`
- `graphs/nucleus_complete.toml`
- `pixel8a-deploy/graphs/tower_atomic_bootstrap.toml`
- `livespore-usb/x86_64/graphs/tower_atomic_bootstrap.toml`

The graph executor's existing `is_optional()` mechanism marks skipped nodes as
`Completed({"skipped": true})`, allowing dependent nodes to proceed.

### 4. Audit Verification (No Code Change Needed)

- **`health.liveness`**: Already correct on both sockets. Neural-api returns
  `{"status":"alive","version":"..."}`. API socket returns `{"status":"healthy","primal":"biomeos"}`.
  Marked RESOLVED in primalSpring's `PRIMAL_GAPS.md` as BM-02 since v2.81.
- **BTSP ClientHello redirect**: Correct by design. API socket redirects to neural-api
  socket which handles full BTSP handshake via `server_handshake()`.

---

## Deep Debt Audit (v3.24)

| Category | Status |
|----------|--------|
| Files >800L (production) | 0 (peak: 799L `node_handlers.rs`) |
| Unsafe in production | 0 (`#![forbid(unsafe_code)]` all crate roots) |
| TODO/FIXME/HACK/XXX | 0 |
| `todo!()`/`unimplemented!()` | 0 |
| Hardcoded primal names | 0 (all `primal_names` constants) |
| Hardcoded IPs/ports | 0 (all in test blocks or warn messages) |
| Mocks in production | 0 |
| `Box<dyn Error>` | 0 (only in `examples/`) |
| `unwrap()` in production | 0 |
| `lazy_static`/`once_cell` | 0 (using `LazyLock`) |
| `#[allow(...)]` | 0 (using `#[expect(reason)]`) |
| C dependencies | rtnetlink → netlink-sys (thin FFI, documented) |

---

## Verification

```
cargo check --workspace     # 0 errors
cargo clippy -- -D warnings # 0 warnings
cargo test --workspace      # 7,814+ pass, 0 failures
cargo fmt --check           # clean
```

---

## References

| Document | Location |
|----------|----------|
| primalSpring audit | User-provided downstream audit (April 2026) |
| Neural API routing | `crates/biomeos-atomic-deploy/src/neural_api_server/routing.rs` |
| API socket dispatch | `crates/biomeos-api/src/unix_server.rs` |
| Graph executor fix | `crates/biomeos-atomic-deploy/src/neural_executor_node_impls.rs` |
| Operation struct | `crates/biomeos-atomic-deploy/src/neural_graph.rs` |
| Bootstrap graphs | `graphs/tower_atomic_bootstrap.toml`, `graphs/nucleus_complete.toml` |
