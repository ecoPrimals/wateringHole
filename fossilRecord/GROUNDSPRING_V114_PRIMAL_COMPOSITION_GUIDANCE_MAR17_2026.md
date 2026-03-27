# groundSpring V114 — Primal Composition Guidance

**Date**: March 17, 2026
**From**: groundSpring V114
**To**: All primals, all springs, ecosystem architects
**Authority**: groundSpring niche.rs capability registry + dispatch.rs method table
**License**: AGPL-3.0-or-later

## Purpose

How to use groundSpring as a measurement primal — alone, in NUCLEUS atomic
combos, and in novel multi-primal compositions. Each primal publishes similar
guidance. This document focuses on what groundSpring offers and how other
primals and springs can leverage it.

groundSpring exposes **8 measurement capabilities** via JSON-RPC 2.0 over Unix
sockets. It delegates numerics to barraCuda (102 delegations), discovers
primals at runtime via capability routing, and falls back to sovereign local
computation when no NUCLEUS is available.

---

## 1. groundSpring Standalone

Any process on the host can call groundSpring directly over its socket.
No NUCLEUS required — groundSpring runs sovereign.

### Socket Discovery

```
1. $GROUNDSPRING_SOCKET              (explicit override)
2. $BIOMEOS_SOCKET_DIR/groundspring-${FAMILY_ID}.sock
3. $XDG_RUNTIME_DIR/biomeos/groundspring-${FAMILY_ID}.sock
4. /tmp/groundspring-${FAMILY_ID}.sock
```

### Available Methods

| Method | Purpose | Key Inputs |
|--------|---------|------------|
| `measurement.noise_decomposition` | Bias vs noise error partitioning | `observed[]`, `modeled[]` |
| `measurement.anderson_validation` | Anderson localization (Lyapunov exponent) | `n_sites`, `disorder`, `energy` |
| `measurement.uncertainty_budget` | Bootstrap + jackknife confidence intervals | `data[]`, `confidence`, `n_bootstrap` |
| `measurement.et0_propagation` | FAO-56 Penman-Monteith evapotranspiration | weather params, `latitude`, `day_of_year` |
| `measurement.regime_classification` | ESN eigenvalue regime detection | `eigenvalues[]`, `margin` |
| `measurement.spectral_features` | Tikhonov spectral reconstruction | `correlator[]`, `n_omega`, `regularization` |
| `measurement.parity_check` | CPU vs GPU numerical parity | `cpu_values[]`, `gpu_values[]`, `tolerance` |
| `measurement.freeze_out` | QCD freeze-out chi-squared grid fit | `observed[]`, `mu_b[]`, grid bounds |
| `health.check` | Full health with capabilities and uptime | — |
| `health.liveness` | Minimal alive signal | — |
| `health.readiness` | Ready to serve (capabilities wired) | — |
| `capability.list` | List registered capabilities | — |
| `lifecycle.status` | Version, family_id, uptime | — |

### Example: Direct Call

```json
{"jsonrpc":"2.0","method":"measurement.noise_decomposition","params":{"observed":[1.0,2.1,3.0],"modeled":[1.1,2.0,2.9]},"id":1}
```

### When to Use Standalone

- Quick measurement validation without NUCLEUS overhead
- CI pipelines that need deterministic validation
- Embedded in deploy graphs as a leaf node
- Any primal that needs measurement uncertainty quantification

---

## 2. groundSpring + Tower (BearDog + Songbird)

**Atomic**: Tower provides crypto identity and discovery.

### What This Unlocks

| Composition | How | Use Case |
|-------------|-----|----------|
| **Signed measurements** | groundSpring produces result → BearDog signs → Songbird announces | Tamper-evident measurement provenance for regulatory compliance |
| **Discoverable measurement service** | Songbird advertises `measurement.*` capabilities | Any primal on the mesh can find and call groundSpring without hardcoded paths |
| **Lineage-verified validation** | BearDog BLAKE3 lineage proof chains measurement → baseline → Python provenance | Full auditability from raw data to final validation verdict |
| **Encrypted measurement relay** | Songbird encrypted UDP + BearDog trust chain | Remote measurement validation across network boundaries |

