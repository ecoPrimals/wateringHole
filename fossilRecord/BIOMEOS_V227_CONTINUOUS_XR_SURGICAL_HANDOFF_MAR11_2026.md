# biomeOS v2.27 — Continuous Systems + XR/Surgical VR Evolution

**Date**: March 11, 2026  
**Primal**: biomeOS  
**Version**: 2.27  
**Status**: COMPLETE  
**Tests**: 3,670+ passing (0 failures)

---

## Summary

biomeOS gains three major capabilities: continuous graph execution (live 60Hz tick loops), immersive XR type foundations (stereo rendering, motion capture, haptic feedback), and a surgical simulation domain model. These form the evolutionary path from ludoSpring game interaction to real-time surgical VR training.

---

## What Was Built

### 1. Continuous Execution (biomeos-graph)

| Component | File | Purpose |
|-----------|------|---------|
| `ContinuousExecutor` | `crates/biomeos-graph/src/continuous.rs` | Fixed-timestep graph loop with session lifecycle |
| `TickClock` | same | Frame-skip protection, budget accumulator |
| `SessionState` | same | Starting/Running/Paused/Stopping/Stopped lifecycle |
| `SensorEventBus` | `crates/biomeos-graph/src/sensor.rs` | `tokio::broadcast` for keyboard/mouse/gamepad/tracking events |
| `SensorCollector` | same | Collects multi-source sensor input into single stream |
| `GraphEventBroadcaster` | `crates/biomeos-graph/src/events.rs` | Push-based event distribution (replaced 5s poll SSE) |
| `CoordinationPattern::Continuous` | `crates/biomeos-graph/src/graph.rs` | Graph-level coordination mode |
| `TickConfig` | same | Target Hz, max accumulator, budget warning thresholds |
| `game_engine_tick.toml` | `graphs/game_engine_tick.toml` | 60Hz continuous graph: input → logic → physics → scene → render |

### 2. XR Type System (biomeos-types)

| Type | File | Purpose |
|------|------|---------|
| `VisualOutputCapability` | `crates/biomeos-types/src/xr.rs` | TwoD / ThreeD(StereoConfig) / Passthrough |
| `StereoConfig` | same | Per-eye resolution, refresh Hz, IPD, FOV |
| `Pose6DoF` | same | Position + orientation + velocity |
| `TrackingFrame` | same | Multi-device tracking snapshot with confidence |
| `MotionCaptureConfig` | same | Backend, Hz, devices, prediction horizon |
| `HapticCommand` | same | Force/vibration/electrotactile commands |
| `HapticDeviceCapabilities` | same | Device limits for safety clamping |
| `TissueMaterial` | same | Young's modulus, Poisson's ratio, tear threshold |
| `AnatomyModel` / `AnatomyLayer` | same | Layered anatomy for rendering + physics |
| `SurgicalInstrument` | same | Scalpel, forceps, endoscope, cautery, etc. |

### 3. XR Rendering Adapters (biomeos-ui)

| Adapter | File | Purpose |
|---------|------|---------|
| `StereoRenderAdapter` | `crates/biomeos-ui/src/capabilities/xr_rendering.rs` | Negotiate/begin/submit/end stereo sessions with petalTongue |
| `MotionCaptureAdapter` | `crates/biomeos-ui/src/capabilities/motion_capture.rs` | OpenXR/SteamVR, 1000Hz, surgical preset |
| `HapticPipeline` | `crates/biomeos-ui/src/capabilities/haptic_feedback.rs` | Device discovery, safety-clamped dispatch, emergency stop |

### 4. Surgical Domain (biomeos-types)

| Type | File | Purpose |
|------|------|---------|
| `SurgicalProcedure` | `crates/biomeos-types/src/surgical.rs` | Procedure definition (instruments, anatomy, difficulty) |
| `ToolTissueInteraction` | same | Penetration depth, reaction force, damage classification |
| `DamageType` | same | Incision, tear, cauterization, compression, puncture |
| `BiosignalType` / `BiosignalStreamConfig` | same | ECG, PPG, EDA, EMG streaming config |
| `PkModelParams` / `PkModelResult` | same | 1/2/3-compartment pharmacokinetics |
| `SurgicalSessionState` | same | Setup/Active/Paused/Completed/EmergencyStopped |
| `SurgicalSessionMetrics` | same | Path length, economy of motion, accuracy, scoring |

### 5. Capability Infrastructure

| Change | Location |
|--------|----------|
| 8 new CapabilityTaxonomy variants | `crates/biomeos-types/src/capability_taxonomy.rs` |
| 8 new Capability enum variants | `crates/biomeos-types/src/capabilities.rs` |
| XR domain (14 JSON-RPC methods) | `config/capability_registry.toml` |
| Medical domain (12 JSON-RPC methods) | same |
| XR + Medical fallback domains | `crates/biomeos-atomic-deploy/src/capability_domains.rs` |
| `surgical-vr` niche template | `crates/biomeos-atomic-deploy/src/handlers/niche.rs` |
| `surgical_vr_deploy.toml` | `graphs/surgical_vr_deploy.toml` |

---

## JSON-RPC Methods Added

### XR Domain (petalTongue)
```
xr.negotiate_stereo    xr.submit_frame       xr.get_render_targets
xr.get_tracking_frame  xr.start_tracking     xr.stop_tracking
xr.calibrate_tracking  xr.discover_haptic    xr.send_haptic
xr.stop_haptic         xr.begin_session      xr.end_session
xr.get_session_state
```

### Medical Domain (healthSpring)
```
medical.load_anatomy         medical.list_anatomy
medical.get_anatomy_layers   medical.simulate_tissue
medical.deform_tissue        medical.reset_tissue
medical.register_tool        medical.update_tool_pose
medical.get_tool_interaction medical.process_biosignal
medical.start_biosignal_stream medical.pk_model
medical.drug_interaction
```

---

## Cross-Spring Impact

| Spring | How It Uses This |
|--------|-----------------|
| **ludoSpring** | Consumes `ContinuousExecutor` for game loops; XR adapters for VR game modes |
| **petalTongue** | Implements `xr.*` JSON-RPC methods; consumes `StereoConfig`, `TrackingFrame` |
| **healthSpring** | Implements `medical.*` JSON-RPC methods; consumes `TissueMaterial`, `AnatomyModel`, `PkModelParams` |

---

## What Comes Next

1. **petalTongue**: Implement `xr.*` JSON-RPC handlers (stereo wgpu targets, OpenXR tracking, haptic device drivers)
2. **healthSpring**: Implement `medical.*` JSON-RPC handlers (FEM tissue deformation, anatomy mesh loading, biosignal DSP)
3. **ludoSpring**: Wire game loop to `ContinuousExecutor` with real sensor input + VR rendering output
4. **surgical-vr niche**: End-to-end validation of the full surgical training pipeline

---

## Quality

- 80 new tests across biomeos-types (25), biomeos-ui (18), biomeos-atomic-deploy (14), biomeos-graph (23)
- All 3,670+ workspace tests pass
- Zero new warnings
- All new code has doc comments
