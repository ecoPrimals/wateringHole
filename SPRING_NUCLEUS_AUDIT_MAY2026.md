# Spring NUCLEUS Composition Audit — May 2026

> Comprehensive 7-dimension audit of all 8 springs for NUCLEUS composition
> completeness, led by library-to-binary rewiring inventory.

**Date**: May 5, 2026
**From**: Ecosystem guidance (wateringHole)
**License**: AGPL-3.0-or-later

---

## The Library-to-Binary Evolution Story

During earlier evolution, springs were the laboratories where primal math was
developed. Work started local to the spring — hotSpring built precision mixing
and df64 GPU emulation, wetSpring evolved spectral analysis and biodiversity
statistics, ludoSpring proved game math under tick-budget constraints — and then
the upstream primal (barraCuda) would pull, review, and absorb. The spring-local
`barracuda/` and `ecoPrimal/` directories are artifacts of this process.

Now that primals have absorbed the math, **springs must rewire from library
imports to binary-only IPC calls** against ecobin-deployed primals. This
rewiring is the primary evolution target.

`metalForge/` is NOT a rewiring target. metalForge is the spring's hardware
abstraction layer — same science code on GPU, CPU, NPU, or mixed systems. It
stays local and informs toadStool about dispatch capabilities. It may need
refinement as toadStool's dispatch contract evolves, but it is architecturally
correct as a spring-local concern.

---

## Audit Dimensions

1. **Library-to-Binary Rewiring Status** (PRIMARY)
2. **Deploy Graphs** — typed TOML expressing science as NUCLEUS compositions
3. **Provenance Integration** — trio pattern compliance
4. **petalTongue Bindings** — can the science "present itself"?
5. **sweetGrass Braiding** — attribution braids for experiments
6. **Paper Expression** — end-to-end NUCLEUS compositions for science papers
7. **Contribution History** — what the spring evolved that primals absorbed

### The Rewiring Tier Model

From hotSpring's `composition.rs`:

```
Rust result (known-good)  <->  IPC composition result (being validated)
```

| Tier | Description | Status |
|------|-------------|--------|
| **2** | Spring server serves domain methods via in-process library calls; validates IPC routing | Routing proven |
| **3** | Spring calls ecobin primals over IPC, compares to library baselines; validates science through primal IPC | Parity proven |
| **4** | Spring drops library dep entirely; all compute through IPC to ecobin primals | Binary-only target |

---

## Summary Matrix

| Spring | Version | gS | Tests | Rewiring Tier | IPC% | Deploy Graphs | Provenance | petalTongue | sweetGrass | Papers |
|--------|---------|-----|-------|---------------|------|---------------|------------|-------------|------------|--------|
| **primalSpring** | v0.9.21 | 4 | 631 | **4** (no barraCuda link) | ~100% | 71 TOMLs | Trio E2E | — (coordinator) | — (coordinator) | Coordination |
| **ludoSpring** | V53 | 4 | 820 | **3** | ~40-60% | 13 TOMLs | Dedicated `ipc/provenance/` | `game_scene` wired | Session braids | 15+ baseCamp |
| **healthSpring** | V59 | 5 | 948 | **3** | ~30-50% | 7 TOMLs | Via `ecoPrimal/src/ipc/` | DataChannel wired | Partial | 8+ baseCamp |
| **airSpring** | v0.10.0 | 0 | 1,364 | **2** | ~25-40% | 4 TOMLs | `ipc/provenance.rs` | Not wired | Not wired | 11 baseCamp |
| **wetSpring** | V151 | 4+ | 1,594 | **2** | ~10-20% | 7 TOMLs | `ipc/provenance.rs` + `sweetgrass.rs` | Partial | Partial | 15+ baseCamp |
| **hotSpring** | v0.6.32 | 5 | 993 | **2** | ~5-15% | 1 TOML | Via `composition.rs` | Not wired | Not wired | 15+ baseCamp |
| **neuralSpring** | V138 | 3 | 1,234 | **2** | ~5-10% | 1 TOML | Via `ipc_dispatch.rs` | Not wired | Not wired | 15+ baseCamp |
| **groundSpring** | V124 | 0 | 1,020 | **1** | ~1-5% | 6 TOMLs | Minimal | Not wired | Not wired | 8 baseCamp |

---

## Per-Spring Audit

---

### 1. primalSpring (v0.9.21 — guideStone Level 4)

**Role**: Coordination hub. Validates compositions, provides `composition` library,
surfaces gaps. Does not own domain science.

#### Dimension 1: Library-to-Binary Rewiring — COMPLETE (Tier 4)

- **Local primal dirs**: `ecoPrimal/` — crate `primalspring` (coordination, not barraCuda fork)
- **barraCuda coupling**: **Zero**. `barracuda::` does not appear under `ecoPrimal/src/`.
  primalSpring talks to primals exclusively over IPC.
- **IPC surface**: Full `ecoPrimal/src/ipc/` — `transport`, `client`, `discover`,
  `capability`, `neural_bridge`, `dispatch`. Canonical wrappers for the ecosystem.
- **niche.rs**: Yes — uses `PrimalClient` / `discover_primal` from `crate::ipc`

primalSpring is the reference implementation for binary-only coordination.

#### Dimension 2: Deploy Graphs — 71 TOMLs

`graphs/` contains `spring_deploy/`, `spring_validation/`, fragments, cells,
downstream manifests, nucleus complete graph. The most comprehensive graph
library in the ecosystem.

#### Dimension 3: Provenance — Trio E2E validated

