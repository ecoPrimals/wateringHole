# hotSpring → barraCuda/toadStool: Verlet Neighbor List Handoff

**Date**: March 5, 2026
**From**: hotSpring (validated on RTX 3090, 9/9 PP Yukawa DSF cases)
**To**: barraCuda (algorithm absorption), toadStool (dispatch optimization)
**Type**: Evolution handoff — algorithmic tier upgrade + runtime adaptation

---

## Summary

hotSpring has implemented and validated a complete Verlet neighbor list pipeline
with adaptive rebuild and runtime algorithm selection. This closes the barraCuda
vs Kokkos-CUDA gap from **27× to 3.7×** (93% closed).

**Key result**: κ=3 cases achieve **992 steps/s** (vs Kokkos-CUDA 3,699 steps/s).

---

## What Was Built (hotSpring-local, ready for absorption)

### 1. `md/neighbor.rs` — Algorithm Selection + VerletListGpu

```rust
pub enum ForceAlgorithm {
    AllPairs,                         // O(N²), N < 500 or cells/dim < 3
    CellList,                         // O(N), medium N (unused in current config)
    VerletList { skin: f64 },         // O(N) compact, N ≥ 500 + cells/dim ≥ 3
}
```

`AlgorithmSelector::from_config(config).select()` auto-selects based on:
- Particle count (`VERLET_MIN_PARTICLES = 500`)
- Cell geometry (`CELLLIST_MIN_CELLS_PER_DIM = 3`)
- Skin fraction (`VERLET_SKIN_FRACTION = 0.2 × rc`)

`VerletListGpu` wraps `CellListGpu` + flat `[N × max_neighbors]` u32 buffer:
- Uses `CellListGpu` with cutoff = `rc` (NOT `rc + skin`) to avoid PBC stencil double-counting
- Build shader searches within `(rc + skin)²` for neighbor inclusion
- Adaptive rebuild: `verlet_check_displacement.wgsl` computes atomic max displacement
- Rebuild triggers when max displacement > skin/2 (typically every 10-50 steps at equilibrium)

### 2. WGSL Shaders (6 new files)

| Shader | Purpose | Bindings |
|--------|---------|----------|
| `verlet_build.wgsl` | Build neighbor list from 27-cell stencil | 7: pos, nb_list, nb_count, params, cell_start, cell_count, sorted_indices |
| `verlet_check_displacement.wgsl` | Atomic max displacement check | 4: pos, ref_pos, max_disp (atomic u32), params |
| `verlet_copy_ref.wgsl` | Save reference positions | 3: pos, ref_pos, params |
| `yukawa_force_verlet_f64.wgsl` | Compact neighbor loop (f64) | 6: pos, forces, pe, params, nb_list, nb_count |
| `yukawa_force_verlet_df64.wgsl` | Compact neighbor loop (DF64) | 6: same |

Force shader params layout:
```
[0] n, [1] kappa, [2] prefactor, [3] cutoff_sq (rc², NOT (rc+skin)²),
[4] box_x, [5] box_y, [6] box_z, [7] max_neighbors
```

Build shader params include cell grid info at indices [8]-[14] (same as cell-list force).

### 3. Simulation Pipeline (`run_simulation_verlet`)

Full velocity-Verlet loop with:
- `Fp64Strategy` branching (Native f64 vs DF64 per GPU)
- Adaptive Verlet rebuild in both equilibration and production
- Streamed dispatch (batched encoder per dump interval)
- ReduceScalarPipeline for KE/PE reduction

### 4. Constants (tolerances/md.rs)

| Constant | Value | Purpose |
|----------|-------|---------|
| `VERLET_SKIN_FRACTION` | 0.2 | Skin = 0.2 × rc (standard MD default) |
| `VERLET_MAX_NEIGHBORS` | 1024 | Flat buffer dimension per particle |
| `VERLET_MIN_PARTICLES` | 500 | Below this, all-pairs wins |

---

## Benchmark Results (RTX 3090, DF64, N=2000)

| Case | Algorithm | Steps/s | Energy Drift | Gap vs Kokkos |
|------|-----------|---------|:---:|:---:|
| k1_G14 | AllPairs | 181 | 0.001% | 4.0× |
| k2_G31 | **Verlet** | **368** | 0.000% | 3.0× |
| k2_G158 | **Verlet** | **846** | 0.000% | 3.6× |
| k3_G100 | **Verlet** | **977** | 0.000% | 3.2× |
| k3_G1510 | **Verlet** | **992** | 0.001% | 3.7× |

