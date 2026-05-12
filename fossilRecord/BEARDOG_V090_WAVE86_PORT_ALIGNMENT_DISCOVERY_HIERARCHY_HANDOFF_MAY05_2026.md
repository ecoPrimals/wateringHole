# BearDog v0.9.0 — Wave 86 Handoff

**Date**: May 5, 2026
**Status**: Committed and pushed
**Branch**: main

---

## Summary

Wave 86 aligns BearDog's TCP IPC port default with the ecosystem convention,
documents the Discovery Escalation Hierarchy, and completes a clean deep debt
sweep confirming zero remaining debt.

## Changes

### 1. TCP IPC Port Alignment (ecosystem convention)

- `DEFAULT_TCP_IPC_PORT`: 9900 → **9100** (matches plasmidBin, primalSpring, ironGate)
- `DEFAULT_METRICS_PORT`: 9100 → **9190** (avoids collision with TCP IPC)
- Zero-config deployments now match what the ecosystem expects
- `BEARDOG_TCP_IPC_PORT` and `BEARDOG_METRICS_PORT` env vars documented

### 2. Discovery Escalation Hierarchy

Documented the 5-tier discovery hierarchy in both `ENVIRONMENT_VARIABLES.md`
and `QUICK_START_ZERO_HARDCODING.md`:

1. Songbird `ipc.resolve`
2. biomeOS Neural API (`capability.discover`)
3. UDS filesystem convention (`beardog-{family}.sock`)
4. Socket registry / manifests
5. TCP probing (well-known ports)

BearDog supports Tier 3 natively. Tier 5 now defaults to 9100.

### 3. Deep Debt Sweep Results

Full audit confirmed:
- **Large files**: 0 files >800 LOC in crates/ (largest: 790)
- **Unsafe code**: 0 blocks — all crates `#![forbid(unsafe_code)]`
- **async-trait**: Fully eliminated (0 deps, 0 usage, gone from Cargo.lock)
- **Hardcoded primal names**: 0 in production code
- **Production mocks**: 0 (Android JNI stubs are legitimate platform backends)

### 4. Clippy / Lint Fixes

- Renamed stale `async_trait_time_ms` → `baseline_time_ms` in benchmarks
- Simplified `impl Future` to `async fn` in beardog-traits test stubs
- Fixed `redundant_pub_crate` in test helper

## CI Status

- `cargo fmt`: clean
- `cargo clippy --workspace`: 0 warnings (library targets)
- `cargo test --workspace`: all passing (exit code 0)

## Files Changed

| File | Change |
|------|--------|
| `crates/beardog-config/src/domains/network_ports.rs` | Port defaults 9900→9100 / 9100→9190 |
| `crates/beardog-types/src/canonical/config/network.rs` | Doc comment updates |
| `crates/beardog-types/src/constants/domains/network_tests.rs` | Test assertion updated |
| `crates/beardog-types/src/constants/domains/PORT_PHILOSOPHY.md` | Default updated |
| `crates/beardog-traits/src/hsm.rs` | async fn simplification |
| `crates/beardog-types/src/tests/coverage_gap_wave18/common.rs` | pub(crate) → pub |
| `crates/beardog-workflows/src/workflows/performance_benchmarks.rs` | async_trait → baseline naming |
| `docs/references/ENVIRONMENT_VARIABLES.md` | New env vars + discovery hierarchy |
| `docs/references/QUICK_START_ZERO_HARDCODING.md` | Discovery hierarchy |

## Ecosystem Note

primalSpring audit (Phase 58+) confirms BearDog has **no new debt**. Wave 84-85-86
evolution is clean. `TCP_FALLBACK_BEARDOG_PORT=9100` now matches our default.

---

_Handoff from bearDog Wave 86 — May 5, 2026_
