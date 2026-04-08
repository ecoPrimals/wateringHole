<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Iteration 75: primalSpring Audit Resolution

**Date**: April 6, 2026
**Commit**: `6a7948d` (main)
**Trigger**: Downstream audit findings from primalSpring

---

## Summary

Resolved all four findings from the primalSpring downstream audit of
coralReef. License, workspace lints, documentation, and IPC code
quality all addressed.

## Changes

### 1. License: AGPL-3.0-only → AGPL-3.0-or-later

- Workspace `Cargo.toml` `license` field updated
- All SPDX headers across ~200 `.rs` files, `.wgsl` fixtures, shell
  scripts, boot configs, showcase/fuzz/tool `Cargo.toml` files
- `LICENSE`, `LICENSE-ORC`, `genomebin/manifest.toml` updated
- All docs (`README.md`, `CONTRIBUTING.md`, `CONVENTIONS.md`,
  `STATUS.md`, `CHANGELOG.md`, `COMPILATION_DEBT_REPORT.md`,
  `specs/SOVEREIGN_MULTI_GPU_EVOLUTION.md`) updated
- Cursor rule `.cursor/rules/coralreef-standards.mdc` updated
- `deny.toml` allow list retains both `AGPL-3.0-only` and
  `AGPL-3.0-or-later` for dependency compatibility

### 2. Workspace unsafe_code lint

- Added `unsafe_code = "deny"` to `[workspace.lints.rust]`
- `coral-driver` is unaffected (does not inherit workspace lints) and
  manages `unsafe` locally for kernel ioctl/mmap/MMIO with `// SAFETY:`
  documentation on every block
- All other crates that inherit workspace lints already had
  `#![forbid(unsafe_code)]` — the workspace-level `deny` documents
  the intent and catches any future crate that forgets
- Test integration files using Rust 2024 `unsafe` `set_var`/`remove_var`
  received `#![allow(unsafe_code, reason = "...")]`

### 3. CONTEXT.md

- Created at repo root with architecture overview, crate map, key
  constraints, IPC capabilities, and entry-point pointers
- Serves AI agents and new collaborators

### 4. IPC `#[allow]` cleanup

- Attempted migration from `#[allow(reason)]` to `#[expect(reason)]`
  per audit recommendation
- Discovery: these lints (`unused_imports`, `dead_code`) never fire on
  `pub use` / `pub fn` items in the library target, but DO fire when
  compiling the binary target with `--all-features` (where `e2e` is
  enabled but the binary doesn't reference the re-exports)
- `#[expect]` fails on the lib target (unfulfilled expectation) while
  the binary target needs suppression → `#[allow(reason)]` is the
  correct cross-target choice
- Updated reason strings to document this cross-target behavior

## Metrics

| Gate | Result |
|------|--------|
| `cargo clippy --workspace --all-features -- -D warnings` | PASS (0 warnings) |
| `cargo test --workspace --all-features` | PASS (4407+ tests, 0 failed) |
| `cargo fmt --check` | PASS |

## Impact on Other Primals

- primalSpring can now validate `AGPL-3.0-or-later` in dependency scans
- Any primal importing `coralreef-core` or `coral-gpu` as a dependency
  sees the updated license metadata in `Cargo.toml`
- No API changes, no IPC protocol changes

## Open Items

- `coral-driver` workspace lint inheritance (pedantic + nursery) deferred
  to a dedicated iteration (~1980 warnings to triage)
- `coral-ember` and `coral-glowplug` workspace lint inheritance pending
