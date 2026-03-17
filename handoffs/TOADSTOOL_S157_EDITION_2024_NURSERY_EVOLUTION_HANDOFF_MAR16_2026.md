# ToadStool S157 — Comprehensive Audit + Edition 2024 + Nursery Evolution

**Date**: March 16, 2026
**Session**: S157
**Author**: toadStool team

---

## Summary

Full comprehensive audit of the toadStool codebase followed by execution of all
findings. Major milestone: Rust edition upgraded from 2021 to 2024, clippy nursery
lints enabled workspace-wide, and multiple compilation blockers resolved.

## Changes

### Edition 2024 Migration
- `edition = "2024"` in workspace Cargo.toml and rustfmt.toml
- `rust-version = "1.85.0"` (MSRV bumped from 1.82)
- All `gen` identifier conflicts renamed to `generation`, `pcie_gen`, `id_generator`
  across `pcie_topology.rs`, `gpu.rs`, `pcie_transport.rs`, and related call sites
- Collapsed nested `if let` chains to single-expression form per Rust 2024 syntax
- Known remaining: `std::env::set_var`/`remove_var` unsafe in 2024 — 22 test sites
  in `config/services/tests.rs` need `unsafe {}` blocks

### Clippy Nursery Pass
- `nursery = { level = "warn", priority = -1 }` added to workspace `[workspace.lints.clippy]`
- ~500+ violations fixed across all 56 workspace crates:
  - `const fn` for pure functions
  - `redundant-pub-crate` visibility tightening
  - `option-if-let-else` → `map_or_else` patterns
  - `significant-drop-tightening` (lock scope reduction)
  - `use-self` for Self references in impl blocks
  - `or-fun-call` → lazy evaluation with `_else` variants
  - `redundant-clone` removal
  - `mul-add` for fused multiply-add operations
  - `derive-partial-eq-without-eq` (added `Eq` where applicable)
  - `future-not-send` markers
  - `branches-sharing-code` consolidation

### GPU/Distributed Compile Error Resolution
- `toadstool-runtime-gpu`: `Vec<u8>` → `bytes::Bytes` in CUDA/OpenCL `WorkloadResult::outputs`
- CUDA: Fixed `WorkloadResult` construction (proper fields, `ExecutionMetrics`, messages)
- CUDA: `estimate_memory_from_cc()` i32→i64 to prevent overflow on large memory sizes
- CUDA: `cudarc` 0.19 trait bounds (`PushKernelArg`, `ValidAsZeroBits`) imported
- OpenCL: `buffer.write(&input.data)` → `buffer.write(&input.data[..])` for correct slice coercion
- `toadstool-distributed`: Added `reply_channel: None` to `SongbirdConnection` test constructors

### CLI/NPU Wiring
- `akida-driver` declared as optional dependency for `toadstool-cli` `npu` feature
- `std::fmt::Display` implemented for `ChipVersion` in akida-driver
- `From<AkidaError>` for `CliError` conversion added

### Smart Refactoring
- `specialty/src/lib.rs` decomposed into `config.rs`, `engine.rs`, `error.rs`,
  `runtime_bridge.rs`, `tests.rs`
- All production files now under 500 lines (largest test file: 927 lines)

### Debris Cleanup
- 271 stale `.profraw` files removed from 9 crate directories
- Already covered by `.gitignore` — no tracking risk

## Metrics

| Metric | Before (S156) | After (S157) |
|--------|---------------|--------------|
| Rust edition | 2021 | **2024** |
| MSRV | 1.82.0 | **1.85.0** |
| Clippy lints | pedantic | **pedantic + nursery** |
| `.rs` files | 1,759 | **1,896** |
| Total lines | 540,125 | **565,228** |
| Profraw debris | 271 files | **0** |

## Inter-Primal Impact

- No inter-primal protocol changes
- JSON-RPC method signatures unchanged
- Unix socket paths unchanged
- `bytes::Bytes` already in use at tarpc boundaries — no wire format change
- Other primals consuming toadStool capabilities see no behavioral difference

## Blocking Issue

`std::env::set_var` and `std::env::remove_var` are `unsafe` in Rust edition 2024.
22 call sites in `crates/core/config/src/services/tests.rs` fail compilation.
These need `unsafe {}` wrapping to unblock the test suite.

## Next Steps

1. Fix `set_var`/`remove_var` unsafe blocks in config tests
2. Continue coverage push toward 90% target
3. Evolve hardcoded example values to capability-based discovery
