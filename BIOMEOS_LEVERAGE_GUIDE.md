<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# biomeOS Leverage Guide — Standalone, Trio, and Ecosystem Compositions

**Date**: March 16, 2026
**Primal**: biomeOS v2.46
**Audience**: All springs, all primals, biomeOS integrators
**Status**: Active

---

## Purpose

This document describes how biomeOS can be leveraged — alone and in
composition with other primals — by springs and ecosystem consumers. Each
primal in the ecosystem produces an equivalent guide. Together, these
guides form a combinatorial recipe book for emergent behaviors.

biomeOS provides **semantic capability routing, lifecycle orchestration,
graph execution (5 coordination patterns), multi-machine federation,
and a typed capability SDK**. It is the conductor of the ecosystem — it
discovers, composes, monitors, and routes without micromanaging any primal.

**Philosophy**: Coordinate by capability, not by name. biomeOS never
calls a primal directly — it resolves a semantic intent to whoever
provides that capability at runtime.

---

## What biomeOS Offers

### Core Capabilities

| Domain | What biomeOS Does | What It Does NOT Do |
|--------|------------------|---------------------|
| **Routing** | Translates 260+ semantic methods across 19 domains to the primal that provides them | Implement any capability itself |
| **Orchestration** | Executes deploy graphs: Sequential, Parallel, ConditionalDag, Pipeline (streaming), Continuous (60 Hz) | Decide what to compute |
| **Lifecycle** | Starts, monitors, auto-resurrects, gracefully shuts down primals | Store state between runs |
| **Federation** | Forms Plasmodium collectives across machines via HTTP JSON-RPC | Provide networking |
| **Discovery** | Resolves capabilities at runtime; env → socket scan → XDG → taxonomy fallback | Announce itself on the network |
| **Typed SDK** | `CapabilityClient` with domain-specific methods for primal-to-primal IPC | Replace raw JSON-RPC (it wraps it) |

### IPC Methods (Semantic Naming)

All methods follow `{domain}.{operation}[.{variant}]` per the
[Semantic Method Naming Standard](./SEMANTIC_METHOD_NAMING_STANDARD.md).

#### Neural API — Capability Routing

| Method | What It Does |
|--------|-------------|
| `capability.call` | Route a semantic request to the provider that handles it |
| `capability.discover` | Find which primal provides a capability domain |
| `capability.register` | Register a new capability provider (springs use this) |
| `capability.list` | List all registered capability domains and providers |
| `capability.providers` | List all providers for a specific capability |
| `capability.route` | Resolve a capability to a primal without calling it |
| `capability.list_translations` | List all 260+ semantic translations |
| `capability.discover_translations` | Find translations for a specific domain |

#### Graph Orchestration (5 Patterns)

| Method | Pattern | What It Does |
|--------|---------|-------------|
| `graph.execute` | Sequential, Parallel, ConditionalDag | Run a deploy graph (steps execute in dependency order) |
| `graph.execute_pipeline` | Pipeline | Streaming execution with bounded mpsc channels between steps |
| `graph.start_continuous` | Continuous | Start a 60 Hz tick loop graph with push events and sensor routing |
| `graph.pause_continuous` | Continuous | Pause without stopping |
| `graph.resume_continuous` | Continuous | Resume paused graph |
| `graph.stop_continuous` | Continuous | Stop and clean up |
| `graph.list` | — | List available deploy graphs |
| `graph.get` | — | Get graph definition |
| `graph.save` | — | Save a new graph |
| `graph.status` | — | Execution status of a running graph |
| `graph.suggest_optimizations` | — | AI-assisted graph optimization suggestions |
| `graph.protocol_map` | — | Show protocol escalation topology |

#### Lifecycle Management

| Method | What It Does |
|--------|-------------|
| `lifecycle.status` | Current ecosystem health, running primals, atomics |
| `lifecycle.get` | Detailed info for a specific primal |
| `lifecycle.register` | Register a primal for lifecycle management |
| `lifecycle.resurrect` | Force restart a primal |
| `lifecycle.apoptosis` | Controlled death of a degraded primal |
| `lifecycle.shutdown_all` | Coordinated graceful shutdown (dependency order) |

#### Protocol Escalation

| Method | What It Does |
|--------|-------------|
| `protocol.status` | Current protocol (JSON-RPC or tarpc) per primal |
| `protocol.escalate` | Upgrade a connection from JSON-RPC to tarpc/bincode |
| `protocol.fallback` | Downgrade back to JSON-RPC |
| `protocol.metrics` | Latency/throughput per protocol per primal |

#### Plasmodium — Multi-Machine Federation

| Method | What It Does |
|--------|-------------|
| `agent.create` | Create a routing context across gates |
| `agent.meld` | Combine capabilities from multiple gates |
| `agent.split` | Distribute a collective across machines |
| `agent.route` | Route a request to the optimal gate |
| `agent.auto_meld` | Automatic capability aggregation |
| `mesh.peers` | Discover federated gates |
| `mesh.health_check` | Cross-gate health probe |

