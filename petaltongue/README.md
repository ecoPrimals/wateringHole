# petalTongue @ wateringHole

Cross-primal integration documentation for petalTongue — the **Universal User Interface** primal.

**Updated**: April 26, 2026 (PG-40 winit fix, live mode, texture/overlay roadmap, graphics node handoff)

---

## Integration Status

petalTongue v1.6.6 (16 crates, edition 2024, `deny(unwrap/expect)`):
- 5,952+ tests passing, 0 failures (1 pre-existing CLI test excluded)
- `#![forbid(unsafe_code)]` unconditional on all 16 crates + UniBin, zero C dependencies
- ~90% line coverage (llvm-cov) — threshold enforced via `llvm-cov.toml`
- UUI glossary module (`petal_tongue_core::uui_glossary`) — canonical terminology for modalities, user types, SAME DAVE
- tarpc binary RPC (primary primal-to-primal, zero-copy `bytes::Bytes`)
- JSON-RPC 2.0 over Unix sockets (secondary, local IPC and debugging)
- HTTP fallback for browser/external clients
- Capability-based discovery -- zero hardcoded primal names, 62+ capability constants, 15 primal identity constants
- **Enriched `capability.list`**: returns `primal`, `version`, `transport[]`, `methods[]`, `depends_on[]`, `data_bindings`, `geometry_types`
- **Sensory Capability Matrix**: `capabilities.sensory` and `capabilities.sensory.negotiate` IPC methods for input×output negotiation
- **Accessibility adapters**: SwitchInputAdapter, AudioInversePipeline, AgentInputAdapter for motor-impaired, blind, and AI users
- Grammar of Graphics engine with Tufte constraint validation
- **DataBinding auto-compiler**: All 11 DataBinding variants (TimeSeries, Distribution, Bar, Gauge, Spectrum, Heatmap, Scatter, Scatter3D, FieldMap, GameScene, Soundscape) auto-compile to Grammar of Graphics
- **Dashboard layout engine**: Multi-panel grid with domain theming and SVG/description export
- **Scenario loader**: Load healthSpring-style JSON scenarios from disk with `--scenario` CLI flag
- **Faceting**: `compile_faceted()` for small multiples (Wrap/Grid layouts)
- **Threshold coloring**: `compile_with_thresholds()` for normal/warning/critical cell colors in heatmaps
- **Tile/Arc geometry**: Real heatmap/fieldmap tile rendering, semicircular gauge arcs
- Domain-aware rendering (7 palettes: health, physics, ecology, agriculture, measurement, neural, game)
- Spring IPC: healthSpring DataChannel auto-compile, dashboard render, wetSpring Scatter/Spectrum, physics bridge, interaction method aliases
- Multi-modal rendering: egui GUI, ratatui TUI, audio sonification, haptic, braille, description, SVG, headless
- Scene graph with Manim-style animation, modality compilers (SVG, audio, description, terminal)
- **Spring absorption**: backpressure, JSONL telemetry, diverging palette, pipeline DAG, provider registry, `temp_env` safe testing, `TryFrom` safe casts, `tempfile` socket isolation
- **Live ecosystem wiring**: sensor feed, interaction broadcast, Neural API registration, GameDataChannel mapping
- **Smart refactoring**: doom-core (910→47 lines lib.rs via module decomposition), petal-tongue-tui/app (887→module tree)
- **Game visualization**: Sprite/Tilemap/GameEntity primitives, GameScene DataBinding for ludoSpring
- **Soundscape synthesis**: 5 waveforms, stereo panning, fade envelopes, Soundscape DataBinding
- **JSONL telemetry provider**: File-based hotSpring/groundSpring bridge via `PETALTONGUE_TELEMETRY_DIR`
- All files under 1,000 lines; all production stubs evolved to implementations

### Grammar of Graphics Engine (Implemented)

petalTongue has evolved from fixed widgets to a **Grammar of Graphics** engine.
Any primal can send a grammar expression via JSON-RPC, and petalTongue compiles it
to the best available output. This replaces per-domain ad-hoc rendering with
a single composable pipeline.

**If your primal has data that humans need to understand, read
[VISUALIZATION_INTEGRATION_GUIDE.md](./VISUALIZATION_INTEGRATION_GUIDE.md).**

Implemented capabilities:
- Declarative grammar expressions (data -> variables -> scales -> geometry -> coordinates)
- Tufte constraint system (data-ink ratio, lie factor, chartjunk, accessibility checks)
- barraCuda GPU compute offload via physics bridge (N-body, molecular dynamics)
- Domain color palettes resolved at runtime from grammar `domain` field
- Streaming visualization for real-time data (`visualization.render.stream`)
- 10 geometry types: Point, Line, Bar, Area, Ribbon, Tile, Arc, Heatmap, Contour, Text
- DataBinding payloads: TimeSeries, Distribution, Bar, Gauge, Heatmap, Scatter, Scatter3D, FieldMap, Spectrum, GameScene, Soundscape
- AnimationPlayer for sequenced scene graph animations
- Scene bridge renderers for both egui (GUI) and ratatui (TUI)

