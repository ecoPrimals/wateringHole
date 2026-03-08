<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# airSpring V0.7.4 → BarraCuda/ToadStool: Stochastic Methods & Drought Index Handoff

**Date**: March 7, 2026
**From**: airSpring (ecology/agriculture validation)
**To**: BarraCuda team (sovereign math engine) + ToadStool team (hardware dispatch)
**airSpring**: v0.7.4 (854 lib + 186 forge tests, 89 binaries, 0 clippy pedantic warnings)
**BarraCuda**: v0.3.3 standalone (`ecoPrimals/barraCuda`)
**ToadStool**: S130+ (`ecoPrimals/phase1/toadstool`)

---

## Executive Summary

airSpring v0.7.4 adds three new experiments that complete the stochastic uncertainty
quantification and drought analysis pipeline. These experiments validate the CPU paths
for existing GPU modules (`mc_et0`, `bootstrap`, `jackknife`) and introduce a new
`eco::drought_index` module for Standardized Precipitation Index computation. All three
are GPU-promotable and represent the next wave of barraCuda absorption candidates.

- **81 experiments** (was 78), **1284/1284 Python** (was 1237), **854 lib tests** (was 848), **89 binaries** (was 86)
- New `eco::drought_index` module consumes `barracuda::special::gamma::ln_gamma`
- New tolerance: `MC_ET0_PROPAGATION` in the 13-tier architecture
- Zero clippy warnings, zero unsafe, all formatting clean

---

## §1 What We Built

### Exp 079: Monte Carlo ET₀ Uncertainty Propagation

Validates `gpu::mc_et0::mc_et0_cpu` against a deterministic Python baseline using
Lehmer LCG (m=2³¹-1, a=16807) and Box-Muller transform for reproducible MC sampling.
Simplified FAO-56 PM ET₀ with Gaussian perturbation of temperature, humidity, wind,
and radiation inputs.

**Tests**: default uncertainty (N=2000), zero uncertainty (deterministic), high
uncertainty (10% CV), arid/humid climate gradient, convergence at multiple N values,
determinism (two runs identical), parametric CI consistency.

**Key finding**: ET₀ std dev ~ 0.2–0.5 mm/day for typical input uncertainty (3–5% CV).

### Exp 080: Bootstrap & Jackknife CI for Seasonal ET₀

Validates `gpu::bootstrap::GpuBootstrap::cpu()` and `gpu::jackknife::GpuJackknife::cpu()`
for seasonal ET₀ confidence intervals. Deterministic bootstrap resampling (B=1000) and
jackknife leave-one-out variance estimation.

**Tests**: full season statistics, known analytical values (mean=5.0, SE=1/√10),
small sample (n=5), constant data (CI width=0, variance=0), monotonicity
(larger data → tighter CI).

### Exp 081: Standardized Precipitation Index (SPI)

New `eco::drought_index` module implementing gamma MLE fitting (Thom 1958),
regularized incomplete gamma function (series + continued fraction), inverse
normal CDF, and multi-scale SPI computation (SPI-1/3/6/12). WMO drought
classification (extremely wet → extremely dry).

**Dependencies**: `barracuda::special::gamma::ln_gamma` — the only upstream
special function needed.

---

## §2 What BarraCuda/ToadStool Should Know

### New barraCuda dependency: `special::gamma::ln_gamma`

airSpring now calls `ln_gamma` from `eco::drought_index::gamma_mle_fit` and
`gamma_series`/`gamma_cf`. The function is called with positive shape parameters
(α > 0) only. Any API changes to `ln_gamma` will break SPI computation.

### GPU Promotion Candidates (3 new)

| Algorithm | Parallelism | Shader Exists? | Complexity |
|-----------|-------------|----------------|------------|
| MC ET₀ (N samples) | Per-sample | Yes (`mc_et0_propagate_f64.wgsl`) | Low — already wired |
| Bootstrap CI (B replicates) | Per-replicate | Yes (`BootstrapMeanGpu`) | Low — already wired |
| Jackknife (n samples) | Per-LOO sample | Yes (`JackknifeMeanGpu`) | Low — already wired |
| SPI drought (grid cells) | Per-cell | **No — new shader needed** | Medium — Newton-Raphson + gamma CDF |

