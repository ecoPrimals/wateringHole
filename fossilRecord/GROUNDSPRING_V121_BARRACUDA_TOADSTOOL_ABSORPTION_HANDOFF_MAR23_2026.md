# groundSpring V121 → barraCuda / toadStool Absorption Handoff

**Date**: March 23, 2026
**From**: groundSpring team
**To**: barraCuda + toadStool maintainers

## Purpose

This handoff identifies patterns, APIs, and shaders from groundSpring V121
that the barraCuda/toadStool team should consider absorbing, plus upstream
issues blocking groundSpring's GPU evolution.

---

## P0: Upstream Compilation Issue

**barraCuda does not compile without the `gpu` feature.** The `validation.rs`
module references a `rel_tolerance` field in `Check` that was added in a GPU
path but not gated. This blocks `cargo clippy --workspace --all-features` in
any consumer that enables `barracuda` but not `barracuda-gpu`.

```
error[E0063]: missing field `rel_tolerance` in initializer of `Check`
  --> barracuda/src/validation.rs:85
```

**Fix**: Either gate the `rel_tolerance` field behind `#[cfg(feature = "gpu")]`
or add a default value / `Option<f64>` wrapper.

---

## barraCuda Usage in groundSpring V121

### Delegation Inventory (274 call sites across 56 modules)

| Domain | Modules | Key Delegations |
|--------|---------|-----------------|
| **Stats** | `stats/agreement/*`, `metrics`, `correlation`, `regression`, `distributions` | `SumReduceF64`, `VarianceReduceF64`, `FusedMapReduceF64`, Pearson/Spearman GPU, linear/quadratic regression |
| **Spectral** | `spectral_recon`, `lanczos`, `band_structure`, `almost_mathieu` | GEMM, Cholesky, CSR SpMV, FFT, eigenvalues |
| **ODE/Stochastic** | `bistable`, `multisignal`, `gillespie`, `drift` | `BatchedOdeRK4F64`, `GillespieGpu`, `WrightFisherGpu` |
| **Optimization** | `freeze_out/*` | `LbfgsConfig`, `BatchNelderMeadConfig`, `grid_search_3d` |
| **FAO-56** | `fao56/*` | `BatchedElementwiseF64`, hydrology GPU pipeline, Monte Carlo WGSL |
| **Ecology** | `rare_biosphere`, `rarefaction` | `BatchedMultinomialGpu` |
| **Anderson** | `anderson/*`, `tissue_anderson`, `transport` | Lyapunov GPU, disorder sweeps, 2D/3D extensions |
| **ESN** | `esn/*` | ESN v2 train/predict |
| **WDM** | `wdm` | trapz, autocorrelation WGSL |

### Evolution State

| API | groundSpring Usage | Status |
|-----|-------------------|--------|
| `DeviceCapabilities` | Adopted in V120 (`gpu.rs`) | ✅ Current |
| `GpuDriverProfile` | Fully removed | ✅ Complete |
| `PrecisionRoutingAdvice` | Active in `gpu.rs` | ✅ Current |
| `BatchedOdeRK4F64` | Active in `bistable.rs` | ✅ Current |
| `normalize_method()` | Implemented locally in `dispatch/` | ⬆ Candidate for upstream |

---

## Shaders for Upstream Absorption

### `metalForge/shaders/`

| Shader | Purpose | Absorption Priority |
|--------|---------|-------------------|
| `anderson_lyapunov.wgsl` | f64 Anderson Lyapunov γ per-realization | **High** — well-tested, aligns with `barracuda::anderson` |
| `anderson_lyapunov_f32.wgsl` | f32 variant for precision comparison | **High** — same |

These are self-contained validation shaders with documented CPU reference
functions. They should live in `barracuda/shaders/validation/` or similar.

### WGSL Operations Referenced (not yet local shaders)

These are `barracuda::` operations that groundSpring calls via feature-gated
delegations. They represent the full barraCuda WGSL surface used by groundSpring:

- `spmv_csr_f64.wgsl` — Lanczos spectral
- `grid_search_3d_f64.wgsl` — Seismic inversion, freeze-out
- `mc_et0_propagate.wgsl` — FAO-56 Monte Carlo
- `hargreaves_batch_f64.wgsl` — FAO-56 batch ET₀
- `kimura_fixation_f64.wgsl` — Drift/selection
- `esn_reservoir_update_f64.wgsl` — ESN regime classification
- `autocorrelation_f64.wgsl` — WDM Green-Kubo
- `jackknife_mean_f64.wgsl` — Jackknife variance

---

## Patterns Worth Absorbing into barraCuda

### 1. `normalize_method()` for RPC dispatch
groundSpring's dispatcher now strips `groundspring.` and `barracuda.` prefixes.
This should be an ecosystem-standard utility in barraCuda's dispatch layer.

### 2. `NdjsonSink` for validation output
Machine-readable NDJSON output for CI pipelines. The `barracuda::validation`
module should consider absorbing this pattern for its own validation harness.

### 3. `IpcError::is_recoverable()` classification
Typed error recovery — Connect/Transport are transient; Remote/Discovery are
permanent. Already standard in wetSpring/healthSpring; should be in barraCuda IPC.

### 4. `ValidationHarness` with `check_relative` / `check_abs_or_rel`
Relative tolerance comparison and combined abs-or-rel checks. The existing
barraCuda `validation.rs` has simpler checks; these patterns handle more
floating-point edge cases.

### 5. Workspace lint hardening
`clippy::unwrap_used` + `clippy::expect_used` denied at workspace level.
Test modules use `#[expect(clippy::unwrap_used, reason = "...")]`. This is
the ecosystem standard going forward.

---

## Patterns Worth Absorbing into toadStool

### 1. 5-tier socket discovery
groundSpring now implements the full biomeOS V266 discovery chain including
`socket-registry.json`. toadStool's device discovery should support this
registry format for hardware capability advertisements.

### 2. `capability_registry.toml` (MCP manifest)
groundSpring publishes a TOML manifest of its 16 measurement tools for
Squirrel/MCP integration. toadStool should publish its compute/hardware
capabilities in the same format.

### 3. Provenance trio lifecycle
`run_lifecycle()` wraps the full session: create → store → commit → attribute,
with graceful degradation. toadStool compute jobs should hook into this for
provenance tracking of GPU dispatch outcomes.

---

## Coordination Requests

1. **Fix `rel_tolerance` compile error** (P0 — blocks `--all-features` CI)
2. **Absorb `anderson_lyapunov` shaders** into barraCuda shader library
3. **Coordinate wgpu 28 → 29 upgrade** (groundSpring MSRV now 1.87, matching wgpu 29)
4. **Propagate `normalize_method()`** to barraCuda dispatch layer
5. **Adopt `capability_registry.toml`** format for toadStool tool manifest
