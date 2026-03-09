# Visualization Integration Guide for petalTongue

**Version**: 1.0.0  
**Date**: March 8, 2026  
**Audience**: Any primal team that wants petalTongue to visualize their data  
**Status**: Active Standard

---

## Quick Summary

petalTongue is evolving from a fixed-widget UI to a **Grammar of Graphics** engine.
Any primal can send a grammar expression via JSON-RPC, and petalTongue will render it
across all available modalities (GUI, TUI, audio, SVG, API).

If you have data you want a human to understand, this guide tells you how to get
petalTongue to render it.

---

## Three Ways to Integrate

### 1. Send Raw Data (Simplest)

Send your data as JSON arrays over JSON-RPC. petalTongue will auto-detect the schema
and generate a default visualization.

```json
{
  "jsonrpc": "2.0",
  "method": "visualization.render",
  "params": {
    "data": {
      "inline": [
        {"timestamp": "2026-03-08T14:00:00Z", "cpu_pct": 42.3, "host": "alpha"},
        {"timestamp": "2026-03-08T14:01:00Z", "cpu_pct": 67.1, "host": "alpha"},
        {"timestamp": "2026-03-08T14:00:00Z", "cpu_pct": 31.8, "host": "beta"}
      ]
    }
  },
  "id": 1
}
```

petalTongue will infer:
- `timestamp` is temporal → X axis
- `cpu_pct` is numeric → Y axis
- `host` is categorical → color or facet

This is the lowest-effort path. petalTongue applies Tufte constraints automatically.

### 2. Send a Grammar Expression (Recommended)

Specify exactly how your data should be visualized using the Grammar of Graphics:

```json
{
  "jsonrpc": "2.0",
  "method": "visualization.render",
  "params": {
    "data": {"source": "capability:health.metrics", "filter": "last_hour"},
    "variables": [
      {"name": "time", "field": "timestamp", "role": "x"},
      {"name": "value", "field": "cpu_pct", "role": "y"},
      {"name": "host", "field": "primal_id", "role": "facet"}
    ],
    "scales": [
      {"variable": "time", "type": "temporal"},
      {"variable": "value", "type": "linear", "domain": [0, 100]}
    ],
    "geometry": [{"type": "line"}, {"type": "area", "alpha": 0.15}],
    "coordinates": {"type": "cartesian"},
    "facets": {"variable": "host", "layout": "wrap", "columns": 2}
  },
  "id": 1
}
```

This gives you full control over the visual mapping while petalTongue handles
multi-modal rendering and accessibility.

### 3. Stream Data (Real-Time)

For live data (simulation output, health metrics, sensor streams), use the
streaming endpoint:

```json
{
  "jsonrpc": "2.0",
  "method": "visualization.render.stream",
  "params": {
    "grammar": { ... },
    "subscription": {
      "capability": "health.metrics",
      "interval_ms": 1000
    }
  },
  "id": 1
}
```

petalTongue subscribes to your data stream and incrementally updates the
visualization without recompiling the entire grammar.

For high-throughput streams (> 1000 rows/sec), use tarpc with `bytes::Bytes`
payloads for zero-copy transfer. See the tarpc section below.

---

## Grammar Expression Reference

### Data Sources

| Type | Format | Use Case |
|------|--------|----------|
| `inline` | JSON array in the request | Small datasets, one-shot |
| `source` (capability) | `"capability:health.metrics"` | Dynamic discovery |
| `source` (primal) | `"primal:<id>.method"` | Direct primal call (not recommended; use capability) |
| `file` | `"file:///path/to/data.csv"` | Local file |
| `stream` | Streaming subscription | Real-time data |

**Sovereignty rule**: Prefer `"capability:X"` over `"primal:name.method"`.
petalTongue resolves capabilities via Songbird discovery. Never hardcode primal names.

### Variable Roles