#### Topology & Introspection

| Method | What It Does |
|--------|-------------|
| `topology.get` | Full ecosystem topology graph |
| `topology.primals` | List running primals with capabilities |
| `topology.proprioception` | Self-awareness: what biomeOS knows about itself |
| `topology.metrics` | Aggregate metrics across all primals |

#### Niche Deployment

| Method | What It Does |
|--------|-------------|
| `niche.list` | List available niche templates |
| `niche.deploy` | Deploy a niche from template |

**Transport**: JSON-RPC 2.0 over Unix socket (required), HTTP JSON-RPC
(inter-gate), tarpc/bincode (optional high-performance path).

---

## 1. biomeOS Standalone

These patterns use biomeOS alone — no specific primal required beyond
what biomeOS discovers at runtime.

### 1.1 Capability Routing as a Service

**For**: Any application that speaks JSON-RPC.

An application sends `capability.call("crypto.sign", { message: "..." })`
to the Neural API socket. biomeOS resolves "crypto.sign" → BearDog,
routes the request, and returns the result. The caller never imports
BearDog, never knows BearDog handled it, and never breaks if a different
primal takes over the "crypto" domain.

```
Application → capability.call("crypto.sign", { message: "..." })
  → biomeOS resolves: crypto → BearDog
  → BearDog signs
  → biomeOS returns signature
```

This works for all 260+ semantic translations across 19 capability
domains.

**Per-spring leverage**:

| Spring | Capability Call | What Happens | Novel Use |
|--------|----------------|-------------|-----------|
| wetSpring | `capability.call("storage.put", { data })` | NestGate stores the sequence | Version 16S pipeline outputs with content-addressed hashes |
| airSpring | `capability.call("ai.chat", { prompt })` | Squirrel → Songbird → Ollama | Natural-language irrigation decision from sensor data |
| hotSpring | `capability.call("compute.dispatch", { shader })` | ToadStool → GPU | Offload lattice QCD matrix ops to sovereign GPU stack |
| neuralSpring | `capability.call("crypto.sign", { hash })` | BearDog signs the checkpoint | Signed model checkpoints for reproducibility attestation |
| groundSpring | `capability.call("discovery.find_primals", {})` | Songbird scans the mesh | Auto-discover which compute providers have GPU for tolerance validation |
| healthSpring | `capability.call("dag.create_session", { name })` | rhizoCrypt opens a workspace | Patient data in ephemeral sessions with automatic expiry |
| ludoSpring | `capability.call("visualization.render", { grammar })` | petalTongue renders the frame | 60 Hz game analytics dashboard via Continuous graphs |

### 1.2 Graph Orchestration for Pipelines

**For**: Any spring that needs multi-step workflows without coding the
orchestration logic.

Deploy graphs are TOML files that define capability-call pipelines with
dependency resolution. biomeOS executes them in order, passing outputs
between steps. Five coordination patterns are available:

| Pattern | When To Use | Example |
|---------|------------|---------|
| **Sequential** | Steps have linear dependencies | Experiment → Analyze → Commit |
| **Parallel** | Independent steps that can run concurrently | Fetch weather + Fetch soil + Fetch satellite |
| **ConditionalDag** | Steps with branching logic | If humidity > threshold → irrigate, else → skip |
| **Pipeline** | Streaming data between steps (bounded mpsc channels) | LC-MS peaks → classification → visualization |
| **Continuous** | Long-running 60 Hz tick loops | Game loop, sensor ingestion, live model inference |

```toml
[graph]
name = "irrigation_decision"
pattern = "Sequential"

[[graph.steps]]
name = "fetch_weather"
capability = "ecology"
operation = "et0_pm"

[[graph.steps]]
name = "check_soil"
capability = "ecology"
operation = "soil_moisture"
depends_on = ["fetch_weather"]

[[graph.steps]]
name = "decide"
capability = "ai"
operation = "chat"
depends_on = ["fetch_weather", "check_soil"]
```

Springs define graphs; biomeOS executes them. The spring never
coordinates primals directly.

**Per-spring graph patterns**:

| Spring | Graph Pattern | Topology |
|--------|--------------|----------|
| wetSpring | Pipeline (streaming) | filter → denoise → classify → visualize |
| airSpring | ConditionalDag | sense → if(dry) irrigate else skip → log |
| hotSpring | Parallel + Sequential | 3 parameter sweeps in parallel → merge → visualize |
| neuralSpring | Pipeline (streaming) | data prep → forward → loss → backprop → checkpoint |
| groundSpring | Sequential | raw → bias correction → uncertainty propagation → validate |
| healthSpring | ConditionalDag | PK/PD model → if(out-of-range) alert else continue → dose |
| ludoSpring | Continuous (60 Hz) | input → state update → physics → render → analytics |

### 1.3 Pipeline Streaming (New in v2.43)

**For**: Springs with data-flow pipelines where each step produces a
stream of results.

