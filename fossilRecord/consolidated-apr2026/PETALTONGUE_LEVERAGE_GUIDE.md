# petalTongue Leverage Guide — Standalone, Trio, and Ecosystem Compositions

**Version**: 3.0.0  
**Date**: March 16, 2026  
**Audience**: Springs, primals, and ecosystem architects  
**Purpose**: How to leverage petalTongue — the Universal User Interface primal — alone, in duos, in trios, and in novel cross-primal combinations across the full 21-primal ecosystem

Each primal in the ecosystem produces an equivalent guide. Together, these guides form a combinatorial recipe book for emergent behaviors.

---

## What petalTongue Offers

petalTongue is the **Universal User Interface** primal. It accepts data through IPC and translates it across every available modality — visual display (egui), terminal display (ratatui TUI), audio sonification, SVG export, terminal character grids, braille tactile grids, haptic command sequences, JSON API, and GPU command buffers. The UUI philosophy: *One Engine, Infinite Representations* — from dolphin to human, paraplegic dev to blind hiker.

petalTongue follows the **SAME DAVE** model (Sensory Afferent, Motor Efferent) — bidirectional feedback loops where every output channel has a corresponding input channel. The canonical terminology lives in `petal_tongue_core::uui_glossary`.

It also provides interactive features: selection, zoom, pan, perspectives, AI-driven focus (via Squirrel), and provenance tracking that traces every rendered pixel back to its source data.

Key capabilities available to any spring or primal via JSON-RPC:

| Capability | Method | What it does |
|-----------|--------|-------------|
| Render data | `visualization.render` | Send DataBindings or spring-native format; auto-compiles to Grammar of Graphics |
| Render raw scene | `visualization.render.scene` | Send a SceneGraph directly — arbitrary visual scenes, not just charts |
| Stream updates | `visualization.render.stream` | Incremental append/replace for real-time data |
| Multi-panel dashboard | `visualization.render.dashboard` | Compose multiple bindings into a themed grid layout |
| Export modality | `visualization.export` | Get SVG, audio, description, haptic, GPU, braille, terminal output |
| Validate before render | `visualization.validate` | Pre-flight Tufte constraint check (data-ink ratio, lie factor, accessibility) |
| Session discovery | `visualization.session.list` | Discover what's currently being visualized |
| Interaction subscribe | `interaction.subscribe` | Receive selection/hover/focus events as they happen |
| Sensor stream | `interaction.sensor_stream.subscribe` | Poll batched sensor events (60 Hz capable) |
| Graph topology | `visualization.render_graph` | Render primal topology as SVG or terminal art |
| Motor commands | `motor.*` | Drive UI state programmatically (panel, zoom, mode, navigate) |
| Introspect | `visualization.introspect` | Query what panels/data are currently visible |
| Provenance | `visualization.showing` | Check if a specific data_id is currently displayed |

All data formats are accepted: the `SpringDataAdapter` auto-detects ludoSpring game channels, ecoPrimals/time-series/v1 envelopes, standard DataBinding arrays, and raw bindings envelopes.

---

## Part 1: One Spring + petalTongue

Each spring can leverage petalTongue independently. No third primal needed — just a Unix socket and JSON-RPC.

### healthSpring → petalTongue

**Already wired.** healthSpring's 6 DataBinding types map directly:

| healthSpring Data | petalTongue Rendering |
|------------------|----------------------|
| PK/PD curves (TimeSeries) | Line charts with temporal axis, threshold coloring for therapeutic range |
| Microbiome abundances (Bar) | Categorical bar charts with health-domain palette |
| Endocrine correlation (Heatmap) | Color-coded matrix with normal/warning/critical cells |
| Diagnostic gauge (Gauge) | Arc or bar with normal range annotation |
| Biosignal spectrum (Spectrum) | Area chart with frequency-domain axis |
| Patient distribution (Distribution) | Histogram with mean/SD markers |

**Novel leverage**: Stream PK/PD curves in real-time during simulated dosing intervals. Use `visualization.render.dashboard` to compose a patient overview: PK curve + microbiome bar + endocrine heatmap + vitals gauges in a single themed panel. Subscribe to `interaction.subscribe` to let clinicians click on an anomalous heatmap cell and receive the cell coordinates back for drill-down.

### hotSpring → petalTongue

**Partially wired** (JSONL telemetry → TimeSeries). hotSpring can push much more:

| hotSpring Data | petalTongue Rendering |
|---------------|----------------------|
| Plasma density evolution (TimeSeries) | Streaming line chart at simulation tick rate |
| Lattice QCD gauge field (Heatmap) | 2D slice visualization with physics palette |
| Spectral eigenvalues (Scatter) | Eigenvalue distribution in complex plane |
| Transport coefficients (Bar) | Comparative bar charts across parameter sweeps |
| Phase diagrams (FieldMap) | 2D field with isolines and domain coloring |

**Novel leverage**: Use `visualization.render.scene` to send custom SceneGraphs for phase-space trajectories — hotSpring computes the physics, petalTongue renders arbitrary parametric curves as BezierPath primitives. Use the Mesh primitive for 3D lattice slice projections. Stream simulation state at each timestep via `visualization.render.stream` to create live plasma evolution animations.

### wetSpring → petalTongue

**Already wired** (backpressure streaming, Scatter 2D ordinations).

| wetSpring Data | petalTongue Rendering |
|---------------|----------------------|
| 16S ordinations (Scatter) | PCoA/NMDS scatter with sample-group colors |
| LC-MS chromatograms (TimeSeries) | Retention time vs intensity peaks |
| PFAS concentration (Bar) | Categorical comparison across sample sites |
| Microbial diversity (Distribution) | Shannon/Simpson index histograms |
| Correlation matrices (Heatmap) | OTU co-occurrence heatmaps |

