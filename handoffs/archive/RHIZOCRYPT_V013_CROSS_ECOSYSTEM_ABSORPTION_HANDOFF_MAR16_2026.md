<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# rhizoCrypt v0.13.0-dev — Cross-Ecosystem Absorption Handoff

**Date**: March 16, 2026 (session 11)
**Primal**: rhizoCrypt v0.13.0-dev
**Status**: Production Ready

---

## Summary

Absorbed 8 patterns from ecosystem springs and sibling primals into rhizoCrypt:
niche self-knowledge, enhanced capability descriptors, `temp-env` test isolation,
deploy graph fallback, CI coverage threshold, workspace lint strictness,
`#[expect(reason)]` audit trail, and wateringHole documentation sync.

---

## Changes

### 1. Niche Self-Knowledge Module (`niche.rs`)
- Created `crates/rhizo-crypt-core/src/niche.rs` — single source of truth for primal identity, capabilities, consumed capabilities, cost estimates, operation dependencies, and semantic mappings
- `capability.list` now sources all data from `niche.rs` instead of hardcoded inline vectors
- 11 niche module tests (consistency, cross-reference, domain validation)
- **Absorbed from**: squirrel, neuralSpring, groundSpring, airSpring

### 2. Enhanced `capability.list` Response
- `CapabilityDescriptor` now includes per-method `MethodDescriptor` with `cost` tier (low/medium/high) and `deps` (prerequisite operations)
- biomeOS Pathway Learner can optimize graph execution order for rhizoCrypt
- `build_capability_descriptors()` builds response from `niche.rs` constants
- **Absorbed from**: loamSpine, sweetGrass

### 3. `temp-env` for Test Isolation
- Replaced all 183 `unsafe { std::env::set_var/remove_var }` blocks across 7 files with `temp_env::with_vars`
- Eliminated all `#[allow(unsafe_code)]` from test modules — zero `unsafe` in entire codebase
- Removed all `ENV_LOCK` / `ENV_TEST_LOCK` static mutexes and manual cleanup helpers
- Added `temp-env = "0.3"` as workspace dev-dependency
- **Absorbed from**: squirrel, groundSpring

### 4. Deploy Graph `fallback = "skip"`
- Added `fallback = "skip"` to all 4 optional nodes in `graphs/rhizocrypt_deploy.toml`
- biomeOS ConditionalDag now gracefully skips unavailable optional dependencies
- **Absorbed from**: wetSpring

### 5. CI Coverage Threshold
- Added `--fail-under-lines 90` to CI coverage job in `.github/workflows/ci.yml`
- Prevents coverage regressions below 90%
- **Absorbed from**: beardog, biomeOS, barraCuda

### 6. Workspace Lint Strictness
- Upgraded `unwrap_used` and `expect_used` from `"warn"` to `"deny"` in workspace lints
- Production code already had zero instances; this prevents regressions
- **Absorbed from**: ludoSpring, squirrel, provenance-trio-types

### 7. `#[expect(reason = "...")]` Strings
- Added `reason = "..."` strings to all 4 `#[expect()]` attrs in production code
- Documents *why* each lint suppression exists for audit trail
- **Absorbed from**: toadstool, loamSpine

### 8. Root & wateringHole Documentation
- Updated README, CHANGELOG, DEPLOYMENT_CHECKLIST, showcase/README with current metrics
- Updated `RHIZOCRYPT_LEVERAGE_GUIDE.md` with niche self-knowledge and enhanced capability.list format
- Updated `PRIMAL_REGISTRY.md` with post-absorption status
- Fixed stale script references in showcase (demo-quick-start.sh, demo-real-discovery.sh)

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy` (pedantic + nursery + cargo, all features) | Clean (0 warnings) |
| `cargo doc --workspace --all-features --no-deps` | Clean |
| `cargo test --workspace --all-features` | 1188+ pass, 0 fail |
| `cargo deny check` | Clean |
| `unsafe_code = "deny"` | Workspace-wide (zero unsafe in tests via temp-env) |
| `unwrap_used`/`expect_used` | `"deny"` workspace-wide |
| Coverage gate | `--fail-under-lines 90` CI enforced |
| SPDX headers | All 106 workspace `.rs` files |
| Max file size | All under 1000 lines |
| Production unwrap/expect | Zero |

---

## Codebase Health

| Metric | Value |
|--------|-------|
| Tests | 1188+ (all features) |
| Coverage | 91.47% line (llvm-cov) |
| `.rs` files | 106 workspace + 4 showcase |
| Crates | 3 (rhizo-crypt-core, rhizo-crypt-rpc, rhizocrypt-service) |
| Edition | 2024 (rust-version 1.87) |
| TODOs/FIXMEs in source | 0 |
| `ENV_LOCK` mutexes | 0 (eliminated via temp-env) |

---

## Remaining Debt (for future sessions)

- Evolve flaky `test_stats_after_operations` in sled tests (sled `size_on_disk()` non-deterministic)
- `provenance-trio-types` advisory tracking (transitive from tarpc)
- Stress-test deploy graph with biomeOS in real niche composition
- 4 showcase `.rs` files missing SPDX headers (standalone demo pseudocode)
- tarpc ops count inconsistency: README says "24 ops", capability_registry has 23 methods
