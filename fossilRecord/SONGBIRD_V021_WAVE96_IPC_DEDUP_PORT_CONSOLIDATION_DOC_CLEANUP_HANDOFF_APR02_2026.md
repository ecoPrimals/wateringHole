# Songbird v0.2.1 — Wave 96 Deep Debt: IPC Dedup, Port Consolidation, Doc Cleanup

**Date**: April 2, 2026  
**Version**: v0.2.1  
**Session**: 36 (Wave 96)  
**Previous**: `SONGBIRD_V021_WAVE93_RING_SLED_CONCURRENCY_HANDOFF_APR02_2026.md`

---

## Summary

Smart refactoring of duplicated IPC connection handlers into a transport-agnostic generic, consolidation of duplicate port sources into `primal_scan_ports()`, evolution of config templates from hardcoded to runtime defaults, production stub evolution to capability-aware logging, stale comment cleanup, root doc refresh, and `deny.toml` hygiene.

---

## What Changed

### IPC Handler Deduplication (Smart Refactoring)

- Extracted `handle_json_rpc_connection<S: AsyncRead + AsyncWrite>()` — transport-agnostic JSON-RPC 2.0 dispatch
- `start_ipc_server` (Unix) and `start_tcp_ipc_server` (TCP) now both delegate to the single generic
- Extracted `create_shared_handler()` and `log_available_methods()` helpers
- Net reduction: ~120 lines of duplicated dispatch logic eliminated

### Hardcoding Evolution

- **Config templates**: Both `init_config` functions (`bin_interface/config.rs` + `commands/config.rs`) now generate templates from `songbird_config::defaults::ports::orchestrator_port()` and `defaults::hosts::default_host()` instead of literal `8080`/`0.0.0.0`
- **Doctor command**: Port check uses `orchestrator_port()` instead of literal `8080`
- **Help text**: All `SONGBIRD_PORT (default: ...)` messages dynamically display the actual env-driven default
- **BearDog socket paths**: Removed hardcoded `/tmp/beardog-default-default.sock` and `/tmp/songbird-http-gateway.sock` from templates; capability discovery at runtime
- **Scan port consolidation**: Added `ports::primal_scan_ports()` aggregation function; `PrimalRegistry` discovery now uses it instead of hardcoded `vec![8080, 8081, 8082, 8083, 8443, 3000, 5000]`

### Production Stub Evolution

- `UniversalSecurityManager`: Methods now log BearDog delegation intent instead of silent `Ok(())`
- `UniversalAccessManager`: `one_click_setup` logs capability discovery; `auto_detect_user_skill` reads `SONGBIRD_VERBOSE` env
- `convenience` module: All functions log orchestrator endpoint discovery and BearDog delegation paths

### deny.toml Hygiene

- Pruned 2 stale `skip` entries (`parking_lot`, `parking_lot_core` — no longer have duplicate versions)
- Remaining warning: `ring`/`rustls` wrapper (expected — ring not in default build)

### Stale Comment Cleanup

- Removed `// Temporarily disabled` import comment in `universal.rs`
- Removed dead `// pub use constants::cli; // Temporarily disabled` in `cli/core/mod.rs`
- Removed `// actual command execution will be implemented` from `cli/types.rs`

### Root Docs Refresh

- `README.md`: Updated test count (12,124), coverage (~72%), lines (~410,685), suite time (~60s)
- `CONTEXT.md`: Same test/coverage updates
- `REMAINING_WORK.md`: Updated audit date, Wave 96 header, metrics, dependency info, JSON-RPC dispatch description

---

## Verification

| Check | Result |
|-------|--------|
| `cargo clippy --workspace` | 0 warnings |
| `cargo test --workspace` | 12,124 passed, 0 failed, 269 ignored |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| `cargo check --workspace` | Clean (0 errors, 0 warnings) |

---

## Unsafe Code Audit

**ZERO** `unsafe` blocks, `unsafe fn`, or `unsafe impl` in production code across all 30 crates. All hits in source are either `// No unsafe impl needed!` comments or `#![forbid(unsafe_code)]` declarations.

---

## Files Modified

- `crates/songbird-orchestrator/src/bin_interface/server.rs` — IPC handler dedup
- `crates/songbird-orchestrator/src/bin_interface/config.rs` — Config template + help text
- `crates/songbird-orchestrator/src/commands/config.rs` — Config template + help text
- `crates/songbird-orchestrator/src/commands/doctor.rs` — Port check
- `crates/songbird-config/src/defaults/ports.rs` — `primal_scan_ports()` function
- `crates/songbird-config/src/config/universal_primals.rs` — Use `primal_scan_ports()`
- `crates/songbird-cli/src/cli/commands/universal.rs` — Stub evolution + comment cleanup
- `crates/songbird-cli/src/cli/core/mod.rs` — Stale comment removal
- `crates/songbird-cli/src/cli/types.rs` — Stale comment removal
- `deny.toml` — Pruned stale skip entries
- `README.md`, `CONTEXT.md`, `REMAINING_WORK.md` — Doc refresh

---

## Next Steps

1. **SB-03**: NestGate IPC migration (blocked on NG-01 `storage.*` methods)
2. **serde_yaml → yaml_serde**: Successor crate available (January 2026, YAML org maintained); migration when convenient
3. **async-trait**: 136 usages verified as dyn-dispatch; blocked on Rust language stabilization
4. **Coverage**: ~72% → 90% target; all 30 crates have inline tests, 9 flagged "no-test-file" crates verified to have inline modules (186 tests in quic, 70 in sovereign-onion, etc.)
