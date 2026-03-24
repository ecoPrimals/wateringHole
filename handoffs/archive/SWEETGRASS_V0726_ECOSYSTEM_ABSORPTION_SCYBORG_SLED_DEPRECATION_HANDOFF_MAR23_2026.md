# SweetGrass v0.7.26 — Ecosystem Absorption, scyBorg License, Sled Deprecation

**Date**: March 23, 2026
**From**: v0.7.25 → v0.7.26
**Status**: All green — 1,128 tests, 0 clippy warnings, 0 doc warnings, 0 unsafe, 0 fmt issues

---

## Summary

SweetGrass v0.7.26 absorbs ecosystem patterns from rhizoCrypt v0.13.0,
loamSpine v0.9.10, ludoSpring V29, barraCuda, and wetSpring. Focus: license
compliance, lint evolution, dependency hygiene, and sovereignty enforcement.

---

## Changes

### License & Compliance
- **scyBorg Triple-Copyleft LICENSE** adopted (AGPL-3.0-or-later + ORC-1.0 + CC-BY-SA-4.0 with Reserved Material section) — matches rhizoCrypt v0.13.0 format
- **SPDX `# SPDX-License-Identifier: AGPL-3.0-only`** on all 12 Cargo.toml files (ludoSpring V29 pattern)

### Sled Deprecation
- `#[deprecated(since = "0.7.26")]` on `SledStore` struct, all impl blocks, factory function, re-export
- Follows rhizoCrypt's deprecation of sled (unmaintained upstream, optional `zstd-sys` C dependency)
- Migration docs point to `sweet-grass-store-redb` (actively maintained, 100% Pure Rust)

### Dependency Hygiene
- **3 unused `async-trait` deps removed** (factory, compression, query)
- **6 retained deps documented** with dyn-compatibility rationale — all traits use `Arc<dyn Trait>`, native RPITIT not object-safe
- **Production binary verified 100% pure Rust** — zero `-sys` crates; `ring`/`cc` only in dev-deps (testcontainers)
- `deny.toml`: `multiple-versions = "deny"` (was `"warn"`) — aligned with BearDog v0.9.0

### Lint Evolution
- **All `#[allow]` → `#[expect(reason)]`** with specific rationale strings (5 sites)
- Unfulfilled expectations removed (loamSpine v0.9.10: don't suppress what doesn't fire)
- **Cast lints added** to workspace: `cast_possible_truncation`, `cast_sign_loss`, `cast_precision_loss`, `cast_lossless`

### Primal Sovereignty
- **`primal_names::names` module deprecated** — hardcoded knowledge of other primals removed; generic `socket_env_var(discovered_name)` retained
- Discovery confirmed capability-based with zero hardcoded addresses (`niche.rs`, `primal_info.rs`)
- All mocks verified behind `#[cfg(any(test, feature = "test"))]`

### JSON-RPC Evolution
- **`normalize_method()`** for case-insensitive dispatch (barraCuda/loamSpine/wetSpring pattern)
- Underscores in operation names preserved (`braid.get_by_hash`)

### Build Infrastructure
- `cargo coverage` / `coverage-html` / `coverage-json` aliases in `.cargo/config.toml`

### Root Docs
- README, CONTEXT, DEVELOPMENT, SPECIFICATION, deploy.sh, showcase, config — all updated to v0.7.26
- LICENSE updated to scyBorg triple-copyleft format
- Duplicate license line in CONTEXT.md removed

---

## Audited — No Action Needed
- **Files**: All under 826 lines (max: `store-redb/tests.rs`); well under 1000-line ceiling
- **Mocks**: All behind `#[cfg(test)]` or `#[cfg(feature = "test")]`; zero in production paths
- **Unsafe**: `#![forbid(unsafe_code)]` on all 10 crates + binary; zero unsafe blocks
- **`/tmp/` paths**: 13 occurrences — all config struct string fixtures, no filesystem operations
- **TODOs**: Zero `TODO`/`FIXME`/`HACK`/`XXX` in any .rs file
- **Debris**: No archive code, no stale scripts, no orphan files

---

## Deferred to v0.8 (Profile-Driven)
- **StorageResultExt** — needs profiling to justify abstraction
- **Tokio feature slimming** — per-crate feature audit needed
- **Fuzz target for JSON-RPC dispatch** — infrastructure exists (fuzz/ crate)
- **async-trait removal** — blocked on stable `dyn Trait` with async fn; all 6 retained uses require object safety

---

## Cross-Ecosystem Signals

| Pattern | Source | Status in sweetGrass |
|---------|--------|---------------------|
| scyBorg triple LICENSE | rhizoCrypt v0.13.0 | ✅ Adopted |
| `#[allow]` → `#[expect(reason)]` | loamSpine v0.9.10 | ✅ Complete |
| SPDX on all Cargo.toml | ludoSpring V29 | ✅ Complete |
| `normalize_method()` | barraCuda/wetSpring | ✅ Adopted |
| sled deprecation | rhizoCrypt v0.13.0 | ✅ Deprecated |
| `multiple-versions = "deny"` | BearDog v0.9.0 | ✅ Adopted |
| cargo-llvm-cov aliases | ludoSpring V29 | ✅ Added |
| Cast lints | loamSpine trio | ✅ Added |
| `primal_names::names` deprecated | sovereignty principle | ✅ Done |

---

## Verification

```
cargo fmt:     PASS (0 diffs)
cargo clippy:  PASS (0 warnings, -D warnings)
cargo doc:     PASS (0 warnings)
cargo test:    1,128 passed, 0 failed, 56 ignored
cargo build --release: PASS
unsafe blocks: 0
```
