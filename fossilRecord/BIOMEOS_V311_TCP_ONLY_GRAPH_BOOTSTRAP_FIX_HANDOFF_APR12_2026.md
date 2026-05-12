# biomeOS v3.11 — TCP-Only Graph Bootstrap Fix

**Date**: 2026-04-12
**Author**: biomeOS team
**Scope**: 4 root causes preventing v3.09 gap fixes from activating at runtime
**Downstream audit**: primalSpring Phase 34 gap report
**Commit**: `8515f246`

## Context

biomeOS v3.09 shipped 5 code-complete gap fixes (BTSP client handshake, method-prefix
demangling, socket directory scan, ipc.resolve, graph.list path resolution). primalSpring
downstream audit confirmed **none activated at runtime** in TCP-only / Docker NUCLEUS
deployments. Root cause: graph bootstrapping in `--tcp-only` mode — 4 independent issues
compounded to produce an empty capability route table, causing all forwarding to fall back
to blind UDS relay.

## Root Causes and Fixes

### 1. `graph.load` self-referential loop
- **Symptom**: `graph.load` via TCP → semantic fallback → `capability.call("graph", "load")` → router finds biomeOS at `neural-api-{family_id}.sock` → socket doesn't exist in TCP-only mode → fail
- **Root cause**: `graph.load` was missing from ROUTE_TABLE; fell through to generic capability.call dispatch
- **Fix**: Added `("graph.load", Route::GraphGet)` to route table — handled locally like `graph.get`
- **File**: `routing.rs` — 1 line

### 2. `NeuralApiServer.graphs_dir` not resolved to absolute
- **Symptom**: `GraphHandler.graphs_dir` was resolved to absolute (v3.09 fix), but `NeuralApiServer.graphs_dir` stayed relative — bootstrap and translation loading used the unresolved path
- **Root cause**: Resolution happened only in `GraphHandler::new_with_metrics_db`, not in `NeuralApiServer::new`
- **Fix**: Resolve relative `graphs_dir` to absolute at `NeuralApiServer` construction (same logic as GraphHandler)
- **File**: `neural_api_server/mod.rs` — 7 lines

### 3. Self-registration uses UDS endpoint in TCP-only mode
- **Symptom**: `register_self_in_registry` registered biomeOS capabilities at `neural-api-{family_id}.sock` even when TCP-only — dead route for all `capability.call` forwarding to self
- **Root cause**: `register_self_in_registry` unconditionally called `register_capability_unix`
- **Fix**: New `tcp_port: Option<u16>` parameter; when `Some`, registers `TransportEndpoint::TcpSocket` instead of `UnixSocket`
- **File**: `bootstrap.rs` — signature change + TCP branch

### 4. Silent parse failures in `graph.list`
- **Symptom**: `graph.list` returned `[]` with no explanation — 8 TOML files on disk but zero graphs listed
- **Root cause**: Both `Graph::from_toml_file` and `GraphLoader::from_file` failures were silently swallowed per-file
- **Fix**: `warn!`-level logging with both error messages when a `.toml` file fails both parsers
- **File**: `handlers/graph/mod.rs` — match-arm restructure

### Bonus: Auto-scan all graphs for capability translations on startup
- Previously only `tower_atomic_bootstrap.toml` got its capability translations loaded
- Now `serve()` calls `load_translations_from_all_graphs()` after bootstrap — scans every `.toml` in `graphs_dir` and registers capability categories from graph nodes
- Ensures the full route table is populated before any client connects — critical for TCP-only where discovery cannot lazily rescan UDS directories
- **File**: `translation_startup.rs` — 50 lines

## Files Changed (7)

| File | Change |
|------|--------|
| `neural_api_server/routing.rs` | +1 route: `graph.load` → `GraphGet` |
| `neural_api_server/mod.rs` | Resolve `graphs_dir` to absolute at construction |
| `bootstrap.rs` | `register_self_in_registry` TCP endpoint support |
| `neural_api_server/bootstrap.rs` | Pass `tcp_port` to self-registration |
| `handlers/graph/mod.rs` | Diagnostic logging for parse failures |
| `neural_api_server/server_lifecycle.rs` | Auto-scan all graphs on startup |
| `neural_api_server/translation_startup.rs` | `load_translations_from_all_graphs()` |

## Validation
- `cargo fmt --all -- --check`: PASS
- `cargo clippy --workspace --all-targets`: PASS (0 warnings)
- `cargo test --workspace`: **7,000+ passed, 0 failed**

## Expected Downstream Impact

Once primalSpring rebuilds against this commit, the v3.09 gap fixes should activate
end-to-end in TCP-only / Docker NUCLEUS:
- `graph.list` returns all 8+ graphs (capability route table populated)
- `graph.load` handled locally (no self-referential loop)
- `capability.call` resolves to TCP endpoint for biomeOS self-capabilities
- All 5 v3.09 fixes (BTSP, demangling, socket dirs, ipc.resolve, graph.list) activate
- NUCLEUS composition forwarding lights up through canonical path
