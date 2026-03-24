<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# Squirrel Leverage Guide — Standalone, Trio, and Ecosystem Compositions

**Date**: March 24, 2026
**Primal**: Squirrel v0.1.0-alpha.25
**Audience**: All springs, all primals, biomeOS integrators
**Status**: Active

---

## Purpose

This document describes how Squirrel can be leveraged — alone and in
composition with other primals — by springs and ecosystem consumers. Each
primal in the ecosystem will produce an equivalent guide. Together, these
guides form a combinatorial recipe book for emergent behaviors.

Squirrel provides **sovereign AI coordination** — vendor-agnostic model
routing, context window management, MCP tool orchestration, and multi-model
workflows. It is the ecosystem's gateway to inference: any spring that
needs an AI answer asks Squirrel, and Squirrel finds the best model,
manages the conversation state, and returns the result.

**Philosophy**: No spring should know or care which model answered.
Squirrel absorbs the vendor complexity so that science, games, and
infrastructure get intelligence without coupling. Models come and go;
the capability interface stays.

---

## IPC Methods (Semantic Naming)

All methods follow `{domain}.{operation}[.{variant}]` per the
[Semantic Method Naming Standard](./SEMANTIC_METHOD_NAMING_STANDARD.md).

| Method | What It Does |
|--------|-------------|
| `ai.query` | Route a prompt to the best available AI model (cost/quality/latency selection) |
| `ai.complete` | Text completion (single-turn inference) |
| `ai.chat` | Chat completion with message history |
| `ai.list_providers` | List available AI providers and their status |
| `capability.announce` | Accept capability and tool announcements from remote primals |
| `capability.discover` | Report own capabilities for socket scanning (niche self-knowledge) |
| `capability.list` | Per-method cost, dependency, and schema info for Pathway Learner |
| `context.create` | Create a new context session (DashMap-backed, versioned) |
| `context.update` | Update an existing context with new data |
| `context.summarize` | Summarize a context session (with AI-driven compression) |
| `system.health` | Health check with uptime, provider count, capability status |
| `system.status` | System status (UniBin alias for system.health) |
| `system.metrics` | Server metrics (total requests, errors, p50/p99 latency) |
| `system.ping` | Connectivity test (returns pong) |
| `discovery.peers` | Scan socket directories for running primals |
| `tool.execute` | Execute MCP tools (local built-ins + remote announced tools) |
| `tool.list` | List available tools with JSON Schema input definitions |
| `health.liveness` | Liveness probe (PRIMAL_IPC_PROTOCOL v3.0) — returns ok if process alive |
| `health.readiness` | Readiness probe (PRIMAL_IPC_PROTOCOL v3.0) — returns ok if ready for requests |
| `lifecycle.register` | Register with biomeOS orchestrator |
| `lifecycle.status` | Heartbeat status report to biomeOS |

**Manifest discovery**: Squirrel writes `$XDG_RUNTIME_DIR/ecoPrimals/squirrel.json`
at startup for biomeOS manifest-based bootstrap discovery (absorbed from rhizoCrypt v0.13).

**Human dignity**: AI operations pass through `DignityEvaluator` checks for
discrimination, manipulation, oversight, and explainability (wateringHole standard).

**Transport**: JSON-RPC 2.0 over Unix socket (primary), tarpc/bincode
(high-perf primal-to-primal), HTTP (feature-gated OFF by default).

**JSON-RPC batch support**: Full Section 6 compliance — array of requests
yields array of responses; notification-only batches yield no response.

---

## 1. Squirrel Standalone

These patterns use Squirrel alone — no other primals required.

### 1.1 Vendor-Agnostic Inference

**For**: Any spring that needs an AI answer without vendor lock-in.

Squirrel abstracts the model layer. The caller sends a prompt; Squirrel
selects the best available provider based on cost, quality, and latency
hints. Cloud APIs, local models, and model hubs are all reachable through
the same call.

```
ai.query {
  prompt: "Classify this 16S rRNA sequence to phylum level: ATCG...",
  max_tokens: 256,
  temperature: 0.1
}
  → { response: "Proteobacteria (confidence 0.94)", provider: "local-llama", latency_ms: 120 }
```

Provider sources (all discovered at runtime):

| Source | Example | How Discovered |
|--------|---------|----------------|
| Cloud API | OpenAI, Anthropic, Gemini | API key in environment |
| Local model | Ollama, llama.cpp, vLLM | `LOCAL_AI_ENDPOINT` env var |
| Model hub | HuggingFace, ModelScope | `MODEL_HUB_CACHE_DIR` env var |
| ToadStool GPU | On-device inference | biomeOS socket scan |

The caller never sees provider details. If the preferred provider fails,
Squirrel falls back to the next available — circuit breaker and retry
logic are built in.

**Spring applications**:

