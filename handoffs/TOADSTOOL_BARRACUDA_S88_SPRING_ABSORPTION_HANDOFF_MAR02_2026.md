# ToadStool/BarraCuda S88 Spring Absorption Handoff

**Date**: March 2, 2026
**Session**: S88
**Scope**: Cross-spring API gap resolution, shader evolution, CI hardening

---

## Summary

S88 focused on absorbing feedback from all 5 springs' latest handoffs
(hotSpring V0617, groundSpring V68, neuralSpring V75/S113, wetSpring V92F,
airSpring V063) and resolving the highest-priority API gaps and shader
requests.

## Changes

### P0 — Correctness

1. **`anderson_4d` + `wegner_block_4d` re-exported** from `spectral/mod.rs`
   - Previously required `spectral::anderson::{anderson_4d, wegner_block_4d}`
   - Now available at `barracuda::spectral::{anderson_4d, wegner_block_4d}`
   - groundSpring V68 request

2. **`SeasonalGpuParams::new()` constructor**
   - Private `_pad0` / `_pad1` fields forced springs to use
     `bytemuck::zeroed()` + field-by-field assignment
   - New `SeasonalGpuParams::new(cell_count, day_of_year, ...)` sets padding
     automatically
   - groundSpring V68 request

3. **`BREAKING_CHANGES.md` created**
   - Per-session log of API changes for downstream springs
   - Includes S86–S88 entries

4. **Feature-gate CI discipline**
   - Added `cargo check --workspace --all-targets` (no features) to
     `.github/workflows/ci.yml`
   - Catches modules accidentally gated behind `#[cfg(feature = "gpu")]`
   - wetSpring, groundSpring request

### P1 — API Gaps

5. **`MultiHeadEsn::from_exported_weights(weights, heads)`**
   - Reconstructs a multi-head ESN from previously exported weights
   - Enables CPU-to-GPU migration and cross-device deployment
   - hotSpring V0617 request (blocks 11-head physics ESN migration)

6. **Cross-spring named tolerances** (10 new constants)
   - `HYDRO_ET0`, `HYDRO_SOIL_MOISTURE`, `HYDRO_WATER_BALANCE`,
     `HYDRO_CROP_COEFFICIENT` (airSpring)
   - `PHYSICS_ANDERSON_EIGENVALUE`, `PHYSICS_LATTICE_ACTION`,
     `PHYSICS_LYAPUNOV` (hotSpring, groundSpring)
   - `BIO_DIVERSITY_SHANNON`, `BIO_DIVERSITY_SIMPSON`,
     `BIO_PHYLOGENETIC` (wetSpring)

7. **`NeighborMode` 4D index convention documented**
   - x-fastest (row-major) with t outermost: `idx = t*Nz*Ny*Nx + z*Ny*Nx + y*Nx + x`
   - Direction ordering: +x, -x, +y, -y, +z, -z, +t, -t
   - hotSpring request (z-fastest vs x-fastest confusion)

### P2 — Shader Evolution

8. **`LbfgsGpu` batched optimizer**
   - Solves N independent optimization problems in parallel
   - L-BFGS with numerical gradient (central differences)
   - WGSL shader `lbfgs_two_loop_f64.wgsl` for future full-GPU dispatch
   - CPU-orchestrated with GPU-ready data layout
   - groundSpring V68 request

9. **`tridiag_eigenvectors()` eigenvector solver**
   - Extends existing Sturm bisection (eigenvalues only) with inverse iteration
   - LU factorization of shifted tridiagonal for numerical stability
   - Gram-Schmidt orthogonalization for degenerate eigenvalues
   - Returns column-major n×n eigenvector matrix
   - groundSpring V68 request (transport, spin-chain eigenvectors)

### Verification

10. **SU(3) shader superset confirmed**
    - toadStool: 14 SU(3) WGSL shaders (including HMC force DF64, pseudofermion, Higgs U(1))
    - hotSpring: 9 SU(3) WGSL shaders
    - All hotSpring shaders present in toadStool; no absorption needed

## Test Results

- 2,872 barracuda lib tests pass (0 failures, 13 ignored)
- 6 new tests: tridiag eigenvectors (4), L-BFGS GPU batch (2)
- 0 clippy warnings, 0 fmt diffs

## Reproduction

```bash
cd phase1/toadStool
cargo check -p barracuda --all-features   # clean
cargo test -p barracuda --lib             # 2,872 pass
cargo clippy -p barracuda --all-features -- -D warnings  # 0 warnings
```

## Spring Impact

| Spring | Items Resolved |
|--------|---------------|
| groundSpring V68 | anderson_4d re-export, SeasonalGpuParams::new(), L-BFGS GPU, tridiag eigenvectors, BREAKING_CHANGES.md |
| hotSpring V0617 | MultiHeadEsn::from_exported_weights(), NeighborMode docs, physics tolerances |
| wetSpring V92F | Feature-gate CI, BREAKING_CHANGES.md, bio diversity tolerances |
| airSpring V063 | Feature-gate CI, hydrology tolerances |
| neuralSpring V75 | (flash attention / fused kernels tracked as P3 future) |

## Tracked Future Evolution (P3)

- Flash attention shader (neuralSpring)
- Fused LayerNorm+GELU (neuralSpring)
- Deformed HFB full wiring (hotSpring)
- Abelian Higgs U(1)+Higgs (hotSpring)
- Richards PDE GPU full wiring (airSpring, groundSpring)
- Multi-GPU interconnect (neuralSpring)
- Batched Brent GPU with custom closures (groundSpring)