**Novel leverage**: Use `visualization.render.dashboard` to create a full analytical workbench: chromatogram + ordination scatter + diversity histogram + co-occurrence heatmap. Stream LC-MS peaks in real-time as they're identified. Use `visualization.export` with modality `"description"` to generate accessible text descriptions of ordination patterns for report generation.

### airSpring → petalTongue

| airSpring Data | petalTongue Rendering |
|---------------|----------------------|
| ET₀ curves across 8 methods (TimeSeries faceted) | Small multiples via `compile_faceted()` — one panel per method |
| Soil moisture profiles (FieldMap) | Depth × position field with soil-moisture palette |
| IoT sensor readings (Gauge, streaming) | Live gauge dashboard for irrigation stations |
| Richards PDE solution (Heatmap) | Spatial discretization with time animation |
| Yield predictions (Bar) | Categorical comparison across management zones |

**Novel leverage**: Use `visualization.render.dashboard` with 8 panels — one per ET₀ method — to visually compare Penman-Monteith vs Hargreaves vs Priestley-Taylor side by side. Stream IoT sensor data at field resolution via `interaction.sensor_stream.subscribe` for real-time irrigation monitoring. Use the FieldMap binding for spatial soil visualizations that no generic chart library can do.

### groundSpring → petalTongue

| groundSpring Data | petalTongue Rendering |
|------------------|----------------------|
| Measurement uncertainty budgets (Bar) | Stacked bars showing error contribution per source |
| Noise spectra (Spectrum) | Power spectral density with Allan variance overlays |
| Error propagation chains (SceneGraph) | Custom DAG scene showing how uncertainty flows |
| Sensor calibration curves (Scatter) | Measured vs reference with confidence bands |

**Novel leverage**: groundSpring quantifies uncertainty for every spring. Use `visualization.render.scene` to build custom provenance-aware DAGs showing uncertainty flow from raw sensor → processing → final result. Combine with petalTongue's `ProvenanceBuffer` — every pixel can be traced to its data source, and groundSpring can annotate that provenance with uncertainty bounds.

### neuralSpring → petalTongue

**Already wired** (pipeline DAGs, diverging palettes).

| neuralSpring Data | petalTongue Rendering |
|------------------|----------------------|
| Training loss curves (TimeSeries) | Live streaming during model training |
| Model architecture (SceneGraph) | Layer-by-layer network visualization via `render.scene` |
| Prediction distributions (Distribution) | Histograms of model output uncertainty |
| Feature importance (Bar) | Ranked bar charts |
| Attention heatmaps (Heatmap) | Transformer attention weight matrices |

**Novel leverage**: Use `visualization.render.scene` to send neuralSpring's computation DAG as a live SceneGraph — nodes are layers, edges are dataflow, and node opacity reflects activation magnitude. Subscribe to `interaction.subscribe` to let researchers click on a layer node and receive the layer_id back for inspection. Use `visualization.export` with `"terminal"` modality for headless training server monitoring.

### ludoSpring → petalTongue

**Already wired** (7 GameChannelType mappings, 60 Hz sensor feed).

| ludoSpring Channel | petalTongue Rendering |
|-------------------|----------------------|
| EngagementCurve | TimeSeries — player engagement over time |
| DifficultyProfile | TimeSeries — difficulty across game sections |
| FlowTimeline | Bar — Csikszentmihalyi flow-state phases |
| UiAnalysis | Bar — Fitts/Hick/Steering law metrics |
| InteractionCostMap | Heatmap — spatial input cost matrix |
| GenerationPreview | Scatter — procedural generation sample points |
| AccessibilityReport | Heatmap — accessibility compliance matrix |

**Novel leverage**: ludoSpring is the first spring that can fully exercise petalTongue's 60 Hz sensor stream. Stream `interaction.sensor_stream.subscribe` for real-time player input telemetry. Use `motor.set_panel` and `motor.navigate` to have the game itself drive petalTongue's UI — when a player enters a new zone, the analytics dashboard switches panels automatically. Use Squirrel (AI adapter) to have an AI analyze the engagement curve and auto-focus petalTongue on the anomalous region.

### primalSpring → petalTongue

**Validates**: petalTongue's visualization pipeline — exp043 tests biomeOS SSE events flowing through petalTongue rendering. fieldMouse deployments (minimal edge units) can run petalTongue's TUI mode for edge visualization.

---

## Part 1B: Using petalTongue with Foundation Primals

Every primal in the ecosystem can leverage petalTongue for representation. Here's how each foundation primal can use petalTongue directly — no third party needed.

### BearDog → petalTongue

**Status**: Not yet wired.

| BearDog Data | petalTongue Rendering |
|-------------|----------------------|
| Key exchange events (TimeSeries) | Timeline showing handshake frequency, latency spikes |
| Identity chain (SceneGraph) | DAG visualization: Ed25519 → X.509 cert → lineage tree |
| Dark Forest beacon activity (Heatmap) | Temporal heatmap of discovery beacons sent/received |
| Encryption throughput (Gauge) | Live gauge for ChaCha20-Poly1305 / AES-GCM ops/sec |
| HSM status (Bar) | Categorical bar: SoloKey vs StrongBox vs software keyring |

**Novel leverage**: Use `visualization.render.scene` to render BearDog's genetic lineage tree as a DAG — each node is a key generation event, edges are derivation chains. Overlay Dark Forest beacon patterns as a temporal heatmap to show when the node is visible vs cloaked. Subscribe to `interaction.subscribe` so an operator clicking on a key node can trigger `beardog.key.inspect` for details.

### Songbird → petalTongue

**Status**: Discovery wired. Topology visualization available.

| Songbird Data | petalTongue Rendering |
|--------------|----------------------|
| Primal topology (SceneGraph) | Force-directed graph of discovered primals and connections |
| Federation graph (SceneGraph) | Multi-tower federation topology with trust edges |
| Discovery events (TimeSeries) | Timeline of mDNS announcements, registrations, heartbeats |
| NAT traversal state (Bar) | Categorical: direct/STUN/relay per peer |
| Network health (Gauge) | Latency, packet loss, connection count gauges |