The first three already have GPU shaders in barraCuda. airSpring's Python baselines
now provide the ground-truth benchmarks needed to validate GPU dispatch with confidence.

SPI is the new promotion candidate. The math per cell:
1. Rolling window sum (1/3/6/12 months) — trivial
2. Gamma MLE via Thom method — `ln(x̄) - mean(ln(x))`, then Newton-Raphson (~10 iter)
3. Gamma CDF via regularized incomplete gamma — series or continued fraction (~100 terms)
4. Inverse normal CDF — rational approximation (Abramowitz & Stegun)

All operations are f64-safe and have no inter-cell dependencies.

### Tolerance Architecture

`MC_ET0_PROPAGATION` uses wider tolerances (abs=0.15, rel=0.08) than deterministic
algorithms because stochastic methods with different RNG implementations produce
statistically equivalent — not bit-identical — distributions. The tolerance was
calibrated by comparing Python and Rust MC outputs across multiple scenarios.

### NaN/JSON Convention

Python `float('nan')` is serialized as JSON `null` (via a `sanitize_nan` helper)
because `serde_json` rejects NaN literals. SPI produces NaN for insufficient data
windows (e.g., SPI-12 for the first 11 months). In Rust, these are `f64::NAN`;
in benchmark JSON, they are `null`.

---

## §3 What We Learned (Relevant to Evolution)

### Stochastic validation requires property-based testing

Exact numerical match between Python and Rust MC outputs is not meaningful because
the RNG implementations differ. Instead, we validate:
- Statistical properties (mean within confidence interval, std dev within bounds)
- Convergence behavior (std dev decreases as N increases)
- Boundary behavior (zero uncertainty → deterministic, high uncertainty → wide spread)
- Determinism (same seed → same result within a single implementation)

This pattern applies to all stochastic GPU shaders across the ecosystem.

### Gamma function numerical stability

The regularized incomplete gamma function requires switching between series expansion
(x < a+1) and continued fraction (x ≥ a+1) for numerical stability. The continued
fraction uses Lentz's method with modified convergence criteria. Using `mul_add` for
fused multiply-add improves both accuracy and satisfies `clippy::suboptimal_flops`.

### `clippy::many_single_char_names` in numerical algorithms

Continued fraction algorithms (gamma_cf, Lentz's method) use conventional variable
names (a, b, c, d, h) from numerical recipes. We allow this lint locally rather than
renaming to less recognizable names — the single-character names ARE the standard
notation in this domain.

---

## §4 Cross-Spring Impact

| Spring | Impact |
|--------|--------|
| **groundSpring** | SPI drought index complements groundSpring's uncertainty toolkit. The gamma MLE + incomplete gamma infrastructure could be shared upstream for other distribution fitting needs. |
| **wetSpring** | Drought stress (SPI < -1) directly affects microbial community composition — connects to baseCamp Paper 06 (no-till Anderson). SPI time series could drive wetSpring's ecological transition detection. |
| **neuralSpring** | Bootstrap/jackknife CI are standard UQ methods already used in ML validation. airSpring's Python baselines provide additional cross-validation targets. |

---

## §5 Verification Commands

```bash
cd airSpring/barracuda

# New validation binaries
cargo run --release --bin validate_mc_et0
cargo run --release --bin validate_bootstrap_jackknife
cargo run --release --bin validate_drought_index

# Full quality gates
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --lib    # 854 tests
cargo test --test determinism  # 5 tests
```

---

*airSpring v0.7.4 — 81 experiments, 1284/1284 Python, 854 lib tests, 89 binaries.
MC ET₀ (26/26), Bootstrap/Jackknife (20/20), SPI drought (20/20). All green.*