### Novel Patterns

**Measurement attestation**: groundSpring validates → BearDog signs the
result with lineage proof → LoamSpine (if present) makes it immutable.
This creates an unforgeable measurement record suitable for regulatory
audit trails (EPA, FDA, EMA).

**Discovery-driven load balancing**: Multiple groundSpring instances
register via Songbird. biomeOS routes `measurement.*` calls to the
least-loaded instance. Horizontal scaling without configuration.

---

## 3. groundSpring + Node (Tower + ToadStool)

**Atomic**: Node adds GPU/NPU/CPU compute dispatch.

### What This Unlocks

| Composition | How | Use Case |
|-------------|-----|----------|
| **GPU-accelerated measurement** | ToadStool routes `compute.dispatch.submit` → barraCuda GPU shaders | 100x speedup for spectral reconstruction, Anderson localization, rarefaction |
| **Multi-GPU measurement pipelines** | ToadStool `shader.compile.wgsl.multi` + streaming progress | Large-scale Monte Carlo uncertainty budgets across GPU fleet |
| **Precision-routed computation** | ToadStool selects f64 vs f32 hardware | Correct precision tier for each measurement domain |
| **NPU regime classification** | ToadStool routes ESN inference to BrainChip AKD1000 | Ultra-low-latency regime detection at the edge |

### Novel Patterns

**Sovereign measurement pipeline**: coralReef compiles WGSL → ToadStool
dispatches to best available GPU → groundSpring validates result against
Python baseline → BearDog signs. Full sovereign stack, zero vendor lock-in.

**Cross-spring GPU sharing**: ToadStool manages a shared GPU pool.
groundSpring submits Anderson localization, hotSpring submits Yukawa MD,
neuralSpring submits surrogate training — all dispatched by ToadStool to
the same hardware without conflicts.

---

## 4. groundSpring + Nest (Tower + NestGate)

**Atomic**: Nest adds content-addressed storage.

### What This Unlocks

| Composition | How | Use Case |
|-------------|-----|----------|
| **Cached measurement results** | NestGate `storage.put` keyed by input hash | Expensive measurements computed once, retrieved by content hash |
| **Baseline storage** | Python baselines stored in NestGate with provenance metadata | Rerun validation against stored baselines without filesystem access |
| **Measurement data pipeline** | NestGate `data.ncbi_fetch`, `data.noaa_ghcnd`, `data.iris_events` | Pull public datasets, run measurements, store results — all via IPC |
| **Reproducibility archive** | Full experiment state (inputs, code version, results) stored immutably | Any measurement can be reproduced from its NestGate archive |

### Novel Patterns

**Content-addressed validation cache**: Hash(benchmark_json + code_version +
feature_flags) → NestGate key. If the result exists, skip re-validation.
If not, compute and store. Eliminates redundant CI work across springs.

**Data provenance chain**: NestGate fetches raw data (SRA accession,
Zenodo DOI) → groundSpring measures → sweetGrass attributes → LoamSpine
records. Full W3C PROV-O chain from public dataset to validated result.

---

## 5. groundSpring + Full NUCLEUS (Tower + Node + Nest + Squirrel)

**Atomic**: Full sovereign stack with AI coordination.

### What This Unlocks

| Composition | How | Use Case |
|-------------|-----|----------|
| **AI-guided measurement** | Squirrel selects measurement method based on data characteristics | Automatic method selection (e.g., jackknife vs bootstrap based on sample size) |
| **Adaptive validation** | Squirrel adjusts tolerance thresholds based on measurement history | Tighter tolerances as code matures, looser for exploratory |
| **Natural language measurement** | Squirrel MCP tools → groundSpring capabilities | "What's the noise decomposition for this dataset?" |
| **Cross-domain insight** | Squirrel correlates groundSpring measurements with healthSpring/wetSpring results | Emergent patterns across springs |

### Novel Patterns

**Measurement-driven experiment design**: Squirrel analyzes groundSpring's
uncertainty budget → identifies the largest error contributor → suggests
the next experiment to reduce uncertainty → dispatches via ToadStool →
validates via groundSpring. Closed-loop scientific method.

