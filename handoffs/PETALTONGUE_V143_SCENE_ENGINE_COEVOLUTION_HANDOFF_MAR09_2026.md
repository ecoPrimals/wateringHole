# petalTongue v1.4.3 -- Scene Engine & healthSpring Coevolution Handoff

**Date**: March 9, 2026
**From**: petalTongue
**Status**: All 16 crates compile, 1,896 tests passing, zero clippy warnings

---

## Summary

petalTongue v1.4.3 adds the `petal-tongue-scene` crate (16th crate) implementing
a declarative scene graph with Manim-style animation, Grammar of Graphics
compiler, Tufte constraint validation, multi-modality output compilers, and
physics bridge for barraCuda IPC. Also completes healthSpring coevolution work
including SAME DAVE channel wiring, interaction subscriptions, and clinical
mode presets.

---

## New: petal-tongue-scene Crate

A pure Rust declarative scene engine that bridges grammar expressions and
rendered output. 69 tests, zero unsafe, clippy pedantic clean.

### Modules

| Module | Purpose |
|--------|---------|
| `primitive` | 8 atomic rendering primitives (Point, Line, Rect, Text, Polygon, Arc, BezierPath, Mesh) with Color, StrokeStyle, hit-test data IDs |
| `transform` | 2D affine (3x3) and 3D (4x4) spatial transforms with composition and inverse |
| `scene_graph` | Hierarchical scene graph (SceneNode tree, flatten to world-space primitives, find_by_data_id) |
| `animation` | 6 easing functions (Linear, EaseIn/Out, EaseInOut, Spring, Bounce), animation targets, Sequential/Parallel sequences |
| `math_objects` | Manim-style: NumberLine, Axes, FunctionPlot, ParametricCurve, VectorField compile to primitives |
| `grammar` | GrammarExpr with VariableBinding, ScaleType, GeometryType, CoordinateSystem, Facet, Aesthetic |
| `tufte` | Machine-checkable constraints: Data-Ink Ratio, Lie Factor, Chartjunk, Color Accessibility, Data Density |
| `compiler` | GrammarExpr + JSON data to SceneGraph (with optional Tufte constraint evaluation) |
| `modality` | SvgCompiler, AudioCompiler, DescriptionCompiler (accessibility text) |
| `physics` | PhysicsWorld with CPU Euler fallback and IPC bridge for `math.physics.nbody` |

### Ecosystem Delegation

The scene engine owns scene description, animation, and grammar compilation.
GPU compute and shader execution are delegated:

- **barraCuda**: Math engine, WGSL shaders, physics simulations (N-body, molecular dynamics) via `math.physics.nbody` IPC
- **Toadstool**: GPU hardware orchestration, dispatch, load balancing
- **coralReef**: WGSL/SPIR-V to native GPU binary compilation

### For Other Primals

Any primal can send visualization data to petalTongue via:

1. **Grammar expressions** (`GrammarExpr` JSON) -- petalTongue compiles to scene graph and renders
2. **Raw scene graphs** (`SceneGraph` JSON) -- direct scene injection for custom visuals
3. **Existing IPC** (`visualization.render`) -- unchanged, backward compatible

New types are in the `petal-tongue-scene` crate. Add as a dependency for type sharing,
or construct the equivalent JSON directly.

---

## healthSpring Coevolution

Completed all items from healthSpring's V9 handoff:

| Item | Status |
|------|--------|
| ChannelRegistry wired to app update loop | Done -- keyboard, pointer, visual-efferent signals recorded |
| `interaction.subscribe` / `poll` / `unsubscribe` IPC | Done -- full subscription lifecycle with broadcast |
| 64KB IPC buffer | Done -- `BufReader::with_capacity(65_536, reader)` |
| `research_mode()` / `patient_facing_mode()` presets | Done -- motor command bundles |
| Motor command history in proprioception panel | Done -- timestamped history display |
| SAME DAVE doc clarification | Done -- neuroanatomy model, not acronym expansion |

---

## Quality Metrics

- **Tests**: 1,896 passing (1,816 to 1,896, +80)
- **Crates**: 16 (15 + petal-tongue-scene)
- **Clippy**: Zero warnings (pedantic enabled, scene crate included)
- **Formatting**: Clean
- **Unsafe**: Zero (workspace-wide `#![forbid(unsafe_code)]`)
- **IPC contract**: No breaking changes (new methods are additive)

---

## For healthSpring

- `interaction.subscribe` returns a subscriber ID; poll with `interaction.poll`
- Motor commands recorded in proprioception panel with timestamps
- `research_mode` and `patient_facing_mode` presets available via `commands_for_mode()`
- Channel registry captures keyboard/pointer/visual-efferent signals per frame

## For barraCuda

- `PhysicsWorld::to_ipc_request()` serializes to `math.physics.nbody` JSON-RPC format
- `PhysicsWorld::apply_ipc_response()` reads back computed positions/velocities
- CPU Euler fallback when barraCuda is unavailable
- Physics bodies have collision shapes (Sphere, Box, None)

## For Toadstool

- Scene graph `flatten()` produces world-transformed primitives ready for GPU dispatch
- Modality compilers can be extended with `GpuCompiler` targeting Toadstool IPC
