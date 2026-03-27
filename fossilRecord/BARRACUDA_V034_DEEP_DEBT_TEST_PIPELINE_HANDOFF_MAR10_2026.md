# barraCuda v0.3.4 — Deep Debt & Test Pipeline Evolution Handoff

**Date**: March 10, 2026
**From**: barraCuda
**To**: All springs, coralReef, toadStool
**Version**: 0.3.4

---

## Summary

Final deep debt sprint completing multi-GPU infrastructure, precision routing
fixes, and test pipeline optimisation. Zero TODO/FIXME/`unimplemented!()` in
codebase. 3,249 tests pass (0 fail, 13 ignored) in 21.5s.

---

## What Changed

### Multi-GPU & Precision (springs should absorb)

1. **Unified GFLOPS/VRAM estimation** — `multi_gpu::mod` now exports shared
   `estimate_gflops(vendor, device_type)` and `estimate_vram_bytes(vendor, device_type)`.
   Springs using `GpuPool` or `MultiDevicePool` get consistent estimates automatically.

2. **Fp64Strategy routing fix** — `SumReduceF64`, `VarianceReduceF64`,
   `NormReduceF64`, `ProdReduceF64` now correctly call `.df64()` (not `.f64()`)
   on Hybrid devices. This was silently compiling DF64 shaders via the wrong
   path. **hotSpring/groundSpring**: if you saw incorrect DF64 reduce results
   on proprietary NVIDIA, this is the fix.

3. **PCIe topology probing** — New `PcieLinkInfo` struct probes Linux sysfs for
   PCIe generation, lane width, NUMA node, and vendor ID per GPU. `PcieBridge`
   uses this for P2P detection (shared NUMA node) and real bandwidth calculation.
   **coralReef**: this enables the RTX 3050 array topology discovery discussed
   in previous sessions.

4. **VRAM quota enforcement** — `WgpuDevice` now accepts optional `QuotaTracker`.
   All `create_buffer_f32/u32/f64` and `create_f32_rw_buffer` check quota before
   proceeding. Returns `BarracudaError::ResourceExhausted` on OOM. Springs using
   `WgpuDevice` directly can inject a quota tracker via `set_quota_tracker()`.

5. **BGL builder** — `BglBuilder` for declarative `wgpu::BindGroupLayout`
   construction: `.storage_read(0).storage_rw(1).uniform(2).build(device)`.
   **wetSpring**: this fulfills V105 request for reusable pipeline layouts.

### Test Pipeline (springs should update test patterns)

6. **Nautilus tests 1430× faster** — Tests now use minimal `test_config()`:
   `pop_size:4, grid_size:2` (16-dim features). The principle: **barraCuda
   validates dispatch mechanics; springs validate convergence.** If you have
   barraCuda tests doing full physics/ML, shrink them.

7. **Board hash zero-alloc** — `format!("{features:?}")` → incremental
   `blake3::Hasher::update(f64::to_le_bytes())`. Same determinism, zero
   allocations. **No API change** — internal optimisation.

8. **Sovereign validation parallelised** — 600+ WGSL shader files validated
   via `rayon::par_iter()`. The harness confirms all shaders parse and
   optimise through the sovereign compiler.

9. **ESN test shrunk** — `test_esn_large_reservoir` (200 reservoir) renamed
   to `test_esn_reservoir_shape` (16 reservoir). Shape validation only.

### Cleanup

10. **Deprecated `discover_coralreef` alias removed** — was already replaced
    by `discover_shader_compiler` (capability-based naming).

---

## Spring Validation Assignments (updated)

| Spring | Module | Validates | Notes |
|--------|--------|-----------|-------|
| **hotSpring** | `ops::*_reduce_f64` | DF64 reduce correctness on proprietary NVIDIA | Fp64Strategy routing now fixed |
| **hotSpring** | `unified_hardware::transfer` | PCIe topology on multi-GPU rigs | `PcieLinkInfo` gives real gen/width/NUMA |
| **groundSpring** | `multi_gpu::mod` | GFLOPS/VRAM estimation accuracy | Shared functions, vendor-specific |
| **wetSpring** | `device::compute_pipeline::BglBuilder` | BGL builder ergonomics | Fulfills V105 request |
| **All springs** | Test pipeline | Test execution time | Principle: dispatch mechanics only |

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | ✅ Pass |
| `cargo clippy --workspace --all-targets` | ✅ Zero warnings |
| `cargo doc --no-deps --workspace` | ✅ Pass |
| `cargo test -p barracuda --lib` | ✅ 3,249 pass / 0 fail / 13 ignored / 21.5s |
| TODO/FIXME/`unimplemented!()` | ✅ Zero |
| `#[allow(dead_code)]` without reason | ✅ Zero |
| `unsafe` blocks | ✅ Zero |

---

## Remaining P1

- DF64 NVK end-to-end hardware verification (Yukawa shaders)
- coralNAK extraction (pending org repo fork)
- Dedicated DF64 shaders for covariance + weighted_dot
- Multi-GPU OOM recovery (quota → automatic workload migration)

## Remaining P2

- Test coverage 80%→90% (`--fail-under`)
- Kokkos validation baseline + GPU parity benchmarks
- RHMC multi-shift CG solver (hotSpring ladder L4)
