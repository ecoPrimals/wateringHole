# barraCuda v0.3.3 — Cross-Spring Rewiring Handoff

**Date**: March 7, 2026
**From**: barraCuda
**To**: toadStool, coralReef, hotSpring, wetSpring, neuralSpring, airSpring, groundSpring

---

## Summary

barraCuda now has a complete cross-spring evolution tracking system with
`PrecisionRoutingAdvice` from toadStool S128, `BatchedOdeRK45F64` from
wetSpring V95, GPU-resident fused stats, and a 27-shader provenance
registry with evolution dates and dependency matrix.

---

## What Changed

### Cross-Spring Evolution Tracking (`shaders::provenance`)

- **27 shader records** with `created` and `absorbed` dates
- **10 evolution timeline events** documenting cross-spring flows:
  - hotSpring DF64 (S58) → all springs (consumer GPU f64-class work)
  - neuralSpring stats (S69) → hotSpring/groundSpring/airSpring
  - wetSpring bio (V87-V90) → neuralSpring HMM/Gillespie adoption
  - groundSpring universals (V74-V80) → tolerance backbone for all
  - neuralSpring (S100) → hotSpring nuclear χ² fits
  - airSpring (V043-V068) → wetSpring environmental monitoring
  - groundSpring (V74-V80) → Anderson Lyapunov, Welford universals
  - neuralSpring (V128) → hotSpring batch_ipr spectral diagnostics
  - hotSpring (V0619) → wetSpring stress_virial, verlet_neighbor
- **`evolution_report()`** generates dependency matrix + timeline
- **6 new records**: `stress_virial`, `verlet_neighbor`, `batch_ipr`,
  `hmm_forward`, `hfb_gradient`, `welford_mean_variance`

### toadStool S128 Integration (`device::driver_profile`)

- **`PrecisionRoutingAdvice`** enum:
  - `F64Native` — native f64 everywhere
  - `F64NativeNoSharedMem` — native f64 but shared-memory reductions fail
  - `Df64Only` — use DF64 for all f64-class work
  - `F32Only` — no f64 support
- **`GpuDriverProfile::precision_routing()`** — three-axis f64 routing
  integrating the shared-memory reliability discovery from toadStool S128

### Fused GPU-Resident Stats (`ops::variance_f64_wgsl`)

- **`mean_variance_to_buffer()`** — fused Welford output stays as
  `wgpu::Buffer` for zero-readback chained pipelines

### BatchedOdeRK45F64 (`ops::rk45_adaptive`)

- **`BatchedOdeRK45F64`** — full-trajectory adaptive Dormand-Prince
  integrator on GPU with host-side step-size control
- **`BatchedRk45Config`** — `atol`, `rtol`, `max_steps`, `t_final`
- 18.5× fewer steps than RK4 for stiff bio regulatory networks

### API Debt Elimination (previous session)

- All 9 `too_many_arguments` evolved to builder/struct patterns
- Deprecated PPPM constructors removed
- Akida SDK paths → capability constant
- 19 CPU reference functions audited

---

## Cross-Spring Dependency Matrix (from provenance registry)

| From \ To | hotSpring | wetSpring | neuralSpring | airSpring | groundSpring |
|-----------|-----------|-----------|--------------|-----------|--------------|
| **hotSpring** | — | 6 | 4 | · | 3 |
| **wetSpring** | 1 | — | 3 | 1 | · |
| **neuralSpring** | 3 | 2 | — | 1 | 2 |
| **airSpring** | · | 4 | 1 | — | · |
| **groundSpring** | 2 | 2 | 2 | 1 | — |

---

## What Each Spring Can Use

### For toadStool
- `PrecisionRoutingAdvice` is now in barraCuda — use `precision_routing()`
  instead of separate `has_reliable_f64()` + `fp64_strategy()` checks
- barraCuda showcase paths in toadStool are stale (point to fossilized
  `crates/barracuda/`); low priority but worth fixing

### For coralReef
- 14/27 cross-spring shaders compiling to SM70 SASS as of Phase 10 Iteration 5
- `compile_wgsl_direct()`, `capabilities()`, and AMD arch support are wired in barraCuda's
  `coral_compiler/` module — ready for end-to-end validation when coralDriver lands

### For hotSpring
- `BatchedOdeRK45F64` can replace per-step GPU dispatch in transport calculations
- `stress_virial` and `verlet_neighbor` tracked in provenance as hotSpring→wetSpring
- `batch_ipr` tracked as neuralSpring→hotSpring contribution

### For wetSpring
- `BatchedOdeRK45F64` implements the P1 request from V95
- `mean_variance_to_buffer()` enables zero-readback chained bio pipelines
- `hmm_forward` tracked in provenance as wetSpring→neuralSpring

### For neuralSpring
- `PrecisionRoutingAdvice::F64NativeNoSharedMem` important for attention kernels
  with workgroup accumulators

### For groundSpring
- `welford_mean_variance` tracked as consumed by all 5 springs
- `chi_squared_f64` tracked as universal statistical test for all springs

---

## Quality

- 3,105 tests (3,089 lib + 15 integration + 1 core)
- Zero clippy warnings, zero unsafe, zero TODOs
- All quality gates green (fmt, clippy -D warnings, doc, deny)

---

## Remaining

| Priority | Item | Status |
|----------|------|--------|
| P1 | DF64 NVK hardware verification | Pending |
| P2 | GpuView zero-copy expansion | Pending |
| P2 | RHMC multi-shift CG solver | Pending |
| P2 | Adaptive HMC dt | Pending |
| P2 | Anderson Lyapunov shaders | Pending |
| P3 | ComputeBackend trait | Pending |
| P3 | ComputeDispatch tarpc | Pending |
| P3 | BandwidthTier in device profile | Pending |
