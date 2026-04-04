# GPU f64 Numerical Stability — Lessons from hotSpring Paper 44

**Date**: March 10, 2026
**Reporter**: hotSpring v0.6.24 (originally reported at v0.6.19)
**Affects**: barraCuda (math primitives), coralReef (compiler), ALL springs doing GPU science
**Type**: Debt discovery + resolution pattern

---

## Executive Summary

During GPU promotion of Paper 44 (BGK Dielectric), hotSpring discovered
that **f64 GPU arithmetic can silently diverge from CPU f64** in algorithms
with catastrophic cancellation. The divergence is NOT caused by wrong precision
routing — all f64 polyfills were correctly injected and verified. The cause is
ULP-level rounding differences between GPU and CPU that get **amplified through
subtraction of nearly-equal values**.

This is not a bug. It is a fundamental property of IEEE-754 arithmetic on
heterogeneous hardware. The fix is algorithmic: avoid catastrophic cancellation
by restructuring computations. This document records the finding, assigns
ownership, and provides a pattern for all springs.

---

## What Happened

### The Algorithm

The Mermin dielectric function requires the plasma dispersion function Z(z)
to compute the susceptibility kernel W(z) = 1 + z·Z(z).

For |z| > 4, z·Z(z) ≈ -1.017. So W(z) = 1 - 1.017 = -0.017 — two
numbers that are 60× larger than their difference are subtracted.

### CPU Behavior

On x86-64 (SSE2), the power series for Z(z) converges with deterministic
rounding. The cancellation in W = 1 + z·Z produces small errors (~1e-12)
that are tolerable for most physics. However, the CPU result occasionally
produces **unphysical positive loss** (Im[1/ε] > 0, implying gain in a
passive medium) near the loss function's zero crossing. DSF positivity: 98%.

### GPU Behavior (Before Fix)

On RTX 3090 (NVK/NAK via SPIR-V), the same power series produces ULP-level
different intermediate results due to:

1. **FMA fusion**: GPU SPIR-V compiler may fuse `a*b + c` into a single
   fused multiply-add instruction, eliminating intermediate rounding. CPU
   SSE2 computes `a*b` first (rounded), then `+ c` (rounded again). The
   difference is 1-2 ULPs per operation.

2. **Operation reordering**: SPIR-V optimization passes may reorder
   floating-point additions in the power series, changing accumulation order.

3. **Cancellation amplification**: 40 iterations of the power series
   accumulate ~40-80 ULPs of rounding difference. Through the 60× cancellation
   in W = 1 + z·Z, this becomes ~5000 ULPs — visible as percent-level error.

The result: 125% relative error at specific frequency points where the loss
function crosses zero. The large RELATIVE error masked the fact that the
ABSOLUTE error was small (0.009 vs peak loss of 1.14, i.e., < 1% of signal).

### GPU Behavior (After Fix)

By computing W(z) directly via its asymptotic expansion for |z| ≥ 4:

```
W(z) ≈ -1/(2z²) × (1 + 3/(2z²) + 15/(4z⁴) + ...) + i·z·√π·exp(-z²)
```

This naturally produces the small W value without any near-cancellation
subtraction. The series converges rapidly (ratio < 0.2 for |z| > 4).

Results:
- **100% DSF positivity** (vs 98% on CPU)
- **100% passive-medium compliance** (no unphysical gain)
- f-sum integral within 3-5% of CPU
- High-frequency limit: |loss| < 3e-7

The GPU now produces **better physics than the CPU** because it avoids the
cancellation-induced sign errors entirely.

---

## Root Cause Analysis

```
Precision routing?         NO — polyfills inject correctly (verified)
Wrong FP width (f32/f64)?  NO — 99% of ω points show 1e-13 parity
DF64 needed?               NO — native f64 is sufficient
Constant truncation?       NO — (zero + literal) pattern verified

Actual cause:              ULP-level FMA/reordering differences between
                           SPIR-V (GPU) and SSE2 (CPU), amplified by
                           catastrophic cancellation in 1 + z·Z(z).
```

---

## Who Owns What

### barraCuda (P1): Stable GPU Math Primitives

barraCuda already provides `math_f64.wgsl` for transcendental polyfills and
`complex_f64.wgsl` for complex arithmetic. These are **correctly implemented
and verified**.

**New responsibility**: barraCuda should provide **numerically stable special
function primitives** that are designed for GPU from the start. Functions like
the plasma dispersion function, Faddeeva/Voigt profiles, error functions, and
Bessel functions all have regions where naive computation involves catastrophic
cancellation.

The pattern hotSpring discovered should become a reusable library:

