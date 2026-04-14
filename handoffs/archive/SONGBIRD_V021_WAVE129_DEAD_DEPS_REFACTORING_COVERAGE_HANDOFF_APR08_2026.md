# Songbird v0.2.1 — Wave 129: Dead Dep Removal, File Refactoring, Coverage

**Date**: April 8, 2026  
**Primal**: Songbird  
**Wave**: 129  
**Status**: Complete  
**Commit**: `011ac7a8`

---

## Changes

### Dead Dependencies Removed
- `parking_lot` — zero usage in orchestrator src or tests (verified via grep)
- `async-stream` — zero usage (only "async stream" appeared in a doc comment)
- `tokio-stream` — zero usage

Impact: faster compilation, reduced dependency tree for `songbird-orchestrator`.

### File Refactoring — Zero Files >800L
- `ai_tests.rs` (863L) → 8-module tree under `ai_tests/`:
  - `mod.rs` (12L), `adapter_creation.rs` (37L), `transport_mock.rs` (128L)
  - `discovery_fallback.rs` (141L), `deprecation_warnings.rs` (58L)
  - `metrics_health.rs` (213L), `model_types_metrics_edges.rs` (154L), `metrics_extended.rs` (166L)
- Largest file in codebase: 778L (test), 711L (production)

### Coverage Expansion (+23 tests)

| Module | Tests Added |
|--------|------------|
| `bin_interface/config.rs` | Default construction, validation, builder/merge, env overrides, init_config template, edge cases |
| `ipc/pure_rust_server/protocol.rs` | JsonRpcRequest serde (with/without params/id), JsonRpcResponse success/error, JsonRpcError helpers |
| `ipc/pure_rust_server/coordination_handlers.rs` | `handle_discover_capabilities` return structure and metadata |

## Audit Summary (Wave 129)

| Category | Status |
|----------|--------|
| Files >800L | 0 (all crates, production + test) |
| Mocks in production | 0 (all behind `#[cfg(test)]` or feature gate) |
| Production unwrap/expect | 0 |
| `#[allow(` without reason | 0 (false positives from multi-line attrs) |
| Hardcoded IPs/ports | Production: configurable via env; test: fixtures only |
| Unused deps | parking_lot, async-stream, tokio-stream removed |
| cargo deny | Pass (advisories ok, bans ok, licenses ok, sources ok) |

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 12,945 passed, 0 failed, 252 ignored |
| Clippy | Clean (pedantic + nursery, `-D warnings`) |
| Format | Clean |
| Build | 30/30 crates, zero warnings |
