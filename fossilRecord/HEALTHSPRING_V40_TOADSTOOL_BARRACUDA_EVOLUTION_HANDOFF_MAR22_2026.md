<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# healthSpring V40 → toadStool / barraCuda Evolution Handoff

**Date**: 2026-03-22
**From**: healthSpring V40
**To**: toadStool team, barraCuda team, coralReef team
**License**: AGPL-3.0-or-later
**Pins**: barraCuda v0.3.7 (rev c04d848), toadStool S163+, coralReef Phase 10+
**Supersedes**: `HEALTHSPRING_V39_TOXICOLOGY_SIMULATION_HORMESIS_HANDOFF_MAR19_2026.md`

---

## Executive Summary

healthSpring V40 is a cross-ecosystem absorption sprint: reviewed all 7 springs,
10+ primals, 49 wateringHole handoffs. Bumped barraCuda from v0.3.5 to v0.3.7.
Resolved module conflicts, extracted magic numbers, smart-refactored large files,
added 39 new tests (809→848). Zero clippy (pedantic+nursery), zero unsafe, zero
`.unwrap()` in library code, zero `#[allow]`.

---

## Part 1: barraCuda Primitive Consumption (v0.3.7)

### GPU Ops (6 — All Rewired)

| healthSpring Op | barraCuda Op | Tier | Status |
|-----------------|-------------|------|--------|
| `HillSweep` | `ops::hill_f64::HillFunctionF64` | A | **LIVE** |
| `PopulationPkBatch` | `ops::population_pk_f64::PopulationPkF64` | A | **LIVE** |
| `DiversityBatch` | `ops::bio::diversity_fusion::DiversityFusionGpu` | A | **LIVE** |
| `MichaelisMentenBatch` | `ops::health::michaelis_menten_batch::MichaelisMentenBatchGpu` | B | **LIVE** |
| `ScfaBatch` | `ops::health::scfa_batch::ScfaBatchGpu` | B | **LIVE** |
| `BeatClassifyBatch` | `ops::health::beat_classify::BeatClassifyGpu` | B | **LIVE** |

### CPU Primitives (~25)

| Category | Primitives |
|----------|-----------|
| **rng** | `lcg_step`, `LCG_MULTIPLIER`, `state_to_f64`, `uniform_f64_sequence`, `normal_sample` |
| **stats** | `mean`, `shannon_from_frequencies`, `simpson`, `chao1`, `pielou_evenness` |
| **stats::bootstrap** | `bootstrap_mean_ci`, `jackknife_mean_bias` |
| **stats::anderson** | `ipr`, `localization_length`, `level_spacing_ratio` |
| **stats::correlation** | `pearson_r`, `spearman_rank` |
| **stats::histogram** | `histogram_uniform` |
| **stats::spectral** | `spectral_density` |
| **numerical** | `OdeSystem`, `BatchedOdeRK4` |
| **health** | `MichaelisMentenParams`, `OralOneCompartmentParams` |

### v0.3.7 Primitives Available but NOT YET Consumed

| Primitive | Where in barraCuda | healthSpring Use Case | Priority |
|-----------|-------------------|----------------------|----------|
| `KimuraGpu` | `stats::evolution` | Mithridatism population genetics (fixation probability under selection) | **P1** |
| `JackknifeGpu` | `stats::jackknife` | NLME diagnostics confidence intervals (VPC, GOF) | **P1** |
| `DeviceClass` | `device` | Vendor-agnostic GPU selection in metalForge/forge layer | **P2** |
| `mc_et0_gpu` | `stats::hydrology` | Monte Carlo pattern for VPC GPU promotion | **P2** |
| `normalize_method()` | `ipc::methods` | IPC bare name alignment | **P2** |
| `tensor.create`/`tensor.matmul` | `ipc::methods` | Future NLME matrix operations | **P3** |

---

## Part 2: What toadStool Should Absorb

### Pipeline Patterns from healthSpring

| Pattern | Description | toadStool Relevance |
|---------|------------|-------------------|
| **NLME handler defaults** | Module-level `NLME_DEFAULT_THETA/OMEGA/SEED` constants eliminate repeated `vec![2.3, 4.4, 0.4]` in every handler | Pipeline stage config defaults |
| **Named tolerance constants** | All algorithm tuning (FOCE lr, SAEM MH scale, tissue cap) in centralized `tolerances.rs` | Stage-level tuning registry |
| **Semantic module split** | `provenance/mod.rs` (types+logic) vs `provenance/registry.rs` (data) | Pipeline stage metadata split |
| **Handler test coverage** | 22 new tests covering JSON-RPC dispatch surface | toadStool dispatch stage testing |

### GPU Promotion Candidates for toadStool Pipeline