The `PipelineExecutor` connects steps with bounded `tokio::sync::mpsc`
channels. Each step processes items as they arrive, enabling true
streaming without buffering entire datasets.

```
wetSpring: spectra → peak_detect → classify → visualize
           Each step processes items as they arrive (no full-dataset buffering)
```

Call via:
```
capability.call("graph", "execute_pipeline", {
    name: "wetspring_lc_ms_pipeline",
    params: { sample_id: "field-north-7" }
})
```

biomeOS returns an NDJSON stream of `StreamItem` envelopes:
```json
{"step": "peak_detect", "status": "progress", "data": { "peak": 42.3, "rt": 12.7 }}
{"step": "classify", "status": "progress", "data": { "compound": "PFOA", "confidence": 0.97 }}
{"step": "visualize", "status": "complete", "data": { "session_id": "lc-ms-042" }}
```

### 1.4 Continuous Graph Execution (New in v2.42)

**For**: Long-running processes that need periodic orchestration.

The `ContinuousExecutor` runs deploy graphs on a 60 Hz tick cycle,
broadcasting events via `GraphEventBroadcaster` and `SensorEventBus`.
Springs subscribe to events rather than polling.

**Per-spring Continuous patterns**:

| Spring | Tick Rate | Event Flow |
|--------|-----------|------------|
| ludoSpring | 60 Hz | player input → game state → physics → render → engagement |
| airSpring | 1 Hz | sensor read → ET₀ calc → threshold check → alert if needed |
| hotSpring | 10 Hz | simulation step → field update → visualization push |
| neuralSpring | variable | training batch → loss calc → gradient update → checkpoint |
| healthSpring | 2 Hz | vitals read → PK/PD update → alert if out-of-range |

### 1.5 Runtime Capability Discovery

**For**: Any primal or spring that needs to adapt to what's available.

`capability.discover` returns who provides a domain and what methods
are available. Springs use this to check before calling:

```
capability.discover { domain: "provenance" }
  → { provider: "sweetgrass", methods: ["create_braid", "get_braid", ...] }

capability.discover { domain: "dag" }
  → { provider: "rhizocrypt", methods: ["create_session", "append_vertex", ...] }
```

If a domain is not available (primal not running), biomeOS returns a
structured `DispatchOutcome::MethodNotFound` with code `-32601`. The
spring degrades gracefully instead of crashing.

### 1.6 Structured Error Handling (New in v2.46)

**For**: Springs that need to make intelligent retry decisions.

biomeOS's `DispatchOutcome` separates protocol errors from application
errors. The typed `IpcError` lets callers react:

| Error | Code | Caller Action |
|-------|------|---------------|
| `MethodNotFound` | -32601 | Try alternate primal or degrade |
| `InvalidRequest` | -32600 | Fix request format |
| `ParseError` | -32700 | Fix JSON encoding |
| `ApplicationError` | varies | Log and retry or propagate |
| `Timeout` | — | Retry with backoff |
| `ConnectionFailed` | — | Re-discover the primal socket |

```rust
match client.try_call("compute.dispatch", params).await {
    Ok(result) => process(result),
    Err(IpcError::Timeout { .. }) => retry_with_backoff(),
    Err(IpcError::JsonRpcError { code: -32601, .. }) => try_alternate_provider(),
    Err(e) => log_and_degrade(e),
}
```

### 1.7 Lifecycle Monitoring

**For**: Any system that needs to know what's alive and healthy.

`lifecycle.status` returns the full ecosystem state: which primals are
running, which atomics are composed, which capabilities are available.

```json
{
  "atomics": { "tower": "healthy", "node": "healthy", "nest": "degraded" },
  "primals": { "beardog": "up", "songbird": "up", "nestgate": "restarting" },
  "capabilities": { "crypto": "available", "storage": "degraded" }
}
```

**Per-spring leverage**:
- petalTongue: Dashboard health display from `lifecycle.status`
- skunkBat: Anomaly detection on health pattern changes
- Any spring: "Is my storage provider available?" before committing results
- healthSpring: Auto-pause clinical pipeline if crypto provider is down

### 1.8 Protocol Escalation (JSON-RPC → tarpc)

**For**: Springs with high-throughput IPC needs.

biomeOS supports transparent protocol escalation: start with JSON-RPC
(universal), escalate to tarpc/bincode (high-performance) when both
sides support it. Springs never code for tarpc directly — biomeOS
manages the negotiation.

```
Spring → capability.call (JSON-RPC) → biomeOS detects tarpc support
  → protocol.escalate → tarpc/bincode (10x throughput for binary data)
```

Aligned at tarpc 0.37 with barraCuda and coralReef for GPU stack parity.

---

## 2. biomeOS + Trio Compositions

The **Provenance Trio** (rhizoCrypt + LoamSpine + sweetGrass)
coordinates through biomeOS's Neural API and graph execution:

```
sweetGrass (Attribution)  — who did what, fair contribution
      |
 LoamSpine (Permanence)   — immutable history, certificates
      |
 rhizoCrypt (Working Memory) — ephemeral DAG, dehydration
      |
 biomeOS (Neural API)     — routes, orchestrates, executes graphs
```

