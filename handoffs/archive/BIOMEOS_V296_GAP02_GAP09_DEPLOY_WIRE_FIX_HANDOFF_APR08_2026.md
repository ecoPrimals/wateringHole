# biomeOS v2.96 — GAP-02 + GAP-09: Deploy Parser Unification & Wire Method Correction

**Date**: April 8, 2026
**From**: biomeOS
**To**: primalSpring, sweetGrass, all primals
**Status**: All critical + medium + low gaps resolved

---

## Summary

Resolves the two remaining items from the primalSpring downstream audit GAP-MATRIX:

1. **GAP-02 (Medium)**: `biomeos deploy` now accepts both graph formats
2. **GAP-09 (Low)**: Attribution domain wire methods corrected for sweetGrass v0.7.5

Additionally fixes 2 environment-dependent test failures that surfaced when primals are running during test execution.

---

## GAP-02: Deploy Path Unified

### Problem
`biomeos deploy tower_atomic_bootstrap.toml` failed because the deploy CLI used only `GraphLoader::from_file()` (expects `[[graph.nodes]]` DeploymentGraph format), but the bootstrap graph uses `[[nodes]]` (neural_graph format).

### Fix
`crates/biomeos/src/modes/deploy.rs` now tries `GraphLoader` first, then falls back to `neural_graph::Graph::from_toml_file()`. Both paths produce a unified `LoadedGraphInfo` struct for validation, dry-run, and display.

### Verification
- 2 new tests: `test_run_neural_graph_format`, `test_run_neural_graph_dry_run`
- `biomeos deploy --validate graphs/tower_atomic_bootstrap.toml` succeeds

---

## GAP-09: Wire Method Correction

### Problem
`defaults.rs` translation table mapped semantic `braid.create` to method `provenance.create_braid`, but sweetGrass v0.7.5 expects wire method `braid.create`. The mismatch caused `-32601 Method Not Found` when routing through capability.call.

### Fix
All attribution domain translations now emit the correct wire method names:

| Semantic Key | Before (wrong) | After (correct) |
|---|---|---|
| `provenance.create_braid` | `provenance.create_braid` | `braid.create` |
| `provenance.get_braid` | `provenance.get_braid` | `braid.get` |
| `attribution.create` | `provenance.create_braid` | `braid.create` |
| `attribution.get` | `provenance.get_braid` | `braid.get` |
| `braid.create` | `provenance.create_braid` | `braid.create` |
| `braid.get` | `provenance.get_braid` | `braid.get` |

Source of truth: `config/capability_registry.toml` `[translations.attribution]`

---

## Test Stability Fix

`NeuralRouter::lazy_rescan_sockets()` scans the host filesystem for primal sockets. When primals (e.g. beardog) are running during tests, this causes false positives in tests that expect empty registries.

Fix: `lazy_rescan_attempted` field promoted to `pub(crate)`, allowing test setup to disable the rescan. Applied to:
- `test_discover_by_category_empty_registry_security`
- `test_semantic_fallback_routes_through_capability_call`

---

## Files Changed

| File | Change |
|---|---|
| `crates/biomeos/src/modes/deploy.rs` | Dual-format graph loading with fallback |
| `crates/biomeos-atomic-deploy/src/capability_translation/defaults.rs` | Wire method names corrected |
| `crates/biomeos-atomic-deploy/src/neural_router/mod.rs` | `lazy_rescan_attempted` → `pub(crate)` |
| `crates/biomeos-atomic-deploy/src/neural_router/discovery.rs` | Test isolation for socket scan |
| `crates/biomeos-atomic-deploy/src/neural_api_server/routing_tests.rs` | Test isolation for socket scan |

---

## Metrics

- Tests: **7,660** passing (0 failures, +2 new)
- Clippy: PASS (0 warnings, `-D warnings`)
- GAP-MATRIX status: **All items resolved** (GAP-01 through GAP-09)
