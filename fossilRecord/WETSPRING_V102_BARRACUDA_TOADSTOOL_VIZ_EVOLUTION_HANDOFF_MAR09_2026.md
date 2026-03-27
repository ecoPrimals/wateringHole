# wetSpring V102 → barraCuda / toadStool Visualization Evolution Handoff

**Date:** March 9, 2026
**From:** wetSpring V102 (ecoPrimals life science Spring)
**To:** barraCuda team, toadStool team
**License:** AGPL-3.0-or-later

---

## Purpose

wetSpring V102 completes full-domain petalTongue coverage. This handoff
documents what the barraCuda and toadStool teams should absorb, evolve,
and support based on what wetSpring learned building 41 scenario builders
across every compute domain.

---

## Part 1: What wetSpring Learned About barraCuda Usage

### Primitive Consumption Patterns

wetSpring now exercises barraCuda primitives through 41 visualization
scenario builders, each calling live math (no mocks). The patterns that
emerged:

**Pattern A: Compute → Single Channel** (most common)
```rust
let result = diversity::shannon(&counts);
node.data_channels.push(gauge("shannon", "Shannon H'", result, ...));
```
Simple 1:1 mapping. 27 of 41 builders use this exclusively.

**Pattern B: Compute → Multi-Channel Decomposition** (composite)
```rust
let result = bistable::run_bistable(&y0, 50.0, 0.01, &params);
for (i, name) in var_names.iter().enumerate() {
    let y_vals = extract_variable(&result, i);
    node.data_channels.push(timeseries(..., &result.t, &y_vals));
}
node.data_channels.push(gauge("steady_state", final_biofilm, ...));
```
ODE systems decompose `OdeResult` into per-variable time series + summary
gauges. All 5 ODE builders use this pattern.

**Pattern C: Compute → Cross-Domain Edge** (composite scenarios)
```rust
let (eco, eco_edges) = ecology_scenario(&samples, &labels);
let (qs, qs_edges) = full_qs_scenario();
edges.push(edge("diversity", "phage_defense", "ecology → QS"));
```
Composite scenarios merge multiple domain tracks with data-flow edges.

### API Observations for barraCuda Team

1. **`OdeResult` is the universal ODE interface.** All 5 ODE scenario builders
   extract variables the same way: `result.y[step * result.n_vars + var_idx]`.
   This is correct but verbose. A `variable_trajectory(var_idx) -> Vec<f64>`
   convenience method on `OdeResult` would reduce boilerplate across all springs.

2. **`DecisionTree::from_arrays` and `RandomForest::from_trees` return `Result`.**
   Scenario builders must handle these gracefully. The error path is "return
   empty scenario" which is correct for visualization but means validation
   must explicitly check node/channel counts.

3. **`KmerCounts::to_histogram()` returns `Vec<u32>`.** The Spectrum channel
   needs `Vec<f64>`. Every consumer must cast. Consider adding
   `to_histogram_f64()` or accepting the cast as intentional.

4. **`UnifracDistanceMatrix::condensed` uses condensed upper-triangle format.**
   Visualization needs full square matrices. All heatmap consumers must expand
   or petalTongue must understand condensed format. We use condensed directly
   and let petalTongue handle expansion.

5. **dN/dS `omega` is `Option<f64>`.** When dS is zero, omega is None (infinite
   selection pressure). Visualization caps at 10.0. Document this convention.

### Primitives wetSpring Needs Next

| Priority | Primitive | Use Case | Current Workaround |
|---|---|---|---|
| P1 | `OdeResult::variable_trajectory()` | ODE scenario decomposition | Manual flat-array indexing |
| P2 | `KmerCounts::to_histogram_f64()` | Spectrum channel | Manual `f64::from` cast |
| P3 | Spatial ecology primitives (kriging, Richards PDE) | FieldMap channel | Channel type defined, no compute yet |

---

## Part 2: What toadStool Should Absorb

### Visualization Infrastructure

wetSpring's `barracuda/src/visualization/` module is 100% schema-only integration
(JSON, no compile-time petalTongue dependency). toadStool does not need to absorb
this — it stays in the spring. But toadStool should be aware of the patterns:

1. **Scenario builders are pure functions.** `fn foo_scenario(data) -> (EcologyScenario, Vec<ScenarioEdge>)`.
   No side effects, fully testable, serializable to JSON.

2. **StreamSession with backpressure.** wetSpring implements healthSpring's pattern:
   500ms timeout, 200ms cooldown, 3 slow pushes before entering cooldown.
   toadStool's compute dispatch should be aware that visualization is a downstream
   consumer that may apply backpressure.

3. **Domain-specific push helpers.** `push_diversity_update()`, `push_ode_step()`,
   `push_pipeline_progress()` encapsulate the JSON-RPC protocol for common patterns.
   If toadStool ever adds native visualization dispatch, these helpers show the API.

### Compute Patterns for GPU Promotion

The 28 new scenario builders exercise compute patterns that inform GPU shader priorities:

| Pattern | Compute | GPU Status | Action |
|---|---|---|---|
| Felsenstein + bootstrap | `felsenstein`, `bootstrap` | `FelsensteinGpu` exists | No action |
| Pairwise dN/dS | `dnds` | `DnDsBatchF64` exists | No action |
| UniFrac matrix | `unifrac` | `UniFracPropagateF64` exists | No action |
| DTL reconciliation | `reconciliation` | `reconciliation_gpu` exists | No action |
| Strict molecular clock | `molecular_clock` | `molecular_clock_gpu` exists | No action |
| Phylogenetic placement | `placement` | No GPU yet | **Candidate** — batch placement scan is embarrassingly parallel |
| K-mer histogram | `kmer` | `KmerHistogramF64` exists | No action |
| ESN train + predict | `esn` | `BioEsn` (GPU) exists | No action |

**One GPU gap identified:** `placement::batch_placement` (placing many queries onto
a reference tree) is embarrassingly parallel and would benefit from GPU acceleration.
The CPU implementation iterates edges sequentially per query.

---

## Part 3: Lessons Learned

1. **healthSpring patterns work.** Track-based composition (`full_study()` →
   `full_ecology_scenario()`), UiConfig, BackpressureConfig, domain push helpers
   — all adapted cleanly from healthSpring to wetSpring. The pattern is proven
   across two springs and should be the standard for all springs.

2. **`push_replace` was silently broken.** The bug (building payload but assigning
   to `_payload`) passed all tests because tests only checked that the session
   accepted the call, not that data reached the socket. Lesson: streaming tests
   should verify frame_count increments AND that the underlying transport is called.

3. **Spectrum channel was dead code for 2 versions.** Defined in V100, unused until
   V102's `kmer_spectrum_scenario`. Springs should not define channel types
   without at least one scenario builder using them.

4. **Composite scenarios are the most valuable visualization.** Scientists don't
   want individual diversity plots — they want the full pipeline view. The
   `full_ecology_scenario` (scientist dashboard) combining all tracks is the
   most impactful single scenario.

5. **Zero mocks in visualization.** Every scenario builder calls live barraCuda
   math with synthetic but realistic data. This means visualization tests also
   validate the compute — a free integration test layer.
