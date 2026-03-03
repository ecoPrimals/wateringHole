# D-DF64 Transfer: toadStool → barraCuda

**Date**: March 3, 2026 — Session 93
**From**: toadStool team
**To**: barraCuda team
**Classification**: Architecture demarcation — precision ownership

---

## Summary

The D-DF64 debt item ("DF64 as default precision path") is transferred from
toadStool's backlog to barraCuda's. This aligns with the architecture
demarcation established in S89:

- **barraCuda** — "WHAT to compute" (math, shaders, precision strategy)
- **toadStool** — "WHERE and HOW" (hardware discovery, orchestration, dispatch)

---

## What barraCuda owns

1. **Precision strategy selection** — `Fp64Strategy::Native` vs `Hybrid` vs
   `Concurrent` decision logic. Currently in `GpuDriverProfile::fp64_strategy()`
   and `fp64_strategy_probed()`.

2. **`df64_rewrite` as default path** — making the naga-guided compiler pass
   the default for consumer GPUs (1:64 FP64:FP32), rather than requiring
   per-op manual DF64 shader variants.

3. **Cross-precision validation** — f64 vs df64 vs f32 correctness testing.
   barraCuda should validate that `df64_rewrite` produces bit-compatible
   results against native f64 reference implementations.

4. **Per-op DF64 shader variants** — the 25 hand-written DF64 WGSL files
   and the decision of when automatic rewriting suffices vs hand-tuning.

---

## What toadStool serves (hardware capabilities)

toadStool's device discovery and capability probing provides the raw hardware
data that barraCuda's precision strategy consumes:

| Capability | Source | Used by barraCuda |
|-----------|--------|-------------------|
| FP64:FP32 core ratio | `GpuDriverProfile::fp64_rate` | `fp64_strategy()` — Full (1:2) → Native, Minimal (1:64) → Hybrid |
| L2 cache size | `wgpu::Limits` / device probing | Cache-aware tile sizing for DF64 GEMM |
| Infinity Cache (AMD) | Device-specific probing | AMD RDNA2/3 has 128MB; affects DF64 working set |
| Memory bandwidth | `device.limits()` queries | DF64 is compute-bound, not memory-bound — ratio matters |
| `SHADER_F64` feature | `wgpu::Features` | Whether f64 compiles at all |
| `can_compile_f64()` probe | Runtime compile test | NAK/NVVM advertise f64 but fail — probe provides ground truth |
| sin/cos f64 workarounds | `needs_sin_f64_workaround_probed()` | Taylor preamble injection for NVK |

toadStool will continue to evolve and enrich this capability surface. If
barraCuda needs additional hardware data (e.g., per-SM register file size,
shared memory limits, warp/wave size), toadStool should expose it via the
existing `GpuDriverProfile` or device capability APIs.

---

## Current state of DF64 infrastructure

Already implemented and working:

- `df64_core.wgsl` — FMA-optimized core arithmetic (add, mul, div, scale)
- `df64_transcendentals.wgsl` — 15 functions (exp, log, sin, cos, tan, sqrt,
  pow, asin, acos, atan, atan2, sinh, cosh, gamma, erf)
- 25 hand-written DF64 WGSL files (GEMM, force fields, lattice QCD, ML)
- `compile_shader_df64()` — auto-injects DF64 core + transcendentals
- `df64_rewrite` — naga-guided compiler pass (Layer 2 of universal precision)
- `Fp64Strategy` enum with `Native`, `Hybrid`, `Concurrent` variants
- Runtime f64 probe (`basic_f64` compile test) catches NAK/NVVM failures

What remains (barraCuda team scope):

- [ ] Validate `df64_rewrite` across all ~280 ops for correctness
- [ ] Make `df64_rewrite` the default compilation path on consumer GPUs
- [ ] Cross-precision validation harness (f64 vs df64 vs f32 reference)
- [ ] Benchmark automatic rewrite vs hand-written DF64 shaders
- [ ] Document precision boundaries (where automatic rewrite needs overrides)

---

## References

- `barraCuda/specs/ARCHITECTURE_DEMARCATION.md` — 3-layer ownership
- `toadStool/specs/HYBRID_FP64_CORE_STREAMING.md` — hybrid precision spec
- `toadStool/DEBT.md` D-DF64 entry — now marked as transferred
- groundSpring V35/V37 — original discovery of NAK f64 compilation failures
