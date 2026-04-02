# biomeOS v2.67 — Remaining Debt Cleanup + Caller-Agnostic Lineage

**Date**: March 22, 2026
**Author**: biomeOS session
**Scope**: Final debt cleanup pass — type-parameter evolution, roster hardcoding, comprehensive codebase health scan

---

## Changes

### LineageDeriver Type-Parameter Evolution
- `load_lineage()` and `has_lineage()` promoted to module-level free functions in `biomeos-spore::beacon_genetics`
- Callers no longer need phantom type parameter (eliminates `LineageDeriver::<DirectBeardogCaller>::load_lineage()` pattern)
- `enroll.rs` now uses `load_lineage(&path)` directly
- Backward-compatible delegating methods retained on `LineageDeriver<C>` for existing callers

### Roster Evolution
- `checks_primal.rs` (doctor mode): `/5` hardcode → dynamic `primals.len()`, warning threshold also dynamic (`< expected / 2`)
- `tools/harvest`: `KNOWN_PRIMALS` normalized to lowercase filesystem convention (`petalTongue` → `petaltongue`), alphabetically sorted

### Comprehensive Debt Scan (v2.67 baseline)

| Category | Status |
|----------|--------|
| TODO/FIXME/HACK markers | **0** |
| `unsafe` in production | **0** (2 in test-utils only, mutex-guarded) |
| Clippy warnings | **0** (pedantic+nursery) |
| Tests | **7,135** passing, 0 failures |
| Files >1000 LOC | **0** (max production section: 648 lines) |
| `.unwrap()` in production | **0** (all 2,409 instances verified inside `#[cfg(test)]`) |
| C dependencies | **0** |

---

## Impact on Ecosystem

- **primalSpring**: No new API changes; all v2.66 alignment holds
- **Other primals**: Free function `load_lineage()` simplifies integration for any primal loading lineage metadata without constructing a full `LineageDeriver`
- **Tooling**: `harvest` now uses correct lowercase socket naming convention

## Files Changed

| File | Change |
|------|--------|
| `biomeos-spore/beacon_genetics/derivation/lineage_deriver.rs` | `load_lineage`, `has_lineage` as free functions |
| `biomeos-spore/beacon_genetics/derivation/mod.rs` | Re-export free functions |
| `biomeos-spore/beacon_genetics/mod.rs` | Re-export free functions |
| `biomeos/src/modes/enroll.rs` | Use free function |
| `biomeos/src/modes/doctor/checks_primal.rs` | Dynamic count |
| `tools/harvest/src/main.rs` | Lowercase convention |
| `README.md`, `CURRENT_STATUS.md`, `CHANGELOG.md`, `QUICK_START.md`, `DOCUMENTATION.md` | v2.67 |
