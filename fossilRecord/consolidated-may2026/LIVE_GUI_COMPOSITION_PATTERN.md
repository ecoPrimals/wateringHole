# Live GUI Composition Pattern

> How any spring validates, and any garden produces, an interactive native-GUI
> product from the same NUCLEUS primals.

**Date:** April 2026 | **Status:** v1.0 (first production pattern) | **Origin:** primalSpring Phase 45 + ludoSpring V46 + esotericWebb

---

## Architectural Principle

Springs prove science. Gardens produce products. **Both compose the same primals.**

```
  NUCLEUS (primals)          Spring (validates)          Garden (produces)
  ┌──────────────┐          ┌──────────────────┐        ┌──────────────────┐
  │ beardog      │          │ Validates:       │        │ Produces:        │
  │ songbird     │◄─────────│  Domain science  │        │  Interactive UI  │
  │ barraCuda    │          │  IPC contracts   │        │  Native GUI      │
  │ petalTongue  │◄─────────│  Data flow       │───────►│  User interaction│
  │ toadStool    │          │  HCI parity      │        │  Session state   │
  │ ...          │          └──────────────────┘        └──────────────────┘
  └──────────────┘           guidestone certifies        biomeOS deploys graph
```

The key evolution: **petalTongue `live` mode** runs both the IPC server and
the native egui window in the same process, sharing `VisualizationState` via
`Arc<RwLock<>>`. Any primal that pushes `visualization.render` over UDS sees
its data rendered in the native window in real time.

---

## The Interaction Loop

```
game state ──► scene payload ──► visualization.render.scene ──► egui window
    ▲                                                               │
    │           interaction.poll ◄── user input (key/mouse/sensor) ◄┘
    └───────────────────────────────────────────────────────────────┘
```

1. **Session logic** (in the garden or spring) produces game/domain state
2. `game.push_scene` packages state into a scene payload
3. The scene is forwarded to petalTongue via `visualization.render.scene` (IPC)
4. petalTongue's egui window renders the scene (via shared `VisualizationState`)
5. User input is captured by petalTongue and made available via `interaction.poll`
6. Session logic polls for input and updates game state — loop repeats

---

## petalTongue `live` Mode

### What It Is

A new CLI subcommand (`petaltongue live`) that combines the two existing modes:

- `petaltongue ui` — egui/eframe native window, no IPC server
- `petaltongue server` — UDS JSON-RPC server, no window

`petaltongue live` = IPC server (background tokio task) + egui window (main
thread), connected via `Arc<RwLock<VisualizationState>>`.

### How to Launch

```bash
# From plasmidBin binary
petaltongue live

# With explicit socket path
petaltongue live --socket /run/user/1000/biomeos/petaltongue-myfamily.sock

# With optional TCP JSON-RPC
petaltongue live --port 9090
```

### IPC Methods Available in Live Mode

| Method | Description |
|--------|-------------|
| `visualization.render` | Push data for rendering (charts, tables, metrics) |
| `visualization.render.scene` | Push a structured scene (game/domain) |
| `visualization.render.stream` | Stream real-time updates (append, set_value) |
| `visualization.render.dashboard` | Composite dashboard layout |
| `visualization.session.list` | List active visualization sessions |
| `visualization.session.status` | Status of a specific session |
| `visualization.export` | Export current view |
| `interaction.subscribe` | Subscribe to user input events |
| `interaction.poll` | Poll for pending user input |
| `motor.*` | Motor/haptic commands |

---

## For Springs: Validating a Live GUI Composition

Springs **validate** that the composition pipeline works. They do not produce
products. The experiment goes in `experiments/` and proves the data flow.

### Pattern

```rust
// 1. Deploy NUCLEUS with petalTongue in live mode
// 2. Begin a domain session
let result = call_primal(game_ep, "game.begin_session", &params)?;

// 3. Generate domain data
for action in actions {
    call_primal(game_ep, "game.record_action", &action)?;
}

// 4. Push scene — this should arrive in petalTongue's native window
let push = call_primal(game_ep, "game.push_scene", &scene_payload)?;
assert!(push["accepted"].as_bool().unwrap_or(false));

// 5. Verify round-trip via visualization.session.list
let sessions = call_primal(viz_ep, "visualization.session.list", &json!({}))?;
assert!(sessions["sessions"].as_array().map_or(false, |s| !s.is_empty()));

// 6. Assert domain invariants hold through the pipeline
let metrics = session.engagement_metrics();
assert!(metrics.composite > 0.0, "flow state preserved through round-trip");
```

### Example: ludoSpring exp078 (Live GUI Composition)

- LOCAL: game session produces well-formed scene payloads (3 checks)
- IPC: `game.push_scene` forwards to petalTongue (3 checks)
- ROUNDTRIP: visualization session appears in petalTongue (1 check)
- PARITY: HCI invariants hold through the pipeline (3 checks)

Any spring can follow this pattern. Replace `game.*` with your domain IPC
methods and `game science` with your domain science.

