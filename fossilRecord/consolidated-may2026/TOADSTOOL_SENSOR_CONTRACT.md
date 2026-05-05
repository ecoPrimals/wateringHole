# Toadstool Sensor Contract — SensorEvent IPC Protocol

**Version**: 1.0.0  
**Date**: April 2, 2026  
**Audience**: Toadstool hardware integration team  
**Status**: Active Standard

---

## Purpose

This document specifies what `SensorEvent` variants Toadstool should emit via
IPC when it detects hardware sensors. petalTongue consumes these events through
its `InputAdapter` pipeline to produce modality-agnostic `InteractionIntent`
values.

Toadstool owns the hardware — petalTongue owns the translation.

## Transport

Toadstool sends sensor events to petalTongue via JSON-RPC over Unix socket:

```json
{
  "jsonrpc": "2.0",
  "method": "interaction.sensor_stream.push",
  "params": {
    "events": [
      { "type": "voice_command", "transcript": "select node five", "confidence": 0.92, "timestamp_ms": 1712070000000 }
    ]
  }
}
```

Until push delivery is wired (PT-06), petalTongue polls via
`interaction.sensor_stream.poll`.

## SensorEvent Variants

### Voice Input (Microphone + Speech Recognizer)

**SensorType**: `Audio`  
**SensorEvent variant**: `VoiceCommand`

```json
{
  "type": "voice_command",
  "transcript": "navigate to dashboard",
  "confidence": 0.87,
  "timestamp_ms": 1712070000000
}
```

**Toadstool responsibilities:**
- Detect microphone via ALSA/PulseAudio/CoreAudio
- Run speech recognition (whisper, OS accessibility, or delegate to Squirrel)
- Emit `VoiceCommand` with transcript and confidence

**petalTongue processing:**
- (Future) `VoiceInputAdapter` maps transcript to `InteractionIntent`
- Currently handled via `AgentInputAdapter` if Squirrel intermediates

### Gesture Input (Camera / Depth Sensor / VR Tracking)

**SensorType**: `Camera` or `Motion`  
**SensorEvent variant**: `Gesture`

```json
{
  "type": "gesture",
  "gesture_type": "Swipe",
  "direction": "Left",
  "magnitude": 0.75,
  "timestamp_ms": 1712070000000
}
```

**Gesture types (GestureType enum):**

| Type | Description |
|------|-------------|
| `Swipe(direction)` | Directional swipe (Up, Down, Left, Right) |
| `PinchIn` | Pinch to zoom in |
| `PinchOut` | Spread to zoom out |
| `Rotate` | Rotation gesture |
| `Wave` | Attention-getting wave |
| `Point` | Point at target |
| `Grab` | Grip / grab gesture |
| `Release` | Open hand / release |
| `Custom(name)` | Custom named gesture |

**Toadstool responsibilities:**
- Detect cameras, depth sensors (Kinect, RealSense), VR controllers
- Run gesture classification (MediaPipe, custom, or delegate)
- Emit `Gesture` with classified type and magnitude

### Touch Input (Touchscreen / Pressure Surface)

**SensorType**: `Touch`  
**SensorEvent variant**: `Touch`

```json
{
  "type": "touch",
  "x": 540.0,
  "y": 960.0,
  "pressure": 0.5,
  "timestamp_ms": 1712070000000
}
```

**Toadstool responsibilities:**
- Detect touchscreen via input subsystem (`/dev/input/event*`)
- Report position in display-space pixels
- Report pressure (0.0 = hover, 1.0 = full press)

### Eye/Gaze Tracking

**SensorType**: `EyeTracker`  
**SensorEvent variant**: `GazePosition`

```json
{
  "type": "gaze_position",
  "x": 960.0,
  "y": 540.0,
  "fixation_ms": 350,
  "timestamp_ms": 1712070000000
}
```

**Toadstool responsibilities:**
- Detect eye tracking hardware (Tobii, VR headset eye tracking)
- Calibrate gaze to display coordinates
- Report fixation duration for dwell-to-select

**petalTongue processing:**
- `fixation_ms >= 500` triggers dwell-select (configurable via NestGate)
- Continuous gaze stream used for focus highlighting

### Switch / Binary Input (Sip-and-Puff, Head Switch, BCI Binary)

**SensorType**: `Switch`  
**SensorEvent variant**: `SwitchActivation`

```json
{
  "type": "switch_activation",
  "switch_id": 0,
  "timestamp_ms": 1712070000000
}
```

**Toadstool responsibilities:**
- Detect switch hardware (USB HID, Bluetooth, custom GPIO)
- Map hardware input to switch ID (0-indexed)
- Emit on activation (not hold — hold-to-repeat is petalTongue's concern)

**petalTongue processing:**
- `SwitchInputAdapter` with `SingleSwitch` or `TwoSwitch` mode
- Two-switch: ID 0 = advance, ID 1 = select
- Single-switch: alternating advance/select with timing

### Agent / Machine Input (Squirrel, API Clients)

**SensorType**: `Agent`  
**SensorEvent variant**: `AgentCommand`

```json
{
  "type": "agent_command",
  "intent": "select",
  "parameters": { "target": "node-42" },
  "timestamp_ms": 1712070000000
}
```

This is typically sent by Squirrel directly via IPC, not through Toadstool
hardware discovery. Included here for completeness of the contract.

**petalTongue processing:**
- `AgentInputAdapter` parses intent and parameters
- Produces same `InteractionIntent` as human input

## Sensor Discovery Protocol

When Toadstool starts, it should announce discovered sensors to petalTongue:

```json
{
  "jsonrpc": "2.0",
  "method": "provider.register_capability",
  "params": {
    "capability": "sensor.eye_tracker",
    "provider_name": "toadstool",
    "socket_path": "/run/biomeos/toadstool.sock",
    "version": "0.4.0",
    "methods": ["sensor.stream.subscribe", "sensor.stream.poll"]
  }
}
```

petalTongue uses this to update the `SensoryCapabilityMatrix` at runtime,
enabling dynamic capability negotiation as hardware is connected/disconnected.

## Capability Strings for Sensor Types

| Sensor | Capability String |
|--------|------------------|
| Microphone | `sensor.audio_input` |
| Camera | `sensor.camera` |
| Depth sensor | `sensor.depth` |
| Touchscreen | `sensor.touch` |
| Eye tracker | `sensor.eye_tracker` |
| Switch device | `sensor.switch` |
| Motion sensor | `sensor.motion` |
| Game controller | `sensor.gamepad` |

## Timeline

| Phase | Owner | Deliverable |
|-------|-------|-------------|
| 1 (Current) | petalTongue | `SensorEvent` variants defined, `capabilities.sensory` IPC live |
| 2 | Toadstool | Hardware discovery emits `provider.register_capability` |
| 3 | Toadstool | Sensor event streaming via `sensor.stream.push` |
| 4 | petalTongue | Remaining `InputAdapter` implementations for each sensor type |
| 5 | Ecosystem | End-to-end validation per `SENSORY_CAPABILITY_MATRIX.md` |
