# ToadStool S187 — Deep Debt Execution: Mocks, Concurrency, Capability Naming

**Date**: April 5, 2026
**Session**: S187
**Primal**: toadStool
**Quality**: 21,515 tests (0 failures), Clippy clean, fmt clean, doc clean (0 warnings)
**Test runtime**: ~2m30s (was ~9min)

---

## Summary

Comprehensive deep debt execution across four major areas: production mock isolation,
test concurrency evolution, cross-primal name capability-first evolution, and external
dependency analysis. All quality gates green.

## 1. Production Mock Isolation

Production mocks (`MockResourceMonitor`, `MockSecurityProvider`, `MockPrimal`)
isolated behind `#[cfg(any(test, feature = "test-mocks"))]` in server, distributed,
and integration crates. Added `test-mocks` feature (non-default) to 3 crate manifests.
No production code paths depended on mock types — clean separation confirmed.

## 2. Test Concurrency Evolution

### Test Performance: 9min → 2m30s
- Removed global `RUST_TEST_THREADS=4` throttle from `.cargo/config.toml`
- Implemented `cfg!(test)` conditional timeouts:
  - mDNS discovery: 50ms (test) vs 3s (production)
  - TCP connect probes: 100ms (test) vs 2-5s (production)
- `ServiceDiscovery` cache-aware refresh prevents redundant mDNS scans

### Production Code Evolution
- `nvpmu/power_manager.rs`: Blind `thread::sleep(50ms)` → poll-until-ready loop
- `nvpmu/watchdog.rs`: `thread::sleep` → `Condvar::wait_timeout` for fast shutdown
- `server/transport.rs`: Fixed 10ms sleep → exponential backoff (1ms–100ms)

### Test block_on → tokio::test
56 `Runtime::new().unwrap().block_on(async { ... })` patterns converted to
`#[tokio::test] async fn` with `temp_env::async_with_vars` across 22+ files.
25 production sync bridges remain (require `#[async_trait]` migration).

## 3. Cross-Primal Capability-First Evolution

### Production refs: 5,104 → 550 (89% reduction)

Major type renames:
| Old | New |
|-----|-----|
| `SongbirdProtocol` | `CoordinationTransport` |
| `SongbirdLoadBalancer` | `CoordinationLoadBalancer` |
| `BearDogSecurityProvider` | `DistributedSecurityProvider` |
| `BearDogCloud` | `PrivateSecurityCloud` |
| `NestGateResult` | `StorageServiceResult` |
| `BearDogIntegrationConfig` | `SecurityServiceIntegrationConfig` |
| `SongbirdNetworkConfigurator` | `OrchestrationNetworkConfigurator` |

All renames include backward-compat: serde aliases, type aliases, legacy env var
fallbacks, parse_type match arms with `// legacy alias` comments.

### Remaining 550 refs are intentional
- Legacy env var names (`SONGBIRD_SOCKET`, `BEARDOG_URL`)
- Serde `alias = "songbird"` for old config/manifests
- `parse_type("beardog")` → `PrimalType::Crypto` compatibility
- Deprecated type aliases (`pub type BearDogBackend = SecurityBackend`)
- `interned_strings::primals::LEGACY_*_LABEL` constants

## 4. External Dependencies

All `*-sys` crates are transitive:
- `drm-sys` via `drm` crate
- `linux-raw-sys` via `rustix` (already adopted as pure-Rust libc alternative)
- `libloading` via `wgpu`/`ash` (GPU driver dynamic loading)
- `zstd-sys` stale lockfile entry (active code uses `ruzstd`)
- `clang-sys`, `cl-sys` unused lockfile entries

**0 C dependencies in workspace manifests.** Pure Rust (ecoBin v3.0 compliant).

## 5. Additional Cleanups

- 2 doc warnings fixed (unresolved link, redundant explicit target)
- License updated to AGPL-3.0-or-later in all root docs
- Root docs updated: README, CONTEXT, DOCUMENTATION, NEXT_STEPS, DEBT
- `#[allow(clippy::future_not_send)]` added to test modules using `async_with_vars`

## Quality Gate

| Gate | Result |
|------|--------|
| `cargo fmt --all -- --check` | 0 diffs |
| `cargo clippy --all-targets -- -D warnings` | 0 warnings |
| `cargo doc --no-deps --document-private-items` | 0 warnings |
| `cargo test --all-targets` | **21,515 tests, 0 failures, 100 ignored** |
| Test runtime | **~2m30s** (was ~9min) |

## Remaining Deep Debt

| Item | Count | Notes |
|------|-------|-------|
| Cross-primal refs (production) | 550 | Intentional legacy compat |
| Production `block_on` | 25 | Sync trait bridges |
| Unsafe blocks | 66 | All in hw-safe/GPU/VFIO/display containment |
| Test coverage | ~80-85% | Remaining gap: hardware-dependent paths |

## Files Changed

~100+ files across crates/server, crates/distributed, crates/core/common,
crates/core/config, crates/core/toadstool, crates/cli, crates/integration,
crates/runtime, crates/auto_config, benches/, contrib/, showcase/.

---

*Handoff by westgate — S187 deep debt execution complete*
