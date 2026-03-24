<!--
SPDX-License-Identifier: CC-BY-SA-4.0
https://creativecommons.org/licenses/by-sa/4.0/
-->

# healthSpring V42 — Deep Debt Resolution: toadStool/barraCuda Absorption Request

**Date:** 2026-03-23
**From:** healthSpring V42
**To:** barraCuda / toadStool / coralReef teams
**Session:** V42 deep debt resolution + audit remediation sprint

## Executive Summary

healthSpring V42 completes a comprehensive deep debt resolution sprint. All 83 experiments now use ValidationHarness (83/83), all 86 workspace members inherit uniform clippy pedantic+nursery lints, and 6 GPU ops are live (3 Tier A upstream, 3 Tier B health-domain). This handoff requests absorption of patterns and primitives proven in healthSpring into the upstream stack.

## What Changed in V42

### Code Quality

- 83 experiment Cargo.toml files now inherit `[lints] workspace = true` (uniform clippy pedantic+nursery+unwrap_used+expect_used)
- validation.rs metric functions (rmse, mae, nse, index_of_agreement) evolved from assert_eq!/panic to Result<f64, LengthMismatch>
- exp064 and exp065 migrated to ValidationHarness (was custom check macro / demo)
- exp055 `.expect()` evolved to `let Some(...) else { exit(1) }` pattern
- GPU coverage exclusion removed from CI — all code counts toward 90% gate
- Hardcoded "biomeOS.sock" evolved to named constant DEFAULT_ORCHESTRATOR_SOCKET

### Tolerance Centralization

- 8 new named constants added to tolerances.rs
- exp050, exp090, exp109 inline literals migrated to centralized constants
- cross_validate.py now imports from control/tolerances.py (single source of truth)

### GPU Dispatch Documentation

- gpu/dispatch/mod.rs now documents the three-path dispatch semantics
- gpu/ode_systems.rs documents MM WGSL migration status vs codegen

## Absorption Requests for barraCuda

### P0: TensorSession API

healthSpring's fused pipeline (`gpu/fused.rs`) uses local WGSL for all 6 ops in a single-encoder pattern. barraCuda's `TensorSession` is the intended replacement. When TensorSession ships, healthSpring can:

- Remove all 6 local WGSL shaders
- Remove fused.rs entirely
- Converge all three dispatch paths to upstream

### P1: Validation Metric Functions

healthSpring's `rmse`, `mae`, `nse`, `r_squared`, `index_of_agreement` (now returning Result) are candidates for `barracuda::stats` or a new `barracuda::validation` module. These are used across multiple springs for baseline comparison.

### P2: ODE System Codegen

Three OdeSystem implementations (MichaelisMentenOde, OralOneCompartmentOde, TwoCompartmentOde) are proven and tested. The `BatchedOdeRK4::generate_shader()` codegen path works. Consider absorbing the health-domain ODE definitions into barraCuda's ODE registry.

### P3: Tolerance Registry Pattern

The centralized `tolerances.rs` pattern (named constants with doc comments, linked to a TOLERANCE_REGISTRY.md spec) has been adopted by groundSpring, neuralSpring, and healthSpring. Consider a `barracuda::validation::tolerances` module or ecosystem guidance doc.

## Absorption Requests for toadStool

### Tier B Dispatch Convergence

`GpuContext::execute` uses barraCuda for all 6 ops. `execute_gpu` (stateless) only uses barraCuda for Tier A (3 ops), falling through to local WGSL for Tier B. When toadStool's dispatch layer supports health-domain ops natively, both paths can converge.

### Sovereign Dispatch Expansion

`gpu/sovereign.rs` currently supports only HillSweep via CoralReefDevice. The remaining 5 ops need sovereign dispatch support.

## Current healthSpring GPU Surface

| Op | WGSL Shader | barraCuda Op | Tier |
|----|-------------|-------------|------|
| HillSweep | hill_dose_response_f64.wgsl | HillFunctionF64 | A |
| PopulationPkBatch | population_pk_f64.wgsl | PopulationPkF64 | A |
| DiversityBatch | diversity_f64.wgsl | DiversityFusionGpu | A |
| MichaelisMentenBatch | michaelis_menten_batch_f64.wgsl | MichaelisMentenBatchGpu | B |
| ScfaBatch | scfa_batch_f64.wgsl | ScfaBatchGpu | B |
| BeatClassifyBatch | beat_classify_batch_f64.wgsl | BeatClassifyGpu | B |

## Quality State

| Metric | Value |
|--------|-------|
| Tests | 863 |
| Experiments | 83/83 ValidationHarness |
| Clippy | pedantic+nursery, zero warnings |
| Coverage gate | 90% line (llvm-cov) |
| unsafe blocks | 0 (workspace forbid) |
| #[allow()] | 0 |
| barraCuda pin | v0.3.7 (rev c04d848) |
| Local WGSL | 6 (validation copies, pending TensorSession) |

---
*Part of ecoPrimals — sovereign computing for science.*
