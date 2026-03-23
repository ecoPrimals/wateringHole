# rhizoCrypt v0.13.0-dev — Deep Debt & Capability Naming Handoff

**Date**: March 23, 2026
**Scope**: Dead dependency removal, capability-based type naming, handler DRY, lint evolution, coverage expansion, ecosystem alignment

---

## Changes Delivered

### 1. Dead Dependency Removal: `parking_lot`

- `parking_lot = "0.12"` was declared in workspace + both crate Cargo.toml files
- **Never imported** in any `.rs` file — pure dead weight
- Removed from all 3 Cargo.toml files, eliminating transitive dependency tree

### 2. Dead Dependency Removal: `anyhow` (prior session)

- `anyhow = "1.0"` was unused after structured error migration to `thiserror`
- Removed from workspace and `rhizo-crypt-rpc` Cargo.toml

### 3. Capability-Based Type Naming: `LoamCommitRef` → `CommitRef`

Core domain type renamed from LoamSpine-specific to provider-agnostic:

- `LoamCommitRef` → `CommitRef` (struct rename)
- `loam_ref` → `commit_ref` (field rename in `SessionState::Committed`)
- `pub type LoamCommitRef = CommitRef` backward-compatible alias retained
- **15+ files updated** across core, RPC, integration, mocks, clients, tests
- All doc comments updated: "LoamSpine" → "permanent storage" / "capability-discovered provider"
- Files affected: `session.rs`, `dehydration.rs`, `slice.rs`, `event.rs`, `constants.rs`, `lib.rs`, `niche.rs`, `rhizocrypt.rs`, `permanent.rs`, `loamspine_http.rs`, `loamspine_http_tests.rs`, `integration/mod.rs`, `integration/mocks.rs`, `unix_socket.rs`

### 4. Handler DRY Refactoring

- Extracted `to_json<T: Serialize>()` — replaced 13 identical `serde_json::to_value(&x).map_err(...)` patterns
- Extracted `vertex_ids_to_value(&[VertexId])` — replaced 4 identical vertex-id-array serialization patterns
- Net reduction: ~40 lines of boilerplate

### 5. `async_trait` Audit (No Change Needed)

- Confirmed correctly used only for `dyn ProtocolAdapter` (trait objects)
- Integration traits already use native RPITIT (Rust 2024)
- This is the correct, modern split — no evolution needed until `dyn async Trait` stabilizes

### 6. Coverage Verified via `cargo-llvm-cov`

- **92.96% line coverage** (up from 92.32%)
- **93.50% region coverage**
- **89.49% function coverage**
- All above the 90% CI gate

### 7. Doc Cleanup

- Updated coverage: 92.32% → 92.96% in README.md, CONTEXT.md, DEPLOYMENT_CHECKLIST.md
- Updated sled description from "high-performance" to "deprecated" in deployment checklist
- Updated deployment checklist date

---

## Current State

| Metric | Value |
|--------|-------|
| Tests | 1330 passing (`--all-features`) |
| Coverage | 92.96% (`--fail-under-lines 90` CI gate) |
| Clippy | 0 warnings (pedantic + nursery + cargo) |
| Doc | 0 warnings (`-D warnings`) |
| Fmt | Clean |
| SPDX | 129 `.rs` files |
| Max file | 867 lines (all under 1000) |
| Unsafe | `deny` workspace-wide, zero `unsafe` blocks |
| Cross-primal deps | Zero (sovereign wire types) |
| Dead deps | Zero (parking_lot + anyhow removed) |

---

## Audit Summary (Clean)

| Check | Result |
|-------|--------|
| TODO/FIXME/HACK/XXX in `.rs` | None |
| `unsafe` blocks | None |
| `todo!()`/`unimplemented!()` | None |
| `#[deprecated]` | None |
| `#[allow(dead_code)]` in prod | None |
| unwrap/expect in production | None |
| Mocks in production | None |
| Hardcoded primal names in core types | None (`CommitRef` is now agnostic) |
| Dead dependencies | None |