**Novel leverage**: Stream Songbird's discovery events via `visualization.render.stream` to build a live animation of the ecosystem coming alive at startup — nodes appear as primals register, edges form as they discover each other. Use `motor.set_zoom` to auto-focus on newly discovered primals. The operator sees the ecosystem self-organize in real time.

### NestGate → petalTongue

**Status**: Not yet wired.

| NestGate Data | petalTongue Rendering |
|--------------|----------------------|
| Storage utilization (Gauge) | Fill gauges per storage pool (ZFS, object store) |
| Content-addressed blob graph (SceneGraph) | DAG showing blob → tree → metadata relationships |
| Quota usage (Bar) | Per-primal quota consumption bars |
| Deduplication ratio (TimeSeries) | Efficiency over time as content accumulates |

**Novel leverage**: petalTongue can use NestGate as an **artifact store**. When petalTongue exports a dashboard as SVG, it calls `storage.put` to persist the artifact in NestGate's content-addressed store. Other primals can retrieve it via `storage.get`. This turns petalTongue from a transient renderer into a permanent record — every dashboard ever rendered is addressable by BLAKE3 hash. Combine with LoamSpine for immutable receipts.

### Squirrel → petalTongue

**Status**: Adapter wired (SquirrelAdapter in frame loop).

| Squirrel Data | petalTongue Rendering |
|--------------|----------------------|
| MCP routing decisions (TimeSeries) | Timeline showing which AI provider handled each query |
| Inference latency (Distribution) | Histogram of response times across providers |
| Context window utilization (Gauge) | How full the context is per active conversation |
| Provider health (Bar) | Status bars: Ollama/Anthropic/OpenAI availability |

**Novel leverage**: Squirrel is petalTongue's **AI co-pilot**. Squirrel subscribes to `interaction.subscribe` and watches what the human is looking at. When an anomaly appears in any dashboard, Squirrel analyzes the visible data via its AI providers and sends `ai.focus`, `ai.select`, or `ai.highlight` interaction events back to petalTongue. The human sees the AI's attention as a soft glow on the anomalous region — no words needed, just shared visual attention. Use `motor.navigate` to let Squirrel literally steer the interface.

### ToadStool → petalTongue

**Status**: Window lifecycle wired. Frame submission NOT yet connected.

| ToadStool Data | petalTongue Rendering |
|---------------|----------------------|
| Compute mesh topology (SceneGraph) | GPU/NPU/CPU dispatch graph showing workload flow |
| Shader compilation events (TimeSeries) | Timeline of WGSL → native compilation |
| Workload distribution (Heatmap) | Device × time heatmap of utilization |
| Frame timing (TimeSeries) | Frame present latency, jitter, dropped frames |

**Novel leverage**: ToadStool is petalTongue's **display backend**. When `display.present` is wired, petalTongue can push pixel buffers to ToadStool for GPU-accelerated display. But the reverse is also valuable: ToadStool sends its compute mesh state to petalTongue for operator visualization — the operator sees which GPU is running what shader, which NPU has the neural workload, and which device is idle. Use `visualization.render.dashboard` to compose a compute-health dashboard alongside the application's own data display.

### biomeOS → petalTongue

**Status**: SSE events wired. Neural API registration complete.

| biomeOS Data | petalTongue Rendering |
|-------------|----------------------|
| NUCLEUS health (Gauge) | Per-node health gauges across the nest |
| Primal coordination state (SceneGraph) | Live graph of which primals are bonded, migrating, or failed |
| Workload distribution (Heatmap) | Tower × primal × time utilization matrix |
| Capability routing (TimeSeries) | Timeline of semantic method calls and their resolution paths |

**Novel leverage**: biomeOS is the **nervous system** and petalTongue is the **sensory cortex**. biomeOS streams NUCLEUS health events via SSE; petalTongue renders them as a living organism diagram — healthy nodes glow, struggling nodes dim, failed nodes flash. Use `visualization.render.scene` with custom SceneGraph primitives to build an anatomical view of the ecosystem. Subscribe to `interaction.subscribe` so the operator can click a struggling node and biomeOS can trigger `lifecycle.migrate` or `lifecycle.heal`.

### coralReef → petalTongue

**Status**: Indirect (via barraCuda).

| coralReef Data | petalTongue Rendering |
|---------------|----------------------|
| Shader cache hit rate (TimeSeries) | Compilation avoidance over time |
| Compilation time by target (Bar) | SM70 vs SM89 vs RDNA2 compilation cost |
| f64 lowering statistics (Distribution) | How many shaders needed precision lowering |

**Novel leverage**: coralReef doesn't call petalTongue directly — the flow is always `barraCuda → coralReef → ToadStool`. But coralReef can push its own telemetry (cache hit rates, compilation times) to petalTongue for operator monitoring. When a shader compilation takes abnormally long, petalTongue highlights it in the compute dashboard and Squirrel can correlate it with GPU utilization anomalies.

### barraCuda → petalTongue

**Status**: Physics bridge wired. 3 ops available (zeros, ones, read).

| barraCuda Data | petalTongue Rendering |
|---------------|----------------------|
| GPU utilization (Gauge) | Per-device utilization gauges |
| Shader dispatch history (TimeSeries) | Which ops ran when, latency per dispatch |
| Numerical precision (Distribution) | DF64 emulation error distribution |
| 786 shader inventory (Bar) | Categorical: GEMM/FFT/NTT/MD/QCD shader counts |

**Novel leverage**: barraCuda is petalTongue's **computation engine**. petalTongue offloads heavy visualization math (100K-point layouts, tessellation, projection) to barraCuda. But barraCuda also benefits: when barraCuda runs a Yukawa MD simulation or lattice QCD computation, it can stream intermediate results to petalTongue for live visualization — the researcher sees the simulation evolving in real time, not just the final result. Use `visualization.render.stream` with `append` mode to build up the visualization frame by frame.

