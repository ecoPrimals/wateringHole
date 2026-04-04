<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# Leverage Guides — How Springs and Gardens Use Primals

```yaml
Version: 1.0.0
Date: April 4, 2026
Status: Active
```

Leverage guides explain how each primal or spring in the ecoPrimals stack can be used **standalone**, in **pairs/trios** (for example Compute Trio, Provenance Trio, Inference Trio), and in **multi-primal** compositions. They are the combinatorial recipe book for springs and gardens: what each entity provides, which IPC or library surfaces to call, how to integrate without hard coupling, and which patterns recur across domains.

---

## barraCuda

**What it provides:** Sovereign mathematical computation — GPU-accelerated scientific computing via WGSL shaders through wgpu; pure Rust, zero unsafe, zero C app deps. Philosophy: math is universal; the substrate (GPU/CPU/NPU) is a detail. barraCuda owns math; other primals own hardware, network, storage, identity.

**IPC (semantic `{domain}.{operation}`):** ~30 methods; legacy `barracuda.{domain}.{operation}` accepted via `normalize_method()`.

| Method | What it does |
|--------|----------------|
| `primal.info` / `primal.capabilities` | Identity, protocol, advertised methods |
| `capabilities.list` | Ecosystem-standard capability probe |
| `device.list` / `device.probe` | Devices, f64, VRAM |
| `health.liveness` / `readiness` / `check` | Probes (aliases: `ping`, `health`, `status`) |
| `tolerances.get` / `validate.gpu_stack` | Numerical tolerances; GPU validation suite |
| `compute.dispatch` | Named compute operation |
| `tensor.*` | create, matmul, element-wise ops |
| `math.*` / `stats.*` / `noise.*` / `rng.uniform` | Primitives |
| `activation.fitts` / `hick` | Human-factors models |
| `fhe.ntt` / `fhe.pointwise_mul` | FHE ops |

**Transport:** JSON-RPC 2.0 (TCP/Unix, newline-delimited per wateringHole), tarpc/bincode primal-to-primal, dual-transport startup (UDS + TCP).

**Library dependency (examples):**

```toml
barracuda = { path = "../barraCuda/crates/barracuda" }
barracuda = { path = "../barraCuda/crates/barracuda", default-features = false, features = ["gpu"] }
barracuda = { path = "../barraCuda/crates/barracuda", default-features = false }
```

**Precision continuum (15 tiers, direction):**

| Direction | Tiers | Purpose |
|-----------|--------|---------|
| Scale-down | Binary → … → TF32 | Throughput, inference, hashing |
| Baseline | F32 | Universal |
| Scale-up | DF64 → … → DF128 | Science, reference |

`PrecisionBrain` maps `PhysicsDomain` variants to tiers using `HardwareCalibration`.

**Standalone patterns:** Direct `barracuda` crate dependency (full / `gpu` only / CPU-only features). GPU statistics (`bootstrap_ci`, `HistogramGpu`, …), `PrecisionBrain` + 15-tier precision continuum (Binary→DF128), `Xoshiro128StarStar` CPU–GPU PRNG parity, FHE ops (`NttGpu`, `PointwiseMulGpu`), `GpuViewF64` zero-copy pipelines, kinetics/ODE (`gompertz`, `BatchedOdeRK45F64`), typed `BarracudaError` for resilient retries, concurrent async readback (`AsyncReadback`), genomics helpers.

**Compute Trio (barraCuda + coralReef + toadStool):** barraCuda authors WGSL → coralReef compiles to native → toadStool dispatches (VFIO). DF64 sovereign path avoids NVVM/f64 poisoning; compile-once dispatch-many; error-aware trio self-heal (precision fallback, device migration, batch halving).

**Duo / multi-primal (samples):** + bearDog (FHE encrypt→compute→decrypt); + nestGate (cache by content hash); + songBird (distributed compute); + sweetGrass (provenance braids); + squirrel (AI suggests params); + petalTongue (compute → render, shared GPU paths).

**Per-spring table (abbrev):** hotSpring (QCD, MD, Anderson, DF64 path); airSpring (ET₀ batch, Richards, hydrology); wetSpring (diversity, alignment, Gompertz); groundSpring (bootstrap, chi², Lanczos); neuralSpring (GEMM, attention, ESN); healthSpring (PK/PD, VPC, beats); ludoSpring (noise, physics, deterministic RNG).

