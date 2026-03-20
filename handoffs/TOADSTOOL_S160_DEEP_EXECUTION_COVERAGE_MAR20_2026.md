<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# ToadStool S160 — Deep Execution + Coverage Expansion Handoff

**Date**: March 20, 2026
**Session**: S160
**Primal**: toadStool
**Type**: Test fixes, coverage expansion, hardcoding evolution, dependency cleanup

## Summary

Continuation of S159 deep audit execution. Fixed 9 broken tests, added 49 new tests, evolved hardcoded constants, removed dead dependencies. All quality gates pass: 21,275 tests, 0 failures, clippy pedantic + nursery clean, fmt clean, doc clean.

## Changes

### Test Fixes (9 broken → 0 failures)
- `test_detect_neuromorphic_platforms`: falsely asserted empty result on Akida-equipped hardware (`/dev/akida0`). Evolved to hardware-agnostic — validates platform shape when present, passes on all machines.
- 7 integration tests in `unibin_execution_coverage_tests.rs`: nested-runtime panics (`#[tokio::test]` + `Runtime::new()`). Converted to `#[test]` + `thread::spawn` + `Builder::new_current_thread()`.
- 2 transport tests: stale assertion ("not yet implemented") after TRpc error evolved to "pending Phase 3". Assertions broadened.

### Coverage Expansion (+49 new tests)
- `crates/core/toadstool/src/resources/types.rs`: 17 tests — `ResourceRequirements::validate()`, `ResourceUsage::is_empty()`, serde round-trips, Default impls
- `crates/security/policies/src/types.rs`: 14 tests — PolicyCondition/Action variants, ViolationAction, LogicalOperator, serde
- `crates/security/sandbox/src/types.rs`: 12 tests — SandboxConfig, ResourceLimits, NetworkConfig defaults, enum serde
- `crates/testing/src/properties/mod.rs`: 6 tests — RoundTripProperty success/failure, ShrinkStrategy debug, TestStatistics

### Hardcoding Evolution
- Akida detection: 6 magic numbers → `AKIDA_*` named constants + `make_akida()` closure
- BearDog config: magic timeouts (30s, 300s, 60s) → named constants, `/tmp` → `std::env::temp_dir()`
- Resource validator: CPU/network/GPU magic numbers → named constants
- Cargo profiles: consolidated `.cargo/config.toml` → `Cargo.toml` single source of truth

### Dependency Cleanup
- Removed dead `procfs` dependency from 3 crates (sandbox, policies, performance)
- 2 bare `#[ignore]` → `#[ignore = "reason"]` (OpenCL, Vulkan hardware tests)

### Documentation
- TRpc transport error and docs: "pending Phase 3 — use JSON-RPC via pure_jsonrpc for IPC"
- `Arc<str>` backtick-escaped in doc comments (server, cli)

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all -- --check` | PASS (0 diffs) |
| `cargo clippy --workspace --all-targets -- -D warnings` | PASS (0 errors, pedantic + nursery) |
| `cargo doc --all-features --no-deps` | PASS (0 warnings) |
| `cargo test --workspace` | PASS (**21,275 tests, 0 failures**, 222 ignored) |
| `cargo llvm-cov` | ~83% line (186K lines instrumented) |
| Files > 1000 lines | 0 |
| Production TODO/FIXME/HACK | 0 |
| License | AGPL-3.0-or-later (100%) |

## Ecosystem Impact

- No API changes — all JSON-RPC methods, IPC contracts, and capabilities unchanged from S159
- Neuromorphic platform detection now hardware-agnostic (works on machines with/without Akida NPU)
- Transport error messages clarify Phase 3 tarpc status

## Remaining Debt

- D-COV: ~83% line coverage → 90% target (hardware mock expansion needed for VFIO/V4L2/DRM paths)
- Phase 3 tarpc binary transport (pending wiring)
- Property-based testing expansion for computation modules
- Multi-primal integration test infrastructure

## Cross-Primal Notes

- No breaking changes. No new IPC methods. No capability changes.
- toadStool stable at S160 — ecosystem consumers can pin without concern.

---

*AGPL-3.0-or-later — ecoPrimals sovereign community property.*
