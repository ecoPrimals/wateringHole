<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# biomeOS Leverage Guide — Standalone, Trio, and Ecosystem Compositions

**Date**: March 14, 2026
**Primal**: biomeOS v2.38
**Audience**: All springs, all primals, biomeOS integrators
**Status**: Active

---

## Purpose

This document describes how biomeOS can be leveraged — alone and in
composition with other primals — by springs and ecosystem consumers. Each
primal in the ecosystem will produce an equivalent guide. Together, these
guides form a combinatorial recipe book for emergent behaviors.

biomeOS provides **semantic capability routing, lifecycle orchestration,
graph execution, and multi-machine federation**. It is the conductor of
the ecosystem — it discovers, composes, monitors, and routes without
micromanaging any primal.

**Philosophy**: Coordinate by capability, not by name. biomeOS never
calls a primal directly — it resolves a semantic intent to whoever
provides that capability at runtime.

---

## IPC Methods (Semantic Naming)

All methods follow `{domain}.{operation}[.{variant}]` per the
[Semantic Method Naming Standard](./SEMANTIC_METHOD_NAMING_STANDARD.md).

### Neural API — Capability Routing

| Method | What It Does |
|--------|-------------|
| `capability.call` | Route a semantic request to the provider that handles it |
| `capability.discover` | Find which primal provides a capability domain |
| `capability.register` | Register a new capability provider (springs use this) |
| `capability.list` | List all registered capability domains and providers |

### Lifecycle Management

| Method | What It Does |
|--------|-------------|
| `lifecycle.status` | Current ecosystem health, running primals, atomics |
| `lifecycle.start` | Start a primal or atomic by name |
| `lifecycle.stop` | Graceful stop with coordinated shutdown |
| `lifecycle.restart` | Restart a primal, preserving socket registration |
| `health.check` | Per-primal or ecosystem-wide health probe |
| `health.check_all` | Health of every running primal in one call |

### Graph Orchestration

| Method | What It Does |
|--------|-------------|
| `graph.execute` | Run a deploy graph (TOML pipeline of capability calls) |
| `graph.list` | List available deploy graphs |
| `graph.validate` | Dry-run a graph for dependency resolution errors |

### Plasmodium — Multi-Machine Federation

| Method | What It Does |
|--------|-------------|
| `plasmodium.meld` | Combine two NUCLEUS instances into a collective |
| `plasmodium.split` | Distribute a collective across machines |
| `plasmodium.mix` | Redistribute capabilities within a collective |
| `plasmodium.status` | Federation topology, latency, capability map |

### AI Bridge

| Method | What It Does |
|--------|-------------|
| `ai.chat` | Route to Squirrel → Songbird → Cloud/Local AI |
| `ai.analyze_graph` | AI analysis of deploy graph structure |
| `ai.learn_from_event` | Feed graph execution events to AI for learning |
| `ai.record_feedback` | Store user feedback on AI suggestions |

### Internal Orchestration

| Method | What It Does |
|--------|-------------|
| `crypto.derive_child_seed` | Derive lineage seeds for new primals (via BearDog) |
| `lineage.verify_siblings` | Verify primals share the same family seed |
| `primal.launch` | Launch a primal binary with correct environment |
| `filesystem.check_exists` | Check paths before graph execution |
| `report.deployment_success` | Log deployment completion for auditing |

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

This works for all 210+ semantic translations across 16 capability
domains.

**Spring applications**:

| Spring | Capability Call | What Happens |
|--------|----------------|-------------|
| wetSpring | `capability.call("storage.put", { data })` | NestGate stores the sequence |
| airSpring | `capability.call("ai.chat", { prompt })` | Squirrel → Songbird → Ollama |
| hotSpring | `capability.call("compute.dispatch", { shader })` | ToadStool → GPU |
| neuralSpring | `capability.call("crypto.sign", { hash })` | BearDog signs the checkpoint |
| groundSpring | `capability.call("discovery.find_primals", {})` | Songbird scans the mesh |
| healthSpring | `capability.call("dag.create_session", { name })` | rhizoCrypt opens a workspace |
| ludoSpring | `capability.call("visualization.render", { grammar })` | petalTongue renders the frame |