| Spring | What Gets Asked |
|--------|----------------|
| wetSpring | Classify taxa from 16S amplicons, summarize DADA2 pipeline outputs |
| airSpring | Predict irrigation need from ET₀ anomalies, explain sensor drift |
| hotSpring | Summarize EOS fit residuals, classify lattice QCD phase transitions |
| neuralSpring | Suggest hyperparameter tuning strategies, explain training loss curves |
| groundSpring | Interpret seismic waveform features, classify calibration anomalies |
| healthSpring | Summarize PK/PD model fits, generate dosing rationale narratives |
| ludoSpring | Generate NPC dialogue, balance game mechanics via AI playtesting; RPGPT composition (ludoSpring logic + Squirrel narration + NestGate + petalTongue + provenance trio) |
| primalSpring | Validates Squirrel's AI coordination — Track 6 exp044 tests multi-MCP routing via Squirrel + biomeOS capability graph |

### 1.2 Context Window Management

**For**: Any spring with multi-turn AI interactions or long-running sessions.

Context sessions are versioned, DashMap-backed workspaces that accumulate
state across multiple AI calls. Each session tracks metadata, version
history, and accumulated context.

```
context.create { metadata: { niche: "wetspring", experiment: "pfas-screen-2026" } }
  → { id: "ctx-01JQ...", version: 1 }

context.update { id: "ctx-01JQ...", data: { step: "dada2_filter", result_count: 14200 } }
  → { id: "ctx-01JQ...", version: 2 }

ai.query { prompt: "Given context ctx-01JQ..., which ASVs are PFAS-degrading candidates?" }
  → (response informed by accumulated context)

context.summarize { id: "ctx-01JQ..." }
  → { summary: "PFAS screening: 14,200 ASVs filtered → 23 candidates...", version: 3 }
```

Context summarization compresses long histories into concise state,
keeping token costs manageable across many turns. NestGate persistence
is wired when NestGate's `storage.put` / `storage.get` capabilities are
discovered at runtime — until then, contexts live in memory.

**Spring applications**:

| Spring | Context Pattern |
|--------|----------------|
| wetSpring | Multi-step pipeline context: filter → denoise → classify → summarize |
| airSpring | Season-long irrigation advisor accumulating daily ET₀ + soil + weather |
| hotSpring | Iterative EOS fitting: narrow parameter space across AI-assisted rounds |
| neuralSpring | Training run advisor: loss curves, hyperparameter history, next-step suggestions |
| groundSpring | Long-running calibration chain with evolving instrument drift context |
| healthSpring | Patient case context across multiple clinic visits and lab results |
| ludoSpring | Game design session: iterating mechanics, balance, and narrative with AI |

### 1.3 MCP Tool Orchestration

**For**: Any spring exposing or consuming tools via Model Context Protocol.

Squirrel acts as an MCP hub. Other primals announce their tools via
`capability.announce`, and Squirrel routes `tool.execute` requests to
the appropriate primal. Tools are defined with JSON Schema input schemas
(from `capability_registry.toml`), enabling LLM-native tool use.

```
tool.list {}
  → [
    { name: "ai.query", description: "Route prompt to AI", input_schema: {...} },
    { name: "compute.submit", description: "Submit GPU workload", input_schema: {...} },
    { name: "storage.put", description: "Store content-addressed blob", input_schema: {...} }
  ]

tool.execute { tool: "compute.submit", args: { shader: "fft_f64", input_hash: "abc..." } }
  → (forwarded to ToadStool via announced socket, result returned)
```

Remote tool announcement:

```
capability.announce {
  primal: "toadstool",
  socket_path: "/run/user/1000/biomeos/toadstool-abc.sock",
  capabilities: ["compute"],
  tools: ["compute.submit", "compute.status", "compute.cancel"]
}
  → { status: "registered", tool_count: 3 }
```

Any primal's tools become available through Squirrel's unified tool
interface — springs and AI agents see one tool catalog regardless of
how many primals are running.

**Spring applications**: Any spring that uses AI agents with tool-use
capabilities (function calling). The AI model sees all ecosystem tools
as available functions and can compose them into multi-step workflows.

### 1.4 Cost-Aware Model Selection

**For**: Any spring operating under compute or budget constraints.

Squirrel's niche self-knowledge (`niche.rs`) includes per-method cost
estimates and GPU benefit hints. The `capability.list` response exposes
these to biomeOS's Pathway Learner for intelligent scheduling:

```
capability.list {}
  → {
    "ai.query":        { latency_ms: 500, cpu: "low", memory_bytes: 8192,  gpu_beneficial: true },
    "ai.chat":         { latency_ms: 800, cpu: "low", memory_bytes: 16384, gpu_beneficial: true },
    "context.create":  { latency_ms: 2,   cpu: "low", memory_bytes: 512,   gpu_beneficial: false },
    "tool.execute":    { latency_ms: 100, cpu: "low", memory_bytes: 4096,  gpu_beneficial: false }
  }
```