projectNUCLEUS pipeline exercised full provenance chain (rhizoCrypt DAG ->
loamSpine commit -> sweetGrass braid) via RPC. Documented in handoffs.

#### Dimension 7: Contribution History

primalSpring's role is coordination — it evolved the composition validation
library, guideStone standard, deploy graph schema, and NUCLEUS atomic model
that all springs consume.

---

### 2. hotSpring (v0.6.32 — guideStone Level 5, CERTIFIED)

**Domain**: Lattice QCD, molecular dynamics, nuclear EOS, HPC physics.

#### Dimension 1: Library-to-Binary Rewiring — Tier 2

- **Local primal dirs**: `barracuda/` (crate `hotspring-barracuda`, ~447 .rs files),
  `metalForge/forge/`
- **barraCuda coupling**: **Heavy**. `barracuda::` is pervasive across physics modules:
  `ops::linalg` (BatchedEighGpu, eigh_f64, GEMM), `ops::md::*` (CellListGpu,
  PppmGpu, forces, electrostatics), `ops::lattice::*`, `pipeline::ReduceScalarPipeline`,
  `shaders::precision::ShaderTemplate`, `special::*`, `numerical::*`, `optimize::*`,
  `sample::*`, `stats::*`, `nautilus::*`, `esn_v2::*`
- **IPC surface**: No `src/ipc/` directory. IPC is scattered across `primal_bridge.rs`
  (socket scan + `NucleusContext::call_by_capability`), `composition.rs` (dual-lane
  validation), `glowplug_client.rs`, `fleet_ember.rs`, `toadstool_report.rs`,
  `squirrel_client.rs`
- **niche.rs**: Yes — LOCAL vs ROUTED capabilities documented
- **Key docs**: `PRIMAL_PROOF_IPC_MAPPING.md` maps domain methods to barraCuda
  JSON-RPC (`tensor.*`, `stats.*`, `compute.dispatch`). `validate_primal_proof`
  binary implements Tier 3 validation (calls ecobin primals, compares to baselines).
- **metalForge**: `metalForge/forge/` with `barracuda` dep. GPU/CPU dispatch profiles.
  Needs refinement to express hardware capabilities as toadStool-routable profiles.

**Rewiring path**: hotSpring has the architecture for Tier 3 (`composition.rs` +
`primal_bridge.rs` + `validate_primal_proof`) but the bulk physics pipeline still
links barraCuda. The incremental path is to expand Tier 3 coverage method-by-method
using the `PRIMAL_PROOF_IPC_MAPPING.md` as the checklist, then consolidate IPC
into a proper `src/ipc/` directory following ludoSpring/healthSpring patterns.

**Standardization**: hotSpring's `composition.rs` dual-lane model and
`PRIMAL_PROOF_IPC_MAPPING.md` are the **template** all springs should adopt for
documenting their rewiring surface.

#### Dimension 2: Deploy Graphs — 1 TOML

`graphs/hotspring_qcd_deploy.toml` — includes provenance trio nodes.
**Gap**: Only one deploy graph for a spring with 33+ experiments across QCD,
MD, nuclear EOS, plasma physics. Each major science pipeline needs its own
composition graph.

#### Dimension 3: Provenance — Via composition.rs

Provenance trio referenced in deploy graph and composition validation, but no
dedicated `ipc/provenance.rs` module. No graceful degradation contract.

#### Dimension 4: petalTongue — Not wired

No DataBinding channels. Science outputs (lattice configs, HMC trajectories,
convergence metrics) are not streamed to petalTongue.

**Vision**: `heatmap` for lattice gauge configurations, `timeseries` for HMC
evolution / plaquette convergence, `gauge` for acceptance rate, `scatter3d` for
phase diagrams. Live lattice QCD: the HMC trajectory IS the figure.

#### Dimension 5: sweetGrass — Not wired

No attribution braids for experiments. The QCD simulation provenance (which
gauge configs contributed to which measurements) is a natural braid target.

#### Dimension 6: Paper Expression

15+ baseCamp papers (Chuna gradient flow, Murillo lattice QCD, Murillo plasma,
self-tuning RHMC, neuromorphic field theory, etc.). 33 experiments. Rich science
but not yet expressed as end-to-end NUCLEUS compositions.

#### Dimension 7: Contribution History

**Massive contributor** to barraCuda evolution:
- df64 double-precision GPU emulation (benefits any spring needing high precision)
- Multi-GPU metallic dispatch (fleet compute patterns)
- Shader pipeline scaling (benefits neuralSpring multi-stage inference)
- SU(3) matrix math, HMC algorithms, CG solvers
- Precision mixing strategies (`Fp64Strategy`, `FmaPolicy`)
- HPC deployment patterns

hotSpring was responsible for a huge amount of barraCuda's evolution and precision
mixing. This evolutionary debt is well-documented but the absorption needs
verification that all hotSpring-originated math is now available via barraCuda IPC.

---

### 3. wetSpring (V151 — guideStone Level 4+)

**Domain**: Life science, analytical chemistry, biodiversity, pharmacology.

#### Dimension 1: Library-to-Binary Rewiring — Tier 2

- **Local primal dirs**: `barracuda/` (crate `wetspring-barracuda`, ~652 .rs files),
  `metalForge/forge/`
- **barraCuda coupling**: **Heavy**. The largest spring-local barraCuda surface.
  Pervasive `barracuda::` across bio/GPU/validation binaries.
