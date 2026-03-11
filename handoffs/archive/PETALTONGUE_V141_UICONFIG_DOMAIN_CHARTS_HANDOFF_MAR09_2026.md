# petalTongue v1.4.1 — UiConfig IPC & Domain-Aware Rendering Handoff

**Date**: March 9, 2026  
**From**: petalTongue  
**Status**: All crates compile, 1,421 tests passing, zero clippy warnings

---

## Summary

petalTongue v1.4.1 adds UiConfig support for spring-driven UI configuration
via IPC, domain-aware chart rendering with automatic palette selection, and
improved Scatter3D visualization. Five additional large files refactored.

---

## Key Changes

### UiConfig IPC (new)

Springs can now push UI configuration alongside data via `visualization.render`:

```json
{
  "method": "visualization.render",
  "params": {
    "session_id": "pk-study-001",
    "title": "PK/PD Analysis",
    "bindings": [...],
    "domain": "health",
    "ui_config": {
      "show_panels": {"left_sidebar": true, "audio_panel": false},
      "mode": "clinical",
      "initial_zoom": "fit",
      "awakening_enabled": false,
      "theme": "clinical-dark"
    }
  }
}
```

Fields in `UiConfig`:
- `show_panels`: Panel visibility map
- `mode`: Initial mode ("clinical", "research", "monitoring")
- `initial_zoom`: Zoom preset ("fit", "1.0", "2.0")
- `awakening_enabled`: Whether to show awakening sequence
- `theme`: Theme override

### Domain-Aware Chart Renderers

Chart renderers for Heatmap, Scatter3D, FieldMap, and Spectrum now use
`DomainPalette` colors based on session domain instead of hardcoded
clinical_theme colors:

| Domain | Colors |
|--------|--------|
| health/clinical | Blue-green medical palette |
| physics/plasma/nuclear | Orange-amber physics palette |
| ecology/chemistry | Green ecology palette |
| agriculture/hydrology | Blue-brown atmospheric palette |
| measurement/calibration | Gray-blue measurement palette |
| ml/neural/surrogate | Purple-cyan neural palette |

Callers pass `domain` through `draw_channel(ui, binding, Some("physics"))`.

### Improved Scatter3D

- Z-axis encoded as color intensity (darker = higher z) and point size
  (larger = higher z) across 8 bands
- Switched from connected `Line` to discrete `Points` rendering
- Point labels shown on hover with x, y, z coordinates
- Header shows z-value range

### File Refactorings

| Before | After |
|--------|-------|
| `chart_renderer.rs` (648 lines) | `chart_renderer/` (basic_charts + domain_charts) |
| `graph_builder.rs` (610 lines) | `graph_builder/` (types + builder + tests) |
| `tarpc_client.rs` (602 lines) | `tarpc_client/` (types + client + tests) |
| `jsonrpc_provider.rs` (611 lines) | `jsonrpc_provider/` (types + provider + tests) |
| `display_verification.rs` (594 lines) | `display_verification/` (types + verifier + tests) |

---

## For Other Primals

### Pushing Data with UI Configuration

1. Discover socket (same as v1.4.0)
2. Send `visualization.render` with optional `ui_config` field
3. petalTongue applies panel visibility, mode, zoom from your config
4. Domain hint selects appropriate color palette automatically

### Domain Selection

Set `domain` in your render request to get appropriate colors:
- healthSpring → `"health"`
- wetSpring → `"ecology"` or `"hydrology"`
- hotSpring → `"physics"` or `"plasma"`
- neuralSpring → `"neural"` or `"ml"`

---

## Quality Metrics

- **Tests**: 1,421 passing, 0 failed, 3 ignored
- **Clippy**: Zero warnings (`-D warnings`)
- **Formatting**: Clean
- **Unsafe**: Zero (workspace-wide `#![forbid(unsafe_code)]`)
- **C deps**: Zero
- **Edition**: 2024 (all crates)
- **Max file**: 650 lines
