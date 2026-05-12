<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0 — Orphan Dead Code Removal & Deep Debt Cleanup

**Date**: April 26, 2026
**Primal**: Squirrel (AI Coordination)
**Sessions**: AJ (orphan cleanup), AI (800-line boundary test extraction)

## Summary

Comprehensive dead code audit and removal across the Squirrel workspace. Identified and deleted ~38 orphaned `.rs` files (~11,870 lines) that were never in any Rust module tree or `Cargo.toml` `[[bin]]` entry — never compiled, pure disk debris. Additionally, extracted tests from two 800-line boundary files to maintain file-size compliance.

## Orphan Removal Breakdown

| Category | Files | Lines | Crates |
|----------|-------|-------|--------|
| Config unified stubs | 4 | 2,172 | `squirrel-mcp-config` |
| Legacy auth files | 7 | 3,101 | `squirrel-mcp-auth` |
| Core context/coordinator/plugins | 4 | 899 | `squirrel-context`, `squirrel-core`, `squirrel-mcp`, `squirrel-plugins` |
| Main capability/ecosystem/error stubs | 8 | 1,769 | `squirrel` (main) |
| Federation coverage test orphans | 3 | 1,453 | `universal-patterns` |
| Unwired demo/tool binaries | 4 | 1,354 | `squirrel-core`, `squirrel-ai-tools`, `squirrel-cli` |
| Misc (prelude, casting, registry) | 3 | 551 | `squirrel-ai-tools`, `universal-patterns` |
| Empty directory cleanup | 1 dir | — | `squirrel-cli` |
| **Total** | **~38** | **~11,870** | **9 crates** |

All files preserved in git history as fossil record per ecoPrimals convention.

## 800-Line Boundary Test Extraction

| File | Before | After | Test file |
|------|--------|-------|-----------|
| `ai-tools/src/common/capability/mod.rs` | 800L | 418L | `capability_tests.rs` |
| `config/src/unified/loader.rs` | 800L | 419L | `loader_tests.rs` |

## Verification Method

Each file was verified as orphaned by confirming:
1. Not declared as `mod` in any parent `mod.rs`, `lib.rs`, or sibling `.rs` module
2. Not referenced via `#[path = "..."]` attribute
3. Not listed in any `[[bin]]` section of `Cargo.toml`
4. Not feature-gated behind any `#[cfg(feature = "...")]` module declaration

Several false positives were identified and excluded (e.g., `ecosystem/registry/types/*.rs` files declared in `types.rs`, feature-gated `squirrel-mcp-server` binary).

## Quality Gates

| Gate | Result |
|------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --workspace --all-targets -- -D warnings -W clippy::pedantic -W clippy::nursery` | PASS (0 warnings) |
| `cargo test --workspace` | PASS (7,178 passed / 0 failures) |
| `cargo deny check` | PASS |

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| `.rs` files | ~1,032 | ~997 |
| Total lines | ~335k | ~325k |
| Tests | 7,178 | 7,178 |
| Orphaned dead files | ~38 | 0 |
| Files >800L (production) | 0 | 0 |

## Files Modified

- `README.md` — file/line counts updated
- `CONTEXT.md` — file/line counts updated
- `CHANGELOG.md` — orphan removal and test extraction entries added
- `CURRENT_STATUS.md` — session AJ entry added

## Commit

All changes in single commit on `main` branch of `primals/squirrel`.
