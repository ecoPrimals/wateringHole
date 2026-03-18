# ToadStool S156 — Full Codebase Audit + Specialty Crate Resurrection

**Date**: March 16, 2026
**Session**: S156
**Primal**: toadStool
**Quality gates**: ALL GREEN (build, fmt, clippy pedantic, doc, test)

---

## Summary

Comprehensive codebase audit against wateringHole standards, specs, and inter-primal
interaction docs. Resurrected `runtime-specialty` crate from 167 compile errors.
All 56 crates now pass build/fmt/clippy/doc/test with zero warnings.

## Changes

### P0: runtime-specialty Resurrected (167 → 0 errors)

Core type drift from `ExecutionResponse`, `ExecutionRequest`, `ExecutionStatus`,
`WorkloadType`, `RuntimeCapabilities`, `RuntimeMetrics` evolution. Fixed:

- Aligned all struct field names (`execution_id` not `workload_id`, `exit_code` not
  `return_code`, `Success` not `Completed`, `Failed { error: Cow }` not `Failed`)
- `platform_features: HashMap<String, bool>` not `String`
- Removed `WorkloadType::Custom` (no longer exists)
- Fixed `Arc<dyn>` vs `Box<dyn>` adapter maps
- Aligned `EmbeddedEmulator`, `ProgrammerInterface`, `CrossCompilationToolchain`
  trait impls with definitions
- Renamed 40+ enum variants to UpperCamelCase with `#[serde(rename)]` wire compat
- Resolved glob re-export ambiguities in `types/` module tree
- Fixed 47 clippy pedantic errors (Default impls, `&PathBuf`→`&Path`, dead fields)
- Rewrote both integration test files against current types
- Made private mainframe fields `pub`, added Debug bounds to trait objects

### P1: Standards Compliance

- **Hardcoding → constants**: Dispatch 5000ms magic → `DISPATCH_DEFAULT_TIMEOUT`
- **Unsafe → safe**: `unreachable!()` in `dma.rs` → `Err(NvPmuError::Hardware(...))`
- **Doc warnings**: 5 nvpmu bracket escapes, 2 specialty HTML tag fixes
- **Unused imports**: `CudaStream` removed from `gpu/cuda_impl/device.rs`
- **Clippy lint**: `needless_return` in `distributed/factory.rs`
- **`warn(missing_docs)`**: 4 clean crates retain it; 39 deferred

### Cleanup

- 5,950 profraw files (2.2 GB) deleted
- 15.2 GB stale target/ cleaned
- 2 orphan CSV files removed from root

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests passing | 21,112 (specialty excluded) | **21,156** (all 56 crates) |
| Crates compiling | 55/56 | **56/56** |
| Clippy warnings | 2 (distributed + specialty) | **0** |
| Doc warnings | 7 | **0** |
| Disk garbage | 17.4 GB | **0** |

## Remaining Work (for next session)

| Priority | Item |
|----------|------|
| P1 | Coverage 83% → 90% (hardware-dependent code needs deeper mocks) |
| P1 | GlowPlug absorption: hotSpring PowerManager → nvpmu `GpuPowerController` |
| P1 | Standardize `capability.list` response format (object format per neuralSpring S156 handoff) |
| P1 | Formalize manifest-based discovery protocol (`$XDG_RUNTIME_DIR/ecoPrimals/*.json`) |
| P2 | E2E sovereign pipeline test: barraCuda → coralReef → toadStool → GPU |
| P2 | Property-based testing for computation-heavy modules |
| P2 | `warn(missing_docs)` progressive rollout (39 crates need doc coverage) |
| P2 | Wire `benches/` directory into workspace (3 criterion benchmarks exist but aren't connected) |
| P3 | Chaos/fault injection tests (framework in `testing/chaos/` but all `#[ignore]`) |

## Cross-Primal Notes

- **coralReef**: USERD_TARGET fix still blocks VFIO PBDMA dispatch (6/7 tests pass)
- **neuralSpring**: IPC discovery bugs fixed in S156; `capability.list` format needs ecosystem standardization
- **hotSpring**: GlowPlug and PowerManager ready for absorption into toadStool nvpmu
- **Compute trio interaction**: glowPlug documented in wateringHole SOVEREIGN_COMPUTE_EVOLUTION.md as the subsystem tying barraCuda/toadStool/coralReef compute lifecycle

## Quality Gate Verification

```
cargo fmt --all -- --check           → PASS (0 diffs)
cargo clippy --workspace --all-targets -- -D warnings → PASS (0 warnings, 56 crates)
cargo doc --workspace --no-deps      → PASS (0 warnings)
cargo test --workspace               → PASS (21,156 passed, 0 failed, 222 ignored)
```
