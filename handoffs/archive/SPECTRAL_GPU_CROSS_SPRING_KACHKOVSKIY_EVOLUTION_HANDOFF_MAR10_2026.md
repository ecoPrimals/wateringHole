# Spectral GPU — Cross-Spring Kachkovskiy Evolution Handoff

**Date**: March 10, 2026
**From**: Cross-spring audit (hotSpring, groundSpring, wetSpring, neuralSpring, barraCuda)
**To**: barraCuda team, hotSpring, groundSpring
**Context**: Kachkovskiy outreach preparation — inventory of spectral primitives, GPU validation status, remaining work, and benchmark gaps
**License**: AGPL-3.0-or-later

---

## Executive Summary

Anderson localization and spectral theory are the most deeply validated
primitives in the ecosystem: **417+ checks** across 4 springs, reproducing
**11 foundational papers** in Kachkovskiy's domain. CPU validation (Python
control + Rust parity) is complete everywhere. GPU validation exists but
has critical gaps that weaken the value proposition for Kachkovskiy's
RTX 5080 — specifically: no large-N scaling data, no SciPy comparison
benchmarks, no two-particle Anderson GPU, and no formal CUDA/Kokkos
comparison for spectral workloads.

This handoff identifies what each spring and barraCuda needs to deliver
to close those gaps.

---

## Part 1: Current State by Spring

### hotSpring — 45/45 checks (Papers 14-22)

| Binary | Checks | Tier | Status |
|--------|:------:|:----:|--------|
| `validate_spectral` | 10/10 | CPU | Anderson 1D, Lyapunov, Aubry-André, Herman γ=ln\|λ\| |
| `validate_lanczos` | 11/11 | CPU | SpMV parity, Lanczos vs Sturm, 2D Anderson, GOE→Poisson |
| `validate_anderson_3d` | 10/10 | CPU | Mobility edge W_c=16.26, dimensional hierarchy |
| `validate_hofstadter` | 10/10 | CPU | Band counting q=2,3,5, Cantor measure, Ten Martini |
| `validate_gpu_spmv` | 8/8 | **GPU** | CSR SpMV parity 1.78e-15 (N up to 4096) |
| `validate_gpu_lanczos` | 6/6 | **GPU** | Eigenvalues match CPU to 1e-15 (N up to 144) |

**toadStool absorption**: Complete. 41KB local spectral code deleted. hotSpring
re-exports from `barracuda::spectral::*`. Write → Absorb → Lean cycle finished.

**Speedup**: Rust 8× faster than Python (4.7s vs 38.3s) for full spectral suite.

**Gaps**:
- 3D Anderson GPU validation missing (large sparse matrix, P2)
- Hofstadter GPU not applicable (Sturm chain is CPU-natural)
- GPU SpMV validated only to N=4096 (64×64 lattice)
- GPU Lanczos validated only to N=144 (12×12 lattice)
- No timing comparison vs SciPy `eigsh` / ARPACK

### groundSpring — 86/86 checks (Exp 008, 009, 012, 018)

| Experiment | Checks | Python | Rust | GPU | Speedup |
|-----------|:------:|:------:|:----:|:---:|--------:|
| Exp 008 Anderson | 8+8 | Done | Done | Wired (`lyapunov_*`) | 29.8× vs Py |
| Exp 009 Almost-Mathieu | 8+8 | Done | Done | Wired (`find_all_eigenvalues`) | **47.4×** |
| Exp 012 Spin chain | 18+18 | Done | Done | **Partial** (eigenvalues GPU, eigenvectors CPU) | — |
| Exp 018 Band edge | 8+10 | Done | Done | Wired (`brent` optimizer) | — |

**Papers**:
- Paper 15: Bourgain & Kachkovskiy (2018) GAFA → Exp 008
- Paper 16: Jitomirskaya & Kachkovskiy (2018) JEMS → Exp 009
- Paper 17: Kachkovskiy (2016) CMP → Exp 012
- Paper 18: Filonov & Kachkovskiy (2018) Acta Math → Exp 018