### 2.1 biomeOS + rhizoCrypt: Orchestrated Ephemeral Workspaces

**biomeOS routes all `dag.*` calls to rhizoCrypt without the caller
knowing rhizoCrypt exists.**

A spring calls:
```
capability.call("dag", "create_session", { name: "experiment-042" })
```

biomeOS resolves `dag` → rhizoCrypt, connects to rhizoCrypt's socket,
forwards the request, and returns the session ID. The spring imported
zero rhizoCrypt code.

**Why biomeOS matters here**: If rhizoCrypt restarts (auto-resurrection),
biomeOS re-discovers its socket and subsequent calls resume transparently.
The spring never handles reconnection.

**Per-spring DAG patterns**:

| Spring | Session Pattern | Vertices |
|--------|----------------|----------|
| wetSpring | One session per sample run | filter, denoise, classify, annotate |
| neuralSpring | One session per training run | data_prep, forward, loss, backprop, checkpoint |
| healthSpring | One session per patient encounter | intake, vitals, PK/PD, dose_decision, outcome |
| hotSpring | One session per parameter sweep | init, evolve_step (×N), converge, report |
| ludoSpring | One session per game match | start, state_update (×N), end, analytics |
| groundSpring | One session per calibration chain | raw, bias_correct, propagate, validate |
| airSpring | One session per irrigation cycle | sense, compute_et0, decide, actuate, log |

### 2.2 biomeOS + LoamSpine: Permanent Commits via Graph

**biomeOS orchestrates the dehydrate-then-commit pattern as a single
graph execution.**

The `rootpulse_commit.toml` deploy graph encodes the canonical flow:

```
dag.create_session → work → dag.dehydrate → commit.session → provenance.create_braid
```

Springs call:
```
capability.call("graph", "execute", { name: "rootpulse_commit", params: { session_id } })
```

biomeOS runs the full pipeline: rhizoCrypt dehydrates, BearDog signs,
NestGate stores, LoamSpine commits, sweetGrass attributes. One call,
five primals, zero coupling.

### 2.3 biomeOS + sweetGrass: Fair Attribution at Scale

**biomeOS tracks which primals and agents contributed to each graph
execution, feeding metadata to sweetGrass for braid creation.**

Every graph execution records: which steps ran, which primals handled
them, timestamps, input/output hashes. This metadata flows to
sweetGrass as a W3C PROV-O braid — automated attribution for every
orchestrated pipeline.

**Per-spring attribution**:

| Spring | What Gets Attributed |
|--------|---------------------|
| wetSpring | Which researcher's data contributed to this taxonomy |
| neuralSpring | Which training runs influenced this model checkpoint |
| ludoSpring | Which designers contributed to this level's balance |
| healthSpring | Which clinician reviewed this dosing decision |
| airSpring | Which sensor network provided the field data |
| groundSpring | Which calibration standard was used for this measurement |
| hotSpring | Which nuclear data library parameterized this simulation |

### 2.4 biomeOS + Full Trio: The RootPulse Pattern

**The complete provenance-backed workflow, orchestrated end to end.**

```
1. capability.call("dag", "create_session")     → rhizoCrypt
2. (spring does its work, appending vertices)
3. capability.call("graph", "execute", { name: "rootpulse_commit" })
   biomeOS runs:
     a. dag.dehydrate          → rhizoCrypt collapses session
     b. crypto.sign            → BearDog signs the Merkle root
     c. storage.store          → NestGate stores the payload
     d. commit.session         → LoamSpine commits permanently
     e. provenance.create_braid → sweetGrass records attribution
4. Spring receives: { commit_id, braid_id, root_hash }
```

One `graph.execute` call replaces five sequential inter-primal
interactions. The spring never coordinates primals. biomeOS handles
failure, retry, and rollback.

---

## 3. biomeOS + Other Primals

### 3.1 biomeOS + BearDog: Secure Capability Routing

**Every capability call through the Neural API can be transparently
signed and verified.**

biomeOS verifies family lineage before routing sensitive requests.
Primals that share a `.family.seed` are siblings; BearDog validates
this using `lineage.verify_siblings` before allowing cross-primal
communication.

**Novel patterns**:
- **Signed graph execution**: Every deploy graph step produces a signed
  receipt. The sequence of receipts is a cryptographic audit trail.
- **JWT-gated capability access**: BearDog issues JWTs that biomeOS
  validates before routing — per-spring access control over capabilities.
- **Genetic routing**: Dark Forest beacons encrypt capability
  announcements so only family members can discover the ecosystem.

### 3.2 biomeOS + Songbird: Discovery-Driven Orchestration

**biomeOS uses Songbird for all network-level discovery: beacon
exchange, peer finding, mesh status.**

When a new primal starts on the network, Songbird announces it.
biomeOS discovers the announcement, probes the primal's capabilities,
and registers it in the capability graph. No configuration needed.

```
New primal boots → Songbird beacon → biomeOS discovers → capability.register
```