Springs can use this to decide whether to invoke AI (expensive) or
heuristics (cheap) for a given step. biomeOS uses it to schedule across
primals — routing ai.query to GPU-equipped nodes and context.create
to any available node.

### 1.5 Peer Discovery

**For**: Any deployer needing to understand the running ecosystem.

Squirrel scans the biomeOS socket directory for active primals and
returns their identities and capabilities:

```
discovery.peers {}
  → [
    { primal: "beardog", socket: "/run/user/1000/biomeos/beardog.sock", capabilities: ["crypto", "auth"] },
    { primal: "songbird", socket: "/run/user/1000/biomeos/songbird.sock", capabilities: ["discovery", "transport"] },
    { primal: "toadstool", socket: "/run/user/1000/biomeos/toadstool.sock", capabilities: ["compute"] }
  ]
```

This is useful for debugging, monitoring dashboards, and dynamic
composition — any primal can ask Squirrel "who's here?" instead of
scanning sockets independently.

---

## 2. Squirrel + Inference Trio

The **Inference Trio** (Squirrel + ToadStool + Songbird) forms the
AI execution pipeline:

```
Squirrel (Routing)          — selects model, manages context, dispatches
      ↕
  ToadStool (Compute)       — GPU/NPU/CPU execution, hardware discovery
      ↕
  Songbird (Transport)      — discovery mesh, TLS, NAT traversal
```

Squirrel sits at the top. It decides *what* to run and *where*;
ToadStool executes the compute; Songbird provides the network fabric
that connects them. Together they deliver sovereign AI inference — no
cloud required, no vendor SDK, pure Rust end to end.

### 2.1 Squirrel + ToadStool: Local GPU Inference

**The core local AI pattern.** Squirrel routes inference to ToadStool
when GPU acceleration is beneficial and available.

```
1. ai.query { prompt: "Summarize this EOS dataset..." }
2. Squirrel evaluates providers:
   - Cloud API: available, ~500ms, $0.003/1K tokens
   - ToadStool local: available, ~200ms, free, GPU sm_89
3. Squirrel selects ToadStool (lower latency, zero cost, sovereign)
4. compute.submit { model: "llama-3.1-8b", prompt: ..., max_tokens: 256 }
   → result from on-device GPU inference
5. Squirrel returns result to caller (provider: "toadstool:gpu-0")
```

The caller asked `ai.query` — they don't know (or care) that inference
ran on a local GPU via ToadStool. Squirrel handles the routing decision,
context formatting, and result normalization.

**Spring applications**:
- hotSpring: EOS parameter estimation using local LLM + ToadStool GPU
  instead of cloud API (data never leaves the machine)
- healthSpring: Patient data summarization on-device (HIPAA compliance
  via zero-exfiltration inference)
- neuralSpring: Hyperparameter suggestions from local model (no API
  latency in tight training loops)
- groundSpring: Real-time seismic waveform classification at the edge
  (no internet required)

### 2.2 Squirrel + Songbird: Federated Model Discovery

**AI provider discovery across the network.** Songbird finds remote
Squirrel instances and their available models.

```
1. Songbird: discovery.register {
     primal: "squirrel",
     capabilities: ["ai.query", "ai.chat"],
     metadata: { models: ["llama-3.1-70b", "mixtral-8x7b"], gpu: true }
   }
2. (Remote Squirrel instance does the same)
3. Songbird: discovery.query { capability: "ai.query" }
   → [
     { primal: "squirrel-site-a", models: ["llama-3.1-70b"], latency_ms: 50 },
     { primal: "squirrel-site-b", models: ["mixtral-8x7b"], latency_ms: 120 }
   ]
4. Squirrel routes to the best available instance
```

In a multi-site deployment, this enables federated inference — each site
has its own Squirrel + ToadStool, and Songbird weaves them into a single
discovery mesh. The caller's `ai.query` transparently routes to whichever
site has the best model for the task.

**Spring applications**:
- wetSpring: Multi-lab consortium where each lab runs its own models;
  queries route to the lab with the best bioinformatics model
- airSpring: Regional weather stations with local models; federation
  for cross-region analysis
- ludoSpring: Game servers with per-region AI; Songbird discovery
  routes NPC dialogue to the nearest model instance

### 2.3 Squirrel + ToadStool + Songbird: Sovereign AI Mesh

**The complete pattern — biomeOS composes the trio as a deploy graph.**

```
1. biomeOS starts Songbird           → discovery mesh active
2. biomeOS starts ToadStool          → discovers GPU, registers with Songbird
3. biomeOS starts Squirrel           → discovers ToadStool via Songbird
4. Squirrel registers with Songbird  → announces ai.* capabilities
5. Spring calls ai.query             → Squirrel routes to ToadStool GPU
6. Result returned                   → sovereign, zero-cloud, zero-vendor
```

The entire inference pipeline is sovereign: Rust binaries, no C FFI,
no vendor SDK, no cloud dependency. Springs invoke `ai.query` and get
intelligence from wherever the ecosystem has compute.