**Gaps**:
- GPU eigenvectors blocked (`tridiag_eigh` not in barraCuda)
- Two-particle transfer matrix chain multiplication not implemented
- No large-lattice GPU scaling validation

### wetSpring — 312+ checks (Exp 107-149)

| Experiment | Checks | Status |
|-----------|:------:|--------|
| Exp107 spectral cross-spring | 25/25 | Complete — Anderson 1D/2D/3D + QS-disorder bridge |
| Exp113-149 QS applications | 287+ | Complete — 28-biome atlas, NPU classifier, 3D phase |

**No gaps**: wetSpring is application-layer. Consumes from barraCuda. N ≤ 1000
at validation scale; GPU not needed for current workloads.

### neuralSpring — 16/16 checks (Papers 022-023)

| Paper | Checks | Status |
|-------|:------:|--------|
| 022 Kachkovskiy-Safarov (spectral commutativity) | 8/8 | All tiers through GPU pipeline |
| 023 Bourgain-Kachkovskiy (Anderson localization) | 8/8 | All tiers through GPU pipeline |

**Benchmarks**: Rust 38.6× faster than Python. GPU ~104× at 103M FLOPs.

**Gaps**: neuralSpring handoff (S139) notes "No Kokkos / Galaxy GPU parity
benchmark document found" and recommends `bench/gpu_kokkos/`.

---

## Part 2: barraCuda `spectral/` Module Status

### Files (15 total)

| File | What | Status |
|------|------|--------|
| `anderson.rs` | 1D/2D/3D Hamiltonians, Lyapunov, localization | **Complete** |
| `hofstadter.rs` | Harper equation, butterfly, Ten Martini | **Complete** |
| `lanczos.rs` | Lanczos eigensolve (CPU + GPU inner SpMV) | **Partial** — GPU SpMV only |
| `sparse.rs` | CSR SpMV (CPU + GPU) | **Complete** |
| `stats.rs` | Level spacing ratio (GOE/GUE/Poisson) | **Complete** |
| `tridiag.rs` | Sturm chain, tridiagonal eigenvalues | **Complete** (CPU) |
| `batch_ipr.rs` | Inverse participation ratio (GPU batch) | **Complete** |

### WGSL Shaders (6 total)

| Shader | Precision | Status |
|--------|-----------|--------|
| `anderson_lyapunov_f64.wgsl` | f64 | Deployed |
| `anderson_lyapunov_f32.wgsl` | f32 | Deployed |
| `batch_ipr_f64.wgsl` | f64 | Deployed |
| `lanczos_iteration_f64.wgsl` | f64 | Deployed |
| `anderson_coupling_f64.wgsl` | f64 | Deployed |
| `fft_radix2_f64.wgsl` | f64 | Deployed |

### What's Missing in barraCuda

| Gap | Priority | Why |
|-----|:--------:|-----|
| **Fully GPU-resident Lanczos** | P1 | Current: GPU does SpMV, CPU does dot/axpy/reorthog. Need all-GPU for N > 10k |
| **GPU tridiag eigenvectors** (`tridiag_eigh`) | P1 | groundSpring Exp 012 blocked; spin chain dynamics needs eigenvectors |
| **Two-particle Anderson Hamiltonian** | P2 | Kachkovskiy's Bourgain paper. L² Hilbert space (L=200 → 40k×40k sparse) |
| **Large-N Lanczos scaling benchmark** | P1 | Only validated to N=144. Need N=1k, 4k, 10k, 40k scaling curve |
| **SciPy `eigsh` comparison harness** | P1 | Direct timing: barraCuda GPU Lanczos vs SciPy ARPACK on same matrix |
| **Kokkos/CUDA spectral comparison** | P2 | Plasma MD gap is 3.7× (LAMMPS). No spectral comparison exists |
| **GPU Anderson 3D sweep** | P2 | Embarrassingly parallel disorder sweep at L=10-50 |

---

## Part 3: Action Items by Team

### barraCuda Team

