# NestGate v4.7.0-dev — Session 61: Deep Debt Hygiene

**Date**: May 11, 2026  
**Commit**: `34d26438` (code), this handoff documents the doc update commit as well  
**Scope**: Dependency hygiene, clippy doc completeness, hardcode elimination  
**Blocking**: Nothing — incremental quality sweep  

---

## Problem

Post-Session 60 (content.* transport parity), a comprehensive deep debt sweep
identified three categories of remaining debt:

1. **Unused dependencies** in `nestgate-api`: `toml`, `async-stream`, `sha2` declared
   but never imported; `fastrand` used only in test code but listed as production dep.
2. **Missing trait documentation**: 16 methods on `NativeAsyncUniversalZfsService` in
   `nestgate-api/handlers/zfs/native_async/traits.rs` lacked doc comments, producing
   clippy `missing_docs` warnings.
3. **Duplicated hardcoded literal**: `"biomeos"` socket-dir fallback in `btsp_client.rs`
   duplicated the canonical constant in `nestgate-config::constants::system`.

## Solution

### Dependency cleanup (`nestgate-api/Cargo.toml`)

- Removed `toml`, `async-stream`, `sha2` from `[dependencies]` (zero usage in source).
- Moved `fastrand` from `[dependencies]` to `[dev-dependencies]` (used only in
  `tests/fault_injection_tests.rs`).

### Clippy doc completeness (`native_async/traits.rs`)

- Added doc comments for all 16 undocumented trait methods on
  `NativeAsyncUniversalZfsService` (health, metrics, pool, dataset, snapshot, clone ops).

### Hardcode elimination (`btsp_client.rs`)

- Replaced inline `"biomeos".to_string()` fallback with
  `nestgate_config::constants::system::ecosystem_path_segment()` — delegates to the
  canonical env-var chain (`ECOSYSTEM_NAME` → `BIOMEOS_SERVICE_NAME` → `"biomeos"`).

## Files Changed

| File | Change |
|------|--------|
| `code/crates/nestgate-api/Cargo.toml` | Remove 3 unused deps, move fastrand to dev-deps |
| `code/crates/nestgate-api/src/handlers/zfs/native_async/traits.rs` | Add 16 doc comments |
| `code/crates/nestgate-rpc/src/rpc/btsp_client.rs` | Delegate to `ecosystem_path_segment()` |
| `Cargo.lock` | Lockfile updated (fewer direct deps) |
| `CHANGELOG.md` | Session 61 entry |

## Verification

```
cargo check --workspace                                — PASS (0 errors)
cargo clippy --workspace --all-features -- -D warnings — PASS (0 warnings)
cargo fmt --all -- --check                             — PASS
cargo test --workspace --lib                           — 8,915 passing, 0 failures
cargo test --workspace                                 — 12,389 passing, 0 failures
```

## Comprehensive Sweep Results

The full sweep confirmed NestGate's debt posture:

| Dimension | Status |
|-----------|--------|
| Files > 800 lines | Zero (largest ~787) |
| `unsafe` code | Zero; `#![forbid(unsafe_code)]` all 20 crate roots |
| ring / openssl / native-tls | Eliminated; pure Rust crypto |
| TODO / FIXME / HACK | Zero in production |
| Commented-out code | Zero |
| Mocks in production | Zero (NoopStorage is null-object, not mock) |
| Other-primal coupling | Zero (only env-var backward compat names) |
| Unused deps | Cleaned this session |

## Documentation

All 8 root docs updated to Session 61 references and current test counts
(8,915 lib / 12,389 full workspace).