Deploy graph (`squirrel_deploy.toml`):

```toml
[[graph.steps]]
name = "discovery"
primal = "songbird"

[[graph.steps]]
name = "compute"
primal = "toadstool"
depends_on = ["discovery"]

[[graph.steps]]
name = "ai"
primal = "squirrel"
depends_on = ["discovery", "compute"]
```

---

## 3. Squirrel + Other Primals

### 3.1 Squirrel + BearDog: Authenticated AI

**Every AI request can carry cryptographic identity.**

```
1. BearDog: crypto.sign { data: prompt_hash, signer: "did:eco:alice" }
   → signature
2. ai.query { prompt: "...", auth: { signer: "did:eco:alice", signature: "..." } }
   → Squirrel verifies identity before routing
3. Response signed: crypto.sign { data: response_hash }
   → caller can verify response authenticity
```

Signed prompts and responses create a non-repudiable AI interaction
record — who asked what, which model answered, and when. JWT delegation
via BearDog is built in: Squirrel validates `did:eco:` identity tokens
without ever holding private keys.

**Applications**: Tamper-evident clinical AI advice (healthSpring),
authenticated research queries with audit trail (wetSpring, hotSpring),
identity-verified game AI interactions (ludoSpring), signed regulatory
analysis reports (airSpring).

### 3.2 Squirrel + NestGate: Cached Context Persistence

**Context sessions persist beyond memory via NestGate storage.**

```
1. context.create { metadata: { experiment: "eos-sweep-42" } }
   → ctx_id (in-memory DashMap)
2. (many context.update calls accumulate state)
3. storage.put { key: ctx_id, data: serialized_context }
   → NestGate persists (Blake3 content-addressed)
4. (Squirrel restarts)
5. storage.get { key: ctx_id }
   → context restored from NestGate
```

Large context windows (multi-MB accumulated state) can be offloaded
to NestGate. Squirrel keeps hot contexts in memory and cold contexts
in NestGate, bringing them back on demand. Blake3 content addressing
means identical contexts deduplicate automatically.

**Applications**: Long-running experiment advisors that survive restarts
(any spring), multi-day game design sessions (ludoSpring), patient case
histories spanning clinic visits (healthSpring), seasonal field campaign
context (airSpring).

### 3.3 Squirrel + biomeOS: Orchestrated AI Workflows

**biomeOS composes multi-step AI pipelines as deploy graphs.**

```toml
# biomeOS graph: ai_assisted_analysis.toml
[[graph.steps]]
name = "collect_data"
capability = "storage"
operation = "get"

[[graph.steps]]
name = "analyze"
capability = "ai"
operation = "query"
depends_on = ["collect_data"]
params = { prompt_template: "Analyze this {NICHE} dataset: {DATA}" }

[[graph.steps]]
name = "store_result"
capability = "storage"
operation = "put"
depends_on = ["analyze"]

[[graph.steps]]
name = "attribute"
capability = "provenance"
operation = "create_braid"
depends_on = ["analyze"]
```

Springs invoke this as a single graph execution. biomeOS routes each
step to the appropriate primal — Squirrel handles `ai.query`, NestGate
handles `storage.*`, sweetGrass handles `provenance.*`. The spring sees
one atomic operation.

**Applications**: Automated analysis pipelines (any spring), AI-assisted
experiment design loops (wetSpring, hotSpring), intelligent monitoring
with AI interpretation (groundSpring, airSpring).

### 3.4 Squirrel + petalTongue: AI-Powered Visualization

**Squirrel provides intelligence; petalTongue provides representation.**

```
1. ai.query { prompt: "What visualization would best show this EOS phase diagram?" }
   → { suggestion: "heatmap with isotherms", grammar_hint: { geom: "raster", ... } }

2. visualization.render {
     grammar: {
       data: eos_data,
       geom: "raster",
       color: "pressure",
       facet: "temperature"
     }
   }
   → rendered visualization
```

Squirrel can also generate Vega-Lite or petalTongue grammar specs
from natural language descriptions — "show me the correlation between
soil pH and microbial diversity" becomes a concrete visualization spec.

**Applications**: Natural language to chart (any spring), AI-suggested
dashboard layouts (biomeOS monitoring), accessible data exploration
for non-programmers (healthSpring clinicians, airSpring agronomists),
AI-generated game UI mockups (ludoSpring).

### 3.5 Squirrel + rhizoCrypt: AI-Assisted DAG Analysis

**Squirrel analyzes rhizoCrypt session graphs for patterns and anomalies.**

```
1. dag.dehydrate { session_id }
   → { merkle_root, vertex_count: 4200, operations: ["filter", "denoise", ...] }

2. ai.query {
     prompt: "Analyze this DAG session: 4200 vertices, operations: [filter, denoise, classify]. Any anomalies?",
     context: dehydration_summary
   }
   → { anomalies: ["unusual vertex fan-out at step 3"], suggestions: ["consider batching filter ops"] }
```