---

## For Gardens: Producing an Interactive Product

Gardens **consume** the validated composition and produce a usable system. The
deploy graph and launch script live in the garden repo.

### Deploy Graph (`graphs/webb_live_interactive.toml`)

Key difference from headless graphs: petalTongue node uses `mode = "live"`
instead of `mode = "server"`.

```toml
[[nodes]]
id = "germinate_petaltongue_live"
depends_on = ["germinate_songbird"]
capabilities = ["visualization", "ui", "interaction"]

[nodes.primal]
by_capability = "visualization"

[nodes.operation]
name = "start"
[nodes.operation.params]
mode = "live"                    # <-- the key change
domain = "game"
family_id = "${FAMILY_ID}"
```

### Launch Script

```bash
# Set up family identity and secrets
export FAMILY_ID="my-garden-interactive"
export BEARDOG_FAMILY_SEED="$(head -c 32 /dev/urandom | xxd -p)"

# Start NUCLEUS
./nucleus_launcher.sh --composition full start

# Launch petalTongue in live mode (this opens the native window)
petaltongue live --socket "$XDG_RUNTIME_DIR/biomeos/petaltongue-${FAMILY_ID}.sock"
```

### Interaction Flow in a Garden

```
Garden session logic ───► game.push_scene ───► petalTongue live window
       ▲                                              │
       │◄──── interaction.poll ◄──── user clicks/keys ┘
```

The garden's session logic runs as a separate process or within biomeOS. It
pushes scene updates and polls for user input, creating a real-time interactive
loop with native GPU rendering.

---

## Generalizing to Other Domains

| Spring | Domain IPC | Garden Product |
|--------|-----------|----------------|
| ludoSpring | `game.*` | esotericWebb: playable CRPG |
| hotSpring | `simulation.*` | MILC dashboard: live lattice QCD results |
| healthSpring | `health.*` | Patient monitor: real-time vitals |
| neuralSpring | `neural.*` | Model explorer: interactive training viz |
| airSpring | `atmosphere.*` | Climate dashboard: live sensor streams |
| wetSpring | `water.*` | Watershed monitor: flow simulation |

Every domain follows the same pattern:

1. **Spring** validates that domain data flows through NUCLEUS to petalTongue
2. **Garden** deploy graph sets petalTongue to `live` mode
3. **Session logic** pushes domain data via `visualization.render.scene`
4. **User interaction** flows back via `interaction.poll`

---

## What This Unlocks

- **Native GPU-accelerated UI** instead of HTML — egui with full eframe rendering
- **User interaction** via `interaction.subscribe/poll` — keyboard, mouse, sensor
- **Real-time streaming** via `visualization.render.stream` — 60fps updates
- **Sensory feedback** — `audio.synthesize`, motor commands already in petalTongue
- **Every spring** can use the same pattern to get a live native dashboard
- **Every garden** produces a real interactive product, not just validated math

---

## Cellular Deployment

As of Phase 46, every spring and garden has a **cell graph** — a ready-to-deploy
biomeOS graph that includes the full NUCLEUS + petalTongue live + domain overlay.

```bash
# Deploy any spring as a live interactive cell
./tools/cell_launcher.sh ludospring start
./tools/cell_launcher.sh hotspring start
./tools/cell_launcher.sh list

# Or via biomeOS directly
biomeos deploy --graph graphs/cells/ludospring_cell.toml
```

Cell graphs live in `springs/primalSpring/graphs/cells/`. guidestone Layer 7
certifies every cell. exp098 validates all 8 cells structurally and via biomeOS
dry-run when available. See `PRIMALSPRING_COMPOSITION_GUIDANCE.md` section 18
for the full cellular deployment model.

---

## Key References

| Document | Location |
|----------|----------|
| petalTongue `live_mode.rs` | `primals/petalTongue/src/live_mode.rs` |
| ludoSpring exp078 | `springs/ludoSpring/experiments/exp078_live_gui_composition/` |
| Cell graphs (all springs) | `springs/primalSpring/graphs/cells/` |
| Cell launcher | `springs/primalSpring/tools/cell_launcher.sh` |
| Cell validation (exp098) | `springs/primalSpring/experiments/exp098_cellular_deployment/` |
| esotericWebb interactive graph | `gardens/esotericWebb/graphs/webb_live_interactive.toml` |
| esotericWebb launch script | `gardens/esotericWebb/deploy/launch_interactive.sh` |
| PetalTonguePushClient | `springs/ludoSpring/barracuda/src/visualization/push_client.rs` |
| VisualizationState | `primals/petalTongue/crates/petal-tongue-ipc/src/visualization_handler/state/` |
| Composition guidance | `springs/primalSpring/wateringHole/PRIMALSPRING_COMPOSITION_GUIDANCE.md` |
| NUCLEUS alignment | `infra/wateringHole/NUCLEUS_SPRING_ALIGNMENT.md` |
