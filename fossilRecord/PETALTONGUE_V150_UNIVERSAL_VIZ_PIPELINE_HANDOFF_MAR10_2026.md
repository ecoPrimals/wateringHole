# petalTongue v1.5.0 — Universal Visualization Pipeline Handoff

**Date**: March 10, 2026  
**From**: petalTongue  
**Version**: 1.5.0  
**Tests**: 2,011 passing  
**Supersedes**: V144, V200 (deep debt)

---

## What Changed

### DataBinding → Grammar of Graphics Auto-Compiler

`petal-tongue-scene::DataBindingCompiler` converts all 8 `DataBinding` variants
into `GrammarExpr` + data rows for the grammar compiler:

| DataBinding | Geometry | Scale | Notes |
|-------------|----------|-------|-------|
| TimeSeries | Line | Linear x/y | x=time, y=value |
| Distribution | Bar | Linear x/y | 20-bin histogram |
| Bar | Bar | Categorical x | Category index as x |
| Gauge | Bar | — | Title shows "label: value unit" |
| Spectrum | Area | Linear x/y | Filled frequency plot |
| Heatmap | Tile | Categorical x/y | Row-major flattening |
| Scatter3D | Point | Perspective3D | z variable binding |
| FieldMap | Tile | Linear x/y | Numeric grid coordinates |

**Auto-wired**: `visualization.render` now compiles every DataBinding to a scene
graph on receive. Springs get rendered automatically.

### Dashboard Layout Engine

`petal-tongue-scene::build_dashboard()` composes DataBindings into multi-panel grid:

- Configurable: `Grid { max_columns }`, `Vertical`, `Horizontal`
- Domain palette theming (health=green/amber/red, ecology=greens/browns, etc.)
- Panel titles, backgrounds, strokes auto-applied
- New IPC method: `visualization.render.dashboard`

### Scenario Loader

`petal-tongue-core::LoadedScenario` parses healthSpring-style JSON scenarios:

- `from_file(path)` / `from_json(json_str)`
- Nested `ecosystem.primals[].data_channels` + `clinical_ranges` + edges
- `inferred_domain()` resolves from node families
- CLI: `petaltongue ui --scenario path/to/scenario.json`

---

## New IPC Method

### `visualization.render.dashboard`

```json
{
  "jsonrpc": "2.0",
  "method": "visualization.render.dashboard",
  "params": {
    "session_id": "study-001",
    "title": "Full Clinical Dashboard",
    "domain": "health",
    "max_columns": 3,
    "bindings": [ ... DataBinding payloads ... ]
  },
  "id": 1
}
```

Response: `{ panel_count, columns, rows, scene_nodes, total_primitives, output (SVG), modality }`

---

## Quality Gates

| Check | Result |
|-------|--------|
| `cargo fmt --all` | Clean |
| `cargo clippy --workspace -- -D warnings` | Zero warnings |
| `cargo test --workspace` | 2,011 pass |
| `RUSTDOCFLAGS="-D warnings" cargo doc` | Clean |
| `#![forbid(unsafe_code)]` | Enforced |
| Edition | 2024, all 16 crates |

---

## For Springs

Any spring pushing `DataBinding` payloads via `visualization.render` now gets
automatic Grammar of Graphics rendering. No changes needed on the spring side.

For multi-panel dashboards, use `visualization.render.dashboard` with multiple
bindings. The dashboard auto-layouts panels in a grid with domain theming.

For offline viewing, export scenario JSON and load with:
```bash
petaltongue ui --scenario my_scenario.json
```

---

## New Exports

| Crate | Export | Purpose |
|-------|--------|---------|
| `petal-tongue-scene` | `DataBindingCompiler` | DataBinding → GrammarExpr |
| `petal-tongue-scene` | `Dashboard`, `DashboardConfig`, `DashboardLayout` | Dashboard types |
| `petal-tongue-scene` | `build_dashboard`, `compose_dashboard` | Dashboard builders |
| `petal-tongue-core` | `LoadedScenario`, `ScenarioNode`, `ScenarioEdge` | Scenario types |

---

## Next Steps

- Tile geometry rendering in grammar compiler (currently placeholder text)
- Arc geometry for proper gauge rendering
- Scale application in compiler (linear, log, temporal transform data values)
- Multi-panel PNG export via tiny-skia
- Live dashboard streaming (backpressure-aware multi-panel updates)