| Local Function | File | GPU Pattern | toadStool Stage |
|----------------|------|-------------|-----------------|
| `cross_reactivity_matrix` | `discovery/affinity_landscape.rs` | Batched Hill sweep over N×M | `SiliconUnit::ShaderCore` |
| `mechanistic_cell_fitness` | `simulation.rs` | Batch per-pathway Hill product | `SiliconUnit::ShaderCore` |
| `ecosystem_simulate` | `simulation.rs` | ODE batch (Lotka-Volterra) | `SiliconUnit::ShaderCore` via `BatchedOdeRK4` |
| `biphasic_dose_response` | `toxicology/mod.rs` | Element-wise dose sweep | `SiliconUnit::ShaderCore` |
| `systemic_burden_score` | `toxicology/mod.rs` | FusedMapReduceF64 | `SiliconUnit::ShaderCore` + `Rop` (scatter-add) |
| `toxicity_ipr` | `toxicology/mod.rs` | Anderson IPR specialization | `SiliconUnit::ShaderCore` |

---

## Part 3: What barraCuda Should Absorb

### New Primitive Requests

1. **`BatchedGradientGpu`** (P0) — FOCE per-subject gradient parallelization. Currently
   computed sequentially in `pkpd/nlme/solver.rs::theta_gradient_step()` via central
   differences. Each subject's gradient is independent → embarrassingly parallel.
   Estimated 10-50× speedup for N>100 subjects.

2. **`HormesisSweepGpu`** (P1) — Biphasic dose-response curve batched over dose vectors.
   `toxicology::biphasic_dose_response` is a simple element-wise operation ideal for
   GPU. Used by `science.toxicology.biphasic_dose_response` IPC handler.

3. **`CausalChainBatchGpu`** (P2) — Multi-pathway Hill product with damage accumulation.
   `simulation::mechanistic_cell_fitness` chains 4 pathway activations with a damage
   term. Entire chain is element-wise over dose vectors.

### IPC Method Alignment

healthSpring uses these JSON-RPC method prefixes in production:

```
science.pkpd.*          (14 methods)
science.microbiome.*    (13 methods)
science.biosignal.*     (8 methods)
science.endocrine.*     (9 methods)
science.diagnostic.*    (11 methods)
science.toxicology.*    (3 methods)
science.simulation.*    (2 methods)
compute.*               (5 methods)
health.*                (2 methods)
data.*                  (3 methods)
lifecycle.*             (3 methods)
capability.*            (2 methods)
mcp.tools.list          (1 method)
primal.*                (3 methods)
```

All method strings are centralized in `bin/healthspring_primal/capabilities.rs` and
`ipc/dispatch/mod.rs`. They follow barraCuda's `normalize_method()` convention
(bare names without primal prefix).

---

## Part 4: Cross-Ecosystem Patterns Worth Propagating

### From healthSpring (propagate to other springs)

1. **`#[expect(reason)]` over `#[allow]`** — healthSpring has zero `#[allow]` in library
   code. Every suppression uses `#[expect]` with a `reason` string. Lint authorship.

2. **Handler test pattern** — Every dispatch handler function gets a smoke test:
   provide valid params → assert expected key in response. Catches deserialization
   regressions.

3. **MCP tool invariant tests** — `no_duplicate_tool_names()`,
   `all_schemas_are_valid_json_objects()`, `all_tools_have_semantic_names()`.

### From Other Springs (healthSpring will absorb next)

| Source | Pattern | Impact |
|--------|---------|--------|
| wetSpring V131 | Validator-fails-on-zero-checks | Prevents false-pass experiments |
| groundSpring V118 | `DefaultRng` for reproducibility | NLME SAEM reproducibility |
| neuralSpring V120 | `OnceLock` GPU device probe cache | Eliminate repeated probe overhead |
| toadStool S163 | Zero-copy `Arc<str>`, `Bytes` | IPC hot path optimization |
| biomeOS V254-260 | Sleep-free IPC test patterns | Test reliability |

---

## Part 5: Quality Snapshot

| Metric | V39 | V40 |
|--------|-----|-----|
| Tests | 809 | 848 |
| Clippy warnings | 0 | 0 |
| `#[allow]` in library | 1 | 0 |
| `.unwrap()` in library | 0 | 0 |
| `unsafe` blocks | 0 | 0 |
| Magic numbers in production | ~25 | ~8 |
| Files > 1000 lines | 1 | 0 |
| barraCuda pin | v0.3.5 | v0.3.7 |
| Production mocks | 0 | 0 |
| Module conflicts | 1 | 0 |

---

## Part 6: Reproduction

```bash
cd healthSpring
cargo test --workspace              # 848 tests, 0 failures
cargo clippy --workspace -- -W clippy::pedantic -W clippy::nursery  # 0 warnings
cargo check --all-features          # all feature gates compile
```

---

*Part of [ecoPrimals](https://github.com/syntheticChemistry) — sovereign computing for science.*
