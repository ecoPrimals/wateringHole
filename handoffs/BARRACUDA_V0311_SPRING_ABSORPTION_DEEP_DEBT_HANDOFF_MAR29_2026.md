<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# barraCuda v0.3.11 — Spring Absorption & Deep Debt Evolution

**Date**: 2026-03-29
**Sprint**: 22
**Version**: 0.3.11
**Scope**: hotSpring lattice QCD absorption (multi-shift CG, GPU-resident RHMC observables, fermion force sign fix), cross-spring shader/algorithm absorption (Perlin f32, LCG 32-bit, Lanczos eigenvectors), tolerance registry expansion, deep debt: CoralReefDevice→SovereignDevice capability-based rename, f64 GPU test evolution, multi-shift CG algorithm fix, coverage expansion, root doc + wateringHole synchronisation
**Previous**: BARRACUDA_V0310_COMPLIANCE_COVERAGE_VALIDATION_FIRST_HANDOFF_MAR29_2026 (fossilRecord)

---

## Summary

Full spring review and absorption cycle. Primary absorption from hotSpring's Lattice QCD
GPU infrastructure: 5 multi-shift CG WGSL shaders (Jegerlehner zeta recurrence), 3 GPU-resident
observable shaders (Hamiltonian assembly, fermion action sum, Metropolis accept/reject), and
critical fermion force sign convention fix. Rust orchestration modules adapted to barraCuda's
WgpuDevice architecture. Secondary absorptions: f32 Perlin noise for ludoSpring, 32-bit LCG
for ludoSpring, Lanczos eigenvector pipeline for groundSpring. 6 new RHMC/lattice tolerance
constants. All quality gates green.

## Changes

### Critical Fix: Fermion Force Sign Convention

- **`staggered_fermion_force_f64.wgsl`** and **`pseudofermion_force_f64.wgsl`** corrected
  from `half_eta` (+η/2) to `neg_eta` (−η), aligning with hotSpring's validated
  `F = −d(x†D†Dx)/dU` derivation. The gauge force outputs ∂S_G/∂U (positive gradient)
  and momentum updates via `P += α_s·dt·F`, so the fermion contribution must be negative.
  Incorrect sign produced wrong HMC trajectories.

### hotSpring Lattice QCD Absorption

- **5 multi-shift CG WGSL shaders**: `ms_zeta_update_f64` (Jegerlehner Algorithm 1),
  `ms_x_update_f64`, `ms_p_update_f64`, `cg_compute_alpha_shifted_f64`,
  `cg_update_xr_shifted_f64`. All under AGPL-3.0-or-later with provenance headers.
- **`gpu_multi_shift_cg.rs`**: Orchestration module with `GpuMultiShiftCgPipelines`
  (pre-compiled pipelines for all 5 shaders), `GpuMultiShiftCgBuffers` (per-solve GPU
  allocation), `GpuMultiShiftCgConfig`, and `multi_shift_cg_generic()` — a closure-based
  CPU reference solver with no lattice type dependency.
- **3 GPU-resident WGSL shaders**: `hamiltonian_assembly_f64` (H = S_gauge + T + S_ferm,
  eliminates CPU readback), `fermion_action_sum_f64` (RHMC sector accumulation),
  `gpu_metropolis_f64` (accept/reject with 9-entry diagnostics).
- **`gpu_resident_observables.rs`**: O(1)-readback pipeline with `ResidentObservablePipelines`,
  `ResidentObservableBuffers`, `MetropolisResult` (9-entry GPU result parsing).

### Cross-Spring Absorptions

- **f32 Perlin 2D** (ludoSpring): `perlin_2d_f32.wgsl` shader, `PerlinNoiseGpuF32` struct,
  `perlin_2d_cpu_f32()` CPU reference. For real-time procedural generation without f64.
- **32-bit LCG contract** (ludoSpring): `lcg_step_u32()`, `state_to_f32()`,
  `uniform_f32_sequence()` using Knuth MMIX 32-bit constants. Game-speed PRNG.
- **Lanczos eigenvector pipeline** (groundSpring): `lanczos_with_basis()` retains Krylov
  basis vectors Q, `lanczos_eigenvectors()` computes Ritz vectors via Q×z back-transform,
  returns top-k eigenpairs sorted by |eigenvalue|.

### Deep Debt Evolution (Sprint 22b)

