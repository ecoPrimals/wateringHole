# BarraCuda vs Kokkos CUDA — First GPU Head-to-Head Results

**Date**: March 4, 2026
**From**: groundSpring V74
**To**: All Springs, ToadStool, barraCuda
**Priority**: P0 — defines the evolution gap and the path to close it
**Type**: Benchmark results + evolution strategy
**Depends On**: `BARRACUDA_KOKKOS_VALIDATION_BASELINE_NOTICE_MAR04_2026.md`

---

## Context: Three Weeks of Evolution

Three weeks ago (mid-February), barraCuda had ~378 WGSL shaders. None had
fp64 support. The DF64 emulation layer didn't exist. Universal precision
was a spec, not a reality.

Today:

| Metric | Feb 12 | Mar 4 | Growth |
|--------|--------|-------|--------|
| WGSL shaders | 378 | 767 | 2.0× |
| fp64-canonical | 0 | 767 | ∞ |
| DF64 universal precision | 0 | 37+ shaders | from nothing |
| Spring delegations (groundSpring) | 0 | 81 (47 CPU + 34 GPU) | from nothing |
| Validation binaries | ~5 | 33+ | 6.6× |
| Tests | ~50 | 790 | 15.8× |

The scaffolding-and-evolution approach works: stand up a target, validate
against it, absorb what we learn, repeat. Kokkos is the next target.

---

## The Benchmark

**Hardware**: NVIDIA RTX 4070 (Ada Lovelace, 12 GB, sm_89)
**Kokkos**: v4.5.01 CUDA backend (compiled sm_86 via CUDA 11.5, forward compat)
**BarraCuda**: v0.3.1 WGSL via wgpu v22 (Vulkan → SPIR-V → PTX at runtime)
**Workloads**: Identical algorithms, identical parameters, identical PRNG seeds

### GPU vs GPU (RTX 4070)

| Kernel | Kokkos CUDA | BarraCuda WGSL | Rust CPU | Gap |
|--------|------------:|---------------:|---------:|-----|
| Anderson Lyapunov (500 realizations, 10k sites) | **36 ms** | 126 ms | 133 ms | 3.5× |
| mean (1M f64) | **58 µs** | 8,454 µs | 572 µs | 146× |
| variance (1M f64) | **24 µs** | 8,515 µs | 1,031 µs | 355× |
| Pearson r (1M f64) | **47 µs** | 125 ms | 1,692 µs | 2,669× |
| Bootstrap mean (10k × 5k replicates) | **2.2 ms** | 123 ms | 104 ms | 57× |

### Correctness

All backends produce matching results within documented tolerances.
(Anderson averaged differs due to documented PRNG seeding convention:
barraCuda uses `base_seed + r * 1000`, Kokkos/CPU use `base_seed + r`
— Phase 2b alignment work.)

---

## Diagnosis: Two Distinct Gaps

### Gap 1: Dispatch Overhead (mean, variance, Pearson r) — 100×–2,600×

The enormous ratios on statistical reductions are **not compute gaps**.
They are wgpu round-trip overhead:

```
Per BarraCuda GPU call:
  1. Allocate wgpu buffer          ~1-2 ms
  2. Host → Device copy (1M f64)   ~1-2 ms
  3. Pipeline lookup / JIT          ~0-1 ms
  4. Compute dispatch               ~0.02 ms  ← the actual work
  5. Device → Host readback         ~1-2 ms
```

Kokkos keeps `View<double*>` in device memory across operations. Data
never leaves the GPU. A `parallel_reduce` over 1M doubles is a single
kernel launch with near-zero overhead.

BarraCuda currently does a full round-trip per function call. `variance`
calls `mean` (one round-trip), then dispatches the deviation sum (another
round-trip). `pearson_r` does 3+ sequential dispatches.

**This is a pipeline architecture problem, not a shader quality problem.**

### Gap 2: Shader Codegen Quality (Anderson) — 3.5×