---

## Part 1C: Using petalTongue with Post-NUCLEUS Primals

### sourDough → petalTongue

**Status**: Not yet wired.

| sourDough Data | petalTongue Rendering |
|---------------|----------------------|
| Scaffold generation events (TimeSeries) | Timeline of `new-primal` scaffold operations |
| Primal health check results (Bar) | Per-primal lifecycle compliance status |
| Config drift (Heatmap) | Primal × config-key deviation from template |

**Novel leverage**: sourDough scaffolds new primals. It can generate **petalTongue-ready data endpoints** as part of every scaffold template — every new primal born from sourDough automatically knows how to push `visualization.render` to petalTongue. sourDough can also use petalTongue to render its own scaffolding reports: which primals have been created, their health check status, and config drift from the canonical template.

### sweetGrass → petalTongue

**Status**: Provenance trio client wired. `provenance.create_braid` NOT yet called.

| sweetGrass Data | petalTongue Rendering |
|----------------|----------------------|
| Attribution braids (SceneGraph) | DAG showing data provenance chains: source → transform → render |
| Privacy level distribution (Bar) | How many records at each of the 5 privacy levels |
| Time decay curves (TimeSeries) | Attribution relevance decay over time |
| Role distribution (Distribution) | Histogram of 12 role types across the ecosystem |

**Novel leverage**: Every pixel petalTongue renders can carry provenance. When petalTongue renders a PK/PD curve from healthSpring, sweetGrass records the full attribution chain: `healthSpring.data_source` → `petalTongue.grammar_transform` → `petalTongue.modality_compile` → `user.interaction`. Click any rendered element and sweetGrass can trace it back to the raw measurement. This is **render provenance** — unique to petalTongue because it's the only primal that can show the human *why* something looks the way it does.

### LoamSpine → petalTongue

**Status**: Provenance trio client wired. `commit.session` NOT yet called.

| LoamSpine Data | petalTongue Rendering |
|---------------|----------------------|
| Ledger growth (TimeSeries) | Append-only ledger size over time |
| Entry types (Bar) | Categorical: LoamEntry types committed |
| Inclusion proof chain (SceneGraph) | Merkle tree visualization of proof paths |
| Federation sync state (Heatmap) | Peer × time sync completeness matrix |

**Novel leverage**: LoamSpine gives petalTongue **permanence**. Every dashboard petalTongue renders can be dehydrated (SVG + grammar expression + DataBindings) and committed to LoamSpine as an immutable LoamEntry. This creates a permanent fossil record of every visualization ever shown. Combine with NestGate (stores the actual SVG bytes) and sweetGrass (records who saw it, when, why). The result: an auditable, immutable, attributed visual record — essential for regulatory compliance in health, defense, and legal domains.

### rhizoCrypt → petalTongue

**Status**: Provenance trio client wired. `dag.create_session` NOT yet called.

| rhizoCrypt Data | petalTongue Rendering |
|----------------|----------------------|
| Working memory DAG (SceneGraph) | Content-addressed DAG with BLAKE3 vertices |
| Session lifecycle (TimeSeries) | Session creation, scoping, dehydration events |
| Merkle proof verification (Distribution) | Proof depth and verification time histograms |
| Slice semantics (Bar) | Which of the 6 slice types are most used |

**Novel leverage**: rhizoCrypt gives petalTongue **session memory**. Each visualization session (a set of open dashboards, zoom level, selected elements, filter state) can be stored as a DAG in rhizoCrypt's ephemeral memory. Close your laptop, open it tomorrow — petalTongue restores exactly where you left off by querying rhizoCrypt. When the session is worth keeping, `dag.dehydration.trigger` pushes it to LoamSpine for permanent storage. This is **stateful visualization** — the interface remembers.

### skunkBat → petalTongue

**Status**: Not yet wired.

| skunkBat Data | petalTongue Rendering |
|--------------|----------------------|
| Threat detection events (TimeSeries) | Timeline of genetic/topology/behavioral/intrusion alerts |
| Quarantine status (Bar) | Which primals are quarantined, monitored, or clear |
| Resource anomalies (Heatmap) | Primal × resource-type anomaly intensity matrix |
| Defense posture (Gauge) | Ecosystem-wide threat level gauge |

**Novel leverage**: skunkBat operates on metadata only (no content inspection). petalTongue can render skunkBat's threat landscape as a **defense dashboard**: a topology view where node color = threat level, edge thickness = traffic volume, and pulsing animations = active detections. skunkBat sends `visualization.render.stream` with real-time threat updates; petalTongue renders them as a living threat map. The operator can click a quarantined node to see skunkBat's reasoning chain (metadata only, respecting privacy). Use `motor.navigate` to auto-focus on the hottest threat.

---

## Part 2: Trio Combinations

### The Provenance Trio (rhizoCrypt + LoamSpine + sweetGrass) + petalTongue

Every visualization session has provenance. petalTongue can participate in the provenance pipeline:

1. **rhizoCrypt**: When petalTongue renders a visualization, the session metadata (bindings, grammar expression, domain, timestamp) can be appended as a DAG event in rhizoCrypt's working memory
2. **sweetGrass**: The attribution chain — which spring provided the data, which grammar rules transformed it, which user interacted with it — can be braided into a sweetGrass attribution record
3. **LoamSpine**: The final rendered artifact (SVG, scene snapshot) can be dehydrated and committed to LoamSpine for permanent storage

**Flow**: `spring.push_data` → `petalTongue.visualization.render` → `rhizoCrypt.dag.append_event` → `sweetGrass.provenance.create_braid` → `LoamSpine.commit`

**Why this matters**: Regulatory compliance for health data visualizations. When healthSpring renders a PK/PD curve, the provenance trio ensures the rendering is attributable, immutable, and auditable. The clinician can later prove exactly what data was shown, how it was transformed, and who saw it.

