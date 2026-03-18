# biomeOS v2.52 — Capability-First Discovery + MCP Aggregation + Provenance

**Date**: March 18, 2026
**Previous**: v2.51 (Ecosystem Absorption — IPC resilience, proptest, MCP tools)
**Scope**: Absorbed 4 patterns from Squirrel alpha.13 and primalSpring v0.3.0

---

## What Changed

### 1. Capability-First Socket Discovery (from Squirrel alpha.13)

biomeOS discovery engine now prefers capability-named sockets over primal-named ones.
When discovering "beardog", the engine first probes `security.sock` and `crypto.sock`
before falling back to `beardog-{family}.sock`.

**Files changed:**
- `crates/biomeos-core/src/socket_discovery/engine.rs` — XDG, family-tmp, and
  `discover_capability()` all try capability sockets first
- `crates/biomeos-core/src/socket_discovery/capability_sockets.rs` — NEW: mapping
  from primal names to capability domain socket names
- `crates/biomeos-core/src/socket_discovery/mod.rs` — updated discovery order docs (8 steps)

**Discovery order (updated):**
1. Env hint
2. Capability-first sockets (security.sock, compute.sock, etc.)
3. XDG runtime (primal-family.sock)
4. Abstract socket (Android)
5. Family-scoped tmp
6. Socket registry (socket-registry.json)
7. Neural API registry query
8. TCP fallback

### 2. MCP Tool Aggregation (`mcp.tools.list`)

New JSON-RPC method aggregates all capability translations into MCP-compliant tool
definitions. Squirrel's AI gateway calls this to discover available tools at runtime.

**Files changed:**
- `crates/biomeos-atomic-deploy/src/handlers/capability.rs` — `mcp_tools_list()` method
- `crates/biomeos-atomic-deploy/src/neural_api_server/routing.rs` — Route + dispatch

### 3. Structured Provenance Type (from primalSpring v0.3.0)

`Provenance` struct tracks where absorbed patterns came from: source spring,
baseline date, description, source version.

**Files changed:**
- `crates/biomeos-types/src/provenance.rs` — NEW: Provenance, ProvenanceManifest
- `crates/biomeos-types/src/lib.rs` — module + re-exports

### 4. Capability Registry TOML Sync Tests (from primalSpring v0.3.0)

Two sync tests prevent config/code drift:
- `capabilities_match_registry_toml` — all TOML providers must be known primals
- `all_core_primals_have_capabilities_in_toml` — core 5 primals must have translations

The sync test immediately caught 3 missing primals: petalTongue, skunkBat, sourDough.

**Files changed:**
- `crates/biomeos-atomic-deploy/src/capability_translation_tests.rs` — 2 new tests
- `crates/biomeos-types/src/primal_names.rs` — PETALTONGUE, SKUNKBAT, SOURDOUGH +
  AUXILIARY_PRIMALS array + display names + updated is_known_primal

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --workspace -- -D warnings` | PASS (0 warnings) |
| `cargo test --workspace` | PASS (5,279 tests, 0 failures) |
| Files >1000 LOC | 0 (engine.rs stayed under via extraction) |

## Delta from v2.51

- **+11 tests** (5,268 → 5,279)
- **+3 new primals** (petalTongue, skunkBat, sourDough)
- **+1 new module** (provenance.rs)
- **+1 new module** (capability_sockets.rs)
- **+1 new JSON-RPC method** (mcp.tools.list)
- **+1 new discovery step** (capability-first sockets)

## Next Steps

- Wire `Provenance` annotations into absorbed modules (ipc.rs, cast.rs, validation.rs)
- Implement capability-first socket **binding** in primals (they currently bind to primal-named sockets)
- Expand MCP tool schemas with richer inputSchema from spring manifests
- Target 90% coverage via llvm-cov
