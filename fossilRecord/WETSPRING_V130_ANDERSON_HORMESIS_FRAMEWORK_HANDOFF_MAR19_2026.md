# wetSpring V130 Handoff — Anderson Hormesis Framework

**Date:** 2026-03-19
**From:** wetSpring V130
**To:** barraCuda team, toadStool team, healthSpring team, ecosystem
**License:** AGPL-3.0-or-later
**Supersedes:** WETSPRING_V129_DEEP_DEBT_EVOLUTION_HANDOFF_MAR18_2026.md

---

## Executive Summary

wetSpring V130 introduces the Anderson Hormesis framework: biphasic dose-response
modeled through the Anderson metal-insulator transition, low-affinity binding
landscape for colonization resistance, and "computation as experiment preprocessor"
methodology. Two new bio modules with 31 tests, 4 tolerance constants, 3 experiment
protocols, cross-spring joint experiment with healthSpring.

1,579+ tests, 109 bio modules, 379 experiments, 218 tolerances, zero local WGSL,
zero unsafe, zero clippy warnings.

---

## New Modules

### `bio::hormesis` (14 tests)
Biphasic dose-response: `R(d) = (1 + A × hill(d, K_stim, n_s)) × (1 − hill(d, K_inh, n_i))`.
Functions: `response`, `evaluate`, `sweep`, `find_peak`, `hormetic_zone`,
`dose_to_disorder`, `predict_hormetic_zone_from_wc`.

### `bio::binding_landscape` (17 tests)
Colonization resistance on disordered epithelial lattice. Composite binding from
weak interactions. IPR and localization length for toxicity delocalization.
Functions: `fractional_occupancy`, `composite_binding`, `selectivity_index`,
`colonization_resistance`, `resistance_surface_sweep`, `binding_ipr`,
`localization_length`.

### `bio::kinetics` (centralized)
Monod and Haldane growth kinetics extracted from 13 validation binaries.

---

## Absorption Candidates for barraCuda

| Priority | Module | Target | Cross-Spring Users |
|----------|--------|--------|--------------------|
| P1 | `hormesis::response` | `barracuda::bio::hormesis` | groundSpring, healthSpring, airSpring |
| P1 | `hormesis::dose_to_disorder` | `barracuda::bio::hormesis` | All Anderson springs |
| P1 | `binding_ipr` | `barracuda::spectral::ipr` | healthSpring, wetSpring |
| P1 | `localization_length` | `barracuda::spectral::localization_length` | healthSpring, wetSpring |
| P1 | `kinetics::monod` | `barracuda::bio::kinetics` | wetSpring, groundSpring |
| P1 | `kinetics::haldane` | `barracuda::bio::kinetics` | wetSpring, groundSpring |
| P2 | Hormesis GPU sweep | `FusedMapReduceF64` | Real-time dose-response |
| P2 | Resistance surface GPU | `BatchedOdeRK4` | 3D parameter exploration |
| P3 | Binding IPR batch GPU | New `BindingIprF64` | High-throughput screening |

---

## Cross-Spring Joint Experiments

- **Exp379 × healthSpring exp097/098:** Colonization resistance surface
- **Planned:** Pesticide hormesis (groundSpring × airSpring)
- **Planned:** Immune calibration (healthSpring)
- **Planned:** Metabolic hormesis, mithridatism

---

## Ecosystem Learning: Computation as Experiment Preprocessor

V130 introduces Phase 4 methodology: Anderson phase diagram predicts WHERE the
hormetic zone is before experiments are designed. All springs can adopt this for
their domain-specific phase transitions. See `whitePaper/STUDY.md` §4.8 and
`whitePaper/METHODOLOGY.md` §3b.

---

## Metrics Delta

| Metric | V129 | V130 |
|--------|------|------|
| Tests | 1,548 | 1,579 |
| Bio modules | 107 | 109 |
| Experiments | 376 | 379 |
| Tolerances | 214 | 218 |
