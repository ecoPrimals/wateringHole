# biomeOS v2.58 — Deep Resilience, Test Extraction, and Flaky Test Hardening

**Date**: March 20, 2026
**From**: biomeOS deep resilience session
**Version**: v2.57 → v2.58

---

## Executive Summary

Continuation of deep audit execution. Fixed 3 classes of flaky tests (TOCTOU socket
discovery, missing socket directory creation, env var races), extracted 4 large inline
test modules into separate files (saving ~2,100 LOC from production modules), and
confirmed library coverage exceeds 90% target. All quality gates pass.

---

## Quality Gates (all passing)

| Gate | Status |
|------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --workspace --all-targets -- -D warnings` | PASS (0 warnings) |
| `cargo test --workspace` | PASS (6,869 tests, 0 failures) |
| `cargo llvm-cov --workspace` | 88.82% overall / 90.54% library (binary entrypoints account for gap) |

---

## Bugs Fixed

### 1. TOCTOU in Federation Socket Discovery

`biomeos-federation/src/discovery/mod.rs` — `discover_unix_sockets()` called
`socket_dir.exists()` then `tokio::fs::read_dir()`, but the directory could vanish
between the two calls (or have restrictive permissions under llvm-cov instrumentation).
The `read_dir` failure was a hard error propagated via `?`, killing the entire discovery
chain. Fixed: made `read_dir` failure non-fatal (warn + return Ok), matching the
existing directory-not-found behavior.

### 2. SocketNucleation Missing Parent Directory

`biomeos-atomic-deploy/src/nucleation.rs` — `family_deterministic_path()` returned a
socket path without ensuring its parent directory existed. The `xdg_runtime_path()`
strategy did create dirs, but `family_deterministic_path()` didn't. Fixed: added
`create_dir_all` in `assign_socket()` (strategy-agnostic), ensuring the parent
directory always exists before returning the path.

### 3. Fossil Test Env Var Race

`biomeos-cli/src/commands/fossil/tests.rs` — 10 tests using `TestEnvGuard` to set
`BIOMEOS_CLI_LOG_ROOT` were running concurrently, causing intermittent failures when
tests read each other's env var state. Fixed: added `#[serial_test::serial]` to all
10 affected tests.

---

## Smart Refactoring — Test Extraction

Extracted inline `#[cfg(test)] mod tests` blocks to dedicated files using Rust 2024
submodule conventions (`foo.rs` → `foo/tests.rs`):

| File | Before | After | Extracted |
|------|--------|-------|-----------|
| `capabilities.rs` (primal-sdk) | 946 | 377 | 579 lines |
| `handlers/discovery.rs` (api) | 908 | 293 | 617 lines |
| `vm_federation.rs` (core) | 929 | 470 | 462 lines |
| `universal_biomeos_manager/discovery.rs` (core) | 923 | 462 | 468 lines |

Total: **2,126 lines** moved out of production modules into dedicated test files.

---

## Coverage Analysis

| Metric | Value |
|--------|-------|
| Overall line coverage | 88.82% (104,150 total lines) |
| Library-only coverage | **90.54%** (102,135 lines, excl binary entrypoints) |
| Function coverage | 90.06% |
| Tests passing | 6,869 |
| Tests failing | 0 |
| Tests ignored | 136 |

The gap between library (90.54%) and overall (88.82%) is entirely binary entrypoints
(`tower.rs`, `main.rs`, `init.rs`, `biomeos-deploy.rs`, `verify-lineage.rs`,
`neural-deploy.rs`) — `fn main()` wrappers that are tested via integration/e2e tests,
not unit tests.

---

## Files Over 1000 LOC

| File | Lines | Type |
|------|-------|------|
| `fossil/tests.rs` | 1,006 | Test file (acceptable) |

Zero production files over 1000 LOC.

---

## Debris Identified

- **`crates/neural-api-client/`** — 1,202 lines, used by `biomeos-api` as path dep
  but NOT listed in workspace `members`. Gets compiled but not tested/linted by
  `cargo test --workspace` or `cargo clippy --workspace`. Should be added to workspace
  or consolidated with `neural-api-client-sync`.

---

## What's Next

1. Add `neural-api-client` to workspace members (or consolidate with sync variant)
2. Split `socket_discovery/engine.rs` (916 LOC, all impl, 0 tests inline) into
   concern-based impl files
3. Split `service/networking.rs` (904 LOC) type definitions into submodules
4. Evolve binary entrypoints to extract logic into testable library functions
5. Push overall coverage past 90% by testing extracted binary logic
6. Continue ecosystem absorption from wateringHole standards

---

## Session Artifacts

All changes in `master` branch. Root docs updated (README.md, CURRENT_STATUS.md,
DOCUMENTATION.md). CHANGELOG.md entry pending commit message.