For science springs with complex computational DAGs, Squirrel can
provide intelligent commentary on session structure — identifying
bottlenecks, suggesting parallelization, and flagging anomalous patterns.

**Applications**: Pipeline optimization suggestions (wetSpring DADA2
runs), training graph analysis (neuralSpring), game session replay
analysis (ludoSpring), experiment workflow auditing (any spring).

### 3.6 Squirrel + sweetGrass: Attributed AI Contributions

**AI contributions are properly attributed in the provenance record.**

```
1. ai.query { prompt: "Classify these ASVs..." }
   → { response: "...", provider: "llama-3.1-8b", model_version: "..." }

2. braid.create {
     activity: { type: "ai_classification" },
     agents: [
       { did: "did:eco:alice", role: "Creator", weight: 0.7 },
       { did: "did:eco:squirrel:llama-3.1-8b", role: "Analyst", weight: 0.3 }
     ],
     entity: { data: classification_result_hash }
   }
   → braid_id (AI's contribution is on record)
```

Squirrel's `ai.list_providers` response includes model identifiers
that map directly to sweetGrass agent DIDs. This closes the attribution
gap — every AI-generated insight carries a record of which model
produced it, alongside the human who prompted it.

**Applications**: AI co-authorship tracking for publications (wetSpring,
hotSpring), AI-assisted game design credit (ludoSpring), AI diagnostic
contribution in clinical settings (healthSpring), transparent AI
involvement in regulatory submissions (airSpring).

### 3.7 Squirrel + LoamSpine: Permanent AI Decision Records

**Critical AI decisions committed to immutable ledger.**

```
1. ai.query { prompt: "Recommend dosing for patient profile X..." }
   → { response: "500mg q12h", confidence: 0.92, model: "med-llm-v3" }

2. entry.append {
     spine_id: patient_spine,
     entry_type: "DataAnchor",
     payload: {
       content_hash: response_hash,
       ai_model: "med-llm-v3",
       confidence: 0.92,
       prompt_hash: prompt_hash
     }
   }
   → permanent, hash-chained record of AI recommendation
```

The AI's recommendation, the model version, and the confidence score
are all committed to an immutable spine. If the recommendation is
later questioned, the full chain of evidence exists — what was asked,
which model answered, and how confident it was.

**Applications**: Clinical AI audit trails (healthSpring — FDA/HIPAA),
regulatory AI analysis provenance (airSpring — USDA), AI-assisted
experimental design records (wetSpring, hotSpring), AI balance
decisions in competitive games (ludoSpring tournament integrity).

### 3.8 Squirrel + skunkBat: AI-Powered Threat Analysis

**Squirrel provides intelligence for skunkBat's threat assessment.**

```
1. skunkBat detects anomalous network pattern
2. ai.query {
     prompt: "Analyze this traffic pattern: [metadata]. Is this a DDoS, port scan, or benign?",
     context: baseline_traffic_profile
   }
   → { classification: "port_scan", confidence: 0.87, recommended_action: "monitor" }
3. skunkBat adjusts defense posture based on AI assessment
```

skunkBat handles detection; Squirrel provides the reasoning. The
separation ensures skunkBat remains metadata-only (no content
inspection) while getting intelligent classification from Squirrel.

**Applications**: Intelligent intrusion detection (any deployment),
anomaly explanation for security dashboards (biomeOS), AI-assisted
incident response (graduated defense with reasoning).

### 3.9 Squirrel + coralReef + barraCuda: AI-Guided Shader Selection

**Squirrel advises which mathematical approach to take; the Sovereign
Compute Pipeline executes it.**

```
1. Spring: "I need to compute FFT on 10M soil sensor readings"
2. ai.query {
     prompt: "Best approach for FFT on 10M f64 readings: split-radix, Bluestein, or mixed-radix?",
     context: { size: 10_000_000, precision: "f64", target: "nvidia_sm89" }
   }
   → { recommendation: "split-radix", rationale: "power-of-2 friendly, optimal for GPU" }
3. barraCuda: select wgsl shader "fft_split_radix_f64"
4. coralReef: compile → SPIR-V
5. ToadStool: dispatch → GPU result
```

Squirrel doesn't execute the math — it advises on approach selection.
The Sovereign Compute Pipeline (barraCuda → coralReef → ToadStool)
does the execution. This separation of intelligence from computation
is the ecosystem's core design principle.

**Applications**: Algorithm selection for large-scale computation
(hotSpring lattice QCD), precision/performance tradeoff advice
(groundSpring seismic inversion), batch strategy for training runs
(neuralSpring).

---

## 4. Novel Spring Compositions

These are higher-order patterns that emerge from combining Squirrel
with multiple primals simultaneously.

### 4.1 AI Experiment Advisor

**Springs**: any + Squirrel + rhizoCrypt + sweetGrass + LoamSpine

A persistent AI advisor that accumulates experiment knowledge across
sessions and provides increasingly informed guidance:

```
1. context.create { metadata: { experiment: "pfas-biodeg-2026" } }
   → ctx_id

2. (Experiment round 1)
   dag.create_session → rhizoCrypt session
   (spring work happens)
   dag.dehydrate → summary_1
   context.update { id: ctx_id, data: summary_1 }

3. ai.query { prompt: "Given rounds 1-N, what should round N+1 test?",
              context: ctx_id }
   → { suggestion: "Increase carbon source concentration...", rationale: "..." }

4. braid.create { agents: [researcher, "did:eco:squirrel:*"], derived_from: [round_N] }
   → attribution for AI's experimental design contribution

5. commit.session { session_id: ctx_id, spine_id: experiment_spine }
   → permanent record of AI-guided experimental progression
```

The context window accumulates across all rounds. The AI's suggestions
improve as more data flows in. The provenance record captures both
human and AI contributions. The spine stores the entire trajectory
permanently.

**Domain applications**:
- **wetSpring**: Multi-round PFAS biodegradation screening — AI suggests
  which bacterial consortia to test next based on prior results
- **hotSpring**: Iterative EOS parameter sweeps — AI narrows the search
  space based on prior fit residuals
- **neuralSpring**: Active learning loops — AI suggests which data to
  label next for maximum model improvement
- **healthSpring**: Adaptive clinical trial design — AI recommends
  dosing adjustments based on interim results

### 4.2 Intelligent Data Marketplace

**Springs**: any + Squirrel + LoamSpine + NestGate + sweetGrass + Songbird

Squirrel acts as the intelligent broker for ecosystem data exchange:

```
1. Producer: NestGate stores dataset, LoamSpine certificates ownership
2. Consumer: "I need soil microbiome data from semi-arid regions"
3. Squirrel: ai.query {
     prompt: "Match this request to available datasets",
     context: { request: consumer_query, catalog: discovered_datasets }
   }
   → { matches: [{ dataset: "soil-metagenome-arid-2026", relevance: 0.91 }] }
4. LoamSpine: certificate.loan → access granted under terms
5. sweetGrass: braid.create → attribution for data producer
```

Squirrel provides the intelligence layer — understanding what the
consumer needs and matching it against what's available. The other
primals handle storage, ownership, and attribution.

**Domain applications**:
- **wetSpring**: AI-matched genomic reference data sharing between labs
- **airSpring**: Intelligent weather model exchange across agricultural
  cooperatives
- **neuralSpring**: Model weight marketplace with AI-assessed fitness
  for specific downstream tasks
- **ludoSpring**: AI-curated game asset marketplace matching style and
  theme compatibility

### 4.3 Multi-Model Deliberation

**Springs**: any + Squirrel + BearDog + sweetGrass

Multiple AI models evaluate the same question; Squirrel synthesizes
the consensus and attributes each model's contribution:

```
1. ai.query { prompt: "Is this seismic event tectonic or induced?",
              model: "model-a" }
   → { answer: "tectonic", confidence: 0.78 }

2. ai.query { prompt: "Is this seismic event tectonic or induced?",
              model: "model-b" }
   → { answer: "induced", confidence: 0.65 }

3. ai.query { prompt: "Is this seismic event tectonic or induced?",
              model: "model-c" }
   → { answer: "tectonic", confidence: 0.82 }

4. ai.query {
     prompt: "Synthesize these three model opinions into a consensus",
     context: [response_a, response_b, response_c]
   }
   → { consensus: "likely tectonic (2/3 agree, higher confidence)",
       dissent: "model-b suggests induced — worth investigating" }

5. sweetGrass: braid.create {
     agents: [
       { did: "did:eco:squirrel:model-a", role: "Analyst", weight: 0.35 },
       { did: "did:eco:squirrel:model-b", role: "Analyst", weight: 0.25 },
       { did: "did:eco:squirrel:model-c", role: "Analyst", weight: 0.40 }
     ]
   }
```

Each model's contribution is weighted and attributed. The deliberation
pattern reduces single-model bias and creates a provenance record of
how the conclusion was reached.

**Domain applications**:
- **groundSpring**: Seismic event classification with model consensus
- **healthSpring**: Differential diagnosis with multiple medical LLMs
- **hotSpring**: EOS phase boundary classification with ensemble AI
- **wetSpring**: Taxonomy assignment with multiple bioinformatics models
- **ludoSpring**: Game balance assessment from multiple AI playtesting agents

### 4.4 AI-Driven Regulatory Narrative

**Springs**: healthSpring/wetSpring/airSpring + Squirrel + LoamSpine + sweetGrass + BearDog

Squirrel generates human-readable narratives from structured data
for regulatory submissions:

```
1. (Experiment complete, all data on LoamSpine spine)
2. entry.get_tip { spine_id: experiment_spine }
   → all session commits, data anchors, certificate events

3. ai.query {
     prompt: "Generate an FDA-compliant summary of this experimental pipeline",
     context: { spine_entries: [...], attribution_braids: [...] }
   }
   → { narrative: "Study XYZ-2026 conducted 14 rounds of PK modeling...",
       citations: [entry_hash_1, entry_hash_2, ...] }

4. crypto.sign { data: narrative_hash, signer: "did:eco:institution" }
   → signed regulatory submission

5. entry.append { spine_id, entry_type: "DataAnchor",
     payload: { type: "regulatory_narrative", hash: narrative_hash } }
   → narrative permanently recorded alongside the data it describes
```

The AI-generated narrative cites specific spine entries (verifiable
via inclusion proofs). The signed narrative is itself committed to
the spine, creating a self-referential audit package.

**Domain applications**:
- **healthSpring + FDA**: AI-generated clinical trial summaries with
  hash-linked evidence
- **wetSpring + EPA**: PFAS screening narratives with instrument
  calibration provenance
- **airSpring + USDA**: Water rights justification narratives with
  ET₀ computation chain

### 4.5 Conversational Ecosystem Explorer

**Springs**: all + Squirrel + Songbird + petalTongue

A natural language interface to the entire running ecosystem:

```
User: "What primals are running and how healthy are they?"
  → Squirrel: discovery.peers {} → 6 primals
  → For each: system.health {} → status
  → ai.query { prompt: "Summarize ecosystem health", context: health_data }
  → petalTongue: visualization.render { grammar: health_dashboard }

User: "Show me wetSpring's latest experiment results"
  → Squirrel: context from NestGate/LoamSpine
  → ai.query { prompt: "Summarize wetSpring results" }
  → petalTongue: render results

User: "Why is ToadStool's latency high?"
  → Squirrel: system.metrics from ToadStool
  → ai.query { prompt: "Diagnose latency spike", context: metrics }
  → { diagnosis: "GPU memory pressure from concurrent FFT jobs" }
```

Squirrel becomes the ecosystem's conversational interface. Any question
about the running system — health, performance, data, history — gets
routed to the appropriate primals, synthesized by AI, and rendered by
petalTongue.

**Applications**: Operator dashboards (biomeOS), researcher portals
(any spring), game master tools (ludoSpring), clinical decision
support systems (healthSpring).

### 4.6 AI-Optimized Deployment Graphs

**Springs**: any + Squirrel + biomeOS + ToadStool

Squirrel analyzes biomeOS deploy graphs and suggests optimizations:

```
1. biomeOS: current deploy graph (13 steps, 4 primals)
2. ai.query {
     prompt: "Optimize this deploy graph for latency",
     context: {
       graph: deploy_graph,
       capability_costs: capability_list_responses,
       hardware: toadstool_inventory
     }
   }
   → {
     suggestions: [
       "Steps 3-5 can run in parallel (no data dependency)",
       "Move ai.query to GPU node (500ms → 200ms with ToadStool)",
       "context.create is cheap — move to early initialization"
     ],
     optimized_graph: { ... }
   }
```

Squirrel uses its knowledge of capability costs (`capability.list`)
and ToadStool's hardware inventory to suggest deploy graph
optimizations that biomeOS can apply.

**Applications**: Automated pipeline optimization (any spring),
resource-aware scheduling (HPC environments), latency-critical
game server deployment (ludoSpring).

### 4.7 Cross-Spring Knowledge Synthesis

**Springs**: multiple + Squirrel + NestGate + sweetGrass + LoamSpine

When multiple springs produce results about related phenomena, Squirrel
synthesizes cross-domain insights:

```
1. wetSpring: "Soil microbiome diversity dropped 30% at site 7"
2. airSpring: "ET₀ anomaly detected at site 7: 2.3σ above seasonal mean"
3. groundSpring: "Soil moisture sensor 7-B shows calibration drift"

4. ai.query {
     prompt: "Correlate these cross-spring observations at site 7",
     context: [wetspring_result, airspring_anomaly, groundspring_drift]
   }
   → {
     synthesis: "Sensor drift in ground moisture readings (groundSpring) likely caused
       the ET₀ anomaly (airSpring). The microbiome shift (wetSpring) may be
       independent — recommend soil sampling before attributing to irrigation.",
     confidence: 0.73,
     recommended_actions: ["recalibrate sensor 7-B", "collect soil core at site 7"]
   }

5. sweetGrass: braid.create { derived_from: [ws_braid, as_braid, gs_braid],
     agents: [{ did: "did:eco:squirrel:*", role: "Analyst" }] }
   → cross-spring synthesis attributed
```

No individual spring could produce this insight. Squirrel provides
the cross-domain reasoning layer, synthesizing observations that span
biology (wetSpring), climate (airSpring), and instrumentation
(groundSpring).

**Domain applications**:
- **Ecology study**: Microbiome + climate + soil cross-correlation
- **Drug development**: PK/PD (healthSpring) + gut microbiome (wetSpring)
  + biomarker model (neuralSpring) correlation