### The Compute Trio (barraCuda + coralReef + toadStool) + petalTongue

petalTongue is a visualization consumer, not a compute provider. The compute trio amplifies what petalTongue can display:

1. **barraCuda**: Offload heavy visualization math — N-body layouts, molecular dynamics, large matrix operations — to GPU compute via `gpu.dispatch`
2. **coralReef**: Compile WGSL shaders for GPU-accelerated rendering when petalTongue's `GpuCompiler` modality is requested
3. **toadStool**: Dispatch compiled shaders to actual GPU hardware

**Flow**: `petalTongue.GpuCompiler.compile(scene)` → GPU commands → `barraCuda.compute.dispatch` → `coralReef.compile` → `toadStool.dispatch`

**Why this matters**: When a spring sends a 100,000-point scatter plot or a real-time lattice QCD field, CPU rendering is too slow. The compute trio makes petalTongue scale to scientific datasets.

### The Discovery Pair (Songbird + biomeOS) + petalTongue

petalTongue discovers springs by capability, not by name. Songbird and biomeOS make this work:

1. **Songbird**: mDNS multicast discovery — petalTongue finds springs that announce `visualization.data.*` capabilities
2. **biomeOS**: Neural API semantic routing — `capability.call("visualization.data.timeseries")` routes to whichever spring has that data, without petalTongue knowing which spring it is

**Why this matters**: New springs are automatically visualized. If someone creates `oceanSpring` tomorrow and it announces `visualization.data.timeseries`, petalTongue discovers and renders it with zero code changes.

---

## Part 3: Novel Cross-Primal Combinations

These are capabilities that emerge when springs combine through petalTongue in ways not yet exercised.

### Comparative Dashboard: hotSpring + wetSpring + groundSpring

**Concept**: A unified uncertainty-aware scientific dashboard.

- **hotSpring** sends plasma simulation results as TimeSeries
- **wetSpring** sends LC-MS chromatograms as TimeSeries
- **groundSpring** annotates both with measurement uncertainty bounds
- **petalTongue** renders a side-by-side dashboard with uncertainty ribbons

**How**: Each spring sends `visualization.render` to the same petalTongue instance. Use `visualization.session.list` to discover co-located sessions. groundSpring uses `visualization.render.scene` to overlay uncertainty bands as semi-transparent Polygon primitives on existing sessions.

### AI-Guided Analysis: Squirrel + neuralSpring + petalTongue

**Concept**: An AI analyst that sees what the human sees and suggests where to look.

- **petalTongue** renders a complex multi-panel dashboard
- **Squirrel** subscribes to `interaction.subscribe` and receives every selection/hover event
- **neuralSpring** receives the interaction stream, runs anomaly detection
- **Squirrel** sends `visualization.interact.apply` to auto-focus petalTongue on the anomaly

**How**: The `SquirrelAdapter` is already wired into petalTongue's frame loop. neuralSpring provides the ML model; Squirrel translates model output to `ai.focus`, `ai.select`, `ai.highlight` interaction events.

### Provenance-Traced Clinical Report: healthSpring + Provenance Trio + petalTongue

**Concept**: A clinical visualization with full regulatory provenance.

- **healthSpring** sends patient PK/PD data
- **petalTongue** renders it as a dashboard with threshold coloring
- **rhizoCrypt** records the session as a DAG event
- **sweetGrass** attributes the data source and the rendering transformation
- **LoamSpine** commits the final SVG export as an immutable artifact
- **petalTongue** stamps the SVG with a provenance watermark via `visualization.export`

**How**: healthSpring pushes bindings. petalTongue renders + exports SVG. The provenance trio works in parallel through biomeOS `capability.call`. The final artifact carries: data hash, rendering grammar, timestamp, attribution braid, and LoamSpine commit ID.

### Game-Science Crossover: ludoSpring + hotSpring + petalTongue

**Concept**: Visualize physics simulations as interactive game scenes.

- **hotSpring** runs an N-body simulation
- **ludoSpring** wraps the simulation in game controls (player steering, zoom, time scale)
- **petalTongue** renders the simulation as a live Mesh/Point scene at 60 Hz
- **ludoSpring** streams player engagement metrics alongside the simulation

**How**: hotSpring sends particle positions as a Mesh primitive via `visualization.render.scene` each frame. ludoSpring sends `motor.set_zoom` and `motor.navigate` to control the camera. petalTongue renders both the physics scene and ludoSpring's engagement overlay as stacked panels.

### Field Intelligence: airSpring + groundSpring + Squirrel + petalTongue

**Concept**: AI-guided precision agriculture monitoring.

- **airSpring** streams IoT sensor data (soil moisture, weather, ET₀) as Gauges
- **groundSpring** adds uncertainty bounds to each sensor reading
- **petalTongue** renders a spatial FieldMap dashboard with live gauge overlays
- **Squirrel** watches the interaction stream and highlights anomalous zones

**How**: airSpring uses `visualization.render.dashboard` with one panel per field zone. groundSpring annotates gauges with uncertainty via streaming updates. Squirrel uses `ai.highlight` to flash irrigation zones that need attention. The farmer sees a live spatial map with AI-guided attention.

### Cross-Spring Anomaly Detection: All Springs + neuralSpring + petalTongue

**Concept**: A meta-dashboard that visualizes the entire ecosystem's health.

- Every spring sends its key metrics to petalTongue via `visualization.render`
- **neuralSpring** subscribes to all sessions via `visualization.session.list`
- **neuralSpring** runs cross-domain anomaly detection (e.g., soil moisture anomaly correlating with biosignal anomaly)
- **petalTongue** renders a unified ecosystem Heatmap where rows are springs and columns are time windows

**How**: Use `visualization.render.dashboard` with one row per spring. neuralSpring uses `visualization.render.scene` to overlay cross-correlation arrows between anomalous cells. Squirrel auto-focuses on the hottest anomaly.

