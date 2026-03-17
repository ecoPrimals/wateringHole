<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# wetSpring Leverage Guide — Standalone, Trio, and Ecosystem Compositions

**Date**: March 17, 2026
**Primal**: wetSpring V126 (`wetspring-barracuda` 0.1.0 + `wetspring-forge` 0.3.0)
**Audience**: All springs, all primals, biomeOS integrators
**Status**: Active

---

## Purpose

This document describes how wetSpring can be leveraged — alone and in
composition with other primals — by springs and ecosystem consumers. Each
primal in the ecosystem produces an equivalent guide. Together, these
guides form a combinatorial recipe book for emergent behaviors.

wetSpring provides **sovereign life-science computation** — 16S amplicon
metagenomics, LC-MS analytical chemistry, PFAS screening, microbial
ecology, quorum-sensing models, and Anderson spectral analysis. Pure Rust,
zero unsafe, zero C application dependencies. 150+ barraCuda primitives
consumed. 354 validation/benchmark binaries. 1,685+ tests.

**Philosophy**: Microbes are everywhere. The diversity index, the QS
threshold, the Anderson localization transition — these are universal
signatures. wetSpring owns the biology; other primals own the hardware,
the network, the storage, the identity. Discover at runtime, compose at
will.

---

## IPC Methods (Semantic Naming)

All methods follow `{namespace}.{domain}.{operation}` per the
[Semantic Method Naming Standard](./SEMANTIC_METHOD_NAMING_STANDARD.md).

| Method | What It Does |
|--------|-------------|
| `science.diversity` | Alpha/beta diversity (Shannon, Simpson, Chao1, Pielou, Bray-Curtis, UniFrac) |
| `science.qs_model` | Quorum-sensing biofilm ODE (Waters 2008, Fernandez 2020, bistable switch) |
| `science.anderson` | Anderson spectral disorder (2D/3D lattice, level spacing ratio, GOE/Poisson) |
| `science.kinetics` | Biogas kinetics (Gompertz, first-order, Monod, Haldane) |
| `science.alignment` | Smith-Waterman local sequence alignment (affine gap) |
| `science.taxonomy` | Naive Bayes k-mer classifier (RDP-style 16S taxonomy) |
| `science.phylogenetics` | Robinson-Foulds distance, phylogenetic placement, Felsenstein pruning |
| `science.nmf` | Non-negative Matrix Factorization (drug repurposing, metagenome decomposition) |
| `science.timeseries` | Cross-spring time series (diversity tracking, perturbation response) |
| `science.ncbi_fetch` | NCBI ESearch/EFetch with NestGate tiered routing |
| `science.full_pipeline` | End-to-end 16S: FASTQ → QC → merge → derep → DADA2 → chimera → taxonomy → diversity |
| `health.check` | Health check (name, version, status, capabilities) |
| `health.liveness` | Kubernetes-style liveness probe |
| `health.readiness` | Readiness probe (GPU available, data loaded) |
| `provenance.begin` | Start provenance-tracked computation session |
| `provenance.record` | Record intermediate result with metadata |
| `provenance.complete` | Finalize session, return provenance chain |
| `brain.observe` | Submit observation to Nautilus neural sentinel |
| `brain.attention` | Query attention weights for active observations |
| `brain.urgency` | Get urgency score (drift detection, anomaly alert) |
| `metrics.snapshot` | Server metrics (calls, errors, latency histogram) |
| `ai.ecology_interpret` | AI-assisted diversity interpretation (Squirrel delegation) |

**Transport**: JSON-RPC 2.0 over Unix socket (primary), batch requests,
notifications. Capability-based discovery via Songbird.

---

## 1. wetSpring Standalone

These patterns use wetSpring alone — no other primals required.

### 1.1 Direct Library Dependency

**For**: Any spring needing biology, ecology, or analytical chemistry.

```toml
[dependencies]
wetspring-barracuda = { path = "../wetSpring/barracuda" }
```