**Novel patterns**:
- **Cross-network graph execution**: A deploy graph that spans two
  machines. biomeOS on machine A discovers machine B's primals via
  Songbird and routes steps to the optimal provider.
- **BirdSong-encrypted coordination**: biomeOS uses BirdSong's
  encrypted beacons for Dark Forest discovery — observers see noise,
  family members see capability announcements.

### 3.3 biomeOS + NestGate: Content-Addressed Pipeline Storage

**biomeOS routes `storage.*` calls to NestGate, enabling deploy graphs
to store intermediate results between steps.**

```toml
[[graph.steps]]
name = "compute_result"
capability = "compute"
operation = "dispatch"

[[graph.steps]]
name = "store_result"
capability = "storage"
operation = "put"
depends_on = ["compute_result"]
input_from = "compute_result"
```

**Novel patterns**:
- **Graph checkpoint/restore**: Long-running graphs store intermediate
  state in NestGate. If a step fails, biomeOS resumes from the last
  stored checkpoint rather than restarting the entire pipeline.
- **Deduplication across springs**: Two springs that produce identical
  intermediate results (same BLAKE3 hash) share storage transparently.
- **Model cache federation**: neuralSpring stores model weights in
  NestGate; biomeOS routes `storage.get` from any gate in the
  Plasmodium collective, downloading from whichever gate has the model.

### 3.4 biomeOS + ToadStool: Compute Scheduling

**biomeOS routes `compute.*` calls to ToadStool, composing compute
dispatches into graph pipelines.**

```
capability.call("compute", "dispatch", { shader: "matmul_f64", inputs: [...] })
  → biomeOS routes to ToadStool
  → ToadStool dispatches to GPU
  → result returned to graph step
```

**Novel patterns**:
- **Fractal compute graphs**: Deploy graphs that recursively decompose
  a problem, dispatch sub-problems to ToadStool in parallel, and
  collect results. biomeOS manages the fan-out/fan-in.
- **Compute-aware scheduling**: biomeOS checks `lifecycle.status` to
  see which Node atomics have GPU availability before routing.
- **PCIe topology-aware placement**: ToadStool S155b exposes switch
  topology. biomeOS routes to the GPU closest to the data for
  lowest-latency dispatch.

### 3.5 biomeOS + Squirrel: AI-Augmented Orchestration

**The AI Bridge routes through biomeOS: Squirrel → Songbird → BearDog
TLS → Cloud/Local AI.**

biomeOS can inject AI steps into any deploy graph:

```toml
[[graph.steps]]
name = "analyze_results"
capability = "ai"
operation = "chat"
depends_on = ["compute_result"]
params = { prompt = "Summarize these results: ${compute_result}" }
```

**Novel patterns**:
- **AI-advised graph execution**: `ai.analyze_graph` inspects a deploy
  graph before execution and suggests optimizations.
- **Feedback loops**: Graph execution results feed back to Squirrel,
  which adjusts parameters for the next run. biomeOS manages the loop.
- **Natural-language orchestration**: Describe what you want in natural
  language; Squirrel translates to a deploy graph; biomeOS executes it.
- **MCP bridging**: Squirrel's MCP server lets external AI tools
  interact with the entire biomeOS ecosystem as tool calls.

### 3.6 biomeOS + petalTongue: Live Ecosystem Visualization

**petalTongue discovers the Neural API and subscribes to ecosystem
events for real-time rendering.**

biomeOS exposes SSE (Server-Sent Events) endpoints for graph execution
progress, primal health changes, and capability registrations.
petalTongue renders these as live dashboards.

```
biomeOS SSE → petalTongue subscribes → Grammar of Graphics rendering
  → topology graphs, health heatmaps, capability flow diagrams
```

**Novel patterns**:
- **Graph execution replay**: biomeOS logs every graph execution.
  petalTongue replays as an animated DAG — useful for debugging.
- **Spring dashboard composition**: Each spring registers custom
  visualization grammars with petalTongue via biomeOS.
- **Continuous graph visualization**: The 60 Hz tick loop pushes
  real-time data that petalTongue renders as live streaming charts.

### 3.7 biomeOS + skunkBat: Anomaly-Monitored Orchestration

**skunkBat monitors biomeOS's capability routing patterns for anomalies.**

**Novel patterns**:
- **Graph execution audit**: skunkBat verifies that every graph
  execution follows the declared dependency order.
- **Capability impersonation detection**: If a rogue process registers
  a capability previously handled by a known primal, skunkBat alerts.
- **Self-healing feedback**: skunkBat → biomeOS → lifecycle.resurrect
  when anomaly patterns suggest a primal is degrading.

### 3.8 biomeOS + barraCuda + coralReef: Sovereign Compute Pipeline

**biomeOS orchestrates the full sovereign GPU stack as a deploy graph.**

```
barraCuda (shader authoring, 806 WGSL shaders)
  → coralReef (WGSL→SPIR-V→native compilation)
  → ToadStool (GPU dispatch via PCIe topology)
  → NestGate (result storage)
```

