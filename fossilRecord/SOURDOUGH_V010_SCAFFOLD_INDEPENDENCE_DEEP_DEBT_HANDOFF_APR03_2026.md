# sourDough v0.1.0 — Scaffold Independence + Deep Debt Resolution

**Date**: April 3, 2026
**Status**: COMPLETE — scaffold independence achieved, deep debt resolved, 94.40% coverage

---

## Scaffold Independence (Budding Primal Pattern)

The primary architectural change: sourDough now generates **self-contained primals**
with zero runtime dependency on `sourdough-core`.

### What Changed

**`crates/sourdough/src/commands/scaffold.rs`** was completely rewritten:

- Core primal traits (`PrimalError`, `PrimalLifecycle`, `PrimalState`, `PrimalHealth`,
  `HealthStatus`, `HealthReport`) are now inlined as string templates
- `new-primal` generates a workspace with its own `-core` crate containing all traits
- `new-crate` uses a path dependency to the primal's own core (e.g., `../{primal}-core`)
- Generated `Cargo.toml` uses granular tokio features instead of `"full"`
- `find_sourdough_core_path` function removed entirely
- Generated `CONVENTIONS.md` and `README.md` reference self-contained structure

**`crates/sourdough/src/commands/validate.rs`** updated:

- Removed the check requiring `sourdough-core` dependency in core crates

### Cross-Primal Impact

Primals scaffolded by sourDough are now fully independent from creation. No primal
needs to reference sourDough at compile time or runtime. This aligns with the
primal sovereignty principle: primals know only themselves.

---

## Deep Debt Resolution

### Dependencies Removed (6)

| Dependency | Crate | Reason |
|-----------|-------|--------|
| `ed25519-dalek` | workspace | Unused; identity via BearDog at runtime |
| `config` (crate) | workspace, sourdough-core | Conflicted with local config module; unused |
| `futures` | workspace, sourdough-core, sourdough-genomebin | Unused; tokio provides all async primitives |
| `walkdir` | sourdough | Unused after scaffold refactor |
| `ignore` | sourdough | Unused after scaffold refactor |
| `pathdiff` | sourdough | Removed with `find_sourdough_core_path` |

### Lint Enforcement

- All `#[allow()]` directives replaced with `#[expect(lint, reason = "...")]`
- Zero remaining `#[allow()]` or `#![allow()]` in the codebase
- `#![forbid(unsafe_code)]` on all crate roots

### genomebin Sign Command

- Removed bash script fallback in `sign_genomebin`
- Returns explicit error guiding toward Pure Rust `sequoia-openpgp` implementation
- `find_genomebin_script` function removed

### genomebin/ Bash Scripts Archived

The entire `genomebin/` directory (5 bash scripts, config templates, service templates)
has been archived to `archive/genomebin_bash_JAN19_2026/`. All functionality is now
in the Pure Rust `sourdough-genomebin` crate.

---

## Test Coverage

| Metric | Before | After |
|--------|--------|-------|
| Total tests | 175 | 229 |
| Coverage | 87.63% | 94.40% |
| sourdough-genomebin validator.rs | 9.23% | ~96% |

### New Tests (54 total)

- `sourdough-genomebin/validator.rs`: 24 tests (file existence, shebang, payload boundary, metadata extraction, architecture count, full validation)
- `sourdough-genomebin/error.rs`: 9 tests (Display for all error variants)
- `sourdough-genomebin/platform.rs`: 21 tests (Display, target_triple, simple_target, is_linux, is_macos, is_musl, fallback_targets, Platform::detect)

---

## Documentation Cleanup

### Archived (fossil record in `archive/`)

- `DEVELOPMENT.md` (Jan 19 — stale Rust 1.70+ references, old test counts)
- `ECOBIN_CERTIFICATION.md` (Jan 19 — historical certification record)
- `genomebin/` directory (Jan 19 — replaced by Pure Rust crate)

### Updated

- `STATUS.md` — reflects 94.40% coverage, scaffold independence, 229 tests
- `CHANGELOG.md` — full session changelog
- `README.md` — rewritten: concise, accurate, no emojis, documents budding primal pattern
- `specs/SOURDOUGH_SPECIFICATION.md` — version 0.1.0, genomebin section updated to Pure Rust
- `specs/ROADMAP.md` — version 0.1.0, current status reflects actual completion state

### Retained

- `CONVENTIONS.md` — still valid ecosystem-level conventions (edition 2024)
- `specs/ARCHITECTURE.md` — recently updated, structurally sound
- `specs/EPHEMERAL_PRIMAL_SCAFFOLDING.md` — new spec for session-as-primal pattern

---

## Remaining Gaps

| Gap | Priority | Notes |
|-----|----------|-------|
| Cross-compilation (musl) | Medium | Needs CI target validation |
| genomeBin signing | Medium | Pure Rust via sequoia-openpgp when BearDog identity available |
| EphemeralOwner<T> | Low | Spec exists; implementation deferred to v0.7+ per ROADMAP |
| biomeOS/neuralAPI connectors | Low | Depends on ecosystem maturity |

---

## Files Changed

| File | Change |
|------|--------|
| `crates/sourdough/src/commands/scaffold.rs` | Complete rewrite for scaffold independence |
| `crates/sourdough/src/commands/validate.rs` | Removed sourdough-core dependency check |
| `crates/sourdough/src/commands/genomebin.rs` | Removed bash script fallback |
| `crates/sourdough/src/commands/mod.rs` | `#[expect]` with reason |
| `crates/sourdough-core/src/ipc.rs` | `#[expect]` with reason |
| `crates/sourdough/Cargo.toml` | Removed walkdir, ignore, pathdiff |
| `crates/sourdough-core/Cargo.toml` | Removed futures, config |
| `crates/sourdough-genomebin/Cargo.toml` | Removed futures |
| `Cargo.toml` (workspace) | Removed ed25519-dalek, config, futures |
| `crates/sourdough-genomebin/src/validator.rs` | 24 new tests |
| `crates/sourdough-genomebin/src/error.rs` | 9 new tests |
| `crates/sourdough-genomebin/src/platform.rs` | 21 new tests |
| `STATUS.md` | Updated with current state |
| `CHANGELOG.md` | Full session changelog |
| `README.md` | Complete rewrite |
| `specs/SOURDOUGH_SPECIFICATION.md` | Version fix, genomebin section update |
| `specs/ROADMAP.md` | Version fix, current status update |

---

**Verification**: `cargo build && cargo test && cargo clippy (pedantic+nursery) && cargo fmt --check && cargo doc && cargo llvm-cov` all pass.

**License**: AGPL-3.0-or-later | ORC | CC-BY-SA-4.0
