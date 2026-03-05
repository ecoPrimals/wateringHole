# Cross-Spring Notice: Kokkos GPU Parity — Driver Constraint and Path Forward

**Date**: March 5, 2026
**From**: hotSpring
**To**: groundSpring, barraCuda, toadStool
**Type**: NOTICE — Kokkos GPU Comparison Blocked by Driver
**Priority**: P0 for Chuna review package

---

## Problem

The Kokkos/LAMMPS vs barraCuda comparison MUST be **GPU vs GPU**. CPU vs GPU
is apples to oranges and proves nothing about competitiveness.

| What we need | What we have |
|---|---|
| Kokkos-CUDA on GPU | Kokkos-OpenMP on CPU (64 threads) |
| LAMMPS pair_style yukawa/kk on CUDA | LAMMPS pair_style yukawa/kk on OpenMP |
| nvidia.ko (proprietary driver) | NVK (open-source Vulkan) |

**Why we can't run Kokkos-CUDA**: CUDA runtime requires the proprietary
NVIDIA driver (`nvidia.ko`). We run NVK (Mesa/Nouveau Vulkan) for open-source
sovereignty. NVK does not support CUDA.

---

## Current Results (CPU, for reference only)

### LAMMPS/Kokkos-OpenMP (N=2048, 64 threads, Threadripper 3970X)

| Case | Production loop time | Steps/s | Wall time |
|------|---------------------|---------|-----------|
| k1_G14 | 543.49s / 10K | 18.4 | 11:58 |
| k1_G72 | 526.90s / 10K | 19.0 | 11:36 |
| k1_G217 | 523.13s / 10K | 19.1 | 11:33 |
| k2_G31 | 536.33s / 10K | 18.6 | 11:48 |
| k2_G158 | running... | | |

Note: 64 threads for 2048 atoms is massively over-parallelized (32 atoms/thread).
4–8 threads would be significantly faster. These numbers are NOT competitive
benchmarks — they're just what we have.

### barraCuda GPU — Native f64 (N=2000, RTX 3090, NVK)

| Metric | Value |
|--------|-------|
| Equil steps/s | 29.2 (5000 steps in 171s) |
| Energy conservation | E=2295.56 ± 0.01 over 15K production steps |
| FP64 rate | 1/64 (consumer Ampere) |
| Pipeline | barraCuda polyfill (exp_f64, log_f64 + native sqrt/round) |

### Python (Sarkas baseline, N=500, vectorized NumPy)

| Metric | Value |
|--------|-------|
| Steps/s | 30–35 |
| Drift | 0.000% (all 9 cases) |
| Purpose | Correctness validation only |

---

## Path to GPU vs GPU Comparison

### Option 1: Proprietary driver switch (FASTEST)

```bash
# Switch to proprietary NVIDIA driver
sudo apt install nvidia-driver-550
# Reboot, rebuild LAMMPS with Kokkos-CUDA
cmake -D Kokkos_ENABLE_CUDA=ON -D Kokkos_ARCH_AMPERE86=ON ...
# Run Kokkos-CUDA benchmarks
# Switch back to NVK for barraCuda benchmarks
```

**Pros**: Real hardware numbers on our exact GPUs (RTX 3090 + Titan V)
**Cons**: Requires reboot cycle, NVK ↔ proprietary switching

### Option 2: Published Kokkos-CUDA benchmarks from literature

Kokkos pair_style yukawa on CUDA is well-benchmarked:

- LAMMPS Kokkos benchmarks: https://docs.lammps.org/Speed_kokkos.html
- Thompson et al., Comp Phys Comm 271, 108171 (2022) — LAMMPS scaling data
- Chuna uses LAMMPS/Kokkos-CUDA daily at MSU/ICER — he HAS these numbers

**Pros**: No driver switching needed, peer-reviewed numbers
**Cons**: Different hardware, harder to normalize

### Option 3: Ask Chuna to run our cases on his ICER cluster

Chuna has access to NVIDIA V100/A100 at MSU ICER. He could:
1. Run our 9 LAMMPS input files (already written, in `lammps_results/`)
2. Report wall times with Kokkos-CUDA backend
3. We report barraCuda GPU numbers on matching hardware (if available)

**Pros**: Directly comparable, builds collaboration
**Cons**: Requires coordination, timeline dependency

