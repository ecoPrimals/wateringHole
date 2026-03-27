# neuralSpring → ToadStool V12 Handoff

**Date**: February 22, 2026 (Session 43)
**ToadStool HEAD**: `5437c170`
**Source**: `neuralSpring/wateringHole/handoffs/NEURALSPRING_V12_SESSION43_HANDOFF_FEB22_2026.md`

---

## What's New for ToadStool

### 4 New WGSL Shaders Ready for Absorption

1. **`logsumexp_reduce.wgsl`** — Batched numerically-stable logsumexp (f32, workgroup 256).
   Extends `barracuda::shaders::math::logsumexp.wgsl` to parallel batched reduction.
   Target: `barracuda::ops::reduce`

2. **`stencil_cooperation.wgsl`** — Fermi imitation dynamics on 2D grid (workgroup 256).
   Complements `spatial_payoff.wgsl` for game theory. Target: `barracuda::ops::stencil`

3. **`rk45_adaptive.wgsl`** — Dormand-Prince RK45 single step with Hill function RHS (workgroup 64).
   Extends `barracuda::shaders::math::rk45_f64.wgsl` with injectable kinetics.
   Target: `barracuda::ops::ode`

4. **`wright_fisher_step.wgsl`** — Wright-Fisher drift + selection with inline xoshiro128** (workgroup 256).
   Binomial sampling for stochastic population genetics. Target: `barracuda::ops::popgen`

### Upstream Wrappers Successfully Validated

| API | Checks | Notes |
|-----|--------|-------|
| `GillespieGpu` | 20/20 | f64 conservation exact |
| `TaxonomyFcGpu` | 3/3 | f64 log-posterior bit-exact |
| `KmerHistogramGpu` | 3/3 | u32 histogram exact |
| `UniFracPropagateGpu` | 2/2 | f64 leaf init exact |
| `chi_squared::*` | 13/13 | PDF/CDF/moments within 1e-4 of SciPy |

### Mixed-Hardware Dispatch (local evolution for absorption)

neuralSpring built `mixed.rs` + `pcie_bridge.rs` in metalForge/forge:
- `MixedSubstrate` enum for GPU↔NPU↔CPU routing
- `TransferCost` model for PCIe 4.0 bandwidth estimation
- `PcieBridge` for device-pair buffer transfer abstraction
- Absorption target: `barracuda::unified_hardware`

### Cross-Spring Contributions

- **wetSpring parity**: TaxonomyFcGpu, KmerHistogramGpu, UniFracPropagateGpu all validated from neuralSpring
- **hotSpring lineage**: RK45 adaptive builds on hotSpring's precision infrastructure (TS-001, TS-003)
- **All Springs**: Mixed-hardware dispatch benefits all Springs (GPU→NPU→CPU routing)

---

*neuralSpring V12 (Session 43) → ToadStool. 4 shaders + mixed-hardware infra for absorption.*
