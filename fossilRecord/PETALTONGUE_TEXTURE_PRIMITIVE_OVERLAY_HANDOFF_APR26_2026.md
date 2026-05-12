# petalTongue — Texture Primitive + Overlay Mode

**From**: primalSpring v0.9.17 (Phase 45c — Graphics Node)
**Date**: April 26, 2026
**For**: petalTongue team

---

## Context

petalTongue's native desktop `live` mode is working (PG-40 resolved, winit
threading fixed in `27ce42a`). We can push dashboards, stream updates, and
poll interactions through JSON-RPC. The system is validated live with
barraCuda science calls rendered in real-time.

The next goal is **petalTongue as full graphics system** — not just
science-grade visualization, but capable of rendering game assets, compositing
external engine output, and providing transparent overlays. Two evolutions
are needed.

---

## 1. Texture Primitive — Raster Content in the Scene Graph

**Priority**: CRITICAL
**Current state**: `Primitive` enum has Point, Line, Rect, Text, Polygon,
Arc, BezierPath, Mesh — all vector. No raster/image/texture support.

### The gap

The `Sprite`/`Tilemap`/`GameScene` model in `petal-tongue-scene/src/sprite.rs`
already defines `texture_id: String` for game-oriented payloads, but this
model is NOT connected to the actual `SceneGraph` → `scene_bridge` → `egui`
render pipeline. The `Primitive` enum that drives rendering has no texture
variant.

This means:
- Cannot display images, icons, or raster content in the scene graph
- Cannot embed external engine frame output (e.g. Godot viewport capture)
- Cannot render game sprites through the standard SceneGraph path
- The existing `Sprite`/`GameScene` types are data-only with no renderer

### Proposed change

Add a `Texture` variant to the `Primitive` enum in
`crates/petal-tongue-scene/src/scene_graph/primitive/mod.rs`:

```rust
pub enum Primitive {
    Point { /* existing */ },
    Line { /* existing */ },
    Rect { /* existing */ },
    Text { /* existing */ },
    Polygon { /* existing */ },
    Arc { /* existing */ },
    BezierPath { /* existing */ },
    Mesh { /* existing */ },
    Texture {
        texture_id: String,
        rect: Rect,
        uv: Option<UvRect>,
        opacity: f32,
        tint: Option<Color>,
    },
}
```

### texture_id resolution

The `texture_id` is a string handle that resolves to pixel data at render
time. Resolution order:

1. **In-process egui texture**: `egui::TextureId` registered via
   `egui::Context::load_texture()` — for static images, icons, sprites
   loaded from disk or IPC
2. **Shared memory (memfd)**: Mapped from toadStool display backend — for
   external engine framebuffer output (zero-copy)
3. **IPC upload**: New `visualization.texture.upload` method that accepts
   base64-encoded RGBA pixels + dimensions, returns a `texture_id`

### Files that need updating

| File | Change |
|------|--------|
| `petal-tongue-scene/src/scene_graph/primitive/mod.rs` | Add `Texture` variant |
| `petal-tongue-scene/src/modality/svg.rs` | Render as `<image>` element |
| `petal-tongue-scene/src/modality/terminal.rs` | Render as placeholder `[IMG]` |
| `petal-tongue-scene/src/modality/audio.rs` | Skip (no audio equivalent) |
| `petal-tongue-scene/src/modality/braille.rs` | Render as `[image: {label}]` |
| `petal-tongue-scene/src/modality/haptic.rs` | Skip |
| `petal-tongue-scene/src/modality/description.rs` | Emit text description |
| `petal-tongue-scene/src/gpu_compiler.rs` | Add `GpuDrawCommand::DrawTexture` |
| `petal-tongue-ui/src/scene_bridge/paint/mod.rs` | `paint_primitive` match arm: resolve `texture_id` → `egui::TextureId`, draw `egui::Shape::image()` |
| `petal-tongue-ui/src/scene_bridge/paint/primitives.rs` | Texture painting implementation |

### New IPC method: `visualization.texture.upload`

```json
{
  "jsonrpc": "2.0",
  "method": "visualization.texture.upload",
  "params": {
    "texture_id": "sprite-hero-idle-01",
    "width": 64,
    "height": 64,
    "format": "rgba8",
    "data": "<base64-encoded RGBA pixels>"
  },
  "id": 1
}
```

Response: `{"texture_id": "sprite-hero-idle-01", "status": "loaded"}`

For shared memory textures (from toadStool display or external engines):