**What you get**: Shannon/Simpson/Chao1 diversity, Bray-Curtis distance
matrices, DADA2 denoising, chimera detection, taxonomy classification,
Smith-Waterman alignment, phylogenetic placement, NMF decomposition,
QS ODE models, Anderson spectral analysis, PFAS screening, Savitzky-Golay
smoothing, EIC peak detection, mzML/FASTQ/MS2/JCAMP-DX parsers.

**Use cases**:
- **airSpring**: Soil microbial diversity from field samples (Shannon H' → Anderson W mapping)
- **healthSpring**: Gut microbiome diversity for PK/PD correlation
- **groundSpring**: Environmental monitoring diversity indices
- **hotSpring**: Hydrothermal vent community ecology (Rika Anderson's Sulfolobus work)
- **ludoSpring**: Procedural biome generation from real ecology data
- **neuralSpring**: Training data for ML models on real biological distributions

### 1.2 IPC Science Primal

**For**: Any primal wanting ecology computation without a compile-time dependency.

```
→ wetspring.sock: {"jsonrpc":"2.0","method":"science.diversity","params":{"counts":[10,20,30,5]},"id":1}
← {"jsonrpc":"2.0","result":{"shannon":1.2798,"simpson":0.7200,"chao1":4.0,"pielou":0.9228},"id":1}
```

**Discovery**: `discover::discover_socket(&socket_env_var("wetspring"), "wetspring")`

### 1.3 Validation Harness Pattern

**For**: Any spring needing structured validation with provenance.

wetSpring's `Validator` + `OrExit<T>` pattern is reusable:
- Named checks with pass/fail/exit-code
- Provenance headers (script, commit, date, hardware, command)
- `hotSpring` pattern: hardcoded expected values, explicit assertions
- Zero-panic: `OrExit` replaces all `unwrap()`/`expect()` in binaries

### 1.4 Tolerance Registry Pattern

**For**: Any spring managing numerical fidelity.

214 named tolerance constants in `tolerances::*`, organized by domain:
`bio/diversity`, `bio/ode`, `gpu`, `instrument`, `spectral`. Every
tolerance has a doc comment explaining provenance and justification.

---

## 2. wetSpring + SCYBORG Provenance Trio

The SCYBORG trio (rhizoCrypt + loamSpine + sweetGrass) provides
cryptographic anchoring, provenance tracking, and IPC patterns.

### 2.1 wetSpring + rhizoCrypt — Anchored Science

**Composition**: wetSpring computes → rhizoCrypt anchors results.

**Use case**: Every diversity analysis gets a cryptographic anchor.
A 16S pipeline run produces a provenance chain: input FASTQ hash →
QC parameters → DADA2 settings → ASV table → diversity indices → anchor.
Any downstream consumer can verify the computation was performed correctly
on the claimed input data.

**Novel pattern**: **Reproducible ecology** — anchor the Python baseline
SHA-256, the Rust validation output, and the GPU result together. Three
independent computations, one verifiable provenance chain. If any
diverges, the anchor chain breaks.

### 2.2 wetSpring + loamSpine — Learning Pathways

**Composition**: wetSpring provides biology → loamSpine learns optimal pathways.

**Use case**: loamSpine observes which wetSpring capabilities are called
most often, in what sequences, with what parameters. It learns that
`science.diversity` → `science.anderson` → `science.qs_model` is a
common pipeline for community health assessment. It can then suggest
pre-warming, caching, or fused execution.

**Novel pattern**: **Adaptive pipeline optimization** — loamSpine tracks
that Anderson W mapping after diversity always uses the same Pielou J →
disorder conversion. It can request wetSpring to expose a fused
`science.diversity_anderson` method that skips the IPC round-trip.

### 2.3 wetSpring + sweetGrass — Resilient IPC

**Composition**: sweetGrass provides IPC patterns → wetSpring gains resilience.

**Use case**: `RetryPolicy` + `CircuitBreaker` for calls to NestGate
(NCBI data), toadStool (GPU dispatch), and petalTongue (visualization).
`IpcErrorPhase::Timeout` classification. `extract_rpc_error()` and
`extract_capabilities()` for structured error handling.

**Novel pattern**: **Graceful degradation** — when toadStool is down,
wetSpring falls back to CPU. When NestGate is unreachable, it uses
sovereign HTTP. When petalTongue isn't running, it writes JSON to disk.
sweetGrass circuit breaker prevents retry storms.

---

## 3. wetSpring + Foundation Primals

### 3.1 wetSpring + barraCuda — GPU-Accelerated Biology

**Composition**: barraCuda provides math → wetSpring provides biology domain.

**Already wired**: 150+ primitives — `GemmF64`, `FusedMapReduceF64`,
`BatchedEighGpu`, `SparseGemmF64`, `TranseScoreF64`, `TopK`,
`PairwiseCosineGpu`, `BatchedOdeRK4`, `HmmForwardGpu`.

**Evolution targets**:
- `execute_gemm_ex(trans_a, trans_b)` — Tikhonov regularization without transpose materialization
- `tridiag_eigh_gpu` — batch Anderson eigensolve
- `stable_gpu::{log1p_f64, expm1_f64}` — numerical robustness in ODE solvers
- `PipelineBuilder` — multi-stage GPU streaming for full 16S pipeline
- `FmaPolicy::Separate` — reproducible cross-vendor results

**Novel pattern**: **Biology-aware GPU dispatch** — wetSpring knows the
biology (diversity indices cluster around [0,5] for Shannon, [0,1] for
Simpson). barraCuda knows the math (f64 precision, FMA policy). Together:
domain-aware precision routing where community ecology uses `FmaPolicy::Separate`
for reproducibility, while NMF drug screening uses `FmaPolicy::Contract`
for throughput.

### 3.2 wetSpring + toadStool — Compute Orchestration

**Composition**: toadStool discovers hardware → wetSpring dispatches science.

**Use case**: wetSpring submits `compute.dispatch.submit` with workload
type `"spectral_cosine"` and parameters. toadStool routes to the best
available GPU (or NPU for ESN inference). Progress callbacks stream to
petalTongue for live visualization.

**Novel pattern**: **Substrate-aware biology** — ESN reservoir computing
for microbial diversity prediction. On GPU: bulk training (8.2× faster
at reservoir 1024). On NPU: streaming inference at 2.8μs/step for
real-time sensor monitoring. toadStool routes based on workload
characteristics discovered at runtime.

### 3.3 wetSpring + NestGate — Sovereign Data

**Composition**: NestGate caches → wetSpring fetches NCBI data.

**Already wired**: Three-tier routing (biomeOS → NestGate → sovereign HTTP).
Content-addressed caching with SHA-256 integrity verification.

**Novel pattern**: **Offline-first metagenomics** — NestGate pre-caches
reference databases (SILVA 138.1, RDP, NCBI nr). Field deployments run
full 16S pipelines without internet. NestGate deduplicates across springs
(airSpring soil samples + wetSpring water samples share reference data).

### 3.4 wetSpring + Songbird — Federated Ecology

**Composition**: Songbird discovers → wetSpring is discovered.

**Use case**: A research group runs wetSpring on three machines:
sequencing station, GPU server, and field laptop. Songbird's BirdSong
discovery finds all three. Each registers its capabilities. The
sequencing station has `ecology.pipeline`, the GPU server has
`ecology.anderson` + GPU, the laptop has `ecology.diversity` only.
biomeOS routes work to the right node.

**Novel pattern**: **Distributed amplicon pipeline** — FASTQ QC on the
sequencer, GPU-accelerated spectral analysis on the server, diversity
visualization on the laptop. All coordinated by Songbird, all
provenance-tracked by the trio, all visualized by petalTongue.

### 3.5 wetSpring + BearDog — Signed Science

**Composition**: BearDog signs → wetSpring computes.

**Novel pattern**: **Cryptographically signed results** — every diversity
index, every ASV table, every taxonomic assignment gets an Ed25519
signature from BearDog via the genetic lineage. Downstream consumers
can verify that wetSpring (and only wetSpring, from this family) produced
the result. Prevents result tampering in regulatory contexts (EPA PFAS
screening, clinical metagenomics).

---

## 4. wetSpring + Post-NUCLEUS Primals

### 4.1 wetSpring + petalTongue — Live Science Dashboard

**Already wired**: `PetalTonguePushClient` for IPC push, `EcologyScenario`
JSON export, 6 scenario types (environmental profile, qs landscape,
biogas reactor, PFAS screening, rare biosphere, drug repurposing).

**Novel pattern**: **Real-time bioreactor monitoring** — ESN sentinel
watches diversity indices streaming from wetSpring. petalTongue renders
the Anderson disorder landscape in real time. When W crosses the
localization transition, the visualization changes from green (extended/QS)
to red (localized/no-QS). Operators see community health collapse before
it happens.

### 4.2 wetSpring + Squirrel — AI-Augmented Ecology

**Already wired**: `ai.ecology_interpret` capability domain.

**Novel pattern**: **Natural language ecology queries** — "What does a
Shannon H' of 2.3 mean for this wastewater treatment plant?" Squirrel
delegates to wetSpring for the computation, interprets the result using
its LLM context, and returns a human-readable explanation with citations
to the underlying papers (Waters 2008, Anderson 1958).

### 4.3 wetSpring + biomeOS — NUCLEUS Science Node

**Already wired**: `wetspring_server` binary, `wetspring_deploy.toml`
graph, `wetspring-ecology.yaml` niche manifest.

**Novel pattern**: **Germination-order science** — biomeOS deploys
wetSpring after barraCuda and toadStool are healthy. wetSpring registers
its 23 capabilities. Other primals discover `ecology.diversity` and start
routing work. If wetSpring goes unhealthy, biomeOS can spawn a second
instance on another node. The capability stays available; the deployment
is sovereign.

---

## 5. Cross-Spring Compositions

These patterns combine wetSpring with sibling springs for emergent behaviors.

### 5.1 wetSpring + airSpring — Soil-Water Nexus

**Composition**: wetSpring provides microbial diversity → airSpring
provides soil moisture + ET₀.

**Novel pattern**: **Coupled hydrology-ecology** — soil moisture drives
microbial activity, which drives nutrient cycling, which drives plant
growth, which drives ET₀. Real data: Michigan agricultural stations
(airSpring) paired with soil metagenomics (wetSpring). The Anderson
disorder W tracks soil health through the growing season.

**IPC flow**: `airSpring.science.soil_moisture` → wetSpring maps moisture
to microbial activity → `wetSpring.science.anderson` → Anderson W maps
to community coherence → back to airSpring for irrigation decisions.

### 5.2 wetSpring + healthSpring — Gut-Environment Axis

**Composition**: wetSpring provides environmental metagenomics →
healthSpring provides human health metrics.

**Novel pattern**: **One Health monitoring** — environmental water quality
(wetSpring: diversity, AMR genes, pathogen screening) correlates with
gut microbiome health (healthSpring: PK/PD, cytokine levels, biosignals).
The Anderson disorder parameter bridges both domains: environmental
W predicts gut W which predicts disease susceptibility.

### 5.3 wetSpring + hotSpring — Extremophile Physics

**Composition**: hotSpring provides physics (plasma, lattice QCD) →
wetSpring provides extremophile biology.

**Novel pattern**: **Yellowstone ecology** — Rika Anderson's *Sulfolobus*
in hot springs. Temperature profiles from hotSpring's thermodynamic
models paired with wetSpring's 16S diversity. At what temperature does
community structure undergo Anderson localization? Is the deconfinement
transition in QCD analogous to the diversity transition in microbial
communities?

### 5.4 wetSpring + groundSpring — Uncertainty-Aware Ecology

**Composition**: groundSpring provides uncertainty quantification →
wetSpring provides ecological measurements.

**Novel pattern**: **Bootstrap diversity** — groundSpring's Monte Carlo
+ bootstrap methods applied to wetSpring's diversity indices. Not just
"Shannon H' = 2.3" but "Shannon H' = 2.3 ± 0.15 (95% CI, 1000 bootstrap
replicates, rarefied to 10,000 reads)". Proper error bars on every
ecological measurement.

### 5.5 wetSpring + neuralSpring — ML-Augmented Metagenomics

**Composition**: neuralSpring provides ML models → wetSpring provides
biological features.

**Novel pattern**: **Transformer taxonomy** — neuralSpring's attention
mechanisms for 16S sequence classification. Instead of naive Bayes k-mer
counting, a transformer trained on SILVA 138.1 achieves species-level
resolution. wetSpring provides the data pipeline, neuralSpring provides
the model, barraCuda provides the GPU.

### 5.6 wetSpring + ludoSpring — Procedural Ecology

**Composition**: ludoSpring provides game design → wetSpring provides
real ecology.

**Novel pattern**: **Biome-accurate game worlds** — procedural generation
using real diversity distributions. A game forest has Shannon H' ≈ 3.5
because that's what real temperate forests show. NPC dialogue references
real microbial ecology. The game teaches biology by simulating it
accurately.

---

## 6. Full Ecosystem Composition

### The Science Stack

```
biomeOS (orchestration)
  ├─ toadStool (compute dispatch)
  │    └─ barraCuda (806 WGSL shaders, GPU math)
  ├─ wetSpring (life science, 23 capabilities)
  │    ├─ NestGate (NCBI data, content-addressed cache)
  │    ├─ petalTongue (live dashboard, 6 scenario types)
  │    └─ Squirrel (AI interpretation, MCP tools)
  ├─ rhizoCrypt + loamSpine + sweetGrass (provenance trio)
  ├─ BearDog (signed results, genetic lineage)
  └─ Songbird (discovery, federation, Dark Forest)
```

Every arrow is JSON-RPC 2.0 over Unix socket. Every connection is
discovered at runtime. Every result is provenance-tracked. Every
computation is reproducible. Every deployment is sovereign.

---

## 7. How Other Primals Can Use wetSpring

| Primal | Why It Would Call wetSpring | Method |
|--------|---------------------------|--------|
| **biomeOS** | Health monitoring of ecosystem nodes | `health.check`, `health.readiness` |
| **toadStool** | GPU workload validation | `science.diversity`, `science.anderson` |
| **petalTongue** | Dashboard data source | `science.diversity`, `science.timeseries` |
| **Squirrel** | AI tool for ecology queries | `ai.ecology_interpret` |
| **NestGate** | Content-addressed biology data | `science.ncbi_fetch` |
| **loamSpine** | Pathway learning from bio pipelines | `science.full_pipeline` |
| **rhizoCrypt** | Anchor science results | `provenance.begin/record/complete` |
| **sweetGrass** | IPC health monitoring | `health.liveness`, `metrics.snapshot` |
| **airSpring** | Soil microbiome diversity | `science.diversity`, `science.anderson` |
| **healthSpring** | Gut microbiome for PK/PD | `science.diversity`, `science.taxonomy` |
| **hotSpring** | Extremophile community ecology | `science.diversity`, `science.phylogenetics` |
| **groundSpring** | Environmental uncertainty | `science.diversity` (with bootstrap) |
| **neuralSpring** | ML training features | `science.diversity`, `science.ncbi_fetch` |
| **ludoSpring** | Procedural biome generation | `science.diversity` (distribution params) |

---

## Versioning

This guide tracks wetSpring's evolution. As capabilities are added,
compositions are updated.

| Version | Date | Changes |
|---------|------|---------|
| V126 | March 17, 2026 | Initial guide: 23 capabilities, 6 scenarios, 5 composition tiers |
