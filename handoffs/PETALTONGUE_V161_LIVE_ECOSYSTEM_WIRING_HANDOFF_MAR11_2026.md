<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# petalTongue V1.6.1 — Live Ecosystem Wiring Handoff — March 11, 2026

**From:** petalTongue V1.6.1 (3,245 tests, 0 failures)
**To:** biomeOS, ludoSpring, toadStool, barraCuda, Squirrel
**License:** AGPL-3.0-only
**Supersedes:** PETALTONGUE_V160_SPRING_SCHEMA_EVOLUTION_HANDOFF_MAR10_2026

---

## Executive Summary

- **Full bidirectional pipeline** between petalTongue UI and ecoPrimals ecosystem
- Sensor events (pointer, key, scroll, click) **broadcast to IPC subscribers** every frame
- UI selection changes **broadcast as interaction events** to subscribers
- petalTongue **self-registers with Neural API** (`lifecycle.register` + 30s heartbeat)
- All 7 **ludoSpring GameDataChannel** types mapped to `DataBinding` variants
- **28 new tests** (3,245 total), clippy clean, fmt clean, zero unsafe
- `docs/LIVE_TESTING.md` for testing with real biomeOS/NUCLEUS/ludoSpring

## What petalTongue Now Provides

### For biomeOS / Neural API

- **Self-registration**: On startup, petalTongue discovers the Neural API socket
  and calls `lifecycle.register` with 4 capabilities:
  - `ui.render` — desktop GUI rendering
  - `visualization.render` — data visualization
  - `ipc.json-rpc` — JSON-RPC 2.0 server
  - `interaction.sensor_stream` — raw UI event streaming
- **Heartbeat**: 30s `lifecycle.status` heartbeat thread
- **Graceful degradation**: If biomeOS is not running, registration fails silently

### For ludoSpring

- **Sensor stream**: ludoSpring can subscribe to `interaction.sensor_stream.subscribe`
  and receive pointer/key/scroll events for Fitts cost, Hick's law, and engagement analysis
- **GameDataChannel rendering**: 7 channel types auto-map to visualization:

| ludoSpring Channel | DataBinding | Notes |
|--------------------|-------------|-------|
| EngagementCurve | TimeSeries | x=time, y=engagement |
| DifficultyProfile | TimeSeries | x=progress, y=difficulty |
| FlowTimeline | Bar | categories=flow states |
| InteractionCostMap | Heatmap | x=region, y=action, z=Fitts |
| GenerationPreview | Scatter | Procedural content |
| AccessibilityReport | FieldMap | WCAG metrics |
| UiAnalysis | FieldMap | Tufte metrics |

- **Game domain theming**: Sessions with `domain: "game"` use the `(220, 160, 80)` palette

### For Squirrel / AI Adaptation

- **Interaction events**: Subscribe to `interaction.subscribe` to receive
  `select`/`deselect` events when the user clicks graph nodes
- **Sensor stream**: Subscribe to raw pointer/key events for behavior analysis

### For toadStool / barraCuda

- No breaking changes. Existing IPC contracts unchanged.
- New `SensorStreamRegistry` re-export from `petal_tongue_ipc` root.

## Validation Scorecard

| Check | Result |
|-------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace -- -W clippy::pedantic` | Clean (0 new warnings) |
| `cargo test --workspace` | 3,245 passed, 0 failures |
| `cargo doc --workspace --no-deps` | Clean |
| `#![forbid(unsafe_code)]` | All crate roots |
| Largest file | 968 lines (all under 1,000) |

## New Files

| File | Lines | Purpose |
|------|-------|---------|
| `crates/petal-tongue-ui/src/sensor_feed.rs` | 97 | egui input → SensorEventIpc conversion |
| `crates/petal-tongue-ui/src/neural_registration.rs` | 98 | Neural API lifecycle.register + heartbeat |
| `crates/petal-tongue-ui/src/game_data_channel.rs` | 213 | ludoSpring channel → DataBinding mapping |
| `crates/petal-tongue-ui/tests/live_primal_integration_tests.rs` | 187 | Full pipeline integration tests |
| `docs/LIVE_TESTING.md` | 113 | Live multi-primal testing guide |

## Modified Files

| File | Change |
|------|--------|
| `crates/petal-tongue-ui/src/app/mod.rs` | +sensor_stream, +interaction_subscribers fields, broadcast in update loop |
| `crates/petal-tongue-ui/src/app/init.rs` | Initialize new fields |
| `crates/petal-tongue-ui/src/main.rs` | IPC handle extraction, Neural API registration call |
| `crates/petal-tongue-ui/src/lib.rs` | Module declarations |
| `crates/petal-tongue-ipc/src/unix_socket_server.rs` | +interaction_subscribers_handle() |
| `crates/petal-tongue-ipc/src/lib.rs` | +SensorStreamRegistry re-export |

## IPC Method Summary (All Available)

```
interaction.sensor_stream.subscribe    → {subscription_id}
interaction.sensor_stream.poll         → SensorEventBatch
interaction.sensor_stream.unsubscribe  → {removed}
interaction.subscribe                  → {subscriber_id}
interaction.poll                       → [InteractionEventNotification]
interaction.unsubscribe                → {removed}
visualization.render                   → session created
visualization.render.stream            → binding updated
visualization.render.dashboard         → multi-panel SVG
```

## Testing with Live Primals

See `docs/LIVE_TESTING.md` for full instructions. Quick verification:

```bash
# Start biomeOS Tower
cd ../biomeOS && cargo run -- nucleus serve --mode tower

# Start petalTongue (auto-registers)
cd petalTongue && cargo run

# Verify registration
echo '{"jsonrpc":"2.0","method":"lifecycle.status","id":1}' | \
  socat - UNIX-CONNECT:$XDG_RUNTIME_DIR/biomeos-neural-api-nat0.sock
```

---

*This handoff is unidirectional: petalTongue → ecosystem. No response expected.*
