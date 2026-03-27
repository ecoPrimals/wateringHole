# wetSpring V101 → petalTongue Visualization Evolution Handoff

**Date:** March 9, 2026
**From:** wetSpring V101
**To:** petalTongue, barraCuda, toadStool teams
**Status:** 78/78 PASS (Exp333: 44/44 + Exp334: 34/34)

---

## What Changed

### Schema Evolution

| Item | Description |
|------|-------------|
| `DataChannel::Spectrum` | 7th channel type: `frequencies: Vec<f64>`, `amplitudes: Vec<f64>` — for Anderson spectral, HRV power spectra, FFT outputs |
| `StreamSession` | Session lifecycle: open → push_initial_render → push_timeseries_append / push_gauge_update / push_replace → close |
| `VisualizationAnnouncement` | Songbird-compatible: 16 capabilities, 7 channel types, `supports_streaming: true` |

### New Scenario Builders (7)

| Builder | Domain | Channels |
|---------|--------|----------|
| `pangenome_scenario` | Pangenome analysis | Heatmap (presence/absence), Bar (core/accessory/unique), Gauge (Heap's α) |
| `hmm_scenario` | Hidden Markov Model | TimeSeries (forward log-α per state), Bar (Viterbi path), Heatmap (posterior probs) |
| `stochastic_scenario` | Gillespie SSA | TimeSeries (trajectory traces), Distribution (final-state), Gauge (mean±SD) |
| `similarity_scenario` | ANI pairwise | Heatmap (full ANI matrix), Distribution (off-diagonal values) |
| `rarefaction_scenario` | Rarefaction curves | TimeSeries (curves per sample), Gauge (observed vs Chao1) |
| `nmf_scenario` | NMF decomposition | Heatmap (W matrix), Heatmap (H matrix), Bar (top features per component) |
| `streaming_pipeline_scenario` | GPU pipeline stages | Bar (stage latencies), Gauge (progress/pass rates), multi-node graph |

### IPC Wiring

- `science.diversity` and `science.full_pipeline` gain `"visualization": true` parameter
- When set, auto-builds scenario from compute results and includes JSON in response
- Best-effort push to petalTongue socket (non-fatal on failure)

### Tooling

- `dump_wetspring_scenarios`: 13 scenarios (was 6), `--stream` flag for StreamSession demo

---

## Recommendations for petalTongue Team

1. **Spectrum renderer**: wetSpring now emits `channel_type: "spectrum"` with `frequencies` + `amplitudes` arrays. petalTongue should add a line/area chart renderer for this type (X=frequency, Y=amplitude).

2. **StreamSession protocol**: wetSpring uses `visualization.render.stream` with `append`, `set_value`, and `replace` operations. Confirm petalTongue handles these operation types.

3. **Songbird discovery**: wetSpring announces 16 `visualization.ecology.*` capabilities plus `visualization.metalforge.*`. petalTongue can use these to auto-discover what wetSpring can render.

4. **Domain theme**: wetSpring uses `domain: "ecology"` (and `"metagenomics"` for specific scenarios). petalTongue should apply ecology-themed color palettes for this domain.

## Recommendations for barraCuda Team

1. **NMF visualization**: wetSpring's `nmf_scenario` wraps `NmfResult` directly. If `NmfResult` gains additional fields (e.g., convergence info), the builder will automatically pick them up.

2. **FitResult evolution**: If `FitResult` gains new named accessors beyond `.slope()` / `.intercept()`, wetSpring builders will adopt them.

## Recommendations for toadStool Team

1. **Streaming pipeline**: The `streaming_pipeline_scenario` is currently CPU-only metadata. When `GpuPipelineSession` gains stage-level timing hooks, the builder should wire real latency data.

---

## Validation Summary

| Exp | Name | Checks |
|-----|------|:------:|
| 333 | Visualization Evolution | 44/44 |
| 334 | Science-to-Viz Pipeline | 34/34 |

All 1,096 barracuda + 203 forge library tests PASS. Zero clippy warnings.
