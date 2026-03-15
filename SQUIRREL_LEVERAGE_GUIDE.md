<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# Squirrel Leverage Guide — Standalone, Trio, and Ecosystem Compositions

**Date**: March 14, 2026
**Primal**: Squirrel v0.1.0 (gen3)
**Audience**: All springs, all primals, biomeOS integrators
**Status**: Active

---

## Purpose

This document describes how Squirrel can be leveraged — alone and in
composition with other primals — by springs and ecosystem consumers. Each
primal in the ecosystem produces an equivalent guide. Together, these
guides form a combinatorial recipe book for emergent behaviors.

Squirrel provides **sovereign AI coordination** — vendor-agnostic model
routing, multi-MCP coordination, context management, and intelligent task
decomposition. It is the "thinking layer" of the ecosystem.

**Philosophy**: Sovereign by default, federated by consent. Squirrel never
couples to a vendor — it discovers AI capabilities at runtime and routes
intelligently. Local inference is preferred; cloud is a fallback, not a
dependency.

---

## IPC Methods (Semantic Naming)

All methods follow `{domain}.{operation}[.{variant}]` per the
[Semantic Method Naming Standard](./SEMANTIC_METHOD_NAMING_STANDARD.md).

| Method | What It Does |
|--------|-------------|
| `ai.query` | Route a prompt to the best available model and return the response |
| `ai.complete` | Text completion with model selection and parameter control |
| `ai.chat` | Multi-turn conversation with managed context window |
| `ai.inference` | Raw model inference (no routing intelligence) |
| `ai.text_generation` | Structured text generation with format constraints |
| `ai.list_providers` | Discover all available AI providers and their capabilities |
| `capability.announce` | Register AI capabilities with the ecosystem |
| `capability.discover` | Find primals offering specific AI capabilities |
| `system.health` | Health check with provider status |
| `system.metrics` | Performance metrics (latency, token counts, cost) |
| `system.ping` | Liveness probe |
| `discovery.peers` | Discover other AI-capable primals |
| `tool.execute` | Execute a registered MCP tool |
| `context.create` | Create a managed context window |
| `context.update` | Add content to a context window |
| `context.summarize` | Compress a context window while preserving key information |

**Transport**: JSON-RPC 2.0 over Unix sockets (required), tarpc/bincode
(optional, feature-gated for high-performance binary RPC).

---

## 1. Squirrel Standalone

These patterns use Squirrel alone — no other primals required.

### 1.1 Vendor-Agnostic Model Routing

**For**: Any spring or application needing AI inference without vendor lock-in.

Squirrel discovers available providers at runtime — local Ollama, any
OpenAI-compatible server, cloud APIs — and routes requests based on task
requirements, latency, cost, and quality constraints.

```
ai.query { prompt: "Analyze this soil moisture trend", constraints: { max_latency_ms: 500, prefer_local: true } }
  → { response: "...", provider: "ollama/mistral-7b", latency_ms: 230, tokens: 512 }
```

The caller never specifies a vendor. Squirrel selects the best available
model for the task. If the preferred provider is down, it falls back
automatically.

**Spring applications**:

| Spring | AI Task |
|--------|---------|
| airSpring | Interpret anomalous ET₀ readings, suggest irrigation adjustments |
| wetSpring | Classify novel microbial sequences, generate taxonomy hypotheses |
| hotSpring | Summarize lattice QCD convergence status, suggest next β sweep |
| neuralSpring | Meta-learning: analyze training curves, suggest hyperparameters |
| groundSpring | Natural-language sensor calibration reports from raw data |
| healthSpring | Clinical decision support: PK/PD interpretation, dosing guidance |
| ludoSpring | Dynamic game narrative generation, NPC dialogue, quest design |

### 1.2 Context Window Management

**For**: Any spring with long-running analysis that exceeds model context limits.

Squirrel manages context windows — tracking what has been said, what
matters, and what can be safely compressed. Springs push data into a
context, and Squirrel ensures the model sees the most relevant content
even when the full history is too large.

```
context.create { name: "experiment-047", max_tokens: 128000 }
  → context_id

context.update { context_id, content: "Step 1: pH measured at 6.8..." }
context.update { context_id, content: "Step 2: Temperature 22.3°C..." }
... (hundreds of updates)

ai.query { prompt: "What is the trend?", context_id }
  → (Squirrel compresses context intelligently, routes with full history awareness)
```

