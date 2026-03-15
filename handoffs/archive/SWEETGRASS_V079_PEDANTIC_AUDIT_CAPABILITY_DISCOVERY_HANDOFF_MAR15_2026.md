# SweetGrass v0.7.9 — Pedantic Audit: Quality + Capability Discovery + Spec Evolution

**Date**: March 15, 2026
**From**: v0.7.8 → v0.7.9
**Status**: Complete — all checks pass

---

## Summary

Comprehensive pedantic audit driven by wateringHole standards compliance review. `capability.list` JSON-RPC method added per `SPRING_AS_NICHE_DEPLOYMENT_STANDARD`. All 10 crates now enforce `#![warn(missing_docs)]` and `clippy::doc_markdown`. Copyright notices added to all 112 source files. Cargo metadata completed on all crates. `test-support` feature renamed to `test`. Spec documents evolved to match reality. PostgreSQL test URLs centralized. `config.rs` smart-refactored.

---

## capability.list — Runtime Discovery

New `capability.list` JSON-RPC method (method #21) enables runtime primal discovery per wateringHole `SPRING_AS_NICHE_DEPLOYMENT_STANDARD`:

```json
{
  "jsonrpc": "2.0",
  "method": "capability.list",
  "params": {},
  "id": 1
}
```

Response:

```json
{
  "primal": "sweetgrass",
  "version": "0.7.9",
  "domains": {
    "anchoring": ["anchor", "verify"],
    "attribution": ["chain"],
    "braid": ["create", "get", "get_by_hash", ...],
    "capability": ["list"],
    "compression": ["compress"],
    "contribution": ["record", "record_session", "record_dehydration"],
    "health": ["check", "detailed"],
    "provenance": ["graph"]
  },
  "methods": ["anchoring.anchor", "anchoring.verify", ...]
}
```

Built from the static dispatch table — always reflects the actual method set.

**Inter-primal impact**: All primals should implement `capability.list` returning their domain/operation map.

---

## Pedantic Lint Evolution

### `#![warn(missing_docs)]` on all 10 crates

Was only enabled on 5 crates. Now all 10 enforce documentation warnings, ensuring all public API items have doc comments.

### `clippy::doc_markdown` enabled

Removed `doc_markdown = "allow"` from workspace lints. All backtick-needing identifiers (e.g., `rhizoCrypt`, `LoamSpine`, `sweetGrass`) now properly escaped in doc comments. Auto-fixed via `cargo clippy --fix`.

### Redundant `#![allow]` removed

Three crate `lib.rs` files had redundant `#[allow(clippy::missing_const_for_fn)]` and `#[allow(clippy::missing_errors_doc)]` that were already handled by workspace-level lint configuration. Removed for clarity.

**Inter-primal pattern**: Let workspace `Cargo.toml` handle shared lints; only add crate-level attributes for crate-specific needs.

---

## Copyright and Metadata

### Copyright notices

`// Copyright (C) 2024–2026 ecoPrimals Project` added to line 2 (after SPDX header) of all 112 `.rs` source files that were missing it.

### Cargo metadata

All 10 crate `Cargo.toml` files now include:

```toml
readme = "../../README.md"
keywords = ["provenance", "attribution", ...]
categories = ["data-structures", ...]
```

**Inter-primal impact**: All primals should have copyright notices on all source files and complete Cargo metadata.

---

## Feature Rename: `test-support` → `test`

Per `clippy::cargo` recommendation, the `test-support` feature was renamed to `test` across 4 crate `Cargo.toml` files and 14 source files. The shorter name follows Rust convention (`feature = "test"` alongside `cfg(test)`).

---

## Spec Evolution

### `SWEETGRASS_SPECIFICATION.md` Section 8.1

Replaced stale gRPC/protobuf service definition with current tarpc + JSON-RPC 2.0 architecture. Added all 21 `{domain}.{operation}` methods including the new `capability.list`.

### `SWEETGRASS_SPECIFICATION.md` Section 12

Updated implementation roadmap to reflect completed v0.7.x phases and planned v0.8.0+.

---

## Smart Refactoring

| File | Before | After |
|------|--------|-------|
| `config.rs` | 879 lines | `config/mod.rs` (455L) + `config/tests.rs` (271L) |

All files now well under 1000 LOC. Largest file is 455 lines.

---

## PostgreSQL Test URLs Centralized

New constants and helpers in `sweet-grass-integration/src/testing.rs`:

| Item | Purpose |
|------|---------|
| `TEST_DB_URL` | Primary test database URL from env |
| `test_db_url()` | Helper with fallback to default |
| `postgres_test_url_for_port()` | Port-parameterized URL builder |

Replaces hardcoded `postgresql://postgres:postgres@localhost:5432/...` strings in factory tests, migration tests, and integration common modules.

---

## deploy.sh Evolution

Replaced hardcoded `DEFAULT_PORT=8080` and `DEFAULT_BACKEND="redb"` with env-var cascades:

```bash
PORT="${SWEETGRASS_HTTP_PORT:-${1:-8080}}"
BACKEND="${STORAGE_BACKEND:-${2:-redb}}"
```

Follows capability-based configuration pattern — no hardcoded defaults in scripts.

---

## Metrics

| Metric | v0.7.8 | v0.7.9 |
|--------|--------|--------|
| Tests | 853 | **857** |
| Region coverage | 91% | 91% |
| JSON-RPC methods | 20 | **21** (`capability.list`) |
| Crates with `missing_docs` | 5 | **10** |
| Copyright headers | ~7 | **112** (all) |
| Cargo metadata complete | 0 | **10** (all) |
| `doc_markdown` lint | suppressed | **enforced** |
| Largest file | 879L | **455L** |

---

## Deferred to v0.9.0

- **Typed JSON-RPC structs**: Evolving `serde_json::Value` params to typed request/response structs is a breaking API change requiring cross-primal coordination. Deferred.

---

## Verification

```
cargo fmt --all -- --check         ✓
cargo check --workspace            ✓ (0 warnings)
cargo clippy --workspace           ✓ (0 warnings)
cargo test --workspace             ✓ (857 tests)
RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps  ✓
```
