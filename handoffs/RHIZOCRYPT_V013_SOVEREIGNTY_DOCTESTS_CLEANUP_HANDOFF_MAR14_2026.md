<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# rhizoCrypt v0.13.0-dev — Sovereignty Cleanup, Doc Tests, Capability-Based Errors

**Date**: March 14, 2026 (session 4)
**Primal**: rhizoCrypt
**Version**: 0.13.0-dev
**Type**: Sovereignty evolution + documentation debt + coverage expansion

---

## Summary

Final sovereignty cleanup and documentation debt pass. Removed all
primal-specific error variants and deprecated trait aliases. Rewrote all
26 ignored doc tests to compile against the current API. Applied JSON-RPC
zero-copy optimization. Updated root docs, crate README, and cleaned
vendor-specific references from code and comments.

1. **1075 tests passing** (was 1022) — +53 new tests across error, store,
   and RPC modules.

2. **91.02% line coverage** (llvm-cov) — up from 90.12%. 87.61% function,
   92.38% region.

3. **30 doc tests passing, 0 ignored** — all 26 previously-ignored doc
   examples rewritten to match current API (was 4 passing, 26 ignored).

4. **Sovereignty: capability-based errors** — removed `BearDog(String)`,
   `LoamSpine(String)`, `NestGate(String)` error variants. Added
   `CapabilityProvider { capability, message }` for structured,
   vendor-agnostic error reporting.

5. **Removed deprecated trait aliases** — `BearDogClient`, `LoamSpineClient`,
   `NestGateClient` removed. All integration now uses `SigningProvider`,
   `PermanentStorageProvider`, `PayloadStorageProvider`.

6. **JSON-RPC zero-copy** — `serde_json::from_slice(&body)` replaces
   two-step `from_utf8` + `from_str`, combining UTF-8 validation and JSON
   parsing in one pass.

7. **Root docs & crate README modernized** — removed RocksDB, BearDogClient,
   and vendor-specific references. Updated metrics, feature flags, and
   module table.

---

## Changes

### Sovereignty: Error Types

| Before | After |
|--------|-------|
| `BearDog(String)` | Removed |
| `LoamSpine(String)` | Removed |
| `NestGate(String)` | Removed |
| (no equivalent) | `CapabilityProvider { capability, message }` |

`is_recoverable()` now covers `Integration` and `CapabilityProvider`.
Helper: `RhizoCryptError::capability_provider("signing", "key not found")`.

### Sovereignty: Deprecated Traits Removed

| Removed | Replacement |
|---------|-------------|
| `BearDogClient` | `SigningProvider` |
| `LoamSpineClient` | `PermanentStorageProvider` |
| `NestGateClient` | `PayloadStorageProvider` |

### Doc Tests Rewritten (26)

All doc examples updated to current API signatures. Changes include:
- Async runtime wrappers (`tokio::runtime::Runtime::new()`)
- Registry setup with `ServiceEndpoint` for discovery
- Correct client constructors (`SigningClient::discover`, `PermanentStorageClient::discover`)
- Correct method names (`call_json` not `call`, `new` not `connect`)

### Coverage Expansion

| File | Change |
|------|--------|
| `error.rs` | `CapabilityProvider` tests (construction, display, recoverability) |
| `store_redb_tests_advanced.rs` | `parse_vertex_set` edge cases, `Clone`, `StorageStats` debug |
| `songbird_rpc.rs` | Function coverage 52% → 96% |

### JSON-RPC Optimization

`handle_jsonrpc()`: Removed intermediate `&str` by using `from_slice`
directly on the `Bytes` body. One allocation eliminated per request.

### Documentation

- `README.md`: 1075 tests, 91.02% coverage, `client` subcommand, doc test metric
- `rhizo-crypt-core/README.md`: Full rewrite — redb/sled (not RocksDB), capability clients (not BearDogClient), updated feature flags and module table
- `CHANGELOG.md`: Session 4 entry
- `ClientFactory` doc comments: removed primal-name parentheticals
- `capabilities/mod.rs`: removed `BearDogClient` anti-pattern reference

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace --all-features --all-targets -- -D warnings` | Clean |
| `cargo doc --workspace --all-features --no-deps` | Clean (0 warnings) |
| `cargo test --workspace --all-features` | 1075 pass, 0 fail |
| `cargo test --doc --workspace --all-features` | 30 pass, 0 ignored |
| `cargo llvm-cov --all-features` | 91.02% lines, 92.38% regions |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| `#![forbid(unsafe_code)]` | Workspace-wide |
| SPDX headers | All `.rs` files |
| Max file size | All under 1000 lines |
| Production TODOs | 0 |
| Production unwrap/expect | 0 |

---

## Remaining Work

1. **Coverage headroom** — 91.02% achieved; remaining gaps:
   - `store_redb.rs` (67%) — internal DB error paths require fault injection
   - `handler.rs` (86%) — some JSON-RPC edge cases
   - `provenance/client.rs` (84%) — mock-only coverage paths

2. **Legacy env var fallbacks** — `BEARDOG_ADDRESS`, `NESTGATE_ADDRESS`,
   `LOAMSPINE_ADDRESS` still supported with deprecation warnings in
   `capability.rs`. Good practice for migration; remove in v1.0.

3. **CI coverage gate** — `cargo-llvm-cov` should be installed in CI
   workflow with 90% enforcement.

4. **Showcase cleanup** — `01-inter-primal-live/05-complete-workflows/`
   README references scripts that don't exist.

---

## Dependency Status

Default build (redb, no http-clients) is 100% Pure Rust (ecoBin compliant).
C deps (`ring` via rustls, `libc` via sled) are properly gated behind
optional features (`http-clients`, `sled`) with documentation.

---

## Handoff Context

Previous sessions:
- Session 1 (Mar 12): wateringHole standards, UniBin, capability discovery
- Session 2 (Mar 13): Deep debt, 862 tests, cargo-deny, service lib extraction
- Session 3 (Mar 14): 90% coverage, platform-agnostic transport, doctor subcommand
- Session 4 (Mar 14): This session — sovereignty, doc tests, 91% coverage

The codebase has zero primal-specific references in error types, traits,
or production code paths. All integration is capability-based with runtime
discovery. Next evolution targets: CI coverage gate, showcase cleanup,
and fault-injection testing for store_redb error paths.
