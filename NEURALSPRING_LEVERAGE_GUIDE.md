<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# neuralSpring Leverage Guide — Standalone, Trio, and Ecosystem Compositions

**Date**: March 17, 2026
**Spring**: neuralSpring V113/S162 (Rust edition 2024, pedantic+nursery)
**Audience**: All springs, all primals, biomeOS integrators
**Status**: Active

---

## Purpose

This document describes how neuralSpring can be leveraged — alone and in
composition with other primals — by springs and ecosystem consumers.
Each primal in the ecosystem will produce an equivalent guide. Together,
these guides form a combinatorial recipe book for emergent behaviors.

neuralSpring is the **ML and spectral analysis validation harness** for
the ecoPrimals stack. It proves that Python ML baselines can be faithfully
ported to sovereign Rust+GPU compute using barraCuda, then exposes those
validated capabilities as JSON-RPC services. 15 science capabilities,
60+ public modules, 130+ named tolerance constants, 260+ validation
binaries, 1133+ tests. Pure Rust, zero unsafe, zero C application
dependencies (ecoBin v3.0).

**Philosophy**: ML and spectral analysis are validated science, not black
boxes. Every neural network inference, every eigendecomposition, every
training trajectory has a provenance chain linking it to a reproducible
Python baseline. neuralSpring doesn't just compute — it proves the
computation is correct. Other primals provide the hardware, storage,
identity, and orchestration; neuralSpring provides validated ML
intelligence and spectral interpretation.

---

## IPC Methods (Semantic Naming)

All methods follow `{namespace}.{domain}.{operation}` per the
[Semantic Method Naming Standard](./SEMANTIC_METHOD_NAMING_STANDARD.md).

| Method | What It Does |
|--------|-------------|
| `health` | Health check (version, status, capabilities, hardware, uptime) |
| `health.liveness` | Kubernetes-style liveness probe (is the process alive?) |
| `health.readiness` | Readiness probe (GPU initialized, dispatcher ready?) |
| `capability.list` | Full capability manifest |
| `science.ipr` | Inverse participation ratio of a wavefunction |
| `science.disorder_sweep` | Anderson disorder sweep (IPR vs disorder strength) |
| `science.spectral_analysis` | Full spectral decomposition with phase classification |
| `science.anderson_localization` | Anderson localization analysis (eigenvalues, IPR, LSR) |
| `science.hessian_eigen` | Hessian eigendecomposition for loss landscape analysis |
| `science.agent_coordination` | Multi-agent quorum sensing via spectral graph theory |
| `science.training_trajectory` | Weight matrix spectral evolution during training |
| `science.evoformer_block` | AlphaFold evoformer block (MSA + pair representation) |
| `science.structure_module` | AlphaFold structure module (3D coordinate prediction) |
| `science.folding_health` | coralForge health check (model status, GPU availability) |
| `science.gpu_dispatch` | Arbitrary Dispatcher operations (44+ ops, GPU/CPU routing) |
| `science.cross_spring_provenance` | Cross-spring WGSL shader provenance report |
| `science.cross_spring_benchmark` | Dispatcher benchmark (variance, mean, softmax, gelu, eigh, shannon, pearson) |
| `science.precision_routing` | Precision routing report (fp64 strategy, bandwidth tier) |
| `primal.forward` | Forward request to another primal (async, capability-based) |
| `data.ncbi_search` / `data.ncbi_fetch` | NCBI data (forwarded to NestGate) |
| `data.pdb_search` / `data.pdb_fetch` | PDB structure data (forwarded to NestGate) |

**Transport**: JSON-RPC 2.0 over Unix socket (primary), tarpc/bincode
(high-throughput primal-to-primal, feature-gated). Capability-based
discovery via `capability.list` + biomeOS `nucleus.register`.

---

## 1. neuralSpring Standalone

These patterns use neuralSpring alone — no other primals required.

### 1.1 Validated ML Inference Library

**For**: Any spring that needs ML primitives with correctness guarantees.

```toml
neural-spring = { path = "../neuralSpring" }
```

neuralSpring exposes 60+ public modules as a Rust library — transformers,
LSTMs, LeNet-5, surrogates, PINNs, DeepONets, quantized inference,
echo state networks, and more. Every module has a corresponding
validation binary that proves its output matches a documented Python
baseline.

