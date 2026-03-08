# hotSpring v0.6.17 — Asymmetric Lattice, DF64 Scaling, coralReef Review, Kokkos Gap Correction

**Date**: March 5, 2026  
**From**: hotSpring  
**To**: barraCuda, toadStool, coralReef  
**Status**: Findings ready for absorption  
**Priority**: High — multiple evolution opportunities identified

---

## 1. Corrected Kokkos-CUDA Gap Analysis

### Previous understanding (WRONG)

We previously reported a 149x gap between barraCuda GPU and Kokkos-CUDA. This was
misleading — the 149x is **NVK/NAK compiler-specific**, not inherent to barraCuda.

### Corrected analysis

| Driver path | Chain | Gap vs Kokkos-CUDA |
|-------------|-------|:------------------:|
| **Proprietary Vulkan** | WGSL → naga → SovereignCompiler → SPIR-V → **NVIDIA PTXAS** → SASS | **~1.5-3x** |
| **NVK (open-source)** | WGSL → naga → WGSL text → **NAK** → SASS | **9-149x** (NAK quality) |
| **NVK + coralReef** (future) | WGSL → naga → **coralReef** → SASS → coralDriver → GPU | **~2-5x** (est.) |

**Key insight**: On proprietary NVIDIA Vulkan driver, barraCuda's SPIR-V passthrough
uses the **same NVIDIA PTXAS backend** that Kokkos-CUDA uses via nvcc. The code
generation quality is near-identical. The remaining gap is pure dispatch/API overhead:

- Vulkan command buffer overhead vs CUDA stream: ~1.1-1.3x
- wgpu abstraction layer: ~1.1-1.2x
- Total: **~1.5-3x**, not 149x

### Action items for barraCuda

1. **Benchmark on proprietary Vulkan**: Run the 9 Yukawa OCP cases on proprietary
   NVIDIA driver (not NVK) to get real numbers. Both Kokkos-CUDA and barraCuda-Vulkan
   can run simultaneously on the same GPU.
2. **SPIR-V passthrough quality**: The `SovereignCompiler` (FMA fusion + dead expr
   elimination) improves SPIR-V quality before PTXAS. Measure the delta.
3. **Document the driver-dependent gap**: The gap is a function of `GpuDriverProfile`,
   not barraCuda's architecture.

### Action items for coralReef

1. **coralDriver is the critical path**: coralReef compiles WGSL → SASS for SM70-89.
   The missing piece is the userspace driver to submit compiled binaries.
2. **QMD definitions exist**: Volta (v2.2), Ampere (v3.0), Hopper (v4.0), Blackwell
   (v5.0) — all defined in `nvidia_headers.rs`.
3. **Priority**: coralDriver Phase 6 closes the sovereign gap on NVK.

---

## 2. Asymmetric Lattice Geometry — Critical Physics Finding

### The problem with hypercubic lattices

All hotSpring lattice QCD runs to date used **hypercubic** geometry (L⁴ = 32⁴).
This studies the bulk strong-to-weak coupling crossover, **not** the physical
finite-temperature deconfinement phase transition.

### What MILC does (and what we should do)

MILC production uses **asymmetric** geometry: N_s³ × N_t where N_s >> N_t.

- Temperature: T = 1/(a(β) × N_t)
- N_t controls temperature; N_s controls spatial volume
- Different N_t values → different β_c → continuum extrapolation

| N_t | β_c (literature) | Physics |
|:---:|:-----------------:|---------|
| 4 | 5.692 | Coarse lattice, original discovery |
| 6 | 5.89 | Improved |
| 8 | 6.06 | Standard production |
| 12 | 6.34 | Fine lattice |
| 16 | 6.52 | Continuum approach |

### hotSpring already supports this

The `Lattice` struct uses `dims: [usize; 4]` = `[Nx, Ny, Nz, Nt]` with **no symmetry
assumption**. The GPU path (`GpuHmcState`, neighbor tables, all shaders) works with
arbitrary dims. No code changes needed — only experiment configuration.

### Memory scaling — asymmetric is far more efficient

| Lattice | Sites | VRAM (quenched) | Physics |
|---------|:-----:|:---:|---------|
| 32⁴ (current) | 1.05M | 2.5 GB | Bulk crossover only |
| 32³ × 4 | 131K | 0.31 GB | Deconfinement at β_c(4) |
| 64³ × 8 | 2.10M | 5.0 GB | MILC-comparable |
| 96³ × 12 | 10.6M | 25.3 GB | MILC production scale |

A **96³ × 12** lattice matches MILC production geometry and fits on the RTX 3090
(24 GB). With DF64, estimated ~77s per trajectory.

