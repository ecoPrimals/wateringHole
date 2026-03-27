<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# rhizoCrypt v0.13.0-dev — Deep Audit & Idiomatic Rust Handoff

**Date**: March 16, 2026 (session 12)
**Primal**: rhizoCrypt v0.13.0-dev
**Status**: Production Ready

---

## Summary

Comprehensive codebase audit focused on deep debt resolution: migrated all test
`#[allow]` attributes to precise `#[expect]` (42 files), replaced all `as` casts
with safe `TryFrom` conversions (10 files), evolved `SignResponse.signature` to
zero-copy `bytes::Bytes`, refactored overlimit test file with domain-based split,
and synced `rustfmt.toml` edition to 2024.

---

## Changes

### 1. `#[allow]` → `#[expect]` Migration (42 test modules)
- All `#[allow(clippy::unwrap_used, clippy::expect_used)]` replaced with precise `#[expect(...)]`
- Each module now only suppresses lints it actually triggers — unfulfilled `#[expect]` is a build error
- Modules using neither `unwrap()` nor `expect()` had the attribute removed entirely
- Audit-trail `reason = "test code"` on every suppression

### 2. Safe Type Conversions (10 files)
- All `as` casts replaced with `TryFrom`/`TryInto` + saturating fallback
- `binary_integration.rs`: `child.id() as i32` → `i32::try_from(...)` with `#![allow(cast_possible_wrap)]` removed
- `service.rs`: limit/session count casts → `TryFrom` with `unwrap_or(MAX)`
- `store_redb.rs`, `store_sled.rs`, `types.rs`, `dehydration.rs`: `len() as u64` → `u64::try_from(...)`
- `loamspine_http.rs`: enum `as u8` → typed `to_u8()` method

### 3. Zero-Copy: `SignResponse.signature`
- `signing.rs` `SignResponse.signature` evolved from `Vec<u8>` to `bytes::Bytes`
- Eliminates intermediate allocation in signing response path

### 4. Smart File Refactoring
- `store_redb_tests_advanced.rs` (1001 lines, 1 over limit) → domain-based split:
  - `store_redb_tests_advanced.rs`: 681 lines (core advanced tests)
  - `store_redb_tests_stats.rs`: 324 lines (stats and metrics tests)

### 5. Configuration Sync
- `rustfmt.toml`: `edition = "2021"` → `edition = "2024"` (matches workspace Cargo.toml)
- `docs/ENV_VARS.md`: documented `CARGO_TARGET_DIR` for noexec mount workaround

### 6. Root Documentation
- README: coverage 91.47% → 91.63%, SPDX count 110 → 107
- CHANGELOG: added session 12 entry
- DEPLOYMENT_CHECKLIST: updated metrics and session reference

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy` (pedantic + nursery + cargo, all features) | Clean (0 warnings) |
| `cargo doc --workspace --all-features --no-deps` | Clean |
| `cargo test --workspace --all-features` | 1188 pass, 0 fail |
| `cargo deny check` | Clean |
| `unsafe_code = "deny"` | Workspace-wide (zero unsafe in tests via temp-env) |
| `unwrap_used`/`expect_used` | `"deny"` workspace-wide |
| Coverage gate | 91.63% lines (`--fail-under-lines 90` CI enforced) |
| SPDX headers | All 107 `.rs` files |
| Max file size | All under 1000 lines |
| Production unwrap/expect | Zero |

---

## Codebase Health

| Metric | Value |
|--------|-------|
| Tests | 1188 (all features) |
| Coverage | 91.63% line (llvm-cov) |
| `.rs` files | 107 workspace |
| Crates | 3 (rhizo-crypt-core, rhizo-crypt-rpc, rhizocrypt-service) |
| Edition | 2024 (rust-version 1.87) |
| TODOs/FIXMEs in source | 0 |
| `#[allow]` in test code | 0 (all migrated to `#[expect]`) |
| `as` casts in production | 0 (all migrated to `TryFrom`) |

---

## Remaining Debt (for future sessions)

- `unix_socket.rs` `http_post`/`parse_http_response` return `Vec<u8>` not `bytes::Bytes` (low-level transport boundary)
- Evolve flaky `test_stats_after_operations` in sled tests (sled `size_on_disk()` non-deterministic)
- `provenance-trio-types` advisory tracking (transitive from tarpc)
- tarpc ops count inconsistency: README says "24 ops", capability_registry has 23 methods
- Coverage gaps in `store_redb.rs` error paths (require database corruption to trigger)
- Coverage gaps in `tarpc.rs`/`signing.rs`/`permanent.rs` success paths (require live servers)
