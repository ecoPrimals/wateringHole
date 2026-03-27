# petalTongue v1.6.0 — Spring Schema Evolution Handoff

**Date**: March 10, 2026
**From**: petalTongue
**Version**: 1.6.0
**Tests**: 2,025 passing

---

## Summary

Spring-driven schema evolution: new data binding variants, axis labels, IPC aliases,
real geometry implementations, threshold-based coloring, and faceting support.

## Changes

### P0 — Schema Alignment

- **DataBinding::Scatter (2D)**: New variant for wetSpring PCoA/UMAP ordinations
  with `x`, `y`, `point_labels`, `x_label`, `y_label`. Compiles to `GeometryType::Point`.
- **Scatter3D axis labels**: `x_label`, `y_label`, `z_label` fields with `#[serde(default)]`
  for backward-compatible deserialization.
- **IPC method aliases**: `visualization.interact.subscribe/poll/unsubscribe` now alias
  to `interaction.subscribe/poll/unsubscribe` (wetSpring naming compatibility).

### P1 — Threshold Coloring & Faceting

- **ThresholdRange cell coloring**: `DataBindingCompiler::compile_with_thresholds()`
  injects threshold status (normal/warning/critical) into Heatmap/FieldMap data rows.
  Tile geometry renders cells using domain palette status colors.
- **Facet wrap (small multiples)**: `GrammarCompiler::compile_faceted()` partitions data
  by facet variable, compiles each group, and arranges panels in a wrapped grid layout.

### P2 — Geometry Implementations

- **Tile geometry**: Real heatmap/fieldmap rendering in the grammar compiler. Each data
  row becomes a filled, color-mapped rectangle. Grid dimensions inferred from unique x/y values.
- **Arc geometry**: Semi-circular gauge rendering. Background arc + filled arc proportional
  to normalized value. Gauge DataBinding now compiles to Arc (was Bar).

## IPC Methods Added/Changed

| Method | Change |
|--------|--------|
| `visualization.interact.subscribe` | New alias for `interaction.subscribe` |
| `visualization.interact.poll` | New alias for `interaction.poll` |
| `visualization.interact.unsubscribe` | New alias for `interaction.unsubscribe` |

## DataBinding Schema

```text
TimeSeries, Distribution, Bar, Gauge, Spectrum, Heatmap, Scatter, Scatter3D, FieldMap
```

9 variants, all auto-compiled to Grammar of Graphics via `DataBindingCompiler`.

## For Springs

- **wetSpring**: Scatter 2D ready for PCoA/UMAP ordinations. Interaction method aliases active.
- **neuralSpring**: ThresholdRange coloring on heatmap cells available via `compile_with_thresholds()`.
  Facet wrap available via `compile_faceted()` for small multiples.
- **healthSpring**: Gauge now renders as a proper semicircular arc.
- **All springs**: Scatter3D can now carry axis labels for dimensional annotations.