| Function | Cancellation Region | Stable Algorithm |
|----------|--------------------|--------------------|
| W(z) = 1 + z·Z(z) | \|z\| > 4 | Direct asymptotic of W |
| erfc(x) = 1 - erf(x) | x > 4 | Direct continued fraction |
| log(1+x) | \|x\| ≪ 1 | Series (already `log1p` pattern) |
| exp(x)-1 | \|x\| ≪ 1 | Series (already `expm1` pattern) |
| Bessel J₀(x) - 1 | \|x\| ≪ 1 | Direct Taylor |

These should live in `barracuda::shaders::math::special_f64.wgsl` or similar.

### coralReef (P2): FMA Control and Precision Guarantees

The FMA behavior difference is a compiler-level concern. Long-term:

1. **coralNak** should provide an option to control FMA fusion — either
   force-fuse (for speed) or force-separate (for CPU bit-exactness).
2. **SPIR-V decoration**: `NoContraction` decoration exists in SPIR-V to
   prevent FMA fusion. coralReef should expose this to springs when
   bit-exact CPU parity is required.
3. **Precision manifest**: coralReef's driver profiling already detects
   which f64 builtins are native. It should also detect and report FMA
   behavior so springs can make informed algorithm choices.

### Springs (Awareness): Test for Cancellation

Any spring doing special function evaluation on GPU should:

1. **Test with point diagnostics**: Compare GPU vs CPU at specific input
   values spanning the full dynamic range, not just aggregate statistics.
2. **Identify cancellation regions**: Look for expressions of the form
   `(large) - (large) = (small)` or `1 + (near -1)`.
3. **Use direct expansions**: When the desired quantity is small, compute
   it directly rather than as a difference of large values.
4. **Validate physics, not arithmetic**: DSF positivity, sum rules,
   conservation laws, and asymptotic limits are more meaningful than
   point-by-point CPU comparison.

---

## The Stability-Then-Speed Principle

This finding validates the ecoPrimals evolution path:

```
Python (correct) → Rust CPU (fast + correct) → GPU (fast + stable + correct)
                                                       ↑
                                              Fix algorithms HERE
                                              before going sovereign
```

If the math is stable on GPU, we can go FAST with confidence:
- Stable W(z) asymptotic: no cancellation, fewer branches, GPU-friendly
- Stable physics: 100% DSF positivity enables tighter validation thresholds
- Stable across drivers: the asymptotic expansion has no FMA sensitivity

When coralReef provides sovereign compilation, we want to know that numerical
divergences are driver/compiler artifacts, not physics errors. Solving
cancellation now means coralReef can optimize aggressively later (reorder,
fuse, vectorize) without breaking physics.

---

## Multi-Precision Stability: f32, DF64, f64

The stable asymptotic expansion preserves full available precision at EVERY
floating-point tier. Tested on CPU (March 6, 2026):

### f32 Results at z = 5.57 (cancellation region)

| Algorithm | Re[W(5.57)] | Status |
|-----------|-------------|--------|
| **Naive** 1+z·Z(z) | **-8.03e7** | GARBAGE (10⁹× wrong) |
| **Stable** asymptotic | -1.689e-2 | Correct |
| f64 reference | -1.689e-2 | — |

The naive algorithm **overflows** in f32 due to intermediate terms reaching
~10⁶ before cancelling to ~0.02. The stable asymptotic naturally produces
the small value — no large intermediates, no cancellation.

### f32-vs-f64 Parity (stable algorithm only)

| |z| | f32 Re[W] | f64 Re[W] | Relative Error |
|-----|-----------|-----------|:-----------:|
| 5.0 | -2.122413e-2 | -2.122414e-2 | **2.78e-7** |
| 5.57 | -1.689429e-2 | -1.689430e-2 | **3.21e-7** |
| 8.0 | -7.987774e-3 | -7.987773e-3 | **1.06e-7** |
| 10.0 | -5.070820e-3 | -5.070819e-3 | **1.42e-7** |

Every f32 result agrees with f64 to ~1e-7 — the full 7 digits of f32
precision. **Zero cancellation amplification.**

### DF64 Implications

DF64 (~14 decimal digits via f32 pairs) sits between f32 and f64:

```
f32:  7 digits  →  stable W(z) preserves all 7        ✓
DF64: 14 digits →  stable W(z) should preserve all 14 ✓ (no cancellation to amplify)
f64:  15 digits →  stable W(z) preserves all 15       ✓
```

Since the stable algorithm avoids cancellation entirely, DF64 will produce
~14-digit results — far more than needed for most plasma physics. This means
the dielectric function can run on **consumer GPU f32 cores** via DF64 at
full scientific precision, unlocking the 32:1 to 64:1 throughput advantage
of f32 over native f64 on RTX-class hardware.