| Role | Aesthetic Channel | Notes |
|------|-------------------|-------|
| `x` | Horizontal position | Required for most geometries |
| `y` | Vertical position | Required for most geometries |
| `z` | Depth (3D only) | Requires 3D coordinate system |
| `color` | Hue / categorical color | Automatic palette assignment |
| `fill` | Fill color | For area, bar, tile |
| `size` | Mark size | Area-proportional (Tufte-correct) |
| `shape` | Point shape | Circle, square, triangle, etc. |
| `alpha` | Opacity | 0.0 - 1.0 |
| `label` | Text annotation | Shown on hover or directly |
| `facet` | Small multiples | Splits into panels |
| `pitch` | Audio frequency | For sonification |
| `volume` | Audio amplitude | For sonification |

### Scale Types

| Type | Domain | Notes |
|------|--------|-------|
| `linear` | Numeric | Default for continuous data |
| `log` | Numeric | Logarithmic (specify base) |
| `temporal` | DateTime | Calendar-aware breaks |
| `categorical` | String | Evenly spaced categories |
| `ordinal` | Integer | Rank-order |
| `color_sequential` | Numeric → Color | Single-hue gradient |
| `color_diverging` | Numeric → Color | Two-hue with midpoint |
| `color_qualitative` | Categorical → Color | Distinct colors per category |

### Geometry Types

| Type | Required Roles | Output |
|------|---------------|--------|
| `point` | x, y | Scatter dots |
| `line` | x, y | Connected line |
| `bar` | x, y | Rectangular bars |
| `area` | x, y | Filled area under line |
| `ribbon` | x, ymin, ymax | Filled band (confidence intervals) |
| `text` | x, y, label | Text annotations |
| `tile` | x, y, fill | Heatmap cells |
| `arc` | angle, fill | Pie / donut segments |
| `errorbar` | x, ymin, ymax | Error bars |
| `mesh3d` | x, y, z | 3D mesh (forwarded to GPU) |
| `sphere` | x, y, z, radius | Molecular atoms |
| `cylinder` | x1,y1,z1,x2,y2,z2,radius | Molecular bonds |

### Coordinate Systems

| Type | Dimensions | Notes |
|------|-----------|-------|
| `cartesian` | 2D | Standard X/Y |
| `polar` | 2D | Angle + radius (pie, radar) |
| `perspective` | 3D | Camera with FOV |
| `orthographic` | 3D | No perspective distortion |
| `hierarchical` | N-D | Nested LOD (universe-scale) |

### Faceting

```json
{
  "facets": {
    "variable": "region",
    "layout": "wrap",
    "columns": 3,
    "scales": "fixed"
  }
}
```

- `layout`: `"wrap"` (single variable) or `"grid"` (row + column variables)
- `scales`: `"fixed"` (same axes, enables comparison), `"free"` (independent axes)

---

## IPC Methods

### Methods petalTongue Exposes (Your Primal Calls These)

| Method | Purpose | Params | Returns |
|--------|---------|--------|---------|
| `visualization.render` | Render a grammar expression | `GrammarExpr` | `RenderResult` (panel IDs) |
| `visualization.render.stream` | Streaming visualization | `GrammarExpr` + subscription | `StreamHandle` |
| `visualization.export` | Export to SVG/PNG/JSON | `GrammarExpr` + format | `Bytes` (file content) |
| `visualization.validate` | Check grammar without rendering | `GrammarExpr` | `ValidationResult` (Tufte score) |
| `visualization.capabilities` | What can petalTongue render? | None | `CapabilitySet` |
| `visualization.dismiss` | Remove a rendered visualization | Panel ID | `Ok` |

### Methods petalTongue Calls (Your Primal Exposes These)

petalTongue will call your primal's methods when the grammar references your data
via capability discovery:

| Method | Purpose | Notes |
|--------|---------|-------|
| `{domain}.list` | List available data | Schema discovery |
| `{domain}.get` | Fetch data rows | One-shot fetch |
| `{domain}.subscribe` | Stream data updates | Continuous feed |
| `{domain}.schema` | Describe data columns | Type inference |

Follow `SEMANTIC_METHOD_NAMING_STANDARD.md` for all method names.

### Events petalTongue Emits (Your Primal Subscribes)