- **IPC surface**: Full `barracuda/src/ipc/` tree — `capability_domains.rs`,
  `compute_dispatch.rs`, `discover.rs`, `dispatch.rs`, `dispatch_strategy.rs`,
  `handlers/` (15 handler modules: science, taxonomy, drug, gonzales, anderson,
  brain, ai, phylogenetics, kinetics, metrics, alignment, data_fetch, vault_ipc,
  expanded), `mcp.rs`, `provenance.rs`, `sweetgrass.rs`, `transport.rs`,
  `resilience.rs`, `stream_item.rs`
- **niche.rs**: Yes — biomeOS socket naming, capability tables, 22 CONSUMED_CAPABILITIES
- **Provenance-specific**: `ipc/provenance.rs`, `ipc/sweetgrass.rs`,
  `provenance_registry.rs`, `provenance.rs`, `vault/provenance.rs`

**Rewiring path**: wetSpring has the richest IPC handler surface of any domain
spring, but the bulk math (spectral deconvolution, phylogenetics, peak detection,
statistical clustering) still links barraCuda as a library. The IPC handlers
serve these results over JSON-RPC but the underlying compute is in-process.
Tier 3 expansion means routing each handler's compute through ecobin barraCuda.

#### Dimension 2: Deploy Graphs — 7 TOMLs

`wetspring_deploy.toml`, `wetspring_science_nucleus.toml`, `wetspring_niche.toml`,
`wetspring_gonzales_exploration.toml`, `wetspring_anderson_atlas.toml`,
`wetspring_basement_deploy.toml`, `wetspring_science_facade.toml`

Good coverage. Anderson atlas and Gonzales exploration graphs tie to specific
science papers.

#### Dimension 3: Provenance — Strong

Dedicated `ipc/provenance.rs` + `ipc/sweetgrass.rs` + `provenance_registry.rs`.
Multiple provenance touchpoints across the IPC tree. Vault storage with
provenance tagging.

#### Dimension 4: petalTongue — Partial

wetSpring is referenced in petalTongue integration docs for scatter/spectrum
channels, but dedicated DataBinding wiring is partial.

**Vision**: `spectrum` for spectral deconvolution (the deconvolution IS the
figure), `timeseries` for sensor streams / growth curves, `scatter` for PCoA
biodiversity ordination, `distribution` for statistical clustering results,
`heatmap` for microbiome abundance matrices. Live lab: the sensor stream IS the
dashboard.

#### Dimension 5: sweetGrass — Partial

`ipc/sweetgrass.rs` exists. Provenance sessions are tracked. Braid creation
is referenced but end-to-end experiment braiding is not fully wired.

#### Dimension 6: Paper Expression

Richest paper portfolio: 15+ baseCamp papers including Anderson localization
framework, Gonzales pharmacology, sub-theses on LTEE/bioag/Anderson QS,
immunological Anderson, hormesis. 294 experiments. Several deploy graphs
already tie to specific papers (anderson_atlas, gonzales_exploration).

**Gap**: Not all papers have corresponding NUCLEUS composition graphs.

#### Dimension 7: Contribution History

- Spectral analysis algorithms -> barraCuda spectral module
- Peak detection and statistical clustering
- Biodiversity statistics (Shannon, Simpson, PCoA)
- Time-series storage patterns -> NestGate
- Streaming pipeline composition patterns
- NPU/edge dispatch (Akida) patterns -> toadStool
- Sample chain-of-custody -> provenance trio patterns

---

### 4. neuralSpring (V138 — guideStone Level 3)

**Domain**: ML/AI inference, transformer architecture, WGSL shader composition.

#### Dimension 1: Library-to-Binary Rewiring — Tier 2

- **Local primal dirs**: No local `barracuda/` directory — main package directly
  depends on `barracuda` from primals. `metalForge/forge/`, `playGround/`.
- **barraCuda coupling**: **Heavy**. Direct `barracuda` dep with rich feature set.
  `barracuda::` pervasive across `src/` and `validate_barracuda_*` binaries.
- **IPC surface**: No `src/ipc/` directory. IPC in `ipc_dispatch.rs` (Level 5
  JSON-RPC over UDS to barraCuda/toadStool/BearDog/Squirrel) and binary RPC
  (`src/bin/neuralspring_primal/`). Optional `primalspring::` for composition proofs.
- **niche.rs**: Yes — JSON-RPC transitional server, NUCLEUS bonding policy

**Rewiring path**: neuralSpring needs a proper `src/ipc/` directory. The
`ipc_dispatch.rs` module is the seed. Unique challenge: inference pipeline
is latency-sensitive (attention, KV-cache, token generation) so IPC overhead
matters more than in science-batch springs.

#### Dimension 2: Deploy Graphs — 1 TOML

`graphs/neuralspring_deploy.toml`

**Gap**: Only one deploy graph. Needs inference pipeline, training loop, and
model-serving composition graphs.

#### Dimension 3: Provenance — Via ipc_dispatch.rs

Referenced in composition capabilities, but no dedicated provenance module.

#### Dimension 4: petalTongue — Not wired

**Vision**: `heatmap` for attention weight matrices (the attention IS the
interpretability figure), `timeseries` for loss curves / perplexity evolution,
`bar` for token probability distributions, `gauge` for inference throughput.
Live inference: the token generation IS the presentation.

#### Dimension 5: sweetGrass — Not wired

Model provenance (which training data, which weights, which inference results)
is a natural braid target for AI reproducibility.

#### Dimension 6: Paper Expression

15+ baseCamp papers: weight Hamiltonians, information propagation, loss
landscapes, neural PGM, multiagent QS, immunological Anderson. Anderson
localization framework applied to neural network weight transport.

#### Dimension 7: Contribution History

