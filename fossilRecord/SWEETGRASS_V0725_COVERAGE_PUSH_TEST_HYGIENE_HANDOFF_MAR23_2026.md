# sweetGrass v0.7.25 — Coverage Push, Test Hygiene, PUBLIC_SURFACE_STANDARD Compliance

**Date**: March 23, 2026
**From**: sweetGrass
**To**: all primals, biomeOS, wateringHole
**Status**: Released
**Previous**: v0.7.24 Deep Debt: Zero-Copy Phase 2, Public Surface, Audit (Mar 23, 2026)

---

## Summary

Pushed line coverage from ~78% to **90.47%** (cargo llvm-cov), refactored
oversized test files, completed PUBLIC_SURFACE_STANDARD Layer 2 + Layer 4
compliance, and cleaned stale coverage artifacts that were distorting metrics.

Combined with v0.7.24 (same session): cross-crate `Arc<str>` zero-copy
migration for `EcoPrimalsAttributes.source_primal`, `.niche`,
`LoamCommitRef.spine_id`, and factory/engine internals.

---

## Changes

### v0.7.25

#### Added

- **15 new tests** — error variant coverage (`Transport`, `Discovery`, `Io`,
  `Store`, `Serialization`), provenance traversal edge cases (`children`,
  `root_braid`, cycle detection, depth-zero), handler gaps
  (`create_provenance_braid`, list filters with agent/tag/offset), sled
  config/constants — total: 1,121 tests
- **README ecoPrimals footer** — per PUBLIC_SURFACE_STANDARD Layer 2

#### Changed

- **Sled tests smart refactored** — 922-line monolithic `store/tests.rs` split
  into `tests/mod.rs` (core CRUD, 230 lines), `tests/query.rs` (419 lines),
  `tests/edge.rs` (257 lines) organized by functional concern
- **Max file size** reduced from 922 to 826 lines

#### Verified

- **PII audit (Layer 4)** — clean: no emails, home paths, private IPs, or API
  keys in codebase; git authors use project identities
- **Coverage artifacts** — phantom 0% entries from stale profraw data eliminated
- **Arc\<str\> filter comparison** — `p.as_ref() == primal.as_str()` correctly
  compares `Arc<str>` against `String` in `memory/filter.rs`

### v0.7.24

#### Added

- **`CONTEXT.md`** — AI-readable context per PUBLIC_SURFACE_STANDARD Layer 3
- **`CONTRIBUTING.md`** — contributor guide with code standards, PR checklist

#### Changed

- **Zero-copy Phase 2** — `EcoPrimalsAttributes.source_primal` and `.niche`
  migrated from `Option<String>` to `Option<Arc<str>>` across all 10 crates;
  `LoamCommitRef.spine_id`, `BraidFactory` internals, `CompressionEngine`
  internals similarly migrated; O(1) atomic clone replaces O(n) heap allocation

---

## Current State

| Metric | Value |
|--------|-------|
| Tests | 1,128 passing |
| Coverage | ~90% lines (llvm-cov, excluding Postgres runtime) |
| JSON-RPC methods | 27 |
| Clippy | 0 warnings (pedantic + nursery) |
| Format | Clean |
| Docs | 0 warnings |
| cargo deny | advisories ok, bans ok, licenses ok, sources ok |
| Unsafe | 0 (`forbid(unsafe_code)` all crates) |
| Production unwraps | 0 (`unwrap_used`/`expect_used` = `deny`) |
| TODOs in source | 0 |
| Pure Rust deps | Confirmed |
| .rs files | 136 (39,903 LOC) |
| Max file | 826 lines (limit: 1000) |

---

## For Other Primals

- **90% coverage pattern**: Coverage artifacts from stale profraw data can
  inflate denominators by 20+ percentage points. Run `cargo llvm-cov clean
  --workspace` before measuring. Exclude phantom files from pre-refactor
  modules with `--ignore-filename-regex`.

- **Smart test refactoring**: When test files approach the 1000-line limit,
  split by functional concern (CRUD, query, edge cases) rather than arbitrary
  line counts. Use `tests/mod.rs` + sub-modules to maintain a single `#[cfg(test)]
  mod tests;` declaration in the parent.

- **PUBLIC_SURFACE_STANDARD compliance**: Layer 2 (README footer linking to
  wateringHole), Layer 3 (CONTEXT.md), Layer 4 (PII scan — grep for emails,
  home paths, private IPs, API keys, git author audit).

---

## Breaking Changes

None.

---

## What's Next

- Cross-compile CI (musl, ARM64, RISC-V)
- `ValidationHarness` + `BaselineProvenance` (healthSpring pattern)
- sunCloud economics integration
- Coverage expansion for Postgres store (Docker-gated)
