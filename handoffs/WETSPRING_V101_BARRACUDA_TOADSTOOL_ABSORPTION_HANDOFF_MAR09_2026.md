# wetSpring V101 → barraCuda / toadStool Absorption Handoff

**Date:** March 9, 2026
**From:** wetSpring V101 (ecoPrimals life science Spring)
**To:** barraCuda team, toadStool team
**License:** AGPL-3.0-or-later
**Status:** 9,060+ checks ALL PASS, 1,399 tests, 334 experiments, 313 binaries

---

## Executive Summary

wetSpring is **fully lean** — zero local WGSL, zero local ODE derivative math,
zero local regression math. All science compute flows through `barraCuda`
primitives (150+ consumed), all hardware dispatch flows through `toadStool`
patterns. This handoff documents what wetSpring learned, what it needs next,
and what should be absorbed upstream.

**Key numbers:**
- 47 CPU bio modules, 47 GPU bio modules (all lean or compose)
- 52 papers reproduced with full three-tier controls (CPU + GPU + metalForge)
- 13 petalTongue visualization scenario builders
- 164 named tolerance constants
- 5 ODE systems using `BatchedOdeRK4<S>::generate_shader()`
- Zero local WGSL, zero unsafe code, zero clippy warnings

---

## Part 1: barraCuda Primitive Consumption Map

### Primitives Consumed (150+)

wetSpring consumes barraCuda primitives at three levels:

#### Level 1: Direct GPU Primitives (always-on, 27 lean modules)

| barraCuda Primitive | wetSpring Module | Domain | Exp |
|---------------------|-----------------|--------|-----|
| `FusedMapReduceF64` | `diversity_gpu` | Shannon, Simpson, Pielou, Chao1 | 004,016 |
| `BrayCurtisF64` | `diversity_gpu` | β-diversity | 004,016 |
| `BatchedEighGpu` | `pcoa_gpu` | PCoA ordination | 016 |
| `GemmF64` | `gemm_cached` | Spectral cosine (926×) | 016 |
| `SmithWatermanGpu` | `alignment` | Banded local alignment | 044 |
| `HmmBatchForwardF64` | `hmm_gpu` | Forward/Viterbi/posterior | 047 |
| `FelsensteinGpu` | `felsenstein` | Phylogenetic pruning | 046 |
| `GillespieGpu` | `gillespie` | Stochastic SSA | 044 |
| `TreeInferenceGpu` | `decision_tree` | PFAS ML | 044 |
| `RfBatchInferenceGpu` | `random_forest_gpu` | RF ensemble | 063 |
| `Dada2EStepGpu` | `dada2_gpu` | Amplicon denoising | — |
| `AniBatchF64` | `ani_gpu` | Nucleotide identity | 058 |
| `DnDsBatchF64` | `dnds_gpu` | Selection pressure | 058 |
| `PangenomeClassifyGpu` | `pangenome_gpu` | Gene classification | 058 |
| `KmerHistogramF64` | `kmer_gpu` | K-mer counting | 081 |
| `UniFracPropagateF64` | `unifrac_gpu` | Phylo diversity | 082 |
| `QualityFilterGpu` | `quality_gpu` | FASTQ QC | — |
| `BatchTolSearchF64` | `tolerance_search` | m/z search | 016 |
| `SparseGemmF64` | Track 3 | Drug repurposing CSR | 161 |
| `TranseScoreF64` | Track 3 | KG embedding | 161 |
| `TopK` | Track 3 | Drug-disease ranking | 161 |
| `PeakDetectF64` | `signal_gpu` | Peak detection | — |
| `KrigingF64` | `kriging` | Spatial interpolation | 087 |
| `WeightedDotF64` | `eic_gpu` | EIC extraction | 087 |
| `SnpBatchF64` | `snp_gpu` | SNP calling | 058 |
| `RarefactionBatchF64` | `rarefaction_gpu` | Rarefaction curves | — |
| `BatchedOdeRK4F64` | `ode_sweep_gpu` | ODE parameter sweep | 049 |

#### Level 2: Trait-Generated GPU (5 ODE systems, Write → Lean)