- **Game science**: Player behavior (ludoSpring) + ML model predictions
  (neuralSpring) + physics simulation fidelity (hotSpring)

---

## 5. Integration Patterns for Springs

### Minimal Integration (standalone Squirrel only)

Add to your spring's `Cargo.toml` under an optional feature:

```toml
[dependencies]
neural-api-client-sync = { path = "../../phase2/biomeOS/crates/neural-api-client-sync", optional = true }

[features]
ai = ["neural-api-client-sync"]
```

Then call via the Neural API bridge:

```rust
use neural_api_client_sync::NeuralBridge;

let bridge = NeuralBridge::discover()?;

let response = bridge.capability_call("ai", "query", &json!({
    "prompt": "Classify this sample: ...",
    "max_tokens": 256,
    "temperature": 0.1
}))?;
```

The spring never imports Squirrel directly. It discovers the capability
at runtime. If Squirrel is not running, the call fails gracefully.

### Context-Managed Integration

For multi-turn AI interactions:

```rust
let bridge = NeuralBridge::discover()?;

let ctx = bridge.capability_call("context", "create", &json!({
    "metadata": { "niche": "airspring", "purpose": "irrigation-advisor" }
}))?;
let ctx_id = ctx["id"].as_str().unwrap();

bridge.capability_call("context", "update", &json!({
    "id": ctx_id,
    "data": { "et0": 6.2, "soil_moisture": 0.23, "forecast": "dry_3d" }
}))?;

let advice = bridge.capability_call("ai", "query", &json!({
    "prompt": format!("Given context {ctx_id}, should we irrigate today?"),
    "temperature": 0.2
}))?;

let summary = bridge.capability_call("context", "summarize", &json!({
    "id": ctx_id
}))?;
```

### Tool-Use Integration (AI Agents)

For springs that expose tools to AI agents:

```rust
let bridge = NeuralBridge::discover()?;

let tools = bridge.capability_call("tool", "list", &json!({}))?;

let result = bridge.capability_call("ai", "query", &json!({
    "prompt": "Use available tools to analyze this seismic event",
    "tools": tools,
    "tool_choice": "auto"
}))?;
```

### Deploy Graph (biomeOS orchestration)

For automated AI-in-the-loop workflows:

```rust
bridge.capability_call("graph", "execute", &json!({
    "graph": "ai_assisted_analysis",
    "params": {
        "DATA_ID": dataset_id,
        "AGENT_DID": agent_did,
        "NICHE": "wetspring",
        "MAX_TOKENS": 512
    }
}))?;
```

---

## 6. What Squirrel Does NOT Do

| Concern | Who Handles It |
|---------|---------------|
| Cryptographic operations | BearDog (crypto.*, auth.*) |
| Content blob storage | NestGate (storage.*) |
| Network transport / TLS | Songbird (discovery.*, transport.*) |
| GPU compute dispatch | ToadStool (compute.*) |
| Immutable ledger | LoamSpine (spine.*, entry.*, commit.*) |
| Ephemeral working memory | rhizoCrypt (dag.*) |
| Provenance / attribution | sweetGrass (braid.*, provenance.*, contribution.*) |
| Visualization / UI | petalTongue (visualization.*) |
| Threat detection | skunkBat (security.*) |
| Shader compilation | coralReef (compile.*) |
| WGSL math authoring | barraCuda (shader.*) |
| Ecosystem orchestration | biomeOS (Neural API) |
| Reward distribution | sunCloud (reward.*) |

Squirrel answers "what does the AI think?" It does not store data,
sign documents, render charts, or run computations. It selects models,
manages context, orchestrates tools, and returns answers. Everything
else is discovered at runtime and composed by biomeOS. Intelligence
through coordination, not through coupling.

---

## References

- `wateringHole/LOAMSPINE_LEVERAGE_GUIDE.md` — Permanence primal guide
- `wateringHole/SWEETGRASS_LEVERAGE_GUIDE.md` — Attribution primal guide
- `wateringHole/RHIZOCRYPT_LEVERAGE_GUIDE.md` — Working memory primal guide
- `wateringHole/SPRING_PROVENANCE_TRIO_INTEGRATION_PATTERN.md` — Integration template
- `wateringHole/CROSS_SPRING_DATA_FLOW_STANDARD.md` — Time series exchange format
- `wateringHole/INTER_PRIMAL_INTERACTIONS.md` — RootPulse coordination flows
- `whitePaper/gen3/PRIMAL_CATALOG.md` — Full primal catalogue
- `whitePaper/gen3/ECOSYSTEM_ARCHITECTURE.md` — NUCLEUS architecture
- `wateringHole/BIOMEOS_LEVERAGE_GUIDE.md` — fieldMouse (minimal deployable unit) vs. niche
- `phase1/squirrel/capability_registry.toml` — Squirrel capability source of truth
- `phase1/squirrel/crates/main/src/niche.rs` — Niche self-knowledge
