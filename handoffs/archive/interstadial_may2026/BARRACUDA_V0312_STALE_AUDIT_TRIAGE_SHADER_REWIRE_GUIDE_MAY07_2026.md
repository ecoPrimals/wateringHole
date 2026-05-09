# barraCuda v0.3.12 — Stale Audit Triage + Shader Rewire Guide

**Date**: 2026-05-07
**Context**: primalSpring Phase 59 audit (projectNUCLEUS sovereignty testing) referenced two barraCuda items — both previously resolved. This handoff clarifies status and provides rewire paths for downstream consumers.

---

## 1. `stats.entropy` — RESOLVED (Sprint 50, May 1 2026)

**PG-61 / PG-47 is closed.** `stats.entropy(data) -> f64` is live and routable over JSON-RPC.

### Wire call

```json
{"jsonrpc":"2.0","method":"stats.entropy","params":{"data":[0.25,0.25,0.25,0.25]},"id":1}
```

Response: `{"jsonrpc":"2.0","result":{"result":1.3862943611198906},"id":1}`

### Implementation

- `stats.entropy` dispatches to `stats.shannon` (Shannon entropy over frequency distribution)
- Accepts `data` (array of counts or frequencies) + optional `base` (default: natural log)
- Registered in `REGISTERED_METHODS` and `capabilities.list`
- Test: `stats_entropy_alias_dispatches_to_shannon`

### For hotSpring / `tictactoe_cell.toml`

The `stats.entropy` call referenced in `tictactoe_cell.toml` will work against barraCuda at `tcp://ironGate:9740` or `unix://$BIOMEOS_SOCKET_DIR/math.sock` without modification.

---

## 2. Shader Absorption — RESOLVED (Sprint 43, Apr 15 2026)

**18/18 barraCuda-targeted shader candidates are upstream.** Springs can rewire from local `path`/`git` deps to IPC calls.

### Rewire paths (Level 2 → Level 5)

| Spring shader | barraCuda IPC method | Notes |
|---|---|---|
| `softmax_f64.wgsl` | `activation.softmax` | JSON-RPC, inline data |
| `gelu_f64.wgsl` | `activation.gelu` | JSON-RPC, inline data |
| `chi_squared_f64.wgsl` | `stats.chi_squared` | JSON-RPC, inline data |
| `linear_regression.wgsl` | `stats.fit_linear` | JSON-RPC, inline data |
| `matrix_correlation.wgsl` | `stats.pearson` / `stats.correlation` | JSON-RPC, inline data |
| `batch_ipr.wgsl` | GPU dispatch via `compute.dispatch` | Requires tensor handle |
| `rk4_parallel.wgsl` | GPU dispatch via `compute.dispatch` | Requires tensor handle |
| `rk45_adaptive.wgsl` | GPU dispatch via `compute.dispatch` | Requires tensor handle |
| `kl_divergence_f64.wgsl` | GPU dispatch via `compute.dispatch` | Requires tensor handle |
| `sigmoid_f64.wgsl` | `math.sigmoid` | JSON-RPC, inline data |
| `hmm_backward_log.wgsl` | GPU dispatch via `compute.dispatch` | Bio domain |
| `hmm_viterbi.wgsl` | GPU dispatch via `compute.dispatch` | Bio domain |
| `wright_fisher_step.wgsl` | GPU dispatch via `compute.dispatch` | Bio domain |
| `pairwise_hamming.wgsl` | GPU dispatch via `compute.dispatch` | Bio domain |
| `pairwise_jaccard.wgsl` | GPU dispatch via `compute.dispatch` | Bio domain |
| `sdpa_scores_f64.wgsl` | `ml.attention` | JSON-RPC, inline data |
| `layer_norm_f64.wgsl` | GPU dispatch via `compute.dispatch` | Norm domain |
| `outer_product_mean_f64.wgsl` | GPU dispatch via `compute.dispatch` | AlphaFold2 domain |

### Two rewire tiers

**Tier A — JSON-RPC inline (no GPU handle needed):**
Springs can call `stats.entropy`, `activation.softmax`, `activation.gelu`, `math.sigmoid`, `stats.chi_squared`, `stats.fit_linear`, `stats.pearson`, `ml.attention` directly over JSON-RPC with inline `data` arrays. No tensor creation required. Suitable for small-to-medium payloads.

**Tier B — GPU tensor pipeline (large payloads):**
For large data (>10K elements), springs should use the tensor pipeline:
1. `tensor.create` → get handle
2. `tensor.batch.submit` with ops → GPU execution
3. Read result

### Not candidates (stay in neuralSpring)

`ipa_scores_f64`, `triangle_attention_f64`, `triangle_mul_*`, `backbone_update_f64`, `torsion_angles_f64`, `msa_*_attention_scores_f64` — protein folding / MSA-specific, not general math primitives.

### coralReef boundary

Shader *compilation* (`shader.compile.wgsl`, `shader.compile.spirv`) is coralReef's domain. barraCuda provides the *runtime dispatch* via `compute.dispatch` and domain-specific JSON-RPC methods. Springs that need custom shader compilation route through coralReef; springs that need standard math/science ops route through barraCuda.

---

## primalSpring gap registry status

| Gap ID | Description | Status |
|--------|-------------|--------|
| PG-47 | `stats.entropy` method-not-found | **CLOSED** Sprint 50 |
| PG-61 | `stats.entropy` missing for hotSpring QCD | **CLOSED** Sprint 50 (= PG-47) |
| GAP-11 | 18 JSON-RPC surface gaps | **14/18 CLOSED** (Sprints 44–50). Remaining 4: ESN v2, nautilus, batched ODE, SimpleMlp — stateful/session APIs, deferred |

---

## Connection info

- **TCP**: `ironGate:9740`
- **UDS**: `$BIOMEOS_SOCKET_DIR/math.sock` (or `math-{family_id}.sock`)
- **Discovery**: Songbird `ipc.resolve` (Tier 1), UDS filesystem (Tier 3), manifest (Tier 4), TCP probe (Tier 5)
- **Methods**: 59 registered (`capabilities.list` for full enumeration)