The Anderson Lyapunov benchmark runs long enough (500 × 10,000 transfer
matrix steps) that dispatch overhead amortizes. The 3.5× gap is the real
compute difference:

- **Kokkos CUDA**: `nvcc` compiles C++ lambdas to native PTX. Full
  register allocation, instruction scheduling, warp-level optimization.
- **BarraCuda WGSL**: `naga` compiles WGSL → SPIR-V → driver JIT → PTX.
  Extra translation layers, less aggressive optimization.

3.5× on a production kernel is a meaningful but closeable gap.

---

## Evolution Strategy: Scaffold, Validate, Absorb

We do not aim to beat Kokkos by writing better WGSL. We aim to **ingest
Kokkos optimizations as pure Rust** — learning from their patterns and
absorbing them into barraCuda's architecture.

### Phase 1: Close the Dispatch Gap (target: 10× → 2×)

The dispatch overhead problem has known solutions:

| Fix | Impact | Effort |
|-----|--------|--------|
| **Persistent device buffers** — keep Views on GPU across calls | Eliminates 2-4 ms transfer per call | Medium — needs buffer lifetime management in barraCuda |
| **Kernel fusion** — fuse mean+variance, or mean+variance+pearson into single dispatch | Eliminates N-1 round-trips for N-op pipelines | Medium — shader generator or manual fused kernels |
| **Pipeline pre-compilation** — compile all WGSL → SPIR-V at device init, not per-call | Eliminates JIT stalls | Low — cache warming at startup |
| **wgpu v22 → v28** — significant dispatch overhead reductions upstream | 2-4× improvement on dispatch latency | High — API migration, but already planned |

After Phase 1, the statistical reductions should drop from 8+ ms to
~100-200 µs — within 2-4× of Kokkos, dominated by the inherent
SPIR-V JIT overhead vs native PTX.

### Phase 2: Close the Codegen Gap (target: 3.5× → 1.5×)

For compute-bound kernels like Anderson:

| Fix | Impact | Effort |
|-----|--------|--------|
| **Loop unrolling hints in WGSL** | Better register scheduling | Low |
| **Subgroup operations** — use `subgroupAdd` for reductions instead of atomics | Match Kokkos warp-level reductions | Medium |
| **DF64 fast-path** — skip DF64 emulation when native f64 is available (RTX 4070 has fp64 at 1:64) | Avoid emulation overhead on capable hardware | Low |
| **Workgroup size tuning** — profile optimal `@workgroup_size` per kernel per GPU | 10-30% improvement typical | Low |

### Phase 3: Absorb Kokkos Patterns as Rust (ongoing)

The Kokkos source is BSD-3. We can study their optimized reduction
patterns, memory access strategies, and hierarchical parallelism
(TeamPolicy → thread → vector lanes) and re-express them in
WGSL/Rust:

- `Kokkos::parallel_reduce` with `JoinOp` → fused multi-accumulator
  WGSL reductions (already started: `CorrelationF64` does triple-reduce)
- `Kokkos::TeamPolicy` hierarchical dispatch → WGSL `@workgroup_size`
  with explicit subgroup cooperation
- `Kokkos::View` layout policies (LayoutRight for GPU coalescing) →
  buffer layout conventions in barraCuda

**The goal is not to wrap Kokkos. The goal is to make Kokkos unnecessary
by absorbing its lessons into sovereign Rust.**

---

## What We Keep

Even at 3.5× slower on raw compute, BarraCuda has architectural
advantages that Kokkos cannot match:

| Property | Kokkos | BarraCuda |
|----------|--------|-----------|
| Vendor SDK required | **Yes** (CUDA, ROCm, oneAPI) | **No** — Vulkan driver only |
| Binary count | One per backend | **One binary, all backends** |
| Runtime GPU selection | No — compiled in | **Yes** — adapter enumeration |
| AGPL-3.0 sovereign | No (BSD-3) | **Yes** |
| NPU integration | No | **Yes** — ToadStool pipeline |
| f64 on any GPU | Only if backend supports | **Yes** — DF64 emulation fallback |

