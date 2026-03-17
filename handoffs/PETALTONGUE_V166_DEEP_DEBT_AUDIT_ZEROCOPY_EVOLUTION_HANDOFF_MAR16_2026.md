# petalTongue v1.6.6 — Deep Debt Audit, Zero-Copy & Test Infrastructure Evolution Handoff

**Date**: March 16, 2026
**Version**: v1.6.6 (same version, deep quality evolution)
**Scope**: Comprehensive audit execution — formatting, coverage, zero-copy migration, hardcoding elimination, large file refactoring, fuzz testing, property-based testing, cross-primal e2e tests, debris cleanup

---

## What Changed

### Comprehensive Audit & Execution

Full codebase audit against wateringHole standards (`STANDARDS_AND_EXPECTATIONS.md`, `ECOBIN_ARCHITECTURE_STANDARD.md`, `PRIMAL_IPC_PROTOCOL.md`, `SEMANTIC_METHOD_NAMING_STANDARD.md`) with all findings executed.

### P0 — Formatting

- Fixed 2 files (`doom-core/wad_loader.rs`, `discovery/jsonrpc_provider/tests.rs`) that drifted from `cargo fmt`

### P1 — Hardcoding → Capability-Based

- Replaced hardcoded `"petalTongue"` string literals with `PRIMAL_NAME` constant in 3 production files:
  - `tutorial_mode.rs` — tutorial graph node name
  - `timeline_view/view.rs` — CSV export path
  - `state_sync/persistence.rs` — state directory path
- Updated `mock-biomeos` sandbox from edition 2021 → 2024
- Improved `AppError::UiNotAvailable` with actionable error message (`Try tui or web mode, or rebuild with --features ui`) and proper `#[cfg_attr(feature = "ui", allow(dead_code))]`

### P2 — Zero-Copy Migration (Arc<str>)

Migrated core ID type aliases per wateringHole zero-copy requirements (`bytes::Bytes` for binary, `Arc<str>` for string IDs):

| Type | Before | After |
|------|--------|-------|
| `DataSourceId` | `String` | `Arc<str>` |
| `GrammarId` | `String` | `Arc<str>` |

All `.clone()` calls on these IDs are now O(1) atomic reference count increments instead of heap allocations. Cascade fixed across `petal-tongue-core`, `petal-tongue-ui`, and test files.

### P2 — Smart Large File Refactoring

Extracted test modules from 3 largest files into sibling test files:

| File | Before | After (prod) | Tests file |
|------|--------|-------------|------------|
| `json_rpc_client.rs` | 902 | 383 | 523 |
| `server.rs` | 850 | 469 | 386 |
| `interaction/engine.rs` | 815 | 398 | 419 |

Used `#[path = "..._tests.rs"] mod tests;` pattern — production code is focused, tests live alongside.

### P2 — Cross-Primal IPC E2E Tests

New `crates/petal-tongue-ipc/tests/cross_primal_e2e.rs` with 6 tests exercising real Unix socket server ↔ JSON-RPC client:
- `health.check` end-to-end
- `topology.get` end-to-end
- `capability.list` end-to-end
- Unknown method → JSON-RPC METHOD_NOT_FOUND (-32601)
- Concurrent clients (2 parallel)
- Server graceful shutdown

### P3 — Fuzz Testing (proptest)

New `crates/petal-tongue-ipc/tests/json_rpc_fuzz.rs`:
- Roundtrip serialization for `JsonRpcRequest` and `JsonRpcResponse`
- Random bytes resilience (never panics on malformed input)
- Random string resilience
- Client ID monotonicity

### P3 — Property-Based Testing (proptest)

New `crates/petal-tongue-core/tests/proptest_core.rs`:
- `BoundingBox` normalization, containment, dimensions (always non-negative)
- `DataObjectId` display contains source string
- `FilterExpr` JSON serialization roundtrip

### Coverage Improvement

| File | Before | After |
|------|--------|-------|
| `data_service.rs` | 85.7% | **90.96%** |
| `headless_mode.rs` | ~96% | **100%** |
| `error.rs` | 93.1% | **100%** |
| **Root crate overall** | 88.67% | **89.76%** |

Remaining gap: `ui_mode.rs` (eframe requires display server) and `main.rs` (async runtime init) — inherently hard-to-test paths.

### Debris Cleanup

Moved legacy docs and scripts to `archive/docs-mar-2026/debris/`:
- `docs/` (5 planning/operations files)
- `web/index.html` (legacy web stub)
- `EVOLUTION_TRACKER.md`, `CHANGELOG.md`, `PROJECT_STATUS.md`
- `.docs-manifest.txt`, `.env.example`

Updated `README.md` and `START_HERE.md` with current metrics.

### Production Mock Audit

Verified all mock code is properly cfg-gated:
- `BiomeOSClient.mock_mode` → `#[cfg(any(test, feature = "test-fixtures"))]` in production returns `MockModeUnavailable`
- `biomeos_ui_manager.rs` `unreachable!()` → inside `#[cfg(not(feature = "mock"))]`
- Zero production mock leakage

### #[allow()] Attribute Audit

All `#[allow()]` attrs justified:
- `tui.rs` — clippy `missing_const_for_fn` false positive on `&mut self`
- `data_service.rs` — `dead_code` on public API awaiting consumers
- `error.rs` — fixed: now `#[cfg_attr(feature = "ui", allow(dead_code))]`

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 5,244 | **5,404** (+160) |
| Coverage (root) | 88.67% | **89.76%** |
| Largest file | 902 lines | **854 lines** |
| `cargo fmt` | FAIL (2 files) | **PASS** |
| `cargo clippy` | PASS | **PASS** |
| `cargo doc` | PASS | **PASS** |
| Hardcoded primal names | 3 in prod | **0** |
| Zero-copy ID types | 0 | **2** (`DataSourceId`, `GrammarId`) |
| Property tests | 0 | **10** (5 IPC + 5 core) |
| Cross-primal e2e tests | 0 | **6** |

---

## Compliance

| Standard | Status |
|----------|--------|
| AGPL-3.0-or-later | ✅ All crates + sandbox |
| SPDX headers | ✅ All source files |
| `#![forbid(unsafe_code)]` | ✅ All crates |
| Edition 2024 | ✅ All 16 crates + sandbox (was 2021) |
| No TODO/FIXME/HACK | ✅ Zero in committed code |
| Files < 1000 lines | ✅ Largest 854 |
| Self-knowledge only | ✅ No hardcoded primal names in production |
| Capability-based discovery | ✅ Runtime discovery, env-overridable |
| Zero-copy (wateringHole) | ✅ `Arc<str>` for IDs, `bytes::Bytes` for payloads |
| Mocks isolated to test | ✅ All cfg-gated |
| UniBin | ✅ Single binary, 6 subcommands |
| ecoBin | ✅ Pure Rust, no C deps |

---

## Next Steps

- Push overall workspace coverage past 90% (requires headless display testing infrastructure for `ui_mode.rs`)
- Continue `Arc<str>` migration to remaining `String` fields in session state, graph validation types
- Explore `Cow<'_, str>` for fields that are sometimes borrowed, sometimes owned
- Add load/stress testing beyond current chaos scenarios
- Add `cargo-fuzz` targets for deeper fuzz coverage
