# barraCuda v0.3.3 — healthSpring / hotSpring Absorption Handoff

**From**: barraCuda
**Date**: 2026-03-09
**Session**: Cross-spring absorption — Hill dose-response (Emax), Population PK Monte Carlo, plasma dispersion W(z)/Z(z), neuralSpring head_split/head_concat alignment

---

## Summary

6 files changed, 2 new files created (+650 / −30 lines). Absorbed healthSpring pharmacology ops and hotSpring plasma dispersion CPU functions into barraCuda. Confirmed neuralSpring MHA reshaping alignment.

---

## Changes for All Springs

### Hill Dose-Response (Emax) — healthSpring Absorption
- `HillFunctionF64` evolved from normalized Hill `[0,1]` to full dose-response:
  `E(x) = Emax × xⁿ / (Kⁿ + xⁿ)`
- New `dose_response(device, k, n, emax)` constructor
- Backward compatible: `new()` defaults to `emax = 1.0`
- Shader `hill_f64.wgsl` updated with `emax` uniform parameter
- healthSpring's `power_f64` f32-path trick NOT absorbed — barraCuda uses `compile_shader_f64()` for proper f64 precision

### Population PK Monte Carlo — healthSpring Absorption
- New `PopulationPkF64` op + `population_pk_f64.wgsl` shader
- GPU-vectorized virtual patient simulation: each thread = one patient
- Wang hash + xorshift32 PRNG (u32-only, no SHADER_INT64 needed)
- Evolved from healthSpring hardcoded values to fully parameterized:
  - `dose_mg`, `f_bioavail`, `base_cl`, `cl_low`, `cl_high` (all configurable)
  - healthSpring hardcoded `CL = 10.0 * (0.5 + u)` → `CL = base_cl * (cl_low + u * (cl_high - cl_low))`

### Plasma Dispersion W(z) and Z(z) — hotSpring Absorption (ISSUE-006)
- New `special::plasma_dispersion` module — CPU-side reference implementations
- `plasma_dispersion_z(z)`: power series for |z| < 6, asymptotic for |z| ≥ 6
- `plasma_dispersion_w(z)`: auto-selects stable branch for |z| ≥ 4
- `plasma_dispersion_w_stable(z)`: direct asymptotic expansion avoids catastrophic cancellation
- All constants extracted: `SQRT_PI`, `SMALL_Z_THRESHOLD`, `W_BRANCH_THRESHOLD`, etc.

### Complex64 Evolution
- `inv()` method added for multiplicative inverse
- `Mul<f64>` and `Mul<Complex64> for f64` trait impls added
- `cpu_complex` module promoted from `#[cfg(test)]` to runtime (needed by `plasma_dispersion`)

### neuralSpring head_split / head_concat Alignment
- Confirmed equivalent index math between barraCuda (f64, entry `main`) and neuralSpring (f32, named entries `head_split`/`head_concat`)
- Both compute `[B, S, D] ↔ [B, H, S, D/H]` with identical memory layout
- No changes needed — already aligned

---

## Quality Gates

All pass (re-verified after all changes):

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy --all-targets --all-features -D warnings` | Pass (zero warnings) |
| `cargo doc --no-deps --all-features` | Pass |
| `cargo test -- hill_f64` | 6/6 pass (3 new dose-response tests) |
| `cargo test -- population_pk_f64` | 6/6 pass (all new) |
| `cargo test -- plasma_dispersion` | 8/8 pass (all new) |
| `cargo test -- cpu_complex` | 4/4 pass (2 new: inv, scalar_mul) |

---

## For healthSpring

- `HillFunctionF64::dose_response(device, ec50, hill_n, emax)` is the canonical GPU Hill path
- `PopulationPkF64::new(device, config)` with `PopulationPkConfig` replaces local GPU dispatch
- Both use `compile_shader_f64()` for proper f64 precision (no f32 exp/log workaround)
- healthSpring can drop local `hill_dose_response_f64.wgsl` and `population_pk_f64.wgsl` shaders

## For hotSpring

- `barracuda::special::plasma_dispersion_w(z)` is the canonical CPU W(z) implementation
- GPU path remains in `shaders/science/plasma/dielectric_mermin_f64.wgsl` (unchanged)
- hotSpring can import `barracuda::special::plasma_dispersion_z` instead of local `dielectric::plasma_dispersion_z`

## For neuralSpring

- Head split/concat WGSL confirmed aligned. No changes needed.
- If neuralSpring needs f64 head reshaping, barraCuda's shaders are ready.

## For wetSpring / airSpring / groundSpring

- `HillFunctionF64::new()` unchanged — existing callers unaffected.
- New `dose_response()` constructor available for dose-response curves.

---

## New Test Count

- Hill F64: 3 → 6 tests (+3 dose-response)
- Population PK F64: 0 → 6 tests (new op)
- Plasma dispersion: 0 → 8 tests (new module)
- Complex64: 2 → 4 tests (+2 new ops)
- **Net new tests: +17**
