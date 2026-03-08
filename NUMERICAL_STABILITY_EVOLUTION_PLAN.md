# Numerical Stability Evolution Plan — Fast AND Safe Math

**Date**: March 8, 2026
**Reporter**: hotSpring v0.6.19
**Affects**: barraCuda, coralReef, BearDog, ToadStool, ALL springs
**Type**: Cross-primal evolution plan
**Principle**: Prove stability first. Then go FAST. Then go ENCRYPTED.

---

## The Vision

Every source of numerical instability must be found and eliminated. This
enables a cascade of capabilities:

```
Stable math → Fast math (route to cheapest precision that works)
            → Safe math (no silent corruption at any tier)
            → Encrypted math (FHE-compatible, predictable noise budget)
            → Sovereign math (pure Rust, any hardware, any precision)
```

If we can prove an algorithm is stable under f32 (7 digits), it will be
stable under DF64 (14 digits), f64 (15 digits), CKKS (approximate FHE),
AND precision mixing (moving data between tiers). Stability is the
foundation that makes everything else possible.

---

## Tier 1: Precision Stability (COMPLETE — March 6, 2026)

### What We Proved

Full audit of 9 cancellation-prone computation families across 70+ WGSL
shaders. Two severe cases fixed, one guarded, six documented.

**Case 1: Plasma W(z) = 1 + z·Z(z)**

| Algorithm | f32 at z=5.57 | f64 at z=5.57 | Status |
|-----------|:---:|:---:|:---:|
| **Naive** 1+z·Z(z) | -8.03e7 (GARBAGE) | 7.44e-3 (wrong sign) | UNSTABLE |
| **Stable** asymptotic | -1.69e-2 (correct) | -1.69e-2 (correct) | STABLE |

**Case 2: BCS v² = 0.5*(1 - ε/E_qp)**

| Algorithm | f32 (eps=100, Δ=1) | f64 (eps=100, Δ=1) | Status |
|-----------|:---:|:---:|:---:|
| **Naive** 1-ε/E_qp | v²=0 (GARBAGE) | 11 digits | UNSTABLE |
| **Stable** Δ²/(2·E_qp·(E_qp+\|ε\|)) | v²=2.5e-5 (correct) | 15 digits | STABLE |

**Case 3: Jacobi eigensolve diff = aqq - app** — existing 1e-14 guard
produces π/4 rotation for degenerate eigenvalues. SAFE at all tiers.

**Additional**: 6 more functions analyzed (gradient flow energy, Mermin
susceptibility ratio, SU(3) Gram-Schmidt, Yukawa, ESN leaky, sigmoid).
All documented as acceptable or already mitigated.

10 new stability tests total (5 for W(z), 5 for BCS v²).
3 WGSL shaders updated with stable BCS v² formula.

### Owner: barraCuda (P1)

Ship stable special function primitives in `special_f64.wgsl`:
- `plasma_w_f64(z)` — direct asymptotic for |z| ≥ 4
- `bcs_v2_stable(eps, delta)` — Δ²-based formula for |ε| > |Δ|
- `erfc_f64(x)` — continued fraction for large x
- `log1p_f64(x)` — series for |x| ≪ 1
- `expm1_f64(x)` — series for |x| ≪ 1

See: `wateringHole/GPU_F64_NUMERICAL_STABILITY.md`
See: `hotSpring/experiments/046_PRECISION_STABILITY_ANALYSIS.md`

---

## Tier 2: Precision Mixing Stability (NEXT)

### The Problem

Real workloads mix precisions:
- Upload f64 data → GPU computes in DF64 → read back as f64
- f32 accumulation → f64 reduction → f32 storage
- CKKS encode f64 → polynomial ring (mod q) → decode f64

Each transition is a potential source of silent corruption.

### Mixing Scenarios to Test