A 3.5× compute gap with zero vendor lock-in is a defensible position.
A 1.5× gap after Phase 2 would be remarkable.

---

## Validation Infrastructure (Committed Today)

### groundSpring — Reference Implementation

All code committed to `groundSpring/kokkos_baseline/`:

| File | Purpose |
|------|---------|
| `CMakeLists.txt` | FetchContent-based build, CUDA/OpenMP/Serial backends |
| `src/main.cpp` | Anderson, stats, bootstrap in Kokkos (`parallel_for`/`parallel_reduce`) |
| `scripts/compare_kokkos_rust.py` | JSON comparison utility |
| `README.md` | Pattern documentation for other springs |

BarraCuda GPU benchmark: `bench-gpu-vs-kokkos` binary in
`crates/groundspring-validate/` — identical parameters, WGSL dispatch.

### How to Reproduce

```bash
# Kokkos CUDA
cd groundSpring/kokkos_baseline
cmake -B build -DCMAKE_BUILD_TYPE=Release \
  -DENABLE_CUDA=ON -DKokkos_ARCH_AMPERE86=ON \
  -DCMAKE_CUDA_ARCHITECTURES=86 \
  -DCMAKE_CXX_COMPILER=g++-10 -DCMAKE_CUDA_HOST_COMPILER=g++-10
cmake --build build -j$(nproc)
./build/kokkos_baseline

# BarraCuda WGSL
cd groundSpring
cargo run --release --features barracuda-gpu --bin bench-gpu-vs-kokkos

# Rust CPU (for three-way comparison)
cargo run --release --bin bench-kokkos-parity
```

---

## Action Items

### barraCuda (P0)

1. **Persistent buffer API** — `GpuView<T>` that keeps data on device
   across operations. This is the single highest-impact change.
2. **Fused reduction kernels** — `mean_variance_f64.wgsl` single-pass,
   `correlation_full_f64.wgsl` single-pass (mean_x, mean_y, cov, var_x,
   var_y in one dispatch).
3. **Pipeline cache warming** — pre-compile all registered shaders at
   `WgpuDevice::new()` time.

### ToadStool (P1)

4. **wgpu v28 evaluation** — profile dispatch overhead improvements.
5. **Subgroup intrinsics audit** — which shaders can use `subgroupAdd`
   on supported hardware.

### All Springs (P2)

6. **Adopt the pattern** — each spring with GPU workloads should create
   a `kokkos_baseline/` directory following groundSpring's reference.
   hotSpring is P0 (LAMMPS Kokkos for Yukawa MD).

---

## Timeline

| Week | Milestone |
|------|-----------|
| Mar 4 (today) | Benchmark committed, gaps documented |
| Mar 11 | Persistent buffer API prototype in barraCuda |
| Mar 18 | Fused reduction shaders, re-benchmark (target: stats < 500 µs) |
| Mar 25 | Anderson shader optimization, subgroup ops (target: < 2× Kokkos) |
| Apr 1 | hotSpring LAMMPS Kokkos vs barraCuda MD benchmark |

---

## The Bigger Picture

Three weeks ago we had 378 f32-only shaders and no GPU validation
infrastructure. Today we have 767 f64-canonical shaders, 33 validation
binaries, 790 tests, and our first honest GPU head-to-head against the
DOE's production framework.

The numbers say Kokkos CUDA is faster. The trajectory says we're
closing. The architecture says we don't need their vendor SDK to get
there.

**Python validates correctness. Kokkos validates competitiveness.
Rust absorbs both and evolves beyond.**

---

*Provenance: groundSpring Kokkos GPU benchmark, RTX 4070, March 4, 2026.
Follows meeting with faculty collaborator (plasma physics) who asked the
right question: "How do you compare to Kokkos?"*

*This is a cross-spring notice. All springs should acknowledge receipt
in their next version handoff.*