**Novel pattern**: **Certified inference** — a spring can import
neuralSpring's transformer module and know that every attention
computation has been validated against PyTorch to within 1e-10
absolute error. The tolerance is named (`TRANSFORMER_NUMPY_VS_PYTORCH`),
centralized, and explained. No other ML library offers this level of
validation provenance.

### 1.2 Spectral Intelligence for Weight Matrices

**For**: Any spring training neural networks or analyzing dynamical systems.

```json
{ "method": "science.spectral_analysis", "params": { "dim": 64, "disorder": 2.0 } }
```

neuralSpring provides a complete spectral analysis toolkit for weight
matrices: eigendecomposition, level spacing ratio (GOE vs Poisson phase
classification), inverse participation ratio (localization), spectral
bandwidth, condition number, and spectral entropy.

**Novel pattern**: **Training health monitoring** — during training, a
spring calls `science.training_trajectory` to track spectral evolution.
If IPR collapses below 0.01 (memorization) or bandwidth explodes 5×
(gradient instability), neuralSpring flags it. The training loop can
adjust learning rate or early-stop based on spectral signals rather than
just loss curves.

### 1.3 Anderson Localization as a Universal Diagnostic

**For**: Any spring analyzing disorder, robustness, or phase transitions.

```json
{ "method": "science.anderson_localization", "params": {
    "lattice_size": 64,
    "disorder_values": [0.5, 1.0, 2.0, 4.0, 8.0, 16.0]
}}
```

Anderson localization — the transition from extended to localized
eigenstates as disorder increases — applies far beyond condensed matter
physics. neuralSpring uses it to analyze neural network weight disorder,
multi-agent coordination resilience, and attention pattern structure.

**Novel pattern**: **Network robustness classification** — inject
controlled disorder into a weight matrix and measure IPR. Extended phase
(GOE statistics) = robust, generalized representation. Localized phase
(Poisson statistics) = fragile, memorized features. This gives a
physics-grounded metric for network health that complements traditional
loss/accuracy metrics.

### 1.4 GPU-Accelerated Scientific Dispatch

**For**: Any spring needing GPU compute with automatic CPU fallback.

```json
{ "method": "science.gpu_dispatch", "params": {
    "op": "eigh", "data": [...], "dim": 64
}}
```

neuralSpring's `Dispatcher` routes 44+ operations (variance, mean,
softmax, gelu, eigh, matmul, ReLU, sigmoid, pearson, shannon, etc.)
to GPU or CPU based on hardware availability. Precision routing
(`PrecisionBrain`) selects the optimal f64 strategy automatically.

**Novel pattern**: **Heterogeneous benchmark** — call
`science.cross_spring_benchmark` to get timing data for 7 representative
ops on the current hardware. Use this to calibrate computational budgets
— if eigendecomposition takes 50μs on GPU but 5ms on CPU, allocate
analysis tasks accordingly.

### 1.5 Protein Structure Prediction (coralForge)

**For**: Any spring analyzing protein structures.

```json
{ "method": "science.evoformer_block", "params": {
    "msa_feat": [...], "pair_feat": [...], "n_seq": 4, "n_res": 8
}}
```

neuralSpring implements AlphaFold2/3-style evoformer blocks, structure
modules, pairformer, diffusion schedules, and confidence heads —
validated against the original architectures. These are exposed as
IPC services for any spring that needs structure prediction without
importing a Python ML framework.

**Novel pattern**: **Spectral folding health** — combine
`science.folding_health` (structure prediction status) with
`science.spectral_analysis` (weight matrix phase) to monitor whether
the evoformer's attention patterns are in the extended (good) or
localized (degenerate) regime during iterative refinement.

### 1.6 130+ Named Tolerance Constants

**For**: Any spring needing scientifically justified numerical thresholds.

neuralSpring's tolerance registry provides runtime introspection of all
named constants with categories and justifications:

| Category | Examples | Count |
|----------|---------|-------|
| machine | `EXACT_F64`, `ZERO_DETECTION` | 5 |
| benchmark | `OPTIMIZER_POSITION`, `BENCHMARK_CROSS_PYTHON` | 7 |
| transformer | `SOFTMAX_SUM`, `GELU_CROSS_PYTHON`, `CAUSAL_MASK_LEAK` | 8 |
| numerical | `LOG_ZERO_GUARD`, `FITNESS_FLOOR`, `HESSIAN_FD_STEP` | 12 |
| spectral | `KAPPUS_WEGNER_REL`, `LEVEL_SPACING_POISSON_TOL` | 8 |
| folding | `FOLDING_EPS`, `SDPA_PASSTHROUGH`, `PLDDT_DEGENERACY` | 6 |
| training_monitor | `BANDWIDTH_GROWTH`, `IPR_COLLAPSE`, `LOSS_DIVERGENCE` | 6 |
| ... | (20 categories total) | 130+ |

**Novel pattern**: **Tolerance inheritance** — a spring needing to
validate its own numerical results can import neuralSpring's tolerance
constants rather than defining ad-hoc magic numbers. The constants
carry mathematical justification in their doc comments.

---

## 2. Duo Compositions (neuralSpring + One Other Primal)

### 2.1 neuralSpring + barraCuda → Validated GPU Science

barraCuda provides 806 WGSL shaders and the Tensor API. neuralSpring
validates that every GPU primitive produces correct results.

**Pattern**: neuralSpring defines the expected output (from Python
baselines) → barraCuda computes on GPU → neuralSpring validates the
result within named tolerances.

**Spring application**: Any spring using barraCuda can run neuralSpring's
260+ validation binaries to confirm correctness on their specific GPU.
Different GPUs may have different f64 behavior — the validation suite
catches it.

### 2.2 neuralSpring + toadStool → Hardware-Aware ML

toadStool provides hardware discovery and compute orchestration.

**Pattern**: toadStool probes GPU capabilities (f64, VRAM, cache) →
neuralSpring selects model size and precision accordingly → toadStool
dispatches via VFIO for deterministic scheduling.

**Spring application**: neuralSpring asks toadStool "what GPU is
available?" and adapts: 24GB VRAM → full transformer. 4GB VRAM →
quantized INT8 inference. CPU only → lightweight MLP. The same science
runs everywhere; toadStool provides the hardware truth.

**Novel combo**: `science.precision_routing` returns the current fp64
strategy and bandwidth tier. A spring can query this before submitting
heavy eigendecomposition to decide whether GPU dispatch is worthwhile.

### 2.3 neuralSpring + coralReef → Sovereign ML Compilation

coralReef provides WGSL→native GPU binary compilation.

**Pattern**: neuralSpring's metalForge contains WGSL shaders for
ML operations (attention, layer norm, softmax). coralReef compiles
these to native GPU ISA. neuralSpring validates the compiled output.

**Spring application**: neuralSpring's `validate_sovereign_compile`
binary proves that coralReef-compiled shaders produce bit-identical
results to naga-compiled shaders. This is the correctness proof for
the sovereign compilation path.

### 2.4 neuralSpring + petalTongue → Visualized Science

petalTongue provides multi-modal UI and data visualization.

**Pattern**: neuralSpring pushes spectral analysis results to
petalTongue via `visualization.render` → petalTongue renders
interactive plots (loss landscapes, spectral phase diagrams,
training trajectories, protein structures).

**Spring application**: neuralSpring exposes 6 visualization scenarios
(spectral study, coralForge study, baseCamp study, cross-spring
evolution, full study). petalTongue renders them with
interactive controls — zoom into localization transitions, scrub
through training epochs, rotate protein structures.

### 2.5 neuralSpring + sweetGrass → Provenance-Tracked ML

sweetGrass provides W3C PROV-O provenance braids.

**Pattern**: neuralSpring records experiment provenance (Python script,
commit, date, command, expected values) → sweetGrass creates a
provenance braid linking each validation result to its exact
reproducibility chain.

**Spring application**: A published result validated by neuralSpring
carries a machine-verifiable provenance chain: "This softmax output
was validated against `python3 -c 'import numpy as np; ...'`
(commit abc123, 2026-02-16) with tolerance `SOFTMAX_CROSS_PYTHON =
1e-14`."

