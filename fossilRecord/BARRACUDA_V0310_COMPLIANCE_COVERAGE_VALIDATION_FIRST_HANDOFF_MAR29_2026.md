<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# barraCuda v0.3.10 — Compliance, Coverage & Validation-First Evolution

**Date**: 2026-03-29
**Sprint**: 21
**Version**: 0.3.10
**Scope**: wateringHole compliance (Semantic Method Naming Standard v2.2.0), validation-first handler pattern, coverage evolution, unsafe code hardening, UniBin CLI flag
**Previous**: BARRACUDA_V0310_DEEP_DEBT_FMA_LINT_HANDOFF_MAR21_2026

---

## Summary

Full audit against wateringHole Semantic Method Naming Standard v2.2.0, UniBin specification,
and ecoBin compliance, followed by systematic execution of all identified gaps. Core outcome:
`health.liveness`, `health.readiness`, `capabilities.list` non-negotiable endpoints implemented
with all required aliases. Validation-first handler refactoring across JSON-RPC and tarpc layers
enables comprehensive input-validation testing without GPU hardware. barracuda-core coverage
evolved from 59.33% to 72.83% line (+13.5pp). 214 unit tests + 8 e2e (up from 148). All
quality gates green.

## Changes

### Semantic Method Naming Standard v2.2.0 Compliance

- **`health.liveness`** — Fast liveness probe returning `{"status": "alive"}`. Required aliases
  wired: `ping`, `health`. Both JSON-RPC and tarpc.
- **`health.readiness`** — Readiness probe checking primal lifecycle state and device
  availability. Returns `ready: true/false` with reason. Both JSON-RPC and tarpc.
- **`capabilities.list`** — Ecosystem-standard capability probe. Alias for `primal.capabilities`.
  Additional alias `capability.list` for typo tolerance. Both JSON-RPC and tarpc.
- **`health.check`** — Existing full health check now wired with `status` and `check` aliases.
- **15 registered methods** in `REGISTERED_METHODS` (up from 12).
- **14 tarpc endpoints** with `LivenessReport`, `ReadinessReport` typed response structs.

### Validation-First Handler Pattern

Refactored all parameter-accepting handlers in both JSON-RPC and tarpc layers to validate
inputs *before* checking GPU device availability:

- **`compute.dispatch`** — Validates `op` field presence and validity, `shape` parsing,
  `tensor_id` existence before device check.
- **`tensor.create`** — Validates `shape`, element count overflow, `data` length mismatch
  before device check.
- **`tensor.matmul`** — Validates `lhs_id`, `rhs_id` presence and tensor existence before
  device-dependent matmul.
- **`fhe.ntt`** — Validates `modulus`, `degree`, `root_of_unity`, `coefficients`, coefficient
  length vs degree before device check.
- **`fhe.pointwise_mul`** — Validates `modulus`, `degree`, `a_coeffs`, `b_coeffs`, lengths
  before device check.
- **tarpc `compute_dispatch`, `tensor_create`, `tensor_matmul`, `fhe_ntt`,
  `fhe_pointwise_mul`** — Same validation-first pattern applied.

This makes all validation paths testable without GPU hardware and provides more precise error
messages to callers (INVALID_PARAMS for bad input, INTERNAL_ERROR for device issues).

### UniBin CLI

- **`--port <PORT>` flag** on `server` subcommand per UniBin standard. Maps to
  `127.0.0.1:<PORT>` bind address. Coexists with `--bind` (explicit takes precedence).

### Unsafe Code Hardening

- **`barracuda-spirv`**: `#![deny(unsafe_code)]` at crate root with targeted
  `#[allow(unsafe_code)]` at the single `wgpu::Device::create_shader_module_passthrough`
  call site. Non-empty SPIR-V assertion added before unsafe boundary. Module documentation
  explains safety invariant and evolution path to safe API.

### Test Coverage Evolution

- **barracuda-core**: 59.33% → 72.83% line coverage (+13.5pp)
- **214 unit tests + 8 e2e** (up from 148 unit tests)
- New test files: `rpc_tests.rs` (extracted from rpc.rs), `methods_coverage_tests.rs`
- Tests added for: health.liveness, health.readiness, capabilities.list, all aliases,
  validation-first error paths (compute missing op, unknown op, tensor data mismatch,
  fhe coefficient mismatch, shape overflow), primal lifecycle states, tensor store operations,
  discovery capability mapping, transport multi-request handling
- **rpc.rs** refactored from 861 to 572 lines via test extraction to `rpc_tests.rs`

### Clippy / Formatting Fixes

- `fhe_ntt_validation.rs`: `cast_lossless` lints resolved via `u128::from()`, `u64::from()`
- `unified.rs`: `DeviceContext::Sovereign` → `Self::Sovereign` (use-self)
- `svd.rs`, `fd_gradient_f64/tests.rs`: inlined format args
- `transport.rs`: `str.trim().split('\n')` → `str.lines()`

## Quality Gates

- `cargo fmt --all --check` ✅
- `cargo clippy --workspace --all-targets --all-features -- -D warnings` ✅
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` ✅
- `cargo deny check` ✅
- `cargo test -p barracuda-core` ✅ (214 lib + 8 e2e, 0 fail)
- `cargo test -p barracuda --lib --no-default-features` ✅ (705 math tests, 0 fail)
- `cargo llvm-cov test -p barracuda-core --lib --summary-only` ✅ (72.83% line)
- `#![forbid(unsafe_code)]` in barracuda + barracuda-core ✅
- `#![deny(unsafe_code)]` in barracuda-spirv ✅
- Zero production `unwrap()` ✅
- Zero TODO/FIXME/HACK in `*.rs` ✅
- Zero files over 1000 LOC ✅

## Codebase Health

- **Rust source files**: 1,085+
- **WGSL shaders**: 806 (all with SPDX headers)
- **Tests**: 3,623+ lib + 214 core + 8 e2e + 705 pure-math (0 failures)
- **Unsafe code**: Zero in barracuda + barracuda-core; 1 targeted allow in barracuda-spirv
- **Lint level**: pedantic + nursery + FMA + use_self + tuple_array + needless_range_loop all `warn`
- **TODO/FIXME/HACK**: Zero
- **`.unwrap()` in production**: Zero
- **Files over 1000 LOC**: Zero
- **Dependencies**: All pure Rust (blake3 `pure`, wgpu/naga 28, zero banned C deps)

## Cross-Primal Pins

| Primal | Version/Session | Status |
|--------|-----------------|--------|
| toadStool | S163 | Dependency audit, zero-copy, code quality |
| coralReef | Phase 10 Iter 62 | Deep audit, coverage, hardcoding evolution |
| All springs | barraCuda v0.3.10 / wgpu 28 | Synced |

## Next Steps

- P1: DF64 end-to-end NVK hardware verification
- P1: coralReef sovereign compiler evolution
- P2: Coverage to 90% (requires f64-capable GPU hardware in CI)
- P2: `missing_const_for_fn` evolution (911 sites, pending Rust const fn stabilization)
- P3: Multi-GPU dispatch evolution
- P3: Pipeline cache re-enable (pending wgpu safe API)
