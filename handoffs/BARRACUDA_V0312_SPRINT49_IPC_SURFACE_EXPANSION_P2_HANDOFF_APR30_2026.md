# barraCuda v0.3.12 — Sprint 49 Handoff (IPC Surface Expansion Phase 2)

**Date**: April 30, 2026
**Sprint**: 49 (Phase 56c — IPC surface gap closure)
**Version**: 0.3.12
**Tests**: 272+ non-GPU pass, 26 BTSP compliance tests pass, 0 failures
**IPC Methods**: 56 registered (was 50)
**Quality Gates**: fmt ✓ clippy (pedantic+nursery) ✓ doc (zero warnings) ✓ deny ✓
**Supersedes**: `BARRACUDA_V0312_SPRINT48_BTSP_WIRE_CLOSURE_HANDOFF_APR29_2026.md`

---

## Context

primalSpring Phase 56c audit identified 18 barraCuda library entry points
without 1:1 JSON-RPC methods (from `PRIMAL_GAPS.md` GAP-11, originally
documented by neuralSpring V133). This sprint closes the highest-priority
subset and reconciles stale items.

## What Changed

### 6 New JSON-RPC Methods

| Method | Params | Returns | Library backing |
|--------|--------|---------|-----------------|
| `stats.shannon` | `counts` or `frequencies` (array) | `{ result: H', unit: "nats" }` | `barracuda::stats::shannon` / `shannon_from_frequencies` |
| `stats.covariance` | `x`, `y` (arrays) | `{ result: Cov(X,Y), convention: "sample" }` | `barracuda::stats::covariance` |
| `stats.spearman` | `x`, `y` (arrays) | `{ result: ρ }` | `barracuda::stats::spearman_correlation` |
| `stats.fit_linear` | `x`, `y` (arrays) | `{ slope, intercept, r_squared, rmse }` | `barracuda::stats::fit_linear` |
| `stats.empirical_spectral_density` | `eigenvalues` (array), `n_bins` (int) | `{ bin_centers, density, n_bins }` | `barracuda::stats::empirical_spectral_density` |
| `linalg.graph_laplacian` | `adjacency` (flat array), `n` (int) | `{ result: L matrix, n }` | `barracuda::linalg::graph_laplacian` |

### `linalg.eigenvalues` / `stats.eigh` Enhanced

Now returns both eigenvalues AND eigenvectors via Jacobi rotation accumulation:
- `{ eigenvalues: [...], eigenvectors: [[col0], [col1], ...], result: [...eigenvalues...] }`
- Backwards-compatible: `result` field still contains eigenvalues for existing consumers

### Gap Reconciliation (Phase 56c)

| Audit item | Status |
|------------|--------|
| 18 IPC surface gaps (GAP-11) | **10 resolved** (pearson, chi_squared, solve, mlp_forward from Sprint 45; shannon, covariance, spearman, fit_linear, spectral_density, graph_laplacian from Sprint 49). **8 remaining** (esn_v2::*, nautilus::*, belief_propagation_chain, numerical_hessian, boltzmann_sampling — all complex/deferred) |
| BufReader lifetime edge-case | **Stale** — resolved Sprint 43 (`6284469e`). Single-BufReader + `get_mut()` pattern. |
| 29 shader absorption candidates | **Stale** — resolved Sprint 43 (18/18 barraCuda-relevant confirmed). |
| Batched OdeRK45F64 (Richards PDE) | **Deferred** — airSpring-specific, low priority. |

## Zero Open Gaps (Phase 55/56/56c Scope)

All P0/P1 items from Phase 55, 56, and 56c are resolved or explicitly deferred
with documented rationale. Remaining GAP-11 items require either:
- Complex domain models (ESN, Nautilus exploration) → dedicated sprint
- Closure-over-IPC design (numerical_hessian) → architecture decision
- Niche use cases (boltzmann_sampling) → demand-driven

## For Downstream Springs

If your spring was blocked on any of these 6 new methods, they are now
available. Wire format is standard JSON-RPC 2.0 over the barraCuda Unix
socket (or TCP with `--port`).

---

<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