---

## For Other Primals

### Visualizing Your Data

The simplest way to get petalTongue to visualize your primal's data:

1. Announce your data capabilities via Songbird discovery
2. Expose `{domain}.get` and `{domain}.schema` JSON-RPC methods
3. Send a `visualization.render` request with a grammar expression (or just raw data)

petalTongue handles modality selection, accessibility, Tufte compliance, and
barraCuda compute offload automatically.

See **[VISUALIZATION_INTEGRATION_GUIDE.md](./VISUALIZATION_INTEGRATION_GUIDE.md)** for
the full grammar reference, domain examples, and sovereignty checklist.

### biomeOS Integration

petalTongue discovers biomeOS via:
1. `BIOMEOS_NEURAL_API_SOCKET` env var (explicit override)
2. `$XDG_RUNTIME_DIR/biomeos/neural-api.sock` (XDG standard)
3. `/tmp/biomeos-neural-api.sock` (legacy fallback)

All communication uses JSON-RPC 2.0 over Unix sockets.

### healthSpring Integration

petalTongue renders healthSpring diagnostic data via `DataChannel` and `DataBinding`:
- `TimeSeries` -> Line charts (PK curves, RR tachograms)
- `Distribution` -> Histograms with mean/SD/patient markers
- `Bar` -> Categorical bar charts (microbiome abundances)
- `Gauge` -> Progress bars with normal/warning ranges
- `Heatmap` -> Endocrine correlation matrices
- `Spectrum` -> Frequency-domain analysis (Pan-Tompkins, biosignal)

These map to grammar geometries: `TimeSeries` -> `GeomLine` + `TemporalScale`,
`Distribution` -> `GeomBar` + `StatBin`, `Bar` -> `GeomBar` + `CategoricalScale`,
`Gauge` -> `GeomArc` (polar) or `GeomRect` with annotation,
`Spectrum` -> `GeomArea` + `FrequencyScale`.

Interaction model: callback-based subscriptions (`interaction.subscribe` with
`callback_method` and `event_filter`), plus poll-based fallback.

### ToadStool Integration

petalTongue discovers ToadStool display backend via capability-based discovery.
tarpc binary RPC for high-performance frame transport.

### barraCuda Integration (v0.3.3+ alignment)

petalTongue offloads heavy visualization computation to barraCuda via capability
discovery (`gpu.dispatch`, `science.gpu.dispatch`).
All payloads use `bytes::Bytes` for zero-copy tarpc transfer. Physics bridge
(`petal-tongue-ipc/src/physics_bridge.rs`) provides async IPC client aligned
with barraCuda's `barracuda.compute.dispatch` contract (using `op` field).

**Current status**: CPU Euler fallback only. barraCuda's `compute.dispatch`
currently supports `zeros`, `ones`, `read` ops. `math.physics.nbody` is wired
in petalTongue but not yet in barraCuda's dispatch table. Physics bridge will
use GPU automatically when barraCuda adds physics ops.

**Discovery**: Follows toadStool S139 dual-write pattern:
1. `BARRACUDA_SOCKET` env (explicit)
2. `$XDG_RUNTIME_DIR/ecoPrimals/discovery/` (ecosystem manifest)
3. `$XDG_RUNTIME_DIR/barracuda/` (primal-specific)
4. `/tmp/barracuda.sock` (fallback)

**Precision**: petalTongue is a visualization consumer, not a compute provider.
Precision routing (`Fp64Strategy`, `PrecisionRoutingAdvice`, `FmaPolicy`)
lives in barraCuda/coralReef. petalTongue accepts and displays data at
whatever precision the ecosystem provides.

### coralReef Integration (Phase 10, Iteration 52)

petalTongue does NOT call coralReef directly. Shader compilation flows:
`barraCuda (WGSL) → coralReef (compile) → toadStool (dispatch)`.
petalTongue receives computed results via IPC.

If petalTongue ever needs GPU rendering (GpuCompiler modality), it would go
through barraCuda's `ComputeDispatch::CoralReef` or wgpu, not coralReef directly.

---

## IPC Protocol

petalTongue follows `UNIVERSAL_IPC_STANDARD_V3.md`:
- **Primary**: JSON-RPC 2.0 over Unix sockets
- **Secondary**: tarpc (binary, zero-copy `bytes::Bytes`)
- **Fallback**: HTTP REST (browser/external only)

