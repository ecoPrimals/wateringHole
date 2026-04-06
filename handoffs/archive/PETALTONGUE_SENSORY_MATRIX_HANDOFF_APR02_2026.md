# petalTongue Sensory Capability Matrix Handoff

**Date**: April 2, 2026
**Phase**: Sensory capability matrix, accessibility adapters, sensor contracts
**Previous**: `PETALTONGUE_DEEP_DEBT_EVOLUTION_PHASE3_HANDOFF_APR02_2026.md`

---

## Summary

Implemented the Sensory Capability Matrix — a formal input×output capability
negotiation system that enables consumer primals (ludoSpring, Squirrel,
primalSpring, Toadstool) to discover what interaction paths are available for
any given user session. This is the architectural foundation for true Universal
User Interface accessibility: a blind paraplegic and a deaf mute can
collaborate as a dev team, and agentic AI (Squirrel) interacts through the
same semantic pipeline as human users.

---

## Changes

### Sensory Capability Matrix (Core Types)

New module `petal_tongue_core::sensory_matrix`:

- **`InputCapabilitySet`**: 13 boolean capability flags (keyboard, mouse,
  touch, voice, gesture, gaze, switch, braille_input, haptic_input, bci,
  sip_puff, api_agent, custom)
- **`OutputCapabilitySet`**: 11 boolean capability flags (visual_display,
  audio, braille_output, haptic_output, force_feedback, description_text,
  svg_print, gpu_3d, terminal, api_machine, custom)
- **`ValidatedPath`**: A tested input→output interaction path with
  `InteractionPattern` and bidirectional flag
- **`InteractionPattern`**: 9 variants (PointAndClick, KeyboardNavigation,
  VoiceAndAudio, SwitchScanning, GazeDwell, TouchGesture, AgentApi,
  BrailleRouting, HapticExploration)
- **`SensoryCapabilityMatrix`**: Top-level type combining input/output sets,
  validated paths, and recommended output modality

Builder methods:
- `from_sensory_capabilities()` — runtime hardware discovery
- `for_agent()` — AI-only sessions
- `recommend_modality_public()` — const fn modality selection

### IPC Methods

Two new JSON-RPC 2.0 methods:

| Method | Purpose |
|--------|---------|
| `capabilities.sensory` | Returns full matrix from runtime discovery. `"agent": true` for AI sessions. |
| `capabilities.sensory.negotiate` | Accepts explicit `input`/`output` capability overrides (e.g. NestGate preferences) and returns tailored matrix. |

Both added to `capability_names::self_capabilities::ALL` (40 total) and routed
in the IPC dispatch table.

### Accessibility Adapters

Three new `InputAdapter` / `InversePipeline` implementations:

| Adapter | User Type | Mechanism |
|---------|-----------|-----------|
| `SwitchInputAdapter` | Motor-impaired | Single-switch auto-advance or two-switch scan+select |
| `AudioInversePipeline` | Blind | Maps audio cursor position → `DataObjectId` for sonified data |
| `AgentInputAdapter` | AI (Squirrel) | Parses JSON commands from `SensorEvent::Generic` → `InteractionIntent` |

### Sensor Extensions

Extended `SensorEvent` with 6 new variants for Toadstool hardware integration:
- `VoiceCommand { text, confidence, timestamp }`
- `Gesture { gesture_type, direction, magnitude, timestamp }`
- `Touch { x, y, pressure, finger_id, timestamp }`
- `GazePosition { x, y, confidence, timestamp }`
- `SwitchActivation { switch_id, pressed, timestamp }`
- `AgentCommand { payload, timestamp }`

New supporting types: `GestureType` (8 variants), `GestureDirection` (8 variants)
New `SensorType` variants: `Touch`, `EyeTracker`, `Switch`, `Agent`
New `InputModality::Agent` variant

### Ecosystem Documentation

| Document | Location |
|----------|----------|
| `SENSORY_CAPABILITY_MATRIX.md` | `wateringHole/petaltongue/` — full matrix specification for consumer primals |
| `TOADSTOOL_SENSOR_CONTRACT.md` | `wateringHole/` — SensorEvent IPC protocol for hardware primals |
| `VISUALIZATION_INTEGRATION_GUIDE.md` | Updated with sensory negotiation section |