### 2.6 neuralSpring + squirrel → AI-Guided Science

squirrel provides sovereign AI coordination (MCP, model routing).

**Pattern**: squirrel suggests experiment parameters (hyperparameters,
architecture choices) → neuralSpring executes the experiment on
GPU → neuralSpring validates the result → squirrel interprets
the spectral analysis and suggests next experiment.

**Spring application**: Automated neural architecture search.
squirrel proposes architectures, neuralSpring trains and validates
them, spectral analysis identifies which architectures have healthy
weight dynamics (extended phase) vs pathological ones (localized).
squirrel learns from the spectral feedback.

### 2.7 neuralSpring + biomeOS → Orchestrated ML Pipelines

biomeOS provides Neural API graph orchestration.

**Pattern**: biomeOS composes neuralSpring into DAG pipelines with
other primals → neuralSpring capabilities are nodes in the
computation graph → biomeOS handles scheduling and data flow.

**Spring application**: A structure prediction pipeline as a biomeOS
DAG: `data.pdb_fetch` (NestGate) → `science.evoformer_block`
(neuralSpring) → `science.structure_module` (neuralSpring) →
`visualization.render` (petalTongue). biomeOS executes the graph;
each node is a JSON-RPC call to the responsible primal.

---

## 3. Trio and Multi-Primal Compositions

### 3.1 Validated Compute Trio (neuralSpring + barraCuda + toadStool)

neuralSpring validates. barraCuda computes. toadStool orchestrates.

```
neuralSpring (Layer 0 — WHAT to prove)
    Expected values, tolerances, provenance
    ↓
barraCuda (Layer 1 — WHAT to compute)
    806 WGSL shaders, CPU fallback
    ↓
toadStool (Layer 3-4 — WHERE to run)
    Hardware discovery, VFIO dispatch
```

**Novel pattern**: **Continuous validation** — neuralSpring's 260+
validation binaries run on any machine to prove the compute stack is
correct on that specific hardware. Deploy a new GPU? Run
`validate_cpu_gpu_parity` to confirm barraCuda+toadStool produces
correct results. No manual testing needed.

### 3.2 Reproducible ML Science
(neuralSpring + barraCuda + sweetGrass + loamSpine)

Every ML experiment is permanently attributed:

1. neuralSpring trains model (via barraCuda GPU dispatch)
2. neuralSpring records provenance (Python baseline, tolerance, result)
3. sweetGrass creates W3C PROV-O braid
4. loamSpine commits to permanent ledger with inclusion proof

**Spring application**: A published paper's neural network results
carry a permanent, machine-verifiable chain: input data → training
code → hardware environment → final weights → inference output →
validation against Python baseline → publication figure. Every link
is cryptographically attested.

### 3.3 Adaptive Spectral Analysis
(neuralSpring + toadStool + squirrel)

AI-guided spectral analysis with hardware adaptation:

1. squirrel proposes disorder parameters for Anderson analysis
2. toadStool reports GPU capabilities (VRAM, f64 support)
3. neuralSpring selects lattice size based on available VRAM
4. neuralSpring runs spectral analysis on GPU
5. squirrel interprets phase diagram and suggests next disorder point
6. Loop until phase boundary is mapped

**Novel pattern**: **Active learning for phase boundaries** — instead
of sweeping disorder uniformly, squirrel focuses sampling on the
localization transition (W ≈ 2t for 1D Anderson), producing a
high-resolution phase boundary with fewer GPU-hours.

### 3.4 Structure Prediction Pipeline
(neuralSpring + barraCuda + coralReef + petalTongue)

End-to-end protein structure prediction with visualization:

1. neuralSpring computes evoformer block (MSA + pair processing)
2. barraCuda dispatches attention/matmul on GPU
3. coralReef compiles ML kernels to native ISA
4. neuralSpring runs structure module (3D coordinate prediction)
5. petalTongue visualizes the predicted structure + confidence

**Novel pattern**: **Spectral folding monitor** — during iterative
refinement, neuralSpring analyzes the attention weight matrices
spectrally. If the evoformer's attention collapses to rank-1
(localized), the refinement has stalled. This spectral signal
triggers architecture adjustments that loss alone wouldn't catch.

