# petalTongue V1.6.4 — Game Scenes, Soundscapes, JSONL Telemetry

**Date**: March 15, 2026  
**From**: petalTongue  
**Status**: Green — 5,113 tests, zero clippy warnings, all crates clean

---

## What Changed

### New DataBinding Variants

Two new channel types added to the universal visualization pipeline:

- **`game_scene`**: 2D game state with tilemap, sprites, entities, and camera control.
  ludoSpring's composable raid visualization can now push game state directly.
- **`soundscape`**: Layered audio definition with waveform types, stereo panning,
  and fade envelopes. Supports game audio, ecology ambience, and any domain.

Total DataBinding variants: 9 → 11 (plus existing `timeseries`, `distribution`,
`bar`, `gauge`, `heatmap`, `scatter`, `scatter3d`, `fieldmap`, `spectrum`).

### New Modules

| Module | Crate | Purpose |
|--------|-------|---------|
| `sprite.rs` | petal-tongue-scene | Sprite, Tilemap, Tile, GameEntity, GameScene types |
| `soundscape.rs` | petal-tongue-scene | SoundLayer, Soundscape, Waveform, stereo synthesis |
| `jsonl_provider.rs` | petal-tongue-discovery | JSONL telemetry file reader (hotSpring bridge) |
| `capability_names.rs` | petal-tongue-core | 60 centralized capability/method/socket constants |

### SpringDataAdapter Evolution

- **UiConfig parsing**: Spring-native pushes now extract `ui_config` (theme, panels,
  mode, zoom) and `thresholds` from the JSON payload instead of discarding them.
- **GameScene detection**: `{"channel_type": "game_scene", "scene": {...}}` auto-detected.
- **Soundscape detection**: `{"channel_type": "soundscape", "definition": {...}}` auto-detected.

### Workspace Lint Evolution

Clippy pedantic + nursery now fully managed via `[workspace.lints.clippy]` in
root `Cargo.toml`. The CI command no longer needs `-W clippy::pedantic -W clippy::nursery`
flags — just `cargo clippy --workspace --all-targets -- -D warnings` is sufficient.

New workspace-level allows: `missing_errors_doc`, `missing_panics_doc`, `must_use_candidate`.

---

## For ludoSpring

The composable raid visualization project can now:

1. Push game scenes via JSON-RPC `visualization.render` with `channel_type: "game_scene"`
2. Push soundscapes via `channel_type: "soundscape"` 
3. Use standard `GameChannelType` for engagement/difficulty/flow data (existing)
4. All three formats auto-detected by `SpringDataAdapter`

### Example game scene push:

```json
{
  "jsonrpc": "2.0",
  "method": "visualization.render",
  "params": {
    "session_id": "raid-1",
    "title": "Dungeon Level 1",
    "bindings": [{
      "channel_type": "game_scene",
      "id": "dungeon_1",
      "label": "Dungeon Level 1",
      "scene": {
        "tilemap": { "dimensions": [32, 24], "tile_size": [16, 16], "tiles": [...] },
        "sprites": [{ "id": "chest", "position": [128, 64], "size": [16, 16] }],
        "entities": [{ "id": "player", "entity_type": "player", "position": [80, 80], "health": 0.9 }],
        "camera_center": [80, 80],
        "camera_zoom": 2.0
      }
    }],
    "domain": "game",
    "ui_config": { "mode": "game", "theme": "dungeon-dark" }
  },
  "id": 1
}
```

---

## For hotSpring

JSONL telemetry files are now discoverable. Write telemetry to
`$PETALTONGUE_TELEMETRY_DIR/*.jsonl` (or `$XDG_DATA_HOME/petaltongue/telemetry/`)
using the standard `{t, section, ...numeric_fields}` schema. petalTongue will
auto-convert each section/field pair to a `TimeSeries` DataBinding.

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 5,076 | 5,113 |
| DataBinding variants | 9 | 11 |
| Capability constants | 0 | 60 |
| Clippy warnings | 0 | 0 |
| Largest file | 876 | 876 |