- **`CoralReefDevice` → `SovereignDevice`**: Capability-based rename. `coral_reef_device.rs`
  → `sovereign_device.rs`. `CoralBuffer` → `SovereignBuffer`. `TOADSTOOL_ADDR_ENV` →
  `DISPATCH_ADDR_ENV`. `CORALREEF_ADDR_ENV` → `COMPILER_ADDR_ENV`. All doc comments evolved
  from primal-name references (coralReef, toadStool) to capability references
  (shader.compile primal, compute.dispatch primal). Backward-compat `#[deprecated]` type
  alias preserved in `device/mod.rs`.
- **f64 GPU test evolution**: 14+ GPU tests across `cubic_spline`, `diversity_fusion`,
  `batched_multinomial`, `cdist_wgsl`, `seasonal_gpu`, `hargreaves_gpu`, `mc_et0_gpu`,
  `richards_gpu`, `brent_gpu`, `linsolve_f64`, `inverse_f64`, `histogram` evolved from
  `test_gpu_device()` / `get_test_device_if_gpu_available()` to `test_f64_device()` —
  prevents false GPU-zeros failures on llvmpipe (no f64 shader capability).
- **Multi-shift CG algorithm fix**: `multi_shift_cg_generic()` zeta recurrence corrected
  to use `beta_prev` and proper `(1.0 - zeta_curr[s] / zeta_prev[s])` ratio in shift term.
- **Perlin f32 shader assertion fix**: `assert!(!contains("f64"))` → `assert!(!contains("enable f64;"))`
  to avoid false-positive from f64 in comments.
- **Histogram test fix**: `get_device()` converted from sync to async, resolving Tokio
  runtime conflict and enabling proper f64-capable device acquisition.
- **Coverage expansion**: New unit tests for `cpu_reference::solve_cpu_thomas` (5 tests),
  `workarounds::detect_workarounds` (8 tests), `quality_filter::QualityConfig` (3 tests).
- **Root docs + wateringHole synchronised**: All `CoralReefDevice` → `SovereignDevice` in
  README, CONTRIBUTING, START_HERE, STATUS, WHATS_NEXT, CHANGELOG, SOVEREIGN_PIPELINE_TRACKER,
  PURE_RUST_EVOLUTION, specs/BARRACUDA_SPECIFICATION, specs/REMAINING_WORK. wateringHole
  README, PRIMAL_REGISTRY, leverage guides updated to v0.3.11 / 816 shaders / 4,162+ tests.

### Tolerance Registry

- 6 new RHMC/lattice HMC constants: `LATTICE_CG_FORCE` (1e-6), `LATTICE_CG_METROPOLIS`
  (1e-8), `LATTICE_RHMC_APPROX_ERROR` (1e-3), `LATTICE_PLAQUETTE` (1e-6),
  `LATTICE_FERMION_FORCE` (1e-4), `LATTICE_METROPOLIS_DELTA_H` (1.0).
- Total registered tolerances: **42**.

## Quality Gates

- `cargo fmt --all --check` — clean
- `cargo clippy --workspace --all-targets --all-features -- -D warnings` — zero warnings
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` — clean
- `cargo test -p barracuda --lib --no-default-features` — 717 tests, 0 fail
- `cargo test -p barracuda-core --lib` — 214 tests, 0 fail
- `#![forbid(unsafe_code)]` in barracuda + barracuda-core
- Zero production `unwrap()`, zero TODO/FIXME/HACK
- Zero files over 1000 LOC
- All deps pure Rust

## Codebase Health

- **WGSL shaders**: 816 (all with SPDX headers)
- **Rust source files**: 1,090
- **Tests**: 3,650+ lib + 214 core + 8 e2e + integration + doctests
- **Tolerance constants**: 42
- **Unsafe code**: Zero in barracuda + barracuda-core; 1 targeted allow in barracuda-spirv

### coralReef IPC Evolution (Sprint 22c)

- **Newline-delimited JSON-RPC framing** (wateringHole v3.1 mandatory) — `jsonrpc_call` now
  tries ndjson first (one JSON object per line, `\n` delimiter) and falls back to HTTP-wrapped
  framing for pre-v3.1 endpoints. Aligns with coralReef Iter 69.
- **Unix socket IPC transport** — `jsonrpc_call` supports `unix:/path/to/socket` addresses via
  `tokio::net::UnixStream`. Lower latency than TCP for local IPC.