### 3.5 Defended ML Inference
(neuralSpring + toadStool + bearDog + skunkBat)

Secure, monitored ML inference:

1. bearDog encrypts inference input
2. toadStool isolates GPU via VFIO (IOMMU)
3. neuralSpring runs inference on isolated GPU
4. skunkBat monitors for anomalous access patterns
5. bearDog signs the output for integrity

**Spring application**: healthSpring clinical ML. Patient biomarkers
encrypted at ingest, processed on IOMMU-isolated GPU, model inference
validated against known baselines, output signed and attributed.
No plaintext patient data on shared GPU memory.

---

## 4. Per-Spring Leverage Patterns

### 4.1 hotSpring (Plasma Physics, Lattice QCD)

| Capability | How neuralSpring Helps |
|-----------|----------------------|
| Spectral phase classification | Classify Anderson/GOE/Poisson phases in Hofstadter butterfly |
| Training trajectory | Track weight spectral evolution in neural network potentials |
| Hessian eigenanalysis | Loss landscape curvature for MD force-field optimization |
| IPR analysis | Localization diagnostics for wavefunction quality |

**Novel combo**: hotSpring runs lattice QCD HMC → neuralSpring
spectral-analyzes the Dirac operator's eigenvalues → detects
localization transition → hotSpring adjusts lattice spacing
at the critical point.

### 4.2 wetSpring (Life Science, Metagenomics)

| Capability | How neuralSpring Helps |
|-----------|----------------------|
| HMM inference | Validated hidden Markov models for phylogenetic inference |
| Bootstrap/diversity | Validated diversity indices (Shannon, Simpson, Chao1) |
| LSTM/GRU | Validated sequence models for genomic time series |
| Smith-Waterman | Validated pairwise alignment with GPU acceleration |

**Novel combo**: wetSpring 16S pipeline → neuralSpring validates
HMM phylogenetic inference against Python baselines → sweetGrass
records provenance from raw reads to published diversity indices.

### 4.3 airSpring (Precision Agriculture)

| Capability | How neuralSpring Helps |
|-----------|----------------------|
| MLP surrogate | Validated FAO-56 ET₀ surrogate model (R² > 0.95) |
| PINN | Physics-informed neural network for soil water dynamics |
| Quantized inference | INT8/INT4 inference for edge deployment |
| DeepONet | Operator learning for irrigation response functions |

**Novel combo**: airSpring edge deployment → neuralSpring provides
INT8-quantized ET₀ surrogate (validated degradation < 1%) → runs
on low-power field hardware via toadStool → squirrel interprets
results for irrigation scheduling.

### 4.4 groundSpring (Uncertainty, Spectral Theory)

| Capability | How neuralSpring Helps |
|-----------|----------------------|
| Spectral analysis | Shared eigendecomposition and spectral metrics |
| Anderson localization | Shared localization framework for disorder analysis |
| Loss landscape | Hessian eigenanalysis for optimization convergence |
| Level spacing ratio | Phase classification (GOE vs Poisson) for random matrices |

**Novel combo**: groundSpring uncertainty quantification + neuralSpring
spectral analysis → joint spectral-uncertainty framework: neuralSpring
classifies the phase of the Hessian at the uncertainty estimate,
groundSpring propagates the appropriate error bounds for that phase.

### 4.5 healthSpring (Clinical, PK/PD)

| Capability | How neuralSpring Helps |
|-----------|----------------------|
| LSTM glucose prediction | Validated CGM time-series prediction |
| Transformer inference | Validated attention-based clinical models |
| PINN pharmacokinetics | Physics-informed PK/PD neural models |
| Quantized clinical | INT8 inference for medical edge devices |

**Novel combo**: healthSpring population PK/PD + neuralSpring PINN
→ physics-informed pharmacokinetic neural network that respects
mass balance constraints → validated against analytical Cole-Hopf
solution → deployed on clinical edge device via quantized inference.

### 4.6 ludoSpring (Game Science, HCI)

| Capability | How neuralSpring Helps |
|-----------|----------------------|
| Game theory | Validated evolutionary game theory (replicator dynamics) |
| Swarm robotics | Validated multi-agent coordination |
| Echo state networks | Validated reservoir computing for game AI |
| Agent coordination | Spectral analysis of multi-agent networks |

