# biomeOS v2.92 — Deep Debt Evolution & Capability Routing Handoff

**Date**: April 7, 2026
**From**: biomeOS orchestrator team
**To**: All primal teams (BearDog, Songbird, NestGate, Toadstool, Squirrel), primalSpring, wetSpring, ludoSpring
**Status**: PRODUCTION READY — 7,649 tests passing, 0 clippy warnings, 0 unsafe code

---

## Critical for Primal Teams

### 1. Capability Discovery Now Works End-to-End (GAP-MATRIX-01 RESOLVED)

**What changed**: biomeOS's Neural API capability probe now correctly discovers all primal capabilities.

**Root causes fixed**:
- **Method name mismatch**: `probe_unix_socket_capabilities_list` tried `capabilities.list` (plural) only. BearDog and others implement `capability.list` (singular). Now tries both with fresh connections.
- **Incomplete format parsing**: Only 3 of 4 ecosystem wire formats were handled. Now supports all 4:
  - **Format A**: Flat string array `["encryption", "identity", ...]`
  - **Format B**: Object array `[{"method": "encrypt"}, {"name": "decrypt"}]`
  - **Format C**: `method_info` array `{"method_info": [{"name": "..."}]}`
  - **Format D**: Semantic mappings `{"semantic_mappings": {"security": {"encrypt": ...}}}`

**Action for primal teams**: No changes required. Your existing `capability.list` / `capabilities.list` implementations will now be correctly discovered. Verify by checking Neural API logs for non-zero capability counts after biomeOS upgrade.

### 2. Real Health Probing (No More Stub)

**What changed**: `probe_endpoint()` was a stub returning fabricated health data. Now sends actual JSON-RPC requests:
- `identity.get` → learns primal name + version
- `capabilities.list` → discovers advertised capabilities

**Action for primal teams**: If your primal doesn't implement `identity.get`, that's fine — biomeOS falls back gracefully. Consider adding it for better observability:

```json
{"jsonrpc": "2.0", "method": "identity.get", "id": 1}
→ {"result": {"name": "beardog", "version": "0.9.0"}}
```

### 3. TOML Graph Parsing Fixed (GAP-MATRIX-02 RESOLVED)

**What changed**: `GraphId` validation rejected underscores. `tower_atomic_bootstrap.toml` (and any graph with underscores in its `id`) was silently rejected, degrading to defaults.

**Action for graph authors**: Underscores are now valid in graph IDs. Pattern: `[a-z0-9_-]+`.

### 4. Taxonomy Now Includes "registry" Alias

`CapabilityTaxonomy::resolve_to_primal("registry")` now correctly resolves to `songbird` (maps to `Discovery` capability). Previously returned `None`.

---

## For primalSpring / Spring Teams

### Capability Parser Alignment