---

### 8. Ecosystem Method Naming Alignment

- Canonical method renamed from `capability.list` → `capabilities.list` (plural, ecosystem standard)
- Added aliases: `capability.list`, `primal.capabilities` for backward compatibility
- Updated `CAPABILITY_DOMAINS`, `COST_ESTIMATES`, `SEMANTIC_MAPPINGS`, `capability_registry.toml`
- Health endpoints also aliased: `health.liveness` ← `ping`/`health`, `health.check` ← `status`/`check`

### 9. Lint Evolution: `missing_errors_doc` allow→warn

- Evolved from `missing_errors_doc = "allow"` to `missing_errors_doc = "warn"`
- Added `# Errors` documentation to 17 public `Result`-returning APIs across capability clients, adapters, error module
- Zero warnings after documentation pass

### 10. Cast Safety Lints

- Added `cast_lossless`, `cast_possible_truncation`, `cast_precision_loss`, `cast_sign_loss` = "warn"
- Zero violations found — codebase has no unsafe casts

### 11. Dead Dependency Removal: `lru`

- `lru = "0.12"` declared in `rhizo-crypt-core/Cargo.toml` but never imported
- Removed, eliminating unnecessary dependency

### 12. Hardcoding Cleanup

- Generalized doc comments in `unix_socket.rs`, `niche.rs`, `storage.rs` to remove primal name references
- All remaining primal names are in test data (acceptable) or named adapter modules (e.g., `loamspine_http.rs`)

### 13. Coverage Expansion

- `signing.rs`: 38.33% → **90.55%** (added mock adapter tests for sign/verify/attest/vertex operations)
- `registry.rs`: 75.46% → **92.27%** (added discovery failure paths, concurrent access, cache tests)
- Added `clear_discovery_source()` method to `DiscoveryRegistry`
- **Total**: 1,348 tests, 92.96% region / 94.05% line coverage

### 14. Documentation Refresh

- Updated metrics across README.md, CONTEXT.md, DEPLOYMENT_CHECKLIST.md, showcase/00_START_HERE.md
- Corrected test count (1,330 → 1,348) and coverage (92.32% → 92.96% region / 94.05% line)
- Fixed ban list count (14 → 16 crates in deny.toml)
- Synchronized dates across all docs to March 23, 2026
- Hardened `.gitignore` (added .env, IDE dirs, coverage artifacts, Thumbs.db)
- Documented `.cargo/config.toml` as machine-specific with developer guidance
- Verified: zero TODOs/FIXMEs/HACKs in production `.rs` code
- Verified: zero `#[deprecated]`, `#[allow(dead_code)]`, or `unimplemented!()` in production
- Archive content properly isolated in `specs/archive/`

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,348 |
| Region Coverage | 92.96% |
| Line Coverage | 94.05% |
| clippy (pedantic+nursery) | Zero warnings |
| Cast lints | Zero warnings |
| `missing_errors_doc` | Zero warnings |
| `cargo doc -D warnings` | Clean |
| `cargo fmt` | Clean |
| Dead dependencies | None |

## For Other Primals

- **`CommitRef` naming pattern**: Other primals using LoamSpine-specific types in their domain models should consider similar capability-agnostic renaming
- **Dead dependency audit**: `parking_lot`, `anyhow`, and `lru` were declared but unused — worth checking in other primals
- **`to_json()` pattern**: Simple helper eliminates repetitive `serde_json::to_value().map_err()` chains in JSON-RPC handlers
- **Coverage gate**: `cargo llvm-cov --fail-under-lines 90` works well as a CI gate
- **`capabilities.list` (plural)**: Ecosystem standard method name — other primals should align
- **Cast lints**: `cast_precision_loss`, `cast_possible_truncation`, `cast_sign_loss`, `cast_lossless` — easy defensive gates
- **`missing_errors_doc = "warn"`**: Forces `# Errors` documentation on all public `Result` APIs