**Typed JSON-RPC error (ecosystem fault tolerance):**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32000,
    "message": "GPU device lost during readback poll",
    "data": { "variant": "DeviceLost", "context": "poll_until_ready" }
  }
}
```

**Does not:** storage (nestGate), crypto (bearDog), hardware discovery (toadStool), network (songBird), provenance (sweetGrass), UI (petalTongue), orchestration (biomeOS).

---

## biomeOS

**What it provides:** Semantic capability routing (~260+ methods / 19 domains), graph execution (Sequential, Parallel, ConditionalDag, Pipeline streaming, Continuous 60 Hz), lifecycle (start, resurrect, apoptosis, shutdown), federation (Plasmodium), typed `CapabilityClient`. Philosophy: coordinate by capability, not by name.

**Core IPC domains:** `capability.*` (call, discover, register, list, route, translations), `graph.*` (execute, execute_pipeline, continuous start/pause/resume/stop, list, status, suggest_optimizations), `lifecycle.*`, `protocol.*` (escalate JSON-RPC → tarpc), `agent.*` / `mesh.*`, `topology.*`, `niche.*`. **Transport:** Unix socket (required), HTTP inter-gate, tarpc optional. **fieldMouse vs niche:** fieldMouse does not run biomeOS; if biomeOS runs, it is a niche deployment.

**Graph coordination patterns:**

| Pattern | When to use |
|---------|-------------|
| Sequential | Linear step dependencies |
| Parallel | Independent concurrent steps |
| ConditionalDag | Branching logic |
| Pipeline | Streaming steps (bounded mpsc) |
| Continuous | Long-running 60 Hz (or configured) tick loops |

**Structured errors (`DispatchOutcome` / `IpcError`) — examples:**

| Error | Code | Typical caller action |
|-------|------|------------------------|
| `MethodNotFound` | -32601 | Alternate provider / degrade |
| `InvalidRequest` | -32600 | Fix request |
| `ParseError` | -32700 | Fix JSON |
| `Timeout` | — | Backoff retry |
| `ConnectionFailed` | — | Re-discover socket |

**CapabilityClient (sketch):**

```rust
use biomeos_primal_sdk::prelude::*;
let client = CapabilityClient::discover()?;
let signature = client.crypto_sign(b"experiment-hash").await?;
let result = client.compute_execute("matmul_f64", json!({ /* ... */ })).await?;
```

**Standalone:** `capability.call` as generic JSON-RPC router; TOML deploy graphs; PipelineExecutor (bounded mpsc streaming); ContinuousExecutor (60 Hz + events); `DispatchOutcome` / `IpcError` structured errors; lifecycle dashboards; protocol escalation aligned with barraCuda/coralReef tarpc 0.37.

**+ Provenance Trio:** Routes `dag.*` to rhizoCrypt; `rootpulse_commit`-style graphs dehydrate → sign → store → commit → braid; automated attribution metadata to sweetGrass.

**+ other primals:** BearDog (signed graphs, JWT, lineage); Songbird (discovery); NestGate (checkpoints, dedup); ToadStool (compute in graphs, PCIe-aware); Squirrel (AI steps in graphs); petalTongue (SSE dashboards); skunkBat (routing anomalies); barraCuda+coralReef+ToadStool sovereign pipeline; sourDough (genomeBins).

**Integration:** `CapabilityClient` / `NeuralBridge` / raw JSON-RPC; springs register as `capability.register` providers.

**Does not:** permanent storage, blobs, crypto, provenance DAGs, compute math, visualization, AI inference — routes only.

---

## coralReef

**What it provides:** Sovereign GPU shader compilation — WGSL/SPIR-V/GLSL → native binaries (NVIDIA SASS SM70–SM89, AMD GFX1030+), f64 transcendental lowering, zero vendor SDK. coralDriver: DRM ioctl dispatch (VFIO, nouveau, amdgpu, nvidia-drm). Philosophy: compiler is replaceable infrastructure.

**IPC:** `shader.compile.wgsl` / `.spirv` / `.wgsl.multi`, `shader.compile.status` / `capabilities`, `health.*`. Response: native `bytes` + `CompilationInfo` (GPR, shared mem, barriers, workgroup).

**WGSL compile request (conceptual):**

```
shader.compile.wgsl {
  source: "@compute @workgroup_size(256) fn main(...) { ... }",
  target: "sm86",
  fma_policy: "allow_fusion"
}
→ { binary: <SASS bytes>, info: { gpr_count, shared_mem_bytes, barrier_count, workgroup_size } }
```

**Sovereign vs poisoned path (summary):** proprietary naga→SPIR-V→NVVM can poison f64 devices; coralReef direct WGSL→SASS avoids that class of failure.

**Standalone:** Multi-target one request; `fma_policy` (`allow_fusion`, `separate`, …) for reproducibility; capability self-description; SPIR-V/GLSL interop; library `GpuContext::auto()` / `from_vfio()` pipeline (compile → alloc → upload → dispatch → readback).

**Compute Trio:** barraCuda selects WGSL + `Fp64Strategy` → coralReef compiles → toadStool dispatches; `KernelCacheEntry` + `dispatch_precompiled`. NVVM poisoning bypass: WGSL → coralReef → SASS (no proprietary NVVM path).

**+ others:** LoamSpine (compilation anchors), sweetGrass (author/compiler/dispatcher braids), rhizoCrypt (optimization session history), Songbird (discovery), Squirrel (flag tuning), biomeOS (`capability.call`), petalTongue (telemetry viz), skunkBat (determinism anomalies).

**Spring recipe cards (condensed):** hotSpring (GPR/occupancy telemetry); neuralSpring (shader evolution via compile metadata fitness); groundSpring (cross-vendor ULP certification); wetSpring (precision-aware multi-GPU routing); airSpring (JIT Richards with constants folded); healthSpring (FMA-separate regulatory chain); ludoSpring (procedural WGSL as content).

**Does not:** author WGSL (barraCuda), precision policy (barraCuda), hardware discovery (toadStool), storage, crypto, orchestration.

---

## healthSpring

**What it provides:** Human health science — PK/PD, microbiome, biosignal, endocrine, diagnostics. Crate `healthspring-barracuda`; IPC science primal (`science.pkpd.*`, etc.). Philosophy: health science is sovereign; discover and compose.

**Library modules:** `pkpd`, `microbiome`, `biosignal`, `endocrine`, `discovery`, `comparative`, `qs`, `uncertainty` — see original guide for entry points.

**GPU (barraCuda) — 6 ops:**

| healthSpring op | barraCuda op | Feature |
|-----------------|--------------|---------|
| `HillSweep` | `HillFunctionF64` | `barracuda-ops` |
| `PopulationPkBatch` | `PopulationPkF64` | `barracuda-ops` |
| `DiversityBatch` | `DiversityFusionGpu` | `barracuda-ops` |
| `MichaelisMentenBatch` | `MichaelisMentenBatchGpu` | `barracuda-ops` |
| `ScfaBatch` | `ScfaBatchGpu` | `barracuda-ops` |
| `BeatClassifyBatch` | `BeatClassifyGpu` | `barracuda-ops` |

Features: `nestgate`, `sovereign-dispatch` (WGSL → coralReef → native).

**Niche (biomeOS):** 79 capabilities, 6 domain dispatchers, 5 workflow graphs (`patient_assessment`, `trt_scenario`, `microbiome_analysis`, `biosignal_monitor`, `deploy`). petalTongue: `DataChannel`, `HealthScenario`, `ClinicalRange`, `PetalTonguePushClient`.

**Capability snapshot:** PK/PD (`hill_dose_response`, `population_pk`, `nlme_*`, `vpc_simulate`, …), microbiome, biosignal, endocrine, diagnostic, clinical, infra (`provenance.*`, `compute.offload`, `data.fetch`, health probes).

**Cross-spring:** Absorbs barraCuda ops, toadStool/metalForge, hotSpring validator pattern, groundSpring cargo-deny hygiene, wetSpring diversity concepts; contributes WGSL/health primitives upstream.

**Does not (by role):** general orchestration — uses biomeOS graphs; storage/crypto via other primals when composed.

---

## loamSpine

**What it provides:** Selective immutable permanence — append-only hash-chained spines, Loam Certificates (mint/transfer/loan/return), inclusion proofs, `commit.session`, `braid.commit`. Philosophy: ephemeral work earns permanence by consent.

**IPC:** `spine.*`, `entry.*`, `certificate.*`, `slice.*`, `proof.*`, `commit.session`, `braid.commit`, health, `capability.list`; rhizoCrypt-compat `permanent-storage.*` aliases.

**Entry types (selection):**

| Entry type | Purpose |
|------------|---------|
| `Genesis` | Chain start |
| `SessionCommit` | rhizoCrypt dehydration anchor |
| `BraidCommit` | sweetGrass braid anchor |
| `DataAnchor` | Content hash anchor |
| `Certificate*` | Mint / transfer / loan / return |
| `Slice*` | Waypoint slice events |
| `Custom` | `type_uri` + payload |

**Standalone:** Audit logs; certificate lifecycle; inclusion proofs; sealed spines; multi-spine organization; entry types (Genesis, SessionCommit, BraidCommit, DataAnchor, Certificate*, Slice*, …).

**+ Trio:** rhizoCrypt dehydrate → `commit.session`; sweetGrass `braid.commit` → immutable attribution; cross-trio query surface on LoamSpine.

**+ others:** BearDog signed entries; NestGate hash-linked blobs; Songbird spine discovery; petalTongue timelines; ToadStool compute result anchors with hardware id; Squirrel commit analytics; skunkBat chain integrity; coralReef+barraCuda+ToadStool full compute→anchor chain.

**Integration:** `NeuralBridge` / `graph.execute` provenance pipelines; certificate mint/loan examples in original guide.

**Does not:** ephemeral DAG (rhizoCrypt), attribution authoring (sweetGrass), blobs (nestGate), orchestration (biomeOS).

---

## neuralSpring

**What it provides:** ML and spectral **validation harness** — Python baselines ported to Rust+GPU with named tolerances; IPC science services. Philosophy: ML/spectral results are proven, not assumed.

**IPC (examples):** `health*`, `capability.list`, `science.ipr`, `science.disorder_sweep`, `science.spectral_analysis`, `science.anderson_localization`, `science.hessian_eigen`, `science.agent_coordination`, `science.training_trajectory`, `science.evoformer_block`, `science.structure_module`, `science.folding_health`, `science.gpu_dispatch`, `science.cross_spring_provenance`, `science.cross_spring_benchmark`, `science.precision_routing`, `primal.forward`, `data.ncbi_*` / `data.pdb_*` (NestGate).

**Standalone:** Library modules + 130+ tolerance categories; spectral diagnostics (IPR, LSR, phase); Anderson as robustness diagnostic; Dispatcher 44+ ops; coralForge IPC (evoformer/structure); `science.cross_spring_provenance` shader lineage.

**Pairs:** + barraCuda (validate GPU), + toadStool (hardware-aware ML), + coralReef (`validate_sovereign_compile`), + petalTongue (six visualization scenarios), + sweetGrass (braids), + squirrel (NAS / active learning), + biomeOS (DAG pipelines).

**Trios:** Validated compute trio; reproducible ML with sweetGrass+loamSpine; adaptive spectral with squirrel; structure pipeline with barraCuda+coralReef+petalTongue; defended inference with bearDog+skunkBat.

**Does not:** own hardware, compile shaders (validates), store data long-term, encrypt, orchestrate, invent core math (barraCuda).

---

## petalTongue

**What it provides:** Universal UI — Grammar of Graphics, multi-modality (egui, TUI, web, headless, audio, braille, haptics, GPU buffers). SAME DAVE model; provenance per pixel.

**Key methods:**

| Capability | Method | Role |
|------------|--------|------|
| Render | `visualization.render` | DataBindings / spring-native → Grammar of Graphics |
| Scene | `visualization.render.scene` | SceneGraph |
| Stream | `visualization.render.stream` | Incremental updates |
| Dashboard | `visualization.render.dashboard` | Multi-panel layout |
| Export | `visualization.export` | SVG, audio, braille, terminal, GPU, … |
| Validate | `visualization.validate` | Tufte / accessibility preflight |
| Sessions | `visualization.session.list` | Active sessions |
| Interaction | `interaction.subscribe` | Selection/hover/focus events |
| Sensors | `interaction.sensor_stream.subscribe` | Batched sensor events (60 Hz capable) |
| Topology | `visualization.render_graph` | Primal topology art |
| Motor | `motor.*` | Programmatic UI control |
| Provenance | `visualization.showing` | Whether `data_id` is on screen |

**Per-spring:** healthSpring (six DataBinding types wired); hotSpring/wetSpring/airSpring/groundSpring/neuralSpring/ludoSpring mappings and novel patterns (dashboards, streaming, uncertainty overlays); primalSpring validates SSE pipeline (exp043).

**Foundation primals:** BearDog, Songbird, NestGate, Squirrel, ToadStool, biomeOS, coralReef, barraCuda — telemetry and bridge patterns (see original for wiring status).

**Trios:** + Provenance Trio (session → braid → commit); + Compute Trio (heavy viz math on GPU); + Songbird+biomeOS discovery.

**Standalone modes:** `petaltongue ui|tui|web|headless|server|status`.

**Does not:** compute domain science — renders what others send.

---

## primalSpring

**What it provides:** Coordination and **composition validation** — biomeOS and Neural API are the primary subject under test. No barraCuda import; no domain science reproduction.

**Capabilities:** `coordination.deploy_atomic`, `coordination.validate_composition`, `coordination.bonding_test`, `composition.nucleus_health`, `nucleus.start` / `nucleus.stop`.

**Tracks (10):** Atomics, graph patterns, emergent systems (RootPulse, RPGPT, coralForge), bonding/Plasmodium, coralForge as Pipeline neural object, cross-spring, showcase patterns, live composition, multi-node bonding, cross-gate deployment.

**IPC resilience:** `IpcError`, `CircuitBreaker`, `RetryPolicy`, `resilient_call`, `DispatchOutcome`, `extract_rpc_*`, 4-format capability parsing, health/self-knowledge, niche `register_with_target`, deploy graph validation (`graph.list` / `validate` / `waves` / `capabilities`), capability-first discovery.

**How primals benefit (samples):** BearDog ordering; Songbird mesh; ToadStool compute/coralForge; NestGate storage; Squirrel AI; Provenance Trio exp020–022; petalTongue exp043; biomeOS pervasive.

**coralForge:** Validated as emergent graph (`coralforge_pipeline.toml`) — NestGate, neuralSpring, hotSpring, wetSpring, ToadStool — exp025.

**fieldMouse:** exp042 ingestion → NestGate + sweetGrass.

**Does not:** math, GPU shaders, direct NestGate, domain papers.

---

## rhizoCrypt

**What it provides:** Ephemeral content-addressed DAG sessions, Merkle proofs, dehydration to permanence, slice semantics (Copy, Loan, Consignment, Escrow, Mirror, Provenance). Philosophy: ephemeral by default, persistent by consent.

**IPC:** `dag.session.*`, `dag.event.*`, `dag.vertex.*`, `dag.merkle.*`, `dag.slice.*`, `dag.dehydration.*`, health, metrics, `capability.list`; HTTP + tarpc. `niche.rs`: costs/deps for Pathway Learner.

**Slice modes:**

| Mode | Semantics |
|------|-----------|
| Copy | Independent fork |
| Loan | Time-limited read |
| Consignment | Hand off for processing |
| Escrow | Held until conditions |
| Mirror | Live read-only replica |
| Provenance | Audit trail access |

**Standalone:** Experiment tracking; multi-agent concurrent append; dedup; proofs; slice checkout modes.

**+ Trio:** Dehydrate → `commit.session` (LoamSpine); `contribution.record_dehydration` / braids (sweetGrass); RootPulse seven-step graph.

**+ others:** Signed vertices (BearDog); NestGate hash bridge; Songbird session discovery; petalTongue DAG viz; ToadStool substrate tags; Squirrel session analysis; skunkBat anomaly monitoring.

**Integration:** `NeuralBridge` minimal/full; TOML `spring_experiment_commit` style graphs.

**Does not:** permanent ledger (loamSpine), blob vault (nestGate), crypto (bearDog), orchestration (biomeOS).

---

## squirrel

**What it provides:** Sovereign AI coordination — vendor-agnostic routing, context sessions, MCP `tool.execute` / `tool.list`, multi-model workflows, `capabilities.list` for Pathway Learner. DignityEvaluator for AI safety. Manifest: `$XDG_RUNTIME_DIR/ecoPrimals/squirrel.json`.

**IPC:** `ai.query` / `complete` / `chat`, `ai.list_providers`, `capabilities.list` (canonical), `capability.*`, `identity.get`, `context.*`, `system.*`, `discovery.peers`, `tool.*`, `lifecycle.*`, `graph.parse` / `graph.validate`, health probes. JSON-RPC batching; strict validation.

**Inference Trio:** Squirrel + ToadStool + Songbird — local GPU inference, federated discovery, deploy graph ordering.

**+ others:** BearDog authenticated prompts/responses; NestGate context persistence; biomeOS AI graphs; petalTongue NL→grammar; rhizoCrypt DAG analysis; sweetGrass AI agents in braids; LoamSpine permanent AI decisions; skunkBat threat classification; coralReef+barraCuda algorithm **advice** (not execution).

**Patterns:** AI experiment advisor; data marketplace broker; multi-model deliberation; regulatory narrative from spine entries; conversational ecosystem explorer; graph optimization suggestions; cross-spring synthesis.

**Does not:** crypto, storage, transport, GPU dispatch, ledger, provenance authoring, UI, shader compile.

---

## sweetGrass

**What it provides:** W3C PROV-O braids — attribution shares, derivation chains, privacy levels, session compression (0/1/Many), PROV-O export, scyBorg license metadata. Proposed: content convergence (v0.8.x).

**IPC:** `braid.*`, `anchoring.*`, `provenance.*`, `attribution.*`, `compression.*`, `contribution.*`, health, `capability.list`.

**Standalone:** Roles (12) with weights; derivation graphs; GDPR-inspired privacy tiers; economic attribution hooks toward sunCloud.

**+ Trio:** Dehydration attribution; `braid.commit` to LoamSpine; full `provenance_pipeline` graph.

**+ others:** Signed braids (BearDog); NestGate blob linkage; Songbird discovery; petalTongue graph render; ToadStool as compute agent; Squirrel missing-attribution hints; skunkBat integrity; shader chain with barraCuda+coralReef+ToadStool.

**Does not:** ephemeral state (rhizoCrypt), raw ledger mechanics (loamSpine), storage, crypto, compute.

---

## toadStool

**What it provides:** Sovereign compute **infrastructure** — GPU/NPU/CPU discovery, VFIO dispatch, PCIe topology, power states, cross-gate routing, Ollama LLM lifecycle, hardware transport (display, capture, serial), coralReef proxy + naga fallback. Philosophy: hardware as capabilities.

**IPC (samples):** `toadstool.health` / `version` / `query_capabilities`, `compute.discover_capabilities`, `compute.submit` / `status` / `result`, `compute.hardware.*` (observe/distill/apply/auto_init/vfio_devices), `compute.dispatch.*`, `gpu.info` / `gpu.memory`, `ollama.*`, `gate.*`, `transport.*`, `shader.compile.*`, `ecology.*`, `discovery.*`, `ai.nautilus.*`.

**Standalone:** `gpu.info` adaptive algorithms; multi-adapter env `TOADSTOOL_GPU_ADAPTER`; PCIe topology for partitioning; `NpuDispatch` (e.g. Akida); cache-aware tiling table; Ollama load/infer/unload; transport.discover/route (camera→GPU→display).

**Compute Trio:** VFIO isolation; hardware-calibrated precision with barraCuda+coralReef; cross-gate distributed dispatch; hw-learn BAR0 tuning.

**Duos:** bearDog secure enclave; songBird federation; nestGate hardware-indexed cache; squirrel VRAM-aware routing; petalTongue DRM path; biomeOS scheduling; sweetGrass hardware in braids; skunkBat PCIe/BAR0 anomalies.

**Per-spring table:** hotSpring (VFIO QCD, hw-learn); airSpring (sensors, serial, mesh); wetSpring (alignment VRAM, HIPAA isolation); groundSpring (tiling, f64 truth); neuralSpring (VRAM, Ollama, federation); healthSpring (HIPAA enclave); ludoSpring (display/capture/multi-GPU).

**Evolution (summary):** Silicon map (shader cores, NPU, future tensor/RT/TMU…); Phases A–D for VFIO, performance surface, multi-unit routing, mixed command streams; tolerance-based routing with barraCuda/coralReef.

**Does not:** math (barraCuda), compile (coralReef primary), storage, crypto, provenance, UI, AI routing logic (squirrel), orchestration (biomeOS).

---

## wetSpring

**What it provides:** Sovereign **life-science** computation — 16S metagenomics, LC-MS, PFAS, QS models, Anderson spectral, kinetics, alignment, taxonomy, phylogenetics, NMF, NCBI fetch, full 16S pipeline IPC. Heavy barraCuda consumption; 354+ validation binaries.

**IPC (representative):**

| Method | Role |
|--------|------|
| `science.diversity` | Alpha/beta diversity |
| `science.qs_model` | QS biofilm ODE |
| `science.anderson` | Disorder / LSR |
| `science.kinetics` | Biogas kinetics |
| `science.alignment` | Smith–Waterman |
| `science.taxonomy` | k-mer classifier |
| `science.phylogenetics` | RF, placement |
| `science.nmf` | NMF |
| `science.timeseries` | Cross-spring series |
| `science.ncbi_fetch` | NCBI via NestGate |
| `science.full_pipeline` | End-to-end 16S |
| `brain.observe` / `brain.attention` / `brain.urgency` | Nautilus sentinel |
| `ai.ecology_interpret` | Squirrel delegation |
| `provenance.begin` / `record` / `complete` | Session provenance |
| `health.*`, `metrics.snapshot` | Ops |

**Standalone:** `wetspring-barracuda` crate; IPC examples; Validator/`OrExit` pattern; 214 named tolerances.

**+ Trio / foundation:** rhizoCrypt anchors; loamSpine pathway learning; sweetGrass circuit breaker/resilience; barraCuda GPU biology; toadStool `compute.dispatch` + petalTongue streaming; NestGate NCBI tiers; Songbird federated pipeline; BearDog signed results.

**+ petalTongue / Squirrel / biomeOS:** Push client, `EcologyScenario`, niche deploy graphs.

**Cross-spring:** airSpring (soil-water nexus); healthSpring (One Health); hotSpring (extremophiles); groundSpring (bootstrap diversity); neuralSpring (transformer taxonomy); ludoSpring (procedural ecology).

**Science stack (conceptual):** biomeOS → toadStool → barraCuda → wetSpring + NestGate + petalTongue + Squirrel + trio + BearDog + Songbird.

**Does not:** replace orchestration (biomeOS) or storage/crypto primitives when used alone.

---

## Version History

| Version | Date | Notes |
|---------|------|--------|
| 1.0.0 | April 4, 2026 | Initial consolidated document. Merges the thirteen per-entity leverage guides: `BARRACUDA_LEVERAGE_GUIDE.md`, `BIOMEOS_LEVERAGE_GUIDE.md`, `CORALREEF_LEVERAGE_GUIDE.md`, `HEALTHSPRING_LEVERAGE_GUIDE.md`, `LOAMSPINE_LEVERAGE_GUIDE.md`, `NEURALSPRING_LEVERAGE_GUIDE.md`, `PETALTONGUE_LEVERAGE_GUIDE.md`, `PRIMALSPRING_LEVERAGE_GUIDE.md`, `RHIZOCRYPT_LEVERAGE_GUIDE.md`, `SQUIRREL_LEVERAGE_GUIDE.md`, `SWEETGRASS_LEVERAGE_GUIDE.md`, `TOADSTOOL_LEVERAGE_GUIDE.md`, `WETSPRING_LEVERAGE_GUIDE.md`. Substantive detail, tables, and code patterns remain documented in those source files where space requires. |

For full method lists, long examples, experiment IDs, and extended “novel pattern” narratives, refer to the individual guides in this directory.
