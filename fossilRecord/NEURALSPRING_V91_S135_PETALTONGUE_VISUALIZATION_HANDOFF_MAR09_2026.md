# neuralSpring V91 S135 — petalTongue Visualization Evolution Handoff

**Date**: March 9, 2026
**From**: neuralSpring (Session 135)
**To**: BarraCUDA, ToadStool, petalTongue, coralReef teams
**License**: AGPL-3.0-or-later
**Covers**: Visualization evolution, DataChannel expansion, live streaming, TrainingVisualizer

---

## Executive Summary

neuralSpring S135 completes the petalTongue visualization evolution plan:
7 new domain scenario builders, all 8 DataChannel types now exercised,
live training dashboard, and TrainingVisualizer for real-time spectral
diagnostics. 56/56 petalTongue validation checks. Zero clippy warnings.

This handoff documents:
1. What neuralSpring now produces for petalTongue
2. What BarraCUDA/ToadStool should know about visualization data flows
3. Absorption opportunities for the petalTongue team
4. Learnings relevant to cross-spring visualization evolution

---

## Part 1: New Domain Scenario Builders

7 new builders in `src/visualization/scenarios/`, each calling real
neuralSpring computation (not synthetic data):

| File | Domain | DataChannel Types Used |
|------|--------|-----------------------|
| `hmm.rs` | HMM phylogenetics (016-018) | **Heatmap**, TimeSeries, Bar, Gauge |
| `game_theory.rs` | Evolutionary game theory (019-021) | **Heatmap**, TimeSeries, Gauge |
| `wdm.rs` | Warm Dense Matter (nW-01..05) | Scatter3D, TimeSeries, Gauge |
| `glucose.rs` | Blood glucose prediction (026) | TimeSeries, **Distribution**, Gauge, Bar |
| `immunological.rs` | Immunological Anderson (nS-06) | Spectrum, **Distribution**, TimeSeries, Gauge |
| `population.rs` | Meta-population + pangenome (024-025) | **Heatmap**, Bar, Scatter3D, Gauge |
| `loss_landscape.rs` | Loss landscape analysis (nS-03) | Spectrum, **FieldMap**, Gauge |

**Bold** = first use of that DataChannel type in neuralSpring.

Total: 12 scenario builders (5 existing + 7 new), all 8 DataChannel types exercised.

---

## Part 2: TrainingVisualizer — Live Spectral Streaming

`TrainingVisualizer` in `src/training_monitor.rs` wraps `StreamSession` and pushes per-epoch:

| Binding ID | Type | Content |
|------------|------|---------|
| `epoch-vs-ipr` | TimeSeries append | Mean IPR per epoch |
| `epoch-vs-bandwidth` | TimeSeries append | Spectral bandwidth per epoch |
| `epoch-vs-entropy` | TimeSeries append | Spectral entropy per epoch |
| `epoch-vs-lsr` | TimeSeries append | Level spacing ratio per epoch |
| `attention-state` | Gauge set | 0=Green, 1=Yellow, 2=Red |
| `current-ipr` | Gauge set | Current epoch mean IPR |
| `current-bandwidth` | Gauge set | Current bandwidth |
| `condition-number` | Gauge set | Current condition number |

This enables live visualization of neural network training health via spectral
diagnostics — the central neuralSpring thesis made visual.

---

## Part 3: For BarraCUDA Team

### Currently Used BarraCUDA APIs in Visualization Paths

The scenario builders call real neuralSpring computation which internally uses:

- `barracuda::linalg::eigh_f64` — Hessian eigenvalues (loss_landscape scenario)
- `barracuda::stats::{mean, variance}` — statistical summaries
- `barracuda::nn::SimpleMlp` — WDM transport surrogate predictions
- `barracuda::nautilus::DriftMonitor` — training drift detection (TrainingVisualizer)

### Absorption Opportunities

1. **DataChannel serialization**: The `DataChannel` enum and its 8 variants are
   defined in neuralSpring's `visualization/types.rs`. As more springs adopt
   petalTongue, consider whether `DataChannel` should move to BarraCUDA or a
   shared crate (currently each spring defines its own compatible types).