**P1 — Benchmark infrastructure** (blocks Kachkovskiy outreach)

1. **`bench_spectral_scaling`** — New binary. Lanczos eigensolve at N = 100, 500,
   1000, 4096, 10000, 40000. Report wall time, GPU utilization, memory. Compare
   CPU Lanczos vs GPU-SpMV Lanczos vs (target) fully-GPU Lanczos.

2. **`bench_scipy_comparison`** — Python harness calling `scipy.sparse.linalg.eigsh`
   on identical Anderson Hamiltonians at N = 100 → 40000. JSON output for
   direct overlay with barraCuda results. This is the benchmark Kachkovskiy
   will ask for first.

3. **Fully GPU-resident Lanczos** — Move dot product, axpy, and reorthogonalization
   to GPU shaders. Current bottleneck: GPU→CPU→GPU round trips per Lanczos
   iteration. For N > 10k, the dispatch overhead dominates.

**P1 — Missing primitive**

4. **`tridiag_eigh`** — GPU tridiagonal eigenvector solver. Unblocks groundSpring
   Exp 012 GPU tier. Options: divide-and-conquer (Cuppen), implicit QL on GPU,
   or bisection + inverse iteration.

**P2 — Kachkovskiy-specific**

5. **Two-particle Anderson Hamiltonian builder** — Tensor product of two 1D
   Anderson lattices with interaction term. Produces L²×L² sparse matrix.
   Consumes existing Lanczos for eigensolve. This is the headline feature
   for the Kachkovskiy pitch: his Bourgain paper on GPU.

6. **GPU Anderson 3D disorder sweep** — Embarrassingly parallel: generate N
   disorder realizations at each W, compute IPR and level statistics. Currently
   CPU-only in hotSpring `validate_anderson_3d`.

### hotSpring

**P1 — GPU scaling validation**

1. **Extend `validate_gpu_lanczos`** — Add checks at N = 400 (20×20 lattice),
   N = 900 (30×30), N = 2500 (50×50). Current max is N=144 (12×12). Report
   timing alongside parity.

2. **Extend `validate_gpu_spmv`** — Add N = 10000 (100×100 lattice), N = 40000
   (200×200). Current max is N=4096 (64×64). This demonstrates the scale
   Kachkovskiy works at.

3. **`validate_gpu_anderson_3d`** — New binary. 3D Anderson at L=10 (1000 sites),
   L=20 (8000 sites), L=30 (27000 sites). GPU Lanczos for eigenvalues, report
   mobility edge and timing.

**P2 — SciPy comparison**

4. **`spectral_benchmark.py`** — Python script in `control/` that runs
   `scipy.sparse.linalg.eigsh` on identical Hamiltonians. JSON output matching
   Rust benchmark format. Enables direct "our GPU vs your SciPy" comparison.

### groundSpring

**P1 — GPU completion**

1. **Exp 012 GPU eigenvectors** — Blocked on barraCuda `tridiag_eigh`. Once
   available, wire into `validate-transport` for full GPU tier.

2. **Two-particle validation prep** — Define the Bourgain-Kachkovskiy two-particle
   Hamiltonian in `anderson.rs`. Python control first (L=20-50), then Rust CPU,
   then GPU. This is Paper 15's full numerical verification.

**P2 — Scaling**

3. **Extend Exp 008 and 009 to larger lattices** — Current validation at small N.
   Add L=100, 500, 1000 for 1D Anderson. Add L=20, 50 for 2D. Report GPU
   speedup curves.

---

## Part 4: Paper Benchmarks We Can Compare Against

### Published Numerical Values (verified)