**Anomaly detection pipeline**: groundSpring's regime_classification on
streaming eigenvalue data → skunkBat monitors for unexpected regime
transitions → BearDog verifies lineage hasn't been tampered → Songbird
alerts the mesh. Real-time measurement anomaly detection.

---

## 6. groundSpring + Provenance Trio (rhizoCrypt + sweetGrass + LoamSpine)

### What This Unlocks

| Composition | How | Use Case |
|-------------|-----|----------|
| **Session tracking** | rhizoCrypt DAG tracks measurement session lifecycle | Every measurement has a session ID, parent/child relationships |
| **Attribution** | sweetGrass records who ran what measurement, on what data, with what code | Full W3C PROV-O attribution chain |
| **Immutable record** | LoamSpine commits measurement results to permanent ledger | Regulatory-grade immutable measurement record |

### Novel Patterns

**SCYBORG measurement provenance**: AGPL code (groundSpring) + ORC
attribution (sweetGrass) + CC-BY-SA data (public datasets) = complete
SCYBORG provenance chain for every measurement result.

**Experiment lineage DAG**: rhizoCrypt maintains a DAG of measurement
sessions. Each session links to its parent (parameter sweep → individual
measurement → sub-measurement). The full tree is dehydratable and
rehydratable for reproducibility.

---

## 7. Cross-Spring Composition Patterns

groundSpring's measurement capabilities compose with every other spring's
domain. The key: groundSpring provides **domain-agnostic measurement
primitives** (noise decomposition, uncertainty budget, parity check,
regime classification) that apply to any scientific domain.

### Spring → groundSpring Patterns

| Spring | What It Sends | groundSpring Method | What It Gets Back |
|--------|---------------|---------------------|-------------------|
| **hotSpring** | Lattice QCD correlator data | `measurement.spectral_features` | Spectral function, peak positions |
| **hotSpring** | Yukawa MD observed vs modeled | `measurement.noise_decomposition` | Bias/noise partition |
| **airSpring** | Weather station data | `measurement.et0_propagation` | ET₀ with uncertainty |
| **airSpring** | Soil parameter estimates | `measurement.uncertainty_budget` | Bootstrap CI for soil params |
| **wetSpring** | 16S diversity metrics | `measurement.noise_decomposition` | Sequencing noise vs biological signal |
| **wetSpring** | Rarefaction curves | `measurement.parity_check` | CPU/GPU parity for rarefaction |
| **neuralSpring** | Model predictions vs targets | `measurement.noise_decomposition` | Model bias vs variance |
| **neuralSpring** | GPU vs CPU inference | `measurement.parity_check` | Numerical parity verification |
| **healthSpring** | Clinical measurement data | `measurement.uncertainty_budget` | Measurement uncertainty for clinical reporting |
| **healthSpring** | PK/PD model fits | `measurement.freeze_out` | Parameter estimation with chi² |
| **ludoSpring** | Player behavior eigenvalues | `measurement.regime_classification` | Flow state vs boredom detection |
| **ludoSpring** | Procedural generation parity | `measurement.parity_check` | Determinism verification |

### groundSpring → Spring Patterns

groundSpring can also **consume** other springs' outputs for cross-domain
validation:

| Source | What groundSpring Gets | How It Uses It |
|--------|------------------------|----------------|
| hotSpring | Nuclear EOS tables | Validate against published baselines |
| airSpring | Multi-method ET₀ | Cross-validate Penman-Monteith implementations |
| wetSpring | Metagenomics pipelines | Validate rarefaction implementations |
| neuralSpring | Surrogate models | Use as fast forward models for spectral features |

### Novel Cross-Spring Combos

**Universal validation service**: Any spring calls
`measurement.parity_check` to verify CPU/GPU agreement.
`measurement.noise_decomposition` to quantify model quality.
`measurement.uncertainty_budget` for statistical rigor.
groundSpring becomes the **measurement backbone** of the ecosystem.

