# hotSpring v0.6.24 — barraCuda Lean-Out & Rewire Handoff

**Date:** March 10, 2026
**From:** hotSpring v0.6.24 (807 lib tests, 0 failures, 0 clippy warnings)
**To:** barraCuda (v0.3.3, `5c16458`) / toadStool (S138) / coralReef (Phase 10)
**License:** AGPL-3.0-only

## Executive Summary

Rewire of hotSpring to barraCuda HEAD (`27011af` → `5c16458`, 2 commits).
Leaned out all duplicate code that barraCuda absorbed from hotSpring in its
plasma-absorption and Complex64-evolution work. hotSpring now delegates
complex arithmetic and plasma dispersion to barraCuda as the single source
of truth, retaining only hotSpring-specific physics (PlasmaParams,
chi0_classical, epsilon_vlasov, f32-stability tests, WGSL shader constant).

**Math is universal. barraCuda owns it. hotSpring consumes it.**

## Changes

### 1. Dependency Pin Update

```
- barracuda = { git = "...", rev = "27011af" }
+ barracuda = { git = "...", rev = "5c16458" }
```

Picks up:
- `f03b854` — plasma dispersion Z/W absorption + healthSpring PK/PD ops
- `5c16458` — CoralReefDevice full GpuBackend impl + sovereign-dispatch feature

### 2. Complex Type Consolidation

**dielectric/complex.rs** (100 → 8 lines): Replaced local `Complex` struct
with `pub use barracuda::ops::lattice::cpu_complex::Complex64 as Complex`.
All downstream code (`plasma_dispersion.rs`, `response.rs`,
`dielectric_multicomponent.rs`) unchanged — the `Complex` name is preserved.

**lattice/complex_f64.rs** (347 → 100 lines): Replaced local `Complex64`
struct and all trait impls with re-export from barraCuda. Retained:
- `from_polar(theta)` as a free function (used by `abelian_higgs.rs`)
- `WGSL_COMPLEX64` shader constant (used by `lattice/su3.rs`)
- Core behavioral tests (now exercising upstream implementation)

### 3. Plasma Dispersion Lean-Out

**plasma_dispersion.rs** (415 → 334 lines): Replaced `plasma_dispersion_z`,
`plasma_dispersion_w`, `plasma_dispersion_w_stable` function bodies with
`pub use barracuda::special::{...}` re-exports. Retained:
- `PlasmaParams` struct and `from_coupling()` constructor
- `chi0_classical` and `epsilon_vlasov` (hotSpring-specific physics)
- All correctness tests (now exercising upstream implementations)
- f32-stability test module (hotSpring-specific, validates GPU precision)

### 4. Clippy Clean-Up (consequential)

The type swap enabled `AddAssign` on `Complex`, resolving pre-existing
`assign_op_pattern` warnings in `dielectric_multicomponent.rs` (2 sites).
Also removed redundant `#[must_use]` on 6 functions returning `Complex`
(now `#[must_use]` via the upstream type).

### 5. Stale Reference Fix

Fixed `validate_pppm.rs` error message: `PppmGpu::new` → `PppmGpu::from_device`.

## Line Count Delta

| File | Before | After | Δ |
|------|--------|-------|---|
| `dielectric/complex.rs` | 101 | 8 | −93 |
| `lattice/complex_f64.rs` | 347 | 100 | −247 |
| `dielectric/plasma_dispersion.rs` | 415 | 334 | −81 |
| **Total** | **863** | **442** | **−421** |

## Validation

- `cargo check --all-targets` — clean
- `cargo test --lib` — 807 passed, 0 failed, 6 ignored
- `cargo clippy --all-targets` — 0 warnings
- `RUSTDOCFLAGS="-D warnings" cargo doc --no-deps` — 0 warnings
- `cargo fmt --check` — clean

## 3-Primal Pipeline Status

```
toadStool (S138)          barraCuda (v0.3.3)         hotSpring (v0.6.24)
─────────────────         ──────────────────         ───────────────────
hardware discovery   →    math + shaders + GPU  →    physics validation
capability routing        3-tier precision            Mermin dielectric
SubstrateCapability       Complex64 (canonical)       DSF / f-sum
PrecisionRouting          plasma_dispersion Z/W       lattice QCD / HMC
shader.compile IPC        4 plasma WGSL shaders       HFB nuclear
                          GpuBackend trait             MD simulations
                          CoralReefDevice              sovereign dispatch
```

## What hotSpring Still Owns (NOT absorbed)

- `PlasmaParams`, `chi0_classical`, `epsilon_vlasov`
- Mermin / completed-Mermin dielectric (`response.rs`)
- Multicomponent Mermin (`dielectric_multicomponent.rs`)
- DSF, f-sum rule, DC conductivity validation
- f32-stability test suite for W(z)
- `from_polar(theta)` free function
- `WGSL_COMPLEX64` shader constant
- All lattice QCD, HMC, RHMC, gradient flow, pseudofermion modules
- HFB nuclear physics, MD simulations, reservoir computing

## Future Work (not addressed)

- **WGSL shader deduplication**: hotSpring embeds dielectric/BGK/Euler shaders
  that barraCuda now also has. Should be resolved when promoting to GPU pipeline.
- **`from_polar` upstream PR**: Consider upstreaming to barraCuda's `Complex64`.
- **coralReef sovereign compile f64 validation**: Tracked in coralReef iteration.
