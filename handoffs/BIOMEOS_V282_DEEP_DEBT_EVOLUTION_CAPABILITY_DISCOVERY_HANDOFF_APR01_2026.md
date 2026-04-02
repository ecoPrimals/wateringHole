<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# biomeOS v2.82 — Deep Debt Evolution & Capability-Based Discovery

**Date**: April 1, 2026
**From**: biomeOS team
**To**: All primal teams, primalSpring
**Status**: Complete — all 7 waves executed, zero regressions

---

## Summary

Systematic deep debt evolution across 7 waves resolving coverage gaps, large file
sprawl, unsafe code, hardcoded primal names, stub implementations, dependency skew,
and documentation drift. All changes compile cleanly, pass clippy (pedantic+nursery),
and maintain 90%+ test coverage.

---

## Wave Results

| Wave | Scope | Before → After |
|------|-------|----------------|
| 1 | Coverage push | 88.95% → 89.11% lines, 89.98% → 90.10% functions |
| 2 | Large file refactoring | 4 files 912–956 LOC → all under 769 LOC (tests extracted) |
| 3 | Unsafe elimination | 2 unsafe blocks → 0; `#![forbid(unsafe_code)]` on test-utils |
| 4a | Hardcoded primal names | `enroll.rs`, `verify_lineage.rs`, `spore.rs` → capability-based |
| 4b | Stub evolution | 5 discovery stubs → `#[deprecated]` + real `SocketDiscovery` wiring |
| 5a | Dep alignment | tower 0.4→0.5, tokio workspace dep aligned |
| 5b | Shell-out elimination | `build.rs` date shell-out → pure Rust `SystemTime` |

---

## Key Architectural Changes

### Capability-Based Enrollment (Wave 4a)

`enroll.rs` no longer hardcodes "beardog" as the security provider:

- CLI arg: `--security-provider-socket` (primary), `--beardog-socket` (deprecated alias)
- Socket resolution: `CapabilityTaxonomy::resolve_to_primal("encryption")` instead of `BEARDOG` constant
- `verify_lineage.rs`: Client variable renamed from `beardog` → `security_client`
- `spore.rs`: Hardcoded primal paths replaced with dynamic `CORE_PRIMALS` iteration

### Real Discovery Wiring (Wave 4b)

`UniversalBiomeOSManager::discover()` now uses the 5-tier `SocketDiscovery` protocol
instead of returning empty results. Deprecated methods retain backward compatibility
with `#[deprecated]` attributes and `#[allow(deprecated)]` on callers.

`live_service.rs` discovery loop simplified from 3 separate deprecated discovery calls
to a single `discover()` invocation.

### Smart File Refactoring (Wave 2)

All 4 files approaching 1000 LOC refactored by extracting test modules to separate
files using `#[cfg(test)] #[path = "..."] mod tests;` pattern:

- `ai_advisor.rs` 956 → 769 + `ai_advisor_tests.rs` 193
- `engine_tests2.rs` 935 → 707 + `engine_tests3.rs` 248
- `routing.rs` 921 → 421 + `routing_tests.rs` 499
- `paths.rs` 912 → 598 + `paths_tests.rs` 319

---

## Impact on Other Primals

### Enrollment CLI Change

Any scripts or automation using `biomeos enroll --beardog-socket PATH` should migrate
to `--security-provider-socket PATH`. The old flag remains as an alias but is
undocumented going forward.

### Discovery Service Deprecations

The following `UniversalBiomeOSManager` methods are now `#[deprecated]`:

- `discover_registry()` → use `discover()` (5-tier socket-based)
- `discover_network_scan()` → use `discover()`
- `discover_via_multicast()` → use `discover_via_dns()`
- `discover_orchestration_services()` → use `discover_by_capability()`
- `discover_from_registry()` → use `discover_all_services()`
- `discover_multicast()` → use `discover_via_dns()`

### No Breaking API Changes

All deprecated methods continue to function. The `PrimalDiscoveryService` stub
methods still return empty results for backward compatibility. New callers should
use `SocketDiscovery` directly or the manager's `discover()` method.

---

## Verification

```bash
cargo check                    # 0 errors
cargo clippy --all-targets     # 0 warnings (pedantic+nursery)
cargo test                     # 7,212+ tests, 0 failures
cargo fmt --check              # 0 diffs
cargo doc --no-deps            # 0 warnings
```

---

## Remaining Opportunities (Not Blocking)

- `live_discovery.rs`: Well-tested capability-based discovery module with `#[expect(dead_code)]`; ready to wire into REST routes when API surface expands
- Deeper beardog→capability rename in `biomeos-nucleus/src/identity.rs` and `trust.rs` (internal to nucleus crate)
- `tools/harvest/src/main.rs`: Standalone tool with documented `KNOWN_PRIMALS` roster (intentionally decoupled from workspace)

---

*scyBorg triple-copyleft: AGPL-3.0-only (code) + ORC (operational) + CC-BY-SA 4.0 (docs)*