- ML-specific WGSL shaders (tokenizer, attention, KV-cache) -> coralReef
- Transformer shaders (matmul, attention, softmax, gelu) -> barraCuda
- Inference pipeline scheduling patterns -> toadStool
- `inference.*` wire standard -> Squirrel provider registration
- Model routing patterns -> Squirrel discovery

neuralSpring's AI capabilities cross-pollinate every spring via Squirrel.

---

### 5. healthSpring (V59 — guideStone Level 5)

**Domain**: Clinical decision support, compliance, pharmacology, biosignal analysis.

#### Dimension 1: Library-to-Binary Rewiring — Tier 3

- **Local primal dirs**: `ecoPrimal/` (crate `healthspring-barracuda`, ~168 .rs files),
  `metalForge/forge/`, `toadstool/`
- **barraCuda coupling**: **Dual-lane**. `Cargo.toml` explicitly documents library
  vs "primal proof" split with a `primal-proof` feature flag. Heavy `barracuda::`
  and `barracuda-core` deps, but the IPC lane is first-class.
- **IPC surface**: Full `ecoPrimal/src/ipc/` — `barracuda_client.rs`,
  `compute_dispatch.rs`, `data_dispatch.rs`, `inference_dispatch.rs`,
  `lifecycle_dispatch.rs`, `btsp.rs`, `client.rs`, `discover.rs`, `error.rs`,
  `dispatch/` (with handlers). Tower atomic support.
- **niche.rs**: Yes

**Rewiring path**: healthSpring is closest to Tier 4 among domain springs.
The explicit `primal-proof` feature flag shows the dual-lane architecture is
intentional. Expand IPC coverage to match full library surface, then flip the
default from library to IPC-only.

**Standardization**: healthSpring's `primal-proof` feature flag pattern is
valuable — other springs could adopt a similar Cargo feature to gate library
vs IPC-only compilation.

#### Dimension 2: Deploy Graphs — 7 TOMLs

`healthspring_biomeos_deploy.toml`, `healthspring_niche_deploy.toml`,
`healthspring_niche.toml`, `healthspring_biosignal_monitor.toml`,
`healthspring_microbiome_analysis.toml`, `healthspring_patient_assessment.toml`,
`healthspring_trt_scenario.toml`

Strong coverage. Clinical scenarios as deploy graphs.

#### Dimension 3: Provenance — Via ecoPrimal/src/ipc/

Provenance referenced through IPC dispatch tree. Dual-tower architecture
(Tower A: data custody with provenance, Tower B: analytics) is a unique
healthSpring pattern for compliance.

#### Dimension 4: petalTongue — DataChannel wired

healthSpring is referenced as the petalTongue integration exemplar in
wateringHole docs. `DataChannel::*` auto-compile to petalTongue views.

**Vision**: `timeseries` for PK/PD curves, `distribution` for biomarker stats,
`scatter3d` for PCoA microbiome ordination, `heatmap` for drug interaction
matrices, `gauge` for clinical thresholds. Live clinic: the patient assessment
IS the dashboard.

#### Dimension 5: sweetGrass — Partial

Clinical compliance audit trails are a provenance trio use case. HIPAA audit
trail patterns enrich the trio. Not fully wired as experiment braids.

#### Dimension 6: Paper Expression

8+ baseCamp papers: Gonzales pharmacology, C. diff colonization, biosignal
sovereign, low-affinity hormesis, QS gene profiling, Mok analyses. 95
experiments.

#### Dimension 7: Contribution History

- Ionic bond runtime enforcement (MitoBeaconFamily trust) -> BearDog
- Data egress fences -> NestGate access control patterns
- Dual-tower enclave pattern -> BearDog cross-family bonds
- `crypto.sign_contract` capability -> BearDog
- HIPAA audit trail patterns -> provenance trio compliance patterns
- Nuclear genetics isolation proof -> BearDog trust model

healthSpring's compliance work hardens security for every spring.

---

### 6. airSpring (v0.10.0 — guideStone Level 0, PRE-DELTA)

**Domain**: Ecological science, agriculture, IoT sensors, environmental compliance.

#### Dimension 1: Library-to-Binary Rewiring — Tier 2

- **Local primal dirs**: `barracuda/` (crate `airspring-barracuda`, ~225 .rs files),
  `metalForge/forge/`
- **barraCuda coupling**: **Strong mix**. `barracuda::` across eco/GPU modules.
- **IPC surface**: Full `barracuda/src/ipc/` + `src/rpc/` + `src/biomeos/`.
  Modules: `compute_dispatch.rs`, `dispatch_outcome.rs`, `mcp.rs`, `mod.rs`,
  `provenance.rs`, `resilience.rs`, `timeseries.rs`
- **niche.rs**: Yes

**Rewiring path**: airSpring has a good IPC foundation (`ipc/` + `rpc/` +
`biomeos/`) despite being pre-delta on guideStone. The IPC surface already
covers compute dispatch, provenance, and timeseries — expand to cover all
domain math (ET0 calculations, soil moisture models, canopy resistance).

#### Dimension 2: Deploy Graphs — 4 TOMLs

`airspring_eco_pipeline.toml`, `airspring_niche_deploy.toml`,
`airspring_provenance_pipeline.toml`, `cross_primal_soil_microbiome.toml`

Cross-primal soil microbiome graph is notable — ties to wetSpring cross-spring
patterns.

#### Dimension 3: Provenance — ipc/provenance.rs

Dedicated `ipc/provenance.rs` module. Environmental compliance provenance
is a natural fit for measurement attribution.

#### Dimension 4: petalTongue — Not wired

