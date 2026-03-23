# rhizoCrypt v0.13.0-dev — scyBorg License, Idiomatic Rust & Coverage Handoff

**Date**: March 23, 2026
**Scope**: scyBorg triple-license compliance, sled deprecation, idiomatic Rust 2024 patterns, StorageResultExt, error-path coverage expansion, audit verification, docs sync

---

## Changes Delivered

### 1. scyBorg Triple-Copyleft License

- Replaced single AGPL-3.0 `LICENSE` file with full scyBorg Triple-Copyleft format
- Three independent copyleft licenses governed by independent nonprofits:
  - **Software**: AGPL-3.0-or-later (Free Software Foundation)
  - **Game Mechanics**: ORC (Open RPG Creative Foundation)
  - **Creative Content/Docs**: CC-BY-SA 4.0 (Creative Commons)
- Reserved Material section (branding, primal names, gate names)
- Full AGPL-3.0 text included in LICENSE

### 2. Sled Backend Deprecation

- `SledDagStore` marked `#[deprecated(since = "0.5.0")]` with migration note
- All `impl` blocks annotated with `#[expect(deprecated)]` (Rust 1.81+ lint hygiene)
- Module docs updated: clearly marked DEPRECATED with rationale (zstd-sys C dependency, unmaintained)
- `lib.rs` re-exports gated with `#[allow(deprecated)]` / `#[expect(deprecated)]`
- CONTEXT.md, README.md updated to reflect deprecated status

### 3. `StorageResultExt` Trait — Idiomatic Error Handling

- New `pub(crate) trait StorageResultExt<T>` in `error.rs`
- `.storage_ctx("context message")` replaces verbose `map_err(|e| RhizoCryptError::storage(format!("...: {e}")))`
- Applied across all of `store_redb.rs` — **40+ map_err chains eliminated**
- `store_redb.rs` reduced from 649 → **552 lines** (15% reduction, identical behavior)
- Zero coverage regression — coverage actually improved

### 4. `#[expect(deprecated)]` Lint Evolution

- Converted `#[allow(deprecated)]` → `#[expect(deprecated, reason = "...")]` where applicable
- `#[expect]` warns if the deprecation vanishes (ensures cleanup when sled is removed)
- Module declarations in `lib.rs` keep `#[allow]` (no warning to expect at module level)

### 5. Coverage Expansion (Prior Session, Same Date)

- `store_redb.rs`: 68.97% → **77.75%** (+20 tests for error paths, edge cases, helpers)
- `songbird/client.rs`: +6 tests (scaffolded registration, refresh errors, disconnect states)
- `adapters/tarpc.rs`: +6 tests (feature-gated oneway, debug, endpoint, connect errors)
- `adapters/http.rs`: +6 tests (debug, clone, URL building, unreachable service errors)
- `toadstool_http.rs`: +5 tests (deployment edge cases, parse_deployment_id, debug, clone)
- Test modules extracted to separate files following existing `#[path = "..."]` pattern

### 6. Audit Verification

| Check | Result |
|-------|--------|
| TODO/FIXME/HACK/XXX in `.rs` | None |
| `unsafe` blocks | None |
| `todo!()`/`unimplemented!()` | None |
| unwrap/expect in production | None |
| Mocks in production | None (all behind `#[cfg(test)]` or `test-utils` feature) |
| Hardcoded primal names | Self-knowledge only; external primals feature-gated interop |
| C dependencies | `ring` behind optional `http-clients` only; default builds pure Rust |
| Dead dependencies | None |
| Production `#[allow(dead_code)]` | None |
| `async_trait` usage | Correct (trait objects require boxing; integration traits use native RPITIT) |

### 7. Smart Refactoring Decision

- Assessed top 10 largest files (500-867 lines) for responsibility splitting
- All files well under 1000 LOC limit (max 867, production max 724)
- Decision: **no unnecessary splits** — files are cohesive and well-organized
- `store.rs` (673), `loamspine_http.rs` (667), `service.rs` (678): tightly-coupled private types, crate-internal consumers — splitting adds navigation overhead without benefit

### 8. Documentation Sync

- README.md: license → scyBorg triple, tests → 1,356, coverage → 93.91%/94.95%, .rs files → 125
- CONTEXT.md: coverage updated, .rs count corrected
- DEPLOYMENT_CHECKLIST.md: metrics synchronized
- showcase/00_START_HERE.md: metrics synchronized

---

## Current State

| Metric | Value |
|--------|-------|
| Tests | 1,356 passing (`--all-features`) |
| Region Coverage | 93.91% |
| Line Coverage | 94.95% |
| Clippy | 0 warnings (pedantic + nursery + cargo + cast lints) |
| Doc | 0 warnings (`-D warnings`) |
| Fmt | Clean |
| Source files | 125 `.rs`, ~44,275 lines |
| Max file | 867 lines (limit: 1000) |
| Unsafe | `deny` workspace-wide, zero `unsafe` blocks |
| Dead deps | Zero |
| C deps (default) | Zero (ecoBin compliant) |
| License | scyBorg Triple-Copyleft (AGPL-3.0+ / ORC / CC-BY-SA 4.0) |

---

## For Other Primals

- **scyBorg LICENSE template**: rhizoCrypt's `LICENSE` file is the canonical format — other primals should adopt the same structure
- **`StorageResultExt` pattern**: Generic trait for `.storage_ctx("msg")` reduces `map_err` boilerplate in any storage backend
- **`#[expect(deprecated)]`**: Prefer over `#[allow(deprecated)]` for intentional deprecations — CI will flag when cleanup is due
- **Sled migration**: Any primals using sled should migrate to redb (Pure Rust, ACID, actively maintained)
- **Coverage gate**: `cargo llvm-cov --fail-under-lines 90` as CI gate — 93.91% with room to grow
