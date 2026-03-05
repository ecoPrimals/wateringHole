# hotSpring v0.6.17 — Modern Rewire Validation (March 5, 2026)

**Date**: March 5, 2026
**From**: hotSpring v0.6.17
**To**: barraCuda, toadStool, all Springs
**Type**: Validation + benchmark results after full modernization
**Depends On**: barraCuda v0.3.3 (standalone), toadStool S94b, coralNAK (cloned)

---

## What Was Done

### 1. Ecosystem Sync

- **barraCuda v0.3.3**: Already synced — wgpu 28, naga 28, fused stats,
  DF64 naga rewriter fix (compound assignments + let bindings)
- **toadStool S94b**: Reviewed — NpuDispatch, NpuParameterController,
  GpuAdapterInfo, capability-based discovery. hotSpring clean: no deprecated
  API usage, no toadStool crate import
- **coralNAK**: Cloned and reviewed. Sovereign Rust shader compiler (Phase 2.8).
  Not yet integrated — SPIR-V frontend + f64 lowering still pending
- **wateringHole**: All handoffs reviewed for rewire guidance

### 2. Nautilus Unification

ESN readout merged into NautilusShell as the single reservoir for the MD brain:
- `MdBrain` now uses `NautilusShell` with `output_dim: 12` (MD_NUM_HEADS)
- Adaptive readout retraining (variance-based: 30/100/300 event intervals)
- Board evolution via `evolve_boards()` (renamed from `evolve_nautilus`)
- Serialization: Nautilus JSON only (backward-compatible with older formats)
- `NautilusShell` extended: `population_respond()`, `retrain_readout()`, configurable `output_dim`

### 3. Tolerance Modernization

All bare literals in production MD code replaced with named constants:
- `MD_ENERGY_FLOOR` (1e-30), `MD_TEMPERATURE_FLOOR` (1e-30)
- `MD_TARGET_TEMPERATURE_GUARD` (1e-15), `BRAIN_EQUILIBRIUM_THRESHOLD` (0.05)
- `DIVISION_GUARD` already existed and is used consistently
- `VERLET_SKIN_FRACTION` (0.2), `VERLET_MAX_NEIGHBORS` (1024)

### 4. API Audit Results

| Area | Status |
|------|--------|
| Deprecated toadStool APIs | Clean — no imports from toadStool crate |
| Deprecated barraCuda APIs | Clean — using `from_device()`, `from_existing()` |
| wgpu 28 patterns | Complete — `PollType::Wait`, `entry_point: Some("main")`, etc. |
| DF64 compilation | Delegated to barraCuda `compile_shader_f64` / `compile_shader_df64` |
| Local naga rewrite code | Removed — using barraCuda's sovereign compiler |
| Fused stats ops | Assessed — CPU post-processing too small for GPU benefit |
| Multi-GPU pool | Assessed — future evolution for parallel sweeps |

---

## Validation Results

### Library Tests

```
test result: ok. 669 passed; 0 failed; 6 ignored
```

### Full 9-Case PP Yukawa DSF Sweep (RTX 3090, N=2000, DF64)

All 9 cases pass with 0.001% energy drift (threshold: 5%).

| Case | κ | Γ | Algorithm | Steps/s | Drift | Wall Time |
|------|---|---|-----------|---------|:---:|-----------|
| k1_G14 | 1 | 14 | AllPairs | 292 | 0.001% | 2.0 min |
| k1_G72 | 1 | 72 | AllPairs | 307 | 0.001% | 1.9 min |
| k1_G217 | 1 | 217 | AllPairs | 329 | 0.001% | 1.8 min |
| k2_G31 | 2 | 31 | Verlet | 306 | 0.001% | 1.9 min |
| k2_G158 | 2 | 158 | Verlet | 303 | 0.001% | 1.9 min |
| k2_G476 | 2 | 476 | Verlet | 303 | 0.001% | 1.9 min |
| k3_G100 | 3 | 100 | Verlet | 314 | 0.001% | 1.9 min |
| k3_G503 | 3 | 503 | Verlet | 313 | 0.001% | 1.9 min |
| k3_G1510 | 3 | 1510 | Verlet | 317 | 0.001% | 1.8 min |

Brain active in all cases (Nautilus: 12 readout retrains, 30 board generations).
Brain adds ~3× overhead vs raw physics (~992 steps/s without brain at κ=3).

### GPU Power Profile

| κ | W (avg) | W (peak) | Temp °C | VRAM MB |
|---|---------|----------|---------|---------|
| 1 | 155 W | 159 W | 62-63 | 578-589 |
| 2 | 95-99 W | 159 W | 62-64 | 586-621 |
| 3 | 95 W | 159 W | 64 | 544-556 |

---

## Kokkos Gap Status

| Milestone | Steps/s (κ=3) | Gap vs Kokkos-CUDA |
|-----------|:---:|:---:|
| Before DF64 (Feb) | 27 (native f64, 1:64) | **137×** |
| After DF64 | 293 (FP32 core streaming) | 12.6× |
| After Verlet | 992 (compact neighbor loop) | **3.7×** |
| With brain | 317 (Nautilus learning) | 11.7× (with intelligence) |

Gap closed from **137× to 3.7×** (97% for raw physics).

### Remaining 3.7× Gap Analysis

1. **Dispatch overhead** (~1.5×): Kokkos persistent kernels vs our per-interval encoders
2. **Workgroup tuning** (~1.2×): Auto-tuned vs fixed 256
3. **Codegen quality** (~1.5×): nvcc native PTX vs naga WGSL→SPIR-V→PTX
4. **Fused VV** (~1.3×): Kick+drift+force in one dispatch vs 4 separate submits

### Why 3.7× Is Actually Good

| Property | Kokkos-CUDA | barraCuda |
|----------|-------------|-----------|
| Vendor lock-in | CUDA SDK required | None — any Vulkan GPU |
| Driver | Proprietary nvidia.ko | NVK (open source) |
| Intelligence | None | Nautilus brain (12 heads) |
| Cross-platform | Recompile per backend | Same binary everywhere |
| Precision tiers | Hardware-locked | DF64/f64/f32/f16 runtime |

---

## What barraCuda Should Absorb

### Priority 1: Verlet Pipeline

- `VerletListGpu` (wraps `CellListGpu` + flat neighbor buffer)
- `ForceAlgorithm` enum + `AlgorithmSelector`
- 6 WGSL shaders (build, check displacement, copy ref, force f64/df64)
- Bug fix: use `CellListGpu::new(device, n, box_l, rc)` NOT `rc + skin`

### Priority 2: Fused VV Kernel

- Kick + drift + force + half-kick in one dispatch
- Reduces submissions from 4→1 per step (~3× fewer GPU submissions)
- Biggest single-item impact on Kokkos gap closure

### Priority 3: Workgroup Auto-Tuning

- Profile optimal `@workgroup_size` per kernel per GPU
- 10-30% improvement typical

---

## What hotSpring Should Wire Next

| Priority | Feature | Source |
|----------|---------|--------|
| P1 | Run brain-sweep with Nautilus persistence | Validate cross-run learning |
| P2 | NpuParameterController from toadStool S94b | Upstream NPU abstraction |
| P2 | N-scaling benchmark (500→8000) | Measure scaling with modern stack |
| P3 | Chuna paper reproductions (43-45) | Gradient flow, dielectric, kinetic-fluid |
| P3 | coralNAK integration | When SPIR-V frontend is ready |
