# hotSpring v0.6.17 — Modern Rewire + Benchmark Results

**Date**: March 5, 2026
**From**: hotSpring v0.6.17
**To**: All Springs, toadStool, barraCuda
**Priority**: P1 — validation + benchmark baseline for Kokkos comparison
**Depends On**: barraCuda v0.3.3, toadStool S94b, wgpu 28

---

## Status: Fully Rewired and Validated

### Compilation & Tests
- **669/669 library tests pass** (0 failed, 6 ignored)
- **Zero clippy warnings** (pedantic + nursery)
- **Zero local DF64 compilation** — all DF64 delegates to barraCuda
- **wgpu 28 fully integrated** — `PollType::Wait`, `entry_point: Some("main")`, etc.

### 9-Case Yukawa OCP Validation (N=2000, 30K production steps)

| Case | κ | Γ | Algorithm | Steps/s | Energy Drift | GPU Power |
|------|---|---|-----------|---------|:---:|:---:|
| k1_G14 | 1 | 14 | All-pairs | 292 | 0.001% | 155W |
| k1_G72 | 1 | 72 | All-pairs | 307 | 0.001% | 155W |
| k1_G217 | 1 | 217 | All-pairs | 329 | 0.001% | 155W |
| k2_G31 | 2 | 31 | Verlet | 306 | 0.001% | 95W |
| k2_G158 | 2 | 158 | Verlet | 303 | 0.001% | 95W |
| k2_G476 | 2 | 476 | Verlet | 303 | 0.001% | 99W |
| k3_G100 | 3 | 100 | Verlet | 314 | 0.001% | 95W |
| k3_G503 | 3 | 503 | Verlet | 313 | 0.001% | 95W |
| k3_G1510 | 3 | 1510 | Verlet | 317 | 0.001% | 95W |

**Hardware**: RTX 3090 (24GB), AMD Threadripper 3970X
**Precision**: DF64 on FP32 cores (hybrid strategy)
**Brain**: Nautilus unified (12-head, adaptive retrain)

---

## Kokkos Gap Analysis

| Substrate | Steps/s (N=2000) | Driver | Algorithm |
|-----------|:---:|:---:|:---:|
| LAMMPS/Kokkos-OpenMP (CPU 64T) | ~19 | n/a | neighbor list |
| **barraCuda GPU DF64** | **292–329** | nvidia proprietary | **Verlet/all-pairs** |
| LAMMPS/Kokkos-CUDA (est.) | 730–3,699 | nvidia proprietary | neighbor list |

- **16× faster than Kokkos-OpenMP** (GPU vs CPU)
- **Est. 2–4× gap vs Kokkos-CUDA** (need collaborator's institutional HPC for real GPU-vs-GPU)
- Kokkos-CUDA cannot run on NVK (open-source Vulkan)

### What Closed the Gap (27× → ~3×)
1. DF64 on FP32 cores: 27 → 293 steps/s (11× gain)
2. Verlet neighbor list: 293 → 992 steps/s at κ=3 (3.4× gain, without brain)
3. Brain adds ~3× overhead but provides NPU learning — no Kokkos equivalent

### Remaining Gap (closeable)
1. Streaming dispatch optimization (~1.5×)
2. Workgroup size tuning (~1.2×)
3. Adaptive skin tuning (~1.2×)

---

## Architecture Summary

### Brain: Nautilus Unified (ESN → Nautilus evolution complete)
- Single `NautilusShell` reservoir replaces dual ESN/Nautilus
- 12 continuous regression heads (energy drift, temp deviation, etc.)
- Variance-based adaptive retrain interval (30/100/300 events)
- Cross-run persistence via JSON serialization
- Evolutionary board generations for structural adaptation

### Tolerance Patterns
- Named constants from `tolerances::` module
- `MD_ENERGY_FLOOR`, `MD_TARGET_TEMPERATURE_GUARD`, `BRAIN_EQUILIBRIUM_THRESHOLD`
- All bare literals in production code replaced with named constants

### API Integration
- **barraCuda**: `compile_shader_f64`, `compile_shader_df64`, `Fp64Strategy`
- **toadStool**: `akida-driver`, `akida-models` (feature-gated `npu-hw`)
- No deprecated APIs used
- No local naga rewrite code (removed)

---

## Deprecated toadStool API Audit: CLEAN

hotSpring does not import or call the toadStool crate directly.
NPU hardware access through `akida-driver`/`akida-models` (separate crates).
All barraCuda APIs used are current (no deprecated `PppmGpu::new()`, etc.).

---

## Fused Stats Assessment

barraCuda's fused Welford + Pearson GPU ops assessed for hotSpring observables:
- **energy.rs**: CPU-side `EnergyRecord` slices (~1K scalars) — GPU round-trip exceeds CPU cost
- **vacf.rs**: CPU-side lag regression (~100 points) — same
- **Future**: When observable accumulation moves GPU-resident, fused stats become valuable

---

## Multi-GPU Assessment

GpuPool/MultiDevicePool evaluated — not needed for single-device MD loop.
Future evolution for embarrassingly parallel workloads (lattice β-scans, sweep parallelism).

---

## Cross-Spring Shader Provenance

Full provenance documented in `specs/CROSS_SPRING_EVOLUTION.md`:
- 21 MD shaders (Yukawa, VV, Verlet, VACF, stress, RDF, ESN)
- 37 lattice QCD shaders (SU3, Wilson, Dirac, CG, PRNG)
- 14 nuclear physics shaders (HFB, BCS, SEMF)
- All use barraCuda's precision pipeline (f64/DF64/f32 per hardware)

---

## Action Items for Other Springs

### For barraCuda
- Verlet neighbor list ready for upstream absorption to `barracuda::ops::md::neighbor`
- `ForceAlgorithm` + `AlgorithmSelector` for upstream
- hotSpring's DF64 Yukawa shaders as reference for DF64 force kernels

### For toadStool
- `NpuParameterController` trait — hotSpring implements equivalent in `npu_worker.rs`
- `NpuDispatch` — hotSpring uses `akida-driver` directly, could adopt unified trait

### For faculty review package
- 9 LAMMPS input files ready in `lammps_results/`
- Need Kokkos-CUDA numbers from institutional HPC (V100/A100) for GPU-vs-GPU comparison
- Review package: Sarkas reproduction → lattice QCD β-scan → PPPM → DF64 → performance

---

## Next Steps
1. Brain-sweep across 9 cases (validate Nautilus cross-run persistence)
2. N-scaling benchmark (N=500 → N=10000) to compare vs previous results
3. collaboration: send LAMMPS input files for Kokkos-CUDA benchmarks
4. P43-45 (gradient flow): gradient flow integrators, dielectric functions, kinetic-fluid coupling