### Option 4: Docker with NVIDIA Container Toolkit (if nvidia.ko is loadable)

If the proprietary driver kernel module exists but we're just not using it:
```bash
# Use nvidia-container-toolkit to run LAMMPS-CUDA in a container
# without switching the host display server
docker run --gpus all lammps-kokkos-cuda ...
```

**Pros**: No reboot, no display server change
**Cons**: Still needs nvidia.ko loaded

---

## Recommended Approach

**Phase 1 (immediate)**: Use published Kokkos-CUDA benchmarks to estimate
the gap. The Kokkos benchmarks page has pair_style yukawa/kk CUDA numbers.
Scale to our N and hardware.

**Phase 2 (Chuna collaboration)**: Send him our 9 LAMMPS input files.
He runs them on ICER with Kokkos-CUDA. We get real numbers.

**Phase 3 (when DF64 is fixed)**: barraCuda DF64 on consumer GPU should be
competitive with Kokkos-CUDA. This is the headline comparison:

```
barraCuda DF64 (WGSL, open-source driver, any Vulkan GPU)
  vs
Kokkos-CUDA (CUDA, proprietary driver, NVIDIA only)
```

If barraCuda DF64 matches Kokkos-CUDA within 2×, that's a win for sovereignty.
If it beats Kokkos-CUDA, that's a publication.

---

## What barraCuda Needs for the Comparison

1. **DF64 pipeline working on NVK** (see companion handoff:
   `HOTSPRING_BARRACUDA_DF64_NAK_SOVEREIGN_HANDOFF_MAR05_2026.md`)

2. **Benchmark infrastructure**: `sarkas_gpu` already reports steps/s, wall
   time, energy drift. Needs to also report:
   - GPU memory bandwidth utilization
   - Kernel launch latency vs compute time
   - DF64 vs native f64 precision comparison (same run, both paths)

3. **Cell-list performance at scale**: For N > 5000, cell-list shaders should
   activate. These also need DF64 validation on NVK.

---

## LAMMPS Input Files Ready

The 9 cases are generated and tested in:
```
hotSpring/benchmarks/kokkos-lammps/lammps_results/in.k*
```

These can be sent directly to Chuna or run on any LAMMPS installation with
Kokkos-CUDA enabled. They use `units lj`, `pair_style yukawa`, standard
NVT + NVE workflow.

---

## Performance Results (Updated March 5, 2026)

| Implementation | Steps/s (N=2000) | Driver | Algorithm | Hardware lock-in |
|---|---|---|---|---|
| Python (Sarkas) | 32 | n/a | all-pairs | None |
| barraCuda CPU (Rust f64) | ~5,000 | n/a | all-pairs | None |
| LAMMPS/Kokkos-OpenMP | ~19 | n/a | neighbor list | None |
| LAMMPS/Kokkos-CUDA | **730–3,699** | nvidia.ko | **neighbor list** | **NVIDIA only** |
| barraCuda GPU native f64 | 29 | NVK | all-pairs | None |
| barraCuda GPU DF64 (all-pairs) | 293–326 | nvidia | all-pairs | nvidia driver |
| **barraCuda GPU DF64 (Verlet)** | **368–992** | **nvidia** | **Verlet neighbor list** | **nvidia driver** |

**Gap closed**: 27× → **3.7×** at κ=3 (Verlet 992 vs Kokkos-CUDA 3,699 steps/s).
9/9 PP Yukawa DSF cases pass with ≤0.004% energy drift.

### What Closed the Gap
1. ✅ DF64 on FP32 cores: 27 → 293 steps/s (11× gain)
2. ✅ Cell-list O(N): ~1× at N=2000 (overhead matches all-pairs at coarse grid)
3. ✅ **Verlet neighbor list**: 293 → 992 steps/s (3.4× gain at κ=3)

### Remaining 3.7× Gap
The gap is dispatch overhead and GPU occupancy, not algorithm:
1. Streaming dispatch optimization (~1.5×)
2. Workgroup size tuning (~1.2×)
3. Adaptive skin tuning for hot systems (~1.2× for k2_G31)

These are engineering problems, not physics problems. The math and algorithm
are now at parity with Kokkos/LAMMPS.

---

*GPU vs GPU. Not GPU vs CPU. That's the only comparison that matters.*
