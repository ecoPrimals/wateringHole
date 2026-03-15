# wetSpring V102 → petalTongue V2 Full-Domain Visualization Handoff

**Date:** March 9, 2026
**From:** wetSpring V102 (ecoPrimals life science Spring)
**To:** petalTongue team, barraCuda team, toadStool team
**License:** AGPL-3.0-or-later
**Status:** 140/140 visualization validation checks PASS, 1,047 lib tests PASS

---

## Executive Summary

wetSpring V102 completes the petalTongue V2 integration: every compute domain
now has at least one scenario builder producing `DataChannel`-typed data that
petalTongue can render. The integration follows healthSpring's mature patterns
(UiConfig, BackpressureConfig, track-based composition, domain push helpers)
and adds the first `FieldMap` channel and first real `Spectrum` channel user.

**Key numbers:**
- 41 scenario builders (was 13 in V101, 6 in V100)
- 8 DataChannel types (added `FieldMap`)
- 4 composite full-pipeline scenarios
- 3 domain-specific streaming push helpers
- `wetspring_dashboard` binary — "anyone with a GPU" scientist UX
- `push_replace` bug fixed — payload was being discarded
- 140/140 validation checks (validate_visualization_v2)

---

## What Changed

### Phase 1: Infrastructure

| Item | File | Change |
|------|------|--------|
| `push_replace` fix | `stream.rs` | Was building JSON but assigning to `_payload` — now delegates to `client.push_replace()` |
| `UiConfig` + `ShowPanels` | `types.rs` | Domain-themed rendering config (theme, zoom, panel visibility) |
| `push_render_with_config()` | `ipc_push.rs` | Sends domain + UiConfig alongside scenario |
| `push_replace()` on client | `ipc_push.rs` | Full channel replacement via JSON-RPC |
| `FieldMap` channel | `types.rs` | Spatial 2D grid data (grid_x, grid_y, row-major values) |
| `BackpressureConfig` | `stream.rs` | 500ms timeout, 200ms cooldown, 3 slow pushes |
| Domain push helpers | `stream.rs` | `push_diversity_update`, `push_ode_step`, `push_pipeline_progress` |

### Phase 2: Scenario Builders (28 new)

| Track | File | Builders |
|---|---|---|
| Phylogenetics | `phylogenetics.rs` | felsenstein, placement, unifrac, dnds, molecular_clock, reconciliation |
| ODE Systems | `ode_systems.rs` | phage_defense, bistable, cooperation, multi_signal, capacitor |
| 16S Pipeline | `pipeline.rs` | quality, dada2, taxonomy, pipeline_overview |
| Population Genomics | `popgen.rs` | snp, population_genomics, kmer_spectrum |
| LC-MS/PFAS | `lcms.rs` | spectral_match, tolerance_search, pfas_overview |
| ML Models | `ml_models.rs` | decision_tree, random_forest, esn |

### Phase 3: Composite Scenarios

| Composite | Nodes | Pattern |
|---|---|---|
| `full_16s_scenario` | quality → DADA2 → taxonomy → diversity | 4+ nodes, data-flow edges |
| `full_pfas_scenario` | spectral match → tolerance → classification | 3+ nodes |
| `full_qs_scenario` | all 5 ODE models linked | 5 nodes, QS cascade edges |
| `full_ecology_scenario` | all tracks merged | 10+ nodes — the scientist dashboard |

### Phase 4: User Empowerment

- `wetspring_dashboard` binary: builds all scenarios, dumps JSON, auto-pushes to petalTongue
- `scripts/visualize.sh`: build + dump + optional petalTongue launch
- `scripts/live_dashboard.sh`: discovers socket, streams live

---

## What petalTongue Should Know

1. **FieldMap channel**: wetSpring defines it but no scenario builder uses it yet.
   Spatial ecology (Richards PDE, kriging, ET0 maps) will be the first users.
   petalTongue should support `fieldmap` as a heatmap with geographic projection.

2. **Spectrum channel**: now has a real user (`kmer_spectrum_scenario`). Previously
   defined but unused. petalTongue should render it as a frequency-amplitude plot.

3. **UiConfig**: wetSpring sends `ecology-dark` theme by default. petalTongue
   should recognize ecology/metagenomics domain themes and apply Tufte principles.

4. **BackpressureConfig**: wetSpring respects the healthSpring pattern (500ms/200ms/3).
   petalTongue should handle slow consumers gracefully.

5. **41 scenarios**: All produce valid JSON. `wetspring_dashboard` dumps them to
   `sandbox/scenarios/`. petalTongue can load them standalone with
   `petaltongue --scenario sandbox/scenarios/`.

---

## What barraCuda / toadStool Should Know

All 41 scenario builders call live barraCuda math — no mocks. The computation
patterns exercised include:

- Felsenstein pruning + bootstrap (phylogenetics)
- Pairwise dN/dS with Jukes-Cantor correction (selection pressure)
- UniFrac distance matrix (beta diversity)
- DTL reconciliation (gene-species tree)
- 5 independent ODE systems via `OdeResult` (RK4)
- DADA2 denoising (amplicon error model)
- K-mer counting + histogram (population genomics)
- Cosine spectral similarity (LC-MS)
- Decision tree + random forest inference (ML)
- ESN reservoir computing (echo state network)

### Unwired Primitives Still Needed

These barraCuda primitives would enable richer visualization:

| Primitive | Use Case |
|---|---|
| `LogsumexpWgsl` | HMM forward log-alpha streaming |
| `SparseGemmF64` | Drug-gene pathway visualization |
| `TranseScoreF64` | Knowledge graph embedding scatter |

---

## Validation

`validate_visualization_v2`: 140/140 checks covering:
- All 28 new scenario builders (node counts, channel counts, JSON serialization)
- All 4 composite scenarios
- FieldMap and UiConfig serialization
- StreamSession lifecycle, backpressure, domain helpers
- Spectrum channel presence in kmer_spectrum_scenario
