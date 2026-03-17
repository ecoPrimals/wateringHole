# ToadStool Session 39 — Cross-Spring Absorption Summary

**Date**: February 22, 2026  
**Scope**: Full absorption of shaders, bug fixes, and evolution items from all Springs

---

## Shader Absorptions Complete

### neuralSpring → barracuda::ops::bio (4 ops wired)

| Shader | Rust Op | Status |
|--------|---------|--------|
| `pairwise_l2.wgsl` | `PairwiseL2Gpu` | ✅ Wired |
| `multi_obj_fitness.wgsl` | `MultiObjFitnessGpu` | ✅ Wired |
| `swarm_nn_forward.wgsl` | `SwarmNnGpu` | ✅ Wired |
| `hill_gate.wgsl` | `HillGateGpu` | ✅ Wired |

### hotSpring → barracuda::ops::physics (11 shaders wired)

| Shader | Module | Status |
|--------|--------|--------|
| `bcs_bisection_f64.wgsl` | `physics::hfb` | ✅ Wired |
| `batched_hfb_density_f64.wgsl` | `physics::hfb` | ✅ Wired |
| `batched_hfb_energy_f64.wgsl` | `physics::hfb` | ✅ Wired |
| `batched_hfb_hamiltonian_f64.wgsl` | `physics::hfb` | ✅ Wired |
| `batched_hfb_potentials_f64.wgsl` | `physics::hfb` | ✅ Wired |
| `deformed_bcs_f64.wgsl` | `physics::hfb_deformed` | ✅ Wired |
| `deformed_density_f64.wgsl` | `physics::hfb_deformed` | ✅ Wired |
| `deformed_energy_f64.wgsl` | `physics::hfb_deformed` | ✅ Wired |
| `deformed_hamiltonian_f64.wgsl` | `physics::hfb_deformed` | ✅ Wired |
| `deformed_potential_f64.wgsl` | `physics::hfb_deformed` | ✅ Wired |
| `deformed_wavefunction_f64.wgsl` | `physics::hfb_deformed` | ✅ Wired |

### wetSpring → barracuda (3 new WGSL + ops)

| Shader | Rust Op | Status |
|--------|---------|--------|
| `kmer_histogram.wgsl` | `KmerHistogramGpu` | ✅ New shader + op |
| `taxonomy_fc.wgsl` | `TaxonomyFcGpu` | ✅ New shader + op (f64) |
| `unifrac_propagate.wgsl` | `UniFracPropagateGpu` | ✅ New shader + op (f64, 2 entry points) |

---

## Bug Fixes

| ID | Issue | Fix |
|----|-------|-----|
| S-15 | Matmul hang when f32 ≤ 0.1 | Removed GPU→CPU readback in NPU sparsity check |
| S-14 | Naive matmul tier hangs on small square matrices | Removed Naive tier; fixed tiled shader `workgroupBarrier()` deadlock |
| S-16 | Transpose 2D incorrect dispatch | Fixed to use TILE=16 matching `@workgroup_size(16, 16)` |

---

## Evolution Items Completed

| Item | Description |
|------|-------------|
| `execute_to_buffer()` | Added to `GemmCachedF64` — zero-copy GPU-resident streaming |
| `barracuda::math` | Convenience module re-exporting CPU special functions (erf, ln_gamma, etc.) |
| `FlatTree` | Generic CSR tree layout for bio ops (Felsenstein, UniFrac, bootstrap, NJ) |
| `sparse_eigh` | Lanczos-based sparse symmetric eigenvalue solver for HFB basis sets |
| `quantize_affine_i8` | Convenience function for symmetric int8 quantization with auto-scaling |

---

## Previously Resolved (confirmed this session)

| ID | Issue | Resolution |
|----|-------|------------|
| TS-001 | pow_f64 returns 0.0 for fractional exponents | ✅ Fixed in S36 (exp_f64 2^k, log_f64 7 terms) |
| TS-003 | acos/sin precision drift in f64 WGSL | ✅ Fixed in S37 (Cody-Waite + 7-term Taylor) |
| TS-004 | FusedMapReduceF64 GPU buffer conflict | ✅ Fixed in S36 |
| ESN export | GPU-train → NPU-deploy workflow | ✅ Implemented in S36 |

---

## Remaining Items (for future sessions)

| Priority | Item | Notes |
|----------|------|-------|
| Low | NPU int8 FC layer (AKD1000) | Awaiting hardware |
| Low | PCIe bus IDs in WgpuDevice | NPU has it; GPU needs wgpu upstream |
| Low | `from_existing_simple()` | Already deprecated with migration note |
| Medium | screened Coulomb | hotSpring plasma physics |
| Medium | Test coverage 65% → 90% | Ongoing |
| Low | cubecl `dirs-sys` transitive dep | Needs upstream PR |

---

## Quality Gates

- ✅ Zero clippy warnings workspace-wide
- ✅ Zero `#[allow(dead_code)]` false positives
- ✅ All production files under 1000 lines
- ✅ All mocks isolated to test code
- ✅ All unsafe is FFI/hardware-boundary only
- ✅ 600+ WGSL shaders wired to Rust — zero orphans
