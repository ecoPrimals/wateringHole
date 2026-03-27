# ToadStool S149 — Deep Debt Execution & Evolution Handoff

**Date**: March 12, 2026
**Session**: S149
**Author**: toadStool team (automated via Cursor agent)
**Status**: 20,192 tests, 0 failures | cargo fmt clean | cargo clippy 0 code warnings | ~86% line coverage

---

## Summary

S149 executed across all remaining debt and evolution gaps identified in S148.
Focus areas: clippy hygiene, credential chain completion, handler refactoring,
dependency cleanup, FFI evolution, and interned constant adoption.

---

## Changes

### Clippy — 0 Code Warnings

- Redundant match guards eliminated (`s if s == "beardog"` → `"beardog"`, const patterns via `|`)
- `map_or(true, ...)` → `is_none_or(...)` (modern idiomatic Rust)
- `Error::new(ErrorKind::Other, e)` → `Error::other(e)`
- Long literal `105000` → `105_000`
- Unused `#[expect]` attribute removed from examples
- `hw-learn` and `nvpmu` Cargo.toml: added `repository`, `readme`, `keywords`, `categories`

### Credential Resolution Fully Wired

- `probe_keyring()`: Reads `$TOADSTOOL_CREDENTIALS` or `$XDG_CONFIG_HOME/toadstool/credentials` (KEY=VALUE format). Enforces 0600 permissions on Unix.
- `probe_security_provider()`: Discovers `crypto` capability socket via `get_socket_path_for_capability("crypto")`, calls `secret.resolve` JSON-RPC via `UnixJsonRpcClient`.
- D-BD-SECRET debt item: **RESOLVED**
- D-KEYRING debt item: Partially resolved (file-based; OS keyring still future)
- 2 new tests: `probe_keyring_reads_credentials_file`, `probe_keyring_rejects_unsafe_permissions`

### Handler Refactoring

- Shader domain (5 handlers + `build_precision_advice`) extracted from `handler/mod.rs` (849→615 lines) to `handler/shader.rs` (248 lines)
- `ShaderHandler` struct with `SharedCoralReefClient`, matching pattern of `HwLearnHandler`, `OllamaHandler`, etc.

### Dependency Cleanup

- Orphaned workspace deps removed: `caps`, `console`, `ipnet`, `futures-util`
- `rust-version` bumped from 1.80 to 1.82

### FFI Evolution

- `nouveau_drm.rs`: Raw `extern "C"` FFI (`open`, `close`) → `rustix::fs::open` + `OwnedFd`
- Minimal `raw_ioctl` retained for DRM opcodes (documented SAFETY)
- `hw-learn` upgraded to `rustix` 1.1

### hw-learn Stubs Implemented

- `RegisterAccess` trait defined in `applicator/mod.rs`, exported from `hw_learn`
- `verify_register_via_access()` uses MMIO for hardware register verification
- `hw_learn_distill` binary updated to match current API
- `RecipeApplicator` wired to optional `&mut dyn RegisterAccess`

### Interned Constants

- `error_formatting.rs`: `"songbird"/"nestgate"/"beardog"` → `primals::SONGBIRD/NESTGATE/BEARDOG`
- `capability_helpers.rs`: Redundant guards → direct const match patterns
- `ecosystem/types.rs`: Same pattern with `|` multi-match

### Script Fixes

- `toadstool-runtime-display` → `toadstool-display` in `run-coverage.sh`, `run-hardware-tests.sh`, `.github/workflows/hardware.yml`

---

## Debt Status After S149

| Item | Status |
|------|--------|
| D-BD-SECRET | **RESOLVED** — `probe_security_provider()` wired |
| D-KEYRING | Partially resolved — file-based done, OS keyring future |
| D-COV | 20,192 tests, ~86% coverage |
| D-SOV | RESOLVED (S94b) |
| D-WC | RESOLVED (S132) |

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all -- --check` | PASS (0 diffs) |
| `cargo clippy --workspace --all-targets` | PASS (0 code warnings) |
| `cargo test --workspace` | PASS (20,192 tests, 0 failures) |
| `cargo build --workspace` | PASS |

---

## Files Modified (Key)

| File | Change |
|------|--------|
| `Cargo.toml` (root) | Removed orphaned deps, bumped rust-version |
| `crates/core/common/src/secret_string.rs` | Wired probe_keyring + probe_security_provider |
| `crates/server/src/pure_jsonrpc/handler/mod.rs` | Extracted shader domain |
| `crates/server/src/pure_jsonrpc/handler/shader.rs` | NEW — shader handlers |
| `crates/core/hw-learn/src/applicator/mod.rs` | RegisterAccess trait |
| `crates/core/hw-learn/src/applicator/nouveau_drm.rs` | FFI → rustix |
| `crates/cli/src/templates/capability_helpers.rs` | Direct const match patterns |
| `crates/cli/src/ecosystem/types.rs` | Direct const match patterns |
| `crates/cli/src/utils/error_formatting.rs` | Interned primal constants |

---

## Spring Pins (unchanged from S147)

| Spring | Pin |
|--------|-----|
| hotSpring | v0.6.30 |
| neuralSpring | V98/S145 |
| coralReef | Iter 35 |
| groundSpring | V100 |
| wetSpring | V109 |
| airSpring | v0.7.5 |
| healthSpring | V19 |
