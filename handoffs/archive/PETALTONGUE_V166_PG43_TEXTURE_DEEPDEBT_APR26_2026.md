# petalTongue v1.6.6 — PG-43 Texture Primitive + Deep Debt Resolution

**Date**: April 26, 2026
**Commits**: `94f6068` (PG-43), `4d63ed6` (dep consolidation), `090eafc` (hardcode fix)

---

## PG-43: Texture Primitive + IPC Methods

### Added

- **`Primitive::Texture`** variant in scene graph — raster content (sprites, images,
  external engine framebuffers) with `texture_id`, position, size, optional UV
  sub-region (`UvRect`), opacity, and tint.
- **`TextureRegistry`** in `VisualizationState` — stores pixel data keyed by
  `texture_id`, versioned for lazy GPU re-upload.
- **`visualization.texture.upload`** IPC method — push base64-encoded RGBA pixel
  data, get a `texture_id` back.
- **`visualization.texture.attach`** IPC method — register a shared-memory source
  (memfd URI); actual mapping deferred to toadStool Display Phase 2.
- **`From<Sprite> for SceneNode`** bridge — converts game `Sprite` models directly
  into scene graph `Primitive::Texture` nodes.
- All 12 exhaustive `match Primitive` sites updated across `petal-tongue-scene`
  (7 sites) and `petal-tongue-ui` (3 sites + 2 wildcards).
- Tests: Primitive serde, Sprite bridge, TextureRegistry, IPC handlers,
  `rich_test_scene()` fixture includes Texture.

### Deferred

- **Overlay mode** — depends on toadStool Display Phase 2 + Wayland `wlr-layer-shell`
- **egui `Shape::image`** with `TextureResolver` — placeholder tinted rect in place

### For downstream (ludoSpring, esotericWebb)

Springs can now push textures via IPC:

```json
{"jsonrpc":"2.0","method":"visualization.texture.upload","params":{
  "texture_id":"hero-idle-01","width":64,"height":64,"format":"rgba8",
  "data":"<base64 RGBA bytes>"},"id":1}
```

Then reference in scene graphs:

```json
{"Texture":{"texture_id":"hero-idle-01","x":10,"y":20,"width":64,"height":64,
  "uv":{"u":0,"v":0,"w":0.5,"h":0.5},"opacity":1.0,"tint":null,"data_id":"sprite-01"}}
```

---

## Deep Debt Resolution

### Dependency Consolidation

- `uuid`: unified 1.7/1.9 version skew to workspace dep (1.9 + v4,serde)
- `tokio-tungstenite`: deduplicated from core+ui into single workspace dep
- `tarpc`: removed unused `tcp` feature (only Unix transport used)
- `chrono`: trimmed default features to clock+serde
- `tokio "full"`: removed from petal-tongue-cli (inherits workspace minimum)

### Hardcode Elimination

- `physics_bridge.rs`: replaced hardcoded `/tmp` with `LEGACY_TMP_PREFIX` constant
- `pixel_renderer_demo.rs`: aligned with `DEMO_OUTPUT_DIR` env pattern

### Audit Findings (clean)

- Zero files >700 lines (largest: 645L)
- Zero `unsafe`, zero `dyn`/`Box<dyn>` in production
- Zero `todo!`/`unimplemented!`/`panic!` in production
- Zero TODO/FIXME/HACK/XXX comments
- Zero `#[allow]` in production (uses `#[expect]` with reasons)
- All mocks gated behind `#[cfg(test)]` or `feature = "test-fixtures"`
- Production `unwrap()`: zero in core paths; handlers use `PoisonError::into_inner`
- `ring` not in lockfile
- Lockfile duplication (thiserror 1.0/2.0, base64 0.21/0.22) is from transitive deps

### Audio Stub Documentation

Audio backends (`direct.rs`, `socket.rs`) doc comments updated to clearly mark
as ToadStool `audio.play` capability-discovery evolution targets.

---

## Verification

- 0 clippy warnings (workspace, all-features)
- 6,022+ tests passing, 0 failures
- macOS aarch64 cross-check clean
- Edition 2024, stable toolchain