**κ=1 remains all-pairs** because cells_per_dim = floor(20.3/8) = 2 < 3.
To get Verlet for κ=1, either increase N (larger box) or reduce rc.

---

## Bug Found and Fixed

**CellListGpu cutoff for Verlet**: Initial implementation used `rc + skin` as the
CellListGpu cutoff, producing 2×2×2 cells for κ=2 (cells_per_dim=2). The 27-cell
stencil with 2 cells/dim wraps around and visits the same cells multiple times,
double-counting neighbors → 60% energy drift.

**Fix**: Build CellListGpu with `rc` as cutoff (not `rc + skin`). The build shader
then searches within `(rc + skin)²` for neighbor inclusion. Since `skin < cell_size`
for valid configs, all neighbors are found within the 27-cell stencil.

**barraCuda should note**: Any upstream Verlet implementation should use
`CellListGpu::new(device, n, box_l, rc)` not `CellListGpu::new(device, n, box_l, rc + skin)`.

---

## Absorption Recommendations for barraCuda

### Priority 1: Upstream Verlet to `barracuda::ops::md::neighbor`

The Verlet list is a natural extension of the existing `CellListGpu`:
- `VerletListGpu` wraps `CellListGpu` + flat neighbor buffer
- Build shader reuses the same cell_start/cell_count/sorted_indices bindings
- Force shaders are drop-in replacements (same physics, different iteration)

### Priority 2: Runtime Algorithm Selection

`ForceAlgorithm` enum + `AlgorithmSelector` should live in barraCuda so all springs
can use it. The current hotSpring implementation is self-contained in `md/neighbor.rs`.

### Priority 3: Dispatch Optimization (toadStool)

The remaining 3.7× gap vs Kokkos is dominated by dispatch overhead:
- Kokkos uses persistent kernel launches with minimal CPU-GPU sync
- Our streamed dispatch creates new encoders per dump interval
- Fused VV kernels (kick+drift+force+kick in one dispatch) could reduce submissions by 3×

### Priority 4: Adaptive Skin Tuning

Current skin = 0.2 × rc is the standard MD default. For hot systems (low Γ, e.g. k2_G31),
particles move fast and rebuild frequently (every ~10 steps). A larger skin trades
more neighbors per force eval for fewer rebuilds. The optimal skin depends on:
- Temperature (particle speed)
- Density (neighbor count)
- GPU VRAM (buffer size for max_neighbors)

This could be auto-tuned at runtime by measuring rebuild frequency and adjusting.

---

## Cross-Spring Learnings

1. **wetSpring** uses `compile_shader_universal(source, Precision::F64)` — hotSpring
   should adopt this instead of the current `create_pipeline_f64` / `create_pipeline_df64` split.

2. **wetSpring** demonstrates `optimal_precision()` → `Fp64Strategy` mapping that
   could be used for the Verlet build shader (which only needs f64 for PBC, not DF64).

3. **Named tolerances** — wetSpring's `tolerances.rs` with provenance comments is the
   model that hotSpring's `tolerances/md.rs` now follows (VERLET_SKIN_FRACTION etc.).

4. **Anderson QS bridge** — wetSpring validates hotSpring's spectral primitives in
   biological settings, confirming the cross-spring evolution thesis.

---

## Files Changed in hotSpring

| File | Change |
|------|--------|
| `md/neighbor.rs` (new) | ForceAlgorithm, AlgorithmSelector, VerletListGpu |
| `md/shaders/verlet_build.wgsl` (new) | Build from cell-list |
| `md/shaders/verlet_check_displacement.wgsl` (new) | Adaptive rebuild check |
| `md/shaders/verlet_copy_ref.wgsl` (new) | Reference position save |
| `md/shaders/yukawa_force_verlet_f64.wgsl` (new) | Verlet force (f64) |
| `md/shaders/yukawa_force_verlet_df64.wgsl` (new) | Verlet force (DF64) |
| `md/shaders.rs` | Shader constants |
| `md/simulation.rs` | `run_simulation_verlet()` |
| `md/mod.rs` | Export neighbor module |
| `bin/sarkas_gpu.rs` | AlgorithmSelector dispatch |
| `bin/bench_cpu_gpu_scaling.rs` | AlgorithmSelector dispatch |
| `tolerances/md.rs` | VERLET_SKIN_FRACTION, VERLET_MAX_NEIGHBORS, VERLET_MIN_PARTICLES |
| `tolerances/mod.rs` | Re-exports |
