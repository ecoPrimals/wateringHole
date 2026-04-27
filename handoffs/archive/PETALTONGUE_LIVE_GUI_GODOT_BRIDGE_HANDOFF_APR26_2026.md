# petalTongue Live GUI + Godot Bridge — Handoff

**Date:** April 26, 2026  
**From:** primalSpring (composition validation)  
**For:** ludoSpring, esotericWebb, all spring teams  
**Phase:** Live Desktop UI + External Engine Integration

---

## What Changed

### 1. IPC Scenes Now Render in the egui Central Panel

Previously, IPC-pushed scenes via `visualization.render`, `visualization.render.grammar`, and `visualization.render.scene` were stored in `VisualizationState.grammar_scenes` but **not displayed** in the main egui window. The central panel only rendered the local topology graph.

**Now:** When `grammar_scenes` is non-empty, the central panel renders those scenes using the scene bridge paint pipeline. Multiple sessions stack vertically with labels. Single sessions fill the available space. `continuous_mode` auto-enables when IPC sessions are active, so `AnimationPlayer` ticks and Manim-style animations run.

**Key files:**
- `petal-tongue-ui/src/app/panels.rs` — `render_ipc_scenes()` in central panel
- `petal-tongue-ui/src/app/update.rs` — auto-enable `continuous_mode`

### 2. TextureRegistry Resolves in egui Painter

`Primitive::Texture` previously painted a placeholder rect. Now it resolves `texture_id` against pre-loaded egui `TextureHandle`s and paints real pixels via `egui::Shape::image()`.

Each frame, `sync_textures_to_egui()` checks the IPC `TextureRegistry` for new or updated textures and uploads them to egui. Version watermarks prevent redundant uploads.

**Key files:**
- `petal-tongue-ui/src/scene_bridge/paint/primitives.rs` — `paint_primitive_textured()`
- `petal-tongue-ui/src/scene_bridge/paint/mod.rs` — `paint_scene_textured()`
- `petal-tongue-ui/src/app/update.rs` — `sync_textures_to_egui()`

### 3. Cell Graphs: spawn=true

All primal nodes in `ludospring_cell.toml` and `esotericwebb_cell.toml` now have `spawn = true` (except `biomeos_neural_api` which must already be running). This means `cell_launcher.sh` actually starts primals.

Updated in both `primalSpring/graphs/cells/` and `plasmidBin/cells/`.

### 4. Live NUCLEUS + Demo Scripts

- **`tools/live_nucleus.sh`** — Starts a NUCLEUS from plasmidBin binaries + petalTongue in live mode, then pushes demo scenes
- **`tools/push_demo_scene.sh`** — Pushes Grammar of Graphics, dashboard, and Manim-style scenes to a running petalTongue socket. Reusable for any live session

### 5. Godot Bridge Prototype

A shared-memory frame bridge for external renderers (Godot 4, or any engine that can write RGBA8 pixels):

- **`tools/godot_bridge.sh`** — Daemon that watches `/dev/shm/godot-frame.rgba` and uploads to petalTongue via `visualization.texture.upload`
- **`tools/godot_bridge.gd`** — Example GDScript that captures Godot viewport and writes to shared memory

**Architecture:**
```
Godot viewport → /dev/shm/godot-frame.rgba → godot_bridge.sh → texture.upload → TextureRegistry → Primitive::Texture → egui paint
```

Grammar of Graphics and Manim overlays render on top of the Godot frame in the same live window.

---

## For ludoSpring

1. Pull latest `primalSpring` and `plasmidBin`
2. Your `ludospring_cell.toml` now spawns primals — test with `cell_launcher.sh`
3. Push game scenes to petalTongue via `visualization.render.grammar` or `visualization.render.scene`
4. For live gameplay: use `visualization.render.stream` for incremental data updates (60Hz capable)
5. For Godot integration: attach `godot_bridge.gd` to your Godot scene, run `godot_bridge.sh` alongside

## For esotericWebb

1. Same as ludoSpring — your cell graph now spawns
2. The Godot bridge pattern enables: Grammar of Graphics overlays + Godot 3D in the same petalTongue window
3. Provenance trio records sessions; certificates mint through the same composition

## JSON-RPC Methods for Live Scenes

| Method | Purpose |
|--------|---------|
| `visualization.render.grammar` | Push a Grammar of Graphics expression (scatter, bar, line) |
| `visualization.render.scene` | Push a SceneGraph (primitives, shapes, text) |
| `visualization.render.dashboard` | Push a multi-panel grid layout |
| `visualization.render.stream` | Push incremental data updates to existing sessions |
| `visualization.texture.upload` | Upload RGBA8 pixels (for Godot bridge, sprites) |
| `interaction.subscribe` | Subscribe to user interaction events |
| `interaction.poll` | Poll for user clicks, selections, hovers |

---

## Known Gaps

| Gap | Status | Notes |
|-----|--------|-------|
| `visualization.texture.attach` | Placeholder | petalTongue has the type but no IPC handler yet |
| UV sub-rect for Primitive::Texture | egui path ignores UV | Full UV requires splitting into sub-rect at paint time |
| Input feedback Godot ← petalTongue | Not wired | Use `interaction.poll` from GDScript via JSON-RPC |
| Mixed Godot + Grammar overlays | Manual | Compositor needs z-ordering API for scene layers |
