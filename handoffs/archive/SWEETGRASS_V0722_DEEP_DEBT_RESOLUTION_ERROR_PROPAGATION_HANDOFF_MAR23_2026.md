# sweetGrass v0.7.22 — Deep Debt Resolution, Error Propagation & Standards Compliance

**Date**: March 23, 2026
**From**: sweetGrass
**To**: rhizoCrypt, loamSpine, biomeOS, all primals
**Status**: Released
**Previous**: v0.7.22 Sovereignty handoff (Mar 17, 2026)

---

## Summary

Comprehensive audit and deep debt resolution sprint across the entire sweetGrass
workspace. Security advisory fixed, silent error swallowing eliminated, type safety
strengthened, store implementations completed, allocation patterns optimized, and
all lint suppressions removed from production code. 27 files modified, zero
regressions.

---

## Changes

### Security
- **RUSTSEC-2026-0049**: Updated `rustls-webpki` 0.103.8 → 0.103.10 (CRL matching logic flaw in testcontainers dep chain)
- **Stale advisory ignore**: Removed `RUSTSEC-2024-0387` from `deny.toml` (no longer matches any crate)
- **`publish = false`**: Added to all 10 workspace crates (not published; fixes cargo-deny wildcard bans)

### Error Propagation (Silent Failures → Explicit Errors)
- **Postgres count query**: `unwrap_or(0)` on `Result` → proper `map_err` error propagation
- **Postgres `row_to_activity`**: 4 `serde_json::from_value().unwrap_or_default()` → error propagation with descriptive context (`"activity used_entities"`, `"activity metadata"`, etc.)

### Type Safety Evolution
- **`ContributionRecord.content_hash`**: `String` → `ContentHash` newtype across core, factory, and all test sites
- **`Capability::from_string`**: `to_lowercase()` allocation → `eq_ignore_ascii_case` (zero allocation for known variants)
- **`hex_encode`**: `fold` + `write!` → const lookup table (branchless, pre-allocated)

### Store Implementation Completion
- **`activities_for_braid` in sled and redb**: Was returning empty `Vec`; now extracts generating activity via `Option::and_then` + `into_iter().collect()`

### Dead Code → Active Use
- **Pipeline handler wire types**: `agent_did`, `description`, `weight` fields were deserialized but unused; now actively stored in braid attribution metadata
- **All `#[allow(dead_code)]`** removed from non-test production code
- **All `#[allow(missing_errors_doc)]`** removed; `# Errors` docs added to 11 public methods

### Documentation
- **`# Errors` sections**: Added to all public `Result`-returning methods in redb, sled, and postgres store crates
- **Spec alignment**: `PRIMAL_SOVEREIGNTY.md` tarpc version 0.34 → 0.37
- **README**: Updated quality table (1,084 tests, 90.0% coverage, cargo deny status)
- **CHANGELOG**: Added Unreleased section with full change inventory
- **CLI output**: `println!` → `writeln!(stdout.lock())` in service binary

---

## Current State

| Metric | Value |
|--------|-------|
| Tests | 1,084 passing |
| Coverage | 90.0% lines (llvm-cov) |
| Clippy | 0 warnings (pedantic + nursery + cargo) |
| Format | Clean |
| Docs | 0 warnings (`-D warnings`) |
| cargo deny | advisories ok, bans ok, licenses ok, sources ok |
| Max file | 808 lines (all under 1000) |
| .rs files | 133 (38,819 LOC) |
| Unsafe | 0 (`forbid(unsafe_code)` all crates) |
| Production unwraps | 0 (`unwrap_used`/`expect_used` = `deny`) |
| `#[allow(dead_code)]` in prod | 0 |
| `#[allow(missing_errors_doc)]` | 0 |
| Cross-primal deps | 0 (sovereign wire types) |
| TODOs in source | 0 |

---

## Audit Summary (Clean)

| Check | Result |
|-------|--------|
| TODO/FIXME/HACK/XXX in `.rs` | None |
| `unsafe` blocks in code | None |
| unwrap/expect in production | None |
| Mocks in production | None (all `#[cfg(test)]` gated) |
| Hardcoded primal names in prod | None (centralized in `primal_names.rs`) |
| `#[allow(` in production | None |
| Silent error swallowing in prod | None (row_mapping, count query fixed) |
| Stub implementations | None (activities_for_braid completed) |

---

## For Other Primals

- **Error propagation pattern**: `unwrap_or_default()` on `serde_json::from_value()` silently swallows parse errors; prefer `map_err` with context strings
- **`publish = false` pattern**: Non-published workspace crates should set this to fix cargo-deny wildcard bans
- **`eq_ignore_ascii_case` pattern**: Avoids allocation for case-insensitive capability parsing (no `to_lowercase()`)
- **Const LUT hex encoding**: Branchless pattern for hex encoding without `fmt::Write` overhead
- **`activities_for_braid` via `was_generated_by`**: Embedded stores (redb, sled) can extract the braid's generating activity without a separate join table

---

## Breaking Changes

None. All changes are backward-compatible. JSON wire formats unchanged.

---

## What's Next

- Content Convergence implementation (`CONTENT_CONVERGENCE.md` spec)
- Cross-compile CI (musl, ARM64, RISC-V)
- GraphQL/SPARQL query endpoints (aspirational, per spec)
- sunCloud economics integration
- Coverage expansion on postgres store and service binary (Docker-gated tests)
