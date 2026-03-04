# barraCuda Evolution Notice: Kokkos as Validation Baseline

**Date**: March 4, 2026
**From**: groundSpring / hotSpring (cross-spring notice)
**To**: All Springs, ToadStool, barraCuda
**Priority**: P1 — affects evolution path for all Springs
**Type**: New validation tier announcement

---

## Summary

Kokkos (Sandia National Laboratories) is now a **validation baseline** for
barraCuda evolution, alongside the existing Python baselines. The evolution
path becomes:

```
Python baseline → Kokkos baseline → Rust validation → GPU acceleration → sovereign pipeline
```

**Python validates correctness. Kokkos validates competitiveness.**

---

## What Is Kokkos

Kokkos is a C++ performance portability framework from Sandia, used in
production DOE codes including LAMMPS, Trilinos, ExaWind, and EMPIRE.

| Aspect | Kokkos | barraCuda |
|--------|--------|-----------|
| Language | C++ templates | Rust + WGSL shaders |
| GPU backend | CUDA, HIP, SYCL, OpenMP | WebGPU/Vulkan (WGSL) |
| Portability | Compile-time backend selection | Runtime shader dispatch |
| Vendor SDK | **Required** (CUDA toolkit, ROCm, oneAPI) | **Not required** — Vulkan driver only |
| Maturity | 10+ years, DOE production | < 1 year |
| License | BSD-3-Clause | AGPL-3.0 |

Related Sandia frameworks: **Cabana** (particle methods on Kokkos),
**ArborX** (geometric search on Kokkos), **Cajita** (structured grids).

Key references:
- Edwards et al., "Kokkos: Enabling manycore performance portability through
  polymorphic memory access patterns," JPDC 74(12), 2014
- Trott et al., "Kokkos 3: Programming Model Extensions for the Exascale Era,"
  IEEE CiSE 24(4), 2022
- Cabana: https://github.com/ECP-copa/Cabana

---

## Why This Matters

Our current evolution validates Rust against Python. Python is correct but
slow — beating Python on performance is not a meaningful benchmark for GPU
compute. Kokkos/Cabana represents the **state of the art** in portable HPC:

1. **Honest benchmarking**: If barraCuda WGSL shaders match or beat Kokkos
   CUDA/HIP kernels on the same physics, that's a real result
2. **Identifies gaps**: Where Kokkos is faster, we learn what to optimize
3. **Credibility**: Faculty reviewers (Murillo, Bazavov) know Kokkos — having
   it as a baseline makes our performance claims auditable
4. **Architecture validation**: Proves that runtime WGSL dispatch can compete
   with compile-time backend selection

---

## Three-Tier Validation (Updated)

```
Tier 0: Python baseline          — correctness reference (bit-exact or documented tolerance)
Tier 1: Kokkos/Cabana baseline   — performance reference (same physics, production HPC tooling)
Tier 2: barraCuda (Rust + WGSL)  — sovereign implementation (no vendor SDK, AGPL-3.0)
```

Each spring should maintain:
- **Tier 0 parity**: Rust matches Python to documented tolerance (existing requirement)
- **Tier 1 benchmark**: Performance comparison against Kokkos for GPU-promoted workloads
- **Tier 2 sovereignty**: No CUDA, no vendor SDK, same binary runs on NVIDIA/AMD/Intel

---

## Affected Springs

| Spring | Kokkos-Relevant Workloads | Priority |
|--------|---------------------------|----------|
| **hotSpring** | Yukawa MD (PPPM, pair forces), lattice QCD (HMC), nuclear EOS | P0 — direct Sarkas/LAMMPS comparison |
| **groundSpring** | Anderson localization (spectral), Monte Carlo sampling | P1 — spectral methods, stochastic |
| **wetSpring** | Gillespie SSA batch, rarefaction Monte Carlo | P2 — bio Monte Carlo |
| **airSpring** | FAO-56 batch, seasonal pipeline | P2 — mostly element-wise |
| **neuralSpring** | ESN reservoir, HMM forward | P3 — ML workloads less Kokkos-relevant |

### hotSpring Is the Entry Point

hotSpring's Sarkas MD reproduction is the natural first target:
- Sarkas is Python-based; LAMMPS is the C++/Kokkos equivalent
- Same Yukawa OCP physics, same PPPM electrostatics
- Direct comparison: Sarkas (Python) vs LAMMPS/Kokkos (C++/CUDA) vs
  barraCuda (Rust/WGSL) on identical DSF cases

---

## Action Items for Springs

### Immediate (This Week)

1. **hotSpring**: Identify LAMMPS Kokkos benchmark cases that overlap with
   existing Sarkas DSF reproduction (9 PP Yukawa cases). Document LAMMPS
   input files and expected observables.

2. **barraCuda**: Add `RELATED_WORK.md` documenting Kokkos architecture
   comparison, Cabana particle methods, and key differences in dispatch model.

### Near-Term (This Month)

3. **hotSpring**: Run LAMMPS/Kokkos on identical Yukawa OCP cases. Record
   wall time, energy drift, FLOPS, memory bandwidth. This becomes the Tier 1
   performance baseline.

4. **groundSpring**: Identify Kokkos kernels for spectral methods (tridiagonal
   eigensolvers, Anderson Hamiltonian) if they exist in Trilinos or other
   Kokkos-based libraries.

5. **All Springs**: Update validation binary headers to include Tier 1
   benchmark reference where applicable.

### Evolution (This Quarter)

6. **barraCuda**: Profile WGSL shader performance against Kokkos CUDA backend
   on shared workloads. Document where we win, where we lose, and why.

7. **ToadStool**: Evaluate whether Kokkos reduction patterns (`parallel_reduce`,
   `parallel_scan`) suggest missing primitives in barraCuda's WGSL shader
   library.

---

## Kokkos Execution Model — Key Concepts for Springs

Springs do not need to learn Kokkos in depth. The relevant concepts:

- **Execution Space**: Where code runs (Serial, OpenMP, CUDA, HIP, SYCL)
- **Memory Space**: Where data lives (HostSpace, CudaSpace, HIPSpace)
- **View**: N-dimensional array with layout and memory space — analogous to
  our `wgpu::Buffer` bindings
- **parallel_for / parallel_reduce / parallel_scan**: The three dispatch
  primitives — analogous to our `@compute` WGSL entry points
- **TeamPolicy**: Hierarchical parallelism (team → thread → vector) —
  analogous to our `@workgroup_size` and subgroup operations

The key architectural difference: Kokkos selects the backend at **compile
time** via CMake flags. barraCuda selects the backend at **runtime** via
`wgpu` adapter enumeration. This means:

- Kokkos: one binary per backend, optimal codegen per target
- barraCuda: one binary for all backends, WGSL JIT by driver

The performance question is whether WGSL JIT can match backend-specific
codegen. Our DF64 results suggest it can for compute-bound kernels.

---

## Provenance

- **Origin**: Coffee meeting with Professor Michael Murillo (MSU CMSE),
  March 4, 2026. He asked how we compare to Kokkos — the right question.
- **Context**: Murillo's domain (plasma MD) is exactly where Kokkos/LAMMPS
  is strongest. Sarkas (his group's code) is the Python baseline; LAMMPS is
  the production C++ baseline. Having both makes our evolution path credible.

---

*This is a cross-spring notice. All springs should acknowledge receipt in
their next version handoff.*