**Vision**: `fieldmap` for ET0/soil moisture spatial grids (the field IS the
figure), `timeseries` for weather station / sensor streams, `heatmap` for
canopy resistance models, `scatter` for crop stress classification, `gauge`
for irrigation thresholds. Live field: the sensor network IS the dashboard.

#### Dimension 5: sweetGrass — Not wired

Environmental compliance measurement attribution is a strong braid use case.

#### Dimension 6: Paper Expression

11 baseCamp papers: ET gold standard, soil moisture validation, yield
validation, forecast scheduling, NPU IoT, NCBI 16S coupling, open data atlas,
cross-spring soil microbiome, immunological Anderson, nucleus deployment.

#### Dimension 7: Contribution History

- PDE solver shaders -> barraCuda
- IoT sensor ingestion patterns -> toadStool edge dispatch
- NPU dispatch (Akida/Coral) composition paths -> toadStool
- Environmental compliance attribution -> provenance trio

---

### 7. groundSpring (V124 — guideStone Level 0, PRE-DELTA)

**Domain**: Geoscience, measurement science, calibration, inverse problems.

#### Dimension 1: Library-to-Binary Rewiring — Tier 1

- **Local primal dirs**: `crates/groundspring/` (optional `barracuda` feature),
  `metalForge/forge/`
- **barraCuda coupling**: **Optional feature gate**. When `barracuda` feature is
  enabled, library-oriented. Unique among springs for making barraCuda optional.
- **IPC surface**: **Minimal**. Single `ipc.rs` entry point, no `src/ipc/` directory.
- **niche.rs**: Yes
- **metalForge**: `metalForge/forge/` with `barracuda` dep (GPU feature)

**Rewiring path**: groundSpring's optional barraCuda feature is architecturally
interesting — it's already structured for conditional compilation. The path is
to expand `ipc.rs` into a proper `src/ipc/` tree and add IPC alternatives for
each barraCuda-feature-gated code path. When all paths have IPC alternatives,
the `barracuda` feature becomes the "library validation" lane and IPC becomes
default.

**Standardization**: groundSpring's optional feature gate for barraCuda is a
pattern other springs could adopt as an intermediate step.

#### Dimension 2: Deploy Graphs — 6 TOMLs

`groundspring_deploy.toml`, `groundspring_nucleus_local.toml`,
`groundspring_nucleus_node.toml`, `groundspring_tower_bootstrap.toml`,
`groundspring_validation.toml`, `groundspring_cross_substrate.toml`

Surprisingly strong graph coverage for a pre-delta spring. nucleus_local,
nucleus_node, and tower_bootstrap show NUCLEUS-aware thinking.

#### Dimension 3: Provenance — Minimal

Primal name constants for trio exist but no dedicated provenance module.
Calibration audit trails are the natural provenance use case.

#### Dimension 4: petalTongue — Not wired

**Vision**: `heatmap` for geospatial data grids, `spectrum` for seismic FFT
analysis (the frequency content IS the figure), `distribution` for
Anderson-Darling / statistical quality checks, `scatter` for inverse problem
parameter estimation, `timeseries` for long-duration calibration records. Live
measurement: the calibration trace IS the verification.

#### Dimension 5: sweetGrass — Not wired

Calibration traceability for metrology is a natural braid — linking measurement
instruments, calibration events, and derived results.

#### Dimension 6: Paper Expression

8 baseCamp papers: Anderson, Bazavov, Dolson, Gonzales, Kachkovskiy, Liu,
Waters analyses. No experiments directory.

#### Dimension 7: Contribution History

- Statistical shader library (Anderson-Darling, WDM) -> barraCuda stats
- Inverse problem solvers -> barraCuda optimize
- Long-duration storage patterns -> NestGate archival
- Calibration traceability -> provenance trio metrology patterns

---

### 8. ludoSpring (V53 — guideStone Level 4, Pure Composition)

**Domain**: Game science, HCI, PCG, engagement metrics, interaction laws.

#### Dimension 1: Library-to-Binary Rewiring — Tier 3

- **Local primal dirs**: `barracuda/` (crate `ludospring-barracuda`, ~108 .rs files),
  `metalForge/forge/`
- **barraCuda coupling**: **Balanced**. Game/engine code uses `barracuda::` for
  tensor math, noise, physics. But IPC layer is first-class with Cargo `ipc`
  feature.
- **IPC surface**: Full `barracuda/src/ipc/` — `composition.rs`, `coralreef.rs`,
  `toadstool.rs`, `nestgate.rs`, `btsp.rs`, `discovery/`, `envelope.rs`,
  `methods.rs`, `handlers/` (delegation, gpu, lifecycle, mcp, neural, science,
  tests). **Covers multiple primals** (barraCuda, coralReef, toadStool, NestGate,
  BearDog) — the broadest multi-primal IPC coverage in any domain spring.
- **Provenance**: Dedicated `ipc/provenance/` with `rhizocrypt.rs`, `loamspine.rs`,
  `sweetgrass.rs`, `mod.rs` — **the only spring with per-trio-primal IPC modules**
- **niche.rs**: Yes

ludoSpring is the **pure composition model** — 12-node cell graph, 30
capabilities, BTSP-enforced, 60Hz tick budget. Its IPC surface is the most
comprehensive and should be the reference implementation for multi-primal wiring.

**Rewiring path**: Expand `ipc` feature coverage until all `barracuda::` math
calls have IPC alternatives, then make `ipc` the default. The 60Hz tick budget
is the hardest constraint — IPC latency must fit within frame time.