When a human interacts with a visualization of your data, petalTongue sends:

```json
{
  "jsonrpc": "2.0",
  "method": "visualization.interact",
  "params": {
    "event": "select",
    "source_capability": "health.metrics",
    "data": {"primal_id": "alpha", "timestamp": "2026-03-08T14:23:00Z"},
    "grammar_id": "health_overview"
  }
}
```

Event types: `select`, `hover`, `brush` (range selection), `zoom`, `dismiss`.

---

## tarpc Integration (High Performance)

For data transfer > 1,000 rows/sec or binary payloads (meshes, images, audio),
use tarpc with `bytes::Bytes`:

```rust
#[tarpc::service]
pub trait VisualizationService {
    async fn render(expr: GrammarExpr, viewport: Viewport) -> RenderResult;
    async fn render_stream(expr: GrammarExpr, viewport: Viewport) -> StreamHandle;
    async fn export(expr: GrammarExpr, format: ExportFormat) -> Bytes;
    async fn validate(expr: GrammarExpr) -> ValidationResult;
    async fn capabilities() -> CapabilitySet;
}
```

petalTongue discovers your tarpc service via capability:
`{"capability": "visualization.render", "transport": "tarpc"}`.

All binary payloads (`Bytes`) are zero-copy over Unix sockets.

---

## barraCuda Integration (GPU Compute)

If your primal produces data that needs heavy computation before visualization
(statistical transforms, 3D tessellation, physics simulation), route the compute
through barraCuda rather than asking petalTongue to do it.

The pipeline:

```
Your Primal (raw data)
    → petalTongue (grammar expression)
    → barraCuda (GPU compute: statistics, projection, tessellation)
    → petalTongue (render the result)
```

petalTongue handles the barraCuda dispatch automatically when the grammar
expression requires computation that exceeds its local capabilities. Your primal
doesn't need to know about barraCuda.

Capabilities petalTongue offloads to barraCuda:

| Capability | Trigger |
|-----------|---------|
| `math.stat.*` | StatDensity, StatSmooth on > 10K rows |
| `math.tessellate.*` | Any 3D geometry (sphere, cylinder, mesh) |
| `math.project.*` | 3D → 2D projection with lighting |
| `math.physics.*` | Simulation steps (N-body, MD, collision) |

---

## Tufte Validation

Every grammar expression is evaluated against Tufte constraints. Your primal
can pre-validate before rendering:

```json
{
  "jsonrpc": "2.0",
  "method": "visualization.validate",
  "params": { "grammar": { ... } },
  "id": 1
}
```

Response includes a score (0.0-1.0) and per-constraint results:

| Constraint | What It Checks |
|------------|---------------|
| `data_ink_ratio` | Proportion of visual elements that carry data |
| `lie_factor` | Whether visual effect matches data effect |
| `chartjunk` | Unnecessary decorative elements |
| `small_multiples` | Suggests faceting over overlaid color |
| `data_density` | Information per unit area |
| `color_accessibility` | Colorblind-safe, redundant encoding |
| `smallest_effective_difference` | Visual weight proportional to need |

Score > 0.75 is good. petalTongue auto-corrects common issues (extends Y-axis
to zero, applies colorblind-safe palette, reduces grid lines) when `auto_correct`
is enabled (default).

---

## Domain-Specific Examples

### biomeOS: Primal Topology

```json
{
  "data": {"source": "capability:orchestration.topology"},
  "variables": [
    {"name": "id", "field": "primal_id", "role": "label"},
    {"name": "health", "field": "health_status", "role": "color"},
    {"name": "connections", "field": "edge_count", "role": "size"}
  ],
  "geometry": [{"type": "point"}, {"type": "line"}],
  "coordinates": {"type": "force_directed"}
}
```

### healthSpring: Patient Vitals

