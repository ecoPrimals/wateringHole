<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.27 — Deep Debt Evolution Handoff

**Date**: April 1, 2026
**Primal**: Squirrel (AI / MCP)
**From**: Deep debt resolution, test concurrency, module refactoring session
**Status**: GREEN — 6,852 tests, 0 failures, clippy clean, fmt clean, doc clean

---

## Summary

Continuation of deep debt resolution. Three areas: (1) test quality — eliminated all
`#[serial]` annotations and `sleep()`-based synchronization, (2) module structure — smart
refactoring of files approaching 1000 lines, (3) production stubs — CLI status evolved from
hardcoded mock values to real system metrics.

## Test Concurrency Evolution

| Metric | Before | After |
|--------|--------|-------|
| `#[serial]` annotations | 22 | 0 |
| `sleep()` in tests | ~50 | 0 (non-chaos) |
| Test count | 6,839 | 6,852 |
| Failures | 0 | 0 |

### Sleep Replacement Patterns

- **Server bind before spawn**: Moved `UnixListener::bind` out of `tokio::spawn` in IPC tests
  (6 sleeps removed in `cross_primal_ipc_tests.rs`)
- **Polling helpers with `yield_now()`**: `await_workflow_done`, `await_all_workflows_done`,
  `await_transport_running`, `await_connections` (32 sleeps replaced across workflow/transport tests)
- **Paused time**: `#[tokio::test(start_paused = true)]` + `tokio::time::advance()` for
  `test_connection_idle_timeout` (replaced 2-second real sleep)
- **Removed unnecessary waits**: TCP/Unix listeners are ready immediately after bind
  (12 sleeps removed in client/JWT tests)
- **`tempfile::TempDir`**: Replaced hardcoded `/tmp` socket paths to prevent parallel collisions

### Serial Removal

All 22 `#[serial]` removed. Justification: `temp_env::with_vars` already acquires an internal
process-wide mutex, making `#[serial]` redundant for env-var isolation.

## Module Refactoring

| File | Before | After | Method |
|------|--------|-------|--------|
| `federation/service.rs` | 973 lines | 819 lines | Tests extracted to `service_tests.rs` via `#[path]` |
| `sdk/infrastructure/config.rs` | 943 lines | 610 lines | Plugin types extracted to `plugin_config.rs` |

No production files over 1000 lines remain.

## CLI Status Evolution

Replaced hardcoded stubs (`"Memory usage: 42MB"`, `"Uptime: 123 seconds"`) with:
- Real PID via `std::process::id()`
- Real RSS from `/proc/self/status` (Linux)
- Environment from `$SQUIRREL_ENV`
- Socket path probed from `$SQUIRREL_SOCKET` / `$XDG_RUNTIME_DIR` / fallback
- New `crates/tools/cli/src/status.rs` module

## Lint Debt Cleanup

- `"".to_string()` → `String::new()` / `unwrap_or_default()` in SDK
- Removed satisfied `clippy::manual_string_new` lint expectation
- Fixed `clippy::or_fun_call` in CLI output

## Docs Sync

- README.md: 7,143 → 6,852 tests
- CONTEXT.md: 7,143 → 6,852 tests, 452k → 453k lines, 1,334 → 1,355 files
- CURRENT_STATUS.md: 6,839 → 6,852 tests, version → alpha.27

## Debris Cleanup

- Moved `specs/HANDOFF_ABSORPTION_ANALYSIS_MAR18_2026.md` → fossilRecord
- Moved `specs/UNIVERSAL_PATTERNS_IMPLEMENTATION_SUMMARY_HISTORICAL.md` → fossilRecord
- Verified `.env` and `mcp-config.env` are gitignored (not tracked, API keys safe)

## CI Gate

```
cargo fmt --all -- --check     ✓
cargo clippy --all-targets --all-features -- -D warnings   ✓ (0 warnings)
cargo test --workspace         ✓ (6,852 passed, 0 failed, 107 ignored)
cargo doc --workspace --no-deps   ✓
```

## Files Changed

| Area | Files |
|------|-------|
| Test concurrency | 8 test files (removed serial + sleeps) |
| Module refactoring | 4 new/modified files (service_tests.rs, plugin_config.rs, mod.rs updates) |
| CLI status | 3 files (main.rs, status.rs, lib.rs) |
| Lint cleanup | 2 files (sdk lib.rs, http.rs) |
| Docs | 3 files (README, CONTEXT, CURRENT_STATUS) |

## Next Session Candidates

- Coverage push toward 90% target (currently ~86.5%)
- `deprecated-adapters` feature gate cleanup (v0.3.0 removal planned)
- `EcosystemPrimalType` deprecated type removal
- Session.rs refactoring (934 lines, in `enhanced/` module)
