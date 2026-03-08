# Cross-Spring Notice: BarraCuda Kokkos Validation Baseline

**Date**: March 4, 2026
**From**: groundSpring
**To**: hotSpring (P0), barraCuda, toadStool
**Type**: FRAGO (Fragmentation Order)

---

## Context

Murillo pointed us at **Kokkos** (Sandia's C++ performance portability
framework) as the right comparison target for BarraCuda. His PhD student
**Thomas Chuna** — who co-authored with Bazavov on SU(3) Lie group
integrators for MILC and published on the DSF/dielectric theory with
Murillo — is the person to prepare a review package for.

Chuna can evaluate our WGSL shaders against MILC production code he
contributed to, and benchmark our Yukawa MD against Kokkos/LAMMPS he
uses daily at MSU/ICER.

## New Evolution Path

```
Python (Sarkas) → Kokkos (LAMMPS) → Rust (hotSpring) → GPU (BarraCuda) → sovereign
```

Python validates correctness. Kokkos validates competitiveness.

## Action Items

### hotSpring (P0 — entry point)

1. Map 9 PP Yukawa DSF cases to LAMMPS input files
2. Record Tier 1 benchmarks (wall time, energy drift, GPU util)
3. Document PPPM comparison (WGSL vs cuFFT)
4. Prepare Chuna review package (physics-first)
5. Experiment plan: `experiments/040_KOKKOS_LAMMPS_VALIDATION.md`

### barraCuda

- Ensure `sarkas_gpu` validation results are documented and reproducible
- PPPM shader performance numbers extracted for comparison
- DF64 precision validation data packaged

### toadStool

- Kokkos build system comparison notes (CMake + Kokkos vs Cargo + wgpu)
- Cross-spring shader evolution documentation updated

## Chuna Review Package Contents

1. Sarkas reproduction (his group's code) — 12 cases, 9/9 GPU
2. Lattice QCD β-scan — quenched 10/10, dynamical 7/7, GPU 8/8
3. PPPM implementation — vendor-agnostic Ewald sum in WGSL
4. DF64 precision validation — f64 storage + f32-pair arithmetic
5. Performance data vs MILC/ICER (he knows those numbers)
6. Public repos: hotSpring, barraCuda (AGPL-3.0)

## References

- Chuna & Bazavov (2021): arXiv:2101.05320 (SU(3) gradient flow integrators)
- Chuna & Murillo (2024): arXiv:2405.07871 (conservative dielectric functions)
- Kokkos: Edwards et al., JPDC 74(12), 2014
- Cabana: https://github.com/ECP-copa/Cabana
- LAMMPS Kokkos: https://docs.lammps.org/Speed_kokkos.html

---

*hotSpring is the entry point. Sketch LAMMPS benchmarks while 32⁴
dynamical run is GPU-bound.*
