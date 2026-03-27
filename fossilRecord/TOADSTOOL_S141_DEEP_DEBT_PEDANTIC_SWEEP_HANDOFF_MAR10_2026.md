# toadStool S141 — Deep Debt Evolution & Pedantic Sweep Handoff

**Date**: March 10, 2026
**Session**: S141
**Primal**: toadStool
**License**: AGPL-3.0-only

---

## Summary

S141 performed a comprehensive code quality evolution with three major themes:
clippy pedantic compliance across all targets (including test code), zero-copy
migration for GPU binary payloads, and sovereignty evolution removing the last
hardcoded primal names from API responses and handler logic.

---

## Changes

### Clippy Pedantic Sweep (120+ fixes, 10 crates)

`cargo clippy --workspace --all-targets -- -D warnings -W clippy::pedantic` now
passes with zero warnings, including test code (`--all-targets`).

Crates affected: `toadstool-client`, `toadstool-auto-config`,
`toadstool-management-monitoring`, `toadstool-management-performance`,
`toadstool-runtime-container`, `toadstool-runtime-wasm`, `toadstool-runtime-gpu`,
`toadstool-integration-protocols`, `toadstool` (core), `toadstool-distributed`,
`toadstool-management-analytics`, `toadstool-sysmon`.

All suppressions use `#[expect(clippy::lint_name, reason = "...")]` pattern per
wateringHole standard (never bare `#[allow]` in production).

### Zero-Copy: `Vec<u8>` → `bytes::Bytes` (6 GPU/runtime types)

| Type | Field | Crate |
|------|-------|-------|
| `ComputeBuffer` | `data` | `runtime/gpu` |
| `UniversalKernel::Binary` | `data` | `runtime/gpu` |
| `WorkloadResult` | `outputs` (HashMap values) | `runtime/gpu` |
| `CompiledKernel` | `binary` | `runtime/gpu` |
| `KernelInput` | `data` | `runtime/gpu` |
| `KernelOutput` | `buffers` (HashMap values) | `runtime/gpu` |

`bytes::Bytes` provides zero-copy cloning (reference-counted) and is the
recommended zero-copy type per wateringHole standards.

### Sovereignty Evolution

| Before | After |
|--------|-------|
| `deploy_graph_status` hardcoded 5-primal array | Runtime socket directory scan |
| `ecology_offload` hardcoded `airspring.sock` | `get_socket_path_for_capability(ECOLOGY)` |
| `"barracuda::activations"` string literal | `capabilities::ACTIVATIONS` |
| `"barracuda::rng"` string literal | `capabilities::RNG` |
| `"barracuda::special_functions"` string literal | `capabilities::SPECIAL_FUNCTIONS` |
| `"coralreef_native"` shader response | `capabilities::SHADER_COMPILE_NATIVE` |
| `"coral_reef_available"` response field | `"native_compiler_available"` |

New `interned_strings::capabilities` constants: `ECOLOGY`, `SCIENCE`,
`ACTIVATIONS`, `RNG`, `SPECIAL_FUNCTIONS`, `SHADER_COMPILE_NATIVE`.

### Fixes

- **Flaky test**: `test_concurrent_resource_monitoring_events` restructured with
  barrier synchronization — subscribe-before-start pattern, 500ms timeout.
- **SPDX**: `examples/real_gpu_pool.rs` corrected from `AGPL-3.0-or-later` to
  `AGPL-3.0-only`.
- **Doc link**: `streaming_dispatch.rs` broken intra-doc link fixed.

### Debris Cleanup

- Stale showcase references removed from `QUICK_REFERENCE.md`
- Broken neuromorphic README links fixed
- `NAK_DEFICIENCIES.md` paths updated for barraCuda separation
- `specs/README.md`, `specs/BARRACUDA_PRIMAL_BUDDING.md` stale refs cleaned
- CI `.github/workflows/ci.yml` evolved from dead `gpu-universal` paths to
  current 4-level showcase structure
- `Cargo.toml` exclude list cleaned (removed non-existent directories)
- `docs/guides/AKIDA_DRIVER_DEPLOYMENT.md` stale showcase path fixed
- `ADR-001-wgpu-over-opencl-cuda.md` benchmark path updated

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all -- --check` | PASS (0 diffs) |
| `cargo clippy --workspace --all-targets -- -D warnings -W clippy::pedantic` | PASS (0 warnings) |
| `cargo doc --workspace --no-deps` | PASS (0 warnings) |
| `cargo check --workspace --all-targets` | PASS |

---

## Inter-Primal Impact

- **barraCuda**: No breaking changes. `capabilities::ACTIVATIONS` etc. are
  string constants matching existing capability names.
- **coralReef**: Response field renamed from `"coral_reef_available"` to
  `"native_compiler_available"`. Tests updated.
- **All primals**: `deploy_graph_status` now discovers primals at runtime via
  socket directory instead of hardcoded list — new primals are automatically
  included.

---

## Remaining Debt (Carried)

| ID | Description | Status |
|----|-------------|--------|
| D-COV | Test coverage → 90% | 83.04% line. Gap: hardware-dependent code. |
| D-S46-001 | Conv2D/Pool shader evolution | Carried |
| D-S18-003 | e2e/fhe integration tests | Chaos framework exists |

---

## Files Modified (Key)

- `crates/core/common/src/interned_strings.rs` — 6 new capability constants
- `crates/server/src/pure_jsonrpc/handler/science_domains.rs` — sovereignty
- `crates/server/src/pure_jsonrpc/handler/science.rs` — sovereignty
- `crates/server/src/pure_jsonrpc/handler/mod.rs` — sovereignty
- `crates/runtime/gpu/src/universal.rs` — zero-copy
- `crates/runtime/gpu/src/types.rs` — zero-copy
- `crates/runtime/gpu/src/compiler.rs` — zero-copy
- `crates/runtime/gpu/src/cpu_resource.rs` — zero-copy
- `crates/runtime/gpu/src/frameworks.rs` — zero-copy
- 10+ crate `src/lib.rs` and test files — clippy pedantic
- `.github/workflows/ci.yml` — stale paths cleaned
- Root docs: STATUS.md, DEBT.md, NEXT_STEPS.md, CHANGELOG.md