All at tarpc 0.37. biomeOS routes each step to the correct primal. The
spring that needs GPU compute calls `capability.call("compute", "dispatch")`
and biomeOS handles the entire chain.

### 3.9 biomeOS + sourDough: GenomeBin Distribution

**biomeOS packages itself and the ecosystem as genomeBins via sourDough.**

genomeBin = ecoBin + deployment wrapper. biomeOS's
`biomeos-genomebin-v3` crate produces self-extracting archives that
sourDough distributes. A new machine downloads the genomeBin, extracts
it, and biomeOS bootstraps the entire ecosystem from a single binary.

---

## 4. Novel Spring Compositions

These are higher-order patterns that emerge from biomeOS orchestrating
multiple primals simultaneously.

### 4.1 Cross-Spring Data Pipeline

**Springs**: any two+ springs + biomeOS (graph orchestration)

Springs never import each other's code. biomeOS routes data between
them:

```
wetSpring produces: { schema: "ecoPrimals/time-series/v1", variable: "soil_moisture_vol" }
  → biomeOS routes to airSpring
airSpring consumes: soil moisture → Penman-Monteith ET₀ → irrigation decision
  → biomeOS routes to petalTongue for visualization
```

| Source Spring | Data | Consumer Spring | Via biomeOS |
|---------------|------|-----------------|-------------|
| wetSpring | soil microbiome | healthSpring | gut-soil microbiome correlation |
| airSpring | weather data | hotSpring | environmental correction factors |
| groundSpring | uncertainty bounds | neuralSpring | confidence-weighted training |
| healthSpring | biosignal patterns | ludoSpring | biometric game difficulty adaptation |
| neuralSpring | model predictions | airSpring | ML-guided irrigation scheduling |
| hotSpring | simulation outputs | groundSpring | uncertainty validation targets |
| ludoSpring | player engagement | neuralSpring | DDA model training data |

### 4.2 Provenance-Backed Scientific Pipeline

**Springs**: any + biomeOS + rhizoCrypt + LoamSpine + sweetGrass + BearDog

Every scientific computation becomes a signed, attributed, permanently
committed chain — the "lab notebook that can't lie."

```
graph.execute("rootpulse_science_pipeline"):
  1. dag.create_session     → rhizoCrypt (ephemeral workspace)
  2. capability.call(spring) → spring runs experiment steps
  3. dag.dehydrate          → rhizoCrypt collapses to summary
  4. crypto.sign            → BearDog signs the Merkle root
  5. storage.store          → NestGate stores the payload
  6. commit.session         → LoamSpine commits permanently
  7. provenance.create_braid → sweetGrass records attribution
```

| Spring | What Gets Provenance-Backed |
|--------|---------------------------|
| wetSpring | 16S rRNA taxonomy pipeline (filter → denoise → classify) |
| airSpring | FAO-56 ET₀ computation chain (sensors → Penman-Monteith → decision) |
| hotSpring | Nuclear EOS parameter sweep (HFB → Yukawa → lattice QCD) |
| neuralSpring | Training run (data prep → forward → loss → backprop → checkpoint) |
| groundSpring | Calibration chain (raw → bias correction → uncertainty propagation) |
| healthSpring | Clinical pipeline (PK/PD model → dosing → outcome prediction) |
| ludoSpring | Game session replay (inputs → state transitions → DDA adjustments) |

### 4.3 Federated Multi-Gate Experiment

**Springs**: any + biomeOS + Songbird + Plasmodium

Two labs, each running a NUCLEUS, form a Plasmodium collective.
biomeOS on each gate discovers the other's capabilities. A deploy graph
that spans both gates runs steps on whichever machine has the required
capability.

```
Gate A (basement):  ToadStool (RTX 4070 GPU), NestGate (1TB SSD)
Gate B (NUC):       NestGate (256GB), low-power sensors

graph.execute("federated_soil_analysis"):
  1. airSpring@B → sensor data collection
  2. storage.put@B → NestGate stores raw data
  3. compute.dispatch@A → ToadStool GPU processes
  4. storage.put@A → NestGate stores results
  5. commit.session@A → LoamSpine commits
```

biomeOS handles cross-gate routing transparently.

### 4.4 Streaming Scientific Pipeline (Pipeline + Trio)

**Springs**: any + biomeOS (Pipeline pattern) + Provenance Trio

New in v2.43 — combine streaming pipeline execution with provenance:

```
graph.execute_pipeline("provenance_streaming"):
  1. dag.create_session → rhizoCrypt
  2. spring.process → streaming results (each item is a DAG vertex)
  3. dag.append_vertex → each streaming item recorded
  4. dag.dehydrate → collapse when stream completes
  5. commit.session → LoamSpine commits
```

Each streaming item becomes a vertex in the provenance DAG — you get
item-level provenance for every data point in the pipeline, not just
the final result.

**Per-spring streaming leverage**:

