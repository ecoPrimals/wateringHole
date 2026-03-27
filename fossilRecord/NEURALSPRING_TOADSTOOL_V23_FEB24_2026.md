# neuralSpring → ToadStool V23 — Session 58 Ecosystem Summary

**Date**: February 24, 2026
**From**: neuralSpring (ecoPrimals/neuralSpring)
**To**: ToadStool/BarraCUDA team (ecoPrimals/phase1/toadstool)
**ToadStool HEAD**: `9404fdb4`

---

## Session 58: Upstream Dispatch Rewiring + GpuDriverProfile

neuralSpring has rewired 7 core `Dispatcher` methods to delegate to upstream
`barracuda::dispatch::domain_ops` and wired in `GpuDriverProfile` for
hardware-adaptive f64 strategy detection.

### What Changed

- **7 methods rewired**: `mat_mul`, `frobenius_norm`, `transpose`, `softmax`,
  `l2_distance`, `mean`, `variance` → all delegate to upstream `domain_ops`
- **GpuDriverProfile wired in**: `Dispatcher` now exposes `driver_profile()`,
  `fp64_strategy()`, `needs_pow_workaround()` from `barracuda::device::driver_profile`
- **New validator**: `validate_cross_spring_evolution` (10/10 PASS)
- **Total rewired**: 11 functions (cumulative S56–S58)

### Cross-Spring Evolution Proven

This session validates that the cross-spring evolution cycle works at scale:

| Spring | Contributed | neuralSpring Now Uses |
|--------|------------|----------------------|
| hotSpring | GpuDriverProfile, Fp64Strategy, df64_core, pow_f64 | driver_profile(), fp64_strategy(), needs_pow_workaround() |
| wetSpring | HMM, Anderson, ODE bio, NMF, Ridge | Anderson localization, HMM phylogenetics |
| neuralSpring | ValidationHarness, batch_fitness, eigh, pairwise ops | Upstream absorbed; rewired to domain_ops |

### Benchmark Observations

- GPU matmul on RTX 4070: first-call includes shader compilation (~270ms),
  subsequent calls show size-based dispatch: small inputs stay on CPU,
  large inputs route to GPU
- FP64 strategy correctly detected as `Hybrid` (1:64 throttled Ada consumer GPU)
- pow(f64,f64) workaround correctly flagged — polyfill in effect

### Quality

- 478 lib tests PASS, 30 forge tests PASS
- 145/146 validate_all (1 pre-existing logsumexp driver issue)
- 0 clippy warnings (pedantic+nursery), 0 fmt issues

---

*neuralSpring V23 ecosystem handoff — 11 functions rewired to upstream BarraCUDA, GpuDriverProfile hardware-awareness operational.*
