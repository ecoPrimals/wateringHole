# sourDough v0.1.0 — Workspace Lints + Smart Refactoring + Doc Cleanup

**Date**: April 3, 2026
**Status**: COMPLETE — workspace lints, scaffold refactor, 96%+ coverage, all docs current

---

## Workspace-Level Lint Configuration

Moved all lint enforcement from per-crate `#![forbid()]`/`#![warn()]` to `[workspace.lints]`
in root `Cargo.toml`. Each crate opts in with `[lints] workspace = true`.

### What Changed

**Root `Cargo.toml`** — new sections:

```toml
[workspace.lints.rust]
unsafe_code = "forbid"
missing_docs = "warn"
rust_2018_idioms = { level = "warn", priority = -1 }
unreachable_pub = "warn"

[workspace.lints.clippy]
all = { level = "warn", priority = -1 }
pedantic = { level = "warn", priority = -1 }
nursery = { level = "warn", priority = -1 }

[profile.release]
lto = true
codegen-units = 1
strip = true
```

**All three crate `Cargo.toml` files** — added `[lints] workspace = true`.

**Crate roots** (`main.rs`, `lib.rs`) — removed per-crate `#![forbid(unsafe_code)]`,
`#![warn(clippy::all, ...)]`, `#![warn(missing_docs)]` (now inherited from workspace).

### Cross-Primal Impact

Generated scaffold code now emits the same `[workspace.lints]` and `[profile.release]`
blocks, so new primals also get workspace-level lint enforcement from birth.

---

## scaffold.rs Smart Refactoring

The monolithic `scaffold.rs` (789 lines) was decomposed into a module directory:

| File | Lines | Responsibility |
|------|-------|----------------|
| `scaffold/mod.rs` | 154 | `ScaffoldCommand` enum, `run` dispatch, `create_primal`, `create_crate` |
| `scaffold/generators.rs` | 220 | `write_workspace_cargo_toml`, `create_core_crate`, `write_specs_directory`, etc. |
| `scaffold/templates.rs` | 438 | All inlined primal DNA (string constants for generated files) |

This was a **smart refactor** — decomposed by responsibility (orchestration / file
writing / template data), not arbitrary line-count splitting.

---

## Doctest Fixes

Three doctests in `sourdough-core` were marked `rust,ignore` due to `#[async_trait]`
dependency. Rewritten to use native Rust 2024 async trait syntax:

- `lib.rs` — `PrimalLifecycle` example now compiles directly
- `identity.rs` — `PrimalIdentity` example uses native `async fn`
- `lifecycle.rs` — `PrimalLifecycle` example uses native `async fn`

Zero ignored doctests remaining.

---

## Parallel genomeBin Processing

The `parallel` field in `GenomeBinBuilder` (previously `#[expect(dead_code)]`) is
now functional. When `self.parallel && files.len() > 1`, ecoBin files are pre-read
concurrently using `tokio::task::JoinSet`.

---

## Doctor genomeBin Tools Implementation

Replaced "not yet implemented" stub in `check_genome_bin_tools()` with functional
check using `sourdough_genomebin::Platform::detect()`. Reports on:

- Platform detection (OS, arch, target triple)
- Archive operations (tar + flate2, Pure Rust)
- Checksum (BLAKE3 + SHA256, Pure Rust)
- Metadata (TOML, Pure Rust)
- Signing status (sequoia-openpgp, planned)

---

## Test Coverage

| Metric | Previous Session | This Session |
|--------|-----------------|--------------|
| Total tests | 229 | 239+ |
| Coverage | 94.40% | 96%+ |
| E2E tests | 1 (rpc_communication) | 3 (+ scaffold lifecycle, add crate) |
| CLI integration | ~20 | 25+ |

### New Tests

- `genomebin test` (valid and missing file paths)
- `genomebin sign` (not implemented and missing file error paths)
- `doctor --comprehensive` output validation
- E2E: scaffold -> build -> test -> validate lifecycle
- E2E: scaffold -> add-crate -> build -> test workspace