```json
{
  "data": {"source": "capability:health.vitals"},
  "variables": [
    {"name": "time", "field": "timestamp", "role": "x"},
    {"name": "heart_rate", "field": "hr_bpm", "role": "y"},
    {"name": "patient", "field": "patient_id", "role": "facet"}
  ],
  "geometry": [{"type": "line"}, {"type": "ribbon", "ymin": "hr_lower", "ymax": "hr_upper", "alpha": 0.2}],
  "scales": [{"variable": "heart_rate", "type": "linear", "domain": [40, 200]}]
}
```

### barraCuda: Shader Performance

```json
{
  "data": {"source": "capability:math.metrics"},
  "variables": [
    {"name": "shader", "field": "shader_name", "role": "x"},
    {"name": "gflops", "field": "throughput_gflops", "role": "y"},
    {"name": "precision", "field": "fp_mode", "role": "color"}
  ],
  "geometry": [{"type": "bar"}],
  "facets": {"variable": "precision", "layout": "wrap", "columns": 2}
}
```

### ToadStool: GPU Hardware Discovery

```json
{
  "data": {"source": "capability:hardware.gpu.list"},
  "variables": [
    {"name": "adapter", "field": "name", "role": "y"},
    {"name": "vram", "field": "vram_mb", "role": "x"},
    {"name": "driver", "field": "driver_name", "role": "color"},
    {"name": "f64", "field": "f64_support", "role": "shape"}
  ],
  "geometry": [{"type": "point"}],
  "coordinates": {"type": "cartesian"}
}
```

### Molecular Visualization (Future)

```json
{
  "data": {"source": "file:///data/protein.pdb"},
  "variables": [
    {"name": "x", "field": "x_coord", "role": "x"},
    {"name": "y", "field": "y_coord", "role": "y"},
    {"name": "z", "field": "z_coord", "role": "z"},
    {"name": "element", "field": "element", "role": "color"},
    {"name": "radius", "field": "vdw_radius", "role": "size"}
  ],
  "geometry": [{"type": "sphere"}, {"type": "cylinder"}],
  "coordinates": {"type": "perspective", "camera": {"orbit": true}}
}
```

---

## Sovereignty Checklist

Before integrating, confirm your primal follows these rules:

- [ ] Data sources use capability strings, not primal names
- [ ] No hardcoded ports or socket paths in grammar expressions
- [ ] Grammar expressions are JSON-serializable (no closures, no raw pointers)
- [ ] Sensitive data is not embedded in inline grammar expressions (use capability references)
- [ ] Your data methods follow `SEMANTIC_METHOD_NAMING_STANDARD.md`
- [ ] Your tarpc service uses `bytes::Bytes` for binary payloads
- [ ] Your primal announces visualization-relevant capabilities via Songbird

---

## Discovery

petalTongue finds your data via capability-based discovery. Announce your
capabilities through Songbird:

```json
{
  "jsonrpc": "2.0",
  "method": "discovery.announce",
  "params": {
    "capabilities": ["health.metrics", "health.vitals"],
    "transport": ["jsonrpc", "tarpc"],
    "schema_endpoint": "health.schema"
  }
}
```

petalTongue queries:

```json
{"method": "discovery.query", "params": {"capability": "health.metrics"}}
```

And receives your socket path and transport type. No hardcoded names.

---

## Related Documents

| Document | Location | Purpose |
|----------|----------|---------|
| Grammar of Graphics Architecture | `petalTongue/specs/GRAMMAR_OF_GRAPHICS_ARCHITECTURE.md` | Full grammar type system |
| Universal Visualization Pipeline | `petalTongue/specs/UNIVERSAL_VISUALIZATION_PIPELINE.md` | End-to-end pipeline spec |
| Tufte Constraint System | `petalTongue/specs/TUFTE_CONSTRAINT_SYSTEM.md` | Visualization quality constraints |
| Semantic Method Naming | `wateringHole/SEMANTIC_METHOD_NAMING_STANDARD.md` | IPC method names |
| Universal IPC Standard V3 | `wateringHole/UNIVERSAL_IPC_STANDARD_V3.md` | Transport protocol |
| biomeOS API Specification | `wateringHole/petaltongue/BIOMEOS_API_SPECIFICATION.md` | biomeOS integration |
