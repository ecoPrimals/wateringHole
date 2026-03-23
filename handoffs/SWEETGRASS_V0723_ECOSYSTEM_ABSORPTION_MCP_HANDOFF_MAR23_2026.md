# sweetGrass v0.7.23 — Ecosystem Absorption: MCP Tool Exposure & Canonical Capabilities

**Date**: March 23, 2026
**From**: sweetGrass
**To**: rhizoCrypt, loamSpine, biomeOS, Squirrel, all primals
**Status**: Released
**Previous**: v0.7.22 Deep Debt Resolution (Mar 23, 2026)

---

## Summary

Absorbed patterns from ecosystem springs and primals: MCP tool exposure
(airSpring v0.10 pattern), canonical `capabilities.list` method naming
(wateringHole SEMANTIC_METHOD_NAMING v2.1), and validation of existing
`DispatchOutcome` alignment (rhizoCrypt v0.13.0). JSON-RPC dispatch
table expanded from 24 to 27 methods. Stale documentation cleaned.

---

## Changes

### Added

- **MCP `tools.list` + `tools.call`** — expose braid operations as MCP tools
  for Squirrel AI coordination. `tools.list` returns 7 tool descriptors with
  JSON Schema `inputSchema`. `tools.call` dispatches named tools through the
  standard JSON-RPC handler table, returning MCP `content` + `isError` envelope.
  Pattern adopted from airSpring v0.10.

- **`capabilities.list` canonical method** — registered per wateringHole
  SEMANTIC_METHOD_NAMING v2.1 as the canonical name. `capability.list` retained
  as backward-compatible alias. Both route to the same handler.

- **8 new protocol tests** — canonical/alias equivalence, `tools.list`
  structure/contents validation, `tools.call` dispatch/error/missing-name,
  `DispatchOutcome` classification tests.

- **Niche self-knowledge expanded** — `niche.rs` now declares `capabilities.list`,
  `tools.list`, `tools.call` in CAPABILITIES array, `operation_dependencies()`,
  `cost_estimates()`, and `semantic_mappings()`.

### Changed

- **JSON-RPC dispatch table**: 24 → 27 methods
- **`find_handler` visibility**: `fn` → `pub(super) fn` (supports `tools.call` cross-module dispatch)
- **`capability_registry.toml`**: Added `capabilities`, `tools` domains with operation metadata
- **`sweetgrass_deploy.toml`**: readiness probe → `capabilities.list` (canonical)

### Validated (Already Implemented)

- **`DispatchOutcome`** — Success/ProtocolError/ApplicationError already aligned with rhizoCrypt v0.13.0
- **`IpcErrorPhase`** — `is_retriable()`, `is_application_error()` already aligned with loamSpine/healthSpring
- **Atomic socket test isolation** — already uses `tempdir()` + `start_uds_listener_at`

### Cleaned

- Removed `docs/HANDOFF_ABSORPTION_REPORT_MAR17_2026.md` (duplicate of wateringHole handoffs)
- Removed `showcase/INTEGRATION_GAPS_REPORT.md` (historical from v0.5.x, all gaps resolved)
- Removed `showcase/ROOTPULSE_EMERGENCE_PLAN.md` (historical, never built, concepts in codebase)
- All version references updated from 0.7.22 → 0.7.23 across README, ROADMAP, DEVELOPMENT,
  CHANGELOG, deploy.sh, specs, showcase, config, deploy graph

---

## Current State

| Metric | Value |
|--------|-------|
| Tests | 1,099 passing |
| JSON-RPC methods | 27 (was 24) |
| Clippy | 0 warnings (pedantic + nursery) |
| Format | Clean |
| Docs | 0 warnings (`-D warnings`) |
| cargo deny | advisories ok, bans ok, licenses ok, sources ok |
| Unsafe | 0 (`forbid(unsafe_code)` all crates) |
| Production unwraps | 0 (`unwrap_used`/`expect_used` = `deny`) |
| TODOs in source | 0 |
| Pure Rust deps | Confirmed (zero C/C++ in production) |
| .rs files | 133 |
| Max file | 808 lines (all under 1000) |

---

## MCP Tool Schema (for Squirrel)

`tools.list` returns tool descriptors in this format:

```json
{
  "tools": [
    {
      "name": "braid.create",
      "description": "Create a new attribution braid from content hash and metadata",
      "inputSchema": {
        "type": "object",
        "properties": {
          "data_hash": {"type": "string"},
          "mime_type": {"type": "string"},
          "size": {"type": "integer"}
        },
        "required": ["data_hash", "mime_type", "size"]
      }
    }
  ]
}
```

`tools.call` accepts `{"name": "braid.create", "arguments": {...}}` and returns
MCP-compatible `{"content": [{"type": "text", "text": ...}], "isError": false}`.

---

## For Other Primals

- **MCP adoption**: Any primal can expose its methods as MCP tools using the same
  pattern — `tools.list` returns tool descriptors, `tools.call` dispatches through
  the existing handler table. Zero new dependencies required.
- **`capabilities.list` canonical**: wateringHole v2.1 says `capabilities.list` is
  the canonical method name. Primals should register both `capabilities.list` and
  `capability.list` (alias) for backward compatibility.
- **`DispatchOutcome` pattern**: Separating protocol errors (parse, version, method
  not found) from application errors (handler failures) enables better retry logic
  at the transport layer.

---

## Breaking Changes

None. All changes are backward-compatible. `capability.list` continues to work.

---

## What's Next

- Cross-compile CI (musl, ARM64, RISC-V)
- `ValidationHarness` + `BaselineProvenance` (healthSpring pattern)
- `PROVENANCE_REGISTRY` completeness tests (neuralSpring pattern)
- sunCloud economics integration
- Coverage expansion on postgres store (Docker-gated tests)
