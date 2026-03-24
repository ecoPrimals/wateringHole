# rhizoCrypt v0.13.0-dev — Session 19 Handoff

**Date**: March 23, 2026
**Scope**: MCP tools, DagBackend enum, GC sweeper, RedbDagStore wiring, proptests, normalize_method, debris cleanup

---

## Changes Delivered

### 1. MCP Tool Definitions (`tools.list`, `tools.call`)

- `niche.rs` exposes `mcp_tools()` returning JSON Schema tool definitions for AI agent coordination
- JSON-RPC handler dispatches `tools.list` → tool catalog, `tools.call` → dynamic method routing via `dispatch_tools_call()`
- Aliases `mcp.tools.list`, `mcp.tools.call` for ecosystem compatibility
- New `tools` capability domain added to all niche constants

### 2. `DagBackend` Enum — Runtime Storage Dispatch

- `DagStore` trait uses RPITIT (`impl Future` returns), making it non-object-safe
- `DagBackend` enum (`Memory`, `Redb`) is the idiomatic Rust solution for runtime dispatch
- `RhizoCrypt.dag_store` field evolved to `Arc<RwLock<Option<DagBackend>>>`
- Inherent methods: `session_count()`, `total_vertex_count()`, `get_all_vertices()`

### 3. `RedbDagStore` Production Wiring

- `RhizoCrypt::start()` now instantiates `DagBackend::Redb` behind `#[cfg(feature = "redb")]`
- `RedbDagStore::get_all_vertices()` with topological iteration
- `StorageBackend::Redb` config variant; `Sled` explicitly `#[deprecated]`

### 4. GC/TTL Background Sweeper

- `gc_sweep()` identifies and discards expired sessions by `max_duration`
- `spawn_gc_sweeper()` as Tokio background task driven by `config.gc_interval`
- `Timestamp::duration_since()` (const fn) for age calculations

### 5. Legacy Method Prefix Normalization

- `normalize_method()` strips `rhizocrypt.` and `rhizo_crypt.` prefixes
- Integrated into JSON-RPC dispatch pipeline for backward compatibility

### 6. Health Response Evolution

- `health.liveness` → `{"status": "alive"}`
- `health.readiness` → `{"status": "ready" | "not_ready"}`
- Aligned with ecosystem Semantic Method Naming Standard

### 7. Property-Based Tests (proptest)

- 5 suites: capability routing completeness, unknown method rejection, normalize_method idempotency, semantic mapping validity, liveness statelessness
- 4-format capability parsing proptests in `parsing.rs`

### 8. Debris Cleanup

- Removed `llvm-cov-full-output.txt` (build artifact)
- Removed `target-ci-check/` (stale CI check target directory)

---

## Current State

| Metric | Value |
|--------|-------|
| Tests | 1,412 passing (`--all-features`) |
| Clippy | 0 warnings (pedantic + nursery + cargo + cast lints) |
| Doc | 0 warnings (`-D warnings`) |
| Fmt | Clean |
| Source files | 128 `.rs`, ~36,336 lines |
| Max file | 867 lines (limit: 1000) |
| Unsafe | `deny` workspace-wide, zero `unsafe` blocks |
| C deps (default) | Zero (ecoBin compliant) |
| License | scyBorg Triple-Copyleft (AGPL-3.0+ / ORC / CC-BY-SA 4.0) |
| IPC Methods | 27 methods, 8 domains (incl. `tools.*` MCP) |

---

## For Other Primals

- **MCP tool pattern**: `niche.rs` → `mcp_tools()` with JSON Schema — any primal can expose tool definitions for AI agent coordination
- **`DagBackend` enum dispatch**: When a trait uses RPITIT (non-object-safe), use enum dispatch instead of `dyn Trait` — idiomatic and zero-overhead
- **`normalize_method()`**: If your primal has legacy method prefixes, normalize them at the handler entry point
- **GC sweeper pattern**: `spawn_gc_sweeper()` with configurable interval — any primal managing sessions should implement TTL cleanup
- **`parse_capability_response()`**: Handles 4 JSON formats for capability lists — use when consuming capabilities from diverse primals
