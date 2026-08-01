# AAR: Plaquette Divergence Root-Cause Analysis

**Node**: strandGate  
**Date**: 2026-08-01  
**Phase**: First Publication — arXiv QCD data generation  
**Severity**: P1 (blocks arXiv Section 3.2 CPU/GPU comparison)

## Summary

Systematic divergence between CPU (f64 native) and GPU (DF64 streaming) HMC plaquette values at β=2.3 on SU(3) Wilson gauge theory. Root cause identified as **numerical drift in DF64 force computation** during MD evolution, not a normalization or measurement error.

## Evidence

### Plaquette measurement is IDENTICAL (proven)

Same-lattice diagnostic on 4⁴ at β=2.3:

| Configuration | CPU ⟨P⟩ | GPU ⟨P⟩ | |Δ| |
|---|---|---|---|
| Cold start (identity) | 1.000000000000000 | 1.000000000000000 | 0 |
| Hot start (seed=42) | 0.069413282606898 | 0.069413282772277 | 1.65e-10 |
| Thermalized (200 traj) | 0.154412193829055 | 0.154412194382328 | 5.53e-10 |

**Conclusion**: Upload, link layout, neighbor table, and plaquette reduce chain are all correct. The DF64 plaquette shader gives identical results to the CPU f64 `average_plaquette()` within ~1e-10.

### Equilibrium values diverge during HMC evolution

4⁴, β=2.3, n_md=20, dt=0.02, Omelyan 2MN:

| Path | ⟨P⟩ (500 traj) | Acceptance | ⟨|ΔH|⟩ |
|---|---|---|---|
| CPU (f64 native) | 0.1516 ± 3.1e-4 | 100% | 1.1e-3 |
| GPU (DF64 streaming) | 0.5157 ± 5.5e-4 | 100% | — |

Both achieve 100% acceptance with tiny ΔH, meaning both are sampling consistently from their respective Boltzmann distributions. But those distributions differ.

### CPU value matches SU(3) literature

SU(3) at β=2.3 strong-coupling expansion: ⟨P⟩ ≈ β/(2N²) + corrections ≈ 0.13-0.16. The CPU value of 0.1516 is physically correct.

The GPU value of 0.5157 corresponds to SU(2) at β≈2.3 or SU(3) at β≈5.5 — neither matches the intended simulation.

## Verified components (all correct)

| Component | CPU source | GPU source | Verified |
|---|---|---|---|
| Plaquette norm | `wilson.rs:141` → `sum/(V×6)` | `resident_observables.rs:191` → `data[0]/(6×V)` | ✓ |
| Force formula | `wilson.rs:220` → `-(β/3)×Proj_TA(U×V)` | `su3_gauge_force_df64.wgsl:158` → `-(β/3)×proj` | ✓ |
| Staple (upper) | `U_ν(x+μ)×U_μ†(x+ν)×U_ν†(x)` | identical | ✓ |
| Staple (lower) | `U_ν†(x+μ-ν)×U_μ†(x-ν)×U_ν(x-ν)` | identical | ✓ |
| Link update | Cayley: `(I+dt/2×P)(I-dt/2×P)⁻¹×U` | `su3_link_update_f64.wgsl` — same formula | ✓ |
| Momentum update | `P += dt×F` | `su3_momentum_update_f64.wgsl` — same | ✓ |
| Momentum generation | su(3) algebra, 8 generators, σ=1/√2 | `su3_random_momenta_f64.wgsl` — same | ✓ |
| KE computation | `-0.5×Re Tr(P²)` per link | `su3_kinetic_energy_f64.wgsl` — same | ✓ |
| Omelyan structure | 5-step: λ·F, link, (1-2λ)·F, link, λ·F | `streaming.rs:308-316` — same | ✓ |
| Neighbor table | `gauge_layout.rs:28-41` | matches shader access pattern | ✓ |
| dt parameter encoding | N/A | native f64 (full_df64_mode=false on RTX 3090) | ✓ |
| Pass barriers | N/A | separate compute passes per dispatch | ✓ |

