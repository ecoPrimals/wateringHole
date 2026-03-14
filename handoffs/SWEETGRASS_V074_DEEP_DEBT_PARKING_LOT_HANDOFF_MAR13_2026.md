# SweetGrass v0.7.4 — Deep Debt: parking_lot + Idiomatic Refactor Handoff

**Date**: March 13, 2026
**From**: SweetGrass (v0.7.4)
**To**: All primal teams
**License**: AGPL-3.0-only

---

## Summary

SweetGrass v0.7.4 migrates all `std::sync::RwLock` usage to `parking_lot::RwLock`
(pure Rust, no lock poisoning, better contention performance). Centralizes
duplicated constants, extracts hardcoded strings to named constants, evolves the
status subcommand to a real HTTP health check, and cleans all stale deprecation
notices from source.

---

## What Changed

### parking_lot::RwLock Migration

All `std::sync::RwLock` replaced with `parking_lot::RwLock` across:

- `MemoryStore` (production in-memory backend)
- `Indexes` (secondary index management)
- `MockAnchoringClient` (test support)
- `MockSessionEventsClient` (test support)

**Why**: `parking_lot` locks are infallible (no `.map_err` poisoning dance),
have better performance under contention, and are pure Rust. The `Indexes` API
is now fully infallible — `add()`/`remove()` return `()`, `get_*` methods return
`Option` or `HashSet` directly.

### Constant Centralization

| Constant | Location | Was |
|----------|----------|-----|
| `DEFAULT_QUERY_LIMIT` | `sweet-grass-store::traits` | Duplicated in sled + postgres |
| `SIGNING_ALGORITHM` | `signer::traits` | Hardcoded `"Ed25519Signature2020"` in tarpc client |
| `error_code::PARSE_ERROR` | `handlers::jsonrpc::error_code` | Magic number `-32700` in UDS handler |

### Status Subcommand

`sweetgrass status` now performs a real HTTP `GET /health` check with response
parsing, replacing the previous raw TCP connection test. Implemented with a
custom pure-Rust HTTP client (no external HTTP dependency).

### Attribution Test Extraction

`attribution/mod.rs` (786 LOC) split into `mod.rs` (302 LOC production) +
`tests.rs` (484 LOC tests) for file-size discipline.

### Stale Reference Cleanup

Removed 4 stale references to non-existent `DEPRECATED_ALIASES_REMOVAL_PLAN.md`
and legacy primal-name comments (`BearDogClient`, `LoamSpineClient`) from source.

---

## No API Changes

All v0.7.3 APIs remain unchanged. No new methods, no breaking changes.
`parking_lot::RwLock` is an internal implementation detail.

---

## For All Primal Teams

No action required. This is an internal quality release. If your primal uses
`sweet-grass-store::DEFAULT_QUERY_LIMIT` or `signer::SIGNING_ALGORITHM`, these
are now canonical exports from their respective trait modules.

---

## SweetGrass v0.7.4 Metrics

| Metric | Value |
|--------|-------|
| Version | 0.7.4 |
| Tests | 746 passing |
| Line coverage | 94% (cargo llvm-cov) |
| Crates | 9 |
| Protocols | JSON-RPC 2.0 + tarpc + REST + UDS |
| License | AGPL-3.0-only |
| Unsafe code | 0 (`#![forbid(unsafe_code)]` all crates) |
| Production unwraps | 0 |
| Clippy | 0 warnings (pedantic + nursery, -D warnings) |
| Max file | 824 lines (limit: 1000) |
| TODOs in source | 0 |
| Lock impl | parking_lot::RwLock (pure Rust, infallible) |

---

## Supersedes

Extends `SWEETGRASS_V073_AUDIT_COVERAGE_HANDOFF_MAR13_2026.md`.
All v0.7.3 methods and contracts remain valid.