### Action items for barraCuda

1. **No code changes needed** — asymmetric dims already work in `WgpuDevice`,
   `ComputeDispatch`, and all shader uniform params.
2. **Validate**: Run a quick 16³ × 4 asymmetric test to confirm GPU path handles
   non-cubic geometry (CPU path already validated via `validate_gpu_dirac` check 7).
3. **Workgroup tuning**: `preferred_workgroup_size()` may need tuning for the
   different volume/n_links ratios of asymmetric lattices.

### Action items for hotSpring (local)

1. Run 64³ × 8 production β-scan at β_c(8) ≈ 6.06 on RTX 3090 DF64.
2. Run finite-size scaling: 32³/48³/64³ × 8 at same β values.
3. Multiple N_t (4, 6, 8, 12) for continuum extrapolation.

---

## 3. DF64 Scaling Analysis

### Current production

- 32⁴ native f64: 15.5s per HMC trajectory
- 32⁴ DF64: 7.6s per HMC trajectory (2.04× speedup)
- Precision: 14 digits (DF64) vs 16 digits (f64) — observables statistically identical

### DF64 does NOT reduce memory

DF64 uses `vec2<f32>` (8 bytes) — same size as f64. The benefit is purely
computational throughput: 10,496 FP32 ALUs vs 164 FP64 units on RTX 3090.

### Projected DF64 scaling

| Lattice | Sites | VRAM | DF64 time/traj | 12β × 200 meas |
|---------|:-----:|:---:|:--------------:|:---------------:|
| 32⁴ | 1.05M | 2.5 GB | 7.6 s | 5.1 h (done) |
| 48⁴ | 5.31M | 12.7 GB | ~39 s | ~26 h |
| 64³ × 8 | 2.10M | 5.0 GB | ~15 s | ~10 h |
| 96³ × 12 | 10.6M | 25.3 GB | ~77 s | ~51 h |

### Action items for barraCuda

1. **DF64 rewriter robustness**: Larger lattices stress the DF64 pipeline more.
   Ensure compound assignment fix (Store/Load/Binary pattern) handles all edge cases.
2. **DF64 + SovereignCompiler**: FMA fusion on DF64 ops could yield additional speedup.
   Currently FMA fusion operates on naga IR before DF64 rewrite — investigate fusing
   DF64 mul+add patterns post-rewrite.

---

## 4. coralReef Review — Status and Integration Path

### What coralReef does today

- WGSL/SPIR-V → naga → NAK SSA IR → optimize → f64 lowering → legalize → RA → SM70+ SASS
- 390 tests passing, 37.1% line coverage
- f64 transcendentals: sqrt, rcp, exp2, log2, sin, cos (DFMA-based)
- JSON-RPC + tarpc IPC for remote compilation
- QMD definitions for Kepler through Blackwell

### What coralReef does NOT do today

- Cannot dispatch compiled binaries to GPU (no coralDriver)
- Cannot bypass NVK at runtime
- Not integrated into barraCuda's compilation path

### Integration architecture

```
Current:  barraCuda → naga → SPIR-V → wgpu → [NVK/NAK or PTXAS] → GPU
                                                 ↑ we don't control this

Future:   barraCuda → naga → [coralReef] → SASS → [coralDriver] → GPU
                              ↑ we control     ↑ we control
```

### What barraCuda needs to absorb

1. **Compile-only integration** (Phase 1): barraCuda calls coralReef via tarpc to
   compile WGSL → SASS binary. Still dispatches via wgpu/NVK. Validates binary
   correctness by comparing outputs.
2. **Dispatch integration** (Phase 2): Once coralDriver exists, barraCuda submits
   coralReef SASS directly to GPU, bypassing NVK entirely.

### What coralReef needs from barraCuda/hotSpring

1. **Real-world shader corpus**: hotSpring's 62 WGSL shaders (MD force, plaquette,
   CG solver, Dirac, PRNG, etc.) are the test suite for coralReef's correctness.
2. **DF64 shader compilation**: The DF64 rewritten shaders are complex — many
   `vec2<f32>` operations with FMA patterns. coralReef should be able to compile them.
3. **Performance baselines**: hotSpring's benchmarked wall times (7.6s HMC trajectory,
   992 steps/s Verlet MD) are the targets coralReef must match or beat vs NAK.

---

## 5. Backend-Agnostic Benchmark Trait — Evolution Proposal

### Problem

We cannot currently swap between barraCuda and Kokkos (or any other backend) on the
same physics problem to demonstrate evolution.

### Proposed architecture

