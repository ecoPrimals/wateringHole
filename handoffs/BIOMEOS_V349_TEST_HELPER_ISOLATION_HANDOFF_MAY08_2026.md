# biomeOS v3.49 — Test Helper Isolation (Priority 4 Code Quality)

**Date**: May 8, 2026
**Primal**: biomeOS
**Version**: 3.49
**Audit Reference**: primalSpring Priority 4 — mock helpers mixed with production code
**Tests**: 7,919 (0 failures, fully concurrent)

---

## What Changed

The primalSpring audit identified that mock/testing helpers for primal simulation
were compiled into production builds. These have been gated behind `#[cfg(test)]`
or feature flags so production binaries carry zero test scaffolding.

### Methods gated behind `#[cfg(test)]`

| Method | Crate | Reason |
|--------|-------|--------|
| `presets::testing()` | `biomeos-core` | Test-only config preset, zero production callers |
| `BiomeOSConfigBuilder::for_testing()` | `biomeos-core` | Test-only config builder, zero production callers |
| `UniversalBiomeOSManager::clear_all_primals()` | `biomeos-core` | Registry reset documented as "useful for testing" |

### Methods gated behind feature flag

| Method | Crate | Gate | Reason |
|--------|-------|------|--------|
| `SecureNucleusDiscovery::inject_primal_for_testing()` | `biomeos-federation` | `#[cfg(any(test, feature = "test-helpers"))]` | Called from integration tests (outside `#[cfg(test)]` scope) |

The `biomeos-federation` crate gains a `test-helpers` feature, enabled in its own
`[dev-dependencies]` so integration tests compile without configuration changes.

### Misleading doc comments fixed

| Item | Change |
|------|--------|
| `SocketDiscovery::with_xdg_override()` | "for testing" → "containers, sandboxes, P2P coordination" |
| `SocketDiscovery::with_temp_dir_override()` | Same |
| `SystemPaths::new_with_xdg_overrides()` | Same |
| `discover_via_multicast_with()` | "Simulated discovery" → accurate env-hint resolution description |

These methods are used by production code (`p2p_coordination`) and are not
test helpers — their documentation incorrectly suggested otherwise.

### Items confirmed already correctly gated

A thorough audit confirmed all other mock/fake/stub implementations across the
codebase are already inside `#[cfg(test)]` modules or dedicated `*_tests.rs`
files: `MockDiscovery`, `MockProvider`, `spawn_mock_server`, `fake_key`,
`create_beardog_stub`, etc.

---

## JH-11 (deferred)

Cross-primal token federation is acknowledged as a long-term architecture gap.
Currently each `MethodGate` validates independently — BearDog-issued ionic tokens
can't be verified by other primals. The `_resource_envelope` forwarding mechanism
(v3.48) is the current workaround. No action until Tier 1-2 are fully cleared.

---

## Verification

```
cargo clippy --all-targets -- -D warnings  # PASS (0 warnings)
cargo fmt --check                           # PASS
cargo test --workspace                      # 7,919 passed, 0 failed
```