| ODE System | Struct | Vars | Params | Parity |
|------------|--------|:----:|:------:|--------|
| Phage Defense | `PhageDefenseOde` | 4 | 11 | Derivative-exact |
| Bistable | `BistableOde` | 5 | 21 | Exact (0.00) |
| Multi-Signal | `MultiSignalOde` | 7 | 24 | Exact (4.44e-16) |
| Cooperation | `CooperationOde` | 4 | 13 | Exact (4.44e-16) |
| Capacitor | `CapacitorOde` | 6 | 16 | Exact (0.00) |

These use `BatchedOdeRK4<S>::generate_shader()` — no local WGSL.

#### Level 3: CPU Math Delegation

| barraCuda Function | wetSpring Usage |
|--------------------|----------------|
| `stats::diversity::{shannon, simpson, chao1, pielou}` | All diversity math |
| `stats::{mean, std_dev, percentile, norm_cdf}` | Statistical analysis |
| `stats::fit_linear` | Heap's law, rarefaction |
| `linalg::nmf` | Non-negative matrix factorization |
| `linalg::ridge` | ESN readout, regression |
| `numerical::ode_bio::*Ode::cpu_derivative` | 5 ODE RHS functions |
| `special::{erf, ln_gamma, regularized_gamma}` | Statistical functions |
| `spectral::{anderson_3d, lanczos, lanczos_eigenvalues}` | Anderson spectral |
| `linalg::{lu_solve, qr_solve, cholesky_solve}` | Linear systems |
| `graph_laplacian` | Community network analysis |

#### Level 4: Compose (7 modules wiring upstream primitives)

| Module | Pattern |
|--------|---------|
| `kmd_gpu` | Element-wise KMD via `FusedMapReduceF64` |
| `merge_pairs_gpu` | Overlap scoring via `FusedMapReduceF64` |
| `robinson_foulds_gpu` | Bipartition via `PairwiseHammingGpu` |
| `derep_gpu` | Parallel hashing via `KmerHistogramGpu` |
| `neighbor_joining_gpu` | GPU distance + CPU NJ loop |
| `reconciliation_gpu` | Batch workgroup-per-family |
| `molecular_clock_gpu` | Relaxed rates via `FusedMapReduceF64` |

---

## Part 2: Three-Tier Paper Controls

Every paper in wetSpring's queue passes through a full control chain.
This verifies that open data + open systems produce the same scientific
conclusions regardless of compute substrate.

### Control Architecture

```
Paper equations (published)
  → Python baseline (57 scripts, SHA-256 integrity)
    → barraCuda CPU (Rust, pure math, EXACT_F64 parity)
      → barraCuda GPU (GPU ↔ CPU within named tolerances)
        → Pure GPU streaming (zero CPU round-trips, 441-837×)
          → metalForge mixed hardware (CPU = GPU = NPU output)
            → biomeOS/NUCLEUS orchestration (IPC, deploy graph)
              → petalTongue visualization (scenario → DataChannel → render)
```

### Control Coverage Matrix

| Tier | Experiments | Checks | Status |
|------|:-----------:|:------:|--------|
| Paper math control | Exp291,313 | 77 | ALL PASS |
| Python baselines | 57 scripts | — | SHA-256 verified |
| barraCuda CPU (v1–v25) | Exp035→323 | 546/546 | EXACT_F64 |
| barraCuda GPU (v1–v14) | Exp064→324 | 1,783+ | Within tolerance |
| Pure GPU streaming (v1–v11) | Exp072→317 | 252+ | Zero round-trips |
| metalForge (v1–v17) | Exp060→326 | 243+ | Substrate-independent |
| NPU reservoir (ESN→int8→Akida) | Exp114-119 | 59 | Classification preserved |
| biomeOS/NUCLEUS IPC | Exp203-208,321-322 | 385 | JSON-RPC fidelity |
| petalTongue visualization | Exp327-334 | 251 | Schema validated |
| **Total** | | **9,060+** | **ALL PASS** |

### Open Data Verification

All 52 paper reproductions use publicly accessible data:
- **NCBI SRA**: PRJNA488170, PRJNA382322, PRJNA1114688, PRJNA283159, PRJEB5293
- **Zenodo**: 14341321 (Jones PFAS library)
- **Published model equations**: ODE parameters from peer-reviewed papers
- **MassBank, EPA, Michigan EGLE**: Spectral and environmental data
- **repoDB**: 1,571 drugs × 1,209 diseases (open dataset)
- **Synthetic at NCBI-realistic scale**: For GPU hypothesis testing

