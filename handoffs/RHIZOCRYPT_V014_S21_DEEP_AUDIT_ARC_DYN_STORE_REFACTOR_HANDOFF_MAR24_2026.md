# rhizoCrypt v0.14.0-dev — Session 21 Handoff

**Date**: March 24, 2026
**Scope**: Comprehensive audit, clippy clean, Arc<dyn> evolution, MetadataValue boxing, store.rs refactor, version alignment, production panic audit

---

## Changes Delivered

### 1. Comprehensive Audit (Full Codebase)

- Audited all 126 `.rs` files against wateringHole standards (semantic naming, UniBin, ecoBin, IPC protocol, sovereignty, human dignity)
- Verified JSON-RPC + tarpc dual-protocol compliance
- Confirmed zero unsafe, zero TODO/FIXME/HACK, zero production panic/unwrap/expect
- Confirmed all SPDX headers present, scyBorg triple-copyleft compliant
- Cross-referenced specs/ against implementation: all specified features implemented

### 2. Clippy Clean (CI Gate Fixed)

- `PlatformKind::current()` → `const fn` (compile-time platform resolution)
- Eliminated `clone_on_copy` on Copy type
- Replaced `needless_collect` with iterator chains (`.count()`, `!.any()`)
- All 3 crates: `cargo clippy --all-targets --all-features -- -D warnings` = 0 warnings

### 3. Arc<Box<dyn>> → Arc<dyn> (Modern Idiomatic Rust)

- Eliminated double heap indirection in 5 capability clients
- `SigningClient`, `StorageClient`, `ProvenanceClient`, `ComputeClient`, `PermanentStorageClient`
- Pattern: `Arc::new(Box::new(adapter))` → `Arc::from(adapter)`

### 4. MetadataValue Enum Stack Size Reduction

- Boxed `Array` and `Object` variants to reduce enum size disparity
- `Array(Vec<Self>)` → `Array(Box<Vec<Self>>)`, `Object(HashMap<...>)` → `Object(Box<HashMap<...>>)`
- Serde handles Box transparently — zero API breakage

### 5. Smart store.rs Refactor (1042 → 659 lines)

- Extracted 363-line test module to `store_tests.rs` using `#[path]` attribute
- Follows existing `store_redb_tests*.rs` pattern
- Zero files over 1000-line limit (max: 867)

### 6. Version Alignment

- Bumped 8 files from `0.13.0-dev` to `0.14.0-dev`: Dockerfile, specs index, capability registry, deploy graph, showcase docs, service README, manifest examples

### 7. Production Safety Audit

- All 42 `panic!()` calls verified inside `#[cfg(test)]` modules only
- All `.to_string()` calls reviewed — none in hot request paths (all in error/test/init)
- Constants centralized in `constants.rs` with semantic names and derivation comments

---

## Current State

| Metric | Value |
|--------|-------|
| Tests | 1,387 passing (`--all-features`) |
| Coverage | 94.60% line coverage (CI gate: 90%) |
| Clippy | 0 warnings (pedantic + nursery + cargo + cast lints) |
| Doc | 0 warnings (`-D warnings`) |
| Fmt | Clean |
| Source files | 126 `.rs`, ~44,200 lines |
| Max file | 867 lines (limit: 1000) |
| Unsafe | `deny` workspace-wide, zero `unsafe` blocks |
| C deps (default) | Zero (ecoBin compliant) |
| License | scyBorg Triple-Copyleft (AGPL-3.0+ / ORC / CC-BY-SA 4.0) |
| IPC Methods | 27 methods, 8 domains (incl. `tools.*` MCP) |
| Storage | `DagBackend::Memory` + `DagBackend::Redb` (redb default, Pure Rust) |

---

## For Other Primals

- **Arc<Box<dyn Trait>> anti-pattern**: If your capability clients use `Arc<Box<dyn ProtocolAdapter>>`, replace with `Arc<dyn ProtocolAdapter>` — eliminates one heap indirection. Use `Arc::from(boxed_value)` for the coercion.
- **Large enum variants**: Box heap-allocated variants (`Vec`, `HashMap`) inside enums where size disparity exists between variants. Serde handles `Box` transparently.
- **File size discipline**: Extract test modules to `{module}_tests.rs` using `#[path]` when files approach 1000 lines. Tests often account for 40-60% of file size.
- **Version alignment**: When bumping workspace version, grep for old version strings in Dockerfile labels, spec frontmatter, deploy graphs, showcase docs, crate READMEs, and manifest doc examples.
- **Clippy pedantic**: `missing_const_for_fn` catches functions that can be `const` — helps the compiler with compile-time evaluation. `needless_collect` and `search_is_some` push toward lazy iterator chains.

## Previous Handoff

- [RHIZOCRYPT_V014_S20_SLED_REMOVAL_SOVEREIGNTY_COVERAGE_HANDOFF_MAR24_2026.md](./RHIZOCRYPT_V014_S20_SLED_REMOVAL_SOVEREIGNTY_COVERAGE_HANDOFF_MAR24_2026.md)