---

## Documentation Updates

### Updated

| File | Change |
|------|--------|
| `specs/ARCHITECTURE.md` | Accurate file map (29 files, ~8100 lines), scaffold module structure |
| `specs/ROADMAP.md` | Quality table (96%+, 239 tests, max 637 lines) |
| `CONVENTIONS.md` | Workspace lints, forbid(unsafe), self-contained scaffolds |
| `CHANGELOG.md` | Full session changelog with prior session history |
| `README.md` | Quality metrics updated |
| `WHATS_NEXT.md` | Quality targets updated |
| `STATUS.md` | All compliance items current |
| `.gitignore` | Removed duplicate entries |

### Created

| File | Purpose |
|------|---------|
| `WHATS_NEXT.md` | Roadmap and priorities per CONVENTIONS.md |
| `START_HERE.md` | New developer guide per CONVENTIONS.md |

### Cleaned

- `.gitignore` duplicate `.DS_Store` and `*~` entries removed
- `specs/SOURDOUGH_SPECIFICATION.md` — server --port N/A documented

---

## Remaining Gaps

| Gap | Priority | Notes |
|-----|----------|-------|
| Cross-compilation (musl) | Medium | Needs CI target validation |
| genomeBin signing | Medium | Pure Rust via sequoia-openpgp |
| EphemeralOwner<T> | Low | Spec exists; deferred to v0.3.0 |
| Archive cleanup decision | Low | `archive/` in sourDough vs ecoPrimals fossil record |

---

## Files Changed

| File | Change |
|------|--------|
| `Cargo.toml` | `[workspace.lints]`, `[profile.release]` |
| `crates/sourdough/Cargo.toml` | `[lints] workspace = true` |
| `crates/sourdough-core/Cargo.toml` | `[lints] workspace = true` |
| `crates/sourdough-genomebin/Cargo.toml` | `[lints] workspace = true`, workspace metadata |
| `crates/sourdough/src/main.rs` | Removed per-crate lint attrs |
| `crates/sourdough-core/src/lib.rs` | Removed per-crate lint attrs, doctest fix |
| `crates/sourdough-genomebin/src/lib.rs` | Removed per-crate lint attrs |
| `crates/sourdough-core/src/identity.rs` | Doctest fix |
| `crates/sourdough-core/src/lifecycle.rs` | Doctest fix |
| `crates/sourdough/src/commands/scaffold.rs` | Deleted (replaced by module) |
| `crates/sourdough/src/commands/scaffold/mod.rs` | New: command dispatch |
| `crates/sourdough/src/commands/scaffold/generators.rs` | New: file writing |
| `crates/sourdough/src/commands/scaffold/templates.rs` | New: primal DNA templates |
| `crates/sourdough/src/commands/doctor.rs` | genomeBin tools implementation |
| `crates/sourdough-genomebin/src/builder.rs` | Parallel processing implementation |
| `crates/sourdough/tests/cli_integration.rs` | 5 new tests |
| `crates/sourdough/tests/e2e_scaffold_lifecycle.rs` | New: 2 e2e tests |
| `specs/ARCHITECTURE.md` | Accurate file map and counts |
| `specs/ROADMAP.md` | Updated quality table |
| `specs/SOURDOUGH_SPECIFICATION.md` | server --port N/A |
| `CHANGELOG.md` | Session changelog |
| `CONVENTIONS.md` | Workspace lints, unsafe policy |
| `STATUS.md` | All items current |
| `README.md` | Quality metrics |
| `WHATS_NEXT.md` | New |
| `START_HERE.md` | New |
| `.gitignore` | Cleaned duplicates |

---

**Verification**: `cargo build && cargo test && cargo clippy --workspace --all-targets && cargo fmt --all -- --check && cargo doc --workspace --no-deps && cargo llvm-cov --workspace` — all pass.

**License**: AGPL-3.0-or-later | ORC | CC-BY-SA-4.0