### Validation Tests

12 integration tests in `crates/petal-tongue-core/tests/sensory_matrix_validation.rs`:
- Blind keyboard user path
- Deaf haptic user path
- Motor-impaired switch user path
- Screen reader user path
- Agentic AI (Squirrel) path
- Audio inverse pipeline resolution
- Toadstool sensor event processing
- BCI binary intent pathway
- Multi-user shared perspective
- Runtime discovery mapping
- JSON serialization roundtrip

---

## Quality Gates (all passing)

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --all-features -D warnings` | Zero warnings |
| `cargo doc --no-deps --all-features` | Clean |
| `cargo test --workspace --all-features` | 5,952 passing (1 pre-existing CLI exclusion) |

---

## Consumer Primal Integration Guide

### ludoSpring / esotericWebb
Call `capabilities.sensory` at session start. If `output.audio` is true but
`output.visual_display` is false, route GameScene through `sonify_game_scene()`
and `hapticize_game_scene()` instead of visual rendering. The matrix tells you
what paths exist without guessing.

### Squirrel (Agentic AI)
Call `capabilities.sensory` with `"agent": true`. Returns a matrix with
`api_agent` input and `api_machine` output. Use `AgentInputAdapter` to send
JSON commands through the same `InteractionIntent` pipeline as human input.

### primalSpring (Orchestration)
Call `capabilities.sensory.negotiate` with explicit capability sets from
NestGate user preferences. Returns validated paths and recommended modality
for per-user session configuration.

### Toadstool (Hardware)
Emit `SensorEvent` variants per `TOADSTOOL_SENSOR_CONTRACT.md`. petalTongue
routes through the appropriate `InputAdapter` based on `SensorType`.

---

## Remaining Evolution (Low Priority)

| Item | Notes |
|------|-------|
| Coverage to 90%+ | 30 lines from threshold; gap in main() orchestration |
| `Cow<'a, str>` on wire types | Marginal benefit for current usage |
| doom-core missing_docs | 65 WAD types need documentation |
| Remove `mock_mode` serde alias | After one release cycle |
| Deprecated HTTP/legacy audio providers | Remove in next major version |
| Toadstool hardware testing | Sensor adapters ready; need real hardware validation |
| NestGate preference integration | `negotiate` method ready; NestGate needs to expose preference API |

---

## Files Changed

### New
- `crates/petal-tongue-core/src/sensory_matrix.rs`
- `crates/petal-tongue-core/tests/sensory_matrix_validation.rs`
- `crates/petal-tongue-ui/src/interaction_adapters/switch_adapter.rs`
- `crates/petal-tongue-ui/src/interaction_adapters/audio_inverse.rs`
- `crates/petal-tongue-ui/src/interaction_adapters/agent_adapter.rs`
- `wateringHole/petaltongue/SENSORY_CAPABILITY_MATRIX.md`
- `wateringHole/TOADSTOOL_SENSOR_CONTRACT.md`

### Modified
- `crates/petal-tongue-core/src/lib.rs` (sensory_matrix module + re-exports)
- `crates/petal-tongue-core/src/capability_names.rs` (2 new capabilities)
- `crates/petal-tongue-core/src/interaction/adapter.rs` (InputModality::Agent)
- `crates/petal-tongue-core/src/sensor/types.rs` (6 SensorEvent + 4 SensorType variants)
- `crates/petal-tongue-core/src/sensor/mod.rs` (re-exports)
- `crates/petal-tongue-ipc/src/unix_socket_rpc_handlers/system.rs` (2 handlers)
- `crates/petal-tongue-ipc/src/unix_socket_rpc_handlers/mod.rs` (dispatch)
- `crates/petal-tongue-ui/src/interaction_adapters/mod.rs` (3 new modules)
- `wateringHole/petaltongue/VISUALIZATION_INTEGRATION_GUIDE.md`
- `CHANGELOG.md`