### The Security Quartet: BearDog + skunkBat + biomeOS + petalTongue

**Concept**: A sovereign security operations center — fully local, no cloud.

- **skunkBat** detects threats across the ecosystem (metadata-only)
- **BearDog** provides cryptographic identity verification for each alert
- **biomeOS** orchestrates quarantine/heal/migrate responses
- **petalTongue** renders the security operations dashboard

**Flow**: `skunkBat.threat.detect` → `beardog.identity.verify` → `biomeOS.lifecycle.quarantine` → `petalTongue.visualization.render.stream`

**Why this matters**: The operator sees a living threat map where each alert is cryptographically attributed, defense posture adjusts in real time, and every quarantine action is visible. No cloud telemetry needed. The entire security operations center runs on one machine.

### The Memory Pipeline: rhizoCrypt + NestGate + LoamSpine + petalTongue

**Concept**: Tiered memory visualization — ephemeral → cached → permanent.

- **rhizoCrypt** holds working session state (what the user is currently looking at)
- **NestGate** caches exported artifacts (SVGs, scene snapshots, audio exports)
- **LoamSpine** commits finalized records to the immutable ledger
- **petalTongue** renders the memory pipeline itself as a 3-tier DAG

**Flow**: User interacts with dashboard → `rhizoCrypt.dag.append_event` → user exports → `nestgate.storage.put` → user finalizes → `loamspine.commit`

**Why this matters**: The user can see *where their work lives* — is it ephemeral (will vanish), cached (retrievable), or permanent (immutable)? petalTongue renders the memory tiers as nested containers. Dragging a session from the "ephemeral" zone to the "permanent" zone triggers the full provenance pipeline.

### The Full Ecosystem Dashboard: All 14 Primals + petalTongue

**Concept**: A single view of the entire sovereign computing stack.

- **biomeOS** provides NUCLEUS health for all primals
- **Songbird** provides discovery topology
- **BearDog** provides identity and trust state
- **skunkBat** provides threat level overlay
- **ToadStool** provides compute utilization
- **Every spring** sends its key metric

**petalTongue renders**: A multi-layer dashboard where:
- **Layer 1**: Topology (Songbird) — who's connected to whom
- **Layer 2**: Health (biomeOS) — node color = health status
- **Layer 3**: Security (skunkBat + BearDog) — threat overlays, trust badges
- **Layer 4**: Data flow (springs) — animated edges showing data volume

**How**: Each primal sends to its own `session_id`. petalTongue uses `visualization.render.dashboard` to compose all sessions into a unified grid. `visualization.session.list` reveals what's active. Squirrel watches the composite view and highlights cross-domain correlations.

### The Scaffolding Feedback Loop: sourDough + petalTongue + sweetGrass

**Concept**: When sourDough scaffolds a new primal, it gets visualization for free.

- **sourDough** generates a new primal from templates
- The template includes `visualization.render` capability registration
- The new primal's test suite includes golden-test DataBindings
- **petalTongue** renders the golden tests during scaffold validation
- **sweetGrass** attributes the scaffold lineage (which template, which version)

**Why this matters**: Every primal born from sourDough is **visualizable from birth**. No integration work needed. The scaffold template includes example DataBindings, and petalTongue renders them as part of the CI/CD validation step.

### The Accessible Science Station: healthSpring + airSpring + petalTongue (multi-modal)

**Concept**: The same data rendered for a sighted researcher AND a blind colleague simultaneously.

- **healthSpring** sends PK/PD curves
- **airSpring** sends ET₀ time series
- **petalTongue** renders both as:
  - Visual: line charts on the desktop display (egui)
  - Audio: sonified curves through speakers (pitch = value, stereo = variable)
  - Braille: tactile grid on a refreshable braille display
  - Terminal: ASCII sparklines for SSH-only access
  - Description: natural language summaries for screen readers

**How**: One `visualization.render` call, multiple `visualization.export` calls with different `modality` parameters. The UUI engine compiles the same Grammar of Graphics expression to each modality independently. Both researchers interact with the same data — one sees it, one hears it, both understand it.

---

## Part 4: What petalTongue Needs From You

### For Springs (data producers)

1. **Send data in any format** — `SpringDataAdapter` normalizes ludoSpring channels, ecoPrimals/time-series/v1, raw DataBindings, and bindings envelopes
2. **Include a `domain` hint** — health, physics, ecology, agriculture, measurement, neural, game — petalTongue selects the right palette, accessibility profile, and Tufte constraints
3. **Use `session_id`** — enables multi-spring dashboards, session management, and provenance tracking
4. **Subscribe to `interaction.subscribe`** — close the feedback loop; receive user clicks/hovers back for drill-down

### For Foundation Primals (infrastructure)

1. **Push telemetry** as DataBindings — petalTongue renders operational metrics in the ecosystem dashboard
2. **Use `visualization.render.scene`** for topology — Songbird's discovery graph, biomeOS's NUCLEUS mesh, rhizoCrypt's DAGs
3. **Use `visualization.render.stream`** for live state — skunkBat threats, BearDog key exchanges, ToadStool dispatches
4. **Subscribe to `interaction.subscribe`** — when the operator clicks a node, you receive the `node_id` and can trigger primal-specific actions (inspect, migrate, quarantine, heal)

---

## Part 5: petalTongue Alone — Self-Leverage

Even without any other primal or spring, petalTongue is a complete self-contained tool.

### Standalone Capabilities

| Mode | What You Get | No Dependencies |
|------|-------------|-----------------|
| `petaltongue ui` | Desktop visualization workbench with tutorial data, graph editor, panel system | Just a binary |
| `petaltongue tui` | Terminal dashboard for SSH-only servers | Pure Rust, no display server |
| `petaltongue web` | Browser-accessible visualization server | axum, no external services |
| `petaltongue headless` | Batch SVG/PNG/JSON export pipeline | Zero display deps |
| `petaltongue server` | Unix socket JSON-RPC visualization service | Accepts data from any process |
| `petaltongue status` | Self-diagnostic: config, socket paths, capabilities | Pure introspection |

