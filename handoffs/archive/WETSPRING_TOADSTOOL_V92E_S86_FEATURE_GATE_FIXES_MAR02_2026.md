# wetSpring → ToadStool: S86 Feature-Gate Fixes + Rewire

**Date:** March 2, 2026
**From:** wetSpring V92E
**To:** ToadStool/BarraCUDA team
**Priority:** High — 3 feature-gate bugs need absorbing

---

## Critical: Feature-Gate Bugs Found During S86 Rewire

wetSpring rewired from ToadStool S79 (`f97fc2ae`) to S86 (`2fee1969`). The
non-GPU build path broke because pure CPU modules were incorrectly gated behind
`#[cfg(feature = "gpu")]`.

### Bug 1: `spectral` module fully GPU-gated

**File:** `crates/barracuda/src/lib.rs`
**Problem:** `pub mod spectral` gated behind `#[cfg(feature = "gpu")]` despite
containing pure CPU code (Anderson localization, Lanczos, Hofstadter, tridiag,
level spacing statistics).
**Fix:** Ungated the module. Gated only `spectral::batch_ipr` (which uses wgpu).

### Bug 2: `linalg::graph` module GPU-gated

**File:** `crates/barracuda/src/linalg/mod.rs`
**Problem:** `pub mod graph` and its re-exports gated behind GPU despite being
pure CPU (graph_laplacian, belief_propagation_chain, effective_rank, etc.).
**Fix:** Ungated module and re-exports.

### Bug 3: `sample` module fully GPU-gated

**File:** `crates/barracuda/src/lib.rs` + `src/sample/mod.rs`
**Problem:** Entire `sample` module GPU-gated because `mod.rs` has `LazyLock`
statics referencing `crate::shaders::precision`. But most samplers (Boltzmann,
LHS, Sobol, maximin) are pure CPU.
**Fix:** Ungated the module in `lib.rs`. In `mod.rs`, gated WGSL statics and
GPU-dependent submodules (`direct`, `sparsity`). CPU samplers always available.

### Bug 4: `stats::hydrology` GPU type re-exports

**File:** `crates/barracuda/src/stats/mod.rs`
**Problem:** `Fao56BaseInputs`, `Fao56Uncertainties`, `SeasonalOutput` re-exported
without `#[cfg(feature = "gpu")]` but only exist in `hydrology::gpu`.
**Fix:** Moved to the `#[cfg(feature = "gpu")]` re-export block.

### Recommendation

Audit all `#[cfg(feature = "gpu")]` gates. Pattern: if a module has mixed
CPU/GPU code, split into submodules (like hydrology did in S84) or use
per-item gating. The WGSL `LazyLock` pattern should consistently use
`#[cfg(feature = "gpu")]`.

## Validation

All fixes verified:
- `cargo check` (CPU, no features): CLEAN
- `cargo check --all-features` (GPU): CLEAN
- `cargo clippy -- -W clippy::pedantic`: 0 warnings
- `cargo test`: 1,044 wetSpring tests PASS
- Exp296: 64/64 cross-spring validation checks PASS

## Primitives Now Consumed: 144

wetSpring now consumes 144 ToadStool primitives (up from 93), including all new
S80-S86 ComputeDispatch ops, spectral analysis, graph theory, sampling, and
hydrology ET₀ methods.
