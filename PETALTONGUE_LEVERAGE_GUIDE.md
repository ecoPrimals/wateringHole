# petalTongue Spring Leverage Guide

**Version**: 1.0.0  
**Date**: March 14, 2026  
**Audience**: Springs, primals, and ecosystem architects  
**Purpose**: How to leverage petalTongue — alone, in trios, and in novel cross-primal combinations

---

## What petalTongue Offers

petalTongue is the **representation primal**. It accepts data through IPC and renders it across every available modality — egui GUI, ratatui TUI, audio sonification, SVG export, terminal character grids, braille tactile grids, haptic command sequences, and GPU command buffers. It also provides interactive features: selection, zoom, pan, perspectives, AI-driven focus (via Squirrel), and provenance tracking that traces every rendered pixel back to its source data.

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

## Part 1: Using petalTongue Alone

Each spring can leverage petalTongue independently. No other primal needed — just a Unix socket and JSON-RPC.

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

---

## Part 4: What petalTongue Needs From You

For petalTongue to visualize your spring's data effectively:

1. **Announce capabilities** via Songbird or `provider.register_capability` — petalTongue discovers you automatically
2. **Send data in any format** — `SpringDataAdapter` normalizes ludoSpring channels, ecoPrimals/time-series/v1, raw DataBindings, and bindings envelopes
3. **Include a `domain` hint** — petalTongue selects the right color palette (health, physics, ecology, agriculture, measurement, neural, game)
4. **Use `session_id`** — enables session management, dismissal, and multi-spring dashboards
5. **Subscribe to interactions** — close the loop by receiving user clicks/hovers back

You do NOT need to know about petalTongue's internals. You do NOT need to import petalTongue as a dependency. Everything flows through capability-based IPC.

---

## IPC Quick Reference

```bash
# Render TimeSeries data
echo '{"jsonrpc":"2.0","method":"visualization.render","params":{"session_id":"my-session","title":"My Data","bindings":[{"channel_type":"timeseries","id":"ts1","label":"Metric","x_label":"Time","y_label":"Value","unit":"units","x_values":[1,2,3],"y_values":[10,20,30]}]},"id":1}' | socat - UNIX-CONNECT:/tmp/petaltongue.sock

# Send a raw SceneGraph
echo '{"jsonrpc":"2.0","method":"visualization.render.scene","params":{"session_id":"custom","scene":{"nodes":{"root":{"id":"root","transform":{"a":1,"b":0,"tx":0,"c":0,"d":1,"ty":0},"primitives":[],"children":[],"visible":true,"opacity":1.0}},"root_id":"root"}},"id":2}' | socat - UNIX-CONNECT:/tmp/petaltongue.sock

# List active sessions
echo '{"jsonrpc":"2.0","method":"visualization.session.list","params":{},"id":3}' | socat - UNIX-CONNECT:/tmp/petaltongue.sock

# Export as SVG
echo '{"jsonrpc":"2.0","method":"visualization.export","params":{"session_id":"my-session","modality":"svg"},"id":4}' | socat - UNIX-CONNECT:/tmp/petaltongue.sock
```

---

*This guide is a living document. As springs discover new edges and capabilities, update this guide at the wateringHole so others can learn from the pattern.*
