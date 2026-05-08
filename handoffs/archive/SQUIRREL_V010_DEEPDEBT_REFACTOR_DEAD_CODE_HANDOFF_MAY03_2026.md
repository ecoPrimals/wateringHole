# Squirrel v0.1.0 — Deep Debt Audit: Refactor, Dead Code, Debris Cleanup

**Date**: May 3, 2026  
**Session**: AW  
**Quality Gates**: fmt ✓ | clippy 0 warnings ✓ | 7,210 tests ✓ | deny ✓

---

## Changes

### Smart Refactor: `jsonrpc_server.rs` (890L → 675L + 225L)

Extracted request parsing and dispatch logic into `jsonrpc_request_processing.rs`:
- `handle_request_or_batch` (JSON-RPC 2.0 Section 6 batch support)
- `handle_single_request` (parse → validate → dispatch)
- `handle_single_request_object` (method extraction, params validation, metrics)
- `test_handle_jsonrpc_line` (integration test helper)

**Result**: Zero production `.rs` files over 800 lines.

### Dead Code Removed

| Item | Location | Reason |
|------|----------|--------|
| `SongbirdLoadBalancerConfig` type alias | `crates/core/core/src/lib.rs` | 0 callers |
| `SongbirdLoadBalancerIntegration` trait | `crates/core/core/src/lib.rs` | 0 callers |
| `parse_primal_type` function | `crates/core/core/src/ecosystem_coordination.rs` | Unused; superseded by capability discovery |
| Unused imports (`PrimalType`, `Error`, `primal_names`) | Multiple | Only consumers removed |

### Debris Cleaned

| Item | Size | Reason |
|------|------|--------|
| `crates/main/tests/error_path_coverage.rs` | 652L | Gated behind non-existent feature `disabled_until_capability_registry_exported` |
| `crates/main/tests/service_discovery_critical_paths.rs` | 628L | Same non-existent feature gate |
| `crates/core/mcp/tests/error_path_coverage.rs` | 259L | `#[cfg(all(feature = "integration-tests", false))]` — permanently disabled |
| `watcher` feature + `notify` dep | rule-system | Zero code usage of fs-watcher |
| `local` feature | ai-tools | Zero cfg gates |
| `storage`, `web` features | SDK | Zero cfg gates |

### Docs Updated

- `docs/CRYPTO_MIGRATION.md` — removed stale `miniz_oxide`/`flate2` reference (eliminated from workspace); added BTSP Phase 3 crypto (`chacha20poly1305`, `hkdf`, `sha2`)

---

## Full Audit Results

| Category | Finding |
|----------|---------|
| Unsafe code | Zero in production |
| `todo!()`/`unimplemented!()` | Zero |
| FIXME/HACK markers | Zero |
| External deps | 100% pure Rust (no C/FFI) |
| Production mocks | All intentional + documented (plugin sandbox, platform fallbacks, WASM boundary) |
| Large files (>800L) | Zero after refactor |
| Hardcoded primal names | Centralized in `primal_names.rs`; runtime paths use capability discovery |

---

## Files Modified

- `crates/main/src/rpc/jsonrpc_server.rs` — 890L → 675L
- `crates/main/src/rpc/jsonrpc_request_processing.rs` — NEW (225L)
- `crates/main/src/rpc/mod.rs` — added module
- `crates/core/core/src/lib.rs` — removed dead aliases
- `crates/core/core/src/ecosystem_coordination.rs` — removed dead code + imports
- `crates/core/core/src/federation/service.rs` — fixed unused import + doc links
- `crates/tools/rule-system/Cargo.toml` — removed dead `watcher` feature + `notify`
- `crates/tools/ai-tools/Cargo.toml` — removed dead `local` feature
- `crates/sdk/Cargo.toml` — removed dead `storage`/`web` features
- `docs/CRYPTO_MIGRATION.md` — corrected crypto table
- `crates/main/tests/error_path_coverage.rs` — DELETED
- `crates/main/tests/service_discovery_critical_paths.rs` — DELETED
- `crates/core/mcp/tests/error_path_coverage.rs` — DELETED
- `CHANGELOG.md`, `CURRENT_STATUS.md`, `README.md` — metrics updated
