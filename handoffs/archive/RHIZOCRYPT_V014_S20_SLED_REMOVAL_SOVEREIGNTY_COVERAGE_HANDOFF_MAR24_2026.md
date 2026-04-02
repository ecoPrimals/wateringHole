# rhizoCrypt v0.14.0-dev — Session 20 Handoff

**Date**: March 24, 2026
**Scope**: Sled removal, sovereignty (legacy env var elimination), async manifest discovery, Arc::clone enforcement, coverage push, docs refresh

---

## Changes Delivered

### 1. Sled Backend Removal (ecoBin Compliance)

- Deleted `store_sled.rs`, `store_sled_tests.rs`, `store_sled_tests_advanced.rs`
- Removed `StorageBackend::Sled` variant, `sled` feature flag, sled constants
- Storage is now `DagBackend::Memory` + `DagBackend::Redb` — both 100% Pure Rust
- Zero C dependencies in default or optional features

### 2. Sovereignty — Legacy Vendor Env Vars Removed

- Removed `BEARDOG_ADDRESS`, `NESTGATE_ADDRESS`, `LOAMSPINE_ADDRESS` fallback branches from `safe_env/capability.rs`
- All capability resolution is purely capability-based: `SIGNING_ENDPOINT`, `PERMANENT_STORAGE_ENDPOINT`, etc.
- Primal code has only self-knowledge; discovers other primals at runtime via capability env vars or Songbird
- No vendor names in production code paths

### 3. Async Manifest Discovery

- `scan_manifests`, `publish_manifest`, `unpublish_manifest`, `discover_by_capability` converted from sync to async (`tokio::fs`)
- Tests refactored to `#[tokio::test]` + `tempfile` — no `block_on` nesting, no `unsafe { std::env::set_var }`
- Maintains `forbid(unsafe_code)` compliance

### 4. Explicit `Arc::clone` in JSON-RPC Handler

- All 24 `server.clone().method().await` patterns → explicit `Arc::clone(&server.primal)` construction
- `RhizoCryptRpcServer` fields `primal` and `start_time` made `pub(crate)` for handler access

### 5. Coverage Push

- ~37 new tests across `rhizocrypt.rs`, `store.rs`, `transport.rs`
- Covers error paths, lifecycle edge cases, GC sweep, redb backend, DAG traversal, platform branches
- Total: 94.65% line coverage (CI gate: 90%)

### 6. Documentation Refresh

- All root docs, specs, and crate READMEs updated to reflect sled removal and sovereignty changes
- ENV_VARS.md: legacy vendor env var section replaced with "Removed" notice
- STORAGE_BACKENDS spec: sled section removed, config examples updated to `DagBackend` enum

---

## Current State

| Metric | Value |
|--------|-------|
| Tests | 1,387 passing (`--all-features`) |
| Coverage | 94.65% line coverage |
| Clippy | 0 warnings (pedantic + nursery + cargo + cast lints) |
| Doc | 0 warnings (`-D warnings`) |
| Fmt | Clean |
| Source files | 125 `.rs`, ~44,200 lines |
| Max file | 867 lines (limit: 1000) |
| Unsafe | `deny` workspace-wide, zero `unsafe` blocks |
| C deps (default) | Zero (ecoBin compliant) |
| License | scyBorg Triple-Copyleft (AGPL-3.0+ / ORC / CC-BY-SA 4.0) |
| IPC Methods | 27 methods, 8 domains (incl. `tools.*` MCP) |
| Storage | `DagBackend::Memory` + `DagBackend::Redb` (redb default, Pure Rust) |

---

## For Other Primals

- **Sled removal pattern**: If your primal still has sled as optional, remove it — redb is the ecosystem standard, 100% Pure Rust, ACID, ecoBin compliant
- **Sovereignty pattern**: Remove all `*_ADDRESS` vendor-specific env var fallbacks. Use `CAPABILITY_ENDPOINT` pattern only. A primal discovers capabilities, not vendors.
- **Async manifest I/O**: Convert synchronous `std::fs` manifest operations to `tokio::fs` for consistency in async runtimes — avoids `block_on` nesting panics in tests
- **`Arc::clone` enforcement**: Use `Arc::clone(&x)` instead of `x.clone()` for all `Arc` types — makes refcount intent explicit

## Previous Handoff

- [RHIZOCRYPT_V013_S19_MCP_DAGBACKEND_GC_PROPTESTS_HANDOFF_MAR23_2026.md](./RHIZOCRYPT_V013_S19_MCP_DAGBACKEND_GC_PROPTESTS_HANDOFF_MAR23_2026.md)
