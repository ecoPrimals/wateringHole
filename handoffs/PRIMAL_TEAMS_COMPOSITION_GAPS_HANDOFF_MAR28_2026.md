# Primal Team Handoffs — Composition Gaps (March 28, 2026)

**From**: primalSpring coordination (Phase 23f)
**Reference**: `primalSpring/docs/PRIMAL_GAPS.md` for full gap registry

Each primal team has specific gaps exposed by the composition decomposition.
Fix the **High** items first — they block the interactive product.

---

## petalTongue Team

**Composition role**: C1 (Render) + C6 (Proprioception) — the visualization and interaction authority.
**Current status**: IPC server mode works, dashboard render + SVG export validated, interaction loop validated.

### Critical gaps to fix

1. **PT-02 (High)**: `web_mode.rs` has no WebSocket/SSE — cannot push live renders to browser.
   - Fix: Add WS endpoint to axum router, wire `DataService::subscribe` to push SVG/JSON on change.
   - Impact: Without this, browsers must poll. This is the #1 gap for a live interface.

2. **EW-01 dependency**: esotericWebb's `push_scene_to_ui` sends flat JSON that doesn't match `SceneGraph`.
   - petalTongue expects `SceneGraph { nodes: HashMap<NodeId, SceneNode>, root_id }` where each `SceneNode` has `id`, `transform: Transform2D { a, b, tx, c, d, ty }`, `primitives`, `children`, `visible`, `opacity`.
   - Coordinate with esotericWebb team on the format.

### Medium gaps

3. **PT-01**: `EguiCompiler` outputs `ModalityOutput::Description` (JSON string), not `EguiShapes`.
   - For full Rust egui as primary interface, add `EguiShapes` variant.
4. **PT-03**: `motor_tx` not wired in server/web mode — `motor.*` methods error.
5. **PT-05**: `visualization.showing` returns `showing: false` when `rendering_awareness` is None.
   - Fix: Initialize to default on server startup.
6. **PT-06**: `callback_method` in subscriptions stored but never invoked (poll-only).

### Validated capabilities (working today)
- `visualization.render.dashboard` with DataBinding `gauge` channel_type
- `visualization.export` (SVG, 5619 bytes)
- `visualization.render.scene` with full `SceneGraph` struct
- `visualization.session.list` (session awareness)
- `interaction.subscribe` / `interaction.poll` / `visualization.interact.apply`
- `visualization.showing` (returns, but `showing: false` without awareness wiring)

### Test your composition
```bash
# C1 standalone
biomeos deploy --graph graphs/compositions/render_standalone.toml
# C6 standalone
biomeos deploy --graph graphs/compositions/proprioception_loop.toml
# Validate
python3 tools/validate_compositions.py  # checks C1 + C6
```

---

## Squirrel Team

**Composition role**: C2 (Narration) — AI query routing, context management.
**Current status**: Not running in live stack. Gap SQ-01 is the primary blocker.

### Critical gap to fix

1. **SQ-01 (High)**: `AiRouter` discovery has 3 paths (HTTP providers + API keys, `AI_PROVIDER_SOCKETS` UDS, biomeOS scan for ToadStool). None natively support Ollama HTTP.
   - Fix option A: Add a "local" provider to `http_provider_config.rs` that wraps the OpenAI-compatible endpoint at `LOCAL_AI_ENDPOINT`.
   - Fix option B: Wire `AI_PROVIDER_SOCKETS` to a tiny Ollama-to-UDS bridge.
   - Impact: Blocks all local AI narration. The gateway currently bypasses Squirrel and calls Ollama directly.

2. **SQ-02 (Medium)**: `LOCAL_AI_ENDPOINT` env var feeds into `AIProviderConfig` but NOT into `AiRouter` discovery.
   - Wire env into provider initialization in `AiRouter::new()`.

### What we need from Squirrel
- `ai.query` that routes to Ollama's `/api/chat` (OpenAI-compatible)
- `ai.list_providers` showing at least one local provider
- `context.create` / `context.summarize` for session context management

### Test your composition
```bash
biomeos deploy --graph graphs/compositions/narration_ai.toml
```

---

## esotericWebb Team

**Composition role**: C3 (Session) — narrative session lifecycle, the "product".
**Current status**: Fully validated (8/8 PASS). Session lifecycle works end-to-end.

### Gaps to fix

1. **EW-01 (High)**: `push_scene_to_ui` sends flat JSON `{node, description, npcs, turn}` to petalTongue's `visualization.render.scene`, which expects a `SceneGraph` struct.
   - Fix: Construct `DataBinding::GameScene` or a proper `SceneGraph` with tagged `channel_type`.
   - Coordinate with petalTongue team on format.

2. **EW-02 (Medium)**: `poll_input` exists on bridge but is NOT wired into the game loop.
   - Add `interaction.poll` call in session tick/act cycle.

3. **EW-04 (Low)**: V6 internal game science duplicates ludoSpring capabilities.
   - Define composition contract: when ludoSpring is present, esotericWebb defers to external `game.evaluate_flow`.

### What's working perfectly
- `session.start`, `session.state`, `session.actions`, `session.act`, `session.graph` — all validated
- `webb.liveness`, `webb.scene.current`, `webb.content.list`
- Actions return `{id, kind, label}` — clean format for UI consumption

### Focus: ludoSpring handles game science, esotericWebb handles narrative
ludoSpring will focus on game and function (flow, engagement, WFC). esotericWebb
focuses on narrative product evolution. The composition layer handles the routing.

---

## NestGate Team

**Composition role**: C5 (Persistence) — storage for sessions, game state, provenance.
**Current status**: Process not running in live stack. Socket exists but stale.

### Gaps to fix

1. **NG-01 (Medium)**: Isomorphic IPC uses in-memory `HashMap`, not `nestgate-core` storage.
   - Wire `nestgate-core` storage backend (RocksDB/sled) into IPC adapter's `storage.*` handlers.
   - Impact: Data lost on restart. C5 validation passes for in-session round-trip but fails for persistence.

2. **NG-02 (Low)**: No dedicated game session API — requires generic `storage.store` with session-keyed blobs.

### What we need from NestGate
- `storage.store` / `storage.retrieve` with real disk persistence
- `health.liveness` responding

---

## ludoSpring Team

**Composition role**: C4 (Game Science) — flow, engagement, WFC, accessibility.
**Current status**: Fully validated (6/6 PASS). All game science methods respond correctly.

### Focus: game and function
ludoSpring should focus on game science quality and function. primalSpring handles
composition and deployment. The validated API surface:
- `game.evaluate_flow` — params: `{skill, challenge, time_pressure}`, returns `{state: "flow"}`
- `game.fitts_cost` — params: `{distance, target_width}`, returns `{index_of_difficulty, movement_time_ms}`
- `game.wfc_step` — params: `{n_tiles, width, height}`, returns collapse state
- `game.engagement` — params: `{skill, challenge, session_duration_s, action_count, exploration_breadth, challenge_seeking, retry_count, deliberate_pauses}`

### Gap to address
- **LS-01 (Medium)**: Gateway hardcodes flow params. Define mapping from esotericWebb session state to ludoSpring inputs (trust → skill, scene difficulty → challenge).

---

## biomeOS Team

**All gaps fixed or worked around.** primalSpring handles:
- BM-02: `health.liveness` not on Neural API → fallback to `graph.list`
- BM-03: `unix://` prefix in `primary_endpoint` → `strip_unix_uri()`

**Reference for other teams**: biomeOS `capability.discover` is the recommended
discovery path. primalSpring's thin gateway uses it exclusively.