2. **Spectral diagnostics as BarraCUDA primitive**: The `WeightSpectralResult`
   (bandwidth, IPR, entropy, LSR, condition number, phase) is a neuralSpring
   type. The underlying `eigh_f64` + IPR + LSR computation could become a
   `barracuda::spectral::analyze_weight_matrix()` primitive.

3. **Training monitor pattern**: The Green/Yellow/Red FSM with spectral triggers
   is a general pattern. If other springs need training-aware monitoring,
   consider absorbing the FSM into `barracuda::nautilus`.

---

## Part 4: For ToadStool Team

### Live Dashboard Binary

`neuralspring_live_dashboard` demonstrates the full pipeline:
GPU computation → BarraCUDA eigensolve → spectral analysis → petalTongue render

This binary discovers petalTongue via `PetalTonguePushClient::discover()` and
falls back to headless mode. ToadStool's orchestration layer should be aware
that springs may now produce continuous visualization streams in addition to
one-shot scenario renders.

### Pipeline DAG Integration

The `full_study()` combiner produces a 12-track graph with 9 cross-domain edges.
This maps naturally to ToadStool's `PipelineGraph` (Kahn's topological sort).
The visualization layer is the user-facing projection of compute pipeline state.

---

## Part 5: For petalTongue Team

### All 8 DataChannel Types Now Exercised

neuralSpring exercises every DataChannel variant with real domain data:

| Type | Example Source |
|------|---------------|
| TimeSeries | CGM trace, PK decay, cooperation frequency |
| Spectrum | Hessian eigenvalues, cytokine barrier heights |
| Gauge | R², condition number, Nash distance, attention state |
| Bar | Viterbi state counts, horizon comparison, gene partition |
| Scatter3D | WDM phase space, population geography |
| Heatmap | FST matrix, transition matrix, payoff matrix |
| Distribution | Prediction errors, dose-response |
| FieldMap | 2D Rosenbrock loss surface |

### Streaming Protocol

`TrainingVisualizer` uses `visualization.render.stream` operations:
- `append` for TimeSeries (x,y pairs)
- `set_value` for Gauge (scalar)

Epoch rate: configurable via `INTERVAL_MS` env var (default 50ms = 20 Hz).
Backpressure: monitored via `StreamSession::backpressure_active()` (>10% error rate).

### scripts/visualize.sh

New convenience script following healthSpring pattern:
- `./scripts/visualize.sh` — dump 13 scenario JSONs
- `./scripts/visualize.sh --live` — start live training dashboard
- `./scripts/visualize.sh --render` — dump + launch petalTongue

---

## Part 6: Learnings for Cross-Spring Evolution

1. **Helper constructors reduce boilerplate**: `heatmap()`, `distribution()`,
   `fieldmap()` constructors (6-7 args each) dramatically simplify scenario
   building. Recommend all springs adopt similar helpers.

2. **Scenario builders should call real computation**: Synthetic data in
   scenarios is a code smell. Every neuralSpring scenario calls actual domain
   functions (HMM forward, replicator dynamics, landscape analysis, etc.).

3. **Live streaming needs the FSM**: Without attention state (Green/Yellow/Red),
   live dashboards are just animated time series. The FSM gives scientists
   actionable signals — "this is going wrong" vs "this is fine."

4. **12-track combiner pattern**: `full_study()` merges N independent studies
   with position offsets and cross-domain edges. This is the standard pattern
   for producing a single "complete view" of a spring's science.

---

## Validation

```
56/56 petalTongue PASS (validate_petaltongue_scenarios)
966/966 lib tests PASS
0 clippy warnings (pedantic+nursery)
0 fmt diff
```

## Files Changed

- **New** (9): 7 scenario builders + `neuralspring_live_dashboard.rs` + `scripts/visualize.sh`
- **Modified** (6): `scenarios/mod.rs`, `training_monitor.rs`, `dump_neuralspring_scenarios.rs`, `visualization/mod.rs`, `validate_petaltongue_scenarios.rs`, root docs