No proprietary data. No cloud dependencies. Zero external API requirements
for core science (NCBI optional, NestGate sovereign fallback).

---

## Part 3: What barraCuda Should Absorb

### Visualization Schema Types

wetSpring evolved `petalTongue` integration types that should move upstream:

| Type | Location | Why Upstream |
|------|----------|-------------|
| `DataChannel` (7 variants) | `visualization/types.rs` | Universal visualization data container — all Springs need it |
| `EcologyScenario` | `visualization/types.rs` | Graph-based scenario schema |
| `ScenarioNode` / `ScenarioEdge` | `visualization/types.rs` | Node/edge graph model |
| `StreamSession` | `visualization/stream.rs` | Progressive rendering lifecycle |
| `VisualizationAnnouncement` | `visualization/capabilities.rs` | Songbird discovery for viz |
| `PetalTonguePushClient` | `visualization/types.rs` | IPC push to petalTongue |

**Recommendation:** Move `DataChannel`, `EcologyScenario`, `ScenarioNode`,
`ScenarioEdge`, and `PetalTonguePushClient` into `barracuda::visualization`
as shared types. Each Spring keeps its own scenario builders but the schema
types are universal.

### Scenario Builder Patterns

wetSpring's 13 scenario builders follow a consistent pattern that could
inform a `barracuda::visualization::ScenarioBuilder` trait:

```rust
fn scenario(data: &DomainResult) -> (EcologyScenario, Vec<ScenarioEdge>) {
    let mut s = scaffold("Title", "Description");
    let mut node = node("id", "label", "type", &["capabilities"]);
    node.data_channels.push(timeseries(...));
    node.data_channels.push(heatmap(...));
    s.nodes.push(node);
    (s, vec![])
}
```

The builder helpers (`node`, `scaffold`, `timeseries`, `heatmap`, `bar`,
`gauge`, `scatter`, `distribution`, `spectrum`) are reusable across Springs.

### Tolerance Patterns

wetSpring's 164 named tolerances follow a hierarchy that could inform
a `barracuda::tolerances` evolution:

| Category | Count | Examples |
|----------|:-----:|---------|
| GPU vs CPU | 23 | `GPU_VS_CPU_SHANNON`, `GPU_VS_CPU_FELSENSTEIN` |
| Python vs Rust | 12 | `PYTHON_CHAO1`, `PYTHON_ODE_SWEEP` |
| Analytical | 8 | `EXACT`, `EXACT_F64` |
| Domain-specific | 45 | `NANOPORE_SIGNAL_SNR`, `NMF_CONVERGENCE_RANK_SEARCH` |
| Instrument | 6 | `PFAS_PPM_5`, `ASARI_MZ_TOLERANCE` |
| Bio module | 70 | per-module constants with scientific justification |

### IPC Handler Patterns

wetSpring's IPC science handlers demonstrate a pattern for other Springs:

```rust
pub fn handle_diversity(params: Value, viz: bool) -> Result<Value> {
    let counts = extract_counts(&params)?;
    let result = compute_diversity(&counts);
    if viz {
        let scenario = ecology_scenario(&[counts], &labels);
        push_scenario_best_effort(&scenario);
    }
    Ok(json!({"shannon": result.shannon, "scenario": scenario_json}))
}
```

The `visualization: bool` flag pattern lets petalTongue opt-in to
visualization without breaking existing IPC consumers.

---

## Part 4: What toadStool Should Know

### metalForge Evolution

The `metalForge/forge/` crate (v0.3.0) is the absorption seam for
toadStool hardware dispatch:

| Module | Purpose | Absorption Path |
|--------|---------|----------------|
| `probe` | GPU (wgpu) + CPU (`/proc`) + NPU (`/dev`) | → `toadstool::discovery` |
| `inventory` | Unified substrate view | → `toadstool::inventory` |
| `dispatch` | Capability-based workload routing | → `toadstool::dispatch` |
| `streaming` | Multi-stage GPU pipeline analysis | → `toadstool::pipeline` |
| `bridge` | forge ↔ barracuda device bridge | Integration point |
| `visualization` | petalTongue scenario builders | Spring-local |

**Dispatch routing pattern** that toadStool should understand:

