# NestGate v4.7.0 — Deep Debt: Dependencies, Host Discovery, Dead Code

**Date**: April 4, 2026
**Scope**: Dependency rationalization, localhost→configurable host, dead code removal, RNG consolidation
**Verification**: Clippy CLEAN, fmt PASS, 12,088 tests (0 failures, ~468 ignored)

---

## Changes

### Dependency Rationalization

| Crate | Removed | Kept/Added | Reason |
|-------|---------|------------|--------|
| nestgate-core | `log`, `getrandom`, `rand` | `fastrand` (already present) | `log` unused (tracing-only); `getrandom` unused; `rand` replaced by `fastrand` |
| nestgate-rpc | `fastrand` (dev-deps) | — | Never used in any `.rs` file |
| nestgate-zfs | `rand` (dependencies) | `rand` (dev-deps only) | Not used in production code, only tests |
| nestgate-network | `rand` | `fastrand` | Load balancer migrated |

**Impact**: Production crates are now `rand`-free. `rand` remains only in test/dev dependencies where test code requires distributions. `log` facade eliminated — workspace is tracing-only.

### RNG Migration: `rand::StdRng` → `fastrand`

Load balancing does not require crypto-grade randomness. Migrated:
- `RandomLoadBalancer` — removed `Arc<Mutex<StdRng>>`, replaced with `fastrand::usize(..)`
- `WeightedRandomLoadBalancer` — same: removed `StdRng` field, replaced `gen_range`/`gen::<f64>()` with `fastrand::usize(..)`/`fastrand::f64()`
- `nestgate-network` `LoadBalancingStrategy::Random` — `rand::thread_rng().gen_range()` → `fastrand::usize(..)`

Benefits: no Mutex contention, lighter dependency tree, correct semantic (non-crypto for routing).

### Localhost Hardcoding → Configurable Host Discovery

**Problem**: `capability_port_discovery.rs` and `primal_discovery/migration.rs` hardcoded `"http://localhost:{port}"` when building service URLs from discovered ports. This is incorrect for non-loopback deployments.

**Fix**: All service URL construction now uses `canonical_defaults::network::discovery_default_host()`:
- Resolution order: `NESTGATE_DEV_HOST` → `NESTGATE_DISCOVERY_FALLBACK_HOST` → `localhost` (with tracing warning)
- Made `discovery_default_host()` public for reuse
- Applied to: `try_discover_api_service`, `try_discover_metrics_service`, `try_discover_storage_service`, `try_environment`, `try_default`

### Dead Code Removal

`optimization.rs` `request_ai_optimization`: Removed dead `if let Ok(...)` block that built a JSON object, threw it away (`let _ = request_data`), logged a warning, and contained an `if false {}` stub. Replaced with honest delegation debug log pointing to `capability.call("ai", ...)`.

## Files Changed

- `nestgate-core/Cargo.toml` — removed `log`, `getrandom`, `rand`
- `nestgate-core/src/traits/load_balancing/algorithms.rs` — `rand` → `fastrand`
- `nestgate-core/src/traits/load_balancing/weighted.rs` — `rand` → `fastrand`
- `nestgate-network/Cargo.toml` — `rand` → `fastrand`
- `nestgate-network/src/handlers/load_balancer.rs` — `rand` → `fastrand`
- `nestgate-rpc/Cargo.toml` — removed unused `fastrand`
- `nestgate-zfs/Cargo.toml` — removed unused `rand` from `[dependencies]`
- `nestgate-config/src/constants/canonical_defaults.rs` — `discovery_default_host()` made public
- `nestgate-config/src/constants/capability_port_discovery.rs` — use configurable host
- `nestgate-discovery/src/primal_discovery/migration.rs` — use configurable host
- `nestgate-api/src/handlers/workspace_management/optimization.rs` — dead code removed

---

*Last Updated: April 4, 2026*