### Self-Monitoring

petalTongue can visualize *itself*. The `DataService` graph engine tracks primal topology including petalTongue's own node. Use `visualization.introspect` to query what panels are open, what data is being displayed, and what sessions are active. This self-awareness enables:

- **Tutorial mode**: When no springs are discovered, petalTongue renders its own capabilities as a tutorial dashboard — the user learns the interface without needing any ecosystem
- **Awakening experience**: A 4-stage self-discovery animation (flower bloom → self-knowledge → ecosystem discovery → interactive tutorial) that runs on first startup
- **Session persistence**: Sessions survive restarts via local state persistence — no external primal needed

### As a Development Tool

Any developer building a new primal or spring can use petalTongue as a **development visualization server**:

```bash
petaltongue server &
echo '{"jsonrpc":"2.0","method":"visualization.render","params":{...},"id":1}' \
  | socat - UNIX-CONNECT:$XDG_RUNTIME_DIR/biomeos/petaltongue-nat0-default.sock
```

Your new primal pushes data via JSON-RPC; petalTongue renders it immediately. No registration, no discovery protocol, no biomeOS — just a socket.

### As a Testing Harness

petalTongue's `visualization.validate` method runs Tufte constraint checks on data before rendering: data-ink ratio, lie factor, chartjunk detection, accessibility compliance. Any spring can use this as a **visualization quality gate** in CI/CD — send proposed bindings, check the validation result, fail the build if constraints are violated.

---

## Part 6: Novel Self-Referential Patterns

These patterns use petalTongue's unique position as the only primal that produces human-perceivable output.

### The Introspection Loop

petalTongue can visualize data *about its own visualization*:

1. A spring sends data → petalTongue renders it
2. petalTongue emits telemetry about the render (frame time, modality selected, Tufte scores)
3. That telemetry feeds back as a TimeSeries to petalTongue's own dashboard
4. The operator sees both the data AND the quality of the rendering in real time

**Why this matters**: A researcher can watch their simulation AND simultaneously see whether the visualization is keeping up (frame drops, data-ink degradation, modality fallback). Meta-visualization.

### The Multi-Modal Bridge

petalTongue is the only primal that can translate between human sensory modalities. This makes it a **universal accessibility adapter**:

- A sighted operator's GUI interactions produce `interaction.subscribe` events
- Those events are re-rendered as audio descriptions for a blind colleague
- The blind colleague's voice commands (via Squirrel → AI → motor events) drive the GUI
- Both humans share the same session, perceiving it through different modalities

No other primal can do this because no other primal understands both sensory input and motor output across modalities.

### The Capability Explorer

petalTongue can discover and render the capabilities of any primal in the ecosystem:

1. Query Songbird for all registered primals
2. For each primal, call `capability.list` via JSON-RPC
3. Render the capability graph as an interactive SceneGraph
4. Clicking a capability node shows which springs use it and which methods expose it

This turns petalTongue into a **live ecosystem documentation tool** — the architecture diagram is always accurate because it's generated from actual runtime state.

---

## Part 7: Emergent Duo Patterns

These two-primal combinations create capabilities neither primal has alone.

### petalTongue + sourDough: Visualizable From Birth

Every primal scaffolded by sourDough gets a `visualization.render` capability template. But the deeper pattern: sourDough can call `visualization.validate` during scaffold testing to verify the new primal's example data produces valid, accessible visualizations before the primal is ever deployed. **Quality-gated scaffolding.**

### petalTongue + skunkBat: The Visible Defense Perimeter

skunkBat detects threats using metadata only. petalTongue renders the threat landscape. Together, they create a **sovereign security operations center** that runs entirely on local hardware. The operator sees live threat animations without any data leaving the machine. skunkBat sends streaming threat events; petalTongue renders them as pulsing topology overlays. Every quarantine decision is visible.

### petalTongue + groundSpring: Uncertainty-Aware Visualization

groundSpring knows the uncertainty of every measurement in the ecosystem. petalTongue renders data. Together: **every chart in the ecosystem can carry error bars derived from actual measurement science**, not guessed confidence intervals. groundSpring annotates petalTongue's data bindings with uncertainty envelopes via `visualization.render.scene` overlay. The Tufte constraint engine validates that uncertainty is always visible — no misleading precision.

### petalTongue + rhizoCrypt: Stateful Sessions

rhizoCrypt is ephemeral working memory. petalTongue produces visualization sessions. Together: **the visualization remembers**. Close your laptop, reopen it tomorrow — rhizoCrypt restores exactly which panels were open, what zoom level, what was selected, what filters were active. The session is a DAG of interaction events that can be replayed, branched, or shared.

### petalTongue + NestGate: Artifact Persistence

NestGate is content-addressed storage. petalTongue exports SVG/PNG/audio. Together: **every visualization ever rendered is addressable by hash**. Export a dashboard → `storage.put` → get back a BLAKE3 content address. Share that address with a colleague → they retrieve the exact same visualization. Immutable, deduplicatable, cacheable.

### petalTongue + biomeOS: The Nervous System's Eyes

biomeOS orchestrates the ecosystem. petalTongue shows humans what's happening. Together: **the operator can see AND act**. Click a struggling primal in the topology → biomeOS receives the click as `lifecycle.heal` intent → the primal is healed → the topology updates → the operator sees it recover. This closes the human-in-the-loop for ecosystem management. biomeOS is the nervous system; petalTongue is the sensory cortex AND the motor cortex.

### petalTongue + Squirrel: AI Co-Pilot for Any Data