**Applications**: Long-running experiment analysis, multi-session game
narratives, iterative clinical trial monitoring.

### 1.3 Multi-MCP Coordination

**For**: Any scenario requiring multiple AI tools to collaborate.

Squirrel coordinates multiple Model Context Protocol servers, routing
sub-tasks to specialized tools and composing their results.

```
tool.execute { tool: "code_review", params: { code: "..." } }
  → routes to a code-analysis MCP server

tool.execute { tool: "data_viz", params: { dataset: "..." } }
  → routes to a visualization MCP server

ai.query { prompt: "Compare these two results", context_id }
  → Squirrel synthesizes outputs from both tools
```

**Applications**: Multi-tool scientific workflows (compute + analyze +
visualize), game content pipelines (generate + validate + balance).

### 1.4 Task Decomposition

**For**: Complex queries that benefit from being split into sub-tasks.

Squirrel can decompose a complex prompt into sub-tasks, route each to
the optimal provider, and synthesize the results.

```
ai.query {
  prompt: "Analyze this 16S rRNA dataset: classify organisms, identify novel taxa, suggest follow-up experiments",
  decompose: true
}
  → Squirrel splits into 3 sub-tasks, routes each optimally, merges results
```

---

## 2. Squirrel + Foundation Trio Compositions

Squirrel's natural trio partners are **BearDog** (crypto) and
**Songbird** (network). Together they form **Tower Atomic + AI** — the
secure, networked, intelligent foundation.

### 2.1 Squirrel + BearDog: Signed AI Responses

**Every AI response can be cryptographically signed for auditability.**

```
ai.query { prompt: "..." }
  → response_text, response_hash

crypto.sign { data: response_hash }
  → signed_response (proves this AI generated this exact output)
```

**Why this matters**: AI provenance. When a clinical decision support
system suggests a dosing adjustment (healthSpring), the recommendation
is signed and attributable. When an AI suggests a game balance change
(ludoSpring), it is provably that AI's output, not a human edit.

**Applications**: Regulatory compliance (healthSpring), academic integrity
(neuralSpring), anti-cheat (ludoSpring), audit trails (all springs).

### 2.2 Squirrel + Songbird: Federated AI Discovery

**Squirrel discovers AI providers across the network via Songbird.**

```
discovery.query { capability: "ai.inference" }
  → [ { primal: "squirrel-abc", models: ["mistral-7b", "llama-3.1-8b"] },
      { primal: "squirrel-def", models: ["codellama-34b"] } ]
```

In a multi-tower deployment (lab cluster, classroom, research campus),
each tower runs its own Squirrel with local models. Songbird discovers
them all. A spring can request inference from the best available
Squirrel in the federation.

**Applications**: Lab-scale AI (multiple research workstations sharing
models), classroom AI (students share local inference capacity),
field station networks (groundSpring/airSpring remote sites).

### 2.3 Squirrel + BearDog + Songbird: Encrypted AI Federation

**Full Tower Atomic + AI**: Encrypted discovery of AI providers across
untrusted networks with lineage-verified trust.

```
1. Songbird discovers remote Squirrel instances via BirdSong
2. BearDog verifies genetic lineage (same family seed → auto-trust)
3. Squirrel routes task to remote instance over encrypted channel
4. Response travels back encrypted, signed, verified
```

**Applications**: Multi-institution research collaboration (each site
runs sovereign AI, shares capacity via federation), privacy-preserving
clinical AI (patient data stays local, only queries travel).

---

## 3. Squirrel + Other Primals

### 3.1 Squirrel + ToadStool: Local Inference Orchestration

**Squirrel routes to ToadStool's local GPU compute for on-device inference.**

```
ai.list_providers → includes { provider: "local/ollama", gpu: "nvidia_sm89", vram: "24GB" }
ai.query { prompt: "...", constraints: { local_only: true } }
  → routed to Ollama on ToadStool-managed GPU
```

Squirrel discovers ToadStool's hardware capabilities at runtime. If a
model fits in VRAM, it runs locally. If not, Squirrel can split the
workload (quantized local + full-precision cloud fallback).

**Applications**: Sovereign inference (no data leaves the machine),
GPU-aware model selection, VRAM-constrained routing, multi-GPU model
parallelism.

### 3.2 Squirrel + NestGate: Model Weight Caching

