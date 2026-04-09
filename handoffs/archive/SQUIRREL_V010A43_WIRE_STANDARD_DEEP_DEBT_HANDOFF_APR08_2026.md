# Squirrel v0.1.0-alpha.43 — Wire Standard L2 + Deep Debt Sprint

**Date**: April 8, 2026
**Scope**: Wire Standard compliance, production mock elimination, dead code removal, Tower Atomic enforcement
**Tests**: 6,850 passing (0 failures, 101 ignored), clippy PASS (0 warnings), fmt PASS, doc PASS

---

## Changes

### 1. Wire Standard L2 Compliance (GAP-MATRIX-05 resolution)

- **`capabilities.list`** — response `methods` field changed from nested object map to flat `["domain.operation", ...]` string array per CAPABILITY_WIRE_STANDARD.md; added L3 fields: `provided_capabilities`, `consumed_capabilities`, `cost_estimates`, `operation_dependencies`, `protocol`, `transport`
- **`identity.get`** — field `primal_id` → `primal`; removed non-standard fields (`transport`, `protocol`, `jwt_issuer`, `jwt_audience`); returns `primal`, `version`, `domain`, `license` per Wire Standard L2
- **`health.liveness`** — added `"status": "alive"` alongside existing `"alive": true` for full L1 compatibility

### 2. Daemon Mode (validated)

- Safe re-exec pattern via `std::process::Command` (zero `unsafe`)
- `--daemon` flag spawns detached child with `SQUIRREL_DAEMONIZED=1`; parent prints PID and exits
- biomeOS discovers daemon via socket probing + manifest; child writes primal manifest

### 3. Tower Atomic Pattern Enforcement

- **`reqwest` banned in `deny.toml`** — all HTTP must route through Songbird service mesh via IPC
- **`DefaultEndpoints::socket_path(service)`** — Unix socket resolution as primary tier in ecosystem-api defaults, before HTTP fallback
- `reqwest` is optional in workspace (behind feature gates); default build is reqwest-free

### 4. Production Mock Elimination

- **SDK MCP `OperationHandler`** — 6 placeholder methods returning fake data (hardcoded calculator tool, text processor, file resources, prompts) replaced with honest empty returns and proper `McpError` when no MCP server connected; added `connected: bool` and `with_connection()` for future IPC wiring
- **Web adapter `get_component_markup`** — `"<div>Component markup placeholder</div>"` → `anyhow::bail!("component {id} markup not available: legacy web plugin adapter does not support component rendering")`

### 5. Dead Code Removal

- **`orchestration/mod.rs`** (791 lines) — discovered never compiled (not in `lib.rs` module tree); used banned `reqwest::Client` directly; removed entirely

### 6. Smart Refactoring

- **`severity.rs`** (803→275 lines production) — 550+ line test section extracted to `severity_tests.rs` via `#[path = "severity_tests.rs"]` pattern

### 7. Lint Cleanup

- SDK unfulfilled `clippy::if_not_else` expectation removed
- `niche.rs` license constant aligned to `AGPL-3.0-or-later`
- Clippy: zero warnings across entire 22-crate workspace

---

## Files Changed

### Wire Standard (3 files)
- `crates/main/src/rpc/handlers_capability.rs`
- `crates/main/src/rpc/handlers_identity.rs`
- `crates/main/src/rpc/handlers_system.rs`

### Mock elimination (2 files + tests)
- `crates/sdk/src/communication/mcp/operations.rs`
- `crates/core/plugins/src/web/adapter.rs`

### Ecosystem defaults (1 file)
- `crates/ecosystem-api/src/defaults.rs`

### Dead code removal (1 file)
- `crates/universal-patterns/src/orchestration/mod.rs` (deleted)

### Smart refactoring (2 files)
- `crates/sdk/src/infrastructure/error/severity.rs` (trimmed to 275 lines)
- `crates/sdk/src/infrastructure/error/severity_tests.rs` (new, 550+ lines)

### Lint / constants (2 files)
- `crates/sdk/src/lib.rs`
- `crates/main/src/niche.rs`

### Root docs (4 files)
- `README.md`, `CONTEXT.md`, `CURRENT_STATUS.md`, `CHANGELOG.md`

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --workspace --all-targets` | PASS (0 warnings) |
| `cargo test --workspace` | 6,850 passing / 0 failures / 101 ignored |
| `cargo doc --workspace --no-deps` | PASS (0 warnings) |
| unsafe code | 0 — `unsafe_code = "forbid"` workspace-wide |
| Production mocks | 0 — all placeholder data eliminated |

---

## Downstream Impact

- **biomeOS**: Can now auto-discover Squirrel via `capabilities.list` flat `methods` array — routing `ai.*` domain calls works with Wire Standard L1+ parsers
- **primalSpring**: GAP-MATRIX-05 for Squirrel is resolved; daemon mode validated; Wire Standard L2 complete
- **Songbird**: Tower Atomic pattern enforced — Squirrel will not make direct HTTP calls; all traffic via IPC

## Next Steps

1. Coverage push: ~86% → 90% target (IPC/network integration tests, binary entry points)
2. `async-trait` migration: 129 → further reduction as `dyn` surfaces shrink
3. Phase 2 placeholders: persistence backends (NestGate), ML/neural network engine, WebSocket transport, marketplace
