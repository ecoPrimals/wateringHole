# airSpring V0.7.5 — Upstream Rewire Cross-Primal Handoff

SPDX-License-Identifier: AGPL-3.0-or-later
**Date**: March 8, 2026
**From**: airSpring
**To**: barraCuda / toadStool / coralReef teams
**Spring Version**: airSpring v0.7.5 (`airspring-barracuda` crate)

---

## Summary

airSpring v0.7.5 synced to barraCuda HEAD (`a898dee`), toadStool S130+, coralReef
Phase 10 Iteration 10. Applied Write→Absorb→Lean to `eco::drought_index`: removed
55 lines of local `regularized_gamma_p`/`gamma_series`/`gamma_cf` and delegated to
upstream `barracuda::special::gamma::regularized_gamma_p`. All 854 lib tests and
20/20 drought index validation checks pass.

## Upstream Pin

| Component | Version | Commit |
|-----------|---------|--------|
| barraCuda | 0.3.3 (unreleased HEAD) | `a898dee` |
| toadStool | S130+ | `bfe7977b` |
| coralReef | Phase 10 Iteration 10 | `d29a734` |

## What Changed

- **`eco::drought_index` leaned**: Local reimplementation of `regularized_gamma_p`
  (Numerical Recipes series/continued-fraction, 55 lines) replaced with upstream
  `barracuda::special::gamma::regularized_gamma_p`. The upstream version adds proper
  `Result<f64>` error handling.
- **Already upstream (from v0.7.4)**: `barracuda::stats::normal::norm_ppf`,
  `barracuda::special::gamma::ln_gamma`.
- **Documented 9 new upstream capabilities** for future wiring.

## New Upstream Capabilities Available

| Capability | barraCuda Module | airSpring Use Case |
|------------|------------------|--------------------|
| `regularized_gamma_q(a, x)` | `special::gamma` | Gamma survival function |
| `digamma(x)` | `special::gamma` + WGSL | Fisher info for gamma MLE |
| `beta(a, b)` / `ln_beta(a, b)` | `special::gamma` + WGSL | Beta distribution (soil texture) |
| `BatchedOdeRK45F64` | `ops::rk45_adaptive` | Adaptive Richards solver on GPU |
| `mean_variance_to_buffer()` | `ops::variance_f64_wgsl` | Zero-readback Welford chain |
| `AutocorrelationF64` | `ops::autocorrelation_f64_wgsl` | ET₀ temporal analysis |
| R² on `CorrelationResult` | `ops::correlation_f64_wgsl` | GPU-side R² |

## toadStool Note

toadStool S130+ has airSpring V071 absorbed. Key deltas to V075:
- 81 experiments (was 72), 854 lib tests, 89 binaries
- `eco::drought_index` is a new consumer of `special::gamma`
- `local_dispatch` and `local_elementwise_f64.wgsl` retired since v0.7.2

## coralReef Note

coralReef Phase 10 corpus still references `local_elementwise_f64.wgsl` from
airSpring. This shader was retired in v0.7.2 — all 6 ops now use upstream
`batched_elementwise_f64.wgsl`. Recommend updating corpus reference.

## Quality Gates

| Check | Result |
|-------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --all-targets -- -D warnings` | PASS |
| `cargo test --lib` | 854/854 PASS |
| `validate_drought_index` | 20/20 PASS |
