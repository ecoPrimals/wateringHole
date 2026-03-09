# petalTongue v1.4.0 — Deep Evolution Handoff

**Date**: March 9, 2026  
**From**: petalTongue  
**Status**: All crates compile, 1,427 tests passing, zero clippy warnings

---

## Summary

petalTongue v1.4.0 is a deep modernization release focused on debt elimination,
healthSpring integration, and architectural evolution toward a bidirectional
universal visualization platform.

---

## Key Changes

### Interaction Engine (new)

A comprehensive bidirectional interaction system in `petal-tongue-core::interaction`:
- **Semantic intents**: `InteractionIntent` (Select, Inspect, Navigate, Manipulate, etc.)
  abstracted from device-specific events
- **Perspective system**: Solves the "6 vs 9" problem — multiple users can view the
  same data from different orientations without conflict
- **Input adapters**: `PointerAdapter`, `KeyboardAdapter` with trait-based extensibility
- **Inverse pipelines**: Per-modality mapping from screen/audio/TUI coordinates back
  to data-space targets
- **Game-engine loop**: 8-step tick cycle (Poll → Translate → Resolve → Apply →
  Recompile → Render → Broadcast → Confirm)

### Spring Integration (new)

- **IPC visualization handler**: `visualization.render`, `visualization.render.stream`,
  `visualization.capabilities` — springs can push data to petalTongue at runtime
- **`ScenarioBuilder` trait**: Standardized way for springs to produce visualization scenes
- **`DomainPalette`**: Domain-specific color themes (Health, Physics, Ecology, etc.)
- **healthSpring compatibility**: Socket path aligned, schema round-trip verified

### Deep Debt Elimination

| Category | Before | After |
|----------|--------|-------|
| Edition | 2024 (11 crates), 2021 (4 crates) | 2024 (all 15 crates) |
| C dependencies | `libc`, `nix`, `atty`, `term_size` | Zero (pure Rust) |
| Clippy warnings | 76 errors, 487 warnings | Zero |
| Production `unwrap()` | ~15 | Zero |
| Lint suppression | `#[allow(...)]` | `#[expect(...)]` (47 items) |
| Hardcoded primals | ~6 files | Zero (capability-based) |
| Hardcoded endpoints | ~15 locations | Env var discovery with fallbacks |
| Mock in production | ~5 modules | All gated behind `#[cfg]` |
| Files > 1000 lines | 0 | 0 (max production: 650) |

### DataBinding Evolution

New variants added to support spring diversity:
- `Heatmap` — 2D density/heat data
- `Scatter3D` — 3D scatter plots
- `FieldMap` — vector/scalar field data
- `Spectrum` — frequency-domain data

Backward-compatible: `DataChannel` alias and `channel_type` serde tag preserved.

---

## IPC Contract Updates

### New Methods

| Method | Direction | Purpose |
|--------|-----------|---------|
| `visualization.render` | Inbound | Full scenario push (bindings + thresholds) |
| `visualization.render.stream` | Inbound | Incremental update (append, set_value, replace) |
| `visualization.capabilities` | Inbound | Query supported features |
| `visualization.interact` | Outbound | Broadcast interaction events |

### Socket Discovery

petalTongue now creates sockets at `XDG_RUNTIME_DIR/petaltongue/*.sock`
(subdirectory, not flat), matching healthSpring's discovery pattern.

---

## For Other Primals

To push visualization data to petalTongue:

1. Discover socket: `PETALTONGUE_SOCKET` env var → `XDG_RUNTIME_DIR/petaltongue/*.sock` → `/tmp/petaltongue-*.sock`
2. Send JSON-RPC `visualization.render` with `DataBinding` payloads
3. Stream updates via `visualization.render.stream`
4. See `wateringHole/petaltongue/VISUALIZATION_INTEGRATION_GUIDE.md` (v2.0.0)

---

## Quality Metrics

- **Tests**: 1,427 passing, 0 failed, 14 ignored
- **Clippy**: Zero warnings (`-D warnings`)
- **Formatting**: Clean
- **Unsafe**: Zero (workspace-wide `#![forbid(unsafe_code)]`)
- **C deps**: Zero
- **Edition**: 2024 (all crates)