**Standardization**: ludoSpring's per-trio-primal IPC modules (`ipc/provenance/
{rhizocrypt,loamspine,sweetgrass}.rs`) should be adopted by all springs.
Multi-primal IPC wrappers for coralReef, toadStool, NestGate are also reference
patterns.

#### Dimension 2: Deploy Graphs — 13 TOMLs

Top-level: `ludospring_deploy.toml`, `ludospring_cell.toml`,
`ludospring_gaming_niche.toml`, `rpgpt_dialogue_engine.toml`,
`rpgpt_compute_engine.toml`.

`composition/` subdirectory (7): `nucleus_game_session.toml`,
`session_provenance.toml`, `engagement_pipeline.toml`, `math_pipeline.toml`,
`science_validation.toml`, `shader_dispatch_chain.toml`,
`game_loop_continuous.toml`.

**Strongest deploy graph coverage** among domain springs. Each composition
aspect (provenance, math, shaders, engagement, game loop) has its own graph.
This is the pattern other springs should follow.

#### Dimension 3: Provenance — Dedicated per-primal modules

`ipc/provenance/{rhizocrypt.rs, loamspine.rs, sweetgrass.rs}` — full trio
wiring with graceful degradation. Session lifecycle (create/save/restore/fork)
tied to provenance. `session_provenance.toml` deploy graph.

**Reference implementation** for the `SPRING_PROVENANCE_TRIO_INTEGRATION_PATTERN`.

#### Dimension 4: petalTongue — game_scene wired

ludoSpring pushes scenes to petalTongue via `game.push_scene`. petalTongue
renders game scenes, TUI.

**Vision**: `game_scene` for live render, `timeseries` for engagement metrics
(Fitts/Hick law validation curves), `gauge` for tick budget (0.6ms target),
`bar` for PCG quality metrics. Live game: the play session IS the experiment.

#### Dimension 5: sweetGrass — Session braids

Session lifecycle braids via provenance modules. Game sessions produce
attribution braids linking player actions, AI decisions, and science
measurements.

#### Dimension 6: Paper Expression

15+ baseCamp papers tied to experiments: noise throughput, tick budget, CPU/GPU
parity, dispatch routing, mixed hardware, nucleus pipeline, raycaster, game
telemetry, doom terminal, roguelike explorer, fishfolk/veloren/abstreet adapters.
101 experiments. The most experiment-dense spring.

**Key**: Paper 26 (`primal_composition_as_scientific_methodology.md`) uses
ludoSpring as its primary worked example — 9 NUCLEUS deploy graphs, composition
recipe, BYOB schema.

#### Dimension 7: Contribution History

- 60Hz composition budget patterns -> biomeOS tick scheduling
- Five-layer validation + guideStone pattern -> primalSpring composition standard
- Session lifecycle (create/save/restore/fork) -> NestGate patterns
- Composition drift detection -> `composition_targets.json` standard
- AI narration under latency -> Squirrel real-time performance
- Game math (Fitts, Hick, Perlin, WFC) -> barraCuda game math module

---

## Cross-Spring Rewiring Standardization

### Patterns to Propagate

| Pattern | Origin | Adopt By |
|---------|--------|----------|
| Per-trio-primal IPC modules (`ipc/provenance/{rhizocrypt,loamspine,sweetgrass}.rs`) | ludoSpring | All springs |
| Multi-primal IPC wrappers (`ipc/{coralreef,toadstool,nestgate}.rs`) | ludoSpring | All springs |
| `primal-proof` Cargo feature flag (library vs IPC compilation) | healthSpring | All springs |
| `composition.rs` dual-lane validation model | hotSpring | All springs |
| `PRIMAL_PROOF_IPC_MAPPING.md` method-by-method IPC surface doc | hotSpring | All springs |
| `primal_bridge.rs` socket scan + `NucleusContext` | hotSpring | All springs |
| Optional `barracuda` feature gate | groundSpring | Springs at Tier 1-2 |
| Rich handler dispatch tree (`ipc/handlers/`) | wetSpring | Springs with diverse domain science |
| Deploy graph per science pipeline (`composition/*.toml`) | ludoSpring | All springs |

### Rewiring Priority Order

1. **ludoSpring** (Tier 3 -> 4): Closest to binary-only. Expand `ipc` feature to
   cover remaining `barracuda::` math. Pure composition model makes this the
   cleanest test case.

2. **healthSpring** (Tier 3 -> 4): `primal-proof` feature flag already gates
   compilation. Expand IPC coverage to match library surface. Compliance
   requirements make binary-only attractive (auditable composition chain).

3. **hotSpring** (Tier 2 -> 3): Has the architecture (`composition.rs`,
   `primal_bridge.rs`, `PRIMAL_PROOF_IPC_MAPPING.md`) but needs a proper
   `src/ipc/` directory. Expand Tier 3 validation coverage. High value: the
   biggest barraCuda contributor validating its own absorption.

4. **wetSpring** (Tier 2 -> 3): Rich IPC handler surface but bulk math is
   library-linked. Route each handler's compute through ecobin barraCuda.

5. **airSpring** (Tier 2 -> 3): Good IPC foundation despite pre-delta. Expand
   to cover all domain math.

6. **neuralSpring** (Tier 2 -> 3): Needs `src/ipc/` directory. Latency-sensitive
   inference pipeline is the unique challenge.

7. **groundSpring** (Tier 1 -> 2): Expand `ipc.rs` into `src/ipc/` tree. Optional
   barraCuda feature is a good starting point.

---

## Per-Spring Evolution Blurbs

Actionable guidance for each spring's local IDE to begin absorbing primalSpring
patterns and moving to a full NUCLEUS composition.

---

### hotSpring — Begin: Create `src/ipc/` and expand Tier 3

You pioneered the rewiring architecture (`composition.rs`, `primal_bridge.rs`,
`PRIMAL_PROOF_IPC_MAPPING.md`). Now consolidate it. Your scattered IPC code
needs a proper home.

**Immediate steps**:
1. Create `barracuda/src/ipc/` directory. Move `primal_bridge.rs` and
   `composition.rs` IPC logic into it. Model the structure on ludoSpring's
   `ipc/` tree (per-primal modules: `barracuda.rs`, `toadstool.rs`,
   `nestgate.rs`, `coralreef.rs`).
2. Create `ipc/provenance/` with per-trio modules (`rhizocrypt.rs`,
   `loamspine.rs`, `sweetgrass.rs`) following ludoSpring's reference.
3. Add a `primal-proof` Cargo feature (from healthSpring's pattern) that gates
   library vs IPC compilation. When enabled, domain physics routes through
   ecobin primals over IPC; when disabled, falls back to in-process library.
4. Expand `PRIMAL_PROOF_IPC_MAPPING.md` — you already have one. Walk each
   `barracuda::` import in the physics modules (df64, SU(3), HMC, CG, EOS)
   and map it to the corresponding barraCuda JSON-RPC method.
5. Wire your first petalTongue DataBinding: stream plaquette convergence as a
   `timeseries` channel. The HMC trajectory IS the figure.
6. Create deploy graphs for your major science pipelines beyond `hotspring_qcd_deploy.toml`.
   Each paper (Chuna gradient flow, Murillo lattice, nuclear EOS) should have its own
   composition graph.

**What you give siblings**: Your dual-lane validation model (`composition.rs`)
and `PRIMAL_PROOF_IPC_MAPPING.md` are the templates every spring should copy.

---

### wetSpring — Begin: Route handler compute through ecobin

You have the richest IPC handler surface of any domain spring (15 handler
modules). But those handlers compute results using in-process `barracuda::` and
then serve them over JSON-RPC. The next step is to route the underlying compute
through ecobin barraCuda over IPC.

**Immediate steps**:
1. Add a `primal-proof` Cargo feature to `wetspring-barracuda/Cargo.toml`
   (from healthSpring's pattern).
2. Create `PRIMAL_PROOF_IPC_MAPPING.md` mapping your domain methods (spectral
   deconvolution, peak detection, statistical clustering, phylogenetics,
   Shannon/Simpson, PCoA) to barraCuda JSON-RPC equivalents.
3. In each IPC handler (`handlers/science.rs`, `handlers/drug.rs`,
   `handlers/gonzales.rs`, etc.), add an IPC-first code path gated by the
   `primal-proof` feature. Compare library vs IPC results for parity.
4. Add per-trio provenance modules following ludoSpring's pattern. You already
   have `ipc/provenance.rs` and `ipc/sweetgrass.rs` — split into
   `ipc/provenance/{rhizocrypt.rs, loamspine.rs, sweetgrass.rs}`.
5. Wire petalTongue DataBindings for your highest-impact science: `spectrum`
   for mass spec, `timeseries` for growth curves, `scatter3d` for PCoA.
6. Your Anderson atlas and Gonzales exploration deploy graphs are strong.
   Ensure each remaining baseCamp paper has a corresponding graph.

**What you give siblings**: Your rich handler dispatch tree (`ipc/handlers/`)
is the template for springs with diverse domain science.

---

### neuralSpring — Begin: Create `src/ipc/` directory

Your IPC surface is a single `ipc_dispatch.rs` file. It needs to become a
proper directory with per-primal modules.

**Immediate steps**:
1. Create `src/ipc/` directory. Move `ipc_dispatch.rs` logic into `ipc/mod.rs`.
   Add per-primal modules: `ipc/barracuda.rs`, `ipc/toadstool.rs`,
   `ipc/squirrel.rs`, `ipc/coralreef.rs`.
2. Create `ipc/provenance/` with per-trio modules.
3. Add a `primal-proof` Cargo feature. Unique challenge: inference pipeline is
   latency-sensitive — attention, KV-cache, token generation. IPC overhead
   matters more here than in science-batch springs. Consider batched IPC calls
   (send full layer computation as one `tensor.matmul` rather than individual ops).
4. Create `PRIMAL_PROOF_IPC_MAPPING.md` mapping transformer ops (matmul,
   attention, softmax, gelu, tokenization) to barraCuda JSON-RPC methods.
5. Wire petalTongue: `heatmap` for attention weights is the highest-visibility
   channel. The attention pattern IS the interpretability figure.
6. Create deploy graphs beyond `neuralspring_deploy.toml` — inference pipeline,
   training loop, and model-serving compositions.

**What you give siblings**: Your Squirrel provider registration pattern gives
every spring AI capabilities. neuralSpring's inference evolution is the
cross-cutting win.

---

### healthSpring — Begin: Expand to Tier 4

You are closest to binary-only among springs that still link barraCuda. Your
`primal-proof` feature flag already gates compilation. Now expand.

**Immediate steps**:
1. Inventory every `barracuda::` call in `healthspring-barracuda` that runs
   under the non-`primal-proof` path. Map each to its IPC equivalent.
2. Expand IPC coverage in `ecoPrimal/src/ipc/barracuda_client.rs` to match
   the full library surface.
3. Run parity tests: library path vs IPC path for all PK/PD modeling,
   biostatistics, and biosignal analysis.
4. When parity is confirmed across all methods, flip the default: make
   `primal-proof` the default feature, library the opt-in fallback.
5. Create per-trio provenance modules in `ecoPrimal/src/ipc/provenance/`.
   Your dual-tower architecture (Tower A custody, Tower B analytics) produces
   unique dual braids — document this pattern.
6. Your DataChannel integration is the ecosystem exemplar. Ensure every
   clinical scenario graph has corresponding petalTongue dashboard definitions.

**What you give siblings**: Your `primal-proof` feature flag pattern is the
single most adoptable innovation — every spring should copy this from your
`Cargo.toml`.

---

### airSpring — Begin: Unpause delta absorption

You have a good IPC foundation (`src/ipc/` + `src/rpc/` + `src/biomeos/`)
despite being pre-delta on guideStone. You are ready to absorb.

**Immediate steps**:
1. Pull latest primalSpring and plasmidBin.
2. Build `airspring_guidestone` binary against a live NUCLEUS using
   `primalspring::composition` API. Target guideStone Level 1 first.
3. Add `primal-proof` Cargo feature to `airspring-barracuda/Cargo.toml`.
4. Create `PRIMAL_PROOF_IPC_MAPPING.md` for your domain: ET0 calculations,
   soil moisture models, PDE solvers, FFT, canopy resistance.
5. Expand `ipc/provenance.rs` into per-trio modules. Your environmental
   compliance use case is a natural fit — measurement attribution for
   regulatory auditors.
6. Wire petalTongue: `fieldmap` is the perfect channel for ET0 spatial grids
   and soil moisture maps. The field grid IS the irrigation recommendation.
7. Your `cross_primal_soil_microbiome.toml` deploy graph is notable — expand
   this cross-spring pattern.

**What you give siblings**: Your IoT sensor ingestion and NPU dispatch patterns
inform toadStool and fieldMouse. Your compliance provenance enriches the trio.

---

### groundSpring — Begin: Expand `ipc.rs` into `src/ipc/`

You have the most minimal IPC surface but a valuable architectural pattern:
barraCuda is an optional Cargo feature. Start from there.

**Immediate steps**:
1. Create `crates/groundspring/src/ipc/` directory. Move `ipc.rs` logic into
   `ipc/mod.rs`. Add per-primal modules.
2. Pull latest primalSpring and plasmidBin.
3. Build `groundspring_guidestone` binary against a live NUCLEUS. Target
   guideStone Level 1.
4. Create `PRIMAL_PROOF_IPC_MAPPING.md` for your domain: FFT, matrix
   decomposition, Anderson-Darling, WDM, inverse problem solvers.
5. Add per-trio provenance modules. Calibration traceability is your unique
   contribution — linking instrument serial numbers, calibration standards,
   and derived measurements into metrological braids.
6. Wire petalTongue: `spectrum` for seismic FFT and `fieldmap` for geospatial
   grids are your primary channels.
7. Your 6 deploy graphs (`nucleus_local`, `nucleus_node`, `tower_bootstrap`,
   `validation`, `cross_substrate`, `deploy`) are surprisingly strong for
   pre-delta — they show NUCLEUS-aware thinking. Build guideStone to validate them.

**What you give siblings**: Your optional `barracuda` feature gate is a
transitional pattern for Tier 1-2 springs. Your statistical shader library
(Anderson-Darling, WDM) benefits every spring with data quality needs.

---

### ludoSpring — Begin: Reach Tier 4

You are the pure composition model and the closest to binary-only. Your
per-trio-primal IPC modules are the reference implementation for the ecosystem.

**Immediate steps**:
1. Inventory remaining `barracuda::` calls not gated by the `ipc` feature.
   These are the final rewiring targets.
2. For each, add the IPC equivalent in the appropriate `ipc/*.rs` module.
   Run parity validation (Python -> Rust library -> IPC composition).
3. When all math calls have IPC alternatives, make `ipc` the default feature.
   Verify 60Hz tick budget still holds — IPC latency must fit within 16.6ms
   frame time (current game.tick is 0.6ms, well within budget).
4. Your provenance modules (`ipc/provenance/{rhizocrypt,loamspine,sweetgrass}.rs`)
   are already operational. Ensure every experiment creates a braid.
5. Extend petalTongue beyond `game_scene` — add science metric dashboards
   (`timeseries` for engagement, `gauge` for tick budget, `heatmap` for
   player action distribution).
6. Your `composition/*.toml` deploy graph pattern (7 graphs for different
   composition aspects) is the gold standard. Document it as a template for
   sibling springs.

**What you give siblings**: Everything. Per-trio IPC modules, multi-primal
wrappers, composition deploy graphs, pure composition model, 60Hz tick-budget
proof. ludoSpring is the worked example for Paper 26 and the reference
implementation for NUCLEUS spring composition.

---

## NUCLEUS Composition Gaps Exposed

| Gap | Springs Affected | Blocked By |
|-----|-----------------|------------|
| No standard `src/ipc/` directory structure | hotSpring, neuralSpring, groundSpring | Adoption of ludoSpring/wetSpring pattern |
| No `primal-proof` feature flag | All except healthSpring | Cargo.toml evolution |
| No per-method IPC mapping doc | All except hotSpring | `PRIMAL_PROOF_IPC_MAPPING.md` adoption |
| Deploy graphs don't cover all science pipelines | hotSpring (1), neuralSpring (1) | Graph authoring |
| petalTongue DataBinding not wired | hotSpring, neuralSpring, airSpring, groundSpring | Channel type mapping + IPC |
| sweetGrass braids not wired to experiments | hotSpring, neuralSpring, airSpring, groundSpring | Provenance module adoption |
| metalForge -> toadStool capability profiles | All springs with metalForge | toadStool dispatch contract refinement |

---

**License**: AGPL-3.0-or-later