| Spring | Stream Items | Provenance Granularity |
|--------|-------------|----------------------|
| wetSpring | LC-MS peaks | Per-peak identification provenance |
| neuralSpring | Training batches | Per-batch gradient provenance |
| airSpring | Sensor readings | Per-reading calibration provenance |
| healthSpring | Vitals samples | Per-sample clinical provenance |

### 4.5 Real-Time Multi-Spring Dashboard

**Springs**: any combination + biomeOS + petalTongue + Songbird

Multiple springs register capability providers. biomeOS aggregates
their health and output events. petalTongue renders a unified dashboard.

```
groundSpring → soil moisture (ecology palette)
airSpring    → ET₀, vapor pressure (measurement palette)
wetSpring    → community diversity (ecology palette)
healthSpring → patient vitals (health palette)

All flow through biomeOS SSE → petalTongue Grammar of Graphics
```

### 4.6 AI-in-the-Loop Experiment

**Springs**: any + biomeOS + Squirrel + rhizoCrypt

Squirrel observes an experiment session (rhizoCrypt DAG vertices) and
suggests parameter adjustments. biomeOS routes the suggestion back to
the spring, which appends the AI-suggested run as a new DAG branch.

```
graph.execute("ai_experiment_loop"):
  1. Spring appends experiment vertex
  2. ai.analyze → Squirrel inspects results
  3. ai.suggest → Squirrel proposes next parameters
  4. Spring appends AI-suggested vertex (branching the DAG)
  5. Repeat until convergence
```

The DAG preserves both human and AI branches, with sweetGrass
attributing which agent contributed each branch.

**Per-spring AI leverage**:

| Spring | AI Loop Application |
|--------|-------------------|
| neuralSpring | Hyperparameter search with AI-guided exploration |
| healthSpring | Drug dosing optimization (PK/PD model → AI → adjusted dose) |
| ludoSpring | Game difficulty auto-tuning based on player engagement |
| airSpring | Irrigation schedule optimization from weather + soil + AI |
| groundSpring | Uncertainty budget optimization (AI identifies dominant error sources) |
| hotSpring | Nuclear parameter fitting (AI explores the nuclear EOS landscape) |
| wetSpring | Metagenomic classifier selection (AI picks optimal k-mer length) |

### 4.7 Consent-Gated Data Sharing

**Springs**: healthSpring + biomeOS + BearDog + rhizoCrypt

Patient data enters a signed rhizoCrypt session. A researcher requests
access via biomeOS. BearDog verifies lineage. If authorized, biomeOS
routes a Loan slice with time-limited access.

```
1. healthSpring: dag.create_session (patient data, BearDog-signed)
2. Researcher: capability.call("dag", "slice", { mode: "Loan", duration: "7d" })
   → biomeOS checks: researcher lineage verified by BearDog?
   → yes: route to rhizoCrypt, return Loan slice
   → no: reject
3. (7 days later: loan expires)
4. Audit: dag.merkle_proof proves data integrity during loan period
```

### 4.8 Continuous Game + Physics Crossover

**Springs**: ludoSpring + hotSpring + biomeOS (Continuous) + petalTongue

biomeOS runs a Continuous graph at 60 Hz that combines game logic
with real physics simulation:

```
graph.start_continuous("physics_game"):
  tick 1: hotSpring.simulate_step() → particle positions
  tick 1: ludoSpring.update_controls() → player input
  tick 1: petalTongue.render() → combined scene
  tick 2: repeat
```

ludoSpring provides game controls. hotSpring provides real physics.
petalTongue renders both. biomeOS orchestrates the tick loop.
No spring knows about any other spring.

### 4.9 Self-Healing Ecosystem

**Springs**: any + biomeOS (lifecycle) + skunkBat (anomaly)

biomeOS monitors all primal health. When a primal crashes, biomeOS
auto-resurrects it. skunkBat monitors resurrection patterns.

```
ToadStool crashes → biomeOS auto-resurrects → health.check passes
ToadStool crashes again → biomeOS resurrects → skunkBat detects loop
skunkBat: "ToadStool OOM — recommend memory limit increase"
biomeOS: adjust config → restart with new limits
```

---

## 5. Integration Patterns for Springs

### Option A: Typed Capability Client (Recommended, New in v2.46)

The `CapabilityClient` provides domain-specific typed methods. No raw
JSON-RPC needed.

Add to your spring's `Cargo.toml` under an optional feature:

```toml
[dependencies]
biomeos-primal-sdk = { path = "../../phase2/biomeOS/crates/biomeos-primal-sdk", optional = true }

[features]
neural = ["biomeos-primal-sdk"]
```

Then call any capability by domain:

```rust
use biomeos_primal_sdk::prelude::*;

let client = CapabilityClient::discover()?;

// Crypto (routes to BearDog)
let signature = client.crypto_sign(b"experiment-hash").await?;
let valid = client.crypto_verify(b"data", &signature, &pub_key).await?;

// Storage (routes to NestGate)
client.storage_put("experiment-042", &result_bytes).await?;
let data = client.storage_get("experiment-042").await?;

// Compute (routes to ToadStool)
let result = client.compute_execute("matmul_f64", json!({ "a": matrix_a, "b": matrix_b })).await?;

// HTTP (routes to Songbird)
let response = client.http_request("POST", "http://api.example.com/v1/data", None, Some(body)).await?;

// Discovery
let providers = client.discover_capability("compute").await?;

// Health
let status = client.health_check("toadstool").await?;
```

