# Interaction Event Taxonomy

**Version:** 1.0.0
**Date:** April 27, 2026
**Audience:** petalTongue, toadStool, ludoSpring, gardens, and any composition handling user/sensor input
**Status:** Active Standard
**License:** AGPL-3.0-or-later

---

## Purpose

Multiple primals and springs produce and consume interaction events:

- **toadStool** discovers hardware sensors and emits `SensorEvent` variants
- **petalTongue** translates sensor events into modality-agnostic `InteractionIntent`
- **ludoSpring** consumes interaction events for game session lifecycle
- **Squirrel** produces agent commands that mimic human input
- **Gardens** wire user interaction through the composition

Each evolved its own event types independently. This standard defines the
unified taxonomy so interaction events compose across domains. It builds on
`TOADSTOOL_SENSOR_CONTRACT.md` (hardware layer) and extends it to cover
UI interaction, game input, and agent commands.

---

## Event Layers

```
Layer 3: Intent         "select node-42"          (petalTongue → consumers)
         ↑ translation
Layer 2: Interaction    click(540, 960)           (petalTongue internal)
         ↑ adaptation
Layer 1: Sensor         touch(540, 960, 0.8)      (toadStool → petalTongue)
         ↑ detection
Layer 0: Hardware       /dev/input/event3          (toadStool internal)
```

| Layer | Owner | Format | Transport |
|-------|-------|--------|-----------|
| 0: Hardware | toadStool | OS-specific | Internal |
| 1: Sensor | toadStool → petalTongue | `SensorEvent` JSON-RPC | `interaction.sensor_stream.push` |
| 2: Interaction | petalTongue | `InteractionEvent` | Internal |
| 3: Intent | petalTongue → consumers | `InteractionIntent` JSON-RPC | `interaction.poll` / `interaction.subscribe` |

Springs and gardens consume **Layer 3 (Intent)** only. They never see raw
sensor data or interaction events. petalTongue owns the translation.

---

## Layer 1: Sensor Events (toadStool → petalTongue)

Defined in `TOADSTOOL_SENSOR_CONTRACT.md`. Summary:

| Sensor Type | Event Variant | Capability String |
|-------------|--------------|-------------------|
| Microphone | `voice_command` | `sensor.audio_input` |
| Camera/Depth | `gesture` | `sensor.camera` / `sensor.depth` |
| Touchscreen | `touch` | `sensor.touch` |
| Eye tracker | `gaze_position` | `sensor.eye_tracker` |
| Switch device | `switch_activation` | `sensor.switch` |
| Game controller | `gamepad` | `sensor.gamepad` |
| Motion sensor | `motion` | `sensor.motion` |
| Agent/AI | `agent_command` | `sensor.agent` |

---

## Layer 3: Interaction Intents (petalTongue → consumers)

This is the taxonomy that springs and gardens consume. All intents are
modality-agnostic — the same intent can originate from mouse, touch, voice,
gaze, gamepad, switch, or agent.

### Navigation Intents

| Intent | Description | Typical Sources |
|--------|-------------|----------------|
| `navigate.up` | Move focus/selection up | Arrow key, D-pad, swipe up, gaze drift up, voice "up" |
| `navigate.down` | Move focus/selection down | Arrow key, D-pad, swipe down, gaze drift down, voice "down" |
| `navigate.left` | Move focus/selection left | Arrow key, D-pad, swipe left, voice "left" |
| `navigate.right` | Move focus/selection right | Arrow key, D-pad, swipe right, voice "right" |
| `navigate.next` | Move to next element | Tab, switch advance, voice "next" |
| `navigate.previous` | Move to previous element | Shift+Tab, voice "previous" |
| `navigate.back` | Return to previous context | Escape, back button, voice "back", gesture swipe-right |

### Selection Intents

| Intent | Description | Typical Sources |
|--------|-------------|----------------|
| `select.activate` | Activate focused element | Enter, click, tap, switch select, gaze dwell, voice "select" |
| `select.toggle` | Toggle focused element | Space, checkbox tap, voice "toggle" |
| `select.context` | Open context menu | Right-click, long-press, voice "options" |
| `select.cancel` | Cancel current operation | Escape, voice "cancel" |

### Manipulation Intents

| Intent | Description | Typical Sources |
|--------|-------------|----------------|
| `manipulate.drag_start` | Begin drag operation | Mouse down + move, touch hold + move |
| `manipulate.drag_move` | Continue drag | Mouse move while down, touch move |
| `manipulate.drag_end` | End drag operation | Mouse up, touch release |
| `manipulate.zoom_in` | Zoom in | Scroll up, pinch out, voice "zoom in", Ctrl++ |
| `manipulate.zoom_out` | Zoom out | Scroll down, pinch in, voice "zoom out", Ctrl+- |
| `manipulate.rotate` | Rotate element | Two-finger rotate, gesture rotate |
| `manipulate.scroll` | Scroll content | Scroll wheel, two-finger swipe, voice "scroll down" |

### Game Intents (ludoSpring domain)

| Intent | Description | Typical Sources |
|--------|-------------|----------------|
| `game.action_primary` | Primary game action | Left click, A button, tap, voice "attack" |
| `game.action_secondary` | Secondary game action | Right click, B button, voice "defend" |
| `game.menu` | Open game menu | Escape, Start button, voice "menu" |
| `game.pause` | Pause/unpause | P key, Start button, voice "pause" |
| `game.inventory` | Open inventory | I key, Select button, voice "inventory" |
| `game.interact` | Interact with world object | E key, X button, voice "interact" |

