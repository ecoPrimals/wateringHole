<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# healthSpring V41 → toadStool / barraCuda Evolution Handoff

**Date**: 2026-03-23
**From**: healthSpring V41
**To**: toadStool team, barraCuda team, coralReef team
**License**: AGPL-3.0-or-later
**Pins**: barraCuda v0.3.7 (rev c04d848), toadStool S163+, coralReef Phase 10+
**Supersedes**: `HEALTHSPRING_V40_TOADSTOOL_BARRACUDA_EVOLUTION_HANDOFF_MAR22_2026.md`

---

## Executive Summary

healthSpring V41 is a deep debt resolution sprint: workspace-level lint
consolidation, library `println!` evolved to `tracing`, hardcoded primal names
evolved to capability-based discovery with env-driven fallback, ODE codegen
wired to GPU dispatch, proptest extended to numerical properties, tolerance
registry synced, CI evolved to validate all experiment binaries. 855 tests,
zero clippy, zero unsafe, zero `#[allow]`.

---

## Part 1: V41 Changes Relevant to toadStool / barraCuda

### Workspace-Level Lint Consolidation

```toml
[workspace.lints.rust]
unsafe_code = "forbid"
missing_docs = "warn"

[workspace.lints.clippy]
all = "deny"
pedantic = "deny"
nursery = "deny"
unwrap_used = "deny"
expect_used = "deny"
```

All 3 library crates (`ecoPrimal`, `metalForge/forge`, `toadstool`) inherit via
`[lints] workspace = true`. Crate-level `#![forbid(unsafe_code)]` and
`#![deny(clippy::*)]` removed — single source of truth. `#[expect()]` with
`reason` used in test modules for `.unwrap()`.

**toadStool/barraCuda takeaway**: Adopt `[workspace.lints]` pattern for
workspace-wide lint governance. `unwrap_used = "deny"` catches accidental
panics in library code while `#[expect(reason)]` documents intentional test
usage.

### Library `println!` → `tracing`

All `println!`/`print!` in `ecoPrimal/src/provenance/mod.rs` evolved to
`tracing::info!` with structured fields. `eprintln!` in `validation.rs` evolved
to `tracing::error!`. Auto-initializing `tracing_subscriber` in
`ValidationHarness::new()` ensures all 83 experiment binaries get structured
output without per-binary changes.

**toadStool/barraCuda takeaway**: If toadStool or barraCuda still use
`println!` in library code, evolve to `tracing`. The auto-init pattern in
`ValidationHarness` avoids N-binary subscriber setup.

### ODE Codegen Wired to GPU Dispatch

`codegen_shader_for_op()` in `ecoPrimal/src/gpu/mod.rs` now generates WGSL via
`BatchedOdeRK4::<MichaelisMentenOde>::generate_shader()` for
`GpuOp::MichaelisMentenBatch`. This provides a barraCuda-generated alternative
to the hand-written `michaelis_menten_batch_f64.wgsl`.

**barraCuda takeaway**: The codegen path is wired and tested. Next steps:
1. Wire `OralOneCompartmentOde` and `TwoCompartmentOde` codegen (implementations exist in `gpu/ode_systems.rs`)
2. Validate codegen shader output matches hand-written shader numerically
3. Consider codegen-first workflow where hand-written shaders become the fallback

### Hardcoded Primal Names → Capability-Based Discovery

| File | Old | New |
|------|-----|-----|
| `ipc/tower_atomic.rs` | `DEFAULT_CRYPTO_PREFIX = "beardog"` | `crypto_socket_prefix()` reads `BIOMEOS_CRYPTO_PREFIX` env |
| `ipc/tower_atomic.rs` | `DEFAULT_DISCOVERY_PREFIX = "songbird"` | `discovery_socket_prefix()` reads `BIOMEOS_DISCOVERY_PREFIX` env |
| `visualization/ipc_push/client.rs` | `DEFAULT_VIZ_PREFIX = "petaltongue"` | `viz_socket_prefix()` reads `BIOMEOS_VIZ_PREFIX` env |