```rust
let workload = BioWorkload::new("diversity", ShaderOrigin::Absorbed)
    .with_data_bytes(10_000_000);  // bandwidth hint

match dispatch::route(&inventory, &workload) {
    Target::Gpu(device) => { /* GPU path */ }
    Target::Npu(device) => { /* NPU bypass, 0 CPU round-trips */ }
    Target::Cpu => { /* CPU fallback */ }
}
```

### NUCLEUS Integration

wetSpring validates Tower→Node→Nest atomics through biomeOS IPC:

| Atomic | What wetSpring Tests | Experiments |
|--------|---------------------|:-----------:|
| Tower | Multi-GPU discovery (3 GPUs), bandwidth-aware routing | Exp269,326 |
| Node | Node-level health, CPU fallback, Songbird discovery | Exp266,321 |
| Nest | Sovereign fallback, deploy graph, capability registry | Exp270,322 |

**Deploy graph:** `phase2/biomeOS/graphs/wetspring_deploy.toml`

### Bandwidth-Aware Routing

wetSpring wired `BioWorkload.data_bytes` for bandwidth-aware dispatch:

| Workload | Data Size | Routing |
|----------|----------|---------|
| kmer | 10 MB | GPU (PCIe bandwidth check) |
| smith_waterman | 50 MB | GPU (large alignment batches) |
| pcoa | 8 MB | GPU (distance matrix eigendecomposition) |
| dada2 | 100 MB | GPU (streaming pipeline preferred) |

---

## Part 5: Lessons Learned for Upstream Evolution

### 1. `FitResult` Named Accessors

wetSpring initially used `fit_result.params[0]` for slope — error-prone.
After barraCuda added `.slope()` and `.intercept()`, all call sites
migrated. **Recommendation:** Continue adding named accessors to
result types (`NmfResult`, `ForwardResult`, etc.).

### 2. ODE `generate_shader()` Pattern

The trait-based WGSL generation (`OdeSystem` trait → `generate_shader()`)
eliminated all local WGSL for ODE systems. This pattern should be
generalized: any domain where the shader structure is fixed but
the equations change should use trait-generated WGSL.

### 3. Precision Routing

wetSpring's GPU modules use `compile_shader_universal(source, Precision::F64)`
via `GpuF64::fp64_strategy()`. The `Fp64Strategy::Hybrid` path (DF64 on
consumer GPUs with limited FP64 units) works correctly for all bio
workloads. Key tolerance finding: Shannon/Simpson GPU parity is within
`1e-10`, ODE sweep parity within `1e-1` (chaotic sensitivity).

### 4. Cross-Spring Primitive Flow

wetSpring consumes primitives from all 5 Springs via barraCuda:

```
hotSpring → DF64, Anderson spectral, ESN, RK4/RK45, erf
wetSpring → diversity, HMM, Felsenstein, DADA2, Gillespie, SW
neuralSpring → graph Laplacian, pairwise Hamming/Jaccard, batch fitness
groundSpring → bootstrap, jackknife, regression
airSpring → 6 ET₀ methods, Penman-Monteith
```

This validates the biome model: Springs don't import each other,
they all lean on barraCuda independently.

### 5. StreamSession for Progressive Rendering

The `StreamSession` lifecycle (open → push → close) allows long-running
computations to stream intermediate results to petalTongue. This
pattern should be generalized in barraCuda for any Spring that does
multi-stage computation.

### 6. Songbird Capability Discovery

wetSpring announces 16 visualization capabilities via Songbird. The
announcement struct includes `supports_streaming: true` and lists
all 7 `DataChannel` types. This pattern enables petalTongue to
auto-discover what any Spring can render.

---

## Part 6: biomeOS / Atomic Graph Integration

### IPC Contract

wetSpring exposes these JSON-RPC 2.0 methods:

| Method | Description | Visualization |
|--------|-------------|:------------:|
| `health` | Primal health check | — |
| `science.diversity` | α/β diversity | Optional |
| `science.qs_model` | QS ODE simulation | — |
| `science.anderson` | Anderson spectral analysis | — |
| `science.ncbi_fetch` | NCBI data acquisition | — |
| `science.full_pipeline` | Full 16S pipeline | Optional |
| `brain.observe` | Bio brain observation | — |
| `brain.attention` | Attention state query | — |
| `brain.urgency` | Urgency assessment | — |

### Deploy Graph