**Novel combo**: ludoSpring game AI + neuralSpring agent coordination
→ spectral analysis of the game's interaction network reveals
whether agents are in a cooperative (extended) or competitive
(localized) phase → game balance tuning informed by spectral theory.

---

## 5. Emergent Ecosystem Patterns

### 5.1 Universal Validation Pattern

Any spring can validate its GPU compute using neuralSpring's harness:

```
Spring → define expected values from Python baselines
       → write validation binary using ValidationHarness
       → centralize tolerances in tolerances.rs
       → run validation → exit 0 (pass) or 1 (fail)
```

This pattern (absorbed from hotSpring) is the ecosystem standard.
neuralSpring's 260+ binaries demonstrate it at scale.

### 5.2 Spectral Diagnostics as a Service

neuralSpring's spectral capabilities compose into a diagnostic
service for any computation that involves matrices:

```
Any spring → neuralSpring: "analyze this weight/interaction matrix"
          → eigendecomposition, IPR, LSR, phase classification
          → "Your matrix is in the localized phase — consider
             regularization or increasing connectivity"
```

This is universal — it applies to neural network weights (ML),
Hamiltonians (physics), adjacency matrices (networks), transition
matrices (stochastic processes), and Hessians (optimization).

### 5.3 Cross-Spring Shader Provenance

neuralSpring tracks which WGSL shaders originated from which spring
and which primals consume them:

```
science.cross_spring_provenance →
{
  "total_shaders": 47,
  "cross_spring_edges": 12,
  "shaders": [
    { "path": "variance_f64.wgsl", "origin": "hotSpring",
      "consumers": ["neuralSpring", "groundSpring", "wetSpring"] },
    ...
  ]
}
```

This creates a dependency graph of mathematical primitives across
the ecosystem — useful for impact analysis when a shader evolves.

### 5.4 Tolerance Ecosystem

neuralSpring's tolerance constants are designed to be shared:

```rust
use neural_spring::tolerances;

assert!((result - expected).abs() < tolerances::CROSS_LANGUAGE);
```

Other springs can depend on these named constants rather than
inventing their own magic numbers. The constants carry mathematical
justification and Python baseline provenance in their documentation.

---

## 6. Creative Cross-Primal Patterns

### 6.1 neuralSpring as ML Oracle

Other primals can treat neuralSpring as an inference-as-a-service
oracle without importing ML dependencies:

```json
{ "method": "science.gpu_dispatch", "params": {
    "op": "matmul", "a": [...], "b": [...], "m": 64, "k": 32, "n": 16
}}
```

The calling primal doesn't know whether the matmul ran on GPU or CPU,
f32 or f64, naga or coralReef. neuralSpring handles dispatch routing
based on hardware capabilities.

### 6.2 neuralSpring as Spectral Compass

Any primal or spring can ask "is this system healthy?" by sending a
matrix for spectral analysis:

- **GOE phase (extended)**: system is well-connected, robust, generic
- **Poisson phase (localized)**: system is fragmented, fragile, specific
- **Transition**: system is at a critical point — small changes have large effects

This applies to: neural network weights, communication network graphs,
agent interaction matrices, control system Jacobians, financial
correlation matrices, ecological interaction webs.

### 6.3 neuralSpring + rhizoCrypt → Ephemeral ML

rhizoCrypt provides ephemeral content-addressed storage (auto-expiry).

**Pattern**: neuralSpring stores intermediate training checkpoints in
rhizoCrypt's ephemeral DAG → after training completes, only the final
model persists → intermediate gradients auto-dehydrate after 72 hours.

**Why it matters**: ML training produces terabytes of intermediate
state. Keeping it forever is wasteful; deleting it immediately loses
the ability to resume from a checkpoint. rhizoCrypt's auto-expiry
provides the sweet spot — checkpoints are available for recovery
during training, then automatically reclaimed.

### 6.4 neuralSpring + Songbird → Federated Validation

songBird provides encrypted networking and federation.

**Pattern**: Run neuralSpring's validation suite across a federation
of heterogeneous hardware. songBird discovers all machines, toadStool
reports each GPU's capabilities, neuralSpring runs validation binaries
on each GPU variant.

