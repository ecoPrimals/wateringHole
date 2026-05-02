# biomeOS v3.35 — Deep Debt: EVOLVED Purge, node_handlers Refactor, Dead Code Gating

**Date**: April 30, 2026
**From**: biomeOS team
**To**: All downstream springs and primals
**Status**: Committed and pushed

---

## Summary

v3.35 removes ~30 stale refactor markers, smart-refactors the largest remaining production file, and gates dead code behind `#[cfg(test)]`.

## Changes

### Stale EVOLVED comment purge (14 files, 9 crates)

Removed all dated `EVOLVED (Jan 27, 2026)` and `EVOLVED (Feb 2026)` comments from production code. These served as refactor markers during the January 2026 debt sweep but had become noise. Affected crates: `biomeos`, `biomeos-api`, `biomeos-atomic-deploy`, `biomeos-cli`, `biomeos-core`, `biomeos-graph`, `biomeos-nucleus`, `biomeos-spore`, `biomeos-ui`.

### Smart refactor: node_handlers.rs (791→504 lines, −36%)

- Extracted 287-line `#[cfg(test)] mod tests` block into dedicated `executor/node_handlers_tests.rs`
- Added `resolve_family_id()` helper to DRY 3 duplicated family-ID resolution patterns (env lookup → `biomeos_core::family_discovery::get_family_id()` fallback)
- Cleaned undated `EVOLVED:` markers from module and executor headers

### Dead code gating

- `load_graphs_from_dir` in `biomeos-graph/src/loader.rs`: `pub` → `#[cfg(test)] pub(crate)` (was only called from its own test module)

## Verification

- `cargo check` — PASS
- `cargo clippy -- -D warnings` — PASS (0 warnings)
- `cargo fmt --check` — PASS
- `cargo test -p biomeos-graph` — 267 passed, 0 failed
- `cargo test -p biomeos-atomic-deploy` — 1214 passed, 13 pre-existing env-dependent failures

## No action required by downstream

These changes are internal to biomeOS. No API, wire format, or behavioral changes.

---

*biomeOS v3.35 | AGPL-3.0-or-later | ecoPrimals Project*