| Source | Destination | Risk | Test |
|--------|-------------|------|------|
| f64 → DF64 → f64 | Round-trip precision loss | hi+lo ≠ original | Upload/readback identity |
| f32 → f64 promotion | Phantom precision (looks precise, isn't) | assert f32 noise floor | Known-value round-trip |
| f64 → f32 truncation | Catastrophic if near cancellation | Stable algorithms immune | W(z) at f32 after f64 compute |
| DF64 → f64 → DF64 | Double-float reassembly error | Two-sum correctness | Dekker/Knuth identity tests |
| GPU → CPU → GPU | FMA behavior change at each hop | Accumulation mismatch | Multi-hop identity test |

### Owner: barraCuda (P1) + springs (testing)

barraCuda already has `f64_to_df64` and `df64_to_f64` conversion helpers.
Need systematic round-trip tests with known-value inputs at the precision
boundary (e.g., values where f32 → f64 promotion introduces phantom bits).

---

## Tier 3: FHE Noise Stability (FUTURE — BearDog + barraCuda)

### Why Stability Matters for FHE

CKKS (Cheon-Kim-Kim-Song) is the FHE scheme for approximate real-number
computation. It encodes real numbers as polynomials over cyclotomic rings.
Every operation introduces noise:

```
Fresh ciphertext:     noise ≈ σ (small)
After addition:       noise ≈ σ₁ + σ₂
After multiplication: noise ≈ Δ · (σ₁ · σ₂)  ← grows FAST
After rescaling:      noise ≈ noise / Δ        ← managed
```

An unstable algorithm in CKKS:
1. **More operations** — power series needs 40-80 terms vs 6-10 for asymptotic
2. **Larger intermediates** — terms reach 10⁶ before cancelling, consuming
   more noise budget per multiplication
3. **Cancellation amplifies noise** — subtracting near-equal encrypted values
   amplifies the FHE noise exactly like it amplifies ULP rounding errors

A stable algorithm in CKKS:
1. **Fewer operations** — asymptotic converges in ~6 multiplications
2. **Small intermediates** — no large values, less noise per operation
3. **No cancellation** — noise passes through without amplification

### Impact on Noise Budget

For W(z) at z=5.57 in CKKS with multiplicative depth L:

| Algorithm | Multiplications | Max Intermediate | Noise Amplification | Required Depth |
|-----------|:---:|:---:|:---:|:---:|
| **Naive** | ~80 | ~10⁶ | 10⁹× (cancellation) | L ≈ 80+ |
| **Stable** | ~10 | ~1 | 1× (no cancellation) | L ≈ 10 |

The stable algorithm requires **8× less multiplicative depth** and
**zero noise amplification** — making it actually feasible for FHE
where the naive algorithm would exhaust the noise budget.

### Current FHE Infrastructure

| Component | Owner | Status |
|-----------|-------|--------|
| NTT/INTT (GPU) | barraCuda | ✅ 19/19 tests |
| Pointwise multiply | barraCuda | ✅ Implemented |
| Key switch | barraCuda | ✅ Implemented |
| Modulus switch | barraCuda | ✅ Implemented |
| Galois rotate | barraCuda | ✅ Implemented |
| BFV scheme | ToadStool showcase | ✅ PoC |
| CKKS scheme | ToadStool showcase | ✅ PoC |
| Key generation | BearDog (planned) | ⬜ Roadmap |
| Noise management | barraCuda | ✅ fhe_modulus_switch |
| Encrypted special functions | — | ⬜ **NEW** (this plan) |

### Owner: BearDog (ciphertext) + barraCuda (GPU FHE ops)

The stable special functions we're building NOW become the encrypted special
functions LATER. Same algorithm, same code path, different data representation.

---

## Tier 4: Genetic Entropy Mixing Stability (FUTURE — BearDog)

### Connection to Numerical Stability

BearDog's genetic entropy mixing (BLAKE3-based three-tier hierarchy) is
cryptographically stable by construction — hash functions have avalanche
property and uniform output regardless of input distribution.

But when genetic mixing is used to derive FHE parameters (ring dimension,
modulus chain, noise distribution), the QUALITY of those parameters affects
the noise budget available for computation. Higher-quality entropy from
Tier 3 (human-lived experience) produces better randomness for:

- CKKS secret key sampling (Gaussian noise)
- Key switching key generation
- Bootstrapping key generation

If the entropy mixing produces biased randomness (a genetic mixing bug),
the FHE noise budget could be silently reduced, making previously-stable
algorithms fail under encryption. This connects genetic stability to
numerical stability.

### Owner: BearDog (P3 — future, once FHE is active)

---

## Evolution Path

```
Phase 1 (DONE):    Stable algorithms — prove f32/DF64/f64 stability ✅
                   10 stability tests, 3 shader fixes, 9 families audited
                   hotSpring Experiment 046

Phase 2 (NEXT):    Precision mixing — round-trip tests at every boundary
                   barraCuda: f64↔DF64, f32↔f64, GPU↔CPU identity tests
                   coralReef: FMA control for bit-exact CPU parity

Phase 3 (FUTURE):  FHE stability — stable algorithms as CKKS circuits
                   barraCuda: encrypted special functions (NTT-domain)
                   BearDog: key generation, scheme parameters
                   ToadStool: FHE pipeline orchestration

Phase 4 (HORIZON): Sovereign encrypted compute
                   coralReef: GPU FHE without Vulkan overhead
                   BearDog: genetic entropy for FHE key material
                   metalForge: CPU↔GPU↔NPU FHE dispatch
```

Each phase validates the previous:
- Phase 2 mixing tests catch silent precision corruption
- Phase 3 FHE tests prove the algorithms survive noise
- Phase 4 sovereign tests prove hardware independence

### The Payoff

```
Fast:       Route to cheapest precision (f32 cores at 64:1 throughput)
Safe:       Proven stable at every tier (no silent corruption)
Encrypted:  FHE-compatible (predictable noise, feasible depth)
Sovereign:  Pure Rust (no C deps, no vendor lock, any hardware)
```

Fast AND safe math. Fast AND safe Rust.

---

## Evidence

- `wateringHole/GPU_F64_NUMERICAL_STABILITY.md` — Tier 1 proof (W(z) + BCS v²)
- `hotSpring/experiments/046_PRECISION_STABILITY_ANALYSIS.md` — full 9-family analysis
- `hotSpring/specs/PRECISION_STABILITY_SPECIFICATION.md` — hotSpring stability spec
- `hotSpring/barracuda/src/physics/dielectric.rs` — 5 W(z) stability tests
- `hotSpring/barracuda/src/physics/hfb_common.rs` — 5 BCS v² stability tests
- `hotSpring/barracuda/src/physics/shaders/dielectric_mermin_f64.wgsl` — stable W(z)
- `hotSpring/barracuda/src/physics/shaders/batched_hfb_density_f64.wgsl` — stable BCS v²
- `hotSpring/barracuda/src/physics/shaders/bcs_bisection_f64.wgsl` — stable BCS v²
- `hotSpring/barracuda/src/physics/shaders/deformed_density_energy_f64.wgsl` — stable BCS v²
- `barraCuda/crates/barracuda/src/ops/fhe_*.rs` — FHE GPU infrastructure
- `phase1/toadStool/showcase/homomorphic-computing/` — CKKS/BFV PoC
- `phase1/bearDog/crates/beardog-genetics/` — entropy mixing engine

---

*ecoPrimals — AGPL-3.0-only*