Socket path: `$XDG_RUNTIME_DIR/petaltongue/petaltongue.sock`
Legacy: `/tmp/petaltongue.sock`

### Visualization JSON-RPC Methods

| Method | Direction | Purpose |
|--------|-----------|---------|
| `visualization.render` | Inbound | Render a grammar expression or raw data |
| `visualization.render.stream` | Inbound | Streaming visualization (append/set_value/replace) |
| `visualization.render.grammar` | Inbound | Render grammar with DataBinding payload |
| `visualization.render.dashboard` | Inbound | Multi-panel dashboard from DataBindings → SVG |
| `visualization.export` | Inbound | Export scene to SVG/JSON/description |
| `visualization.validate` | Inbound | Pre-render Tufte constraint check |
| `visualization.dismiss` | Inbound | Remove a visualization session |
| `visualization.capabilities` | Inbound | Query supported features and geometry types |
| `interaction.subscribe` | Inbound | Subscribe to interaction events (callback or poll) |
| `interaction.poll` | Inbound | Poll pending interaction events |
| `interaction.unsubscribe` | Inbound | Remove interaction subscription |
| `visualization.interact.subscribe` | Inbound | Alias for `interaction.subscribe` (wetSpring compat) |
| `visualization.interact.poll` | Inbound | Alias for `interaction.poll` (wetSpring compat) |
| `visualization.interact.unsubscribe` | Inbound | Alias for `interaction.unsubscribe` (wetSpring compat) |
| `visualization.interact.apply` | Inbound | Programmatic interaction (zoom, filter, select) |
| `visualization.interact.perspectives` | Inbound | List active perspective views |
| `capabilities.sensory` | Inbound | Query sensory capability matrix (runtime discovery or agent) |
| `capabilities.sensory.negotiate` | Inbound | Negotiate tailored matrix with explicit input/output caps |
| `audio.synthesize` | Inbound | On-demand soundscape synthesis (returns WAV metadata) |
| `visualization.render.scene` | Inbound | Direct SceneGraph submission |
| `motor.*` | Outbound | Motor commands to springs |
| `visualization.interact` | Outbound | User interaction event notifications |

---

## Documents

| Document | Purpose |
|----------|---------|
| [PETALTONGUE_NEEDS_FROM_ECOSYSTEM.md](./PETALTONGUE_NEEDS_FROM_ECOSYSTEM.md) | **What petalTongue needs from other primals** (3D pipeline, audio, GPU ops) |
| [VISUALIZATION_INTEGRATION_GUIDE.md](./VISUALIZATION_INTEGRATION_GUIDE.md) | **How to get petalTongue to visualize your data** (v2.1.0) |
| [SENSORY_CAPABILITY_MATRIX.md](./SENSORY_CAPABILITY_MATRIX.md) | **Input×output capability negotiation protocol** for consumer primals |
| [SCENE_FORMAT_REFERENCE.md](./SCENE_FORMAT_REFERENCE.md) | **GameScene, Soundscape, narrative JSON schemas** for ludoSpring, esotericWebb |
| [BIOMEOS_INTEGRATION_HANDOFF.md](./BIOMEOS_INTEGRATION_HANDOFF.md) | biomeOS integration guide (fossil record, v1.3.0 baseline) |
| [BIOMEOS_API_SPECIFICATION.md](./BIOMEOS_API_SPECIFICATION.md) | API contract and endpoints |
| [QUICK_START_FOR_BIOMEOS.md](./QUICK_START_FOR_BIOMEOS.md) | 5-minute quick start |
| [NEURAL_API_INTEGRATION_RESPONSE.md](./NEURAL_API_INTEGRATION_RESPONSE.md) | Neural API response format |
| [PETALTONGUE_SHOWCASE_LESSONS_LEARNED.md](./PETALTONGUE_SHOWCASE_LESSONS_LEARNED.md) | Production insights (fossil record, Jan 3 baseline) |

---

## Standards Compliance

| Standard | Status |
|----------|--------|
| `UNIBIN_ARCHITECTURE_STANDARD.md` | Compliant (1 binary, 6 modes) |
| `ECOBIN_ARCHITECTURE_STANDARD.md` | Compliant (pure Rust, no C deps, no genomeBin yet) |
| `UNIVERSAL_IPC_STANDARD_V3.md` | Compliant (JSON-RPC + tarpc + HTTP fallback) |
| `SEMANTIC_METHOD_NAMING_STANDARD.md` | Compliant (`visualization.*`, `interaction.*` namespaces) |
| `PRIMAL_IPC_PROTOCOL.md` | Compliant |
| `UNIVERSAL_USER_INTERFACE_SPEC` | Compliant — UUI glossary, multi-modal, SAME DAVE |
| License | AGPL-3.0-or-later on all crates |