```json
{
  "jsonrpc": "2.0",
  "method": "visualization.texture.attach",
  "params": {
    "texture_id": "godot-viewport",
    "source": "memfd://godot-fb-0",
    "width": 1920,
    "height": 1080,
    "format": "rgba8",
    "refresh": "per_frame"
  },
  "id": 1
}
```

### Connecting Sprite/GameScene to SceneGraph

Once the Texture primitive exists, bridge the existing `Sprite`/`GameScene`
model to the SceneGraph render pipeline:

```rust
impl From<Sprite> for SceneNode {
    fn from(sprite: Sprite) -> Self {
        SceneNode {
            id: NodeId::new(),
            transform: Transform2D::translate(sprite.x, sprite.y)
                .then_rotate(sprite.rotation)
                .then_scale(sprite.scale_x, sprite.scale_y),
            primitives: vec![Primitive::Texture {
                texture_id: sprite.texture_id,
                rect: Rect::from_size(sprite.width, sprite.height),
                uv: sprite.uv_rect,
                opacity: sprite.opacity,
                tint: sprite.tint,
            }],
            children: vec![],
            visible: sprite.visible,
            opacity: sprite.opacity,
            label: sprite.label,
            data_source: None,
        }
    }
}
```

---

## 2. Overlay Mode — Transparent Window Over External Games

**Priority**: MEDIUM (depends on Texture primitive + toadStool Display Phase 2)

### The need

For "attach NUCLEUS to an existing game" scenarios, petalTongue needs a
mode where it renders a transparent overlay on top of another application's
window — displaying HUD, dashboards, metrics, collectible UI without
replacing the game's own rendering.

### Proposed mode: `overlay`

Beyond existing `live`, `web`, `server`, `ui` modes:

```bash
petaltongue overlay --target-window "Godot Engine" --socket /path/to/ipc.sock
```

### Implementation approaches (choose based on display stack)

**Option A: Wayland layer-shell** (recommended for Wayland compositors)
- Use `wlr-layer-shell-unstable-v1` protocol to create an overlay surface
- Position above the target window's layer
- Alpha-transparent background, only petalTongue content visible
- Input: configurable — pass-through by default, capture on hover over
  petalTongue elements

**Option B: toadStool display compositing** (recommended for DRM-direct)
- petalTongue renders to a toadStool-managed framebuffer with alpha
- toadStool composites petalTongue layer on top of external engine layer
- See toadStool handoff: `display.composite` method

**Option C: X11 overlay** (fallback for X11 sessions)
- Override-redirect window with `_NET_WM_WINDOW_TYPE_DOCK`
- ARGB visual for transparency
- Input: X11 shape extension for click-through

### Scene graph for overlay

Overlay mode uses the same SceneGraph/visualization.render pipeline. The
only difference is the window is transparent and positioned over the target.
Existing `channel_type` bindings (gauge, bar, timeseries) work unchanged.

New overlay-specific bindings:

| channel_type | Purpose |
|--------------|---------|
| `hud` | Fixed-position elements (health bar, minimap, FPS counter) |
| `tooltip` | Contextual popup near cursor position |
| `notification` | Transient messages (item acquired, achievement) |

These compose existing primitives (Rect, Text, gauge, bar) with absolute
positioning in overlay space.

---

## Summary — What We Need From petalTongue

| Evolution | Priority | Blocks | Estimated Scope |
|-----------|----------|--------|-----------------|
| Texture Primitive | CRITICAL | Game content rendering, sprite display, external engine embedding | New `Primitive` variant + 10 file updates + 2 new IPC methods |
| Overlay Mode | MEDIUM | Transparent overlays on existing games | New mode in main.rs + layer-shell/compositor integration |

The Texture primitive is the single most impactful change — it bridges the
gap between petalTongue's existing data visualization and game-grade content
rendering. Once textures work, sprites, tilemaps, and external framebuffer
embedding all fall out naturally.

---

**References**:
- Primitive enum: `petal-tongue-scene/src/scene_graph/primitive/mod.rs`
- Sprite/GameScene: `petal-tongue-scene/src/sprite.rs`
- Scene bridge paint: `petal-tongue-ui/src/scene_bridge/paint/mod.rs`
- GpuCompiler: `petal-tongue-scene/src/gpu_compiler.rs`
- Grammar types: `petal-tongue-ipc/src/visualization_handler/types/grammar.rs`
- primalSpring gap registry: `primalSpring/docs/PRIMAL_GAPS.md`

License: AGPL-3.0-or-later
