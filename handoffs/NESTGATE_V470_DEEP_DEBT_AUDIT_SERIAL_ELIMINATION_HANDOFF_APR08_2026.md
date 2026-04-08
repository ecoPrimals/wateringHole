# NestGate V4.7.0 — Deep Debt Audit, Serial Elimination & Dead Code Cleanup

**Date**: April 8, 2026  
**Scope**: Workspace-wide audit and cleanup  
**Previous**: Session 35 (GAP-MATRIX-04 ZFS JSON-RPC/UDS bridge)

---

## Summary

Comprehensive deep debt audit of the entire NestGate workspace. Executed targeted
cleanup on the actionable items found. The codebase is in excellent shape — most
audit categories returned clean.

## Changes

### #[serial] elimination (last one)
- `setup_logging()` in `nestgate-bin/src/cli/runtime.rs` evolved from `.init()` to
  `.try_init()`, making it safe for concurrent test execution
- Removed `#[serial]` attribute and `serial_test` import from `cli/tests.rs`
- Removed `serial_test` dev-dependency from `nestgate-bin/Cargo.toml`
- **Zero `#[serial]` tests remain** in the entire workspace

### Dead code removal
- Removed `gather_socket_search_dirs()` in `nestgate-rpc` isomorphic_ipc/atomic/discovery.rs
  — was defined but never called, suppressed with `#[allow(dead_code)]`
- **Zero `#[allow(dead_code)]` in production** code now

### Deprecated constant cleanup
- Removed 4 deprecated URL constants with zero callers:
  - `DEFAULT_API_BASE_URL` (`"http://localhost:8080"`)
  - `DEFAULT_WEBSOCKET_URL` (`"ws://localhost:8080/ws"`)
  - `DEFAULT_METRICS_URL` (`"http://localhost:9090"`)
  - `DEFAULT_WEB_UI_URL` (`"http://localhost:3000"`)
- Env-driven functions (`default_api_base_url()`, etc.) are the canonical replacements
- Deprecated markers: 188 → 181

### Root documentation alignment
- README.md, STATUS.md, CHANGELOG.md updated to April 8, 2026
- Test counts: ~11,842 passing, 461 ignored, 0 failures
- Serial tests: updated from "1" to "0"
- IPC routes: added `zfs.*` to semantic naming compliance list

## Comprehensive Audit Findings (all clean)

| Category | Status |
|----------|--------|
| Unsafe code | Zero — `#![forbid(unsafe_code)]` on all 22 crates |
| Production `.unwrap()` | Zero — all unwraps are in `#[cfg(test)]` modules |
| `#[allow(clippy::*)]` in production | Zero |
| `thread::sleep` / `block_on` in production | Zero |
| Clippy warnings | Zero (workspace-wide) |
| `todo!()` / `unimplemented!()` in production | Zero (only in doc examples) |
| `FIXME` / `HACK` | Zero |
| Production files over 800 lines | Zero (max ~758 lines) |
| Hardcoded primal names | Zero (self-knowledge only) |
| `.bak` / `.old` / `.orig` / `.tmp` files | Zero |
| Hot-path `.clone()` | All verified necessary (ownership transfer or one-time init) |
| `curl` in installer | Intentional bootstrap design (avoids reqwest deps for standalone binary) |
| Production placeholders (501s) | Intentional security boundaries for destructive HTTP ops |

## Files Changed

- `code/crates/nestgate-bin/Cargo.toml` — removed `serial_test` dev-dep
- `code/crates/nestgate-bin/src/cli/runtime.rs` — `.init()` → `.try_init()`
- `code/crates/nestgate-bin/src/cli/tests.rs` — removed `#[serial]` and import
- `code/crates/nestgate-config/src/constants/canonical_defaults.rs` — removed 4 deprecated constants
- `code/crates/nestgate-rpc/src/rpc/isomorphic_ipc/atomic/discovery.rs` — removed dead function
- `README.md`, `STATUS.md`, `CHANGELOG.md` — metrics and date alignment

## Verification

```
cargo fmt --all                                              — clean
cargo clippy --workspace --all-features -- -D warnings       — 0 warnings
cargo test --workspace --all-features                        — 11,842 passed, 0 failed, 461 ignored
```

## Commit

`321b068e` — `refactor: deep debt cleanup — eliminate #[serial], dead code, deprecated constants`