| Observable | Published | Our Result | Source |
|-----------|----------|------------|--------|
| 3D W_c (mobility edge) | 16.5 ± 0.5 | 16.26 ± 0.95 | Slevin & Ohtsuki (1999) |
| Critical exponent ν | 1.57 ± 0.02 | Consistent | Slevin & Ohtsuki (1999) |
| Herman Lyapunov γ | ln\|λ\| (exact) | 4 decimal places | Herman (1983) |
| Hofstadter q=2 bands | 2 (exact) | 2 | Hofstadter (1976) |
| Hofstadter q=3 bands | 3 (exact) | 3 | Hofstadter (1976) |
| Hofstadter q=5 bands | 5 (exact) | 5 | Hofstadter (1976) |
| Aubry-André transition | λ_c = 1 (exact) | Confirmed | Jitomirskaya (1999) |
| GOE ⟨r⟩ | 0.5307 | Verified | Mehta (2004) |
| Poisson ⟨r⟩ | 0.3863 | Verified | Berry-Tabor (1977) |

### Computational Benchmarks We Do NOT Have (needed)

| Benchmark | Published Reference | What We'd Compare |
|-----------|-------------------|-------------------|
| SciPy `eigsh` (ARPACK) Lanczos timing | Standard tool — run ourselves | barraCuda GPU Lanczos |
| cuSPARSE SpMV throughput | NVIDIA documentation / benchmarks | barraCuda GPU SpMV (WGSL) |
| MAGMA GPU eigensolve | ICL Tennessee benchmarks | barraCuda GPU Lanczos |
| Kokkos sparse eigensolve | Trilinos/Anasazi benchmarks | barraCuda spectral stack |
| Julia/CUDA.jl sparse eigensolve | Community benchmarks | barraCuda (vendor-agnostic angle) |

### Internal Benchmarks We Have

| Metric | Value | Source |
|--------|-------|--------|
| Rust vs Python spectral suite | **8×** (4.7s vs 38.3s) | hotSpring |
| Almost-Mathieu GPU eigenvalues | **47.4×** vs CPU | groundSpring Exp 009 |
| neuralSpring GPU 15-domain | **104×** vs Python | neuralSpring |
| GPU SpMV parity | 1.78e-15 | hotSpring |
| GPU Lanczos parity | 1e-15 | hotSpring |
| Kokkos-LAMMPS plasma MD gap | 3.7× (down from 27×) | hotSpring (NOT spectral) |

---

## Part 5: Kachkovskiy Outreach Readiness

### Ready Now

- 11 papers reproduced in his domain
- 417+ automated checks passing
- GPU Lanczos validated to machine precision
- Hofstadter butterfly in ~3s on RTX 4070
- Public repos with runnable binaries

### Not Ready (blocks compelling demo)

| Gap | Impact on Pitch |
|-----|----------------|
| No SciPy comparison | Can't answer "how fast vs what I use?" |
| N ≤ 144 GPU Lanczos | Too small to impress — his lattices are 1000+ |
| No two-particle GPU | His Bourgain paper is the headline |
| No scaling curves | Can't show where GPU crosses CPU |

### Minimum Viable Demo for Kachkovskiy

1. **GPU Lanczos at N=10000+** with timing
2. **SciPy `eigsh` comparison** on same hardware (same matrix, wall time)
3. **Hofstadter butterfly visualization** (already have this)
4. **Anderson 3D mobility edge** on GPU with timing at L=20+

With items 1-4, the pitch becomes: "Here's your math running on a $600 GPU,
faster than SciPy on your CPU, at lattice sizes that matter for research.
No CUDA. Runs on your 5080."

---

## Recommended Priority

| Priority | Item | Team | Effort |
|:--------:|------|------|--------|
| **P0** | `bench_scipy_comparison` harness | hotSpring + barraCuda | 1 session |
| **P0** | Extend GPU Lanczos to N=10000 | barraCuda | 1-2 sessions |
| **P1** | Fully GPU-resident Lanczos | barraCuda | 2-3 sessions |
| **P1** | `tridiag_eigh` GPU eigenvectors | barraCuda | 2 sessions |
| **P1** | GPU Anderson 3D at L=20-30 | hotSpring | 1 session |
| **P2** | Two-particle Anderson builder | barraCuda + groundSpring | 2-3 sessions |
| **P2** | Kokkos spectral comparison | barraCuda | 2 sessions |
| **P2** | Scaling curve visualization | petalTongue | 1 session |