The spring never imports BearDog, NestGate, or any other primal. It
discovers capabilities at runtime. If biomeOS is not running, the call
fails gracefully with `IpcError::ConnectionFailed`.

### Option B: Sync Neural Bridge (Minimal)

For synchronous / non-async code:

```toml
[dependencies]
neural-api-client-sync = { path = "../../phase2/biomeOS/crates/neural-api-client-sync", optional = true }
```

```rust
use neural_api_client_sync::NeuralBridge;

let bridge = NeuralBridge::discover()?;
let result = bridge.capability_call("crypto", "sign", &json!({ "message": "hash" }))?;
```

### Option C: Raw JSON-RPC (Zero dependencies)

For springs that don't want any Rust dependency on biomeOS:

```bash
echo '{"jsonrpc":"2.0","method":"capability.call","params":{"capability":"crypto","operation":"sign","args":{"message":"hash"}},"id":1}' | \
  socat - UNIX-CONNECT:$XDG_RUNTIME_DIR/biomeos/neural-api.sock
```

### Graph-Based Integration

Define a TOML deploy graph:

```toml
[graph]
name = "my_spring_pipeline"
pattern = "Pipeline"

[[graph.steps]]
name = "collect_data"
capability = "ecology"
operation = "soil_moisture"

[[graph.steps]]
name = "analyze"
capability = "ai"
operation = "chat"
depends_on = ["collect_data"]

[[graph.steps]]
name = "commit"
capability = "commit"
operation = "session"
depends_on = ["analyze"]
```

Execute from your spring:

```rust
let client = CapabilityClient::discover()?;
// ... or use NeuralBridge::discover()? for sync
```

### Capability Provider Registration (Spring as Provider)

Springs that expose capabilities register with biomeOS:

```rust
let bridge = NeuralBridge::discover()?;
bridge.capability_call("capability", "register", &json!({
    "domain": "ecology",
    "methods": ["soil_moisture", "et0_pm", "community_diversity"],
    "socket": "/run/user/1000/biomeos/airspring-family123.sock"
}))?;
```

Once registered, any other spring can call
`capability.call("ecology", "soil_moisture")` and biomeOS routes
to your spring.

---

## 6. What biomeOS Does NOT Do

| Concern | Who Handles It |
|---------|---------------|
| Permanent storage | LoamSpine (`commit.*`) |
| Content blob storage | NestGate (`storage.*`) |
| Signing / encryption | BearDog (`crypto.*`) |
| Attribution / provenance | sweetGrass (`provenance.*`) |
| Ephemeral DAG sessions | rhizoCrypt (`dag.*`) |
| Discovery / networking | Songbird (`discovery.*`, `mesh.*`) |
| Compute dispatch | ToadStool (`compute.*`) |
| Visualization | petalTongue (`visualization.*`) |
| AI inference | Squirrel (`ai.*`) |
| Shader authoring | barraCuda (`shader.*`) |
| Shader compilation | coralReef (`compiler.*`) |
| Anomaly detection | skunkBat (`audit.*`) |
| GenomeBin distribution | sourDough (`distribution.*`) |

biomeOS routes to all of these. It implements none of them. This is
fundamental — the conductor does not play the instruments.

---

## See Also

- [rhizoCrypt Leverage Guide](./RHIZOCRYPT_LEVERAGE_GUIDE.md) — ephemeral DAG sessions
- [LoamSpine Leverage Guide](./LOAMSPINE_LEVERAGE_GUIDE.md) — permanent storage and certificates
- [sweetGrass Leverage Guide](./SWEETGRASS_LEVERAGE_GUIDE.md) — attribution and provenance braids
- [petalTongue Leverage Guide](./PETALTONGUE_LEVERAGE_GUIDE.md) — universal user interface
- [ToadStool Leverage Guide](./TOADSTOOL_LEVERAGE_GUIDE.md) — compute and GPU dispatch
- [Squirrel Leverage Guide](./SQUIRREL_LEVERAGE_GUIDE.md) — AI coordination
- [barraCuda Leverage Guide](./BARRACUDA_LEVERAGE_GUIDE.md) — sovereign GPU math
- [coralReef Leverage Guide](./CORALREEF_LEVERAGE_GUIDE.md) — shader compilation
- [Semantic Method Naming Standard](./SEMANTIC_METHOD_NAMING_STANDARD.md) — method naming
- [Primal IPC Protocol](./PRIMAL_IPC_PROTOCOL.md) — transport layer
- [Primal Registry](./PRIMAL_REGISTRY.md) — full primal catalogue

---

**License**: AGPL-3.0-or-later