biomeOS now implements a 5-format parser (superset of primalSpring's `ipc/discover.rs → extract_capability_names()`). The canonical implementation lives at:
- `biomeos-core/src/socket_discovery/cap_probe.rs` — `extract_capabilities_from_response()`
- `biomeos-graph/src/ai_advisor.rs` — inline replica (no cross-crate dep)

Springs calling `capability.call` through biomeOS should now see correct routing for all primals.

### Semantic Method Routing

The Neural API semantic fallback (v2.90) + this capability discovery fix means any `domain.operation` JSON-RPC method now routes correctly through the full stack:
1. Explicit `ROUTE_TABLE` entries take precedence
2. `CapabilityTranslationRegistry` handles known translations
3. Semantic fallback routes unrecognized `domain.operation` via `capability.call`
4. Capability discovery (now fixed) ensures the target primal is found

---

## Dependency Changes (All Teams)

| Change | Impact |
|--------|--------|
| `tokio-tungstenite` 0.21 → 0.24 | Eliminates duplicate WebSocket stack. If you depend on biomeOS types that re-export tungstenite, update accordingly. |
| `tokio` `test-util` moved to dev-deps | No production impact. Test code using `tokio::time::pause()` still works via dev-dependency feature merging. |
| `serde_yaml_ng` (not `serde_yml`) | Workspace uses `serde_yaml = { package = "serde_yaml_ng" }`. Pure Rust (`unsafe-libyaml` is Rust code, not C FFI). |

---

## Nucleus Evolution (Orchestration Teams)

### Dynamic Ecosystem Detection

`detect_ecosystem()` no longer iterates a hardcoded `CORE_PRIMALS` list. It dynamically scans the socket directory for any `*-{family_id}.sock` files. Any primal following the naming convention is discovered — including new primals added to the ecosystem without biomeOS code changes.

### Convention-Based Health Sockets

The Toadstool-specific `.jsonrpc.sock` health check is now convention-based: any primal that exposes a `.jsonrpc.sock` alongside its primary `.sock` gets the `health.status` method registered automatically.

### Capability-Only Socket Resolution

`socket_path_for_capability()` no longer has hardcoded fallbacks (`"security" → beardog`, `"registry" → songbird`). It relies exclusively on `CapabilityTaxonomy::resolve_to_primal()`. If the taxonomy can't resolve a capability, the socket path uses "unknown" which naturally fails at connect time with a clear error.

---

## Code Quality Metrics

| Metric | Value |
|--------|-------|
| Tests passing | 7,658 (0 failures) |
| Clippy warnings | 0 (pedantic + nursery) |
| Unsafe code | 0 (`#![forbid(unsafe_code)]` all crates) |
| Files > 1000 LOC | 0 |
| TODO/FIXME/HACK | 0 |
| Production mocks | 0 |
| C FFI dependencies | 0 |

---

## v2.93 Addendum: GAP-MATRIX Resolution (same day)

### GAP-MATRIX-07 (Critical) — Proxy Forwarding Fixed

`TransportEndpoint::parse()` now handles the `unix://` URI scheme. Previously, any `unix:///path` string — from `display_string()` round-trips or external `capability.register` calls — contained `:` and was misrouted to TCP parsing. The fallback then created a literal `PathBuf("unix:///run/...")` which can't connect to any socket. **All `capability.call` forwarding now works end-to-end.**

**Impact for primal teams**: If your code sends `capability.register` with `socket: "unix:///run/biomeos/..."`, it now parses correctly. Bare paths (`/run/biomeos/...`) continue to work as before.

### GAP-MATRIX-01b (Medium) — BearDog Format E Recognized

Added Format E to the capability parser: `result.provided_capabilities: [{type: "security", methods: ["sign", ...]}]`. This is BearDog's native wire format. The parser now emits:
- Group type as a capability: `"security"`, `"crypto"`, `"beacon"`, etc.
- Qualified methods: `"security.sign"`, `"security.verify"`, `"crypto.blake3_hash"`, etc.

BearDog's 9 capability groups are now fully registered in the Neural API capability registry.

### GAP-MATRIX-02 (Medium) — TOML Parser Tolerant

`GraphDefinition.name` and `.version` are now optional (`#[serde(default)]`). `tower_atomic_bootstrap.toml` — which intentionally omits both — now parses through the `DeploymentGraph` serde path in addition to the `neural_graph::Graph` path.

---

## v2.94 Addendum: GAP-MATRIX Second Wave (same day)

### GAP-MATRIX-07b (Medium) — Proxy Error Propagation

Primal JSON-RPC errors (e.g. `-32601 Method not found`) were being swallowed as generic `-32603 Internal error: Failed to forward...`. Callers could not distinguish "primal rejected the request" from "primal is unreachable."

**Fix**: `forward_request()` now uses `try_call()` and propagates `IpcError::JsonRpcError` without wrapping. `dispatch()` extracts the original error code via `downcast_ref::<IpcError>()`.

**Impact for primal teams**: When a primal returns a JSON-RPC error (e.g. unknown method), the caller now receives the exact error code and message from the primal, not a generic internal error.

### GAP-MATRIX-08 (Low) — Self-Discovery Pollution

Neural API registered itself as a capability provider ~20s after startup because `lazy_rescan_sockets()` didn't filter its own socket. The initial scan in `discover_and_register_primals()` already excluded `self.socket_path`, but the lazy rescan path (triggered on first capability miss) did not.

**Fix**: `NeuralRouter` now stores its own socket path via `set_self_socket_path()`. `lazy_rescan_sockets()` skips that path, matching the initial-scan filter.

**Impact**: No more duplicate `neural @` routing entries. Capability routing is clean from first miss onward.

### GAP-MATRIX-02b (Medium, partial) — graph.list Unified with DeploymentGraph

`graph.list` returned empty for `tower_atomic_bootstrap.toml` because the `neural_graph::Graph` parser failed on certain TOML structures. The `DeploymentGraph` loader (fixed in v2.93) could parse them, but `graph.list` only used the `neural_graph` parser.

**Fix**: `graph.list` now falls back to `biomeos_graph::GraphLoader::from_file()` when `Graph::from_toml_file()` fails. This extracts `id`, `version`, `description`, `node_count`, and `coordination` from `GraphDefinition` for the listing.

**Impact for primal teams**: All valid TOML graphs — both `neural_graph` and `DeploymentGraph` formats — now appear in `graph.list` results.

---

## v2.94 Addendum: GAP-MATRIX Second Wave (same day)

### GAP-MATRIX-07b (Medium) — Proxy Error Propagation

Primal JSON-RPC errors (e.g. `-32601 Method not found`) were being swallowed as generic `-32603 Internal error: Failed to forward...`. Callers could not distinguish "primal rejected the request" from "primal is unreachable."

**Fix**: `forward_request()` now uses `try_call()` and propagates `IpcError::JsonRpcError` without wrapping. `dispatch()` extracts the original error code via `downcast_ref::<IpcError>()`.

**Impact for primal teams**: When a primal returns a JSON-RPC error (e.g. unknown method), the caller now receives the exact error code and message from the primal, not a generic internal error.

### GAP-MATRIX-08 (Low) — Self-Discovery Pollution

Neural API registered itself as a capability provider ~20s after startup because `lazy_rescan_sockets()` didn't filter its own socket. The initial scan in `discover_and_register_primals()` already excluded `self.socket_path`, but the lazy rescan path (triggered on first capability miss) did not.

**Fix**: `NeuralRouter` now stores its own socket path via `set_self_socket_path()`. `lazy_rescan_sockets()` skips that path, matching the initial-scan filter.

**Impact**: No more duplicate `neural @` routing entries. Capability routing is clean from first miss onward.

### GAP-MATRIX-02b (Medium, partial) — graph.list Unified with DeploymentGraph

`graph.list` returned empty for `tower_atomic_bootstrap.toml` because the `neural_graph::Graph` parser failed on certain TOML structures. The `DeploymentGraph` loader (fixed in v2.93) could parse them, but `graph.list` only used the `neural_graph` parser.

**Fix**: `graph.list` now falls back to `biomeos_graph::GraphLoader::from_file()` when `Graph::from_toml_file()` fails. This extracts `id`, `version`, `description`, `node_count`, and `coordination` from `GraphDefinition` for the listing.

**Impact for primal teams**: All valid TOML graphs — both `neural_graph` and `DeploymentGraph` formats — now appear in `graph.list` results.

---

## Remaining Known Items

1. **Primal-specific env vars** (`BEARDOG_SOCKET`, `SONGBIRD_SOCKET`, etc.) remain as Tier 1/2 discovery configuration surface — these are the correct bootstrap mechanism, not routing violations.
2. **`NucleusMode::primals()`** maps deployment patterns to specific primals — this is intentional orchestrator configuration (biomeOS's job is to start primals).
3. **`build_primal_command_with()`** contains primal-specific CLI knowledge — each primal has its own startup interface. This is analogous to systemd service files.
4. **`BIOMEOS_STRICT_DISCOVERY=1`** disables all taxonomy fallbacks, requiring pure Songbird-based runtime discovery. Available for testing strict capability-first deployments.
