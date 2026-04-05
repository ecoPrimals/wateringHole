# barraCuda v0.3.11 — Sprint 30: Deep Debt Audit, Smart Refactoring & Test Stability

**Date**: 2026-04-05
**Primal**: barraCuda
**Version**: 0.3.11
**Session**: Sprint 30

---

## Summary

Full codebase audit against wateringHole standards followed by execution on all identified
deep debt, evolution gaps, and test stability issues. Smart module refactoring of the largest
remaining file, SIGSEGV resolution for parallel GPU tests, disabled test evolution, stale doc
cleanup, and dependency analysis. All quality gates green.

---

## Changes

### Smart Module Refactoring: `barracuda-naga-exec`

- **`executor.rs`** (934 lines) → `executor.rs` (208L) + `invocation.rs` (756L)
- `InvocationContext` struct and all per-invocation execution logic extracted to
  dedicated `invocation.rs` module with clear separation of concerns:
  - `executor.rs` owns parse, validate, dispatch (workgroup iteration)
  - `invocation.rs` owns per-thread IR statement/expression interpretation
- New `DispatchCoords` config struct replaces 10-parameter `InvocationContext::new()`
  constructor — `#[expect(clippy::too_many_arguments)]` suppression eliminated
- `LOOP_ITERATION_LIMIT` named constant replaces magic `100_000` literal
- All 16 naga-exec tests pass, clippy pedantic clean

### Test Stability: SIGSEGV Resolution via nextest Serialization

- `fhe_chaos_tests` and `fault_injection` binaries added to `profile.coverage`
  exclusions — these SIGSEGV under LLVM instrumentation + parallel GPU driver FFI
  interaction with coverage probes
- `hardware_verification` also excluded from coverage (same root cause)
- New `test-groups.gpu-serial` with `max-threads = 1` serializes chaos, fault
  injection, and property tests
- Overrides applied to `profile.ci` and `profile.default` nextest profiles
- Root cause: Mesa llvmpipe thread safety in Vulkan adapter contention under
  concurrent `wgpu::Instance::create_surface` / `device.create_shader_module` calls

### Disabled Test Evolution

- `test_nn_vision_integration` (was `#[ignore]` with reason "NeuralNetwork API removed")
  evolved to `test_vision_pipeline_preprocessing`
- New test validates `VisionPipeline` directly: builds pipeline with `RandomFlip` +
  `RandomCrop`, processes a batch, asserts output dimensions
- All 8 API integration tests now pass (was 7 pass + 1 ignored)

### Stale Documentation Cleanup

- `nn/mod.rs` doc example referenced removed `NeuralNetwork` type — evolved to
  show current re-exported types (`Layer`, `Optimizer`, `LossFunction`, `NetworkConfig`)
- Root docs updated: README, STATUS, CONTEXT, CHANGELOG, WHATS_NEXT with Sprint 30
  achievements, accurate test counts (3,823 lib + 16 naga-exec + 220 core), file
  count (1,122 Rust source files)

### Dependency Audit

- 6 duplicate transitive crate pairs analyzed via `cargo tree -d`:
  `foldhash`, `getrandom`, `hashbrown`, `rand`, `rand_chacha`, `rand_core`
- Root causes: tarpc 0.37 → rand 0.8 (latest tarpc), wgpu/naga → hashbrown 0.15
- Cannot be resolved from barraCuda side — documented for upstream tracking

---

## Quality Gates

| Gate | Status | Detail |
|------|--------|--------|
| `cargo fmt --check` | Pass | All crates clean |
| `cargo clippy --workspace --all-features --all-targets -- -D warnings` | Pass | Zero warnings, pedantic+nursery |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --all-features --no-deps` | Pass | Zero warnings |
| `cargo deny check` | Pass | Advisories, bans, licenses, sources |
| `cargo test -p barracuda --lib --all-features` | Pass | 3,823 tests, 13 ignored |
| `cargo test -p barracuda-core --lib -- --test-threads=1` | Pass | 220 tests |
| `cargo test -p barracuda-naga-exec` | Pass | 16 tests |
| API integration tests | Pass | 8 pass, 0 ignored |
| File size (1000L max) | Pass | Largest: 845 lines |
| Zero TODO/FIXME/HACK | Pass | Confirmed clean |
| Zero production `.unwrap()` | Pass | Confirmed clean |
| Zero `#[allow(` without reason | Pass | All `#[expect(` with reason |

---

## Files Changed

### New Files
- `crates/barracuda-naga-exec/src/invocation.rs` — Per-invocation execution context (756 lines)

### Modified Files
- `crates/barracuda-naga-exec/src/executor.rs` — `InvocationContext` extracted (934→208 lines)
- `crates/barracuda-naga-exec/src/lib.rs` — `mod invocation` registered
- `.config/nextest.toml` — Coverage exclusions, `gpu-serial` test group, profile overrides
- `crates/barracuda/tests/api_integration_tests.rs` — Test evolution (ignored→active)
- `crates/barracuda/src/nn/mod.rs` — Doc example updated (removed `NeuralNetwork` reference)
- `specs/REMAINING_WORK.md` — Sprint 30 achievements documented
- `README.md` — Sprint 30 in Recent, updated test/file counts
- `STATUS.md` — Date bump, Sprint 30 entry
- `CONTEXT.md` — Updated test and file counts
- `CHANGELOG.md` — Sprint 30 changelog entry
- `WHATS_NEXT.md` — Sprint 30 in Recently Completed

---

## Cross-Primal Impact

**None.** All changes are internal to barraCuda. No IPC protocol changes, no API
surface changes, no behavioral changes visible to consumers.

---

## Remaining Known Debt

- `tarpc` pulls duplicate `rand` 0.8 alongside direct `rand` 0.9 — upstream-blocked
- `wgpu`/`naga` 28 use `hashbrown` 0.15 vs ecosystem `hashbrown` 0.16 — upstream-blocked
- `barracuda-spirv` single `unsafe` block for `create_shader_module_passthrough` —
  requires wgpu to expose safe SPIR-V API (tracked via `wgpu#4854`)
- `NeuralNetwork` variant in `WorkloadType` enum retained — valid for workload
  classification even though the training API was removed