Squirrel routes AI queries. petalTongue renders data. Together: **the AI can see what the human sees**. Squirrel subscribes to petalTongue's interaction stream, watches what the human is studying, and proactively highlights anomalies via `ai.highlight`. The human and the AI share visual attention. No separate chat window — the AI's thoughts appear as glow effects on the data itself.

### petalTongue + BearDog: Cryptographically Signed Visualizations

BearDog signs anything. petalTongue exports anything. Together: **a cryptographically signed SVG**. Export a clinical report → BearDog signs the SVG hash with the operator's Ed25519 key → the signed artifact is deposited in NestGate → anyone can verify the visualization hasn't been tampered with. Essential for legal, regulatory, and medical evidence.

---

## Part 8: Emergent Trio and Quartet Patterns

### The Provenance Pipeline: petalTongue + sweetGrass + LoamSpine

Every visualization has attribution AND permanence:
- petalTongue renders a spring's data
- sweetGrass records the full attribution chain (who provided the data, how it was transformed, who saw it)
- LoamSpine commits the rendered artifact as an immutable ledger entry

**The result**: An auditable, attributed, immutable visual record. "This PK/PD chart was rendered from healthSpring patient #42's data at 14:23 UTC, transformed by Grammar rule G7, viewed by Dr. Chen, and committed to ledger entry L-9281." Essential for FDA/EMA compliance.

### The Memory Stack: petalTongue + rhizoCrypt + NestGate + LoamSpine

Three tiers of memory for visualization:
1. **Working** (rhizoCrypt): Current session state — panels, zoom, selection. Ephemeral. Lost on reboot unless preserved.
2. **Cached** (NestGate): Exported artifacts — SVGs, audio exports, scene snapshots. Content-addressed. Survives restarts. Garbage-collected when no longer referenced.
3. **Permanent** (LoamSpine): Finalized records — signed, attributed, immutable. Survives forever.

petalTongue renders the memory tiers themselves as a 3-zone dashboard. Dragging a session from "working" to "permanent" triggers the full provenance pipeline.

### The Sovereign SOC: petalTongue + skunkBat + BearDog + biomeOS

A complete security operations center on a single machine:
- skunkBat detects → petalTongue renders threat map → operator clicks threat → BearDog verifies identity → biomeOS quarantines
- All local. No cloud. No telemetry. The entire defense posture is visible and actionable.

### The AI Research Station: petalTongue + neuralSpring + Squirrel + groundSpring

AI-guided, uncertainty-aware research:
- neuralSpring trains a model → streams loss curves to petalTongue
- groundSpring annotates curves with uncertainty bounds
- Squirrel watches the training dashboard → detects convergence stall → auto-adjusts learning rate
- petalTongue renders the whole process: loss + uncertainty + AI attention + hyperparameter history

The researcher sees training progress, knows the statistical confidence, and has an AI co-pilot watching for problems.

### The Digital Twin: petalTongue + airSpring + hotSpring + ToadStool

Real-time physical simulation with live visualization:
- hotSpring runs a thermodynamic simulation on ToadStool's GPU
- airSpring feeds real IoT sensor data as boundary conditions
- petalTongue renders the evolving simulation state as a live FieldMap
- The operator adjusts parameters via `motor.*` commands; the simulation responds

This is a **digital twin** — the physical system (a field, a reactor, a climate zone) is simulated live, visualized live, and controlled live, all on sovereign hardware.

### The Accessible Science Lab: petalTongue + Any Spring + Squirrel

Universal accessibility for any scientific domain:
- Any spring sends data
- petalTongue renders it across ALL modalities simultaneously
- A sighted researcher sees charts (egui)
- A blind colleague hears sonified data (audio modality)
- A motor-impaired colleague uses voice commands via Squirrel → `motor.*`
- A remote colleague gets terminal sparklines over SSH (TUI)
- An AI agent gets JSON API (headless)

The same Grammar of Graphics expression compiles to every modality. Accessibility is not a feature — it is the architecture. **Every spring gets universal accessibility for free through petalTongue.**

---

## Part 9: How Springs Should Use petalTongue

The fastest path from "I have data" to "a human can see it":

### Minimal Integration (5 minutes)

```bash
# 1. Start petalTongue
petaltongue server &

# 2. Send data (any format)
echo '{"jsonrpc":"2.0","method":"visualization.render","params":{
  "session_id":"my-spring",
  "title":"My Spring Data",
  "bindings":[{
    "channel_type":"timeseries",
    "id":"metric1",
    "label":"Temperature",
    "x_label":"Time (s)",
    "y_label":"°C",
    "unit":"celsius",
    "x_values":[0,1,2,3,4,5],
    "y_values":[20.1,20.3,20.7,21.2,21.8,22.5]
  }]
},"id":1}' | socat - UNIX-CONNECT:$XDG_RUNTIME_DIR/biomeos/petaltongue-nat0-default.sock
```

That's it. petalTongue auto-detects the data format, selects a domain palette, checks Tufte constraints, and renders to whatever modality is available.

### Full Integration Checklist

1. **Announce capabilities** via Songbird — petalTongue discovers you automatically
2. **Include `domain` hint** — selects the right color palette (health, physics, ecology, agriculture, measurement, neural, game)
3. **Use `session_id`** — enables multi-spring dashboards, session management, dismissal
4. **Subscribe to `interaction.subscribe`** — receive user clicks/hovers back for drill-down
5. **Stream updates** via `visualization.render.stream` — incremental append for real-time data
6. **Validate in CI** via `visualization.validate` — Tufte quality gate before deployment

### What You Do NOT Need

- You do NOT import petalTongue as a dependency
- You do NOT need to know petalTongue's internal types
- You do NOT need to handle rendering, layout, color, accessibility, or modality
- You do NOT need to know what display is connected
- Everything flows through capability-based JSON-RPC

---

*This guide is a living document. As springs discover new edges and capabilities, update this guide at the wateringHole so others can learn from the pattern.*

---

**License**: AGPL-3.0-or-later