**toadStool takeaway**: Any hardcoded primal names in toadStool should follow
this pattern — env var with sensible default, never compile-time coupling to
another primal's name.

### Proptest Numerical Properties

5 new property-based tests in `pkpd/dose_response.rs`:
- Hill function boundedness: `0 ≤ response ≤ emax`
- IC50 identity: `response(ec50) ≈ emax/2`
- Monotonicity: increasing concentration → increasing response
- EC value ordering: `ec10 < ec20 < ec50 < ec80 < ec90`
- Zero response at zero concentration

**barraCuda takeaway**: These properties test the `barracuda::stats::hill`
primitive indirectly. Consider adding equivalent proptests in barraCuda itself.

### Rustdoc Coverage Push

104 `///` doc comments added across `metalForge/forge/` and `toadstool/` public
APIs. `missing_docs = "warn"` surfaced 548 items — first pass covers all
public structs, enums, fields, functions, and constants in the two downstream
crates.

---

## Part 2: barraCuda Primitive Consumption (v0.3.7)

### GPU Ops (6 — All Live)

| healthSpring Op | barraCuda Op | Status |
|-----------------|-------------|--------|
| `HillSweep` | `ops::hill_f64::HillFunctionF64` | **LIVE** |
| `PopulationPkBatch` | `ops::population_pk_f64::PopulationPkF64` | **LIVE** |
| `DiversityBatch` | `ops::bio::diversity_fusion::DiversityFusionGpu` | **LIVE** |
| `MichaelisMentenBatch` | `ops::health::michaelis_menten_batch::MichaelisMentenBatchGpu` | **LIVE** |
| `ScfaBatch` | `ops::health::scfa_batch::ScfaBatchGpu` | **LIVE** |
| `BeatClassifyBatch` | `ops::health::beat_classify::BeatClassifyGpu` | **LIVE** |

### CPU Primitives (~25)

| Category | Primitives |
|----------|-----------|
| **rng** | `lcg_step`, `LCG_MULTIPLIER`, `state_to_f64`, `uniform_f64_sequence`, `normal_sample` |
| **stats** | `mean`, `hill`, `shannon_from_frequencies`, `simpson`, `chao1_classic`, `bray_curtis`, `pielou_evenness` |
| **stats::bootstrap** | `bootstrap_mean_ci`, `jackknife_mean_bias` |
| **stats::anderson** | `ipr`, `localization_length`, `level_spacing_ratio` |
| **stats::correlation** | `pearson_r`, `spearman_rank` |
| **stats::histogram** | `histogram_uniform` |
| **stats::spectral** | `spectral_density` |
| **numerical** | `OdeSystem`, `BatchedOdeRK4` (codegen + CPU integration) |
| **health** | `MichaelisMentenParams`, `OralOneCompartmentParams`, `mm_auc`, `scr_rate`, `antibiotic_perturbation` |
| **special** | `anderson_diagonalize` |
| **device** | `WgpuDevice`, `CoralReefDevice`, `BufferBinding`, `DispatchDescriptor`, `GpuBackend` |

### v0.3.7 Primitives Available but NOT YET Consumed

| Primitive | healthSpring Use Case | Priority |
|-----------|----------------------|----------|
| `KimuraGpu` | Mithridatism population genetics (fixation under selection) | **P1** |
| `JackknifeGpu` | NLME diagnostics confidence intervals (VPC, GOF) | **P1** |
| `DeviceClass` | Vendor-agnostic GPU selection in metalForge/forge layer | **P2** |
| `mc_et0_gpu` | Monte Carlo pattern for VPC GPU promotion | **P2** |
| `normalize_method()` | IPC bare name alignment | **P2** |
| `tensor.create`/`tensor.matmul` | Future NLME matrix operations | **P3** |

---

## Part 3: What toadStool Should Absorb

