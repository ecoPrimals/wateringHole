<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->

# healthSpring V35 → toadStool / barraCuda Evolution Handoff

**Date**: March 17, 2026
**From**: healthSpring V35
**To**: toadStool team, barraCuda team, coralReef team
**License**: AGPL-3.0-or-later
**Pins**: barraCuda v0.3.5, toadStool S156+, coralReef Phase 10 Iteration 52+

---

## Executive Summary

- healthSpring V35 has **613 tests**, **73 experiments**, **6 WGSL shaders**, **79 JSON-RPC capabilities**
- IPC resilience (CircuitBreaker, RetryPolicy, DispatchOutcome&lt;T&gt;) absorbed from ecosystem
- Sovereign GPU dispatch via CoralReefDevice wired (feature-gated)
- **3 Tier B WGSL shaders** ready for barraCuda absorption
- Safe cast module prevents silent truncation in GPU dispatch parameters

---

## Part 1: barraCuda Primitive Consumption Map

healthSpring consumes these barraCuda modules:

| Module | Primitives Used |
|--------|-----------------|
| stats | shannon_from_frequencies, simpson, pielou_evenness, chao1_classic, bray_curtis, hill, mean |
| ops | HillFunctionF64, PopulationPkF64, DiversityFusionGpu |
| device | WgpuDevice, CoralReefDevice (sovereign-dispatch feature) |
| numerical | OdeSystem, BatchedOdeRK4 |
| rng | lcg_step, LCG_MULTIPLIER, state_to_f64, uniform_f64_sequence |
| health | pkpd::mm_auc, microbiome::antibiotic_perturbation, biosignal::scr_rate |
| special | anderson_diagonalize |

**NOT used**: linalg (local 2×2/3×3 Cholesky — intentional optimization), nn, spectral, nautilus, validation

---

## Part 2: WGSL Shader Status

| Shader | Tier | Status | barraCuda action |
|--------|------|--------|------------------|
| hill_dose_response_f64.wgsl | A | Absorbed upstream | Lean — local copy for reference only |
| population_pk_f64.wgsl | A | Absorbed upstream | Lean — local copy for reference only |
| diversity_f64.wgsl | A | Absorbed upstream | Lean — local copy for reference only |
| michaelis_menten_batch_f64.wgsl | B | Local, validated (Exp083) | **Absorb** — per-patient MM ODE with Wang hash PRNG |
| scfa_batch_f64.wgsl | B | Local, validated (Exp083) | **Absorb** — 3-output Michaelis-Menten kinetics |
| beat_classify_batch_f64.wgsl | B | Local, validated (Exp083) | **Absorb** — per-beat template cross-correlation |

---

## Part 3: Sovereign Dispatch Wiring

- `gpu/sovereign.rs` calls `CoralReefDevice::with_auto_device()` when `sovereign-dispatch` feature is enabled
- Uses `discover_shader_compiler()` from `ipc/socket.rs` as fast-path hint
- HillSweep is first sovereign op; other ops fall back to wgpu path
- `strip_f64_enable()` documented as legacy path — coralReef's f64 lowering replaces it

**toadStool action**: Verify `PrecisionRoutingAdvice` for healthSpring workloads (population PK Monte Carlo is the highest-priority GPU workload at >100K patients)

**coralReef action**: Confirm healthSpring's 6 WGSL shaders compile on SM70+ (they should — hotSpring/groundSpring reported 84/93 cross-spring shaders compiling)

---

## Part 4: IPC Evolution

- `IpcError` (8 variants) with `thiserror` — aligns with airSpring/groundSpring
- `DispatchOutcome<T>` — protocol vs application error separation
- `CircuitBreaker` + `RetryPolicy` — exponential backoff, 3 failures → open, 5s cooldown
- 4-format capability parsing — handles all ecosystem response shapes
- `safe_cast` module — `usize_u32`, `usize_f64`, `f64_f32` for GPU dispatch parameters

**toadStool action**: healthSpring's `compute_dispatch` client already uses typed wrappers for `compute.dispatch.submit/result/capabilities`. Confirm these align with current toadStool IPC contract.

---

## Part 5: GPU Evolution Readiness

| Rust Module | GPU Status | Next Step |
|-------------|------------|-----------|
| pkpd/dose_response | Tier A via barraCuda HillFunctionF64 | Done — Lean |
| pkpd/population_pk | Tier A via barraCuda PopulationPkF64 | Done — Lean |
| microbiome/diversity | Tier A via barraCuda DiversityFusionGpu | Done — Lean |
| pkpd/nonlinear (MM) | Tier B local shader | **barraCuda absorb** |
| microbiome/clinical (SCFA) | Tier B local shader | **barraCuda absorb** |
| biosignal/arrhythmia | Tier B local shader | **barraCuda absorb** |
| pkpd/nlme (FOCE/SAEM) | CPU only | Tier C — new shader needed (per-subject gradient) |
| microbiome/anderson | CPU only | Tier C — eigensolve shader needed |
| biosignal/fft | CPU only | Tier C — radix-2 FFT shader exists in barraCuda |

---

## Part 6: Learnings for Upstream

1. **`enable f64;` in WGSL must be stripped** — wgpu/naga handles f64 via device features, not shader directives. The `strip_f64_enable()` workaround should be obsoleted by coralReef's native compilation.

2. **`pow(f64, f64)` is unsupported on NVIDIA via NVVM** — use `exp(n * log(c))` cast through f32. coralReef's f64 transcendental lowering (DFMA on NVIDIA, native on AMD) should resolve this.

3. **u64 PRNG not portable across GPU vendors** — u32-only xorshift32 + Wang hash is the safe pattern.

4. **Fused pipeline (single encoder) eliminates ~30× overhead** at small sizes. TensorSession will formalize this.

5. **At 10M+ elements, memory bandwidth dominates** — buffer streaming needed for next tier.

6. **`safe_cast` module prevents silent truncation** when converting usize → u32 for GPU buffer sizes. Recommend upstream equivalent.

7. **healthSpring's local Cholesky** (2×2/3×3 special case with general fallback) is faster than barraCuda's general Cholesky for NLME iteration — document as intentional optimization, not a gap.

---

## Part 7: Recommended Upstream Actions

### barraCuda team

| # | Action |
|---|--------|
| 1 | Absorb 3 Tier B shaders (michaelis_menten_batch, scfa_batch, beat_classify_batch) into `shaders/bio/` or `shaders/science/` |
| 2 | Add `safe_cast` equivalent to barraCuda core (prevents silent truncation in all springs) |
| 3 | When TensorSession ships f64 support, healthSpring's `execute_fused()` can migrate |

### toadStool team

| # | Action |
|---|--------|
| 1 | Verify `SpringDomain::Health` is registered in the provenance flow matrix |
| 2 | Confirm `compute.dispatch.submit` contract alignment with healthSpring's `compute_dispatch` client |
| 3 | Add healthSpring's 6 WGSL shaders to the cross-spring shader validation suite |

### coralReef team

| # | Action |
|---|--------|
| 1 | Compile healthSpring's 6 WGSL shaders to SM70+ SASS as part of cross-spring validation |
| 2 | Confirm f64 transcendental support for `exp(n * log(c))` pattern (Hill dose-response core) |

---

**healthSpring V35 | 613 tests | 73 experiments | 6 WGSL shaders | 79 capabilities | AGPL-3.0-or-later**
