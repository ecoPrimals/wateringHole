# barraCuda v0.3.3 — Deep Audit, Zero-Copy Evolution, Coverage Sprint

**Date**: March 9, 2026
**From**: barraCuda
**To**: coralReef, toadStool, all springs
**Type**: Deep Debt Evolution + Quality Handoff

---

## Summary

Full codebase audit and execution pass covering zero-copy evolution, modern
idiomatic Rust, test coverage expansion, and quality gate hardening. ~50 GPU
dispatch paths evolved to bytemuck zero-copy. Error types evolved to `Arc<str>`.
GPU backend download evolved to `bytes::Bytes`. Hardcoded GPU performance
estimates refactored to capability-based pattern matching. Coverage tests added
for 7 previously uncovered modules.

---

## What Changed

### Zero-Copy Upload Evolution (~50 dispatch paths)

The pervasive pattern across GPU ops:
```rust
// Before: allocates Vec<u8> on every dispatch
let data: Vec<u8> = values.iter().flat_map(|v| v.to_le_bytes()).collect();
device.alloc_buffer_init("buf", &data);

// After: zero-copy view into existing &[f64] / &[f32] memory
device.alloc_buffer_init("buf", bytemuck::cast_slice(values));
```

Affected modules: pipeline, MD (verlet, leapfrog, thermostat), linalg (matmul,
svd, qr, triangular_solve), reduce (sum, prod, norm, mean_variance), optimize
(bfgs, nelder_mead, cg_solver), PDE (rk4, heat_equation), grid (fft, expand),
lattice (stencil, gauge_action), spectral (batch_ipr), stats (histogram, erf).

### GpuBackend::download() → bytes::Bytes

Return type evolved from `Result<Vec<u8>>` to `Result<bytes::Bytes>` on the
`GpuBackend` trait, `WgpuDevice` impl, `CoralReefDevice` scaffold, and
`Arc<B>` blanket impl.

### NpuTensorStorage → BytesMut

NPU tensor storage evolved from `Vec<u8>` to `bytes::BytesMut`. `read_to_cpu()`
returns `self.data.clone().freeze()` — ref-count bump, not a full buffer copy.

### ShaderCompilation(Arc<str>)

Error variant evolved from `String` to `Arc<str>`. All 10 f64 WGSL shader
op files (cosine_similarity, weighted_dot, hermite, bessel_i0/j0/j1/k0,
beta, digamma, covariance) now use `Arc::from(format!(...))` and
`Arc::clone(msg)` instead of `msg.clone()` String allocation.

### GPU Performance Fallback Estimates

13 hardcoded constants (`ESTIMATED_GFLOPS_NVIDIA_DISCRETE`,
`ESTIMATED_VRAM_BYTES_NVIDIA_DISCRETE`, etc.) refactored to:

```rust
mod fallback_estimates {
    pub fn gflops(vendor: u32, device_type: DeviceType) -> f64 { ... }
    pub fn vram_bytes(vendor: u32, device_type: DeviceType) -> u64 { ... }
}
```

Pattern-matched by vendor (NVIDIA 0x10de, AMD 0x1002, Intel 0x8086, Apple,
software) and device type (Discrete, Integrated, Virtual, Cpu).

### Coverage Expansion

| Module | Tests Added | Coverage Before |
|--------|-------------|-----------------|
| `spectral/batch_ipr` | 3 GPU tests | 0% |
| `stats/histogram` | 4 GPU tests | 0% |
| `staging/ring_buffer` | 8 GPU tests | <30% |
| `staging/unidirectional` | 7 GPU tests | <30% |
| `staging/stateful` | 3 GPU tests | <30% |
| `shaders/precision/cpu` | 22+ CPU tests | <30% |
| `surrogate/adaptive` | 4 GPU tests (multi-kernel) | existing basic |
| `surrogate/rbf` | 4 GPU tests (multi-kernel) | existing basic |

### GPU-Heavy Test Timeout Fix

`edge_conv::tests::test_edge_conv_basic` was timing out at 60s on llvmpipe.
Nextest config updated with `gpu-heavy` test group slow-timeout overrides:
- `default` profile: 60s
- `ci` and `gpu` profiles: 180s
- `quick` profile: 120s

### CI Coverage Hardening

CI pipeline now has dual coverage targets:
- `--fail-under-lines 80` — hard gate (llvmpipe baseline)
- `--fail-under-lines 90` — stretch target (continue-on-error, requires GPU)

### Doc Collision Fix

`barracuda-core`'s `[[bin]] name = "barracuda"` set to `doc = false`, resolving
the Cargo #6313 documentation filename collision between the binary and library.

---

## What Springs Should Know

- **bytemuck::cast_slice** is now the standard pattern for buffer uploads.
  Springs contributing new ops should use `bytemuck::cast_slice(&data)` instead
  of the `flat_map(to_le_bytes).collect()` pattern.
- **GpuBackend::download()** returns `bytes::Bytes`. Callers get zero-copy
  semantics; use `.to_vec()` only when mutation is needed.
- **Arc<str> errors**: If springs handle `BarracudaError::ShaderCompilation`,
  the inner type is now `Arc<str>` (implements `Display`/`Debug` identically).
- **Test patterns**: New GPU tests use `get_test_device_if_gpu_available()`
  guard. See `batch_ipr.rs` or `histogram.rs` for the canonical pattern.

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy --all-targets --all-features` | Pass (zero warnings) |
| `cargo doc --no-deps` | Pass (zero warnings) |
| `cargo deny check` | Pass |
| `cargo nextest run -p barracuda --lib --profile quick` | All pass |

---

## Files Changed (key files)

| File | Change |
|------|--------|
| `src/device/backend.rs` | `download()` return type → `bytes::Bytes` |
| `src/device/wgpu_backend.rs` | `download()` impl → `Bytes` |
| `src/device/coral_reef_device.rs` | `download()` impl → `Bytes` |
| `src/error.rs` | `ShaderCompilation(String)` → `ShaderCompilation(Arc<str>)` |
| `src/npu_executor.rs` | `NpuTensorStorage::data` → `BytesMut` |
| `src/multi_gpu/multi_device_pool.rs` | Constants → `fallback_estimates` module |
| `src/ops/cosine_similarity_f64.rs` (+ 9 more) | `String` → `Arc<str>` error path |
| ~50 files across `ops/`, `pipeline/`, `staging/` | `bytemuck::cast_slice` evolution |
| `src/spectral/batch_ipr.rs` | Coverage tests (3) |
| `src/stats/histogram.rs` | Coverage tests (4) |
| `src/staging/ring_buffer.rs` | Coverage tests (8) |
| `src/staging/unidirectional.rs` | Coverage tests (7) |
| `src/staging/stateful.rs` | Coverage tests (3) |
| `src/shaders/precision/cpu.rs` | Coverage tests (22+) |
| `src/surrogate/rbf/tests.rs` | Additional kernel tests (4) |
| `src/surrogate/adaptive/mod.rs` | Additional kernel tests (4) |
| `.config/nextest.toml` | GPU-heavy timeout overrides |
| `.github/workflows/ci.yml` | 90% coverage stretch target |
| `crates/barracuda-core/Cargo.toml` | `doc = false` on binary |
| `STATUS.md`, `CHANGELOG.md`, `WHATS_NEXT.md` | Updated |
| `specs/REMAINING_WORK.md` | Updated with sprint achievements |
