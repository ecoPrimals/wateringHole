# barraCuda v0.3.12 — Sprint 44 Handoff (primalSpring Composition Audit)

**Date**: April 20, 2026
**Sprint**: 44 (composition audit — unblocks Level 5 for 3 springs)
**Version**: 0.3.12
**Tests**: 4,393+ passed, 0 failures
**IPC Methods**: 39 registered (+7 from Sprint 43's 32)
**Quality Gates**: fmt ✓ clippy (pedantic+nursery) ✓ doc (zero warnings) ✓ deny ✓
**Supersedes**: `BARRACUDA_V0312_SPRINT43_BTSP_PHASE3_DEEP_DEBT_HANDOFF_APR15_2026.md`

---

## Context

primalSpring v0.9.16 consolidated validation results from 5 springs (hotSpring L5,
healthSpring L4, wetSpring L4, ludoSpring L4, neuralSpring L3). barraCuda was
identified as the **single biggest blocker** — 6 missing JSON-RPC methods
blocked Level 5 certification for wetSpring, healthSpring, and neuralSpring.

## What Changed

### 6 New JSON-RPC Methods (32→39)

| Method | Domain | Implementation | Who Needs It |
|--------|--------|----------------|-------------|
| `stats.variance` | stats | CPU — `barracuda::stats::correlation::variance` | wetSpring, healthSpring |
| `stats.correlation` | stats | CPU — `barracuda::stats::correlation::pearson_correlation` | wetSpring, healthSpring |
| `linalg.solve` | linalg | CPU — Gaussian elimination with partial pivoting | wetSpring |
| `linalg.eigenvalues` | linalg | CPU — Jacobi iteration for symmetric matrices | wetSpring, neuralSpring |
| `spectral.fft` | spectral | CPU — Cooley-Tukey radix-2, zero-padded | wetSpring |
| `spectral.power_spectrum` | spectral | CPU — |X(k)|²/N from FFT | wetSpring |

### tensor.matmul_inline Convenience Path

Inline-data matrix multiply — springs send `lhs`/`rhs` as nested arrays, receive
product matrix directly. Eliminates the create→operate→extract three-call pattern.

### Fitts' Law Shannon Formula Fix

Corrected from `log₂(2D/W + 1)` to `log₂(D/W + 1)` per MacKenzie 1992 / ISO 9241-411.

### Response Schema Standardization

All scalar-returning methods now include a `"result"` key:
- `activation.fitts`: added `"result": mt` alongside `"movement_time"`
- `activation.hick`: added `"result": rt` alongside `"reaction_time"`
- `tensor.reduce`: added `"result": value` alongside `"value"`

Springs can uniformly extract `response["result"]` for any method.

### stats.std_dev Convention Documented

`stats.std_dev` and `stats.variance` responses include:
`"convention": "sample", "denominator": "N-1"` — explicit Bessel's correction.

### Verified (No Code Change Needed)

- **Hick's law**: default already uses `log₂(N)` (not `log₂(N+1)`)
- **perlin3d(0,0,0)**: returns 0.0 — existing test covers all integer lattice points

## Files Changed

- `crates/barracuda-core/src/ipc/methods/math.rs` — 6 new handlers + Fitts fix + schema
- `crates/barracuda-core/src/ipc/methods/mod.rs` — 7 new dispatch arms + REGISTERED_METHODS
- `crates/barracuda-core/src/ipc/methods/tensor.rs` — matmul_inline + reduce schema
- `crates/barracuda-core/src/ipc/mod.rs` — wire documentation tables
- `crates/barracuda-core/src/discovery.rs` — linalg/spectral domain descriptions
- `crates/barracuda-core/src/ipc/methods_tests/registry_tests.rs` — count 32→39

## Deep Debt Audit (Sprint 44b — Apr 20)

12-axis deep debt audit post-Sprint 44 — all axes green:
- Files >800L: zero (largest 783L test file, `math.rs` at 483L)
- TODO/FIXME/HACK/XXX: zero
- `#[allow(`: zero (all `#[expect(`)
- `async-trait`: zero
- `Box<dyn Error>` prod: zero (doc-only)
- `Result<T, String>` prod: zero (test-only)
- `println!/eprintln!` lib: zero (binary CLI only)
- Mocks prod: zero (test/doc only)
- `unsafe` prod: zero (test-only env var manipulation)
- Hardcoded primal names prod: zero (env-overridable defaults)
- External C/FFI deps: zero (all pure Rust, blake3 `pure`)
- `unwrap()/expect()` prod: zero (test/doc only)

Quality gates: `cargo fmt` ✓, `clippy -D warnings` ✓, `RUSTDOCFLAGS="-D warnings" cargo doc` ✓

## Sprint 44c: Phase 45 Audit — CPU Tensor Fallback (Apr 20)

Resolves **primalSpring Phase 45 gap #6**: `tensor.create` / `tensor.matmul`
(handle-based) returned "No GPU device available" on headless hosts.

### What changed

- **`CpuTensor` store** added to `BarraCudaPrimal` — parallel to existing GPU
  tensor store, holds `Vec<f32>` + shape for CPU-resident tensors.
- All 7 handle-based tensor ops (`tensor.create`, `tensor.matmul`, `tensor.add`,
  `tensor.scale`, `tensor.clamp`, `tensor.reduce`, `tensor.sigmoid`) now
  automatically fall back to CPU when `primal.device()` returns `None`.
- GPU path is **always preferred** — CPU fallback is transparent to callers.
- `tensor.create` response includes `"backend": "cpu"` when CPU path is used.
- `cpu_matmul` implements row-major matrix multiplication with `mul_add` FMA.
- CPU sigmoid uses `1/(1+exp(-x))` on f32.
- 2 new roundtrip tests: create→matmul→reduce (verifies 2×3 × 3×2 = 415 sum),
  add/scale/clamp/sigmoid on CPU tensors.
- 113 IPC method tests pass (was 111; 2 updated from error→success assertions,
  2 new CPU roundtrip tests).

### Wire contract update (v1.1.0)

- CPU fallback section in `specs/TENSOR_WIRE_CONTRACT.md`
- IPC namespace guide: 9 namespaces documented (`tensor`, `stats`, `activation`,
  `linalg`, `spectral`, `noise`, `fhe`, `math`, `compute`)
- Socket naming: authoritative `math.sock` / `math-{fid}.sock` vs legacy
  `barracuda.sock` symlink clarified

### Deep debt scan (Sprint 44c)

12-axis deep debt scan — all axes green (same result as Sprint 44b).

### Files changed

- `crates/barracuda-core/src/lib.rs` — `CpuTensor` struct, `store_cpu_tensor`,
  `get_cpu_tensor` methods, updated `tensor_count` to include CPU tensors
- `crates/barracuda-core/src/ipc/methods/tensor.rs` — CPU fallback in all 7
  handle-based ops, `cpu_matmul` + `cpu_tensor_result` helpers
- `crates/barracuda-core/src/ipc/methods_tests/tensor_fhe_tests.rs` — 2 new
  tests, 1 test updated (no-GPU → CPU fallback assertion)
- `crates/barracuda-core/src/ipc/methods_tests/comprehensive_tests.rs` — 1 test
  updated (tensor.create CPU fallback assertion)
- `crates/barracuda-core/src/ipc/methods_tests/mod.rs` — tensor fn imports added
- `specs/TENSOR_WIRE_CONTRACT.md` — CPU fallback, namespace guide, socket naming

## Sprint 44d: Deep Debt — Magic Number Evolution (Apr 20)

**12 production files** evolved from bare `256u32`/`128u32`/`64u32` workgroup size
literals to named constants (`WORKGROUP_SIZE_1D`/`WORKGROUP_SIZE_MEDIUM`/`WORKGROUP_SIZE_COMPACT`):

- `add.rs`, `mul.rs`, `fma.rs` — elementwise ops workgroup tier selection
- `sparse_matmul_quantized.rs` — quantized sparse matmul dispatch
- `fhe_ntt/compute.rs`, `fhe_intt/compute.rs` — FHE transform dispatch
- `fused_kl_divergence_f64.rs`, `fused_chi_squared_f64.rs` — fused stat dispatch
- `cumprod_f64.rs` — cumulative product dispatch

New `WORKGROUP_SIZE_MEDIUM = 128` constant added for integrated GPU tier.
`chi_squared.rs` bisection bracket evolved to `BISECTION_LOWER_BRACKET` named constant.

12-axis deep debt audit clean. All quality gates green.

## Remaining

- `OdeRK45F64` batching for Richards PDE (airSpring-specific, low priority)

---

**License**: AGPL-3.0-or-later
