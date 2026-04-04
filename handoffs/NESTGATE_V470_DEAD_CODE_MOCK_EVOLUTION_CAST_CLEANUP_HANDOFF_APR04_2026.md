# NestGate v4.7.0-dev — Dead Code Deletion, Mock Evolution & Cast Cleanup

**Date**: April 4, 2026  
**Primal**: NestGate (Storage / Permanence)  
**Session**: 22  
**Trigger**: Deep debt execution — production mocks, orphan files, unsafe casts  

---

## Actions Taken

### 1. Dead Code Deletion — Orphan Files (~4,318 lines)

A module-tree audit found production `.rs` files on disk that were never declared in any
`mod.rs`, meaning they were never compiled. All were deleted:

| Location | Files | Lines |
|----------|-------|-------|
| `performance_dashboard/{core,zfs_integration,http_handlers}.rs` | 3 | 984 |
| `performance_dashboard/analyzer/` subtree | 5 | 1,696 |
| `performance_dashboard/endpoints/` subtree | 3 | 124 |
| `rest/rpc/{universal_rpc_router,capability_based_router,primal_agnostic_rpc}.rs` | 3 | 1,399 |
| `load_testing/handlers.rs` | 1 | 115 |
| **Total** | **15** | **~4,318** |

Notable: `zfs_integration.rs` contained hardcoded mock ZFS data (fabricated ARC stats,
trend data, growth rates), copy-paste error messages (`"self.base_url"`), and `.await`
calls on sync functions. It was never compiled.

### 2. Production Mock Evolution

**`credential_validation.rs` `authenticate()`**:
- **Before**: Issued a demo token for any username (always `success: true`)
- **After**: Returns `success: false` — identity provider not yet wired
- Dead `AuthToken` and `TokenType` types removed from `auth_manager.rs`

### 3. Automation Integration Deprecation

**`nestgate-zfs/automation/integration.rs`**:
- Shell types `IntelligentDatasetManager` and `AutomationConfig` marked `#[deprecated(since = "4.7.0")]`
- Migration note points to `DatasetAutomation::new()` from the engine module
- Redundant tests removed (5 → 2)

### 4. `as` Cast Evolution (idiomatic Rust)

Narrowing `as u32` casts replaced with `u32::try_from().unwrap_or(u32::MAX)`:

| File | Cast | Risk |
|------|------|------|
| `automation/engine.rs` | `count() as u32`, `len() as u32` | Truncation if >4B items |
| `metrics_collector/collector.rs` | `n.get() as u32` (CPU cores) | Truncation if >4B cores |
| `metrics_collector/collector.rs` | `(mem_total_kb / ...) as u32` (GB) | Truncation if >4 PB RAM |

---

## Verification

```
cargo fmt --all -- --check    → PASS
cargo clippy --workspace --all-features -- -D warnings → PASS (0 warnings)
cargo test --workspace        → 12,236 passed, 0 failed, 471 ignored
```

Test delta: -4 (3 removed redundant integration tests + 1 consolidated auth test).

---

## Files Modified

### Deleted (15 files, ~4,318 lines)
- `code/crates/nestgate-api/src/handlers/performance_dashboard/core.rs`
- `code/crates/nestgate-api/src/handlers/performance_dashboard/zfs_integration.rs`
- `code/crates/nestgate-api/src/handlers/performance_dashboard/http_handlers.rs`
- `code/crates/nestgate-api/src/handlers/performance_dashboard/analyzer/` (5 files)
- `code/crates/nestgate-api/src/handlers/performance_dashboard/endpoints/` (3 files)
- `code/crates/nestgate-api/src/rest/rpc/universal_rpc_router.rs`
- `code/crates/nestgate-api/src/rest/rpc/capability_based_router.rs`
- `code/crates/nestgate-api/src/rest/rpc/primal_agnostic_rpc.rs`
- `code/crates/nestgate-api/src/handlers/load_testing/handlers.rs`

### Evolved
- `code/crates/nestgate-api/src/handlers/auth_production/credential_validation.rs`
- `code/crates/nestgate-api/src/handlers/auth_production/auth_manager.rs`
- `code/crates/nestgate-zfs/src/automation/integration.rs`
- `code/crates/nestgate-zfs/src/automation/engine.rs`
- `code/crates/nestgate-api/src/handlers/metrics_collector/collector.rs`

### Documentation updated
- `STATUS.md`, `CHANGELOG.md`, `README.md`, `CONTRIBUTING.md`, `START_HERE.md`
- `QUICK_REFERENCE.md`, `QUICK_START.md`, `CONTEXT.md`
- `tests/README.md`, `tests/DISABLED_TESTS_REFERENCE.md`

---

## Remaining Deep Debt

| Category | Status |
|----------|--------|
| Orphan test files (`*_tests.rs` not in mod tree) | ~15 files identified — low priority, inert |
| `#[allow(deprecated)]` suppressions | Many — active migration from old config types |
| `#[allow(dead_code)]` in `rest/rpc/manager/` | Production reservation — documented rationale |
| `as f64` ratio casts | Standard for display math — low risk |
| `dev-stubs` feature tree | Gated behind opt-in feature — acceptable |
| `get_arc_stats_fallback()` in observe | Feature-gated `mock-metrics` — not default build |
