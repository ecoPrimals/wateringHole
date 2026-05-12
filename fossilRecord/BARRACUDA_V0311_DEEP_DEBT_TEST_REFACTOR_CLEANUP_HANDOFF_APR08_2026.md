# barraCuda v0.3.11 — Sprint 37: Deep Debt — Test Module Refactor & Code Cleanup

**Date**: April 8, 2026
**Primal**: barraCuda
**Version**: 0.3.11
**Supersedes**: BARRACUDA_V0311_DOMAIN_SOCKET_NAMING_FLAKY_FIX_HANDOFF (archived)

---

## Summary

Sprint 37 smart-refactors the last >800-line file in the codebase and
resolves the remaining minor deep debt items identified by the 12-axis audit.

## Changes

### Smart Refactoring

`methods_tests.rs` (951 LOC) → 6 domain-focused test modules + hub:

| Module | Lines | Coverage |
|--------|-------|----------|
| `mod.rs` (hub) | 30 | Shared imports, `test_primal()`, submodule declarations |
| `registry_tests.rs` | 103 | parse_shape, normalize_method, REGISTERED_METHODS |
| `primal_wire_tests.rs` | 161 | primal.info, identity.get, Wire Standard L2 compliance |
| `device_health_tests.rs` | 193 | device, health, tolerances, alias dispatch |
| `dispatch_compute_tests.rs` | 113 | dispatch routing, validate, compute errors |
| `tensor_fhe_tests.rs` | 168 | tensor + FHE error paths |
| `comprehensive_tests.rs` | 167 | all routes, text protocol, tensor store |

### Code Cleanup

- `buffer_test.rs`: 6 `println!` calls removed from test code in library `src/` path
- `nadam_gpu.rs`: Stale `// BEFORE: ... // AFTER: ...` evolution narrative removed
- `force_interpolation.rs`: `for i in 0..positions.len()` → `iter().zip()`

### 12-Axis Deep Debt Audit: Clean Bill

| Axis | Status |
|------|--------|
| Files >800L | 0 (largest: 790L `wgpu_caps.rs`) |
| `unsafe` in production | 1 (wgpu passthrough, documented) |
| `#[allow(` | 0 (all `#[expect(`) |
| `Result<T, String>` in production | 0 |
| `TODO`/`FIXME`/`HACK` in .rs | 0 |
| `println!`/`eprintln!` in library src/ | 0 |
| External C/FFI in crates/ | 0 |
| Commented-out code | 0 |
| Mocks in production | 0 |
| Other-primal hardcoding | 0 |
| Error types | All thiserror |
| Hardcoded paths in production | 0 |

## Quality Gates

- **4,207 tests** pass, 0 fail, 14 skipped
- `cargo fmt --all --check` — clean
- `cargo clippy --workspace --all-targets --all-features -- -D warnings` — clean
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` — clean

## Remaining Blocked Work

- **BTSP Phase 2 handshake client**: BearDog `btsp.session.*` RPCs still stubs.
  barraCuda server-side BTSP enforcement blocked on BearDog completing session layer.
