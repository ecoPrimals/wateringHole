<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# rhizoCrypt v0.13.0-dev — Edition 2024 + Niche Standard Handoff

**Date**: March 15, 2026 (session 10)
**Primal**: rhizoCrypt v0.13.0-dev
**Status**: Production Ready

---

## Summary

Absorbed patterns from the spring ecosystem (wetSpring, airSpring, healthSpring) to evolve rhizoCrypt to Edition 2024, comply with the Spring-as-Niche Deployment Standard, and synchronize wateringHole documentation.

---

## Changes

### Edition 2024 Migration
- Workspace, fuzz, and showcase Cargo.toml all set to `edition = "2024"`, `rust-version = "1.87"`
- 183 `std::env::set_var`/`remove_var` calls wrapped in `unsafe {}` (Edition 2024 requirement)
- Workspace lint changed from `forbid` to `deny` for `unsafe_code`; `forbid` preserved in non-test builds via `#[cfg_attr(not(test), forbid(unsafe_code))]`
- 10 nested `if`/`if let` chains collapsed into Edition 2024 `if let` chains
- Edition 2024 `rustfmt` import reordering applied (types before modules)

### biomeOS Niche Standard Compliance
- `graphs/rhizocrypt_deploy.toml` — 5-node deploy graph (BearDog → Songbird → rhizoCrypt → LoamSpine → sweetGrass)
- `capability_registry.toml` — 23 JSON-RPC methods across 7 domains

### `#[expect()]` Lint Migration
- 5 production `#[allow(clippy::...)]` migrated to `#[expect(clippy::...)]`
- 1 stale suppression caught and removed (`missing_const_for_fn` on `RateLimiter::disabled()`)

### wateringHole Documentation Sync
- `SPRING_PROVENANCE_TRIO_INTEGRATION_PATTERN.md`: fixed stale method names
- `RHIZOCRYPT_LEVERAGE_GUIDE.md`: updated to 23 current semantic method names
- `PRIMAL_REGISTRY.md`: updated rhizoCrypt entry

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy` (pedantic + nursery + cargo) | Clean (0 warnings) |
| `cargo doc --workspace --all-features --no-deps` | Clean |
| `cargo test --workspace --all-features` | 1177 pass, 0 fail |
| `cargo deny check` | Clean |
| `unsafe_code = "deny"` | Workspace-wide |
| SPDX headers | All 106 `.rs` files |
| Max file size | All under 1000 lines |

---

## Spring Absorption Analysis

Reviewed all six ecoSprings (hot, ground, neural, wet, air, health) for patterns to absorb:

| Absorbed | Source | Detail |
|----------|--------|--------|
| Edition 2024 | wetSpring, airSpring, healthSpring | `rust-version = "1.87"` |
| Deploy graph | airSpring | `graphs/rhizocrypt_deploy.toml` |
| Capability registry | wetSpring | `capability_registry.toml` |
| `#[expect()]` over `#[allow()]` | wetSpring V117 | Caught 1 stale suppression |
| Method name sync | — | wateringHole doc fix only |

No science code absorption needed — rhizoCrypt is infrastructure, springs route via `capability.call("dag", ...)`.

---

## Remaining Debt (for future sessions)

- Evolve flaky `test_stats_after_operations` in sled tests (sled `size_on_disk()` non-deterministic)
- `provenance-trio-types` advisory tracking (transitive from tarpc)
- Production readiness: stress-test deploy graph with biomeOS in real niche composition