**NestGate caches model weights and AI artifacts by content hash.**

```
storage.get { hash: model_weights_hash }
  → cached model weights (no re-download needed)

storage.put { hash: response_hash, data: ai_response }
  → cache AI responses for identical queries (semantic dedup)
```

**Applications**: Offline AI (model weights cached locally via NestGate),
response caching for repeated queries, experiment reproducibility
(exact model version is content-addressed).

### 3.3 Squirrel + rhizoCrypt: AI-Augmented Sessions

**AI agents participate in DAG sessions like any other agent.**

```
dag.create_session { name: "ai-experiment-analysis" }
dag.append_vertex { agent_did: "did:eco:researcher", payload: { data: raw_results } }
dag.append_vertex { agent_did: "did:eco:squirrel", payload: { analysis: "...", model: "llama-3.1-8b" } }
dag.append_vertex { agent_did: "did:eco:researcher", payload: { follow_up: "..." } }
```

Squirrel's contributions are tracked with the same provenance as human
contributions. The DAG captures the full human-AI collaboration history.

**Applications**: AI-assisted experiment design, human-AI pair programming
of scientific workflows, collaborative game design where AI and humans
co-create.

### 3.4 Squirrel + petalTongue: Intelligent Visualization

**Squirrel analyzes data and generates Grammar of Graphics expressions
for petalTongue to render.**

```
ai.query {
  prompt: "Visualize the correlation between soil moisture and ET₀",
  context: { soil_data, et0_data }
}
  → { grammar: { data: ..., geom: "point", aes: { x: "moisture", y: "et0", color: "season" }, ... } }

visualization.render { grammar }
  → petalTongue renders the visualization
```

The AI understands what to show; petalTongue knows how to show it.
Squirrel generates the visualization specification; petalTongue
applies Tufte constraints and renders to the best available modality.

