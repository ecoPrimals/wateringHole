# petalTongue v1.4.4 -- Spring Absorption & Deep Evolution Handoff

**Date**: March 9, 2026
**From**: petalTongue
**Status**: All 16 crates compile, tests green, zero clippy warnings

---

## Summary

petalTongue v1.4.4 absorbs integration requirements from all six springs
(healthSpring V12, neuralSpring S134, wetSpring V101, hotSpring, groundSpring,
airSpring) and the wateringHole VISUALIZATION_INTEGRATION_GUIDE v2.0.0.

This handoff completes the scene engine → IPC → rendering pipeline integration
and closes 10 evolution gaps identified during the spring ecosystem review.

---

## Absorptions Completed

### From healthSpring V12

| Item | Status |
|------|--------|
| `visualization.validate` IPC method (pre-render Tufte check) | Done |
| `visualization.export` IPC method (SVG/JSON/description export) | Done |
| `visualization.dismiss` IPC method (remove rendered visualization) | Done |
| `visualization.interact.apply` (programmatic interaction) | Done |
| `visualization.interact.perspectives` (list active perspectives) | Done |
| Callback-based `interaction.subscribe` with event filters | Done |
| Domain theming: `domain=health` / `domain=clinical` color palettes | Done |
| `UiConfig` passthrough consumed in render pipeline | Already done (V143) |
| `replace` stream operation for all DataBinding types | Already done (V143) |

### From wetSpring V101

| Item | Status |
|------|--------|
| Spectrum channel rendering (Area geometry: frequency → amplitude) | Done |
| `domain=ecology` / `domain=metagenomics` color palette | Done |
| StreamSession protocol compatibility (append, set_value, replace) | Done |

### From neuralSpring S134

| Item | Status |
|------|--------|
| `domain=ml` / `domain=neural` color palette | Done |
| 64KB IPC buffer compatibility | Already done (V143) |

### From wateringHole VISUALIZATION_INTEGRATION_GUIDE v2.0.0

| Item | Status |
|------|--------|
| 6 domain color palettes (health, physics, ecology, agriculture, measurement, neural) | Done |
| Grammar-aware IPC (`visualization.render.grammar`) | Done (V143) |
| 5 new IPC methods from spec | Done |
| Callback-based interaction subscription (not just poll) | Done |
| Sovereignty: no hardcoded primal names in production | Done |

---

## New Modules and Changes

### `petal-tongue-scene` (16 new items)

| Module | Change |
|--------|--------|
| `domain_palette.rs` | New: 6 domain palettes with 6 categorical colors each |
| `compiler.rs` | Domain-aware palette resolution; Area geometry for Spectrum |
| `animation.rs` | AnimationPlayer: manages active animations per tick |
| `modality.rs` | TerminalCompiler: scene graph → ratatui character grid |

### `petal-tongue-ipc` (12 new items)

| Module | Change |
|--------|--------|
| `visualization_handler.rs` | 5 new request/response types; validate, export, dismiss handlers |
| `visualization_handler.rs` | Callback-based `subscribe_with_filter()`, `pending_callbacks()` |
| `unix_socket_rpc_handlers.rs` | 5 new IPC method handlers in dispatch |
| `physics_bridge.rs` | New: async barraCuda IPC with CPU Euler fallback |

### `petal-tongue-ui` (2 new items)

| Module | Change |
|--------|--------|
| `scene_bridge.rs` | New: scene graph → egui paint commands bridge |
| `lib.rs` | `#![forbid(unsafe_code)]` added |

### `petal-tongue-tui` (1 new item)

| Module | Change |
|--------|--------|
| `scene_bridge.rs` | New: SceneWidget (ratatui Widget for scene graph rendering) |

### Deep Debt Resolved

| Issue | Resolution |
|-------|-----------|
| Hardcoded `"beardog"` in property_panel.rs | Replaced with capability-based discovery text |
| Hardcoded `localhost:8080` in primal_details.rs | Uses `PETALTONGUE_WEB_URL` env var |
| Hardcoded `/tmp/biomeos-neural-api.sock` | Uses constants/env pattern |
| Hardcoded ports in constants.rs | Now overridable via `PETALTONGUE_WEB_PORT` / `PETALTONGUE_HEADLESS_PORT` |
| Hardcoded songbird socket path | Uses `SONGBIRD_SOCKET_FALLBACK` env var |
| Missing `#![forbid(unsafe_code)]` in petal-tongue-ui | Added |
| Hardcoded primal names in tests | Replaced with generic `"sample_primal"` |

---

## IPC Method Coverage

petalTongue now implements these visualization IPC methods:

| Method | Status | Added |
|--------|--------|-------|
| `visualization.render` | Live | V141 |
| `visualization.render.stream` | Live | V141 |
| `visualization.render.grammar` | Live | V143 |
| `visualization.validate` | **Live** | **V144** |
| `visualization.export` | **Live** | **V144** |
| `visualization.dismiss` | **Live** | **V144** |
| `visualization.capabilities` | Live | V141 |
| `interaction.subscribe` | Live (callback+poll) | V143 / **V144** |
| `interaction.poll` | Live | V143 |
| `interaction.unsubscribe` | Live | V143 |
| `visualization.interact.apply` | **Live** | **V144** |
| `visualization.interact.perspectives` | **Live** | **V144** |

---

## For Springs

### healthSpring
- All P0 and P1 items from V12 handoff are implemented server-side.
- `visualization.interact.subscribe` now accepts `events`, `callback_method`, `grammar_id` params.
- `visualization.validate` returns Tufte score + per-constraint results.
- Domain palettes: `health`, `clinical` → green/amber/red clinical palette.

### wetSpring
- Spectrum data renders as Area geometry (filled region + line overlay).
- Domain palettes: `ecology`, `metagenomics` → greens/browns ecological palette.
- All 3 stream operations work for all 8 DataBinding types.

### neuralSpring
- Domain palettes: `ml`, `neural` → electric blue/magenta palette.
- Grammar expressions compile to domain-themed visualizations.

### hotSpring / groundSpring / airSpring
- Domain palettes ready: `physics`/`plasma`, `measurement`/`calibration`, `agriculture`/`atmospheric`.
- These springs should add `PetalTonguePushClient` following healthSpring's pattern.

### barraCuda
- Physics bridge (`physics_bridge.rs`) discovers barraCuda socket at runtime.
- `barracuda.compute.dispatch` with `math.physics.nbody` payload.
- CPU Euler fallback when barraCuda is unavailable.

---

## Quality Metrics

- **Workspace**: Compiles clean
- **Clippy**: Zero warnings (pedantic, `-D warnings`)
- **Tests**: 77 (scene) + 79 (IPC) + 33 (TUI) + 4 (UI bridge) = 193 in modified crates
- **Unsafe**: Zero (workspace-wide `#![forbid(unsafe_code)]`)
- **Formatting**: Clean (`cargo fmt --check`)

---

## Remaining Evolution Targets

| Target | Priority | Notes |
|--------|----------|-------|
| `visualization.interact.sync` (perspective sync mode) | P2 | Needs multi-user state |
| `visualization.render.stream` grammar subscription mode | P2 | Needs capability-based data resolution |
| Capability-based data resolution (`"source": "capability:X"`) | P2 | Requires Songbird integration |
| hotSpring/groundSpring/airSpring viz push clients | P1 | Follow healthSpring pattern |
| GPU rendering via Toadstool IPC | P2 | Needs GpuCompiler modality |
| Industry-standard benchmarks for barraCuda GPU | P2 | No Kokkos/STREAM/HPCG yet |
