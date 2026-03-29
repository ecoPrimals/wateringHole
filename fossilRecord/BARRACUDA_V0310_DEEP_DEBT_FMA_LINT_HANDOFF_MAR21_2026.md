<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# barraCuda v0.3.10 — Deep Debt Solutions, FMA Evolution & Lint Promotion

**Date**: 2026-03-21
**Sprint**: 19–20
**Version**: 0.3.10
**Scope**: Deep debt solutions, idiomatic Rust evolution, FMA precision, lint promotion, iterator evolution
**Previous**: BARRACUDA_V038_ECOSYSTEM_ABSORPTION_HANDOFF_MAR21_2026

---

## Summary

Two sprints of deep debt evolution. Sprint 19: comprehensive codebase audit, RPC tolerance
registry evolution, cast safety, 6 domain feature gates, typed error evolution. Sprint 20:
625 suboptimal_flops sites evolved to mul_add() for FMA precision, 4 clippy lints promoted
from allow to warn, 45 needless_range_loop sites evolved to idiomatic iterators. 232 files
changed across Sprint 20 alone. All quality gates green.

## Changes

### Sprint 19: Deep Debt Solutions & Idiomatic Rust Evolution (v0.3.9)

- **RPC `tolerances_get` evolved to centralized tolerance registry** — Previously hardcoded
  (abs_tol, rel_tol) pairs; now delegates to `barracuda::tolerances::by_name()` and `tier()`
  for runtime introspection. Legacy aliases mapped to tiered constants.
- **Cast safety evolution in `TensorSession`** — All `usize as u32` casts replaced with
  `barracuda::cast::usize_as_u32()` returning `CastOverflow` on overflow. New
  `AttentionDims::as_u32()` helper.
- **6 new domain feature gates** — `domain-fhe`, `domain-md`, `domain-lattice`,
  `domain-physics`, `domain-pharma`, `domain-genomics` (for `ops::bio`), `domain-fold`
  (for `ops::alphafold2`). All included in `domain-models` umbrella — default builds unchanged.
- **Typed errors in `FlatTree::validate()`** — From `Result<(), &'static str>` to
  `BarracudaError::InvalidInput`.
- **3 new tarpc tolerance tests**

### Sprint 20: FMA Evolution & Lint Promotion (v0.3.10)

- **625 `suboptimal_flops` sites → `mul_add()`** — All `a*b + c` patterns across library (415)
  and tests (210) evolved to `f64::mul_add()` / `f32::mul_add()` for hardware FMA precision
  (single rounding). Bessel functions, RK45/RK4 solvers, ODE integrators, normal distribution,
  Jacobi eigensolvers, Crank-Nicolson PDE, polynomial evaluations, MD observables all use FMA.
- **4 clippy lints promoted from `allow` to `warn`**:
  - `suboptimal_flops` (415 → 0)
  - `use_self` (332 → 0, all evolved to `Self`)
  - `tuple_array_conversions` (2 → 0, evolved to `<[T; N]>::from()`)
  - `needless_range_loop` (45 → 0, all evolved to idiomatic iterators)
- **45 `needless_range_loop` sites → idiomatic iterators** — Multi-array indexed loops
  refactored to `.zip()`, `.enumerate()`, `.iter_mut()` across QR, SVD, CSR, Cholesky,
  attention, ESN, Nautilus, Nelder-Mead, L-BFGS, Metropolis, conv2d, bootstrap.
- SVD rank-deficient test threshold relaxed `1e-10` → `1e-7` for FMA rounding path.

### Breaking (API) — Sprint 19 only

- **6 ops submodules now feature-gated** — `ops::fhe_*` requires `domain-fhe`, `ops::md`
  requires `domain-md`, etc. All included in `domain-models` umbrella (on by default).
- **`FlatTree::validate()` return type changed** — From `Result<(), &str>` to typed error.
- **`tolerances_get` RPC values changed** — Now sourced from centralized module.

Sprint 20 (v0.3.10) has **no breaking changes**.

## Quality Gates

- `cargo fmt --all --check` ✅
- `cargo clippy --all-targets -p barracuda -p barracuda-core` ✅ (zero warnings on lib+tests)
- `cargo test -p barracuda -p barracuda-core` ✅ (3,623+ pass, 0 fail)
- `#![forbid(unsafe_code)]` ✅
- Zero production `unwrap()` ✅
- Zero TODO/FIXME/HACK in `*.rs` ✅

## Codebase Health

- **Rust source files**: 1,085
- **WGSL shaders**: 806 (all with SPDX headers)
- **Tests**: 3,623+ lib + 130 core (0 failures)
- **Unsafe code**: Zero (`#![forbid(unsafe_code)]`)
- **Lint level**: pedantic + nursery + `suboptimal_flops` + `use_self` + `needless_range_loop` + `tuple_array_conversions` all `warn`
- **TODO/FIXME/HACK**: Zero
- **`.unwrap()` in production**: Zero
- **Files over 1000 LOC**: Zero
- **FMA policy**: All math uses `mul_add()` — `suboptimal_flops` enforced at `warn`

## Cross-Primal Pins

| Primal | Version/Session | Status |
|--------|-----------------|--------|
| toadStool | S163 | Dependency audit, zero-copy, code quality |
| coralReef | Phase 10 Iter 62 | Deep audit, coverage, hardcoding evolution |
| All springs | barraCuda v0.3.10 / wgpu 28 | Synced |

## Next Steps

- P1: DF64 end-to-end NVK hardware verification
- P1: coralReef sovereign compiler evolution
- P2: Coverage to 90% (requires f64-capable GPU hardware in CI)
- P2: `missing_const_for_fn` evolution (911 sites, pending Rust const fn stabilization)
- P3: Multi-GPU dispatch evolution