### System Intents

| Intent | Description | Typical Sources |
|--------|-------------|----------------|
| `system.help` | Request help/accessibility info | F1, voice "help" |
| `system.search` | Open search | Ctrl+F, voice "search" |
| `system.command` | Open command palette | Ctrl+Shift+P, voice "command" |
| `system.fullscreen` | Toggle fullscreen | F11, double-tap |

---

## Intent Wire Format

All intents travel as JSON-RPC over the `interaction.poll` method:

```json
{
  "jsonrpc": "2.0",
  "method": "interaction.poll",
  "params": {
    "since_tick": 1041
  },
  "id": 42
}
```

Response:

```json
{
  "jsonrpc": "2.0",
  "result": {
    "intents": [
      {
        "intent": "select.activate",
        "target": "node-42",
        "timestamp_ms": 1714254000123,
        "source_modality": "touch",
        "confidence": 1.0,
        "metadata": {}
      },
      {
        "intent": "navigate.down",
        "target": null,
        "timestamp_ms": 1714254000456,
        "source_modality": "gamepad",
        "confidence": 1.0,
        "metadata": { "axis_value": 0.85 }
      }
    ],
    "tick": 1042
  },
  "id": 42
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `intent` | String | Yes | Intent name from taxonomy above |
| `target` | String? | No | Element ID if applicable |
| `timestamp_ms` | u64 | Yes | Unix epoch milliseconds |
| `source_modality` | String | No | Origin modality for analytics/accessibility |
| `confidence` | f64 | No | 0.0–1.0; meaningful for voice/gesture (default 1.0) |
| `metadata` | Object | No | Modality-specific data (axis values, transcript, etc.) |

---

## Subscription Model

For continuous compositions (60Hz games), polling every frame adds latency.
petalTongue supports event subscription:

```json
{
  "jsonrpc": "2.0",
  "method": "interaction.subscribe",
  "params": {
    "intent_filter": ["game.*", "navigate.*", "select.*"],
    "delivery": "push"
  },
  "id": 1
}
```

Push delivery uses NDJSON streaming — petalTongue writes events as they
arrive, the consumer reads them as a stream. See `DEPLOYMENT_AND_COMPOSITION.md`
§Pipeline for the streaming transport.

---

## Modality Mapping

How petalTongue maps sensor events to intents (configurable per composition):

| Sensor | Mapping Rules |
|--------|--------------|
| **Keyboard** | Direct keycode → intent mapping (configurable keybinds) |
| **Mouse** | Click → `select.activate`; right-click → `select.context`; scroll → `manipulate.scroll`; drag → `manipulate.drag_*` |
| **Touch** | Tap → `select.activate`; long-press → `select.context`; swipe → `navigate.*`; pinch → `manipulate.zoom_*` |
| **Gamepad** | D-pad/stick → `navigate.*`; A → `game.action_primary`; B → `game.action_secondary`; Start → `game.menu` |
| **Voice** | NLU intent classification → closest intent (confidence-gated) |
| **Gaze** | Fixation (≥500ms) → `select.activate`; drift → `navigate.*` |
| **Switch** | Single-switch: alternating `navigate.next` / `select.activate`; two-switch: advance/select |
| **Agent** | Direct intent passthrough from Squirrel `agent_command` |

---

## Composing Events Across Domains

When a cell graph has both a game UI (ludoSpring) and a science dashboard
(hotSpring), petalTongue routes intents by **focus context**:

```
User focus: "game" panel
  → keyboard/gamepad events route to game.* intents
  → click on dashboard panel switches focus

User focus: "dashboard" panel
  → keyboard events route to navigate.* / select.* intents
  → click on game panel switches focus
```

Focus context is managed by petalTongue's scene graph. The consumer
(spring or garden) declares which intent namespaces it handles:

```toml
[[graph.node]]
name = "game_logic"
intent_namespaces = ["game", "navigate", "select"]

[[graph.node]]
name = "science_dashboard"
intent_namespaces = ["navigate", "select", "manipulate", "system"]
```

---

## Accessibility First

The intent taxonomy is designed accessibility-first:

1. **Every intent has multiple input paths** — no capability requires a
   specific modality. `select.activate` works from keyboard, mouse, touch,
   voice, gaze, switch, or agent.

2. **Voice and switch are first-class** — not afterthoughts. The taxonomy
   was designed with sip-and-puff and eye-tracking users in mind.

3. **Confidence-gated inputs** — voice and gesture inputs carry confidence
   scores. Consumers can set thresholds: `min_confidence = 0.8` rejects
   ambiguous voice commands rather than misinterpreting them.

4. **Source modality is informational** — consumers SHOULD NOT branch on
   modality. The intent is the same regardless of how the user produced it.
   Modality is tracked for analytics, not logic.

---

## Related Documents

- `TOADSTOOL_SENSOR_CONTRACT.md` — Layer 1: hardware sensor events
- `COMPOSITION_TICK_MODEL_STANDARD.md` — Temporal models for continuous compositions
- `DEPLOYMENT_AND_COMPOSITION.md` §Continuous — 60Hz tick loop
- `GARDEN_COMPOSITION_ONRAMP.md` — Garden product integration
- `petaltongue/README.md` — petalTongue integration hub

---

**Input is not one thing. Keyboards, voices, eyes, switches, agents — all produce the same intents. The taxonomy makes interaction composable.**