- **Capability-domain socket discovery** — `discover_shader_compiler()` now scans
  `$XDG_RUNTIME_DIR/biomeos/shader.sock` (coralReef's capability-domain symlink) before
  falling back to JSON manifest scan and TCP port probe.
- **`biomeos` namespace integration** — discovery scans both `ecoPrimals` and `biomeos`
  directories under `$XDG_RUNTIME_DIR` for JSON manifests, resolving the namespace mismatch.
- **Unix socket preference in manifests** — `read_jsonrpc_from_value` extracts `"unix"`
  transport from Phase 10 manifests, preferring it over TCP when the socket exists.
- **Response parsing factored** — `parse_jsonrpc_response` shared between ndjson, HTTP, and
  Unix socket paths (DRY).
- New tests: ndjson TCP roundtrip with mock server, Unix socket roundtrip with mock server,
  `parse_jsonrpc_response` unit tests (ok/error/missing/invalid), Unix socket preference tests,
  biomeos namespace discovery, constants coverage.

### f64 Transcendental Pipeline Awareness (Sprint 22d)

- **Composite transcendental probes** — two new probe shaders that combine multiple
  f64 transcendentals in a single shader. RTX 3090 proprietary driver passes individual
  sqrt/sin/cos/exp/log probes but crashes on composite shaders (NVVM JIT failure).
  `composite_transcendental` and `exp_log_chain` probes now catch this.
- **`F64BuiltinCapabilities` evolved** — `has_f64_transcendentals()` requires all individual
  ops PLUS composite probes to pass. 16 probes total.
- **`get_test_device_if_f64_transcendentals_available()`** — async-first test gate with
  full probe suite. Sync wrapper via `tokio_block_on` for `#[test]` contexts.
- **10 failing tests → 0** — Bessel J₀/K₀, Beta, Digamma, Born-Mayer tests now use
  transcendental gate. Tests skip gracefully on hardware with broken composite f64.
- **Sin/cos probes non-trivial arguments** — `sin(9.21...)` / `cos(9.21...)` catch
  large-argument precision loss.
- **Per-operation tracing** — adapter name, vendor, driver, per-op pass/fail logged.
- **coralReef capabilities evolved** — `shader.compile.capabilities` now returns
  structured `CompileCapabilitiesResponse` with `f64_transcendentals` per-op polyfill
  availability (sin, cos, sqrt, exp2, log2, rcp, exp, log, composite_lowering).

## Cross-Primal Pins

| Primal | Version/Session | Status |
|--------|-----------------|--------|
| toadStool | S163 | Dependency audit, zero-copy, code quality |
| coralReef | Phase 10 Iter 70 | f64 transcendental capabilities reporting, structured CompileCapabilitiesResponse, composite polyfill |
| hotSpring | v0.6.32 | Multi-shift CG + GPU-resident observables absorbed |
| groundSpring | — | Lanczos eigenvectors absorbed |
| ludoSpring | — | f32 Perlin + 32-bit LCG absorbed |

### Probe Test Coverage & GPU Silicon Capability Matrix (Sprint 22e)

- **19 new tests** — 14 probe unit tests (composite gate logic, heuristic pessimism,
  Display output, PROBES array validation) + 5 DeviceCapabilities tests
  (has_f64_transcendentals, needs_sqrt_f64_workaround). 4,194 total, 0 failures.
- **`GPU_SILICON_CAPABILITY_MATRIX.md` spec** — living document mapping FP64 rates
  by GPU generation (NVIDIA Kepler→Blackwell Ultra, AMD GCN5→CDNA4, Intel Arc→Xe-HPC).
  Key finding: both vendors deprioritizing FP64 (Blackwell Ultra: 1:64, MI350X: half
  the FP64 matrix TFLOPS of MI300X). Documents DF64 decomposition strategy (complete
  library exists, naga blocks transcendentals, coralReef bypasses), toadStool VFIO
  silicon exposure path (tensor cores, RT cores, TMU via sovereign pipeline).

## Next Steps

- P0: Route transcendental-heavy shaders through coralReef sovereign compiler when `has_f64_transcendentals() == false` (use `fp64_strategy: "software"` in compile requests)
- P0: DF64 transcendentals via coralReef sovereign path (bypasses naga poisoning — complete library exists, just needs routing)
- P1: Tensor core GEMM routing for eigensolvers/preconditioners via toadStool VFIO + coralReef HMMA/WGMMA emission
- P1: DF64 end-to-end NVK hardware verification
- P1: Wire `gpu_multi_shift_cg` into full RHMC HMC trajectory (end-to-end lattice solve)
- P2: Coverage to 90% (requires f64-capable GPU hardware in CI)
- P2: `BatchedTridiagEigh` GPU op (groundSpring candidate)
- P3: Multi-GPU dispatch evolution
- P3: Mixed-precision iterative refinement (tensor core approximate + shader core DF64 residual)