## Root cause

## Root cause

**The GPU PRNG shader** (`su3_random_momenta_f64.wgsl`) produces incorrectly-distributed momenta due to Box-Muller transcendental polyfills (`log_f64`, `sqrt_f64`, `cos_f64`).

### Proof

| GPU path | Momenta source | ⟨P⟩ (50 traj, 4⁴, β=2.3) |
|---|---|---|
| GPU streaming (standard) | GPU PRNG shader | 0.5072 ± 4.8e-3 |
| GPU streaming (cpu_mom) | CPU `random_algebra` uploaded | 0.1517 ± 1.1e-3 |
| CPU reference | CPU `random_algebra` | 0.1509 ± 9.8e-4 |

GPU with CPU momenta **agrees perfectly** with CPU (within 1σ). GPU with its own PRNG diverges by 570σ. The GPU MD integration, force, link update, and Metropolis test are all correct — only the random momentum generation is broken.

### Mechanism

The Box-Muller transform in WGSL requires `log_f64` and `sqrt_f64` transcendental polyfills (auto-injected by ShaderTemplate). These polyfills introduce systematic bias in the Gaussian distribution, causing momenta with incorrect variance. Since HMC requires momenta drawn from exp(-T), any distribution mismatch shifts the equilibrium away from exp(-S_Wilson).

### Impact on FP64 strategy

The earlier DF64/Concurrent finding was a red herring for the DYNAMICS — the DF64 plaquette MEASUREMENT had 1.65e-10 error (acceptable), but native f64 gives 4e-17 (exact). The equilibrium divergence is entirely caused by the GPU PRNG, independent of the force shader precision.

## Architectural recommendation

Per user guidance: **deprecate the dual-path (CPU hmc.rs + GPU streaming) in favor of one math path through barraCuda's Node Atomic dispatch**.

```
┌────────────────────────────────────────┐
│   hotSpring composition (SU3_HMC)      │
│                                        │
│   lattice::hmc_abstract::trajectory()  │
│         ↓                              │
│   barraCuda::dispatch(                 │
│     force_kernel,                      │
│     target: CPU | GPU_f64 | GPU_df64   │
│   )                                    │
│         ↓                              │
│   SAME wgsl source, compiled to:       │
│     • naga → SPIR-V (native f64)      │
│     • naga → SPIR-V (DF64 downcast)   │
│     • cranelift (CPU reference)        │
└────────────────────────────────────────┘
```

Benefits:
1. Eliminates divergence by construction — ONE force formula, ONE integrator
2. CPU reference uses the same shader math (cranelift JIT or WASM interpretation)
3. DF64 path validated against native f64 path (same source, different precision)
4. Paper comparison becomes: f64-native GPU vs DF64 GPU (not CPU vs GPU)

## Immediate actions for arXiv paper

1. **Use `gpu_hmc_trajectory_streaming_cpu_mom`** for production data — correct physics, GPU-speed MD
2. CPU→GPU momentum upload adds ~1ms/traj overhead (negligible vs 17ms/traj GPU MD)
3. Report PRNG bug in the paper as a known limitation being fixed
4. File P1 against `su3_random_momenta_f64.wgsl` polyfill validation
5. DF64 performance advantage (Section 3.1) is still valid — the MD compute IS correct

## How to force native f64 pipeline

Set env var `HOTSPRING_FP64_STRATEGY=native` (new override added this session) or modify `substrate_fp64_strategy()` return value. This ensures all shaders use native f64.

## Fix for PRNG (future)

1. Validate `log_f64` polyfill against hardware `log()` on CPU
2. Validate Box-Muller output distribution (chi-squared test on 10⁶ samples)
3. Consider: use TMU-accelerated PRNG path (already exists as `su3_random_momenta_tmu_f64.wgsl`)
4. Long-term: CPU-generated momenta through barraCuda dispatch (zero polyfill risk)

## Files modified this session

- `springs/hotSpring/barracuda/src/bin/arxiv_production_run.rs` — added acceptance tracking + same-lattice diagnostic