**Why it matters**: A research group with mixed hardware (NVIDIA,
AMD, Intel) can validate that barraCuda produces consistent results
across all GPUs. The federation provides comprehensive hardware
coverage that no single machine can achieve.

### 6.5 Multi-Spring Concurrent Science

neuralSpring's IPC service supports concurrent requests (configurable
semaphore, default 4 concurrent connections). Multiple springs can
query spectral analysis simultaneously:

```
hotSpring → neuralSpring: science.spectral_analysis (lattice QCD Dirac)
wetSpring → neuralSpring: science.spectral_analysis (HMM transition matrix)
groundSpring → neuralSpring: science.hessian_eigen (optimization Hessian)
ludoSpring → neuralSpring: science.agent_coordination (game network)

All four run concurrently. neuralSpring routes GPU ops to Dispatcher.
```

---

## 7. How Springs Should Consume neuralSpring

### Minimal Integration (library dependency)

```toml
# In Cargo.toml
neural-spring = { path = "../neuralSpring" }
```

```rust
use neural_spring::tolerances;
use neural_spring::validation::ValidationHarness;
use neural_spring::gpu_dispatch::Dispatcher;
```

No IPC needed. Import as a library for validation harness, tolerances,
spectral analysis, and GPU dispatch.

### IPC Integration (JSON-RPC service)

```rust
let socket = discover_by_capability("science.spectral_analysis", "neuralspring");
let result = call(&socket, "science.spectral_analysis", &params, timeout).await?;
```

Discover by capability, not by name. neuralSpring registers its
capabilities with biomeOS at startup.

### Full Ecosystem Integration (biomeOS pipeline)

```json
{
  "pipeline": "structure_prediction",
  "nodes": [
    { "capability": "data.pdb_fetch", "params": { "pdb_id": "1UBQ" } },
    { "capability": "science.evoformer_block", "params": { "n_iter": 8 } },
    { "capability": "science.structure_module", "params": {} },
    { "capability": "visualization.render", "params": { "title": "1UBQ" } }
  ]
}
```

biomeOS resolves capabilities to primals and executes the DAG.

### What NOT to Do

- **Don't hardcode neuralSpring's socket path** — discover by capability
- **Don't duplicate spectral analysis** — neuralSpring has it validated
- **Don't invent tolerance constants** — import from `tolerances.rs`
- **Don't skip validation** — run the validation suite on your hardware
- **Don't assume GPU** — neuralSpring falls back to CPU transparently

---

## 8. What neuralSpring Does NOT Do

neuralSpring is deliberately bounded. It does not:

- **Own hardware** — that's toadStool
- **Compile shaders** — that's coralReef (neuralSpring validates them)
- **Store data** — that's nestGate
- **Encrypt data** — that's bearDog
- **Route network traffic** — that's songBird
- **Manage identity** — that's bearDog/biomeOS
- **Render UI** — that's petalTongue (neuralSpring pushes data to it)
- **Orchestrate primals** — that's biomeOS
- **Invent math** — that's barraCuda (neuralSpring validates it)

neuralSpring owns the validation and spectral intelligence. Proving
that the math is correct, analyzing what the matrices mean, and
providing certified ML inference. Everything else is delegated to the
primal that owns that domain.

---

## References

- `neuralSpring/README.md` — Full spring documentation
- `neuralSpring/specs/EVOLUTION_MAPPING.md` — Python → Rust → GPU mapping
- `neuralSpring/specs/BARRACUDA_USAGE.md` — barraCuda integration audit
- `neuralSpring/src/tolerances/mod.rs` — All named tolerance constants
- `neuralSpring/src/provenance/mod.rs` — Python baseline provenance
- `wateringHole/BARRACUDA_LEVERAGE_GUIDE.md` — barraCuda leverage guide
- `wateringHole/TOADSTOOL_LEVERAGE_GUIDE.md` — toadStool leverage guide
- `wateringHole/SEMANTIC_METHOD_NAMING_STANDARD.md` — Method naming
- `whitePaper/gen3/PRIMAL_CATALOG.md` — Full primal catalogue
- `whitePaper/gen3/SPRING_CATALOG.md` — Spring catalogue