The biomeOS deploy graph (`wetspring_deploy.toml`) defines:
- Socket: `$XDG_RUNTIME_DIR/wetspring.sock`
- Capabilities: `["science.diversity", "science.qs_model", ...]`
- Dependencies: `["nestgate"]` (optional, sovereign fallback)
- Health interval: 30s

### Tower/Node Deployment

For multi-node deployment, wetSpring validates:
- GPU discovery across Tower nodes
- NPU→GPU bypass (zero CPU round-trips)
- GPU→CPU fallback when GPU unavailable
- Bandwidth-aware multi-GPU routing
- 8-stage mixed pipeline dispatch
- Full 47-workload catalog routing (45 GPU + 2 CPU-only)

---

## Part 7: Action Items

### For barraCuda Team

1. **Absorb `DataChannel` schema types** — Move 7 channel types to `barracuda::visualization` as shared types for all Springs
2. **Consider `ScenarioBuilder` trait** — Common pattern across all 13 wetSpring builders
3. **`StreamSession` in shared types** — Session lifecycle for progressive rendering
4. **`NmfResult` named accessors** — Follow the `FitResult.slope()` pattern
5. **Tolerance module evolution** — Consider absorbing the hierarchy pattern (GPU vs CPU, Python vs Rust, analytical, domain)
6. **Cross-spring primitive documentation** — Document which primitives each Spring consumes for absorption planning

### For toadStool Team

1. **Absorb metalForge probe/inventory** — `forge::probe` and `forge::inventory` are absorption-ready
2. **Bandwidth-aware dispatch** — Wire `BioWorkload.data_bytes` through dispatch routing
3. **NUCLEUS atomic validation** — wetSpring has 385 IPC checks validating Tower/Node/Nest patterns
4. **Deploy graph standard** — Formalize the TOML deploy graph format from biomeOS
5. **NPU bypass routing** — wetSpring validates NPU→GPU bypass with zero CPU round-trips

### For Both Teams

1. **Open data controls documented** — All 52 papers use open data, verified in `specs/PAPER_REVIEW_QUEUE.md`
2. **Three-tier matrix complete** — 39/39 actionable papers have CPU + GPU + metalForge validation
3. **Cross-spring model validated** — 5 Springs, 150+ primitives, zero cross-imports, all lean on barraCuda
4. **petalTongue integration live** — 13 scenario builders, 7 DataChannel types, StreamSession, Songbird

---

## Validation Summary

| Chain | Experiments | Checks | Status |
|-------|:-----------:|:------:|--------|
| V101 viz evolution | Exp333-334 | 78 | PASS |
| V100 petalTongue + mixed HW | Exp327-332 | 173 | PASS |
| V99 biomeOS/NUCLEUS | Exp321-326 | 166 | PASS |
| V98 full chain | Exp313-318 | 173 | PASS |
| V88 experiment buildout | Exp263-270 | 427 | PASS |
| All time | 334 experiments | 9,060+ | ALL PASS |

---

## Appendix: Experiment Index (V98–V101)

| Exp | Name | Type | Checks |
|-----|------|------|:------:|
| 313 | Paper Math Control v5 | Paper | 32 |
| 314 | barraCuda CPU v24 | CPU | 67 |
| 316 | barraCuda GPU v13 | GPU | 25 |
| 317 | Pure GPU Streaming v11 | Streaming | 25 |
| 318 | metalForge v16 | metalForge | 24 |
| 319 | Cross-Spring Evolution V98+ | Evolution | 52 |
| 320 | Cross-Spring Benchmark | Benchmark | 24 ops |
| 321 | biomeOS/NUCLEUS Integration | Integration | 42 |
| 322 | Cross-Primal Pipeline | Pipeline | 22 |
| 323 | CPU v25 | CPU | 46 |
| 324 | GPU v14 | GPU | 27 |
| 326 | metalForge v17 | metalForge | 29 |
| 327 | petalTongue Viz Schema | Visualization | 45 |
| 328 | CPU vs GPU Parity (Viz) | GPU | 27 |
| 329 | metalForge petalTongue | metalForge | 19 |
| 330 | biomeOS Full Chain | Integration | 34 |
| 331 | Local Evolution | Evolution | 24 |
| 332 | Mixed HW Dispatch | Dispatch | 24 |
| 333 | Viz Evolution | Visualization | 44 |
| 334 | Science-to-Viz Pipeline | Pipeline | 34 |
