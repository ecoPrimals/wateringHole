# SweetGrass v0.7.12 — Edition 2024 Migration + Spring Absorption + Chaos Tests

**Date**: March 15, 2026
**From**: v0.7.11 → v0.7.12
**Status**: Complete — all checks pass
**License**: AGPL-3.0-only
**Supersedes**: `SWEETGRASS_V0711_JSONRPC_SPEC_COMPLIANCE_DEEP_DEBT_HANDOFF_MAR15_2026.md`

---

## Summary

Edition 2024 migration with MSRV 1.87, adopting let-chains, safe env var
handling in tests, and resolver 3. Cross-spring pattern absorption from
airSpring (capability niche architecture), groundSpring (chaos/fault testing),
and biomeOS V2.39 (env var safety). Capability descriptors evolved with
dependency/cost metadata for intelligent niche dispatch.

---

## Edition 2024 Migration

### Workspace changes

```toml
# Before
edition = "2021"
resolver = "2"

# After
edition = "2024"
rust-version = "1.87"
resolver = "3"
```

### Let-chains adoption

Edition 2024 stabilizes let-chains, enabling `if let ... && condition { }`.
8 collapsible_if patterns modernized:

| File | Pattern |
|------|---------|
| `factory/attribution/mod.rs` | Derivation loop + parent resolve |
| `factory/attribution/mod.rs` | Role inference from activity |
| `store/memory/filter.rs` | Time range matching (2 patterns) |
| `store/memory/indexes.rs` | Derivation index cleanup |
| `query/provo.rs` | Compute unit inclusion |
| `query/traversal.rs` | Activity inclusion |
| `store-postgres/store/mod.rs` | Activity deserialization |
| `store-redb/store/mod.rs` | Filter matching (7 patterns) |
| `store-sled/store/mod.rs` | Filter matching (4 patterns) |
| `service/uds.rs` | Parent directory creation |

**Inter-primal pattern**: Upgrade to Edition 2024. Collapse nested `if let` + `if`
patterns to let-chains for clarity and clippy compliance.

### Env var safety

`std::env::set_var`/`remove_var` are `unsafe` in Edition 2024. Strategy:

1. **Workspace lint**: `unsafe_code = "deny"` (was `"forbid"`)
2. **Production crates**: `#![cfg_attr(not(test), forbid(unsafe_code))]` +
   `#![cfg_attr(test, deny(unsafe_code))]`
3. **Test modules**: `#[allow(unsafe_code)]` + `unsafe { std::env::set_var(...) }`

This preserves zero unsafe in production while allowing test modules to
use env mutation (serialized via `#[serial]`).

**Inter-primal pattern**: For Edition 2024, do NOT add `unsafe` blocks to
production code. Wrap env mutations in `unsafe { }` only in `#[cfg(test)]`
modules with `#[allow(unsafe_code)]` and `#[serial]`.

---

## Capability Niche Architecture (from airSpring)

`capability.list` now returns per-operation metadata:

```json
{
  "primal": "sweetgrass",
  "version": "0.7.12",
  "protocol": "jsonrpc-2.0",
  "transport": ["http", "uds"],
  "domains": { "braid": ["create", "get", ...], ... },
  "methods": ["braid.create", ...],
  "operations": {
    "braid.create": { "depends_on": [], "cost": "low" },
    "braid.commit": { "depends_on": ["braid.create"], "cost": "medium" },
    "attribution.chain": { "depends_on": ["braid.create"], "cost": "high" },
    ...
  }
}
```

New fields:
- `protocol`: Transport protocol identifier
- `transport`: Supported transport types
- `operations`: Per-method dependency graph and cost hints

**Inter-primal pattern**: All primals should evolve `capability.list` to include
`depends_on` (operation dependency graph) and `cost` (low/medium/high) metadata.
This enables biomeOS to construct intelligent dispatch graphs.

---

## Chaos/Fault Tests (from groundSpring)

11 chaos tests for attribution calculations:

| Test | Scenario |
|------|----------|
| `chaos_zero_weight_config` | Empty role_weights HashMap |
| `chaos_extreme_decay_factor_zero` | decay_factor = 0.0 |
| `chaos_extreme_decay_factor_one` | decay_factor = 1.0 |
| `chaos_zero_min_share` | min_share = 0.0 |
| `chaos_max_depth_zero` | max_depth = 0 with derivation chain |
| `chaos_empty_contributors_normalize` | Normalize empty chain |
| `chaos_single_zero_share_normalize` | Normalize chain with 0.0 shares |
| `chaos_rewards_zero_value` | Calculate rewards with 0.0 total |
| `chaos_rewards_large_value` | Calculate rewards with f64::MAX/2 |
| `chaos_many_contributors` | 100 contributors, normalize |
| `chaos_deep_derivation_chain` | 20-deep chain (capped by max_depth) |

All tests verify `is_finite()` on computed values.

**Inter-primal pattern**: Add chaos/fault tests for any calculation involving
floats, weights, or recursive structures. Test with 0.0, 1.0, f64::MAX/2,
empty inputs, and large collections.

---

## Hardcoding Eliminated

| Constant | Value | Was hardcoded in |
|----------|-------|------------------|
| `identity::DEFAULT_REDB_PATH` | `"./data/sweetgrass.redb"` | `factory/mod.rs` (4 locations) |
| `identity::DEFAULT_SLED_PATH` | `"./data/sweetgrass"` | `factory/mod.rs` (2 locations) |

---

## Files Modified

| Crate | Files | Changes |
|-------|-------|---------|
| Workspace | `Cargo.toml` | Edition 2024, MSRV 1.87, resolver 3, `unsafe_code = "deny"` |
| `sweet-grass-core` | `lib.rs` | `cfg_attr` unsafe pattern, `DEFAULT_REDB_PATH`, `DEFAULT_SLED_PATH` |
| `sweet-grass-core` | `config/tests.rs`, `primal_info.rs` | `unsafe` env wrappers |
| `sweet-grass-service` | `lib.rs`, `factory/*`, `handlers/*`, `uds.rs`, `bootstrap.rs`, `server/tests.rs` | `cfg_attr` unsafe, `unsafe` env wrappers, let-chains |
| `sweet-grass-factory` | `attribution/mod.rs`, `attribution/tests.rs` | Let-chains, 11 chaos tests |
| `sweet-grass-store` | `memory/filter.rs`, `memory/indexes.rs` | Let-chains |
| `sweet-grass-store-redb` | `store/mod.rs` | Let-chains (7 patterns) |
| `sweet-grass-store-sled` | `store/mod.rs` | Let-chains (4 patterns) |
| `sweet-grass-store-postgres` | `lib.rs`, `store/mod.rs`, `store/tests.rs` | `cfg_attr` unsafe, let-chains |
| `sweet-grass-query` | `provo.rs`, `traversal.rs` | Let-chains |
| `sweet-grass-integration` | `lib.rs`, `anchor.rs`, `listener/*`, `discovery/tests.rs` | `cfg_attr` unsafe, test env wrappers |

---

## Metrics

| Metric | v0.7.11 | v0.7.12 |
|--------|---------|---------|
| Tests | 892 | **903** |
| Edition | 2021 | **2024** |
| MSRV | — | **1.87** |
| Chaos tests | 17 (service) | **28** (+11 attribution) |
| Hardcoded paths | 2 | **0** |
| Let-chains | 0 | **8 patterns** |
| Unsafe in production | 0 | 0 |
| Clippy warnings | 0 | 0 |
| Max file | 804L | **808L** |

---

## Deferred

- **Provenance trio session lifecycle** — `begin`/`record`/`complete` helpers
  require coordination with rhizoCrypt and loamSpine wire types. Deferred.
- **Zero-copy serde borrowing** — Lifetime threading through store traits.
  Deferred to v0.8.0+.
- **Showcase script modernization** — Obsolete CLI flags. Separate pass.

---

## Verification

```
cargo fmt --all -- --check         ✓
cargo check --workspace            ✓ (0 warnings)
cargo clippy --workspace --all-targets --all-features -- -D warnings  ✓ (0 warnings)
cargo test --workspace             ✓ (903 tests)
cargo doc --workspace --no-deps    ✓ (0 warnings)
```