### 1.2 Graph Orchestration for Pipelines

**For**: Any spring that needs multi-step workflows without coding the
orchestration logic.

Deploy graphs are TOML files that define capability-call pipelines with
dependency resolution. biomeOS executes them in order, passing outputs
between steps.

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

**Applications**: Experiment pipelines (wetSpring), training workflows
(neuralSpring), clinical decision chains (healthSpring), game event
sequences (ludoSpring), calibration chains (groundSpring).

### 1.3 Lifecycle Monitoring

**For**: Any system that needs to know what's alive and healthy.

`lifecycle.status` returns the full ecosystem state: which primals are
running, which atomics are composed, which capabilities are available.
`health.check_all` probes every primal in one call.

```
lifecycle.status → {
  atomics: { tower: "healthy", node: "healthy", nest: "degraded" },
  primals: { beardog: "up", songbird: "up", nestgate: "restarting" },
  capabilities: { crypto: "available", storage: "degraded" }
}
```

**Applications**: Dashboard health display (petalTongue), automated
alerting (skunkBat), spring self-diagnosis ("is my storage provider
available?").

### 1.4 Runtime Capability Discovery

**For**: Any primal or spring that needs to adapt to what's available.

`capability.discover` returns who provides a domain and what methods
are available. Springs use this to check before calling:

```
capability.discover { domain: "provenance" }
  → { provider: "sweetgrass", methods: ["create_braid", "get_braid", ...] }

capability.discover { domain: "dag" }
  → { provider: "rhizocrypt", methods: ["create_session", "append_vertex", ...] }
```

If a domain is not available (primal not running), the spring degrades
gracefully instead of crashing.

### 1.5 Continuous Graph Execution

**For**: Long-running processes that need periodic orchestration.

The `ContinuousExecutor` runs deploy graphs on a 60 Hz tick cycle,
broadcasting events via `GraphEventBroadcaster` and `SensorEventBus`.
Springs subscribe to events rather than polling.

**Applications**: Real-time game loops (ludoSpring), sensor ingestion
pipelines (groundSpring, airSpring), live model inference
(neuralSpring), surgical instrument tracking (healthSpring).

---

## 2. biomeOS + Trio Compositions

The **Memory & Attribution Stack** (rhizoCrypt + LoamSpine + sweetGrass)
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

**Spring applications**:
- wetSpring: "Which researcher's data contributed to this taxonomy?"
- neuralSpring: "Which training runs influenced this model checkpoint?"
- ludoSpring: "Which designers contributed to this level's balance?"

### 2.4 biomeOS + Full Trio: The RootPulse Pattern

**The complete provenance-backed workflow, orchestrated end to end.**

```
1. capability.call("dag", "create_session")     → rhizoCrypt
2. (spring does its work, appending vertices)
3. capability.call("graph", "execute", { name: "rootpulse_commit" })
   biomeOS runs:
     a. dag.dehydrate          → rhizoCrypt collapses session
     b. crypto.sign            → BearDog signs the summary
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

```
capability.call("crypto.sign", { message }) → biomeOS checks lineage → BearDog signs
```

**Novel patterns**:
- **Signed graph execution**: Every deploy graph step produces a signed
  receipt. The sequence of receipts is a cryptographic audit trail.
- **JWT-gated capability access**: BearDog issues JWTs that biomeOS
  validates before routing capability calls — per-spring access control
  over which capabilities a spring can invoke.

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
- **Compute-aware scheduling**: biomeOS checks
  `lifecycle.status` to see which Node atomics have GPU availability
  before routing compute-heavy graph steps.

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
  graph before execution and suggests optimizations (reordering,
  parallelization, caching).
- **Feedback loops**: Graph execution results feed back to Squirrel,
  which adjusts parameters for the next run. biomeOS manages the loop.
- **Natural-language orchestration**: A spring describes what it wants
  in natural language; Squirrel translates to a deploy graph; biomeOS
  executes it.

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
  petalTongue can replay the execution as an animated DAG — useful for
  debugging pipelines and presenting experiment workflows.
- **Spring dashboard composition**: Each spring registers custom
  visualization grammars with petalTongue via biomeOS. The ecosystem
  dashboard assembles all spring grammars into a unified view.

### 3.7 biomeOS + skunkBat: Anomaly-Monitored Orchestration

**skunkBat monitors biomeOS's capability routing patterns for anomalies.**

Normal operation produces a baseline of capability call frequencies,
latencies, and provider routing patterns. skunkBat detects deviations:
unexpected capability calls, unusual routing changes, timing anomalies.

**Novel patterns**:
- **Graph execution audit**: skunkBat verifies that every graph
  execution follows the declared dependency order and that no
  unauthorized steps were injected.
- **Capability impersonation detection**: If a rogue process registers
  a capability that was previously handled by a known primal, skunkBat
  alerts.

### 3.8 biomeOS + barraCuda + coralReef: Sovereign Compute Pipeline

**biomeOS orchestrates the full sovereign GPU stack as a deploy graph.**

```
barraCuda (shader authoring) → coralReef (WGSL→SPIR-V compilation)
  → ToadStool (GPU dispatch) → NestGate (result storage)
```

biomeOS routes each step to the correct primal. The spring that needs
GPU compute calls `capability.call("compute", "dispatch", { ... })` and
biomeOS handles the entire chain.

### 3.9 biomeOS + sourDough: GenomeBin Distribution

**biomeOS packages itself and the ecosystem as genomeBins via sourDough.**

genomeBin = ecoBin + deployment wrapper. biomeOS's
`biomeos-genomebin-v3` crate produces self-extracting archives that
sourDough distributes through the NestGate federation. A new machine
downloads the genomeBin, extracts it, and biomeOS bootstraps the entire
ecosystem from a single binary.

---

## 4. Novel Spring Compositions

These are higher-order patterns that emerge from biomeOS orchestrating
multiple primals simultaneously.

### 4.1 Cross-Spring Data Pipeline

**Springs**: any two+ springs + biomeOS (graph orchestration)

Springs never import each other's code. biomeOS routes data between
them using the [Cross-Spring Data Flow Standard](./CROSS_SPRING_DATA_FLOW_STANDARD.md):

```
wetSpring produces: { schema: "ecoPrimals/time-series/v1", variable: "soil_moisture_vol", ... }
  → biomeOS routes to airSpring
airSpring consumes: soil moisture → Penman-Monteith ET₀ → irrigation decision
  → biomeOS routes result to petalTongue for visualization
```

Deploy graph:
```toml
[graph]
name = "soil_to_irrigation"
pattern = "Sequential"

[[graph.steps]]
name = "soil_data"
capability = "ecology"
operation = "soil_moisture"

[[graph.steps]]
name = "et0_calc"
capability = "ecology"
operation = "et0_pm"
depends_on = ["soil_data"]

[[graph.steps]]
name = "render_decision"
capability = "visualization"
operation = "render"
depends_on = ["et0_calc"]
```

**Applications**: Any cross-domain data handoff. The pattern applies to
any spring pair that produces/consumes the time-series schema.

### 4.2 Provenance-Backed Scientific Pipeline

**Springs**: any + biomeOS + rhizoCrypt + LoamSpine + sweetGrass + BearDog

Every scientific computation becomes a signed, attributed, permanently
committed chain — the "lab notebook that can't lie."

```
graph.execute("rootpulse_science_pipeline"):
  1. dag.create_session     → rhizoCrypt (ephemeral workspace)
  2. capability.call(spring) → spring runs experiment steps (each is a vertex)
  3. dag.dehydrate          → rhizoCrypt collapses to summary
  4. crypto.sign            → BearDog signs the Merkle root
  5. storage.store          → NestGate stores the payload
  6. commit.session         → LoamSpine commits permanently
  7. provenance.create_braid → sweetGrass records fair attribution
```

biomeOS executes all seven steps as a single graph. The spring calls
`graph.execute` once.

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

Two labs, each running a NUCLEUS instance, form a plasmodium collective.
biomeOS on each gate discovers the other's capabilities. A deploy graph
that spans both gates runs steps on whichever machine has the required
capability.

```
Gate A (basement):  ToadStool (GPU), NestGate (1TB SSD)
Gate B (NUC):       NestGate (256GB), low-power sensors

graph.execute("federated_soil_analysis"):
  1. groundSpring@B → sensor data collection
  2. capability.call("storage.put")@B → NestGate stores raw data
  3. capability.call("compute.dispatch")@A → ToadStool GPU processes
  4. capability.call("storage.put")@A → NestGate stores results
  5. commit.session@A → LoamSpine commits (permanent record on SSD)
```

biomeOS handles the cross-gate routing transparently. The spring
defines the graph; Plasmodium handles the federation.

### 4.4 Real-Time Multi-Spring Dashboard

**Springs**: any combination + biomeOS + petalTongue + Songbird

Multiple springs register capability providers. biomeOS aggregates
their health and output events. petalTongue renders a unified dashboard
with domain-appropriate palettes.

```
groundSpring → soil moisture (ecology palette)
airSpring    → ET₀, vapor pressure (measurement palette)
wetSpring    → community diversity (ecology palette)
healthSpring → patient vitals (health palette)

All flow through biomeOS SSE → petalTongue Grammar of Graphics
```

Each spring registers a visualization grammar:
```
capability.register {
  domain: "visualization",
  grammar: { data: "time_series", geom: "line", ... }
}
```

petalTongue discovers all registered grammars via biomeOS and composes
them into a multi-panel dashboard. No spring knows about any other
spring.

### 4.5 AI-in-the-Loop Experiment

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

**Applications**: Hyperparameter search (neuralSpring), drug dosing
optimization (healthSpring), game difficulty auto-tuning (ludoSpring),
irrigation schedule optimization (airSpring).

### 4.6 Consent-Gated Data Sharing

**Springs**: healthSpring + biomeOS + BearDog + rhizoCrypt

Patient data enters a signed rhizoCrypt session. A researcher requests
access via biomeOS. BearDog verifies the researcher's identity and
lineage. If authorized, biomeOS routes a Loan slice from rhizoCrypt
with time-limited access. The loan expires automatically.

```
1. healthSpring: dag.create_session (patient data, BearDog-signed vertices)
2. Researcher: capability.call("dag", "slice", { mode: "Loan", duration: "7d" })
   → biomeOS checks: researcher lineage verified by BearDog?
   → yes: route to rhizoCrypt, return Loan slice
   → no: reject
3. (7 days later: loan expires)
4. Audit: dag.merkle_proof proves data integrity during loan period
```

### 4.7 Self-Healing Ecosystem

**Springs**: any + biomeOS (lifecycle) + skunkBat (anomaly)

biomeOS monitors all primal health. When a primal crashes, biomeOS
auto-resurrects it. skunkBat monitors the resurrection patterns for
anomalies (crash loops, resource exhaustion). If skunkBat detects a
pattern, it recommends scaling changes to biomeOS.

```
ToadStool crashes → biomeOS auto-resurrects → health.check passes
ToadStool crashes again → biomeOS resurrects → skunkBat detects loop
skunkBat: "ToadStool OOM — recommend memory limit increase"
biomeOS: adjust config → restart with new limits
```

---

## 5. Integration Patterns for Springs

### Minimal Integration (biomeOS capability routing only)

Add to your spring's `Cargo.toml` under an optional feature:

```toml
[dependencies]
neural-api-client-sync = { path = "../../phase2/biomeOS/crates/neural-api-client-sync", optional = true }

[features]
neural = ["neural-api-client-sync"]
```

Then call any capability via the Neural API bridge:

```rust
use neural_api_client_sync::NeuralBridge;

let bridge = NeuralBridge::discover()?;

// Route to any primal by capability — never by name
let result = bridge.capability_call("crypto", "sign", &serde_json::json!({
    "message": "experiment-result-hash"
}))?;

let result = bridge.capability_call("storage", "put", &serde_json::json!({
    "key": "experiment-042",
    "data": payload
}))?;
```

The spring never imports BearDog, NestGate, or any other primal. It
discovers capabilities at runtime. If biomeOS is not running, the call
fails gracefully.

### Graph-Based Integration (pipeline orchestration)

Define a TOML deploy graph in `graphs/`:

```toml
[graph]
name = "my_spring_pipeline"
pattern = "Sequential"

[[graph.steps]]
name = "collect_data"
capability = "ecology"
operation = "soil_moisture"

[[graph.steps]]
name = "analyze"
capability = "ai"
operation = "chat"
depends_on = ["collect_data"]
params = { prompt = "Interpret these soil readings: ${collect_data}" }

[[graph.steps]]
name = "commit"
capability = "commit"
operation = "session"
depends_on = ["analyze"]
```

Then execute from your spring:

```rust
let bridge = NeuralBridge::discover()?;
bridge.capability_call("graph", "execute", &serde_json::json!({
    "name": "my_spring_pipeline",
    "params": { "site_id": "field-north-7" }
}))?;
```

biomeOS runs the entire pipeline, routing each step to the correct
primal.

### Capability Provider Registration (spring as provider)

Springs that expose capabilities register with biomeOS:

```rust
let bridge = NeuralBridge::discover()?;
bridge.capability_call("capability", "register", &serde_json::json!({
    "domain": "ecology",
    "methods": ["soil_moisture", "et0_pm", "community_diversity"],
    "socket": "/run/user/1000/biomeos/wetspring-family123.sock"
}))?;
```

Once registered, any other spring or primal can call
`capability.call("ecology", "soil_moisture", ...)` and biomeOS routes
to your spring. See the
[Spring-as-Provider Pattern](./SPRING_AS_PROVIDER_PATTERN.md) for the
full contract.

### Full Trio Integration (via biomeOS graphs)

Use biomeOS graph execution for the complete provenance pipeline:

```rust
let bridge = NeuralBridge::discover()?;

// Create ephemeral workspace
bridge.capability_call("dag", "create_session", &session_args)?;

// Do your spring's work (append vertices)
bridge.capability_call("dag", "append_vertex", &vertex_args)?;

// One call to run the full provenance pipeline
bridge.capability_call("graph", "execute", &serde_json::json!({
    "name": "rootpulse_commit",
    "params": { "session_id": session_id }
}))?;
// biomeOS handles: dehydrate → sign → store → commit → attribute
```

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
- [Spring-as-Provider Pattern](./SPRING_AS_PROVIDER_PATTERN.md) — registering capabilities
- [Cross-Spring Data Flow Standard](./CROSS_SPRING_DATA_FLOW_STANDARD.md) — time-series exchange
- [Spring Provenance Trio Integration](./SPRING_PROVENANCE_TRIO_INTEGRATION_PATTERN.md) — trio pattern
- [Semantic Method Naming Standard](./SEMANTIC_METHOD_NAMING_STANDARD.md) — method naming
- [Universal IPC Standard v3](./UNIVERSAL_IPC_STANDARD_V3.md) — transport layer
- [Primal Registry](./PRIMAL_REGISTRY.md) — full primal catalogue