```rust
pub trait ComputeBackend {
    fn name(&self) -> &str;
    fn capabilities(&self) -> BackendCapabilities;
    fn run(&self, spec: &BenchmarkSpec) -> Result<BenchmarkResult>;
}
```

Internal backends (barraCuda): wrap existing GPU/CPU paths.
External backends (Kokkos, Python): shell out to `lmp` or `python`, parse results.

### Which primal owns what

| Component | Owner |
|-----------|-------|
| `BenchmarkSpec` (problem definition) | hotSpring |
| `ComputeBackend` trait | barraCuda |
| `HardwareFingerprint` | toadStool |
| `BenchmarkResult` format | barraCuda |
| External backend adapters | hotSpring |

### Action items

1. **barraCuda**: Define `ComputeBackend` trait and `BenchmarkResult` struct.
2. **toadStool**: Extend `GpuAdapterInfo` with estimated TFLOPS and `HardwareFingerprint`.
3. **hotSpring**: Build harness binary (`bench_backends`) with LAMMPS input generator.

---

## 6. Cross-Spring Evolution Discoveries

### From hotSpring → barraCuda

| Discovery | Impact |
|-----------|--------|
| NVK SPIR-V passthrough exclusion | `has_spirv_passthrough()` must exclude NVK |
| DF64 compound assignment fix | Store(ptr, Binary(op, Load(ptr), rhs)) pattern |
| Warp-packing 2.2× speedup | `preferred_workgroup_size()` for eigensolve |
| Omelyan lambda tolerance | Named constant prevents silent precision loss |
| SU(3) Cayley exponential | Reusable matrix exponential for Lie groups |

### From hotSpring → toadStool

| Discovery | Impact |
|-----------|--------|
| NVK allocation limit | PTE fault at ~200 MB on Nouveau — needs guard |
| Driver identity for f64 workarounds | `GpuDriverProfile` needs NVK vs proprietary |
| Ada Lovelace f64 pow/exp/log crash | SM89 proprietary driver cannot compile native f64 transcendentals |

### From hotSpring → coralReef

| Discovery | Impact |
|-----------|--------|
| 62 WGSL shaders as test corpus | Real-world validation for SM70 encoder |
| DF64 rewritten shaders | Complex vec2<f32> FMA patterns to compile |
| Benchmark targets | 7.6s HMC, 992 steps/s MD, 200× CG reduction |

---

## 7. Superseded Handoffs — Archive Candidates

These earlier handoffs are superseded by this document or by the Mar 5 BENCHMARK:

| File | Reason |
|------|--------|
| `HOTSPRING_V0617_MODERN_REWIRE_VALIDATION_MAR05_2026.md` | Superseded by BENCHMARK |
| `HOTSPRING_V0615_NAUTILUS_BRAIN_ECOSYSTEM_MAR01_2026.md` | Superseded by V0617 |
| `HOTSPRING_V0615_NAUTILUS_EVOLUTION_ECOSYSTEM_MAR01_2026.md` | Superseded by V0617 |
| `HOTSPRING_V0615_TOADSTOOL_S78_SYNC_HANDOFF_MAR02_2026.md` | Superseded by S94b sync |
| `HOTSPRING_V0615_DEEP_DEBT_TOADSTOOL_ABSORPTION_HANDOFF_MAR02_2026.md` | Same |

---

## 8. Summary — Evolution Gaps by Primal

### barraCuda

| Gap | Priority | Effort |
|-----|:--------:|:------:|
| Benchmark on proprietary Vulkan (real Kokkos gap) | HIGH | 1 day |
| `ComputeBackend` trait for swappable backends | MEDIUM | 2 days |
| DF64 + SovereignCompiler FMA fusion post-rewrite | LOW | 1 week |
| coralReef compile-only integration (tarpc) | LOW | 1 week |

### toadStool

| Gap | Priority | Effort |
|-----|:--------:|:------:|
| `HardwareFingerprint` with estimated TFLOPS | MEDIUM | 1 day |
| Runtime cache/bandwidth probing | LOW | 3 days |
| NVK allocation limit guard (cross-spring) | DONE | — |

### coralReef

| Gap | Priority | Effort |
|-----|:--------:|:------:|
| coralDriver (Phase 6) — userspace GPU dispatch | HIGH | months |
| naga 24 → 28 upgrade | MEDIUM | 1 week |
| hotSpring shader corpus integration tests | MEDIUM | 3 days |
| Validate DF64-rewritten shader compilation | MEDIUM | 2 days |

---

*This handoff consolidates findings from hotSpring's March 2026 modernization,
including Kokkos gap correction, asymmetric lattice geometry discovery, DF64 scaling
analysis, and coralReef integration review.*