**Applications**: Natural-language data exploration ("show me the
outliers"), automated figure generation for papers, accessible
data narratives (audio sonification via petalTongue for vision-impaired
researchers).

### 3.5 Squirrel + sweetGrass: Attributed AI

**Every AI inference is attributed in the provenance graph.**

```
ai.query { ... } → response
provenance.create_braid {
  agents: [{ did: "did:eco:squirrel", role: "Generator" }],
  artifact: response_hash,
  model: "llama-3.1-8b",
  provider: "ollama"
}
```

sweetGrass tracks which model generated what, enabling fair attribution
when AI contributes to collaborative work. The scyBorg provenance trio
(AGPL code + ORC mechanics + CC-BY-SA content) applies to AI outputs.

### 3.6 Squirrel + LoamSpine: Permanent AI Knowledge

**Important AI insights are permanently committed.**

```
ai.query { prompt: "What is the most significant finding?" }
  → insight

commit.session { entry: { type: "ai_insight", content: insight, model, signed: true } }
  → permanent LoamSpine entry (the AI's "lab notebook")
```

**Applications**: AI-generated hypotheses worth preserving, model
evaluation records (which model performed best on which task), audit
trail of AI-assisted decisions.

### 3.7 Squirrel + skunkBat: AI-Powered Threat Analysis

**Squirrel provides AI reasoning for skunkBat's anomaly detection.**

```
(skunkBat detects anomalous network pattern)
ai.query {
  prompt: "Analyze this network anomaly pattern",
  context: { anomaly_metadata }
}
  → { analysis: "Pattern consistent with port scanning from unknown lineage", severity: "medium", recommendation: "quarantine" }
```

**Applications**: AI-augmented intrusion analysis, intelligent alert
triage (reduce false positives), behavioral pattern recognition.

### 3.8 Squirrel + barraCuda: AI-Guided Computation

**AI guides mathematical computation strategy.**

```
ai.query {
  prompt: "Given this matrix structure, what is the optimal factorization approach?",
  context: { matrix_metadata: { size: "10000x10000", sparsity: 0.95, symmetry: true } }
}
  → { recommendation: "Use Lanczos for sparse eigensolve", shader: "eigensolve_lanczos_f64.wgsl" }
```

Squirrel's domain knowledge (learned from context) guides barraCuda's
shader selection. The AI recommends the math; barraCuda executes it;
ToadStool dispatches it; coralReef compiles it.

---

## 4. Novel Spring Compositions

These are higher-order patterns that emerge from combining Squirrel with
multiple primals simultaneously.

### 4.1 AI-Driven Scientific Pipeline

**Springs**: any + Squirrel + rhizoCrypt + ToadStool + petalTongue

The AI designs the experiment, tracks it in a DAG, dispatches compute,
and visualizes results — an intelligent research assistant.

```
1. ai.query { "Design an experiment to test X" }
     → experimental design (steps, parameters, expected outcomes)
2. dag.create_session { name: "ai-designed-experiment" }
3. For each step:
     a. compute.submit { shader, params }    (ToadStool dispatches)
     b. dag.append_vertex { result }         (rhizoCrypt tracks)
     c. ai.query { "Interpret this result" } (Squirrel analyzes)
4. visualization.render { grammar }          (petalTongue shows results)
5. ai.query { "What should we try next?" }   (Squirrel suggests)
```

### 4.2 Provenance-Complete AI Research

**Springs**: any + Squirrel + rhizoCrypt + LoamSpine + sweetGrass + BearDog

Every AI-assisted research step is tracked, signed, attributed, and
permanently committed. The full chain from "AI suggested this hypothesis"
to "GPU computed this result" to "human verified this conclusion" is
in the provenance graph.

```
1. ai.query → hypothesis          (Squirrel, attributed)
2. compute.submit → result        (ToadStool, tracked)
3. ai.query → interpretation      (Squirrel, attributed)
4. dag.dehydrate → summary        (rhizoCrypt, content-addressed)
5. crypto.sign → signed_summary   (BearDog, tamper-evident)
6. commit.session → permanent     (LoamSpine, immutable)
7. provenance.create_braid        (sweetGrass, fair attribution)
```

This is the "AI lab notebook that can't lie" pattern — every AI
contribution is cryptographically attributed alongside human work.

### 4.3 Adaptive Game AI with Learning Memory

**Springs**: ludoSpring + Squirrel + rhizoCrypt + sweetGrass

AI-driven dynamic difficulty adjustment where the AI learns from
player history stored in DAG sessions.

```
1. dag.get_session_vertices { player_session }
     → player's full game history as a DAG
2. ai.query {
     prompt: "Analyze player behavior and suggest difficulty adjustment",
     context: player_history
   }
     → { difficulty_delta: -0.3, reasoning: "Player struggling with puzzle mechanics" }
3. dag.append_vertex { agent_did: "did:eco:squirrel", payload: { adjustment } }
4. provenance.create_braid → attribution (AI contributed this adjustment)
```

The AI learns from each player's full history. Adjustments are
attributed. Players can see when and why the AI changed difficulty.

### 4.4 Multi-Site Federated AI with Sovereignty

**Springs**: any + Squirrel + Songbird + BearDog + NestGate

Multiple research sites, each running sovereign AI, collaborate without
sharing raw data. Models are cached locally. Only queries and responses
cross site boundaries, encrypted and signed.

```
Site A (hospital):
  ai.query { patient_data } → local_inference (data never leaves site A)

Site B (research lab):
  ai.query { "Analyze aggregate trends from sites A, C, D" }
    → Squirrel queries federated Squirrels via Songbird
    → Each site returns only aggregated/anonymized results
    → BearDog verifies lineage at each hop
    → NestGate caches federated results locally
```

### 4.5 AI-Augmented Sensor Network Intelligence

**Springs**: groundSpring + airSpring + Squirrel + rhizoCrypt + petalTongue

IoT sensor networks feed data to Squirrel for real-time interpretation.
The AI detects anomalies, suggests actions, and generates dashboards.

```
groundSpring → dag.append_vertex { soil_moisture: 0.12, alert: "critically_low" }
airSpring    → dag.append_vertex { et0: 7.3, alert: "extreme_demand" }

ai.query {
  prompt: "What is happening and what should we do?",
  context: { recent_sensor_vertices }
}
  → "Soil moisture critically low with extreme ET₀. Immediate irrigation
     recommended. Expected recovery in 48h with 25mm application."

visualization.render { grammar: { data: sensor_timeseries, geom: "line+alert_band" } }
```

### 4.6 Cross-Domain Knowledge Synthesis

**Springs**: any combination + Squirrel

Squirrel can synthesize knowledge across domains that would otherwise
never interact. Because it has no hardcoded domain coupling, the same
AI coordination layer works for any combination of springs.

```
ai.query {
  prompt: "Are there correlations between soil microbiome diversity (wetSpring)
           and crop yield response to irrigation (airSpring)?",
  context: {
    microbiome_data: (from rhizoCrypt session),
    yield_data: (from rhizoCrypt session)
  }
}
  → cross-domain insight that neither spring could generate alone
```

This is Squirrel's unique value: it is the only primal that can reason
across all domains simultaneously, because it understands natural
language and context, not just structured data.

---

## 5. Integration Patterns for Springs

### Minimal Integration (standalone Squirrel only)

Call via the Neural API bridge — the spring never imports Squirrel directly:

```rust
use neural_api_client_sync::NeuralBridge;

let bridge = NeuralBridge::discover()?;
let response = bridge.capability_call("ai", "query", &serde_json::json!({
    "prompt": "Analyze this dataset",
    "constraints": { "max_latency_ms": 1000, "prefer_local": true }
}))?;
```

If Squirrel is not running, the call fails gracefully. The spring
degrades to non-AI mode.

### Direct IPC (for high-throughput)

For performance-critical paths, springs can connect directly to Squirrel's
Unix socket:

```rust
use universal_patterns::transport::UniversalTransport;

let transport = UniversalTransport::connect_discovered("squirrel").await?;
let response = transport.json_rpc_call("ai.query", &params).await?;
```

### tarpc Binary RPC (maximum performance)

For the highest throughput (thousands of inferences per second), use
the tarpc binary protocol:

```rust
// Feature-gated: requires Squirrel built with `tarpc-rpc`
let client = SquirrelClientBuilder::new()
    .socket_path(get_socket_path("squirrel"))
    .build().await?;

let result = client.query_ai(params).await?;
// Arc<str> identifiers, zero-copy, O(1) clone semantics
```

### Deploy Graph (biomeOS orchestration)

For automated AI-augmented workflows:

```toml
[graph]
name = "ai_assisted_experiment"
pattern = "Sequential"

[[graph.steps]]
name = "collect_data"
capability = "compute"
operation = "submit"

[[graph.steps]]
name = "ai_analysis"
capability = "ai"
operation = "query"
depends_on = ["collect_data"]
params = { prompt = "Analyze the results from the previous step" }

[[graph.steps]]
name = "visualize"
capability = "visualization"
operation = "render"
depends_on = ["ai_analysis"]
```

---

## 6. What Squirrel Does NOT Do

| Concern | Who Handles It |
|---------|---------------|
| Permanent storage | LoamSpine (commit/checkout) |
| Content blob storage | NestGate (put/get by hash) |
| Signing / encryption | BearDog (crypto.*) |
| Attribution / provenance | sweetGrass (provenance.*) |
| Discovery / networking | Songbird (discovery.*) |
| GPU compute dispatch | ToadStool (compute.*) |
| Shader compilation | coralReef (shader.compile.*) |
| Mathematics / shaders | barraCuda (math.*) |
| Visualization | petalTongue (visualization.*) |
| Ephemeral memory | rhizoCrypt (dag.*) |
| Orchestration | biomeOS (Neural API) |
| Defense | skunkBat (defense.*) |

Squirrel provides AI reasoning and coordination. Everything else is
discovered at runtime and composed by biomeOS. This is fundamental —
intelligence through coordination, not through coupling.

---

## 7. What Makes Squirrel Novel

Squirrel is uniquely positioned in the ecosystem because:

1. **Cross-domain reasoning**: The only primal that understands natural
   language. It can synthesize insights across springs that have no
   direct relationship (soil microbiome ↔ crop yield ↔ weather patterns).

2. **Adaptive routing**: As the ecosystem grows and models improve,
   Squirrel's routing evolves without code changes. New providers appear
   via capability discovery; Squirrel incorporates them automatically.

3. **Context persistence**: Unlike stateless API calls, Squirrel maintains
   context across interactions. A multi-day experiment can maintain
   conversational context, enabling "what changed since yesterday?" queries.

4. **Sovereign AI**: All inference can run locally via Ollama/ToadStool.
   No data leaves the machine unless the operator explicitly configures
   cloud fallback. This is essential for clinical data (healthSpring),
   classified research, and personal computing.

5. **The thinking layer**: Every other primal provides a specific
   capability (crypto, storage, compute, visualization). Squirrel
   provides *reasoning* — the ability to decide what to do, not just
   how to do it.
