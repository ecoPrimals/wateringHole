# biomeOS v3.34 — Deep Debt: Hardcoding Elimination + Lint Hygiene

**Date**: April 30, 2026
**From**: biomeOS team
**To**: All downstream springs and primals
**Status**: Committed and pushed

---

## Summary

v3.34 eliminates the last hardcoded filesystem paths in production code and brings all `#[allow]` attributes into compliance with the `reason` annotation standard used by `#[expect]` throughout the codebase.

## Changes

### Hardcoded path elimination (7 files)

| File | Before | After |
|------|--------|-------|
| `biomeos/src/modes/cli.rs` | `"/tmp"` socket scan fallback | `DEFAULT_SOCKET_DIR` |
| `biomeos-graph/src/executor/node_handlers.rs` | `"/tmp"` socket resolution fallback | `DEFAULT_SOCKET_DIR` |
| `biomeos-core/src/deployment_mode.rs` | `"/run/user/{uid}/biomeos"` | `LINUX_RUNTIME_DIR_PREFIX` constant |
| `biomeos-atomic-deploy/src/orchestrator.rs` | `"/run/user/{uid}"` | `LINUX_RUNTIME_DIR_PREFIX` constant |
| `biomeos-nucleus/src/client/family_seed.rs` | `"/run/user/{uid}/biomeos/family.seed"` | `LINUX_RUNTIME_DIR_PREFIX` constant |
| `biomeos-ui/src/device_management_server/mod.rs` | `"/run/user/{uid}/biomeos-..."` | `LINUX_RUNTIME_DIR_PREFIX` constant |
| `biomeos-atomic-deploy/src/primal_coordinator.rs` | `"/run/user/$(id -u)/..."` shell hint | `LINUX_RUNTIME_DIR_PREFIX` constant |

**Result**: Zero hardcoded filesystem paths remain in production code outside the canonical constants modules (`defaults.rs`, `constants/mod.rs`, `path_builder.rs`).

### Lint hygiene: #[allow] reason annotations (8 files)

- `biomeos-test-utils/src/lib.rs` — `#![allow(..., reason = "test-only crate")]`
- 7 crate roots (`biomeos`, `biomeos-atomic-deploy`, `biomeos-deploy`, `biomeos-api`, `biomeos-spore`, `biomeos-ui`, `biomeos-cli`) — `#![cfg_attr(test, allow(..., reason = "tests use unwrap/expect for concise assertions"))]`

## Verification

- `cargo check` — PASS
- `cargo clippy -- -D warnings` — PASS (0 warnings)
- `cargo fmt --check` — PASS
- `cargo test --workspace` — 8,064+ tests, pre-existing env-dependent failures only

## No action required by downstream

These changes are internal to biomeOS. No API, wire format, or behavioral changes.

---

*biomeOS v3.34 | AGPL-3.0-or-later | ecoPrimals Project*