**Federated measurement**: Multiple springs contribute measurements to
a shared rhizoCrypt session. groundSpring aggregates, decomposes noise,
and sweetGrass attributes each contribution. The result is a
multi-domain measurement with full provenance from every contributor.

---

## 8. How Other Primals Can Leverage groundSpring

Each primal can use groundSpring without importing it. Discover via
`capability.call` or direct socket.

### For barraCuda

groundSpring is barraCuda's primary **validation consumer**. Every new
barraCuda op gets a groundSpring validation binary that runs
`measurement.parity_check` between CPU and GPU paths. The Write → Validate
→ Handoff → Absorb → Lean cycle depends on groundSpring proving parity.

### For ToadStool

groundSpring exercises `compute.dispatch.submit` with real scientific
workloads (Anderson localization, spectral reconstruction). ToadStool
uses groundSpring as a **benchmark primal** — if groundSpring's
measurements agree at 1e-12 tolerance, the dispatch is correct.

### For Squirrel

groundSpring's 8 measurement methods map directly to MCP tools.
Squirrel can offer natural-language measurement analysis:
"Analyze the noise in this dataset" → `measurement.noise_decomposition`.
"How confident are we in this estimate?" → `measurement.uncertainty_budget`.

### For skunkBat

groundSpring's `measurement.regime_classification` detects phase
transitions in eigenvalue spectra. skunkBat can use this to detect
anomalous regime shifts that indicate security threats (resource
exhaustion, data poisoning, model drift).

### For petalTongue

groundSpring's spectral reconstruction, rarefaction curves, and
uncertainty budgets are visualization-ready. petalTongue can render
groundSpring results directly via egui_plot/egui_graphs.

---

## 9. Deployment Patterns

### Minimal (Sovereign)

```toml
# groundspring_deploy.toml
[graph]
nodes = ["groundspring"]
```

groundSpring alone. CPU computation. No NUCLEUS needed.

### Tower-Enhanced

```toml
[graph]
nodes = ["beardog", "songbird", "groundspring"]
edges = [
  { from = "beardog",  to = "groundspring", capability = "crypto.sign" },
  { from = "songbird", to = "groundspring", capability = "discovery.register" },
]
```

Signed measurements, discoverable on the mesh.

### Full Compute

```toml
[graph]
nodes = ["beardog", "songbird", "toadstool", "groundspring"]
edges = [
  { from = "toadstool", to = "groundspring", capability = "compute.dispatch" },
]
```

GPU-accelerated measurement with sovereign dispatch.

### Full NUCLEUS

```toml
[graph]
nodes = ["beardog", "songbird", "toadstool", "nestgate", "squirrel", "groundspring"]
fallback = { nestgate = "skip", squirrel = "skip", toadstool = "skip" }
```

Everything. Optional nodes degrade gracefully.

---

## 10. IPC Contract

### Request Format

```json
{
  "jsonrpc": "2.0",
  "method": "measurement.<operation>",
  "params": { ... },
  "id": 1
}
```

### Response Format

```json
{
  "jsonrpc": "2.0",
  "result": { ... },
  "id": 1
}
```

### Error Format

```json
{
  "jsonrpc": "2.0",
  "error": { "code": -32000, "message": "..." },
  "id": 1
}
```

### Resilience

Callers should use `CircuitBreaker` + `RetryPolicy` for all IPC calls.
groundSpring's `BiomeOsError::is_recoverable()` classifies transient vs
permanent failures. Transport and discovery errors are retriable; protocol
and serialization errors are not.

---

## Summary

groundSpring is a **measurement primitive** — small, focused, composable.
It doesn't try to be a full scientific computing environment. It provides
8 measurement methods that compose with the NUCLEUS primals to create
measurement pipelines of arbitrary sophistication:

- **Alone**: Fast, deterministic measurement validation
- **+ Tower**: Signed, discoverable measurements
- **+ Node**: GPU-accelerated measurement at scale
- **+ Nest**: Cached, reproducible measurements with data pipelines
- **+ Full NUCLEUS**: AI-guided, attributed, immutable measurements
- **+ Provenance Trio**: SCYBORG-compliant measurement provenance
- **+ Other Springs**: Universal measurement backbone for the ecosystem