### Pipeline Patterns from healthSpring V41

| Pattern | Description | toadStool Relevance |
|---------|------------|-------------------|
| **Workspace `[lints]`** | Single-source lint governance, inherited by all crates | Adopt for toadStool workspace |
| **Auto-init tracing** | `ValidationHarness` sets up `tracing_subscriber` once | Pipeline execution logging |
| **Env-driven discovery** | `BIOMEOS_*_PREFIX` env vars for primal sockets | toadStool compute dispatch config |
| **ODE codegen** | `BatchedOdeRK4::generate_shader()` wired to `GpuOp` | toadStool stage codegen pathway |
| **Proptest numerical** | Hill monotonicity, boundedness, EC ordering | Stage output validation |

### GPU Promotion Candidates for toadStool Pipeline

| Local Function | File | GPU Pattern | Priority |
|----------------|------|-------------|----------|
| `cross_reactivity_matrix` | `discovery/affinity_landscape.rs` | Batched Hill sweep over N×M | **P1** |
| `mechanistic_cell_fitness` | `simulation.rs` | Batch per-pathway Hill product | **P1** |
| `ecosystem_simulate` | `simulation.rs` | ODE batch (Lotka-Volterra) via `BatchedOdeRK4` | **P2** |
| `biphasic_dose_response` | `toxicology/mod.rs` | Element-wise dose sweep | **P2** |
| `systemic_burden_score` | `toxicology/mod.rs` | FusedMapReduceF64 | **P2** |
| `toxicity_ipr` | `toxicology/mod.rs` | Anderson IPR specialization | **P3** |

---

## Part 4: What barraCuda Should Absorb

### New Primitive Requests

1. **`BatchedGradientGpu`** (P0) — FOCE per-subject gradient parallelization.
   `pkpd/nlme/solver.rs::theta_gradient_step()` computes per-subject central
   differences sequentially. Each subject's gradient is independent. Estimated
   10-50× speedup for N>100 subjects.

2. **`HormesisSweepGpu`** (P1) — Biphasic dose-response curve batched over dose
   vectors. `toxicology::biphasic_dose_response` is element-wise, ideal for GPU.

3. **`CausalChainBatchGpu`** (P2) — Multi-pathway Hill product with damage
   accumulation. `simulation::mechanistic_cell_fitness` chains 4 pathway
   activations. Element-wise over dose vectors.

### ODE System Implementations Ready for Upstream

healthSpring has 3 `OdeSystem` trait implementations in `gpu/ode_systems.rs`:
- `MichaelisMentenOde` — capacity-limited PK elimination
- `OralOneCompartmentOde` — first-order absorption + elimination
- `TwoCompartmentOde` — bi-exponential distribution + elimination

These generate valid WGSL via `BatchedOdeRK4::generate_shader()`. barraCuda could
absorb these as canonical health-domain ODE systems in `barracuda::health::ode`.

---

## Part 5: Quality Snapshot

| Metric | V40 | V41 |
|--------|-----|-----|
| Tests | 848 | 855 |
| Clippy warnings | 0 | 0 |
| `#[allow]` in library | 0 | 0 |
| `.unwrap()` in library | 0 | 0 |
| `unsafe` blocks | 0 | 0 |
| Lint governance | per-crate | workspace `[lints]` |
| Library println | ~4 sites | 0 (all `tracing`) |
| Hardcoded primal names | 3 | 0 (env-driven) |
| ODE codegen wired | 0 ops | 1 op (MM batch) |
| barraCuda pin | v0.3.7 | v0.3.7 |

---

## Part 6: Reproduction

```bash
cd healthSpring
cargo test --workspace              # 855 tests, 0 failures
cargo clippy --workspace            # 0 non-doc warnings (548 missing_docs warns)
cargo fmt --check --all             # 0 diffs
```

---

*Part of [ecoPrimals](https://github.com/syntheticChemistry) — sovereign computing for science.*