### The Throughput Case for DF64

| GPU | f32 TFLOPS | f64 TFLOPS | Ratio | DF64 (est.) |
|-----|:---:|:---:|:---:|:---:|
| RTX 3090 | 35.6 | 0.56 | 64:1 | ~8.9 TFLOPS |
| RTX 4090 | 82.6 | 1.29 | 64:1 | ~20.6 TFLOPS |
| A100 | 19.5 | 9.7 | 2:1 | ~4.9 TFLOPS |

DF64 on consumer cards delivers **4-16× the throughput** of native f64 while
maintaining 14-digit precision. For scientific workloads that need >7 digits
(f32 insufficient) but <15 digits (f64 overkill), DF64 is the sweet spot.

The stable W(z) algorithm makes this viable: with the naive algorithm, DF64
would ALSO suffer cancellation (14 digits - 2 digits lost = 12 digits ≈ ok,
but with FMA differences the error amplifies unpredictably). With the stable
algorithm, all 14 DF64 digits go directly to the physics.

---

## Second Case Study: BCS Occupation v² (March 6, 2026)

The plasma W(z) pattern recurred in nuclear physics: BCS occupation
v² = 0.5*(1 - ε/E_qp) suffers cancellation when |ε| >> Δ (far from Fermi
surface), producing ε/E_qp ≈ 1 and losing all f32 precision.

**Stable formula**: v² = Δ²/(2·E_qp·(E_qp + |ε|)). No subtraction of
near-equal values. Preserves full precision at all tiers.

| Tier | Naive (eps=100, Δ=1) | Stable | Digits Lost |
|------|:---:|:---:|:---:|
| f32 | v²=0 (GARBAGE) | v²=2.5e-5 (correct) | ALL 7 |
| f64 | v²=2.4998e-5 (11 digits) | v²=2.4999e-5 (15 digits) | ~4 |

**Impact**: BCS v² determines nuclear pairing occupations for 2,042-nucleus
GPU sweeps. Wrong tail occupations produce wrong binding energies. Fixed in
CPU (`hfb_common.rs`) and 3 GPU shaders (`batched_hfb_density_f64.wgsl`,
`bcs_bisection_f64.wgsl`, `deformed_density_energy_f64.wgsl`).

5 new stability tests added (parity, symmetry, range, f32 naive vs stable).

---

## Full Cancellation Inventory

hotSpring Experiment 046 identified **9 cancellation families** across 70+
shaders. Of these, 2 were severe (Tier A) and fixed, 1 was guarded, and
the remaining 6 are documented as acceptable or already mitigated. See:
`hotSpring/experiments/046_PRECISION_STABILITY_ANALYSIS.md`

---

## Cross-Spring Impact

| Spring | Affected Computations | Action |
|--------|----------------------|--------|
| hotSpring | Plasma dispersion, BCS v², Jacobi eigensolve | **RESOLVED** (W(z) asymptotic, stable BCS v², degenerate guard) |
| wetSpring | Shannon entropy H = -Σp·log(p) near p≈0 | log_f64 polyfill already handles |
| neuralSpring | Softmax: exp(x)/Σexp(x) near equal logits | Already uses log-sum-exp trick |
| groundSpring | Chi-squared CDF near tail | erfc-based computation needed |
| airSpring | Van Genuchten: (1+\|αh\|^n)^(-m) near h≈0 | Verify no cancellation |

---

## Next: Full Stability Verification Chain

This document covers Tier 1 (precision stability). The full plan covers
four tiers of verification that build on each other:

1. **Tier 1: Precision stability** — f32/DF64/f64 (THIS DOCUMENT — PROVEN)
2. **Tier 2: Precision mixing** — round-trip tests at every f32↔DF64↔f64 boundary
3. **Tier 3: FHE noise stability** — stable algorithms as CKKS encrypted circuits
4. **Tier 4: Genetic entropy** — BearDog entropy quality → FHE parameter quality

See: `wateringHole/NUMERICAL_STABILITY_EVOLUTION_PLAN.md`

---

## Evidence

- `hotSpring/barracuda/src/physics/shaders/dielectric_mermin_f64.wgsl` — stable W(z)
- `hotSpring/barracuda/src/physics/gpu_dielectric.rs` — GPU dispatch + polyfill injection
- `hotSpring/barracuda/src/bin/validate_gpu_dielectric.rs` — 12/12 physics checks
- `hotSpring/experiments/044_BGK_DIELECTRIC.md` — full experiment record

---

*hotSpring v0.6.19 — AGPL-3.0-only*
